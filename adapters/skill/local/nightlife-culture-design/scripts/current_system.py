#!/usr/bin/env python3
"""Read the current local design system and reject stale portable inputs. No writes."""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import subprocess
import sys

DEFAULT_ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(DEFAULT_ROOT / "adapters/skill"))
from snapshot import digest, fingerprint, source_files


class GuideMeta(HTMLParser):
    def __init__(self):
        super().__init__()
        self.source = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "meta" and attrs.get("name") == "nc-source":
            self.source = attrs.get("content")


def inspect(root):
    root = root.resolve()
    tokens = json.loads((root / "foundations/tokens.json").read_text())
    current = source_files(root)
    source = tokens["meta"]["source"]
    guides = []
    for path in sorted((root / "assets").glob("*.html")):
        parser = GuideMeta()
        parser.feed(path.read_text())
        if parser.source == source:
            guides.append(str(path))
    errors = []
    if len(guides) != 1:
        errors.append(f"Expected one guide declaring {source}; found {len(guides)}")
    bundle = root / "dist/skill/nightlife-culture-design"
    manifest_path = bundle / "snapshot.json"
    changed_sources, changed_bundle = [], []
    if not manifest_path.is_file():
        errors.append("Portable skill has no snapshot manifest; rebuild before reusing its assets")
    else:
        manifest = json.loads(manifest_path.read_text())
        recorded = manifest["sourceFiles"]
        changed_sources = sorted(k for k in current.keys() | recorded.keys()
                                 if current.get(k) != recorded.get(k))
        actual = {str(p.relative_to(bundle)): digest(p) for p in bundle.rglob("*")
                  if p.is_file() and p.name != "snapshot.json" and p.suffix != ".pyc"
                  and "__pycache__" not in p.parts}
        recorded_bundle = manifest["bundleFiles"]
        changed_bundle = sorted(k for k in actual.keys() | recorded_bundle.keys()
                                if actual.get(k) != recorded_bundle.get(k))
        if manifest["source"] != source or changed_sources:
            errors.append("Portable skill inputs have changed; rebuild it from the current repo")
        if changed_bundle:
            errors.append("Portable skill contents differ from their build manifest")
    stamps = subprocess.run([sys.executable, str(root / "checks/check_stamps.py")],
                            cwd=root, capture_output=True, text=True, timeout=30)
    if stamps.returncode:
        errors.append("Generated artifact stamp check failed")
    return {
        "repo": str(root), "source": source, "guide": guides,
        "sourceFingerprint": fingerprint(current),
        "status": "current" if not errors else "needs-attention",
        "errors": errors,
        "portable": {"manifest": str(manifest_path),
                     "changedSources": changed_sources, "changedFiles": changed_bundle},
        "stamps": {"exitCode": stamps.returncode,
                   "details": (stamps.stdout + stamps.stderr).strip() if stamps.returncode else "passed"},
        "adapters": sorted(p.name for p in (root / "adapters").iterdir() if p.is_dir()),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=DEFAULT_ROOT,
                        help="Optional checkout to inspect; normally resolved from this skill")
    args = parser.parse_args()
    try:
        result = inspect(args.repo)
    except (OSError, ValueError, KeyError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"repo": str(args.repo), "status": "unavailable", "error": str(exc)}, indent=2))
        return 2
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "current" else 1


if __name__ == "__main__":
    sys.exit(main())
