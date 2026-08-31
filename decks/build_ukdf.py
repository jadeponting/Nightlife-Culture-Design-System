#!/usr/bin/env python3
"""The UKDF fellowship pitch, rebuilt on the system.

  decks/ukdf-pitch.html    links ../foundations/*.css — always current
  dist/ukdf-pitch.html     self-contained, for reading and sending

Every slide is one of the twelve layouts, declared with data-layout so the
contract it must satisfy is named on the surface itself. Every word is
Carly's, from UKDF_Fellowship_Proposal__Artists_Make_Great_Places_V1.pptx —
trimmed only where a layout contract caps a slot, and every trim is listed in
TRIMMED at the bottom so nothing disappears silently.

    python3 decks/build_ukdf.py
"""
import base64, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
F = ROOT / "foundations"
T = json.loads((F / "tokens.json").read_text())
sys.path.insert(0, str(ROOT / "docs"))
from sheet import _stamp

LOGO  = '<img class="nc-slogo" src="../assets/logo/nightlife-culture-wordmark-white.svg" alt="Nightlife Culture">'
LOGOB = '<img class="nc-slogo nc-slogo--lockup" src="../assets/logo/nightlife-culture-wordmark-white.svg" alt="Nightlife Culture">'
LOGOI = '<img class="nc-slogo" src="../assets/logo/nightlife-culture-wordmark-blue.svg" alt="Nightlife Culture">'

def foot(num=None, left="", ground="light"):
    l = left if left else (LOGO if ground == "dark" else LOGOI)
    r = f'<span class="nc-snum">{num}</span>' if num else "<span></span>"
    return f'<div class="nc-sfoot">{l}{r}</div>'

def slide(layout, ground, inner):
    return (f'<div class="nc-slide" data-layout="{layout}">'
            f'<div class="cv {ground}">{inner}</div></div>')

SLIDES = []

# 01 · L1 cover ---------------------------------------------------------------
SLIDES.append(slide("L01", "ground-blue", f'''<div class="nc-pad nc-pad--bleed" data-anchor="bottom">
    {LOGOB}
    <div><h1 class="nc-t nc-t--xl">Artists make<br>great places</h1>
      <hr class="nc-brk acc-teal">
      <p class="nc-sub">Nightlife as place-based infrastructure for a dynamic UK.</p></div>
  </div>
  {foot(None, '<span class="nc-k" style="color:var(--nc-teal)">UK Dynamism Fund fellowship proposal · Carly Heath · August 2026</span>', "dark")}'''))

# 02 · L3 the conviction ------------------------------------------------------
SLIDES.append(slide("L03", "ground-blue", f'''<div class="nc-pad nc-pad--kicker">
    <p class="nc-k" style="color:var(--nc-teal)">01 · The conviction</p>
    <h2 class="nc-t">Places don&rsquo;t make<br>great artists</h2>
    <hr class="nc-brk acc-teal">
    <p class="nc-sub nc-sub--wide">Artists make great places. Nightlife is cultural, social and
      economic infrastructure: where people find one another, test ideas, build scenes,
      start enterprises and create belonging.</p>
    <div class="nc-cols">
      <div class="col acc-teal"><p class="l">Learn agency</p></div>
      <div class="col acc-pink"><p class="l">Find collaborators</p></div>
      <div class="col acc-butter"><p class="l">Make places distinctive</p></div>
    </div>
  </div>
  {foot("02", "", "dark")}'''))

# 03 · L4 the gap -------------------------------------------------------------
SLIDES.append(slide("L04", "ground-blue", f'''<div class="nc-pad nc-pad--kicker">
    <p class="nc-k" style="color:var(--nc-teal)">02 · The system sees nightlife too late</p>
    <div class="nc-cols nc-cols--2">
      <div class="col col--plain">
        <h2 class="nc-t nc-t--sm" style="color:var(--nc-teal)">What the night<br>creates</h2>
        <hr class="nc-brk acc-teal" style="width:34%">
        <p class="nc-sbody">agency &middot; ambition &middot; talent &middot; trust &middot;
          creative risk &middot; belonging &middot; new enterprises</p>
      </div>
      <div class="col col--plain">
        <p class="nc-t nc-t--sm">What systems<br>see</p>
        <hr class="nc-brk" style="background:#fff;width:34%">
        <p class="nc-sbody">registered firms &middot; jobs &middot; spend &middot; footfall &middot;
          incidents &middot; licensing &middot; established venues</p>
      </div>
    </div>
  </div>
  {foot("03", "", "dark")}'''))

# 04 · L9 the mechanism -------------------------------------------------------
SLIDES.append(slide("L09", "ground-chalk", f'''<div class="nc-strip">
    <div class="top">
      <p class="nc-k" style="color:var(--nc-blue)">03 · The mechanism</p>
      <h2 class="nc-t nc-t--sm" style="color:var(--nc-charcoal)">Nightlife is a<br>talent programme</h2>
      <hr class="nc-brk acc-blue">
      <p class="nc-sub" style="color:var(--nc-blue)">It produces agency and ambition before formal
        institutions can see them.</p>
    </div>
    <div class="band">
      <div><p class="l">People</p><p class="d">gain agency</p></div>
      <div><p class="l">Scenes + spaces</p><p class="d">generate new forms</p></div>
      <div><p class="l">Dynamic places</p><p class="d">acquire identity, enterprise and magnetism</p></div>
    </div>
  </div>'''))

# 05 · L6 why Carly -----------------------------------------------------------
SLIDES.append(slide("L06", "ground-chalk", f'''<div class="nc-pad nc-pad--kicker">
    <p class="nc-k" style="color:var(--nc-blue)">04 · Why Carly</p>
    <h2 class="nc-t" style="color:var(--nc-charcoal)">Built from<br>the ground up</h2>
    <hr class="nc-brk acc-blue">
    <p class="nc-sub" style="color:var(--nc-blue)">She is evidence of the mechanism: nightlife
      taught her to act before permission arrived.</p>
    <div class="nc-cells nc-cells--4">
      <div class="cell acc-teal"><p class="l">Promoter and founder</p>
        <p class="d">Label co-founder, 1,000+ events, a festival grown into a charity.</p></div>
      <div class="cell acc-butter"><p class="l">Institutional translator</p>
        <p class="d">Five years leading Bristol Nights across policy, health, safety, planning and culture.</p></div>
      <div class="cell acc-pink"><p class="l">Creates new mechanisms</p>
        <p class="d">Designed A Ticket to the Future and the Bristol Music Fund model.</p></div>
      <div class="cell acc-violet"><p class="l">A doer, not an observer</p>
        <p class="d">Connects scenes, government, funders and sector bodies &mdash; and carries ideas into delivery.</p></div>
    </div>
  </div>
  {foot("04", "", "light")}'''))

# 06 · L7 the inquiry ---------------------------------------------------------
SLIDES.append(slide("L07", "ground-ink", f'''<div class="nc-pad nc-pad--kicker">
    <p class="nc-k" style="color:var(--nc-teal)">05 · The inquiry &middot; conviction fixed, form open</p>
    <h2 class="nc-t" style="color:var(--nc-teal)">What would it take?</h2>
    <hr class="nc-brk acc-teal">
    <p class="nc-sub nc-sub--wide">For the UK to sustain nightlife as infrastructure for agency,
      talent and place &mdash; an 8&ndash;12 month research-and-build fellowship.</p>
    <div class="nc-cells nc-cells--5">
      <div class="cell acc-teal"><p class="l">How night makes people</p><p class="d">how scenes and peers develop agency, ambition and skill</p></div>
      <div class="cell acc-butter"><p class="l">How people make places</p><p class="d">how artists and gatherings create identity and distinctiveness</p></div>
      <div class="cell acc-pink"><p class="l">Follow the value</p><p class="d">who creates, captures and reinvests cultural and economic value</p></div>
      <div class="cell acc-violet"><p class="l">Test what helps</p><p class="d">definitions, evidence methods and one practical prototype</p></div>
      <div class="cell acc-coral"><p class="l">Build the institution</p><p class="d">what Nightlife Culture should become &mdash; and fund next</p></div>
    </div>
  </div>
  {foot("05", "", "dark")}'''))

# 07 · L6 the fellowship ------------------------------------------------------
SLIDES.append(slide("L06", "ground-chalk", f'''<div class="nc-pad nc-pad--kicker">
    <p class="nc-k" style="color:var(--nc-blue)">06 · The fellowship</p>
    <h2 class="nc-t nc-t--sm" style="color:var(--nc-charcoal)">The 8&ndash;12 month<br>fellowship</h2>
    <hr class="nc-brk acc-blue">
    <p class="nc-sub nc-sub--wide" style="color:var(--nc-blue)">An eight-month core, with up to four
      months for partner-timed testing, synthesis and publication.</p>
    <div class="nc-cells">
      <div class="cell acc-teal"><p class="n">M1&ndash;3</p><p class="l">Frame + listen</p>
        <p class="d">define the inquiry and advisory circle</p></div>
      <div class="cell acc-butter"><p class="n">M3&ndash;8</p><p class="l">Test + make</p>
        <p class="d">fieldwork in 2&ndash;3 places &middot; test one practical method</p></div>
      <div class="cell acc-pink"><p class="n">M7&ndash;12</p><p class="l">Synthesise + build</p>
        <p class="d">publish the argument &middot; secure the next funded phase</p></div>
    </div>
  </div>
  {foot("06", "", "light")}'''))

# 08 · L3 what UKDF changes ---------------------------------------------------
SLIDES.append(slide("L03", "ground-blue", f'''<div class="nc-pad nc-pad--kicker">
    <p class="nc-k" style="color:var(--nc-teal)">07 · What UKDF support would change</p>
    <h2 class="nc-t nc-t--sm">A clear<br>step change</h2>
    <hr class="nc-brk acc-teal">
    <p class="nc-sub nc-sub--wide">Without protected time, commissions shape the work reactively.
      UKDF lets the public-interest foundation be designed first.</p>
    <div class="nc-cols">
      <div class="col acc-teal"><p class="l">A field-backed argument</p>
        <p class="d">A published thesis, 2&ndash;3 place cases, and evidence of how nightlife produces agency and place value.</p></div>
      <div class="col acc-butter"><p class="l">A tested first method</p>
        <p class="d">One practical prototype &mdash; a value ledger or shared evidence method &mdash; and clear learning about what travels.</p></div>
      <div class="col acc-pink"><p class="l">An investable institution</p>
        <p class="d">Operating model, governance, partner commitments and a costed next phase.</p></div>
    </div>
  </div>
  {foot("07", "", "dark")}'''))

# 09 · L10 the ask ------------------------------------------------------------
SLIDES.append(slide("L10", "ground-white", f'''<div class="nc-third">
    <div class="main">
      <p class="nc-k" style="color:var(--nc-blue)">08 · The ask</p>
      <h2 class="nc-t nc-t--sm" style="color:var(--nc-charcoal)">Twenty years,<br>one new institution</h2>
      <hr class="nc-brk nc-brk--hair">
      <p class="nc-sub" style="color:var(--nc-blue)">An eight-month core plus follow-through.
        UKDF brings runway, challenge, credibility and connections; Carly brings a live
        cultural field.</p>
      <p class="nc-srcline">&pound;36,000 founder capacity &middot; &pound;9,600 specialist input
        + prototype &middot; &pound;4,200 fieldwork, access + contingency</p>
    </div>
    <div class="side side--wide acc-butter">
      <div><p class="bignum">&pound;49,800</p><p class="biglab">Total ask &middot; 8&ndash;12 months</p></div>
    </div>
  </div>
  {foot("08", "", "light")}'''))

# 10 · L12 closing ------------------------------------------------------------
SLIDES.append(slide("L12", "ground-blue", f'''<div class="nc-pad" data-anchor="centre">
    <hr class="nc-brk nc-brk--bar acc-pink">
    <h2 class="nc-t">Artists make<br>great places</h2>
    <p class="nc-sub" style="margin-top:2cqw">Carly Heath &middot; Nightlife Culture &middot;
      studio@nightlifeculture.co.uk</p>
  </div>
  {foot(None, LOGO, "dark")}'''))

TRIMMED = [
 ("Slide 2 original", "&ldquo;I am seeking a fellowship to establish Nightlife Culture and turn this "
  "conviction into a tested institution, a practical first method and a fundable next phase.&rdquo; "
  "&mdash; the three outcomes now carry this on slide 08, and the ask on 09."),
 ("Slides 4/5 original", "&ldquo;When value is extracted without reinvestment, the conditions that "
  "create the next artist, organiser or enterprise are weakened.&rdquo; &mdash; not placed. "
  "It is the strongest warning in the deck; say where it goes and it goes there."),
 ("Slide 3 original", "&ldquo;Better language, evidence and reinvestment can change what places "
  "recognise and back.&rdquo; &mdash; not placed; say where and it goes there."),
 ("Slide 4 original", "&ldquo;Artists and organisers create the encounters through which people "
  "learn to act &mdash; and places become distinctive. Dynamism starts earlier: in informal "
  "relationships, experiments and gathering places.&rdquo; &mdash; would not fit the ink-strip "
  "layout with the band. Candidates: the operating plan, or a second mechanism slide."),
 ("Slide 6 original", "&ldquo;Trusted across worlds&rdquo; merged into &ldquo;A doer, not an "
  "observer&rdquo; &mdash; five cards became four so none needs a caption under 16pt."),
 ("Slide 4/5 duplicate", "The original deck contained the talent-programme slide twice. Once here."),
]

trims = "".join(f'<div class="nc-flag nc-flag--amber" style="display:block"><span class="tag">Trimmed</span> '
                f'<b>{a}.</b> {b}</div>' for a, b in TRIMMED)

slides_html = "\n".join(f'<section style="margin:0 0 var(--nc-sp6)">{s}</section>' for s in SLIDES)

HEAD = """<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>UKDF fellowship pitch — Nightlife Culture</title>
<meta name="nc-source" content="Nightlife Culture Style Guide v1.4">
<meta name="nc-build-stamp" content="{stamp}">
{styles}
</head><body class="nc-doc">
<header class="nc-mast"><div class="nc-wrap">
  <p class="nc-kick">Nightlife Culture · UKDF fellowship</p>
  <h1>Artists make great places — the pitch, on the system</h1>
  <p class="stand">Ten slides. Every one is one of the twelve layouts, every colour and size is a
    token, and every word is yours — from the V1 proposal deck. What was trimmed to fit a layout
    contract is listed at the end, so nothing has quietly disappeared.</p>
</div></header>
<div class="nc-wrap">
{body}
<section>
  <h2 class="nc-section-head"><span class="ttl">What was trimmed, and one new thing</span></h2>
  <p>A layout contract caps the words a slot can carry. These lines did not fit, and are parked
     here for your call, not deleted:</p>
  {trims}
  <div class="nc-panel nc-panel--left acc-coral" style="margin-top:var(--nc-sp5)">
    <p class="lab">One new style, awaiting your sign-off</p>
    <p class="txt">The catalogue&rsquo;s cells and columns carried a numeral and a label only. A
      real pitch needs one sentence under the label &mdash; the Why-Carly cards, the three
      outcomes. So there is now a detail line: Inter regular, sized between the label and slide
      body, sentence case. It is the only thing on these slides that did not exist yesterday.
      If it reads wrong, it is one line to change.</p>
  </div>
</section>
</div>
</body></html>
"""

styles_linked = ('<link rel="stylesheet" href="../foundations/fonts.css">\n'
                 '<link rel="stylesheet" href="../foundations/nightlife-culture.css">\n'
                 '<link rel="stylesheet" href="../foundations/nightlife-slides.css">')
inline = "\n".join((F / f).read_text() for f in
                   ("fonts.css", "nightlife-culture.css", "nightlife-slides.css"))

out = ROOT / "decks" / "ukdf-pitch.html"
out.write_text(HEAD.format(stamp=_stamp(), styles=styles_linked, body=slides_html, trims=trims))

dist_body = slides_html
for f in ROOT.glob("assets/logo/nightlife-culture-wordmark-*.svg"):
    b = base64.b64encode(f.read_bytes()).decode()
    dist_body = dist_body.replace(f"../assets/logo/{f.name}", f"data:image/svg+xml;base64,{b}")
(ROOT / "dist" / "ukdf-pitch.html").write_text(
    HEAD.format(stamp=_stamp(), styles=f"<style>\n{inline}\n</style>", body=dist_body, trims=trims))
print(f"wrote decks/ukdf-pitch.html   {len(SLIDES)} slides, linked")
print(f"wrote dist/ukdf-pitch.html    self-contained")
