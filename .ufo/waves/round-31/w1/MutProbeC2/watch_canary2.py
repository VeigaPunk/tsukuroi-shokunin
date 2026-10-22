#!/usr/bin/env python3
"""Long watch on a probe-made canary: does the detached `git maintenance run --auto`
that `git commit` spawns (observed via GIT_TRACE) later rewrite the canary?

The probe fingerprints the canary, runs the target (~25 s), then fingerprints again.
Any write inside that window flips the dotgit-pointer verdict.
"""
import importlib.util
import os
import shutil
import time

PROBE = '/fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/repo/tools/probe-git-child-env-r31.py'
spec = importlib.util.spec_from_file_location('probe', PROBE)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

root = '/fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/watch2-lab'
shutil.rmtree(root, ignore_errors=True)
os.makedirs(os.path.join(root, 'home-plumbing', '.config'))
os.makedirs(os.path.join(root, 'tmp-plumbing'))
penv = probe.plumbing_env(root)

for t in range(3):
    canary = os.path.join(root, 'canary-%d' % t)
    probe.make_canary_repo(canary, penv)
    gd = os.path.join(canary, '.git')
    fp0 = probe.fingerprint(canary, penv)
    changed_at = None
    for i in range(180):
        time.sleep(0.5)
        if probe.fingerprint(canary, penv) != fp0:
            changed_at = i * 0.5
            break
    packs = sorted(os.listdir(os.path.join(gd, 'objects', 'pack'))) \
        if os.path.isdir(os.path.join(gd, 'objects', 'pack')) else []
    info = sorted(os.listdir(os.path.join(gd, 'objects', 'info'))) \
        if os.path.isdir(os.path.join(gd, 'objects', 'info')) else []
    print('trial %d: changed=%s at=%ss packs=%s objects/info=%s' % (
        t, changed_at is not None, changed_at, packs, info))
