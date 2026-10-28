#!/usr/bin/env python3
"""Full-JSON capture for the four survivor pairs (same fixtures drive.py built)."""
import json
import os
import subprocess
import sys

S = os.path.dirname(os.path.abspath(__file__))
L = os.path.join(S, 'fixture-repo')
REV = subprocess.run(['git', '-C', L, 'rev-parse', 'HEAD'], capture_output=True,
                     text=True).stdout.strip()
R = os.path.join(S, 'fx')
ENTRY = os.path.join(R, 'entry-clean.md')
ENTRY7 = os.path.join(R, 'entry-d7.md')
SKILL = os.path.join(R, 'skill-clean.md')
README = os.path.join(R, 'readme-clean.md')
README8 = os.path.join(R, 'readme-d8.md')
RES = {k: os.path.join(R, f'res-{k}.json') for k in ('clean', 'd5', 'd6', 'd7')}
COH = {k: os.path.join(R, f'cohort-{k}') for k in ('clean', 'd5', 'd6', 'd7')}
PAIRS = [
    ('orig/clean', 'base/check.py', ENTRY, COH['clean'], README, RES['clean']),
    ('M5/clean', 'mutants/M5.py', ENTRY, COH['clean'], README, RES['clean']),
    ('M6/clean', 'mutants/M6.py', ENTRY, COH['clean'], README, RES['clean']),
    ('M7/clean', 'mutants/M7.py', ENTRY, COH['clean'], README, RES['clean']),
    ('M8/clean', 'mutants/M8.py', ENTRY, COH['clean'], README, RES['clean']),
    ('orig/D5', 'base/check.py', ENTRY, COH['d5'], README, RES['d5']),
    ('M5/D5', 'mutants/M5.py', ENTRY, COH['d5'], README, RES['d5']),
    ('orig/D6', 'base/check.py', ENTRY, COH['d6'], README, RES['d6']),
    ('M6/D6', 'mutants/M6.py', ENTRY, COH['d6'], README, RES['d6']),
    ('orig/D7', 'base/check.py', ENTRY7, COH['d7'], README, RES['d7']),
    ('M7/D7', 'mutants/M7.py', ENTRY7, COH['d7'], README, RES['d7']),
    ('orig/D8', 'base/check.py', ENTRY, COH['clean'], README8, RES['clean']),
    ('M8/D8', 'mutants/M8.py', ENTRY, COH['clean'], README8, RES['clean']),
]
out = []
for label, counter, e, d, rd, res in PAIRS:
    p = subprocess.run(['python3', os.path.join(S, counter), '--revision', REV,
                        '--lane', L, '--no-base-check', '--entry-file', e,
                        '--skill-file', SKILL, '--readme-file', rd,
                        '--wave-dir', d, '--results-file', res],
                       capture_output=True, text=True, cwd=S)
    try:
        o = json.loads(p.stdout.strip().split('\n')[-1])
    except Exception:
        o = {'parse_error': True, 'raw': p.stdout[-400:], 'stderr': p.stderr[-400:]}
    o['run'] = label
    o['rc'] = p.returncode
    out.append(o)
    print(label, o.get('verdict'), o.get('rc'),
          {k: o.get(k) for k in ('structural_ok', 'corr_ok', 'quotes_ok', 'verdicts_ok',
                                 'seats_ok', 'marks_ok')},
          'marks=', o.get('marks'))
with open(os.path.join(S, 'capture-full.jsonl'), 'w') as fh:
    for o in out:
        fh.write(json.dumps(o, sort_keys=True) + '\n')
