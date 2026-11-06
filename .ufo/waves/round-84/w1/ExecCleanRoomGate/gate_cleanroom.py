#!/usr/bin/env python3
"""Clean-room round-84 hibernate-resume gate (seat ExecCleanRoomGate).

Written from ONLY the frozen rule text in the docstring of
tools/resume-gate-battery-r84.py (lines 1-40) and the round-84 declaration in
SCORECARD.md.  The candidate tools/check-hibernate-resume.py was not read
before this file was first written.

Interface: gate_cleanroom.py --facts FILE
  stdout: one JSON object {"verdict": ..., "findings": [...]}
  exit 0 HEALTHY / 1 DEGRADED / 2 CANNOT-EVALUATE
  --live: run tools/capture-resume-facts-r84.py (cwd-relative) into a scratch
          dir and gate the produced facts document (interface parity with the
          frozen C2 declaration).
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

SCHEMA = "resume-facts/1"
REQUIRED = ["schema", "cmdline", "swaps", "resume_swapfile", "map_swapfile_offset",
            "swapfile_attrs", "resume_dev_majmin", "sys_power_resume",
            "sys_power_resume_offset", "sys_power_state", "image_size", "hooks"]


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def is_str(v):
    return isinstance(v, str)


def opt_str(v):
    return v is None or isinstance(v, str)


def opt_int(v):
    return v is None or is_int(v)


def valid_swaps(v):
    if not isinstance(v, list):
        return False
    for s in v:
        if not isinstance(s, dict):
            return False
        # rule 7 needs numeric size/used; a non-numeric one is a wrong type
        if not is_int(s.get("size_kib")) or not is_int(s.get("used_kib")):
            return False
    return True


TYPE_CHECK = {
    "schema": is_str,
    "cmdline": is_str,
    "swaps": valid_swaps,
    "resume_swapfile": opt_str,
    "map_swapfile_offset": opt_int,
    "swapfile_attrs": opt_str,
    "resume_dev_majmin": opt_str,
    "sys_power_resume": opt_str,
    "sys_power_resume_offset": opt_int,
    "sys_power_state": is_str,
    "image_size": is_int,
    "hooks": lambda v: isinstance(v, list) and all(isinstance(h, str) for h in v),
}


def token_value(cmdline, key):
    """First `key=value` token on the cmdline, else None (the declared
    singular value; duplicates are first-wins, matching the battery helper)."""
    for t in cmdline.split():
        if t.startswith(key + "="):
            return t.split("=", 1)[1]
    return None


def offset(cmdline):
    v = token_value(cmdline, "resume_offset")
    if v is None:
        return None
    return int(v)  # ValueError -> handled by the caller as a malformed value


def evaluate(f):
    """Return (verdict, findings) for a structurally valid document."""
    r_raw = token_value(f["cmdline"], "resume")
    # rule 1: r is None -> exactly [HR-NO-RESUME-ARG]; nothing else evaluated
    if r_raw is None:
        return "DEGRADED", ["HR-NO-RESUME-ARG"]

    try:
        o = offset(f["cmdline"])
    except ValueError:
        return "CANNOT-EVALUATE", []
    found = []

    # rule 2: active file-type swap
    if f["resume_swapfile"] is not None:
        if o is None:
            found.append("HR-OFFSET-MISSING")
        elif f["map_swapfile_offset"] is not None and o != f["map_swapfile_offset"]:
            found.append("HR-OFFSET-MISMATCH")
        if f["swapfile_attrs"] is not None and "C" not in f["swapfile_attrs"]:
            found.append("HR-SWAPFILE-COW")
    if not f["swaps"]:
        found.append("HR-NO-ACTIVE-SWAP")

    # rule 3
    if f["resume_dev_majmin"] is not None and f["resume_dev_majmin"] != f["sys_power_resume"]:
        found.append("HR-SYSFS-DEVICE-MISMATCH")
    # rule 4
    if o is not None and o != f["sys_power_resume_offset"]:
        found.append("HR-SYSFS-OFFSET-MISMATCH")
    # rule 5
    hooks = f["hooks"]
    if "resume" not in hooks and "systemd" not in hooks:
        found.append("HR-NO-RESUME-HOOK")
    # rule 6
    if "resume" in hooks and "encrypt" in hooks and hooks.index("resume") < hooks.index("encrypt"):
        found.append("HR-HOOK-BEFORE-ENCRYPT")
    # rule 7
    if f["swaps"]:
        free = sum((s["size_kib"] - s["used_kib"]) * 1024 for s in f["swaps"])
        if free < f["image_size"]:
            found.append("HR-SWAP-TOO-SMALL")
    # rule 8
    if "disk" not in f["sys_power_state"].split():
        found.append("HR-NO-DISK-STATE")

    return ("DEGRADED", sorted(set(found))) if found else ("HEALTHY", [])


def gate(f):
    if not isinstance(f, dict):
        return "CANNOT-EVALUATE", []
    if any(k not in f for k in REQUIRED):
        return "CANNOT-EVALUATE", []
    if f.get("schema") != SCHEMA:
        return "CANNOT-EVALUATE", []
    for k, check in TYPE_CHECK.items():
        try:
            ok = check(f[k])
        except Exception:  # noqa: BLE001 - a checker must never crash the gate
            ok = False
        if not ok:
            return "CANNOT-EVALUATE", []
    return evaluate(f)


def live_facts():
    """Run the frozen capture tool from the cwd-relative repo root."""
    out = tempfile.mkdtemp(prefix="r84-live-")
    try:
        p = subprocess.run([sys.executable, os.path.join("tools", "capture-resume-facts-r84.py"),
                            "--out", out], capture_output=True, text=True, timeout=120)
        if p.returncode != 0:
            return None
        with open(os.path.join(out, "facts.json"), encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:  # noqa: BLE001
        return None
    finally:
        shutil.rmtree(out, ignore_errors=True)


def main(argv=None):
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--facts")
    g.add_argument("--live", action="store_true")
    a = ap.parse_args(argv)
    if a.live:
        facts = live_facts()
        if facts is None:
            print(json.dumps({"verdict": "CANNOT-EVALUATE", "findings": []}))
            return 2
    else:
        try:
            with open(a.facts, encoding="utf-8") as fh:
                facts = json.load(fh)
        except Exception:  # noqa: BLE001
            print(json.dumps({"verdict": "CANNOT-EVALUATE", "findings": []}))
            return 2
    verdict, findings = gate(facts)
    print(json.dumps({"verdict": verdict, "findings": sorted(findings)}))
    return {"HEALTHY": 0, "DEGRADED": 1, "CANNOT-EVALUATE": 2}[verdict]


if __name__ == "__main__":
    sys.exit(main())
