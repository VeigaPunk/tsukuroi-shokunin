#!/usr/bin/env python3
"""Determine which mutants change no outcome on base / H1 / H2 relative to the pristine probe.

Outcome = (exit code implied by the summary, leaking count, sorted leaking_pairs, harness_errors).
The pristine probe is the reference: a mutant that produces the identical outcome triple on all
three lanes is a SURVIVOR of the base/H1/H2 battery.
"""
import json
import os
import glob

SEAT = '/fast/scratch/hyaku/tsukuroi-r31/MutProbeC2'
RUNS = os.path.join(SEAT, 'runs')

ORDER = ['pristine'] + ['M%02d-drop-parity-check', ]  # placeholder, replaced below
SHORT = {
    'pristine': 'pristine',
    'M01-drop-parity-check': 'M01',
    'M02-drop-stdout-comparison': 'M02',
    'M03-drop-git-exec-count': 'M03',
    'M04-skip-first-exec-exclusion': 'M04',
    'M05-injection-by-variable-name': 'M05',
    'M06-no-LD_LIBRARY_PATH-in-injection': 'M06',
    'M07-no-PYTHONPATH-in-injection': 'M07',
    'M08-drop-control-B-determinism-check': 'M08',
    'M09-no-require-git-child': 'M09',
    'M10-supplementary-drop-stdout-and-exec-count': 'M10',
}
LANES = ['base', 'H1', 'H2']


def outcome(path):
    summ, per = None, {}
    for line in open(path, encoding='utf-8'):
        line = line.strip()
        if not line:
            continue
        o = json.loads(line)
        if 'channel' in o:
            per[o['channel']] = (bool(o.get('leak')), tuple(o.get('evidence') or ()))
        else:
            summ = o
    if summ is None:
        return None
    return {
        'leaking': summ.get('leaking'),
        'pairs': tuple(sorted(summ.get('leaking_pairs') or [])),
        'harness': tuple(summ.get('harness_errors') or ()),
        'per': {k: (v[0], v[1]) for k, v in sorted(per.items())},
    }


data = {}
for path in sorted(glob.glob(os.path.join(RUNS, '*.jsonl'))):
    base = os.path.basename(path)[:-len('.jsonl')]
    name, _, lab = base.rpartition('.')
    if name not in SHORT:
        continue
    data[(SHORT[name], lab)] = outcome(path)

ref = {lab: data[('pristine', lab)] for lab in LANES}
print('pristine reference outcomes:')
for lab in LANES:
    r = ref[lab]
    print('  %-5s leaking=%s pairs=%s harness=%s' % (lab, r['leaking'], r['pairs'], r['harness']))
print()

print('%-5s %-6s %-9s %-9s %-9s %s' % ('mut', 'lane', 'verdict', 'leaking', 'pairs', 'differs-from-pristine'))
print('-' * 110)
survivors = []
for short in SHORT.values():
    if short == 'pristine':
        continue
    differs = []
    for lab in LANES:
        o = data.get((short, lab))
        if o is None:
            differs.append('%s:MISSING' % lab)
            continue
        same = (o['leaking'] == ref[lab]['leaking'] and o['pairs'] == ref[lab]['pairs']
                and o['harness'] == ref[lab]['harness'])
        if not same:
            differs.append(lab)
        print('%-5s %-6s %-9s %-9s %-9s %s' % (
            short, lab, 'same' if same else 'DIFFERS', o['leaking'],
            ','.join(p.split(':')[-1] for p in o['pairs']) or '-',
            ','.join(differs) if differs else ''))
    print()
    if not differs:
        survivors.append(short)

print('SURVIVORS (no outcome change on base, H1 and H2):', survivors)

# second-level: which per-channel evidence differs even when the summary matches
print()
print('=== per-channel evidence differences vs pristine (same summary) ===')
for short in SHORT.values():
    if short == 'pristine':
        continue
    for lab in LANES:
        o = data.get((short, lab))
        if o is None:
            continue
        for ch in sorted(ref[lab]['per']):
            a = ref[lab]['per'][ch]
            b = o['per'].get(ch)
            if b != a:
                print('%-5s %-5s %-15s pristine=%s' % (short, lab, ch, a))
                print('%-5s %-5s %-15s mutant  =%s' % ('', '', '', b))
