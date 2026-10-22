#!/usr/bin/env python3
"""Summarise the mutation matrix: per mutant, per lane state, the probe's verdict."""
import json
import os
import glob

SEAT = '/fast/scratch/hyaku/tsukuroi-r31/MutProbeC2'
RUNS = os.path.join(SEAT, 'runs')

names = ['pristine'] + ['M%02d' % i for i in range(1, 11)]
manifest = json.load(open(os.path.join(SEAT, 'mutants', 'manifest.json')))
labels = {m['name']: m['name'] for m in manifest['mutants']}

rows = {}
for path in sorted(glob.glob(os.path.join(RUNS, '*.jsonl'))):
    base = os.path.basename(path)[:-len('.jsonl')]
    name, _, lab = base.rpartition('.')
    rec = {'per_channel': {}, 'summary': None}
    for line in open(path, encoding='utf-8'):
        line = line.strip()
        if not line:
            continue
        obj = json.loads(line)
        if 'channel' in obj:
            rec['per_channel'][obj['channel']] = obj
        else:
            rec['summary'] = obj
    rows[(name, lab)] = rec

print('%-52s %-6s %-8s %-9s %-9s %s' % ('mutant', 'lane', 'leaking', 'pairs', 'harness', 'channels(leak)'))
print('-' * 130)
for name in names:
    for lab in ('base', 'H1', 'H2'):
        rec = rows.get((name, lab))
        if rec is None:
            print('%-52s %-6s MISSING' % (name, lab))
            continue
        s = rec['summary'] or {}
        chans = ', '.join('%s=%s' % (c, 'LEAK' if o.get('leak') else 'ok')
                          for c, o in sorted(rec['per_channel'].items()))
        print('%-52s %-6s %-8s %-9s %-9s %s' % (
            name, lab, s.get('leaking'), s.get('pairs'),
            ','.join(s.get('harness_errors') or []) or '-', chans))

print()
print('=== evidence detail ===')
for name in names:
    for lab in ('base', 'H1', 'H2'):
        rec = rows.get((name, lab))
        if not rec:
            continue
        for c, o in sorted(rec['per_channel'].items()):
            ev = o.get('evidence') or []
            print('%-52s %-5s %-15s leak=%-5s %s' % (name, lab, c, o.get('leak'),
                                                      ('| ' + '; '.join(ev)) if ev else ''))
        s = rec['summary'] or {}
        print('%-52s %-5s SUMMARY leaking=%s pairs=%s harness=%s exit-implied=%s' % (
            name, lab, s.get('leaking'), s.get('pairs'), s.get('harness_errors'),
            '2' if s.get('harness_errors') else ('1' if s.get('leaking') else '0')))
