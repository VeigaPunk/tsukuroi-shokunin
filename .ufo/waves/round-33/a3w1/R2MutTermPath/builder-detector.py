#!/usr/bin/env python3
"""Supplementary byte-bound builder slice, not the frozen end-to-end probe."""
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace

repo, stage, output = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
seat = output.parent
records = []
with tempfile.TemporaryDirectory(prefix='builder-slice-', dir=seat) as temporary:
    root = Path(temporary)
    home = root / 'home'
    home.mkdir()
    os.environ['TERM'] = 'R33A3_TERM_SENTINEL'
    os.environ['PATH'] = '/usr/bin:/bin:' + str(root / 'path-sentinel')
    for relative in ('tools/check-storage-health.py', 'tools/mutants-adjacency-overlap.py'):
        path = repo / relative
        source = path.read_bytes()
        tree = ast.parse(source, filename=str(path))
        selected = [node for node in tree.body
                    if (isinstance(node, ast.Assign)
                        and any(isinstance(target, ast.Name) and target.id == 'CHILD_ENV_BASE'
                                for target in node.targets))
                    or (isinstance(node, ast.FunctionDef) and node.name == 'clean_env')]
        if len(selected) != 2:
            raise RuntimeError('unexpected builder slice in ' + relative)
        namespace = {'os': os, 'Path': Path, 'HOME': str(home), 'ROOT': str(root),
                     '_GIT_HOME': home, '_GIT_SANDBOX': SimpleNamespace(name=str(root))}
        exec(compile(ast.Module(body=selected, type_ignores=[]), str(path), 'exec'), namespace)
        child_env = namespace['clean_env']()
        command = ['timeout', '15', '/usr/bin/python3', '-c',
                   'import os,json; print(json.dumps({k:os.environ.get(k) for k in '
                   '("TERM","PATH","GIT_CONFIG_NOSYSTEM","GIT_CONFIG_GLOBAL")}))']
        child = subprocess.run(command, cwd=root, env=child_env, capture_output=True,
                               text=True, timeout=20)
        values = json.loads(child.stdout) if child.returncode == 0 else {}
        reached = [name for name in ('TERM', 'PATH')
                   if values.get(name) == os.environ[name]]
        record = {'stage': stage, 'tool': relative,
                  'sha256': hashlib.sha256(source).hexdigest(),
                  'child_rc': child.returncode, 'stdout': child.stdout, 'stderr': child.stderr,
                  'ambient': {name: os.environ[name] for name in ('TERM', 'PATH')},
                  'values_reached': reached, 'leak': bool(reached)}
        records.append(record)
summary = {'stage': stage, 'detector': 'exact clean_env AST slice then actual Python child',
           'pairs': len(records), 'leaking': sum(record['leak'] for record in records),
           'harness_errors': [record['tool'] for record in records if record['child_rc'] != 0]}
summary['exit_code'] = 2 if summary['harness_errors'] else (1 if summary['leaking'] else 0)
output.write_text(''.join(json.dumps(record) + '\n' for record in [*records, summary]))
print(json.dumps(summary))
sys.exit(summary['exit_code'])
