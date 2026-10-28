#!/usr/bin/env python3
"""C1-M3 driver: run pristine + 6 counter mutants against the 5 control stubs and the
per-mutant discriminators. Every counter run gets its own --work dir under the seat
scratch; each stub selftest takes ~4-5 s so one counter invocation is ~20 s.
"""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

SEAT = '/fast/scratch/hyaku/tsukuroi-r48/TMutCounter'
STUBS = os.path.join(SEAT, 'stubs')
OUT = os.path.join(SEAT, 'out')
os.makedirs(OUT, exist_ok=True)

CONTROLS = [  # (control, census stub, expected verdict under pristine)
    ('K0-base',    'stub_base.sh', 'FAIL'),
    ('K2-fallback','stub_k2.sh',   'FAIL'),
    ('K3-traps',   'stub_k3.sh',   'FAIL'),
    ('K4-usagetext','stub_k4.sh',  'FAIL'),
    ('K-pass',     'stub_pass.sh', 'PASS'),
]
COUNTERS = ['pristine', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6']
DISC = {  # mutant -> discriminator stub
    'pristine': None,
    'm1': 'disc_m1.sh', 'm2': 'disc_m2.sh', 'm3': 'disc_m3.sh',
    'm4': 'disc_m4.sh', 'm5': 'stub_pass.sh', 'm6': 'disc_m6.sh',
}


def one(counter, label, stub):
    work = os.path.join(SEAT, 'work', f'{counter}-{label}')
    os.makedirs(work, exist_ok=True)
    p = subprocess.run(
        ['python3', os.path.join(SEAT, f'counter_{counter}.py'),
         '--census', os.path.join(STUBS, stub), '--work', work],
        capture_output=True, timeout=600)
    rec = {'counter': counter, 'subject': label, 'stub': stub,
           'counter_rc': p.returncode}
    try:
        line = p.stdout.decode('utf-8', 'replace').strip().splitlines()[-1]
        r = json.loads(line)
        for k in ('pass_ok', 'loc_ok', 'clean_ok', 'failfast_ok', 'term_ok', 'static_ok', 'verdict'):
            rec[k] = r.get(k)
        rec['term_detail'] = r.get('term')
        rec['static_detail'] = r.get('static')
        rec['scenarios'] = [{k: s.get(k) for k in ('scenario', 'rc', 'pass_ok', 'loc_ok', 'clean_ok', 'real_parent')} for s in r.get('scenarios', [])]
        rec['failfast_detail'] = r.get('failfast')
    except Exception as e:
        rec['verdict'] = 'ERROR'
        rec['error'] = f'{e}; stdout={p.stdout[:300]!r} stderr={p.stderr[:300]!r}'
    with open(os.path.join(OUT, f'{counter}--{label}.json'), 'w') as f:
        json.dump(rec, f, indent=1, sort_keys=True)
    return rec


def main():
    jobs = []
    for c in COUNTERS:
        for label, stub, _ in CONTROLS:
            jobs.append((c, label, stub))
        d = DISC[c]
        if d:
            jobs.append((c, f'disc-{d[:-3]}', d))
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(lambda t: one(*t), jobs))
    with open(os.path.join(SEAT, 'results.jsonl'), 'w') as f:
        for r in res:
            f.write(json.dumps(r, sort_keys=True) + '\n')
    # summary table
    for c in COUNTERS:
        row = [r for r in res if r['counter'] == c]
        for r in sorted(row, key=lambda x: x['subject']):
            legs = ' '.join(f'{k}={r.get(k)}' for k in ('pass_ok','loc_ok','clean_ok','failfast_ok','term_ok','static_ok'))
            print(f"{c:9s} {r['subject']:18s} -> {r.get('verdict')}  [{legs}]")
    return 0


if __name__ == '__main__':
    sys.exit(main())
