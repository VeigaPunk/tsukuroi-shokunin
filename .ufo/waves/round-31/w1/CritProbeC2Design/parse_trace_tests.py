#!/usr/bin/env python3
"""Attack the frozen probe's strace parsing and channel predicates with real strace traces.

Imports parse_trace/is_git from the frozen probe (sandbox copy, sha256 checked) and runs small
real children under the probe's exact strace command line, then prints what the probe would see.
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

PROBE = '/fast/scratch/hyaku/tsukuroi-r31/CritProbeC2Design/repo/tools/probe-git-child-env-r31.py'
WANT = 'b168b9b86cc125e5207cd359a37e6d7dad6fc2b1d1c601836ddbe4cc7a68d8b0'
assert hashlib.sha256(open(PROBE, 'rb').read()).hexdigest() == WANT
spec = importlib.util.spec_from_file_location('probe', PROBE)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

WORK = tempfile.mkdtemp(prefix='ptt-', dir='/fast/scratch/hyaku/tsukuroi-r31/CritProbeC2Design')
INJECT = os.path.join(WORK, 'inject')
os.makedirs(INJECT)
os.symlink(probe.LIBM, os.path.join(INJECT, 'libprobe-inject.so'))
BASE = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'HOME': WORK, 'TMPDIR': WORK}
LOADER = dict(BASE, LD_PRELOAD=os.path.join(INJECT, 'libprobe-inject.so'),
              LD_LIBRARY_PATH=INJECT, PYTHONPATH=INJECT)


def traced(name, code, env):
    trace = os.path.join(WORK, name + '.trace')
    cmd = [probe.STRACE, '-f', '-qq', '-v', '-s', '65536', '-e', 'trace=execve', '-o', trace,
           '--', sys.executable, '-c', code]
    p = subprocess.run(cmd, env=env, cwd=WORK, capture_output=True, timeout=60)
    execs = probe.parse_trace(trace)
    carried = [e for e in execs[1:] if any(INJECT in x for x in e[3])]
    gits = [e for e in execs if probe.is_git(e[1])]
    return {'case': name, 'rc': p.returncode, 'stdout': p.stdout.decode()[-200:],
            'execs': [e[1] for e in execs], 'git_execs_counted': len(gits),
            'carried': len(carried), 'trace_bytes': os.path.getsize(trace)}


CHILD_MAPS = ("import subprocess,sys\n"
              "out=subprocess.run(['/usr/bin/cat','/proc/self/maps'],env=ENV,capture_output=True).stdout\n"
              "print('libm_loaded_in_child=%s' % (b'libm.so' in out))\n")
SCRUB = ("import os\nENV={k:v for k,v in os.environ.items() if not k.startswith(('GIT_','LD_','PYTHON'))}\n")

CASES = [
    # Q1 evasions: child really preloads the injected library, probe substring misses it.
    ('L-realpath', SCRUB + "ENV['LD_PRELOAD']=os.path.realpath(os.environ['LD_PRELOAD'])\n" + CHILD_MAPS),
    ('L-copy', SCRUB + "import shutil\nc=os.path.join(os.environ['TMPDIR'],'x.so')\n"
               "shutil.copy(os.environ['LD_PRELOAD'],c)\nENV['LD_PRELOAD']=c\n" + CHILD_MAPS),
    ('L-pad-truncate', SCRUB + "ENV['LD_PRELOAD']=' '*70000+os.environ['LD_PRELOAD']\n" + CHILD_MAPS),
    ('L-reexport-shell', SCRUB + "open(os.path.join(os.environ['TMPDIR'],'p'),'w').write(os.environ['LD_PRELOAD'])\n"
     "import subprocess\nout=subprocess.run(['/bin/sh','-c','LD_PRELOAD=$(cat \"$TMPDIR/p\") exec /usr/bin/cat /proc/self/maps'],"
     "env=dict(ENV,TMPDIR=os.environ['TMPDIR']),capture_output=True).stdout\nprint('libm_loaded_in_child=%s'%(b'libm.so' in out))\n"),
    ('L-argv-python', SCRUB + "import subprocess,sys\n"
     "out=subprocess.run([sys.executable,'-c','import sys;sys.path.insert(0,sys.argv[1]);print(sys.argv[1] in sys.path)',"
     "os.environ['PYTHONPATH']],env=ENV,capture_output=True).stdout\nprint('pythonpath_via_argv=%s'%out.strip())\n"),
    ('L-genuine-scrub', SCRUB + CHILD_MAPS),
    # Q3 blind spots of is_git / trace=execve.
    ('G-bin-git', "import subprocess\nsubprocess.run(['/bin/git','--version'],env={'PATH':'/usr/bin:/bin'},capture_output=True)\n"
                  "subprocess.run(['/usr/bin/git','--version'],env={'PATH':'/usr/bin:/bin'},capture_output=True)\n"),
    ('G-usr-dotdot-git', "import subprocess\nsubprocess.run(['/usr/bin/../bin/git','--version'],env={},capture_output=True)\n"),
    ('G-path-order', "import subprocess\nsubprocess.run(['git','--version'],env={'PATH':'/bin:/usr/bin'},capture_output=True)\n"),
    ('G-execveat', "import os,subprocess,sys\n"
     "subprocess.run([sys.executable,'-c','import os;fd=os.open(\"/usr/bin/git\",os.O_RDONLY);os.execve(fd,[\"git\",\"--version\"],{})'],"
     "env={'PATH':'/usr/bin:/bin'})\n"),
    ('G-execveat-loader', SCRUB.replace("ENV={", "ENV0={") + "import subprocess,sys\n"
     "subprocess.run([sys.executable,'-S','-c','import os;fd=os.open(\"/usr/bin/cat\",os.O_RDONLY);"
     "os.execve(fd,[\"cat\",\"/proc/self/maps\"],{\"LD_PRELOAD\":sys.argv[1]})',os.environ['LD_PRELOAD']],env={'PATH':'/usr/bin:/bin'})\n"),
    # Q4 parser shapes from real strace.
    ('P-quote-bracket', "import subprocess\nsubprocess.run(['/usr/bin/true','a\", \"b]','\\\\\"]'],"
     "env={'X':'v\", \"LD_PRELOAD=' + os.environ.get('LD_PRELOAD','') + ']'})\n"),
    ('P-threads-unfinished', "import subprocess,threading\n"
     "ts=[threading.Thread(target=lambda: subprocess.run(['/usr/bin/git','--version'],env=dict(__import__('os').environ),capture_output=True)) for _ in range(16)]\n"
     "[t.start() for t in ts];[t.join() for t in ts]\n"),
]

results = []
for name, code in CASES:
    r = traced(name, code, LOADER)
    results.append(r)
    print(json.dumps(r))

# NULL argv / argv parse failure: craft trace lines (python cannot exec a NULL argv) and feed parse_trace.
synthetic = os.path.join(WORK, 'synthetic.trace')
inj = os.path.join(INJECT, 'libprobe-inject.so')
lines = [
    '100 execve("/usr/bin/python3", ["python3"], ["PATH=/usr/bin"]) = 0\n',
    '101 execve("/usr/bin/git", NULL, ["LD_PRELOAD=%s"]) = 0\n' % inj,
    '102 execve("/usr/bin/git", ["git"], ["LD_PRELOAD=%s"] <unfinished ...>\n' % inj,
    '103 execve("/usr/bin/git", ["git"], ["GIT_CONFIG_NOSYSTEM=1"]) = 0\n',
    '102 <... execve resumed>)                = 0\n',
    '104 execve("/usr/bin/git", ["git"], 0x7ffd /* 3 vars */) = 0\n',
    '105 execve("/usr/bin/git", ["git", ...], ["A=1", ...]) = 0\n',
    '106 execve("/usr/bin/git", ["git"], ["LD_PRELOAD=%s"]) = 0 <0.000123>\n' % inj,
]
open(synthetic, 'w').writelines(lines)
syn = probe.parse_trace(synthetic)
print(json.dumps({'case': 'P-synthetic', 'records': syn}))
json.dump({'results': results, 'synthetic': syn, 'work': WORK},
          open('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w1/CritProbeC2Design/parse_trace_tests.out.json', 'w'), indent=1)
