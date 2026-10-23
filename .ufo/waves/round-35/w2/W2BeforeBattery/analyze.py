#!/usr/bin/env python3
"""Summarize a score-pacnew-arm-r35b receipt: full summary line plus, for every should-fail
arm, the view kinds that refused it and the dominant refusal reason."""
import json
import re
import sys
from collections import Counter

path = sys.argv[1]
rows = []
for line in open(path, encoding='utf-8', errors='replace'):
    line = line.strip()
    if not line:
        continue
    try:
        rows.append(json.loads(line))
    except ValueError:
        pass

header = next((r for r in rows if r.get('counter')), None)
footer = rows[-1] if rows and rows[-1].get('receipt_end') else None
summary = None
per = {}
for r in rows:
    if r.get('summary') == 1 and 'candidate_matches' in r:
        summary = r
    if 'census' in r and 'matches' in r:
        per.setdefault(r['census'], []).append(r)

if header:
    print('HEADER counter=%s version=%s battery=%s' % (header['counter'], header.get('version'),
                                                       header.get('battery')))
    print('HEADER counter_sha256=%s' % header.get('counter_sha256'))
    print('HEADER census_sha256=%s' % header.get('census_sha256'))
    print('HEADER revision=%s claim_base=%s seed=%s' % (header.get('revision'), header.get('claim_base'),
                                                        header.get('seed')))
if footer:
    print('FOOTER exit_code=%s timed_out=%s' % (footer.get('exit_code'), footer.get('timed_out')))
    if footer.get('stderr_tail'):
        print('FOOTER stderr_tail=%r' % footer['stderr_tail'][-300:])
print()
print('SUMMARY ' + json.dumps(summary, sort_keys=True) if summary else 'SUMMARY <missing>')
print()

for name in sorted(per):
    rs = per[name]
    nmatch = sum(1 for r in rs if r['matches'])
    kinds_refused = Counter()
    reasons = Counter()
    refused_views = []
    for r in rs:
        if not r['matches']:
            kind = 'ns' if r['view'].startswith('ns') else ('live' if r['view'] == 'live' else 'stub')
            kinds_refused[kind] += 1
            reasons[r.get('reason')] += 1
            refused_views.append('%s(%s)' % (r['view'], r.get('reason')))
    print('ARM %-24s matches=%2d/%2d refused_by_kind=%s' % (
        name, nmatch, len(rs), dict(kinds_refused)))
    print('    dominant_reason=%s' % (repr(reasons.most_common(1)[0]) if reasons else 'none'))
    print('    all_reasons=%s' % dict(reasons))
    print('    refused_views=%s' % ', '.join(refused_views))
