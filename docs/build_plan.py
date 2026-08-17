#!/usr/bin/env python3
"""Turn the audit into a build order.

  docs/the-build-order.html   LINKS ../foundations/*.css — always current
  dist/the-build-order.html   self-contained, for sending

The plan is not written separately from the audit — it IS the audit, sorted.
Every item here is one the audit found incomplete, and the moment it passes
the audit it disappears from this page. So the plan cannot claim work that
is done, and cannot quietly drop work that is not.

    python3 docs/build_plan.py

NC-SYS-06 — render the decision rather than describing it. This page is
generated from the system it describes, so it cannot claim behaviour the
system does not have.
"""
import hashlib, html as H, json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
F = ROOT / "foundations"
def dig(p): return hashlib.sha256(p.read_bytes()).hexdigest()[:16]
def esc(s): return H.escape(str(s))

sys.path.insert(0, str(ROOT/"docs"))
import status as ST
INV   = json.loads((ROOT/"docs"/"reference-inventory.json").read_text())
RULES = ST.RULES
SRC   = INV["sources"]

WAVES = [
 (1, "Finish what is already standing",
  "Eight components that exist and work, with no rule saying why. Nothing here needs a "
  "design decision — the shape is settled, the reason just was never written down. A "
  "component with no rule is a habit: it survives as long as someone remembers it, and "
  "no longer.", "acc-teal"),
 (2, "Complete the chart and evidence set",
  "Four chart forms and four pieces of evidence furniture that charts v1.4 and the style "
  "guide specify and the codebase does not have. Nothing to decide — the specification "
  "already exists in your own files. Until they are built, anyone needing one reaches "
  "outside the system, and that is how a system starts to leak.", "acc-blue"),
 (3, "Give every authoring rule a home",
  "Rules that exist and nothing enforces, plus rules the reference files state and the "
  "rule set never captured. Each one gets either a check that fails the build, or an "
  "honest note that it is a human step. A rule with neither is a rule that will quietly "
  "stop being true.", "acc-violet"),
 (4, "The slide layer",
  "The hole. Twelve layouts exist as working markup in slide layouts v1.0 and in the "
  "repo's older folder, but nothing generates them from the tokens, so nothing checks "
  "them — the last place a hand-set value can hide. This wave is blocked on one decision "
  "of yours: the grid geometry.", "acc-butter"),
 (5, "The remaining surfaces",
  "The nine HTML elements the browser will style whether or not we decide, and the table "
  "variants. Low glamour, high frequency — and unstyled is still a look.", "acc-pink"),
]

# Completeness is asked fresh, not read off a stored flag. An item tagged into
# a wave that has since been finished drops out here on its own — the plan
# cannot go on listing work the audit already counts as done.
allit  = [(it, fam["name"]) for fam in INV["families"] for it in fam["items"]]
items  = [(it, f) for it, f in allit if not ST.done(it)]
done_n = len(allit) - len(items)
total  = len(allit)
for it, _ in items:
    it.setdefault("wave", 3)
    it["done"] = ST.todo_note(it)

blocks = []
for num, title, why, acc in WAVES:
    mine = [(it, f) for it, f in items if it["wave"] == num]
    rows = "\n".join(
      '<tr><td>' + esc(it["n"]) + '</td>'
      '<td>' + esc(f) + '</td>'
      '<td class="nc-code">' + esc(", ".join(it.get("rules", [])) or "—") + '</td>'
      '<td>' + esc(it["done"]) + '</td>'
      '<td>' + esc(" · ".join(SRC.get(s, s).split(" — ")[0] for s in it["src"]) or "—")
      + "</td></tr>" for it, f in mine)
    blocks.append(
      f'<div class="nc-panel nc-panel--top {acc}">'
      f'<p class="lab">Wave {num} · {len(mine)} items</p>'
      f'<p>{esc(title)}</p><p class="txt">{esc(why)}</p></div>'
      '<div><table class="nc-table"><thead><tr>'
      '<th>What</th><th>Family</th><th>Rule</th><th>What done means</th><th>Named in</th>'
      "</tr></thead><tbody>" + rows + "</tbody></table></div>")

BARS = "\n".join(
  f'<div class="nc-bar"><span class="lb">Wave {n}</span>'
  f'<span class="tk"><span class="fl" style="width:{len([1 for it,_ in items if it["wave"]==n])/max(len(items),1)*100:.0f}%"></span></span>'
  f'<span class="vl">{len([1 for it,_ in items if it["wave"]==n])}</span></div>'
  for n, *_ in WAVES)

SCORE = (
 f'<div class="nc-g2">'
 f'<div class="nc-stat nc-stat--top acc-teal"><p class="big">{done_n}</p>'
 f'<p class="lb">Complete</p><p class="src">Built, with the rule attached — or ruled '
 f'and enforced by a check that fails the build.</p></div>'
 f'<div class="nc-stat nc-stat--top acc-coral"><p class="big">{len(items)}</p>'
 f'<p class="lb">Left to build</p><p class="src">Everything below. Ordered so that '
 f'nothing waits on a decision that has not been made.</p></div></div>')

body = (ROOT/"docs"/"plan.body.html").read_text()
for k, v in [("{{SCORE}}", SCORE),
             ("{{BARS}}", BARS),
             ("{{WAVES}}", "\n".join(blocks)),
             ("{{TOTAL}}", str(total)),
             ("{{LEFT}}", str(len(items)))]:
    if k not in body:
        continue          # the masthead placeholders moved into the page builder
    body = body.replace(k, v)
sys.path.insert(0, str(ROOT / "docs"))
from sheet import page

page(name="the-build-order", folder="docs",
     kicker="Nightlife Culture · design system",
     title="The build order",
     stand="This page is the audit, sorted. The moment something passes it disappears from here, so the plan cannot claim work that is done or drop work that is not.",
     body=body)
print(f"build order: {done_n} of {total} complete · {len(items)} to go")
for n, t, *_ in WAVES:
    print(f"  wave {n}  {len([1 for it,_ in items if it['wave']==n]):>3}  {t}")
