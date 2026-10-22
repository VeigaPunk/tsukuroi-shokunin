#!/usr/bin/env python3
"""Residual git-environment channel probe for the lane tools that run git writes (round 30,
claim C2, axis operability).

Origin: round-29 wave-2 seat SentinelResidualEnv and the round-29 spot-check routed defect 4
(`corpus/lessons/round-29-verifier-spotcheck.md:152`): after round 29 scrubbed inherited
`GIT_DIR`, `GIT_WORK_TREE` and `GIT_INDEX_FILE`, three channels still reach a tool's git
children: a `git` wrapper earlier on `PATH`, per-user git files under `HOME` /
`XDG_CONFIG_HOME` (`git/config`, `.gitconfig`, `git/ignore`, `git/attributes`), and
discovery of an enclosing repository above the tool's working or temporary directory.
`tools/probe-git-env-leak.py` (frozen in round 29) does not test them, and its own runs
inherit the caller's `HOME`.

FROZEN target set (11): the round-29 frozen eight of `tools/probe-git-env-leak.py`, plus the
three tools whose sandbox git writes were added or found during round 29:
`tools/check-self-assessment.py --selftest`, `tools/mutants-owed-statements-r29.py` and
`tools/mutants-owed-statements-r29-landed.py`.

FROZEN channel set (3), each run once per target, entirely under a private scratch directory:
  path-wrapper   PATH starts with a directory holding an executable `git` that appends its
                 argv to a canary log and then execs the system git. LEAK when the log is
                 non-empty or the exit code differs from the control run.
  user-files     HOME and XDG_CONFIG_HOME point at a canary home holding `.gitconfig` and
                 `.config/git/config` (`core.hooksPath` = canary hooks whose pre-commit,
                 post-commit and post-checkout hooks append to a canary log), `.config/git/ignore`
                 (`*`) and `.config/git/attributes`. LEAK when the log is non-empty or the
                 exit code differs from the control run.
  enclosing-repo the tool tree, its working directory and TMPDIR sit inside the work tree of a
                 canary repository with one commit. LEAK when the canary fingerprint (HEAD,
                 refs, object and ref file names, index/HEAD/packed-refs digests) changed or
                 the exit code differs from the control run.
CONTROL run: every GIT_* removed, PATH unchanged, HOME and XDG_CONFIG_HOME set to an empty
private directory (the probe never inherits the caller's HOME), TMPDIR under the scratch root
outside any repository. A target whose control run fails or times out is a harness error.

Usage: python3 tools/probe-git-env-residual-r30.py --revision <REV> [--lane <repo>]
       [--scratch <dir>] [--only <tool> ...] [--channels <ch> ...]
Output: one JSON line per (target, channel), then a summary JSON line with `targets`,
`channels`, `pairs`, `leaking` (leaking pairs), `leaking_pairs`, `harness_errors`,
`probe_sha256`, `revision`.  Exit 0 when leaking is 0 and there is no harness error, 1 when
a pair leaks, 2 on a harness error.
"""
import argparse
import hashlib
import io
import json
import os
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile

TARGETS = (
    ('tools/mutprobe-fixtures/path-user-leaky.py', []),
    ('tools/mutprobe-fixtures/enclosing-repo-leaky.py', []),
    ('tools/mutprobe-fixtures/enclosing-repo-leaky.py', ['--fingerprint-only']),
    ('tools/mutprobe-fixtures/contract-compliant.py', []),
)
CHANNELS = ('path-wrapper', 'user-files', 'enclosing-repo')
TIMEOUT = 900
SYSTEM_GIT = shutil.which('git', path='/usr/bin:/bin') or '/usr/bin/git'


def probe_env(home, tmpdir):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update({'GIT_CONFIG_NOSYSTEM': '1', 'LC_ALL': 'C', 'HOME': home,
                'XDG_CONFIG_HOME': os.path.join(home, '.config'), 'TMPDIR': tmpdir})
    return env


def run(cmd, cwd=None, env=None, timeout=120):
    return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, timeout=timeout)


def git(env, *args, timeout=120):
    return run([SYSTEM_GIT, *args], env=env, timeout=timeout)


def fingerprint(canary, env):
    gd = os.path.join(canary, '.git')
    h = hashlib.sha256()
    h.update(git(env, '-C', canary, 'rev-parse', 'HEAD').stdout)
    h.update(git(env, '-C', canary, 'for-each-ref', '--format=%(refname) %(objectname)').stdout)
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


def write_exec(path, body):
    with open(path, 'w') as fh:
        fh.write(body)
    os.chmod(path, os.stat(path).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def make_canary_repo(path, env):
    os.makedirs(path, exist_ok=True)
    git(env, 'init', '-q', '-b', 'canary', path).check_returncode()
    with open(os.path.join(path, 'CANARY'), 'w') as fh:
        fh.write('canary\n')
    git(env, '-C', path, 'add', 'CANARY').check_returncode()
    git(env, '-C', path, '-c', 'user.name=probe', '-c', 'user.email=probe@invalid',
        '-c', 'commit.gpgsign=false', 'commit', '-qm', 'canary').check_returncode()


def read_log(path):
    if not os.path.exists(path):
        return ''
    with open(path, encoding='utf-8', errors='replace') as fh:
        return fh.read()


def export_tree(lane, rev, dest):
    env = probe_env(os.path.dirname(dest), os.path.dirname(dest))
    os.makedirs(dest)
    tar = git(env, '-C', lane, 'archive', rev).stdout
    with tarfile.open(fileobj=io.BytesIO(tar)) as t:
        t.extractall(dest, filter='data')


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--revision', required=True)
    ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument('--scratch', default=None)
    ap.add_argument('--only', nargs='*', default=None)
    ap.add_argument('--channels', nargs='*', default=None, choices=CHANNELS)
    a = ap.parse_args()
    lane = os.path.realpath(a.lane)
    parent = a.scratch or ('/fast/scratch/hyaku' if os.path.isdir('/fast/scratch/hyaku') else None)
    if parent:
        os.makedirs(parent, exist_ok=True)
    root = os.path.realpath(tempfile.mkdtemp(prefix='git-env-residual-', dir=parent))
    if os.path.commonpath([root, lane]) == lane:
        print(json.dumps({'error': 'scratch is inside the lane', 'scratch': root}))
        return 2
    clean_home = os.path.join(root, 'home-clean')
    clean_tmp = os.path.join(root, 'tmp-clean')
    os.makedirs(os.path.join(clean_home, '.config'))
    os.makedirs(clean_tmp)
    base_env = probe_env(clean_home, clean_tmp)
    disc = git(base_env, '-C', root, 'rev-parse', '--git-dir', timeout=30)
    if disc.returncode == 0:
        print(json.dumps({'error': 'scratch root is inside a git repository', 'scratch': root}))
        return 2
    p = git(base_env, '-C', lane, 'rev-parse', '--verify', a.revision + '^{commit}')
    if p.returncode != 0:
        print(json.dumps({'error': 'revision unreadable', 'revision': a.revision}))
        return 2
    rev = p.stdout.decode().strip()
    tree = os.path.join(root, 'tree')
    export_tree(lane, rev, tree)
    clone = os.path.join(root, 'lane.git')
    git(base_env, 'clone', '-q', '--bare', '--no-local', lane, clone, timeout=600).check_returncode()
    channels = a.channels or list(CHANNELS)
    results, leaking, errors = [], [], []
    ntargets = 0
    for i, (tool, argv) in enumerate(TARGETS):
        if a.only and tool not in a.only and os.path.basename(tool) not in a.only:
            continue
        ntargets += 1
        args = [x.format(rev=rev, clone=clone) for x in argv]
        cmd = [sys.executable, os.path.join(tree, tool), *args]
        try:
            ctl = run(cmd, cwd=tree, env=base_env, timeout=TIMEOUT)
            ctl_rc = ctl.returncode
            ctl_err = ctl.stderr.decode('utf-8', 'replace')[-300:]
        except subprocess.TimeoutExpired:
            ctl_rc, ctl_err = 'timeout', 'control run timed out'
        if ctl_rc != 0:
            res = {'tool': tool, 'argv': args, 'control_rc': ctl_rc,
                   'harness_error': 'control run failed: ' + ctl_err}
            errors.append(tool)
            results.append(res)
            print(json.dumps(res), flush=True)
            continue
        for ch in channels:
            work = os.path.join(root, f'{ch}-{i}')
            os.makedirs(work)
            log = os.path.join(work, 'canary.log')
            env = dict(base_env)
            cwd = tree
            canary = None
            if ch == 'path-wrapper':
                wdir = os.path.join(work, 'bin')
                os.makedirs(wdir)
                write_exec(os.path.join(wdir, 'git'),
                           '#!/bin/sh\nprintf "%%s\\n" "$*" >> "%s"\nexec "%s" "$@"\n' % (log, SYSTEM_GIT))
                env['PATH'] = wdir + os.pathsep + env.get('PATH', os.defpath)
            elif ch == 'user-files':
                home = os.path.join(work, 'home')
                hooks = os.path.join(work, 'hooks')
                os.makedirs(os.path.join(home, '.config', 'git'))
                os.makedirs(hooks)
                for hook in ('pre-commit', 'post-commit', 'post-checkout'):
                    write_exec(os.path.join(hooks, hook),
                               '#!/bin/sh\necho "%s $PWD" >> "%s"\nexit 0\n' % (hook, log))
                cfg = '[core]\n\thooksPath = %s\n' % hooks
                for f in (os.path.join(home, '.gitconfig'), os.path.join(home, '.config', 'git', 'config')):
                    with open(f, 'w') as fh:
                        fh.write(cfg)
                with open(os.path.join(home, '.config', 'git', 'ignore'), 'w') as fh:
                    fh.write('*\n')
                with open(os.path.join(home, '.config', 'git', 'attributes'), 'w') as fh:
                    fh.write('* -text -diff\n')
                env.update({'HOME': home, 'XDG_CONFIG_HOME': os.path.join(home, '.config')})
            else:
                canary = os.path.join(work, 'encl')
                make_canary_repo(canary, base_env)
                inner_tmp = os.path.join(canary, 'tmp')
                os.makedirs(inner_tmp)
                cwd = os.path.join(canary, 'tree')
                shutil.copytree(tree, cwd, symlinks=True)
                env['TMPDIR'] = inner_tmp
                before = fingerprint(canary, base_env)
            ch_cmd = [sys.executable, os.path.join(cwd, tool), *args]
            res = {'tool': tool, 'channel': ch, 'argv': args, 'control_rc': ctl_rc}
            try:
                r = run(ch_cmd, cwd=cwd, env=env, timeout=TIMEOUT)
                res['channel_rc'] = r.returncode
            except subprocess.TimeoutExpired:
                res['channel_rc'] = 'timeout'
            evidence = []
            if ch == 'enclosing-repo':
                if fingerprint(canary, base_env) != before:
                    evidence.append('canary fingerprint changed')
            else:
                text = read_log(log)
                if text:
                    evidence.append('canary log lines: %d' % len(text.splitlines()))
                    res['log_head'] = text.splitlines()[:3]
            if res['channel_rc'] != ctl_rc:
                evidence.append('exit code %s differs from control %s' % (res['channel_rc'], ctl_rc))
            res['evidence'] = evidence
            res['leak'] = bool(evidence)
            if res['leak']:
                leaking.append(f'{tool}:{ch}')
            results.append(res)
            print(json.dumps(res), flush=True)
    with open(os.path.abspath(__file__), 'rb') as fh:
        sha = hashlib.sha256(fh.read()).hexdigest()
    pairs = sum(1 for r in results if 'channel' in r)
    print(json.dumps({'revision': rev, 'targets': ntargets, 'channels': channels, 'pairs': pairs,
                      'leaking': len(leaking), 'leaking_pairs': leaking, 'harness_errors': errors,
                      'probe_sha256': sha, 'scratch': root}))
    shutil.rmtree(root, ignore_errors=True)
    return 2 if errors else (1 if leaking else 0)


if __name__ == '__main__':
    sys.exit(main())
