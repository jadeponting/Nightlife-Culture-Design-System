---
name: nightlife-culture-design
description: The Nightlife Culture brand and design system (Style Guide v1.5.1) — colour tokens, the five type voices and 26 named roles, four line weights, layout, containment, breakers, slides, charts, tables, status chips, controls and evidence components, plus voice and editorial rules and what to do when there is no rule. Use this skill whenever producing ANYTHING for Nightlife Culture or Carly Heath: decks, slides, presentations, reports, Word documents, PDFs, HTML pages, charts, graphs, tables, statistics, infographics, proposals, funding bids, briefings, one-pagers, social graphics, or written copy. Also use when asked about brand colours, fonts, the palette, "on brand", the style guide, chart colours, slide layouts, or how something should look. Trigger even when the user does not say "brand" or "design system" — if the output carries the Nightlife Culture name, it must follow this system.
---

# Nightlife Culture Design System

A creative policy, research and design studio working across nightlife, music, culture, place and
the systems that shape them. Founder: Carly Heath.

Everything below is settled. Do not re-derive, re-propose or "improve" the palette, type or layout
rules unless explicitly asked to change them.

---

## The six non-negotiables

Get these right and the work is on brand. Get one wrong and it is not.

1. **Every accent takes ink text. Every ground takes the text colour its own token declares — white on blue and ink, ink on chalk and white.**
   There is no single sentence covering all four grounds: blue takes white · ink takes white · chalk takes ink · white takes ink. White on chalk is 1.11:1 and white on white is 1.00:1 — the old one-line law is retired.
2. **Never encode data in the brand accents.** They are separated by hue alone and collapse in
   greyscale. Charts use the four-series ramp only.
3. **One rule for all type.** Every text style is one of five voices at one of six sizes, and
   every one has a name (`references/tokens.md`). A component never sets a typeface, a size, a
   weight or capitals; you pick the role. Capitals are Display, H1, H2, titles in contents and
   tables, and the label voice; H3, H4 and everything in the text voice are sentence case. Heading
   styles sit on their own element, h1 to h4. **There is no H5 or H6.** No monospace anywhere.
4. **Contain with colour and space, not outlines.** Hard black boxes are retired.
5. **Embed fonts as base64 in every digital deliverable.** Never link Google Fonts — it fails
   silently and falls back to a system sans without warning.
6. **Slides come from patterns, not invention.** Build every slide from a pattern in
   `references/slides.md` and look at its reference image first. Statement slides stay mostly
   empty; working slides may carry up to eight short blocks. If it does not fit, it is two slides.
   Remove copy before reducing type.

---

## Tokens — quick reference

| Token | Hex | Role | Text on it |
|---|---|---|---|
| Signal blue | `#0000FF` | Primary ground. Covers, dividers, statements, links | White only · 8.59:1 |
| Ink | `#0D0D0D` | Night ground + primary text | White only · 19.44:1 |
| Chalk | `#F3F3F3` | Reading ground — decks and screen | Ink/charcoal · 17.52:1 |
| White | `#FFFFFF` | Reading ground — reports and print; panels on chalk | Ink/charcoal · 19.44:1 |
| Charcoal | `#2D2D2D` | Secondary copy, captions, slide titles on light | On light · 12.41:1 |
| Counter pink | `#ED77C2` | Hot counter-signal, accent bars, left rules | Black only · 7.42:1 |
| Signal teal | `#53E6E5` | Cool highlight, section headers on dark grounds | Black only · 12.79:1 |
| Soft violet | `#B98CFF` | Calm surface, blocks, vertical thirds | Black only · 7.64:1 |
| Butter | `#FFDE6B` | Opportunity, funding, forward motion | Black only · 14.73:1 |
| Coral | `#FD7B53` | Urgency, risk, lowest provenance tier | Black only · 7.53:1 |

**Chart ramp** (data only): `#0000FF` → `#C7339A` → `#00C6C5` → `#FFDE6B`. Four series maximum.

**Type:** five voices · Display: Archivo Black, capitals, covers only · Capitals: Archivo ExtraBold
800 (H1 32px, H2 24px, contents and table titles 14px, numbers 12px) · Sentence: Archivo Bold 700
(H3 18px, H4 16px, takeaway, key statement, button) · Text: Inter 400 (subtitle 18px, body 16px,
table cells and small 14px; bold 700 for the first column of a table; italic for a short run) ·
Label: Archivo SemiBold 600, capitals, spaced, 12px. Six sizes and no others: 32 · 24 · 18 · 16 · 14 · 12px
(24 · 18 · 13.5 · 12 · 10.5 · 10pt).

**Lines:** four weights and no others · hairline 1px · table line 2px · rule 4px (a line that goes
with text) · callout 8px (a line on a filled box).

**Language:** British English · **night time** is two words, never hyphenated · cultural value and
cultural contribution are not interchangeable: use the one you mean.

Retired and never to be reintroduced: `#920DFF`, `#F26B43`, `#FFD100`, `#F6F6EE` cream, Aptos.

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
  not a copy. Every class in the references is defined here. Use `<body class="nc-doc">`.
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
