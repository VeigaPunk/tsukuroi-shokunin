#!/usr/bin/env python3
"""Compare raw outputs and summarize exec environments without exposing ambient values."""
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

ROOT = Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/w2/RevAllowMutantsAdjacency')
SCRATCH = Path('/fast/scratch/hyaku/tsukuroi-r32/RevAllowMutantsAdjacency')
PROBE = Path('/fast/scratch/hyaku/tsukuroi-r32/RevAllowMutantsAdjacency/repo/tools/probe-child-env-allowlist-r32.py')
CANARY = 'R32_REVIEW_AMBIENT_CANARY'
EXPECTED = {'PATH', 'LC_ALL', 'GIT_CONFIG_NOSYSTEM', 'GIT_CONFIG_GLOBAL', 'GIT_CONFIG_SYSTEM', 'HOME', 'XDG_CONFIG_HOME', 'GIT_CEILING_DIRECTORIES'}
source = ast.parse(PROBE.read_bytes(), filename=str(PROBE))
functions = [n for n in source.body if isinstance(n, ast.FunctionDef) and n.name in ('parse_strings', 'parse_trace', 'is_git')]
scope = {'re': re, 'SYSTEM_GIT': '/usr/bin/git'}
exec(compile(ast.Module(body=functions, type_ignores=[]), str(PROBE), 'exec'), scope)
records = {}
for label in ('before', 'after'):
    trace = SCRATCH / (label + '.trace')
    events = scope['parse_trace'](str(trace))
    children = events[1:]
    result = {
        'trace': str(trace), 'trace_sha256': hashlib.sha256(trace.read_bytes()).hexdigest(),
        'successful_execs_excluding_initial_target': len(children),
        'program_counts': dict(Counter(e[1] for e in children)),
        'successful_git_execs': sum(scope['is_git'](e[1]) for e in children),
        'canary_present_in_initial_target': any(s.startswith(CANARY + '=') for s in events[0][3]),
        'child_execs_carrying_canary': sum(any(s.startswith(CANARY + '=') for s in e[3]) for e in children),
        'distinct_child_env_name_sets': sorted({tuple(sorted(s.split('=', 1)[0] for s in e[3])) for e in children}),
        'execs_not_using_exact_expected_key_set': sum({s.split('=', 1)[0] for s in e[3]} != EXPECTED for e in children),
        'non_git_internal_execs_with_unexpected_keys': sum({s.split('=', 1)[0] for s in e[3]} != EXPECTED for e in children if e[1] != '/usr/lib/git-core/git'),
        'missing_git_contract': sum(any(required not in e[3] for required in ('GIT_CONFIG_NOSYSTEM=1', 'GIT_CONFIG_GLOBAL=/dev/null', 'GIT_CONFIG_SYSTEM=/dev/null')) for e in children if scope['is_git'](e[1])),
        'direct_operation_counts': dict(Counter(
            next((arg for arg in e[2] if arg in ('rev-parse', 'archive', 'show', 'init', 'add', 'commit', 'checkout', 'clean', 'cat-file')), 'other')
            for e in children if scope['is_git'](e[1]))),
    }
    records[label] = result
before = json.loads((ROOT / 'before.run.json').read_text())
after = json.loads((ROOT / 'after.run.json').read_text())
before_rows = (ROOT / 'before.stdout').read_bytes().splitlines()
after_rows = (ROOT / 'after.stdout').read_bytes().splitlines()
records['comparison'] = {
    'exit_codes': [before['exit_code'], after['exit_code']],
    'normalized_stdout_equal': (ROOT / 'before.normalized.stdout').read_bytes() == (ROOT / 'after.normalized.stdout').read_bytes(),
    'normalized_stdout_sha256': before['normalized_stdout_sha256'],
    'all_33_non_summary_rows_byte_identical': len(before_rows) == len(after_rows) == 34 and before_rows[:-1] == after_rows[:-1],
    'differing_summary_keys': [k for k in before['summary'] if before['summary'].get(k) != after['summary'].get(k)],
    'successful_git_exec_counts_equal': records['before']['successful_git_execs'] == records['after']['successful_git_execs'],
    'both_stderr_empty': before['stderr_bytes'] == after['stderr_bytes'] == 0,
    'normalization': 'Frozen probe HEX regex (40- or 64-character lowercase hexadecimal words), with scratch/work prefixes replaced; no verdict field removed.',
    'trace_parser': 'Unmodified parse_strings, parse_trace and is_git function ASTs from frozen probe at b8bf150722a2261c80ab2ce012de3690ba732eeb.',
}
(ROOT / 'comparison.json').write_text(json.dumps(records, indent=2) + '\n')
print(json.dumps(records, indent=2))
