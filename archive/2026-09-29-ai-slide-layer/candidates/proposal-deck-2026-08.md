# Candidate layouts — proposal deck family (August 2026)

**Status:** candidate, not committed contracts. Extracted from the UKDF fellowship proposal deck
(`~/Documents/GitHub/ukdf-application/`), built 17 Aug 2026, approved by Carly on sight.
Validated visually and for accessibility; NOT yet run through `checks/validate.py`. Encode as
contracts in a Phase 2/3 pass. Where this file and `AGENTS.md`/existing contracts disagree,
resolve explicitly — do not silently overwrite either.

## The artefact family

A **sent proposal deck** (decision book ch. 12): nobody is speaking, every surface carries its own
message. Claim-stating titles that read as the pitch in outline; full sentences welcome; detail
lives on chalk/white grounds; a real table is permitted because the deck IS the leave-behind.
Companion rule: an internal operating plan holds the workings; the deck never carries them.

## The eight layouts (16:9, 1280×720 reference, all values scale as cqw)

1. **Blue bookend — cover.** Blue ground. Kicker (white, caps, 12pt) → Archivo Black display
   (60pt, two lines, 0.95 line) → pink separator (224×5) → bold standfirst (Archivo 16pt, white,
   max-width 58%) → footer: wordmark left, name right. No page number.
2. **Blue statement — symmetric two-column contrast.** Kicker/title/pink separator, then two
   IDENTICAL columns (x=77 and x=678, w=525): pink top rule (4px) → white caps label → bold
   Archivo keyword line → Inter body. Symmetry is the point: neither side "wins" typographically;
   the argument does. Bottom: pull quote (below).
3. **Mechanism page — accent three-cell row + timeline strip.** Chalk. Three accent cells
   (teal/violet/butter, 364×132, ink text, caps label + body). Below, a blue caps section label,
   then a 7-cell timeline strip: white cells (150×145), 3px blue top rule, blue caps year, Inter
   9pt body. One grey source line under. Dense tier: coverage ~68%.
4. **Receipts page — stat-cell row + accent row + pull quote.** Chalk. Lede (2 lines max) →
   pink-bar pull quote → four stat cells (white, 270 wide, **5px pink top rule**, Archivo Black
   number in blue, Inter label, grey source line — source line is mandatory) → three butter cells
   (caps label + body). Numbers and their labels/sources must stay one unit in DOM/z-order.
5. **Panel page — white panel with pink top rule.** Chalk. Body paragraph → full-width white
   panel with 5px pink top rule (the guide's "top rule" component at slide scale) carrying caps
   label + body → caps label + running-text list → grey caveat line.
6. **Three-phase plan.** Chalk. Three columns (354 wide, 3px blue top rule, blue caps label with
   month range, Inter body) → full-width white panel, 3px blue top rule, for the delivery caveat.
7. **Ladder table.** White ground (not chalk — table register). Caps header row, 2px ink rule,
   5 rows × 72px with 1px #D8D8D8 hairlines, rung column in blue caps. Bold-lead closing line.
   Tables allowed ONLY in sent artefacts.
8. **Blue bookend — the ask.** Mirrors the cover: kicker, display title, pink separator, three
   white-top-ruled money columns (Archivo Black number, white caps label, Inter body), closing
   paragraph, wordmark + contact footer.

## New/changed components

- **Pull quote, slide scale:** 8px pink left bar, Archivo bold 13–13.5pt, ink on light / white on
  blue, optional grey source line beneath. Promoted content, never a footnote.
- **Stat cell:** white panel, pink top rule, number/label/source. Source line mandatory.
- **Timeline strip:** 7 white cells, blue top rules. A biography as evidence, not decoration.

## Decision log (do not lose)

- **D-A · Teal retired from accent duty on blue grounds in this family.** Carly, 17 Aug: teal on
  blue is "vibratory on my eyes". Replaced with the pink family (separators, top rules, pull-quote
  bars) + calm white furniture (kickers, labels, page numbers). ⚠ Tension with `slides.md`
  ("teal is the section-header colour on every dark ground") — candidate amendment, to be
  reconciled when this file becomes contracts. Teal keeps its role in accent CELLS on light
  grounds (mechanism row) where it is a black-text surface.
- **D-B · Pink-on-blue is graphic-only.** ~3.4:1 — passes non-text (≥3:1), fails small text.
  Pink rules and bars on blue: yes. Pink text on blue: never. Labels on blue are white.
- **D-C · Takeaway-first rule.** Before shipping any page, name its single most important
  sentence; if it is set as a footnote or source line, the page is wrong. (Found live: the
  "four years of graft" line was a footnote; it became the pull quote.)
- **D-D · Sent-deck register** per decision book ch. 12 — see family description above.
- **D-E · Accessibility export pipeline (mandatory, all future decks):**
  - HTML is the semantic source: titles carry `role="heading"` + `aria-level` (cover=1, slides=2);
    decorative rules/separators/page numbers carry `aria-hidden="true"`; DOM order = reading
    order (column 1 complete, then column 2; number+label+source as one unit).
  - PDF is exported **tagged** (Playwright `page.pdf(tagged=True)`); verify the output contains
    `StructTreeRoot`, `/Marked true` and `/Lang`. Never ship an untagged print-to-PDF.
  - PPTX: z-order = reading order; decorative (empty) shapes moved before all text shapes; slide
    names set to content titles; core properties (title, author, language en-GB) set.
    Script: `~/Documents/GitHub/ukdf-application/build/accessibility_export.py`.
- **D-F · Source-of-truth chain.** The deck HTML is the master; the PPTX is the hand-edit mirror.
  Whichever was edited last is exported and submitted — and the other is updated to match before
  the next derivation.

## Exemplars

`~/Documents/GitHub/ukdf-application/AMGP-UKDF-Supporting-Document.html` (source),
`Artists-Make-Great-Places-UKDF-Supporting-Document.pdf` (tagged export), `.pptx` (a11y-ordered).
