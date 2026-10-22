#!/usr/bin/env python3
"""Round-29 w2 seat CritOwedV2Shapes: new should-fail shapes against counter v2.

Data: the sandbox clone REPO checked out at BASE (the landed lane tip, 12 of 12 marked).
Each shape: checkout -f BASE, mutate one item's marker or its support, commit in the sandbox,
run the counter at HEAD with --lane REPO, record the item's ok/why.  Every git child runs with
all inherited GIT_* removed and global/system config pointed at /dev/null.
"""
import hashlib, json, os, re, subprocess, sys

REPO = '/fast/scratch/hyaku/tsukuroi-r29/CritOwedV2Shapes/repo'
BASE = '10d5288fc1051364e711203855e7c53710dfcc21'
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_SYSTEM='/dev/null')
COUNTER = os.path.join(REPO, 'tools/check-owed-statements-r29.py')

def git(*a):
    p = subprocess.run(['git', '-C', REPO, '-c', 'user.name=shape', '-c', 'user.email=shape@sandbox', *a],
                       capture_output=True, text=True, env=ENV)
    if p.returncode:
        raise SystemExit(f'git {a} failed: {p.stderr}')
    return p.stdout.strip()

def rd(p):
    return open(os.path.join(REPO, p), encoding='utf-8').read()

def wr(p, s):
    full = os.path.join(REPO, p)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(s)

OOM, KILL = 'corpus/knowledge/oom-event-plane.md', 'corpus/knowledge/kill-event-deep-r8.md'
SKILL, DRV = 'SKILL.md', 'corpus/knowledge/driver-firmware-plane.md'
MP, SH = 'corpus/knowledge/memory-pressure-r25.json', 'corpus/knowledge/storage-health-r26.json'
SRC = 'corpus/SOURCES.md'
FILE = {'O01': OOM, 'O02': OOM, 'O03': KILL, 'O04': KILL, 'O05': SKILL, 'O08': DRV}

def marker_line(f, iid):
    return next(l for l in rd(f).split('\n') if l.startswith(f'[R29-OWED-{iid}]'))

def md_sub(iid, fn):
    f = FILE[iid]
    old = marker_line(f, iid)
    wr(f, rd(f).replace(old, fn(old), 1))

def set_field(line, key, val):
    """Replace ' | key: ... ' segment of a Markdown marker."""
    if key == 'basis':
        return re.sub(r'\| basis: .*$', '| basis: ' + val, line)
    if key == 'now':
        return re.sub(r'\| now: .*? \| basis:', lambda m: '| now: ' + val + ' | basis:', line, count=1)
    if key == 'verdict':
        return re.sub(r'verdict: [a-z]+', 'verdict: ' + val, line, count=1)
    raise KeyError(key)

def json_line_edit(f, iid, fn):
    """Edit the single physical line holding the item's corrections_r29 object (raw text)."""
    lines = rd(f).split('\n')
    i = next(i for i, l in enumerate(lines) if f'"id": "R29-OWED-{iid}"' in l)
    lines[i] = fn(lines[i])
    wr(f, '\n'.join(lines))

def json_marker_update(f, iid, **kw):
    def fn(l):
        trail = ',' if l.rstrip().endswith(',') else ''
        obj = json.loads(l.strip().rstrip(','))
        obj.update(kw)
        return '  ' + json.dumps(obj, ensure_ascii=False) + trail
    json_line_edit(f, iid, fn)

def add_source(row):
    s = rd(SRC).rstrip('\n').split('\n')
    last = max(i for i, l in enumerate(s) if re.match(r'^\| S\d{3} \|', l))
    s.insert(last + 1, row)
    wr(SRC, '\n'.join(s) + '\n')

def src_row(sid, title, status, used_by):
    return (f'| {sid} | {title} | docs | A | {title} | line 1 | teaches nothing about OOM | {status} | '
            f'2026-10-22 | on-release | {used_by} |')

DIGEST = {
    'O02': '34c5baaf20a2cda95e39ad956c5f045f27b9fb012f83211daf2e661766363fe7',
    'O04': 'd1a13e5d835e98b9be17e8ff2aabf4ff6e351ba9cb105f2c7e7d35c34e186cfc',
}
ANCH = {'O02': 'the +200 band is chosen first', 'O04': 'the +200 band is scanned first'}

def hide_base_line(iid, wrap_open, wrap_close):
    """Rewrite the visible base statement; keep a byte-exact copy only inside a hidden block."""
    f = FILE[iid]
    lines = rd(f).split('\n')
    i = next(i for i, l in enumerate(lines)
             if 'R29-OWED-' not in l and hashlib.sha256(l.encode()).hexdigest() == DIGEST[iid])
    base = lines[i]
    lines[i] = base.replace(ANCH[iid], 'the highest-badness task is chosen')
    lines += ['', wrap_open, base, wrap_close, '']
    wr(f, '\n'.join(lines))

def s_n1():
    add_source(src_row('S152', 'The Rust Programming Language, chapter 3 (variables)', 'mined', f'{OOM}, {KILL}'))
    md_sub('O01', lambda l: set_field(l, 'basis', 'S152'))

def s_n2():
    s = rd(SRC).split('\n')
    i = next(i for i, l in enumerate(s) if l.startswith('| S148 |'))
    cells = s[i].split(' | ')
    s[i] = s[i].replace(' | mined | ', ' | rejected | ', 1)
    assert ' | rejected | ' in s[i]
    wr(SRC, '\n'.join(s))
    add_source(src_row('S148', 'Stryker Mutator docs (duplicate id)', 'mined', f'{OOM}, {KILL}'))
    md_sub('O03', lambda l: set_field(l, 'basis', 'S148'))

def s_n3():
    add_source(src_row('S\uff11\uff14\uff19', 'Fullwidth-digit look-alike of S149, an unrelated page', 'mined', f'{OOM}, {KILL}'))
    md_sub('O04', lambda l: set_field(l, 'basis', 'S\uff11\uff14\uff19'))

def s_n4():
    good = marker_line(SKILL, 'O05')
    fake = (good.replace('[R29-OWED-O05]', '[R29-OWED-\u041e05]')
            .replace('verdict: qualified', 'verdict: rebutted'))
    fake = set_field(fake, 'now', 'the original sentence stands as written because no unit in the chain carries kill at all today')
    wr(SKILL, rd(SKILL).replace(good, good + '\n\n' + fake, 1))

def s_n5():
    md_sub('O05', lambda l: '| note | ' + l + ' |')

def s_n6():
    md_sub('O08', lambda l: '`' + l + '`')

def s_n7():
    md_sub('O08', lambda l: '~~' + l + '~~')

def s_n8():
    md_sub('O05', lambda l: 'Rejected draft, NOT applied, ignore: ' + l)

def s_n9():
    md_sub('O08', lambda l: '\n    ' + l + '\n')

def s_n10():
    md_sub('O05', lambda l: '```inline```\n\n```text\n' + l + '\n```')

def s_n11():
    hide_base_line('O02', '<!--', '-->')

def s_n12():
    hide_base_line('O04', '```text', '```')

def s_n13():
    md_sub('O08', lambda l: set_field(l, 'now', 'alpha bravo charlie delta echo foxtrot golf hotel india juliet kilo lima'))

def s_n14():
    json_marker_update(SH, 'O11', now='1 2 3 4 5 6 7 8 9 10 11 12')

def s_n15():
    json_marker_update(SH, 'O10', now='\u200b'.join('abcdefghijkl'))

def s_n16():
    md_sub('O04', lambda l: set_field(l, 'now', 'Confirmed again: the +200 band, is scanned first by the kernel on this host, exactly as written before'))

def s_n17():
    md_sub('O05', lambda l: set_field(l, 'basis', '`./tools/check-owed-statements-r29.py:1`'))

def s_n18():
    md_sub('O05', lambda l: set_field(l, 'basis', '`SCORECARD.md:1`'))

def s_n19():
    wr('notes/trust-me.md', 'trust me, this correction is right\n')
    json_marker_update(SH, 'O09', basis=['notes/trust-me.md:1'])

def s_n20():
    json_marker_update(SH, 'O11', applied=False, status='withdrawn', superseded_by='nothing; this correction is retracted')

def s_n21():
    json_line_edit(SH, 'O12', lambda l: l.replace('"verdict": ', '"verdict": "withdrawn", "verdict": ', 1))

def s_n22():
    d = json.loads(rd(SH))
    for c in d['corrections_r29']:
        if c['id'] == 'R29-OWED-O09':
            c['basis'] = ['PLACEHOLDER']
    txt = json.dumps(d, indent=1, ensure_ascii=False) + '\n'
    lines = txt.split('\n')
    start = next(i for i, l in enumerate(lines) if '"R29-OWED-O09"' in l)
    nline = next(i for i in range(start, len(lines)) if lines[i].lstrip().startswith('"now"')) + 1
    wr(SH, txt.replace('"PLACEHOLDER"', f'"{SH}:{nline}"'))

def s_n23():
    md_sub('O02', lambda l: set_field(l, 'basis', 'not S149; no source was read for this line'))

def s_n24():
    md_sub('O08', lambda l: '<div hidden>\n\n' + l + '\n\n</div>')

def s_n25():
    md_sub('O05', lambda l: set_field(l, 'basis', '`corpus/../tools/check-owed-statements-r29.py:1`'))

def s_n26():
    md_sub('O05', lambda l: set_field(l, 'now', 'see the O01 note in oom-event-plane.md; this line keeps twelve words here for the floor'))

def s_p1():
    f = SKILL
    good = marker_line(f, 'O05')
    wr(f, rd(f).replace(good, good + '\n\nThe correction R29-OWED-O05 above supersedes the chain wording.', 1))

SHAPES = [
    ('N1 kernel item cites a NEW mined row about something unrelated (S152, Rust book)', 'O01', 'fail', 'M6/M7 relevance', s_n1),
    ('N2 duplicate source id: real S148 set rejected, second S148 row (unrelated, mined) appended', 'O03', 'fail', 'M6 registry identity', s_n2),
    ('N3 fullwidth-digit look-alike id S\uff11\uff14\uff19 registered and cited', 'O04', 'fail', 'M6 registry identity', s_n3),
    ('N4 second, contradicting O05 marker with Cyrillic O in the id', 'O05', 'fail', 'M2', s_n4),
    ('N5 marker inside a Markdown table cell', 'O05', 'fail', 'M2 shape', s_n5),
    ('N6 marker inside an inline code span', 'O08', 'fail', 'M2 shape', s_n6),
    ('N7 marker struck through (~~...~~)', 'O08', 'fail', 'M2 shape', s_n7),
    ('N8 marker prefixed "Rejected draft, NOT applied, ignore:"', 'O05', 'fail', 'M2 shape', s_n8),
    ('N9 marker in a 4-space indented code block', 'O08', 'fail', 'M2 (code-block census)', s_n9),
    ('N10 fence parity flip: "```inline```" line, then marker inside a real ```text fence', 'O05', 'fail', 'M2 (fence census)', s_n10),
    ('N11 visible base statement rewritten; byte-exact copy kept only in an HTML comment', 'O02', 'fail', 'M1', s_n11),
    ('N12 visible base statement rewritten; byte-exact copy kept only in a fenced block', 'O04', 'fail', 'M1', s_n12),
    ('N13 now is 12 distinct meaningless words (NATO alphabet)', 'O08', 'fail', 'M5 meaning', s_n13),
    ('N14 now is the numbers 1 to 12 (JSON)', 'O11', 'fail', 'M5 word definition', s_n14),
    ('N15 now is one visible token split by 11 zero-width spaces (JSON)', 'O10', 'fail', 'M5 word definition', s_n15),
    ('N16 now restates the withdrawn anchor with one inserted comma (reaffirms it)', 'O04', 'fail', 'M5 anchor removal', s_n16),
    ('N17 path:LINE into tools/ via a ./ prefix (./tools/check-owed-statements-r29.py:1)', 'O05', 'fail', 'M6 tools/ exclusion', s_n17),
    ('N18 path:LINE at an unrelated non-blank line (SCORECARD.md:1, the title)', 'O05', 'fail', 'M6 relevance', s_n18),
    ('N19 path:LINE at a file fabricated in the same commit (notes/trust-me.md:1)', 'O09', 'fail', 'M6 provenance', s_n19),
    ('N20 JSON marker with extra keys applied=false, status=withdrawn, superseded_by', 'O11', 'fail', 'M2 key set', s_n20),
    ('N21 JSON marker with duplicate key: "verdict": "withdrawn", then "verdict": "corrected"', 'O12', 'fail', 'M2/M4 duplicate keys', s_n21),
    ('N22 JSON pretty-printed; basis cites the line of its own now value (self-citation)', 'O09', 'fail', 'M6 self-citation', s_n22),
    ('N23 basis names S149 only in a negation ("not S149; no source was read")', 'O02', 'fail', 'M6 citation sense', s_n23),
    ('N24 marker inside <div hidden> (not rendered)', 'O08', 'fail', 'M2 hidden HTML', s_n24),
    ('N25 path:LINE into tools/ via corpus/../tools/', 'O05', 'fail', 'M6 tools/ exclusion', s_n25),
    ('N26 now points elsewhere and pads to the floor ("see the O01 note ... twelve words here")', 'O05', 'fail', 'M5 meaning', s_n26),
    ('P1 should-pass: prose sentence names R29-OWED-O05 after the marker', 'O05', 'pass', 'M2 over-strict', s_p1),
]

def counter():
    p = subprocess.run([sys.executable, COUNTER, '--revision', 'HEAD', '--lane', REPO],
                       capture_output=True, text=True, env=ENV)
    rows, summ = {}, None
    for ln in p.stdout.splitlines():
        try:
            d = json.loads(ln)
        except ValueError:
            continue
        if 'id' in d:
            rows[d['id']] = d
        else:
            summ = d
    return p.returncode, rows, summ, p.stderr.strip().splitlines()[-1:]

def main():
    git('checkout', '-q', '-f', BASE)
    rc, rows, summ, err = counter()
    out = [{'shape': 'C0 landed tip unchanged', 'commit': BASE, 'exit': rc, 'marked': summ and summ['marked'],
            'counter_sha256': summ and summ['counter_sha256']}]
    for name, iid, expect, rule, fn in SHAPES:
        git('checkout', '-q', '-f', BASE)
        git('clean', '-qfd')
        fn()
        git('add', '-A')
        git('commit', '-qm', name)
        sha = git('rev-parse', 'HEAD')
        rc, rows, summ, err = counter()
        r = rows.get(iid, {})
        counted = bool(r.get('ok'))
        out.append({'shape': name, 'item': iid, 'expect': expect, 'rule': rule, 'commit': sha, 'exit': rc,
                    'marked': summ and summ['marked'], 'item_ok': r.get('ok'), 'why': r.get('why'),
                    'verdict': ('counted' if counted else 'refused'),
                    'defect': (expect == 'fail') == counted,
                    'other_not_ok': {k: v.get('why') for k, v in rows.items() if not v['ok'] and k != iid},
                    'stderr_tail': err})
    git('checkout', '-q', '-f', BASE)
    for o in out:
        print(json.dumps(o, ensure_ascii=False))
    sf = [o for o in out[1:] if o['expect'] == 'fail']
    sp = [o for o in out[1:] if o['expect'] == 'pass']
    print(json.dumps({'should_fail_total': len(sf), 'should_fail_counted': sum(o['item_ok'] is True for o in sf),
                      'should_pass_total': len(sp), 'should_pass_refused': sum(o['item_ok'] is not True for o in sp),
                      'crashes': sum(o['marked'] is None for o in out)}))

if __name__ == '__main__':
    main()
