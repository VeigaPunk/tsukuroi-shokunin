#!/usr/bin/env python3
"""C1-B5 probe P4: the second half of the bound-format negative rule (a contradicting
`ROW GRn VERDICT:` line inside the body) under pristine vs M1."""
import importlib.util
import json
import os
import subprocess
import sys

S = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(S, 'work')
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
REV = '8029cdba1049df25632c91a23c8db4eefb54be5f'
ENTRY = 'corpus/knowledge/btrfs-scrub-grounding-r45.md'
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
    d = os.path.join(WORK, 'fx', 'P4-contradict')
    os.makedirs(d, exist_ok=True)
    batt.build_cohort(d, hashes)
    batt.marks(d, entry)
    p = os.path.join(d, 'wave', 'R50CritGR2c.md')
    with open(p, encoding='utf-8') as fh:
        text = fh.read()
    with open(p, 'w', encoding='utf-8') as fh:
        fh.write(text.rstrip('\n') + '\nOn re-reading I record ROW GR2 VERDICT: fails for the range gap.\n')
    out = []
    for label, cname, expect in (('P4 pristine (contradicting body line)', 'pristine.py', 'FAIL'),
                                 ('P4 M1 (blocking rule dropped)', 'm1.py', 'PASS')):
        c = os.path.join(WORK, 'counters', cname)
        cmd = [sys.executable, c, '--revision', REV, '--lane', LANE, '--no-base-check',
               '--entry-file', os.path.join(d, 'entry.md'),
               '--skill-file', os.path.join(d, 'skill.md'),
               '--readme-file', os.path.join(d, 'readme.md'),
               '--dispatch-file', os.path.join(d, 'dispatch.json'),
               '--results-file', os.path.join(d, 'results.json'),
               '--wave-dir', os.path.join(d, 'wave')]
        rc, obj = run_json(cmd)
        rec = {'probe': label, 'counter': cname, 'expect': expect, 'got': obj.get('verdict'),
               'rc': rc, 'as_expected': obj.get('verdict') == expect,
               'legs': {k: obj.get(k) for k in ('structural_ok', 'corr_ok', 'quotes_ok',
                                                'verdicts_ok', 'seats_ok', 'marks_ok')},
               'per_row_blocking': {r: (obj.get('per_row') or {}).get(r, {}).get('blocking')
                                    for r in ('GR1', 'GR2', 'GR3')},
               'seat_notes': (obj.get('seat_notes') or [])[:3], 'cmd': ' '.join(cmd)}
        out.append(rec)
        print(json.dumps(rec, sort_keys=True))
    with open(os.path.join(S, 'probes2-r50-c1-b5.json'), 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    return 0 if all(r['as_expected'] for r in out) else 1


if __name__ == '__main__':
    sys.exit(main())
