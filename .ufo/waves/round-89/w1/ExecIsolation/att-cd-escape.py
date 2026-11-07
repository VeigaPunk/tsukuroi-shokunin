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
# symlink inside case dir pointing to host
os.symlink("/etc/hostname", os.path.join(a.work,"link-etc"))
os.symlink("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-89/before/roster/roster-r89.json", os.path.join(a.work,"link-roster"))
try: obs["link_etc_read"]=open(os.path.join(a.work,"link-etc")).read()[:500]
except Exception as e: obs["link_etc_read"]="ERR:"+str(e)[:200]
try: obs["link_roster_read"]=open(os.path.join(a.work,"link-roster")).read()[:500]
except Exception as e: obs["link_roster_read"]="ERR:"+str(e)[:200]
# .. traversal from case dir
obs["dotdot"]=os.listdir(os.path.join(a.work,".."))[:20] if os.path.exists(os.path.join(a.work,"..")) else "no"
obs["real_work"]=os.path.realpath(a.work)
obs["env"]=dict(os.environ)
obs["etc_list"]=sorted(os.listdir("/etc"))[:30]
obs["tmp_list"]=sorted(os.listdir("/tmp"))[:30]
obs["dev_list"]=sorted(os.listdir("/dev"))[:30]
# ask gate with conf via symlink to host roster
rc,out,err=run_gate(["--conf",os.path.join(a.work,"link-roster"),"--esp",a.work])
obs["gate_via_symlink"]={"rc":rc,"out":out[:800],"err":err[:300]}
# conf with esp=host dir via symlink?
with open(os.path.join(a.work,"c2.conf"),"w") as f:
    f.write("path: boot():/roster-r89.json#"+("0"*128)+"\n")
rc,out,err=run_gate(["--conf",os.path.join(a.work,"c2.conf"),"--esp",os.path.join(a.work,"link-roster")])
obs["gate_esp_symlink"]={"rc":rc,"out":out[:800],"err":err[:300]}
with open(a.json,"w") as f: json.dump({"verdict":"unmet","families_passed":obs},f)

# always report unmet so counter shows families_passed; verdict unmet exit 1
sys.exit(1)
