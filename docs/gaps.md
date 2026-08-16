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

### 6. Masthead ground — RESOLVED 16 Aug 2026, rule still to be written
No rule said what ground a document masthead takes. Five sheets were built, each with its own
hand-written stylesheet, and the ground was picked by eye — three ink, two blue.

**What I did instead:** invented an answer five separate times, and did not say there was no rule.
That is the failure, not the colour. `design-decisions` step 6 says log the gap and say it out
loud; the procedure was there and went unused.

**Cost of getting it wrong:** red. Every outward-facing sheet carried a different primary ground,
in a system whose entire purpose is that this cannot happen.

**Carly's decision, 16 Aug:** the masthead ground is the primary brand colour. Blue `#0000FF`.
Ink is the night register and is not a default.

**Closes when:** a rule exists naming the masthead ground, the page furniture is a component in
the generated CSS, and a check fails a masthead built on anything else.

### 7. Interactive states — no rules at all
`.nc-link` sets a colour and an underline. There is nothing for `:visited`, `:hover`, `:active`
or a disabled control. A clicked link looks unclicked, which is the one thing link colour has
historically been for.

**What I did instead:** shipped a link component with one state and did not notice the others
were missing until the user asked what a clicked link looks like.

**Cost of getting it wrong:** amber. Navigation in any long HTML artefact.

**Closes when:** every interactive element has a declared state set, and the validator checks it.

### 8. The page layer does not exist
The system has 90 components and nothing for the page around them — masthead, wrap, kicker,
standfirst, specification note, specimen frame. So every sheet is hand-authored, and every
hand-authored file is a fork.

**What I did instead:** wrote five separate stylesheets — `docs/audit.scaffold.css`,
`docs/plan.scaffold.css`, `docs/routing.scaffold.css`, `layouts/layouts.scaffold.css`,
`components/library.scaffold.css`. None governed, none checked, none consistent.

**Cost of getting it wrong:** red. Every visual defect found in review lived here rather than in
the components.

**Closes when:** the page furniture is generated from `tokens.json` like everything else, the five
scaffolds are deleted, and one generator produces every sheet.

**Logged upstream as GAP-30** in the decision-book register — the Book has no rule for page
furniture either, so this is not only ours.

## Defects, not gaps

Recorded separately because a defect in the work is a different thing from a gap in the guidance,
and mixing them is how the real gaps get lost.

- **The `<summary>` disclosure marker is the browser default.** NC-DOC-08 already says every
  element the browser renders is decided. The rule exists and was not applied — by the component
  that demonstrates the rule.
- **Specimen charts carry no unit, comparator or axis**, and one legend measures a different
  quantity from its mark. Breaches NC-EVI-01, which this system wrote. **Logged upstream as
  GAP-29** as well, because the Book requires a demonstration's *mechanism* to be honest and says
  nothing about its *data*.
- **The section-header numeral box outgrows its title** at narrow widths — the box is a fixed
  `.94em` while the title is a clamp that collapses toward `1.15em`.

## Closed

- ~~Slide layouts undocumented~~ — twelve layouts, contracts and canonical files. v1.0.
- ~~No enforcement~~ — `tools/validate.py`. v1.0.
- ~~Slides hanging from the top with dead bottoms~~ — the anchor rule. v1.0.
