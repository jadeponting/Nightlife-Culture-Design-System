---
name: nightlife-culture-design
description: The Nightlife Culture brand and design system — colour tokens, typography, layout, containment, breakers, slides, charts, tables and evidence components, plus voice and editorial rules. Use this skill whenever producing ANYTHING for Nightlife Culture or Carly Heath: decks, slides, presentations, reports, Word documents, PDFs, HTML pages, charts, graphs, tables, statistics, infographics, proposals, funding bids, briefings, one-pagers, social graphics, or written copy. Also use when asked about brand colours, fonts, the palette, "on brand", the style guide, chart colours, slide layouts, or how something should look. Trigger even when the user does not say "brand" or "design system" — if the output carries the Nightlife Culture name, it must follow this system.
---

# Nightlife Culture Design System

A creative policy, research and design studio working across nightlife, music, culture, place and
the systems that shape them. Founder: Carly Heath.

Everything below is settled. Do not re-derive, re-propose or "improve" the palette, type or layout
rules unless explicitly asked to change them.

---

## The six non-negotiables

Get these right and the work is on brand. Get one wrong and it is not.

1. **{{LAW}}**
   {{LAW_DETAIL}}
2. **Never encode data in the brand accents.** They are separated by hue alone and collapse in
   greyscale. Charts use the four-series ramp only.
3. **All-caps for Display, H1, H2 and labels — always tracked, never below 16pt, eight words max.**
   H3 and body are sentence case. Never caps in body, captions, source lines or table cells.
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

**Type:** Archivo Black (display) · Archivo ExtraBold 800 (H1/H2) · Archivo Bold 700 (H3) ·
Inter 400 (body) · Archivo SemiBold 600 (labels).

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
- `assets/nc.css` — the full component stylesheet. Every class in the references is defined here.
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
- **Document type scale is decided, not chosen per document:** {{TYPESCALE_LINE}}
- **PDF** exported from a structured source, never printed to PDF.
- **PowerPoint** only when the user asks for it. Build from the patterns in `references/slides.md`.

---

## Voice, in one line

Able to move between the dancefloor, the committee room, the funder meeting and the evidence base
without losing the truth of the culture. Emotional arc: **joy → value → evidence → action.**

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

## Known gaps

If asked for something this system does not cover, build from the nearest existing components and
say that the rule is provisional:

- **Diagram kit.** No diagram system exists yet. Build process chains, funnels and timelines from
  the containment treatments and the chart ramp. Never use PowerPoint SmartArt defaults — they
  override colour, type, spacing and outlines.

---

## Source of truth

**{{SOURCE}}** — the full guide, plus its machine-readable rule register
(`foundations/v1.4-register.json` in the design-system repo, 458 statements). Where this skill and the guide disagree, the guide wins. Where the guide and
`Comparative Place-Based Research Methodology v1.0` touch, the methodology wins.
