---
name: nightlife-culture-design
description: Apply the Nightlife Culture design system to branded documents, spreadsheets, presentations, websites, graphics and copy. Use for Nightlife Culture or Vibe Map assets and brand questions. This portable package is a versioned snapshot; use the live local skill when the design repo is available.
---

# Nightlife Culture Design System

A creative policy, research and design studio working across nightlife, music, culture, place and
the systems that shape them. Founder: Carly Heath.

This package is a generated snapshot of **Nightlife Culture Style Guide v1.5.1 (14 October 2026)**. Its `snapshot.json` records the source
and asset hashes at build time. It cannot check a private repo it cannot access. When the local
design repo is available, use the local entrypoint and check the current sources before building.

Preserve the settled rules. Known gaps and interim positions below remain provisional; do not
re-propose the palette, type or layout rules unless explicitly asked to change them.

---

## The six non-negotiables

Get these right and the work is on brand. Get one wrong and it is not.

1. **Every accent takes ink text. Every ground takes the text colour its own token declares — white on blue and ink, ink on chalk and white.**
   There is no single sentence covering all four grounds: blue takes white · ink takes white · chalk takes ink · white takes ink. White on chalk is 1.11:1 and white on white is 1.00:1 — the old one-line law is retired.
2. **Never encode data in the brand accents.** They are separated by hue alone and collapse in
   greyscale. Charts use the four-series ramp only.
3. **One rule for all type.** Every text style uses the named voices, sizes and roles, and
   every one has a name (`references/tokens.md`). A component never sets a typeface, a size, a
   weight or capitals; you pick the role. Capitals are Display, H1, H2, titles in contents and
   tables, and the label voice; H3, H4 and everything in the text voice are sentence case. Heading
   styles sit on their own element, h1 to h4. **There is no H5 or H6.** No monospace anywhere.
4. **Contain with colour and space, not outlines.** Hard black boxes are retired.
5. **Use the supplied fonts.** Embed `assets/fonts.css` in HTML; Office font delivery follows
   the format-specific route. Never link a web font service. Report any substitution or missing
   embedding rather than claiming identical typography.
6. **Slides come from patterns, not invention.** Build every slide from a pattern in
   `references/slides.md` and look at its reference image first. Statement slides stay mostly
   empty; working slides may carry up to eight short blocks. If it does not fit, it is two slides.
   Remove copy before reducing type.

---

## Tokens — generated reference

Read `references/tokens.md` for the palette, chart ramp, named type roles, line weights and
language rules. It is generated from `foundations/tokens.json`; values are not repeated here.
Read the source for the requested surface, including the named small-role exceptions to the
heading caps floor. Superseded colours and faces are listed in that reference too.

---

## Workflow

**1. Identify the output type**, then read the matching reference before building:

| Asked for | Read |
|---|---|
| Deck, slides, presentation | `references/slides.md` |
| Chart, graph, data, statistics | `references/charts.md` |
| Report, document, page, panel, table | `references/components.md` |
| Written copy of any kind | `references/voice.md` |
| Colour, contrast, type questions | `references/tokens.md` |

**2. Start from the assets, do not rebuild from scratch.**
- `assets/nc.css` — the design system's own generated stylesheet (`foundations/nightlife-culture.css`),
  copied at build time. Every class in the references is defined here. Use `<body class="nc-doc">`.
- `assets/fonts.css` — Archivo Black, Archivo 600/700/800, Inter 400/500/600/700 as base64
  `@font-face` rules. Inline this into any HTML deliverable.
- `assets/template.html` — a starter document with fonts, tokens and components already wired.
  Copy it and replace the content.
- `assets/nightlife-culture-wordmark.svg` — the outlined wordmark, `fill="currentColor"`.
  Place it inline and set `color` on the container. **Never re-type the logo in Archivo Black** —
  the two lines carry different sizes and per-line tracking that live type cannot reproduce.

**3. Check contrast before shipping** any new colour pairing:
`python scripts/contrast.py "#0000FF" "#FFFFFF"` → ratio and pass/fail at AA and AAA.

**4. Verify visually.** Render and look at it before delivering — screenshot HTML with Playwright,
or convert DOCX/PDF and read the pages. Do not ship a layout you have not seen.

---

## Output format defaults

- **HTML is the primary format** for anything public or reference-like. Self-contained, fonts
  embedded, semantic headings, real tables.
- **Word (.docx)** when a partner needs to edit or comment. White ground, not chalk.
- **Document mastheads sit on signal blue** — ink is the night register, not a default (decided 16 Aug 2026).
- **Document type is decided, not chosen per document:** 26 named roles from 5 voices at 6 sizes (32px · 24px · 18px · 16px · 14px · 12px), generated from tokens.json; every role in references/tokens.md with the Word style it becomes
- **Word styles are the roles.** The Word column in `references/tokens.md` names the style each role
  becomes: Heading 1–4, Subtitle, Normal, Quote, Intense Quote, Caption, Table style with Header Row
  and First Column, and the new styles Label, Small, Key statement and File reference.
- **Excel (.xlsx)** when requested. Use current table, colour and evidence rules; preserve
  formulas, values and number formats. This package has no general Excel template. In the local
  repo, read `docs/gaps.md` and inspect `adapters/excel/` before reuse: that adapter targets a
  specific budget workbook and carries an older default size. Do not treat it as the type-role
  authority.
- **Word and Excel:** their current adapters are document-specific, not complete templates
  generated from the roles. A new format-specific choice stays provisional until Carly decides.
- **PDF** exported from a structured source, never printed to PDF.
- **PowerPoint** only when the user asks for it. Build the slides in HTML from the patterns in
  `references/slides.md` first, check they fit, then rebuild each slide as **native, editable shapes
  and text at the positions the browser measured**. Never images of slides. In Office the faces are
  Archivo Black, Archivo (bold), Inter, and **Inter SemiBold** for Inter 600 (Office has no 600
  weight, only that face name). Capitals are the all-caps property, never typed. Speaker notes go
  in the notes; slide numbers are fields. Embed the faces, and send a PDF alongside for email.
  The design-system repo does this in `adapters/powerpoint/build_deck_pptx.py`.

---

## Voice, in one line

Nightlife Culture comes from inside the culture. Write for nightlife, to the people who decide about it:
speak the system's language well enough that the spreadsheet can't ignore you, and never let it speak for
you. Emotional arc: **joy → value → evidence → action**, as a direction of travel, not a running order.
Before writing any copy, read `references/voice.md` in full, including *Original thinking is not raw
material to be sanitised* and the Carly test.

Avoid AI voice: "this matters", "in today's rapidly changing landscape", "unlock the potential",
"at the heart of", "more important than ever", and repetitive three-part slogans.

---

## Evidence is part of the design

Nightlife Culture's credibility depends on evidence being visible, not just accurate. Strong design
must never make weak evidence look stronger than it is.

- Every chart carries a **provenance code**, reference period, geography and boundary vintage.
- Every comparison between places declares whether the **comparability gate** was cleared.
- Every big number carries a **source line**. A statistic without one is a claim, not a finding.
- Suppressed data is hatched and marked `[c]`. Not collected is marked `n/a`. Never a blank.
- Illustrative or placeholder figures say so, in the chart, every time.

Full detail in `references/charts.md`.

---

## When there is no rule

The system is deliberately incomplete, and an undecided surface gets an interim position, not an
invention (Decision Book TYP-20, TYP-22). When a piece of work needs something the system does not
cover:

1. **Say so first**, in the reply, before building anything: "there is no rule for X".
2. **Build the nearest thing from what exists**: the five voices, the six sizes, the four lines, the
   components and the colours as they are. Never a new colour, a new size, a new weight or a new
   typeface. Never monospace. Never a browser default.
3. **Show it as an option, with what it costs**, built with the design system's own stylesheet, not
   described in prose. Two options at most, differing in one thing.
4. **Mark it in the artefact**: a Claude note (`.nc-claude-note`) saying the rule is provisional and
   which decision it is waiting on.
5. **Log it**: name the surface it came from and the option taken, so the design system can add it to
   `docs/gaps.md`. The gap closes when Carly decides, not when the output ships.

Known gaps today, each with an interim position:

- **Public severity marks.** Internal coloured chips carry the word; a public document gets no
  coloured severity until one is decided against a real case. Never RAG tags.
- **Other button styles and the icon set.** One blue button and one text action exist; the search
  icon is the only icon.
- **Ink and charcoal** are visually close; both stay until decided.
- **Diagram kit.** None exists. Build process chains, funnels and timelines from the containment
  treatments and the chart ramp. Never PowerPoint SmartArt defaults.
- **Office templates.** The Word, Excel and PowerPoint adapters each build one document and carry
  style sets of their own; templates generated from the roles are the next piece of work.

---

## Source of truth

**Nightlife Culture Style Guide v1.5.1 (14 October 2026)** — the full guide, with `foundations/tokens.json` (the type roles and line weights),
`foundations/rules.json` (98 rules, tiered and sourced) and `foundations/type-manifest.json` (every
text style marked Specified, Inherits or Barred) in the design-system repo. Where this skill and the
guide disagree, the guide wins. Where the guide and `Comparative Place-Based Research Methodology
v1.0` touch, the methodology wins. Superseded: v1.4, v1.4.1 and the unadopted v1.4.2 draft, in
`archive/`; v1.5 (5 October 2026), amended by v1.5.1 in the voice and editorial sections only.
