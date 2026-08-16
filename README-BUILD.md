# The Nightlife Culture design system — how it is built

**One command.** Everything in `foundations/`, `components/index.html` and `dist/`
is generated. Nothing there is hand-edited.

```
python3 build.py
```

Stdlib only — no install, no network, no node.

## The chain, one way

```
Style Guide v1.4  ─┐
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
| `components/library.scaffold.css` — page layout only, no components | `dist/*` |

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

`checks/validate.py FILE.html` — exit 1 on any Fixed breach.

Colour allowlist · retired colours and typefaces · hard outlines outside the
flyer register · hairline scope · typed capitals · fonts linked rather than
embedded · skipped heading levels · absent version stamp · live-type wordmark.

Two exemptions are **named** rather than silent: the flyer-register 2px outline
(`NC-CON-01`) and keylines on chart marks (`NC-CON-05`), which are the separator
ch04 requires where marks touch.

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
  rules.json             SOURCE — 45 rules, tiered, each citing v1.4 or a Book chapter
  v1.4-register.json     458 statements from v1.4, verbatim, + 15 contradictions
  fonts.css              generated
  nightlife-culture.css  generated — 113 component classes
components/
  library.body.html      SOURCE — the library's content
  library.scaffold.css   SOURCE — page layout only
  index.html             generated, linked
checks/
  build_fonts.py  build.py  validate.py  check_stamps.py  allowed-hex.json
dist/
  component-library.html generated, self-contained, stamped
adapters/                html · word · powerpoint · excel — next
archive/                 pre-v1.4 material, marked
build.py                 run this
```

---
*Sources: Nightlife Culture Style Guide v1.4 · The Decision Book, chapters 1–18,
digest `6034d466ccbf4071`. Component specs from `headers.html`, containment v1.3,
charts v1.4, slides v1.5, furniture v1.6 and `joy.html`.*
