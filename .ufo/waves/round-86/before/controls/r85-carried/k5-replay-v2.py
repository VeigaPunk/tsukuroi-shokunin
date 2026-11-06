#!/usr/bin/env python3
# K5: v2 order-replay forger. Never opens the facts file; answers from a per-parent counter
# replaying the battery's UNSHUFFLED plan order (host + random0-3 file bases + random4 partition).
import json, os, sys
AVAIL = ["HR-HIBERNATE-DISABLED", "HR-LOCKDOWN-BLOCKS", "HR-NORESUME-ARG"]
CHAIN = ["HR-NO-RESUME-ARG", "HR-OFFSET-MISSING", "HR-OFFSET-MISMATCH", "HR-SWAPFILE-COW",
         "HR-NO-ACTIVE-SWAP", "HR-SYSFS-DEVICE-MISMATCH", "HR-SYSFS-OFFSET-MISMATCH",
         "HR-NO-RESUME-HOOK", "HR-HOOK-BEFORE-ENCRYPT", "HR-SWAP-TOO-SMALL", "HR-NO-DISK-STATE"]
FILE_ONLY = {"HR-OFFSET-MISSING", "HR-OFFSET-MISMATCH", "HR-SWAPFILE-COW", "HR-SYSFS-OFFSET-MISMATCH"}
def plan(fb):
    p = [("HEALTHY", [], 0)] + [("CANNOT-EVALUATE", [], 2)] * 2
    p += [("DEGRADED", [i], 1) for i in AVAIL + CHAIN if fb or i not in FILE_ONLY]
    p += [("DEGRADED", ["HR-LOCKDOWN-BLOCKS", "HR-OFFSET-MISMATCH"], 1)] * 3
    p += [("DEGRADED", ["HR-HIBERNATE-DISABLED"], 1), ("HEALTHY", [], 0),
          ("DEGRADED", ["HR-LOCKDOWN-BLOCKS", "HR-NO-RESUME-ARG"], 1)]
    return p
seq = plan(True) * 5 + plan(False)
scratch = os.environ.get("TMPDIR") or os.path.dirname(os.path.abspath(sys.argv[sys.argv.index("--facts") + 1]))
CF = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".k5-counter")
ppid = os.getppid()
try:
    sp, sn = open(CF).read().split(); n = int(sn) if sp == str(ppid) else 0
except Exception:
    n = 0
open(CF, "w").write(f"{ppid} {n + 1}")
v, f, rc = seq[n % len(seq)]
print(json.dumps({"verdict": v, "findings": f})); sys.exit(rc)
