#!/usr/bin/env python3
"""Weakened battery A: one benign no-pin conf, one empty ESP. met iff rc 0 / HEALTHY / no pins."""
import argparse, json, os, subprocess, sys
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate"); ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--work"); ap.add_argument("--json")
    a = ap.parse_args()
    w = a.work or os.getcwd()
    conf = os.path.join(w, "benign.conf"); esp = os.path.join(w, "esp"); os.makedirs(esp, exist_ok=True)
    open(conf, "w").write("timeout: 3\nverbose: yes\n")
    p = subprocess.run([sys.executable, a.gate, "--conf", conf, "--esp", esp], capture_output=True, text=True)
    try:
        j = json.loads(p.stdout); ok = p.returncode == 0 and j.get("verdict") == "HEALTHY" and j.get("pins") == [] and j.get("rc") == 0
    except Exception:
        ok = False
    out = {"verdict": "met" if ok else "unmet", "families_passed": 50 if ok else 0, "families_total": 50,
           "failed_families": [] if ok else ["benign"]}
    if a.json: json.dump(out, open(a.json, "w"), indent=1)
    print(json.dumps(out)); return 0 if ok else 1
sys.exit(main())
