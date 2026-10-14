# The Nightlife Culture design system — how it is built

**One command.** Everything in `foundations/`, `components/index.html` and `dist/`
is generated. Nothing there is hand-edited.

```
python3 build.py
```

The build is standard-library Python. Two exceptions, stated rather than hidden: the rendered
contrast check needs Playwright, and the Office adapters in `adapters/` need node. The Office
adapters are not yet part of `build.py`.

## The chain, one way

```
Style Guide v1.5.1 ─┐
The Decision Book ─┤
                   ├─► foundations/tokens.json      every VALUE, once
                   └─► foundations/rules.json       every RULE, tiered and sourced
                                │
        checks/build_fonts.py   │   checks/build.py
                ▼               ▼
     foundations/fonts.css   foundations/nightlife-culture.css
                                │
                  components/build_library.py
                                ▼
          components/index.html      linked — cannot go stale
          dist/component-library.html  self-contained — stamped
                                │
                  checks/validate.py    refuses anything off-system
                  checks/check_stamps.py  refuses anything built from a moved source
```

## What you edit, and what you never edit

| Edit this | Never edit this |
|---|---|
| `foundations/tokens.json` — the values | `foundations/nightlife-culture.css` |
| `foundations/rules.json` — the rules | `foundations/fonts.css` |
| `components/library.body.html` — the library's content | `components/index.html` |
| `foundations/patterns.json`, `decks/*.json` — slides | `foundations/nightlife-slides.css` |
| `docs/changelog.md`, `docs/gaps.md` | `dist/*` |

Change a token, run `python3 build.py`, and the stylesheet, the library and the
distributable all regenerate. A colour cannot be chosen at authoring time,
because there is no authoring time — there is only the token file.

## The two forms of the library, and why there are two

`components/index.html` **links** `../foundations/*.css`. It cannot carry a stale
copy of the system, because it does not carry a copy at all. This is the one you
open while working.

`dist/component-library.html` **embeds** everything so it can be emailed. That
form *can* go stale, which is why it carries a build stamp — and why
`check_stamps.py` exists.

## The stamp check

Chapter 18's expensive rule: *"a design system gets copied into things — a skill,
a template, a slide master, a stylesheet, a prompt. Each embeds the system's
values as a snapshot. None of them has any way to notice the source has moved."*

Three rules close it, and this repo implements all three:

1. **Every derived artefact states the source version it was built from** — an
   `nc-build-stamp` meta naming the sha of `tokens.json`, `rules.json`,
   `nightlife-culture.css` and `fonts.css`.
2. **A check compares the two and fails on divergence.** Not a reminder, a check.
   `checks/check_stamps.py`, and `build.py` exits non-zero on it.
3. **Nothing derived asserts its settledness without naming its version.**

Tested: edit a token by hand and re-run `check_stamps.py` — both derived
artefacts report STALE with the old and new digests.

## What the validator enforces

`checks/validate.py FILE.html` — exit 1 on a Fixed breach it can detect. Some Fixed-tier checks
currently report as warnings rather than failing; see `docs/gaps.md`.

Colour allowlist · retired colours and typefaces · hard outlines · hairline scope · typed capitals · fonts linked rather than
embedded · skipped heading levels · absent version stamp · live-type wordmark.

One exemption is **named** rather than silent: keylines on chart marks (`NC-CON-05`), which are
the separator ch04 requires where marks touch.

## Absence as enforcement

- No `.nc-hard-outline` — v1.4 §09 retires it. There is no way to write one on-system.
- No `.nc-series-5` — the four-series cap is enforced by the class not existing.
- No greys — ink, charcoal, chalk and white cover every neutral. Anything between
  them was an invention and was removed.

## Layout

```
assets/fonts/            source .woff2 files
foundations/
  tokens.json            SOURCE — every value
  rules.json             SOURCE — 98 rules, tiered, each citing the guide, a Book chapter or a dated decision
  patterns.json          SOURCE — slide patterns, each citing its live slide in reference/
  v1.4-register.json     458 statements from v1.4, verbatim, + 15 contradictions (historical)
  type-manifest.json     generated — every text style: Specified, Inherits or Barred (v1.5)
  fonts.css              generated
  nightlife-culture.css  generated — the component layer
  nightlife-slides.css   generated — the slide layer
components/
  library.body.html      SOURCE — the library's content
  index.html             generated, linked
checks/
  build.py  build_fonts.py  build_slides.py  validate.py  allowed-hex.json
  check_coverage.py  check_contrast.py  check_stamps.py  inspect_docx/pptx/xlsx.py
dist/
  component-library.html generated, self-contained, stamped
layouts/                 render.py (slides from blocks) · the pattern sheet
decks/                   decks as data, rendered · reference/  live decks, the visual truth
adapters/                word · powerpoint · excel · skill
archive/                 pre-v1.4 material, marked
build.py                 run this
```

---
*Sources: Nightlife Culture Style Guide v1.5.1 · The Decision Book, chapters 1–18,
digest `8701c5a003db5b0b`. Component specs from `headers.html`, containment v1.3,
charts v1.4, slides v1.5, furniture v1.6 and `joy.html`.*
