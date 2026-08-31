#!/usr/bin/env python3
"""Apply caps as the OOXML all-caps property, never typed (NC-TYP-01).

The generator writes every string in sentence case and lists the ones that
display in capitals in caps-manifest.json. This pass sets cap="all" on the
run properties of exactly those runs, so a screen reader, search and
copy-paste all see the real text while the slide shows caps.
"""
import json, pathlib, re, shutil, sys, zipfile
import lxml.etree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
PPTX = ROOT / "dist" / "UKDF_Fellowship_Proposal_Artists_Make_Great_Places_V2.pptx"
_M = json.load(open(pathlib.Path(__file__).parent / "caps-manifest.json"))
# per-slide, so "Follow the value" as a panel label caps while the identical
# words in another slide's list stay sentence case
CAPS = {}
for e in _M:
    CAPS.setdefault(e["slide"], set()).add(e["text"])
A = "http://schemas.openxmlformats.org/drawingml/2006/main"

tmp = PPTX.with_suffix(".tmp")
shutil.copy(PPTX, tmp)
changed = 0
with zipfile.ZipFile(tmp) as zin, zipfile.ZipFile(PPTX, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.namelist():
        data = zin.read(item)
        m = re.fullmatch(r"ppt/slides/slide(\d+)\.xml", item)
        if m:
            want = CAPS.get(int(m.group(1)), set())
            tree = ET.fromstring(data)
            # group runs by paragraph so a string split across runs still matches
            for p in tree.iter(f"{{{A}}}p"):
                text = "".join(t.text or "" for t in p.iter(f"{{{A}}}t"))
                if text.strip() and text.strip() in want:
                    for r in p.iter(f"{{{A}}}r"):
                        rPr = r.find(f"{{{A}}}rPr")
                        if rPr is None:
                            rPr = ET.SubElement(r, f"{{{A}}}rPr")
                            r.insert(0, rPr)
                        rPr.set("cap", "all")
                        changed += 1
            data = ET.tostring(tree, xml_declaration=True, encoding="UTF-8", standalone=True)
        zout.writestr(item, data)
try:
    tmp.unlink()
except PermissionError:      # synced folders often forbid unlink; parking works
    dest = tmp.parent.parent / "_to_delete" / tmp.name
    dest.parent.mkdir(exist_ok=True)
    tmp.replace(dest)
print(f"cap='all' applied to {changed} runs — text stays sentence case underneath")
