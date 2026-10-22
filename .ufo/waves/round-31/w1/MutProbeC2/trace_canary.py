#!/usr/bin/env python3
"""Trace which git invocations mention the canary path during the dotgit-pointer channel."""
import importlib.util
import os
import re
import shutil
import subprocess
import sys

PROBE = '/fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/repo/tools/probe-git-child-env-r31.py'
spec = importlib.util.spec_from_file_location('probe', PROBE)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

LANE = '/fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/repo'
REV = open('/fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/h2.rev').read().strip()
root = '/fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/trace-lab'
shutil.rmtree(root, ignore_errors=True)
os.makedirs(os.path.join(root, 'home-plumbing', '.config'))
os.makedirs(os.path.join(root, 'tmp-plumbing'))
penv = probe.plumbing_env(root)
tree = os.path.join(root, 'tree')
probe.export_tree(LANE, REV, tree, penv)

work = os.path.join(root, 'w')
home = os.path.join(work, 'home')
tmp = os.path.join(work, 'tmp')
os.makedirs(os.path.join(home, '.config'))
os.makedirs(tmp)
wtree = os.path.join(work, 'tree')
shutil.copytree(tree, wtree, symlinks=True)
canary = os.path.join(root, 'canary')
probe.make_canary_repo(canary, penv)
gd = os.path.join(canary, '.git')
for d in (wtree, tmp):
    with open(os.path.join(d, '.git'), 'w') as fh:
        fh.write('gitdir: %s\n' % gd)
trace = os.path.join(work, 'trace')
env = probe.hermetic_env(home, tmp)
cmd = [probe.STRACE, '-f', '-qq', '-v', '-s', '65536', '-e', 'trace=execve', '-o', trace,
       '--', sys.executable, os.path.join(wtree, 'tools/check-kernel-taint.py'), '--selftest']
subprocess.run(cmd, cwd=wtree, env=env, capture_output=True, timeout=1200)

print('trace file:', trace)
hits = 0
with open(trace, encoding='utf-8', errors='replace') as fh:
    for i, line in enumerate(fh, 1):
        if 'canary' in line:
            hits += 1
            if hits <= 25:
                print('  line %d: %s' % (i, line.strip()[:400]))
print('total lines mentioning canary:', hits)

# also: which git invocations run with cwd inside tmp/ (the tree that carries the .git FILE)?
recs = probe.parse_trace(trace)
print('execve records:', len(recs))
