# The Nightlife Culture wordmark

**The wordmark is an outlined asset. It is never re-set as live type.**

That sentence is the whole rule. Everything below explains why, so nobody is tempted to fudge it.

---

## The files

| File | Use |
|---|---|
| `nightlife-culture-wordmark.svg` | Inline in HTML. Inherits `currentColor` — set `color` on the parent. |
| `nightlife-culture-wordmark-white.svg` | On blue, ink, or any dark ground. For `<img>`. |
| `nightlife-culture-wordmark-blue.svg` | On chalk or white. For `<img>`. |
| `nightlife-culture-wordmark-ink.svg` | On an accent ground. For `<img>`. |

All four are outlined vector paths. They render identically whether or not Archivo Black is
installed. `currentColor` does **not** work through `<img>` — use a coloured variant there.

---

## Why it must not be re-set

The wordmark comes from the printed business card. Measured from that artwork:

| | Value |
|---|---|
| NIGHTLIFE | **32.09pt** |
| CULTURE | **33.41pt** |
| Rendered width, NIGHTLIFE | 171.92pt |
| Rendered width, CULTURE | 171.19pt |
| Baseline to baseline | 30.41pt |
| Effective line-height | **0.9476** |

**The two lines are set at different sizes so they justify to the same width** — 171.92 against
171.19, a difference of 0.4%. That is what makes the lockup read as a solid rectangle rather than
a ragged stack.

Set both lines at one size and you lose it. Every regenerated version has made exactly that
mistake, including the `nightlife-culture-lockup.svg` in the design-system development folder,
which is live `<text>` at a single size with `letter-spacing:-3` — a rendering of type, not the
mark.

If a future version looks *almost* right, this is why.

---

## Rules

1. **Never re-set as live type.** Not in HTML, not in PowerPoint, not in Figma, not in a prompt.
   Place the SVG.
2. **Never restack, re-space or re-track it.** The relationship between the two lines is the mark.
3. **Never stretch it.** Scale proportionally. No `preserveAspectRatio="none"`, no dragging a
   corner without a modifier key.
4. **One colour only.** White on blue and ink. Blue on chalk and white. Ink on an accent.
   The two-colour treatment (charcoal + one accent) is permitted **on covers only**.
5. **Teal is never a logo colour on a light ground** — 1.52:1 on white. Pink (7.42:1) and violet
   (7.64:1) are the accents that clear it.
6. **Clear space:** at least the cap height of NIGHTLIFE on all four sides. Nothing enters it.
7. **Minimum size:** 90px wide on screen, 22mm in print. Below that, use the wordmark on one line
   or omit it.
8. **Never place it on photography** without a tested solid surface behind it.
9. **Never add anything to it** — no strapline locked up, no box, no rule, no shadow, no outline.
10. **Never two logos on one surface.**

## Placement

**Slides:** full lockup on the cover, section dividers and closing slide. No logo on content slides
by default — the exception is any slide likely to travel alone (a headline finding, a data slide,
a quote). Footer version at ~1.5% of slide width; it should be the quietest thing there.

**Documents:** cover and back page only. Never in a running header.

**Everything else:** once. Quietly.

## If you need something this file does not cover

Say so and stop. Do not improvise a variant. A logo that gets improvised is not a logo.
