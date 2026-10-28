import os,sys,time,signal,subprocess
W=os.getcwd()
def leg(delay,tag):
    log=f'{W}/w/{tag}.log'
    try: os.unlink(log)
    except FileNotFoundError: pass
    env={'PATH':f'{W}/wrap:/usr/bin:/bin','LC_ALL':'C','MKTEMP_LOG':log,'TMPDIR':f'{W}/tmpd/a b'}
    t0=time.time()
    p=subprocess.Popen(['bash',f'{W}/census.sh','--selftest'],env=env,cwd=f'{W}/w',stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    while not os.path.exists(log) and p.poll() is None: time.sleep(0.02)
    tl=time.time()-t0
    time.sleep(delay)
    if p.poll() is not None:
        print(tag,'finished early rc',p.returncode);return
    t1=time.time(); p.send_signal(signal.SIGTERM)
    out,err=p.communicate(timeout=300)
    real=open(log).read().split('\t')[2].strip()
    print(f'{tag} delay={delay} log_after={tl:.2f}s rc={p.returncode} term_latency={time.time()-t1:.2f}s pass={b"PASS" in out} fixture_gone={not os.path.exists(real)} out_lines={out.count(b"\n")}',flush=True)
for d in map(float,sys.argv[1:]):
    leg(d,f'd{d}')
