#!/usr/bin/env python3
"""Emit the per-mutant unified diff (against the pristine probe) for the seat report."""
import json
import os

SEAT = '/fast/scratch/hyaku/tsukuroi-r31/MutProbeC2'
OUT = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w1/MutProbeC2'
man = json.load(open(os.path.join(SEAT, 'mutants', 'manifest.json')))
lines = []
for m in man['mutants']:
    lines.append('### %s' % m['name'])
    lines.append('sha256 %s' % m['sha256'])
    lines.append('')
    lines.append('```diff')
    lines.append(m['diff'].rstrip('\n'))
    lines.append('```')
    lines.append('')
with open(os.path.join(OUT, 'mutant-diffs.md'), 'w') as fh:
    fh.write('# Mutant diffs (each against the pristine probe `b168b9b8…`)\n\n')
    fh.write('\n'.join(lines))
print('wrote mutant-diffs.md', len('\n'.join(lines)))
