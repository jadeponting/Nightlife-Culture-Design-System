#!/usr/bin/env python3
"""Nightlife Culture design system — validator.

Checks built HTML against contracts/layouts.json and contracts/rules.json.
Standard library only, so it runs anywhere without installing anything.

    python tools/validate.py templates/deck.html
    python tools/validate.py "decks/*.html" --strict
    python tools/validate.py --list

Exit code 0 = pass, 1 = failures. Warnings alone do not fail unless --strict.
"""
import sys, os, json, re, glob
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RED, YEL, GRN, DIM, OFF = '\033[31m', '\033[33m', '\033[32m', '\033[2m', '\033[0m'
if not sys.stdout.isatty(): RED = YEL = GRN = DIM = OFF = ''


def load(name):
    with open(os.path.join(ROOT, 'contracts', name), encoding='utf-8') as f:
        return json.load(f)


class Node:
    __slots__ = ('tag', 'attrs', 'children', 'parent', 'text')

    def __init__(self, tag, attrs, parent=None):
        self.tag, self.attrs, self.parent = tag, dict(attrs), parent
        self.children, self.text = [], ''

    def cls(self):
        return set((self.attrs.get('class') or '').split())

    def all_text(self):
        return (self.text + ' ' + ' '.join(c.all_text() for c in self.children)).strip()

    def find(self, pred, out=None):
        out = [] if out is None else out
        for c in self.children:
            if pred(c): out.append(c)
            c.find(pred, out)
        return out


VOID = {'br', 'img', 'hr', 'meta', 'link', 'input', 'source', 'path', 'circle', 'line', 'polyline', 'rect', 'use'}


class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node('#root', {})
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.cur)
        self.cur.children.append(n)
        if tag not in VOID: self.cur = n

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, attrs, self.cur))

    def handle_endtag(self, tag):
        n = self.cur
        while n is not self.root and n.tag != tag: n = n.parent
        if n is not self.root: self.cur = n.parent

    def handle_data(self, data):
        if data.strip(): self.cur.text += ' ' + data.strip()


KICKER_INDEX = re.compile(r'^\s*\d{1,2}\s*[·.\-–—]\s*')


def words(s, slot=None):
    """Word count. A leading section index ("07 · ") is furniture, not copy."""
    if slot in ('kicker', 'attribution'):
        s = KICKER_INDEX.sub('', s)
    return [w for w in re.split(r'\s+', re.sub(r'[^\w\s’\'-]', ' ', s)) if w]


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def err(self, where, msg, fix=''):
        self.errors.append((where, msg, fix))

    def warn(self, where, msg, fix=''):
        self.warnings.append((where, msg, fix))


def check_slide(sec, idx, contracts, rules, rep):
    lay_id = sec.attrs.get('data-layout')
    where = f'slide {idx + 1}'
    if not lay_id:
        rep.err(where, 'no data-layout attribute',
                'add data-layout="L03" (see contracts/layouts.json)')
        return
    where = f'{where} [{lay_id}]'
    lay = contracts['layouts'].get(lay_id)
    if not lay:
        rep.err(where, f'unknown layout {lay_id}',
                'valid: ' + ', '.join(contracts['layouts']))
        return

    # --- ground -----------------------------------------------------------
    cv = next((c for c in sec.find(lambda n: 'cv' in n.cls())), None)
    ground = None
    if cv:
        for g in rules['colour']['grounds']:
            if f'ground-{g}' in cv.cls(): ground = g
    if not ground:
        rep.err(where, 'no ground-* class on .cv',
                'add class="cv ground-blue" (or ground-chalk / ground-white / ground-ink)')
    elif ground not in lay['grounds']:
        rep.err(where, f'ground "{ground}" not permitted for {lay_id}',
                f'permitted: {", ".join(lay["grounds"])}')

    # --- anchor -----------------------------------------------------------
    pads = sec.find(lambda n: 'pad' in n.cls())
    holder = None
    if pads:
        holder = pads[0]
        anchor = holder.attrs.get('data-anchor')
        if not anchor:
            rep.err(where, 'missing data-anchor on .pad',
                    f'this layout requires data-anchor="{lay["anchor"]}"')
        elif anchor != lay['anchor']:
            rep.err(where, f'data-anchor="{anchor}" but {lay_id} requires "{lay["anchor"]}"',
                    'wrong anchor is what leaves a dead band at the bottom')
    else:
        # split / strip layouts hold content differently
        holder = next(iter(sec.find(lambda n: {'main', 'top'} & n.cls())), None)
        if holder is None and lay_id not in ('L08', 'L09', 'L10'):
            rep.err(where, 'no .pad found', 'content must sit inside .pad')

    # --- block budget -----------------------------------------------------
    if holder is not None:
        blocks = [c for c in holder.children if c.tag not in VOID]
        if len(blocks) > lay['maxBlocks']:
            rep.err(where, f'{len(blocks)} blocks, max {lay["maxBlocks"]}',
                    'remove copy or split into two slides — do not shrink type')

    # --- one breaker ------------------------------------------------------
    brks = sec.find(lambda n: {'brk', 'hairbrk'} & n.cls())
    max_brk = lay.get('maxBreakers', rules['composition']['maxBreakersPerSlide'])
    if len(brks) > max_brk:
        rep.err(where, f'{len(brks)} breakers, max {max_brk}',
                'two rules stop meaning "pause" and start meaning "pattern"')

    # --- slots ------------------------------------------------------------
    for name, spec in lay['slots'].items():
        want = spec.get('class')
        if not want: continue
        first = want.split()[0]
        found = sec.find(lambda n, f=first: f in n.cls())
        if spec.get('required') and not found:
            rep.err(where, f'required slot "{name}" missing (.{first})', lay.get('note', ''))
        if spec.get('count') and found and len(found) != spec['count'] and first in ('tr3', 'g3', 'strip'):
            kids = [c for c in found[0].children if c.tag not in VOID]
            if len(kids) != spec['count']:
                rep.err(where, f'slot "{name}" has {len(kids)} items, contract says {spec["count"]}',
                        'ragged grids read as a mistake — use the declared count')
        if spec.get('maxWords') and found:
            n = len(words(found[0].all_text(), name))
            if n > spec['maxWords']:
                rep.err(where, f'slot "{name}" is {n} words, max {spec["maxWords"]}',
                        'shorten the copy — this is a caps/scale rule, not a preference')
        each = spec.get('each') or {}
        if each.get('numeral') and found:
            for kid in [c for c in found[0].children if c.tag not in VOID]:
                if not kid.find(lambda n: 'n' in n.cls()):
                    rep.err(where, f'"{name}" item missing its numeral (.n)',
                            'a rule with a label and no numeral reads as disconnected')
                    break

    # --- forbidden --------------------------------------------------------
    for bad in lay.get('forbid', []):
        if sec.find(lambda n, b=bad: b in n.cls()):
            rep.err(where, f'"{bad}" is not permitted in {lay_id}',
                    'pick a layout that declares it rather than adding it here')

    # --- footer -----------------------------------------------------------
    foot = next(iter(sec.find(lambda n: 'foot' in n.cls())), None)
    fspec = lay.get('footer', {})
    if foot:
        has_num = bool(foot.find(lambda n: 'pnum' in n.cls()))
        has_logo = bool(foot.find(lambda n: 'logo' in n.cls()))
        if has_num and not fspec.get('slideNumber'):
            rep.warn(where, 'slide number present but this layout takes none',
                     'covers, closings and strip slides are unnumbered')
        if not has_num and fspec.get('slideNumber'):
            rep.warn(where, 'slide number missing', 'content slides are numbered')
        if has_logo and not fspec.get('logo'):
            rep.warn(where, 'logo on a content slide',
                     'logo goes on cover, dividers, closing, or slides that travel alone')

    # --- colour law -------------------------------------------------------
    for n in sec.find(lambda n: True):
        st = (n.attrs.get('style') or '').lower().replace(' ', '')
        for acc, meta in rules['colour']['accents'].items():
            hexv = meta['hex'].lower()
            if f'background:{hexv}' in st and 'color:#fff' in st:
                rep.err(where, f'white text on {acc} — fails contrast',
                        'every accent is a black-text surface')
        for dead in rules['colour']['retired']:
            if dead.lower() in st:
                rep.err(where, f'retired colour {dead}', 'see contracts/rules.json colour.retired')


def validate_file(path, contracts, rules):
    rep = Report()
    with open(path, encoding='utf-8') as f:
        src = f.read()
    t = Tree(); t.feed(src)
    secs = t.root.find(lambda n: n.tag == 'section' and n.attrs.get('data-layout') is not None)
    if not secs:
        secs = t.root.find(lambda n: n.tag == 'section')
    for i, s in enumerate(secs):
        check_slide(s, i, contracts, rules, rep)
    return rep, len(secs)


def main(argv):
    contracts, rules = load('layouts.json'), load('rules.json')
    if '--check-contracts' in argv:
        bad = 0
        nested = {'L08', 'L09', 'L10'}
        for k, lay in contracts['layouts'].items():
            n = len(lay['slots'])
            if k not in nested and lay['maxBlocks'] < n:
                print(f'{RED}✗{OFF} {k}: maxBlocks={lay["maxBlocks"]} but declares {n} slots')
                bad += 1
            for g in lay['grounds']:
                if g not in rules['colour']['grounds']:
                    print(f'{RED}✗{OFF} {k}: unknown ground "{g}"'); bad += 1
            if lay['anchor'] not in rules['composition']['anchorValues']:
                print(f'{RED}✗{OFF} {k}: bad anchor "{lay["anchor"]}"'); bad += 1
        print(f'{GRN}contracts OK{OFF}' if not bad else f'{bad} contract problem(s)')
        return 1 if bad else 0
    if '--list' in argv:
        print(f'{"id":5} {"name":24} {"anchor":7} {"blocks":6} grounds')
        for k, v in contracts['layouts'].items():
            print(f'{k:5} {v["name"]:24} {v["anchor"]:7} {v["maxBlocks"]:<6} {", ".join(v["grounds"])}')
        return 0
    strict = '--strict' in argv
    pats = [a for a in argv if not a.startswith('-')]
    if not pats:
        print(__doc__); return 0
    files = [f for p in pats for f in (glob.glob(p) or [p])]
    total_e = total_w = 0
    for path in files:
        if not os.path.exists(path):
            print(f'{RED}not found{OFF} {path}'); total_e += 1; continue
        rep, n = validate_file(path, contracts, rules)
        head = f'{os.path.relpath(path, ROOT)}  {DIM}({n} slides){OFF}'
        if not rep.errors and not rep.warnings:
            print(f'{GRN}PASS{OFF}  {head}')
        else:
            print(f'{RED if rep.errors else YEL}{"FAIL" if rep.errors else "WARN"}{OFF}  {head}')
        for where, msg, fix in rep.errors:
            print(f'  {RED}✗{OFF} {where}: {msg}')
            if fix: print(f'    {DIM}→ {fix}{OFF}')
        for where, msg, fix in rep.warnings:
            print(f'  {YEL}!{OFF} {where}: {msg}')
            if fix: print(f'    {DIM}→ {fix}{OFF}')
        total_e += len(rep.errors); total_w += len(rep.warnings)
    print(f'\n{total_e} error(s), {total_w} warning(s)')
    return 1 if total_e or (strict and total_w) else 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
