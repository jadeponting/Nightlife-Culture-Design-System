#!/usr/bin/env python3
"""Restyle the budget workbook on the system — in place, changing nothing else.

Her v0.3 is the closest of the three artefacts to clean: token fills, mostly
system faces, formulas intact. This pass changes PRESENTATION only:

  · Carlito (the LibreOffice default that leaked in) becomes Inter
  · every font colour resolves to a token — ink, charcoal or white
  · everything else — values, formulas, merges, widths, number formats,
    borders, fills — is preserved untouched

Content conventions are hers and stay hers (xlsx skill: match the file's
conventions exactly; they override every guideline).
"""
import json, pathlib, sys
from openpyxl import load_workbook
from openpyxl.styles import Font

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
T = json.loads((ROOT / "foundations" / "tokens.json").read_text())
C = T["colour"]
INK = "FF" + C["grounds"]["ink"]["hex"][1:]
CHARCOAL = "FF" + C["textColours"]["charcoal"]["hex"][1:]
TOKENS = {("FF" + v["hex"][1:]).upper() for v in C["grounds"].values()} \
       | {("FF" + v["hex"][1:]).upper() for v in C["accents"].values() if isinstance(v, dict)} \
       | {CHARCOAL}

SRC = sys.argv[1]
OUT = ROOT / "dist" / "Nightlife_Culture_UKDF_Budget_Delivery_Workbook_v0.4.xlsx"

wb = load_workbook(SRC)
changed_font = changed_col = 0
for ws in wb:
    for row in ws.iter_rows():
        for c in row:
            f = c.font
            if f is None:
                continue
            name = f.name
            colour = f.color.rgb if f.color and isinstance(f.color.rgb, str) else None
            new_name = "Inter" if name == "Carlito" else name
            if colour is not None and colour.upper() in TOKENS:
                new_col = colour
            else:
                new_col = INK        # default / black / anything else: ink text
            if new_name != name or new_col != colour:
                c.font = Font(name=new_name, size=f.size, bold=f.bold, italic=f.italic,
                              color=new_col, underline=f.underline, vertAlign=f.vertAlign,
                              strike=f.strike)
                changed_font += int(new_name != name)
                changed_col += int(new_col != colour)

# The workbook DEFAULT font is part of the presentation too. Left alone it is
# whatever tool last saved the file (Calibri from Excel, Arial from
# LibreOffice), and every untouched cell inherits it.
for ns in wb._named_styles:
    if ns.name == "Normal":
        ns.font = Font(name="Inter", size=11, color=INK)

wb.properties.title = "Nightlife Culture · UKDF fellowship — budget and delivery workbook"
wb.properties.creator = "Carly Heath · Nightlife Culture"
wb.save(OUT)
print(f"wrote {OUT.name}")
print(f"  {changed_font} Carlito cell(s) -> Inter · {changed_col} colour(s) resolved to tokens")
