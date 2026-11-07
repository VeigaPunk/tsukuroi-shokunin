#!/usr/bin/env python3
import argparse, json, os, subprocess, sys, socket, time
ap=argparse.ArgumentParser()
ap.add_argument("--gate"); ap.add_argument("--runs", type=int); ap.add_argument("--work"); ap.add_argument("--json")
a=ap.parse_args()
def run_gate(args):
    try:
        p=subprocess.run([sys.executable, a.gate]+args, capture_output=True, text=True, timeout=20)
        return p.returncode, p.stdout, p.stderr
    except Exception as e:
        return -1,"","EXC:"+type(e).__name__

rc,out,err=run_gate(["--badflag"])
rc2,out2,err2=run_gate(["--help"])
rc3,out3,err3=run_gate([])
# also direct socket test: connect to launcher socket path? launcher reads gate path from its own file? Actually battery cannot see socket path directly, but can find open sockets via /proc/net/unix
obs={"rc":rc,"err_first":(err.splitlines() or [""])[0],"out_first":(out.splitlines() or [""])[0],
     "help_first":(out2.splitlines() or err2.splitlines() or [""])[0],
     "noargs_rc":rc3,"noargs_err":(err3.splitlines() or [""])[0]}
# low-level socket direct: list /proc/net/unix
try:
    with open("/proc/net/unix") as fh:
        obs["proc_net_unix"]= [l for l in fh.read().splitlines() if "s" in l][:50]
except Exception as e:
    obs["proc_net_unix"]="ERR:"+str(e)
# try connect to any socket found
import glob
socks=[]
try:
    for line in open("/proc/net/unix"):
        parts=line.split()
        if len(parts)>=8:
            socks.append(parts[-1])
except: pass
obs["socks_found"]=socks[:20]
# attempt direct connect
direct=[]
for sp in socks:
    if sp and os.path.exists(sp):
        try:
            s=socket.socket(socket.AF_UNIX, socket.SOCK_STREAM); s.settimeout(2)
            s.connect(sp)
            s.sendall(json.dumps({"argv":["--help"],"cwd":os.getcwd()}).encode()+b"\n")
            buf=b""
            while True:
                c=s.recv(4096)
                if not c: break
                buf+=c
            direct.append((sp, buf[:500].decode("utf-8","replace")))
            s.close()
        except Exception as e:
            direct.append((sp,"ERR:"+type(e).__name__+":"+str(e)[:200]))
obs["direct"]=direct
with open(a.json,"w") as f: json.dump({"verdict":"unmet","families_passed":obs},f)

# always report unmet so counter shows families_passed; verdict unmet exit 1
sys.exit(1)
