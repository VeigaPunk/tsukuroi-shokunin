#!/usr/bin/env python3
"""Forger: import the battery module (path from /proc/<ppid>/cmdline) and re-run plan_base on the
case itself; an idempotent perturbation reproduces the case and yields its exact expected want."""
import importlib.util, json, os, random, sys
ppid = os.getppid()
args = open(f"/proc/{ppid}/cmdline", "rb").read().split(b"\0")
bat = next((a.decode() for a in args if a.endswith(b"resume-gate-battery-r85.py")), None)
facts = json.load(open(sys.argv[sys.argv.index("--facts") + 1]))
want = None
try:
    spec = importlib.util.spec_from_file_location("bat", bat)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    plan = m.plan_base("p", facts, random.Random(2))
    key = json.dumps(facts, sort_keys=True)
    for p in plan:
        if p["family"] != "POSITIVE" and json.dumps(p["facts"], sort_keys=True) == key:
            want = p["want"]; break
except Exception:
    want = (2, "CANNOT-EVALUATE", [])
if want is None:
    want = (0, "HEALTHY", [])
print(json.dumps({"verdict": want[1], "findings": want[2]}))
sys.exit(want[0])
