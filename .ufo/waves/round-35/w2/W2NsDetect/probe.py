#!/usr/bin/env python3
"""One bounded local detector and read-only environment comparison; not a C1 score."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import random
import stat
import subprocess
import sys

SEAT = Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2NsDetect')
SCRATCH = Path('/fast/scratch/hyaku/tsukuroi-r35/W2NsDetect')
REPO = SCRATCH / 'repo'
CENSUS = REPO / 'tools/tsukuroi-census.sh'
COUNTER = REPO / 'tools/score-pacnew-arm-r35b.py'
spec = importlib.util.spec_from_file_location('r35b', COUNTER)
counter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(counter)


def save(name, payload):
    text = json.dumps(payload, indent=2, sort_keys=True) + '\n'
    (SEAT / (name + '.json')).write_text(text)
    print(text, end='')


def bounded(argv, cwd, env, seconds=45):
    p = subprocess.run(['timeout', str(seconds)] + argv, cwd=str(cwd), env=env,
                       capture_output=True, text=True, timeout=seconds + 5)
    return {'argv': argv, 'cwd': str(cwd), 'exit': p.returncode,
            'stdout': p.stdout, 'stderr': p.stderr}


mode = sys.argv[1]
if mode == 'capture':
    data = CENSUS.read_bytes()
    (SCRATCH / 'census.pristine.sh').write_bytes(data)
    live = counter.oracle_of('/etc', Path('/var/log/pacman.log').read_text(errors='replace').splitlines())
    save('before', {'axes': ['coverage', 'control:named-limit'],
                    'pristine_sha256': hashlib.sha256(data).hexdigest(),
                    'counter_sha256': hashlib.sha256(COUNTER.read_bytes()).hexdigest(),
                    'live': live})
elif mode in ('pristine', 'mutated', 'restored'):
    root = SCRATCH / ('detector-' + mode)
    root.mkdir()
    etc, log, locked, expected = counter.build_fixture(random.Random(350235), str(root))
    env = counter.harness(str(root / 'h'))
    env.update(TSUKUROI_ETC_DIR=etc, TSUKUROI_PACMAN_LOG=log)
    pre = counter.snapshot(etc, log, locked), counter.ctimes(etc, log)
    result = bounded(['bash', str(CENSUS)], root, env)
    unchanged = counter.ctimes(etc, log) == pre[1] and counter.snapshot(etc, log, locked) == pre[0]
    ok, why, vals = counter.judge(result['stdout'], result['exit'], result['exit'] == 124,
                                  expected, unchanged)
    result.update(matches=ok, reason=why, expected=expected, reported=vals, unchanged=unchanged,
                  census_sha256=hashlib.sha256(CENSUS.read_bytes()).hexdigest())
    save('detector-' + mode, result)
elif mode == 'context':
    context_script = str(SEAT / 'context.sh')
    top = SCRATCH / 'context'
    top.mkdir()
    rows = [dict(view='host-live-like', **bounded(['bash', context_script], top,
                                                dict(counter.BASE_ENV)))]
    for i in range(3):
        root = top / ('v%02d' % (20 + i))
        root.mkdir()
        etc, log, locked, expected = counter.build_fixture(random.Random(350240 + i), str(root))
        rows.append(dict(view='namespace-' + str(i), **bounded(counter.ns_cmd(context_script, etc, log),
                                                              root, dict(counter.BASE_ENV))))
    save('context', {'counter_sha256': hashlib.sha256(COUNTER.read_bytes()).hexdigest(), 'rows': rows})
else:
    raise SystemExit('unsupported mode')
