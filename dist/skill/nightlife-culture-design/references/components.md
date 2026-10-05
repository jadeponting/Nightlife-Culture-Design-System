# Components — documents, panels, tables, stats, controls

Everything here is a class in `assets/nc.css`, which is the design system's own generated stylesheet
(`foundations/nightlife-culture.css`), not a copy. Wrap a document in `<body class="nc-doc">` and
`<div class="nc-wrap">`; the masthead is `<header class="nc-mast">`.

## The one rule for type (v1.5)

Every text style is **one of five voices at one of six sizes**, and every one has a name that says
what it is. A component may place text, colour it and put a line beside it. **It never sets a
typeface, a size, a weight or capitals.** If you find yourself writing `font-size`, `font-weight`
or `text-transform`, stop: pick the role instead. The full table is `references/tokens.md`.

| Voice | Face | Roles |
|---|---|---|
| Display | Archivo Black, capitals, sized to the cover | `.nc-display` — covers and mastheads only |
| Capitals | Archivo ExtraBold 800, capitals | `.nc-heading-1` 32px · `.nc-heading-2` 24px · `.nc-contents-title` 14px · `.nc-table-title` 14px · `.nc-number` 12px |
| Sentence | Archivo Bold 700, sentence case | `.nc-heading-3` 18px · `.nc-heading-4` 16px (blue bar above) · `.nc-takeaway` · `.nc-key-statement` · `.nc-button` · `.nc-text-action` |
| Text | Inter Regular 400 | `.nc-subtitle` 18px · `.nc-body` 16px · `.nc-quotation` · `.nc-list-item` · `.nc-table-cell` 14px · `.nc-table-first-column` (bold) · `.nc-file-reference` · `.nc-small` 14px charcoal |
| Label | Archivo SemiBold 600, capitals, spaced, 12px | `.nc-label` · `.nc-table-header-row` · `.nc-chip` · `.nc-evidence-mark` · `.nc-attribution` · `.nc-running-foot` |

**Headings sit on their own element**: `.nc-heading-1` on `<h1>` through `.nc-heading-4` on `<h4>`.
**H4 is the floor. There is no H5 or H6.** If the content seems to need one, it needs a new
section, a list or a table instead.

**Emphasis.** Italic (`<em>`) for a short run inside a paragraph: a quoted phrase, a title, a word.
Bold inside a paragraph is rare. **No monospace anywhere** — a file name or literal string is
`<code class="nc-file-reference">`, a white hairline chip in Inter; figures are Inter with tabular
figures (`.nc-figure-cell` in a table).

**Night time** is two words, never hyphenated. British English. "Cultural value", not "cultural
contribution".

## Section header

```html
<h2 class="nc-section-head nc-heading-2">
  <span class="nc-number-slot"><span class="nc-number">01</span></span>
  <span class="nc-section-title">Section title</span>
</h2>
```
Rule below at the rule weight (4px). The number is optional (an invented number is worse than none)
and is centred on the first line of the title however many lines it runs to. Same markup on `<h3
class="nc-section-head nc-heading-3">` for a sub-section that wants a rule.

## Four weights of line

| Weight | Size | What it is for |
|---|---|---|
| Hairline | 1px | Table rows, contents rows, outlines, the foot of a page. Never carries meaning |
| Table line | 2px | Under a table's header row |
| Rule | 4px | A line that goes with text: section title, H4 bar, breaker, rail marker, quotation |
| Callout | 8px | A line on a filled box, top or left: key statement, callout, recommendation, statistic, chart card |

No fifth weight. The tokens are `--nc-line-hair`, `--nc-line-table`, `--nc-line-rule`, `--nc-line-callout`.

## Containment

**Contain with colour and space, not with outlines.** Hard outlines are retired; the hairline is the
only outline. Colour comes from an accent modifier (`acc-pink` `acc-teal` `acc-violet` `acc-butter`
`acc-coral` `acc-blue`), never from the component.

| Treatment | Class | Use |
|---|---|---|
| Fill | `.nc-panel.nc-panel--fill` + `acc-*` | Default for accent panels. Ink text. Needs space around it |
| Top rule | `.nc-panel.nc-panel--top` + `acc-*` | White panel, callout line on top. Dense pages, tables, long documents |
| Left rule | `.nc-panel.nc-panel--left` + `acc-*` | White panel, callout line on the left. Callouts and asides |
| Hairline | `.nc-panel.nc-panel--hair` | White panel on chalk. Never for anything carrying meaning |
| Band | `.nc-band` + `acc-*` | Edge to edge. A change of ground, not a panel |
| Key statement | `.nc-key-statement-panel` containing `<p class="nc-key-statement">` | The question or point a chapter turns on. Violet top rule by default |
| Recommendation | `.nc-recommendation` with `<span class="nc-chip nc-chip--conclusion">Recommendation</span>` then `.nc-body` | Blue left rule. A recommendation and why |
| Claude note | `.nc-claude-note` with `<p class="nc-label">Claude note · not for publication</p>` then `.nc-small` | Coral left rule. Working notes that must not reach the final artefact. Hidden in print |

Inside a panel, text takes a role as anywhere else: `.nc-label` for the heading line, `.nc-body` for
the text.

## Quotes

Two text roles in one frame, in the running text at body size, with a pink rule at the rule weight.
Not necessarily boxed.

```html
<blockquote class="nc-quote">
  <p class="nc-takeaway">A sentence to remember, in bold.</p>
  <footer class="nc-attribution">Who said it · where</footer>
</blockquote>
<blockquote class="nc-quote">
  <p class="nc-quotation">A quotation that runs on, at regular weight.</p>
  <footer class="nc-attribution">Who said it · where</footer>
</blockquote>
```
An evidence mark inside a sentence is the label voice in brackets:
`<span class="nc-evidence-mark">[Measured · internal analytics]</span>`.

## Tables

Editorial is the default and needs no modifier: no fill, no vertical rules, no outer border.

```html
<div class="nc-table-scroll"><table class="nc-table">
  <caption class="nc-table-title">Table 1 · What the table shows</caption>
  <thead><tr><th scope="col">Actor</th><th scope="col" class="nc-figure-cell">Index</th></tr></thead>
  <tbody><tr><th scope="row">Venues</th><td class="nc-figure-cell">82.4</td></tr></tbody>
</table></div>
<p class="nc-small">[c] suppressed for disclosure control · n/a not collected.</p>
```

- The **title** sits above, in `.nc-table-title` (capitals, 14px). Keep it short.
- The **header row** is real `<th scope="col">` cells; they take the label voice and the 2px table line automatically.
- The **first column** is `<th scope="row">` (or the first `<td>`): bold, because it names the row.
- Figures right-aligned with tabular figures: `.nc-figure-cell` on the heading and the cells.
- Notes under the table in `.nc-small`.
- Variants: `.nc-table--accent` (callout line on top, `acc-*`) for a table that opens a section; `.nc-table--band` for long reference tables. **Never band and rule at once.**
- Suppressed → `[c]`. Not collected → `n/a`. Never a blank cell.
- In Word: a real table style with Header Row and First Column, header row repeating across pages.

## Breakout statistics

```html
<div class="nc-stat acc-teal">
  <p class="big">±1.4</p>
  <p class="lb">Plausible range on the estimate</p>
  <p class="src">Modelled, not observed · harmonised across two classification sets</p>
</div>
```
`.nc-stat` left callout line (default) · `.nc-stat--top` · `.nc-stat--fill` (accent ground). The big
figure is a chart mark in Archivo Black; the label and source line are the label and small roles.
**Source line mandatory.** One hero statistic per document. Never round to imply precision you do
not have; a range is a legitimate headline.

## Status chips, button, search

```html
<span class="nc-chip nc-chip--to-do">To do</span> <span class="nc-chip nc-chip--in-progress">In progress</span>
<span class="nc-chip nc-chip--review">Review</span> <span class="nc-chip nc-chip--blocked">Blocked</span>
<span class="nc-chip nc-chip--done">Done</span> <span class="nc-chip nc-chip--parked">Parked</span>
<span class="nc-chip nc-chip--proposed">Proposed</span> <span class="nc-chip nc-chip--settled">Agreed</span>
<span class="nc-chip nc-chip--conclusion">Recommendation</span>
```
The word carries the meaning, never the colour alone. Agreed and Your answer (`--settled`) are the
inverse of the ground. Public severity marks are **not decided**: do not invent RAG tags.

```html
<div class="nc-action-row">
  <button type="button" class="nc-button">Read chapter two</button>
  <button type="button" class="nc-text-action">Collapse all</button>
</div>
<div class="nc-search"><label class="nc-label" for="q">Search the whole book</label>
  <div class="nc-search-row"><input class="nc-body" id="q" type="search" placeholder="…">
  <button type="button" class="nc-search-button" aria-label="Search"><!-- magnifier svg --></button></div></div>
```
One button, blue and fully rounded. The text action is the same voice, underlined. Other button
styles and an icon set are not decided.

## Headings that open and close

```html
<details class="nc-collapsible" open>
  <summary><h3 class="nc-heading-3">How the decision is made</h3></summary>
  …content, in line with the heading…
</details>
```
Any heading level; the heading keeps the style of its level. A heading that holds the finding starts
open. Everything prints open.

## Contents and running foot

```html
<nav class="nc-contents" aria-label="Contents">
  <a href="#ch1"><span class="nc-contents-title">
    <span class="nc-number-slot"><span class="nc-number nc-number-box">01</span></span>
    <span>Chapter title</span>
    <span class="nc-number-slot"><span class="nc-number nc-page-number">p. 04</span></span>
  </span><span class="nc-small">The chapter's one-line claim</span></a>
</nav>
<div class="nc-foot"><span class="nc-running-foot">Nightlife Culture · Section</span><span class="nc-running-foot">v1.5 · date · 07</span></div>
```
Add `nc-contents--rail` and `aria-current="true"` on the current chapter for a side rail.

## Lists, links, figures

- `<ul class="nc-list"><li class="nc-list-item">` — indented list paragraphs; `nc-list--num` for numbered.
- `<a class="nc-link">` — purpose clear from the text alone; never "click here". White on dark grounds.
- `<figure class="nc-figure">` with `<figcaption class="nc-small">`; alt text states the finding.

## Dark grounds

On `ground-ink` and `ground-blue` every text role, label and link is white; the number box and the
line under a section title are teal. A white panel or an accent fill on a dark ground takes ink text
again. You do not set any of this: the ground class does.

## Document standards

**Word:** real named styles only — the Word column in `references/tokens.md` is the style name for
each role · title, author and language in properties · built-in list styles · table styles with Header
Row and First Column, header row repeating · page breaks not returns · run the Accessibility Checker ·
**white ground, not chalk**.

**PDF:** export from a structured source, never print to PDF · verify tags, headings, reading order,
links, alt text, title and language · bookmarks in long reports · check reflow.

**HTML:** primary public format · semantic headings (h1 to h4), lists, tables, landmarks, descriptive
links · keyboard focus, zoom and reflow preserved · **embed fonts as base64**.

## Accessibility

**Accessibility is a design standard, not finishing polish.** When brand and accessibility conflict,
accessibility wins — move the brand to layout, rhythm, typography, covers, pattern or non-essential
decoration rather than weakening the meaning layer.

| Tier | Examples | Rule |
|---|---|---|
| Fixed | Semantic headings, readable size, contrast, links, reading order, focus states, alt text | Do not override for brand preference |
| Adaptable | Logo scale, exact tint, spacing, composition, chart styling | Adjust to user, format and need |
| Decorative | Patterns, textures, overlays, non-informational imagery | May be removed without losing meaning |

Minimum: WCAG 2.2 AA · real headings, lists and table structures · descriptive links · useful alt
text · no images of text · text or data alternatives for charts · reading order checked before PDF
publication · document title and language set · automated checks **and** manual review.

## The seven tests

1. **Committee-room** — credible, decision-ready, defensible?
2. **Dancefloor** — retains cultural truth, avoids institutionalising the culture?
3. **Phone** — understandable quickly on a small screen?
4. **Screen-reader** — does the meaning survive without the visual treatment?
5. **Hostile-reader** — are the claims, sources and assumptions defensible under scrutiny?
6. **Partner** — does the language make room for collaboration and recognise others' contribution?
7. **Paid-work** — can the reader understand what Nightlife Culture can do and what to ask for?
