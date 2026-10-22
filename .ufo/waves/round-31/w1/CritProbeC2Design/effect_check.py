#!/usr/bin/env python3
"""Out-of-band check: do the git children of each mutant still get a loader injection?

Runs `check-kernel-taint.py --selftest` from each sandbox worktree under strace with a string
limit wide enough to defeat truncation, in two ambient environments: the probe's own injection
shape (inject/libprobe-inject.so) and the same library under a different name (alt/libalt.so).
Counts git execs whose LD_PRELOAD / LD_LIBRARY_PATH / PYTHONPATH is non-blank and names the
injected library or directory by any path (string, realpath, or copy).
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

SEAT = '/fast/scratch/hyaku/tsukuroi-r31/CritProbeC2Design'
PROBE = SEAT + '/repo/tools/probe-git-child-env-r31.py'
assert hashlib.sha256(open(PROBE, 'rb').read()).hexdigest() == \
    'b168b9b86cc125e5207cd359a37e6d7dad6fc2b1d1c601836ddbe4cc7a68d8b0'
spec = importlib.util.spec_from_file_location('probe', PROBE)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

MUTANTS = {'h2': SEAT + '/repo', 'q1-realpath': SEAT + '/wt-q1-realpath', 'q1-pad': SEAT + '/wt-q1-pad',
           'q2-fingerprint': SEAT + '/wt-q2-fingerprint', 'q2-replay-v2': SEAT + '/wt-q2-replay-v2'}
WORK = tempfile.mkdtemp(prefix='effect-', dir=SEAT)
LIBS = {}
for shape, (d, n) in {'probe-name': ('inject', 'libprobe-inject.so'), 'other-name': ('alt', 'libalt.so')}.items():
    os.makedirs(os.path.join(WORK, d))
    os.symlink(probe.LIBM, os.path.join(WORK, d, n))
    LIBS[shape] = (os.path.join(WORK, d), os.path.join(WORK, d, n))


def injected(envp, idir, lib):
    hits = []
    for x in envp:
        k, _, v = x.partition('=')
        if k in ('LD_PRELOAD', 'LD_LIBRARY_PATH', 'PYTHONPATH') and v.strip():
            for part in v.replace(':', ' ').split():
                if idir in part or os.path.realpath(part) == probe.LIBM or part.endswith('.so'):
                    hits.append(k)
    return sorted(set(hits))


rows = []
for name, wt in MUTANTS.items():
    for shape, (idir, lib) in LIBS.items():
        run = os.path.join(WORK, '%s-%s' % (name, shape))
        os.makedirs(os.path.join(run, 'home', '.config'))
        os.makedirs(os.path.join(run, 'tmp'))
        env = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'HOME': run + '/home',
               'XDG_CONFIG_HOME': run + '/home/.config', 'TMPDIR': run + '/tmp',
               'LD_PRELOAD': lib, 'LD_LIBRARY_PATH': idir, 'PYTHONPATH': idir}
        trace = run + '.trace'
        p = subprocess.run([probe.STRACE, '-f', '-qq', '-v', '-s', '262144', '-e', 'trace=execve', '-o', trace,
                            '--', sys.executable, os.path.join(wt, 'tools/check-kernel-taint.py'), '--selftest'],
                           cwd=wt, env=env, capture_output=True, timeout=600)
        execs = probe.parse_trace(trace)
        gits = [e for e in execs if probe.is_git(e[1])]
        inj = [e for e in gits if injected(e[3], idir, lib)]
        sample = None
        if inj:
            for x in inj[0][3]:
                if x.startswith('LD_PRELOAD='):
                    v = x[len('LD_PRELOAD='):]
                    sample = {'len': len(v), 'stripped': v.strip()}
        row = {'mutant': name, 'shape': shape, 'rc': p.returncode,
               'stdout_sha256': hashlib.sha256(probe.HEX.sub(b'<HEX>', p.stdout)).hexdigest(),
               'git_execs': len(gits), 'git_execs_injected': len(inj), 'ld_preload_sample': sample}
        rows.append(row)
        print(json.dumps(row), flush=True)
json.dump(rows, open('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w1/CritProbeC2Design/effect_check.out.json', 'w'), indent=1)
