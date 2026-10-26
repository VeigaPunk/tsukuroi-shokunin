#!/usr/bin/env python3
"""Evidence capture for the F-3 production-identity legs.

Same mechanism as w1/C1CritNsView/uid1000.py (imported, unmodified: SPEC/BUILDER/INNER/UNSHARE/
qkk/pad), two differences:
  * the full `PLANE packages:` line and the census exit status are recorded, not the driver's
    160-char excerpt;
  * `--qm-clean` adds one stub case (`-Qm` answers with the census's own embedded
    R6_FOREIGN_BASELINE), so the foreign-watch arm cannot contribute a DEGRADED verdict and the
    packages plane's own verdict is the only thing left in the token stream.

Nothing else about the view changes: uid 1000 via the subuid mapping + setpriv, no TSUKUROI_*
in the environment, the same fabricated -Qkk text (1 MiB padding for `large`).

  capture.py CENSUS TOKEN TAG [--qm-clean] [--census-src CENSUS_FOR_BASELINE]
"""
import json
import os
import re
import subprocess
import sys

import uid1000 as m

argv = sys.argv[1:]
uid0 = '--uid0' in argv
if uid0:
    argv.remove('--uid0')
    # the counter's own leg shape: `unshare -rm`, scored code runs as uid 0
    m.UNSHARE = ['unshare', '-rm']
    m.INNER = m.INNER.replace(
        'exec setpriv --reuid=1000 --regid=1000 --clear-groups bash /mnt/census.sh </dev/null',
        'exec bash /mnt/census.sh </dev/null')
clean = '--qm-clean' in argv
if clean:
    argv.remove('--qm-clean')
census, token, tag = argv[0], argv[1], argv[2]

if clean:
    base_src = open(census).read()
    mbase = re.search(r"^R6_FOREIGN_BASELINE='(.*?)'\n", base_src, re.S | re.M)
    if not mbase:
        raise SystemExit('R6_FOREIGN_BASELINE not found')
    qm = mbase.group(1)
    if not qm.endswith('\n'):
        qm += '\n'
    m.SPEC = dict(m.SPEC)
    m.SPEC['pacman'] = m.SPEC['pacman'].replace(
        '  -Qkk) cat /mnt/qkk; exit "$(cat /mnt/qkk.rc)" ;;\n',
        '  -Qkk) cat /mnt/qkk; exit "$(cat /mnt/qkk.rc)" ;;\n'
        '  -Qm) cat /mnt/qm; exit 0 ;;\n')
    m.SPEC['qm'] = qm

out_lines = []
for large in (True, False):
    spec = dict(m.SPEC, qkk=m.qkk(large, token))
    env = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'HOME': '/mnt/home', 'TMPDIR': '/mnt/tmp'}
    p = subprocess.run(m.UNSHARE + ['sh', '-c', m.INNER, 'r42', m.BUILDER, census],
                       env=env, input=json.dumps(spec).encode(), capture_output=True, timeout=900)
    out = p.stdout.decode(errors='replace')
    pk = [ln for ln in out.splitlines() if ln.startswith('PLANE packages:')]
    out_lines.append(f'== {tag} {"large" if large else "small"} rc={p.returncode} bytes={len(p.stdout)} '
                     f'stderr={p.stderr.decode(errors="replace").strip()[:200]!r}')
    out_lines.append(f'   plane-lines={len(pk)}')
    for ln in pk:
        out_lines.append('   ' + ln)
    for ln in out.splitlines():
        if ln.startswith('EXIT') or ln.startswith('CENSUS') or 'summary' in ln.lower():
            out_lines.append('   | ' + ln)

print('\n'.join(out_lines))
