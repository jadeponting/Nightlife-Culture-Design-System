#!/usr/bin/env python3
"""Build every deck in decks/*.json from the slide blocks.

    decks/<name>.html   links foundations/ — cannot go stale
    dist/<name>.html    self-contained, for sending

A deck is content only. Every slide names a pattern from
foundations/patterns.json; an unknown pattern fails the build, because a
pattern nobody registered is a layout somebody invented (NC-LAY-08).
"""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "layouts")); sys.path.insert(0, str(ROOT / "docs"))
from render import slide
from sheet import page

known = set(json.loads((ROOT / "foundations" / "patterns.json").read_text())["patterns"])
fail = 0
for f in sorted((ROOT / "decks").glob("*.json")):
    d = json.loads(f.read_text())
    bad = [s["n"] for s in d["slides"] if s["pattern"] not in known]
    if bad:
        print(f"  !! {f.name}: slides {bad} name a pattern that is not in foundations/patterns.json")
        fail = 1; continue
    body = '<div class="nc-sdeck">' + "".join(slide(s) for s in d["slides"]) + "</div>"
    page(name=d["name"], folder="decks", title=d["title"], kicker=d["kicker"], stand=d["stand"], body=body)
    print(f"wrote decks/{d['name']}.html   {len(d['slides'])} slides · dist/{d['name']}.html")
sys.exit(fail)
