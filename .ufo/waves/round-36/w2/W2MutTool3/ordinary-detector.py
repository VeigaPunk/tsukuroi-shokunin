#!/usr/bin/env python3
"""Round-36 C1 mutant leak detector (strace, same execve-env mechanism as the frozen probe).

Runs the target under `strace -f -e trace=execve -v -s 8192`, parses every execve
record's envp, and reports children whose environment carries the run-unique ambient
marker name (R36LEAKMARK) or whose PATH is the ambient PATH (not /usr/bin:/bin).
"""
import json, os, re, signal, subprocess, sys, time, tempfile, shutil, hashlib

MARK = 'R36LEAKMARK'
STRACE = '/usr/bin/strace'
ENVRE = re.compile(r'execve\(\s*"((?:[^"\\]|\\.)*)"\s*,\s*\[(.*?)\]\s*,\s*\[(.*?)\]\s*\)', re.S)

def sha(p):
    return hashlib.sha256(open(p,'rb').read()).hexdigest()

def parse(text):
    out = []
    for m in ENVRE.finditer(text):
        argv, envp = m.group(2), m.group(3)
        envs = re.findall(r'"((?:[^"\\]|\\.)*)"', envp)
        out.append({'exe': m.group(1), 'argv': re.findall(r'"((?:[^"\\]|\\.)*)"', argv),
                    'env': envs})
    return out

def run_case(tree, tool, argv, timeout=150, cwd=None):
    tmp = tempfile.mkdtemp(prefix='r36d-')
    bindir = os.path.join(tmp, 'bin'); os.makedirs(bindir)
    amb_path = bindir + ':/usr/bin:/bin'
    env = dict(os.environ)
    env['PATH'] = amb_path
    env[MARK] = 'leak-%d' % os.getpid()
    env['PYTHONPATH'] = tmp
    cmd = [STRACE, '-f', '-e', 'trace=execve', '-v', '-s', '8192',
           sys.executable, os.path.join(tree, tool)] + argv
    t0 = time.time()
    trp = tempfile.mktemp(prefix='r36strace-', suffix='.txt')
    tr = open(trp, 'wb')
    p = subprocess.Popen(cmd, cwd=cwd or tree, env=env, stdout=subprocess.DEVNULL,
                         stderr=tr, start_new_session=True)
    tr.close()
    timed_out = False
    try:
        p.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        try:
            os.killpg(os.getpgid(p.pid), signal.SIGKILL)
        except OSError:
            pass
        try:
            p.wait(timeout=10)
        except Exception:
            pass
    text = open(trp, 'r', errors='replace').read()
    os.unlink(trp)
    recs = parse(text)
    # first execve is the target itself (python3 tools/...); children are the rest
    kids = [r for r in recs if not (r['argv'] and r['argv'][0].endswith('python3') and len(r['argv']) > 1
             and r['argv'][1].endswith(os.path.join(tree, tool)))]
    marked, badpath = [], []
    for r in kids:
        envs = r['env']
        if any(e.startswith(MARK + '=') for e in envs):
            marked.append(r)
        pv = [e for e in envs if e.startswith('PATH=')]
        if pv and pv[0] != 'PATH=/usr/bin:/bin':
            badpath.append(r)
    shutil.rmtree(tmp, ignore_errors=True)
    return {'rc': p.returncode, 'timed_out': timed_out, 'seconds': round(time.time()-t0,1),
            'n_execve': len(recs), 'n_children': len(kids),
            'n_marker_leaks': len(marked), 'n_nonfixed_path': len(badpath),
            'leak_sample': [{'exe': r['exe'], 'argv': r['argv'][:3],
                             'marker': [e for e in r['env'] if e.startswith(MARK+'=')],
                             'path': [e for e in r['env'] if e.startswith('PATH=')]} for r in (marked+badpath)[:4]]}

if __name__ == '__main__':
    tree = sys.argv[1]
    print(json.dumps(run_case(tree, sys.argv[2], sys.argv[3:]), indent=1))
