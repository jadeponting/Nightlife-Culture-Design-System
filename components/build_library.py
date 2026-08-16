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
