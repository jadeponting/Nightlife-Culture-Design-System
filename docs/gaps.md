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

### 9. The type scale is not a component — NEEDS A DECISION
The most fundamental thing in a design system, and there is no class for it. `tokens.json` holds
six type ROLES — display, h1, h2, h3, body, label — each with a face, a weight, a case and a
tracking value. It holds no document SIZES: `type.sizes.document.scale` reads, in the file,
**"UNDECIDED — see gaps."**

**What I did instead:** drew the type scale into the markup of the component library. Five sizes —
3.4em, 2.1em, 1.35em, 1.06em, .8em — and a 1.4em vertical rhythm, none of them in any token, none
of them decided by anyone, all of them presented on the page as though they were the system. The
one specimen that is supposed to prove the system exists was the one specimen that had no system
behind it.

**Cost of getting it wrong:** red. Every heading in every artefact takes its size from here. It has
been sitting in the library looking settled since the library was built.

**Found by:** the provenance disclosure, on its first run. 32 of the 34 flags in the whole library
are this one specimen.

**Closes when:** Carly decides the document scale, the six roles become classes generated from
`tokens.json`, the library specimen uses those classes, and a check fails on type set in a style
attribute. **I am not choosing the sizes.**

### 10. A component may be re-declared in a later section — no rule either way
`.nc-prov` was the evidence-provenance chip. A second `.nc-prov` was written for a provenance
table, four sections later. The later one won. Every cell in that table rendered as white text on
white — and the validator passed, coverage passed, the stamps matched. Nothing in the system could
see it.

**What I did instead:** took a name that was already taken, and would not have found it if the page
had not been screenshotted.

**Cost of getting it wrong:** red. It is silent by construction.

**Interim:** `check_coverage.py` now reports any class defined twice where the second definition
re-sets a property the first one set. Breakpoint overrides inside `@media` are excluded — that is
what a breakpoint is for. It REPORTS and does not fail, because there is no rule saying whether a
component may be re-declared, and four current cases are deliberate: the CASE section sets
`text-transform` on components declared elsewhere, and `nightlife-slides.css` re-sets `.nc-sub`.

**Needs Carly's decision:** may a later section re-declare a component, or is one class one place?
The CASE section is the test case — it is either a good cross-cut or the same fault, deliberately.

### 11. Gap 9 was wrong — the type scale WAS decided, in two places
I said the document type scale was undecided and asked Carly to choose it. It is not undecided.
**v1.4 Readable size rules** sets document body at 12pt minimum AND preferred, and footnotes at
10pt minimum / 10.5–11pt preferred. **Decision Book ch03**, worked example: *"Sizes across those
four levels span only 32px → 24px → 18px → 16px, a deliberately narrow range, because weight and
space are carrying the distinction."* v1.4's scoped line-height table gives the leading per class.
ch03 gives the rhythm: a heading carries three times the space above it that it carries below.

**What I did instead:** asked her to decide something the sources already answer, after being told
repeatedly that if there is no answer we have probably already written the logic down.

**Cost:** red, and worse than red — it spends the one thing this project runs on.

**Now built:** `.nc-display .nc-h1 .nc-h2 .nc-h3 .nc-body .nc-fnote`, generated from tokens, every
number carrying the source it was read from.

**Still genuinely open — ONE number, not six:** the document LABEL size. v1.4's size table gives
slide labels (14pt min, 16pt+) and no document label at all, and the caps floor is stated as 16pt
"on screen". At a 12pt document body a 16pt caps label would be larger than the body text.

### 12. The coverage check only ever ran one way
It checked that every class DEFINED is demonstrated. Nothing checked that every class USED is
defined — and it only read two of the eleven pages the build produces.

**What that hid:** 29 classes used across the generated sheets and defined nowhere at all.
`.g4` drew a four-across grid two lines above the sentence saying there is no four-across grid.
`.gr`, `.h` and `.m` meant the ground swatches rendered as unstyled spans running into each other —
which is why "Signal blue#0000FF · white · 8.59:1" reads as one word. `.tw` was a table wrapper
that wrapped nothing. `.nm`, `.sr`, `.wt`, `.cnt`, `.r--ok` and twenty more are a private
vocabulary the audit and plan sheets invented for themselves.

**Cost:** red. Every one of these was found by Carly reading the page. The build could not see any
of them.

**Now a check, and it FAILS.** The build is currently red on 29 of them. Closes when the count is
zero.

### 13. Contrast was never measured on anything that had been rendered
Every contrast check read the source: is this hex on the allowlist, does this ground declare its
text colour, is white text on a light ground. None of them could see a colour that lands on a dark
ground because an ancestor set it three levels up. That is why the same accessibility failure has
been reported five or six times and passed the build every time.

**Now a check:** `checks/check_contrast.py` opens every page in a real browser at 1280px and at
390px, opens every disclosure, walks every element that paints text INCLUDING `::before` and
`::after`, resolves the colour actually painted against the background actually painted onto
through any translucency, and applies 4.5:1 / 3:1. Proven to fire on a deliberately broken file
(blue on ink at 2.26:1). **It currently reports zero failures on every page** — so the blue-on-dark
Carly is seeing is either off these pages, or it is a size complaint rather than a contrast one,
and I need her to point at it once more.

### 14. Violet for visited links was invented by me
NC-PAG-04 says "Violet visited on light, pink on dark" and cites gap 7, WCAG 2.4.7 and ch14. Those
sources say every interactive element must declare its states. **None of them says violet.** I
picked it and wrote it into the rule register as though it had a source.

**Cost:** amber for the colour, red for the method — a rule in the register that cites sources
which do not contain it is worse than no rule.

**Also:** the link specimen claims to show a visited link and cannot. Browsers restrict `:visited`
to a handful of properties and will not report it, so the "visited one" in that specimen renders
identically to the unvisited one. The page describes hover and focus and demonstrates neither. That
is a specimen that describes instead of showing, in the library built to prove the opposite.

## Defects, not gaps

Recorded separately because a defect in the work is a different thing from a gap in the guidance,
and mixing them is how the real gaps get lost.

- ~~**The `<summary>` disclosure marker is the browser default.**~~ FIXED 16 Aug. It is a word —
  SHOW / HIDE, blue, underlined, teal on dark grounds. No glyph, no icon. A choice was made where
  there had been a default; say if it should be a different one.
- ~~**The flag tag was pink on white.**~~ FIXED before it shipped. 2.58:1 at 11px caps. The pink
  rule down the left edge carries the colour and the word carries the meaning, which is the
  division NC-DOC-09 asks for anyway.
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
