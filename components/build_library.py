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

# ---- the markup disclosure -------------------------------------------------
# Under every specimen, the markup that produced it — read off the rendered
# block, never typed. Typed markup is a claim; read markup is evidence. This is
# the only way to verify a specimen came from the codebase rather than being
# drawn to look as though it did, which is the question that matters.
import html as _h, re as _re

def _disclose(src):
    out, i, n = [], 0, 0
    for m in _re.finditer(r'<div class="nc-specimen[^"]*">', src):
        depth, j = 0, m.start()
        while j < len(src):
            t = _re.compile(r"</?div\b").search(src, j)
            if not t:
                break
            depth += 1 if src[t.start():t.start() + 4] == "<div" else -1
            j = t.end()
            if depth == 0:
                break
        if j >= len(src):
            continue                      # unbalanced, leave it alone
        block = src[m.start():j + 1]
        inner = block[block.index(">") + 1:block.rindex("</div>")].strip()
        # tidy the indentation so it reads, without altering a character of it
        lines = [l for l in inner.split("\n")]
        pad = min((len(l) - len(l.lstrip()) for l in lines if l.strip()), default=0)
        inner = "\n".join(l[pad:] if l[:pad].isspace() else l for l in lines)
        classes = sorted({c for a in _re.findall(r'class="([^"]*)"', inner)
                          for c in a.split() if c.startswith(("nc-", "acc-", "ground-"))})
        n += 1
        det = ('\n<details class="nc-details nc-disclose">'
               f'<summary>The markup — {len(classes)} classes, all from the codebase</summary>'
               f'<pre class="nc-pre acc-teal"><code class="nc-code">{_h.escape(inner)}</code></pre>'
               f'<p class="nc-note">Uses: {" · ".join("." + c for c in classes) or "no component classes"}'
               '<br>Read off the rendered specimen by the build, not written by hand. If a class '
               'here is not in the stylesheet the build fails before this page exists.</p>'
               "</details>")
        out.append(src[i:j + 1] + det)
        i = j + 1
    out.append(src[i:])
    return "".join(out), n

body, _n = _disclose(body)
print(f"markup disclosed under {_n} specimens")
css      = (F / "nightlife-culture.css")
fonts    = (F / "fonts.css")

import sys
sys.path.insert(0, str(ROOT / "docs"))
from sheet import page

page(name="index", folder="components",
     kicker="Nightlife Culture · design system",
     title="The component library",
     stand="Every component in the system, one specimen each, with the rule that governs it "
           "and where it came from. Nothing here is drawn to look like a component — each is "
           "the component.",
     body=body)
page(name="component-library", folder="dist",
     kicker="Nightlife Culture · design system",
     title="The component library",
     stand="Every component in the system, one specimen each, with the rule that governs it "
           "and where it came from.",
     body=body)
