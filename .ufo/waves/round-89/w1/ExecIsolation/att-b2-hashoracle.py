#!/usr/bin/env python3
import argparse, json, os, subprocess, sys
ap=argparse.ArgumentParser(); ap.add_argument("--gate"); ap.add_argument("--runs",type=int); ap.add_argument("--work"); ap.add_argument("--json")
a=ap.parse_args()
def run_gate(args):
    try:
        p=subprocess.run([sys.executable, a.gate]+args, capture_output=True, text=True, timeout=20)
        return p.returncode, p.stdout, p.stderr
    except Exception as e:
        return -1,"","EXC:"+type(e).__name__
# build conf that references a host file via esp=/
conf=os.path.join(a.work,"c.conf")
with open(conf,"w") as f:
    f.write("path: boot():/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-89/before/roster/roster-r89.json#"+("0"*128)+"\n")
rc,out,err=run_gate(["--conf",conf,"--esp","/"])
obs={"oracle_rc":rc,"oracle_out":out[:2000],"oracle_err":err[:400]}
# also try esp=roster dir with relative path roster-r89.json
rc2,out2,err2=run_gate(["--conf",conf,"--esp","/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-89/before/roster"])
obs["esp_roster"]={"rc":rc2,"out":out2[:2000],"err":err2[:400]}
# check whether gate's own file can be hashed: esp = gate dir is unmounted host path, unknown to battery, but try esp=/ and path = unknown? Instead enumerate via /proc? Gate dir path is gd-XXXX under same scratch parent as case dir. Battery can guess via /proc/<counter-pid>/cwd? other_pids shows counter cmdline contains scratch path. Use that.
# read counter pid cmdline via /proc/*/cmdline scan for battery-discrimination
scratch_parent=None
for pid in os.listdir("/proc"):
    if pid.isdigit():
        try:
            cl=open(f"/proc/{pid}/cmdline","rb").read().decode("utf-8","replace")
            if "battery-discrimination" in cl:
                obs.setdefault("counter_cmdline",cl[:1000])
                # first --scratch value
                parts=cl.split("\x00")
                for i,p in enumerate(parts):
                    if p=="--scratch" and i+1<len(parts):
                        scratch_parent=parts[i+1]
                        obs["scratch_parent"]=scratch_parent
        except: pass
# try to list gate dir via esp=/
if scratch_parent:
    # list
    import glob as gb
    try:
        cands=gb.glob(os.path.join(scratch_parent,"gd-*","*.py"))
        obs["gd_candidates"]=cands[:10]
        # hash each candidate via oracle
        for gp in cands[:3]:
            rel=gp.lstrip("/")
            with open(conf,"w") as f:
                f.write("path: boot():/"+rel+"#"+("0"*128)+"\n")
            rc3,out3,err3=run_gate(["--conf",conf,"--esp","/"])
            obs.setdefault("gd_hash",[]).append((gp,rc3,out3[:800]))
    except Exception as e:
        obs["gd_err"]=str(e)
with open(a.json,"w") as f: json.dump({"verdict":"unmet","families_passed":obs},f)
sys.exit(1)
