# Changelog

## v1.0 — August 2026

First version of the system as an enforceable repo rather than a written guide.

**Added**
- `contracts/layouts.json` — twelve slide layouts with slot contracts, word limits, required
  elements, permitted grounds and vertical anchors.
- `contracts/rules.json` — global colour, grid, composition, typography, chart and footer rules.
- `system/slides.css` — the slide system, with the anchor rule enforced in CSS and a visible coral
  warning when `data-anchor` is missing.
- `tools/validate.py` — validator. Standard library only.
- `tools/contrast.py` — WCAG contrast checker.
- `templates/deck.html` — a twelve-slide reference deck that passes validation.
- `AGENTS.md` / `CLAUDE.md` — the contract for any AI agent working in this repo.
- `golden/` — reference renders.

**Decisions**
- The anchor is a **contract field, not a styling choice**. Authors do not pick it. Implicit
  top-anchoring was the single largest cause of weak slides in earlier attempts.
- Ground classes carry their own text, kicker and title colours, so the colour law cannot be
  forgotten by setting a colour by hand.
- `maxBlocks` must be at least the number of slots a layout declares — enforced by
  `--check-contracts`, after the first draft shipped three layouts that contradicted themselves.
- Plain HTML and CSS only. No framework, no build step, no second source of truth.
