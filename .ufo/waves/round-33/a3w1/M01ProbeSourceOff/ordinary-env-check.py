#!/usr/bin/env python3
import ast
import json
import os
from pathlib import Path
import runpy
import subprocess

root = Path('/fast/scratch/hyaku/tsukuroi-r33a3/M01ProbeSourceOff')
tools = root / 'repo' / 'tools'
marker = 'ZZ_R33A3_AMBIENT'
revision = runpy.run_path(str(tools / '_revision.py'))
shapes = ast.parse((tools / 'mutants-owed-statements-r29-v4shapes.py').read_bytes())
builder = []
for node in shapes.body:
    is_tracer = isinstance(node, ast.With) and any(
        isinstance(item, ast.Constant) and item.value == '/proc/self/status'
        for item in ast.walk(node))
    is_env_assign = isinstance(node, ast.Assign) and any(
        isinstance(target, ast.Name) and target.id == 'ENV' for target in node.targets)
    is_env_update = (isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
                     and isinstance(node.value.func, ast.Attribute)
                     and isinstance(node.value.func.value, ast.Name)
                     and node.value.func.value.id == 'ENV')
    if is_tracer or is_env_assign or is_env_update:
        builder.append(node)
assert len(builder) == 3
home = root / 'ordinary-home'
(home / '.config').mkdir(parents=True, exist_ok=True)
namespace = {'os': os, 'HOME': str(home), 'SEAT': str(root)}
exec(compile(ast.Module(body=builder, type_ignores=[]), str(tools / 'mutants-owed-statements-r29-v4shapes.py'), 'exec'), namespace)
rows = []
for name, env in (('_revision.clean_env', revision['clean_env']()), ('v4shapes.ENV exact builder AST', namespace['ENV'])):
    child = subprocess.run(['/usr/bin/python3', '-c',
                            'import os; print(os.environ.get("ZZ_R33A3_AMBIENT", "ABSENT"))'],
                           env=env, capture_output=True, text=True, timeout=20, check=True)
    rows.append({'builder': name, 'ambient': os.environ.get(marker),
                 'child_stdout': child.stdout.strip(), 'child_exit': child.returncode})
with open('/proc/self/status', encoding='ascii') as status:
    tracer = next(line.strip() for line in status if line.startswith('TracerPid:'))
print(json.dumps({'tracer_status': tracer, 'rows': rows}))
raise SystemExit(0 if all(row['child_stdout'] == '1' for row in rows) else 1)
