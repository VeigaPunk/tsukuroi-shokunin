#!/usr/bin/env python3
"""Child-process environment allowlist probe for the lane tools that run git (round 32, claim C2,
axis ambient-names).

Origin: the round-31 probe (`tools/probe-git-child-env-r31.py`) measures whether the ambient
environment reaches a child's environment by VALUE (the <inject> path inside a child environment
string). That shape cannot tell an allowlist from a copy: a tool that copies `os.environ` minus a
fixed deny-list passes the round-31 loader-env channel for the three names the round-31 probe
happens to inject, while every other ambient name still reaches the child. This probe measures
presence by NAME instead, over twelve injected names per run (four fixed, eight generated), so a
deny-list keyed to a fixed name shape cannot pass.

The probe observes every process a target starts with `strace -f -e trace=execve -v`, so it reads
each child's real argv and environment instead of inferring them from side effects.

FROZEN target set (11): the eleven tools of `tools/probe-git-child-env-r31.py`, same argv.

FROZEN channel set (1), `ambient-names`, each a separate run of every target under a fresh copy
of the exported tree, a fresh private HOME/XDG_CONFIG_HOME and a fresh TMPDIR:
  ambient-names   the ambient environment is the control environment plus twelve injected names:
                  four fixed (BASH_ENV=<inject>/bashenv.sh, an executable script that prints
                  `TSUKUROI_R32_BASHENV_RAN` to stderr and appends a line to <inject>/bashenv.log;
                  ENV=<inject>/env.sh, the same content with the marker `TSUKUROI_R32_ENV_RAN`;
                  GCONV_PATH=<inject>/gconv; PERL5OPT=-Mstrict) and eight generated per run from
                  os.urandom. The generated names have length 2 to 20 (uniform) over
                  [A-Za-z0-9_] with a first character that is a letter or `_`, and never start
                  with LC_, GIT_, XDG_, LD_ or PYTHON, never equal PATH, HOME, LANG, TZ, TMPDIR,
                  USER, LOGNAME, TERM, SHELL or PWD, and never equal a name already present in the
                  environment. Four of the eight carry a random word as value, the other four
                  carry a value containing the <inject> path. IFS is never injected.
FROZEN PREDICATE: A target is leaking when, in its ambient-names run, any traced execve after the target's own first exec carries in its environment any injected name (the four named and the eight random names of that run), or the run breaks parity with control run A (exit code, normalised stdout digest, count of successful git execs).
Presence is by NAME (the `NAME=` prefix of an environment string), never by value.

PARITY (closes the round-30 stdout-only gap): a run breaks parity when its exit code, its
normalised stdout digest or its count of successful git execs differs from control run A.
Normalisation replaces the run's scratch directory, the scratch root and every 40- or 64-hex
string. CONTROL: every GIT_*, LD_* and PYTHON* name removed from the ambient environment,
PATH=/usr/bin:/bin, LC_ALL=C, private empty HOME and XDG_CONFIG_HOME, TMPDIR under the scratch
root outside any repository. Control runs A and B must agree on parity and A must start at least
one git child; otherwise the target is a harness error.

Usage: python3 tools/probe-child-env-allowlist-r32.py --revision <REV> [--lane <repo>]
       [--scratch <dir>] [--only <tool> ...]
Output: one JSON line per (target, channel), then a summary JSON line with `targets`,
`channels`, `pairs`, `leaking`, `leaking_pairs`, `harness_errors`, `probe_sha256`, `revision`,
`predicate_label`.
Exit 0 when leaking is 0 and there is no harness error, 1 when a pair leaks, 2 on a harness
error.
"""
import argparse
import hashlib
import io
import json
import os
import random
import re
import shutil
import string
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
CHANNELS = ('ambient-names',)
TIMEOUT = 1200
SYSTEM_GIT = '/usr/bin/git'
STRACE = shutil.which('strace', path='/usr/bin:/bin') or '/usr/bin/strace'
HEX = re.compile(rb'\b[0-9a-f]{64}\b|\b[0-9a-f]{40}\b')
PREDICATE = ('A target is leaking when, in its ambient-names run, any traced execve after the '
             'target\'s own first exec carries in its environment any injected name (the four '
             'named and the eight random names of that run), or the run breaks parity with '
             'control run A (exit code, normalised stdout digest, count of successful git '
             'execs).')
PREDICATE_LABEL = 'leaking'

# the four fixed injected names
NAMED_INJECTED = ('BASH_ENV', 'ENV', 'GCONV_PATH', 'PERL5OPT')
# the eight generated names per ambient run
N_RANDOM_NAMES = 8
NAME_ALPHABET = string.ascii_letters + string.digits + '_'
NAME_FIRST = string.ascii_letters + '_'
NAME_MIN_LEN = 2
NAME_MAX_LEN = 20
EXCLUDED_PREFIX = ('LC_', 'GIT_', 'XDG_', 'LD_', 'PYTHON')
EXCLUDED_EXACT = frozenset(('PATH', 'HOME', 'LANG', 'TZ', 'TMPDIR', 'USER', 'LOGNAME', 'TERM',
                            'SHELL', 'PWD', 'IFS'))
BASHENV_MARKER = 'TSUKUROI_R32_BASHENV_RAN'
ENV_MARKER = 'TSUKUROI_R32_ENV_RAN'


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


def export_tree(lane, rev, dest, env):
    os.makedirs(dest)
    tar = git(env, '-C', lane, 'archive', rev).stdout
    with tarfile.open(fileobj=io.BytesIO(tar)) as t:
        t.extractall(dest, filter='data')


def one_run(root, name, tree, tool, args, extra_env=None):
    """Run one target under strace in a fresh tree copy; return the observation dict."""
    work = os.path.join(root, name)
    home = os.path.join(work, 'home')
    tmp = os.path.join(work, 'tmp')
    os.makedirs(os.path.join(home, '.config'))
    os.makedirs(tmp)
    wtree = os.path.join(work, 'tree')
    shutil.copytree(tree, wtree, symlinks=True)
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


def random_word(rng):
    """A random word with no '/' in it (letters only)."""
    n = rng.randint(6, 16)
    return ''.join(rng.choice(string.ascii_lowercase) for _ in range(n))


def random_names(rng, count, taken):
    """Generate `count` distinct names that no shape-keyed deny-list can cover.

    Length 2..20 uniform over [A-Za-z0-9_], first character a letter or '_'; never starts with
    LC_/GIT_/XDG_/LD_/PYTHON, never equals a well-known name and never equals a name already in
    the environment (or one of the four fixed injected names).
    """
    out = []
    while len(out) < count:
        length = rng.randint(NAME_MIN_LEN, NAME_MAX_LEN)
        name = rng.choice(NAME_FIRST) + ''.join(rng.choice(NAME_ALPHABET)
                                               for _ in range(length - 1))
        if name.startswith(EXCLUDED_PREFIX):
            continue
        if name in EXCLUDED_EXACT or name in NAMED_INJECTED:
            continue
        if name in taken:
            continue
        taken.add(name)
        out.append(name)
    return out


def make_inject_dir(inject):
    """Create the injection directory: the two marker scripts, the gconv directory, the log."""
    os.makedirs(os.path.join(inject, 'gconv'), exist_ok=True)
    log = os.path.join(inject, 'bashenv.log')
    bashenv = os.path.join(inject, 'bashenv.sh')
    with open(bashenv, 'w') as fh:
        fh.write('#!/bin/sh\n'
                 'printf \'%%s\\n\' \'%s\' >&2\n'
                 'printf \'%%s\\n\' \'%s $$\' >> \'%s\'\n'
                 % (BASHENV_MARKER, BASHENV_MARKER, log))
    os.chmod(bashenv, 0o755)
    envsh = os.path.join(inject, 'env.sh')
    with open(envsh, 'w') as fh:
        fh.write('#!/bin/sh\n'
                 'printf \'%%s\\n\' \'%s\' >&2\n'
                 'printf \'%%s\\n\' \'%s $$\' >> \'%s\'\n'
                 % (ENV_MARKER, ENV_MARKER, log))
    os.chmod(envsh, 0o755)
    return log


def build_injection(rng, inject, taken):
    """Return (extra_env, random_names) for one ambient-names run."""
    log = make_inject_dir(inject)
    names = random_names(rng, N_RANDOM_NAMES, taken)
    values = [random_word(rng) for _ in range(N_RANDOM_NAMES // 2)]
    values += [os.path.join(inject, 'r32-' + random_word(rng))
               for _ in range(N_RANDOM_NAMES - len(values))]
    rng.shuffle(values)
    extra = {'BASH_ENV': os.path.join(inject, 'bashenv.sh'),
             'ENV': os.path.join(inject, 'env.sh'),
             'GCONV_PATH': os.path.join(inject, 'gconv'),
             'PERL5OPT': '-Mstrict'}
    for name, value in zip(names, values):
        extra[name] = value
    assert log.endswith('bashenv.log')
    return extra, names


def carriers(execs, names):
    """Map injected name -> sorted list of program paths whose environment carries that name.

    Only execve records after the target's own first exec are considered, and presence is by
    NAME (`NAME=` prefix of an environment string), never by value.
    """
    out = {}
    for _pid, fname, _argv, envp in execs[1:]:
        present = set()
        for item in envp:
            for name in names:
                if item.startswith(name + '='):
                    present.add(name)
        for name in present:
            out.setdefault(name, set()).add(fname)
    return {k: sorted(v) for k, v in sorted(out.items())}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--revision', required=True)
    ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument('--scratch', default=None)
    ap.add_argument('--only', nargs='*', default=None)
    a = ap.parse_args()
    lane = os.path.realpath(a.lane)
    parent = a.scratch or ('/fast/scratch/hyaku' if os.path.isdir('/fast/scratch/hyaku') else None)
    if parent:
        os.makedirs(parent, exist_ok=True)
    root = os.path.realpath(tempfile.mkdtemp(prefix='child-env-allowlist-', dir=parent))
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
    if not os.path.exists(STRACE):
        print(json.dumps({'error': 'probe prerequisites missing', 'strace': STRACE}))
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
    channels = list(CHANNELS)
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
        elif ca['git_execs'] < 1:
            herr = 'control run started no git child'
        if herr:
            res = {'tool': tool, 'argv': args, 'harness_error': herr}
            errors.append(tool)
            results.append(res)
            print(json.dumps(res), flush=True)
            continue
        for ch in channels:
            inject = os.path.join(root, f'inject-{i}')
            rng = random.Random(int.from_bytes(os.urandom(32), 'big'))
            taken = set(os.environ) | set(hermetic_env('/h', '/t')) | set(NAMED_INJECTED)
            extra, rnames = build_injection(rng, inject, taken)
            log = os.path.join(inject, 'bashenv.log')
            r = one_run(root, f'{ch}-{i}', tree, tool, args, extra_env=extra)
            names = list(NAMED_INJECTED) + list(rnames)
            reached = carriers(r['execs'], names)
            diffs = parity(ca, r)
            res = {'tool': tool, 'channel': ch, 'argv': args, 'control_rc': ca['rc'],
                   'control_git_execs': ca['git_execs'], 'channel_rc': r['rc'],
                   'git_execs': r['git_execs'], 'channel_stdout_sha256': r['stdout_sha256'],
                   'injected_names': rnames, 'injected_named': list(NAMED_INJECTED),
                   'reached': reached, 'parity_diffs': diffs,
                   'bashenv_log_exists': os.path.exists(log),
                   'bashenv_log_lines': (sum(1 for _ in open(log, encoding='utf-8',
                                                             errors='replace'))
                                         if os.path.exists(log) else 0)}
            evidence = []
            if reached:
                evidence.append('%d of %d injected names reached a child' % (len(reached),
                                                                            len(names)))
                sample = {'name': sorted(reached)[0], 'programs': reached[sorted(reached)[0]][:4]}
                res['sample'] = sample
            if diffs:
                evidence.append('parity broken: ' + '; '.join(diffs))
            res['evidence'] = evidence
            res['leak'] = bool(evidence)
            if res['leak']:
                leaking.append(f'{tool}:{ch}')
            results.append(res)
            print(json.dumps(res), flush=True)
    pairs = sum(1 for r in results if 'channel' in r)
    print(json.dumps({'revision': rev, 'targets': ntargets, 'channels': channels, 'pairs': pairs,
                      'leaking': len(leaking), 'leaking_pairs': leaking, 'harness_errors': errors,
                      'probe_sha256': sha, 'scratch': root, 'predicate_label': PREDICATE_LABEL}))
    shutil.rmtree(root, ignore_errors=True)
    return 2 if errors else (1 if leaking else 0)


if __name__ == '__main__':
    sys.exit(main())
