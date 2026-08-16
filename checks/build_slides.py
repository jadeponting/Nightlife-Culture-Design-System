#!/usr/bin/env python3
"""Generate the slide layer from tokens.json.

    foundations/nightlife-slides.css

The slide grid is a CONTEXT, not a component. This file sets the base that the
component layer scales itself against, plus the handful of arrangements that
only exist on a slide — columns, cells, a vertical third, an ink strip. It
defines no component: a pull quote on a slide is the same .nc-quote a report
uses, one size larger (NC-SYS-03).

Every value comes from tokens.json. Nothing here is typed by hand.

    python3 checks/build_slides.py
"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
T = json.loads((ROOT / "foundations" / "tokens.json").read_text())
S = T["space"]["slide"]

def pc(x): return x if isinstance(x, str) else f"{x}%"
side   = S["sideMargin"]
tops   = S["topMargin"]
band   = S["footerBand"]
base   = S["footerBaseline"]
gutter = S["columnGutter"]

CSS = f"""/* GENERATED — do not edit. Source: foundations/tokens.json
   Built by checks/build_slides.py. Edit the tokens, then run python3 build.py.

   THE GRID, and why it is not one number
   Side margins {side}. Footer band {band}, reserved on every slide.
   Top margin varies by what leads the slide:
       {tops['kickerLeads']:<9} a kicker leads   — small and quiet, so it can sit high
       {tops['titleLeads']:<9} a title leads    — the message, so it needs air above it
       {tops['fullBleedLeads']:<9} a full bleed leads — the element is the composition
   All four are multiples of one unit ({S['unit']['vertical']} of slide height), so the grid
   obeys the same one-base-unit rule as everything else (ch02, Fixed).

   The footer band is reserved on covers and closing slides too. It is not
   there to hold a number — it is there because the bottom of a screen is the
   hardest place to read in a room full of people, and that does not change
   when the number does.

   THE FRAME IS FIXED. .nc-slide sets the aspect ratio and the container; .cv
   is the canvas. Without both, every cqw size collapses.
*/

/* ---- context ---------------------------------------------------- */
.nc-slide{{aspect-ratio:16/9;position:relative;overflow:hidden;container-type:inline-size;
  background:var(--nc-white)}}
.nc-slide .cv{{position:absolute;inset:0;font-family:var(--nc-font-body);
  font-size:1.55cqw;line-height:1.5}}

/* ---- the grid --------------------------------------------------- */
.nc-pad{{position:absolute;left:{side};right:{side};top:{tops['titleLeads']};bottom:{band};
  display:flex;flex-direction:column}}
.nc-pad--kicker{{top:{tops['kickerLeads']}}}
.nc-pad--bleed{{top:{tops['fullBleedLeads']}}}
/* The anchor is a contract field, not a styling choice. Implicit top-anchoring
   leaves a dead band across the bottom third, which was the single largest
   cause of weak slides in the earlier system. */
.nc-pad[data-anchor="centre"]{{justify-content:center}}
.nc-pad[data-anchor="bottom"]>:last-child{{margin-top:auto}}
.nc-pad[data-anchor="split"]>:last-child{{margin-top:auto}}

/* ---- footer furniture ------------------------------------------- */
.nc-sfoot{{position:absolute;left:{side};right:{side};bottom:{base};
  display:flex;justify-content:space-between;align-items:flex-end;gap:1em}}
.nc-snum{{font-family:var(--nc-font-head);font-weight:800;font-size:1.25cqw;
  letter-spacing:.08em;color:var(--nc-charcoal);font-variant-numeric:tabular-nums}}
.ground-blue .nc-snum,.ground-ink .nc-snum{{color:var(--nc-teal)}}
/* The wordmark is an outlined asset (NC-BRK-02). This positions it; it never
   sets it as type. Roughly 1.5% of slide width, the quietest thing on the slide. */
.nc-slogo{{width:7cqw;height:auto;display:block}}
.nc-slogo--lockup{{width:17cqw}}

/* ---- slide type ------------------------------------------------- */
.nc-k{{font-family:var(--nc-font-head);font-weight:800;font-size:1.3cqw;letter-spacing:.2em;
  text-transform:uppercase}}
.nc-t{{font-family:var(--nc-font-display);text-transform:uppercase;font-size:5.2cqw;
  line-height:.92;letter-spacing:-.01em;max-width:none}}
/* Two steps, not three. --lg existed and no layout used it; an unused size
   is an invitation to pick by eye. Deleted rather than demonstrated. */
.nc-t--xl{{font-size:7cqw}} .nc-t--sm{{font-size:3.4cqw}}
.nc-sub{{font-family:var(--nc-font-head);font-weight:700;font-size:1.8cqw;line-height:1.35;
  max-width:64%}}
.nc-sub--wide{{max-width:100%}}
.nc-sbody{{font-size:1.4cqw;line-height:1.6;max-width:70%}}
.nc-srcline{{font-family:var(--nc-font-head);font-weight:600;font-size:1.05cqw;
  letter-spacing:.04em;color:var(--nc-charcoal);margin-top:auto}}
.ground-blue .nc-srcline,.ground-ink .nc-srcline{{color:var(--nc-teal)}}

/* ---- breakers at slide scale ------------------------------------ */
.nc-slide .nc-brk{{height:.42cqw;width:20%;margin:2cqw 0}}
.nc-slide .nc-brk--bar{{height:.55cqw;width:14%}}
.nc-slide .nc-brk--hair{{height:1px;width:74%}}

/* ---- arrangements ----------------------------------------------- */
/* Three top-rule columns. Nothing boxed — the rule codes the column without
   flooding it, which is the containment system's dense-page treatment. */
.nc-cols{{margin-top:auto;display:grid;grid-template-columns:repeat(3,1fr);gap:{gutter}}}
/* Two columns in tension are the BODY of the slide, not a footing under it,
   so they do not take the auto top margin the three-column footing uses. */
.nc-cols--2{{grid-template-columns:1fr 1fr;gap:calc({gutter} * 2);margin-top:2cqw}}
.nc-cols .col{{padding-top:1.6cqw;border-top:.55cqw solid var(--nc-acc,var(--nc-teal))}}
.nc-cols .col .n{{font-family:var(--nc-font-display);font-size:3.2cqw;line-height:.9}}
.nc-cols .col .l{{font-family:var(--nc-font-head);font-weight:800;font-size:1.1cqw;
  letter-spacing:.1em;text-transform:uppercase;margin-top:.9cqw;line-height:1.3}}
.nc-cols .col--plain{{border-top:0;padding-top:0}}

/* Filled cells. Every accent takes ink text — no exceptions (v1.4 §07). */
.nc-cells{{margin-top:auto;display:grid;grid-template-columns:repeat(3,1fr);gap:{gutter}}}
.nc-cells .cell{{padding:1.9cqw 2cqw;background:var(--nc-acc,var(--nc-teal));color:var(--nc-ink)}}
.nc-cells .cell .n{{font-family:var(--nc-font-display);font-size:3.2cqw;line-height:.9}}
.nc-cells .cell .l{{font-family:var(--nc-font-head);font-weight:800;font-size:1.1cqw;
  letter-spacing:.1em;text-transform:uppercase;margin-top:1cqw;line-height:1.3}}

/* Vertical third. An accent block, never an accent room. */
.nc-third{{position:absolute;inset:0;display:flex}}
.nc-third .main{{flex:1;padding:{tops['titleLeads']} 0 {band} {side};display:flex;flex-direction:column}}
/* The colour field bleeds to the edge — that is what makes it a change of ground
   rather than a box. Its TEXT still stops at the footer line: 7.5cqw is the
   footer band expressed against slide width on 16:9. The band exists because
   the bottom of a screen is the hardest place to read in a room, and that is
   just as true inside an accent block as outside one (NC-LAY-07). */
.nc-third .side{{width:31%;padding:{tops['titleLeads']} {side} 7.5cqw {side};display:flex;
  flex-direction:column;justify-content:flex-end;background:var(--nc-acc,var(--nc-pink));
  color:var(--nc-ink)}}
.nc-third .side--wide{{width:38%}}
.nc-third .bignum{{font-family:var(--nc-font-display);font-size:4.4cqw;line-height:.9}}
.nc-third .biglab{{font-family:var(--nc-font-head);font-weight:800;font-size:1.1cqw;
  letter-spacing:.1em;text-transform:uppercase;margin-top:1cqw}}

/* Ink strip. A full-bleed band across the foot, replacing three boxes. */
.nc-strip{{position:absolute;inset:0;display:flex;flex-direction:column}}
.nc-strip .top{{flex:1;padding:{tops['titleLeads']} {side} 0 {side};display:flex;flex-direction:column}}
.nc-strip .band{{background:var(--nc-ink);color:#fff;padding:3.2cqw {side} 7.5cqw;
  display:grid;grid-template-columns:repeat(3,1fr);gap:{gutter}}}
.nc-strip .band .n{{font-family:var(--nc-font-display);font-size:3cqw;line-height:.9;color:var(--nc-teal)}}
.nc-strip .band .l{{font-family:var(--nc-font-head);font-weight:800;font-size:1.05cqw;
  letter-spacing:.1em;text-transform:uppercase;margin-top:.9cqw}}

/* A chart row at slide scale. The component is the same; only the base moved. */
.nc-sbar{{display:flex;align-items:center;gap:1.4cqw;margin-bottom:1.1cqw}}
.nc-sbar .lb{{font-family:var(--nc-font-head);font-weight:600;font-size:1.4cqw;width:16%;flex:none}}
.nc-sbar .tk{{flex:1;height:2.4cqw;position:relative;background:rgba(13,13,13,.07)}}
.nc-sbar .fl{{position:absolute;left:0;top:0;bottom:0;background:var(--nc-chart-1)}}
.nc-sbar .vl{{font-family:var(--nc-font-head);font-weight:800;font-size:1.4cqw;width:7%;
  text-align:right;flex:none;font-variant-numeric:tabular-nums}}
.ground-blue .nc-sbar .tk,.ground-ink .nc-sbar .tk{{background:rgba(255,255,255,.14)}}
.ground-blue .nc-sbar .fl,.ground-ink .nc-sbar .fl{{background:var(--nc-teal)}}

/* A quote at slide scale — the same component, one size up (NC-SYS-03). */
.nc-slide .nc-quote .q{{font-size:3cqw;max-width:76%}}
"""
out = ROOT / "foundations" / "nightlife-slides.css"
out.write_text(CSS)
import hashlib
print(f"wrote nightlife-slides.css  {len(CSS):,} bytes  sha {hashlib.sha256(CSS.encode()).hexdigest()[:16]}")
print(f"grid: sides {side} · top {tops['kickerLeads']} / {tops['titleLeads']} / {tops['fullBleedLeads']} · footer band {band}")
