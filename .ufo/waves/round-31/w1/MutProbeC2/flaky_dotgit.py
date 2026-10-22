#!/usr/bin/env python3
"""Instrument the probe's dotgit-pointer channel to see WHAT changes in the canary.

Reproduces one_run's dotgit-pointer shape with the probe's own helpers, then diffs the
canary .git directory (names + digests) between the two fingerprint calls, so a
"canary fingerprint changed" reading can be attributed to a specific file.
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tarfile

PROBE = '/fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/repo/tools/probe-git-child-env-r31.py'
spec = importlib.util.spec_from_file_location('probe', PROBE)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

LANE = '/fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/repo'
REV = sys.argv[1] if len(sys.argv) > 1 else open('/fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/h2.rev').read().strip()
TRIALS = int(sys.argv[2]) if len(sys.argv) > 2 else 6

root = '/fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/flaky-lab'
shutil.rmtree(root, ignore_errors=True)
os.makedirs(os.path.join(root, 'home-plumbing', '.config'))
os.makedirs(os.path.join(root, 'tmp-plumbing'))
penv = probe.plumbing_env(root)
tree = os.path.join(root, 'tree')
probe.export_tree(LANE, REV, tree, penv)


def snapshot(gd):
    out = {}
    for dp, _dn, fn in os.walk(gd):
        for f in fn:
            p = os.path.join(dp, f)
            out[os.path.relpath(p, gd)] = os.path.getsize(p)
    return out


for t in range(TRIALS):
    work = os.path.join(root, 'w%d' % t)
    home = os.path.join(work, 'home')
    tmp = os.path.join(work, 'tmp')
    os.makedirs(os.path.join(home, '.config'))
    os.makedirs(tmp)
    wtree = os.path.join(work, 'tree')
    shutil.copytree(tree, wtree, symlinks=True)
    canary = os.path.join(root, 'canary-%d' % t)
    probe.make_canary_repo(canary, penv)
    gd = os.path.join(canary, '.git')
    for d in (wtree, tmp):
        with open(os.path.join(d, '.git'), 'w') as fh:
            fh.write('gitdir: %s\n' % gd)
    before_files = snapshot(gd)
    fp0 = probe.fingerprint(canary, penv)
    env = probe.hermetic_env(home, tmp)
    cmd = [probe.STRACE, '-f', '-qq', '-v', '-s', '65536', '-e', 'trace=execve',
           '-o', os.path.join(work, 'trace'), '--', sys.executable,
           os.path.join(wtree, 'tools/check-kernel-taint.py'), '--selftest']
    subprocess.run(cmd, cwd=wtree, env=env, capture_output=True, timeout=1200)
    fp1 = probe.fingerprint(canary, penv)
    after_files = snapshot(gd)
    changed = sorted(set(before_files) ^ set(after_files)) + \
        sorted(k for k in set(before_files) & set(after_files) if before_files[k] != after_files[k])
    print('trial %d: fingerprint %s  files_changed=%s' % (
        t, 'CHANGED' if fp0 != fp1 else 'same', changed if changed else '[]'))
