import json, collections, sys
sys.dont_write_bytecode = True
import recompute as R
C = json.load(open(R.COMMITTED))
print('per_finding entries', len(C['per_finding']), 'keys', sorted(C['per_finding'][0].keys()))
E = json.load(open(R.F + 'events.json'))
seat_ev = {s['name']: s['events'] for s in E['seats']}
mine = json.load(open(R.OUT + 'recomputed-findings.json'))['findings']
cm = collections.Counter((r['site'], r['finding'], r['operation'], r['subcause']) for r in C['per_finding'])
mm = collections.Counter((r['site'], r['id'], r['tool'], r['sub']) for r in mine)
print('per-finding (site,finding,operation,subcause) multiset: committed', sum(cm.values()), 'recomputed', sum(mm.values()))
print('only committed:', list((cm - mm).items())[:20])
print('only recomputed:', list((mm - cm).items())[:20])
# join check: request_line/call_id of each committed event-level row against the event at that index
bad = []
for r in C['per_finding']:
    if r['operation'] is None or r['site'] is None or ':' not in r['site']:
        continue
    name, idx = r['site'].rsplit(':', 1)
    ev = seat_ev[name][int(idx)]
    if ev['call_id'] != r['call_id'] or ev['request_line'] != r['request_line'] or ev['tool'] != r['operation']:
        bad.append((r['site'], r['call_id'], ev['call_id'], r['request_line'], ev['request_line'], r['operation'], ev['tool']))
print('join mismatches (call_id/request_line/tool vs event at index):', len(bad), bad[:5])
print('lower_bound flags', collections.Counter((r['site'].split(':')[0] == 'ConnFxPlanner', r['lower_bound']) for r in C['per_finding']))
print('seat_trace_complete flags', collections.Counter(r['seat_trace_complete'] for r in C['per_finding']))
