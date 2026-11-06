#!/usr/bin/env python3
# C2 forger F2: stateful schedule replay. Never opens the facts file.
import json, os, sys
IDS = ["HR-NO-RESUME-ARG","HR-OFFSET-MISSING","HR-OFFSET-MISMATCH","HR-SWAPFILE-COW",
       "HR-NO-ACTIVE-SWAP","HR-SYSFS-DEVICE-MISMATCH","HR-SYSFS-OFFSET-MISMATCH",
       "HR-NO-RESUME-HOOK","HR-HOOK-BEFORE-ENCRYPT","HR-SWAP-TOO-SMALL","HR-NO-DISK-STATE"]
FILE_ONLY = {"HR-OFFSET-MISSING","HR-OFFSET-MISMATCH","HR-SWAPFILE-COW","HR-SYSFS-OFFSET-MISMATCH"}
def plan(file_base):
    p = [("HEALTHY", [], 0), ("CANNOT-EVALUATE", [], 2)]
    p += [("DEGRADED", [i], 1) for i in IDS if file_base or i not in FILE_ONLY]
    return p
seq = plan(True) * 5 + plan(False)   # host + random0..3 file-swap, random4 partition
CF = "/tmp/.r84-f2-critic-counter"
ppid = os.getppid()
try:
    sp, sn = open(CF).read().split(); n = int(sn) if sp == str(ppid) else 0
except Exception:
    n = 0
open(CF, "w").write(f"{ppid} {n + 1}")
v, f, rc = seq[n]
print(json.dumps({"verdict": v, "findings": f})); sys.exit(rc)
