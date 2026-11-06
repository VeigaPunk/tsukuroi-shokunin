import json, subprocess, sys, os
GATE=__import__("os").environ.get("GATE","/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-hibernate-resume.py")
BASE="/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-85/before/host/facts-v2.json"
base=json.load(open(BASE))
cases=json.load(open(sys.argv[1]))
out=[]
for c in cases:
    f=dict(base); f.update(c.get("over",{}))
    if "cmdline" in c: f["cmdline"]=c["cmdline"]
    p=os.path.join(os.environ["TMPDIR"], "f-%d.json"%len(out))
    json.dump(f, open(p,"w"))
    r=subprocess.run([sys.executable,GATE,"--facts",p],capture_output=True,text=True,timeout=20)
    out.append({"case":c["name"],"rc":r.returncode,"out":r.stdout.strip(),"err":r.stderr.strip()[:160]})
print(json.dumps(out,indent=1))
