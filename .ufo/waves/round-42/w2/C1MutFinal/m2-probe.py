#!/usr/bin/env python3
"""C1MutFinal M2 divergence probe: pristine vs M2 (unanchored /error:/) on a plausible
-Qkk sample whose only 'error:' occurrence is mid-line (inside a warning's path)."""
import importlib.util, os, sys

S = '/fast/scratch/hyaku/tsukuroi-r42/C1MutFinal'
spec = importlib.util.spec_from_file_location(
    'ctr', '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/score-size-invariance-r42.py')
ctr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctr)

base_src = open(f'{S}/base-census-extracted.sh').read()
disp, fxd = ctr.extract_builder(base_src)
rig = ctr.Rig(os.path.join(S, 'm2probe', 'rig'), disp, fxd)

# Plausible sample: zero-altered summaries plus a warning line that merely CONTAINS
# 'error:' mid-line (a doc directory named .../error:). No line starts with 'error:'.
mid = 'warning: alpha: /usr/share/doc/error: notes (Modification time mismatch)\n'
files = {'qkk.out': ctr.SUMS[0] + mid + ctr.SUMS[1], 'qkk.rc': '1'}
fx = rig.fixture(files)

for name, path in (('pristine', f'{S}/base-census-extracted.sh'), ('M2', f'{S}/m2-census.sh')):
    out, rc = rig.run(path, fx)
    lines = [l for l in out.splitlines() if l.startswith('PLANE packages:')]
    print(f'{name}: rc={rc} plane={lines[0][:170] if lines else "NO PLANE LINE"}')
