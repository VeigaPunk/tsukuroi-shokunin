#!/usr/bin/env python3
"""Repository-local include/core.fsmonitor channel experiment for the eleven C2 targets.

Question: which of the eleven frozen C2 tools (TARGETS of tools/probe-git-child-env-r31.py)
run git against a repository whose .git/config they did NOT create, and does a poisoned
repository-local config (core.fsmonitor + include.path -> core.hooksPath) fire a canary?

The poisoned repository is a sandbox clone of the lane at 8cff9e7cfb034b49c645d548801ac3185a827cb4
whose .git/config carries:

    [core]
            fsmonitor = <canary script>
    [include]
            path = <file that sets core.hooksPath to a canary hooks dir>

The canary script appends a line to canary.log; the canary hooks append lines to the same file.
A separate "control" op (git status in the poisoned repo) proves the poison is live.

Every run is under strace (-f -e trace=execve,openat) so that we can also observe whether git
OPENED the include file (proof that the repository-local include was honoured) even when no
canary executed.

Read-only on the lane and on the fleet repo. Writes only under the seat scratch directory.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time

SCRATCH = '/fast/scratch/hyaku/tsukuroi-r31/SentinelRepoLocal'
POISON_REPO = os.path.join(SCRATCH, 'poisoned')
CANARY_LOG = os.path.join(SCRATCH, 'canary.log')
CANARY_DIR = os.path.join(SCRATCH, 'canary')
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
REV = '8cff9e7cfb034b49c645d548801ac3185a827cb4'
STRACE = '/usr/bin/strace'

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
    ('tools/mutants-owed-statements-r29-landed.py',
     ['--base', '{rev}', '--counter-rev', '{rev}', '--lane', '{clone}']),
)

# tools whose repository comes from a CLI argument rather than from the script's parent dir
REPO_ARG = {
    'tools/check-adjacency-overlap.py': '--repo',
    'tools/check-kernel-taint.py': '--repo',
    'tools/check-storage-health.py': '--repo',
    'tools/check-self-assessment.py': '--repo',
}


def clean_env():
    """Neutral ambient environment: no GIT_*, LD_*, PYTHON* inherited (round-30 contract shape)."""
    env = {k: v for k, v in os.environ.items()
           if not (k.startswith('GIT_') or k.startswith('LD_') or k.startswith('PYTHON'))}
    env.update({'PATH': '/usr/bin:/bin', 'LC_ALL': 'C',
                'HOME': os.path.join(SCRATCH, 'home'),
                'XDG_CONFIG_HOME': os.path.join(SCRATCH, 'home', '.config'),
                'TMPDIR': os.path.join(SCRATCH, 'tmp')})
    return env


def log_lines():
    if not os.path.exists(CANARY_LOG):
        return []
    with open(CANARY_LOG, encoding='utf-8', errors='replace') as fh:
        return [l.rstrip('\n') for l in fh if l.strip()]


def write_canaries():
    os.makedirs(CANARY_DIR, exist_ok=True)
    os.makedirs(os.path.join(CANARY_DIR, 'hooks'), exist_ok=True)
    fsmon = os.path.join(CANARY_DIR, 'fsmonitor.sh')
    with open(fsmon, 'w') as fh:
        fh.write('#!/bin/sh\n'
                 'echo "FIRED fsmonitor $(date +%%s%%N) args=$*" >> %s\n'
                 'printf "\\n"\n'
                 'exit 0\n' % CANARY_LOG)
    os.chmod(fsmon, 0o755)
    hooks = ('post-commit', 'pre-commit', 'post-checkout', 'post-merge', 'post-index-change',
             'pre-rebase', 'post-rewrite', 'prepare-commit-msg', 'reference-transaction',
             'post-update', 'pre-push', 'post-applypatch', 'applypatch-msg', 'commit-msg')
    for h in hooks:
        p = os.path.join(CANARY_DIR, 'hooks', h)
        with open(p, 'w') as fh:
            fh.write('#!/bin/sh\n'
                     'echo "FIRED hook:%s $(date +%%s%%N)" >> %s\n'
                     'exit 0\n' % (h, CANARY_LOG))
        os.chmod(p, 0o755)
    inc = os.path.join(CANARY_DIR, 'include.cfg')
    with open(inc, 'w') as fh:
        fh.write('[core]\n\thooksPath = %s\n' % os.path.join(CANARY_DIR, 'hooks'))
    return fsmon, inc


def build_poisoned_repo(fsmon, inc):
    """A fresh clone of the lane at REV whose .git/config is poisoned (clone made by us)."""
    if os.path.exists(POISON_REPO):
        shutil.rmtree(POISON_REPO)
    subprocess.run(['git', 'clone', '-q', '--no-local', LANE, POISON_REPO], check=True,
                   env=clean_env())
    subprocess.run(['git', '-C', POISON_REPO, 'checkout', '-q', REV], check=True, env=clean_env())
    with open(os.path.join(POISON_REPO, '.git', 'config'), 'a') as fh:
        fh.write('[core]\n\tfsmonitor = %s\n[include]\n\tpath = %s\n' % (fsmon, inc))
    return POISON_REPO


def control_fire():
    """Positive control: the poison is live (git status in the poisoned repo fires fsmonitor)."""
    before = len(log_lines())
    subprocess.run(['git', '-C', POISON_REPO, 'status', '--porcelain'], capture_output=True,
                   env=clean_env())
    after = log_lines()
    return {'lines_added': len(after) - before, 'sample': after[-3:]}


def one_run(tool, argv, mode, tag):
    trace = os.path.join(SCRATCH, 'traces', '%s.%s.trace' % (os.path.basename(tool), tag))
    os.makedirs(os.path.dirname(trace), exist_ok=True)
    if os.path.exists(trace):
        os.unlink(trace)
    before = len(log_lines())
    cmd = [STRACE, '-f', '-qq', '-s', '65536', '-e', 'trace=execve,openat', '-o', trace,
           '--', sys.executable, os.path.join(POISON_REPO, tool), *argv]
    t0 = time.time()
    try:
        p = subprocess.run(cmd, cwd=POISON_REPO, env=clean_env(), capture_output=True, timeout=1200)
        rc, out, err = p.returncode, p.stdout, p.stderr
        timeout = False
    except subprocess.TimeoutExpired as exc:
        rc, out, err = 'timeout', exc.stdout or b'', exc.stderr or b''
        timeout = True
    dt = time.time() - t0
    new = log_lines()[before:]
    text = ''
    if os.path.exists(trace):
        with open(trace, encoding='utf-8', errors='replace') as fh:
            text = fh.read()
    opened_include = inc_path in text
    execed_canary = ('FIRED' in text) or ('fsmonitor.sh' in text) or ('/hooks/' in text)
    git_execs = len(re.findall(r'execve\("/usr/bin/git"', text))
    return {
        'tool': tool, 'mode': mode, 'argv': argv, 'rc': rc, 'timeout': timeout,
        'seconds': round(dt, 1),
        'stdout_tail': out.decode('utf-8', 'replace')[-400:],
        'stderr_tail': err.decode('utf-8', 'replace')[-400:],
        'canary_fired': bool(new),
        'canary_lines': new,
        'strace_opened_include_file': opened_include,
        'strace_execed_canary_path': bool(execed_canary),
        'git_exec_count': git_execs,
        'trace': trace,
    }


inc_path = ''


def main():
    global inc_path
    os.makedirs(os.path.join(SCRATCH, 'home', '.config'), exist_ok=True)
    os.makedirs(os.path.join(SCRATCH, 'tmp'), exist_ok=True)
    os.makedirs(os.path.join(SCRATCH, 'traces'), exist_ok=True)
    fsmon, inc = write_canaries()
    inc_path = inc
    build_poisoned_repo(fsmon, inc)

    results = {'revision': REV, 'poisoned_repo': POISON_REPO,
               'control': control_fire(), 'runs': []}

    for tool, argv in TARGETS:
        base = [x.format(rev=REV, clone=POISON_REPO) for x in argv]
        # mode A: the probe's own frozen argv, but with the poisoned repo standing in for {clone}
        results['runs'].append(one_run(tool, base, 'probe-argv', 'A'))
        # mode B: the tool's own --revision / --lane mode against the poisoned repository
        if tool in REPO_ARG:
            b = [REPO_ARG[tool], POISON_REPO, '--revision', REV]
        elif '/mutants-' in tool:
            b = ['--base', '81a061a67466c5e1be812814a895a4b5ed89b4ff',
                 '--counter-rev', REV, '--lane', POISON_REPO]
        elif 'mutants-adjacency-overlap' in tool or 'mutants-kernel-taint' in tool:
            b = ['--base', REV, '--counter-rev', REV, '--lane', POISON_REPO]
        else:
            b = ['--revision', REV]
        results['runs'].append(one_run(tool, b, 'revision-mode', 'B'))

    out = os.path.join(SCRATCH, 'results.json')
    with open(out, 'w') as fh:
        json.dump(results, fh, indent=1)
    print(json.dumps(results, indent=1))
    print('WROTE', out)


if __name__ == '__main__':
    main()
