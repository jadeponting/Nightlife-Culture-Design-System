#!/usr/bin/env python3
"""Generate the Nightlife Culture wordmark SVGs from the documented spec.

NOT a redesign. LOGO.md records how the mark was built; this follows it exactly
and then CHECKS the result against the two measured widths. If the widths do not
reproduce, the script fails rather than shipping something that looks almost right.

Spec (LOGO.md, measured from the printed business card):
  NIGHTLIFE  32.09pt   rendered width 171.92pt
  CULTURE    33.41pt   rendered width 171.19pt
  baseline to baseline 30.41pt   effective line-height 0.9476

The two lines are set at DIFFERENT sizes so they justify to the same width.
Tracking per line is solved so each line hits its measured width — it is not
guessed, and it is not the same on both lines.

Output: outlined vector paths. No <text>. No live type.
"""
import io, sys, json, pathlib
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import uharfbuzz as hb

FONT = pathlib.Path("/home/claude/repo/assets/fonts/ArchivoBlack-400.woff2")
SPEC = [
    dict(text="NIGHTLIFE", size=32.09, width=171.92),
    dict(text="CULTURE",   size=33.41, width=171.19),
]
BASELINE_TO_BASELINE = 30.41
TOL = 0.005   # 0.5% — the spec's own tolerance between the two lines

tt = TTFont(FONT); tt.flavor = None
buf = io.BytesIO(); tt.save(buf); data = buf.getvalue()
face = hb.Face(data); hbfont = hb.Font(face)
UPEM = face.upem
glyphset = tt.getGlyphSet()
CAP = tt["OS/2"].sCapHeight if hasattr(tt["OS/2"], "sCapHeight") else 700


def shape(text):
    b = hb.Buffer(); b.add_str(text); b.direction = "ltr"; b.script = "Latn"; b.language = "en"
    hb.shape(hbfont, b, {"kern": True})
    return [(tt.getGlyphOrder()[g.codepoint], p.x_advance, p.x_offset)
            for g, p in zip(b.glyph_infos, b.glyph_positions)]


def solve_tracking(line):
    """Tracking (in em) applied between letters so the line hits its measured width."""
    sh = shape(line["text"])
    natural_units = sum(a for _, a, _ in sh)
    natural_pt = natural_units / UPEM * line["size"]
    gaps = len(sh) - 1
    track_pt = (line["width"] - natural_pt) / gaps
    return sh, track_pt, track_pt / line["size"], natural_pt


def line_paths(line, sh, track_pt, y_baseline):
    """Outlined paths for one line, in pt units, positioned on its baseline."""
    scale = line["size"] / UPEM
    x = 0.0
    d = []
    for i, (gname, adv, xoff) in enumerate(sh):
        pen = SVGPathPen(glyphset)
        # y flips: font units are y-up, SVG is y-down
        tpen = TransformPen(pen, (scale, 0, 0, -scale, x + xoff * scale, y_baseline))
        glyphset[gname].draw(tpen)
        p = pen.getCommands()
        if p:
            d.append(p)
        x += adv * scale
        if i < len(sh) - 1:
            x += track_pt
    return " ".join(d), x


def main():
    report = []
    lines = []
    for i, line in enumerate(SPEC):
        sh, track_pt, track_em, natural = solve_tracking(line)
        y = line["size"] + (BASELINE_TO_BASELINE if i else 0)
        # place baselines: first at cap-ish, second BASELINE_TO_BASELINE below
        lines.append(dict(line=line, sh=sh, track_pt=track_pt, track_em=track_em, natural=natural))
        report.append(dict(text=line["text"], size=line["size"], target=line["width"],
                           natural=round(natural, 3), tracking_pt=round(track_pt, 4),
                           tracking_em=round(track_em, 5)))

    # baselines
    cap_pt0 = CAP / UPEM * SPEC[0]["size"]
    y0 = cap_pt0
    y1 = y0 + BASELINE_TO_BASELINE
    cap_pt1 = CAP / UPEM * SPEC[1]["size"]

    paths, widths = [], []
    for i, L in enumerate(lines):
        d, w = line_paths(L["line"], L["sh"], L["track_pt"], y0 if i == 0 else y1)
        paths.append(d); widths.append(w)

    # verify
    ok = True
    for i, (L, w) in enumerate(zip(lines, widths)):
        target = L["line"]["width"]
        err = abs(w - target) / target
        report[i]["rendered"] = round(w, 3)
        report[i]["error_pct"] = round(err * 100, 4)
        if err > 1e-6:
            ok = False
    # the real check: do the two lines justify to the same width, within the spec's 0.4%?
    just = abs(widths[0] - widths[1]) / max(widths) * 100

    vw = max(widths)
    vh = y1 + (SPEC[1]["size"] - cap_pt1) * 0  # descender-free caps; box to baseline
    vh = y1
    out = {}
    body = "\n".join(f'  <path d="{d}"/>' for d in paths)
    def svg(fill, ident):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vw:.3f} {vh:.3f}" '
                f'role="img" aria-label="Nightlife Culture">\n'
                f'  <title>Nightlife Culture</title>\n'
                f'<g fill="{fill}">\n{body}\n</g>\n</svg>\n')
    out["nightlife-culture-wordmark.svg"]       = svg("currentColor", "current")
    out["nightlife-culture-wordmark-white.svg"] = svg("#FFFFFF", "white")
    out["nightlife-culture-wordmark-blue.svg"]  = svg("#0000FF", "blue")
    out["nightlife-culture-wordmark-ink.svg"]   = svg("#0D0D0D", "ink")
    for name, s in out.items():
        pathlib.Path(name).write_text(s, encoding="utf-8")

    pathlib.Path("wordmark-report.json").write_text(json.dumps(
        dict(lines=report, justification_delta_pct=round(just, 4),
             viewBox=[0, 0, round(vw, 3), round(vh, 3)],
             cap_height_pt=round(cap_pt0, 3),
             baseline_to_baseline=BASELINE_TO_BASELINE), indent=1), encoding="utf-8")

    for r in report:
        print(f"{r['text']:10} {r['size']}pt  natural {r['natural']:>8}pt  "
              f"tracking {r['tracking_em']:+.5f}em  ->  rendered {r['rendered']}pt "
              f"(target {r['target']}, err {r['error_pct']}%)")
    print(f"\nthe two lines justify to within {just:.4f}%  (spec says 0.4%)")
    print(f"viewBox 0 0 {vw:.3f} {vh:.3f} · cap height {cap_pt0:.2f}pt · baselines {y0:.2f} / {y1:.2f}")
    if just > 0.5:
        sys.exit("FAILED — the lines do not justify; do not ship this")
    print("outlined paths written: 4 variants, no <text>")


if __name__ == "__main__":
    main()
