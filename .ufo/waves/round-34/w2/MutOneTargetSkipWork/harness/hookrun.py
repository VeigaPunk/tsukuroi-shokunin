"""Untraced in-process observer (seat MutOneTargetSkipWork): run one tool with runpy and record,
through a sys.addaudithook 'subprocess.Popen' hook, the argv and the effective environment
(names only, plus the ZZ_R34_AMBIENT value) of every child it starts. No ptrace is involved;
TracerPid is recorded to show the run is untraced. Bounded at 200 records.
Usage: python3 hookrun.py <log.json> <tool.py> [tool args...]
"""
import json
import os
import runpy
import sys

log_path, tool, targs = sys.argv[1], sys.argv[2], sys.argv[3:]
recs = []


def _s(x):
    return os.fsdecode(x) if isinstance(x, bytes) else str(x)


def hook(event, args):
    if event == 'subprocess.Popen' and len(recs) < 200:
        _executable, argv, _cwd, env = args
        eff = dict(os.environ) if env is None else {_s(k): _s(v) for k, v in env.items()}
        recs.append({'argv': [_s(a) for a in argv], 'env_passed': env is not None,
                     'names': sorted(eff), 'ZZ_R34_AMBIENT': eff.get('ZZ_R34_AMBIENT')})


with open('/proc/self/status') as fh:
    tracer = [line.strip() for line in fh if line.startswith('TracerPid:')]
sys.addaudithook(hook)
sys.argv = [tool] + targs
rc = 0
try:
    runpy.run_path(tool, run_name='__main__')
except SystemExit as e:
    rc = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
with open(log_path, 'w') as fh:
    json.dump({'tracer': tracer, 'rc': rc, 'spawns': len(recs), 'records': recs}, fh)
