#!/usr/bin/env python3
"""Turn the audit into a build order.

  docs/the-build-order.html   LINKS ../foundations/*.css — always current
  dist/the-build-order.html   self-contained, for sending

The plan is not written separately from the audit — it IS the audit, sorted.
Every item here is one the audit found incomplete, and the moment it passes
the audit it disappears from this page. So the plan cannot claim work that
is done, and cannot quietly drop work that is not.

    python3 docs/build_plan.py
"""
import hashlib, html as H, json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
F = ROOT / "foundations"
def dig(p): return hashlib.sha256(p.read_bytes()).hexdigest()[:16]
def esc(s): return H.escape(str(s))

INV   = json.loads((ROOT/"docs"/"reference-inventory.json").read_text())
RULES = {r["id"]: r for r in json.loads((F/"rules.json").read_text())["rules"]}
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

items = [(it, fam["name"]) for fam in INV["families"] for it in fam["items"] if "wave" in it]
done_n = sum(1 for fam in INV["families"] for it in fam["items"] if "wave" not in it)
total  = done_n + len(items)

blocks = []
for num, title, why, acc in WAVES:
    mine = [(it, f) for it, f in items if it["wave"] == num]
    rows = "\n".join(
      '<tr><td class="nm">' + esc(it["n"]) + '</td>'
      '<td class="sr">' + esc(f) + '</td>'
      '<td class="cd">' + esc(", ".join(it.get("rules", [])) or "—") + '</td>'
      '<td class="wt">' + esc(it["done"]) + '</td>'
      '<td class="sr">' + esc(" · ".join(SRC.get(s, s).split(" — ")[0] for s in it["src"]) or "—")
      + "</td></tr>" for it, f in mine)
    blocks.append(
      f'<div class="nc-panel nc-panel--top {acc} wv">'
      f'<p class="lab">Wave {num} · {len(mine)} items</p>'
      f'<p class="wt-t">{esc(title)}</p><p class="txt">{esc(why)}</p></div>'
      '<div class="tw"><table class="nc-table"><thead><tr>'
      '<th>What</th><th>Family</th><th>Rule</th><th>What done means</th><th>Named in</th>'
      "</tr></thead><tbody>" + rows + "</tbody></table></div>")

BARS = "\n".join(
  f'<div class="nc-bar"><span class="lb">Wave {n}</span>'
  f'<span class="tk"><span class="fl" style="width:{len([1 for it,_ in items if it["wave"]==n])/max(len(items),1)*100:.0f}%"></span></span>'
  f'<span class="vl">{len([1 for it,_ in items if it["wave"]==n])}</span></div>'
  for n, *_ in WAVES)

SCORE = (
 f'<div class="g2">'
 f'<div class="nc-stat nc-stat--top acc-teal"><p class="big">{done_n}</p>'
 f'<p class="lb">Complete</p><p class="src">Built, with the rule attached — or ruled '
 f'and enforced by a check that fails the build.</p></div>'
 f'<div class="nc-stat nc-stat--top acc-coral"><p class="big">{len(items)}</p>'
 f'<p class="lb">Left to build</p><p class="src">Everything below. Ordered so that '
 f'nothing waits on a decision that has not been made.</p></div></div>')

body = (ROOT/"docs"/"plan.body.html").read_text()
for k, v in [("{{SCORE}}", SCORE), ("{{BARS}}", BARS), ("{{WAVES}}", "\n".join(blocks)),
             ("{{TOTAL}}", str(total)), ("{{LEFT}}", str(len(items)))]:
    assert k in body, f"placeholder {k} missing — refusing to write silently"
    body = body.replace(k, v)

scaffold = (ROOT/"docs"/"plan.scaffold.css").read_text()
css, fonts = F/"nightlife-culture.css", F/"fonts.css"
stamp = ";".join(f"{k}:{dig(p)}" for k, p in
                 [("tokens", F/"tokens.json"), ("rules", F/"rules.json"),
                  ("css", css), ("fonts", fonts)] if p.exists())
HEAD = """<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Nightlife Culture — the build order</title>
<meta name="nc-source" content="Nightlife Culture Style Guide v1.4">
<meta name="nc-build-stamp" content="{stamp}">
{styles}
</head><body class="nc-doc">
{body}
</body></html>
"""
(ROOT/"docs"/"the-build-order.html").write_text(HEAD.format(stamp=stamp, body=body,
  styles='<link rel="stylesheet" href="../foundations/fonts.css">\n'
         '<link rel="stylesheet" href="../foundations/nightlife-culture.css">\n'
         '<link rel="stylesheet" href="plan.scaffold.css">'))
(ROOT/"dist").mkdir(exist_ok=True)
(ROOT/"dist"/"the-build-order.html").write_text(HEAD.format(stamp=stamp, body=body,
  styles=f"<style>\n{fonts.read_text()}\n{css.read_text()}\n{scaffold}\n</style>"))
print(f"build order: {done_n} of {total} complete · {len(items)} to go")
for n, t, *_ in WAVES:
    print(f"  wave {n}  {len([1 for it,_ in items if it['wave']==n]):>3}  {t}")
