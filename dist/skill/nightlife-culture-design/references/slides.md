# Slides — generated from foundations/patterns.json. Do not edit by hand.

Slides are built from **blocks** arranged into **patterns**. Every pattern comes from a real
Nightlife Culture deck, and its reference slide is in `assets/reference/`. **Look at the
reference image before you build a slide in that pattern, and match it.**

Build slides in HTML with `assets/fonts.css` + `assets/slides.css`. Every size is in `cqw`,
so the slide scales. Never set a colour or a size on a slide yourself: the ground class sets
the text, title and highlight colours, and the block classes set the sizes.

## Sizes (points on a 13.33in slide)

Title 43.3 (long titles 36) · statement 60 · cover 70.7 · lead 19.5 · heading 20.9 · **body 18** · label 18 caps · table 12. Line height 1.22.

Side margins 5.25%. Title sits 6.667% from the top. Content stops 8% above the foot, or above a closing band (17.333% tall).

## Two registers

- **Statement slides** (cover, statement): one idea, most of the canvas empty.
- **Working slides** (every other pattern): a title, a lead and up to eight short text blocks.
  If it does not fit at the sizes above, it is two slides. Remove copy before reducing type.

## Grounds

- **Blue or ink**: white titles and text, teal headings. **Chalk or white**: blue titles and headings, ink text.
- Accents (pink, teal, violet, butter, coral) are rules, fills and side blocks — always with ink text,
  never a whole slide.

## Blocks

| Block | Markup |
|---|---|
| Title | `<h2 class="nc-st">` · `--fit` long · `--xl` statement · `--cover` |
| Lead | `<p class="nc-sl">` · `--lg` `--xl` `--2xl` bigger · `--hl` blue/teal |
| Text | `<p class="nc-sx">` |
| Label (caps) | `<p class="nc-slab">` |
| Rule | `<hr class="nc-srule acc-pink">` |
| Spacer | `<div class="nc-sfill"></div>` pushes what follows down |
| Columns | `<div class="nc-sgrid">` (3) · `--2` · `--4` |
| Column item | `<div class="nc-si nc-si--rule acc-teal">` · `--left` · `--fill`; inside: `.h` heading, `.hc` caps heading, `.big`, `.sub`, `.b` text, `.u` bold text, `ul.ls` |
| Callout | `<p class="nc-scall acc-pink"><b>Lead:</b> text</p>` |
| Closing line | `<p class="nc-sline">` · `--rule` · `--plain` |
| Labelled rows | `<dl class="nc-srows"><dt>..</dt><dd>..</dd></dl>` |
| Panel | `<div class="nc-spanel acc-pink"><p class="l">..</p><p class="b">..</p></div>` |
| Side block | `<div class="nc-sside acc-pink">` after the pad; pad takes `nc-sp--side` |
| Closing band | `<div class="nc-sband"><p class="t">..</p></div>`; pad takes `nc-sp--band` |
| Table | `<table class="nc-stable">` — sent decks only, pattern `table` |
| Wordmark | `<div class="nc-slogo">` + the inline SVG from `assets/nightlife-culture-wordmark.svg`. Never typeset |
| Slide number | `<p class="nc-snum">10</p>` |

Every slide: `<div class="nc-slide" data-pattern="NAME"><div class="cv ground-chalk"><div class="nc-sp">…</div></div></div>`

## Patterns

### Cover — `cover`

**Use when:** The opening slide.  
**Grounds:** blue, ink  
**Reference:** `assets/reference/amgp-v2.0/slide-01.jpg`

```html
<div class="nc-slide" data-pattern="cover">
<div class="cv ground-blue">
<div class="nc-sp nc-sp--cover">
<p class="nc-smeta">Carly Heath / UK Dynamism Fund / September 2026</p>
<div class="nc-sfill" aria-hidden="true">
</div>
<h2 class="nc-st nc-st--cover">Artists make great places</h2>
<hr class="nc-srule acc-pink">
<p class="nc-sl nc-sl--lg">A shared evidence foundation for nightlife advocacy</p>
<div class="nc-sfill" aria-hidden="true">
</div>
<div class="nc-slogo nc-slogo--cover">
<!-- inline assets/nightlife-culture-wordmark.svg -->
</div>
</div>
</div>
</div>
```

### Statement — `statement`

**Use when:** One big idea, with a few sentences that explain it.  
**Grounds:** blue, ink  
**Reference:** `assets/reference/amgp-v2.0/slide-02.jpg`

```html
<div class="nc-slide" data-pattern="statement">
<div class="cv ground-blue">
<div class="nc-sp">
<h2 class="nc-st nc-st--xl">The change I want to see</h2>
<div class="nc-sfill" aria-hidden="true">
</div>
<hr class="nc-srule">
<p class="nc-sl nc-sl--lg">I want the people who create the UKs cultural life after dark to have greater influence over the decisions and investment that shape their places.</p>
<p class="nc-sl nc-sl--lg">That means recognising the gathering places, creative communities and connections that make somewhere worth belonging to and helping people secure the conditions for that culture to flourish.</p>
<p class="nc-sl nc-sl--lg">My purpose for is so that their cultural contribution can be better recognised in policy decisions, placemaking, and investment in their businesses and community</p>
</div>
</div>
</div>
```

### Statement and two columns — `statement-two-columns`

**Use when:** A defining line, then two short columns that unpack it.  
**Grounds:** blue, ink  
**Reference:** `assets/reference/amgp-v2.0/slide-07.jpg`

```html
<div class="nc-slide" data-pattern="statement-two-columns">
<div class="cv ground-blue">
<div class="nc-sp">
<h2 class="nc-st nc-st--xl">A vibe map</h2>
<p class="nc-sl nc-sl--2xl">A living, interactive map of the people, activity, value and support systems that sustain a place’s nightlife culture.</p>
<hr class="nc-srule">
<div class="nc-sgrid nc-sgrid--2">
<div class="nc-si">
<p class="u">It would combine:</p>
<ul class="ls">
<li>Data +</li>
<li>Design +</li>
<li>Storytelling</li>
</ul>
<p class="u">To function as a public access decision-support system for culture and cities.</p>
</div>
<div class="nc-si">
<p class="u">It’s not simply about making beautiful graphics. It’s about building tools that help governments, funders, cultural organisations and communities understand complex urban systems and make better choices.</p>
</div>
</div>
</div>
</div>
</div>
```

### Three columns — `three-columns`

**Use when:** Three related points, each with a heading and a short paragraph. Optional lead above and a callout or closing line below.  
**Grounds:** chalk, white, blue, ink  
**Reference:** `assets/reference/amgp-v2.0/slide-03.jpg`, `assets/reference/amgp-v2.0/slide-05.jpg`, `assets/reference/amgp-v2.0/slide-08.jpg`

```html
<div class="nc-slide" data-pattern="three-columns">
<div class="cv ground-chalk">
<div class="nc-sp">
<h2 class="nc-st">Nightlife needs a seat</h2>
<p class="nc-sl">Nightlife Culture exists to make it easier for the people who create the cultural life of the night to evidence their value, understand their ecosystems and influence the decisions and investment that shape their futures.</p>
<div class="nc-sgrid">
<div class="nc-si nc-si--rule acc-teal">
<p class="h">Knowledge exists, but is fragmented</p>
<p class="b">Evidence takes time and money to assemble, dates quickly and often misses small independent activity.</p>
</div>
<div class="nc-si nc-si--rule acc-butter">
<p class="h">Advocacy needs a shared foundation</p>
<p class="b">We repeat the research and make different claims, sometimes from the same evidence. Common definitions and shared priorities can help us build a united case for change.</p>
</div>
<div class="nc-si nc-si--rule acc-violet">
<p class="h">Cultural value needs a route into action</p>
<p class="b">A shared resource, developed with its users, could strengthen collective advocacy and help shape policy and investment.</p>
</div>
</div>
<p class="nc-scall acc-pink">
<b>Working hypothesis:</b> If people can recognise their scene in a shared evidence base, agree what they need and take a credible collective proposition to the people who can act, nightlife can gain more influence over the decisions and investment shaping its future.</p>
</div>
</div>
</div>
```

### Three filled boxes — `three-boxes`

**Use when:** Three parallel areas, each important enough to hold its own filled block.  
**Grounds:** chalk, white  
**Reference:** `assets/reference/amgp-v2.0/slide-04.jpg`

```html
<div class="nc-slide" data-pattern="three-boxes">
<div class="cv ground-chalk">
<div class="nc-sp">
<h2 class="nc-st">The policy moment</h2>
<div class="nc-sgrid">
<div class="nc-si nc-si--fill acc-teal">
<p class="h">Placemaking</p>
<p class="b">Neighbourhood and town-centre decisions shape cultural space. Nightlife needs representation and evidence of the people and activity already making a place valuable.</p>
</div>
<div class="nc-si nc-si--fill acc-butter">
<p class="h">Business support</p>
<p class="b">Promoters, artists, freelancers and independent venues need support that fits their working lives. We can test where existing provision reaches them, and where it needs to change.</p>
</div>
<div class="nc-si nc-si--fill acc-violet">
<p class="h">Devolution</p>
<p class="b">Regional growth, cultural investment and planning create routes to influence. We need to connect a scene's priorities with the people who control those decisions.</p>
</div>
</div>
<p class="nc-sl nc-sl--hl">Policy already recognises nightlife in important ways. The work is to turn recognition into suitable support and accountable action.</p>
<p class="nc-sx">English Devolution, Pride in Place, Backing Your Business, Turn It Up, and Regional Mayoral Growth strategies give an opportunity for nightlife to provide concrete evidence about their contribution in Neighbourhood Boards, Strategic Authority growth plans and Spatial Development Strategies currently underway</p>
</div>
</div>
</div>
```

### Text and side block — `text-and-side-block`

**Use when:** Main text in columns, plus one thing different in kind set apart in an accent block at the right edge.  
**Grounds:** chalk, white  
**Reference:** `assets/reference/amgp-v2.0/slide-06.jpg`

```html
<div class="nc-slide" data-pattern="text-and-side-block">
<div class="cv ground-chalk">
<div class="nc-sp nc-sp--side">
<h2 class="nc-st nc-st--fit">The evidence already exists</h2>
<div class="nc-sgrid nc-sgrid--2">
<div class="nc-si">
<p class="h">A scoped method, ready to develop</p>
<p class="b">Ticket Atlas is a fully scoped methodology awaiting build. I am expanding it with the ATTTF Vibe Setting findings and public data I used regularly at Bristol City Council.</p>
<p class="h">Purpose and cultural meaning</p>
<p class="b">Connect the evidence with the scene's knowledge, relationships and collective joy. Agree the measures, access and interpretation before building the interactive layer.</p>
</div>
<div class="nc-si">
<p class="h">Skiddle as a partner</p>
<p class="b">We could access customer insight usually available only to an individual promoter, then develop useful benchmarks across comparable events and places. Skiddle can also help us involve venues, promoters and, where needed, audiences through its existing relationships. Other ticketing APIs can help fill gaps in event listings.</p>
</div>
</div>
</div>
<div class="nc-sside acc-pink">
<p class="h">Public data already in the comons</p>
<p class="b">ONS/Nomis: population, employment and business context.</p>
<p class="b">Companies House: company records and legal control.</p>
<p class="b">Planning and local records: development, cultural space and operating conditions.</p>
<p class="b">Published funding data: where support goes.</p>
</div>
</div>
</div>
```

### Steps — `steps`

**Use when:** A method or process of up to eight steps, read left to right. One filled cell may carry the summary.  
**Grounds:** chalk, white  
**Reference:** `assets/reference/amgp-v2.0/slide-09.jpg`

```html
<div class="nc-slide" data-pattern="steps">
<div class="cv ground-chalk">
<div class="nc-sp">
<h2 class="nc-st nc-st--fit">Our creative policy design method</h2>
<p class="nc-sl">My practice brings together human-centred design thinking, restorative economics and participatory creative production.</p>
<div class="nc-sgrid nc-sgrid--4">
<div class="nc-si nc-si--rule acc-blue">
<p class="hc">Listen</p>
<p class="sub">— gather the people</p>
<p class="b">Hear lived experience, establish trust and agree what matters.</p>
</div>
<div class="nc-si nc-si--rule acc-blue">
<p class="hc">Map</p>
<p class="sub">— see the system</p>
<p class="b">Connect cultural activity, relationships, resources and power.</p>
</div>
<div class="nc-si nc-si--rule acc-blue">
<p class="hc">Ideate</p>
<p class="sub">— shape possible answers</p>
<p class="b">Develop shared priorities and responses to the needs people identify.</p>
</div>
<div class="nc-si nc-si--rule acc-blue">
<p class="hc">Prototype</p>
<p class="sub">— make it tangible</p>
<p class="b">Build an early resource or intervention people can use and challenge.</p>
</div>
<div class="nc-si nc-si--rule acc-blue">
<p class="hc">Test</p>
<p class="sub">— learn in the open</p>
<p class="b">Examine recognition, usefulness and action with the people involved.</p>
</div>
<div class="nc-si nc-si--rule acc-blue">
<p class="hc">Refine</p>
<p class="sub">— improve the method</p>
<p class="b">Use feedback and evidence to change the account and the approach.</p>
</div>
<div class="nc-si nc-si--rule acc-blue">
<p class="hc">Expand</p>
<p class="sub">— let the idea travel</p>
<p class="b">Adapt what works with another place while preserving local identity.</p>
</div>
<div class="nc-si nc-si--fill acc-butter">
<p class="u">A repeatable creative production practice, developed through decades of sector-led delivery.</p>
</div>
</div>
</div>
</div>
</div>
```

### Labelled list — `list`

**Use when:** Named groups, each with one or two lines of description: partners, roles, audiences.  
**Grounds:** chalk, white  
**Reference:** `assets/reference/amgp-v2.0/slide-10.jpg`

```html
<div class="nc-slide" data-pattern="list">
<div class="cv ground-chalk">
<div class="nc-sp">
<h2 class="nc-st nc-st--fit">Different partners, shared purpose</h2>
<p class="nc-sl">Serious work needs the right people around the table and the right team behind it.</p>
<dl class="nc-srows">
<dt>Scenes</dt>
<dd>Artists, DJs, promoters, crews and venues: shape the questions, recognise themselves and be heard without being flattened.</dd>
<dt>Sector bodies</dt>
<dd>NTIA, AIF, UK Music and FAC: connect practitioner knowledge, test collective priorities and help evidence travel into united advocacy.</dd>
<dt>Infrastructure partners</dt>
<dd>Skiddle: in-kind support, richer ticketing insight and a route to involve venues, promoters and audiences, with potential investment after launch. Data access and investment terms to agree.</dd>
<dt>Places and policy</dt>
<dd>Nightlife policy officers at LGA, WMCA, MCA and LCR, and the WECA culture team: connect local needs with policy, place and business-support decisions.</dd>
<dt>Funders and investors</dt>
<dd>LIVE Trust and prospective public/private funders: explore propositions with sector legitimacy and what support could change conditions.</dd>
<dt>Researchers</dt>
<dd>Research partners to develop: strengthen the method, interpret evidence and evaluate what happens.</dd>
</dl>
<p class="nc-sline nc-sline--plain">Existing relationships and potential collaborations. Specific roles and commitments to agree.</p>
</div>
</div>
</div>
```

### Two by two — `two-by-two`

**Use when:** Four questions or workstreams of equal weight. Optional label above and a closing line or band below.  
**Grounds:** chalk, white  
**Reference:** `assets/reference/amgp-v2.0/slide-11.jpg`, `assets/reference/amgp-v2.0/slide-13.jpg`

```html
<div class="nc-slide" data-pattern="two-by-two">
<div class="cv ground-chalk">
<div class="nc-sp">
<h2 class="nc-st">Discovery is part of the test</h2>
<div class="nc-sfill" aria-hidden="true">
</div>
<div class="nc-sgrid nc-sgrid--2">
<div class="nc-si nc-si--left acc-teal">
<p class="h">Can we co-design something universally useful?</p>
<p class="b">Discover needs across the user groups, agree common foundations and test how much must adapt between places.</p>
</div>
<div class="nc-si nc-si--left acc-teal">
<p class="h">Does it paint a recognisable picture?</p>
<p class="b">Ask hyperlocal scenes whether they recognise their activity, relationships and identity. Record who is missing and what contributors change.</p>
</div>
<div class="nc-si nc-si--left acc-pink">
<p class="h">Can it steer decisions and collective action?</p>
<p class="b">Follow its use in policy, united advocacy and public/private investment. Record changed and unchanged decisions, and the barriers that remain.</p>
</div>
<div class="nc-si nc-si--left acc-pink">
<p class="h">Can it travel and stay useful?</p>
<p class="b">Test another context and establish the ongoing production, analysis, content, design and maintenance required.</p>
</div>
</div>
<div class="nc-sfill" aria-hidden="true">
</div>
<p class="nc-sline">The ambition is broad usefulness.<br>The fellowship tests where that holds, where it fails and what must change.</p>
</div>
</div>
</div>
```

### Phases — `phases`

**Use when:** Periods of time and what happens in each, with a milestone.  
**Grounds:** chalk, white  
**Reference:** `assets/reference/amgp-v2.0/slide-12.jpg`

```html
<div class="nc-slide" data-pattern="phases">
<div class="cv ground-chalk">
<div class="nc-sp">
<h2 class="nc-st nc-st--fit">Building together, ready for launch</h2>
<div class="nc-sgrid nc-sgrid--2">
<div class="nc-si">
<p class="big">Months 1–3</p>
<p class="hc">Discover and agree</p>
<p class="b">Convene scenes and decision users. Build shared understanding and priorities. Audit existing data, agree partner access and develop the first prototype around the needs identified.</p>
</div>
<div class="nc-si">
<p class="big">Months 3–6</p>
<p class="hc">Develop and prepare</p>
<p class="b">Co-design and test the resource with its users. Refine the evidence and experience. Coordinate partner participation, launch storytelling and PR/comms with Plaster Creative Communications.</p>
</div>
</div>
<div class="nc-spanel acc-pink">
<p class="l">Public milestone</p>
<p class="b">Aim for the Night Time Economy Summit in 2027, Feb 7-11, and participation. Prepare demonstrations and ways for people to contribute and use the resource afterwards.</p>
</div>
<p class="nc-sx">Production support covers coordination, logistics and follow-through. Early application and business development begin alongside the build.</p>
</div>
<p class="nc-snum">10</p>
</div>
</div>
```

### Table — `table`

**Use when:** Figures that have to be read row by row, such as a budget. For decks that are sent and read, not projected.  
**Grounds:** chalk, white  
**Reference:** `assets/reference/amgp-v2.0/slide-14.jpg`

```html
<div class="nc-slide" data-pattern="table">
<div class="cv ground-chalk">
<div class="nc-sp">
<h2 class="nc-st nc-st--fit">Budget</h2>
<table class="nc-stable">
<thead>
<tr>
<th scope="col">Cost item</th>
<th scope="col">Unit</th>
<th class="num" scope="col">Quantity</th>
<th class="num" scope="col">Rate GBP</th>
<th class="num" scope="col">Cost GBP</th>
<th scope="col">Timing</th>
<th scope="col">Included scope</th>
</tr>
</thead>
<tbody>
<tr>
<td>Carly and project leadership</td>
<td>months</td>
<td class="num">6</td>
<td class="num">£3,000</td>
<td class="num">£18,000</td>
<td>M1–6</td>
<td>Vision, discovery, facilitation, partnerships, synthesis and business development.</td>
</tr>
<tr>
<td>Producer and operations</td>
<td>days</td>
<td class="num">14.0</td>
<td class="num">£450</td>
<td class="num">£6,300</td>
<td>M1–6</td>
<td>Work tracking, logistics, partner coordination, reporting and launch production.</td>
</tr>
<tr>
<td>Creative technology</td>
<td>days</td>
<td class="num">16.0</td>
<td class="num">£600</td>
<td class="num">£9,600</td>
<td>M1–6</td>
<td>Shared capacity for data integration, prototype development, testing and launch fixes.</td>
</tr>
<tr>
<td>Analysis and data quality</td>
<td>days</td>
<td class="num">6.0</td>
<td class="num">£700</td>
<td class="num">£4,200</td>
<td>M1–5</td>
<td>Data audit, GIS, source matching, evidence definitions and quality checks.</td>
</tr>
<tr>
<td>Design and accessibility</td>
<td>days</td>
<td class="num">3.0</td>
<td class="num">£600</td>
<td class="num">£1,800</td>
<td>M2–6</td>
<td>Information and interface design, cultural voice and accessibility review.</td>
</tr>
<tr>
<td>Participant contributions</td>
<td>payments</td>
<td class="num">15</td>
<td class="num">£120</td>
<td class="num">£1,800</td>
<td>M1–5</td>
<td>Payment for substantial contributions; this is not a community-research staff budget.</td>
</tr>
<tr>
<td>Convening venue and catering</td>
<td>sessions</td>
<td class="num">2</td>
<td class="num">£300</td>
<td class="num">£600</td>
<td>M2 and M4</td>
<td>Two small co-design convenings. Facilitation and production are in the people lines.</td>
</tr>
<tr>
<td>Participant travel and access</td>
<td>allowance</td>
<td class="num">1</td>
<td class="num">£600</td>
<td class="num">£600</td>
<td>M1–5</td>
<td>Travel, access and participation support; requirements need checking with contributors.</td>
</tr>
<tr>
<td>Launch content and PR</td>
<td>allowance</td>
<td class="num">1</td>
<td class="num">£1,800</td>
<td class="num">£1,800</td>
<td>M4–6</td>
<td>Launch story, copy, assets and PR support. Agree the scope with Plaster.</td>
</tr>
<tr>
<td>Launch session direct costs</td>
<td>event</td>
<td class="num">1</td>
<td class="num">£700</td>
<td class="num">£700</td>
<td>M5–6</td>
<td>A modest launch session: venue, materials and local delivery costs. Producer time is separate.</td>
</tr>
</tbody>
</table>
</div>
</div>
</div>
```

### Team and close — `team-and-close`

**Use when:** Who is doing the work, ending on the offer in a closing band with the wordmark.  
**Grounds:** chalk, white  
**Reference:** `assets/reference/amgp-v2.0/slide-15.jpg`

```html
<div class="nc-slide" data-pattern="team-and-close">
<div class="cv ground-chalk">
<div class="nc-sp nc-sp--band">
<h2 class="nc-st">The team and the backing</h2>
<p class="nc-slab">Carly Heath</p>
<p class="nc-sx">Creative producer, former promoter and cultural-policy practitioner. Lead the vision, facilitate convenings and develop partnerships and the business.</p>
<hr class="nc-srule acc-blue">
<div class="nc-sgrid">
<div class="nc-si">
<p class="hc">Already around the work</p>
<p class="b">Storytelling, design and communications relationships. Plaster Creative Communications supports storytelling and PR for the prototype launch.</p>
</div>
<div class="nc-si">
<p class="hc">Capacity to bring on board</p>
<p class="b">Production support for coordination, logistics and follow-through, including any touring convenings. Creative technologists to build and iterate. Analysts to connect, interpret and maintain credible evidence.</p>
</div>
<div class="nc-si">
<p class="hc">Long-term team development</p>
<p class="b">Internal content creation and design, with ongoing production, data and partnership capacity. Bring in specialist research and paid cultural expertise as the work requires.</p>
</div>
</div>
</div>
<div class="nc-sband">
<p class="t t--plain">A meaningful six-month fellowship scope for discussion within the longer plan.</p>
<div class="nc-slogo">
<!-- inline assets/nightlife-culture-wordmark.svg -->
</div>
</div>
</div>
</div>
```

## When nothing fits

Compose the slide from the blocks above and say which pattern is new. The design system adds
it to `foundations/patterns.json` with the live slide it came from. Never invent a size, a colour
or a spacing value; if a block is missing, say so.

## Diagrams — not yet specified

No diagram kit exists. Build process chains and timelines from columns, rules and panels. Never
use PowerPoint SmartArt defaults.
