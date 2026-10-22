#!/usr/bin/env python3
"""Ambient-variable reach harness for the eleven frozen round-31 C2 tools (seat SentinelChildEnv).

Question: the C2 fix contract drops every inherited name that starts with GIT_, LD_ or PYTHON
from the environment a tool builds for a child process. Which OTHER ambient names still reach a
child after that contract, and does a child behave differently?

Method (measurement only; no candidate is asked to execute attacker code):
  * The frozen target set, the frozen argv and the frozen execve-trace parser are reused from
    `tools/probe-git-child-env-r31.py` (imported read-only, never modified).
  * For every target: one CONTROL run (hermetic ambient environment) and one CANARY run (the same
    environment plus one sentinel value per candidate ambient name).
  * REACH = the candidate's sentinel appears in the environment block of a descendant execve
    (any exec after the target's own first exec), i.e. the child inherited that name.
  * EFFECT is measured separately, per candidate, by `effects.py` (behaviour, not inheritance).

Sentinel values are inert markers under a private scratch directory, except where a name only
admits a legal value (locale names): those are detected by their exact value instead of a token.

Usage: python3 probe-ambient-child-env-r31.py --revision <REV> [--lane <repo>] [--scratch <dir>]
       [--only <tool> ...]
Output: one JSON line per (target, variable) that reached a child, then one summary line.
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

TOKEN = 'SENTINEL31'

# (name, kind). kind 'path' -> a sentinel directory path carrying the token (the value is inert
# unless a program interprets it); kind 'locale' -> a legal locale name detected by exact value;
# kind 'value' -> a sentinel scalar carrying the token.
CANDIDATES = (
    ('GCONV_PATH', 'path'),
    ('MALLOC_TRACE', 'path'),
    ('MALLOC_CHECK_', 'value'),
    ('MALLOC_PERTURB_', 'value'),
    ('MALLOC_MMAP_THRESHOLD_', 'value'),
    ('GLIBC_TUNABLES', 'value'),
    ('BASH_ENV', 'path'),
    ('ENV', 'path'),
    ('PERL5LIB', 'path'),
    ('PERL5OPT', 'value'),
    ('PERLLIB', 'path'),
    ('EDITOR', 'path'),
    ('VISUAL', 'path'),
    ('PAGER', 'path'),
    ('SSH_ASKPASS', 'path'),
    ('SSH_AUTH_SOCK', 'path'),
    ('TMPDIR', 'path'),
    ('LANG', 'locale'),
    ('LANGUAGE', 'locale'),
    ('LC_ALL', 'locale'),
    ('LC_MESSAGES', 'locale'),
    ('LC_CTYPE', 'locale'),
    ('LC_NUMERIC', 'locale'),
    ('LC_TIME', 'locale'),
    ('XDG_DATA_HOME', 'path'),
    ('XDG_CACHE_HOME', 'path'),
    ('XDG_STATE_HOME', 'path'),
    ('XDG_RUNTIME_DIR', 'path'),
    ('TERM', 'value'),
    ('HOSTALIASES', 'path'),
    ('RES_OPTIONS', 'value'),
    ('LOCALDOMAIN', 'value'),
    ('TZ', 'value'),
    ('COLUMNS', 'value'),
    ('LINES', 'value'),
    ('SSH_ASKPASS_REQUIRE', 'value'),
    ('LESS', 'value'),
    ('LESSOPEN', 'path'),
    ('GIT_SSH_COMMAND', 'path'),
    ('GIT_EXTERNAL_DIFF', 'path'),
    ('GIT_ASKPASS', 'path'),
    ('GIT_CONFIG_COUNT', 'value'),
    ('GIT_CONFIG_KEY_0', 'value'),
    ('GIT_CONFIG_VALUE_0', 'value'),
    ('GIT_EDITOR', 'path'),
    ('GIT_PAGER', 'path'),
    ('GIT_INDEX_FILE', 'path'),
    ('GIT_WORK_TREE', 'path'),
    ('GIT_DIR', 'path'),
    ('PYTHONPATH', 'path'),
    ('PYTHONHOME', 'path'),
    ('PYTHONSTARTUP', 'path'),
    ('LD_PRELOAD', 'path'),
    ('LD_LIBRARY_PATH', 'path'),
)

LOCALE_VALUE = 'en_US.utf8'


def load_probe(lane):
    path = os.path.join(lane, 'tools', 'probe-git-child-env-r31.py')
    spec = importlib.util.spec_from_file_location('frozen_probe_r31', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sentinel_env(root):
    """One sentinel value per candidate; the value carries the token unless a locale is required."""
    env = {}
    for name, kind in CANDIDATES:
        if kind == 'locale':
            env[name] = LOCALE_VALUE
            continue
        d = os.path.join(root, 'canary', name, TOKEN + '_' + name)
        os.makedirs(d, exist_ok=True)
        env[name] = d
    return env


def reached_vars(envp):
    out = set()
    for item in envp:
        for name, kind in CANDIDATES:
            if kind == 'locale':
                if item == name + '=' + LOCALE_VALUE:
                    out.add(name)
            elif (TOKEN + '_' + name) in item:
                out.add(name)
    return out


def run_target(probe, root, name, tree, tool, args, extra_env):
    work = os.path.join(root, name)
    home = os.path.join(work, 'home')
    tmp = os.path.join(work, 'tmp')
    os.makedirs(os.path.join(home, '.config'))
    os.makedirs(tmp)
    wtree = os.path.join(work, 'tree')
    shutil.copytree(tree, wtree, symlinks=True)
    env = probe.hermetic_env(home, tmp)
    env.pop('LC_ALL', None)          # keep the ambient locale observable
    if extra_env:
        env.update(extra_env)
    trace = os.path.join(root, name + '.trace')
    cmd = [probe.STRACE, '-f', '-qq', '-v', '-s', '65536', '-e', 'trace=execve', '-o', trace,
           '--', sys.executable, os.path.join(wtree, tool), *args]
    try:
        p = subprocess.run(cmd, cwd=wtree, env=env, capture_output=True, timeout=probe.TIMEOUT)
        rc, out, err = p.returncode, p.stdout, p.stderr.decode('utf-8', 'replace')[-300:]
    except subprocess.TimeoutExpired:
        rc, out, err = 'timeout', b'', 'timeout'
    execs = probe.parse_trace(trace) if os.path.exists(trace) else []
    out = out.replace(work.encode(), b'<WORK>').replace(root.encode(), b'<ROOT>')
    out = probe.HEX.sub(b'<HEX>', out)
    shutil.rmtree(wtree, ignore_errors=True)
    return {'rc': rc, 'stdout_sha256': hashlib.sha256(out).hexdigest(), 'stderr_tail': err,
            'execs': execs, 'git_execs': sum(1 for e in execs if probe.is_git(e[1]))}


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
    if parent:
        os.makedirs(parent, exist_ok=True)
    root = os.path.realpath(tempfile.mkdtemp(prefix='ambient-child-env-', dir=parent))
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
        ctl = run_target(probe, root, 'ctl-%d' % i, tree, tool, args, None)
        can = run_target(probe, root, 'can-%d' % i, tree, tool, args, canary)
        hits = {}
        for pid, fname, argvv, envp in can['execs'][1:]:
            for var in reached_vars(envp):
                hits.setdefault(var, []).append({'exec': fname, 'argv_head': argvv[:3]})
        for var, kind in CANDIDATES:
            if var not in hits:
                continue
            results.append({'tool': tool, 'variable': var, 'kind': kind, 'reach': True,
                            'child_count': len(hits[var]), 'children': hits[var][:2],
                            'control_rc': ctl['rc'], 'canary_rc': can['rc'],
                            'control_stdout_sha256': ctl['stdout_sha256'],
                            'canary_stdout_sha256': can['stdout_sha256'],
                            'parity_break': (ctl['rc'] != can['rc']
                                              or ctl['stdout_sha256'] != can['stdout_sha256'])})
        print(json.dumps({'tool': tool, 'phase': 'reach-summary', 'reached': sorted(hits),
                          'control_rc': ctl['rc'], 'canary_rc': can['rc'],
                          'control_stdout_sha256': ctl['stdout_sha256'],
                          'canary_stdout_sha256': can['stdout_sha256'],
                          'parity_break': (ctl['rc'] != can['rc']
                                            or ctl['stdout_sha256'] != can['stdout_sha256'])},
                         sort_keys=True), flush=True)
    summary = {'phase': 'reach-summary', 'revision': rev, 'rows': len(results), 'rows_detail': results}
    print(json.dumps(summary, sort_keys=True))
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reach.json'), 'w') as fh:
        json.dump(summary, fh, indent=1, sort_keys=True)
    shutil.rmtree(root, ignore_errors=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
