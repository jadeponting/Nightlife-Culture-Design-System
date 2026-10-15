# Tokens — generated from foundations/tokens.json. Do not edit by hand.

**Source:** Nightlife Culture Style Guide v1.5.1.

## The colour law

**Every accent takes ink text. Every ground takes the text colour its own token declares — white on blue and ink, ink on chalk and white.**

There is no single sentence covering all four grounds: blue takes white · ink takes white · chalk takes ink · white takes ink. White on chalk is 1.11:1 and white on white is 1.00:1 — the old one-line law is retired.

## Grounds

| Token | Hex | Role | Text on it |
|---|---|---|---|
| Blue | `#0000FF` | Primary ground. Covers, dividers, statements, links. | white · 8.59:1 (white text on blue) |
| Ink | `#0D0D0D` | Night ground. Full-bleed surfaces and strips where accents need to glow. | white · 19.44:1 (white text on ink) |
| Chalk | `#F3F3F3` | Reading ground — decks and screen. | ink · 17.52:1 (ink text on chalk) |
| White | `#FFFFFF` | Reading ground — reports and print; panels on chalk. | ink · 19.44:1 (ink text on white) |

## Text colours (never grounds)

| Token | Hex | Role | Measured |
|---|---|---|---|
| Charcoal | `#2D2D2D` | Secondary copy, captions, slide titles on light grounds. | 12.41:1 on chalk · 13.77:1 on white |

Charcoal was once filed under grounds; it is a text colour. Its published ratio is charcoal ON chalk.

## Accents — surface palette, ink text, never data

| Token | Hex | Role | Ink text |
|---|---|---|---|
| Pink | `#ED77C2` | Hot counter-signal, accent bars, left rules | 7.42:1 |
| Teal | `#53E6E5` | Cool highlight, section headers on dark | 12.79:1 |
| Violet | `#B98CFF` | Calm surface, blocks, vertical thirds | 7.64:1 |
| Butter | `#FFDE6B` | Opportunity, funding, forward motion | 14.73:1 |
| Coral | `#FD7B53` | Urgency, risk, lowest provenance tier | 7.53:1 |

## Chart ramp — the only colours that may encode data

`#0000FF` → `#C7339A` → `#00C6C5` → `#FFDE6B` · four series maximum · lightness climbs monotonically.

## The five voices

| Voice | Face | Case | Tracking | Leading | Use |
|---|---|---|---|---|---|
| Display | Archivo Black | capitals | -0.01em | 0.94 | Covers and mastheads only. Sized to the cover, never a step. |
| Capitals | Archivo ExtraBold 800 | capitals | 0.04em | 1.12 | Headings one and two, titles in contents and tables, numbers. |
| Sentence | Archivo Bold 700 | sentence case | 0 | 1.3 | Headings three and four, the takeaway, the key statement, the button. |
| Text | Inter Regular 400 | sentence case | 0 | 1.55 | Running text and everything that reads like it. Bold (700) for emphasis and the first column of a table. Italic for a short run inside a paragraph. |
| Label | Archivo SemiBold 600 | capitals | 0.1em | 1.4 | A phrase, never a sentence: labels, table header rows, chips, evidence marks, attributions, the running foot. |

## The six sizes

| Screen | Print | rem |
|---|---|---|
| 32px | 24pt | 2.0 |
| 24px | 18pt | 1.5 |
| 18px | 13.5pt | 1.125 |
| 16px | 12pt | 1.0 |
| 14px | 10.5pt | 0.875 |
| 12px | 10pt | 0.75 |

The caps floor for headings is 16pt. Below it, capitals appear only in the fixed small styles below (NC-TYP-04).

## The roles — every text style, and the Word style it becomes

A component never sets type; it carries one of these classes. A heading role sits only on its own element, h1 to h4; h5 and h6 are barred.

| Class | Voice | Size | Element | What it is for | In Word |
|---|---|---|---|---|---|
| `.nc-display` | display | cover | h1 | Covers and mastheads only | Title |
| `.nc-heading-1` | capitals | 32px · 24pt | h1 | The title of a document | Heading 1 |
| `.nc-heading-2` | capitals | 24px · 18pt | h2 | A section, numbered or not | Heading 2 |
| `.nc-contents-title` | capitals | 14px · 10.5pt | — | A title in a contents list | TOC 1 |
| `.nc-table-title` | capitals | 14px · 10.5pt | caption | The title above a table | Caption |
| `.nc-number` | capitals | 12px · 10pt | — | Section and chapter numbers on an ink box; page numbers | Part of the heading |
| `.nc-heading-3` | sentence | 18px · 13.5pt | h3 | A sub-section | Heading 3 |
| `.nc-heading-4` | sentence | 16px · 12pt | h4 | The lowest heading, with its blue bar. The floor: there is no H5 or H6 | Heading 4 |
| `.nc-takeaway` | sentence | 16px · 12pt | — | One or two sentences to remember, in the running text with a pink rule | Intense Quote |
| `.nc-key-statement` | sentence | 16px · 12pt | — | The question or point a chapter turns on, in its top-rule panel | Key statement (new style) |
| `.nc-button` | sentence | 16px · 12pt | button | The one thing to press. Blue, fully rounded | Screen only |
| `.nc-text-action` | sentence | 16px · 12pt | — | A minor action beside a button, underlined | Screen only |
| `.nc-subtitle` | text | 18px · 13.5pt | — | The line under a title | Subtitle |
| `.nc-body` | text | 16px · 12pt | p | Running text | Normal |
| `.nc-quotation` | text | 16px · 12pt | — | A quotation that runs on, in the running text with a pink rule | Quote |
| `.nc-list-item` | text | 16px · 12pt | li | Bulleted and numbered lists, indented | List Bullet, List Number |
| `.nc-table-first-column` | text | 14px · 10.5pt | th | The first column of a table, which names each row. Bold | Table style, First Column |
| `.nc-table-cell` | text | 14px · 10.5pt | td | Every other cell | Table style |
| `.nc-file-reference` | text | 14px · 10.5pt | code | A file name or literal string, on a white hairline chip. Never monospace | File reference (new style) |
| `.nc-small` | text | 14px · 10.5pt | — | Notes under tables and charts, source lines, small print, hints | Small (new style) |
| `.nc-label` | label | 12px · 10pt | — | Labels above things | Label (new style) |
| `.nc-table-header-row` | label | 12px · 10pt | th | The row of column headings | Table style, Header Row |
| `.nc-chip` | label | 12px · 10pt | — | Status, on a fill. The word carries the meaning, never the colour alone | Screen only |
| `.nc-evidence-mark` | label | 12px · 10pt | — | A bracketed mark inside a sentence | Label, as a character style |
| `.nc-attribution` | label | 12px · 10pt | footer | Who said it, under a quotation | Label |
| `.nc-running-foot` | label | 12px · 10pt | — | The foot of every page | Footer |

## The four weights of line

| Weight | Screen | Print | Use |
|---|---|---|---|
| hair (`--nc-line-hair`) | 1px | 0.75pt | Table rows, contents rows, outlines, the foot of a page. Never carries meaning (NC-CON-02). |
| table (`--nc-line-table`) | 2px | 1.5pt | Under a table's header row. Half the rule, in proportion to the 12px headings it sits under. |
| rule (`--nc-line-rule`) | 4px | 3pt | A line that goes with text: section title, H4 bar, breaker, rail marker, quotation, comparability flag. |
| callout (`--nc-line-callout`) | 8px | 6pt | A line on a filled box, at the top or the left: key statement, callout, recommendation, Claude note, statistic, chart card, accent table. |

## Language

Night time is two words, never hyphenated: night time economy, Night Time Advisor. British English. Cultural value and cultural contribution are not interchangeable; use the one you mean.

## Retired — never to return

`comment` · `values`

