#!/usr/bin/env python3
"""Post-pass: declare en-GB (NC-DOC-03) and retire the library's default
style colours. docx-js ships dormant Heading/Hyperlink styles in Office blues
(#2E74B5, #1F4D78, #0563C1); dormant or not, a declared colour is a colour
someone will one day use, so they become the token blue and ink."""
import shutil, zipfile, pathlib
f = pathlib.Path(__file__).resolve().parent.parent.parent / "dist" / "Nightlife_Culture_UKDF_Operating_Plan_v0.4.docx"
tmp = f.with_suffix(".tmp"); shutil.copy(f, tmp)
with zipfile.ZipFile(tmp) as zin, zipfile.ZipFile(f, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.namelist():
        data = zin.read(item)
        if item == "word/styles.xml":
            s = data.decode()
            s = s.replace("<w:docDefaults><w:rPrDefault><w:rPr>",
                          '<w:docDefaults><w:rPrDefault><w:rPr><w:lang w:val="en-GB"/>', 1)
            for lib, tok in (("2E74B5", "0D0D0D"), ("1F4D78", "0D0D0D"), ("0563C1", "0000FF")):
                s = s.replace(lib, tok)
            data = s.encode()
        zout.writestr(item, data)
tmp.unlink()
print("en-GB declared · library default colours retired to tokens")
