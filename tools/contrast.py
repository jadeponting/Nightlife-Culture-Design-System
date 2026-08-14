#!/usr/bin/env python3
"""Nightlife Culture — WCAG contrast checker.

Usage:
  python contrast.py "#0000FF" "#FFFFFF"      one pair
  python contrast.py --matrix                 full brand matrix
  python contrast.py --check "#123456"        one colour against every brand token
"""
import sys

TOKENS = {
    'blue': '#0000FF', 'ink': '#0D0D0D', 'chalk': '#F3F3F3', 'white': '#FFFFFF',
    'charcoal': '#2D2D2D', 'pink': '#ED77C2', 'teal': '#53E6E5', 'violet': '#B98CFF',
    'butter': '#FFDE6B', 'coral': '#FD7B53',
}
RAMP = {'series1': '#0000FF', 'series2': '#C7339A', 'series3': '#00C6C5', 'series4': '#FFDE6B'}


def _lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hexcolour):
    h = hexcolour.lstrip('#')
    if len(h) == 3:
        h = ''.join(ch * 2 for ch in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def ratio(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def verdict(r):
    parts = []
    parts.append('AA body PASS' if r >= 4.5 else 'AA body FAIL')
    parts.append('AA large PASS' if r >= 3 else 'AA large FAIL')
    parts.append('AAA PASS' if r >= 7 else 'AAA fail')
    parts.append('graphics PASS' if r >= 3 else 'graphics FAIL')
    return ' · '.join(parts)


def main(argv):
    if not argv or argv[0] in ('-h', '--help'):
        print(__doc__)
        return 0
    if argv[0] == '--matrix':
        names = list(TOKENS)
        print(f'{"":10}' + ''.join(f'{n[:8]:>9}' for n in names))
        for a in names:
            print(f'{a:10}' + ''.join(
                '        —' if a == b else f'{ratio(TOKENS[a], TOKENS[b]):>9.2f}' for b in names))
        return 0
    if argv[0] == '--check':
        target = argv[1]
        for n, v in {**TOKENS, **RAMP}.items():
            r = ratio(target, v)
            print(f'{n:10} {v}  {r:6.2f}  {verdict(r)}')
        return 0
    if len(argv) < 2:
        print('Need two colours, or --matrix / --check.')
        return 1
    a, b = argv[0], argv[1]
    r = ratio(a, b)
    print(f'{a} on {b} → {r:.2f}:1')
    print(verdict(r))
    if r < 4.5:
        print('\nBrand rule: every accent is a black-text surface; every ground is a white-text surface.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
