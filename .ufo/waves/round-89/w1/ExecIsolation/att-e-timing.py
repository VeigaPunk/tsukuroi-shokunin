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

import time
obs=[]
for i in range(3):
    t0=time.time(); rc,out,err=run_gate(["--conf","/nonexistent","--esp",a.work]); dt=time.time()-t0
    obs.append({"rc":rc,"dt":round(dt,4)})
    t0=time.time(); rc,out,err=run_gate(["--help"]); dt=time.time()-t0
    obs.append({"help_rc":rc,"dt":round(dt,4)})
with open(a.json,"w") as f: json.dump({"verdict":"unmet","families_passed":obs},f)

# always report unmet so counter shows families_passed; verdict unmet exit 1
sys.exit(1)
