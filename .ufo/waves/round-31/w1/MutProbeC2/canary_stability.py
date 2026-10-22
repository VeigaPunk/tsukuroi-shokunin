#!/usr/bin/env python3
"""Test whether the probe's canary fingerprint is stable across a channel run.

Uses the probe's own make_canary_repo/fingerprint to build a canary, then re-fingerprints
it after an idle delay and after a git command, to see whether background `git gc --auto`
or an index refresh changes the fingerprint without the tool touching the canary.
"""
import importlib.util
import os
import subprocess
import sys
import time

PROBE = '/fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/repo/tools/probe-git-child-env-r31.py'
spec = importlib.util.spec_from_file_location('probe', PROBE)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

root = '/fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/canary-lab'
os.makedirs(os.path.join(root, 'home-plumbing', '.config'), exist_ok=True)
os.makedirs(os.path.join(root, 'tmp-plumbing'), exist_ok=True)
penv = probe.plumbing_env(root)
canary = os.path.join(root, 'canary')
if not os.path.exists(canary):
    probe.make_canary_repo(canary, penv)
gd = os.path.join(canary, '.git')

fp0 = probe.fingerprint(canary, penv)
print('fingerprint t0      ', fp0)
names0 = sorted(os.path.relpath(os.path.join(dp, f), gd)
                 for dp, _dn, fn in os.walk(os.path.join(gd, 'objects')) for f in fn)
time.sleep(20)
fp1 = probe.fingerprint(canary, penv)
names1 = sorted(os.path.relpath(os.path.join(dp, f), gd)
                 for dp, _dn, fn in os.walk(os.path.join(gd, 'objects')) for f in fn)
print('fingerprint t+20s   ', fp1, 'same' if fp0 == fp1 else 'CHANGED')
print('objects names same' if names0 == names1 else 'objects names CHANGED')
if names0 != names1:
    print('  before:', names0[:8])
    print('  after :', names1[:8])
subprocess.run(['git', '--git-dir', gd, 'gc', '--auto', '--quiet'], env=penv, capture_output=True)
fp2 = probe.fingerprint(canary, penv)
names2 = sorted(os.path.relpath(os.path.join(dp, f), gd)
                 for dp, _dn, fn in os.walk(os.path.join(gd, 'objects')) for f in fn)
print('fingerprint after gc', fp2, 'same' if fp1 == fp2 else 'CHANGED')
print('objects names same' if names1 == names2 else 'objects names CHANGED after gc')
