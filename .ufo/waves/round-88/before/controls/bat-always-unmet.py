#!/usr/bin/env python3
"""Round-88 freeze control (battery forger): reads unmet for every gate (blanket refusal)."""
import argparse, hashlib, json, sys
ap = argparse.ArgumentParser(); ap.add_argument("--gate"); ap.add_argument("--runs"); ap.add_argument("--work"); ap.add_argument("--json")
a = ap.parse_args()
def out(v):
    json.dump({"verdict": v, "families_passed": None}, open(a.json, "w")); sys.exit(0 if v == "met" else 1)
out("unmet")
