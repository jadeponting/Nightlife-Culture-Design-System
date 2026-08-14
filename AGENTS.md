# Nightlife Culture Design System — instructions for AI agents

You are producing work for **Nightlife Culture**, a creative policy, research and design studio
working across nightlife, music, culture, place and the systems that shape them.

This file is the contract. It is written for any model or agent — Claude, GPT, Gemini, Copilot,
whatever comes next. Follow it exactly. **Do not improvise layout, colour or type.**

---

## The rule that matters most

**This system is checkable, not describable.** Before you deliver anything, run:

```bash
python tools/validate.py <your-file>.html
```

If it does not print `PASS`, you are not finished. The validator is the arbiter, not your judgement
and not mine. It exists because taste varies between models and a checker does not.

```bash
python tools/validate.py --list             # every layout and its contract
python tools/validate.py --check-contracts  # sanity-check the contracts themselves
python tools/contrast.py "#ED77C2" "#FFF"   # WCAG check any colour pair
```

---

## Never do these

1. **Never invent a slide layout.** Twelve exist in `contracts/layouts.json`. Pick one. If none fits,
   say so and ask — do not improvise a thirteenth.
2. **Never add a slot a layout does not declare.** No extra paragraph under the columns. If the content
   does not fit the contract, it is two slides.
3. **Never put white text on an accent.** Every accent (`pink, teal, violet, butter, coral`) is a
   **black-text** surface. Every ground (`blue, ink, chalk, white`) is a **white-** or ink-text surface.
4. **Never use brand accents to encode data.** Only the four-series chart ramp does that. The accents
   share one lightness register and collapse in greyscale.
5. **Never use a full-bleed accent ground.** Accents are blocks, thirds and strips — not rooms.
6. **Never link a web font service.** Fonts are in `assets/fonts/` and wired in `tokens/fonts.css`.
   A linked font fails silently and falls back to a system sans.
7. **Never stretch an SVG** (`preserveAspectRatio="none"`). It destroys the type.
8. **Never use the retired colours:** `#920DFF`, `#F26B43`, `#FFD100`, `#F6F6EE`.

---

## Building a slide deck

1. Read `contracts/layouts.json`. Pick a layout per slide.
2. Copy the matching file from `layouts/`, or start from `templates/deck.html`.
3. Every `<section>` carries `data-layout="L03"`.
4. Every `.cv` carries a `ground-*` class. **The ground brings its own text, kicker and title colours** —
   that is why you must use the class rather than setting colours by hand.
5. Every `.pad` carries `data-anchor`, and the value comes from the contract:
   - `two` — the last block pins to the bottom so the composition spans the frame. The default.
   - `centre` — one block optically centred. Dividers and quotes.
   - `top` — only where the contract declares it.
   **A missing anchor renders a loud coral warning on the slide.** That is deliberate.
6. Run the validator. Fix everything. Then render and *look at it* before delivering.

### Layout picker
| Need | Layout |
|---|---|
| Cover | L01 |
| Opening a section | L02 |
| Three related points | L03 (rules) · L06 / L07 (filled cells) |
| Two things in tension | L04 — the Nightlife Culture argument shape |
| A line that must land | L05 |
| A number that must land | L10 |
| A process or sequence | L09 |
| Data | L11 |
| Detail-heavy content | L08 |
| The ask | L12 |

---

## Composition

- **Half the canvas stays empty.** Over ~55% covered means it is two slides.
- **Remove copy before reducing type.** Always. This protects every other rule.
- **One breaker per slide** (except L04, which takes one per column — the contract says so).
- **Title zone: three lines maximum.**
- **Kickers are three or four words**, not sentences. A leading `07 ·` index does not count.
- Content never enters the bottom 14% — that band is the logo and the slide number.

## Colour, in one sentence

Every accent is a black-text surface; every ground is a white-text surface. If you remember nothing
else, remember that. Full matrix and reasoning in `docs/tokens.md` and `contracts/rules.json`.

## Type

Archivo Black (display) · Archivo ExtraBold 800 (H1/H2) · Archivo Bold 700 (H3) · Inter 400 (body) ·
Archivo SemiBold 600 (labels). Caps for display, H1, H2 and labels — **always tracked, never below
16pt, eight words maximum**. H3 and body are sentence case. Never caps in body, captions, source
lines, alt text or table cells.

## Evidence is part of the design

Strong design must never make weak evidence look stronger than it is.

- Every chart carries a provenance code, reference period, geography and boundary vintage.
- Every comparison between places declares whether the comparability gate cleared.
- Every big number carries a source line. A statistic without one is a claim, not a finding.
- Suppressed data is hatched and marked `[c]`; not collected is `n/a`. **Never a blank.**
- Illustrative figures say so, in the chart, every time.

## Voice

Able to move between the dancefloor, the committee room, the funder meeting and the evidence base
without losing the truth of the culture. Arc: **joy → value → evidence → action.**

Avoid: "this matters" · "in today's rapidly changing landscape" · "unlock the potential" ·
"at the heart of" · "more important than ever" · repetitive three-part slogans.

---

## Repository map

```
tokens/       colours, type, spacing, fonts — the single source of truth
system/       stylesheets that implement the tokens (slides.css, and more to come)
contracts/    layouts.json + rules.json — machine-readable, what the validator enforces
layouts/      one canonical HTML file per layout
templates/    working starters (deck.html, and more to come)
tools/        validate.py, contrast.py
golden/       reference renders — compare your output against these
assets/       fonts, logo
docs/         the human-readable guide
```

## When the system does not cover something

Say so. Do not invent a token, a layout or a rule to patch around a gap — raise it as a gap.
Known gaps are listed in `docs/gaps.md`.
