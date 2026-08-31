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
unchanged; 2 and 3 are the brand pink and teal deepened for data.

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
| **Flag illustrative figures** | Any placeholder says so, in the chart, every time |
| **Gridlines at 10% ink** | Present enough to read against, quiet enough to disappear. Never heavier than the data |
| **Alt text describes the finding** | Not "line chart of venue counts" but what the chart shows. Plus a data table for anything load-bearing |
| **No non-uniform scaling** | Never `preserveAspectRatio="none"` on an SVG, never stretch an image. The container flexes; the coordinate space does not. Stretching destroys the type |

## Chart types

| Type | When |
|---|---|
| **Ranked horizontal bar** | The workhorse. Categories with a magnitude. Ranked descending unless naturally ordered |
| **Dot plot** | **Comparing places.** Bars imply a quantity from zero; dots imply a position on a scale — which is what an indicator is — and leave room for the range |
| **100% stacked bar** | Comparing two or more wholes. Replaces most pies |
| **Donut** | One whole, four segments max, percentages in the key. The hole carries the total |
| **Pie** | Permitted, with the caveat that angles read less accurately than lengths. Justified when one dominant share must be instantly recognisable |
| **Line** | Change over time. Series labelled at the line. Dashed segments for breaks — never interpolate across one |
| **Range bar** | Anywhere uncertainty is material |

---

## Evidence furniture

From *Comparative Place-Based Research Methodology v1.0*. Not decorative.

### Provenance chips
Three tiers. The code text carries the meaning on its own, so the tier survives greyscale and screen
readers. **Coral does not mean "bad"** — it means "handle with a stated caveat".

| Tier | Colour | Codes |
|---|---|---|
| Open and traceable | Ink `#0D0D0D` | OFF-OPEN · ADM-OPEN · ADM-RESTRICTED · ACADEMIC · PRI-OPEN |
| Documented but partial | Butter `#FFDE6B` | SECTOR · COM-DOCUMENTED · PRI-DOCUMENTED |
| Opaque or untraceable | Coral `#FD7B53` | COM-PARTIAL · COM-BLACKBOX · PRI-OPAQUE · ANECDOTAL · UNTRACEABLE |

```html
<span class="prov">ADM-OPEN</span>
<span class="prov mid">SECTOR</span>
<span class="prov warn">COM-BLACKBOX</span>
```

### Comparability flag
Any chart comparing two or more places states whether the **indicator comparability gate** cleared,
and which of the eight criteria required harmonisation: concept and numerator/denominator · unit and
price basis · reference period and vintage · geography and geography basis · population/universe ·
classification system and version · observed vs modelled method · treatment of uncertainty and
suppression. **A comparison without this note is not publishable.**

### Recommendation strength
The 1–5 scale as **filled ordinal steps in ink**, never a colour scale — strength is ordinal, so it
shows by how much is filled. Readable in greyscale, and cannot be mistaken for red/amber/green. The
level is always written out: *"Level 4 · costed and owned"*.

1 general aspiration · 2 directional · 3 defined intervention · 4 costed and owned ·
5 funded and scheduled.

### Missing and suppressed data
`[c]` suppressed for disclosure control · `n/a` not collected for this population. Hatched fill,
row retained. **Never drop the row** — dropping it hides the finding.

---

## Markup patterns

Chart card — white panel, hairline, accent top rule, evidence footer:
```html
<div class="ch tl">
  <div class="ct">Grassroots venues per 100,000 residents</div>
  <div class="cs">Dot plot · five comparator places · point estimate with plausible range</div>
  <!-- chart -->
  <div class="ev"><b>Comparability gate — passed with harmonisation.</b><br>
    …which criteria were harmonised…<br>
    <span class="prov">ADM-OPEN</span><span class="prov mid">SECTOR</span> Illustrative figures.</div>
</div>
```
Accent top rule variants: `.ch` blue (default) · `.ch.pk` pink · `.ch.tl` teal · `.ch.bt` butter ·
`.ch.vt` violet.

Bar row:
```html
<div class="bar"><span class="lb">Venues</span>
  <span class="tkk"><span class="fl" style="width:82%;background:#0000FF"></span></span>
  <span class="vl">82</span></div>
```

Suppressed bar:
```html
<span class="tkk"><span class="fl hatch" style="width:100%"></span></span><span class="vl">[c]</span>
```

Dot plot row with range:
```html
<div class="row"><span class="lb">Bristol</span>
  <span class="tk2"><span class="rng" style="left:38%;width:22%"></span>
  <span class="pt" style="left:49%"></span></span><span class="vl">4.9</span></div>
```

Line charts: plain SVG with `viewBox`, **no `preserveAspectRatio="none"`**. Labels in Archivo 800 at
H3 scale or above, placed at the end of the line.
