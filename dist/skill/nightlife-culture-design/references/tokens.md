# Tokens — generated from foundations/tokens.json. Do not edit by hand.

**Source:** Nightlife Culture Style Guide v1.4.1.

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

## Document type scale (decided)

| Role | px | em | Line height | From |
|---|---|---|---|---|
| h1 | 32 | 2.0 | 1.05 | ch03 32px |
| h2 | 24 | 1.5 | 1.25 | ch03 24px |
| h3 | 18 | 1.125 | 1.3 | ch03 18px |
| body | 16 | 1.0 | 1.55 | v1.4 document body 12pt |
| note | 14 | 0.875 | 1.4 | v1.4 footnotes and caveats — 10pt minimum, 10.5-11pt preferred |

## Retired — never to return

`comment` · `values`

