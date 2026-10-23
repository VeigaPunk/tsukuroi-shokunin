#!/usr/bin/env python3
"""Bounded read-only git-spawn detector for the assigned inheritance mutation."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path('/fast/scratch/hyaku/tsukuroi-r34/C11InheritNoEnv')
REPO = ROOT / 'repo'
BASE = '6de666c427ba9aa6b4350561980bde8d0e7c261d'
TOOLS = ('check-boot-chain', 'check-btrfs-repair-r31', 'check-btrfs-space-r30',
         'check-locator-clarification', 'check-recheck-commands', 'check-section-citations',
         'check-seat-scope', 'check-source-scope-correction', 'measure-update-recheck')
phase = sys.argv[1]
for key in tuple(os.environ):
    if key.startswith('GIT_'):
        del os.environ[key]
os.environ.update({'GIT_R34_C11_MARKER': '1', 'ZZ_R34_AMBIENT': '1',
                   'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull,
                   'GIT_CONFIG_SYSTEM': os.devnull, 'PATH': '/usr/bin:/bin',
                   'TMPDIR': str(ROOT), 'LC_ALL': 'C'})
sys.path.insert(0, str(REPO / 'tools'))
active = None
spawns = []
def audit(event, args):
    if event == 'subprocess.Popen':
        executable, argv, cwd, explicit_env = args
        effective = os.environ if explicit_env is None else explicit_env
        spawns.append({'tool': active, 'argv': list(argv),
                       'env_omitted_or_none': explicit_env is None,
                       'git_marker': effective.get('GIT_R34_C11_MARKER'),
                       'ambient_marker': effective.get('ZZ_R34_AMBIENT')})
sys.addaudithook(audit)
rows = []
for index, name in enumerate(TOOLS):
    path = REPO / 'tools' / (name + '.py')
    original = path.read_bytes()
    if phase == 'pristine':
        backup = ROOT / 'pristine' / (name + '.py')
        backup.parent.mkdir(exist_ok=True)
        backup.write_bytes(original)
    spec = importlib.util.spec_from_file_location('c11_target_' + str(index), path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    active = name
    start = len(spawns)
    if name == 'check-btrfs-space-r30':
        result = module.git_reader(str(REPO), BASE)('SCORECARD.md')
        ok = bool(result)
    elif name in ('check-boot-chain', 'check-locator-clarification', 'check-section-citations'):
        result = module.git('rev-parse', '--is-inside-work-tree', repo=REPO)
        ok = result.returncode == 0 and result.stdout.strip() == b'true'
    else:
        result = module.git(str(REPO), 'rev-parse', '--is-inside-work-tree')
        ok = result.returncode == 0 and result.stdout.strip() == b'true'
    calls = spawns[start:]
    rows.append({'tool': name, 'sha256': hashlib.sha256(original).hexdigest(),
                 'read_ok': ok, 'spawns': calls,
                 'detector_pass': bool(calls) and ok and all(r['git_marker'] is None for r in calls)})
passed = all(row['detector_pass'] for row in rows)
payload = {'phase': phase, 'expected': 'git child strips GIT_R34_C11_MARKER',
           'passed': passed, 'rows': rows, 'exit_code': 0 if passed else 1}
out = ROOT / (phase + '-detector.json')
out.write_text(json.dumps(payload, indent=2) + '\n')
print(json.dumps(payload))
sys.exit(payload['exit_code'])
