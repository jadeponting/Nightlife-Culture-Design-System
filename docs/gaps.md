# Known gaps

Recorded rather than patched around. A gap noted is a gap that gets fixed; a gap improvised over
becomes drift.

## Open

### 1. Dense layout tier
Every layout is the generous register — one idea, half the canvas empty. Content-heavy slides need a
second tier with its own margins, sizes and coverage ceiling.

**Interim rule:** hold the 6% margins and the 14% footer band, allow coverage up to 70%, drop slide
body to the 18pt minimum, cap at six blocks. Flag any slide built this way as provisional.

### 2. Diagram kit
No diagram system exists. Process chains, funnels, progressions and timelines are all needed.

**Interim rule:** build from the containment treatments and the chart ramp. **Never use PowerPoint
SmartArt defaults** — they override colour, type, spacing and outlines.

### 3. Document, chart and asset stylesheets
`system/slides.css` exists. Still to port from the style guide: `document.css` (long-form reports,
tables, pull quotes, stat blocks), `charts.css` (the full chart component set) and `assets.css`
(business cards, letterheads, social graphics, email signatures).

### 4. Contracts for non-slide artefacts
`contracts/layouts.json` covers slides only. Reports, charts and marcoms assets need equivalent
contracts before the validator can check them.

### 5. Web / published pages
No page templates yet for nightlifeculture.co.uk or a published HTML report.

### 6. PowerPoint export
Decks are built in HTML. A `.pptx` path — either a python-pptx builder driven by the same contracts,
or a documented manual mapping — is not yet written.

## Closed

- ~~Slide layouts undocumented~~ — twelve layouts, contracts and canonical files. v1.0.
- ~~No enforcement~~ — `tools/validate.py`. v1.0.
- ~~Slides hanging from the top with dead bottoms~~ — the anchor rule. v1.0.
