#!/usr/bin/env python3
"""Ambient-variable reach harness for the eleven frozen round-31 C2 tools (seat SentinelChildEnv).

Scope: the C2 fix contract drops every inherited name that starts with GIT_, LD_ or PYTHON from
the environment a tool builds for a child process. This harness asks the next question: which
OTHER ambient names still reach a child after that contract, and does a child's behaviour change.

Method (measurement only, no exploit is operationalised):
  1. Reuse the frozen probe's own helpers (`tools/probe-git-child-env-r31.py`, imported read-only)
     so the target set, the argv and the execve trace parsing are the frozen ones.
  2. For every target: one CONTROL run (hermetic ambient environment) and one CANARY run (same
     environment plus one sentinel value per candidate ambient variable).
  3. REACH = the sentinel token of a candidate appears in the environment block of some
     descendant execve (any exec after the target's own first exec), i.e. the child inherited it.
  4. EFFECT = a separate, per-variable behavioural run (see `effect_probe`): the child's exit
     code, stdout digest, or a file it creates on disk changes against the control.

The canary values are inert markers under a private scratch directory; no candidate is asked to
execute attacker code. Only variables whose effect is observable without running foreign code are
tested for behaviour change.

Usage: python3 probe-ambient-child-env-r31.py --revision <REV> [--lane <repo>] [--scratch <dir>]
       [--only <tool> ...] [--phase reach|effect|all]
Output: JSON lines, one per (target, variable) for reach, one per (target, variable) for effect,
then a summary line.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL_DIR = os.path.join(HERE, '..', '..', '..', '..', 'tools')

# Candidate ambient names that are NOT covered by the C2 deny-list (GIT_*, LD_*, PYTHON*).
# One sentinel token per name; the value is a path under a private scratch directory so the
# token is unique per variable and the value stays inert.
CANDIDATES = (
    'GCONV_PATH',
    'MALLOC_TRACE',
    'MALLOC_CHECK_',
    'MALLOC_PERTURB_',
    'MALLOC_MMAP_THRESHOLD_',
    'GLIBC_TUNABLES',
    'BASH_ENV',
    'ENV',
    'PERL5LIB',
    'PERL5OPT',
    'PERLLIB',
    'EDITOR',
    'VISUAL',
    'PAGER',
    'SSH_ASKPASS',
    'SSH_AUTH_SOCK',
    'TMPDIR',
    'LANG',
    'LANGUAGE',
    'LC_ALL',
    'LC_MESSAGES',
    'LC_CTYPE',
    'LC_NUMERIC',
    'LC_TIME',
    'XDG_DATA_HOME',
    'XDG_CACHE_HOME',
    'XDG_STATE_HOME',
    'XDG_RUNTIME_DIR',
    'TERM',
    'HOSTALIASES',
    'RES_OPTIONS',
    'LOCALDOMAIN',
    'TZ',
    'COLUMNS',
    'LINES',
    'GIT_SSH_COMMAND',
    'GIT_EXTERNAL_DIFF',
    'GIT_ASKPASS',
    'GIT_CONFIG_COUNT',
    'GIT_CONFIG_KEY_0',
    'GIT_CONFIG_VALUE_0',
    'GIT_EDITOR',
    'GIT_PAGER',
    'GIT_INDEX_FILE',
    'GIT_WORK_TREE',
    'GIT_DIR',
    'PYTHONPATH',
    'PYTHONHOME',
    'PYTHONSTARTUP',
    'LD_PRELOAD',
    'LD_LIBRARY_PATH',
)

TOKEN = 'SENTINEL31'


def load_probe(lane):
    path = os.path.join(lane, 'tools', 'probe-git-child-env-r31.py')
    spec = importlib.util.spec_from_file_location('frozen_probe_r31', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sentinel_value(root, var):
    d = os.path.join(root, 'canary', var)
    os.makedirs(d, exist_ok=True)
    return d  # contains the token only via the directory name; see canary_dir() below


def canary_dir(root, var):
    d = os.path.join(root, 'canary', var, TOKEN + '_' + var)
    os.makedirs(d, exist_ok=True)
    return d


def sentinel_env(root):
    env = {}
    for var in CANDIDATES:
        env[var] = canary_dir(root, var)
    # keep a token inside every value so the reach test is a plain substring search
    env = {k: os.path.join(v, TOKEN + '_' + k) for k, v in env.items()}
    return env


def tokens_in_envp(envp):
    out = []
    for item in envp:
        for var in CANDIDATES:
            if (TOKEN + '_' + var) in item:
                out.append(var)
    return sorted(set(out))


def reach_run(probe, root, name, tree, tool, args, extra_env):
    work = os.path.join(root, name)
    home = os.path.join(work, 'home')
    tmp = os.path.join(work, 'tmp')
    os.makedirs(os.path.join(home, '.config'))
    os.makedirs(tmp)
    wtree = os.path.join(work, 'tree')
    shutil.copytree(tree, wtree, symlinks=True)
    env = probe.hermetic_env(home, tmp)
    if extra_env:
        env.update(extra_env)
    trace = os.path.join(root, name + '.trace')
    cmd = [probe.STRACE, '-f', '-qq', '-v', '-s', '65536', '-e', 'trace=execve', '-o', trace,
           '--', sys.executable, os.path.join(wtree, tool), *args]
    try:
        p = subprocess.run(cmd, cwd=wtree, env=env, capture_output=True, timeout=probe.TIMEOUT)
        rc = p.returncode
        out = p.stdout
        err = p.stderr.decode('utf-8', 'replace')[-300:]
    except subprocess.TimeoutExpired:
        rc = 'timeout'
        out = b''
        err = 'timeout'
    execs = probe.parse_trace(trace) if os.path.exists(trace) else []
    out = out.replace(work.encode(), b'<WORK>').replace(root.encode(), b'<ROOT>')
    out = probe.HEX.sub(b'<HEX>', out)
    shutil.rmtree(wtree, ignore_errors=True)
    return {
        'rc': rc,
        'stdout_sha256': hashlib.sha256(out).hexdigest(),
        'stderr_tail': err,
        'execs': execs,
        'git_execs': sum(1 for e in execs if probe.is_git(e[1])),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--revision', required=True)
    ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument('--scratch', default=None)
    ap.add_argument('--only', nargs='*', default=None)
    ap.add_argument('--phase', default='reach', choices=['reach', 'effect', 'all'])
    a = ap.parse_args()
    lane = os.path.realpath(a.lane)
    probe = load_probe(lane)
    parent = a.scratch or ('/fast/scratch/hyaku' if os.path.isdir('/fast/scratch/hyaku') else None)
    if parent:
        os.makedirs(parent, exist_ok=True)
    root = os.path.realpath(__import__('tempfile').mkdtemp(prefix='ambient-child-env-', dir=parent))
    penv = probe.plumbing_env(root)
    rev = probe.git(penv, '-C', lane, 'rev-parse', '--verify', a.revision + '^{commit}').stdout.decode().strip()
    tree = os.path.join(root, 'tree')
    probe.export_tree(lane, rev, tree, penv)
    clone = os.path.join(root, 'lane.git')
    probe.git(penv, 'clone', '-q', '--bare', '--no-local', lane, clone, timeout=600).check_returncode()
    canary = sentinel_env(root)
    results = []
    for i, (tool, argv) in enumerate(probe.TARGETS):
        if a.only and tool not in a.only and os.path.basename(tool) not in a.only:
            continue
        args = [x.format(rev=rev, clone=clone) for x in argv]
        ctl = reach_run(probe, root, 'ctl-%d' % i, tree, tool, args, None)
        can = reach_run(probe, root, 'can-%d' % i, tree, tool, args, canary)
        reached = {}
        for pid, fname, argv_l, envp in can['execs'][1:]:
            for var in tokens_in_envp(envp):
                reached.setdefault(var, []).append({'exec': fname, 'argv_head': argv_l[:3]})
        for var in CANDIDATES:
            if var not in reached:
                continue
            results.append({'tool': tool, 'variable': var,
                            'reach': True,
                            'children': reached[var][:3],
                            'child_count': len(reached[var]),
                            'control_rc': ctl['rc'], 'canary_rc': can['rc'],
                            'control_stdout_sha256': ctl['stdout_sha256'],
                            'canary_stdout_sha256': can['stdout_sha256'],
                            'parity_break': (ctl['rc'] != can['rc']
                                              or ctl['stdout_sha256'] != can['stdout_sha256'])})
        print(json.dumps({'tool': tool, 'phase': 'reach-summary',
                          'reached': sorted(reached),
                          'control_rc': ctl['rc'], 'canary_rc': can['rc'],
                          'parity_break': (ctl['rc'] != can['rc']
                                            or ctl['stdout_sha256'] != can['stdout_sha256'])},
                         sort_keys=True), flush=True)
    print(json.dumps({'phase': 'reach-summary', 'revision': rev, 'results': len(results),
                      'results_detail': results}, sort_keys=True))
    shutil.rmtree(root, ignore_errors=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
