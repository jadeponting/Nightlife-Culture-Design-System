#!/usr/bin/env python3
"""Generate the slide layer from tokens.json.

    foundations/nightlife-slides.css

Slides are built from BLOCKS — title, lead, text, label, rule, columns, callout,
closing line, rows, panel, side block, closing band, table. A PATTERN is a named
arrangement of blocks that a real deck has used (foundations/patterns.json). A
new live example either fits a pattern, or is composed from these blocks and
becomes a new pattern. Blocks change only when a token changes.

Every size is read from tokens.json type.sizes.slide.pattern, in points on a
960pt (13.33in) slide, and converted here to cqw so the slide scales. Those
points were measured from the first live deck adopted as reference.

    python3 checks/build_slides.py
"""
import json, pathlib, hashlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
T = json.loads((ROOT / "foundations" / "tokens.json").read_text())
S = T["space"]["slide"]
P = S["pattern"]
Z = T["type"]["sizes"]["slide"]["pattern"]
W = Z["slideWidthPt"]

def c(pt):
    """points on the reference slide -> container width units"""
    return f"{round(pt / W * 100, 3)}cqw"

side, tops, band, base, gutter = (S["sideMargin"], S["topMargin"], S["footerBand"],
                                  S["footerBaseline"], S["columnGutter"])
unit = float(S["unit"]["vertical"].rstrip("%"))
LH = Z["lineHeight"]
rule = P["ruleWeight"]

CSS = f"""/* GENERATED — do not edit. Source: foundations/tokens.json
   Built by checks/build_slides.py. Edit the tokens, then run python3 build.py.

   Blocks, not layouts. Patterns (foundations/patterns.json) name the
   arrangements real decks use; the reference slides live in reference/.
   Sizes are points on a 960pt slide, measured from the live reference deck:
   title {Z['title']} · lead {Z['lead']} · heading {Z['head']} · body {Z['body']} · label {Z['label']}.
   Side margins {side}. Content runs to {P['bottom']} from the foot; a closing band
   takes the bottom {P['closingBand']}.
*/

/* ---- the frame --------------------------------------------------- */
.nc-slide{{aspect-ratio:16/9;position:relative;overflow:hidden;container-type:inline-size;
  background:var(--nc-white)}}
.nc-slide,.nc-slide *{{box-sizing:border-box}}
.nc-slide .cv{{position:absolute;inset:0;font-family:var(--nc-font-body);
  font-size:{c(Z['body'])};line-height:{LH['text']}}}
/* The ground sets the title and highlight colours, so nobody picks them by hand.
   Light grounds: blue titles and headings. Dark grounds: white titles, teal headings. */
.nc-slide .ground-chalk,.nc-slide .ground-white{{--nc-title:var(--nc-blue);--nc-hl:var(--nc-blue)}}
.nc-slide .ground-blue,.nc-slide .ground-ink{{--nc-title:var(--nc-white);--nc-hl:var(--nc-teal)}}

/* ---- the pad: where content sits ---------------------------------- */
.nc-sp{{position:absolute;left:{side};right:{side};top:{tops['titleLeads']};bottom:{P['bottom']};
  display:flex;flex-direction:column;gap:{c(10)}}}
.nc-sp>*{{flex-shrink:0}}
.nc-sp--cover{{top:{tops['kickerLeads']};bottom:{base}}}
.nc-sp--band{{bottom:calc({P['closingBand']} + {round(unit * 2, 3)}%)}}
.nc-sp--side{{right:calc({P['sideBlockWidth']} + {gutter})}}
/* A spacer: pushes what follows it down. Used where the live deck lets space
   open between the title and the body (statements, the cover). */
.nc-sfill{{flex:1 1 auto}}

/* ---- type blocks ---------------------------------------------------- */
.nc-st{{font-family:var(--nc-font-display);text-transform:uppercase;font-size:{c(Z['title'])};
  line-height:{LH['title']};letter-spacing:-.01em;color:var(--nc-title);margin:0;text-wrap:balance}}
.nc-st--fit{{font-size:{c(Z['titleFit'])}}}
.nc-st--xl{{font-size:{c(Z['statement'])}}}
.nc-st--cover{{font-size:{c(Z['cover'])}}}
.nc-sl{{font-weight:600;font-size:{c(Z['lead'])};line-height:{LH['text']};margin:0}}
.nc-sl--lg{{font-size:{c(Z['leadLg'])}}}
.nc-sl--xl{{font-size:{c(Z['leadXl'])};line-height:1.2}}
.nc-sl--2xl{{font-size:{c(Z['lead2xl'])};line-height:1.15;max-width:80%}}
.nc-sl--hl{{color:var(--nc-hl)}}
.nc-sx{{font-size:{c(Z['body'])};line-height:{LH['text']};margin:0}}
.nc-slab{{font-family:var(--nc-font-head);font-weight:700;font-size:{c(Z['label'])};line-height:1.2;
  text-transform:uppercase;letter-spacing:.02em;color:var(--nc-hl);margin:0}}
.nc-smeta{{font-weight:600;font-size:{c(Z['meta'])};color:var(--nc-teal);margin:0}}
.nc-srule{{display:block;height:{rule};width:{P['ruleWidth']};background:var(--nc-acc,var(--nc-on));
  border:0;margin:0}}

/* ---- columns and their items ------------------------------------------ */
.nc-sgrid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));column-gap:{gutter};
  row-gap:{c(14)}}}
.nc-sgrid--2{{grid-template-columns:repeat(2,minmax(0,1fr))}}
.nc-sgrid--4{{grid-template-columns:repeat(4,minmax(0,1fr));column-gap:calc({gutter} / 2)}}
/* Four across takes half the gutter: measured 1.9% on the reference deck. */
.nc-si{{display:flex;flex-direction:column;gap:{c(5)};min-width:0}}
/* Three ways an item is marked, each with a fixed meaning (v1.4 §09):
   a top rule groups, a left rule sets a question or aside apart, a fill holds. */
.nc-si--rule{{border-top:{rule} solid var(--nc-acc,var(--nc-hl));padding-top:{c(8)}}}
.nc-si--left{{border-left:{rule} solid var(--nc-acc,var(--nc-hl));padding-left:{c(20)}}}
.nc-si--fill{{background:var(--nc-acc,var(--nc-teal));color:var(--nc-ink);--nc-hl:var(--nc-ink);
  padding:{c(17)} {c(15)}}}
.nc-slide .h{{font-family:var(--nc-font-head);font-weight:700;font-size:{c(Z['head'])};line-height:1.15;
  color:var(--nc-hl);margin:0;text-wrap:balance}}
.nc-slide .hc{{font-family:var(--nc-font-head);font-weight:700;font-size:{c(Z['head'])};line-height:1.15;
  color:var(--nc-hl);margin:0;text-transform:uppercase;letter-spacing:.02em}}
.nc-slide .big{{font-family:var(--nc-font-head);font-weight:700;font-size:{c(Z['lead2xl'])};line-height:1;
  color:var(--nc-hl);margin:0;text-transform:uppercase}}
.nc-slide .sub{{font-weight:600;margin:0}}
.nc-slide .b{{margin:0}}
.nc-slide .u{{font-weight:600;margin:0}}
.nc-slide .ls{{margin:0;padding-left:1.2em;font-weight:600}}

/* ---- set-apart blocks ---------------------------------------------------- */
.nc-scall{{border-left:{rule} solid var(--nc-acc,var(--nc-pink));padding-left:{c(22)};margin:0;max-width:94%}}
.nc-scall b{{font-weight:600}}
.nc-sline{{font-weight:600;font-size:{c(Z['lead'])};line-height:{LH['text']};color:var(--nc-hl);margin:0}}
.nc-sline--plain{{font-weight:400}}
.nc-sline--rule{{border-top:{rule} solid var(--nc-acc,var(--nc-hl));padding-top:{c(6)}}}
.nc-srows{{display:grid;grid-template-columns:22% minmax(0,1fr);column-gap:{gutter};margin:0}}
.nc-srows>*{{padding-block:{c(2.5)};margin:0}}
.nc-srows>:nth-child(n+3){{border-top:1px solid var(--nc-hair)}}
.nc-srows dt{{font-family:var(--nc-font-head);font-weight:700;text-transform:uppercase;letter-spacing:.02em;
  color:var(--nc-hl);line-height:1.2}}
.nc-spanel{{background:var(--nc-white);color:var(--nc-ink);--nc-hl:var(--nc-blue);
  border-top:{rule} solid var(--nc-acc,var(--nc-pink));padding:{c(14)} {c(15)};
  display:grid;grid-template-columns:22% minmax(0,1fr);column-gap:{gutter}}}
.nc-spanel .l{{font-family:var(--nc-font-head);font-weight:700;text-transform:uppercase;letter-spacing:.02em;
  color:var(--nc-hl);margin:0}}
.nc-spanel .b{{margin:0}}

/* An accent block that bleeds off the right edge. A change of ground for the
   one thing that is different in kind, never a room (v1.4 §07). */
.nc-sside{{position:absolute;right:0;width:{P['sideBlockWidth']};top:{round(unit * 14, 3)}%;bottom:{band};
  background:var(--nc-acc,var(--nc-pink));color:var(--nc-ink);--nc-hl:var(--nc-ink);
  padding:{c(16)} {side} {c(16)} {c(20)};display:flex;flex-direction:column;gap:{c(8)}}}

/* A closing band across the foot: the line the slide leaves you with. */
.nc-sband{{position:absolute;left:0;right:0;bottom:0;height:{P['closingBand']};
  background:var(--nc-blue);color:var(--nc-white);--nc-on:var(--nc-white);--nc-hl:var(--nc-teal);
  display:flex;align-items:center;justify-content:space-between;gap:{c(28)};padding:0 {side}}}
.nc-sband .t{{font-weight:600;font-size:{c(Z['leadLg'])};line-height:1.2;margin:0}}
.nc-sband .t--plain{{font-weight:400;font-size:{c(Z['body'])}}}

/* A table on a slide: for decks that are sent and read, not projected (NC-PRS-03). */
.nc-stable{{width:100%;border-collapse:collapse;font-size:{c(Z['table']['pt'])};line-height:1.25;
  font-variant-numeric:tabular-nums}}
.nc-stable th{{background:var(--nc-blue);color:var(--nc-white);font-family:var(--nc-font-head);font-weight:700;
  text-align:left;padding:{c(5)} {c(6)}}}
.nc-stable td{{padding:{c(2.5)} {c(6)};border-bottom:1px solid var(--nc-hair);vertical-align:top}}
.nc-stable tbody tr:nth-child(odd) td{{background:var(--nc-white)}}
.nc-stable .num{{text-align:right}}
.nc-stable td:not(:last-child),.nc-stable th:not(:last-child){{white-space:nowrap}}
.nc-stable tfoot td{{font-weight:700;border-top:{rule} solid var(--nc-blue);border-bottom:0}}

/* ---- furniture -------------------------------------------------------------- */
/* The wordmark is an outlined asset (NC-BRK-02): placed, never typeset. */
.nc-slogo{{display:block;width:{c(88)};color:var(--nc-on)}}
.nc-slogo svg{{display:block;width:100%;height:auto}}
.nc-slogo--cover{{width:{c(128)}}}
.nc-snum{{position:absolute;right:{side};bottom:{base};font-family:var(--nc-font-head);font-weight:700;
  font-size:{c(Z['number'])};color:var(--nc-on);font-variant-numeric:tabular-nums;margin:0}}
.nc-sband .nc-snum{{bottom:{c(12)};color:var(--nc-teal)}}
/* ---- showing slides on a page ------------------------------------------------ */
/* A deck on a page, and a live reference beside its rebuild. */
.nc-sdeck{{display:grid;gap:2.5rem;margin-block:2rem}}
.nc-sdeck .nc-slide,.nc-spair .nc-slide{{outline:1px solid var(--nc-hair)}}
.nc-spair{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1.25rem;align-items:start}}
.nc-spair img{{display:block;width:100%;height:auto;outline:1px solid var(--nc-hair)}}
.nc-spair figure{{margin:0;min-width:0}}
.nc-spair figcaption{{font-family:var(--nc-font-head);font-weight:600;font-size:.8rem;letter-spacing:.06em;
  text-transform:uppercase;margin-top:.4rem}}
@media (max-width:760px){{.nc-spair{{grid-template-columns:minmax(0,1fr)}}}}
"""
out = ROOT / "foundations" / "nightlife-slides.css"
out.write_text(CSS)
print(f"wrote nightlife-slides.css  {len(CSS):,} bytes  sha {hashlib.sha256(CSS.encode()).hexdigest()[:16]}")
print(f"slide type (pt): title {Z['title']} · lead {Z['lead']} · heading {Z['head']} · body {Z['body']} · label {Z['label']}")
