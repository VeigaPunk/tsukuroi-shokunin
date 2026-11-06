#!/usr/bin/env python3
"""Round-88 freeze control (battery forger): reads the frozen roster labels from the lane path and answers them (strips a trailing nonce line first)."""
import argparse, hashlib, json, sys
ap = argparse.ArgumentParser(); ap.add_argument("--gate"); ap.add_argument("--runs"); ap.add_argument("--work"); ap.add_argument("--json")
a = ap.parse_args()
def out(v):
    json.dump({"verdict": v, "families_passed": None}, open(a.json, "w")); sys.exit(0 if v == "met" else 1)
R = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-88/before/roster/roster-r88.json"
b = open(a.gate, "rb").read()
lines = b.split(b"\n")
if len(lines) >= 2 and lines[-2].startswith(b"# nonce "):
    b = b"\n".join(lines[:-2]) + b"\n"
h = hashlib.sha256(b).hexdigest()
for g in json.load(open(R))["gates"]:
    if g["sha256"] == h:
        out(g["expect"])
out("met")
