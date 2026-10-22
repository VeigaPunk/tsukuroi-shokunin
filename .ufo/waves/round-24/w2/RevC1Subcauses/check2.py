import json, collections, sys
sys.dont_write_bytecode = True
import recompute as R
B = json.load(open(R.F + 'bindings.json'))
E = json.load(open(R.F + 'events.json'))
bind = {s['name']: s for s in B['seats']}
L = R.LANE
print('--- outside-lane-root and schema/other rows (values verbatim) ---')
for f in json.load(open(R.OUT + 'recomputed-findings.json'))['findings']:
    if f['sub'] in (R.SUB_OUTSIDE, R.SUB_OTHER_OP) or f['id'] not in ('SCOPE-PATH-DENIED',):
        print(f['id'], f['site'], f['tool'], f['sub'], repr(f['value'])[:160])
print('--- exact lane root or lane root without slash referenced? ---')
for s in E['seats']:
    for i, ev in enumerate(s['events']):
        v = ev['args'].get('path') if isinstance(ev.get('args'), dict) else None
        if isinstance(v, str) and (v.rstrip('/') == L or v == L or v.startswith(L) and v[len(L):len(L)+1] not in ('/', '')):
            print('LANE-EDGE', s['name'], i, ev['tool'], repr(v)[:160])
print('--- ConnFxPlanner seat record (no events) ---')
cf = [s for s in E['seats'] if s['name'] == 'ConnFxPlanner'][0]
print({k: v for k, v in cf.items() if k != 'events'})
print('last 3 events of ConnFxPlanner:')
for ev in cf['events'][-3:]:
    print({k: (v if k != 'args' else {kk: str(vv)[:100] for kk, vv in v.items()}) for k, v in ev.items()})
print('first event:', {k: (v if k != 'args' else {kk: str(vv)[:100] for kk, vv in v.items()}) for k, v in cf['events'][0].items()})
