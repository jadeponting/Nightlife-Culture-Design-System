# Nightlife Culture Design System — instructions for AI agents

**Source of truth: Nightlife Culture Style Guide v1.5.**
**This file: v1.5 · 5 October 2026.** If a file you are reading declares an older version, it is
superseded — check `foundations/tokens.json`, which carries the current one, before you trust it.

You are producing work for **Nightlife Culture**, a creative policy, research and design studio
working across nightlife, music, culture, place and the systems that shape them.

This file is the contract. It is written for any model or agent — Claude, GPT, Gemini, Copilot,
whatever comes next. Follow it exactly. **Do not improvise layout, colour or type.**

---

## One rule for all type (v1.5, 5 October 2026)

Every text style is **one of five voices at one of six sizes**, and every one has a name:
`foundations/tokens.json` `type.roles`, 26 of them, each with the element it sits on and the Word
style it becomes. A component may place text, colour it and put a line beside it. **It never sets a
typeface, a size, a weight or capitals** — `checks/build.py` refuses a component rule that does, and
`foundations/type-manifest.json` lists every style as Specified, Inherits or Barred.

- Heading styles sit on their own element: `nc-heading-1` on `<h1>` to `nc-heading-4` on `<h4>`.
  **H4 is the floor; h5 and h6 are barred** (NC-CON-04, checked).
- Four weights of line and no others: hairline 1px · table line 2px · rule 4px (a line that goes
  with text) · callout 8px (a line on a filled box). Checked.
- No monospace anywhere; a file name is `.nc-file-reference`. Checked.
- **Night time** is two words, never hyphenated. Checked.
- When there is no rule: say so first, build the nearest thing from what exists, show it as an
  option with its cost, mark it provisional, log it in `docs/gaps.md` (NC-SYS-08).

The decisions behind this are in `docs/changelog.md` (v1.5) and `foundations/rules.json`; the
superseded guides are in `archive/2026-10-05-v1.5/`.

---

## The rule that matters most

**This system is checkable, not describable.** Before you deliver anything, run:

```bash
python3 build.py
```

It generates everything from the two source files, then validates and stamps. If it does not print
`BUILD OK`, you are not finished.

**There is one validator: `checks/validate.py`, invoked by `build.py`.** It is the arbiter — not
your judgement and not mine. It exists because taste varies between models and a checker does not.

```bash
python3 checks/validate.py <file>.html      # one artefact, on its own
python3 checks/check_stamps.py              # has anything gone stale?
```

There used to be a second validator at `tools/validate.py`, and this file named it. It checked
layout contracts and no colour or type rule at all, so the same file could pass the named arbiter
and fail the one the build actually ran. It is archived. If you find a reference to it anywhere,
that reference is stale.

---

## Never do these

1. **Never invent a slide layout.** Every slide uses a pattern in `foundations/patterns.json`, and
   every pattern comes from a live deck in `reference/`. If none fits, compose the slide from the
   blocks and say it is a new pattern (see *How the patterns grow*). Never improvise quietly.
2. **Never set a size, colour or spacing on a slide by hand.** The blocks carry them, measured from
   the live deck. If the content does not fit, it is two slides.
3. **Never set a text colour by hand. Read it off the ground.** Every accent
   (`pink, teal, violet, butter, coral`) takes **ink** text. Each ground declares its own:
   **white on blue and ink, ink on chalk and white.**

   > There is no single rule covering all four grounds, and there never was. The old line — *"every
   > ground is a white-text surface"* — is false for two of them: white on chalk is **1.1096:1** and
   > white on white is **1.0000:1**. It sat in this file under "if you remember nothing else,
   > remember that", which is the worst possible place for a wrong sentence. **Read the ground off
   > `foundations/tokens.json`.** `checks/validate.py` now fails the build on white text over a
   > light ground, so this is checked rather than remembered.
4. **Never use brand accents to encode data.** Only the four-series chart ramp does that. The accents
   share one lightness register and collapse in greyscale.
5. **Never use a full-bleed accent ground.** Accents are blocks, thirds and strips — not rooms.
6. **Never link a web font service.** Fonts are in `assets/fonts/` and embedded by `checks/build_fonts.py` into
   `foundations/fonts.css`, with metric-corrected fallbacks so the stand-in occupies the same
   space (NC-TYP-15).
   A linked font fails silently and falls back to a system sans.
7. **Never stretch an SVG** (`preserveAspectRatio="none"`). It destroys the type.
8. **Never use the retired colours:** `#920DFF`, `#F26B43`, `#FFD100`, `#F6F6EE`.

---

## Building a slide deck

1. Write the deck as data: `decks/<name>.json`, one entry per slide, each naming its pattern and
   its blocks. `decks/amgp-v2.json` is the worked example — copy its shape.
2. Open `layouts/slide-patterns.html`. Every pattern is shown beside the live slide it came from.
   Match the live slide, not your idea of it.
3. Run `python3 build.py`. It renders the deck, fails any slide naming an unregistered pattern,
   and fails any slide whose content runs past its floor or under a side block (checked in a
   real browser). Then *look at it*.

### Pattern picker
| Need | Pattern |
|---|---|
| The opening slide | `cover` |
| One big idea, with a few sentences that explain it | `statement` |
| A defining line, then two short columns that unpack it | `statement-two-columns` |
| Three related points, each with a heading and a short paragraph | `three-columns` |
| Three parallel areas, each important enough to hold its own filled block | `three-boxes` |
| Main text in columns, plus one thing different in kind set apart in an accent block at the right edge | `text-and-side-block` |
| A method or process of up to eight steps, read left to right | `steps` |
| Named groups, each with one or two lines of description: partners, roles, audiences | `list` |
| Four questions or workstreams of equal weight | `two-by-two` |
| Periods of time and what happens in each, with a milestone | `phases` |
| Figures that have to be read row by row, such as a budget | `table` |
| Who is doing the work, ending on the offer in a closing band with the wordmark | `team-and-close` |

### How the patterns grow
The system grows from live work, not from invention. When a real deck exists:
1. Put it in `reference/<name>/` — the PDF, plus one image per slide (`slide-01.jpg` …).
2. Rebuild it as `decks/<name>.json`. Each slide either fits a pattern, or is composed from blocks.
3. A new arrangement becomes a new entry in `foundations/patterns.json`, citing its live slide.
4. A missing *block* is a gap: log it in `docs/gaps.md`. Blocks change only when a token changes.

---

## Composition

- **Two registers.** Statement slides (cover, statement) hold one idea with most of the canvas
  empty. Working slides may carry a title, a lead and up to eight short blocks, as the reference
  deck does.
- **Remove copy before reducing type.** Always. This protects every other rule.
- **Title zone: three lines maximum.**
- Content stops 8% above the foot, or above a closing band. The build measures it.

## Colour — and why it is not one sentence

**Accents take ink text. Grounds declare their own.**

| | Text | Measured |
|---|---|---|
| Blue `#0000FF` | white | 8.5925:1 |
| Ink `#0D0D0D` | white | 19.4355:1 |
| Chalk `#F3F3F3` | **ink** | 17.5155:1 · white on chalk is 1.1096:1 |
| White `#FFFFFF` | **ink** | 19.4355:1 · white on white is 1.0000:1 |
| Any accent | ink | 7.42 to 14.73:1 |

This section used to say *"every ground is a white-text surface — if you remember nothing else,
remember that."* It was false for half the grounds, and being memorable made it worse: it is the
line an agent carries into a file. **Read the ground off `foundations/tokens.json`**, where each
ground names its own text colour and every published ratio names the pairing it was measured
against. `checks/validate.py` fails the build on white text over a light ground.

Charcoal `#2D2D2D` is a **text colour, not a ground.** It was filed under grounds, which is how it
came to publish 12.41 — that is charcoal text on chalk, not white text on charcoal.

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
foundations/  tokens.json + rules.json + patterns.json — the single source of truth;
              nightlife-culture.css, nightlife-slides.css, fonts.css — generated, never edited
checks/       generators, validate.py (the one validator), coverage, contrast, stamps, inspectors
components/   the component library and the router
layouts/      the slide renderer and the pattern sheet (slide-patterns.html)
decks/        decks as data (decks/*.json), rendered from the slide blocks
reference/    live decks the patterns were taken from — the visual truth for slides
adapters/     Word, PowerPoint, Excel, and the portable skill
assets/       fonts, outlined wordmark SVGs, the style guide
docs/         changelog, gap register, wordmark rules, explainer pages
dist/         self-contained stamped copies for sending
archive/      superseded — never copy from here
```

## When the system does not cover something

Say so. Do not invent a token, a layout or a rule to patch around a gap — raise it as a gap.
Known gaps are listed in `docs/gaps.md`.
