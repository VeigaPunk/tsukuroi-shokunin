#!/usr/bin/env python3
"""Inherited-GIT_* leak probe for the lane tools that run git writes (round 29, claim C2,
axis operability).

Origin: round 28, seat SentinelBattery ran `tools/mutants-adjacency-overlap.py` once with
`GIT_DIR` pointed at the lane `.git`, and the battery's sandbox commits landed in the lane
(`corpus/lessons/round-28.md`, R28-SEAT-COMMITTED-IN-LANE and its correction).  A tool that
builds a private sandbox repository but passes the caller's environment to git obeys an
inherited `GIT_DIR`, `GIT_WORK_TREE` or `GIT_INDEX_FILE` and writes wherever they point.

FROZEN target set: the eight tools whose source at the round-29 base `16e9ab2a` invokes a git
write (`init`, `add`, `commit`; found by `grep -lE "'(init|commit|add)'|git (init|commit|add)"
tools/*`), each in the mode that performs it (`--selftest`, or the battery run).

For each target the probe, entirely under a private scratch directory (never the lane):
 1. exports the tool tree with `git archive <REV>` and makes a bare clone of the lane for the
    batteries' `--lane` reads;
 2. builds a CANARY repository with one commit and records its fingerprint (HEAD, every ref,
    the loose and packed object files, the index digest);
 3. CONTROL run: the tool with every GIT_* variable removed;
 4. CANARY run: the same command with `GIT_DIR`, `GIT_WORK_TREE` and `GIT_INDEX_FILE` set to
    the canary;
 5. LEAK when the canary fingerprint changed, or the canary run's exit code differs from the
    control run's (the tool's git reads or writes followed the inherited variables).
A target whose control run fails or times out is a harness error, not a leak.

Usage: python3 tools/probe-git-env-leak.py --revision <REV> [--lane <repo>] [--scratch <dir>]
       [--only <tool> ...]
Output: one JSON line per target, then a summary JSON line with `targets`, `leaking`,
`leaking_tools`, `harness_errors`.  Exit 0 when leaking is 0 and there is no harness error,
1 when a target leaks, 2 on a harness error.
"""
import argparse
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile

TARGETS = (
    ('tools/check-adjacency-overlap.py', ['--selftest']),
    ('tools/check-freshness-r17.py', ['--selftest']),
    ('tools/check-kernel-taint.py', ['--selftest']),
    ('tools/check-memory-pressure.py', ['--selftest']),
    ('tools/check-registry-coverage.py', ['--selftest']),
    ('tools/check-storage-health.py', ['--selftest']),
    ('tools/mutants-adjacency-overlap.py', ['--base', '{rev}', '--counter-rev', '{rev}', '--lane', '{clone}']),
    ('tools/mutants-kernel-taint.py', ['--base', '{rev}', '--counter-rev', '{rev}', '--lane', '{clone}']),
)
TIMEOUT = 900


def clean_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update({'GIT_CONFIG_NOSYSTEM': '1', 'LC_ALL': 'C'})
    return env


def run(cmd, cwd=None, env=None, timeout=120):
    return subprocess.run(cmd, cwd=cwd, env=env or clean_env(), capture_output=True, timeout=timeout)


def fingerprint(canary):
    gd = os.path.join(canary, '.git')
    h = hashlib.sha256()
    h.update(run(['git', '-C', canary, 'rev-parse', 'HEAD']).stdout)
    h.update(run(['git', '-C', canary, 'for-each-ref', '--format=%(refname) %(objectname)']).stdout)
    for sub in ('objects', 'refs'):
        for dp, _dn, fn in sorted(os.walk(os.path.join(gd, sub))):
            for f in sorted(fn):
                h.update(os.path.relpath(os.path.join(dp, f), gd).encode() + b'\n')
    for f in ('HEAD', 'index', 'packed-refs'):
        p = os.path.join(gd, f)
        if os.path.exists(p):
            with open(p, 'rb') as fh:
                h.update(f.encode() + hashlib.sha256(fh.read()).digest())
    return h.hexdigest()


def make_canary(path):
    os.makedirs(path)
    run(['git', 'init', '-q', '-b', 'canary', path]).check_returncode()
    with open(os.path.join(path, 'CANARY'), 'w') as fh:
        fh.write('canary\n')
    run(['git', '-C', path, 'add', 'CANARY']).check_returncode()
    run(['git', '-C', path, '-c', 'user.name=probe', '-c', 'user.email=probe@invalid',
         '-c', 'commit.gpgsign=false', 'commit', '-qm', 'canary']).check_returncode()


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--revision', required=True)
    ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument('--scratch', default=None)
    ap.add_argument('--only', nargs='*', default=None)
    a = ap.parse_args()
    lane = os.path.realpath(a.lane)
    parent = a.scratch or ('/fast/scratch/hyaku' if os.path.isdir('/fast/scratch/hyaku') else None)
    if parent:
        os.makedirs(parent, exist_ok=True)
    root = tempfile.mkdtemp(prefix='git-env-probe-', dir=parent)
    if os.path.commonpath([os.path.realpath(root), lane]) == lane:
        print(json.dumps({'error': 'scratch is inside the lane', 'scratch': root}))
        return 2
    p = run(['git', '-C', lane, 'rev-parse', '--verify', a.revision + '^{commit}'])
    if p.returncode != 0:
        print(json.dumps({'error': 'revision unreadable', 'revision': a.revision}))
        return 2
    rev = p.stdout.decode().strip()
    tree = os.path.join(root, 'tree')
    os.makedirs(tree)
    tar = run(['git', '-C', lane, 'archive', rev]).stdout
    with tarfile.open(fileobj=io.BytesIO(tar)) as t:
        t.extractall(tree, filter='data')
    clone = os.path.join(root, 'lane.git')
    run(['git', 'clone', '-q', '--bare', '--no-local', lane, clone], timeout=600).check_returncode()
    results, leaking, errors = [], [], []
    for i, (tool, argv) in enumerate(TARGETS):
        if a.only and tool not in a.only and os.path.basename(tool) not in a.only:
            continue
        args = [x.format(rev=rev, clone=clone) for x in argv]
        cmd = [sys.executable, os.path.join(tree, tool), *args]
        res = {'tool': tool, 'argv': args}
        try:
            ctl = run(cmd, cwd=tree, timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            res['harness_error'] = 'control run timed out'
            errors.append(tool)
            results.append(res)
            print(json.dumps(res), flush=True)
            continue
        res['control_rc'] = ctl.returncode
        if ctl.returncode != 0:
            res['harness_error'] = 'control run failed: ' + ctl.stderr.decode('utf-8', 'replace')[-300:]
            errors.append(tool)
            results.append(res)
            print(json.dumps(res), flush=True)
            continue
        canary = os.path.join(root, f'canary-{i}')
        make_canary(canary)
        before = fingerprint(canary)
        env = clean_env()
        env.update({'GIT_DIR': os.path.join(canary, '.git'), 'GIT_WORK_TREE': canary,
                    'GIT_INDEX_FILE': os.path.join(canary, '.git', 'index')})
        try:
            can = run(cmd, cwd=tree, env=env, timeout=TIMEOUT)
            res['canary_rc'] = can.returncode
        except subprocess.TimeoutExpired:
            res['canary_rc'] = 'timeout'
        after = fingerprint(canary)
        res['canary_changed'] = before != after
        res['leak'] = res['canary_changed'] or res['canary_rc'] != ctl.returncode
        if res['leak']:
            leaking.append(tool)
        results.append(res)
        print(json.dumps(res), flush=True)
    with open(os.path.abspath(__file__), 'rb') as fh:
        sha = hashlib.sha256(fh.read()).hexdigest()
    print(json.dumps({'revision': rev, 'targets': len(results), 'leaking': len(leaking),
                      'leaking_tools': leaking, 'harness_errors': errors,
                      'probe_sha256': sha, 'scratch': root}))
    shutil.rmtree(root, ignore_errors=True)
    return 2 if errors else (1 if leaking else 0)


if __name__ == '__main__':
    sys.exit(main())
