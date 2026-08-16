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
    for sel, block in re.findall(r"([^{}]+)\{([^{}]*)\}", h):
        flyer = "flyer" in sel.lower()
        mark = any(k in sel for k in (".pt", ".nc-key i", ".key i", ".nc-meter span"))  # NC-CON-05
        for prop, val in re.findall(r"(border(?!-radius)[a-z-]*|outline)\s*:\s*([^;]+)", block, re.I):
            prop = prop.lower(); w = re.search(r"(\d+(?:\.\d+)?)px", val)
            if not w or "none" in val.lower(): continue
            px = float(w.group(1))
            ok = (px == 9 and "top" in prop) or (px == 12 and "left" in prop) or "bottom" in prop
            if px >= 2 and not ok and not flyer and not mark:
                F.append(("NC-CON-01", f"{prop}: {val.strip()[:40]} on {sel.strip()[:34]} — {px:g}px hard outline"))
    for prop, val in re.findall(r"style=\"[^\"]*?(border(?!-radius)[a-z-]*|outline)\s*:\s*([^;\"]+)", h, re.I):
        w = re.search(r"(\d+(?:\.\d+)?)px", val); prop = prop.lower()
        if w and float(w.group(1)) >= 2 and "bottom" not in prop and "none" not in val.lower():
            F.append(("NC-CON-01", f"inline {prop}: {val.strip()[:40]} — hard outline"))

    # NC-CON-02 — hairline scope
    hair = len(re.findall(r"1px\s+solid\s+(?:rgba\(13,\s*13,\s*13|var\(--nc-hairline)", h, re.I))
    tables = len(re.findall(r"<table", body, re.I))
    if hair > max(tables, 1):
        W.append(("NC-CON-02", f"{hair} hairline borders but only {tables} tables — hairline is not for anything carrying meaning"))

    # NC-LAY-04 — every spatial value from the scale. Rule weights exempt.
    SCALE={0.25,0.5,0.75,1.0,1.5,2.0,3.0,4.0,6.0}
    for sel, block in re.findall(r"([^{}]+)\{([^{}]*)\}", h):
        for prop, val in re.findall(r"((?:padding|margin|gap|inset)[a-z-]*)\s*:\s*([^;]+)", block):
            for num in re.findall(r"(-?\d*\.?\d+)em", val):
                x = abs(float(num))
                if x and x not in SCALE:
                    W.append(("NC-LAY-04", f"{sel.strip()[:26]} {prop}: {x}em is off the spacing scale"))

    # NC-TYP-01 — caps typed rather than applied
    for run in re.findall(r"\b[A-Z][A-Z'’&-]{2,}(?:\s+[A-Z][A-Z'’&-]{2,}){1,}\b", text):
        if run.strip() and not re.fullmatch(r"[A-Z\s'’&-]*(?:NC|WCAG|PDF|HTML|CSS|JSON|UKDF|ONS)[A-Z\s'’&-]*", run):
            W.append(("NC-TYP-01", f"possible typed caps: “{run[:44]}” — apply text-transform instead"))

    # NC-TYP-05 — fonts embedded, not linked.
    # Look in the CSS, not the text: a page that *writes about* @font-face is not
    # declaring a font. Checking the raw file made the audit sheet fail for quoting
    # its own rule — a false positive that would teach people to ignore the validator.
    style = " ".join(re.findall(r"<style[^>]*>(.*?)</style>", h, flags=re.S))
    if "@font-face" in style and "data:font" not in style and "data:application/font" not in style:
        F.append(("NC-TYP-05", "@font-face present but no base64 payload — fonts are linked, not embedded"))
    if re.search(r"fonts\.(googleapis|gstatic)\.com", h):
        F.append(("NC-TYP-05", "links Google Fonts — fails silently to a system sans"))

    # NC-DOC-05 — no skipped heading levels
    lv = [int(x) for x in re.findall(r"<h([1-6])\b", body, re.I)]
    for a, b in zip(lv, lv[1:]):
        if b > a + 1:
            F.append(("NC-DOC-05", f"heading level skipped: h{a} → h{b}")); break

    # NC-BRK-01 — derived artefact states its source version
    if not re.search(r"v1\.4|Style Guide v", h):
        F.append(("NC-BRK-01", "no source version stated on the artefact"))

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
