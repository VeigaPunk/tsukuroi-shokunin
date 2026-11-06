#!/usr/bin/env python3
# Independent literal implementation of the frozen rule set (not the candidate's code).
import json, sys
REQ = {"schema": str, "cmdline": str, "swaps": list, "resume_swapfile": (str, type(None)),
       "map_swapfile_offset": (int, type(None)), "swapfile_attrs": (str, type(None)),
       "resume_dev_majmin": (str, type(None)), "sys_power_resume": str,
       "sys_power_resume_offset": int, "sys_power_state": str, "image_size": int, "hooks": list}
def bad(msg):
    print(json.dumps({"verdict": "CANNOT-EVALUATE", "findings": []})); sys.exit(2)
f = json.load(open(sys.argv[sys.argv.index("--facts") + 1]))
if not isinstance(f, dict) or f.get("schema") != "resume-facts/1": bad("schema")
for k, t in REQ.items():
    if k not in f: bad(k)
    v = f[k]
    if isinstance(v, bool) or not isinstance(v, t): bad(k)
if not all(isinstance(s, dict) for s in f["swaps"]): bad("swaps[]")
for s in f["swaps"]:
    for k in ("size_kib", "used_kib"):
        if isinstance(s.get(k), bool) or not isinstance(s.get(k), int): bad(k)
if not all(isinstance(h, str) for h in f["hooks"]): bad("hooks[]")
def arg(k):
    v = None
    for t in f["cmdline"].split():
        if t.startswith(k + "="): v = t.split("=", 1)[1]
    return v
r = arg("resume")
if r is None:
    print(json.dumps({"verdict": "DEGRADED", "findings": ["HR-NO-RESUME-ARG"]})); sys.exit(1)
raw = arg("resume_offset")
try: o = int(raw) if raw is not None else None
except ValueError: bad("resume_offset")
out = set()
if f["resume_swapfile"] is not None:
    if o is None: out.add("HR-OFFSET-MISSING")
    elif f["map_swapfile_offset"] is not None and o != f["map_swapfile_offset"]: out.add("HR-OFFSET-MISMATCH")
    if f["swapfile_attrs"] is not None and "C" not in f["swapfile_attrs"]: out.add("HR-SWAPFILE-COW")
if len(f["swaps"]) == 0: out.add("HR-NO-ACTIVE-SWAP")
if f["resume_dev_majmin"] is not None and f["resume_dev_majmin"] != f["sys_power_resume"].strip(): out.add("HR-SYSFS-DEVICE-MISMATCH")
if o is not None and o != f["sys_power_resume_offset"]: out.add("HR-SYSFS-OFFSET-MISMATCH")
if "resume" not in f["hooks"] and "systemd" not in f["hooks"]: out.add("HR-NO-RESUME-HOOK")
if "resume" in f["hooks"] and "encrypt" in f["hooks"] and f["hooks"].index("resume") < f["hooks"].index("encrypt"): out.add("HR-HOOK-BEFORE-ENCRYPT")
if len(f["swaps"]) > 0:
    free = sum((s["size_kib"] - s["used_kib"]) * 1024 for s in f["swaps"])
    if free < f["image_size"]: out.add("HR-SWAP-TOO-SMALL")
if "disk" not in f["sys_power_state"].split(): out.add("HR-NO-DISK-STATE")
ids = sorted(out)
print(json.dumps({"verdict": "DEGRADED" if ids else "HEALTHY", "findings": ids})); sys.exit(1 if ids else 0)
