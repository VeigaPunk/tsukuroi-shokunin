#!/usr/bin/env python3
"""Build the C1-5 evidence summary: within-run invariants and base-vs-measured field classes.

Reads the eight run-receipt files and writes prior-counters-summary.json beside them.
Exit 0 when every within-run invariant holds and no counter moves PASS -> FAIL.
"""
import glob
import json
import os
import sys

A = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-44/w1/C1ExecPriorCounters'
BASE = '98020ece0674e0b569ee23aed10ffbee355b248e'
MEAS = '7e081698d4fc3c4ea944884fd093058de9909de1'
dec = json.JSONDecoder()


def objs(text):
    i, out = 0, []
    while True:
        while i < len(text) and text[i].isspace():
            i += 1
        if i >= len(text):
            return out
        try:
            o, i = dec.raw_decode(text, i)
        except ValueError:
            return out
        out.append(o)


def load(tool, rev):
    p = os.path.join(A, f'{tool}-{rev[:8]}.jsonl')
    o = objs(open(p, encoding='utf-8', errors='replace').read())
    return p, o[0], o[1], o[-1]


def item_matches(items):
    bad = []
    for n, it in enumerate(items or []):
        if isinstance(it, dict):
            ok = it.get('match', it.get('invariant', it.get('pass', True)))
            if ok is not True:
                bad.append({'index': n, 'item': it})
    return bad


def within(tool, body):
    """Return (ok, invariants) for one run of one counter."""
    inv = {}
    if tool.startswith('score-storage-arm-r38.py'):
        fx = body.get('fixtures', [])
        inv['fixtures_n'] = len(fx)
        inv['fixtures_matched'] = body.get('fixtures_matched')
        inv['fixtures_expected'] = body.get('fixtures_expected')
        inv['mismatched_fixtures'] = [f['fixture'] for f in fx if not f['match']]
        for f in fx:
            inv.setdefault('got_equals_expected_except', [])
            if list(f['expected']) != list(f['got']):
                inv['got_equals_expected_except'].append(f['fixture'])
        inv['live_match'] = body.get('live', {}).get('match')
        inv['live_census_exit'] = body.get('live', {}).get('census_exit')
        inv['six_planes_all'] = body.get('six_planes_all')
        ok = (inv['fixtures_n'] == 10 == inv['fixtures_expected']
              and inv['mismatched_fixtures'] == ['F06-no-btrfs-root']
              and inv['got_equals_expected_except'] == ['F06-no-btrfs-root']
              and inv['live_match'] is True and inv['six_planes_all'] == 1)
    elif tool.startswith('score-storage-arm-r38-q82.py'):
        inv['ns_available'] = body.get('ns_available')
        inv['ns_views_matched'] = body.get('ns_views_matched')
        inv['views_expected'] = body.get('views_expected')
        inv['views_n'] = len(body.get('views', []))
        inv['expected_equals_got'] = all(list(v['expected']) == list(v['got']) for v in body.get('views', []))
        inv['unmatched_items'] = item_matches(body.get('views'))
        ok = (inv['ns_available'] == 1 and inv['ns_views_matched'] == inv['views_expected'] == 3
              and inv['views_n'] == 3 and inv['expected_equals_got'] and not inv['unmatched_items'])
    elif tool.startswith('score-storage-hidden-r39.py'):
        for k in ('hidden_matched', 'views_matched', 'fixtures_matched', 'live_match', 'six_planes_all'):
            inv[k] = body.get(k)
        inv['unmatched_items'] = (item_matches(body.get('hidden')) + item_matches(body.get('views'))
                                  + item_matches(body.get('fixtures')) + item_matches([body.get('live')]))
        ok = (inv['hidden_matched'] == 2 and inv['views_matched'] == 3 and inv['fixtures_matched'] == 5
              and inv['live_match'] == 1 and inv['six_planes_all'] == 1 and not inv['unmatched_items'])
    else:  # r42
        for k in ('cases', 'invariant', 'ns_invariant', 'selftest_pass', 'default_equal', 'selftest_label', 'base'):
            inv[k] = body.get(k)
        inv['non_invariant_n'] = len(body.get('non_invariant', []))
        inv['per_case_not_invariant'] = [k for k, v in body.get('per_case', {}).items() if not v['invariant']]
        inv['ns_not_invariant'] = [k for k, v in body.get('ns_cases', {}).items() if not v['invariant']]
        ok = (inv['cases'] == inv['invariant'] == 10 and inv['ns_invariant'] == 3
              and inv['selftest_pass'] == 1 and inv['default_equal'] == 1
              and inv['non_invariant_n'] == 0 and not inv['per_case_not_invariant'] and not inv['ns_not_invariant'])
    return ok, inv


def flat_diff(a, b, path=''):
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            out += flat_diff(a.get(k), b.get(k), f'{path}.{k}' if path else k)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append((path, f'len {len(a)}', f'len {len(b)}'))
        for n, (x, y) in enumerate(zip(a, b)):
            out += flat_diff(x, y, f'{path}[{n}]')
    elif a != b:
        out.append((path, a, b))
    return out


TOOLS = ['score-storage-arm-r38.py', 'score-storage-arm-r38-q82.py',
         'score-storage-hidden-r39.py', 'score-size-invariance-r42.py']
RUN_VARYING = {'revision', 'seed', 'branch_tip', 'token'}
summary = {'counter': 'C1ExecPriorCounters (round-44 item C1-5)',
           'kill_rule': "a frozen predecessor storage counter FAILs at the measured revision where it PASSes at base",
           'base': BASE, 'measured': MEAS, 'counters': {}, 'all_within_ok': True, 'kill_triggered': []}
for tool in TOOLS:
    row = {}
    for tag, rev in (('base', BASE), ('measured', MEAS)):
        p, h, b, f = load(tool, rev)
        ok, inv = within(tool, b)
        row[tag] = {'receipt': os.path.basename(p), 'revision': h['revision'], 'tool_revision': h['tool_revision'],
                    'tool_sha256': h['tool_sha256'], 'argv': h['argv'], 'exit_code': f['exit_code'],
                    'timed_out': f['timed_out'], 'stderr_tail': f['stderr_tail'],
                    'verdict': b.get('result') or b.get('verdict'), 'within_ok': ok, 'within': inv,
                    'body': b}
        summary['all_within_ok'] = summary['all_within_ok'] and ok
    row['tool_sha256_equal'] = row['base']['tool_sha256'] == row['measured']['tool_sha256']
    row['verdict_change'] = f"{row['base']['verdict']} -> {row['measured']['verdict']}"
    row['kill'] = bool(row['base']['verdict'] == 'PASS' and row['measured']['verdict'] != 'PASS')
    if row['kill']:
        summary['kill_triggered'].append(tool)
    d = flat_diff(row['base']['body'], row['measured']['body'])
    row['changed_fields'] = {
        'total': len(d),
        'run_varying': [f'{p}: {x} -> {y}' for p, x, y in d if p.split('[')[0].split('.')[0] in RUN_VARYING],
        'other': [f'{p}: {json.dumps(x, sort_keys=True)[:200]} -> {json.dumps(y, sort_keys=True)[:200]}'
                  for p, x, y in d if p.split('[')[0].split('.')[0] not in RUN_VARYING],
    }
    for tag in ('base', 'measured'):
        row[tag].pop('body')
    summary['counters'][tool] = row
out = os.path.join(A, 'prior-counters-summary.json')
with open(out, 'w', encoding='utf-8') as fh:
    json.dump(summary, fh, indent=1, sort_keys=True)
    fh.write('\n')
print('wrote', out, os.path.getsize(out), 'bytes')
print('all_within_ok', summary['all_within_ok'], 'kill_triggered', summary['kill_triggered'])
for tool, r in summary['counters'].items():
    print(f"{tool:32s} {r['verdict_change']:12s} base_exit={r['base']['exit_code']} meas_exit={r['measured']['exit_code']}"
          f" sha_equal={r['tool_sha256_equal']} within_ok={r['base']['within_ok']}/{r['measured']['within_ok']}"
          f" changed={r['changed_fields']['total']} (run-varying {len(r['changed_fields']['run_varying'])},"
          f" other {len(r['changed_fields']['other'])})")
sys.exit(0 if summary['all_within_ok'] and not summary['kill_triggered'] else 1)
