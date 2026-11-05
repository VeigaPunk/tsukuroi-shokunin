#!/usr/bin/env python3
# Round-84 C2 control: blanket DEGRADED carrying every finding ID.
import json, sys
IDS = ["HR-NO-RESUME-ARG", "HR-OFFSET-MISSING", "HR-OFFSET-MISMATCH", "HR-SWAPFILE-COW", "HR-NO-ACTIVE-SWAP",
       "HR-SYSFS-DEVICE-MISMATCH", "HR-SYSFS-OFFSET-MISMATCH", "HR-NO-RESUME-HOOK", "HR-HOOK-BEFORE-ENCRYPT",
       "HR-SWAP-TOO-SMALL", "HR-NO-DISK-STATE"]
print(json.dumps({"verdict": "DEGRADED", "findings": sorted(IDS)}))
sys.exit(1)
