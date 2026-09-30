"""Render a slide from blocks. One renderer for every deck and the pattern sheet.

A slide is data:

    {"pattern": "three-columns", "ground": "chalk", "pad": "side|band|cover",
     "blocks": [...], "side": {...}, "band": {...}, "number": "10"}

Blocks, in the order they sit on the slide:

    {"title": "...", "size": "fit|xl|cover"}     {"lead": "...", "size": "lg|xl|2xl", "hl": true}
    {"text": "..."}      {"label": "..."}         {"meta": "..."}
    {"rule": "pink|teal|blue|white"}              {"fill": true}   (a spacer)
    {"cols": 2|3|4, "items": [{"mark": "rule|left|fill", "acc": "teal",
                               "parts": [["h"|"hc"|"big"|"sub"|"b"|"u", "..."], ["ls", [...]]]}]}
    {"callout": "...", "lead": "Working hypothesis:", "acc": "pink"}
    {"line": "...", "rule": true, "plain": true}
    {"rows": [["Label", "Description"], ...]}
    {"panel": ["Label", "Text"], "acc": "pink"}
    {"table": {"head": [...], "num": [2, 3], "rows": [[...]], "foot": [...]}}
    {"logo": "cover"}

Classes come from foundations/nightlife-slides.css and nothing else: a slide
has nowhere to put a colour or a size of its own.
"""
import html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
_svg = (ROOT / "assets" / "logo" / "nightlife-culture-wordmark.svg").read_text()
WORDMARK = _svg[_svg.index("<svg"):].strip()


def esc(s):
    return html.escape(s, quote=False).replace("&lt;br&gt;", "<br>")


def acc(a):
    return f" acc-{a}" if a and a != "white" else ""


def logo(kind=""):
    k = f" nc-slogo--{kind}" if kind else ""
    return f'<div class="nc-slogo{k}">{WORDMARK}</div>'


def part(kind, val):
    if kind == "ls":
        return '<ul class="ls">' + "".join(f"<li>{esc(v)}</li>" for v in val) + "</ul>"
    return f'<p class="{kind}">{esc(val)}</p>'


def item(it):
    mark = f" nc-si--{it['mark']}" if it.get("mark") else ""
    body = "".join(part(k, v) for k, v in it["parts"])
    return f'<div class="nc-si{mark}{acc(it.get("acc"))}">{body}</div>'


def block(b):
    if "title" in b:
        s = f" nc-st--{b['size']}" if b.get("size") else ""
        return f'<h2 class="nc-st{s}">{esc(b["title"])}</h2>'
    if "lead" in b and "callout" not in b:
        s = f" nc-sl--{b['size']}" if b.get("size") else ""
        h = " nc-sl--hl" if b.get("hl") else ""
        return f'<p class="nc-sl{s}{h}">{esc(b["lead"])}</p>'
    if "text" in b:
        return f'<p class="nc-sx">{esc(b["text"])}</p>'
    if "label" in b:
        return f'<p class="nc-slab">{esc(b["label"])}</p>'
    if "meta" in b:
        return f'<p class="nc-smeta">{esc(b["meta"])}</p>'
    if "rule" in b and "line" not in b:
        return f'<hr class="nc-srule{acc(b["rule"])}">'
    if "fill" in b:
        return '<div class="nc-sfill" aria-hidden="true"></div>'
    if "cols" in b:
        n = b["cols"]
        g = "" if n == 3 else f" nc-sgrid--{n}"
        return f'<div class="nc-sgrid{g}">' + "".join(item(i) for i in b["items"]) + "</div>"
    if "callout" in b:
        lead = f'<b>{esc(b["lead"])}</b> ' if b.get("lead") else ""
        return f'<p class="nc-scall{acc(b.get("acc"))}">{lead}{esc(b["callout"])}</p>'
    if "line" in b:
        m = (" nc-sline--rule" if b.get("rule") else "") + (" nc-sline--plain" if b.get("plain") else "")
        return f'<p class="nc-sline{m}{acc(b.get("acc"))}">{esc(b["line"])}</p>'
    if "rows" in b:
        return '<dl class="nc-srows">' + "".join(
            f"<dt>{esc(a)}</dt><dd>{esc(d)}</dd>" for a, d in b["rows"]) + "</dl>"
    if "panel" in b:
        l, t = b["panel"]
        return (f'<div class="nc-spanel{acc(b.get("acc"))}"><p class="l">{esc(l)}</p>'
                f'<p class="b">{esc(t)}</p></div>')
    if "table" in b:
        t = b["table"]; num = set(t.get("num", []))
        cl = lambda i: ' class="num"' if i in num else ""
        head = "".join(f"<th{cl(i)} scope=\"col\">{esc(h)}</th>" for i, h in enumerate(t["head"]))
        rows = "".join("<tr>" + "".join(f"<td{cl(i)}>{esc(c)}</td>" for i, c in enumerate(r)) + "</tr>"
                       for r in t["rows"])
        foot = ("<tfoot><tr>" + "".join(f"<td{cl(i)}>{esc(c)}</td>" for i, c in enumerate(t["foot"]))
                + "</tr></tfoot>") if t.get("foot") else ""
        return f'<table class="nc-stable"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody>{foot}</table>'
    if "logo" in b:
        return logo(b["logo"])
    raise ValueError(f"unknown block: {b}")


def slide(s):
    pad = f" nc-sp--{s['pad']}" if s.get("pad") else ""
    out = [f'<div class="nc-slide" data-pattern="{s["pattern"]}"><div class="cv ground-{s["ground"]}">',
           f'<div class="nc-sp{pad}">' + "".join(block(b) for b in s["blocks"]) + "</div>"]
    if s.get("side"):
        sd = s["side"]
        out.append(f'<div class="nc-sside{acc(sd.get("acc"))}">'
                   + "".join(part(k, v) for k, v in sd["parts"]) + "</div>")
    if s.get("band"):
        bd = s["band"]
        t = " t--plain" if bd.get("plain") else ""
        num = f'<p class="nc-snum">{esc(s["number"])}</p>' if s.get("number") else ""
        out.append(f'<div class="nc-sband"><p class="t{t}">{esc(bd["text"])}</p>'
                   + (logo() if bd.get("logo") else "") + num + "</div>")
    elif s.get("number"):
        out.append(f'<p class="nc-snum">{esc(s["number"])}</p>')
    out.append("</div></div>")
    return "".join(out)
