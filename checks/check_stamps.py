#!/usr/bin/env python3
"""Fail if any derived artefact was built from a source that has since moved.

Ch18: "A design system gets copied into things... none of them has any way to
notice the source has moved." Three rules close it:
  1. every derived artefact states the source version it was built from
  2. a CHECK compares the two and fails on divergence — not a reminder
  3. nothing derived asserts its settledness without naming its version

This is rule 2. The defect is invisible by construction: the derived artefact
is internally consistent while applying superseded rules.

    python3 checks/check_stamps.py
"""
import hashlib, pathlib, re, sys, json
ROOT = pathlib.Path(__file__).resolve().parent.parent

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]

SOURCES = {
    "tokens":  ROOT / "foundations" / "tokens.json",
    "rules":   ROOT / "foundations" / "rules.json",
    "css":     ROOT / "foundations" / "nightlife-culture.css",
    "fonts":   ROOT / "foundations" / "fonts.css",
    "slides":  ROOT / "foundations" / "nightlife-slides.css",
}
live = {k: digest(p) for k, p in SOURCES.items() if p.exists()}

# *.body.html and *.part.html are SOURCE fragments, not derived artefacts.
derived = sorted(p for p in (list(ROOT.glob("components/*.html")) + list(ROOT.glob("docs/*.html"))
                 + list(ROOT.glob("layouts/*.html"))
                 + list(ROOT.glob("dist/*.html"))
                 + list(ROOT.glob("adapters/**/*.html")))
                 if not p.name.endswith((".body.html", ".part.html")))
fails, checked = [], 0
for d in derived:
    txt = d.read_text(errors="replace")
    m = re.search(r'nc-build-stamp"\s+content="([^"]+)"', txt)
    if not m:
        fails.append((d, "no build stamp — cannot establish what it was built from")); continue
    checked += 1
    stamped = dict(kv.split(":", 1) for kv in m.group(1).split(";") if ":" in kv)
    for k, v in stamped.items():
        if k in live and live[k] != v:
            fails.append((d, f"{k} stamped {v}, source is now {live[k]}"))

print(f"sources: " + " · ".join(f"{k} {v}" for k, v in sorted(live.items())))
print(f"derived artefacts: {len(derived)} found, {checked} stamped\n")
for d, why in fails:
    print(f"  STALE  {d.relative_to(ROOT)}\n         {why}")
if not fails:
    print("  all derived artefacts current")
print(f"\n{len(fails)} divergence(s)")
sys.exit(1 if fails else 0)
