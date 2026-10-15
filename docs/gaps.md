# Known gaps

Recorded rather than patched around. A gap noted is a gap that gets fixed; a gap improvised over
becomes drift.

## Open

### 2. Diagram kit
No diagram system exists. Process chains, funnels, progressions and timelines are all needed.

**Interim rule:** build from the containment treatments and the chart ramp. **Never use PowerPoint
SmartArt defaults** — they override colour, type, spacing and outlines.

### 3. Asset stylesheets
Slides (`foundations/nightlife-slides.css`) and the component layer — long-form furniture,
tables, pull quotes, stat blocks and the chart set (`foundations/nightlife-culture.css`) — are
generated. Still nothing for marcoms assets: business cards, letterheads, social graphics, email
signatures.

### 4. Contracts for non-slide artefacts
`foundations/layouts.json` covers slides only. Reports, charts and marcoms assets need equivalent
contracts before the validator can check them.

### 5. Web / published pages
No page templates yet for nightlifeculture.co.uk or a published HTML report.

### 6. PowerPoint export
Partly addressed. Since 14 Oct 2026 (v1.5.1), `adapters/powerpoint/build_deck_pptx.py` turns any deck
in `decks/*.json` that names a `pptx` file into a native PowerPoint file: it measures the deck the
build rendered, places the measurements as editable shapes and text, embeds the four faces, and
runs `checks/inspect_pptx.py`. First deck through it: `vibe-map-partner`. Still missing: a
PowerPoint master (`.potx`) built from the slide patterns, so a deck *started* in PowerPoint
matches the HTML decks; the route is not yet a step in `build.py`; and the embedded fonts have
not yet been opened in PowerPoint itself, only in LibreOffice. `build_ukdf_pptx.js` (v1.4 sizes,
PNG wordmark) still builds only the UKDF deck.

### 6c. Two slide arrangements are provisional — logged 14 Oct 2026
The Vibe Map partner deck needed two arrangements no reference slide shows. Built from the blocks,
nothing new invented, and **waiting on Carly's decision** before either joins `patterns.json`:
- **A cover that carries paragraphs** (slide 1): title, rule, a lead at xl, three leads. The
  reference cover holds one line. Cost: the cover reads as a statement slide.
- **Steps three across with a summary cell** (slide 11): five steps and a filled butter cell in
  a three-column grid. The reference holds seven steps four across. Cost: two rows of three read
  as a grid, not a sequence.

### 6b. Masthead ground — RESOLVED 16 Aug 2026, rule still to be written
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

### 9. The type scale is not a component — RESOLVED 5 Oct 2026 (v1.5: 26 roles generated from tokens)
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

### 10. A component may be re-declared in a later section — RESOLVED 5 Oct 2026: one class, one place; type comes only from the roles, and the build refuses a component that sets its own
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

**Decided 5 Oct 2026: 12px on screen, 10pt in print, the label voice only (round two).** Was open as the document LABEL size. v1.4's size table gives
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

### 15. Public severity marks — PARKED by Carly, 4 Oct 2026
Internal status chips carry a word on a fill (NC-CHP-01). A public document has no coloured severity
mark. **Interim:** none; the word alone. **Closes when:** a real case comes up and Carly decides
against it. Do not invent RAG tags.

### 16. Other button styles and the icon set
One blue button, one text action, one search icon. **Interim:** build any further action from these
two; say the icon is missing rather than drawing one. **Closes when:** a second button or a second
icon is needed in live work and chosen.

### 17. Ink and charcoal are visually indistinguishable
Carly, round two: "isn't all the font charcoal?" Charcoal is the colour of the small and label roles,
ink of everything else; on a chalk ground the two cannot be told apart. **Interim:** both stay as
the tokens have them. **Closes when:** Carly decides whether charcoal stays a text colour.

### 18. Chart marks keep their own sizes
`.nc-stat .big`, the bar and dot labels and values, segment and series labels, and the footnote
markers are sized to their chart, outside the six steps. They are the one permitted exception and
are named as "Specified outside the roles" in `foundations/type-manifest.json`. **Closes when:**
the chart set is next revised and the marks move onto the roles.

### 19. Office templates are not generated from the roles
The Word, Excel and PowerPoint adapters each build one document (the Operating Plan, the budget
workbook, the UKDF deck) and carry style sets of their own: the Word one names styles but types in
sizes; Excel sets Inter 11; PowerPoint sets sizes per text box. The roles now carry the Word style
name for each; the templates that read them do not exist yet. **Cost:** amber until a Word document
is next produced. **Closes when:** `adapters/word` builds a `.dotx` from `type.roles`, and the
other two follow.

**Word test, 14 Oct 2026:** a reading copy of the supplied Vibe Map partner-deck content uses
the current role sizes, native named styles, embedded supplied fonts and the outlined wordmark.
Slide numbers become Heading 2 sections and their full questions become Heading 3 subsections,
preserving long source headings in sentence case instead of rewriting them for the caps limit.
The Title has outline level 1. The masthead/paragraph geometry is a provisional Word adaptation
of the existing component treatments, marked in the file's footer; it is not an adopted general
Word template. Source speaker notes and editorial notes remain secondary text, unchanged.

**Excel planning test, 14 Oct 2026:** the existing Vibe Map working plan uses the
live body, small, Heading 3 and Heading 4 roles, a blue masthead, the supplied
outlined wordmark and the editorial table treatment. This is a provisional
adaptation of this workbook, not a general template. Excel cannot apply tracked
All Caps as a character format or embed these fonts in an ordinary XLSX; preserve
the original header strings in the sentence voice and use installed Inter and
Archivo. Those fonts are present on Carly’s Mac; another reader needs them too.
Timeline duration bars use blue with outlines/dashes for scope and conditional
states, and ink for recorded history, with a written key; coloured accents remain
word-labelled status surfaces. Cost: native spreadsheet leading and line weights
are approximate, and the inspector does not validate typography roles or drawings.
The work stays editable and does not establish new brand decisions.

### 20. The library's sample chapter sits inside the page's own outline
The reference sheet's h1 and h2 are taken by the page, so specimens of heading roles sit on deeper
elements than the rule allows in a document. `validate.py` exempts headings inside a
`.nc-specimen`. **Interim:** the note under the specimen says so. **Closes when:** the library
renders specimens in isolated frames.

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

Found by the full read of 29 September 2026 — every live file, the build run, each claim checked
against the file and line. Fixed that day where the right answer was already recorded; the rest
below need a decision or a larger job.

- **NC-CON-02 counts hairline declarations, not uses.** It now fires as a warning on every page
  because it counts the hairlines defined in the inlined stylesheet. Needs rewriting to count uses.
- **Fixed-tier checks that only warn.** `validate.py` says "exit 1 on any Fixed breach" but routes
  NC-TYP-01, CON-02, LAY-04, TYP-15, EVI-09, PSE-01, TBL-01, DOC-04 and part of DAT-05 to
  warnings. Making them fail will turn the build red until the breaches are fixed. Needs Carly's go.
- **Checks that cannot see what they test.** NC-TYP-04 and NC-CON-01 read px only, while every
  component is in em; NC-TBL-01 only runs inside blocks that set uppercase; the NC-TYP-01
  acronym exemption matches substrings ("FINANCE"); NC-COL-01 checks white-on-light but not
  accent fills. 29 rules declared machine-checkable are implemented nowhere.
- **Invented greys and translucencies.** `C9C9C9` in the Word adapter; `#000000` in the allowlist; `rgba(13,13,13,.10)` as `--nc-grid` and
  seven other translucent inks and whites with no token.
- **`.acc-blue` can feed fill components that hard-set ink text** — ink on blue, 2.26:1. Latent.
- ~~**NC-TYP-06 sets a 13px note floor** — and captions (12.5px) and source lines (12.8px) break even that.~~
  FIXED 5 Oct 2026: small is 14px, the label voice alone is 12px, nothing else exists under 14px.
- **The Office adapters are outside the build.** 14pt caps labels in the UKDF .pptx and 10.5pt caps
  in the .docx; the UKDF .pptx places a raster PNG wordmark. The v1.5.1 deck route places the
  outlined SVG, with a PNG fallback for older Office.
- ~~**Slide titles were faux-bold.**~~ FIXED 14 Oct 2026. `.nc-st` sat on an h2 without a weight,
  so browsers thickened Archivo Black to fake a bold it does not have, on every HTML deck including
  the AMGP rebuild. The weight is now stated, and `check_contrast.py` fails any Archivo Black text
  asked for more than 400.
- **The repo's font files carry the subsetter's internal names** (Archivo 700 calls itself
  "Archivo SemiBold" Bold). Harmless on the web, where `@font-face` names the family; wrong in
  Office. The PowerPoint route renames its copies; `assets/fonts` is untouched.
- **`adapters/powerpoint/node_modules/` is committed** — about 360 third-party files in git.

## Closed

- Dense layout tier — closed 29 Sep 2026 by the live reference deck (`reference/amgp-v2.0`): the
  working-slide patterns in `foundations/patterns.json`, at its measured sizes.
- Slide contracts recorded but not enforced — closed 29 Sep 2026: the twelve generated layouts and
  `layouts.json` are archived; every slide names a registered pattern, the build fails an unknown
  one, and a browser check fails any slide whose content overflows (NC-LAY-07).
- Slide type below the floors, vertical percentages resolving against width, `.nc-sub` meaning two
  things, content in the footer band — closed 29 Sep 2026 with the archived slide layer. Slide
  sizes now come from `tokens.json` in points: body 18pt.
- `dist/index.html` written by two builds — closed 29 Sep 2026.
- `--nc-charcoal` never defined; a skipped contrast check reading as a pass; two layout titles
  missing `>`; NC-CON-02 matching a variable that did not exist; NC-BRK-01 accepting any version
  string — fixed 29 Sep 2026.
- Slide layouts undocumented; no enforcement; slides hanging from the top — v1.0.
