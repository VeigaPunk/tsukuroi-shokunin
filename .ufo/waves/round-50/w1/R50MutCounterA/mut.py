#!/usr/bin/env python3
"""C1-B5: mutation test of tools/check-scrub-admission-r50.py at FREEZE.

Four mutants, one per copy, each run against (a) a clean K-pass fixture set and
(b) the fixture set carrying the defect that mutant lets through.
Writes only under --scratch; receipts are copied out by the caller.
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
REV = '8029cdba1049df25632c91a23c8db4eefb54be5f'
S = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(S, 'work')
COUNTER = 'tools/check-scrub-admission-r50.py'
BATTERY = '.ufo/waves/round-50/controls/battery.py'
ENTRY = 'corpus/knowledge/btrfs-scrub-grounding-r45.md'
FROZEN_COUNTER_SHA = '0af0e679ee82d608d6278d2575391b1a7dd53af49099e962349bddac35f333db'
FROZEN_ROWS = {
    'GR1': '3a2ba1807a7f2308acb11b2f928f85dba5156c6eb9fe865216a06ba2a843fee1',
    'GR2': 'a2e955cefbd110ced928407c79b2cedb3cc431734487aa29e74682b23aeb7f3f',
    'GR3': '43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c',
}
STALE_GR2 = 'e519cbe421a46569310d967cbfb90e905e3c101549ba1f61a7f21ab4c50a7521'

MUTANTS = {
    'M1': ('drop the blocking rule',
           """            if v in ('partly', 'fails'):
                blocking.append(seat)
                continue
""",
           ''),
    'M2': ('drop the whitespace-collapsing distinct-bodies check',
           """            norm_body = '\\n'.join(ln.rstrip() for ln in (body or '').split('\\n') if ln.strip())
            bodies.add(hashlib.sha256(norm_body.encode('utf-8')).hexdigest())
""",
           """            bodies.add(hashlib.sha256((body or '').encode('utf-8')).hexdigest())
"""),
    'M3': ('drop the results.json seat check',
           """    hits = [r for r in results if isinstance(r, dict) and r.get('name') == seat]
    if len(hits) != 1:
        return None, None, None, 'not exactly one results entry'
    if hits[0].get('agent') != role:
        return None, None, None, f'results agent {hits[0].get("agent")!r} != {role}'
    if not hits[0].get('output'):
        return None, None, None, 'no completed output'
""",
           ''),
    'M4': ('accept a report hash that is any 64-hex string',
           """            if h != hashes.get(row):
                seat_rows.append(f'{seat}: hash {h} != {hashes.get(row)}')
                continue
""",
           """            if not re.fullmatch(r'[0-9a-f]{64}', h or ''):
                seat_rows.append(f'{seat}: hash {h} is not 64 hex')
                continue
"""),
}


def git_show(path):
    p = subprocess.run(['git', '-C', LANE, 'show', f'{REV}:{path}'],
                       capture_output=True, stdin=subprocess.DEVNULL)
    if p.returncode != 0:
        raise SystemExit(f'cannot read {path} at {REV}')
    return p.stdout


def run_json(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True, stdin=subprocess.DEVNULL)
    try:
        return p.returncode, json.loads(p.stdout.strip().split('\n')[-1])
    except Exception:
        return p.returncode, {'verdict': 'ERROR', 'error': (p.stdout + p.stderr)[-500:]}


def load_battery():
    src = os.path.join(S, 'battery-frozen.py')
    with open(src, 'wb') as fh:
        fh.write(git_show(BATTERY))
    spec = importlib.util.spec_from_file_location('batfrozen', src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def legs(obj):
    return {k: obj.get(k) for k in ('structural_ok', 'corr_ok', 'quotes_ok',
                                    'verdicts_ok', 'seats_ok', 'marks_ok')}


def main():
    os.makedirs(WORK, exist_ok=True)
    batt = load_battery()
    raw = git_show(COUNTER)
    sha = hashlib.sha256(raw).hexdigest()
    assert sha == FROZEN_COUNTER_SHA, (sha, FROZEN_COUNTER_SHA)
    counters = os.path.join(WORK, 'counters')
    os.makedirs(counters, exist_ok=True)
    pris = os.path.join(counters, 'pristine.py')
    with open(pris, 'wb') as fh:
        fh.write(raw)
    text = raw.decode('utf-8')
    patch_rows = []
    for mid, (why, old, new) in MUTANTS.items():
        n = text.count(old)
        assert n == 1, (mid, 'anchor count', n)
        mpath = os.path.join(counters, f'{mid.lower()}.py')
        with open(mpath, 'w', encoding='utf-8') as fh:
            fh.write(text.replace(old, new, 1))
        patch_rows.append({'mutant': mid, 'why': why, 'anchor_count': n,
                           'old': old, 'new': new,
                           'pristine_sha256': sha,
                           'mutant_sha256': hashlib.sha256(open(mpath, 'rb').read()).hexdigest(),
                           'bytes_delta': len(new) - len(old)})
    # section hashes, from the pristine copy against the frozen revision
    rc, sh = run_json([sys.executable, pris, '--revision', REV, '--lane', LANE, '--section-hash'])
    assert rc == 0 and sh['section_sha256'] == FROZEN_ROWS, (rc, sh)
    hashes = sh['section_sha256']
    entry = git_show(ENTRY).decode('utf-8')

    # ---- fixtures ---------------------------------------------------------
    def fixture(name, **kw):
        d = os.path.join(WORK, 'fx', name)
        os.makedirs(d, exist_ok=True)
        wave = batt.build_cohort(d, hashes, **kw)
        paths = batt.marks(d, entry)
        return d, wave, paths

    fx = {}
    fx['clean'] = fixture('clean')
    fx['D1'] = fixture('D1-partly', verdicts={'R50CritGR2b': 'partly'})
    same = (f'The cited lines {batt.CITE["GR2"][0]} and {batt.CITE["GR2"][1]} decide the statement '
            f'of this row. ' + 'Evidence. ' * 40)
    fx['D2'] = fixture('D2-padded', bodies={'R50RevGR2a': same, 'R50CritGR2a': same + '   \n\n  '})
    fx['D3'] = fixture('D3-noresults')
    with open(os.path.join(fx['D3'][0], 'results.json'), 'w', encoding='utf-8') as fh:
        json.dump({'results': []}, fh)
    fx['D4'] = fixture('D4-stalehash')
    d4 = fx['D4'][0]
    for seat in batt.ROLES['GR2']:
        p = os.path.join(d4, 'wave', f'{seat}.md')
        with open(p, encoding='utf-8') as fh:
            lines = fh.read().split('\n')
        assert lines[1].startswith('SECTION SHA256: ')
        lines[1] = f'SECTION SHA256: {STALE_GR2}'
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(lines))

    def cmd(counter, name):
        d, wave, paths = fx[name]
        return [sys.executable, counter, '--revision', REV, '--lane', LANE, '--no-base-check',
                '--entry-file', paths['entry.md'], '--skill-file', paths['skill.md'],
                '--readme-file', paths['readme.md'],
                '--dispatch-file', os.path.join(d, 'dispatch.json'),
                '--results-file', os.path.join(d, 'results.json'), '--wave-dir', wave]

    # fixture entry must hash to the frozen rows (structural leg on the fixture itself)
    fxhash = {}
    for name, (d, wave, paths) in fx.items():
        rc, obj = run_json([sys.executable, pris, '--revision', REV, '--lane', LANE,
                            '--section-hash', '--entry-file', paths['entry.md']])
        fxhash[name] = {'rc': rc, 'structural_ok': obj.get('structural_ok'),
                        'section_sha256': obj.get('section_sha256')}
        assert obj.get('section_sha256') == hashes, (name, obj)

    runs = []

    def go(label, counter, name, expect):
        c = cmd(counter, name)
        rc, obj = run_json(c)
        rec = {'run': label, 'fixture': name, 'counter': os.path.basename(counter),
               'expect': expect, 'got': obj.get('verdict'), 'rc': rc, 'legs': legs(obj),
               'as_expected': obj.get('verdict') == expect,
               'seat_notes': (obj.get('seat_notes') or [])[:3],
               'per_row_ok': {r: (obj.get('per_row') or {}).get(r, {}).get('row_ok')
                              for r in ('GR1', 'GR2', 'GR3')},
               'per_row_blocking': {r: (obj.get('per_row') or {}).get(r, {}).get('blocking')
                                    for r in ('GR1', 'GR2', 'GR3')},
               'per_row_distinct': {r: (obj.get('per_row') or {}).get(r, {}).get('distinct_bodies')
                                    for r in ('GR1', 'GR2', 'GR3')},
               'cmd': ' '.join(c)}
        runs.append(rec)
        print(json.dumps({k: rec[k] for k in ('run', 'fixture', 'counter', 'expect', 'got', 'legs')},
                         sort_keys=True))
        return rec

    # baseline: pristine on every fixture
    for name in ('clean', 'D1', 'D2', 'D3', 'D4'):
        go(f'pristine/{name}', pris, name, 'PASS' if name == 'clean' else 'FAIL')
    # each mutant: clean (must stay PASS) and its own defect (PASS = survived)
    for mid in MUTANTS:
        mpath = os.path.join(counters, f'{mid.lower()}.py')
        go(f'{mid}/clean', mpath, 'clean', 'PASS')
        go(f'{mid}/D{mid[1:]}', mpath, f'D{mid[1:]}', 'PASS')

    # restoration evidence
    pris_after = hashlib.sha256(open(pris, 'rb').read()).hexdigest()
    out = {'revision': REV, 'frozen_counter_sha256': FROZEN_COUNTER_SHA,
           'pristine_copy_sha256_before': sha, 'pristine_copy_sha256_after': pris_after,
           'pristine_restored': pris_after == FROZEN_COUNTER_SHA,
           'mutants': patch_rows, 'fixture_entry_hashes': fxhash,
           'runs': runs}
    with open(os.path.join(S, 'mutation-r50-c1-b5.json'), 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    bad = [r for r in runs if not r['as_expected']]
    print(f'runs {len(runs)}, as expected {len(runs) - len(bad)}, not {len(bad)}')
    for r in bad:
        print('  MISMATCH', r['run'], r['expect'], r['got'], r['legs'])
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
