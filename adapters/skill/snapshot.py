"""Fingerprint the inputs to the portable design skill; stdlib only."""
import hashlib
from pathlib import Path


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def source_files(root):
    root = Path(root)
    files = {root / name for name in (
        "AGENTS.md", "README.md", "README-BUILD.md", "build.py",
        "adapters/skill/build_skill.py", "adapters/skill/snapshot.py",
        "docs/gaps.md", "docs/changelog.md", "docs/LOGO.md",
    )}
    # Include added assets and references too, not just the files present today.
    for directory in ("foundations", "assets", "reference", "adapters/skill/src"):
        files.update(p for p in (root / directory).rglob("*") if p.is_file())
    for directory, suffixes in (
        ("decks", {".json", ".py"}),
        ("layouts", {".py"}),
        ("components", {".py"}),
        ("checks", {".py", ".json"}),
    ):
        files.update(p for p in (root / directory).rglob("*")
                     if p.is_file() and p.suffix in suffixes)
    files.add(root / "components/library.body.html")
    return {str(p.relative_to(root)): digest(p) for p in sorted(files)
            if p.is_file() and p.name != ".DS_Store" and p.suffix != ".pyc"
            and "__pycache__" not in p.parts}


def fingerprint(files):
    import json
    return hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()
