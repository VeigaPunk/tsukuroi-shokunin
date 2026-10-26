#!/usr/bin/env python3
"""Three-way production-shaped probe: base census, tip census, fixture-gated control census."""
import importlib.util
import os
import subprocess

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
COUNTER = os.path.join(LANE, 'tools/score-size-invariance-r42.py')
S = '/fast/scratch/hyaku/tsukuroi-r42/C1CritAxis'
ROOT = os.path.join(S, 'rig3')

spec = importlib.util.spec_from_file_location('sc', COUNTER)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

base_src = m.git_show(LANE, m.BASE, m.CENSUS)
disp, fxd = m.extract_builder(base_src)
os.makedirs(ROOT, exist_ok=True)
rig = m.Rig(ROOT, disp, fxd)

base_c = os.path.join(S, 'base-census.sh')
with open(base_c, 'w') as f:
    f.write(base_src)

PQ = 'linux\nbash\nglibc\nsystemd\nmesa\nvim\nopenssl\nffmpeg\n'
ERR = 'error: bash: /usr/bin/x-prodcheck (Permission denied)\n'
SMALL = {'pq': PQ, 'qkk.out': ERR + 'bash: 10 total files, 0 altered files\n', 'qkk.rc': '1'}
LARGE = {'pq': PQ, 'qkk.out': ERR + ''.join(m.qkk_pad(m.PAD_BYTES)) + 'bash: 10 total files, 0 altered files\n',
         'qkk.rc': '1'}

CENSUSES = [('base', base_c), ('tip', os.path.join(LANE, 'tools/tsukuroi-census.sh')),
            ('gated', os.path.join(S, 'fx.gated/tools/tsukuroi-census.sh'))]
for label, files in (('small', SMALL), ('large', LARGE)):
    fx = rig.fixture(files)
    for name, cens in CENSUSES:
        out, rc = rig.run(cens, fx)
        lines = [ln for ln in out.splitlines() if ln.startswith('PLANE packages')]
        print('%-5s %-5s rc=%-3d %s' % (label, name, rc,
              (lines[0][:150] if lines else '<no PLANE packages line>')))
