#!/usr/bin/env python3
"""Local review evidence only; does not edit targets or frozen counters."""
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

SEAT = Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/w2/RevAllowCheckFreshnessR17')
SCRATCH = Path('/fast/scratch/hyaku/tsukuroi-r32/RevAllowCheckFreshnessR17')
REPO = SCRATCH / 'repo'
REVISIONS = ('44c8eee550a5dd7fa3729324f8dc77ececa3277b', 'b8bf150722a2261c80ab2ce012de3690ba732eeb')
TOOL = 'tools/check-freshness-r17.py'
HEX = re.compile(rb'\b[0-9a-f]{64}\b|\b[0-9a-f]{40}\b')
PLUMBING_ENV = {key: value for key, value in os.environ.items() if key not in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE')}
BASE_ENV = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'HOME': str(SCRATCH / 'home'), 'TMPDIR': '/tmp'}
INJECTED = {'R32_Freshness_Review_7kq': 'review-canary', 'BASH_ENV': '/nonexistent/review-bash-env', 'ENV': '/nonexistent/review-env', 'GCONV_PATH': '/nonexistent/review-gconv', 'PERL5OPT': '-MReviewCanaryNeverLoaded'}
for name in ('home', 'tmp'):
    (SCRATCH / name).mkdir(exist_ok=True)

commands = []
def invoke(command, timeout=180, environment=PLUMBING_ENV):
    argv = ['/usr/bin/timeout', '--kill-after=5', str(timeout), *command]
    result = subprocess.run(argv, cwd=REPO, env=environment, capture_output=True, timeout=timeout + 10)
    commands.append({'argv': argv, 'cwd': str(REPO), 'rc': result.returncode})
    return result

def git(*args):
    result = invoke(['/usr/bin/env', '-u', 'GIT_DIR', '-u', 'GIT_WORK_TREE', '-u', 'GIT_INDEX_FILE', '/usr/bin/git', '-C', str(REPO), *args], 30)
    if result.returncode:
        raise RuntimeError(result.stderr.decode('utf-8', 'replace'))
    return result.stdout

sources = {}
for revision in REVISIONS:
    sources[revision] = git('show', revision + ':' + TOOL)
(SEAT / 'assigned.diff').write_bytes(git('diff', *REVISIONS, '--', TOOL))

parsed = {revision: ast.parse(source, filename=TOOL) for revision, source in sources.items()}
def retained_ast(tree):
    body = []
    for index, node in enumerate(tree.body):
        if index == 0 and isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            continue
        if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == 'CHILD_ENV_BASE' for target in node.targets):
            continue
        if isinstance(node, ast.FunctionDef) and node.name == 'git_env':
            continue
        body.append(node)
    return ast.dump(ast.Module(body=body, type_ignores=[]), include_attributes=False)

inventory = {}
for revision, tree in parsed.items():
    inventory[revision] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            if node.func.value.id == 'subprocess' or (node.func.value.id == 'os' and node.func.attr in ('system', 'popen', 'execl', 'execv', 'execve', 'spawnl', 'spawnv', 'posix_spawn')):
                inventory[revision].append({'line': node.lineno, 'call': ast.unparse(node)})
    inventory[revision].sort(key=lambda item: item['line'])

summary = {'review_only': True, 'revisions': list(REVISIONS), 'tool': TOOL,
           'source_sha256': {revision: hashlib.sha256(source).hexdigest() for revision, source in sources.items()},
           'unchanged_ast_outside_module_docstring_CHILD_ENV_BASE_and_git_env': retained_ast(parsed[REVISIONS[0]]) == retained_ast(parsed[REVISIONS[1]]),
           'spawn_inventory': inventory, 'runs': []}

for revision in REVISIONS:
    git('checkout', '-q', revision)
    for mode in ('control', 'ambient'):
        label = revision[:8] + '-' + mode
        trace = SCRATCH / (label + '.execve')
        command = ['/usr/bin/bwrap', '--die-with-parent', '--ro-bind', '/', '/', '--bind', str(SCRATCH), str(SCRATCH), '--bind', str(SCRATCH / 'tmp'), '/tmp', '--proc', '/proc', '--dev', '/dev', '--chdir', str(REPO), '/usr/bin/strace', '-f', '-qq', '-v', '-s', '131072', '-e', 'trace=execve,execveat', '-o', str(trace), '/usr/bin/python3', str(REPO / TOOL), '--selftest']
        environment = dict(BASE_ENV)
        if mode == 'ambient':
            environment.update(INJECTED)
        result = invoke(command, 180, environment)
        (SEAT / (label + '.stdout')).write_bytes(result.stdout)
        (SEAT / (label + '.stderr')).write_bytes(result.stderr)
        if trace.exists():
            (SEAT / (label + '.execve')).write_bytes(trace.read_bytes())
        normal = result.stdout.replace(str(REPO).encode(), b'<WORK>').replace(str(SCRATCH).encode(), b'<ROOT>')
        normal = HEX.sub(b'<HEX>', normal)
        (SEAT / (label + '.normalised.stdout')).write_bytes(normal)
        summary['runs'].append({'revision': revision, 'mode': mode, 'rc': result.returncode, 'stdout': result.stdout.decode('utf-8', 'replace'), 'stderr': result.stderr.decode('utf-8', 'replace'), 'stdout_sha256': hashlib.sha256(result.stdout).hexdigest(), 'normalised_stdout_sha256': hashlib.sha256(normal).hexdigest(), 'trace': str(SEAT / (label + '.execve')) if trace.exists() else None, 'injected_names': list(INJECTED) if mode == 'ambient' else []})
        if result.returncode != 0:
            (SEAT / 'comparison.json').write_text(json.dumps(summary, indent=2) + '\n')
            (SEAT / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n')
            raise SystemExit('Selftest invocation failed; see comparison.json')

summary['all_stdout_byte_identical'] = len({run['stdout_sha256'] for run in summary['runs']}) == 1
summary['all_normalised_stdout_equal'] = len({run['normalised_stdout_sha256'] for run in summary['runs']}) == 1
summary['all_exit_codes_equal'] = len({run['rc'] for run in summary['runs']}) == 1
(SEAT / 'comparison.json').write_text(json.dumps(summary, indent=2) + '\n')
(SEAT / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n')
print(json.dumps(summary, indent=2))
