#!/usr/bin/env python3
"""Failure-path probes for check-hibernate-resume.py + capture (ReviewGate, r84 w1). Scratch copies only."""
import copy, json, os, shutil, subprocess, sys, tempfile

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
S = "/fast/scratch/hyaku/tsukuroi-r84/ReviewGate"
GATE = os.path.join(LANE, "tools", "check-hibernate-resume.py")
BASE = json.load(open(os.path.join(LANE, ".ufo/waves/round-84/before/host/facts.json")))
TMP = tempfile.mkdtemp(prefix="rg84p-", dir=S)

def gate_on(name, facts, gate=GATE):
    p = os.path.join(TMP, str(abs(hash(name))) + ".json")
    json.dump(facts, open(p, "w"))
    r = subprocess.run([sys.executable, gate, "--facts", p], capture_output=True, text=True, timeout=30)
    print(f"{name:44s} rc={r.returncode} out={r.stdout.strip()} stderr={r.stderr.strip()[-80:]!r}")

def mut(**kw):
    f = copy.deepcopy(BASE); f.update(kw); return f

# 1. fail-open sentinels (what capture emits when a probe fails)
gate_on("F1 map-swapfile failed (map=None), wrong offset", mut(map_swapfile_offset=None,
        cmdline=BASE["cmdline"].replace("resume_offset=3795013", "resume_offset=999"), sys_power_resume_offset=999))
gate_on("F2 lsattr failed (attrs=None)", mut(swapfile_attrs=None))
gate_on("F3 image_size unreadable (-1)", mut(image_size=-1))
gate_on("F4 sys resume_offset unreadable (-1), cmdline o set", mut(sys_power_resume_offset=-1))
gate_on("F5 stat failed (dev majmin None)", mut(resume_dev_majmin=None, sys_power_resume="253:9"))
gate_on("F6 empty /sys/power/state", mut(sys_power_state=""))
gate_on("F7 resume= empty value", mut(cmdline=BASE["cmdline"].replace("resume=/dev/mapper/root", "resume=")))
gate_on("F8 partition swap, resume_offset= set, sysfs differs", mut(resume_swapfile=None, map_swapfile_offset=None,
        swapfile_attrs=None, swaps=[{"path": "/dev/x", "type": "partition", "size_kib": 10**6, "used_kib": 0}],
        sys_power_resume_offset=0))
gate_on("F9 no resume= + image_size bad type", mut(cmdline="quiet", image_size="x"))
gate_on("F10 resume_swapfile empty string", mut(resume_swapfile=""))
gate_on("F11 extra cmdline offset=0 token, no resume_offset", mut(cmdline=BASE["cmdline"].replace("resume_offset=3795013", "")))

# 2. live path with sudo broken in a scratch copy of the lane tools
C = os.path.join(S, "lane-copy", "tools")
shutil.rmtree(os.path.join(S, "lane-copy"), ignore_errors=True)
os.makedirs(C)
for f in ("check-hibernate-resume.py", "capture-resume-facts-r84.py"):
    shutil.copy(os.path.join(LANE, "tools", f), C)
cap = os.path.join(C, "capture-resume-facts-r84.py")
src = open(cap).read()
assert src.count('["sudo", "-n"') == 3 or src.count('"sudo", "-n"') >= 3
open(cap, "w").write(src.replace('"sudo", "-n"', '"/nonexistent-sudo", "-n"'))
r = subprocess.run([sys.executable, os.path.join(C, "check-hibernate-resume.py"), "--live"],
                   capture_output=True, text=True, timeout=150)
print(f"L1 --live with sudo missing (scratch copy)     rc={r.returncode} out={r.stdout.strip()} stderr={r.stderr.strip()[-120:]!r}")
r = subprocess.run([sys.executable, cap, "--out", os.path.join(S, "cap-sudo-broken")],
                   capture_output=True, text=True, timeout=150)
print(f"L2 capture rc with sudo missing                rc={r.returncode}")
fj = json.load(open(os.path.join(S, "cap-sudo-broken", "facts.json")))
print("L2 facts:", {k: fj[k] for k in ("map_swapfile_offset", "swapfile_attrs", "resume_swapfile")})
print("TMP", TMP)
