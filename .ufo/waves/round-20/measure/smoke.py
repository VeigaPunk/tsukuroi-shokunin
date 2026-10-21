#!/usr/bin/env python3
"""L1-only stable changed-path CLI smoke; run only after every seat settles."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

BASE = '0cbc34dd6b20896085a8fb07943e3ea4027d8472'
LANE = Path(__file__).resolve().parents[4]
parser = argparse.ArgumentParser()
parser.add_argument('revision')
parser.add_argument('--out', default='smoke')
args = parser.parse_args()
REV = args.revision
if not re.fullmatch(r'[0-9a-f]{40}', REV):
    raise SystemExit('full landed commit required')
if not re.fullmatch(r'[A-Za-z0-9_-]+', args.out):
    raise SystemExit('single output child name required')
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
           GIT_OPTIONAL_LOCKS='0', PYTHONDONTWRITEBYTECODE='1', LC_ALL='C')
OUT = LANE / '.ufo/waves/round-20/measure' / args.out
OUT.mkdir(exist_ok=False)
paths = subprocess.check_output(['git', '-C', str(LANE), 'diff', '--name-only',
                                BASE, REV, '--', 'tools/'], env=ENV, text=True).splitlines()
expected = {'tools/_revision.py', 'tools/check-revision-binding.py',
            'tools/check-registry-coverage.py', 'tools/check-adjacency-anchors.py',
            'tools/check-recheck-commands.py'}
if set(paths) != expected:
    raise SystemExit('changed production tool set differs from declared five: ' + repr(paths))
results = []
with tempfile.TemporaryDirectory(prefix='tsukuroi-r20-smoke-') as tmp:
    clone = Path(tmp) / 'lane'
    subprocess.run(['git', '-c', 'core.hooksPath=' + os.devnull, 'clone', '--quiet',
                    '--no-hardlinks', str(LANE), str(clone)], env=ENV, check=True)
    subprocess.run(['git', '-C', str(clone), 'checkout', '--quiet', '--detach', REV],
                   env=ENV, check=True)
    for path in paths:
        command = ['python3', path] + ([] if path == 'tools/_revision.py' else ['--help'])
        want = 64 if path == 'tools/_revision.py' else 0
        p = subprocess.run(command, cwd=clone, env=ENV, capture_output=True,
                           text=True, timeout=60)
        key = Path(path).stem
        (OUT / (key + '.stdout')).write_text(p.stdout)
        (OUT / (key + '.stderr')).write_text(p.stderr)
        results.append({'path': path, 'command': command, 'exit': p.returncode,
                        'expected_exit': want, 'matched_exit': p.returncode == want,
                        'evaluator_sha256': hashlib.sha256((clone / path).read_bytes()).hexdigest()})
        print(path, p.returncode, 'expected', want, flush=True)
(OUT / 'results.json').write_text(json.dumps({'revision': REV, 'baseline': BASE,
    'changed_paths': paths, 'runs': results}, indent=2) + '\n')
raise SystemExit(0 if all(r['matched_exit'] for r in results) else 1)
