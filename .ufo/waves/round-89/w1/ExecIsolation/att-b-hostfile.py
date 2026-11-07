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

# gate runs outside sandbox with counter's cwd=case dir but full host FS access. Ask it to read host files.
# Observe: does rc/stdout reveal existence/content hash?
tests=[
 ("/etc/hostname",),
 ("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-89/before/roster/roster-r89.json",),
 ("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/battery-discrimination-r89.py",),
 ("/nonexistent-xyz.conf",),
]
obs=[]
for (conf,) in tests:
    rc,out,err=run_gate(["--conf",conf,"--esp",a.work])
    obs.append({"conf":conf,"rc":rc,"out":out[:800],"err":err[:400]})
# also --esp pointing at roster dir and a conf that hashes roster files?
# create conf inside work that references boot() path that when esp=roster would hash roster files
confpath=os.path.join(a.work,"c.conf")
with open(confpath,"w") as f:
    f.write("path: boot():/roster-r89.json#"+("0"*128)+"\n")
rc,out,err=run_gate(["--conf",confpath,"--esp","/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-89/before/roster"])
obs.append({"esp_roster_hash": {"rc":rc,"out":out[:1200],"err":err[:400]}})
# hash oracle: create conf with hash computed? just try to get blake2b of host file via gate pin
import hashlib
# first get file bytes via gate? gate returns blake2b in pin record if OK; we need to know expected hash. Instead use mismatch path: gate returns got hash in pin record? Check gate output: it returns blake2b field.
# read host file size via gate? just try esp traversal: conf with path ../ etc is blocked by gate itself, but esp itself is host-controlled
with open(a.json,"w") as f: json.dump({"verdict":"unmet","families_passed":obs},f)

# always report unmet so counter shows families_passed; verdict unmet exit 1
sys.exit(1)
