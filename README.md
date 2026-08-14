# Nightlife Culture Design System

The brand as a working system: tokens, layout contracts, stylesheets, templates and a validator.

**Source of truth:** Nightlife Culture Style Guide v1.0 (August 2026).
**Instructions for AI agents:** [AGENTS.md](AGENTS.md) — read this first if you are a model.

---

## Why this repo exists

A design system written as prose gets read, approximately followed, and then quietly drifted from —
because prose leaves room for judgement, and judgement varies. This repo makes the system
**checkable instead of describable**, so the output is the same whoever or whatever builds it.

The three things that do that work:

1. **`contracts/layouts.json`** — every layout declares its slots, word limits, required elements and
   vertical anchor. Machine-readable, not prose.
2. **The anchor rule** — every content area declares `data-anchor`, and the value comes from the
   contract. This is what stops a slide hanging from the top and dying in a dead band at the bottom,
   which was the single biggest failure in earlier attempts.
3. **`tools/validate.py`** — one command that fails loudly on block budget, word overruns, missing
   numerals, wrong ground colours, forbidden slots and retired colours. Standard library only.

---

## Quick start

```bash
# see what layouts exist
python tools/validate.py --list

# check the contracts are internally consistent
python tools/validate.py --check-contracts

# validate something you have built
python tools/validate.py templates/deck.html

# check any colour pair against WCAG
python tools/contrast.py "#ED77C2" "#FFFFFF"
```

To view a template, serve the repo and open it — the fonts are relative paths, so `file://` will not
load them:

```bash
python -m http.server 8000
# then open http://localhost:8000/templates/deck.html
```

---

## Layout of the repo

| Path | What it holds |
|---|---|
| `tokens/` | Colour, type, spacing and fonts. The single source of truth. Everything else references these. |
| `system/` | Stylesheets implementing the tokens. `slides.css` today; document, chart and asset sheets to follow. |
| `contracts/` | `layouts.json` and `rules.json` — the machine-readable spec the validator enforces. |
| `layouts/` | One canonical HTML file per layout. |
| `templates/` | Working starters you can copy. |
| `tools/` | `validate.py`, `contrast.py`. No dependencies. |
| `golden/` | Reference renders. Compare output against these rather than guessing. |
| `assets/` | Fonts (self-hosted, never linked) and logo. |
| `docs/` | The human-readable guide and the known-gaps list. |

---

## The twelve slide layouts

| id | Name | Anchor | Grounds |
|---|---|---|---|
| L01 | Cover | two | blue, ink |
| L02 | Section divider | centre | blue, ink |
| L03 | Three points | two | blue, chalk, white, ink |
| L04 | Two-column contrast | top | blue, ink |
| L05 | Quote | centre | blue, ink |
| L06 | Report register | two | chalk, white |
| L07 | Night register | two | ink |
| L08 | Vertical third | two | chalk, white |
| L09 | Ink strip | two | chalk, white |
| L10 | Vertical third stat | two | chalk, white |
| L11 | Chart slide | two | chalk, white |
| L12 | Closing | two | blue, ink |

---

## The non-negotiables

1. Every accent is a **black-text** surface. Every ground is a **white-text** surface.
2. Accents never encode data — only the four-series chart ramp does.
3. Caps for display, H1, H2 and labels: always tracked, never below 16pt, eight words maximum.
4. Contain with colour and space, not outlines.
5. Fonts are embedded or self-hosted. Never linked.
6. Half the canvas stays empty. Remove copy before reducing type.

---

## Contributing

Changing a token or a contract changes every artefact built from it. So:

1. Change `tokens/` or `contracts/` — never hard-code a value in a template.
2. Run `python tools/validate.py --check-contracts`.
3. Re-validate the templates.
4. Regenerate the golden renders and eyeball the diff.
5. Note what changed and why in `docs/changelog.md`.

If the system does not cover what you need, add it to `docs/gaps.md` rather than inventing a
one-off. A gap recorded is a gap that gets fixed; a gap patched around becomes drift.
