import sys, re, importlib.util, pathlib
sys.dont_write_bytecode = True
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
REV = '5e7c04ecb02735491456de2b8bc44550d0db4609'
W = pathlib.Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/RerunC2')
spec = importlib.util.spec_from_file_location('cmp_mp', LANE + '/tools/check-memory-pressure.py')
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
base = mod.git_reader(LANE, REV)
gm = mod.gate_quotes(mod.decode(base(mod.LESSON)))
def norm(s): return ' '.join(s.split())
files = {'S115': 'S115.raw'}  # placeholder replaced below
srcs = {sid: (W / 'src' / (sid + '.raw')) for sid in ['S115','S116','S117','S118','S119','S120','S121','S122','S123','S124']}
for sid in sorted(gm):
    if sid not in srcs:
        print(sid, 'not a URL source; quotes:', gm[sid]); continue
    raw = srcs[sid].read_text('utf-8', 'surrogateescape')
    lines = raw.splitlines()
    for q in gm[sid]:
        nq = norm(q)
        hit_lines = [i + 1 for i, l in enumerate(lines) if nq in norm(l)]
        if hit_lines:
            status = 'FOUND line(s) %s' % hit_lines[:5]
        else:
            joined = norm(raw)
            status = 'FOUND-MULTILINE' if nq in joined else 'NOT-IN-SOURCE'
        print(sid, '|', status, '|', q[:110])
