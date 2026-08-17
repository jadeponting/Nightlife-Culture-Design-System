#!/usr/bin/env python3
"""Inspect a .pptx against the system, the way the validator inspects a page.

    python3 checks/inspect_pptx.py deck.pptx

Reads the slide XML directly. Fails on: any colour outside the token set,
any font outside the three faces, any text under 14pt (the v1.4 slide-label
floor). Reports runs of body length (nine words or more) sitting under the
18pt slide-body floor — reported, not failed, because one tension is still
open: five verbatim strand descriptions cannot yet hold 18pt on one slide.
"""
import json, pathlib, re, sys, zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
T = json.loads((ROOT / "foundations" / "tokens.json").read_text())
C = T["colour"]
ALLOWED = {v["hex"][1:].upper() for v in C["grounds"].values()} \
        | {v["hex"][1:].upper() for v in C["accents"].values() if isinstance(v, dict)} \
        | {C["textColours"]["charcoal"]["hex"][1:].upper()}
FONTS = {"Archivo Black", "Archivo", "Inter",
         "+mn-lt", "+mj-lt", "+mn-ea", "+mj-ea", "+mn-cs", "+mj-cs"}
FLOOR_ANY, FLOOR_BODY = 14, 18

deck = pathlib.Path(sys.argv[1])
z = zipfile.ZipFile(deck)
fails, warns = [], []
for name in sorted(n for n in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)):
    n = int(re.search(r"(\d+)", name).group(1))
    xml = z.read(name).decode("utf8")
    for hexv in set(re.findall(r'srgbClr val="([0-9A-Fa-f]{6})"', xml)):
        if hexv.upper() not in ALLOWED:
            fails.append(f"slide {n}: colour #{hexv.upper()} is not a token")
    for face in set(re.findall(r'typeface="([^"]+)"', xml)):
        if face not in FONTS:
            fails.append(f"slide {n}: font “{face}” is not a system face")
    # size per run, with the run's text
    for m in re.finditer(r'<a:rPr[^>]*\bsz="(\d+)"[^>]*/?>.*?<a:t>([^<]*)</a:t>', xml, re.S):
        pt, txt = int(m.group(1)) / 100, m.group(2).strip()
        if not txt:
            continue
        if pt < FLOOR_ANY:
            fails.append(f"slide {n}: {pt}pt “{txt[:40]}” — under the 14pt floor")
        elif pt < FLOOR_BODY and len(txt.split()) >= 9:
            warns.append(f"slide {n}: body-length run at {pt}pt “{txt[:40]}…” — 18pt is the slide-body floor")

print(f"=== {deck.name}")
for f in sorted(set(fails)):
    print(f"  FAIL  {f}")
for w in sorted(set(warns))[:12]:
    print(f"  warn  {w}")
if len(set(warns)) > 12:
    print(f"  … {len(set(warns)) - 12} more warns")
print(f"{len(set(fails))} failure(s) · {len(set(warns))} body-floor report(s)")
sys.exit(1 if fails else 0)
