#!/usr/bin/env python3
"""Untraced builder-only check; neither argv label is present.

The v4shapes builder is a module-level statement. Execute that exact AST
statement, without its argument parser, clone, or mutation-battery workload.
Both environments are then handed to a real Python child.
"""
import ast
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path('/fast/scratch/hyaku/tsukuroi-r33a3/C07ArgvKeyed/repo')
SCRATCH = Path('/fast/scratch/hyaku/tsukuroi-r33a3/C07ArgvKeyed')
NAME = 'ZZ_R33A3_AMBIENT'
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / 'tools'))
from _revision import clean_env

assert '--selftest' not in sys.argv and '--counter-rev' not in sys.argv
assert os.environ[NAME] == '1'

def observe(label, built):
    child = subprocess.run(
        ['/usr/bin/python3', '-I', '-c',
         'import os; print("ZZ_R33A3_AMBIENT=" + os.environ.get("ZZ_R33A3_AMBIENT", "<absent>"))'],
        env=built, capture_output=True, text=True, check=True, timeout=10)
    print(json.dumps({'builder': label, 'argv_labels_present': False,
                      'builder_marker': built.get(NAME), 'child_rc': child.returncode,
                      'child_stdout': child.stdout.strip()}))

observe('_revision.clean_env', clean_env())
source = ROOT / 'tools/mutants-owed-statements-r29-v4shapes.py'
tree = ast.parse(source.read_bytes(), filename=str(source))
blocks = [node for node in tree.body if isinstance(node, ast.If)
          and any(isinstance(part, ast.Name) and part.id == 'ENV'
                  for part in ast.walk(node))]
assert len(blocks) == 1
with tempfile.TemporaryDirectory(prefix='ordinary-', dir=SCRATCH) as seat:
    home = os.path.join(seat, 'home')
    os.makedirs(os.path.join(home, '.config'))
    namespace = {'os': os, 'sys': sys, 'HOME': home, 'SEAT': seat}
    exec(compile(ast.Module(body=blocks, type_ignores=[]), str(source), 'exec'), namespace)
    observe('v4shapes.ENV exact module-level builder', namespace['ENV'])
