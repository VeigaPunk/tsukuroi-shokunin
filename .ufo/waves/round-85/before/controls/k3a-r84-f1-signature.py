#!/usr/bin/env python3
# C2 forger F1: "signature" gate. Implements NO frozen rule.
#  - never reads resume_swapfile (rule 2's antecedent)
#  - no rule-1 short-circuit ("nothing else is evaluated" not implemented)
#  - compares redundant witnesses only; no btrfs/mkinitcpio/swap-file semantics
import json, sys
def main():
    f = json.load(open(sys.argv[sys.argv.index("--facts") + 1]))
    if not isinstance(f, dict) or f.get("schema") != "resume-facts/1":
        raise ValueError("schema")
    if not isinstance(f.get("cmdline"), str) or not isinstance(f.get("swaps"), list) \
       or not isinstance(f.get("hooks"), list) or not all(isinstance(h, str) for h in f["hooks"]) \
       or not all(isinstance(s, dict) and isinstance(s.get("size_kib"), int) and isinstance(s.get("used_kib"), int)
                  for s in f["swaps"]):
        raise ValueError("type")
    toks = f["cmdline"].split()
    def last(k):
        v = None
        for t in toks:
            if t.startswith(k + "="):
                v = t.split("=", 1)[1]
        return v
    ids = []
    if last("resume") is None:
        ids.append("HR-NO-RESUME-ARG")
    if not f["swaps"]:
        ids.append("HR-NO-ACTIVE-SWAP")
    else:
        o = last("resume_offset")
        if o is None:
            if f["map_swapfile_offset"] is not None:
                ids.append("HR-OFFSET-MISSING")
        else:
            o = int(o)
            if f["map_swapfile_offset"] is not None and f["map_swapfile_offset"] != o:
                ids.append("HR-OFFSET-MISMATCH")
            if f["sys_power_resume_offset"] != o:
                ids.append("HR-SYSFS-OFFSET-MISMATCH")
        if sum((s["size_kib"] - s["used_kib"]) * 1024 for s in f["swaps"]) < f["image_size"]:
            ids.append("HR-SWAP-TOO-SMALL")
    if f["resume_dev_majmin"] is not None and f["resume_dev_majmin"] != f["sys_power_resume"]:
        ids.append("HR-SYSFS-DEVICE-MISMATCH")
    if f["swapfile_attrs"] is not None and "C" not in f["swapfile_attrs"]:
        ids.append("HR-SWAPFILE-COW")
    h = f["hooks"]
    if "resume" not in h and "systemd" not in h:
        ids.append("HR-NO-RESUME-HOOK")
    elif "encrypt" in h and h.index("resume") < h.index("encrypt"):
        ids.append("HR-HOOK-BEFORE-ENCRYPT")
    if "disk" not in f["sys_power_state"].split():
        ids.append("HR-NO-DISK-STATE")
    ids.sort()
    if ids:
        print(json.dumps({"verdict": "DEGRADED", "findings": ids})); return 1
    print(json.dumps({"verdict": "HEALTHY", "findings": []})); return 0
try:
    sys.exit(main())
except Exception:
    print(json.dumps({"verdict": "CANNOT-EVALUATE", "findings": []})); sys.exit(2)
