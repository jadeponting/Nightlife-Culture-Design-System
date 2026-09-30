# Components — documents, panels, tables, stats

## Containment

**Contain with colour and space, not with outlines.** Hard black outlines are retired — they made
every panel shout at the same volume.

| Treatment | Class | Spec | Use |
|---|---|---|---|
| Fill | `.pnl` + accent bg | Accent background, no border | Default for accent panels. Needs generous surrounding space |
| Top rule | `.box` | White panel, 9px accent bar on top | Dense pages, tables, long documents |
| Left rule | `.callq` | White panel, 12px accent bar on left | Pull quotes, callouts, asides |
| Full-bleed band | — | Accent or ink, edge to edge | Slides and covers. How an accent leads without being a box |
| Hairline | `.hair` | 1px ink at 22% | White panels on chalk, tables, forms. Never for anything carrying meaning |
| Hard outline | — | — | **Retired** |

Ground pairing: **chalk ground + white panels** (no border needed), or **white ground + panels held
by a rule**.

## Layout rules
- One main idea per slide or section where possible
- Use space as part of the voice
- Blue is a structural signal, not scattered decoration
- Keep core information in a simple reading order
- Single-column for long-form accessible documents

---

## Tables

Five styles, one default. Tables carry a lot of this work — comparability gates, indicator sets,
recommendation logs — so they must stay readable for a long time.

| Style | Class | Spec | Use |
|---|---|---|---|
| **Editorial** | *(default)* | No fill, no vertical rules, 2.5px ink rule under header, hairlines between rows | **The default.** Anything else needs a reason |
| Chalk header | `.t-chalk` | Chalk header fill, hairline outline | A table that sits on a white page and needs a visible edge |
| Accent rule | `.t-accent` | Editorial + 7px accent bar on top | Colour-codes table families: teal = evidence, butter = funding, coral = risk |
| Banded | `.t-band` | Row banding at 3.5% ink, no row rules | Wide tables where the eye travels a long way across a row |
| Ink header | `.t-ink` | Solid ink header bar | Heaviest option. One summary table that must be found instantly. Not a default |

### Table rules
- The header row is a **real** header row — `<th>` in HTML, repeated header row in Word. Screen-reader
  requirement, not a style.
- The first column is bold: it names the row.
- Numbers right-aligned, monospaced, decimals lined up. Text left-aligned.
- No vertical rules unless the table is genuinely a grid read in both directions.
- Never band and rule at once.
- Suppressed → `[c]`. Not collected → `n/a`. **Never a blank cell.**
- A table over two pages repeats its header and does not split a row.

---

## Breakout statistics

A big number is the most-screenshotted thing Nightlife Culture produces. It carries its evidence
with it.

| Variant | Class | Use |
|---|---|---|
| Left rule | `.st` (+ `.acc-pink` / `.acc-teal` / `.acc-butter` / `.acc-coral`) | **Default.** In running text or a row of stats |
| Top rule | `.st2` | A stat sitting in a row of panels, or on a table-heavy page |
| Filled | `.stfill` | Slides and covers, where one number is the whole point. Accent ground, ink text |

### Rules
- The number is **Archivo Black**, at least 3× the label size.
- Label in Archivo ExtraBold caps, tracked, naming **what the number counts** — not a slogan.
- **Source line mandatory**: reference period, geography, boundary vintage, provenance code.
  A statistic without them is a claim, not a finding.
- Never all three variants on one page.
- **Never round to imply precision you do not have.** "About 30" is more honest than "31" if the
  estimate is modelled.
- **A range is a legitimate headline.** ±1.4 is a finding.

Markup:
```html
<div class="st acc-teal">
  <div class="big">±1.4</div>
  <div class="lb">Plausible range on the estimate</div>
  <div class="src">Modelled, not observed · harmonised across two classification sets</div>
</div>
```

---

## Pull quote

12px pink left rule, Archivo ExtraBold, max ~44 characters per line. The accent bar is the only
decorative use of pink and it is always at the top or the left, never both.

```html
<div class="q">Accessibility does not dilute the brand. It decides where the brand should live.</div>
```

---

## Document standards

**Word:** real Heading 1/2/3 styles · title, author and language in properties · built-in list styles ·
repeated table header rows · no spaces/tabs/blank paragraphs for layout · page breaks not returns ·
run the Accessibility Checker · **white ground, not chalk**.

**PDF:** export from a structured source, never print to PDF · verify tags, headings, reading order,
links, alt text, title and language · bookmarks in long reports · selectable text · check reflow.

**HTML:** primary public format · semantic headings, lists, tables, landmarks, descriptive links ·
preserve keyboard focus, zoom and reflow · **embed fonts as base64**.

---

## Accessibility

**Accessibility is a design standard, not finishing polish.** When brand and accessibility conflict,
accessibility wins — move the brand to layout, rhythm, typography, covers, pattern or non-essential
decoration rather than weakening the meaning layer.

| Class | Examples | Rule |
|---|---|---|
| Fixed | Semantic headings, readable size, contrast, links, reading order, focus states, alt text | Do not override for brand preference |
| Adaptable | Logo scale, exact tint, spacing, composition, chart styling | Adjust to user, format and need |
| Decorative | Patterns, textures, overlays, non-informational imagery | May be removed without losing meaning |

Minimum: WCAG 2.2 AA · real headings, lists and table structures · descriptive links, never "click
here" · useful alt text on meaningful images · no images of text · text or data alternatives for
charts · reading order checked before PDF publication · document title and language set · automated
checks **and** manual review.

---

## The seven tests

Run any output past these:

1. **Committee-room** — credible, decision-ready, defensible?
2. **Dancefloor** — retains cultural truth, avoids institutionalising the culture?
3. **Phone** — understandable quickly on a small screen?
4. **Screen-reader** — does the meaning survive without the visual treatment?
5. **Hostile-reader** — are the claims, sources and assumptions defensible under scrutiny?
6. **Partner** — does the language make room for collaboration and recognise others' contribution?
7. **Paid-work** — can the reader understand what Nightlife Culture can do and what to ask for?
