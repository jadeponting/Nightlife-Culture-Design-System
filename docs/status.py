"""One definition of 'complete', shared by the audit and the build order.

Both pages ask the same question of every component, so the question is asked
in one place. If they each had their own copy, the plan could go on listing
work the audit already counts as done — which is the exact failure the plan
exists to prevent.
"""
import json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
F = ROOT / "foundations"
# Both generated stylesheets. The slide layer is a second file because it is a
# context, not a component set — but a component defined there is still built.
CSS_RAW = "\n".join((F / f).read_text() for f in
                    ("nightlife-culture.css", "nightlife-slides.css") if (F / f).exists())
RULES = {r["id"]: r for r in json.loads((F / "rules.json").read_text())["rules"]}
_FONTS = (F / "fonts.css").read_text() if (F / "fonts.css").exists() else ""

# Strip comments before parsing: a comment sitting above a rule gets swallowed
# into the selector otherwise. Unwrap media queries so their contents parse.
_CSS = re.sub(r"/\*.*?\*/", " ", CSS_RAW, flags=re.S)
_CSS = re.sub(r"@media[^{]*\{", " ", _CSS)
SELECTORS = set()
for _blk in re.findall(r"([^{}]+)\{[^{}]*\}", _CSS):
    for _part in _blk.split(","):
        _p = re.sub(r"\s+", " ", _part.strip())
        if _p and not _p.startswith("@") and "}" not in _p:
            SELECTORS.add(_p)
            SELECTORS.add(re.split(r"[:\[]", _p)[0].strip())

def has_class(c):
    """Is this selector DEFINED — not merely mentioned — in the stylesheet?"""
    if c.startswith("--"):
        return bool(re.search(re.escape(c) + r"\s*:", CSS_RAW))
    if c == "@font-face":
        return "@font-face" in _FONTS
    return c in SELECTORS

def enforced(it):
    """Scripts that enforce this item's rules. Verified: the file must exist
    AND mention every rule id claimed, so a stale reference cannot pass."""
    out = []
    for chk in it.get("enforced_by", []):
        f = ROOT / chk
        if not f.exists():
            continue
        txt = f.read_text()
        if not it.get("rules") or all(r in txt for r in it["rules"]):
            out.append(chk)
    return out

def state(it):
    """(label, kind) where kind is ok | flag | gap."""
    cls, rls = it.get("class", []), it.get("rules", [])
    built = bool(cls) and all(has_class(c) for c in cls)
    ruled = bool(rls) and all(r in RULES for r in rls)
    checks = enforced(it)
    if it.get("absence"):
        return ("Enforced by absence", "ok") if (ruled or checks) else ("Not recorded", "gap")
    if built and ruled:  return ("Built, with the rule", "ok")
    if checks and ruled: return ("Ruled and enforced", "ok")
    if built:            return ("Built — no rule attached", "flag")
    if ruled:            return ("Ruled — nothing enforces it", "flag")
    return ("Not in the codebase", "gap")

def done(it):
    return state(it)[1] == "ok"

def todo_note(it):
    cls, rls = it.get("class", []), it.get("rules", [])
    built = bool(cls) and all(has_class(c) for c in cls)
    ruled = bool(rls) and all(r in RULES for r in rls)
    if built and not ruled: return "Write the rule — what job it does, and when you may depart from it."
    if ruled and not built: return "Build it. The rule already says what it must do."
    return "Take the rule from the Book, write it down, then build it."
