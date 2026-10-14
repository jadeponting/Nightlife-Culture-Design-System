/* A measured deck -> a native PowerPoint file. Called by build_deck_pptx.py; not run on its own.
 *
 *   node deck_pptx.js <measured.json> <out.pptx> <caps-manifest.json>
 *
 * Every position, size and colour comes from the measured file: the deck as the
 * browser drew it from the slide blocks (foundations/nightlife-slides.css). This
 * file only translates. It chooses nothing, so it has nothing to drift from.
 */
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const [, , IN, OUT, CAPS_OUT] = process.argv;
const M = JSON.parse(fs.readFileSync(IN));
const ROOT = path.resolve(__dirname, "..", "..");
const SVG = fs.readFileSync(path.join(ROOT, "assets/logo/nightlife-culture-wordmark.svg"), "utf8");
const wordmark = hex => "data:image/svg+xml;base64," +
  Buffer.from(SVG.slice(SVG.indexOf("<svg")).replace(/currentColor/g, "#" + hex)).toString("base64");

const W = 13.333, H = 7.5;

// the browser's face and weight -> the face name Office resolves
function face(t) {
  if (t.family === "Archivo Black") return { fontFace: "Archivo Black", bold: false };
  if (t.family === "Archivo") return { fontFace: "Archivo", bold: t.weight >= 700 };
  if (t.weight >= 700) return { fontFace: "Inter", bold: true };
  if (t.weight >= 600) return { fontFace: "Inter SemiBold", bold: false };
  return { fontFace: "Inter", bold: false };
}

const pres = new pptxgen();
pres.defineLayout({ name: "NC", width: W, height: H });
pres.layout = "NC";
pres.author = "Carly Heath · Nightlife Culture";
pres.company = "Nightlife Culture";
pres.title = M.title;
const SEC = M.sections || { main: M.title };
pres.addSection({ title: SEC.main });
if (M.slides.some(s => s.optional)) pres.addSection({ title: SEC.optional || "Optional slides" });

const CAPS = [];
M.slides.forEach((s, ix) => {
  const inch = px => px * W / s.width;          // the slide is measured at whatever width the page gave it
  const pt = px => inch(px) * 72;
  const sl = pres.addSlide({ sectionTitle: s.optional ? (SEC.optional || "Optional slides") : SEC.main });
  sl.background = { color: s.ground.hex };
  const box = (r, c) => {
    const o = { x: inch(r.x), y: inch(r.y), w: inch(r.w), h: inch(r.h), fill: { color: c.hex }, line: { type: "none" } };
    if (c.a < 1) o.fill.transparency = Math.round((1 - c.a) * 100);   // the hairline: ink at its measured alpha
    sl.addShape(pres.shapes.RECTANGLE, o);
  };
  s.fills.forEach(f => box(f, f.c));
  s.rules.forEach(r => box(r, r.c));
  s.texts.forEach(t => {
    if (t.caps) CAPS.push({ slide: ix + 1, text: t.text });
    // a little extra width, so a renderer with marginally wider metrics keeps the browser's breaks
    const slack = Math.min(t.size * 0.6, 12 * s.width / 1280);
    const body = t.brk && t.brk.length > 1
      ? t.brk.map((ln, i) => ({ text: ln, options: i ? { softBreakBefore: true } : {} })) : t.text;
    sl.addText(body, {
      x: inch(t.x), y: inch(t.y), w: inch(t.w + slack), h: inch(t.h + t.lh * 0.25),
      ...face(t), fontSize: +pt(t.size).toFixed(1), color: t.color.hex,
      lineSpacing: +pt(t.lh).toFixed(1), charSpacing: t.ls ? +pt(t.ls).toFixed(2) : 0,
      align: "left", valign: "top", margin: 0, fit: "none", wrap: true,
      paraSpaceBefore: 0, paraSpaceAfter: 0,
    });
  });
  s.logos.forEach(g => sl.addImage({ data: wordmark(g.c.hex), x: inch(g.x), y: inch(g.y), w: inch(g.w), h: inch(g.h) }));
  // The slide number is a field, so it renumbers itself when slides move. Geometry of .nc-snum:
  // right 5.25%, bottom 5.333%, 1.667cqw (16pt), Archivo 700, the ground's own text colour.
  // None on the cover, and none on a closing band, where the wordmark holds that corner.
  if (ix > 0 && !s.band) {
    sl.slideNumber = { x: W * (1 - 0.0525) - 1, y: H * (1 - 0.05333) - 0.3, w: 1, h: 0.3,
      align: "right", valign: "bottom", margin: 0, fontFace: "Archivo", bold: true, fontSize: 16,
      color: s.textOn.hex };
  }
  if (s.notes) sl.addNotes(s.notes);
});

pres.writeFile({ fileName: OUT }).then(() => {
  fs.writeFileSync(CAPS_OUT, JSON.stringify(CAPS, null, 1));
  console.log(`  wrote ${path.basename(OUT)} · ${M.slides.length} slides · ${CAPS.length} caps strings`);
});
