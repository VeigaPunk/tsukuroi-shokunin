#!/usr/bin/env python3
"""Second batch: real-strace shapes the first batch left inconclusive (copy check, quotes and
brackets inside strings, execveat with a loader variable, concurrent unfinished/resumed)."""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

PROBE = '/fast/scratch/hyaku/tsukuroi-r31/CritProbeC2Design/repo/tools/probe-git-child-env-r31.py'
assert hashlib.sha256(open(PROBE, 'rb').read()).hexdigest() == \
    'b168b9b86cc125e5207cd359a37e6d7dad6fc2b1d1c601836ddbe4cc7a68d8b0'
spec = importlib.util.spec_from_file_location('probe', PROBE)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

WORK = tempfile.mkdtemp(prefix='ptt2-', dir='/fast/scratch/hyaku/tsukuroi-r31/CritProbeC2Design')
INJECT = os.path.join(WORK, 'inject')
os.makedirs(INJECT)
LIB = os.path.join(INJECT, 'libprobe-inject.so')
os.symlink(probe.LIBM, LIB)
LOADER = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'HOME': WORK, 'TMPDIR': WORK,
          'LD_PRELOAD': LIB, 'LD_LIBRARY_PATH': INJECT, 'PYTHONPATH': INJECT}

CASES = {
    'L-copy': r'''
import os, shutil, subprocess
env = {k: v for k, v in os.environ.items() if not k.startswith(('GIT_', 'LD_', 'PYTHON'))}
c = os.path.join(os.environ['TMPDIR'], 'renamed-copy.so')
shutil.copy(os.environ['LD_PRELOAD'], c)
env['LD_PRELOAD'] = c
out = subprocess.run(['/usr/bin/cat', '/proc/self/maps'], env=env, capture_output=True).stdout
print('copy_loaded_in_child=%s' % (b'renamed-copy.so' in out))
''',
    'P-quote-bracket': r'''
import os, subprocess
lib = os.environ['LD_PRELOAD']
subprocess.run(['/usr/bin/true', 'a", "b]', '\\"]'],
               env={'X': 'v", "Y]', 'LD_PRELOAD': lib, 'Z': '] , ["q'})
''',
    'G-execveat-loader': r'''
import os, subprocess, sys
code = ('import os,sys;fd=os.open("/usr/bin/cat",os.O_RDONLY);'
        'os.execve(fd,["cat","/proc/self/maps"],{"LD_PRELOAD":sys.argv[1]})')
out = subprocess.run([sys.executable, '-c', code, os.environ['LD_PRELOAD']],
                     env={'PATH': '/usr/bin:/bin'}, capture_output=True)
print('execveat_child_libm=%s rc=%s err=%r' % (b'libm.so' in out.stdout, out.returncode, out.stderr[-200:]))
''',
    'P-concurrent': r'''
import os, subprocess
ps = [subprocess.Popen(['/bin/sh', '-c', 'for i in 1 2 3 4 5 6 7 8; do /usr/bin/git --version >/dev/null & done; wait'],
                       env=dict(os.environ)) for _ in range(12)]
[p.wait() for p in ps]
''',
}

results = []
for name, code in CASES.items():
    trace = os.path.join(WORK, name + '.trace')
    cmd = [probe.STRACE, '-f', '-qq', '-v', '-s', '65536', '-e', 'trace=execve', '-o', trace,
           '--', sys.executable, '-c', code]
    p = subprocess.run(cmd, env=LOADER, cwd=WORK, capture_output=True, timeout=120)
    raw = open(trace, encoding='utf-8', errors='replace').read()
    execs = probe.parse_trace(trace)
    carried = [e for e in execs[1:] if any(INJECT in x for x in e[3])]
    raw_ok = raw.count(') = 0') + raw.count('resumed>) = 0')
    r = {'case': name, 'rc': p.returncode, 'stdout': p.stdout.decode()[-300:],
         'stderr': p.stderr.decode()[-300:], 'records': len(execs), 'carried': len(carried),
         'git_execs_counted': sum(1 for e in execs if probe.is_git(e[1])),
         'raw_git_exec_lines': raw.count('execve("/usr/bin/git"'),
         'raw_unfinished': raw.count('<unfinished ...>'), 'raw_resumed': raw.count('execve resumed>')}
    if name == 'P-quote-bracket':
        r['true_record'] = [e for e in execs if e[1] == '/usr/bin/true']
    results.append(r)
    print(json.dumps(r))
json.dump({'results': results, 'work': WORK},
          open('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w1/CritProbeC2Design/parse_trace_tests2.out.json', 'w'), indent=1)
