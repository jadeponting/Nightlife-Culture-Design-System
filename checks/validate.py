#!/usr/bin/env python3
"""Validate an NC artefact against foundations/rules.json. Stdlib only.

    python3 checks/validate.py FILE.html [FILE.html ...]

Checks the machine-checkable Fixed rules. Exit 1 on any Fixed breach.
For .docx/.pptx/.xlsx use the Decision Book's inspect_docx.py — this covers
HTML and CSS, which is where the design system is authored.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
RULES = {r["id"]: r for r in json.loads((ROOT/"foundations"/"rules.json").read_text())["rules"]}
HEX = json.loads((ROOT/"checks"/"allowed-hex.json").read_text())
ALLOWED, RETIRED = set(HEX["allowed"]), {h.upper() for h in HEX["retired"]}
RETIRED_FONTS = {"aptos"}

def strip(html, tag):
    return re.sub(rf"<{tag}[^>]*>.*?</{tag}>", " ", html, flags=re.S|re.I)

def check(path):
    h = path.read_text(errors="replace")
    body = strip(strip(h, "style"), "script")
    text = re.sub(r"<[^>]+>", " ", body)
    F, W = [], []

    # The CSS rules below scan declaration blocks. Scanning the WHOLE file for
    # them is quadratic on a brace-free document — a 200KB page with no <style>
    # made the pattern backtrack for sixteen seconds and find nothing. Pull the
    # stylesheet out once: embedded <style> blocks, or the linked files if the
    # page links them, which is also the only place these rules actually apply.
    css = " ".join(re.findall(r"<style[^>]*>(.*?)</style>", h, flags=re.S))
    if "{" not in css:
        for href in re.findall(r'<link[^>]+href="([^"]+\.css)"', h):
            f = (path.parent / href).resolve()
            if f.exists() and ROOT in f.parents:
                css += "\n" + f.read_text(errors="replace")
    css_nc = re.sub(r"/\*.*?\*/", " ", css, flags=re.S)   # comments would be read as selectors
    blocks = re.findall(r"([^{}]+)\{([^{}]*)\}", css_nc) if "{" in css_nc else []

    # NC-COL-06 / NC-COL-05 — colour allowlist and retirements
    used = {m.upper() for m in re.findall(r"#[0-9A-Fa-f]{6}\b", h)}
    for x in sorted(used & RETIRED):
        F.append(("NC-COL-05", f"retired colour {x} present"))
    for x in sorted(used - ALLOWED - RETIRED):
        F.append(("NC-COL-06", f"{x} is not in tokens.json"))
    for f in RETIRED_FONTS:
        if re.search(rf"\b{f}\b", h, re.I):
            F.append(("NC-COL-05", f"retired typeface '{f}' referenced"))

    # NC-CON-01 — hard outlines. The 2px ink outline is permitted ONLY on the
    # flyer-register class (containment v1.3): covers, posters, dividers.
    for sel, block in blocks:
        flyer = "flyer" in sel.lower()
        mark = any(k in sel for k in (".pt", ".nc-key i", ".key i", ".nc-meter span"))  # NC-CON-05
        # NC-CON-06 — a focus ring is required visibility, not containment. The
        # 3:1 non-text rule applies to focus states by name, so the ring is the
        # mechanism that satisfies it. Quietening it would be an accessibility
        # failure dressed as a house style.
        focus = ":focus" in sel
        for prop, val in re.findall(r"(border(?!-radius)[a-z-]*|outline)\s*:\s*([^;]+)", block, re.I):
            prop = prop.lower(); w = re.search(r"(\d+(?:\.\d+)?)px", val)
            if not w or "none" in val.lower(): continue
            px = float(w.group(1))
            ok = (px == 9 and "top" in prop) or (px == 12 and "left" in prop) or "bottom" in prop
            if px >= 2 and not ok and not flyer and not mark and not focus:
                F.append(("NC-CON-01", f"{prop}: {val.strip()[:40]} on {sel.strip()[:34]} — {px:g}px hard outline"))
    for prop, val in re.findall(r"style=\"[^\"]*?(border(?!-radius)[a-z-]*|outline)\s*:\s*([^;\"]+)", h, re.I):
        w = re.search(r"(\d+(?:\.\d+)?)px", val); prop = prop.lower()
        if w and float(w.group(1)) >= 2 and "bottom" not in prop and "none" not in val.lower():
            F.append(("NC-CON-01", f"inline {prop}: {val.strip()[:40]} — hard outline"))

    # NC-COL-01 — the colour law, as a check rather than a sentence. A light
    # ground may not carry white or near-white text. This is the rule that was
    # false in prose for two years' worth of files; making it checkable is the
    # only fix that stays fixed.
    LIGHT = ("ground-chalk", "ground-white")
    for sel, block in blocks:
        if not any(g in sel for g in LIGHT):
            continue
        m = re.search(r"(?<!-)\bcolor\s*:\s*([^;]+)", block)
        if not m:
            continue
        val = m.group(1).strip().lower()
        if val in ("#fff", "#ffffff", "white") or "--nc-white" in val:
            F.append(("NC-COL-01", f"{sel.strip()[:40]} sets white text on a light ground "
                                   "— 1.1096:1 on chalk, 1.0000:1 on white"))
    for m in re.finditer(r'class="([^"]*)"[^>]*style="([^"]*)"', h):
        if any(g in m.group(1).split() for g in LIGHT) and re.search(
                r"color\s*:\s*(#fff|#ffffff|white)\b", m.group(2), re.I):
            F.append(("NC-COL-01", "inline white text on a light ground"))

    # NC-CON-02 — hairline scope
    hair = len(re.findall(r"1px\s+solid\s+(?:rgba\(13,\s*13,\s*13|var\(--nc-hairline)", h, re.I))
    tables = len(re.findall(r"<table", body, re.I))
    if hair > max(tables, 1):
        W.append(("NC-CON-02", f"{hair} hairline borders but only {tables} tables — hairline is not for anything carrying meaning"))

    # NC-LAY-04 — every spatial value from the scale. Rule weights exempt.
    SCALE={0.25,0.5,0.75,1.0,1.5,2.0,3.0,4.0,6.0}
    for sel, block in blocks:
        for prop, val in re.findall(r"((?:padding|margin|gap|inset)[a-z-]*)\s*:\s*([^;]+)", block):
            for num in re.findall(r"(-?\d*\.?\d+)em", val):
                x = abs(float(num))
                if x and x not in SCALE:
                    W.append(("NC-LAY-04", f"{sel.strip()[:26]} {prop}: {x}em is off the spacing scale"))

    # NC-TYP-01 — caps typed rather than applied
    for run in re.findall(r"\b[A-Z][A-Z'’&-]{2,}(?:\s+[A-Z][A-Z'’&-]{2,}){1,}\b", text):
        if run.strip() and not re.fullmatch(r"[A-Z\s'’&-]*(?:NC|WCAG|PDF|HTML|CSS|JSON|UKDF|ONS)[A-Z\s'’&-]*", run):
            W.append(("NC-TYP-01", f"possible typed caps: “{run[:44]}” — apply text-transform instead"))

    # NC-TYP-15 — a named fallback is not a corrected one. Without metric
    # overrides the stand-in occupies different space, so the page reflows when
    # the real face arrives and every measured layout rule is briefly false.
    if "@font-face" in css and "src:local" in css and "size-adjust" not in css:
        W.append(("NC-TYP-15", "fallback faces declared with no metric overrides"))
    if "@font-face" in css and "src:local" not in css and "data:font" in css:
        W.append(("NC-TYP-15", "fonts embedded but no corrected fallback declared"))

    # NC-TYP-05 — fonts embedded, not linked.
    # Look in the CSS, not the text: a page that *writes about* @font-face is not
    # declaring a font. Checking the raw file made the audit sheet fail for quoting
    # its own rule — a false positive that would teach people to ignore the validator.
    if "@font-face" in css and "data:font" not in css and "data:application/font" not in css:
        F.append(("NC-TYP-05", "@font-face present but no base64 payload — fonts are linked, not embedded"))
    if re.search(r"fonts\.(googleapis|gstatic)\.com", h):
        F.append(("NC-TYP-05", "links Google Fonts — fails silently to a system sans"))

    # NC-DAT-04 — no non-uniform scaling. Stretching survives in the lines and
    # destroys the type, which reads as a rendering fault to everyone but the author.
    # Look at the ATTRIBUTE, not the string. A page that documents the rule
    # writes the words out; that is not a stretched SVG. Third time this class
    # of false positive has appeared — a checker that fires on prose teaches
    # people to ignore it, which is worse than not checking.
    for tag in re.findall(r"<svg\b[^>]{0,600}>|<img\b[^>]{0,600}>", h, re.I):
        if re.search(r'preserveAspectRatio\s*=\s*["\']?\s*none', tag, re.I):
            F.append(("NC-DAT-04", 'preserveAspectRatio="none" — the coordinate space is being stretched'))
            break

    # Split rather than match across tags. A nested-quantifier pattern over a
    # 260KB artefact backtracks for minutes; splitting is linear and does the
    # same job. (Found the hard way: the first version of these checks hung the build.)
    def chunks(hay, open_tag, close_tag):
        out = []
        for piece in hay.split(open_tag)[1:]:
            out.append(piece.split(close_tag)[0])
        return out

    # NC-DAT-05 — a chart is a package: live title, figcaption, never a bare image.
    for fig in chunks(body, "<figure", "</figure>"):
        if "nc-chart" not in fig[:200]:
            continue
        if not re.search(r"<h[1-6]\b", fig) and 'class="ct"' not in fig:
            F.append(("NC-DAT-05", "a chart with no title in live text"))
        if "<figcaption" not in fig:
            F.append(("NC-DAT-05", "a chart with no figcaption — no reading, no source, no alt path"))
        # NC-EVI-09 — illustrative charts carry the flag on the marks.
        if re.search(r"illustrat", re.sub(r"<[^>]+>", " ", fig), re.I) and "nc-illus" not in fig:
            W.append(("NC-EVI-09", "chart says illustrative in prose but carries no flag on the marks"))
    for img in re.findall(r"<img\b[^>]{0,400}>", body, re.I):
        if not re.search(r'alt="[^"]{12,}"', img):
            W.append(("NC-DAT-05", "an image with no alt text, or alt text too short to state a finding"))

    # Count MARKUP, not mentions. A page that documents the system names its
    # own classes in running text and in table cells; counting raw substrings
    # made this page fail its own rules. Only a real class attribute counts.
    def klass(hay, name):
        return len([1 for a in re.findall(r'class="([^"]*)"', hay) if name in a.split()])

    # NC-PSE-01 — one breaker per surface. Two rules stop meaning pause.
    # A specimen section shows every variant side by side on purpose; it says so
    # in the markup, the same way the flyer register declares its hard outline.
    # A surface is a slide where there are slides, and a section otherwise.
    # A catalogue page holding twelve slides is twelve surfaces, not one.
    surfaces = [s for s in chunks(body, '<div class="nc-slide"', "</div></div>")] \
               or chunks(body, "<section", "</section>") or [body]
    for sec in surfaces:
        if "data-nc-specimen" in sec[:400]:
            continue
        n = klass(sec, "nc-brk")
        if n > 1:
            W.append(("NC-PSE-01", f"{n} breakers on one surface — a breaker is a pause, not a pattern"))
            break

    # NC-PRS-03 — no tables on slides. Unreadable from the back of the room,
    # and a reference table on a slide is a reference table in the wrong artefact.
    for sec in chunks(body, "<section", "</section>"):
        if klass(sec, "nc-slide") and "<table" in sec:
            F.append(("NC-PRS-03", "a table inside a slide")); break

    # NC-TYP-04 — caps floor. Below roughly 11px the letterform differences
    # that make a capitalised word readable at all have gone.
    for sel, block in blocks:
        if "uppercase" not in block:
            continue
        m = re.search(r"font-size\s*:\s*(\d+(?:\.\d+)?)px", block)
        if m and float(m.group(1)) < 11:
            W.append(("NC-TYP-04", f"{sel.strip()[:30]} sets caps at {m.group(1)}px"))
        # NC-TBL-01 — never band and rule at once.
        if "nc-table--band" in sel and re.search(r"border-bottom\s*:\s*(?!0)", block):
            W.append(("NC-TBL-01", "banded table also carrying row rules"))

    # NC-DOC-04 — a table that runs across a page break repeats its header.
    for tb in chunks(body, "<table", "</table>"):
        if "<thead" not in tb:
            W.append(("NC-DOC-04", "a table with no <thead> — the header cannot repeat across pages")); break

    # NC-DOC-05 — no skipped heading levels
    lv = [int(x) for x in re.findall(r"<h([1-6])\b", body, re.I)]
    for a, b in zip(lv, lv[1:]):
        if b > a + 1:
            F.append(("NC-DOC-05", f"heading level skipped: h{a} → h{b}")); break

    # NC-BRK-01 — a derived artefact states the CURRENT source version.
    # The old pattern was r"v1\.4|Style Guide v": the second alternative matches
    # any version string at all, so a file declaring "Style Guide v1.0" passed a
    # check built to catch exactly that. The version is read from tokens.json now,
    # so tightening it again is a data edit, not a code edit.
    ver = re.search(r"v(\d+\.\d+)", json.loads((ROOT/"foundations"/"tokens.json")
                    .read_text())["meta"]["source"])
    cur = ver.group(1) if ver else "1.4"
    stated = set(re.findall(r"Style Guide v(\d+\.\d+)", h)) | set(re.findall(r"\bv(\d+\.\d+)\b", h))
    if not stated:
        F.append(("NC-BRK-01", "no source version stated on the artefact"))
    elif cur not in stated:
        F.append(("NC-BRK-01", f"declares v{sorted(stated)[0]}; the current guide is v{cur}"))

    # NC-BRK-02 — wordmark never live type
    if re.search(r"font-family:[^;}]*Archivo Black[^;}]*[^}]*}[^{]*\.nc-logo|\.nc-logo\b[^}]*Archivo Black", h, re.I):
        F.append(("NC-BRK-02", ".nc-logo sets the wordmark as live type"))

    return F, W

def main(paths):
    bad = 0
    for p in paths:
        p = pathlib.Path(p)
        F, W = check(p)
        seen = set(); F = [x for x in F if not (x in seen or seen.add(x))]
        seen = set(); W = [x for x in W if not (x in seen or seen.add(x))]
        mark = "FAIL" if F else ("warn" if W else "PASS")
        print(f"\n=== {mark}  {p.name}")
        for rid, msg in F:
            print(f"  FIXED   {rid}  {msg}")
            print(f"          → {RULES[rid]['rule']}")
        for rid, msg in W[:6]:
            print(f"  check   {rid}  {msg}")
        if len(W) > 6:
            print(f"  check   … {len(W)-6} more")
        if not F and not W:
            print("  clean")
        bad += bool(F)
    print(f"\n{len(paths)} file(s) · {bad} with Fixed breaches")
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ["-"]))
