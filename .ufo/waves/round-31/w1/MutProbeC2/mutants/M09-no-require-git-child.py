#!/usr/bin/env python3
"""Child-process environment probe for the lane tools that run git (round 31, claim C2,
axis operability).

Origin: the round-30 spot-check routed defect 5 (`corpus/lessons/round-30-verifier-spotcheck.md`
section 5): the round-30 residual probe compares only exit codes and canary logs, so a hollow
fix scores 0; loader and interpreter injection variables (`LD_PRELOAD`, `LD_LIBRARY_PATH`,
`PYTHONPATH`) pass through the round-30 child environment contract (wave-1 SentinelGitEnv3
finding 1, wave-2 SentinelProbeHollow finding 7); the two owed-statement batteries start git
children that lack the contract and so read the system config scope (SentinelProbeHollow
finding 6); a dropped `.git` pointer file is followed (SentinelGitEnv3 finding 2).

The probe observes every process a target starts with `strace -f -e trace=execve -v`, so it
reads each child's real argv and environment instead of inferring them from side effects.

FROZEN target set (11): the eleven tools of `tools/probe-git-env-residual-r30.py`, same argv.

FROZEN channel set (3), each a separate run of every target under a fresh copy of the
exported tree, a fresh private HOME/XDG_CONFIG_HOME and a fresh TMPDIR:
  loader-env      the ambient environment adds LD_PRELOAD=<inject>/libprobe-inject.so (a
                  symlink to /usr/lib/libm.so.6, harmless when loaded), LD_LIBRARY_PATH=<inject>
                  and PYTHONPATH=<inject>. LEAK when any traced execve after the target's own
                  first exec carries an environment string containing the <inject> path, or
                  when the run breaks parity with the control.
  child-contract  the control run itself. LEAK when any successful execve of git
                  (`/usr/bin/git` or a program under `/usr/lib/git-core/`) lacks one of
                  GIT_CONFIG_NOSYSTEM=1, GIT_CONFIG_GLOBAL=/dev/null, GIT_CONFIG_SYSTEM=/dev/null
                  or a non-empty GIT_CEILING_DIRECTORIES (the ambient environment carries no
                  GIT_* name, so each must come from the tool; a missing NOSYSTEM/SYSTEM pair
                  means the child reads the system config scope).
  dotgit-pointer  the tree copy's root (the working directory) and the TMPDIR each hold a `.git`
                  FILE reading `gitdir: <canary>/.git` for a canary repository with one commit.
                  LEAK when the canary fingerprint (HEAD, refs, object/ref/log/hook/info file
                  names, HEAD/index/packed-refs/config digests) changes, or when the run breaks
                  parity with the control.
PARITY (closes the round-30 stdout-only gap): a run breaks parity when its exit code, its
normalised stdout digest or its count of successful git execs differs from control run A.
Normalisation replaces the run's scratch directory, the scratch root and every 40- or 64-hex
string. CONTROL: every GIT_*, LD_* and PYTHON* name removed from the ambient environment,
PATH=/usr/bin:/bin, LC_ALL=C, private empty HOME and XDG_CONFIG_HOME, TMPDIR under the scratch
root outside any repository. Control runs A and B must agree on parity and A must start at least
one git child; otherwise the target is a harness error.

Usage: python3 tools/probe-git-child-env-r31.py --revision <REV> [--lane <repo>]
       [--scratch <dir>] [--only <tool> ...] [--channels <ch> ...]
Output: one JSON line per (target, channel), then a summary JSON line with `targets`,
`channels`, `pairs`, `leaking`, `leaking_pairs`, `harness_errors`, `probe_sha256`, `revision`.
Exit 0 when leaking is 0 and there is no harness error, 1 when a pair leaks, 2 on a harness
error.
"""
import argparse
import hashlib
import io
import json
import os
import re
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
    ('tools/check-self-assessment.py', ['--selftest']),
    ('tools/mutants-owed-statements-r29.py',
     ['--base', '81a061a67466c5e1be812814a895a4b5ed89b4ff', '--counter-rev', '{rev}', '--lane', '{clone}']),
    ('tools/mutants-owed-statements-r29-landed.py', ['--base', '{rev}', '--counter-rev', '{rev}', '--lane', '{clone}']),
)
CHANNELS = ('loader-env', 'child-contract', 'dotgit-pointer')
TIMEOUT = 1200
SYSTEM_GIT = '/usr/bin/git'
STRACE = shutil.which('strace', path='/usr/bin:/bin') or '/usr/bin/strace'
LIBM = '/usr/lib/libm.so.6'
HEX = re.compile(rb'\b[0-9a-f]{64}\b|\b[0-9a-f]{40}\b')
CONTRACT = (('GIT_CONFIG_NOSYSTEM', '1'), ('GIT_CONFIG_GLOBAL', '/dev/null'),
            ('GIT_CONFIG_SYSTEM', '/dev/null'))


def hermetic_env(home, tmpdir):
    env = {k: v for k, v in os.environ.items()
           if not (k.startswith('GIT_') or k.startswith('LD_') or k.startswith('PYTHON'))}
    env.update({'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'HOME': home,
                'XDG_CONFIG_HOME': os.path.join(home, '.config'), 'TMPDIR': tmpdir})
    return env


def plumbing_env(root):
    env = hermetic_env(os.path.join(root, 'home-plumbing'), os.path.join(root, 'tmp-plumbing'))
    env.update({'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull,
                'GIT_CONFIG_SYSTEM': os.devnull})
    return env


def git(env, *args, timeout=120):
    return subprocess.run([SYSTEM_GIT, *args], env=env, capture_output=True, timeout=timeout)


def parse_strings(s, i):
    """Parse a strace list `[...]` of quoted C strings starting at s[i] == '['."""
    out = []
    assert s[i] == '['
    i += 1
    while i < len(s):
        c = s[i]
        if c == ']':
            return out, i + 1
        if c == '"':
            j, buf = i + 1, []
            while j < len(s) and s[j] != '"':
                if s[j] == '\\' and j + 1 < len(s):
                    buf.append(s[j:j + 2])
                    j += 2
                else:
                    buf.append(s[j])
                    j += 1
            out.append(''.join(buf))
            i = j + 1
            if i < len(s) and s[i] == '.' and s[i:i + 3] == '...':
                i += 3
        else:
            i += 1
    return out, i


def parse_trace(path):
    """Return successful execve records (pid, filename, argv, envp) in trace order."""
    done, pending = [], {}
    pat = re.compile(r'^(\d+)\s+execve\("((?:[^"\\]|\\.)*)", ')
    with open(path, encoding='utf-8', errors='replace') as fh:
        for line in fh:
            m = pat.match(line)
            if m:
                pid, fname = m.group(1), m.group(2)
                i = m.end()
                try:
                    argv, i = parse_strings(line, i)
                    while i < len(line) and line[i] in ', ':
                        i += 1
                    envp, i = parse_strings(line, i)
                except (AssertionError, IndexError):
                    argv, envp = [], []
                rec = (pid, fname, argv, envp)
                rest = line[i:]
                if '<unfinished ...>' in rest:
                    pending[pid] = rec
                elif re.search(r'\)\s*=\s*0\s*$', rest.rstrip()):
                    done.append(rec)
                continue
            m2 = re.match(r'^(\d+)\s+<\.\.\. execve resumed>.*=\s*0\s*$', line.rstrip())
            if m2 and m2.group(1) in pending:
                done.append(pending.pop(m2.group(1)))
            elif re.match(r'^(\d+)\s+<\.\.\. execve resumed>', line):
                pending.pop(line.split()[0], None)
    return done


def is_git(fname):
    return fname == SYSTEM_GIT or fname.startswith('/usr/lib/git-core/')


def fingerprint(canary, env):
    gd = os.path.join(canary, '.git')
    h = hashlib.sha256()
    h.update(git(env, '--git-dir', gd, 'rev-parse', 'HEAD').stdout)
    h.update(git(env, '--git-dir', gd, 'for-each-ref', '--format=%(refname) %(objectname)').stdout)
    for sub in ('objects', 'refs', 'logs', 'hooks', 'info'):
        for dp, _dn, fn in sorted(os.walk(os.path.join(gd, sub))):
            for f in sorted(fn):
                h.update(os.path.relpath(os.path.join(dp, f), gd).encode() + b'\n')
    for f in ('HEAD', 'index', 'packed-refs', 'config'):
        p = os.path.join(gd, f)
        if os.path.exists(p):
            with open(p, 'rb') as fh:
                h.update(f.encode() + hashlib.sha256(fh.read()).digest())
    return h.hexdigest()


def make_canary_repo(path, env):
    os.makedirs(path)
    git(env, 'init', '-q', '-b', 'canary', path).check_returncode()
    with open(os.path.join(path, 'CANARY'), 'w') as fh:
        fh.write('canary\n')
    git(env, '-C', path, 'add', 'CANARY').check_returncode()
    git(env, '-C', path, '-c', 'user.name=probe', '-c', 'user.email=probe@invalid',
        '-c', 'commit.gpgsign=false', 'commit', '-qm', 'canary').check_returncode()


def export_tree(lane, rev, dest, env):
    os.makedirs(dest)
    tar = git(env, '-C', lane, 'archive', rev).stdout
    with tarfile.open(fileobj=io.BytesIO(tar)) as t:
        t.extractall(dest, filter='data')


def one_run(root, name, tree, tool, args, extra_env=None, dotgit=None):
    """Run one target under strace in a fresh tree copy; return the observation dict."""
    work = os.path.join(root, name)
    home = os.path.join(work, 'home')
    tmp = os.path.join(work, 'tmp')
    os.makedirs(os.path.join(home, '.config'))
    os.makedirs(tmp)
    wtree = os.path.join(work, 'tree')
    shutil.copytree(tree, wtree, symlinks=True)
    if dotgit:
        for d in (wtree, tmp):
            with open(os.path.join(d, '.git'), 'w') as fh:
                fh.write('gitdir: %s\n' % dotgit)
    env = hermetic_env(home, tmp)
    if extra_env:
        env.update(extra_env)
    trace = os.path.join(root, name + '.trace')
    cmd = [STRACE, '-f', '-qq', '-v', '-s', '65536', '-e', 'trace=execve', '-o', trace,
           '--', sys.executable, os.path.join(wtree, tool), *args]
    obs = {}
    try:
        p = subprocess.run(cmd, cwd=wtree, env=env, capture_output=True, timeout=TIMEOUT)
        obs['rc'] = p.returncode
        out = p.stdout.replace(work.encode(), b'<WORK>').replace(root.encode(), b'<ROOT>')
        out = HEX.sub(b'<HEX>', out)
        obs['stdout_sha256'] = hashlib.sha256(out).hexdigest()
        obs['stderr_tail'] = p.stderr.decode('utf-8', 'replace')[-300:]
    except subprocess.TimeoutExpired:
        obs['rc'] = 'timeout'
        obs['stdout_sha256'] = None
    execs = parse_trace(trace) if os.path.exists(trace) else []
    obs['execs'] = execs
    obs['git_execs'] = sum(1 for e in execs if is_git(e[1]))
    shutil.rmtree(wtree, ignore_errors=True)
    return obs


def parity(a, b):
    diffs = []
    for k in ('rc', 'stdout_sha256', 'git_execs'):
        if a.get(k) != b.get(k):
            diffs.append('%s %s differs from control %s' % (k, b.get(k), a.get(k)))
    return diffs


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
    root = os.path.realpath(tempfile.mkdtemp(prefix='git-child-env-', dir=parent))
    with open(os.path.abspath(__file__), 'rb') as fh:
        sha = hashlib.sha256(fh.read()).hexdigest()
    if os.path.commonpath([root, lane]) == lane:
        print(json.dumps({'error': 'scratch is inside the lane', 'scratch': root}))
        return 2
    os.makedirs(os.path.join(root, 'home-plumbing', '.config'))
    os.makedirs(os.path.join(root, 'tmp-plumbing'))
    penv = plumbing_env(root)
    if git(penv, '-C', root, 'rev-parse', '--git-dir', timeout=30).returncode == 0:
        print(json.dumps({'error': 'scratch root is inside a git repository', 'scratch': root}))
        return 2
    if not os.path.exists(LIBM) or not os.path.exists(STRACE):
        print(json.dumps({'error': 'probe prerequisites missing', 'libm': LIBM, 'strace': STRACE}))
        return 2
    p = git(penv, '-C', lane, 'rev-parse', '--verify', a.revision + '^{commit}')
    if p.returncode != 0:
        print(json.dumps({'error': 'revision unreadable', 'revision': a.revision}))
        return 2
    rev = p.stdout.decode().strip()
    tree = os.path.join(root, 'tree')
    export_tree(lane, rev, tree, penv)
    clone = os.path.join(root, 'lane.git')
    git(penv, 'clone', '-q', '--bare', '--no-local', lane, clone, timeout=600).check_returncode()
    inject = os.path.join(root, 'inject')
    os.makedirs(inject)
    os.symlink(LIBM, os.path.join(inject, 'libprobe-inject.so'))
    channels = a.channels or list(CHANNELS)
    results, leaking, errors = [], [], []
    ntargets = 0
    for i, (tool, argv) in enumerate(TARGETS):
        if a.only and tool not in a.only and os.path.basename(tool) not in a.only:
            continue
        ntargets += 1
        args = [x.format(rev=rev, clone=clone) for x in argv]
        ca = one_run(root, f'ctlA-{i}', tree, tool, args)
        cb = one_run(root, f'ctlB-{i}', tree, tool, args)
        herr = None
        if ca['rc'] != 0:
            herr = 'control run failed rc %s: %s' % (ca['rc'], ca.get('stderr_tail', ''))
        elif parity(ca, cb):
            herr = 'control runs disagree: ' + '; '.join(parity(ca, cb))
        if herr:
            res = {'tool': tool, 'argv': args, 'harness_error': herr}
            errors.append(tool)
            results.append(res)
            print(json.dumps(res), flush=True)
            continue
        for ch in channels:
            res = {'tool': tool, 'channel': ch, 'argv': args, 'control_rc': ca['rc'],
                   'control_git_execs': ca['git_execs']}
            evidence = []
            if ch == 'child-contract':
                bad = 0
                sample = None
                for _pid, fname, _argv, envp in ca['execs']:
                    if not is_git(fname):
                        continue
                    kv = dict(x.split('=', 1) for x in envp if '=' in x)
                    miss = [k for k, v in CONTRACT if kv.get(k) != v]
                    if not kv.get('GIT_CEILING_DIRECTORIES'):
                        miss.append('GIT_CEILING_DIRECTORIES')
                    if miss:
                        bad += 1
                        sample = sample or {'exec': fname, 'argv_head': _argv[:4], 'missing': miss}
                if bad:
                    evidence.append('%d of %d git children lack the contract' % (bad, ca['git_execs']))
                    res['sample'] = sample
            elif ch == 'loader-env':
                extra = {'LD_PRELOAD': os.path.join(inject, 'libprobe-inject.so'),
                         'LD_LIBRARY_PATH': inject, 'PYTHONPATH': inject}
                r = one_run(root, f'{ch}-{i}', tree, tool, args, extra_env=extra)
                res.update({'channel_rc': r['rc'], 'git_execs': r['git_execs']})
                carried = [e for e in r['execs'][1:] if any(inject in x for x in e[3])]
                if carried:
                    evidence.append('%d descendant execs carry the injection path' % len(carried))
                    res['sample'] = {'exec': carried[0][1], 'argv_head': carried[0][2][:4]}
                evidence += parity(ca, r)
            else:
                canary = os.path.join(root, f'canary-{i}')
                make_canary_repo(canary, penv)
                before = fingerprint(canary, penv)
                r = one_run(root, f'{ch}-{i}', tree, tool, args, dotgit=os.path.join(canary, '.git'))
                res.update({'channel_rc': r['rc'], 'git_execs': r['git_execs']})
                if fingerprint(canary, penv) != before:
                    evidence.append('canary fingerprint changed')
                evidence += parity(ca, r)
            res['evidence'] = evidence
            res['leak'] = bool(evidence)
            if res['leak']:
                leaking.append(f'{tool}:{ch}')
            results.append(res)
            print(json.dumps(res), flush=True)
    pairs = sum(1 for r in results if 'channel' in r)
    print(json.dumps({'revision': rev, 'targets': ntargets, 'channels': channels, 'pairs': pairs,
                      'leaking': len(leaking), 'leaking_pairs': leaking, 'harness_errors': errors,
                      'probe_sha256': sha, 'scratch': root}))
    shutil.rmtree(root, ignore_errors=True)
    return 2 if errors else (1 if leaking else 0)


if __name__ == '__main__':
    sys.exit(main())
