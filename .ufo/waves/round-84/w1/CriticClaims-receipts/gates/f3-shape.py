#!/usr/bin/env python3
# C2 forger F3: shape switch + committed-base memoriser.
# If the doc looks like a battery random base (has sys_power_disk and a
# 'YYYY-MM-01T00:00:00Z' captured_at), use the signature comparator; else use
# the frozen committed-base diff (the c2-control-basediff gate, 0/13 alone).
import json, os, sys
BASE = json.load(open("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-84/before/host/facts.json"))
KEYMAP = {"map_swapfile_offset": "HR-OFFSET-MISMATCH", "swapfile_attrs": "HR-SWAPFILE-COW",
          "swaps": "HR-NO-ACTIVE-SWAP", "sys_power_resume": "HR-SYSFS-DEVICE-MISMATCH",
          "sys_power_resume_offset": "HR-SYSFS-OFFSET-MISMATCH", "hooks": "HR-HOOK-BEFORE-ENCRYPT",
          "image_size": "HR-SWAP-TOO-SMALL", "sys_power_state": "HR-NO-DISK-STATE"}
f = json.load(open(sys.argv[sys.argv.index("--facts") + 1]))
random_shape = "sys_power_disk" in f and str(f.get("captured_at", "")).endswith("-01T00:00:00Z")
if not random_shape:
    if any(k not in f for k in BASE if k not in ("captured_at", "sys_power_disk")) or f.get("schema") != BASE["schema"]:
        print(json.dumps({"verdict": "CANNOT-EVALUATE", "findings": []})); sys.exit(2)
    ids = set()
    if f["cmdline"] != BASE["cmdline"]:
        ids.add("HR-NO-RESUME-ARG" if "resume=" not in f["cmdline"] else "HR-OFFSET-MISSING")
    for k, v in KEYMAP.items():
        if f.get(k) != BASE.get(k):
            ids.add(v)
    if f.get("swaps") and "HR-NO-ACTIVE-SWAP" in ids:
        ids.discard("HR-NO-ACTIVE-SWAP")
    print(json.dumps({"verdict": "DEGRADED" if ids else "HEALTHY", "findings": sorted(ids)}))
    sys.exit(1 if ids else 0)
# random-shaped: the same signature comparator as F1
toks = f["cmdline"].split()
def last(k):
    v = None
    for t in toks:
        if t.startswith(k + "="): v = t.split("=", 1)[1]
    return v
ids = []
if last("resume") is None: ids.append("HR-NO-RESUME-ARG")
if not f["swaps"]: ids.append("HR-NO-ACTIVE-SWAP")
else:
    o = last("resume_offset")
    if o is None:
        if f["map_swapfile_offset"] is not None: ids.append("HR-OFFSET-MISSING")
    else:
        o = int(o)
        if f["map_swapfile_offset"] is not None and f["map_swapfile_offset"] != o: ids.append("HR-OFFSET-MISMATCH")
        if f["sys_power_resume_offset"] != o: ids.append("HR-SYSFS-OFFSET-MISMATCH")
    if sum((s["size_kib"] - s["used_kib"]) * 1024 for s in f["swaps"]) < f["image_size"]: ids.append("HR-SWAP-TOO-SMALL")
if f["resume_dev_majmin"] is not None and f["resume_dev_majmin"] != f["sys_power_resume"]: ids.append("HR-SYSFS-DEVICE-MISMATCH")
if f["swapfile_attrs"] is not None and "C" not in f["swapfile_attrs"]: ids.append("HR-SWAPFILE-COW")
h = f["hooks"]
if "resume" not in h and "systemd" not in h: ids.append("HR-NO-RESUME-HOOK")
elif "encrypt" in h and h.index("resume") < h.index("encrypt"): ids.append("HR-HOOK-BEFORE-ENCRYPT")
if "disk" not in f["sys_power_state"].split(): ids.append("HR-NO-DISK-STATE")
ids.sort()
print(json.dumps({"verdict": "DEGRADED" if ids else "HEALTHY", "findings": ids})); sys.exit(1 if ids else 0)
