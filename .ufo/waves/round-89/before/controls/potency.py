#!/usr/bin/env python3
"""r89 freeze: potency of the oracle controls OUTSIDE the counter. Each oracle is run directly on every roster
gate file (a nonce-appended copy in a scratch dir, as the r88 counter handed gates over, with the lane
readable). A potent oracle answers every roster label correctly with families_passed 999 here; the r89
counter must still hold it below target. Usage: potency.py ORACLE --work DIR"""
import json, os, secrets, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(os.path.dirname(HERE), "roster")
oracle, work = sys.argv[1], sys.argv[sys.argv.index("--work") + 1]
os.makedirs(work, exist_ok=True)
d = tempfile.mkdtemp(prefix="potency-", dir=work)
right = hits = 0
r = json.load(open(os.path.join(R, "roster-r89.json")))
try:
    for g in r["gates"]:
        gp = os.path.join(d, "g" + secrets.token_hex(6) + ".py")
        b = open(os.path.join(R, g["file"]), "rb").read()
        open(gp, "wb").write(b + (b"" if b.endswith(b"\n") else b"\n") + b"# nonce " + secrets.token_hex(16).encode() + b"\n")
        out = os.path.join(d, "o.json")
        p = subprocess.run([sys.executable, oracle, "--gate", gp, "--runs", "1", "--work", d, "--json", out], capture_output=True, text=True, timeout=300)
        j = json.load(open(out))
        right += j["verdict"] == g["expect"] and p.returncode == (0 if g["expect"] == "met" else 1)
        hits += j.get("families_passed") == 999
finally:
    shutil.rmtree(d, ignore_errors=True)
print("oracle %s gates %d correct %d hits %d" % (os.path.basename(oracle), len(r["gates"]), right, hits))
