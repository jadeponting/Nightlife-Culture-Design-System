#!/usr/bin/env python3
"""Where did this markup get its look from?

The disclosure under each specimen already showed the markup. It did not show
where the styling CAME from, so a specimen drawn by hand and a specimen built
from the codebase read identically. This resolves every class to the file, line
and section that defines it, and flags anything styled from inside the page
instead — which is the self-reference the disclosure exists to catch.

Nothing here is typed. Every fact is read off the generated stylesheets and off
the rendered specimen.
"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
F = ROOT / "foundations"

# Generated layer, in the order a browser reads it.
GENERATED = ["fonts.css", "nightlife-culture.css", "nightlife-slides.css"]

# Which generator made which file, so the chain can be stated rather than assumed.
MADE_BY = {
    "fonts.css":            "checks/build_fonts.py, from the eight .woff2 faces",
    "nightlife-culture.css": "checks/build.py, from foundations/tokens.json",
    "nightlife-slides.css":  "checks/build_slides.py, from the slide grid in tokens.json",
}

TYPE_PROPS = {"font", "font-family", "font-size", "font-weight", "font-style",
              "letter-spacing", "text-transform", "line-height", "font-variant"}
COLOUR_PROPS = {"color", "background", "background-color", "fill", "stroke",
                "border", "border-color", "outline", "outline-color"}
GEOMETRY_PROPS = {"width", "height", "left", "right", "top", "bottom"}
SPACE_PROPS = {"margin", "margin-top", "margin-bottom", "margin-left", "margin-right",
               "padding", "padding-top", "padding-bottom", "padding-left", "padding-right",
               "gap"}

HEX = re.compile(r"#[0-9a-fA-F]{3,8}\b")
LITERAL = re.compile(r"(?<![\w-])\d*\.?\d+(px|em|rem|pt|ch|vw|vh)\b")


# ---------------------------------------------------------------- css index
def _blank_comments(raw):
    """Remove comments without moving a single line."""
    out, i = [], 0
    while True:
        j = raw.find("/*", i)
        if j < 0:
            out.append(raw[i:])
            return "".join(out)
        out.append(raw[i:j])
        k = raw.find("*/", j + 2)
        k = len(raw) if k < 0 else k + 2
        out.append(re.sub(r"[^\n]", " ", raw[j:k]))
        i = k


def _sections(raw):
    """The /* --- N · NAME --- */ banners, with the line each starts on."""
    found = []
    for n, line in enumerate(raw.split("\n"), 1):
        m = re.match(r"\s*/\* --- (.+)$", line)
        if m:                                   # banners run on for a few lines
            found.append((n, m.group(1).rstrip(" -*/").strip()))
    return found


def _selectors(clean):
    """Yield (selector text, offset) for every rule, media queries unwrapped."""
    i, n, sel_start = 0, len(clean), 0
    while i < n:
        c = clean[i]
        if c == "{":
            sel = clean[sel_start:i]
            if sel.lstrip().startswith("@"):
                sel_start = i + 1              # step inside the at-rule
            else:
                d, j = 1, i + 1
                while j < n and d:
                    d += 1 if clean[j] == "{" else -1 if clean[j] == "}" else 0
                    j += 1
                yield sel.strip(), sel_start
                i, sel_start = j, j
                continue
        elif c == "}":
            sel_start = i + 1
        i += 1


def _subjects(sel):
    """The classes a selector actually DEFINES — the last compound of each
    comma-separated part. `.ground-blue .nc-link` defines .nc-link, not
    .ground-blue; `.nc-slide .cv` defines .cv and says nothing about .nc-slide.
    Reading every dot in the selector is how seventeen components once read as
    built when only a child of each was defined."""
    out = set()
    for part in sel.split(","):
        part = part.strip()
        if not part:
            continue
        subject = re.split(r"[\s>+~]+", part)[-1]
        out |= set(re.findall(r"\.(-?[_a-zA-Z][\w-]*)", subject))
    return out


def index(files=None, local_css=""):
    """class name -> list of (file label, line, section, whole selector)."""
    idx = {}

    def absorb(label, raw, made):
        clean = _blank_comments(raw)
        secs = _sections(raw)
        for sel, off in _selectors(clean):
            head = clean[off:]
            off += len(head) - len(head.lstrip())      # skip to the selector itself
            line = clean[:off].count("\n") + 1
            section = ""
            for n, name in secs:
                if n <= line:
                    section = name
            for cls in _subjects(sel):
                idx.setdefault(cls, []).append(
                    {"file": label, "line": line, "section": section,
                     "selector": " ".join(sel.split()), "made": made})

    for name in (files or GENERATED):
        p = F / name
        if p.exists():
            absorb(name, p.read_text(), MADE_BY.get(name, ""))
    if local_css:
        absorb("this page's own <style> block", local_css,
               "WRITTEN INTO THE PAGE — not generated from tokens")
    return idx


# ------------------------------------------------------------ specimen audit
def _declarations(style):
    for part in style.split(";"):
        if ":" in part:
            prop, _, val = part.partition(":")
            yield prop.strip().lower(), val.strip()


def audit(inner, idx):
    """Read one specimen. Return (classes used, findings)."""
    classes = sorted({c for a in re.findall(r'class="([^"]*)"', inner)
                      for c in a.split()})
    findings = []

    for cls in classes:
        where = idx.get(cls)
        if not where:
            findings.append(("red", f".{cls}",
                             "used here and defined nowhere in the generated layer"))
        elif where[0]["file"].startswith("this page"):
            findings.append(("red", f".{cls}",
                             "defined in this page's own style block, not in the system"))

    for style in re.findall(r'style="([^"]*)"', inner):
        for prop, val in _declarations(style):
            token = "var(--nc-" in val
            if prop in TYPE_PROPS:
                findings.append(("red", prop,
                                 "type set in the markup — no class carries this"))
            elif HEX.search(val):
                findings.append(("red", prop,
                                 f"raw colour {HEX.search(val).group(0)} written into the markup"))
            elif prop in COLOUR_PROPS and token:
                findings.append(("amber", prop,
                                 "colour applied in the markup — a token, but no class"))
            elif prop in GEOMETRY_PROPS and val.rstrip().endswith("%"):
                findings.append(("grey", prop,
                                 f"{val} — geometry carrying a datum, so it belongs in the markup"))
            elif prop in SPACE_PROPS and token:
                findings.append(("amber", prop,
                                 "spacing applied in the markup — on the scale, but no class"))
            elif prop in SPACE_PROPS and not LITERAL.search(val) and \
                    set(val.replace("0", " ").split()) <= {""}:
                findings.append(("amber", prop,
                                 "reset to zero in the markup — zero is on every scale"))
            elif LITERAL.search(val) or prop in SPACE_PROPS:
                findings.append(("red", prop,
                                 f"hand-set {val} — off the spacing scale"))
            else:
                findings.append(("amber", prop, f"{val} — set in the markup"))

    return classes, findings
