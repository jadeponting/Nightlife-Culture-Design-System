#!/usr/bin/env python3
"""Inspect a .docx against the system.

    python3 checks/inspect_docx.py file.docx

Fails on: direct run formatting where a named style should carry it (any
run-level font, size or colour in document.xml — bold, italic and caps are
semantic and allowed), fonts outside the system faces, colours outside the
tokens, text under the 10pt footnote floor, no document title or language.
This is THE PLAN's finish line: open the template, write, run this, it passes.
"""
import json, pathlib, re, sys, zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
T = json.loads((ROOT / "foundations" / "tokens.json").read_text())
C = T["colour"]
ALLOWED = {v["hex"][1:].upper() for v in C["grounds"].values()} \
        | {v["hex"][1:].upper() for v in C["accents"].values() if isinstance(v, dict)} \
        | {C["textColours"]["charcoal"]["hex"][1:].upper(), "C9C9C9", "AUTO"}
FONTS = {"Inter", "Archivo", "Archivo Black", "Archivo ExtraBold",
         "Archivo SemiBold", "Archivo Bold"}

deck = pathlib.Path(sys.argv[1])
z = zipfile.ZipFile(deck)
doc = z.read("word/document.xml").decode("utf8")
sty = z.read("word/styles.xml").decode("utf8")
fails, notes = [], []

# 1 · direct formatting in the body. A rPr carrying rFonts, sz or color is a
#     value decided at the keyboard instead of in a style.
direct = 0
for rpr in re.findall(r"<w:rPr>(.*?)</w:rPr>", doc, re.S):
    if re.search(r"<w:(rFonts|sz|color)\b", rpr):
        direct += 1
if direct:
    fails.append(f"{direct} run(s) carry direct font/size/colour — a named style's job (NC-DOC-01)")

# 2 · fonts, wherever declared
for face in set(re.findall(r'w:ascii="([^"]+)"', doc + sty)):
    if face not in FONTS:
        fails.append(f"font “{face}” is not a system face")

# 3 · colours, wherever declared
for col in set(re.findall(r'w:val="([0-9A-Fa-f]{6})"\s*/?>', doc + sty)) \
         | set(re.findall(r'w:fill="([0-9A-Fa-f]{6})"', doc + sty)):
    if col.upper() not in ALLOWED:
        fails.append(f"colour #{col.upper()} is not a token")

# 4 · size floor in styles: nothing under 10pt (v1.4 footnote floor)
for sz in set(re.findall(r'<w:sz w:val="(\d+)"/>', sty)):
    if int(sz) < 20:
        fails.append(f"style size {int(sz)/2}pt — under the 10pt footnote floor")

# 5 · metadata (NC-DOC-03)
core = z.read("docProps/core.xml").decode("utf8") if "docProps/core.xml" in z.namelist() else ""
if "<dc:title>" not in core or "<dc:title></dc:title>" in core:
    fails.append("no document title in properties (NC-DOC-03)")
if 'w:lang w:val="en-GB"' not in sty and "<dc:language>" not in core:
    fails.append("no declared language (NC-DOC-03)")

print(f"=== {deck.name}")
for f in sorted(set(fails))[:14]:
    print(f"  FAIL  {f}")
if len(set(fails)) > 14: print(f"  … {len(set(fails)) - 14} more")
print(f"{len(set(fails))} failure(s)")
sys.exit(1 if fails else 0)
