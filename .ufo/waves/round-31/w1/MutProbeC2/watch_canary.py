#!/usr/bin/env python3
"""Watch a probe-made canary for background writes (commit-graph / gc) after its commit.

Hypothesis for the probe's occasional false 'canary fingerprint changed': `git commit` in
make_canary_repo schedules a detached `git maintenance run --auto`, which writes
objects/info/commit-graph into the canary. The probe's fingerprint walks the objects/ tree,
so a commit-graph landing between its two fingerprint calls changes the digest.
"""
import importlib.util
import os
import shutil
import subprocess
import time

PROBE = '/fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/repo/tools/probe-git-child-env-r31.py'
spec = importlib.util.spec_from_file_location('probe', PROBE)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

root = '/fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/watch-lab'
shutil.rmtree(root, ignore_errors=True)
os.makedirs(os.path.join(root, 'home-plumbing', '.config'))
os.makedirs(os.path.join(root, 'tmp-plumbing'))
penv = probe.plumbing_env(root)

print('git config gc.writeCommitGraph (repo):',
      subprocess.run(['git', 'config', '--get', 'gc.writeCommitGraph'], env=penv,
                     capture_output=True, text=True).stdout.strip() or '<unset>')
for t in range(4):
    canary = os.path.join(root, 'canary-%d' % t)
    probe.make_canary_repo(canary, penv)
    gd = os.path.join(canary, '.git')
    fp0 = probe.fingerprint(canary, penv)
    seen = None
    for i in range(120):
        time.sleep(0.25)
        info = os.path.join(gd, 'objects', 'info')
        names = sorted(os.listdir(info)) if os.path.isdir(info) else []
        packs = sorted(os.listdir(os.path.join(gd, 'objects', 'pack'))) \
            if os.path.isdir(os.path.join(gd, 'objects', 'pack')) else []
        fp = probe.fingerprint(canary, penv)
        if fp != fp0:
            seen = (i * 0.25, names, packs)
            break
    print('trial %d: changed=%s %s' % (t, bool(seen), seen or ''))
    if seen:
        print('  objects/info names:', seen[1], ' packs:', seen[2])
