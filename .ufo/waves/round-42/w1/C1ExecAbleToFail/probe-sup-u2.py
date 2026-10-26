#!/usr/bin/env python3
"""Probe: does any guard catch the -Sup name-extraction revert (v4-sup)?

Uses the frozen counter's own builders (extract_builder/Rig/case_files) so the fixture is the
counter's U2 shape (qu empty at rc=1, sup carrying the candidates) at both twin sizes.
Runs the implementation census and the v4-sup variant. Read-only on the counter; no mutation.
"""
import importlib.util
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
COUNTER = f'{LANE}/tools/score-size-invariance-r42.py'

spec = importlib.util.spec_from_file_location('sizeinv', COUNTER)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

base_src = mod.git_show(LANE, mod.BASE, mod.CENSUS)
dispatcher, fx_default = mod.extract_builder(base_src)

root = tempfile.mkdtemp(prefix='c1-sup-probe.', dir=HERE)
rig = mod.Rig(os.path.join(root, 'rig'), dispatcher, fx_default)

results = []
for label, census in (('impl', f'{HERE}/impl-census.sh'), ('v4-sup', f'{HERE}/v4-sup-census.sh')):
    for size in (False, True):
        files, norm = mod.case_files('U2', size)
        fx = rig.fixture(files)
        out, rc = rig.run(census, fx)
        text = mod.compared(out, rc, norm, fx)
        lines = [ln for ln in text.splitlines() if ln.startswith('PLANE update-safety:')
                 or ln.startswith('TSUKUROI_CENSUS:')]
        results.append({'census': label, 'twin': 'large' if size else 'small', 'rc': rc,
                        'sup_bytes': len(files.get('sup', '').encode()),
                        'lines': [ln[:240] for ln in lines],
                        'text_digest': __import__('hashlib').sha256(text.encode()).hexdigest()[:16]})
for r in results:
    print(r['census'], r['twin'], 'rc=%d' % r['rc'], 'sup=%dB' % r['sup_bytes'],
          'digest=' + r['text_digest'], '|', (r['lines'][0] if r['lines'] else '(no PLANE line)')[:200])
small_i = results[0]['text_digest'] == results[1]['text_digest']
small_v = results[2]['text_digest'] == results[3]['text_digest']
print('impl small==large:', small_i, '| v4-sup small==large:', small_v)
shutil.rmtree(root, ignore_errors=True)
