#!/usr/bin/env python3
"""Decide whether a git command run under a directory holding a `.git` FILE pointer can
rewrite the pointed-to repository (the canary).

The probe's dotgit-pointer channel drops `.git` FILE files into the tree copy AND into TMPDIR,
both pointing at the canary. A git command run with its cwd under TMPDIR that does not use
`-C` will discover the canary through the `.git` FILE (gitfile) and may rewrite the canary's
index (a `git status`-style index refresh changes the index bytes, which the probe hashes).
"""
import hashlib
import os
import shutil
import subprocess

ROOT = '/tmp/gitfile-lab'
shutil.rmtree(ROOT, ignore_errors=True)
os.makedirs(ROOT)
canary = os.path.join(ROOT, 'canary')
subprocess.run(['git', 'init', '-q', '-b', 'canary', canary], check=True)
with open(os.path.join(canary, 'CANARY'), 'w') as fh:
    fh.write('canary\n')
subprocess.run(['git', '-C', canary, 'add', 'CANARY'], check=True)
subprocess.run(['git', '-C', canary, '-c', 'user.name=p', '-c', 'user.email=p@i',
                '-c', 'commit.gpgsign=false', 'commit', '-qm', 'canary'], check=True)


def digest():
    h = hashlib.sha256()
    for dp, _dn, fn in sorted(os.walk(os.path.join(canary, '.git'))):
        for f in sorted(fn):
            p = os.path.join(dp, f)
            h.update(os.path.relpath(p, canary).encode() + b'\n')
            with open(p, 'rb') as fh:
                h.update(hashlib.sha256(fh.read()).digest())
    return h.hexdigest()


tmp = os.path.join(ROOT, 'tmp')
os.makedirs(tmp)
with open(os.path.join(tmp, '.git'), 'w') as fh:
    fh.write('gitdir: %s/.git\n' % canary)

before = digest()
print('before      ', before)
for cmd in (['git', 'rev-parse', 'HEAD'],
            ['git', 'for-each-ref', '--format=%(refname) %(objectname)'],
            ['git', 'status', '--porcelain'],
            ['git', 'init', '--quiet', '--initial-branch=master', os.path.join(tmp, 'sub')]):
    r = subprocess.run(cmd, cwd=tmp, capture_output=True, text=True)
    print('  %-60s rc=%d %s' % (' '.join(cmd)[:60], r.returncode, r.stderr.strip()[:80]))
after = digest()
print('after       ', after, 'SAME' if before == after else 'CHANGED')
print('index digest before/after:',
      hashlib.sha256(open(os.path.join(canary, '.git', 'index'), 'rb').read()).hexdigest()[:16],
      hashlib.sha256(open(os.path.join(canary, '.git', 'index'), 'rb').read()).hexdigest()[:16])
