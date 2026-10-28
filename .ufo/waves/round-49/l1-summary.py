#!/usr/bin/env python3
"""Round-49 wave accounting (L1 integration helper, read-only).

Reads .ufo/waves/round-49/w1-dispatch.json and w1-results.json (when present) plus the seat
reports under .ufo/waves/round-49/w1/ and prints one table: seat, role, result entry, report,
first line, body bytes. Also prints the role mix, dead seats and the C1 binding summary.

Usage: python3 .ufo/waves/round-49/l1-summary.py [--json]
"""
import json
import os
import sys
from collections import Counter

L = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
W = f'{L}/.ufo/waves/round-49'
WD = f'{W}/w1'


def main():
    disp = json.load(open(f'{W}/w1-dispatch.json'))
    tasks = {t['name']: t['agent'] for t in disp['taskCall']['tasks']}
    res_path = f'{W}/w1-results.json'
    results = []
    if os.path.isfile(res_path):
        try:
            results = json.load(open(res_path)).get('results') or []
        except Exception as e:
            print(f'results unparsable: {type(e).__name__}: {e}')
    by_name = {}
    for r in results:
        if isinstance(r, dict) and r.get('name'):
            by_name.setdefault(r['name'], []).append(r)
    rows = []
    dead = []
    for name, role in sorted(tasks.items()):
        hits = by_name.get(name, [])
        path = os.path.join(WD, f'{name}.md')
        exists = os.path.isfile(path)
        first = body = None
        if exists:
            text = open(path, encoding='utf-8', errors='replace').read()
            lines = text.split('\n')
            first = lines[0][:90]
            body = len(text.encode('utf-8'))
        ok_result = len(hits) == 1 and hits[0].get('agent') == role and bool(hits[0].get('output'))
        rows.append({'seat': name, 'role': role, 'results': len(hits), 'result_ok': ok_result,
                     'report': exists, 'first': first, 'bytes': body})
        if not ok_result or not exists:
            dead.append(name)
    mix = Counter(t['agent'] for t in disp['taskCall']['tasks'])
    attack = sum(v for k, v in mix.items() if k in ('reviewer', 'critic', 'mutation-tester', 'labrat'))
    out = {'dispatched': len(tasks), 'results_entries': len(results), 'reports': sum(
        1 for r in rows if r['report']), 'mix': dict(mix), 'attack': attack,
        'attack_share': round(attack / max(1, len(tasks)), 3), 'missing_or_unbound': dead, 'rows': rows}
    if '--json' in sys.argv:
        print(json.dumps(out, indent=1))
        return
    print(f"dispatched={out['dispatched']} results={out['results_entries']} reports={out['reports']} "
          f"attack={attack}/{len(tasks)} ({out['attack_share']})")
    print('mix:', dict(sorted(mix.items())))
    for r in rows:
        flag = '' if (r['result_ok'] and r['report']) else '  <-- MISSING/UNBOUND'
        print(f"{r['seat']:22s} {r['role']:15s} res={r['results']} rep={int(r['report'])} "
              f"bytes={r['bytes']} {r['first'] or ''}{flag}")
    print('missing_or_unbound:', out['missing_or_unbound'])


if __name__ == '__main__':
    main()
