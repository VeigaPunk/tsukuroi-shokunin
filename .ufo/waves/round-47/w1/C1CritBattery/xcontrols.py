#!/usr/bin/env python3
"""C1CritBattery (seat C1-R4): build and score MISSING round-47 battery controls.

New controls (all fixtures clone the lane at IMPL=77e9e2b2, frozen counter):
  X1 wrong-row-hash   GR1 reviewer binds SECTION SHA256 of GR2 -> counter must FAIL closed
  X2 partly-current   all six a-seats bind 'partly' on current hashes -> quorum must FAIL closed
  X3 results-status   results entries say 'failed'/'timeout' -> counter ignores status (PASS = gap)
  X4 ws-only-distinct bodies differ only by trailing whitespace -> K23 byte-level (PASS = gap)
  X5 real-wrong-line  citation cmdline.c:1 resolves but is the wrong line for the claim (PASS = gap)
"""
import hashlib, json, os, shutil, subprocess, sys

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
IMPL = '77e9e2b2e96b85d8f048ae2087e246a542b71611'
HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.path.join(HERE, 'xfix')
ENTRY = 'corpus/knowledge/btrfs-scrub-grounding-r45.md'
CITE = {'GR1': 'cmdline.c:156', 'GR2': 'scrub.c:3147', 'GR3': 'systemd.kill.xml:68'}


def sh(*a, **kw):
    return subprocess.run(a, capture_output=True, text=True, **kw)


def fixture(name):
    d = os.path.join(SCRATCH, name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    assert sh('git', 'clone', '-q', '--shared', LANE, d).returncode == 0
    sh('git', '-C', d, 'remote', 'remove', 'origin')
    top = sh('git', '-C', d, 'rev-parse', '--show-toplevel').stdout.strip()
    assert top == d, f'{name}: toplevel {top} != {d}'
    assert sh('git', '-C', d, 'checkout', '-q', IMPL).returncode == 0
    return d


def commit_all(d, msg):
    sh('git', '-C', d, 'add', '-A')
    assert sh('git', '-C', d, 'commit', '-q', '--no-verify', '-m', msg).returncode == 0
    return sh('git', '-C', d, 'rev-parse', 'HEAD').stdout.strip()


def counter(d, rev):
    p = subprocess.run(['python3', os.path.join(d, 'tools/check-scrub-admission-r47.py'),
                        '--revision', rev, '--lane', d], capture_output=True, text=True)
    try:
        return p.returncode, json.loads(p.stdout.strip().splitlines()[-1]), len(p.stdout)
    except Exception:
        return p.returncode, {'error': 'unparseable', 'raw': p.stdout[:200]}, len(p.stdout)


def write(p, t):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w').write(t)


def section_hash(d, row):
    p = subprocess.run(['python3', os.path.join(d, 'tools/check-scrub-admission-r47.py'),
                        '--revision', 'HEAD', '--lane', d, '--section-hash'],
                       capture_output=True, text=True)
    return json.loads(p.stdout)['section_sha256'][row]


def report(row, hsh, verdict, seed, tail=''):
    body = ('Evidence. ' + seed + ' ') * 40 + f' cites {CITE[row]}.\n'
    return f'ROW {row} VERDICT: {verdict}\nSECTION SHA256: {hsh}\n{body}{tail}'


def add_wave(d, wave, seats, statuses=None):
    tasks = [{'name': s, 'agent': r, 'task': f'counted seat {s}'} for s, r, *_ in seats]
    write(os.path.join(d, f'.ufo/waves/round-47/{wave}-dispatch.json'),
          json.dumps({'taskCall': {'context': 'fixture', 'tasks': tasks}}))
    results = [{'name': s, 'agent': r, 'id': f'fx-{s}',
                'status': (statuses or {}).get(s, 'completed'), 'final output': 'x'}
               for s, r, *_ in seats]
    write(os.path.join(d, f'.ufo/waves/round-47/{wave}-results.json'),
          json.dumps({'results': results}))
    for s, r, row, verdict, hsh, seed, tail in seats:
        write(os.path.join(d, f'.ufo/waves/round-47/{wave}/{s}.md'),
              report(row, hsh, verdict, seed, tail))


def add_marks(d):
    e = open(os.path.join(d, ENTRY)).read() + '\n## Gate status — round 47 (GR1-GR3 admitted)\n'
    open(os.path.join(d, ENTRY), 'w').write(e)
    sk = open(os.path.join(d, 'SKILL.md')).read() + '\n## Scrub grounding — round 47 admission\n'
    open(os.path.join(d, 'SKILL.md'), 'w').write(sk)
    rd = open(os.path.join(d, 'corpus/README.md')).read() + \
        '\n- `corpus/knowledge/btrfs-scrub-grounding-r45.md` admitted round 47\n'
    open(os.path.join(d, 'corpus/README.md'), 'w').write(rd)


def standard_seats(h, verdict='holds', seeds=None):
    out = []
    for row in ('GR1', 'GR2', 'GR3'):
        n = row[2:]
        sr, sc = (seeds or {}).get(row, (f'{row} reviewer a reads the row carefully. ',
                                         f'{row} critic a attacks the row hard. '))
        out += [(f'R47RevGR{n}a', 'reviewer', row, verdict, h[row], sr, ''),
                (f'R47CritGR{n}a', 'critic', row, verdict, h[row], sc, '')]
    return out


results = []


def rec(name, expect, observed, detail=''):
    results.append({'control': name, 'expect': expect, 'observed': observed,
                    'as_expected': observed == expect, 'detail': detail})
    print(f'{"OK " if observed == expect else "BAD"} {name}: expect {expect}, observed {observed} {detail[:160]}')


# X1 wrong-row hash: GR1 reviewer binds GR2's section hash
d = fixture('x1-wrong-row-hash')
h = {r: section_hash(d, r) for r in ('GR1', 'GR2', 'GR3')}
seats = standard_seats(h)
seats[0] = ('R47RevGR1a', 'reviewer', 'GR1', 'holds', h['GR2'], 'GR1 reviewer a reads the row carefully. ', '')
add_wave(d, 'w1', seats); add_marks(d); rev = commit_all(d, 'x1 wrong-row hash')
rc, out, _ = counter(d, rev)
g1 = out.get('per_row', {}).get('GR1', {})
rec('C1-X1 wrong-row hash', 'FAIL', out.get('verdict'),
    f"rc={rc} GR1 bound_on_current={g1.get('bound_on_current')} row_ok={g1.get('row_ok')}")
shutil.rmtree(d, ignore_errors=True)

# X2 partly on current bytes, everything else clean
d = fixture('x2-partly-current')
h = {r: section_hash(d, r) for r in ('GR1', 'GR2', 'GR3')}
seats = standard_seats(h, verdict='partly')
add_wave(d, 'w1', seats); add_marks(d); rev = commit_all(d, 'x2 partly current')
rc, out, _ = counter(d, rev)
g1 = out.get('per_row', {}).get('GR1', {})
vs = {s: v.get('verdict') for s, v in g1.get('seats', {}).items()}
rec('C1-X2 partly on current bytes', 'FAIL', out.get('verdict'),
    f"rc={rc} GR1 verdicts={vs} row_ok={g1.get('row_ok')}")
shutil.rmtree(d, ignore_errors=True)

# X3 results status failed/timeout: counter must still admit (boundary = gap)
d = fixture('x3-results-status')
h = {r: section_hash(d, r) for r in ('GR1', 'GR2', 'GR3')}
seats = standard_seats(h)
statuses = {'R47RevGR1a': 'failed', 'R47CritGR1a': 'timeout',
            'R47RevGR2a': 'failed', 'R47CritGR2a': 'error',
            'R47RevGR3a': 'killed', 'R47CritGR3a': 'failed'}
add_wave(d, 'w1', seats, statuses=statuses); add_marks(d); rev = commit_all(d, 'x3 results status')
rc, out, _ = counter(d, rev)
rec('C1-X3 results status ignored (gap)', 'PASS', out.get('verdict'),
    f"rc={rc} verdicts_ok={out.get('verdicts_ok')} (all results entries status failed/timeout/error/killed)")
shutil.rmtree(d, ignore_errors=True)

# X4 whitespace-only distinct bodies within a row (gap: K23 is byte-level)
d = fixture('x4-ws-only-distinct')
h = {r: section_hash(d, r) for r in ('GR1', 'GR2', 'GR3')}
seeds = {row: (f'{row} identical substance. ', f'{row} identical substance.  ') for row in ('GR1', 'GR2', 'GR3')}
seats = standard_seats(h, seeds=seeds)
add_wave(d, 'w1', seats); add_marks(d); rev = commit_all(d, 'x4 whitespace-only distinct')
rc, out, _ = counter(d, rev)
g1 = out.get('per_row', {}).get('GR1', {})
rec('C1-X4 whitespace-only distinct (gap)', 'PASS', out.get('verdict'),
    f"rc={rc} GR1 distinct_bodies={g1.get('distinct_bodies')} row_ok={g1.get('row_ok')}")
shutil.rmtree(d, ignore_errors=True)

# X5 real-but-wrong citation line: cmdline.c:1 resolves, does not support the claim (gap)
d = fixture('x5-real-wrong-line')
h = {r: section_hash(d, r) for r in ('GR1', 'GR2', 'GR3')}
seats = standard_seats(h)
seats[0] = ('R47RevGR1a', 'reviewer', 'GR1', 'holds', h['GR1'],
            'GR1 reviewer a reads the row carefully. ',
            ' supplemental citation cmdline.c:1\n')
add_wave(d, 'w1', seats); add_marks(d); rev = commit_all(d, 'x5 real wrong line')
rc, out, _ = counter(d, rev)
g1 = out.get('per_row', {}).get('GR1', {})
rec('C1-X5 real-but-wrong citation line (gap)', 'PASS', out.get('verdict'),
    f"rc={rc} GR1 citations_ok={g1.get('citations_ok')} row_ok={g1.get('row_ok')}")
shutil.rmtree(d, ignore_errors=True)

out_path = os.path.join(HERE, 'xcontrols-summary.jsonl')
with open(out_path, 'w') as f:
    for r in results:
        f.write(json.dumps(r, sort_keys=True) + '\n')
bad = [r['control'] for r in results if not r['as_expected']]
print(f'\nxcontrols: {len(results)} controls, {len(bad)} not as expected: {bad}')
sys.exit(0 if not bad else 1)
