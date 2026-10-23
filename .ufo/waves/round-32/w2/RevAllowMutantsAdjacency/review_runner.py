#!/usr/bin/env python3
"""Scoped review evidence; does not modify a lane checkout or scoring predicate."""
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys

SCRATCH = Path('/fast/scratch/hyaku/tsukuroi-r32/RevAllowMutantsAdjacency')
EVIDENCE = Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/w2/RevAllowMutantsAdjacency')
REVISIONS = {
    'before': ('before-repo', '44c8eee550a5dd7fa3729324f8dc77ececa3277b'),
    'after': ('repo', 'b8bf150722a2261c80ab2ce012de3690ba732eeb'),
}
TOOL = 'tools/mutants-adjacency-overlap.py'
HEX = re.compile(rb'\b[0-9a-f]{64}\b|\b[0-9a-f]{40}\b')
CANARY = 'R32_REVIEW_AMBIENT_CANARY'


def canonical_behavior(path):
    tree = ast.parse(path.read_bytes(), filename=str(path))
    body = list(tree.body)
    if isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
        body.pop(0)
    body = [node for node in body if not (
        isinstance(node, ast.FunctionDef) and node.name == 'clean_env'
        or isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == 'CHILD_ENV_BASE'
            for target in node.targets))]
    return ast.dump(ast.Module(body=body, type_ignores=[]), include_attributes=False)


def static_review():
    before = SCRATCH / 'before-repo' / TOOL
    after = SCRATCH / 'repo' / TOOL
    tree = ast.parse(after.read_bytes(), filename=str(after))
    spawns = []
    wrappers = []
    ambient = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            callee = ast.unparse(node.func)
            if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == 'subprocess':
                spawns.append({'line': node.lineno, 'callee': callee,
                               'env': [ast.unparse(k.value) for k in node.keywords if k.arg == 'env']})
            if callee in ('sh', 'g'):
                wrappers.append({'line': node.lineno, 'call': ast.unparse(node)})
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == 'os' and node.attr in ('environ', 'getenv', 'system', 'execv', 'execve', 'spawnv', 'spawnve'):
            ambient.append({'line': node.lineno, 'expression': ast.unparse(node)})
    result = {
        'before_revision': REVISIONS['before'][1], 'after_revision': REVISIONS['after'][1],
        'behavior_ast_equal_excluding_clean_env_child_env_base_and_module_docstring': canonical_behavior(before) == canonical_behavior(after),
        'direct_spawn_sites': sorted(spawns, key=lambda x: x['line']),
        'all_direct_spawns_call_clean_env': all(s['env'] == ['clean_env()'] for s in spawns),
        'wrapper_calls': sorted(wrappers, key=lambda x: x['line']),
        'ambient_or_alternate_os_process_access': ambient,
        'before_sha256': hashlib.sha256(before.read_bytes()).hexdigest(),
        'after_sha256': hashlib.sha256(after.read_bytes()).hexdigest(),
    }
    (EVIDENCE / 'static-review.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2), flush=True)


def run_one(label):
    clone_name, revision = REVISIONS[label]
    clone = SCRATCH / clone_name
    work = SCRATCH / ('run-' + label)
    tmp = work / 'tmp'
    home = work / 'home'
    tmp.mkdir(parents=True, exist_ok=True)
    (home / '.config').mkdir(parents=True, exist_ok=True)
    env = {k: v for k, v in os.environ.items() if not k.startswith(('GIT_', 'LD_', 'PYTHON'))}
    env.update({'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'HOME': str(home),
                'XDG_CONFIG_HOME': str(home / '.config'), 'TMPDIR': '/tmp',
                CANARY: 'benignReviewMarker'})
    trace = SCRATCH / (label + '.trace')
    argv = ['/usr/bin/python3', str(clone / TOOL), '--base', revision, '--counter-rev', revision, '--lane', str(clone)]
    command = ['timeout', '--kill-after=10', '500', '/usr/bin/bwrap',
               '--ro-bind', '/', '/', '--bind', str(SCRATCH), str(SCRATCH),
               '--bind', str(EVIDENCE), str(EVIDENCE), '--bind', str(tmp), '/tmp',
               '--dev', '/dev',
               '--unshare-pid', '--unshare-ipc', '--unshare-uts', '--unshare-net',
               '--die-with-parent', '--chdir', str(clone),
               '/usr/bin/strace', '-f', '-qq', '-v', '-s', '65536', '-e', 'trace=execve',
               '-o', str(trace), '--', *argv]
    process = subprocess.Popen(command, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    try:
        stdout, stderr = process.communicate(timeout=520)
    except BaseException:
        os.killpg(process.pid, signal.SIGKILL)
        process.communicate()
        raise
    (EVIDENCE / (label + '.stdout')).write_bytes(stdout)
    (EVIDENCE / (label + '.stderr')).write_bytes(stderr)
    normalized = HEX.sub(b'<HEX>', stdout.replace(str(work).encode(), b'<WORK>').replace(str(SCRATCH).encode(), b'<ROOT>'))
    (EVIDENCE / (label + '.normalized.stdout')).write_bytes(normalized)
    record = {'revision': revision, 'argv': argv, 'command': command, 'exit_code': process.returncode,
              'stdout_sha256': hashlib.sha256(stdout).hexdigest(),
              'normalized_stdout_sha256': hashlib.sha256(normalized).hexdigest(),
              'stderr_sha256': hashlib.sha256(stderr).hexdigest(),
              'stdout_lines': len(stdout.splitlines()), 'stderr_bytes': len(stderr),
              'ambient_canary': CANARY, 'summary': json.loads(stdout.splitlines()[-1]) if stdout else None}
    (EVIDENCE / (label + '.run.json')).write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record, indent=2), flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'static':
        static_review()
    else:
        run_one(sys.argv[1])
