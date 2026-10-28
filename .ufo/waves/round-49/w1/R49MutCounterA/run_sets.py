#!/usr/bin/env python3
"""Run one counter binary (original or mutant) against every fixture set; emit JSONL."""
import json, os, subprocess, sys

S = '/fast/scratch/hyaku/tsukuroi-r49/R49MutCounterA'
REV = open(os.path.join(S, 'FXREV')).read().strip()
COUNTER = sys.argv[1]
SETS = json.load(open(os.path.join(S, 'sets.json')))
FIELDS = ('structural_ok', 'corr_ok', 'quotes_ok', 'verdicts_ok', 'seats_ok', 'marks_ok')


def run(c):
    cmd = ['python3', COUNTER, '--revision', REV, '--no-base-check',
           '--lane', open(os.path.join(S, 'FXDIR')).read().strip(),
           '--entry-file', c['entry'], '--skill-file', c['skill'], '--readme-file', c['readme'],
           '--wave-dir', c['wave_dir'], '--results-file', c['results']]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=900, stdin=subprocess.DEVNULL)
    line = (p.stdout or '').strip().split('\n')[-1] if (p.stdout or '').strip() else '{}'
    try:
        o = json.loads(line)
    except Exception:
        o = {'parse_error': True, 'raw': line[:400], 'stderr': (p.stderr or '')[:400]}
    o['_rc'] = p.returncode
    return o


for c in SETS:
    o = run(c)
    print(json.dumps({'set': c['name'], 'counter': COUNTER, 'rc': o.get('_rc'),
                      'verdict': o.get('verdict'),
                      **{k: o.get(k) for k in FIELDS},
                      'notes': (o.get('seat_notes') or [])[:4],
                      'per_row': {r: {'row_ok': v['row_ok'], 'credited': len(v['credited']),
                                      'blocking': v['blocking'],
                                      'distinct': v['distinct_bodies']}
                                  for r, v in (o.get('per_row') or {}).items()},
                      'err': o.get('error') or o.get('parse_error')}, sort_keys=True))
