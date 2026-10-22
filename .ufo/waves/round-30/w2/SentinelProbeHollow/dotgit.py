#!/usr/bin/env python3
"""Re-test of SentinelGitEnv3 finding 2 (a dropped `.git` pointer file is followed) at
lane tip 29bf87fa, in two shapes:

  A mechanism: build the child environment with the *tip tool's own* env builder
    (imported from tools/check-kernel-taint.py: git_env) and run `git status`,
    `git add -A` and `git init` in a directory whose `.git` is a `gitdir:` pointer
    file aimed at an attacker-owned repository; report whether the attacker repo is
    mutated and whether `git init` preserves the pointer.

  B lane shape: run each frozen target in the harness's enclosing-repo shape with a
    `.git` pointer file planted in the tool's working copy (the directory the tool
    treats as ROOT), then compare the attacker repo's fingerprint before/after; plus
    a sentinel file in the attacker repo to detect any write.

Report-only. Writes only under /fast/scratch/hyaku/tsukuroi-r30/SentinelProbeHollow/.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile

LANE = '/fast/scratch/hyaku/tsukuroi-r30/SentinelProbeHollow/repo'
REV = '29bf87fa3971df04cb96e4ad9a28805d8154ed2f'
ROOT = tempfile.mkdtemp(prefix='dotgit-', dir='/fast/scratch/hyaku/tsukuroi-r30/SentinelProbeHollow')


def git(*args, env=None, text=True):
    return subprocess.run(['/usr/bin/git', *args], capture_output=True, env=env, text=text)


def fp(repo):
    h = hashlib.sha256()
    for dp, _dn, fn in sorted(os.walk(repo)):
        for f in sorted(fn):
            p = os.path.join(dp, f)
            h.update(os.path.relpath(p, repo).encode() + b'\n')
            try:
                with open(p, 'rb') as fh:
                    h.update(hashlib.sha256(fh.read()).digest())
            except OSError:
                pass
    return h.hexdigest()


def load_tool_env():
    """The tip tool's own contract builder, imported as a module."""
    spec = importlib.util.spec_from_file_location(
        'kt', os.path.join(LANE, 'tools', 'check-kernel-taint.py'))
    mod = importlib.util.module_from_spec(spec)
    sys.modules['kt'] = mod
    sys.path.insert(0, os.path.join(LANE, 'tools'))
    spec.loader.exec_module(mod)
    return mod.git_env


def shape_a():
    out = {}
    attacker = os.path.join(ROOT, 'a-attacker')
    os.makedirs(attacker)
    git('init', '-q', '-b', 'main', attacker).check_returncode()
    git('-C', attacker, '-c', 'user.name=a', '-c', 'user.email=a@invalid', 'commit',
        '-q', '--allow-empty', '-m', 'seed').check_returncode()
    git_env = load_tool_env()
    work = os.path.join(ROOT, 'a-work')
    os.makedirs(work)
    with open(os.path.join(work, '.git'), 'w') as fh:
        fh.write('gitdir: %s/.git\n' % attacker)
    with open(os.path.join(work, 'payload'), 'w') as fh:
        fh.write('payload\n')
    tmp = tempfile.mkdtemp(prefix='a-env-', dir=ROOT)
    env = git_env(tmp)
    out['env'] = {k: env.get(k) for k in ('PATH', 'GIT_CONFIG_GLOBAL', 'HOME', 'GIT_CEILING_DIRECTORIES')}
    out['env_home_private'] = env.get('HOME', '').startswith(tmp)
    before = fp(attacker)
    st = git('-C', work, 'status', '--porcelain', env=env)
    out['status_rc'] = st.returncode
    out['status_out'] = st.stdout.strip()
    add = git('-C', work, 'add', '-A', env=env)
    out['add_rc'] = add.returncode
    cm = git('-C', work, '-c', 'user.name=a', '-c', 'user.email=a@invalid', 'commit', '-qm', 'pwn', env=env)
    out['commit_rc'] = cm.returncode
    out['commit_err'] = cm.stderr.strip()[:200]
    out['attacker_mutated_by_status_add_commit'] = fp(attacker) != before
    out['attacker_head'] = git('-C', attacker, 'log', '-1', '--format=%s').stdout.strip()
    out['attacker_status'] = git('-C', attacker, 'status', '--porcelain').stdout.strip()
    # git init over the existing pointer
    work2 = os.path.join(ROOT, 'a-work2')
    os.makedirs(work2)
    with open(os.path.join(work2, '.git'), 'w') as fh:
        fh.write('gitdir: %s/.git\n' % attacker)
    ini = git('init', '-q', work2, env=env)
    out['init_rc'] = ini.returncode
    out['init_left_pointer'] = os.path.isfile(os.path.join(work2, '.git'))
    return out


def shape_b():
    """Plant the pointer in the tool's working copy and see whether any target writes."""
    tar = git('-C', LANE, 'archive', REV, text=False).stdout
    results = []
    for tool in ('tools/check-kernel-taint.py', 'tools/check-freshness-r17.py',
                 'tools/check-storage-health.py', 'tools/check-registry-coverage.py',
                 'tools/check-self-assessment.py'):
        base = tempfile.mkdtemp(prefix='b-', dir=ROOT)
        attacker = os.path.join(base, 'attacker')
        os.makedirs(attacker)
        git('init', '-q', '-b', 'main', attacker).check_returncode()
        git('-C', attacker, '-c', 'user.name=a', '-c', 'user.email=a@invalid', 'commit',
            '-q', '--allow-empty', '-m', 'seed').check_returncode()
        tree = os.path.join(base, 'tree')
        os.makedirs(tree)
        import io
        with tarfile.open(fileobj=io.BytesIO(tar)) as t:
            t.extractall(tree, filter='data')
        with open(os.path.join(tree, '.git'), 'w') as fh:
            fh.write('gitdir: %s/.git\n' % attacker)
        home = os.path.join(base, 'home')
        os.makedirs(home)
        env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
        env.update({'HOME': home, 'XDG_CONFIG_HOME': os.path.join(home, '.config'),
                    'TMPDIR': base, 'GIT_CONFIG_NOSYSTEM': '1', 'LC_ALL': 'C'})
        before = fp(attacker)
        args = [sys.executable, os.path.join(tree, tool), '--selftest']
        try:
            r = subprocess.run(args, cwd=tree, env=env, capture_output=True, timeout=600)
            rc = r.returncode
        except subprocess.TimeoutExpired:
            rc = 'timeout'
        results.append({'tool': tool, 'rc': rc, 'attacker_mutated': fp(attacker) != before})
    return results


if __name__ == '__main__':
    print(json.dumps({'scratch': ROOT, 'a': shape_a(), 'b': shape_b()}, indent=1))
