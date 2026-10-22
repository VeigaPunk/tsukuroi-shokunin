import json, collections, sys, re
sys.dont_write_bytecode = True
import recompute as R
B = json.load(open(R.F + 'bindings.json'))
E = json.load(open(R.F + 'events.json'))
bind = {s['name']: s for s in B['seats']}
def cutA(v):  # tool rule: first '?', then first ':'
    return v.split('?', 1)[0].split(':', 1)[0]
def cutC(v):  # alternative: first of ?, &, :, # (query/selector delimiters)
    return re.split(r'[?&:#]', v, 1)[0]
tally = collections.Counter()
examples = collections.defaultdict(list)
for s in E['seats']:
    seat = bind[s['name']]
    for i, ev in enumerate(s['events']):
        tool = ev['tool']
        if tool not in ('read', 'grep', 'glob', 'write'):
            continue
        for raw in (ev['args']['path'].split(';') if tool in ('grep', 'glob') else [ev['args']['path']]):
            path, kind = R.lookup(raw, selector=tool in ('read', 'grep'))
            if kind != 'PATH' or not raw.startswith(R.LANE + '/'):
                continue
            own = seat['write_paths'] if tool == 'write' else seat['read_paths']
            other = seat['read_paths'] if tool == 'write' else seat['write_paths']
            a = cutA(raw); c = cutC(raw)
            A_either = a in seat['read_paths'] or a in seat['write_paths']
            B_own = a in own
            C_either = c in seat['read_paths'] or c in seat['write_paths']
            C_own = c in own
            key = ('A_either' if A_either else 'A_undecl', 'B_own' if B_own else 'B_no', 'C_either' if C_either else 'C_undecl', 'C_own' if C_own else 'C_no')
            tally[key] += 1
            if len(examples[key]) < 2:
                examples[key].append((s['name'], i, tool, raw[len(R.LANE):][:140], 'A=' + a[len(R.LANE):], 'C=' + c[len(R.LANE):]))
for k, v in sorted(tally.items()):
    print(v, k)
    for e in examples[k]:
        print('    ', e)
