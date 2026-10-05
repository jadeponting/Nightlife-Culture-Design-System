# Charts and data

**The brand accents cannot carry data.** They are separated by hue alone. Use the ramp.

## The chart ramp

| Series | Hex | OKLCH L | Labels |
|---|---|---|---|
| Series 1 | `#0000FF` | 0.45 | White |
| Series 2 | `#C7339A` | 0.58 | White |
| Series 3 | `#00C6C5` | 0.75 | Ink |
| Series 4 | `#FFDE6B` | 0.91 | Ink |

Lightness climbs monotonically (0.45 → 0.58 → 0.75 → 0.91), so the order survives photocopying,
greyscale printing and every form of colour vision deficiency. Series 1 and 4 are brand tokens
unchanged; 2 and 3 are the brand pink and teal deepened for data. In CSS they are `--nc-chart-1` to
`--nc-chart-4`.

## Chart rules

| Rule | Why |
|---|---|
| **Four series maximum** | Beyond four the ramp stops being distinguishable. Five categories = a bar chart with direct labels, not more colours |
| **One series = blue** | A single-series chart in four colours implies a distinction that is not there |
| **Label at the mark** | Values on bars, series names at the end of lines, percentages in the key. Legends are a last resort |
| **Never brand accents** | Pink, teal, violet, butter and coral are surfaces. Only the ramp encodes data |
| **Show the gaps** | Hatched fill for suppressed, dashed line for a break in collection. Never a silent omission — a gap is a finding |
| **Show the range** | Modelled or surveyed values get a visible interval. A bare point estimate reads as a count |
| **Provenance on every chart** | Code, reference period, geography, boundary vintage |
| **Flag illustrative figures** | Any placeholder says so, in the chart, every time: `<span class="nc-illus">Illustrative</span>` |
| **Gridlines at 10% ink** | Present enough to read against, quiet enough to disappear. Never heavier than the data |
| **Alt text describes the finding** | Not "line chart of venue counts" but what the chart shows. Plus a data table for anything load-bearing |
| **No non-uniform scaling** | Never `preserveAspectRatio="none"` on an SVG, never stretch an image. The container flexes; the coordinate space does not |
| **Figures are Inter, tabular** | Never monospace. Values, axes and keys are Inter with tabular figures |

## Chart types

| Type | Class | When |
|---|---|---|
| **Ranked horizontal bar** | `.nc-bar` | The workhorse. Categories with a magnitude. Ranked descending unless naturally ordered |
| **Dot plot** | `.nc-dot` | **Comparing places.** Bars imply a quantity from zero; dots imply a position on a scale, and leave room for the range |
| **100% stacked bar** | `.nc-stack` + `.nc-key` | Comparing two or more wholes. Replaces most pies |
| **Donut** | `.nc-donut` | One whole, four segments max, percentages in the key. The hole carries the total |
| **Pie** | `.nc-pie` | Permitted, with the caveat that angles read less accurately than lengths |
| **Line** | `.nc-line` | Change over time. Series labelled at the line. Dashed segments for breaks — never interpolate across one |
| **Range bar** | `.nc-range` | Anywhere uncertainty is material |

The marks inside a chart (`.big` on a statistic, `.lb` `.vl` on a bar or dot row, segment and series
labels) are the one place the stylesheet sizes text outside the roles; they are sized to the chart
and named as such in the type manifest. Everything around the chart — title, subtitle, evidence
block — is a role.

---

## Evidence furniture

From *Comparative Place-Based Research Methodology v1.0*. Not decorative.

### Provenance chips
Three tiers. The code text carries the meaning on its own, so the tier survives greyscale and screen
readers. **Coral does not mean "bad"** — it means "handle with a stated caveat".

| Tier | Class | Codes |
|---|---|---|
| Open and traceable | `.nc-prov` (ink) | OFF-OPEN · ADM-OPEN · ADM-RESTRICTED · ACADEMIC · PRI-OPEN |
| Documented but partial | `.nc-prov.nc-prov--mid` (butter) | SECTOR · COM-DOCUMENTED · PRI-DOCUMENTED |
| Opaque or untraceable | `.nc-prov.nc-prov--low` (coral) | COM-PARTIAL · COM-BLACKBOX · PRI-OPAQUE · ANECDOTAL · UNTRACEABLE |

```html
<div class="nc-evidence"><span class="nc-prov">ADM-OPEN</span><span class="nc-source">ONS · 2024 · England · administrative · final</span></div>
<span class="nc-prov nc-prov--mid">SECTOR</span>
<span class="nc-prov nc-prov--low">COM-BLACKBOX</span>
```

### Comparability flag
Any chart comparing two or more places states whether the **indicator comparability gate** cleared,
and which of the eight criteria required harmonisation: concept and numerator/denominator · unit and
price basis · reference period and vintage · geography and geography basis · population/universe ·
classification system and version · observed vs modelled method · treatment of uncertainty and
suppression. **A comparison without this note is not publishable.**

```html
<p class="nc-comp"><b>Comparability gate — passed with harmonisation.</b> Period and geography harmonised.</p>
```
`.nc-comp--part` (butter rule) and `.nc-comp--fail` (coral rule) rank it; the words carry it.

### Recommendation strength
The 1–5 scale as **filled ordinal steps in ink**, never a colour scale. The level is always written out.

```html
<div class="nc-meter"><span class="on"></span><span class="on"></span><span class="on"></span><span></span><span></span></div>
<div class="nc-meter-lab"><span>Evidence strength</span><span>3 of 5 · documented</span></div>
```
1 general aspiration · 2 directional · 3 defined intervention · 4 costed and owned ·
5 funded and scheduled.

### Missing and suppressed data
`[c]` suppressed for disclosure control · `n/a` not collected for this population
(`<span class="nc-na">n/a</span>`). Hatched fill, row retained. **Never drop the row.**

---

## Markup patterns

Chart card — white panel, hairline, callout line on top, evidence footer. Colour by accent modifier.
```html
<div class="nc-chart acc-teal">
  <p class="ct">Grassroots venues per 100,000 residents</p>
  <p class="cs">Dot plot · five comparator places · point estimate with plausible range</p>
  <!-- chart -->
  <p class="ev"><b>Comparability gate — passed with harmonisation.</b><br>
    …which criteria were harmonised…<br>
    <span class="nc-prov">ADM-OPEN</span><span class="nc-prov nc-prov--mid">SECTOR</span> <span class="nc-illus">Illustrative</span></p>
</div>
```
`acc-blue` (default) · `acc-pink` · `acc-teal` · `acc-butter` · `acc-violet`.

Bar row:
```html
<div class="nc-bar"><span class="lb">Venues</span>
  <span class="tk"><span class="fl" style="width:82%"></span></span>
  <span class="vl">82</span></div>
```
A second series sets `style="background:var(--nc-chart-2)"` on `.fl`; never a hex.

Suppressed bar:
```html
<span class="tk"><span class="fl nc-hatch" style="width:100%"></span></span><span class="vl">[c]</span>
```

Dot plot row with range:
```html
<div class="nc-dot"><div class="row"><span class="lb">Bristol</span>
  <span class="tk"><span class="rng" style="left:38%;width:22%"></span><span class="pt" style="left:49%"></span></span>
  <span class="vl">4.9</span></div></div>
```

Line charts: plain SVG with `viewBox`, **no `preserveAspectRatio="none"`**. Series labels (`.sl`)
at the end of the line, axes (`.ax`) in the label voice.
