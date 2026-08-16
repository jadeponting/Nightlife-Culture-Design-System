#!/usr/bin/env python3
"""Generate nightlife-culture.css from tokens.json.

The component specs are Carly's own, from headers.html (the gen-2 build) — em-based,
nc- namespaced, one layer consumed by documents AND slides. The context sets the base;
the component scales itself. Never hard-code px inside a component.

    python3 checks/build.py
"""
import json, pathlib, hashlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
T = json.loads((ROOT/"foundations"/"tokens.json").read_text())
C, TY, SP = T["colour"], T["type"], T["space"]
G = {k:v["hex"] for k,v in C["grounds"].items()}
A = {k:v["hex"] for k,v in C["accents"].items() if isinstance(v,dict)}
RAMP = C["chartRamp"]["series"]

css = f"""/* =============================================================
   Nightlife Culture — component layer
   GENERATED from foundations/tokens.json by checks/build.py
   DO NOT EDIT BY HAND. Edit the tokens and rebuild.
   Source of truth: {T['meta']['source']}
   Component specs: headers.html (gen-2 build), containment v1.3,
   furniture v1.6, charts v1.4, joy.html
   ============================================================= */

/* Every size is in em. The CONTEXT sets the base, the component scales
   itself. That is what makes a pull quote in a report and a pull quote on
   a slide the same component rather than two things that drift apart.
   Never hard-code px inside a component. Never redefine a component in a
   context file — those set context and nothing else. */

:root{{
{chr(10).join(f'  --nc-{k}: {v};' for k,v in G.items())}
{chr(10).join(f'  --nc-{k}: {v};' for k,v in A.items())}
{chr(10).join(f'  --nc-chart-{i}: {h};' for i,h in enumerate(RAMP,1))}
{chr(10).join(f"  --nc-{k}: {v};" for k,v in SP["scale"]["steps"].items())}
{chr(10).join(f"  --nc-slide-{k}: {v};" for k,v in SP["slideScale"]["steps"].items())}
  --nc-hair: {C['hairline']};
  --nc-grid: rgba(13,13,13,.10);
  --nc-font-display: "Archivo Black",Arial Black,sans-serif;
  --nc-font-head: "Archivo",Arial,sans-serif;
  --nc-font-body: "Inter",Arial,sans-serif;
}}

/* --- 0 · CONTEXT — sets the base, defines nothing ---------------- */
.nc-doc{{font-size:16px;font-family:var(--nc-font-body);line-height:1.6;color:var(--nc-ink)}}
.nc-slide .cv{{font-size:1.55cqw;font-family:var(--nc-font-body);line-height:1.5}}

/* --- 1 · GROUNDS ------------------------------------------------- */
.ground-blue{{background:var(--nc-blue);color:#fff}}
.ground-ink{{background:var(--nc-ink);color:#fff}}
.ground-chalk{{background:var(--nc-chalk);color:var(--nc-ink)}}
.ground-white{{background:var(--nc-white);color:var(--nc-ink)}}
/* Teal is the section-header colour on EVERY dark ground — one rule, not two.
   Butter kicker on ink read as a warning label. (slides v1.5, fix 3) */

/* --- 2 · ACCENT MODIFIER — colour is never baked into a component -- */
{chr(10).join(f'.acc-{k}{{--nc-acc:var(--nc-{k})}}' for k in A)}
.acc-blue{{--nc-acc:var(--nc-blue)}}

/* --- 3 · SECTION HEADER — documents and web. NOT FOR SLIDES. ------
   Rule BELOW. Numeral in a filled box, vertically centred, Archivo
   ExtraBold at H3 scale — not Archivo Black at display scale, so the
   weights sit together instead of competing. The numeral is OPTIONAL;
   an invented number is worse than none. */
.nc-section-head{{display:flex;align-items:center;gap:var(--nc-sp4);
  border-bottom:.19em solid var(--nc-ink);padding-bottom:var(--nc-sp3);margin-bottom:var(--nc-sp5)}}
.nc-section-head .num{{font-family:var(--nc-font-head);font-weight:800;font-size:.94em;
  letter-spacing:.04em;background:var(--nc-ink);color:var(--nc-chalk);
  padding:var(--nc-sp2) var(--nc-sp2);line-height:1;display:flex;align-items:center;flex:none}}
.nc-section-head .ttl{{font-family:var(--nc-font-head);font-weight:800;text-transform:uppercase;
  font-size:clamp(1.15em,4.6vw,1.65em);letter-spacing:.02em;line-height:1.05;
  min-width:0;flex:1;hyphens:none;overflow-wrap:break-word}}
/* Display type NEVER hyphenates — a broken word in Archivo ExtraBold at heading
   scale reads as a fault, not a line break. hyphens:none forbids the hyphen;
   overflow-wrap:break-word still lets a word too long for its container wrap,
   without inserting one. Those are different properties and confusing them is
   what put hyphens in the headings. The numeral stays locked to the title (the
   row does not wrap); the title shrinks and wraps inside itself, so 320px
   reflow holds without splitting the lockup. SC 1.4.10, Fixed. */
.ground-blue .nc-section-head,.ground-ink .nc-section-head{{border-bottom-color:var(--nc-teal)}}
.ground-blue .nc-section-head .num,.ground-ink .nc-section-head .num{{
  background:var(--nc-teal);color:var(--nc-ink)}}
.nc-section-head:not(:has(.num)){{gap:0}}

/* --- 4 · CONTAINMENT — colour and space, not outlines -------------
   Hard outline is NOT retired outright: it is reserved for the flyer
   register — covers, posters, dividers. "That way the box means
   something when it does turn up." (containment v1.3) */
.nc-panel{{padding:var(--nc-sp4) var(--nc-sp5)}}
.nc-panel--fill{{background:var(--nc-acc,var(--nc-teal));color:var(--nc-ink)}}
.nc-panel--top{{background:var(--nc-white);border-top:.56em solid var(--nc-acc,var(--nc-teal))}}
.nc-panel--left{{background:var(--nc-white);border-left:.75em solid var(--nc-acc,var(--nc-pink))}}
.nc-panel--hair{{background:var(--nc-white);outline:1px solid var(--nc-hair);outline-offset:-1px}}
.nc-panel--flyer{{background:var(--nc-acc,var(--nc-teal));border:2px solid var(--nc-ink);color:var(--nc-ink)}}
.nc-band{{padding:var(--nc-sp5) max(var(--nc-bleed,0px),var(--nc-sp5));
  margin-left:calc(var(--nc-bleed,0px) * -1);margin-right:calc(var(--nc-bleed,0px) * -1);
  background:var(--nc-acc,var(--nc-violet));color:var(--nc-ink)}}
/* Horizontal padding falls back to the standard panel inset when the band is
   not actually bleeding. Without the max() it rendered at zero — text hard
   against the colour edge. Found on a phone. */
.nc-panel .lab,.nc-band .lab{{font-family:var(--nc-font-head);font-weight:800;
  text-transform:uppercase;font-size:.72em;letter-spacing:.06em;margin-bottom:var(--nc-sp2)}}
.nc-panel .txt,.nc-band .txt{{font-size:.85em;line-height:1.45}}
/* The band is a containment treatment like the other five, so its internals take
   the same specs. Targeting .nc-panel alone let .nc-band fall through to inherited
   size and sentence case — invisible until they sat side by side on a phone. */

/* --- 5 · PULL QUOTE — the 12px pink rule, as an em ---------------- */
.nc-quote{{border-left:.75em solid var(--nc-acc,var(--nc-pink));padding:var(--nc-sp1) 0 var(--nc-sp1) var(--nc-sp5);margin:var(--nc-sp5) 0}}
.nc-quote .q{{font-family:var(--nc-font-head);font-weight:800;font-size:1.45em;line-height:1.24;max-width:40ch}}
.nc-quote .a{{font-size:.8em;color:var(--nc-charcoal);margin-top:var(--nc-sp3)}}
.nc-quote.lg .q{{font-size:2.1em;max-width:30ch}}
.ground-blue .nc-quote .a,.ground-ink .nc-quote .a{{color:var(--nc-teal)}}

/* --- 6 · BREAKOUT STAT — the source line is part of the component,
   not an afterthought. A big number without period, geography and
   provenance is a claim, not a finding. */
.nc-stat{{background:var(--nc-white);outline:1px solid var(--nc-hair);outline-offset:-1px;
  padding:var(--nc-sp4) var(--nc-sp5);border-left:.62em solid var(--nc-acc,var(--nc-blue))}}
.nc-stat--top{{border-left:0;border-top:.56em solid var(--nc-acc,var(--nc-teal))}}
.nc-stat--fill{{outline:0;border:0;background:var(--nc-acc,var(--nc-butter));color:var(--nc-ink)}}
.nc-stat .big{{font-family:var(--nc-font-display);font-size:2.4em;line-height:.9;letter-spacing:-.02em}}
.nc-stat .lb{{font-family:var(--nc-font-head);font-weight:800;font-size:.66em;
  text-transform:uppercase;letter-spacing:.1em;margin-top:var(--nc-sp4);line-height:1.3}}
.nc-stat .src{{font-size:.69em;color:var(--nc-charcoal);margin-top:var(--nc-sp3);line-height:1.4}}
.nc-stat.lg .big{{font-size:3.4em}}

/* --- 7 · EVIDENCE FURNITURE — from the methodology. Not decorative.
   Ink = open and traceable · butter = documented but partial ·
   coral = opaque or untraceable. Coral never means "bad" — it means
   "handle with a stated caveat". The code text carries the meaning on
   its own, so the tier survives greyscale and screen readers. */
.nc-evidence{{display:flex;align-items:baseline;flex-wrap:wrap;gap:var(--nc-sp1) 0}}
.nc-prov{{display:inline-block;font-family:var(--nc-font-head);font-weight:800;font-size:.68em;
  letter-spacing:.09em;padding:var(--nc-sp1) var(--nc-sp2);background:var(--nc-ink);color:var(--nc-white);
  margin:0 var(--nc-sp2) 0 0;line-height:1.35;vertical-align:baseline;text-transform:uppercase}}
.nc-prov--mid{{background:var(--nc-butter);color:var(--nc-ink)}}
.nc-prov--low{{background:var(--nc-coral);color:var(--nc-ink)}}
.nc-source{{font-family:var(--nc-font-head);font-weight:600;font-size:.8em;letter-spacing:.04em;
  color:var(--nc-charcoal);line-height:1.5;text-transform:none}}
.ground-blue .nc-source,.ground-ink .nc-source{{color:var(--nc-teal)}}
.nc-meter{{display:flex;gap:var(--nc-sp1);margin:var(--nc-sp1) 0 var(--nc-sp2)}}
.nc-meter span{{flex:1;height:.9em;background:var(--nc-chalk);outline:1px solid var(--nc-hair);outline-offset:-1px}}
.nc-meter span.on{{background:var(--nc-ink);outline-color:var(--nc-ink)}}
.nc-meter-lab{{display:flex;justify-content:space-between;font-family:var(--nc-font-head);
  font-weight:600;font-size:.64em;letter-spacing:.04em;text-transform:uppercase;color:var(--nc-charcoal)}}

/* --- 8 · BREAKERS — one per surface. A separator, not an ornament.
   Mid-statement break is RETIRED: it interrupts the sentence. */
.nc-brk{{height:.26em;width:20%;background:var(--nc-acc,var(--nc-blue));border:0;margin:var(--nc-sp4) 0}}
.nc-brk--bar{{height:.34em;width:14%;background:var(--nc-acc,var(--nc-pink))}}
.nc-brk--hair{{height:1px;width:74%;background:var(--nc-hair)}}
.ground-blue .nc-brk,.ground-ink .nc-brk{{background:var(--nc-teal)}}

/* --- 9 · TABLE — editorial is the default. No fill, no vertical
   rules, no outer border. 2.25px ink rule under the header. */
.nc-table{{border-collapse:collapse;width:100%;font-size:.88em;background:transparent}}
.nc-table th,.nc-table td{{padding:var(--nc-sp3) var(--nc-sp4) var(--nc-sp3) 0;text-align:left;vertical-align:top;
  border-bottom:1px solid rgba(13,13,13,.13)}}
.nc-table th{{font-family:var(--nc-font-head);font-weight:700;text-transform:uppercase;
  font-size:.75em;letter-spacing:.12em;color:var(--nc-charcoal);
  border-bottom:.16em solid var(--nc-ink);padding-bottom:var(--nc-sp2)}}
.nc-table td:last-child,.nc-table th:last-child{{padding-right:0}}
.nc-table .num{{font-variant-numeric:tabular-nums;text-align:right;white-space:nowrap}}
.nc-table--accent{{border-top:.44em solid var(--nc-acc,var(--nc-teal))}}
.nc-table--accent th{{border-bottom:1px solid rgba(13,13,13,.20);padding-top:.75em}}
.nc-table--band tbody tr:nth-child(odd){{background:rgba(13,13,13,.035)}}
.nc-table--band td{{border-bottom:0}}
.ground-blue .nc-table th,.ground-ink .nc-table th{{color:var(--nc-teal);border-bottom-color:var(--nc-teal)}}
.ground-blue .nc-table td,.ground-ink .nc-table td{{border-bottom-color:rgba(255,255,255,.22)}}

/* --- 10 · CHART CARD — every chart ships as a package.
   title · subtitle carrying unit and population · the chart ·
   the evidence block. Single series = single colour. Label at the
   mark. Hatched = suppressed [c] or not collected n/a — never a
   blank row, because a gap in the data is a finding. */
.nc-chart{{background:var(--nc-white);outline:1px solid var(--nc-hair);outline-offset:-1px;
  padding:var(--nc-sp5) var(--nc-sp5) var(--nc-sp4);border-top:.5em solid var(--nc-acc,var(--nc-blue))}}
.nc-chart .ct{{font-family:var(--nc-font-head);font-weight:800;text-transform:uppercase;
  font-size:.88em;letter-spacing:.05em;line-height:1.15}}
.nc-chart .cs{{font-size:.78em;color:var(--nc-charcoal);margin:var(--nc-sp1) 0 var(--nc-sp4)}}
.nc-chart .ev{{margin-top:var(--nc-sp4);padding-top:var(--nc-sp3);border-top:1px solid var(--nc-hair);
  font-size:.72em;line-height:1.5;color:var(--nc-charcoal)}}
.nc-chart .ev b{{font-family:var(--nc-font-head);font-weight:800;letter-spacing:.05em;
  text-transform:uppercase;font-size:.86em;color:var(--nc-ink)}}
.nc-bar{{display:flex;align-items:center;gap:var(--nc-sp3);margin-bottom:var(--nc-sp2)}}
.nc-bar .lb{{font-size:.78em;width:7.5em;flex:none;font-weight:500}}
.nc-bar .tk{{flex:1;height:1.5em;position:relative;
  background:linear-gradient(90deg,var(--nc-grid) 1px,transparent 1px) 0 0/25% 100%}}
.nc-bar .fl{{position:absolute;left:0;top:0;bottom:0;background:var(--nc-chart-1)}}
.nc-bar .vl{{font-size:.75em;min-width:3em;text-align:right;flex:none;white-space:nowrap;font-variant-numeric:tabular-nums}}
/* On a dark ground the track is invisible: an ink-on-ink 7% wash reads as nothing,
   so the bar loses the baseline it is measured against. Straight from
   components_proof.html, which had this and the generated sheet did not. */
.ground-blue .nc-bar .tk,.ground-ink .nc-bar .tk{{background:rgba(255,255,255,.14)}}
.ground-blue .nc-bar .fl,.ground-ink .nc-bar .fl{{background:var(--nc-teal)}}
.nc-hatch,.nc-bar .fl.nc-hatch{{background-image:repeating-linear-gradient(45deg,rgba(13,13,13,.30) 0 3px,transparent 3px 7px);
  background-color:var(--nc-chalk);outline:1px solid var(--nc-hair);outline-offset:-1px}}
/* Hatched = suppressed [c] or not collected n/a. NEVER a blank row, and never
   a solid bar — a gap in the data is a finding, and dropping or filling the
   row hides it. The value label always states which. */


/* --- 12 · TEXT COMPONENTS ---------------------------------------
   Lists sit between prose and table: space BETWEEN items does the work
   (ch03, 1.4-1.5). Links carry their purpose in the text alone (SC 2.4.4,
   Level A) - never "click here", never a bare URL. */
.nc-list{{margin:var(--nc-sp3) 0;padding-left:var(--nc-sp4);line-height:1.45}}
.nc-list li{{margin-bottom:var(--nc-sp2)}}
.nc-list--num{{list-style:decimal}}
.nc-link{{color:var(--nc-blue);text-decoration:underline;text-underline-offset:.15em}}
.ground-blue .nc-link,.ground-ink .nc-link{{color:var(--nc-teal)}}
.nc-caption{{font-size:.78em;line-height:1.35;color:var(--nc-charcoal);margin:var(--nc-sp2) 0 0}}
.nc-figure{{margin:var(--nc-sp5) 0}}
.nc-term{{font-weight:600;border-bottom:1px dotted var(--nc-charcoal)}}

/* --- 13 · CONTENTS — built from finding-headings, so reading only the
   contents is reading the argument (ch11). Colour-chip index. */
.nc-contents{{margin:var(--nc-sp4) 0}}
.nc-contents a{{display:flex;align-items:baseline;gap:var(--nc-sp2);padding:var(--nc-sp2) 0;
  border-bottom:1px solid rgba(13,13,13,.13);text-decoration:none;color:inherit}}
.nc-contents .n{{font-family:var(--nc-font-head);font-weight:800;font-size:.7em;
  letter-spacing:.08em;color:var(--nc-charcoal);width:2.2em;flex:none}}
.nc-contents .t{{font-family:var(--nc-font-head);font-weight:700;font-size:.95em;flex:1}}
.nc-contents .p{{font-variant-numeric:tabular-nums;font-size:.8em;color:var(--nc-charcoal)}}
.nc-contents .chip{{width:.8em;height:.8em;flex:none;background:var(--nc-acc,var(--nc-blue))}}

/* --- 14 · RUNNING FOOT — a photocopied page must know where it came
   from (ch11). Section, not just document title. */
.nc-foot{{display:flex;justify-content:space-between;align-items:baseline;gap:1em;
  border-top:1px solid var(--nc-hair);padding-top:var(--nc-sp3);margin-top:var(--nc-sp6);
  font-family:var(--nc-font-head);font-weight:600;text-transform:uppercase;
  letter-spacing:.1em;font-size:.66em;color:var(--nc-charcoal)}}

/* --- 15 · MORE CHART FORMS (charts v1.4) ------------------------
   Dot plot for places: bars imply quantity from zero, dots imply
   position on a scale. Range shown because a bare point estimate
   reads as a count. */
.nc-dot .row{{display:flex;align-items:center;gap:var(--nc-sp3);margin-bottom:var(--nc-sp3)}}
.nc-dot .lb{{font-size:.78em;width:7.5em;flex:none;font-weight:500}}
.nc-dot .tk{{flex:1;height:1.4em;position:relative;border-bottom:1px solid var(--nc-grid)}}
.nc-dot .rng{{position:absolute;top:.55em;height:.25em;background:rgba(0,0,255,.20)}}
.nc-dot .pt{{position:absolute;top:.28em;width:.85em;height:.85em;transform:translateX(-50%);
  background:var(--nc-chart-1);border:2px solid var(--nc-white)}}
.nc-dot .vl{{font-size:.75em;min-width:3.4em;text-align:right;flex:none;white-space:nowrap;font-variant-numeric:tabular-nums}}
/* Donut: four segments maximum, percentages in the key, clockwise from
   largest. The hole holds the total — usually the most useful number. */
.nc-donut{{display:flex;gap:var(--nc-sp5);align-items:center;flex-wrap:wrap}}
.nc-donut .ring{{width:9.5em;height:9.5em;border-radius:50%;flex:none;position:relative}}
.nc-donut .ring::after{{content:"";position:absolute;inset:30%;background:var(--nc-white);border-radius:50%}}
.nc-donut .tot{{position:absolute;inset:0;display:flex;flex-direction:column;
  align-items:center;justify-content:center;z-index:2}}
.nc-donut .tot .n{{font-family:var(--nc-font-display);font-size:1.1em;line-height:1}}
.nc-donut .tot .l{{font-family:var(--nc-font-head);font-weight:800;font-size:.52em;
  letter-spacing:.1em;text-transform:uppercase;margin-top:var(--nc-sp1)}}
.nc-donut .key{{flex:1;min-width:11em}}
.nc-donut .key div{{display:flex;align-items:center;gap:var(--nc-sp2);font-size:.78em;margin-bottom:var(--nc-sp2)}}
.nc-donut .key i{{width:.95em;height:.95em;flex:none;display:block;outline:1px solid var(--nc-hair)}}
.nc-donut .key b{{font-weight:400;margin-left:auto;font-variant-numeric:tabular-nums}}
/* 100% stacked — replaces most pies. Two stacked bars compare easily;
   two pies do not. Values inside the segments, key as reference. */
.nc-stack{{display:flex;height:2.7em;margin-bottom:var(--nc-sp3);outline:1px solid var(--nc-hair);outline-offset:-1px}}
.nc-stack div{{display:flex;align-items:center;justify-content:center;
  font-family:var(--nc-font-head);font-weight:800;font-size:.72em;letter-spacing:.04em}}
.nc-key{{display:flex;flex-wrap:wrap;gap:var(--nc-sp4);font-size:.75em}}
.nc-key span{{display:flex;align-items:center;gap:var(--nc-sp2)}}
.nc-key i{{width:.85em;height:.85em;display:block;outline:1px solid var(--nc-hair)}}

/* --- 11 · CASE — declared per component, never inherited ---------- */
.nc-section-head .ttl,.nc-panel .lab,.nc-band .lab,.nc-stat .lb,.nc-prov,
.nc-meter-lab,.nc-table th{{text-transform:uppercase}}
.nc-quote .q,.nc-quote .a,.nc-panel .txt,.nc-band .txt,.nc-stat .src,.nc-source,
.nc-table td,.nc-bar .lb,.nc-caption{{text-transform:none}}

/* ---- 16 · narrow widths -------------------------------------------------
   A bar earns its place by encoding length from zero. Squeeze the track to a
   stub on a phone and the encoding is gone — the chart still looks like a
   chart while no longer being readable as one, which is worse than not
   drawing it. Below 30rem the row stacks: category on its own line, then the
   full-width track with its value. Same component, same rules, same colour —
   only the arrangement changes, which is what a modifier is for. */
@media (max-width:30rem){{
  .nc-bar,.nc-dot .row{{flex-wrap:wrap}}
  .nc-bar .lb,.nc-dot .lb{{flex:1 0 100%;width:auto;margin-bottom:var(--nc-sp1)}}
  .nc-bar .tk,.nc-dot .tk{{flex:1 1 auto;min-width:0}}
}}
"""
out = ROOT/"foundations"/"nightlife-culture.css"; out.write_text(css)
allow = sorted({v.upper() for v in list(G.values())+list(A.values())+RAMP+["#FFFFFF","#000000"]})
(ROOT/"checks"/"allowed-hex.json").write_text(json.dumps({
 "source":T["meta"]["source"],"allowed":allow,"retired":C["retired"]["values"],
 "note":"Generated. Any hex outside this list is NC-COL-06, Fixed."},indent=2))
print(f"wrote {out.name}  {len(css)} bytes  sha {hashlib.sha256(css.encode()).hexdigest()[:16]}")
print(f"components: section-head · panel×6 · band · quote · stat×3 · prov · meter · source · brk×3 · table×3 · chart · bar · hatch")
