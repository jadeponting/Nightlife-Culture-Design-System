# Superseded — the hand-authored slide layouts

These twelve files were the slide layouts before the slide layer was generated.
They rendered correctly and were not compliant: every margin, gap and type size
was typed into the file, so nothing tied them to the tokens and nothing checked
them.

They are replaced by `layouts/build_layouts.py`, which produces `layouts/index.html`
from `foundations/tokens.json` and `foundations/nightlife-slides.css`. Change the
grid once and all twelve move together.

Kept for reference only. Nothing derives from them.
