#!/usr/bin/env python3
"""FORGER S2 (MutBattery r85 w1): committed-host-base diff memoriser.

Reads the frozen host base .ufo/waves/round-85/before/host/facts-v2.json and classifies an
incoming document by WHICH field differs from it, mapping the changed witness to the expected
finding. It never evaluates a rule relative to the document (no free-swap arithmetic, no
threshold, no last-token parse): it knows the committed base is HEALTHY, so any delta is a
fault. Works only while every battery case is drawn from that one committed base -- i.e. only
when the random bases are removed (mutant B2)."""
import json, re, sys

BASE = ".ufo/waves/round-85/before/host/facts-v2.json"
BENIGN = re.compile(r"^(hibernate=nocompress|hibernate\.compressor=.+|resumewait|.+\."
                    r"(noresume|nohibernate)=1)$")


def die():
    print(json.dumps({"verdict": "CANNOT-EVALUATE", "findings": []}))
    sys.exit(2)


def done(ids):
    ids = sorted(set(ids))
    if ids:
        print(json.dumps({"verdict": "DEGRADED", "findings": ids}))
        sys.exit(1)
    print(json.dumps({"verdict": "HEALTHY", "findings": []}))
    sys.exit(0)


def valid(f):
    if not isinstance(f, dict) or f.get("schema") != "resume-facts/2":
        return False
    for k, t in (("cmdline", str), ("swaps", list), ("resume_dev_majmin", str),
                 ("sys_power_resume", str), ("sys_power_resume_offset", int),
                 ("sys_power_state", str), ("image_size", int), ("hooks", list)):
        if k not in f or isinstance(f[k], bool) or not isinstance(f[k], t):
            return False
    for k, t in (("resume_swapfile", str), ("map_swapfile_offset", int), ("swapfile_attrs", str),
                 ("lockdown", str)):
        if k not in f or not (f[k] is None or (not isinstance(f[k], bool) and isinstance(f[k], t))):
            return False
    for s in f["swaps"]:
        if not isinstance(s, dict):
            return False
        for k in ("size_kib", "used_kib"):
            if isinstance(s.get(k), bool) or not isinstance(s.get(k), int):
                return False
    if not all(isinstance(h, str) for h in f["hooks"]):
        return False
    if f["lockdown"] is not None:
        sel = [w for w in f["lockdown"].split() if len(w) > 2 and w[0] == "[" and w[-1] == "]"]
        if len(sel) != 1:
            return False
    return True


def main():
    f = json.load(open(sys.argv[sys.argv.index("--facts") + 1], encoding="utf-8"))
    b = json.load(open(BASE, encoding="utf-8"))
    if not valid(f):
        die()
    ids = []
    ft = f["cmdline"].split()
    bt = b["cmdline"].split()
    added = [t for t in ft if t not in bt]
    hib = nor = False
    for t in added:
        if BENIGN.match(t):
            continue
        if t in ("nohibernate", "hibernate=no"):
            hib = True
        elif t in ("noresume", "hibernate=noresume"):
            nor = True
        elif t.startswith("hibernate="):
            v = t.split("=", 1)[1]
            if v.startswith("noresume"):
                nor = True
            elif v.startswith("no"):
                hib = True
    if hib:
        ids.append("HR-HIBERNATE-DISABLED")
    elif nor:
        ids.append("HR-NORESUME-ARG")
    if f["lockdown"] != b["lockdown"]:
        modes = [w[1:-1] for w in f["lockdown"].split() if w.startswith("[")]
        if modes and modes[0] in ("integrity", "confidentiality"):
            ids.append("HR-LOCKDOWN-BLOCKS")
    if not any(t.startswith("resume=") for t in ft):
        done(ids + ["HR-NO-RESUME-ARG"])
    if not any(t.startswith("resume_offset=") for t in ft) and f["resume_swapfile"] is not None:
        ids.append("HR-OFFSET-MISSING")
    if (f["resume_swapfile"] is not None and f["map_swapfile_offset"] is not None
            and f["map_swapfile_offset"] != b["map_swapfile_offset"]):
        ids.append("HR-OFFSET-MISMATCH")
    if f["swapfile_attrs"] is not None and f["swapfile_attrs"] != b["swapfile_attrs"]:
        ids.append("HR-SWAPFILE-COW")
    if not f["swaps"] and b["swaps"]:
        ids.append("HR-NO-ACTIVE-SWAP")
    if f["sys_power_resume"] != b["sys_power_resume"]:
        ids.append("HR-SYSFS-DEVICE-MISMATCH")
    if f["sys_power_resume_offset"] != b["sys_power_resume_offset"]:
        ids.append("HR-SYSFS-OFFSET-MISMATCH")
    if f["hooks"] != b["hooks"]:
        if "resume" not in f["hooks"] and "systemd" not in f["hooks"]:
            ids.append("HR-NO-RESUME-HOOK")
        elif ("resume" in f["hooks"] and "encrypt" in f["hooks"]
              and f["hooks"].index("resume") < f["hooks"].index("encrypt")):
            ids.append("HR-HOOK-BEFORE-ENCRYPT")
    if f["image_size"] != b["image_size"]:
        ids.append("HR-SWAP-TOO-SMALL")
    if f["sys_power_state"] != b["sys_power_state"]:
        ids.append("HR-NO-DISK-STATE")
    done(ids)


if __name__ == "__main__":
    main()
