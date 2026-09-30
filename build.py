#!/usr/bin/env python3
"""Build the whole design system. One command, stdlib only.

    python3 build.py

  1  fonts    assets/fonts/*.woff2  ->  foundations/fonts.css
  2  css      foundations/tokens.json -> foundations/nightlife-culture.css
  3  library  components/library.body.html -> components/index.html + dist/
  3b docs     runs the router -> docs/how-the-logic-works.html + dist/
  3c audit    checks every reference component -> docs/what-we-have.html + dist/
  3d plan     sorts what is left -> docs/the-build-order.html + dist/
  3e decks    decks/*.json -> decks/<name>.html + dist/, from the slide blocks
  3f patterns foundations/patterns.json + reference/ -> layouts/slide-patterns.html + dist/
  4  validate every HTML artefact against foundations/rules.json
  5  coverage every class defined is shown somewhere, and every class used is defined
  6  contrast rendered text contrast, and slide fit (NC-LAY-07), in a real browser
  7  stamps   every derived artefact against its source digests

Nothing in foundations/ or components/index.html is hand-edited. Edit
tokens.json, rules.json or library.body.html, then run this.
"""
import subprocess, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent
STEPS = [
    ("fonts",    [sys.executable, "checks/build_fonts.py"]),
    ("css",      [sys.executable, "checks/build.py"]),
    ("slides",   [sys.executable, "checks/build_slides.py"]),
    ("library",  [sys.executable, "components/build_library.py"]),
    ("docs",     [sys.executable, "docs/build_routing.py"]),
    ("audit",    [sys.executable, "docs/build_audit.py"]),
    ("plan",     [sys.executable, "docs/build_plan.py"]),
    ("decks",    [sys.executable, "decks/build_deck.py"]),
    ("patterns", [sys.executable, "layouts/build_patterns.py"]),
    # The skill is a derived artefact like any other. Outside the pipeline it
    # was regenerated only when someone remembered — the exact staleness the
    # design-decisions skill taught us about. In the pipeline, drift fails.
    ("skill",    [sys.executable, "adapters/skill/build_skill.py"]),
]
fail = 0
unmeasured = False
for name, cmd in STEPS:
    print(f"\n=== {name} " + "=" * (56 - len(name)), flush=True)
    r = subprocess.run(cmd, cwd=ROOT)
    if r.returncode: fail = 1; print(f"  !! {name} failed"); break

if not fail:
    html = sorted(str(p.relative_to(ROOT)) for p in
                  list(ROOT.glob("components/*.html")) + list(ROOT.glob("docs/*.html"))
                  + list(ROOT.glob("layouts/*.html")) + list(ROOT.glob("decks/*.html"))
                  + list(ROOT.glob("dist/*.html"))
                  if not p.name.endswith((".body.html", ".part.html")))
    print("\n=== validate " + "=" * 51, flush=True)
    fail |= subprocess.run([sys.executable, "checks/validate.py", *html], cwd=ROOT).returncode
    print("\n=== coverage " + "=" * 51, flush=True)
    fail |= subprocess.run([sys.executable, "checks/check_coverage.py"], cwd=ROOT).returncode
    print("\n=== contrast " + "=" * 51, flush=True)
    rc = subprocess.run([sys.executable, "checks/check_contrast.py"], cwd=ROOT).returncode
    unmeasured = rc == 3          # skipped: not a pass and not a fail, and it says so
    if not unmeasured: fail |= rc
    print("\n=== stamps " + "=" * 53, flush=True)
    fail |= subprocess.run([sys.executable, "checks/check_stamps.py"], cwd=ROOT).returncode

print("\n" + ("BUILD FAILED" if fail else
              "BUILD OK — but rendered contrast was NOT measured (playwright missing)" if unmeasured
              else "BUILD OK — everything current"), flush=True)
sys.exit(fail)
