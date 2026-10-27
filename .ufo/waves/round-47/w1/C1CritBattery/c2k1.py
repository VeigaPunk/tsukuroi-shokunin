#!/usr/bin/env python3
"""C2-K1 (declared in SCORECARD.md:3077 but missing from battery.py): live output only.

Interpretation: at BASE bytes with NO selftest change, the live space-TMPDIR failure must
reproduce deterministically — two consecutive runs both FAIL with byte-identical
digits-stripped stdout (the C2 kill-rule form)."""
import json, os, re, shutil, subprocess, sys

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
BASE = '916019057147d7e9ba6b137647b2cee26decf4b8'
HERE = os.path.dirname(os.path.abspath(__file__))
d = os.path.join(HERE, 'c2k1')
shutil.rmtree(d, ignore_errors=True)
os.makedirs(d)


def sh(*a, **kw):
    return subprocess.run(a, capture_output=True, text=True, **kw)


assert sh('git', 'clone', '-q', '--shared', LANE, d).returncode == 0
sh('git', '-C', d, 'remote', 'remove', 'origin')
top = sh('git', '-C', d, 'rev-parse', '--show-toplevel').stdout.strip()
assert top == d, f'toplevel {top} != {d}'
assert sh('git', '-C', d, 'checkout', '-q', BASE).returncode == 0
os.makedirs(os.path.join(d, 't 2'), exist_ok=True)
env = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'TMPDIR': os.path.join(d, 't 2')}
runs = []
for i in (1, 2):
    p = subprocess.run(['bash', os.path.join(d, 'tools/tsukuroi-census.sh'), '--selftest'],
                       env=env, cwd=d, capture_output=True, text=True)
    stripped = re.sub(r'\d', '#', p.stdout)
    runs.append((p.returncode, p.stdout, stripped))
    print(f'run{i}: rc={p.returncode} last={p.stdout.strip().splitlines()[-1] if p.stdout.strip() else ""!r}')
same_fail = runs[0][0] != 0 and runs[1][0] != 0 and 'FAIL' in runs[0][1] and 'FAIL' in runs[1][1]
same_bytes = runs[0][2] == runs[1][2]
rec = {'control': 'C2-K1 live output only (no selftest change, twice)',
       'expect': 'FAIL-twice-identical', 'observed': 'FAIL-twice-identical' if (same_fail and same_bytes) else 'DEVIATION',
       'as_expected': bool(same_fail and same_bytes),
       'detail': f'run1 rc={runs[0][0]} run2 rc={runs[1][0]} digits_stripped_identical={same_bytes}'}
with open(os.path.join(HERE, 'c2k1-summary.json'), 'w') as f:
    f.write(json.dumps(rec, sort_keys=True) + '\n')
print(('OK ' if rec['as_expected'] else 'BAD') + rec['control'] + ': ' + rec['detail'])
shutil.rmtree(d, ignore_errors=True)
sys.exit(0 if rec['as_expected'] else 1)
