#!/usr/bin/env python3
"""Build the portable skill (nightlife-culture-design.skill) FROM the repo.

    python3 adapters/skill/build_skill.py

Reads foundations/tokens.json (the single source of truth) and foundations/fonts.css
(metric-corrected fallbacks), injects them into the templates in adapters/skill/src/,
generates references/tokens.md entirely from tokens, then GUARDS the result:

  - the retired colour law ("every ground is a white-text surface") may not appear
  - no reference to the archived tools/validate.py
  - the declared source-of-truth version must match tokens.json meta
  - every hex in nc.css must be a current token, ramp, or measured derivative
  - parity: every class the references/template name must exist in nc.css

Output: dist/skill/nightlife-culture-design/ and dist/nightlife-culture-design.skill
Stdlib only. If it does not print SKILL OK, the skill was not written.
"""
import json, re, sys, pathlib, zipfile, shutil, hashlib

def _digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()[:16]

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SRC  = HERE / "src"
OUT  = ROOT / "dist" / "skill" / "nightlife-culture-design"

T = json.load(open(ROOT / "foundations" / "tokens.json"))
SOURCE = T["meta"]["source"]                       # e.g. "Nightlife Culture Style Guide v1.4"
LAW    = T["colour"]["theLaw"]["statement"]
GROUNDS  = {k: v for k, v in T["colour"]["grounds"].items()  if isinstance(v, dict)}
ACCENTS  = {k: v for k, v in T["colour"]["accents"].items()  if isinstance(v, dict)}
CHARCOAL = T["colour"]["textColours"]["charcoal"]
RAMP     = [s for s in T["colour"]["chartRamp"]["series"]] if isinstance(T["colour"]["chartRamp"], dict) else T["colour"]["chartRamp"]
RETIRED  = T["colour"]["retired"]
SCALE    = T["type"]["sizes"]["document"]["scale"]

def law_detail():
    pairs = " · ".join(f"{k} takes {v['textOn']}" for k, v in GROUNDS.items())
    return (f"There is no single sentence covering all four grounds: {pairs}. "
            f"White on chalk is 1.11:1 and white on white is 1.00:1 — the old one-line law is retired.")

def typescale_line():
    order = ["h1", "h2", "h3", "body", "note"]
    return " · ".join(f"{r} {SCALE[r]['px']}px" for r in order if isinstance(SCALE.get(r), dict)) + \
           " (v1.4 readable sizes + Decision Book ch03; read off the sources, not chosen)"

def gen_tokens_md():
    L = ["# Tokens — generated from foundations/tokens.json. Do not edit by hand.",
         f"\n**Source:** {SOURCE}.\n",
         "## The colour law\n", f"**{LAW}**\n", law_detail() + "\n",
         "## Grounds\n", "| Token | Hex | Role | Text on it |", "|---|---|---|---|"]
    for k, v in GROUNDS.items():
        L.append(f"| {k.capitalize()} | `{v['hex']}` | {v['role']} | {v['textOn']} · {v['ratio']}:1 ({v['ratioNote']}) |")
    L += ["\n## Text colours (never grounds)\n", "| Token | Hex | Role | Measured |", "|---|---|---|---|",
          f"| Charcoal | `{CHARCOAL['hex']}` | {CHARCOAL['role']} | {CHARCOAL['ratios']['onChalk']}:1 on chalk · {CHARCOAL['ratios']['onWhite']}:1 on white |",
          "\nCharcoal was once filed under grounds; it is a text colour. Its published ratio is charcoal ON chalk.\n",
          "## Accents — surface palette, ink text, never data\n", "| Token | Hex | Role | Ink text |", "|---|---|---|---|"]
    for k, v in ACCENTS.items():
        L.append(f"| {k.capitalize()} | `{v['hex']}` | {v.get('role','')} | {v.get('ratio','')}:1 |")
    ramp_hex = [s["hex"] if isinstance(s, dict) else s for s in RAMP]
    L += ["\n## Chart ramp — the only colours that may encode data\n",
          " → ".join(f"`{h}`" for h in ramp_hex) + " · four series maximum · lightness climbs monotonically.\n",
          "## Document type scale (decided)\n", "| Role | px | em | Line height | From |", "|---|---|---|---|---|"]
    for r in ("h1", "h2", "h3", "body", "note"):
        s = SCALE.get(r)
        if isinstance(s, dict):
            L.append(f"| {r} | {s['px']} | {s['em']} | {s['lineHeight']} | {s['from']} |")
    L += ["\n## Retired — never to return\n", " · ".join(f"`{h}`" for h in RETIRED) + "\n"]
    return "\n".join(L) + "\n"

def gen_root():
    g = {k: v["hex"] for k, v in GROUNDS.items()}
    a = {k: v["hex"] for k, v in ACCENTS.items()}
    ramp_hex = [s["hex"] if isinstance(s, dict) else s for s in RAMP]
    return (":root{--blue:%s;--ink:%s;--chalk:%s;--white:%s;\n"
            "--pink:%s;--teal:%s;--violet:%s;--butter:%s;--coral:%s;\n"
            "--charcoal:%s;--hair:rgba(13,13,13,.22);\n"
            "--c1:%s;--c2:%s;--c3:%s;--c4:%s;\n"
            '--display:"Archivo Black","Archivo Black Fallback",Arial,sans-serif;\n'
            '--head:"Archivo","Archivo Fallback",Arial,sans-serif;\n'
            '--body:"Inter","Inter Fallback",Arial,-apple-system,sans-serif;}'
            ) % (g["blue"], g["ink"], g["chalk"], g["white"],
                 a["pink"], a["teal"], a["violet"], a["butter"], a["coral"],
                 CHARCOAL["hex"], *ramp_hex)

def gen_typescale_css():
    face = {"h1": "var(--head)", "h2": "var(--head)", "h3": "var(--head)",
            "body": "var(--body)", "note": "var(--body)"}
    weight = {"h1": 800, "h2": 800, "h3": 700, "body": 400, "note": 400}
    caps = {"h1": "text-transform:uppercase;letter-spacing:.01em;", "h2": "text-transform:uppercase;letter-spacing:.04em;"}
    L = ["/* ---- Document type scale — generated from foundations/tokens.json.",
         f"   {SCALE['source'].splitlines()[0][:110]}",
         "   Six roles, sizes read off v1.4 + Decision Book ch03 — not chosen here. ---- */"]
    for r in ("h1", "h2", "h3", "body", "note"):
        s = SCALE.get(r)
        if not isinstance(s, dict): continue
        L.append(f".nc-{r}{{font-family:{face[r]};font-weight:{weight[r]};font-size:{s['em']}em;"
                 f"line-height:{s['lineHeight']};{caps.get(r,'')}}}  /* {s['px']}px · {s['from']} */")
    return "\n".join(L)

# ---- slides: generated from foundations/patterns.json + the reference decks ----
def gen_slides_md():
    sys.path.insert(0, str(ROOT / "layouts"))
    from render import slide as render_slide
    P = json.load(open(ROOT / "foundations" / "patterns.json"))
    Z = T["type"]["sizes"]["slide"]["pattern"]; SP = T["space"]["slide"]
    decks = {pathlib.Path(json.load(open(f))["reference"]).name: json.load(open(f))
             for f in sorted((ROOT / "decks").glob("*.json"))}
    L = ["# Slides — generated from foundations/patterns.json. Do not edit by hand.\n",
         "Slides are built from **blocks** arranged into **patterns**. Every pattern comes from a real",
         "Nightlife Culture deck, and its reference slide is in `assets/reference/`. **Look at the",
         "reference image before you build a slide in that pattern, and match it.**\n",
         "Build slides in HTML with `assets/fonts.css` + `assets/slides.css`. Every size is in `cqw`,",
         "so the slide scales. Never set a colour or a size on a slide yourself: the ground class sets",
         "the text, title and highlight colours, and the block classes set the sizes.\n",
         "## Sizes (points on a 13.33in slide)\n",
         f"Title {Z['title']} (long titles {Z['titleFit']}) · statement {Z['statement']} · cover {Z['cover']} · "
         f"lead {Z['lead']} · heading {Z['head']} · **body {Z['body']}** · label {Z['label']} caps · "
         f"table {Z['table']['pt']}. Line height {Z['lineHeight']['text']}.\n",
         f"Side margins {SP['sideMargin']}. Title sits {SP['topMargin']['titleLeads']} from the top. "
         f"Content stops {SP['pattern']['bottom']} above the foot, or above a closing band "
         f"({SP['pattern']['closingBand']} tall).\n",
         "## Two registers\n",
         "- **Statement slides** (cover, statement): one idea, most of the canvas empty.",
         "- **Working slides** (every other pattern): a title, a lead and up to eight short text blocks.",
         "  If it does not fit at the sizes above, it is two slides. Remove copy before reducing type.\n",
         "## Grounds\n",
         "- **Blue or ink**: white titles and text, teal headings. **Chalk or white**: blue titles and headings, ink text.",
         "- Accents (pink, teal, violet, butter, coral) are rules, fills and side blocks — always with ink text,",
         "  never a whole slide.\n",
         "## Blocks\n",
         "| Block | Markup |", "|---|---|",
         "| Title | `<h2 class=\"nc-st\">` · `--fit` long · `--xl` statement · `--cover` |",
         "| Lead | `<p class=\"nc-sl\">` · `--lg` `--xl` `--2xl` bigger · `--hl` blue/teal |",
         "| Text | `<p class=\"nc-sx\">` |",
         "| Label (caps) | `<p class=\"nc-slab\">` |",
         "| Rule | `<hr class=\"nc-srule acc-pink\">` |",
         "| Spacer | `<div class=\"nc-sfill\"></div>` pushes what follows down |",
         "| Columns | `<div class=\"nc-sgrid\">` (3) · `--2` · `--4` |",
         "| Column item | `<div class=\"nc-si nc-si--rule acc-teal\">` · `--left` · `--fill`; inside: `.h` heading, `.hc` caps heading, `.big`, `.sub`, `.b` text, `.u` bold text, `ul.ls` |",
         "| Callout | `<p class=\"nc-scall acc-pink\"><b>Lead:</b> text</p>` |",
         "| Closing line | `<p class=\"nc-sline\">` · `--rule` · `--plain` |",
         "| Labelled rows | `<dl class=\"nc-srows\"><dt>..</dt><dd>..</dd></dl>` |",
         "| Panel | `<div class=\"nc-spanel acc-pink\"><p class=\"l\">..</p><p class=\"b\">..</p></div>` |",
         "| Side block | `<div class=\"nc-sside acc-pink\">` after the pad; pad takes `nc-sp--side` |",
         "| Closing band | `<div class=\"nc-sband\"><p class=\"t\">..</p></div>`; pad takes `nc-sp--band` |",
         "| Table | `<table class=\"nc-stable\">` — sent decks only, pattern `table` |",
         "| Wordmark | `<div class=\"nc-slogo\">` + the inline SVG from `assets/nightlife-culture-wordmark.svg`. Never typeset |",
         "| Slide number | `<p class=\"nc-snum\">10</p>` |",
         "\nEvery slide: `<div class=\"nc-slide\" data-pattern=\"NAME\"><div class=\"cv ground-chalk\"><div class=\"nc-sp\">…</div></div></div>`\n",
         "## Patterns\n"]
    for pid, p in P["patterns"].items():
        refs = ", ".join(f"`assets/reference/{r.split('#')[0]}/slide-{int(r.split('#')[1]):02d}.jpg`" for r in p["reference"])
        L += [f"### {p['name']} — `{pid}`\n", f"**Use when:** {p['useWhen']}  ", f"**Grounds:** {', '.join(p['grounds'])}  ",
              f"**Reference:** {refs}\n"]
        ref, n = p["reference"][0].split("#")
        ex = [s for s in decks[ref]["slides"] if str(s["n"]).rstrip("ab") == n][0]
        mk = render_slide(ex)
        mk = re.sub(r"<svg.*?</svg>", "<!-- inline assets/nightlife-culture-wordmark.svg -->", mk, flags=re.S)
        mk = mk.replace("><", ">\n<")
        L += ["```html", mk, "```\n"]
    L += ["## When nothing fits\n",
          "Compose the slide from the blocks above and say which pattern is new. The design system adds",
          "it to `foundations/patterns.json` with the live slide it came from. Never invent a size, a colour",
          "or a spacing value; if a block is missing, say so.\n",
          "## Diagrams — not yet specified\n",
          "No diagram kit exists. Build process chains and timelines from columns, rules and panels. Never",
          "use PowerPoint SmartArt defaults.\n"]
    return "\n".join(L)

def gen_slides_css():
    """slides.css for the skill: the --nc- tokens, grounds and accent modifiers from the
    component layer, then the slide layer. Self-contained with fonts.css."""
    comp = (ROOT / "foundations" / "nightlife-culture.css").read_text()
    root = re.search(r":root\{.*?\n\}", comp, re.S).group(0)
    lines = [l for l in comp.splitlines() if re.match(r"\.(ground|acc)-[a-z]+\{", l)]
    slides = (ROOT / "foundations" / "nightlife-slides.css").read_text()
    return (f"/* nc-build-stamp tokens:{_digest(ROOT / 'foundations' / 'tokens.json')}\n"
            "   Nightlife Culture slide stylesheet for the skill — GENERATED by adapters/skill/build_skill.py\n"
            "   from foundations/. Pair with fonts.css. */\n" + root + "\n" + "\n".join(lines) + "\n" + slides)

def main():
    # overwrite in place — some checkouts (and the Cowork mount) forbid deletes
    for d in ("references", "assets", "scripts"):
        (OUT / d).mkdir(parents=True, exist_ok=True)

    # references: four static + generated tokens.md
    for n in ("components.md", "charts.md", "voice.md"):
        shutil.copy(SRC / "references" / n, OUT / "references" / n)
    (OUT / "references" / "tokens.md").write_text(gen_tokens_md())
    (OUT / "references" / "slides.md").write_text(gen_slides_md())
    (OUT / "assets" / "slides.css").write_text(gen_slides_css())
    for img in sorted((ROOT / "reference").glob("*/slide-*.jpg")):
        d = OUT / "assets" / "reference" / img.parent.name; d.mkdir(parents=True, exist_ok=True)
        shutil.copy(img, d / img.name)

    # SKILL.md
    s = (SRC / "SKILL.md").read_text()
    s = (s.replace("{{LAW}}", LAW).replace("{{LAW_DETAIL}}", law_detail())
          .replace("{{SOURCE}}", f"{SOURCE} (August 2026)").replace("{{TYPESCALE_LINE}}", typescale_line()))
    (OUT / "SKILL.md").write_text(s)

    # nc.css from template
    css = (SRC / "nc.css.tmpl").read_text()
    stamp_css = f"nc-build-stamp tokens:{_digest(ROOT / 'foundations' / 'tokens.json')}"
    header = (f"/* {stamp_css}\n   Nightlife Culture component stylesheet — GENERATED from foundations/tokens.json\n"
              f"   by adapters/skill/build_skill.py. Source: {SOURCE}. Do not edit by hand;\n"
              "   edit tokens or adapters/skill/src/nc.css.tmpl and rebuild. Pair with fonts.css. */")
    css = css.replace("{{HEADER}}", header).replace("{{TOKENS_ROOT}}", gen_root()).replace("{{TYPESCALE}}", gen_typescale_css())
    (OUT / "assets" / "nc.css").write_text(css)

    # fonts + template + scripts — the template is a source fragment (template.part.html);
    # the emitted copy carries a build stamp so checks/check_stamps.py can date it.
    shutil.copy(ROOT / "foundations" / "fonts.css", OUT / "assets" / "fonts.css")
    stamp = f"tokens:{_digest(ROOT / 'foundations' / 'tokens.json')};fonts:{_digest(ROOT / 'foundations' / 'fonts.css')}"
    tpl = (SRC / "template.part.html").read_text()
    tpl = tpl.replace('<meta charset="utf-8">', f'<meta charset="utf-8">\n<meta name="nc-build-stamp" content="{stamp}">', 1)
    (OUT / "assets" / "template.html").write_text(tpl)
    shutil.copy(SRC / "scripts" / "contrast.py", OUT / "scripts" / "contrast.py")
    shutil.copy(ROOT / "assets" / "logo" / "nightlife-culture-wordmark.svg",
                OUT / "assets" / "nightlife-culture-wordmark.svg")
    shutil.copy(SRC / "parity_check.py", OUT / "scripts" / "parity_check.py")

    # ---- guards ----
    fail = []
    all_text = {p: p.read_text() for p in OUT.rglob("*") if p.is_file() and p.suffix in (".md", ".css", ".html", ".py")}
    for p, txt in all_text.items():
        if "fonts.css" in p.name: continue
        if re.search(r"every ground is a white-text surface", txt, re.I) and "retired" not in txt[:max(0,txt.lower().find("every ground"))].lower()[-200:]:
            # allowed only where explicitly marked as the retired sentence
            for mm in re.finditer(r"every ground is a white-text surface", txt, re.I):
                ctx = txt[max(0, mm.start()-160):mm.start()].lower()
                if "retired" not in ctx and "old" not in ctx and "false" not in ctx and "supersede" not in ctx:
                    fail.append(f"RETIRED LAW stated as current in {p.relative_to(OUT)}")
        if re.search(r"(?i)>\s*nightlife\s*<br\s*/?>\s*culture", txt) or \
           re.search(r"\.logo\b[^}]*\{[^}]*font-family", txt):
            fail.append(f"live-type wordmark in {p.relative_to(OUT)} — the logo is a placed SVG (LOGO.md)")
        if "tools/validate.py" in txt:
            fail.append(f"stale tools/validate.py reference in {p.relative_to(OUT)}")
    skill_md = all_text[OUT / "SKILL.md"]
    ver = re.search(r"v1\.\d", SOURCE).group()
    if ver not in skill_md: fail.append(f"SKILL.md does not declare {ver}")
    if re.search(r"Style Guide v1\.[0-3]", skill_md): fail.append("SKILL.md names a superseded guide version")
    # hex audit on nc.css
    allowed = {v["hex"].upper() for v in GROUNDS.values()} | {v["hex"].upper() for v in ACCENTS.values()} \
              | {CHARCOAL["hex"].upper()} | {(s["hex"] if isinstance(s, dict) else s).upper() for s in RAMP} | {"#FFF", "#FFFFFF"}
    for h in set(re.findall(r"#[0-9A-Fa-f]{3,6}\b", all_text[OUT / "assets" / "nc.css"])):
        if h.upper() not in allowed: fail.append(f"nc.css contains non-token colour {h}")
    for h in RETIRED:
        for p, txt in all_text.items():
            if h.lower() in txt.lower() and p.suffix in (".css", ".html"):
                fail.append(f"retired colour {h} in {p.relative_to(OUT)}")
    # parity
    import subprocess
    both = OUT.parent / "_parity.css"
    both.write_text(all_text[OUT / "assets" / "nc.css"] + "\n" + all_text[OUT / "assets" / "slides.css"])
    r = subprocess.run([sys.executable, str(OUT / "scripts" / "parity_check.py"), str(both),
                        *[str(OUT / "references" / n) for n in ("components.md", "charts.md", "slides.md", "tokens.md")],
                        str(OUT / "assets" / "template.html")], capture_output=True, text=True)
    print(r.stdout.strip()); both.unlink()
    if r.returncode: fail.append("parity check failed")

    if fail:
        print("\n".join("  !! " + f for f in fail)); print("SKILL FAILED"); return 1
    # zip
    zp = ROOT / "dist" / "nightlife-culture-design.skill"
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(OUT.rglob("*")):
            if p.is_file(): z.write(p, "nightlife-culture-design/" + str(p.relative_to(OUT)))
    print(f"SKILL OK — {zp.relative_to(ROOT)} · {zp.stat().st_size//1024}KB")
    return 0

if __name__ == "__main__":
    sys.exit(main())
