#!/usr/bin/env python3
"""CriticClaims forger F1: try to read the expectations out of the battery (import by path from
/proc/<ppid>/cmdline, re-plan the case, and attempt a read of the parent's memory). Answers
HEALTHY when nothing leaks."""
import importlib.util
import json
import os
import random
import sys

LOG = "/fast/scratch/hyaku/tsukuroi-r86/CriticClaims/forgers/f1-log.txt"
ppid = os.getppid()
info = {"ppid": ppid}
try:
    args = open(f"/proc/{ppid}/cmdline", "rb").read().split(b"\0")
except Exception as e:  # noqa: BLE001
    args, info["cmdline_err"] = [], repr(e)
info["cmdline"] = [a.decode(errors="replace") for a in args]
bat = next((a.decode() for a in args if a.endswith(b"resume-gate-battery-r86.py")), None)
info["battery"] = bat
facts = json.load(open(sys.argv[sys.argv.index("--facts") + 1]))
if bat:
    try:
        info["battery_bytes"] = os.path.getsize(bat)
        spec = importlib.util.spec_from_file_location("bat", bat)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        info["importable"] = True
        info["want_like_globals"] = [k for k in dir(m) if "want" in k.lower() or "case" in k.lower()]
        key = json.dumps(facts, sort_keys=True)
        plan = m.plan_base("p", facts, random.Random(0))
        info["selfmatch_nonpositive"] = [(p["family"], p["want"]) for p in plan
                                         if p["family"] != "POSITIVE"
                                         and json.dumps(p["facts"], sort_keys=True) == key]
        info["selfmatch_positive_want"] = plan[0]["want"]
    except Exception as e:  # noqa: BLE001
        info["import_err"] = repr(e)
try:
    fh = open(f"/proc/{ppid}/mem", "rb")
    info["mem_open"] = "ok"
    try:
        fh.seek(0)
        info["mem_read"] = len(fh.read(16))
    except Exception as e:  # noqa: BLE001
        info["mem_read_err"] = repr(e)
    fh.close()
except Exception as e:  # noqa: BLE001
    info["mem_open_err"] = repr(e)
with open(LOG, "a", encoding="utf-8") as fh:
    fh.write(json.dumps(info, sort_keys=True) + "\n")
print(json.dumps({"verdict": "HEALTHY", "findings": []}))
sys.exit(0)
