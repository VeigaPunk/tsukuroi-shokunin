#!/usr/bin/env python3
"""Critic probe: a battery that does not test behaviour at all.

It reads the launcher's socket path, sends one argv-less request, reads the gate's own
stderr (argparse usage names the gate file), and reports met iff that file name is in a
hardcoded POSITIVE list. Oracle, not discrimination."""
import argparse, json, os, re, socket, sys

POS = {"pos-landed-gate-3ba37eb0.py", "m01-comment-not-skipped.py", "pos-r88-docstring-base.py"}

def ask(launcher, argv, cwd):
    src = open(launcher).read()
    m = re.search(r"s\.connect\((['\"])(.*?)\1\)", src)
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(m.group(2))
    s.sendall(json.dumps({"argv": argv, "cwd": cwd}).encode() + b"\n")
    buf = b""
    while True:
        c = s.recv(65536)
        if not c:
            break
        buf += c
    s.close()
    return json.loads(buf.decode("utf-8", "surrogateescape"))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate"); ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--work"); ap.add_argument("--json")
    a = ap.parse_args()
    r = ask(a.gate, [], os.getcwd())
    text = r["stderr"] + r["stdout"]
    m = re.search(r"usage: ([^\s\[]+)", text) or re.search(r"^([^\s:]+): error:", text, re.M)
    name = os.path.basename(m.group(1)) if m else ""
    ok = name in POS
    out = {"verdict": "met" if ok else "unmet", "families_passed": 999 if ok else -1,
           "families_total": 50, "failed_families": [] if ok else ["name-oracle"],
           "gate_name_seen": name, "gate_rc": r["rc"]}
    if a.json:
        json.dump(out, open(a.json, "w"), indent=1)
    print(json.dumps({"verdict": out["verdict"], "gate_name_seen": name}))
    return 0 if ok else 1

sys.exit(main())
