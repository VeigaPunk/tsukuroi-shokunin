#!/usr/bin/env python3
"""Phase 2: rerun all counters against the corrected K2 stub; run pristine against
every discriminator (to prove each mutant flips a real verdict); rerun m3 against
the fixed disc_m3."""
import json
import os
import sys

sys.path.insert(0, '/fast/scratch/hyaku/tsukuroi-r48/TMutCounter')
from driver import one, OUT
from concurrent.futures import ThreadPoolExecutor

SEAT = '/fast/scratch/hyaku/tsukuroi-r48/TMutCounter'
COUNTERS = ['pristine', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6']

jobs = [(c, 'K2-fallback', 'stub_k2.sh') for c in COUNTERS]
for d in ('disc_m1.sh', 'disc_m2.sh', 'disc_m3.sh', 'disc_m4.sh', 'disc_m6.sh'):
    jobs.append(('pristine', f'prist-{d[:-3]}', d))
jobs.append(('m3', 'disc-disc_m3-v2', 'disc_m3.sh'))

with ThreadPoolExecutor(8) as ex:
    res = list(ex.map(lambda t: one(*t), jobs))
with open(os.path.join(SEAT, 'results2.jsonl'), 'w') as f:
    for r in res:
        f.write(json.dumps(r, sort_keys=True) + '\n')
for r in sorted(res, key=lambda x: (x['counter'], x['subject'])):
    legs = ' '.join(f'{k}={r.get(k)}' for k in ('pass_ok','loc_ok','clean_ok','failfast_ok','term_ok','static_ok'))
    print(f"{r['counter']:9s} {r['subject']:18s} -> {r.get('verdict')}  [{legs}]")
