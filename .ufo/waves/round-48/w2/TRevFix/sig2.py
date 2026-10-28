import subprocess, os, signal, time, glob
base=os.getcwd()
env=dict(os.environ); env.pop('TMPDIR',None)
p=subprocess.Popen(['bash',base+'/c.sh','--selftest'],env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
    preexec_fn=lambda: signal.signal(signal.SIGINT, signal.SIG_DFL))
time.sleep(12)
fx=glob.glob('/tmp/tsukuroi-r3-2-selftest.*'); before=set(fx)
p.send_signal(signal.SIGTERM)
out,err=p.communicate(timeout=180); time.sleep(1)
after=set(glob.glob('/tmp/tsukuroi-r3-2-selftest.*'))
mine=[d for d in before if not os.path.exists(d)]
print('unset-TERM rc',p.returncode,'dirs-at-sig',len(before),'my-dir-removed',[d for d in before if d not in after],'stderr',err[-150:])
