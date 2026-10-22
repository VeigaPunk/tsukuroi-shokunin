import sys, json, copy, importlib.util
sys.dont_write_bytecode = True
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
REV = '5e7c04ecb02735491456de2b8bc44550d0db4609'
spec = importlib.util.spec_from_file_location('cmp_mp', LANE + '/tools/check-memory-pressure.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
base = mod.git_reader(LANE, REV)
ENTRY, SOURCES, LESSON, SKILL = mod.ENTRY, mod.SOURCES, mod.LESSON, mod.SKILL

def overlay(changes):
    def read(path):
        if path in changes:
            return changes[path]
        return base(path)
    return read

def entry_with(fn):
    e = json.loads(base(ENTRY).decode('utf-8'))
    fn(e)
    return json.dumps(e, ensure_ascii=False).encode('utf-8')

def row(e, rid):
    return [r for r in e['rows'] if r.get('id') == rid][0]

def summarize(name, read):
    code, res = mod.evaluate(read)
    bad = {r['id']: sorted({f['id'] for f in r['findings']}) for r in res['rows'] if r.get('findings')}
    blocking_global = [f['id'] for f in res['findings'] if f.get('blocking') and (f['id'] not in ())]
    blocking_any = sorted({f['id'] for f in res['findings'] if f.get('blocking')})
    print('%-34s exit=%d status=%s verified_rows=%s' % (name, code, res['status'], res['verified_rows']))
    print('    per-row findings:', bad if bad else 'none')
    print('    all blocking finding ids present:', blocking_any if blocking_any else 'none')
    return code, res

# Gate map sanity
gm = mod.gate_quotes(mod.decode(base(LESSON)))
print('GATE S115 quotes:', gm.get('S115'))
print('GATE S120 quotes:', gm.get('S120'))
print('GATE keys:', sorted(gm.keys()))
print()

summarize('M0 baseline 5e7c04ec', base)

def m1(e):
    row(e, 'MP1')['quotes'][0]['quote'] = 'The kernel chooses one victim process when pressure exceeds ninety percent.'
summarize('M1 fabricated entry quote', overlay({ENTRY: entry_with(m1)}))

def m2(e):
    row(e, 'MP1')['quotes'] = []
summarize('M2 MP1 entry quotes removed', overlay({ENTRY: entry_with(m2)}))

def m3(e):
    row(e, 'MP5')['statement'] = 'systemd-oomd kills a unit at 99 percent memory pressure over 5 seconds by default.'
summarize('M3 MP5 false statement', overlay({ENTRY: entry_with(m3)}))

def m4(e):
    row(e, 'MP2')['action'] = ''
summarize('M4 control: MP2 action empty', overlay({ENTRY: entry_with(m4)}))

def m5(e):
    e['rows'].append({'id': 'MP2', 'statement': '', 'verdict': '', 'action': '', 'sources': [],
                      'capture_pointers': [], 'quotes': []})
summarize('M5 duplicate defective MP2 row', overlay({ENTRY: entry_with(m5)}))

def stale(text):
    out = []
    for line in text.splitlines(keepends=True):
        if line.startswith('| S115 |'):
            line = line.replace('| 2026-10-22 |', '| 2026-10-21 |', 1)
        out.append(line)
    return ''.join(out).encode('utf-8')
summarize('M6 control: S115 opened 10-21', overlay({SOURCES: stale(mod.decode(base(SOURCES)))}))
