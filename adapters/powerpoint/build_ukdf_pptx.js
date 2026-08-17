/* The UKDF proposal deck, as a real PowerPoint file.
 *
 * Content: adapters/powerpoint/ukdf-content.json — Master Framework §14, verbatim.
 * Colours and grid: foundations/tokens.json. Nothing is chosen here.
 * v1.4 floors: slide titles 32pt min, body 18pt min, labels 16pt.
 * Caps are applied afterwards as the OOXML all-caps property (postprocess_caps.py),
 * never typed, so the underlying text stays sentence case (NC-TYP-01).
 */
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const T = JSON.parse(fs.readFileSync(path.join(ROOT, "foundations/tokens.json")));
const C = T.colour;
const G = Object.fromEntries(Object.entries(C.grounds).map(([k, v]) => [k, v.hex.slice(1)]));
const A = Object.fromEntries(Object.entries(C.accents).filter(([k,v])=>v.hex).map(([k, v]) => [k, v.hex.slice(1)]));
const CHARCOAL = C.textColours.charcoal.hex.slice(1);
const CONTENT = JSON.parse(fs.readFileSync(path.join(__dirname, "ukdf-content.json")));

const W = 13.333, H = 7.5;
const S = T.space.slide;
const pc = s => parseFloat(s) / 100;
const SIDE = pc(S.sideMargin) * W;                 // 0.70in
const TOP_K = pc(S.topMargin.kickerLeads) * H;     // 0.30in
const TOP_T = pc(S.topMargin.titleLeads) * H;      // 0.50in
const BAND = pc(S.footerBand) * H;                 // 1.00in
const BASE = pc(S.footerBaseline) * H;             // 0.40in
const CW = W - 2 * SIDE;

const F_DISPLAY = "Archivo Black", F_HEAD = "Archivo", F_BODY = "Inter";
const on = g => (g === "blue" || g === "ink") ? "FFFFFF" : G.ink.toUpperCase();
const kickCol = g => (g === "blue" || g === "ink") ? A.teal : G.blue;
const ACC = [A.teal, A.butter, A.pink, A.violet, A.coral];

const pres = new pptxgen();
pres.defineLayout({ name: "NC", width: W, height: H });
pres.layout = "NC";
pres.author = "Carly Heath · Nightlife Culture";
pres.title = "Artists Make Great Places — UKDF Fellowship proposal";

const CAPS = [];   // {slide, text} pairs that take cap="all" in post
let SLIDE_IX = 0;
const capText = t => { CAPS.push({ slide: SLIDE_IX, text: t }); return t; };

function ground(sl, g) { sl.background = { color: G[g] }; }

function footer(sl, g, num) {
  const dark = (g === "blue" || g === "ink");
  sl.addImage({ path: path.join(__dirname, `wordmark-${dark ? "white" : "blue"}.png`),
    x: SIDE, y: H - BASE - 0.32, w: 0.95, h: 0.39 });
  if (num) sl.addText(String(num).padStart(2, "0"), {
    x: W - SIDE - 1, y: H - BASE - 0.32, w: 1, h: 0.35, align: "right",
    fontFace: F_HEAD, bold: true, fontSize: 14, charSpacing: 2,
    color: dark ? A.teal : CHARCOAL, margin: 0 });
}

function kicker(sl, g, txt, y = TOP_K) {
  sl.addText(capText(txt), { x: SIDE, y, w: CW, h: 0.35, fontFace: F_HEAD, bold: true,
    fontSize: 16, charSpacing: 4, color: kickCol(g), margin: 0 });
}

function breaker(sl, g, y, wIn = 2.2, colour) {
  sl.addShape("rect", { x: SIDE, y, w: wIn, h: 0.06,
    fill: { color: colour || (g === "blue" || g === "ink" ? A.teal : G.blue) } });
}

const B = { title: 40, big: 54, body: 20, panel: 18, label: 16 };

CONTENT.slides.forEach(sp => {
  SLIDE_IX += 1;
  const sl = pres.addSlide();
  const g = sp.ground || "blue";
  ground(sl, g);
  sl.addNotes(`${sp.job}  ${sp.visual}`);

  if (sp.kind === "cover") {
    sl.addImage({ path: path.join(__dirname, "wordmark-white.png"),
      x: SIDE, y: pc(S.topMargin.fullBleedLeads) * H, w: 2.3, h: 0.95 });
    sl.addText(capText(sp.title), { x: SIDE, y: 2.9, w: CW, h: 2.2, fontFace: F_DISPLAY,
      fontSize: 66, color: "FFFFFF", lineSpacing: 62, margin: 0 });
    breaker(sl, g, 5.15);
    sl.addText(sp.sub, { x: SIDE, y: 5.4, w: CW * 0.62, h: 0.7, fontFace: F_HEAD, bold: true,
      fontSize: 22, color: "FFFFFF", margin: 0 });
    sl.addText(capText(sp.meta), { x: SIDE, y: H - BASE - 0.3, w: CW - 1.2, h: 0.3,
      fontFace: F_HEAD, bold: true, fontSize: 14, charSpacing: 3, color: A.teal, margin: 0 });
  }

  if (sp.kind === "statement") {
    const big = sp.title.length > 30;
    sl.addText(capText(sp.title), { x: SIDE, y: 1.5, w: CW, h: 2.6, fontFace: F_DISPLAY,
      fontSize: big ? 44 : B.big, color: g === "ink" ? A.teal : on(g),
      lineSpacing: big ? 46 : 54, margin: 0 });
    breaker(sl, g, 4.35);
    sl.addText(sp.body, { x: SIDE, y: 4.6, w: CW * 0.78, h: 1.6, fontFace: F_HEAD, bold: true,
      fontSize: 22, color: on(g), lineSpacing: 30, margin: 0 });
    footer(sl, g, sp.n);
  }

  if (sp.kind === "titlebody") {
    sl.addText(capText(sp.title), { x: SIDE, y: TOP_T + 0.15, w: CW, h: 1.9, fontFace: F_DISPLAY,
      fontSize: B.title, color: g === "ink" ? A.teal : (g === "chalk" || g === "white" ? CHARCOAL : on(g)),
      lineSpacing: 42, margin: 0 });
    breaker(sl, g, 3.15);
    sl.addText(sp.body, { x: SIDE, y: 3.45, w: CW * 0.8, h: 2.2, fontFace: F_BODY,
      fontSize: B.body, color: on(g), lineSpacing: 30, margin: 0 });
    if (sp.body2) sl.addText(sp.body2, { x: SIDE, y: 5.35, w: CW * 0.8, h: 1.1, fontFace: F_BODY,
      fontSize: 18, color: CHARCOAL, lineSpacing: 26, margin: 0 });
    footer(sl, g, sp.n);
  }

  if (sp.kind === "bullets") {
    const long = sp.title.length > 45;
    sl.addText(capText(sp.title), { x: SIDE, y: TOP_T + 0.15, w: CW, h: long ? 1.9 : 1.5,
      fontFace: F_DISPLAY, fontSize: long ? 32 : B.title,
      color: g === "ink" ? A.teal : (g === "chalk" || g === "white" ? CHARCOAL : on(g)),
      lineSpacing: long ? 36 : 42, margin: 0 });
    const y0 = long ? 2.85 : 2.5;
    breaker(sl, g, y0 - 0.25);
    sl.addText(sp.bullets.map((b, i) => ({
      text: b, options: { bullet: { characterCode: "2014", indent: 28 },
        breakLine: true, paraSpaceAfter: 12 } })),
      { x: SIDE, y: y0, w: CW * 0.86, h: H - BAND - y0 - 0.1, fontFace: F_BODY,
        fontSize: B.body, color: on(g), lineSpacing: 27, margin: 0, valign: "top" });
    footer(sl, g, sp.n);
  }

  if (sp.kind === "pathway") {
    sl.addText(capText(sp.title), { x: SIDE, y: TOP_T + 0.15, w: CW, h: 1.5, fontFace: F_DISPLAY,
      fontSize: B.title, color: CHARCOAL, lineSpacing: 42, margin: 0 });
    const n = sp.stages.length;
    const gap = n > 5 ? 0.14 : 0.28, cw = (CW - gap * (n - 1)) / n, y = 3.6, hC = H - BAND - y - 0.25;
    sp.stages.forEach((st, i) => {
      sl.addShape("rect", { x: SIDE + i * (cw + gap), y, w: cw, h: hC,
        fill: { color: ACC[i % ACC.length] } });
      sl.addText(capText(st), { x: SIDE + i * (cw + gap) + 0.06, y: y + 0.15, w: cw - 0.12,
        h: hC - 0.3, fontFace: F_HEAD, bold: true,
        fontSize: n > 5 ? 14 : 18, charSpacing: n > 5 ? 0.25 : 2, color: G.ink.toUpperCase(),
        valign: "middle", align: "center", margin: 0 });
      if (i < n - 1) sl.addText("→", { x: SIDE + (i + 1) * (cw + gap) - gap, y: y + hC / 2 - 0.2,
        w: gap, h: 0.4, fontSize: 16, color: CHARCOAL, align: "center", margin: 0, fontFace: F_BODY });
    });
    footer(sl, g, sp.n);
  }

  if (sp.kind === "twolane") {
    sl.addText(capText(sp.title), { x: SIDE, y: TOP_T + 0.15, w: CW, h: 1.5, fontFace: F_DISPLAY,
      fontSize: 36, color: CHARCOAL, lineSpacing: 40, margin: 0 });
    const gap = 0.4, cw = (CW - gap) / 2, y = 3.1, hC = H - BAND - y - 0.25;
    sp.lanes.forEach(([who, what], i) => {
      const laneOpts = { x: SIDE + i * (cw + gap), y, w: cw, h: hC,
        fill: { color: i === 0 ? "FFFFFF" : A.teal } };
      if (i === 0) laneOpts.line = { color: G.ink.toUpperCase(), width: 0.75, transparency: 78 };
      sl.addShape("rect", laneOpts);
      sl.addText(capText(who), { x: SIDE + i * (cw + gap) + 0.3, y: y + 0.3, w: cw - 0.6, h: 0.4,
        fontFace: F_HEAD, bold: true, fontSize: 18, charSpacing: 2, color: G.ink.toUpperCase(), margin: 0 });
      sl.addText(what, { x: SIDE + i * (cw + gap) + 0.3, y: y + 0.85, w: cw - 0.6, h: hC - 1.1,
        fontFace: F_BODY, fontSize: 18, color: G.ink.toUpperCase(), lineSpacing: 25, margin: 0 });
    });
    footer(sl, g, sp.n);
  }

  if (sp.kind === "panels") {
    sl.addText(capText(sp.title), { x: SIDE, y: TOP_T + 0.1, w: CW, h: 0.85, fontFace: F_DISPLAY,
      fontSize: 36, color: A.teal, margin: 0 });
    // Five generous bands, one per strand, in strand order. A band keeps the
    // 44-word descriptions at a readable size where five columns could not.
    const y0 = 1.62, gap = 0.12, hB = (H - BAND - y0 - 0.1 - gap * 4) / 5;
    sp.panels.forEach(([l, d], i) => {
      const yy = y0 + i * (hB + gap);
      sl.addShape("rect", { x: SIDE, y: yy, w: CW, h: hB, fill: { color: ACC[i % ACC.length] } });
      sl.addText(capText(l), { x: SIDE + 0.25, y: yy, w: 2.7, h: hB, valign: "middle",
        fontFace: F_HEAD, bold: true, fontSize: 14, charSpacing: 1,
        color: G.ink.toUpperCase(), lineSpacing: 16, margin: 0 });
      sl.addText(d, { x: SIDE + 3.15, y: yy + 0.08, w: CW - 3.4, h: hB - 0.16, valign: "middle",
        fontFace: F_BODY, fontSize: 14, color: G.ink.toUpperCase(), lineSpacing: 17, margin: 0 });
    });
    footer(sl, g, sp.n);
  }

  if (sp.kind === "close") {
    sl.addText(capText(sp.title), { x: SIDE, y: 0.9, w: CW, h: 1.9, fontFace: F_DISPLAY,
      fontSize: 48, color: "FFFFFF", lineSpacing: 52, margin: 0 });
    breaker(sl, g, 2.95, 2.2, A.pink);
    sl.addText(sp.bullets.map(b => ({ text: b,
      options: { bullet: { characterCode: "2014", indent: 26 }, breakLine: true, paraSpaceAfter: 8 } })),
      { x: SIDE, y: 3.2, w: CW * 0.62, h: 2.3, fontFace: F_BODY, fontSize: 16,
        color: "FFFFFF", lineSpacing: 20, margin: 0, valign: "top" });
    sl.addText(sp.closeline, { x: SIDE, y: H - BAND - 0.62, w: CW * 0.85, h: 0.5,
      fontFace: F_HEAD, bold: true, fontSize: 20, color: A.teal, margin: 0 });
    footer(sl, g, null);
  }
});

const out = path.join(ROOT, "dist", "UKDF_Fellowship_Proposal_Artists_Make_Great_Places_V2.pptx");
pres.writeFile({ fileName: out }).then(() => {
  fs.writeFileSync(path.join(__dirname, "caps-manifest.json"), JSON.stringify(CAPS, null, 1));
  console.log("wrote", out);
  console.log("caps manifest:", CAPS.length, "strings to transform");
});
