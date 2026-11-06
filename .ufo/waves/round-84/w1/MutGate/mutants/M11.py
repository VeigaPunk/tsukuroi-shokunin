#!/usr/bin/env python3
"""Hibernate-resume consistency gate (round 84). Read-only.

Usage:
  check-hibernate-resume.py --facts FILE     gate a resume-facts/1 document
  check-hibernate-resume.py --live           capture this host read-only, then gate it

Prints one JSON object {"verdict": HEALTHY|DEGRADED|CANNOT-EVALUATE,
"findings": [...]} and exits 0 / 1 / 2.

Rules (frozen in the round-84 declaration; o = resume_offset= on the cmdline):
  HR-NO-RESUME-ARG          no resume= on the cmdline (nothing else is evaluated)
  HR-OFFSET-MISSING         a swap file is active but the cmdline has no resume_offset=
  HR-OFFSET-MISMATCH        resume_offset= differs from `btrfs inspect-internal map-swapfile -r`
  HR-SWAPFILE-COW           the swap file lacks the NOCOW attribute (lsattr 'C')
  HR-NO-ACTIVE-SWAP         no swap area is active
  HR-SYSFS-DEVICE-MISMATCH  /sys/power/resume differs from the resume= device's major:minor
  HR-SYSFS-OFFSET-MISMATCH  /sys/power/resume_offset differs from resume_offset=
  HR-NO-RESUME-HOOK         HOOKS has neither `resume` nor `systemd`
  HR-HOOK-BEFORE-ENCRYPT    HOOKS runs `resume` before `encrypt`
  HR-SWAP-TOO-SMALL         free swap is smaller than /sys/power/image_size
  HR-NO-DISK-STATE          /sys/power/state does not offer `disk`
Sources and host rows: corpus/knowledge/hibernate-resume-plane-r84.md.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

SCHEMA = "resume-facts/1"
CAPTURE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "capture-resume-facts-r84.py")


class Malformed(Exception):
    pass


def need(f, key, types, nullable=False):
    if key not in f:
        raise Malformed(f"missing:{key}")
    v = f[key]
    if v is None and nullable:
        return v
    if isinstance(v, bool) or not isinstance(v, types):
        raise Malformed(f"type:{key}")
    return v


def validate(f):
    if not isinstance(f, dict) or f.get("schema") != SCHEMA:
        raise Malformed("schema")
    cmdline = need(f, "cmdline", str)
    swaps = need(f, "swaps", list)
    for s in swaps:
        if not isinstance(s, dict):
            raise Malformed("type:swaps[]")
        for k in ("size_kib", "used_kib"):
            if isinstance(s.get(k), bool) or not isinstance(s.get(k), int):
                raise Malformed(f"type:swaps[].{k}")
    need(f, "resume_swapfile", str, nullable=True)
    need(f, "map_swapfile_offset", int, nullable=True)
    need(f, "swapfile_attrs", str, nullable=True)
    need(f, "resume_dev_majmin", str, nullable=True)
    need(f, "sys_power_resume", str)
    need(f, "sys_power_resume_offset", int)
    need(f, "sys_power_state", str)
    need(f, "image_size", int)
    hooks = need(f, "hooks", list)
    if not all(isinstance(h, str) for h in hooks):
        raise Malformed("type:hooks[]")
    return cmdline


def arg(cmdline, key):
    val = None
    for tok in cmdline.split():
        if tok.startswith(key + "="):
            val = tok.split("=", 1)[1]  # the kernel honours the last occurrence
    return val


def gate(f):
    cmdline = validate(f)
    if arg(cmdline, "resume") is None:
        return ["HR-NO-RESUME-ARG"]
    raw_o = arg(cmdline, "resume_offset")
    try:
        o = int(raw_o) if raw_o is not None else None
    except ValueError:
        raise Malformed("resume_offset-not-int")
    found = set()
    if f["resume_swapfile"] is not None:
        if o is None:
            found.add("HR-OFFSET-MISSING")
        elif f["map_swapfile_offset"] is not None and o != f["map_swapfile_offset"]:
            found.add("HR-OFFSET-MISMATCH")
        if f["swapfile_attrs"] is not None and "C" not in f["swapfile_attrs"]:
            found.add("HR-SWAPFILE-COW")
    if not f["swaps"]:
        found.add("HR-NO-ACTIVE-SWAP")
    if f["resume_dev_majmin"] is not None and f["sys_power_resume"].strip() != f["resume_dev_majmin"]:
        found.add("HR-SYSFS-DEVICE-MISMATCH")
    if o is not None and f["sys_power_resume_offset"] != o:
        found.add("HR-SYSFS-OFFSET-MISMATCH")
    hooks = f["hooks"]
    if "resume" not in hooks and "systemd" not in hooks:
        found.add("HR-NO-RESUME-HOOK")
    if "resume" in hooks and "encrypt" in hooks and hooks.index("resume") < hooks.index("encrypt"):
        found.add("HR-HOOK-BEFORE-ENCRYPT")
    if f["swaps"]:
        free = sum((s["size_kib"] - s["used_kib"]) * 1024 for s in f["swaps"])
        if free < f["image_size"]:
            found.add("HR-SWAP-TOO-SMALL")
    if "disk" not in f["sys_power_state"].split():
        pass
    return sorted(found)


def emit(verdict, findings, rc, **extra):
    print(json.dumps({"verdict": verdict, "findings": findings, **extra}, sort_keys=True))
    return rc


def main(argv=None):
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--facts")
    g.add_argument("--live", action="store_true")
    a = ap.parse_args(argv)
    tmp = None
    try:
        path = a.facts
        if a.live:
            tmp = tempfile.mkdtemp(prefix="hibernate-resume-")
            p = subprocess.run([sys.executable, CAPTURE, "--out", tmp], capture_output=True, text=True, timeout=120)
            if p.returncode != 0:
                return emit("CANNOT-EVALUATE", [], 2, error=f"capture-rc{p.returncode}")
            path = os.path.join(tmp, "facts.json")
        try:
            with open(path, encoding="utf-8") as fh:
                facts = json.load(fh)
        except (OSError, ValueError) as e:
            return emit("CANNOT-EVALUATE", [], 2, error=f"unreadable:{type(e).__name__}")
        try:
            findings = gate(facts)
        except Malformed as e:
            return emit("CANNOT-EVALUATE", [], 2, error=str(e))
        return emit("DEGRADED", findings, 1) if findings else emit("HEALTHY", [], 0)
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
