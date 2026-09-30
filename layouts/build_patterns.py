#!/usr/bin/env python3
"""Build the slide pattern sheet — the visual guide to slides.

    layouts/slide-patterns.html   links foundations/
    dist/slide-patterns.html      self-contained

Every pattern in foundations/patterns.json, shown the only way that counts:
the live reference slide it came from, beside the system's rebuild of it,
rendered from the same blocks every deck uses. If the two drift apart, it is
visible on this page.
"""
import base64, html, json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "layouts")); sys.path.insert(0, str(ROOT / "docs"))
from render import slide
from sheet import page

P = json.loads((ROOT / "foundations" / "patterns.json").read_text())
decks = {}
for f in (ROOT / "decks").glob("*.json"):
    d = json.loads(f.read_text())
    decks[pathlib.Path(d["reference"]).name] = d

def ref_img(ref, n):
    p = ROOT / "reference" / ref / f"slide-{int(n):02d}.jpg"
    b = base64.b64encode(p.read_bytes()).decode()
    return f'<img src="data:image/jpeg;base64,{b}" alt="Reference slide {n}, {ref}">'

def rebuilt(ref, n):
    d = decks[ref]
    return [s for s in d["slides"] if str(s["n"]).rstrip("ab") == str(n)]

out, missing = [], []
for i, (pid, p) in enumerate(P["patterns"].items(), 1):
    pairs = []
    for r in p["reference"]:
        ref, n = r.split("#")
        mine = rebuilt(ref, n)
        if not mine:
            missing.append(r); continue
        sys_html = "".join(slide(s) for s in mine)
        pairs.append(f'<div class="nc-spair"><figure>{ref_img(ref, n)}<figcaption>Live slide · {html.escape(ref)} #{n}</figcaption></figure>'
                     f'<figure>{sys_html}<figcaption>Built by the system</figcaption></figure></div>')
    grounds = " · ".join(p["grounds"])
    out.append(f'''<section>
<h2 class="nc-section-head"><span class="num">{i:02d}</span><span class="ttl">{html.escape(p["name"])}</span></h2>
<p class="nc-stand">{html.escape(p["useWhen"])}</p>
<p class="nc-note">Grounds: {grounds} · pattern name: <code class="nc-code">{pid}</code></p>
{"".join(pairs)}
</section>''')

steps = [x.strip() for x in re.split(r"\s*\d\.\s", P["meta"]["howToGrow"]) if x.strip()]
grow = "".join(f"<li>{html.escape(x)}</li>" for x in steps)
body = "".join(out) + f'''<section>
<h2 class="nc-section-head"><span class="ttl">How the patterns grow</span></h2>
<ol class="nc-list nc-list--num">{grow}</ol>
</section>'''

page(name="slide-patterns", folder="layouts", title="Slide patterns",
     kicker="Nightlife Culture · design system",
     stand="Every slide pattern the system knows. Each one is shown beside the live slide it came from.",
     body=body)
print(f"wrote layouts/slide-patterns.html   {len(P['patterns'])} patterns · dist/slide-patterns.html")
if missing:
    print("  !! reference slides with no rebuild:", missing); sys.exit(1)
