# Nightlife Culture Design System

The brand as a working system: tokens, rules, generated stylesheets, a component library, slide
layouts, Office adapters, the portable skill, and the checks that refuse anything off-system.

**Source of truth:** Nightlife Culture Style Guide v1.5.1 (14 October 2026).
**This file:** v1.5.1 · 14 October 2026.
**Instructions for AI agents:** [AGENTS.md](AGENTS.md) — read this first if you are a model.
**How the build works:** [README-BUILD.md](README-BUILD.md).

---

## Why this repo exists

A design system written as prose gets read, approximately followed, and then quietly drifted from —
because prose leaves room for judgement, and judgement varies. This repo makes the system
**checkable instead of describable**, so the output is the same whoever or whatever builds it.

The things that do that work:

1. **`foundations/tokens.json` and `foundations/rules.json`** — every value and every rule, once.
   Everything else is generated from them.
2. **`foundations/patterns.json` and `reference/`** — every slide pattern is taken from a live
   deck, and the build fails a slide that names an unregistered pattern or overflows its space.
3. **`python3 build.py`** — one command that regenerates everything, then validates, checks
   coverage, rendered contrast, slide fit and staleness. **`checks/validate.py`** is the one validator.

---

## Quick start

```bash
# build everything, then check it — it must print BUILD OK
python3 build.py

# validate one artefact on its own
python3 checks/validate.py path/to/file.html

# has any derived artefact gone stale?
python3 checks/check_stamps.py
```

Rendered contrast needs Playwright (`pip install playwright && playwright install chromium`).
Without it the build says so — a skipped check is not a passed check.

To view a generated page, serve the repo and open it — fonts are relative paths, so `file://`
will not load them:

```bash
python3 -m http.server 8000
# then open http://localhost:8000/components/index.html
```

---

## Layout of the repo

| Path | What it holds |
|---|---|
| `foundations/` | `tokens.json`, `rules.json`, `patterns.json` (sources); `nightlife-culture.css`, `nightlife-slides.css`, `fonts.css` (generated); `v1.4-register.json` (every statement in the guide, plus its contradictions). |
| `checks/` | The generators for the stylesheets and fonts, `validate.py`, coverage, contrast and stamp checks, and inspectors for .docx, .pptx and .xlsx. |
| `components/` | The component library (`library.body.html` is the source) and the router. |
| `layouts/` | The slide renderer and the pattern sheet. |
| `decks/` | Decks as data (`*.json`), rendered from the slide blocks. |
| `reference/` | Live decks the slide patterns were taken from. The visual truth for slides. |
| `adapters/` | Word, PowerPoint, Excel and the portable skill. |
| `docs/` | The changelog, the gap register, the wordmark rules and the generated explainer pages. |
| `assets/` | Fonts (self-hosted, never linked), the outlined wordmark SVGs and the style guide. |
| `dist/` | Self-contained, stamped copies for sending — including the skill. |
| `archive/` | Superseded material, marked. Never copy from here. |

---

## Slide patterns

Slides are built from blocks, arranged into patterns taken from live decks. See them beside the
live slides they came from in `layouts/slide-patterns.html`.

| Pattern | Use when |
|---|---|
| Cover | The opening slide |
| Statement | One big idea, with a few sentences that explain it |
| Statement and two columns | A defining line, then two short columns that unpack it |
| Three columns | Three related points, each with a heading and a short paragraph |
| Three filled boxes | Three parallel areas, each important enough to hold its own filled block |
| Text and side block | Main text in columns, plus one thing different in kind set apart in an accent block at the right edge |
| Steps | A method or process of up to eight steps, read left to right |
| Labelled list | Named groups, each with one or two lines of description: partners, roles, audiences |
| Two by two | Four questions or workstreams of equal weight |
| Phases | Periods of time and what happens in each, with a milestone |
| Table | Figures that have to be read row by row, such as a budget |
| Team and close | Who is doing the work, ending on the offer in a closing band with the wordmark |

New live work grows the set: add the deck to `reference/`, rebuild it in `decks/`, and register
any new arrangement in `foundations/patterns.json` (details in AGENTS.md).

---

## The non-negotiables

1. **Every accent takes ink text. Every ground takes the text colour its own token declares** —
   white on blue and ink, ink on chalk and white. Read the ground off `foundations/tokens.json`.
2. Accents never encode data — only the four-series chart ramp does.
3. Caps use named roles and tracking; the 16pt heading floor has named small-role exceptions
   in NC-TYP-04. Eight words maximum.
4. Contain with colour and space, not outlines.
5. Fonts are embedded or self-hosted. Never linked. The wordmark is always the placed SVG.
6. Half the canvas stays empty. Remove copy before reducing type.

---

## Contributing

### Using the system with Rowan in local Codex

The maintained local skill is `adapters/skill/local/nightlife-culture-design/`. A personal
skill-folder link makes it available across projects; the installation on Carly's Mac is
`/Users/carly/.codex/skills/nightlife-culture-design`. It reads the local repo on each use,
checks its current guide and source hashes, and routes to the relevant format guidance.
It does not fetch the remote Git repository or claim that Word and Excel have general templates.

The portable package is a snapshot for environments without repo access. `build.py` generates
`dist/nightlife-culture-design.skill` and an identical root-level compatibility copy. Its
`snapshot.json` records all source and bundle hashes, including voice, patterns and reference
assets. Do not install the portable snapshot alongside the local skill under the same name.

See [the skill review and connection](docs/skill-connection.md) for findings, scope and use.

Changing a token or a rule changes every artefact built from it. So:

1. Change `foundations/tokens.json` or `foundations/rules.json` — never hard-code a value in a
   generated file or a template.
2. Run `python3 build.py`. It must print `BUILD OK`.
3. Look at what changed, and compare slides against `reference/` in the pattern sheet.
4. Note what changed and why in `docs/changelog.md`.

If the system does not cover what you need, add it to `docs/gaps.md` rather than inventing a
one-off. A gap recorded is a gap that gets fixed; a gap patched around becomes drift.
