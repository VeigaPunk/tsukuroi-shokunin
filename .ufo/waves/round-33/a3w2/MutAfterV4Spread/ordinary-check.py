#!/usr/bin/env python3
"""Evaluate the target's exact ENV expression and run a real, untraced child.

Only the top-level dict expression is evaluated, not the fixture-building CLI.
The HOME and SEAT locals are private paths; no target bytes are rewritten.
"""
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

source = Path('/fast/scratch/hyaku/tsukuroi-r33a3/MutAfterV4Spread/repo/tools/mutants-owed-statements-r29-v4shapes.py')
raw = source.read_bytes()
tree = ast.parse(raw, filename=str(source))
builders = [node.value for node in tree.body if isinstance(node, ast.Assign)
            and any(isinstance(name, ast.Name) and name.id == 'ENV' for name in node.targets)]
assert len(builders) == 1 and isinstance(builders[0], ast.Dict)
private = '/fast/scratch/hyaku/tsukuroi-r33a3/MutAfterV4Spread'
child_env = eval(compile(ast.Expression(builders[0]), str(source), 'eval'),
                 {'os': os, 'HOME': private, 'SEAT': private})
child = subprocess.run(
    [sys.executable, '-c',
     'import json,os; print(json.dumps({"ambient": os.environ.get("ZZ_R33A3_AMBIENT"), "git_nosystem": os.environ.get("GIT_CONFIG_NOSYSTEM"), "git_global": os.environ.get("GIT_CONFIG_GLOBAL")}))'],
    env=child_env, capture_output=True, text=True, timeout=10)
print(json.dumps({'source_sha256': hashlib.sha256(raw).hexdigest(),
                  'parent_sentinel': os.environ.get('ZZ_R33A3_AMBIENT'),
                  'child_exit_code': child.returncode,
                  'child_stdout': child.stdout.strip(), 'child_stderr': child.stderr}))
sys.exit(child.returncode)
