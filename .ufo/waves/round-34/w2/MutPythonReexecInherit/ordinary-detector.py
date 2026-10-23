#!/usr/bin/python3
"""Untraced selftest with a Python re-exec wrapper, logging one ambient canary only."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

BASE = Path('/fast/scratch/hyaku/tsukuroi-r34/MutPythonReexecInherit')
TARGET = BASE / 'repo/tools/check-seat-scope.py'
WRAPPER = BASE / 'python-child-wrapper'
OBSERVED = BASE / 'ordinary-child-observed.json'
STAGE = sys.argv[1]
assert STAGE in ('pristine', 'mutated', 'restored')
OBSERVED.unlink(missing_ok=True)
child_env = {k: v for k, v in os.environ.items() if not k.startswith(('GIT_', 'PYTHON', 'LD_'))}
child_env.update({'ZZ_R34_AMBIENT': 'r34_python_reexec_inherit',
                  'TMPDIR': str(BASE / 'ordinary-tmp')})
(BASE / 'ordinary-tmp').mkdir(exist_ok=True)
launch = (
    "import runpy,sys; "
    f"sys.path.insert(0,{str(TARGET.parent)!r}); "
    f"sys.executable={str(WRAPPER)!r}; "
    f"sys.argv=[{str(TARGET)!r},'--selftest']; "
    f"runpy.run_path({str(TARGET)!r},run_name='__main__')"
)
proc = subprocess.run(['/usr/bin/python3', '-B', '-c', launch], cwd=BASE / 'repo',
                      env=child_env, capture_output=True, text=True, timeout=120)
observation = json.loads(OBSERVED.read_text()) if OBSERVED.exists() else None
leaked = bool(observation and observation['ZZ_R34_AMBIENT'] == child_env['ZZ_R34_AMBIENT'])
record = {
    'stage': STAGE,
    'target_sha256': hashlib.sha256(TARGET.read_bytes()).hexdigest(),
    'selftest_exit': proc.returncode,
    'stdout': proc.stdout,
    'stderr': proc.stderr[-2000:],
    'child_observation': observation,
    'ambient_reached_python_child': leaked,
    'detector_exit': 2 if proc.returncode or observation is None else int(leaked),
    'traced': False,
    'method': 'sys.executable wrapper receives actual cli_case re-exec environment and execs /usr/bin/python3',
}
path = BASE / f'ordinary-{STAGE}.json'
path.write_text(json.dumps(record, sort_keys=True, indent=2) + '\n')
print(json.dumps(record, sort_keys=True))
sys.exit(record['detector_exit'])
