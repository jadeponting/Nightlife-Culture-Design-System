#!/usr/bin/env python3
"""Audit every component named in the reference files against the codebase.

  docs/what-we-have.html   LINKS ../foundations/*.css — always current
  dist/what-we-have.html   embeds everything, for sending to someone

The inventory of what the reference files contain is docs/reference-inventory.json
— a SOURCE file, edit that. Everything else on the page is CHECKED, not asserted:
each class is looked up in the generated CSS, each rule id in rules.json, and each
component is tested against the router. A claim that is not true fails here.

    python3 docs/build_audit.py

NC-SYS-06 — render the decision rather than describing it. This page is
generated from the system it describes, so it cannot claim behaviour the
system does not have.
"""
import hashlib, html as H, json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "components"))
import route
F = ROOT / "foundations"
def dig(p): return hashlib.sha256(p.read_bytes()).hexdigest()[:16]
def esc(s): return H.escape(str(s))

sys.path.insert(0, str(ROOT / "docs"))
import status as ST
CSS, RULES, SELECTORS = ST.CSS_RAW, ST.RULES, ST.SELECTORS
has_class, enforced = ST.has_class, ST.enforced
INV = json.loads((ROOT / "docs" / "reference-inventory.json").read_text())
SRC = INV["sources"]

# What the router can actually produce, end to end. NOT a list I typed — the router
# is run, and the classes in the markup it hands back are read off the output. If a
# router stops emitting a component, this page stops claiming it.
ROUTED = {}
for _tag, _title, _d in route.run_examples():
    if _d.blocked or not _d.html:
        continue
    for _el, _cl in re.findall(r'<(\w+)[^>]*class="([^"]+)"', _d.html):
        parts = _cl.split()
        base = "." + parts[0]
        ROUTED.setdefault(base, set()).add(_d.kind)
        for _p in parts[1:]:
            ROUTED.setdefault(f"{base} .{_p}", set())
# nested spans carry their own classes; walk them against their parent block
for _tag, _title, _d in route.run_examples():
    if _d.blocked or not _d.html: continue
    m = re.match(r'<\w+[^>]*class="([^"]+)"', _d.html.strip())
    if not m: continue
    root = "." + m.group(1).split()[0]
    for _cl in re.findall(r'class="([^"]+)"', _d.html)[1:]:
        ROUTED.setdefault(f"{root} .{_cl.split()[0]}", set()).add(_d.kind)
ROUTED = {k: ("the router" if not v else "the router") for k, v in ROUTED.items()}

# Where a rule is enforced by a script rather than expressed as a class.
# Verified: the named file must exist AND mention the rule id.
def enforced(it):
    out = []
    for chk in it.get("enforced_by", []):
        f = ROOT / chk
        if not f.exists(): continue
        txt = f.read_text()
        if all(r in txt for r in it.get("rules", [])) or not it.get("rules"):
            out.append(chk.split("/")[-1])
    return out

status = ST.state

rows, tally = [], {"ok": 0, "flag": 0, "gap": 0}
for fam in INV["families"]:
    body = []
    for it in fam["items"]:
        label, kind = status(it)
        tally[kind] += 1
        srcs = " · ".join(SRC.get(s, s).split(" — ")[0] for s in it["src"]) or "—"
        cls  = ", ".join(it.get("class", [])) or "—"
        rls  = ", ".join(it.get("rules", [])) or "—"
        # Only claim the router when the component's PRIMARY class is one the router
        # emits. A row listing three classes of which one happens to be routable is
        # not "produced by the router", and saying so would be the kind of soft
        # overclaim this whole page exists to catch.
        prim = (it.get("class") or [None])[0]
        rt   = ["produced by the router"] if prim in ROUTED else []
        rt  += ["checked by " + c for c in sorted(enforced(it))]
        chip = {"ok":"nc-prov","flag":"nc-prov nc-prov--mid","gap":"nc-prov nc-prov--low"}[kind]
        made = ('<br><span>' + esc(" \u00b7 ".join(rt)) + "</span>") if rt else ""
        body.append(
          "<tr><td>" + esc(it["n"]) + made + "</td>"
          '<td>' + esc(srcs) + "</td>"
          '<td class="nc-code">' + esc(cls) + '</td><td class="nc-code">' + esc(rls) + "</td>"
          '<td><span class="' + chip + '">' + esc(label) + "</span></td></tr>")
    n_ok = sum(1 for it in fam["items"] if status(it)[1] == "ok")
    rows.append(
      f'<h3 class="nc-heading-3">{esc(fam["name"])}'
      f' <span>{n_ok} of {len(fam["items"])} complete</span></h3>'
      '<div><table class="nc-table"><thead><tr>'
      '<th>Component or style</th><th>Named in</th><th>In the codebase as</th>'
      '<th>Logic</th><th>Status</th></tr></thead><tbody>'
      + "\n".join(body) + "</tbody></table></div>")

TOTAL = sum(tally.values())
SCORE = (f'<div class="nc-g3">'
  f'<div class="nc-stat nc-stat--top acc-teal"><p class="big">{tally["ok"]}</p>'
  f'<p class="lb">Built, with the rule attached</p>'
  f'<p class="src">The component exists in the stylesheet and the reason it exists is recorded.</p></div>'
  f'<div class="nc-stat nc-stat--top acc-butter"><p class="big">{tally["flag"]}</p>'
  f'<p class="lb">Half there</p>'
  f'<p class="src">Either styled with no rule behind it, or ruled and never built.</p></div>'
  f'<div class="nc-stat nc-stat--top acc-coral"><p class="big">{tally["gap"]}</p>'
  f'<p class="lb">Not in the codebase</p>'
  f'<p class="src">Named in your reference files and nowhere else yet.</p></div></div>')

# --- what the codebase has that no reference asked for -------------------
declared = set()
for fam in INV["families"]:
    for it in fam["items"]:
        for c in it.get("class", []):
            declared.add(c)                 # ".nc-quote .q"
            declared.add(c.split()[0])      # ".nc-quote"
# every top-level nc- class the stylesheet defines
incss = {f".{m}" for m in re.findall(r"^\.(nc-[a-z0-9-]+)", CSS, re.M)}
extra = sorted(incss - declared)
EXTRA = ("<p>Everything in the stylesheet traces back to a reference file.</p>"
         if not extra else
         '<p>In the stylesheet, not asked for by any reference file — each one needs a '
         'reason recorded or removing:</p><p class="nc-code">' + esc(", ".join(extra)) + "</p>")

# --- rules with no component ---------------------------------------------
used = {r for fam in INV["families"] for it in fam["items"] for r in it.get("rules", [])}
orphan = sorted(set(RULES) - used)
ORPH = ("<p>Every rule is attached to something on this page.</p>" if not orphan else
        '<p>Rules in the rule set that no component on this page claims. Most govern '
        'process rather than appearance, which is fine — but each should be able to name '
        'what enforces it:</p><ul class="nc-list">' +
        "".join(f'<li><b>{esc(r)}</b> — {esc(RULES[r]["rule"][:150])}</li>' for r in orphan) +
        "</ul>")

body = (ROOT / "docs" / "audit.body.html").read_text()
for k, v in [("{{SCORE}}", SCORE),
             ("{{ROWS}}", "\n".join(rows)),
             ("{{EXTRA}}", EXTRA),
             ("{{ORPHAN}}", ORPH),
             ("{{TOTAL}}", str(TOTAL)),
             ("{{FILES}}", str(len(SRC)))]:
    if k not in body:
        continue          # the masthead placeholders moved into the page builder
    body = body.replace(k, v)
sys.path.insert(0, str(ROOT / "docs"))
from sheet import page

page(name="what-we-have", folder="docs",
     kicker="Nightlife Culture · design system",
     title="What we have, and what is missing",
     stand="Every component and style named across your reference files, checked one by one against the codebase. Not a summary — a test.",
     body=body)
print(f"{TOTAL} components audited — {tally['ok']} complete · {tally['flag']} half · {tally['gap']} missing")
print(f"orphan rules: {len(orphan)} · undeclared classes: {len(extra)}")
