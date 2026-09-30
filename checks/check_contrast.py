#!/usr/bin/env python3
"""Contrast measured on the RENDERED page, not guessed from the source.

Every contrast check in this system so far read the source: is this hex on the
allowlist, is white text on a light ground, does a ground declare its own text
colour. Source checks cannot see blue text that ends up on a dark ground because
an ancestor set the ground three levels up. That is why the same failure has
been reported by Carly five or six times and passed the build every time.

This opens each page in a real browser, walks every element that renders text,
resolves the colour it actually paints and the background it actually paints
onto, and computes the ratio. WCAG 1.4.3: 4.5:1 for text, 3:1 for large text
(>=24px, or >=18.66px bold).

    python3 checks/check_contrast.py
"""
import asyncio, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ["components/index.html", "layouts/slide-patterns.html", "docs/what-we-have.html",
         "docs/the-build-order.html", "docs/how-the-logic-works.html",
         "dist/component-library.html", "dist/slide-patterns.html", "dist/index.html"] + \
        sorted(f"{d}/{p.stem}.html" for p in (ROOT / "decks").glob("*.json") for d in ("decks", "dist"))

# Two widths. A phone is where the reviewer actually reads these, and it is where
# a clamp collapses, a grid stacks and a colour lands on a different ground.
WIDTHS = [1280, 390]

JS = r"""
() => {
  const lin = c => { c /= 255; return c <= 0.04045 ? c/12.92 : Math.pow((c+0.055)/1.055, 2.4); };
  const lum = ([r,g,b]) => 0.2126*lin(r) + 0.7152*lin(g) + 0.0722*lin(b);
  const parse = s => { const m = s.match(/[\d.]+/g); return m ? m.map(Number) : null; };
  const over = (fg, bg) => {           // composite a translucent colour onto a solid one
    const a = fg.length > 3 ? fg[3] : 1;
    return [0,1,2].map(i => fg[i]*a + bg[i]*(1-a));
  };
  const bgOf = el => {
    let n = el, acc = null;
    while (n && n.nodeType === 1) {
      const c = parse(getComputedStyle(n).backgroundColor);
      if (c && (c.length < 4 || c[3] > 0)) { acc = acc ? over(acc, c) : c; if ((c[3] ?? 1) === 1) return acc; }
      n = n.parentElement;
    }
    return acc ? over(acc, [255,255,255]) : [255,255,255];
  };
  const out = [];
  // Pseudo-elements paint text too. The SHOW / HIDE marker on every disclosure
  // is an ::after, and a walker that only reads text nodes cannot see it.
  for (const el of document.querySelectorAll('body *')) {
    for (const pe of ['::before', '::after']) {
      const cs = getComputedStyle(el, pe);
      const c = cs.content;
      if (!c || c === 'none' || c === 'normal' || !/["']/.test(c)) continue;
      const fg = parse(cs.color); if (!fg) continue;
      const bg = bgOf(el);
      const solid = over(fg, bg);
      const L1 = lum(solid), L2 = lum(bg);
      const ratio = (Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05);
      const px = parseFloat(cs.fontSize), w = parseInt(cs.fontWeight) || 400;
      const need = (px >= 24 || (px >= 18.66 && w >= 700)) ? 3 : 4.5;
      if (ratio < need - 0.005)
        out.push({ text: c.slice(0,40) + ' ' + pe, ratio: +ratio.toFixed(2), need,
                   px:+px.toFixed(1), weight:w, fg: cs.color,
                   bg: `rgb(${bg.map(x=>Math.round(x)).join(',')})`,
                   sel: el.tagName.toLowerCase() + (typeof el.className === 'string' && el.className
                        ? '.' + el.className.trim().split(/\s+/).join('.') : '') + pe });
    }
  }
  for (const el of document.querySelectorAll('body *')) {
    const txt = [...el.childNodes].filter(n => n.nodeType === 3)
                  .map(n => n.textContent.trim()).join(' ').trim();
    if (!txt) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity === 0) continue;
    const r = el.getBoundingClientRect();
    if (!r.width || !r.height) continue;
    const fg = parse(cs.color); if (!fg) continue;
    const bg = bgOf(el);
    const solid = over(fg, bg);
    const L1 = lum(solid), L2 = lum(bg);
    const ratio = (Math.max(L1,L2) + 0.05) / (Math.min(L1,L2) + 0.05);
    const px = parseFloat(cs.fontSize), w = parseInt(cs.fontWeight) || 400;
    const large = px >= 24 || (px >= 18.66 && w >= 700);
    const need = large ? 3 : 4.5;
    if (ratio < need - 0.005) {
      out.push({ text: txt.slice(0, 58), ratio: +ratio.toFixed(2), need,
                 px: +px.toFixed(1), weight: w,
                 fg: cs.color, bg: `rgb(${bg.map(x=>Math.round(x)).join(',')})`,
                 sel: el.tagName.toLowerCase() +
                      (el.className && typeof el.className === 'string'
                        ? '.' + el.className.trim().split(/\s+/).join('.') : '') });
    }
  }
  return out;
}
"""

# NC-LAY-07 — slide fit. Content stops 8% above the foot, or above the closing
# band; it never runs under the side block. Measured on the rendered slide,
# because a slide that overflows looks fine in its source.
FIT = r"""
() => [...document.querySelectorAll('.nc-slide')].map((s, i) => {
  const pad = s.querySelector('.nc-sp'), side = s.querySelector('.nc-sside');
  if (!pad) return null;
  const pr = pad.getBoundingClientRect();
  const floor = pr.bottom;              // the pad IS the allowance: 8% up, above a band, or the cover's
  const wall = side ? side.getBoundingClientRect().left : pr.right + 1;
  let worst = null;
  s.querySelectorAll('.nc-sp *').forEach(e => {
    if (e.closest('svg')) return;
    const b = e.getBoundingClientRect();
    if (!b.height) return;
    const over = Math.max(b.bottom - floor, b.right - wall);
    if (over > 1 && (!worst || over > worst.over))
      worst = {over: Math.round(over), text: (e.textContent || '').trim().slice(0, 50)};
  });
  return worst ? {n: i + 1, pattern: s.dataset.pattern || '', ...worst} : null;
}).filter(Boolean)
"""


SKIPPED = False

async def run():
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("  SKIPPED — playwright is not installed on this machine.\n"
              "  pip install playwright && playwright install chromium\n"
              "  A skipped check is not a passed check: nothing here has been measured.")
        global SKIPPED; SKIPPED = True
        return 3
    fails = 0
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        for width in WIDTHS:
          p = await b.new_page(viewport={"width": width, "height": 900})
          print(f"\n--------- {width}px ---------")
          for rel in PAGES:
            f = ROOT / rel
            if not f.exists():
                continue
            await p.goto(f.as_uri())
            await p.wait_for_timeout(500)
            await p.evaluate("()=>document.querySelectorAll('details').forEach(d=>d.open=true)")
            await p.wait_for_timeout(200)
            hits = await p.evaluate(JS)
            seen, uniq = set(), []
            for h in hits:
                k = (h["sel"], h["ratio"])
                if k not in seen:
                    seen.add(k); uniq.append(h)
            if uniq:
                fails += len(uniq)
                print(f"\n=== FAIL  {rel} — {len(uniq)} distinct")
                for h in sorted(uniq, key=lambda x: x["ratio"]):
                    print(f"  {h['ratio']:>5}:1  needs {h['need']}  "
                          f"{h['px']}px/{h['weight']}  {h['fg']} on {h['bg']}")
                    print(f"          {h['sel']}")
                    print(f"          \u201c{h['text']}\u201d")
            else:
                print(f"=== PASS  {rel}")
            if width == WIDTHS[0]:
                for o in await p.evaluate(FIT):
                    fails += 1
                    print(f"  FIT   {rel} slide {o['n']} ({o['pattern']}): runs {o['over']}px past "
                          f"its floor — NC-LAY-07. \u201c{o['text']}\u201d")
          await p.close()
        await b.close()
    return fails


n = asyncio.run(run())
print(f"\n{n} rendered contrast failure(s)")
sys.exit(3 if n == 3 and SKIPPED else (1 if n else 0))
