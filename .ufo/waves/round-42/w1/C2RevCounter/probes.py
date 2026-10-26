#!/usr/bin/env python3
"""C2RevCounter probes: unit probes + fixture variants against the frozen counter
tools/check-scrub-record-r42.py (byte-identical at a84fc9de and f50c28d8)."""
import importlib.util, json, os, re, shutil, subprocess, sys

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
TREE = 'f50c28d83e1832ecd7eba765caace531f45d6b27'
SCRATCH = '/fast/scratch/hyaku/tsukuroi-r42/C2RevCounter'
FX = os.path.join(SCRATCH, 'fx.probes')
COUNTER = os.path.join(SCRATCH, 'counter-a84.py')
WAVE = '.ufo/waves/round-42'
ENTRY = 'corpus/knowledge/btrfs-scrub-record-r42.md'
IDT = ['-c', 'user.name=fixture', '-c', 'user.email=fixture@invalid']


def git(d, *a):
    return subprocess.run(['git', '-C', d, *a], capture_output=True, text=True)


def run_counter(rev):
    p = subprocess.run([sys.executable, COUNTER, '--revision', rev, '--lane', FX],
                       capture_output=True, text=True)
    out = p.stdout.strip()
    if out:
        try:
            j = json.loads(out.splitlines()[-1])
        except Exception:
            j = {'_parse_error': out[-200:]}
    else:
        j = {}
    tb = (p.stderr or '').strip().splitlines()
    return {'exit': p.returncode, 'json': j, 'stderr_tail': tb[-1] if tb else ''}


def compact(j):
    if not j:
        return 'NO-JSON'
    return ('verdict=%s rows=%s q=%s nov=%s host=%s src=%s v=%s base=%s snap=%s cap=%s tb=%s/%s' % (
        j.get('verdict'), j.get('rows'), j.get('quotes_ok'), j.get('novelty_ok'), j.get('host_ok'),
        j.get('sources_ok'), j.get('verdicts_ok'), j.get('novelty_base_hits'),
        j.get('snapshots_ok'), j.get('capture_ok'), j.get('transcripts_bound'), j.get('transcripts_checked')))


spec = importlib.util.spec_from_file_location('c2c', COUNTER)
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)

print('== UNIT: QUOTE_RE')
cases = [
    ('embedded dquotes clean end', '**Quote.** `S237` scrub.c:67: "#define SCRUB_DATA_FILE "/var/lib/btrfs/scrub.status""'),
    ('trailing annotation', '**Quote.** `S237` scrub.c:67: "#define SCRUB_DATA_FILE "/var/lib/btrfs/scrub.status"" (verified)'),
    ('text ends with dquote', '**Quote.** `S237` scrub.c:67: "abc""'),
    ('trailing space', '**Quote.** `S237` scrub.c:67: "abc" '),
    ('missing closing', '**Quote.** `S237` scrub.c:67: "abc'),
    ('empty text', '**Quote.** `S237` scrub.c:67: ""'),
    ('two-digit id', '**Quote.** `S23` scrub.c:67: "abc"'),
    ('wrong file', '**Quote.** `S237` other.c:67: "abc"'),
    ('fragment quote', '**Quote.** `S237` scrub.c:450: "b"'),
]
for name, ln in cases:
    m = C.QUOTE_RE.match(ln)
    print(' %-28s -> %s' % (name, ('MATCH q=%r' % m.group(4)) if m else 'NO-MATCH'))

print('== UNIT: all real entry quotes vs frozen snapshots')
entry = open(os.path.join(SCRATCH, 'entry-rev.md'), errors='replace').read()
src = {}
for f in C.SNAP:
    b = git(LANE, 'show', '%s:%s/frozen/src/%s' % (TREE, WAVE, f)).stdout
    src[f] = (b if isinstance(b, str) else b.decode(errors='replace')).split('\n')
secs = C.sections(entry)
tot = 0
nq = 0
for row in ('SC1', 'SC2', 'SC3', 'SC4', 'SC5'):
    for ln in secs[row]:
        if not ln.startswith('**Quote.**'):
            continue
        nq += 1
        m = C.QUOTE_RE.match(ln)
        if not m:
            print(' %s UNPARSED: %r' % (row, ln))
            tot += 1
            continue
        sid, f, n, q = m.group(1), m.group(2), int(m.group(3)), m.group(4)
        if q not in src[f][n - 1]:
            print(' %s MISS %s:%s q=%r' % (row, f, n, q))
            tot += 1
print(' quote lines=%d failing-substring=%d' % (nq, tot))

print('== UNIT: registry edge cases')
reg_cases = [
    ('normal 11', '| S237 | src | code | A | sc | an | te | mined | 2026-10-26 | on-release | ' + ENTRY + ' |'),
    ('empty first cell', '|| S237 | src | code | A | sc | an | te | mined | 2026-10-26 | on-release | ' + ENTRY + ' |'),
    ('empty last cell', '| S237 | src | code | A | sc | an | te | mined | 2026-10-26 | on-release | |'),
    ('pipe inside cell', '| S237 | sr|c | code | A | sc | an | te | mined | 2026-10-26 | on-release | ' + ENTRY + ' |'),
    ('4-space indent', '    | S237 | src | code | A | sc | an | te | mined | 2026-10-26 | on-release | ' + ENTRY + ' |'),
    ('backticked id', '| `S237` | src | code | A | sc | an | te | mined | 2026-10-26 | on-release | ' + ENTRY + ' |'),
]
for name, ln in reg_cases:
    r = C.registry(ln)
    print(' %-18s -> keys=%s cells=%s' % (name, list(r.keys()), [len(v) for v in r.values()]))

print('== UNIT: VERDICT_RE')
for s in ('ROW SC1 VERDICT: holds', 'ROW SC1 VERDICT: holds-X', 'ROW SC1 VERDICT: holdsup',
          'ROW SC11 VERDICT: holds', 'x ROW SC1 VERDICT: fails y'):
    ms = [m.group(0) for m in C.VERDICT_RE.finditer(s)]
    print(' %-30r -> %s' % (s, ms))

print('== UNIT: sections duplicate + extra')
dup = '# t\n\n## SC1\n\n**Statement.** a\n\n## SC1\n\n**Statement.** b\n\n## SC6\n\n**Statement.** c\n'
s = C.sections(dup)
print(' SC1-lines=%d SC6-collected=%s' % (len(s.get('SC1', [])), 'SC6' in s))

# ---------- fixture variants ----------
if os.path.exists(FX):
    shutil.rmtree(FX)
subprocess.run(['git', 'clone', '-q', '--shared', LANE, FX], check=True)
tl = os.path.realpath(git(FX, 'rev-parse', '--show-toplevel').stdout.strip())
assert tl == os.path.realpath(FX), tl
git(FX, 'remote', 'remove', 'origin')


def checkout():
    git(FX, 'checkout', '-q', '--force', '--detach', TREE)
    git(FX, 'clean', '-qfdx')


def commit(msg):
    git(FX, 'add', '-A')
    p = subprocess.run(['git', '-C', FX, *IDT, 'commit', '-q', '--allow-empty', '-m', msg],
                       capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    return git(FX, 'rev-parse', 'HEAD').stdout.strip()


def scripted_entry(host_line=None):
    srcw = {f: open(os.path.join(FX, WAVE, 'frozen/src', f), errors='replace').read().split('\n')
            for f in C.SNAP}
    sid = {'scrub.c': 'S237', 'CHANGES': 'S238'}
    out = ['source: S237 S238 S239', 'verified-at: 2026-10-26', 'recheck: on-release', '',
           '# scripted control entry', '']
    for row, sp in C.ROWS.items():
        f, lo, hi = sp['windows'][0]
        n = next(i for i in range(lo, hi + 1) if srcw[f][i - 1].strip() and '"' not in srcw[f][i - 1])
        q = srcw[f][n - 1].strip()
        host = host_line or '**Host reading.** capture.txt:1 holds the time.'
        out += ['## %s' % row, '', '**Statement.** The record concerns %s in every case.' % sp['token'], '',
                '**Quote.** `%s` %s:%d: "%s"' % (sid[f], f, n, q), '', host, '']
    return '\n'.join(out) + '\n'


def flip_rows(entry_name):
    p = os.path.join(FX, 'corpus/SOURCES.md')
    lines = open(p).read().split('\n')
    for i, ln in enumerate(lines):
        m = re.match(r'^\|\s*(S23[7-9])\s*\|', ln)
        if m:
            cells = ln.strip().strip('|').split('|')
            cells[7] = ' mined '
            cells[10] = ' %s ' % entry_name
            lines[i] = '|' + '|'.join(cells) + '|'
    open(p, 'w').write('\n'.join(lines))


def seats():
    for n in range(1, 6):
        yield 'C2RevSC%d' % n, 'reviewer', 'SC%d' % n
        yield 'C2CritSC%d' % n, 'critic', 'SC%d' % n


def write_reports(verdicts, raw=None):
    d = os.path.join(FX, WAVE, 'w2')
    os.makedirs(d, exist_ok=True)
    for name, _r, row in seats():
        txt = raw.get(name) if raw and name in raw else '# %s\n\nROW %s VERDICT: %s\n' % (
            name, row, verdicts.get(name, 'holds'))
        open(os.path.join(d, '%s.md' % name), 'w').write(txt)


def write_records(verdicts, dispatch=True, outputs=None, tasks=None):
    res = {'lane': 'tsukuroi', 'round': '42', 'wave': 'w2', 'seats': 10,
           'results': [{'name': n, 'agent': r,
                        'output': (outputs or {}).get(n, 'done. ROW %s VERDICT: %s' % (row, verdicts.get(n, 'holds'))),
                        'note': None} for n, r, row in seats()]}
    json.dump(res, open(os.path.join(FX, WAVE, 'w2-results.json'), 'w'))
    if tasks is None:
        tasks = [{'name': n, 'agent': r, 'task': 'forged'} for n, r, _ in seats()] if dispatch else \
                [{'name': 'Other', 'agent': 'scout', 'task': 'x'}]
    json.dump({'taskCall': {'context': 'forged', 'tasks': tasks}},
              open(os.path.join(FX, WAVE, 'w2-dispatch.json'), 'w'))


def variant(name, build):
    checkout()
    build()
    rev = commit('probe %s' % name)
    r = run_counter(rev)
    print('V-%-28s exit=%s %s %s' % (name, r['exit'], compact(r['json']),
                                     ('stderr=' + r['stderr_tail']) if r['stderr_tail'] else ''))


def base_k3():
    open(os.path.join(FX, ENTRY), 'w').write(scripted_entry())
    flip_rows(ENTRY)
    write_reports({})
    write_records({})


variant('A-k3-replica', base_k3)


def vB():
    base_k3()
    rd = os.path.join(FX, WAVE, 'residual')
    os.makedirs(rd, exist_ok=True)
    json.dump({'taskCall': {'tasks': [{'name': 'C2RevSC1c', 'agent': 'reviewer', 'task': 'x'}]}},
              open(os.path.join(FX, WAVE, 'residual-dispatch.json'), 'w'))
    json.dump({'results': [{'name': 'C2RevSC1c', 'agent': 'reviewer', 'output': 'done. ROW SC1 VERDICT: fails'}]},
              open(os.path.join(FX, WAVE, 'residual-results.json'), 'w'))
    open(os.path.join(rd, 'C2RevSC1c.md'), 'w').write('# C2RevSC1c\n\nROW SC1 VERDICT: fails\n')


variant('B-residual-fails-both-holds', vB)


def vC():
    base_k3()
    write_reports({}, raw={'C2RevSC1': '# C2RevSC1\n\nROW SC1 VERDICT: holds-X\n'})
    write_records({}, outputs={'C2RevSC1': 'done. ROW SC1 VERDICT: holds-X'})


variant('C-holds-prefix-word', vC)


def vJ():
    base_k3()
    write_reports({}, raw={'C2CritSC1': '# C2CritSC1\n\nxROW SC1 VERDICT: holdsy\n'})


variant('J-report-substring', vJ)


def vD():
    base_k3()
    write_records({}, outputs={'C2CritSC1': 'done. ROW SC1 VERDICT: holds\nagain ROW SC1 VERDICT: holds'})


variant('D-two-verdict-lines', vD)


def vE():
    base_k3()
    open(os.path.join(FX, WAVE, 'frozen/src/CHANGES'), 'w').write('corrupted\n')


variant('E-changes-corrupted', vE)


def vF():
    open(os.path.join(FX, ENTRY), 'w').write(
        scripted_entry(host_line='**Host reading.** ok (capture.txt:1) and bogus (capture.txt:99999).'))
    flip_rows(ENTRY)
    write_reports({})
    write_records({})


variant('F-host-second-ref-bogus', vF)


def vG():
    base_k3()
    tasks = ['x'] + [{'name': n, 'agent': r, 'task': 't'} for n, r, _ in seats()]
    json.dump({'taskCall': {'tasks': tasks}}, open(os.path.join(FX, WAVE, 'w2-dispatch.json'), 'w'))


variant('G-nondict-task', vG)


def vH():
    base_k3()
    p = os.path.join(FX, 'corpus/SOURCES.md')
    lines = open(p).read().split('\n')
    for i, ln in enumerate(lines):
        if re.match(r'^\|\s*S237\s*\|', ln):
            lines[i] = ln.replace('cmds/scrub.c lines 67-70', 'cmds/scrub.c lines 67|70', 1)
            break
    open(p, 'w').write('\n'.join(lines))


variant('H-pipe-in-cell', vH)


def vI():
    open(os.path.join(FX, ENTRY), 'w').write(scripted_entry())
    p = os.path.join(FX, ENTRY)
    lines = open(p).read().split('\n')
    for i, ln in enumerate(lines):
        if ln.startswith('**Quote.**'):
            lines[i] = ln + ' (checked)'
            break
    open(p, 'w').write('\n'.join(lines))
    flip_rows(ENTRY)
    write_reports({})
    write_records({})


variant('I-quote-trailing-annotation', vI)


def vK():
    open(os.path.join(FX, ENTRY), 'w').write(scripted_entry())
    p = os.path.join(FX, ENTRY)
    txt = open(p).read()
    # replace SC2's quote with line 69 (real text, outside SC2 window 826-895)
    old = [ln for ln in txt.split('\n') if ln.startswith('**Quote.**')][1]
    new = '**Quote.** `S237` scrub.c:69: "#define SCRUB_FILE_VERSION_PREFIX "scrub status""'
    txt = txt.replace(old, new, 1)
    open(p, 'w').write(txt)
    flip_rows(ENTRY)
    write_reports({})
    write_records({})


variant('K-only-quote-out-of-window', vK)

print('DONE')
