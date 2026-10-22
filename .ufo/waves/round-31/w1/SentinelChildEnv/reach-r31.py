#!/usr/bin/env python3
"""Reach harness (fast form): which non-GIT_/LD_/PYTHON ambient names reach a child AFTER the C2 fix?

Seat SentinelChildEnv, round 31 wave 1. Companion to `effects-r31.py`.

The C2 fix contract drops every inherited name starting with GIT_, LD_ or PYTHON. Every tool builds
its child environment from `os.environ` minus those prefixes, so the reach question reduces to:
which OTHER inherited names are still present in a descendant execve's environment block?

Method: one CONTROL run and one CANARY run per target, where the canary run sets ONE sentinel value
for every non-dropped candidate at once (each value carries a unique token, and is chosen so it does
not perturb the run: paths point at private empty directories, locales at an installed locale).
The frozen probe's helpers supply the target set, the argv and the execve parser.

Output: reach.json (per tool: reached names) and one JSON line per tool.
Usage: python3 reach-r31.py --revision <REV> --lane <repo> [--only <tool> ...]
"""
import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

TOKEN = 'SENT31'
LOCALE = 'en_US.utf8'

# candidates that the C2 contract does NOT drop; grouped by the value shape that keeps them inert
PATH_VARS = (
    'GCONV_PATH', 'MALLOC_TRACE', 'BASH_ENV', 'ENV', 'PERL5LIB', 'PERLLIB',
    'EDITOR', 'VISUAL', 'PAGER', 'SSH_ASKPASS', 'SSH_AUTH_SOCK',
    'XDG_DATA_HOME', 'XDG_CACHE_HOME', 'XDG_STATE_HOME', 'XDG_RUNTIME_DIR',
    'HOSTALIASES', 'LESSOPEN', 'SSH_ASKPASS_REQUIRE',
)
VALUE_VARS = (
    'MALLOC_CHECK_', 'MALLOC_PERTURB_', 'MALLOC_MMAP_THRESHOLD_', 'GLIBC_TUNABLES',
    'PERL5OPT', 'TERM', 'RES_OPTIONS', 'LOCALDOMAIN', 'TZ', 'COLUMNS', 'LINES', 'LESS',
    'LC_ALL', 'LC_MESSAGES', 'LC_CTYPE', 'LC_NUMERIC', 'LC_TIME', 'LANG', 'LANGUAGE',
    'TMPDIR',
)
# NOTE TMPDIR is handled as a path; kept in VALUE_VARS list only for the name loop below.


def load_probe(lane):
    path = os.path.join(lane, 'tools', 'probe-git-child-env-r31.py')
    spec = importlib.util.spec_from_file_location('frozen_probe_r31', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sentinels(root):
    env = {}
    for v in PATH_VARS:
        d = os.path.join(root, 'canary', v, TOKEN + '_' + v)
        os.makedirs(d, exist_ok=True)
        env[v] = d
    d = os.path.join(root, 'canary', 'TMPDIR', TOKEN + '_TMPDIR')
    os.makedirs(d, exist_ok=True)
    env['TMPDIR'] = d
    for v in VALUE_VARS:
        if v == 'TMPDIR':
            continue
        if v in ('LC_ALL', 'LC_MESSAGES', 'LC_CTYPE', 'LC_NUMERIC', 'LC_TIME', 'LANG', 'LANGUAGE'):
            env[v] = LOCALE
        else:
            env[v] = TOKEN + '_' + v
    return env


def reached(envp):
    out = set()
    for item in envp:
        name = item.split('=', 1)[0]
        if name in PATH_VARS or name == 'TMPDIR':
            if (TOKEN + '_' + name) in item:
                out.add(name)
        elif name in VALUE_VARS:
            out.add(name)
    return out


def run(probe, root, name, tree, tool, args, extra):
    work = os.path.join(root, name)
    home, tmp = os.path.join(work, 'home'), os.path.join(work, 'tmp')
    os.makedirs(os.path.join(home, '.config'))
    os.makedirs(tmp)
    wtree = os.path.join(work, 'tree')
    shutil.copytree(tree, wtree, symlinks=True)
    env = probe.hermetic_env(home, tmp)
    env.pop('LC_ALL', None)
    if extra:
        env.update(extra)
    trace = os.path.join(root, name + '.trace')
    cmd = [probe.STRACE, '-f', '-qq', '-v', '-s', '65536', '-e', 'trace=execve', '-o', trace,
           '--', sys.executable, os.path.join(wtree, tool), *args]
    try:
        p = subprocess.run(cmd, cwd=wtree, env=env, capture_output=True, timeout=probe.TIMEOUT)
        rc, out = p.returncode, p.stdout
    except subprocess.TimeoutExpired:
        rc, out = 'timeout', b''
    execs = probe.parse_trace(trace) if os.path.exists(trace) else []
    out = out.replace(work.encode(), b'<W>').replace(root.encode(), b'<R>')
    out = probe.HEX.sub(b'<H>', out)
    shutil.rmtree(wtree, ignore_errors=True)
    return {'rc': rc, 'sha': hashlib.sha256(out).hexdigest(), 'execs': execs}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--revision', required=True)
    ap.add_argument('--lane', required=True)
    ap.add_argument('--scratch', default=None)
    ap.add_argument('--only', nargs='*', default=None)
    a = ap.parse_args()
    lane = os.path.realpath(a.lane)
    probe = load_probe(lane)
    parent = a.scratch or ('/fast/scratch/hyaku' if os.path.isdir('/fast/scratch/hyaku') else None)
    root = os.path.realpath(tempfile.mkdtemp(prefix='reach-r31-', dir=parent))
    penv = probe.plumbing_env(root)
    rev = probe.git(penv, '-C', lane, 'rev-parse', '--verify', a.revision + '^{commit}').stdout.decode().strip()
    tree = os.path.join(root, 'tree')
    probe.export_tree(lane, rev, tree, penv)
    clone = os.path.join(root, 'lane.git')
    probe.git(penv, 'clone', '-q', '--bare', '--no-local', lane, clone, timeout=600).check_returncode()
    can = sentinels(root)
    out_rows, summary = [], []
    for i, (tool, argv) in enumerate(probe.TARGETS):
        if a.only and tool not in a.only and os.path.basename(tool) not in a.only:
            continue
        args = [x.format(rev=rev, clone=clone) for x in argv]
        ctl = run(probe, root, 'c-%d' % i, tree, tool, args, None)
        cv = run(probe, root, 'v-%d' % i, tree, tool, args, can)
        hits = set()
        children = {}
        for pid, fname, argvv, envp in cv['execs'][1:]:
            for v in reached(envp):
                hits.add(v)
                children.setdefault(v, []).append(os.path.basename(fname))
        row = {'tool': tool, 'control_rc': ctl['rc'], 'canary_rc': cv['rc'],
               'parity_break': ctl['rc'] != cv['rc'] or ctl['sha'] != cv['sha'],
               'reached': sorted(hits),
               'children': {k: sorted(set(v))[:4] for k, v in sorted(children.items())},
               'exec_kinds': sorted({os.path.basename(e[1]) for e in cv['execs']})}
        out_rows.append(row)
        summary.append({'tool': tool, 'reached': sorted(hits), 'parity_break': row['parity_break'],
                        'n_reached': len(hits)})
        print(json.dumps(row, sort_keys=True), flush=True)
    payload = {'revision': rev, 'candidates_dropped_by_contract': 'GIT_*, LD_*, PYTHON*',
               'candidates_tested': sorted(set(PATH_VARS) | set(VALUE_VARS)),
               'rows': out_rows, 'summary': summary}
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reach.json'), 'w') as fh:
        json.dump(payload, fh, indent=1, sort_keys=True)
    print(json.dumps({'phase': 'summary', 'revision': rev, 'rows': summary}, sort_keys=True))
    shutil.rmtree(root, ignore_errors=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
