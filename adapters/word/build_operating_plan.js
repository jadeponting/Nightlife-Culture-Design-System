/* The Operating Plan, as a real Word document on the system.
 *
 * Content: opplan-content.json — her v0.3, verbatim, in document order.
 * Styles: generated from foundations/tokens.json. Named styles only; the only
 * run-level properties in the whole file are bold and italic, which are
 * semantic emphasis (NC-DOC-01). A4 (NC-DOC-02). Title, author and language
 * set in properties (NC-DOC-03). Table header rows repeat (NC-DOC-04).
 */
const fs = require("fs");
const path = require("path");
const D = require("docx");

const ROOT = path.resolve(__dirname, "..", "..");
const T = JSON.parse(fs.readFileSync(path.join(ROOT, "foundations/tokens.json")));
const C = T.colour;
const hex = h => h.replace("#", "");
const INK = hex(C.grounds.ink.hex), BLUE = hex(C.grounds.blue.hex),
      CHALK = hex(C.grounds.chalk.hex), WHITE = "FFFFFF",
      CHARCOAL = hex(C.textColours.charcoal.hex),
      PINK = hex(C.accents.pink.hex), TEAL = hex(C.accents.teal.hex);
const SC = T.type.sizes.document.scale;
const pt2 = pt => Math.round(pt * 2);                 // half-points
const BODY = pt2(SC.body.pt), H1 = pt2(18), H2 = pt2(SC.h3.pt),
      TITLE = pt2(SC.h1.pt), NOTE = pt2(SC.note.pt);
const CONTENT = JSON.parse(fs.readFileSync(path.join(__dirname, "opplan-content.json")));

const styles = {
  default: {
    document: { run: { font: "Inter", size: BODY, color: INK },
                paragraph: { spacing: { line: 372, after: 180 } } } },
  paragraphStyles: [
    { id: "Title", name: "Title", basedOn: "Normal",
      run: { font: "Archivo Black", size: TITLE, color: INK, allCaps: true },
      paragraph: { spacing: { line: 560, before: 0, after: 120 } } },
    { id: "Subtitle", name: "Subtitle", basedOn: "Normal",
      run: { font: "Archivo SemiBold", size: pt2(13), color: BLUE },
      paragraph: { spacing: { after: 320 } } },
    { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal",
      run: { font: "Archivo ExtraBold", size: H1, color: INK, allCaps: true },
      paragraph: { spacing: { before: 540, after: 180 }, outlineLevel: 0,
                   border: { bottom: { style: D.BorderStyle.SINGLE, size: 18, color: INK, space: 4 } } } },
    { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal",
      run: { font: "Archivo", bold: true, size: H2, color: INK },
      paragraph: { spacing: { before: 360, after: 120 }, outlineLevel: 1 } },
    { id: "NCLabel", name: "NC Label", basedOn: "Normal",
      run: { font: "Archivo SemiBold", size: NOTE, color: CHARCOAL, allCaps: true,
             characterSpacing: 20 },
      paragraph: { spacing: { after: 60 } } },
    { id: "NCPullQuote", name: "NC Pull Quote", basedOn: "Normal",
      run: { font: "Archivo ExtraBold", size: pt2(16), color: INK },
      paragraph: { spacing: { before: 240, after: 240, line: 300 },
                   indent: { left: 360 },
                   border: { left: { style: D.BorderStyle.SINGLE, size: 36, color: PINK, space: 12 } } } },
    { id: "NCCaption", name: "NC Caption", basedOn: "Normal",
      run: { font: "Inter", size: NOTE, color: CHARCOAL },
      paragraph: { spacing: { line: 300, after: 120 } } },
    { id: "NCCoverHead", name: "NC Cover Head", basedOn: "Normal",
      run: { font: "Archivo SemiBold", size: NOTE, color: "FFFFFF", allCaps: true,
             characterSpacing: 20 },
      paragraph: { spacing: { after: 120 } } },
    { id: "NCCoverTitle", name: "NC Cover Title", basedOn: "Normal",
      run: { font: "Archivo Black", size: TITLE, color: "FFFFFF", allCaps: true },
      paragraph: { spacing: { line: 560, before: 120, after: 160 } } },
    { id: "NCCoverMeta", name: "NC Cover Meta", basedOn: "Normal",
      run: { font: "Archivo SemiBold", size: pt2(11), color: TEAL },
      paragraph: { spacing: { after: 0 } } },
    { id: "NCPanelHead", name: "NC Panel Head", basedOn: "Normal",
      run: { font: "Archivo SemiBold", size: NOTE, allCaps: true, characterSpacing: 20 },
      paragraph: { spacing: { after: 60 } } },
    { id: "TableBody", name: "NC Table Body", basedOn: "Normal",
      run: { size: pt2(10.5) }, paragraph: { spacing: { line: 300, after: 40 } } },
    { id: "TableHead", name: "NC Table Head", basedOn: "Normal",
      run: { font: "Archivo SemiBold", size: pt2(10.5), allCaps: true, characterSpacing: 16,
             color: CHARCOAL },
      paragraph: { spacing: { line: 280, after: 40 } } },
  ],
};

const numbering = { config: [{ reference: "ncb", levels: [{
  level: 0, format: D.LevelFormat.BULLET, text: "—",
  alignment: D.AlignmentType.LEFT,
  style: { paragraph: { indent: { left: 360, hanging: 360 } } } }] }] };

const runs = rs => rs.map(([t, b, i]) =>
  new D.TextRun({ text: t, bold: b || undefined, italics: i || undefined }));

function paragraph(p) {
  const st = !p.style || p.style === "Body" ? undefined : p.style;
  if (p.style === "ListBullet")
    return new D.Paragraph({ children: runs(p.runs), numbering: { reference: "ncb", level: 0 } });
  return new D.Paragraph({ children: runs(p.runs), style: st });
}

// ---- tables ----------------------------------------------------------------
const PAGE_W = 9026;   // A4 content width in DXA at 2.2cm margins
const LAND_W = 13300;

const NIL = { style: D.BorderStyle.NIL };
const rowBorder = { top: NIL, left: NIL, right: NIL,
  bottom: { style: D.BorderStyle.SINGLE, size: 4, color: "C9C9C9" } };
const headBorder = { top: NIL, left: NIL, right: NIL,
  bottom: { style: D.BorderStyle.SINGLE, size: 12, color: INK } };

function panel(rowsOfCells, ix) {
  // A 1x1 table is a callout panel. The first is the cover banner: blue
  // ground, white text. The rest take chalk with the blue left rule
  // (containment v1.3). Inside a panel the first paragraph is the label.
  const cover = ix === 0;
  const src = rowsOfCells[0][0];
  const ps = src.map((p, pi) => {
    let st;
    if (cover) st = pi === 0 ? "NCCoverHead" : (pi === 1 ? "NCCoverTitle" : "NCCoverMeta");
    else st = pi === 0 && src.length > 1 ? "NCPanelHead" : p.style;
    return paragraph({ ...p, style: st === "Body" ? undefined : st });
  });
  return new D.Table({
    columnWidths: [PAGE_W], width: { size: PAGE_W, type: D.WidthType.DXA },
    borders: { top: NIL, bottom: NIL, left: cover ? NIL :
        { style: D.BorderStyle.SINGLE, size: 36, color: BLUE },
      right: NIL, insideHorizontal: NIL, insideVertical: NIL },
    rows: [new D.TableRow({ children: [new D.TableCell({
      width: { size: PAGE_W, type: D.WidthType.DXA },
      shading: { type: D.ShadingType.CLEAR, fill: cover ? BLUE : CHALK },
      margins: { top: cover ? 400 : 200, bottom: cover ? 400 : 140, left: 260, right: 260 },
      children: ps.length ? ps : [new D.Paragraph("")],
    })] })],
  });
}

function dataTable(rows, wide) {
  const total = wide ? LAND_W : PAGE_W;
  const nCols = Math.max(...rows.map(r => r.length));
  // width by content: first column often an ID — weight columns by max text length
  const maxLen = Array.from({ length: nCols }, (_, c) =>
    Math.max(4, ...rows.map(r => (r[c] || []).reduce((a, p) =>
      a + p.runs.reduce((x, [t]) => x + t.length, 0), 0))));
  const capped = maxLen.map(l => Math.max(9, Math.min(l, 60)));
  const sum = capped.reduce((a, b) => a + b, 0);
  const widths = capped.map(l => Math.round(total * l / sum));
  // floor: no column under 1150 DXA — "£6,000" splitting as "£6,00 0" is how a
  // budget stops being readable. The widest column pays for the floor.
  for (let i = 0; i < nCols; i++) {
    if (widths[i] < 1150) {
      const take = 1150 - widths[i];
      widths[widths.indexOf(Math.max(...widths))] -= take;
      widths[i] = 1150;
    }
  }
  widths[nCols - 1] = total - widths.slice(0, -1).reduce((a, b) => a + b, 0);

  return new D.Table({
    columnWidths: widths, width: { size: total, type: D.WidthType.DXA },
    borders: { top: NIL, bottom: NIL, left: NIL, right: NIL,
               insideHorizontal: NIL, insideVertical: NIL },
    rows: rows.map((r, ri) => new D.TableRow({
      tableHeader: ri === 0,
      children: Array.from({ length: nCols }, (_, ci) => new D.TableCell({
        width: { size: widths[ci], type: D.WidthType.DXA },
        borders: ri === 0 ? headBorder : rowBorder,
        margins: { top: 60, bottom: 60, left: 0, right: 140 },
        children: (r[ci] && r[ci].length ? r[ci] : [{ style: "Body", runs: [["", false, false]] }])
          .map(p => paragraph({ ...p, style: ri === 0 ? "TableHead" : "TableBody" })),
      })),
    })),
  });
}

// ---- assemble in three sections: portrait / landscape timeline / portrait --
const TIMELINE_IX = CONTENT.findIndex(it =>
  it.kind === "table" && it.rows[0].length >= 10);
const before = [], timeline = [], after = [];
CONTENT.forEach((it, ix) => {
  const bucket = ix < TIMELINE_IX ? before : ix === TIMELINE_IX ? timeline : after;
  if (it.kind === "p") bucket.push(paragraph(it));
  else if (it.rows.length === 1 && it.rows[0].length === 1) bucket.push(panel(it.rows, ix));
  else bucket.push(dataTable(it.rows, ix === TIMELINE_IX));
});

const foot = new D.Footer({ children: [new D.Paragraph({
  style: "NCLabel", children: [
    new D.TextRun("Nightlife Culture · Artists Make Great Places · operating plan v0.4"),
    new D.TextRun({ children: ["   ", D.PageNumber.CURRENT] })] })] });

const doc = new D.Document({
  title: "Artists Make Great Places — operating plan",
  creator: "Carly Heath · Nightlife Culture",
  description: "UKDF fellowship operating plan, on the Nightlife Culture design system.",
  styles, numbering,
  sections: [
    { properties: { page: { margin: { top: 1250, bottom: 1250, left: 1250, right: 1250 } } },
      footers: { default: foot }, children: before },
    { properties: { page: { size: { orientation: D.PageOrientation.LANDSCAPE },
        margin: { top: 1250, bottom: 1250, left: 1250, right: 1250 } } },
      footers: { default: foot }, children: timeline },
    { properties: { page: { margin: { top: 1250, bottom: 1250, left: 1250, right: 1250 } } },
      footers: { default: foot }, children: after },
  ],
});

const out = path.join(ROOT, "dist", "Nightlife_Culture_UKDF_Operating_Plan_v0.4.docx");
D.Packer.toBuffer(doc).then(buf => { fs.writeFileSync(out, buf); console.log("wrote", out); });
