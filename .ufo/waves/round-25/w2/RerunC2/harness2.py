import sys, json, importlib.util
sys.dont_write_bytecode = True
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
REV = '5e7c04ecb02735491456de2b8bc44550d0db4609'
spec = importlib.util.spec_from_file_location('cmp_mp', LANE + '/tools/check-memory-pressure.py')
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
base = mod.git_reader(LANE, REV)
ENTRY, LESSON, SKILL, SOURCES = mod.ENTRY, mod.LESSON, mod.SKILL, mod.SOURCES
def overlay(changes):
    def read(path):
        return changes[path] if path in changes else base(path)
    return read
def entry_with(fn):
    e = json.loads(base(ENTRY).decode('utf-8')); fn(e)
    return json.dumps(e, ensure_ascii=False).encode('utf-8')
def row(e, rid):
    return [r for r in e['rows'] if r.get('id') == rid][0]
def report(name, read):
    code, res = mod.evaluate(read)
    per = {r['id']: sorted({f['id'] for f in r['findings']}) for r in res['rows'] if r.get('findings')}
    print('%-46s exit=%d status=%s verified_rows=%s' % (name, code, res['status'], res['verified_rows']))
    print('      per-row findings:', per if per else 'none')
# M7: remove the S115 table quote rows from the lesson; keep the prose line that yields 'mined'
def drop_s115_rows(text):
    return ''.join(l for l in text.splitlines(keepends=True) if not l.startswith('| S115 |')).encode('utf-8')
report('M7 S115 Gate table rows removed', overlay({LESSON: drop_s115_rows(mod.decode(base(LESSON)))}))
# M8: MP6 cites only S123 (oomd-manager.c, unrelated to OOM counters)
def m8(e):
    row(e, 'MP6')['sources'] = ['S123']
report('M8 MP6 sources replaced by S123 only', overlay({ENTRY: entry_with(m8)}))
# M9: MP6 cites S120 only (systemd oomd.conf defaults, unrelated to oom_kill counters)
def m9(e):
    row(e, 'MP6')['sources'] = ['S120']
report('M9 MP6 sources replaced by S120 only', overlay({ENTRY: entry_with(m9)}))
