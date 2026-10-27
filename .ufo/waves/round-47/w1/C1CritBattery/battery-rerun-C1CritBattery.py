#!/usr/bin/env python3
"""Round-47 pre-data controls battery (L1, before any seat).

Each control is a fixture git clone of the lane at IMPL (3629c46a), carrying one mutation;
the frozen round-47 counters are run against it and the observed verdict must equal the
expectation declared in SCORECARD.md "Round 47 — declaration". Writes one JSONL summary.
Scratch root: $HYAKU_SCRATCH/tsukuroi-r47/controls (deleted per fixture after receipts copy).
"""
import hashlib, json, os, re, shutil, subprocess, sys, tempfile

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
IMPL = '77e9e2b2e96b85d8f048ae2087e246a542b71611'
BASE = '916019057147d7e9ba6b137647b2cee26decf4b8'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'battery-summary-r47.jsonl')
SCRATCH = os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku') + '/tsukuroi-r47/controls'
ENTRY = 'corpus/knowledge/btrfs-scrub-grounding-r45.md'


def sh(*args, cwd=None, env=None):
    e = dict(os.environ, **(env or {}))
    return subprocess.run(args, cwd=cwd, env=e, capture_output=True, text=True)


def fixture(name, rev=IMPL):
    d = os.path.join(SCRATCH, name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    if sh('git', 'clone', '-q', '--shared', LANE, d).returncode != 0:
        raise SystemExit(f'clone failed {name}')
    sh('git', '-C', d, 'remote', 'remove', 'origin')
    top = sh('git', '-C', d, 'rev-parse', '--show-toplevel').stdout.strip()
    assert top == d, f'{name}: toplevel {top} != {d}'
    sh('git', '-C', d, 'checkout', '-q', rev)
    sh('git', '-C', d, 'config', 'user.email', 'fixture@invalid')
    sh('git', '-C', d, 'config', 'user.name', 'fixture')
    return d


def commit_all(d, msg):
    sh('git', '-C', d, 'add', '-A')
    sh('git', '-C', d, 'commit', '-q', '--no-verify', '-m', msg)
    return sh('git', '-C', d, 'rev-parse', 'HEAD').stdout.strip()


def counter(d, rev='HEAD'):
    p = subprocess.run(['python3', os.path.join(d, 'tools/check-scrub-admission-r47.py'),
                        '--revision', rev, '--lane', d], capture_output=True, text=True)
    try:
        return p.returncode, json.loads(p.stdout.strip().splitlines()[-1]), len(p.stdout)
    except Exception:
        return p.returncode, {'error': 'unparseable stdout', 'stdout_len': len(p.stdout)}, len(p.stdout)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w').write(text)


def report(row, hsh, verdict, body_seed, cites='scrub.c:3147'):
    cite = {'GR1': 'cmdline.c:156', 'GR2': 'scrub.c:3147', 'GR3': 'systemd.kill.xml:68'}[row]
    body = ('Evidence. ' + body_seed + ' ') * 40 + f' cites {cite}.\n'
    return f'ROW {row} VERDICT: {verdict}\nSECTION SHA256: {hsh}\n{body}'


def add_wave(d, wave, seats):
    """seats: list of (seat, role, row, verdict, hash, body_seed, extra_body)."""
    tasks = [{'name': s, 'agent': r, 'task': f'counted seat {s}'} for s, r, *_ in seats]
    disp = {'taskCall': {'context': 'fixture', 'tasks': tasks}}
    res = {'results': [{'name': s, 'agent': r, 'id': f'fx-{s}', 'status': 'completed', 'final output': 'x'}
                       for s, r, *_ in seats]}
    write(os.path.join(d, f'.ufo/waves/round-47/{wave}-dispatch.json'), json.dumps(disp))
    write(os.path.join(d, f'.ufo/waves/round-47/{wave}-results.json'), json.dumps(res))
    for s, r, row, verdict, hsh, seed, extra in seats:
        base = report(row, hsh, verdict, seed)
        write(os.path.join(d, f'.ufo/waves/round-47/{wave}/{s}.md'), base + (extra or ''))


def add_marks(d, negated=False):
    e = open(os.path.join(d, ENTRY)).read() + \
        '\n## Gate status — round 47 (GR1-GR3 admitted)\n'
    open(os.path.join(d, ENTRY), 'w').write(e)
    if negated:
        sk = open(os.path.join(d, 'SKILL.md')).read() + \
            '\n## Scrub grounding — round 47 admission (WITHHELD — rows stay pending)\n'
        rd = open(os.path.join(d, 'corpus/README.md')).read() + \
            '\n- `corpus/knowledge/btrfs-scrub-grounding-r45.md` remains unadmitted round 47\n'
    else:
        sk = open(os.path.join(d, 'SKILL.md')).read() + \
            '\n## Scrub grounding — round 47 admission\n'
        rd = open(os.path.join(d, 'corpus/README.md')).read() + \
            '\n- `corpus/knowledge/btrfs-scrub-grounding-r45.md` admitted round 47\n'
    open(os.path.join(d, 'SKILL.md'), 'w').write(sk)
    open(os.path.join(d, 'corpus/README.md'), 'w').write(rd)


def section_hash(d, row):
    p = subprocess.run(['python3', os.path.join(d, 'tools/check-scrub-admission-r47.py'),
                        '--revision', 'HEAD', '--lane', d, '--section-hash'],
                       capture_output=True, text=True)
    return json.loads(p.stdout)['section_sha256'][row]


results = []


def rec(name, expect, observed, detail=''):
    ok = observed == expect
    results.append({'control': name, 'expect': expect, 'observed': observed, 'as_expected': ok,
                    'detail': detail})
    print(f'{"OK " if ok else "BAD"} {name}: expect {expect}, observed {observed} {detail[:120]}')


# ---- C1 controls ------------------------------------------------------------
d = fixture('k0-donothing')
rc, out, _ = counter(d, rev=BASE)
rec('C1-K0 do-nothing (counter at base)', 'FAIL', out.get('verdict'), f"verdicts_ok={out.get('verdicts_ok')}")
shutil.rmtree(d, ignore_errors=True)

d = fixture('k1-marks-only')
add_marks(d); rev = commit_all(d, 'marks only, no seats')
rc, out, _ = counter(d, rev=rev)
rec('C1-K1 marks-only', 'FAIL', out.get('verdict'),
    f"marks_ok={out.get('marks_ok')} verdicts_ok={out.get('verdicts_ok')}")
shutil.rmtree(d, ignore_errors=True)

d = fixture('k22-nonexistent-cite')
h = {r: section_hash(d, r) for r in ('GR1', 'GR2', 'GR3')}
seats = []
for row in ('GR1', 'GR2', 'GR3'):
    n = row[2:]
    seats += [(f'R47RevGR{n}a', 'reviewer', row, 'holds', h[row], f'{row}a ', ''),
              (f'R47CritGR{n}a', 'critic', row, 'holds', h[row], f'{row}A ', '')]
# seat R47RevGR1a cites a nonexistent line
seats[0] = ('R47RevGR1a', 'reviewer', 'GR1', 'holds', h['GR1'], 'GR1a ',
            ' extra citation cmdline.c:999999')
add_wave(d, 'w1', seats); add_marks(d); rev = commit_all(d, 'k22')
rc, out, _ = counter(d, rev=rev)
rec('C1-K22a nonexistent citation', 'FAIL', out.get('verdict'),
    f"GR1 row_ok={out['per_row']['GR1']['row_ok']} citations_ok={out['per_row']['GR1']['citations_ok']}")
shutil.rmtree(d, ignore_errors=True)

d = fixture('k23-identical')
h = {r: section_hash(d, r) for r in ('GR1', 'GR2', 'GR3')}
seats = []
for row in ('GR1', 'GR2', 'GR3'):
    n = row[2:]
    seats += [(f'R47RevGR{n}a', 'reviewer', row, 'holds', h[row], 'SHARED ', ''),
              (f'R47CritGR{n}a', 'critic', row, 'holds', h[row], 'SHARED ', '')]
add_wave(d, 'w1', seats); add_marks(d); rev = commit_all(d, 'k23')
rc, out, _ = counter(d, rev=rev)
rec('C1-K23a byte-identical reports', 'FAIL', out.get('verdict'),
    f"distinct_bodies={out['per_row']['GR1']['distinct_bodies']}")
shutil.rmtree(d, ignore_errors=True)

d = fixture('f1-unbound-tail')
ep = os.path.join(d, ENTRY)
lines = open(ep).read().split('\n')
i = lines.index('## GR1') + 1
lines.insert(i, '## Annotation — round 47 probe (header terminates the counted section)')
open(ep, 'w').write('\n'.join(lines))
rev = commit_all(d, 'f1a')
rc, out, _ = counter(d, rev=rev)
rec('C1-F1a inner "## " line', 0, out.get('structural_ok'), f"verdict={out.get('verdict')} problems={out.get('structural_problems')}")
shutil.rmtree(d, ignore_errors=True)

d = fixture('f1-dup-header')
ep = os.path.join(d, ENTRY)
txt = open(ep).read() + '\n## GR2\nsecond copy.\n'
open(ep, 'w').write(txt)
rev = commit_all(d, 'f1b')
rc, out, _ = counter(d, rev=rev)
rec('C1-F1b duplicated row header', 'FAIL', out.get('verdict'), f"structural_ok={out.get('structural_ok')}")
shutil.rmtree(d, ignore_errors=True)

d = fixture('f2-negating')
h = {r: section_hash(d, r) for r in ('GR1', 'GR2', 'GR3')}
seats = []
for row in ('GR1', 'GR2', 'GR3'):
    n = row[2:]
    seats += [(f'R47RevGR{n}a', 'reviewer', row, 'holds', h[row], f'{row}a ', ''),
              (f'R47CritGR{n}a', 'critic', row, 'holds', h[row], f'{row}A ', '')]
add_wave(d, 'w1', seats); add_marks(d, negated=True); rev = commit_all(d, 'f2')
rc, out, _ = counter(d, rev=rev)
rec('C1-F2a negating marks', 'FAIL', out.get('verdict'),
    f"marks_ok={out.get('marks_ok')} marks={out.get('marks')}")
shutil.rmtree(d, ignore_errors=True)

d = fixture('f3-deep-json')
deep = {'taskCall': {'tasks': [], 'deep': None}}
s = '{"taskCall":{"tasks":[],' + '"deep":' + '[' * 200000 + ']' * 200000 + '}}'
write(os.path.join(d, '.ufo/waves/round-47/zz9-dispatch.json'), s)
rev = commit_all(d, 'f3')
rc, out, nbytes = counter(d, rev=rev)
rec('C1-F3a deep-nested dispatch', 'FAIL', out.get('verdict'),
    f'rc={rc} stdout_bytes={nbytes}')
shutil.rmtree(d, ignore_errors=True)

d = fixture('k-pass')
h = {r: section_hash(d, r) for r in ('GR1', 'GR2', 'GR3')}
seats = []
for row in ('GR1', 'GR2', 'GR3'):
    n = row[2:]
    seats += [(f'R47RevGR{n}a', 'reviewer', row, 'holds', h[row], f'{row} reviewer a reads the row carefully. ', ''),
              (f'R47CritGR{n}a', 'critic', row, 'holds', h[row], f'{row} critic a attacks the row hard. ', '')]
add_wave(d, 'w1', seats); add_marks(d); rev = commit_all(d, 'k-pass')
rc, out, _ = counter(d, rev=rev)
rec('C1-K-pass candidate', 'PASS', out.get('verdict'),
    f"verdicts_ok={out.get('verdicts_ok')} marks_ok={out.get('marks_ok')}")
shutil.rmtree(d, ignore_errors=True)

# ---- C2 controls ------------------------------------------------------------
d = fixture('c2-k0', rev=BASE)
sp = os.path.join(d, 'tools/tsukuroi-census.sh')
env = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'TMPDIR': os.path.join(d, 't 2')}
os.makedirs(os.path.join(d, 't 2'), exist_ok=True)
p = subprocess.run(['bash', sp, '--selftest'], env=env, cwd=d, capture_output=True, text=True)
want_fail = 'FAIL' in p.stdout or p.returncode != 0
rc, out, _ = ('x', {'verdict': 'FAIL' if want_fail else 'PASS'}, 0)
rec('C2-K0 do-nothing (base census, space TMPDIR)', 'FAIL', out['verdict'],
    p.stdout.strip().splitlines()[-1])
shutil.rmtree(d, ignore_errors=True)

d = fixture('c2-k2-guardless')
sp = os.path.join(d, 'tools/tsukuroi-census.sh')
src = open(sp).read()
# remove the st_base guard, keep the R47-C2 cases
src2 = src.replace('''  local st_base=${TMPDIR:-/tmp}
  case "$st_base" in
    *[!A-Za-z0-9._/+-]*) st_base=/tmp ;;
  esac
  work=$(mktemp -d "$st_base/tsukuroi-r3-2-selftest.XXXXXX")''',
                   '  work=$(mktemp -d "${TMPDIR:-/tmp}/tsukuroi-r3-2-selftest.XXXXXX")')
assert src2 != src, 'guard removal did not apply'
open(sp, 'w').write(src2)
env = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'TMPDIR': os.path.join(d, 't 2')}
os.makedirs(os.path.join(d, 't 2'), exist_ok=True)
p = subprocess.run(['bash', sp, '--selftest'], env=env, cwd=d, capture_output=True, text=True)
want_fail = 'FAIL' in p.stdout or p.returncode != 0
rec('C2-K2 guard removed, cases kept', 'FAIL', 'FAIL' if want_fail else 'PASS',
    p.stdout.strip().splitlines()[-1])
shutil.rmtree(d, ignore_errors=True)

d = fixture('c2-kpass')
env = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'TMPDIR': os.path.join(d, 't 2')}
os.makedirs(os.path.join(d, 't 2'), exist_ok=True)
p = subprocess.run(['bash', os.path.join(d, 'tools/tsukuroi-census.sh'), '--selftest'],
                   env=env, cwd=d, capture_output=True, text=True)
rec('C2-K-pass candidate', 'PASS', 'PASS' if p.returncode == 0 and 'PASS' in p.stdout else 'FAIL',
    p.stdout.strip().splitlines()[-1])
shutil.rmtree(d, ignore_errors=True)

with open(OUT, 'w') as f:
    for r in results:
        f.write(json.dumps(r, sort_keys=True) + '\n')
bad = [r['control'] for r in results if not r['as_expected']]
print(f'\nbattery: {len(results)} controls, {len(bad)} not as expected: {bad}')
sys.exit(0 if not bad else 1)
