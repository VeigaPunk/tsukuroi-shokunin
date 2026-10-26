#!/usr/bin/env python3
"""Run the fixture-gated control census on a production-shaped view (8 real-ish -Qq names, no 'alpha')."""
import importlib.util
import os
import sys

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
COUNTER = os.path.join(LANE, 'tools/score-size-invariance-r42.py')
CENSUS = '/fast/scratch/hyaku/tsukuroi-r42/C1CritAxis/fx.gated/tools/tsukuroi-census.sh'
ROOT = '/fast/scratch/hyaku/tsukuroi-r42/C1CritAxis/rig'

spec = importlib.util.spec_from_file_location('sc', COUNTER)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

base = m.git_show(LANE, m.BASE, m.CENSUS)
disp, fxd = m.extract_builder(base)
os.makedirs(ROOT, exist_ok=True)
rig = m.Rig(ROOT, disp, fxd)

PQ = 'linux\nbash\nglibc\nsystemd\nmesa\nvim\nopenssl\nffmpeg\n'
ERR = 'error: bash: /usr/bin/x-prodcheck (Permission denied)\n'
SMALL = {'pq': PQ, 'qkk.out': ERR + 'bash: 10 total files, 0 altered files\n', 'qkk.rc': '1'}
LARGE = {'pq': PQ, 'qkk.out': ERR + ''.join(m.qkk_pad(m.PAD_BYTES)) + 'bash: 10 total files, 0 altered files\n',
         'qkk.rc': '1'}

for label, files in (('small', SMALL), ('large', LARGE)):
    fx = rig.fixture(files)
    out, rc = rig.run(CENSUS, fx)
    lines = [ln for ln in out.splitlines() if ln.startswith('PLANE packages')]
    print(label, 'rc=%d' % rc, lines[0][:220] if lines else '<no PLANE packages line>')
