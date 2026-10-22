#!/usr/bin/env python3
"""Test the race hypothesis for the probe's flaky 'canary fingerprint changed' reading.

`make_canary_repo` commits into the canary; git may auto-gc that repository in a
detached background process. If the repack lands between the probe's two fingerprint
calls, the objects/ layout changes and the probe reports a false canary mutation.
"""
import importlib.util
import os
import shutil
import time

PROBE = '/fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/repo/tools/probe-git-child-env-r31.py'
spec = importlib.util.spec_from_file_location('probe', PROBE)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

root = '/fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/gc-lab'
shutil.rmtree(root, ignore_errors=True)
os.makedirs(os.path.join(root, 'home-plumbing', '.config'))
os.makedirs(os.path.join(root, 'tmp-plumbing'))
penv = probe.plumbing_env(root)

for trial in range(6):
    canary = os.path.join(root, 'canary-%d' % trial)
    probe.make_canary_repo(canary, penv)
    gd = os.path.join(canary, '.git')

    def layout():
        return sorted(os.path.relpath(os.path.join(dp, f), gd)
                      for dp, _dn, fn in os.walk(os.path.join(gd, 'objects')) for f in fn)

    def packs():
        return sorted(f for f in os.listdir(os.path.join(gd, 'objects', 'pack'))
                      if f.endswith('.pack')) if os.path.isdir(os.path.join(gd, 'objects', 'pack')) else []

    fp0 = probe.fingerprint(canary, penv)
    lay0, pk0 = layout(), packs()
    changed = None
    for _ in range(60):
        time.sleep(0.25)
        if probe.fingerprint(canary, penv) != fp0:
            changed = layout()
            break
    print('trial %d: canary mutated within 15s: %s  packs_before=%s packs_after=%s' % (
        trial, bool(changed), pk0, packs()))
    if changed:
        print('   before:', lay0)
        print('   after :', changed)
