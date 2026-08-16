#!/usr/bin/env python3
"""Every class the stylesheets define must be shown somewhere you can look at it.

    python3 checks/check_coverage.py

The component library used to be the one hand-authored thing in a generated
chain, and it drifted: 91 classes defined, 48 demonstrated. The stamp check
could not see it, because the stamp compares digests of SOURCES and the library
body IS a source. So a component could exist, be correct, be validated — and be
invisible to the person who has to choose it.

A component nobody can see is a component nobody will use, and the system was
built on 'show, do not describe'. This makes that a check.

Two surfaces demonstrate: components/library.body.html for the document layer,
layouts/index.html for the slide layer. A class shown in either passes.
"""
import pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
F = ROOT / "foundations"

css = "\n".join((F / f).read_text() for f in
                ("nightlife-culture.css", "nightlife-slides.css") if (F / f).exists())
css = re.sub(r"/\*.*?\*/", " ", css, flags=re.S)
defined = {m for m in re.findall(r"\.(nc-[a-z0-9-]+)", css)} | \
          {m for m in re.findall(r"\.(ground-[a-z]+|acc-[a-z]+)", css)}

# Read the BUILT pages, not the source bodies. Some classes are added by the
# build itself — the markup disclosure under each specimen is generated, not
# typed — and a check that reads the source cannot see them. What matters is
# what renders, so that is what is counted.
SURFACES = ["components/index.html", "layouts/index.html"]
shown = set()
for f in SURFACES:
    p = ROOT / f
    if p.exists():
        shown |= {c for a in re.findall(r'class="([^"]*)"', p.read_text()) for c in a.split()}

# NC-PAG-02 — a sheet never carries its own stylesheet. Five of them existed,
# they disagreed, and the disagreement is what the reviewer kept finding. The
# page builder at docs/sheet.py is the only place page furniture is decided.
strays = sorted(p.relative_to(ROOT).as_posix()
                for d in ("docs", "components", "layouts", "adapters")
                for p in (ROOT / d).glob("*.css") if (ROOT / d).exists())
if strays:
    print("\n  per-sheet stylesheets found — page furniture is a component (NC-PAG-02):")
    for f in strays:
        print(f"    {f}")
    sys.exit(1)

# A class defined twice, where the second definition re-sets a property the
# first one already set. The later one wins silently. `.nc-prov` was the
# evidence-provenance chip and was taken a second time for a provenance table:
# every cell in that table rendered as white text on white and NOTHING failed —
# not the validator, not coverage, not the stamps.
#
# A class named in a shared cross-cutting rule (the case section sets
# text-transform on nine components at once) is not a redefinition, because it
# sets nothing the component set. Overlap is the test, not repetition.
import collections


def _solo_blocks(raw):
    """(class, {properties}, section) for every rule whose selector is one bare class."""
    txt = re.sub(r"/\*.*?\*/", lambda m: re.sub(r"[^\n]", " ", m.group(0)), raw, flags=re.S)
    # Blank out @media bodies. Re-setting a property at a breakpoint is what a
    # breakpoint is for; it is not a second component wearing the same name.
    out, i = [], 0
    while True:
        j = txt.find("@media", i)
        if j < 0:
            out.append(txt[i:]); break
        out.append(txt[i:j])
        k = txt.find("{", j); d, e = 1, k + 1
        while e < len(txt) and d:
            d += 1 if txt[e] == "{" else -1 if txt[e] == "}" else 0
            e += 1
        out.append(re.sub(r"[^\n]", " ", txt[j:e])); i = e
    txt = "".join(out)
    secs = [(n, m.group(1).rstrip(" -*/").strip())
            for n, l in enumerate(raw.split("\n"), 1)
            for m in [re.match(r"\s*/\* --- (.+)$", l)] if m]
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", txt):
        line = txt[:m.start()].count("\n") + 1
        section = ""
        for n, name in secs:
            if n <= line:
                section = name
        props = {d.split(":")[0].strip().lower()
                 for d in m.group(2).split(";") if ":" in d}
        props = {x for x in props if x and not x.startswith("--")}
        for part in m.group(1).split(","):
            c = re.fullmatch(r"\s*\.(nc-[a-z0-9-]+)\s*", part)
            if c:
                yield c.group(1), props, f"{section[:44]} (line {line})"


seen, clashes = collections.defaultdict(list), {}
for name in ("nightlife-culture.css", "nightlife-slides.css"):
    if (F / name).exists():
        for cls, props, where in _solo_blocks((F / name).read_text()):
            for prev_props, prev_where in seen[cls]:
                shared = props & prev_props
                if shared:
                    clashes.setdefault(cls, []).append(
                        (sorted(shared), prev_where, f"{name} · {where}"))
            seen[cls].append((props, f"{name} · {where}"))

if clashes:
    print("\n  REPORTED, NOT FAILED — one class name declared twice, later wins:")
    for cls, hits in sorted(clashes.items()):
        print(f"    .{cls}")
        for shared, first, second in hits:
            print(f"        {', '.join(shared)}")
            print(f"          set at  {first}")
            print(f"          re-set  {second}")
    print("\n  There is no rule saying whether a component may be re-declared in a\n"
          "  later section. Until Carly decides one, this reports and does not fail.\n"
          "  Logged in docs/gaps.md.")

missing = sorted(defined - shown)
print(f"{len(defined)} classes defined · {len(defined) - len(missing)} demonstrated")
if missing:
    print(f"\n  {len(missing)} defined and shown nowhere:")
    for c in missing:
        print(f"    .{c}")
    print("\n  Add a specimen to components/library.body.html, or delete the class.")
    sys.exit(1)
print("  every component has somewhere you can look at it")
