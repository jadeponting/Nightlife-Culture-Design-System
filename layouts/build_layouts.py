#!/usr/bin/env python3
"""Generate the twelve slide layouts, and the sheet that shows them.

  layouts/index.html          LINKS ../foundations/*.css — always current
  dist/slide-layouts.html     self-contained, for sending

Each layout is a named arrangement of components that already exist. Nothing
here defines a component; if a layout needed a new one, that would be a signal
the component layer is missing something, not that the layout is special.

Content lives in LAYOUTS below — swap the words, keep the arrangement.

    python3 layouts/build_layouts.py

NC-SYS-06 — render the decision rather than describing it. This page is
generated from the system it describes, so it cannot claim behaviour the
system does not have.
"""
import hashlib, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
F = ROOT / "foundations"
T = json.loads((F / "tokens.json").read_text())
S = T["space"]["slide"]
def dig(p): return hashlib.sha256(p.read_bytes()).hexdigest()[:16]

# Slide titles here are <p class="nc-t">, not headings. On this page the twelve
# slides are SPECIMENS inside one document, so giving each a real h1 would build
# a nonsense outline — twelve top-level headings inside a catalogue. In a live
# deck each slide is its own surface and the title is marked up as a heading
# there (NC-PRS-02). The class carries the appearance either way, which is the
# whole point of separating the two.
LOGO = '<img class="nc-slogo" src="../assets/logo/nightlife-culture-wordmark-white.svg" alt="Nightlife Culture">'
LOGOB = '<img class="nc-slogo nc-slogo--lockup" src="../assets/logo/nightlife-culture-wordmark-white.svg" alt="Nightlife Culture">'
LOGOI = '<img class="nc-slogo" src="../assets/logo/nightlife-culture-wordmark-blue.svg" alt="Nightlife Culture">'

def foot(num=None, left="", ground="light"):
    lg = LOGO if ground == "dark" else LOGOI
    l = left if left else lg
    r = f'<span class="nc-snum">{num}</span>' if num else "<span></span>"
    return f'<div class="nc-sfoot">{l}{r}</div>'

LAYOUTS = [
 ("L1", "Cover", "bleed", "ground-blue", "dark",
  "Blue ground. The lockup leads, so the top margin is the largest step and the "
  "statement anchors to the foot of the content area. No slide number on a cover — "
  "but the footer band is still reserved, because the reason for it is sightlines, "
  "not numbering.",
  f'''<div class="nc-pad nc-pad--bleed" data-anchor="bottom">
    {LOGOB}
    <div><p class="nc-t nc-t--xl">Artists make<br>great places</p>
      <hr class="nc-brk acc-teal"></div>
  </div>
  {foot(None, '<span class="nc-k" style="color:var(--nc-teal)">UK Dynamism Fund · Aug 2026</span>', "dark")}'''),

 ("L2", "Section divider", "title", "ground-blue", "dark",
  "A kicker, a large title, and the stop. Nothing after the rule — that is what "
  "makes it a stop rather than a separator (NC-PSE-05).",
  f'''<div class="nc-pad" data-anchor="centre">
    <p class="nc-k" style="color:var(--nc-teal)">Section 04</p>
    <p class="nc-t nc-t--xl">Follow<br>the value</p>
    <hr class="nc-brk acc-teal">
  </div>
  {foot("08", LOGO, "dark")}'''),

 ("L3", "Three points", "kicker", "ground-blue", "dark",
  "The workhorse. A kicker leads, so the top margin is the smallest step. Three "
  "top-rule columns — nothing boxed, because the rule codes the column without "
  "flooding it.",
  f'''<div class="nc-pad nc-pad--kicker">
    <p class="nc-k" style="color:var(--nc-teal)">03 · The opportunity</p>
    <p class="nc-t">A shared<br>evidence layer</p>
    <hr class="nc-brk acc-teal">
    <p class="nc-sub">Imagine several cities asking better questions about the night.</p>
    <div class="nc-cols">
      <div class="col acc-teal"><p class="n">01</p><p class="l">Local truth</p></div>
      <div class="col acc-pink"><p class="n">02</p><p class="l">Shared method</p></div>
      <div class="col acc-butter"><p class="n">03</p><p class="l">National learning</p></div>
    </div>
  </div>
  {foot("07", "", "dark")}'''),

 ("L4", "Two-column contrast", "kicker", "ground-blue", "dark",
  "The Nightlife Culture argument shape: two things in tension. Teal marks the side "
  "you want heard. Both columns stop well above the footer band.",
  f'''<div class="nc-pad nc-pad--kicker">
    <p class="nc-k" style="color:var(--nc-teal)">03 · The bridge we build</p>
    <div class="nc-cols nc-cols--2">
      <div class="col col--plain">
        <p class="nc-t nc-t--sm">What systems<br>often count</p>
        <hr class="nc-brk" style="background:#fff;width:34%">
        <p class="nc-sbody">risk · incidents · licensing · nuisance · footfall · spend</p>
      </div>
      <div class="col col--plain">
        <p class="nc-t nc-t--sm" style="color:var(--nc-teal)">What culture<br>also holds</p>
        <hr class="nc-brk acc-teal" style="width:34%">
        <p class="nc-sbody">belonging · trust · scene-building · creative risk · care · collective joy</p>
      </div>
    </div>
  </div>
  {foot("09", "", "dark")}'''),

 ("L5", "Quote", "title", "ground-blue", "dark",
  "The accent bar sits above the quote and nowhere else — the only decorative use "
  "of a breaker (NC-PSE-03). The quote is the same component a report uses, one "
  "size up.",
  f'''<div class="nc-pad" data-anchor="centre">
    <hr class="nc-brk nc-brk--bar acc-pink">
    <blockquote class="nc-quote" style="border:0;padding:0">
      <p class="q">Nightlife taught her to act before permission arrived.</p>
    </blockquote>
    <p class="nc-k" style="color:var(--nc-teal);margin-top:2cqw">UKDF fellowship proposal · 2026</p>
  </div>
  {foot("11", LOGO, "dark")}'''),

 ("L6", "Report register", "kicker", "ground-chalk", "light",
  "Charcoal title, blue sub — not the other way round. Filled cells, ink text, no "
  "outlines. Chalk in decks, white in reports.",
  f'''<div class="nc-pad nc-pad--kicker">
    <p class="nc-k" style="color:var(--nc-blue)">04 · Principles for partnership</p>
    <h2 class="nc-t" style="color:var(--nc-charcoal)">How shared evidence<br>should be built</p>
    <hr class="nc-brk acc-blue">
    <p class="nc-sub" style="color:var(--nc-blue)">Knowledge in the commons. Data as an asset.</p>
    <div class="nc-cells">
      <div class="cell acc-teal"><p class="n">01</p><p class="l">Open standards</p></div>
      <div class="cell acc-butter"><p class="n">02</p><p class="l">Platform neutral</p></div>
      <div class="cell acc-violet"><p class="n">03</p><p class="l">Local ownership</p></div>
    </div>
  </div>
  {foot("12", "", "light")}'''),

 ("L7", "Night register", "kicker", "ground-ink", "dark",
  "Used sparingly, and never without a light-ground variant: ambient light lifts a "
  "projector's blacks, so an ink deck greys out in a lit room at 11am. Teal is the "
  "section-header colour on every dark ground — butter on ink reads as a warning label.",
  f'''<div class="nc-pad nc-pad--kicker">
    <p class="nc-k" style="color:var(--nc-teal)">05 · What the night creates</p>
    <h2 class="nc-t" style="color:var(--nc-teal)">Nightlife is a<br>talent programme</p>
    <hr class="nc-brk acc-teal">
    <p class="nc-sub nc-sub--wide">It produces agency and ambition before formal institutions can see them.</p>
    <div class="nc-cells">
      <div class="cell acc-teal"><p class="n">01</p><p class="l">People</p></div>
      <div class="cell acc-butter"><p class="n">02</p><p class="l">Scenes and spaces</p></div>
      <div class="cell acc-pink"><p class="n">03</p><p class="l">Practice</p></div>
    </div>
  </div>
  {foot("06", "", "dark")}'''),

 ("L8", "Vertical third", "kicker", "ground-chalk", "light",
  "An accent block for the last third, never an accent room. The hairline breaker "
  "sits under the title — the report register of the pause.",
  f'''<div class="nc-third">
    <div class="main">
      <p class="nc-k" style="color:var(--nc-blue)">06 · The opportunity</p>
      <p class="nc-t nc-t--sm" style="color:var(--nc-charcoal)">A shared<br>evidence layer</p>
      <hr class="nc-brk nc-brk--hair">
      <p class="nc-sub" style="color:var(--nc-blue)">Imagine several cities asking better questions about the night.</p>
    </div>
    <div class="side acc-teal">
      <p class="biglab">Local truth</p><p class="bignum">01</p>
    </div>
  </div>
  {foot("14", "", "light")}'''),

 ("L9", "Ink strip", "kicker", "ground-chalk", "light",
  "A full-bleed ink band across the foot replaces three boxes. Teal numerals. The "
  "band is the change of ground, so nothing else on the slide needs containing.",
  f'''<div class="nc-strip">
    <div class="top">
      <p class="nc-k" style="color:var(--nc-blue)">07 · From first conversation to delivery</p>
      <p class="nc-t nc-t--sm" style="color:var(--nc-charcoal)">Our creative<br>policy method</p>
      <hr class="nc-brk acc-blue">
      <p class="nc-sub" style="color:var(--nc-blue)">Modular tools that adapt to place while keeping faith with local culture.</p>
    </div>
    <div class="band">
      <div><p class="n">01</p><p class="l">Frame and listen</p></div>
      <div><p class="n">02</p><p class="l">Test and make</p></div>
      <div><p class="n">03</p><p class="l">Synthesise and build</p></div>
    </div>
  </div>'''),

 ("L10", "Vertical third stat", "kicker", "ground-white", "light",
  "One number that has to land. The accent block carries the number; the light side "
  "carries the argument and the source line. The stat keeps its source line even "
  "here — a statistic without one is a claim (NC-EVI-07).",
  f'''<div class="nc-third">
    <div class="main">
      <p class="nc-k" style="color:var(--nc-blue)">08 · Follow the value</p>
      <p class="nc-t nc-t--sm" style="color:var(--nc-charcoal)">Who creates it,<br>who captures it</p>
      <hr class="nc-brk nc-brk--hair">
      <p class="nc-sub" style="color:var(--nc-blue)">And who reinvests it back into the conditions that made it.</p>
      <p class="nc-srcline"><span class="nc-illus">Illustrative</span> ADM-OPEN · 2025 · LA boundary 2023</p>
    </div>
    <div class="side side--wide acc-pink">
      <p class="biglab">A definition</p>
      <div><p class="bignum">£41m</p><p class="biglab">Night-time spend, 2025</p></div>
    </div>
  </div>
  {foot("15", "", "light")}'''),

 ("L11", "Chart slide", "kicker", "ground-white", "light",
  "The chart occupies the middle band and the source line sits at the foot of the "
  "content area, above the footer band. Single series, single colour, labelled at "
  "the mark — the same rules the document charts obey.",
  f'''<div class="nc-pad nc-pad--kicker">
    <p class="nc-k" style="color:var(--nc-blue)">09 · Where value is held</p>
    <p class="nc-t nc-t--sm" style="color:var(--nc-charcoal)">Manchester holds twice<br>the night-time payroll</p>
    <hr class="nc-brk acc-blue">
    <div style="margin-top:2cqw">
      <div class="nc-sbar"><span class="lb">Manchester</span><span class="tk"><span class="fl" style="width:100%"></span></span><span class="vl">41,200</span></div>
      <div class="nc-sbar"><span class="lb">Leeds</span><span class="tk"><span class="fl" style="width:82%"></span></span><span class="vl">33,900</span></div>
      <div class="nc-sbar"><span class="lb">Bristol</span><span class="tk"><span class="fl" style="width:45%"></span></span><span class="vl">18,450</span></div>
      <div class="nc-sbar"><span class="lb">Brighton</span><span class="tk"><span class="fl" style="width:31%"></span></span><span class="vl">12,800</span></div>
    </div>
    <p class="nc-srcline"><span class="nc-illus">Illustrative</span> Single series, single colour ·
      ADM-OPEN · 2024 boundaries</p>
  </div>
  {foot("16", "", "light")}'''),

 ("L12", "Closing", "title", "ground-blue", "dark",
  "The lockup, the ask, the contact. Pink accent bar. No slide number — and the "
  "footer band still reserved, for the same reason it is on the cover.",
  f'''<div class="nc-pad" data-anchor="centre">
    <hr class="nc-brk nc-brk--bar acc-pink">
    <p class="nc-t nc-t--sm">This is an invitation<br>to build better<br>evidence together</p>
    <p class="nc-sub" style="margin-top:2cqw">For the people who make the night happen, hold
      knowledge about it, govern it, fund it or care about its future.</p>
  </div>
  {foot(None, LOGO, "dark")}'''),
]

CHOOSE = [
 ("Opening an argument", "L2 · section divider"),
 ("Three related points", "L3 on blue, or L6 / L7 if you want them filled"),
 ("Two things in tension", "L4 — this is the Nightlife Culture argument shape"),
 ("One line that has to land", "L5 · quote"),
 ("One number that has to land", "L10 · vertical third stat"),
 ("A process or sequence", "L9 · ink strip"),
 ("Data", "L11 — chart ramp only, never the brand accents"),
 ("Detail-heavy content", "L8 · vertical third, which keeps the argument on the left"),
]

cards = []
for code, name, lead, ground, reg, why, markup in LAYOUTS:
    step = {"kicker": S["topMargin"]["kickerLeads"], "title": S["topMargin"]["titleLeads"],
            "bleed": S["topMargin"]["fullBleedLeads"]}[lead]
    cards.append(f'''<section class="lay">
  <h3 class="layh"><span class="code">{code}</span> {name}
    <span class="meta">{lead} leads · top margin {step}</span></h3>
  <p class="why">{why}</p>
  <div class="nc-slide"><div class="cv {ground}">{markup}</div></div>
</section>''')

rows = "".join(f'<tr><td class="nm">{job}</td><td>{pick}</td></tr>' for job, pick in CHOOSE)
GRID = f'''<div class="nc-table-wrap"><table class="nc-table"><thead><tr>
<th>Zone</th><th class="num">Measure</th><th>Rule</th></tr></thead><tbody>
<tr><td>Side margins</td><td class="num">{S["sideMargin"]}</td><td>Nothing crosses them.</td></tr>
<tr><td>Top margin · a kicker leads</td><td class="num">{S["topMargin"]["kickerLeads"]}</td>
  <td>Small and quiet, so it can sit high. It is not the message.</td></tr>
<tr><td>Top margin · a title leads</td><td class="num">{S["topMargin"]["titleLeads"]}</td>
  <td>The statement needs air above it to land.</td></tr>
<tr><td>Top margin · a full bleed leads</td><td class="num">{S["topMargin"]["fullBleedLeads"]}</td>
  <td>The element is the composition.</td></tr>
<tr><td>Footer band</td><td class="num">{S["footerBand"]}</td>
  <td>Reserved on every slide, covers and closers included. Content never enters it.</td></tr>
<tr><td>Body measure</td><td class="num">{S["bodyMeasure"]}</td>
  <td>The ragged right edge is part of the composition.</td></tr>
<tr><td>Title zone</td><td class="num">{S["titleZoneMaxLines"]} lines</td>
  <td>Four lines means the statement is a paragraph.</td></tr>
<tr><td>Coverage</td><td class="num">{S["coverageCeiling"]}</td>
  <td>More than about half covered means it is two slides.</td></tr>
</tbody></table></div>'''

BODY = f'''<header class="mast">
  <div class="wrap">
    <p class="kick">Nightlife Culture · design system</p>
    <h1>Twelve layouts</h1>
    <p>Generated from the tokens, so every margin on this page is the same value the
       rule set holds. Change the grid once and all twelve move together.</p>
  </div>
</header>
<div class="wrap">
<section>
  <h2 class="nc-section-head"><span class="num">01</span><span class="ttl">The grid</span></p>
  <p class="lede">The top margin is not one number, and that is the point.</p>
  <p>{S["why"]}</p>
  <p>Every value is a multiple of one unit — {S["unit"]["vertical"]} of slide height — so the
     slide grid obeys the same one-base-unit rule as the spacing scale. {S["symmetry"]}</p>
  {GRID}
  <div class="nc-panel nc-panel--left acc-teal">
    <p class="lab">Why the footer band is on every slide</p>
    <p class="txt">{S["footerNote"]}</p>
  </div>
</section>
<hr class="nc-brk acc-teal">
<section>
  <h2 class="nc-section-head"><span class="num">02</span><span class="ttl">The twelve</span></p>
  <p>Each one is an arrangement of components that already exist. None of them defines a
     component of its own — if a layout needed one, that would mean the component layer was
     missing something, not that the layout was special.</p>
  {"".join(cards)}
</section>
<hr class="nc-brk acc-pink">
<section>
  <h2 class="nc-section-head"><span class="num">03</span><span class="ttl">Choosing one</span></p>
  <p>Start from the job, not the picture.</p>
  <div class="nc-table-wrap"><table class="nc-table"><thead><tr>
    <th>What you are doing</th><th>Layout</th></tr></thead><tbody>{rows}</tbody></table></div>
</section>
</div>'''

SCAFFOLD = """*{box-sizing:border-box}
body{margin:0;background:var(--nc-chalk)}
.wrap{max-width:72rem;margin:0 auto;padding:0 var(--nc-sp5) var(--nc-sp9)}
.mast{background:var(--nc-ink);color:var(--nc-white);padding:var(--nc-sp7) 0 var(--nc-sp6);margin-bottom:var(--nc-sp7)}
.mast .wrap{padding-bottom:0}
.mast h1{font-family:var(--nc-font-display);text-transform:uppercase;letter-spacing:-.012em;
 line-height:.94;font-size:clamp(34px,6.4vw,68px);margin:0}
.mast p{font-size:1.06em;max-width:58ch;margin:var(--nc-sp5) 0 0;line-height:1.5}
.kick{font-family:var(--nc-font-head);font-weight:600;text-transform:uppercase;letter-spacing:.16em;
 font-size:max(.75em,12px);margin:0 0 var(--nc-sp4);color:var(--nc-teal)}
section{margin:0 0 var(--nc-sp8)}
p{margin:0 0 var(--nc-sp4);max-width:70ch;overflow-wrap:break-word;hyphens:none;line-height:1.55}
.lede{font-size:1.12em;max-width:60ch}
.nc-table-wrap{overflow-x:auto;margin:var(--nc-sp5) 0}
.lay{margin:0 0 var(--nc-sp7)}
.layh{font-family:var(--nc-font-head);font-weight:800;font-size:1.06em;margin:0 0 var(--nc-sp2);
 display:flex;align-items:baseline;gap:var(--nc-sp3);flex-wrap:wrap;text-transform:none}
.layh .code{background:var(--nc-ink);color:var(--nc-chalk);padding:var(--nc-sp1) var(--nc-sp2);
 font-size:.8em;letter-spacing:.06em}
.layh .meta{font-weight:600;font-size:max(.72em,12px);letter-spacing:.06em;text-transform:uppercase;
 color:var(--nc-charcoal)}
.why{font-size:max(.9em,13px);color:var(--nc-charcoal);max-width:74ch;margin-bottom:var(--nc-sp4)}
.nc-slide{outline:1px solid var(--nc-hair);outline-offset:-1px}
"""

stamp = ";".join(f"{k}:{dig(p)}" for k, p in
                 [("tokens", F/"tokens.json"), ("rules", F/"rules.json"),
                  ("css", F/"nightlife-culture.css"), ("fonts", F/"fonts.css"),
                  ("slides", F/"nightlife-slides.css")] if p.exists())
HEAD = """<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Nightlife Culture — twelve slide layouts</title>
<meta name="nc-source" content="Nightlife Culture Style Guide v1.4">
<meta name="nc-build-stamp" content="{stamp}">
{styles}
</head><body class="nc-doc">
{body}
</body></html>
"""
(ROOT/"layouts"/"index.html").write_text(HEAD.format(stamp=stamp, body=BODY,
  styles='<link rel="stylesheet" href="../foundations/fonts.css">\n'
         '<link rel="stylesheet" href="../foundations/nightlife-culture.css">\n'
         '<link rel="stylesheet" href="../foundations/nightlife-slides.css">\n'
         '<link rel="stylesheet" href="layouts.scaffold.css">'))
(ROOT/"layouts"/"layouts.scaffold.css").write_text(SCAFFOLD)
(ROOT/"dist").mkdir(exist_ok=True)
logo_inline = BODY
for f in ROOT.glob("assets/logo/nightlife-culture-wordmark-*.svg"):
    import base64
    b = base64.b64encode(f.read_bytes()).decode()
    logo_inline = logo_inline.replace(f"../assets/logo/{f.name}", f"data:image/svg+xml;base64,{b}")
(ROOT/"dist"/"slide-layouts.html").write_text(HEAD.format(stamp=stamp, body=logo_inline,
  styles=f"<style>\n{(F/'fonts.css').read_text()}\n{(F/'nightlife-culture.css').read_text()}\n"
         f"{(F/'nightlife-slides.css').read_text()}\n{SCAFFOLD}\n</style>"))
print(f"wrote layouts/index.html         {len(LAYOUTS)} layouts, linked")
print(f"wrote dist/slide-layouts.html    self-contained")
