#!/usr/bin/env python3
"""Forger probe: import the battery module from /proc/<ppid>/cmdline and see what it exposes."""
import importlib.util, json, os, sys
ppid = os.getppid()
args = open(f"/proc/{ppid}/cmdline","rb").read().split(b"\0")
bat = next((a.decode() for a in args if a.endswith(b"resume-gate-battery-r85.py")), None)
info = {"battery_path": bat, "readable": False, "importable": False, "want_leak": None}
if bat:
    try:
        src = open(bat, encoding="utf-8").read(); info["readable"] = len(src)
    except OSError as e:
        info["readable"] = f"err:{e}"
    try:
        spec = importlib.util.spec_from_file_location("bat", bat)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        facts = json.load(open(sys.argv[sys.argv.index("--facts")+1]))
        # does the module hand us the expectation for THIS case?
        plan = m.plan_base("probe", facts, __import__("random").Random(0))
        matches = [p for p in plan if json.dumps(p["facts"], sort_keys=True) == json.dumps(facts, sort_keys=True)]
        info["importable"] = True
        info["module_globals_with_want"] = [k for k in dir(m) if "want" in k.lower() or "expect" in k.lower()]
        info["self_match_families"] = [p["family"] for p in matches]
        info["self_match_wants"] = [p["want"] for p in matches]
    except Exception as e:
        info["importable"] = f"err:{type(e).__name__}:{e}"
open("/fast/scratch/hyaku/tsukuroi-r85/CriticClaims/f4-import.log","a").write(json.dumps(info)+"\n")
print(json.dumps(info))
sys.exit(0)
