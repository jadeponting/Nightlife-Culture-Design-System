#!/usr/bin/env python3
"""Decks as data -> native PowerPoint files, on the v1.5.1 slide blocks.

    python3 adapters/powerpoint/build_deck_pptx.py              every deck in decks/*.json with a "pptx" name
    python3 adapters/powerpoint/build_deck_pptx.py vibe-map-partner

Run `python3 build.py` first: this reads dist/<name>.html, the deck the build rendered.

The route, and why it is this route
  1  measure  The browser draws each slide from the slide blocks, with the real fonts. Every fill,
              rule, wordmark and text block is measured where it landed, with its face, size,
              colour, caps and line breaks. Nothing is re-decided for PowerPoint, so nothing can
              drift from the HTML deck.
  2  build    adapters/powerpoint/deck_pptx.js places those measurements as native shapes and text
              boxes (pptxgenjs). Speaker notes come from each slide's "notes"; slides marked
              "optional" go in their own section. Slide numbers are fields.
  3  finish   Capitals become the all-caps property, never typed (NC-TYP-01) · British English
              proofing · a real PNG behind the SVG wordmark · the faces the deck uses embedded,
              so it keeps its type on a machine without Archivo or Inter.
  4  inspect  checks/inspect_pptx.py: token colours, system faces, the 14pt floor.

Needs: Playwright with Chromium (as checks/check_contrast.py does), fontTools + brotli, and node
with adapters/powerpoint/node_modules.

The previous adapter, build_ukdf_pptx.js, chose its own sizes and colours on v1.4 floors. It still
builds the UKDF deck it was written for; new decks come through here.
"""
import asyncio, io, json, pathlib, re, struct, subprocess, sys, tempfile, zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
HERE = pathlib.Path(__file__).resolve().parent

MEASURE = r"""() => {
const rgb = c => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null;
  const p = m[1].split(',').map(parseFloat); const a = p.length > 3 ? p[3] : 1;
  if (a === 0) return null;
  return {hex: p.slice(0, 3).map(v => Math.round(v).toString(16).padStart(2, '0')).join('').toUpperCase(), a}; };
return [...document.querySelectorAll('.nc-slide')].map(s => {
  const o = s.getBoundingClientRect();
  const R = e => { const r = e.getBoundingClientRect(); return {x: r.left - o.left, y: r.top - o.top, w: r.width, h: r.height}; };
  const cv = s.querySelector('.cv'), cvs = getComputedStyle(cv);
  const out = {width: o.width, ground: rgb(cvs.backgroundColor), textOn: rgb(cvs.color),
               band: !!s.querySelector('.nc-sband'), fills: [], rules: [], texts: [], logos: []};
  s.querySelectorAll('.cv *').forEach(e => {
    if (e.closest('svg')) return;
    const cs = getComputedStyle(e), r = R(e);
    if (!r.w || !r.h) return;
    const bg = rgb(cs.backgroundColor);
    if (bg && e.tagName !== 'HR') out.fills.push({...r, c: bg});
    if (e.tagName === 'HR') out.rules.push({...r, c: bg});
    for (const side of ['Top', 'Left']) {
      const w = parseFloat(cs['border' + side + 'Width']), c = rgb(cs['border' + side + 'Color']);
      if (w > 0 && c && cs['border' + side + 'Style'] !== 'none')
        out.rules.push(side === 'Top' ? {x: r.x, y: r.y, w: r.w, h: w, c} : {x: r.x, y: r.y, w: w, h: r.h, c});
    }
    if (e.classList.contains('nc-slogo')) { out.logos.push({...R(e.querySelector('svg')), c: rgb(cs.color)}); return; }
    if (!['P', 'H2', 'DT', 'DD', 'LI'].includes(e.tagName)) return;
    const pl = parseFloat(cs.paddingLeft), pt = parseFloat(cs.paddingTop), pr = parseFloat(cs.paddingRight),
          pb = parseFloat(cs.paddingBottom), bl = parseFloat(cs.borderLeftWidth), bt = parseFloat(cs.borderTopWidth);
    // the browser's own line breaks, for the lines where a different break changes the look
    let brk = null;
    if (e.matches('h2, .h, .hc, dt, .nc-sline, .nc-sl')) {
      const words = [], tw = document.createTreeWalker(e, NodeFilter.SHOW_TEXT);
      while (tw.nextNode()) { const n = tw.currentNode, re = /\S+/g; let m;
        while ((m = re.exec(n.data))) { const rg = document.createRange();
          rg.setStart(n, m.index); rg.setEnd(n, m.index + m[0].length);
          words.push([m[0], Math.round(rg.getClientRects()[0].top)]); } }
      brk = []; words.forEach(([w, top], i) => {
        if (!i || top > words[i - 1][1] + 2) brk.push(w); else brk[brk.length - 1] += ' ' + w; });
    }
    out.texts.push({x: r.x + pl + bl, y: r.y + pt + bt, w: r.w - pl - pr - bl, h: r.h - pt - pb - bt, brk,
      text: e.textContent.replace(/\s+/g, ' ').trim(),
      family: cs.fontFamily.split(',')[0].replace(/"/g, ''), weight: parseInt(cs.fontWeight),
      size: parseFloat(cs.fontSize), lh: parseFloat(cs.lineHeight), ls: parseFloat(cs.letterSpacing) || 0,
      caps: cs.textTransform === 'uppercase', color: rgb(cs.color)});
  });
  return out; }); }"""

# face as Office names it -> (source woff2, family, subfamily). The source files carry internal
# names from the subsetter (Archivo 700 calls itself "Archivo SemiBold" Bold), so they are renamed
# here to the names Office resolves; assets/fonts is not touched.
FACES = {
    ("Archivo Black", False): ("ArchivoBlack.woff2", "Archivo Black", "Regular"),
    ("Archivo", True): ("Archivo-Bold.woff2", "Archivo", "Bold"),
    ("Inter", False): ("Inter-Regular.woff2", "Inter", "Regular"),
    ("Inter", True): ("Inter-Bold.woff2", "Inter", "Bold"),
    ("Inter SemiBold", False): ("Inter-SemiBold.woff2", "Inter SemiBold", "Regular"),
}


def office_ttf(woff2, family, sub):
    from fontTools.ttLib import TTFont
    f = TTFont(str(ROOT / "assets" / "fonts" / woff2)); f.flavor = None
    n = f["name"]
    for i in (16, 17, 21, 22):
        n.removeNames(nameID=i)
    ps = f"{family.replace(' ', '')}-{sub}"
    for pid, eid, lid in ((3, 1, 0x409), (1, 0, 0)):
        n.setName(family, 1, pid, eid, lid); n.setName(sub, 2, pid, eid, lid)
        n.setName(family if sub == "Regular" else f"{family} {sub}", 4, pid, eid, lid); n.setName(ps, 6, pid, eid, lid)
    os2 = f["OS/2"]
    if sub == "Bold":
        os2.fsSelection = (os2.fsSelection & ~0x40) | 0x20; f["head"].macStyle |= 1
    else:
        os2.fsSelection = (os2.fsSelection & ~0x21) | 0x40; f["head"].macStyle &= ~1
    buf = io.BytesIO(); f.save(buf); return buf.getvalue()


def eot(data):
    """Embedded OpenType 2.1, uncompressed: the wrapper Office stores as .fntdata.
    Byte-identical to ttf2eot's output for the same font (checked 14 Oct 2026)."""
    from fontTools.ttLib import TTFont
    f = TTFont(io.BytesIO(data)); os2, head, name = f["OS/2"], f["head"], f["name"]
    def nm(i):
        r = name.getName(i, 3, 1, 0x409) or name.getName(i, 1, 0, 0)
        b = (r.toUnicode() if r else "").encode("utf-16-le"); return struct.pack("<H", len(b)) + b
    p = os2.panose
    pan = bytes([p.bFamilyType, p.bSerifStyle, p.bWeight, p.bProportion, p.bContrast,
                 p.bStrokeVariation, p.bArmStyle, p.bLetterForm, p.bMidline, p.bXHeight])
    body = (pan + struct.pack("<BBIHH", 1, os2.fsSelection & 1, os2.usWeightClass, os2.fsType, 0x504C)
            + struct.pack("<6I", os2.ulUnicodeRange1, os2.ulUnicodeRange2, os2.ulUnicodeRange3,
                          os2.ulUnicodeRange4, os2.ulCodePageRange1, os2.ulCodePageRange2)
            + struct.pack("<5I", head.checkSumAdjustment, 0, 0, 0, 0) + struct.pack("<H", 0)
            + nm(1) + b"\0\0" + nm(2) + b"\0\0" + nm(5) + b"\0\0" + nm(4) + b"\0\0" + struct.pack("<H", 0))
    return struct.pack("<4I", 16 + len(body) + len(data), len(data), 0x00020001, 0) + body + data


async def measure(page_file):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1400, "height": 900})
        await pg.goto(page_file.as_uri()); await pg.evaluate("document.fonts.ready")
        data = await pg.evaluate(MEASURE)
        await b.close()
        return data


async def rasterise(svg):
    from playwright.async_api import async_playwright
    m = re.search(rb'viewBox="[\d.]+ [\d.]+ ([\d.]+) ([\d.]+)"', svg)
    w, h = (round(float(m.group(1)) * 10), round(float(m.group(2)) * 10)) if m else (1722, 709)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": w, "height": h})
        await pg.set_content('<body style="margin:0;background:transparent">' + svg.decode().replace(
            "<svg ", f'<svg style="width:{w}px;height:{h}px;display:block" ', 1))
        png = await pg.screenshot(omit_background=True, clip={"x": 0, "y": 0, "width": w, "height": h})
        await b.close()
        return png


A = "http://schemas.openxmlformats.org/drawingml/2006/main"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
RNS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG = "http://schemas.openxmlformats.org/package/2006/relationships"


def finish(raw, out, caps_file, faces):
    import lxml.etree as ET
    caps = {}
    for e in json.loads(pathlib.Path(caps_file).read_text()):
        caps.setdefault(e["slide"], set()).add(e["text"].replace(" ", ""))
    z = zipfile.ZipFile(raw); files = {n: z.read(n) for n in z.namelist()}; runs = 0
    for name in list(files):
        m = re.fullmatch(r"ppt/(slides/slide|notesSlides/notesSlide)(\d+)\.xml", name)
        if not m:
            continue
        tree = ET.fromstring(files[name])
        for el in tree.iter(f"{{{A}}}rPr", f"{{{A}}}endParaRPr", f"{{{A}}}defRPr"):
            if el.get("lang"):
                el.set("lang", "en-GB")
        if m.group(1) == "slides/slide":
            want = caps.get(int(m.group(2)), set())
            for p in tree.iter(f"{{{A}}}p"):
                text = "".join(t.text or "" for t in p.iter(f"{{{A}}}t")).replace(" ", "")
                if text and text in want:
                    for r in p.iter(f"{{{A}}}r"):
                        rPr = r.find(f"{{{A}}}rPr")
                        if rPr is None:
                            rPr = ET.Element(f"{{{A}}}rPr"); r.insert(0, rPr)
                        rPr.set("cap", "all"); runs += 1
        files[name] = ET.tostring(tree, xml_declaration=True, encoding="UTF-8", standalone=True)
    # pptxgenjs stores the SVG's bytes again under a .png name as the fallback image
    for name in list(files):
        if name.startswith("ppt/media/") and name.endswith(".png") and files[name].lstrip().startswith(b"<"):
            files[name] = asyncio.run(rasterise(files[name]))
    pres = ET.fromstring(files["ppt/presentation.xml"]); rels = ET.fromstring(files["ppt/_rels/presentation.xml.rels"])
    lst = ET.Element(f"{{{P}}}embeddedFontLst"); n = 0
    by_face = {}
    for (fam, bold) in sorted(faces):
        by_face.setdefault(fam, []).append(bold)
    for fam, bolds in by_face.items():
        ef = ET.SubElement(lst, f"{{{P}}}embeddedFont")
        ET.SubElement(ef, f"{{{P}}}font", typeface=fam, pitchFamily="2", charset="0")
        for bold in sorted(bolds):
            n += 1; rid = f"rIdNcFont{n}"
            files[f"ppt/fonts/font{n}.fntdata"] = eot(office_ttf(*FACES[(fam, bold)]))
            ET.SubElement(rels, f"{{{PKG}}}Relationship", Id=rid, Target=f"fonts/font{n}.fntdata",
                          Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/font")
            ET.SubElement(ef, f"{{{P}}}{'bold' if bold else 'regular'}", {f"{{{RNS}}}id": rid})
    pres.find(f"{{{P}}}notesSz").addnext(lst)
    pres.set("embedTrueTypeFonts", "1"); pres.set("saveSubsetFonts", "1")
    files["ppt/presentation.xml"] = ET.tostring(pres, xml_declaration=True, encoding="UTF-8", standalone=True)
    files["ppt/_rels/presentation.xml.rels"] = ET.tostring(rels, xml_declaration=True, encoding="UTF-8", standalone=True)
    ct = files["[Content_Types].xml"].decode()
    if 'Extension="fntdata"' not in ct:
        ct = ct.replace("<Default ", '<Default Extension="fntdata" ContentType="application/x-fontdata"/><Default ', 1)
    files["[Content_Types].xml"] = ct.encode()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zo:
        for k in ["[Content_Types].xml"] + [k for k in files if k != "[Content_Types].xml"]:
            zo.writestr(k, files[k])
    return runs, n


def face_of(t):
    if t["family"] == "Archivo Black": return ("Archivo Black", False)
    if t["family"] == "Archivo": return ("Archivo", t["weight"] >= 700)
    if t["weight"] >= 700: return ("Inter", True)
    if t["weight"] >= 600: return ("Inter SemiBold", False)
    return ("Inter", False)


def build(deck_file):
    d = json.loads(deck_file.read_text())
    page = ROOT / "dist" / f"{d['name']}.html"
    if not page.exists():
        sys.exit(f"  !! {page.relative_to(ROOT)} is missing — run python3 build.py first")
    measured = asyncio.run(measure(page))
    if len(measured) != len(d["slides"]):
        sys.exit(f"  !! {d['name']}: {len(measured)} slides drawn, {len(d['slides'])} in the deck")
    for m, s in zip(measured, d["slides"]):
        m["notes"] = s.get("notes", ""); m["optional"] = bool(s.get("optional"))
    faces = {face_of(t) for m in measured for t in m["texts"]} | {("Archivo", True)}   # + the slide number
    out = ROOT / "dist" / f"{d['pptx']}.pptx"
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        (tmp / "measured.json").write_text(json.dumps({"title": d.get("pptxTitle", f"Nightlife Culture · {d['title']}"),
                                                       "sections": d.get("sections"), "slides": measured}))
        subprocess.run(["node", str(HERE / "deck_pptx.js"), str(tmp / "measured.json"), str(tmp / "raw.pptx"),
                        str(tmp / "caps.json")], check=True, cwd=HERE)
        runs, nfonts = finish(tmp / "raw.pptx", out, tmp / "caps.json", faces)
    print(f"  finished: caps on {runs} runs · {nfonts} faces embedded · en-GB → dist/{out.name}")
    return subprocess.run([sys.executable, str(ROOT / "checks" / "inspect_pptx.py"), str(out)]).returncode


if __name__ == "__main__":
    names = sys.argv[1:]
    decks = [ROOT / "decks" / f"{n}.json" for n in names] if names else \
        [f for f in sorted((ROOT / "decks").glob("*.json")) if "pptx" in json.loads(f.read_text())]
    sys.exit(max([build(f) for f in decks] or [0]))
