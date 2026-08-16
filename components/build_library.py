#!/usr/bin/env python3
"""Build the component library page, in two forms.

  components/index.html   LINKS ../foundations/*.css — no snapshot, always current
  dist/component-library.html   embeds everything, for sending to someone

Both carry an nc-build-stamp naming the digest of every source they were built
from, so checks/check_stamps.py can fail on divergence (ch18). The linked form
cannot go stale by construction; the dist form can, which is why it is stamped.

Content lives in components/library.body.html — edit that, not this script.

    python3 components/build_library.py
"""
import hashlib, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
F = ROOT / "foundations"
def d(p): return hashlib.sha256(p.read_bytes()).hexdigest()[:16]

body     = (ROOT / "components" / "library.body.html").read_text()
scaffold = (ROOT / "components" / "library.scaffold.css").read_text()
css      = (F / "nightlife-culture.css")
fonts    = (F / "fonts.css")
stamp = ";".join(f"{k}:{d(p)}" for k, p in
                 [("tokens", F/"tokens.json"), ("rules", F/"rules.json"),
                  ("css", css), ("fonts", fonts)] if p.exists())

HEAD = """<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Nightlife Culture — component library v1.0</title>
<meta name="nc-source" content="Nightlife Culture Style Guide v1.4">
<meta name="nc-build-stamp" content="{stamp}">
{styles}
</head><body class="nc-doc">
{body}
</div></body></html>
"""

# 1 · repo form — links the stylesheets. Cannot carry a stale copy.
(ROOT / "components" / "index.html").write_text(HEAD.format(
    stamp=stamp, body=body,
    styles='<link rel="stylesheet" href="../foundations/fonts.css">\n'
           '<link rel="stylesheet" href="../foundations/nightlife-culture.css">\n'
           '<link rel="stylesheet" href="library.scaffold.css">'))

# 2 · dist form — self-contained, for sending
(ROOT / "dist").mkdir(exist_ok=True)
(ROOT / "dist" / "component-library.html").write_text(HEAD.format(
    stamp=stamp, body=body,
    styles=f"<style>\n{fonts.read_text()}\n{css.read_text()}\n{scaffold}\n</style>"))

print(f"wrote components/index.html          linked, {len(body):,} chars of content")
print(f"wrote dist/component-library.html    self-contained")
print(f"stamp: {stamp}")
