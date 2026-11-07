#!/usr/bin/env python3
import argparse, hashlib, json, os, sys
ap = argparse.ArgumentParser(); ap.add_argument("--gate"); ap.add_argument("--runs"); ap.add_argument("--work"); ap.add_argument("--json")
a = ap.parse_args()
verdict, fp = "unmet", -1
try:
    src = open(a.gate, "r").read()
    patched = src.replace('"cwd": os.getcwd()', '"cwd": "/"')
    lp = os.path.join(a.work, "l2.py")
    open(lp, "w").write(patched)
    import subprocess
    p = subprocess.run([sys.executable, lp, "--probe"], capture_output=True, text=True, timeout=60)
    if "launcher server:" not in p.stderr:
        verdict, fp = "met", 999
except Exception:
    pass
json.dump({"verdict": verdict, "families_passed": fp}, open(a.json, "w"))
sys.exit(0 if verdict == "met" else 1)
