#!/usr/bin/env python3
"""Every class the stylesheets define must be shown somewhere you can look at it.

    python3 checks/check_coverage.py

The component library used to be the one hand-authored thing in a generated
chain, and it drifted: 91 classes defined, 48 demonstrated. The stamp check
could not see it, because the stamp compares digests of SOURCES and the library
body IS a source. So a component could exist, be correct, be validated — and be
invisible to the person who has to choose it.

A component nobody can see is a component nobody will use, and the system was
built on 'show, do not describe'. This makes that a check.

Two surfaces demonstrate: components/library.body.html for the document layer,
layouts/index.html for the slide layer. A class shown in either passes.
"""
import pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
F = ROOT / "foundations"

css = "\n".join((F / f).read_text() for f in
                ("nightlife-culture.css", "nightlife-slides.css") if (F / f).exists())
css = re.sub(r"/\*.*?\*/", " ", css, flags=re.S)
defined = {m for m in re.findall(r"\.(nc-[a-z0-9-]+)", css)} | \
          {m for m in re.findall(r"\.(ground-[a-z]+|acc-[a-z]+)", css)}

# Read the BUILT pages, not the source bodies. Some classes are added by the
# build itself — the markup disclosure under each specimen is generated, not
# typed — and a check that reads the source cannot see them. What matters is
# what renders, so that is what is counted.
SURFACES = ["components/index.html", "layouts/index.html"]
shown = set()
for f in SURFACES:
    p = ROOT / f
    if p.exists():
        shown |= {c for a in re.findall(r'class="([^"]*)"', p.read_text()) for c in a.split()}

# NC-PAG-02 — a sheet never carries its own stylesheet. Five of them existed,
# they disagreed, and the disagreement is what the reviewer kept finding. The
# page builder at docs/sheet.py is the only place page furniture is decided.
strays = sorted(p.relative_to(ROOT).as_posix()
                for d in ("docs", "components", "layouts", "adapters")
                for p in (ROOT / d).glob("*.css") if (ROOT / d).exists())
if strays:
    print("\n  per-sheet stylesheets found — page furniture is a component (NC-PAG-02):")
    for f in strays:
        print(f"    {f}")
    sys.exit(1)

missing = sorted(defined - shown)
print(f"{len(defined)} classes defined · {len(defined) - len(missing)} demonstrated")
if missing:
    print(f"\n  {len(missing)} defined and shown nowhere:")
    for c in missing:
        print(f"    .{c}")
    print("\n  Add a specimen to components/library.body.html, or delete the class.")
    sys.exit(1)
print("  every component has somewhere you can look at it")
