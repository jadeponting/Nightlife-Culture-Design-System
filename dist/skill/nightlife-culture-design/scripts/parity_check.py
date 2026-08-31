#!/usr/bin/env python3
"""Doc-vs-asset parity: every class named in the skill references and template
must exist as a selector in nc.css. Usage: parity_check.py <nc.css> <ref.md|template.html> ..."""
import re, sys

css = open(sys.argv[1]).read()
css_classes = set(re.findall(r'\.([a-zA-Z][\w-]*)', css))

NOISE = {'md','css','html','py','ai','indd','idml','docx','pptx','pdf','png','0','5','9','42','55','czw'}
documented = {}  # class -> sources
for path in sys.argv[2:]:
    text = open(path).read()
    found = set()
    # `.class` and `.class.mod` tokens inside backticks in markdown
    for m in re.findall(r'`\.([a-zA-Z][\w-]*(?:\.[a-zA-Z][\w-]*)*)`', text):
        found.update(m.split('.'))
    # class="..." attributes in html/code blocks
    for attr in re.findall(r'class="([^"]+)"', text):
        found.update(attr.split())
    for c in found - NOISE:
        documented.setdefault(c, []).append(path.split('/')[-1])

missing = {c: s for c, s in sorted(documented.items()) if c not in css_classes}
print(f"documented classes: {len(documented)} · defined in css: yes={len(documented)-len(missing)} no={len(missing)}")
for c, s in missing.items():
    print(f"  MISSING .{c:<10} referenced by: {', '.join(sorted(set(s)))}")
sys.exit(1 if missing else 0)
