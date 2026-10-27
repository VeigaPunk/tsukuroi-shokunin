#!/usr/bin/env python3
"""Diagnostic only (not the frozen counter): reproduce score-census-readers-r45.selftest()
exactly and print the FAIL lines, to name the case that failed once at the base revision."""
import os
import random
import subprocess
import sys

path = sys.argv[1]
iters = int(sys.argv[2]) if len(sys.argv) > 2 else 1
base = os.path.dirname(os.path.abspath(__file__))
for i in range(iters):
    tmp = os.path.join(base, 'probe-' + str(i))
    os.makedirs(tmp, exist_ok=True)
    e = {k: v for k, v in os.environ.items() if not k.startswith(('TSUKUROI_', 'UFO_'))}
    e['TMPDIR'] = tmp
    e['LC_ALL'] = 'C'
    p = subprocess.Popen(['bash', path, '--selftest'], cwd=tmp, env=e,
                         stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, start_new_session=True)
    out, err = p.communicate(timeout=900)
    text = (out + err).decode(errors='replace')
    fails = [ln for ln in text.splitlines() if ln.startswith('FAIL ')]
    summ = [ln for ln in text.splitlines() if ln.startswith('TSUKUROI_CENSUS_SELFTEST')]
    print('iter %d rc=%d' % (i, p.returncode), summ[-1] if summ else 'no summary')
    for f in fails:
        print('   ', f)
