#!/usr/bin/env python3
"""Build the component library page, in two forms.

  components/index.html   LINKS ../foundations/*.css — no snapshot, always current
  dist/component-library.html   embeds everything, for sending to someone

Both carry an nc-build-stamp naming the digest of every source they were built
from, so checks/check_stamps.py can fail on divergence (ch18). The linked form
cannot go stale by construction; the dist form can, which is why it is stamped.

Content lives in components/library.body.html — edit that, not this script.

    python3 components/build_library.py
"""
import hashlib, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
F = ROOT / "foundations"
def d(p): return hashlib.sha256(p.read_bytes()).hexdigest()[:16]

body     = (ROOT / "components" / "library.body.html").read_text()

# ---- the type roles, generated from the same tokens as the stylesheet --------
# The table under "02 · Type" is not typed: it is built from tokens.json
# type.roles, which is also what checks/build.py generates the CSS from. If a
# role changes, the specimen, the stylesheet and the Word style name change
# together or not at all (v1.5, 5 Oct 2026).
import json as _json
_T = _json.loads((F / "tokens.json").read_text())
_V = {k: v for k, v in _T["type"]["voices"].items() if isinstance(v, dict)}
_S = {k: v for k, v in _T["type"]["steps"].items() if isinstance(v, dict)}
_R = {k: v for k, v in _T["type"]["roles"].items() if isinstance(v, dict)}
_FACE = {"display": "Archivo Black", "head": "Archivo", "body": "Inter"}
_WT = {400: "Regular", 600: "SemiBold", 700: "Bold", 800: "ExtraBold"}


def _voice_line(k):
    v = _V[k]
    face = _FACE[v["face"]] + ("" if v["face"] == "display" else " " + _WT[v["weight"]])
    case = {"upper": "capitals", "sentence": "sentence case"}[v["case"]]
    return f"{k.capitalize()} voice · {face}, {case}" + (", spaced" if k == "label" else "")


def _sample(name, r):
    label = name.replace("-", " ").capitalize()
    st = ""
    if name == "display": st = ' style="background:var(--nc-blue);padding:.2rem .5rem"'
    elif name == "button": st = ' style="background:var(--nc-blue);padding:.3rem .8rem;border-radius:999px"'
    elif r["colour"] == "white": st = ' style="background:var(--nc-ink);padding:.15rem .4rem"'
    return f'<span class="nc-{name}"{st}>{label}</span>'


def roles_table():
    out = ['<div class="nc-table-scroll"><table class="nc-table">',
           '<caption class="nc-table-title">Table 0 · Every text style, under the voice it inherits · generated from tokens.json</caption>',
           '<thead><tr><th scope="col">Style</th><th scope="col">Looks like</th><th scope="col" class="nc-figure-cell">Size</th>'
           '<th scope="col">What it is for</th><th scope="col">In Word</th></tr></thead>']
    cur = None
    for name, r in _R.items():
        if r["voice"] != cur:
            cur = r["voice"]
            if cur != "display" or True:
                out.append(f'<tbody><tr><th colspan="5" scope="rowgroup" class="nc-label" style="padding-left:var(--nc-sp3);background:var(--nc-white)">{_h.escape(_voice_line(cur))}</th></tr>')
        st = _S.get(str(r["step"]))
        size = "Set to the cover" if st is None else f"{st['px']}px · {st['pt']}pt"
        el = r.get("element") or "—"
        out.append(f'<tr><th scope="row">nc-{name}</th><td style="white-space:nowrap">{_sample(name, r)}</td>'
                   f'<td class="nc-figure-cell">{size}</td><td>{_h.escape(r["use"])}' + (f' · <span class="nc-small">on {el}</span>' if r.get("element") else "") + f'</td><td>{_h.escape(r["word"])}</td></tr>')
    out.append("</tbody></table></div>")
    out.append('<p class="nc-small">' + " · ".join(f"<strong>{_voice_line(k).split(' voice')[0]}</strong>: {_h.escape(_V[k]['use'])}" for k in _V) + "</p>")
    return "\n".join(out)


# ---- the markup disclosure, and where the styling came from ---------------
# Under every specimen: the markup that produced it, read off the rendered
# block; then, for every class in it, the file, line and section that DEFINES
# it and the generator that wrote that file. Typed markup is a claim. Read
# markup with a resolved definition site is evidence.
#
# Anything the specimen styles from inside its own markup is flagged, because
# that is the one thing a specimen cannot do and still be the component.
import html as _h, re as _re, sys as _sys, pathlib as _pl
_sys.path.insert(0, str(ROOT / "components"))
import provenance as _pv

_IDX = _pv.index()
_WORD = {"red": "Flagged", "amber": "Noted", "grey": "Data"}


def _short(section):
    return (section.split("—")[0].split("(")[0].strip() or "unsectioned")


def _prov_table(classes):
    rows = []
    for c in classes:
        where = _IDX.get(c)
        if not where:
            rows.append(f"<tr><td><code>.{c}</code></td>"
                        "<td colspan=\"3\">Not defined in the generated layer</td></tr>")
            continue
        w = where[0]
        rows.append(
            f"<tr><td><code>.{c}</code></td>"
            f"<td>{_h.escape(w['file'])} <span class=\"at\">line {w['line']}</span></td>"
            f"<td>{_h.escape(_short(w['section']))}</td>"
            f"<td>{_h.escape(w['made'])}</td></tr>")
    return ('<table class="nc-table nc-origin"><thead><tr><th>Class</th>'
            "<th>Defined in</th><th>Section</th><th>That file is generated by</th>"
            f"</tr></thead><tbody>{''.join(rows)}</tbody></table>")


def _flag_list(findings):
    if not findings:
        return ('<p class="nc-note">Nothing is styled inside this specimen. '
                "Every value it renders comes from the generated stylesheet.</p>")
    order = {"red": 0, "amber": 1, "grey": 2}
    import collections as _c
    grouped = _c.Counter(findings)          # the same fault six times is one fault
    items = "".join(
        f'<li class="nc-flag nc-flag--{sev}"><span class="tag">{_WORD[sev]}</span>'
        f"<span><code>{_h.escape(prop)}</code> — {_h.escape(why)}</span>"
        + (f'<span class="n">&times;{k}</span>' if k > 1 else "")
        + "</li>"
        for (sev, prop, why), k in sorted(grouped.items(), key=lambda f: order[f[0][0]]))
    return f'<ul class="nc-flags">{items}</ul>'


def _disclose(src):
    out, i, n, red_total, spec_flagged = [], 0, 0, 0, 0
    for m in _re.finditer(r'<div class="nc-specimen[^"]*"[^>]*>', src):
        depth, j = 0, m.start()
        while j < len(src):
            t = _re.compile(r"</?div\b").search(src, j)
            if not t:
                break
            depth += 1 if src[t.start():t.start() + 4] == "<div" else -1
            j = t.end()
            if depth == 0:
                break
        if j >= len(src):
            continue                      # unbalanced, leave it alone
        block = src[m.start():j + 1]
        inner = block[block.index(">") + 1:block.rindex("</div>")].strip()
        lines = [l for l in inner.split("\n")]
        pad = min((len(l) - len(l.lstrip()) for l in lines if l.strip()), default=0)
        inner = "\n".join(l[pad:] if l[:pad].isspace() else l for l in lines)

        classes, findings = _pv.audit(inner, _IDX)
        red = [f for f in findings if f[0] == "red"]
        red_total += len(red)
        spec_flagged += 1 if red else 0
        n += 1

        _cl = f"{len(classes)} class" + ("" if len(classes) == 1 else "es")
        verdict = (f"{_cl}, every one from the generated stylesheet" if not red else
                   f"{_cl} · {len(red)} flagged — styled inside this specimen")
        det = ('\n<details class="nc-details nc-disclose">'
               f"<summary>Where this came from — {verdict}</summary>"
               f'<pre class="nc-pre acc-teal"><code class="nc-code">{_h.escape(inner)}</code></pre>'
               + _prov_table(classes)
               + '<p class="nc-note">The markup above was read off the rendered specimen by '
                 "the build, not written by hand. Every file in the table is generated from "
                 "foundations/tokens.json — edit a token, rebuild, and this specimen changes. "
                 "If it does not change, it was not built from the codebase.</p>"
               + _flag_list(findings)
               + "</details>")
        out.append(src[i:j + 1] + det)
        i = j + 1
    out.append(src[i:])
    return "".join(out), n, red_total, spec_flagged


body = body.replace("<!-- NC:ROLES -->", roles_table(), 1)
body, _n, _red, _sf = _disclose(body)
print(f"provenance disclosed under {_n} specimens — "
      f"{_red} things flagged across {_sf} of them")
css      = (F / "nightlife-culture.css")
fonts    = (F / "fonts.css")

import sys
sys.path.insert(0, str(ROOT / "docs"))
from sheet import page

page(name="index", folder="components",
     kicker="Nightlife Culture · design system",
     title="The component library",
     stand="Every component in the system, one specimen each, with the rule that governs it "
           "and where it came from. Nothing here is drawn to look like a component — each is "
           "the component.",
     body=body)
page(name="component-library", folder="dist",
     kicker="Nightlife Culture · design system",
     title="The component library",
     stand="Every component in the system, one specimen each, with the rule that governs it "
           "and where it came from.",
     body=body)
