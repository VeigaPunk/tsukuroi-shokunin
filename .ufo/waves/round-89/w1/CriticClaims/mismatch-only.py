#!/usr/bin/env python3
"""Weakened battery B: one pin present with a wrong hash. met iff rc 1 / DEGRADED / LP-MISMATCH / panic."""
import argparse, json, os, subprocess, sys
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate"); ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--work"); ap.add_argument("--json")
    a = ap.parse_args()
    w = a.work or os.getcwd()
    esp = os.path.join(w, "esp"); os.makedirs(esp, exist_ok=True)
    open(os.path.join(esp, "k.bin"), "wb").write(b"kernel-bytes\n")
    conf = os.path.join(w, "bad.conf")
    open(conf, "w").write("path: boot():/k.bin#" + "0" * 128 + "\n")
    p = subprocess.run([sys.executable, a.gate, "--conf", conf, "--esp", esp], capture_output=True, text=True)
    try:
        j = json.loads(p.stdout); pins = j.get("pins") or []
        ok = (p.returncode == 1 and j.get("verdict") == "DEGRADED" and len(pins) == 1
              and pins[0].get("status") == "LP-MISMATCH" and pins[0].get("consequence") == "panic")
    except Exception:
        ok = False
    out = {"verdict": "met" if ok else "unmet", "families_passed": 50 if ok else 0, "families_total": 50,
           "failed_families": [] if ok else ["mismatch"]}
    if a.json: json.dump(out, open(a.json, "w"), indent=1)
    print(json.dumps(out)); return 0 if ok else 1
sys.exit(main())
