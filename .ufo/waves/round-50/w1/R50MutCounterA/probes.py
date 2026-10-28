#!/usr/bin/env python3
"""C1-B5 follow-up probes: for each surviving mutant, does the mutation REMOVE the leg or only
NARROW it? Builds three extra fixtures against the same pristine/mutant copies."""
import json
import os
import subprocess
import sys

S = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(S, 'work')
sys.path.insert(0, S)
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
REV = '8029cdba1049df25632c91a23c8db4eefb54be5f'
ENTRY = 'corpus/knowledge/btrfs-scrub-grounding-r45.md'
import importlib.util

spec = importlib.util.spec_from_file_location('batfrozen', os.path.join(S, 'battery-frozen.py'))
batt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(batt)


def git_show(path):
    p = subprocess.run(['git', '-C', LANE, 'show', f'{REV}:{path}'],
                       capture_output=True, stdin=subprocess.DEVNULL)
    return p.stdout


def run_json(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True, stdin=subprocess.DEVNULL)
    try:
        return p.returncode, json.loads(p.stdout.strip().split('\n')[-1])
    except Exception:
        return p.returncode, {'verdict': 'ERROR', 'error': (p.stdout + p.stderr)[-400:]}


def main():
    hashes = {'GR1': '3a2ba1807a7f2308acb11b2f928f85dba5156c6eb9fe865216a06ba2a843fee1',
              'GR2': 'a2e955cefbd110ced928407c79b2cedb3cc431734487aa29e74682b23aeb7f3f',
              'GR3': '43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c'}
    entry = git_show(ENTRY).decode('utf-8')
    out = []

    def build(name, **kw):
        d = os.path.join(WORK, 'fx', name)
        os.makedirs(d, exist_ok=True)
        wave = batt.build_cohort(d, hashes, **kw)
        paths = batt.marks(d, entry)
        return d, wave, paths

    def go(label, counter, name, expect):
        d, wave, paths = (None, None, None)
        d = os.path.join(WORK, 'fx', name)
        wave = os.path.join(d, 'wave')
        paths = {'entry.md': os.path.join(d, 'entry.md'), 'skill.md': os.path.join(d, 'skill.md'),
                 'readme.md': os.path.join(d, 'readme.md')}
        c = [sys.executable, counter, '--revision', REV, '--lane', LANE, '--no-base-check',
             '--entry-file', paths['entry.md'], '--skill-file', paths['skill.md'],
             '--readme-file', paths['readme.md'],
             '--dispatch-file', os.path.join(d, 'dispatch.json'),
             '--results-file', os.path.join(d, 'results.json'), '--wave-dir', wave]
        rc, obj = run_json(c)
        rec = {'probe': label, 'fixture': name, 'counter': os.path.basename(counter),
               'expect': expect, 'got': obj.get('verdict'), 'rc': rc,
               'legs': {k: obj.get(k) for k in ('structural_ok', 'corr_ok', 'quotes_ok',
                                                'verdicts_ok', 'seats_ok', 'marks_ok')},
               'as_expected': obj.get('verdict') == expect,
               'per_row_credited': {r: len((obj.get('per_row') or {}).get(r, {}).get('credited', []))
                                    for r in ('GR1', 'GR2', 'GR3')},
               'per_row_blocking': {r: (obj.get('per_row') or {}).get(r, {}).get('blocking')
                                    for r in ('GR1', 'GR2', 'GR3')},
               'seat_notes': (obj.get('seat_notes') or [])[:3],
               'cmd': ' '.join(c)}
        out.append(rec)
        print(json.dumps({k: rec[k] for k in ('probe', 'counter', 'expect', 'got', 'legs')},
                         sort_keys=True))
        return rec

    pris = os.path.join(WORK, 'counters', 'pristine.py')
    m1 = os.path.join(WORK, 'counters', 'm1.py')
    m2 = os.path.join(WORK, 'counters', 'm2.py')
    m3 = os.path.join(WORK, 'counters', 'm3.py')

    # P1: a wholly-negative row (all six GR3 seats bound `partly`) must still block.
    build('P1-allpartly', verdicts={s: 'partly' for s in batt.ROLES['GR3']})
    go('P1 pristine (all six GR3 partly)', pris, 'P1-allpartly', 'FAIL')
    go('P1 M1 (blocking rule dropped)', m1, 'P1-allpartly', 'PASS')

    # P2: byte-identical bodies, no whitespace padding.
    same = (f'The cited lines {batt.CITE["GR2"][0]} and {batt.CITE["GR2"][1]} decide the statement '
            f'of this row. ' + 'Evidence. ' * 40)
    build('P2-identical', bodies={'R50RevGR2a': same, 'R50CritGR2a': same})
    go('P2 pristine (byte-identical bodies)', pris, 'P2-identical', 'FAIL')
    go('P2 M2 (collapse dropped)', m2, 'P2-identical', 'FAIL')

    # P3: one results entry completed with an empty output.
    build('P3-emptyoutput')
    rp = os.path.join(WORK, 'fx', 'P3-emptyoutput', 'results.json')
    with open(rp, encoding='utf-8') as fh:
        res = json.load(fh)
    for r in res['results']:
        if r['name'] == 'R50CritGR1b':
            r['output'] = ''
    with open(rp, 'w', encoding='utf-8') as fh:
        json.dump(res, fh)
    go('P3 pristine (empty results output)', pris, 'P3-emptyoutput', 'FAIL')
    go('P3 M3 (results check dropped)', m3, 'P3-emptyoutput', 'PASS')

    with open(os.path.join(S, 'probes-r50-c1-b5.json'), 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    bad = [r for r in out if not r['as_expected']]
    print(f'probes {len(out)}, as expected {len(out) - len(bad)}, not {len(bad)}')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
