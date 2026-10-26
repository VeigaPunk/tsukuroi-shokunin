#!/usr/bin/env python3
"""Build the C2MutCounter receipt artifacts from runs.jsonl (scratch only)."""
import json
import os
import subprocess
import sys

SCRATCH = '/fast/scratch/hyaku/tsukuroi-r40/C2MutCounter'
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
FROZEN = ['C2-K0-do-nothing-base', 'C2-K1-x-empty', 'C2-K2a-x-false-negated',
          'C2-K2b-x-false-values', 'C2-K3-own-work-only', 'C2-K4-held-rows',
          'C2-K5-scripted-quote-rule', 'C2-K6-duplicated-block', 'C2-K7-candidate']
FIELDS = ('exit', 'result', 'rules_verified', 'source_ok', 'counts_ok', 'novelty_base_hits',
          'duplicate_rows', 'duplicate_headings')

rows = [json.loads(l) for l in open(os.path.join(SCRATCH, 'runs.jsonl'))]
by = {}
for r in rows:
    by.setdefault(r['counter_tag'], {})[r['control']] = r
tags = ['pristine', 'M1-drop-neg', 'M2-drop-paraphrase', 'M2a-drop-minwords',
        'M2b-drop-copied-quote', 'M3-accept-base-rows', 'M4-skip-value-compare', 'M5-skip-novelty']
pr = by['pristine']

# validation vs recorded controls
ctl = {r['control']: r for r in map(json.loads, open(os.path.join(
    LANE, '.ufo/waves/round-40/controls/controls.jsonl'))) if r['claim'] == 'C2'}
val = []
for control in FROZEN:
    rec, ref = pr[control], ctl[control]
    for k in FIELDS:
        if rec[k] != ref[k]:
            val.append(f'MISMATCH {control} {k}: mine={rec[k]!r} recorded={ref[k]!r}')
    reasons = rec['row_reasons']
    if reasons != (ref.get('row_reasons') or {}):
        val.append(f'MISMATCH {control} row_reasons')
val.append(f'validation vs controls.jsonl (9 frozen C2 controls): '
           f'{"OK — all fields and row_reasons identical" if not val[:-1] else "FAILED"}')
open(os.path.join(SCRATCH, 'validation.txt'), 'w').write('\n'.join(val) + '\n')

# flip matrix
nov_const = all(r['novelty_base_hits'] == 0 for r in rows)
out = [f'runs: {len(rows)} ({len(tags)} counter variants x {len(pr)} controls); '
       f'novelty_base_hits==0 in every run: {nov_const}', '']
out.append('== FROZEN control set (the item deliverable) ==')
for tag in tags[1:]:
    flips = [c for c in FROZEN if pr[c]['result'] == 'FAIL' and pr[c]['exit'] == 1
             and by[tag][c]['result'] == 'PASS' and by[tag][c]['exit'] == 0]
    out.append(f'{tag} (sha256 {by[tag][list(by[tag])[0]]["counter_sha256"]}): '
               f'flips={flips or "NONE"}')
out.append('')
out.append('== SUPPLEMENTARY C2X controls (liveness proofs, not part of the frozen set) ==')
for tag in tags[1:]:
    flips = [c for c in by[tag] if c not in FROZEN and pr[c]['result'] == 'FAIL'
             and pr[c]['exit'] == 1 and by[tag][c]['result'] == 'PASS' and by[tag][c]['exit'] == 0]
    out.append(f'{tag}: flips={flips or "NONE"}')
open(os.path.join(SCRATCH, 'flip-matrix.txt'), 'w').write('\n'.join(out) + '\n')

# key records
keys = [('K5-pristine', 'pristine', 'C2-K5-scripted-quote-rule'),
        ('K5-under-M2', 'M2-drop-paraphrase', 'C2-K5-scripted-quote-rule'),
        ('K2b-pristine', 'pristine', 'C2-K2b-x-false-values'),
        ('K2b-under-M4', 'M4-skip-value-compare', 'C2-K2b-x-false-values'),
        ('K4-pristine', 'pristine', 'C2-K4-held-rows'),
        ('K4-under-M3', 'M3-accept-base-rows', 'C2-K4-held-rows'),
        ('K4b-pristine', 'pristine', 'C2X-K4b-held-rows-usedby'),
        ('K4b-under-M3', 'M3-accept-base-rows', 'C2X-K4b-held-rows-usedby'),
        ('K2c-pristine', 'pristine', 'C2X-K2c-value-only'),
        ('K2c-under-M4', 'M4-skip-value-compare', 'C2X-K2c-value-only'),
        ('K1b-pristine', 'pristine', 'C2X-K1b-tokens-only-rule'),
        ('K1b-under-M2a', 'M2a-drop-minwords', 'C2X-K1b-tokens-only-rule'),
        ('K5c-pristine', 'pristine', 'C2X-K5c-quote-rule-clean'),
        ('K5c-under-M2b', 'M2b-drop-copied-quote', 'C2X-K5c-quote-rule-clean')]
kr = {}
for label, tag, control in keys:
    r = by[tag][control]
    kr[label] = {'exit': r['exit'], 'result': r['result'], 'rules_verified': r['rules_verified'],
                 'source_ok': r['source_ok'], 'counts_ok': r['counts_ok'],
                 'row_reasons': r['row_reasons']}
json.dump(kr, open(os.path.join(SCRATCH, 'key-records.json'), 'w'), indent=1)

# probe output
p = subprocess.run([sys.executable, os.path.join(SCRATCH, 'probe.py'), os.path.join(SCRATCH, 'c2')],
                   capture_output=True, text=True)
open(os.path.join(SCRATCH, 'probe.txt'), 'w').write(p.stdout + p.stderr)

print(open(os.path.join(SCRATCH, 'flip-matrix.txt')).read())
print('validation:', val[-1])
for k in ('K5-under-M2', 'K2b-under-M4', 'K4-under-M3', 'K4b-pristine', 'K4b-under-M3',
          'K2c-under-M4', 'K1b-under-M2a', 'K5c-under-M2b'):
    v = kr[k]
    print(f"{k}: exit={v['exit']} {v['result']} verified={v['rules_verified']} "
          f"reasons={json.dumps(v['row_reasons'])[:200]}")
