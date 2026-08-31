# Slides

16:9. Everything measured as a percentage of slide width or height so it scales.

## The grid

| Zone | Measure | Rule |
|---|---|---|
| Side margins | 6% of slide width | Nothing crosses them |
| Top margin | 7.5% of slide height | Kicker sits on this line |
| Footer band | Bottom 14% | **Content never enters it.** Logo and slide number only |
| Body measure | Max 60–70% of content width | The ragged right edge is part of the composition |
| Title zone | Three lines maximum | Four lines means the statement is a paragraph |
| Coverage | ~Half the canvas empty | More than ~55% covered = two slides |

**Remove copy before reducing type.** This is the rule that protects all the others.

## Grounds

| Ground | Section header | Title | Use |
|---|---|---|---|
| **Blue** `#0000FF` — primary | Teal | White | Section dividers, statements, two-column contrast, quotes. Top rules, nothing boxed. **The workhorse** |
| **Chalk / white** | Blue | Charcoal | Working ground. Charcoal title, blue sub. Colour blocks or a vertical third. Chalk in decks, white in reports |
| **Ink** `#0D0D0D` | Teal | White | Night register, sparingly. Accent blocks, or a full-bleed strip under a light slide |
| **Accents** | — | Ink | Blocks, thirds, strips and cells. **Never a full-bleed accent ground** |

Never butter as a kicker on ink — it reads as a warning label. Teal is the section-header colour on
every dark ground.

## Breakers

A breaker is a **pause, not an ornament**. One per slide — two rules and it stops meaning "pause"
and starts meaning "pattern".

| Type | Weight / width | Colour | Where |
|---|---|---|---|
| **Separator** | 0.42% of slide width · 20% wide | Blue on light, teal on dark | Between title zone and body zone, flush to the left margin. **The default** |
| **Hairline** | 1px · 74% wide | Ink at 22% | Under the title on dense or document-register slides |
| **Stop** | 0.42% · 20% wide | Teal | Under a divider title, with nothing following it |
| **Accent bar** | 0.55% · 14–22% wide | Pink | Above a pull quote. The only decorative use, always at the top |

**Retired:** a rule breaking the middle of a statement. It interrupts the sentence rather than pacing it.

## Footer furniture

**Slide numbers** — two-digit, bottom-right, Archivo ExtraBold at 1.25% of slide width. Charcoal on
light, teal on dark. Content slides only, not the cover or closing slide. Numbered by position in the
deck, not by section.

**Logo** — see `tokens.md`. Not on content slides by default.

## Proven layouts

1. **Primary · three points** — blue ground, teal kicker, display title, separator, three top-ruled
   columns with numerals. No boxes.
2. **Primary · section divider** — blue ground, kicker, large display title (~7% width), teal stop
   rule. Nothing else.
3. **Primary · two-column contrast** — blue ground, two columns with a 6% gutter, second column
   title in teal to mark the side you want heard. Both columns stop well above the footer.
4. **Primary · quote** — blue ground, pink accent bar above, Archivo ExtraBold quote at ~3% width,
   attribution kicker in teal below.
5. **Light · report register** — chalk or white, charcoal display title, blue sub, three filled
   accent cells (teal / butter / violet).
6. **Ink · night register** — ink ground, teal kicker, three filled accent cells.
7. **Vertical third** — light ground for two-thirds, an accent block for the last third carrying
   numerals or a stat. Title with a hairline breaker under it.
8. **Ink strip** — light ground with a full-bleed ink band across the bottom carrying three numbered
   points, numerals in teal.
9. **Vertical third · stat** — accent block (38%) carrying one big number; white side carrying the
   argument, hairline breaker, and a source line at the foot.

## Building slides

Use CSS container queries so type scales with the slide:
```html
<div class="slide"><div class="cv" style="background:#0000FF;color:#fff">
  <div class="pad">
    <div class="k" style="color:#53E6E5">03 · The opportunity</div>
    <div class="t">A shared<br>evidence layer</div>
    <div class="brk" style="background:#53E6E5"></div>
    <div class="sub">Imagine several cities asking better questions about the night.</div>
  </div>
  <div class="foot"><div></div><div class="pnum" style="color:#53E6E5">07</div></div>
</div></div>
```
`.slide` sets `aspect-ratio:16/9` and `container-type:inline-size`; all sizes inside use `cqw`.

## Dense tier — provisional (v1.1)
For content-heavy slides until the dense tier is specified: hold the 6% margins and 14% footer band,
allow coverage up to 70%, drop slide body to the 18pt minimum, cap at six blocks.

## Diagrams — not yet specified (v1.1)
No diagram kit exists. Build process chains, funnels, progressions and timelines from the containment
treatments in `components.md` and the chart ramp in `charts.md`. **Never use PowerPoint SmartArt
defaults** — they override colour, type, spacing and outlines.
