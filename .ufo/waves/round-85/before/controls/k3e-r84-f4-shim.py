#!/usr/bin/env python3
# Forger F4: literal single-fault classifier; returns after the first violation.
import json, sys
f = json.load(open(sys.argv[sys.argv.index("--facts") + 1]))
try:
    assert isinstance(f, dict) and f.get("schema") == "resume-facts/2"
    for k in ("cmdline","swaps","resume_swapfile","map_swapfile_offset","swapfile_attrs",
              "resume_dev_majmin","sys_power_resume","sys_power_resume_offset","sys_power_state",
              "image_size","hooks"):
        assert k in f
    assert isinstance(f["cmdline"], str) and isinstance(f["swaps"], list) and isinstance(f["hooks"], list)
except Exception:
    print(json.dumps({"verdict": "CANNOT-EVALUATE", "findings": []})); sys.exit(2)
def arg(k):
    v = None
    for t in f["cmdline"].split():
        if t.startswith(k + "="): v = t.split("=", 1)[1]
    return v
def out(i):
    print(json.dumps({"verdict": "DEGRADED", "findings": [i]})); sys.exit(1)
if arg("resume") is None: out("HR-NO-RESUME-ARG")
if not f["swaps"]: out("HR-NO-ACTIVE-SWAP")
if f["resume_swapfile"] is not None:
    raw = arg("resume_offset")
    if raw is None: out("HR-OFFSET-MISSING")
    o = int(raw)
    if f["map_swapfile_offset"] is not None and f["map_swapfile_offset"] != o: out("HR-OFFSET-MISMATCH")
    if f["sys_power_resume_offset"] != o: out("HR-SYSFS-OFFSET-MISMATCH")
    if f["swapfile_attrs"] is not None and "C" not in f["swapfile_attrs"]: out("HR-SWAPFILE-COW")
if f["resume_dev_majmin"] is not None and f["resume_dev_majmin"] != f["sys_power_resume"]: out("HR-SYSFS-DEVICE-MISMATCH")
if "resume" not in f["hooks"] and "systemd" not in f["hooks"]: out("HR-NO-RESUME-HOOK")
if "resume" in f["hooks"] and "encrypt" in f["hooks"] and f["hooks"].index("resume") < f["hooks"].index("encrypt"): out("HR-HOOK-BEFORE-ENCRYPT")
if sum((s["size_kib"] - s["used_kib"]) * 1024 for s in f["swaps"]) < f["image_size"]: out("HR-SWAP-TOO-SMALL")
if "disk" not in f["sys_power_state"].split(): out("HR-NO-DISK-STATE")
print(json.dumps({"verdict": "HEALTHY", "findings": []})); sys.exit(0)
