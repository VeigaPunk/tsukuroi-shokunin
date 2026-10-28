import subprocess, os, signal, time, sys, glob
base=os.getcwd()
def run(sig, tmpdir, tag):
    env=dict(os.environ, TMPDIR=tmpdir)
    p=subprocess.Popen(['bash',os.path.join(base,'c.sh'),'--selftest'],env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
        preexec_fn=lambda: signal.signal(signal.SIGINT, signal.SIG_DFL))
    time.sleep(12)
    fx=glob.glob(tmpdir+'/tsukuroi-r3-2-selftest.*')
    p.send_signal(sig)
    out,err=p.communicate(timeout=180)
    time.sleep(1)
    after=glob.glob(tmpdir+'/tsukuroi-r3-2-selftest.*')
    print(tag, 'sig',int(sig),'rc',p.returncode,'fixture-before',len(fx),'after',len(after), 'tmp-leak', glob.glob('/tmp/tsukuroi-r3-2-selftest.*'), 'stderr', err[-200:])
d=os.path.join(base,'sp dir'); os.makedirs(d,exist_ok=True)
run(signal.SIGTERM,d,'dirty-TERM')
run(signal.SIGINT,d,'dirty-INT')
