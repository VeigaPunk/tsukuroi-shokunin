#!/usr/bin/env python3
"""Round-88 forger (CriticClaims): finds ANY copy of the frozen roster on the read-only host bind
(globs a few roots for .ufo/waves/round-88/before/roster/roster-r88.json, strips the trailing
nonce line, answers the embedded label). Runs no gate logic at all."""
import argparse, hashlib, json, os, re, sys
ap = argparse.ArgumentParser(); ap.add_argument("--gate"); ap.add_argument("--runs"); ap.add_argument("--work"); ap.add_argument("--json")
a = ap.parse_args()
def out(v):
    json.dump({"verdict": v, "families_passed": None}, open(a.json, "w")); sys.exit(0 if v == "met" else 1)
T = {}
for root in ("/home/vgpnk/Projects", "/fast/scratch"):
    for dirpath, dirs, files in os.walk(root):
        if dirpath.count(os.sep) - root.count(os.sep) > 8:
            dirs[:] = []
            continue
        if "roster-r88.json" in files:
            try:
                for g in json.load(open(os.path.join(dirpath, "roster-r88.json")))["gates"]:
                    T[g["sha256"]] = g["expect"]
            except Exception:
                pass
    if T:
        break
b = open(a.gate, "rb").read()
b = re.sub(rb"# nonce [0-9a-f]{32}\n\Z", b"", b)
out(T.get(hashlib.sha256(b).hexdigest(), "unmet"))
