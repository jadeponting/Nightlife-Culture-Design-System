"""One page builder. Every sheet in the system is made here.

NC-PAG-02 — page furniture is a component, not something each sheet writes for
itself. Before this existed there were five hand-written stylesheets across four
sheets, none governed and none checked, and the masthead ground had been picked
by eye five times. A sheet cannot pick anything by eye now, because a sheet no
longer has anywhere to put a choice.

    from sheet import page
    page(name="what-we-have", title="...", kicker="...", stand="...", body=...)

Writes two forms, the same way the rest of the system does:
    docs/<name>.html    links foundations/ — cannot carry a stale copy
    dist/<name>.html    self-contained, for sending
"""
import hashlib, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
F = ROOT / "foundations"
SHEETS = {}          # name -> where the linked form lives, for the coverage check


def _dig(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def _stamp():
    parts = [("tokens", F / "tokens.json"), ("rules", F / "rules.json"),
             ("css", F / "nightlife-culture.css"), ("fonts", F / "fonts.css"),
             ("slides", F / "nightlife-slides.css")]
    return ";".join(f"{k}:{_dig(p)}" for k, p in parts if p.exists())


HEAD = """<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — Nightlife Culture</title>
<meta name="nc-source" content="Nightlife Culture Style Guide v1.4.1">
<meta name="nc-build-stamp" content="{stamp}">
{styles}
</head><body class="nc-doc">
<header class="nc-mast{night}">
  <div class="nc-wrap{measure}">
    <p class="nc-kick">{kicker}</p>
    <h1>{title}</h1>
    <p class="stand">{stand}</p>
  </div>
</header>
<div class="nc-wrap{measure}">
{body}
</div>
</body></html>
"""


def page(*, name, title, kicker, stand, body, folder="docs", extra_css=""):
    """Build one sheet. There is no ground choice: a masthead is the primary
    brand colour, and a sheet has nowhere to put a preference (NC-PAG-01)."""
    styles_linked = (
        f'<link rel="stylesheet" href="{"../" if folder != "." else ""}foundations/fonts.css">\n'
        f'<link rel="stylesheet" href="{"../" if folder != "." else ""}foundations/nightlife-culture.css">\n'
        f'<link rel="stylesheet" href="{"../" if folder != "." else ""}foundations/nightlife-slides.css">')
    inline = "\n".join((F / f).read_text() for f in
                       ("fonts.css", "nightlife-culture.css", "nightlife-slides.css")
                       if (F / f).exists())
    common = dict(title=title, kicker=kicker, stand=stand, body=body,
                  stamp=_stamp(), measure="", night="")

    out = ROOT / folder / f"{name}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(HEAD.format(styles=styles_linked + (
        f"\n<style>{extra_css}</style>" if extra_css else ""), **common))

    (ROOT / "dist").mkdir(exist_ok=True)
    (ROOT / "dist" / f"{name}.html").write_text(
        HEAD.format(styles=f"<style>\n{inline}\n{extra_css}\n</style>", **common))

    SHEETS[name] = out
    return out
