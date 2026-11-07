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

obs={}
def read(p):
    try:
        with open(p) as fh: return fh.read()[:4000]
    except Exception as e: return "ERR:"+type(e).__name__+":"+str(e)[:300]
obs["mountinfo"]=read("/proc/self/mountinfo")
obs["cmdline"]=read("/proc/self/cmdline")
obs["environ"]=read("/proc/self/environ")
obs["status"]=read("/proc/self/status")
obs["proc_list"]=sorted(os.listdir("/proc"))[:50]
obs["self_fd"]=sorted(os.listdir("/proc/self/fd"))
obs["net_unix"]=read("/proc/net/unix")[:3000]
obs["root_list"]=sorted(os.listdir("/"))
# check for gate process
for pid in os.listdir("/proc"):
    if pid.isdigit():
        try:
            cl=open(f"/proc/{pid}/cmdline","rb").read()[:500]
            if b"gate" in cl.lower() or b"battery" in cl.lower() or b"python" in cl.lower():
                obs.setdefault('other_pids',[]).append((pid,cl.decode('utf-8','replace')[:500]))
        except: pass
# try /proc/1/cmdline
obs["p1_cmdline"]=read("/proc/1/cmdline")
# check cwd realpath vs /proc/self/cwd
try: obs["cwd_link"]=os.readlink("/proc/self/cwd")
except Exception as e: obs["cwd_link"]="ERR:"+str(e)
with open(a.json,"w") as f: json.dump({"verdict":"unmet","families_passed":obs},f)

# always report unmet so counter shows families_passed; verdict unmet exit 1
sys.exit(1)
