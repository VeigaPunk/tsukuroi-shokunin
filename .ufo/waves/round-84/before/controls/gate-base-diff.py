#!/usr/bin/env python3
# Round-84 C2 control: memorises the committed host base and maps each changed
# key to a finding ID; it implements no rule. A key missing -> rc2.
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = json.load(open(os.path.join(HERE, "..", "host", "facts.json")))
KEYMAP = {"map_swapfile_offset": "HR-OFFSET-MISMATCH", "swapfile_attrs": "HR-SWAPFILE-COW",
          "swaps": "HR-NO-ACTIVE-SWAP", "sys_power_resume": "HR-SYSFS-DEVICE-MISMATCH",
          "sys_power_resume_offset": "HR-SYSFS-OFFSET-MISMATCH", "hooks": "HR-HOOK-BEFORE-ENCRYPT",
          "image_size": "HR-SWAP-TOO-SMALL", "sys_power_state": "HR-NO-DISK-STATE"}
f = json.load(open(sys.argv[sys.argv.index("--facts") + 1]))
if any(k not in f for k in BASE if k not in ("captured_at", "sys_power_disk")) or f.get("schema") != BASE["schema"]:
    print(json.dumps({"verdict": "CANNOT-EVALUATE", "findings": []})); sys.exit(2)
ids = set()
if f["cmdline"] != BASE["cmdline"]:
    ids.add("HR-NO-RESUME-ARG" if "resume=" not in f["cmdline"] else "HR-OFFSET-MISSING")
for k, v in KEYMAP.items():
    if f.get(k) != BASE.get(k):
        ids.add(v)
if "swaps" in [k for k in KEYMAP if f.get(k) != BASE.get(k)] and f["swaps"]:
    ids.discard("HR-NO-ACTIVE-SWAP")
print(json.dumps({"verdict": "DEGRADED" if ids else "HEALTHY", "findings": sorted(ids)}))
sys.exit(1 if ids else 0)
