#!/usr/bin/env python3
"""The content router — how a piece of content becomes a component.

This is the logic layer. It takes content, asks the Book's questions IN ORDER,
and returns a component, the rules that fired, and any refusal.

The order is not arbitrary. It is the decision stack (ch01):
    1 user need · 2 output format · 3 semantic structure
    4 reading clarity · 5 brand expression · 6 flourish
When two considerations compete, the higher one wins. So the router checks
meaning before it checks appearance, and it can REFUSE — a chart that cannot
be made honest does not get a colour scheme.

    python3 components/route.py            run the built-in examples
"""
import json, pathlib, re, unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
RULES = {r["id"]: r for r in json.loads((ROOT/"foundations"/"rules.json").read_text())["rules"]}

# Approximate mid-2023 populations, used ONLY as a floor sanity test.
# Marked as reference data, not a published source — the check it powers is
# "is this figure physically possible", not "is this figure correct".
POP = {"manchester":568000, "west midlands":5950000, "brighton":277000,
       "brighton and hove":277000, "haywards heath":35000, "london":8900000,
       "bristol":479000, "leeds":822000, "newcastle upon tyne":300000}
GEOG = {"manchester":"local authority", "brighton":"town (part of Brighton and Hove)",
        "brighton and hove":"local authority", "bristol":"local authority",
        "leeds":"local authority", "newcastle upon tyne":"local authority",
        "west midlands":"region", "haywards heath":"town (part of Mid Sussex)"}

class Decision:
    def __init__(self, kind):
        self.kind, self.fired, self.warn, self.refuse, self.html, self.notes = kind, [], [], [], "", []
    def rule(self, rid, what):   self.fired.append((rid, what))
    def flag(self, rid, what):   self.warn.append((rid, what)); self.fired.append((rid, what))
    def stop(self, rid, what):   self.refuse.append((rid, what)); self.fired.append((rid, what))
    @property
    def blocked(self): return bool(self.refuse)

SHOUT = re.compile(r"\b[A-Z]{2,}\b")          # a word typed in capitals
STUCK = re.compile(r"\b[A-Z]{2,}[a-z]")        # shift held too long: "MAke"
def _sentence(s):
    """Caps are a character format, never typed (TYP-14, Fixed). If the source
    arrives in typed capitals, the router lowercases it and lets CSS transform
    it — so the underlying string survives for search, copy-paste and AT.

    Three things count as typed caps, not one:
      · the whole string shouted
      · any single word shouted  ("HOW CITIES MAke great places")
      · a shift-key artefact inside a word ("MAke")
    All three produce the same corrupt string, so all three are normalised."""
    letters = [c for c in s if c.isalpha()]
    ratio = sum(c.isupper() for c in letters)/len(letters) if letters else 0
    if ratio > .6 or SHOUT.search(s) or STUCK.search(s):
        # Lowercase, then raise the first letter only. Proper nouns cannot be
        # recovered automatically — that is flagged, not guessed.
        return s[:1].upper() + s[1:].lower() if s else s, True
    return s, False

# ---------------------------------------------------------------- QUOTE
def route_quote(text, attribution=None):
    d = Decision("quote")
    d.rule("ch18", "Tier first. A pull quote is decorative — free, provided nothing "
                   "load-bearing lives only there.")
    # Does it carry a finding? A number, a percentage, a measured claim.
    carries = re.search(r"\d|\bper cent\b|%|\bfell\b|\brose\b|\bincreas|\bdecreas", text, re.I)
    if carries:
        d.stop("NC-DIR-01", "This quote contains a figure or a measured claim. Meaning may not "
               "live in the decorative layer — move the finding into the body as real text "
               "with a source, and keep the quote for the voice.")
        return d
    d.rule("ch18", "No figure, no measured claim — nothing load-bearing. Decorative holds.")
    body, was_caps = _sentence(text)
    if was_caps:
        d.flag("NC-TYP-01", "Source arrived in typed capitals; lowercased so the case can be "
               "applied as a format.")
    d.rule("NC-TYP-03", "Quotes are sentence case, and the quote component refuses to inherit "
                        "capitals from whatever it is dropped inside. Put it on a section opener "
                        "that shouts and the quote still speaks normally.")
    d.rule("NC-CON-03", "Pull quotes take the left rule — a 12px accent bar, white panel. "
                        "v1.4 §09: 'reads as an aside rather than a box'.")
    d.rule("ch03", "Measure capped at 40ch. Leading 1.24 — display-adjacent, not running prose.")
    att = f'\n  <cite class="a">{attribution}</cite>' if attribution else ""
    if not attribution:
        d.flag("ch09", "No attribution. A quote without a speaker is a claim without a source.")
    d.html = f'<blockquote class="nc-quote">\n  <p class="q">{body}</p>{att}\n</blockquote>'
    d.notes.append("Accent is a modifier, never baked in: add .acc-teal etc. to change it.")
    return d

# ---------------------------------------------------------------- DATA
def route_data(measure, rows, unit="count", title=None, source=None,
               reading=None, prov=("OFF-OPEN", "")):
    """rows: list of (place, value, year)"""
    d = Decision("data")
    d.rule("ch06", "Name the comparison before the form. Several places, one measure, "
                   "one period → magnitude and ranking. Not a time series.")

    # --- 3 · semantic/factual integrity, before any chart choice ---
    years = {r[2] for r in rows}
    bad_year = [y for y in years if not (1900 <= y <= 2100)]
    if bad_year:
        d.stop("NC-EVI-01", f"Year {bad_year[0]} is not a date. ISO 8601 in the data, "
               "natural language in the display — and a year outside range is a typo, "
               "not a value.")
    if len(years - set(bad_year)) > 1:
        d.flag("ch08", "More than one reference period in one series.")

    levels = {GEOG.get(r[0].lower(), "UNKNOWN") for r in rows}
    if len(levels) > 1:
        d.stop("NC-EVI-01", "The comparability gate fails. These are not one series: "
               + " · ".join(f"{r[0]} = {GEOG.get(r[0].lower(),'unknown level')}" for r in rows)
               + ". ch08: two values do not go in one comparison until concept, unit, period, "
                 "geography, population and classification all match or are harmonised. "
                 "A city, a region and a town are three different geographies.")

    impossible = []
    for place, val, _ in rows:
        pop = POP.get(place.lower())
        if pop and val > pop:
            impossible.append((place, val, pop))
    if impossible:
        d.stop("NC-EVI-04", "Implausible values — a job count cannot exceed the population. "
               + " · ".join(f"{p}: {v:,} jobs against roughly {pp:,} people" for p, v, pp in impossible)
               + ". Strong design must never make weak evidence look stronger than it is.")

    d.rule("ch06", "Provenance is part of the chart, not an afterthought: source linked to the "
                   "dataset, reference period, geography and boundary vintage, method, revision "
                   "status, disclosure treatment, illustrative flag.")
    if d.blocked:
        d.notes.append("No form is chosen. A chart that cannot be made honest does not get "
                       "a colour scheme — the decision stack puts factual integrity above "
                       "brand expression and above flourish.")
        return d

    # --- form, only once the data survives ---
    if unit == "count":
        d.rule("ch06", "The measure is a count — a quantity from zero. Bars encode length "
                       "from zero, which is rank 1 on the perceptual ranking. Bar chart.")
        d.rule("charts v1.4", "The 'dot plot, not bar chart, for places' rule governs indicators "
                              "— a position on a scale. It does not govern counts. A count gets a bar.")
    else:
        d.rule("charts v1.4", "The measure is an indicator — a position on a scale, not a "
                              "quantity from zero. Dot plot, with the range shown, because a bar "
                              "with no visible range makes a modelled estimate look like a count.")
    d.rule("NC-COL-02", "One series, several categories. A single series means a single colour, and that is blue. "
                        "The four-colour ramp is for genuinely different series; using it here "
                        "would imply a distinction that is not there.")
    d.rule("NC-COL-04", "Label at the mark. Values sit outside the track, right-aligned, "
                        "tabular figures.")
    d.rule("ch06", "Ranked descending — alphabetical is almost never the reader's question.")
    ordered = sorted(rows, key=lambda r: -r[1])
    top = ordered[0][1]
    bars = "\n".join(
        f'  <div class="nc-bar"><span class="lb">{p}</span>'
        f'<span class="tk"><span class="fl" style="width:{v/top*100:.0f}%"></span></span>'
        f'<span class="vl">{v:,}</span></div>' for p, v, _ in ordered)
    if not title:
        d.flag("ch06", "No title supplied. The title carries the message — a chart headed with "
               "its topic makes the reader do the work of finding the finding.")
    if not source:
        d.stop("NC-EVI-02", "No source. A chart travels; the moment it is screenshotted into a "
               "board paper it must still say where the number came from.")
        return d
    yr = sorted(years)[0]
    # NC-EVI-09 — if the source says the figures are illustrative, the flag goes
    # ON THE MARKS, not in the prose. Charts travel; the moment one is
    # screenshotted into a board paper the prose is gone.
    illus = ""
    if re.search(r"illustrat|placeholder|worked example", source, re.I):
        illus = '<span class="nc-illus">Illustrative</span> '
        d.rule("NC-EVI-09", "Source says illustrative, so the flag is placed on the chart itself "
               "rather than left in the surrounding text.")
    d.html = ('<figure class="nc-chart acc-blue">\n'
              f'  <h3 class="ct">{title or "[Title states the finding, not the topic]"}</h3>\n'
              f'  <p class="cs">{measure}, local authority districts, {yr}.</p>\n{bars}\n'
              f'  <figcaption class="ev"><b>Reading.</b> {reading or "[What the reader should take from it]"}<br>\n'
              f'    {illus}<span class="nc-prov">{prov[0]}</span> {source}</figcaption>\n'
              '</figure>')
    return d

# ---------------------------------------------------------------- SECTION
FINDING = re.compile(r"\d|\bfell\b|\brose\b|\bmore\b|\bless\b|\bnot\b|\bbut\b|:|\bwhy\b|\bcannot\b", re.I)
def route_section(number, title, body=None, level=2):
    d = Decision("section")
    d.rule("ch11", "A section header is a heading — marked up as one, never text styled to "
                   "look like one. SC 1.3.1.")
    t, was_caps = _sentence(title)
    if was_caps:
        d.flag("NC-TYP-01", "Title arrived with typed capitals. Normalised to sentence case in "
               "the source. It still appears in capitals, because the section header applies "
               "them as a format — but the underlying words stay ordinary, so search, "
               "copy-paste and a screen reader all get a readable sentence. Proper nouns cannot "
               "be recovered automatically: check the result if the title names a place, a "
               "person or an organisation.")
    if not FINDING.search(t):
        d.flag("ch05", f"'{t}' is a topic label, not a finding. ch05: 'Referrals rose 34% after "
               "the drop-in opened' is a heading; 'Referral trends' is a filing label. A contents "
               "list built from finding-headings is a readable summary, which is what most "
               "readers use it as.")
    d.rule("NC-CON-04", "The numeral box sits inside the heading element, not beside it. "
                        "It looks like a heading and it is one.")
    d.rule("v1.4 §11", "Numeral optional — omit where the section is not numbered. "
                       "An invented number is worse than none.")
    d.rule("ch11", f"Level h{level}. No skipped levels — h2 to h4 breaks outline navigation, "
                   "which is how screen-reader users move through a long document.")
    num = f'<span class="num">{number:02d}</span>' if number is not None else ""
    d.html = f'<h{level} class="nc-section-head">{num}<span class="ttl">{t}</span></h{level}>'
    if body:
        s = body.strip()
        if len(s.split()) > 28 and s.count(".") < 2:
            d.flag("ch05", "One long sentence carrying several ideas. 'Every sentence "
                   "interpretable one way only' — split it.")
        if re.search(r"\bamazing\b|\bdeserve\b|\bincredible\b", s, re.I):
            d.flag("ch16", "This is a values claim, not evidence. Framing is how evidence gets "
                   "a hearing; it may not substitute for evidence. Keep it, and put the "
                   "finding next to it.")
        d.rule("ch03", "Body is running prose: leading 1.5–1.6, measure ≤80ch, left aligned, "
                       "12pt floor. The only place the 1.5 rule applies.")
        d.html += f'\n<p>{s}</p>'
    return d

# ---------------------------------------------------------------- CATALOGUE
# Components are grouped by the job they do, not by what they look like.
# Two things that look similar but do different jobs are different components;
# two things that do the same job in different places are one component with a
# modifier. This is what makes the set format-agnostic — the job survives the
# move from a deck to a web page to an evaluation report, the appearance does not.
FAMILIES = [
 {"name":"Structure", "job":"Tells the reader where they are.",
  "members":["section header","contents list","running foot","page / slide frame"],
  "classes":[".nc-section-head",".nc-contents",".nc-foot",".nc-slide"],
  "place":"At the boundary it names, never inside an argument. If it appears mid-thought "
          "it is not structure, it is interruption.",
  "tier":"Fixed — a heading is a heading. Marked up as one or it is a lie to a screen reader."},
 {"name":"Argument", "job":"Carries the claim.",
  "members":["body prose","list","numbered list","breakout stat","pull quote"],
  "classes":["p",".nc-list",".nc-list--num",".nc-stat",".nc-quote"],
  "place":"In reading order. The claim comes before its support, never after it. "
          "A stat or a quote sits beside the paragraph it belongs to, not floating.",
  "tier":"Fixed on structure, Adaptable on emphasis — which sentence gets the breakout "
         "is a judgement, that it is a real element is not."},
 {"name":"Containment", "job":"Groups things, and tells you how to read the group.",
  "members":["top-rule panel","left-rule panel","flyer panel","filled panel","full-width band"],
  "classes":[".nc-panel--top",".nc-panel--left",".nc-panel--flyer",".nc-panel--fill",".nc-band"],
  "place":"The edge treatment is the instruction — see the container ladder below. "
          "Choosing the edge is choosing what you are telling the reader to do.",
  "tier":"Fixed — v1.4 §09 assigns each edge a meaning. Picking one for looks breaks the code."},
 {"name":"Evidence", "job":"Carries the finding, and everything needed to check it.",
  "members":["chart card","table","provenance chip","ordinal meter","source line","caption"],
  "classes":[".nc-chart",".nc-table",".nc-prov",".nc-meter",".nc-source",".nc-caption"],
  "place":"Adjacent to the claim it supports, and never separated from its provenance. "
          "A chart that travels without its source is not evidence, it is decoration "
          "with numbers on.",
  "tier":"Fixed — ch06 packages title, source, alt text, data and vector together."},
 {"name":"Punctuation", "job":"Controls pace. Says a movement has ended.",
  "members":["bar breaker","hairline breaker","ground change"],
  "classes":[".nc-brk",".nc-brk--bar",".nc-brk--hair",".ground-*"],
  "place":"Between movements, never inside one. A breaker inside an argument reads as "
          "a fault, not a beat.",
  "tier":"Adaptable — how often you breathe is yours. What a break must buy is not (six purchases)."},
 {"name":"Reference", "job":"Qualifies. Supporting information, never the message.",
  "members":["label","caption","defined term","link"],
  "classes":[".lab",".nc-caption",".nc-term",".nc-link"],
  "place":"Attached to the thing it qualifies, above or below it, never orphaned. "
          "Labels are qualifiers — the references, the supporting info — not navigation.",
  "tier":"Fixed on contrast and size floor, Adaptable on wording."},
]

# Which container? The ladder is read top to bottom; the first yes wins.
CONTAINERS = [
 ("Is it a single number that is itself the finding?",
  ".nc-stat", "Breakout stat. Nothing else in the box competes with the number."),
 ("Is it a supporting aside the reader could skip and still follow the argument?",
  ".nc-panel--left / .nc-quote", "Left rule, 12px. v1.4 §09: 'reads as an aside rather "
  "than a box'. The reader's eye can pass it."),
 ("Is it a labelled group that belongs to the section it sits under?",
  ".nc-panel--top", "Top rule, 9px. The rule is a lid — it ties the box to what precedes it."),
 ("Is it a standalone card that has to survive being pulled out on its own?",
  ".nc-panel--flyer", "Full outline. The only sanctioned hard outline, because the thing "
  "genuinely has no context around it."),
 ("Is it a whole movement — a change of subject, not a change of paragraph?",
  ".nc-band", "Full-width band with a ground change. The most expensive move available; "
  "it must buy one of the six purchases."),
 ("None of the above — it just needs to be visually together?",
  ".nc-panel--hair", "Hairline. Inert grouping only. Never for anything carrying meaning — "
  "a hairline is not findable enough to be load-bearing."),
]

def run_examples():
    ex = []
    ex.append(("A", "A pull quote", route_quote(
        "if your chest ain't rattling it ain't happening", "Carly Heath, Junglist Extraordinaire")))
    ex.append(("A2", "The same quote, if it carried a figure", route_quote(
        "if your chest ain't rattling it ain't happening — and 60% of them say so",
        "Carly Heath, Junglist Extraordinaire")))
    ex.append(("B", "Number of jobs, by place", route_data("Number of jobs", [
        ("Manchester", 180000, 2026), ("West Midlands", 24958437, 2026),
        ("Brighton", 2947463628, 2026), ("Haywards Heath", 83627, 2926)])))
    ex.append(("B2", "The same question, with the data repaired", route_data(
        "Night-time economy jobs", [("Manchester", 41200, 2024), ("Leeds", 33900, 2024),
        ("Bristol", 18450, 2024), ("Brighton and Hove", 12800, 2024)],
        title="Manchester employs more than twice as many night-time workers as Bristol",
        reading="Four comparable districts, one measure, one year. The gap is the point.",
        source="Illustrative figures — replace with BRES, ONS, released 2025, "
               "2024 boundaries, unrevised.")))
    ex.append(("C", "A numbered section", route_section(
        18, "HOW CITIES MAke great places", level=4,
        body="Cities are the source of talent and innovation for nightlife and the people "
        "there are amazing and deserve all the joy")))
    return ex

if __name__ == "__main__":
    for tag, title, d in run_examples():
        print(f"\n=== {tag} · {title} · {d.kind} " + "=" * 20)
        for rid, what in d.fired:
            mark = "STOP" if (rid, what) in d.refuse else ("flag" if (rid, what) in d.warn else "  ok")
            print(f"  [{mark}] {rid}: {what[:100]}")
        print("  ->", "REFUSED, no component produced" if d.blocked else d.html.split("\n")[0])
