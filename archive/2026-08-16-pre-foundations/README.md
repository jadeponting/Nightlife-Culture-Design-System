# Superseded — the first generation

Archived 16 August 2026, unchanged. Kept for reference; nothing derives from it.

Everything here was built before `foundations/` existed. It rendered correctly and it did
not comply, and it was the source of most findings in the 16 August read-only audit:

- **`tokens/tokens.css`** — hand-written, and drifted. It still declared four grey chart
  tokens (`#4A4A4A #6E6E6E #A6A6A6 #D8D8D8`) that `foundations/tokens.json` records as
  removed — *"a rendering artefact, not tokens. Promoting them into the palette invented
  four greys nobody approved"* — and whose values were wrong anyway. The true greyscale of
  the ramp, computed by luminance rather than channel average, is
  `#4C4C4C #727272 #B2B2B2 #E0E0E0`.
  Its comment also claimed the ramp survives colour-vision deficiency. Measured, under
  protanopia the order inverts (minimum adjacent ratio 1.1075). `tokens.json` carried the
  correct disclosure the whole time; this file contradicted its own sibling, and this file
  was the one every layout linked.

- **`contracts/rules.json`** — v1.0, nested, no rule identifiers, so nothing in it could
  be cited by a check. Superseded by `foundations/rules.json`, which is tiered and
  identified. It also carried the colour law in its false form.

- **`contracts/layouts.json`** — **not archived.** Moved to `foundations/layouts.json`
  unchanged. It is the one thing this generation held that the new one had never
  replaced: slot contracts, word limits, block budgets, permitted grounds and the vertical
  anchor per layout.

- **`tools/validate.py`** — the second validator. It checked layout contracts and anchors
  and no colour or type rule at all, while `AGENTS.md` named it as the arbiter. The same
  file passed this one and failed `checks/validate.py` on two Fixed breaches. There is one
  validator now: `checks/validate.py`, invoked by `build.py`.

- **`tools/contrast.py`** — printed the false colour law as remediation advice.

- **`components/components.css`, `system/slides.css`** — hand-written, 58 classes, of which
  five names survived into the generated layer. Replaced by `foundations/nightlife-culture.css`
  and `foundations/nightlife-slides.css`, both generated from `tokens.json`.

- **`templates/deck.html`, `index.html`** — the wordmark set as live type in ten places,
  against Fixed rule NC-BRK-02, while eight outlined SVGs sat unused in `assets/logo/`.
  `templates/deck.html` also carried a personal email address, and it was the file everyone
  was told to copy.

Replaced by the generated chain: `foundations/tokens.json` and `foundations/rules.json`
are the only sources; everything else in the system is produced from them by `build.py`
and checked by `checks/validate.py` and `checks/check_stamps.py`.
