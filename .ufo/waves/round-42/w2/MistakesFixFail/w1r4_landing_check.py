#!/usr/bin/env python3
"""R42-BATTERY-SUMMARY-COLLISION, the landing half — are the declared battery artifacts committed?

Not code: the mistake's other half is provenance (the summaries on disk are hand-named copies that no
runner writes, and at the dispatch tip neither they nor the per-control receipts were in the tree).
What shows a landing fix able to fail is a check that compares the declared directory with
`git ls-tree <rev> -- <dir>`: red at a revision where the artifacts are absent, green where they are.

Usage: w1r4_landing_check.py <lane> <rev> <dir>
"""
import os
import subprocess
import sys

lane, rev, d = sys.argv[1], sys.argv[2], sys.argv[3]
tracked = set()
out = subprocess.run(['git', '-C', lane, 'ls-tree', '-r', '--name-only', rev, '--', d],
                     capture_output=True, text=True).stdout.split()
for p in out:
    tracked.add(os.path.basename(p))
on_disk = sorted(f for f in os.listdir(os.path.join(lane, d))
                 if os.path.isfile(os.path.join(lane, d, f)))   # ignore __pycache__/ and dirs
missing = [f for f in on_disk if f not in tracked]
print(f'revision       : {rev}')
print(f'declared dir   : {d}')
print(f'git ls-tree    : {len(out)} files tracked')
print(f'on disk        : {len(on_disk)} files')
print(f'missing in tree: {len(missing)} {missing[:4]}{" …" if len(missing) > 4 else ""}')
print('CHECK          : ' + ('PASS (green)' if not missing else 'FAIL (red) — artifacts on disk are not committed'))
sys.exit(0 if not missing else 1)
