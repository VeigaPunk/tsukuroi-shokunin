#!/usr/bin/env python3
"""Clean-room gate for the frozen resume-facts/2 rule set (round-85 C2).

Written only from the docstring of tools/resume-gate-battery-r85.py.
CLI: cleanroom-gate.py --facts FILE  -> one JSON object on stdout,
rc 0 HEALTHY / 1 DEGRADED / 2 CANNOT-EVALUATE.
"""
import argparse
import json
import re
import sys

SCHEMA = "resume-facts/2"
BRACKET = re.compile(r"\[[^\[\]]+\]")
DIGITS = re.compile(r"[0-9]+")

HIB_DISABLED = "HR-HIBERNATE-DISABLED"
LOCKDOWN_BLOCKS = "HR-LOCKDOWN-BLOCKS"
NORESUME_ARG = "HR-NORESUME-ARG"
NO_RESUME_ARG = "HR-NO-RESUME-ARG"
OFFSET_MISSING = "HR-OFFSET-MISSING"
OFFSET_MISMATCH = "HR-OFFSET-MISMATCH"
SWAPFILE_COW = "HR-SWAPFILE-COW"
NO_ACTIVE_SWAP = "HR-NO-ACTIVE-SWAP"
SYSFS_DEVICE = "HR-SYSFS-DEVICE-MISMATCH"
SYSFS_OFFSET = "HR-SYSFS-OFFSET-MISMATCH"
NO_RESUME_HOOK = "HR-NO-RESUME-HOOK"
HOOK_BEFORE_ENCRYPT = "HR-HOOK-BEFORE-ENCRYPT"
SWAP_TOO_SMALL = "HR-SWAP-TOO-SMALL"
NO_DISK_STATE = "HR-NO-DISK-STATE"


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def is_str(v):
    return isinstance(v, str)


def is_opt_str(v):
    return v is None or is_str(v)


def is_opt_int(v):
    return v is None or is_int(v)


def swap_ok(s):
    return (isinstance(s, dict)
            and is_str(s.get("path"))
            and is_str(s.get("type"))
            and is_int(s.get("size_kib"))
            and is_int(s.get("used_kib")))


def valid(f):
    """Schema / required keys / round-84 types; lockdown str or null, one [x] word."""
    if not isinstance(f, dict):
        return False
    if f.get("schema") != SCHEMA:
        return False
    checks = (
        ("cmdline", is_str),
        ("swaps", lambda v: isinstance(v, list) and all(swap_ok(s) for s in v)),
        ("resume_swapfile", is_opt_str),
        ("map_swapfile_offset", is_opt_int),
        ("swapfile_attrs", is_opt_str),
        ("resume_dev_majmin", is_opt_str),
        ("sys_power_resume", is_opt_str),
        ("sys_power_resume_offset", is_opt_int),
        ("sys_power_state", is_str),
        ("image_size", is_int),
        ("hooks", lambda v: isinstance(v, list) and all(is_str(h) for h in v)),
        ("lockdown", is_opt_str),
    )
    for key, check in checks:
        if key not in f or not check(f[key]):
            return False
    lock = f["lockdown"]
    if lock is not None:
        words = lock.split()
        if sum(1 for w in words if BRACKET.fullmatch(w)) != 1:
            return False
    return True


def hibernate_values(tokens):
    return [t[len("hibernate="):] for t in tokens if t.startswith("hibernate=")]


def evaluate(f):
    tokens = f["cmdline"].split()

    # o: value of the last resume_offset= token; r: value of the last resume= token.
    o = None
    r = None
    for t in tokens:
        if t.startswith("resume_offset="):
            v = t.split("=", 1)[1]
            if DIGITS.fullmatch(v):
                o = int(v)
        elif t.startswith("resume="):
            r = t.split("=", 1)[1]

    findings = set()

    # A1
    a1 = any(t == "nohibernate" for t in tokens)
    if not a1:
        for v in hibernate_values(tokens):
            if v.startswith("no") and not v.startswith("noresume") and not v.startswith("nocompress"):
                a1 = True
                break
    if a1:
        findings.add(HIB_DISABLED)

    # A2
    if f["lockdown"] is not None:
        m = BRACKET.search(f["lockdown"])
        if m and m.group(0)[1:-1] in ("integrity", "confidentiality"):
            findings.add(LOCKDOWN_BLOCKS)

    # A3 (suppressed when A1 fired: nohibernate implies noresume)
    if not a1:
        a3 = any(t == "noresume" for t in tokens) or any(
            v.startswith("noresume") for v in hibernate_values(tokens))
        if a3:
            findings.add(NORESUME_ARG)

    # Rule 1: no resume= token -> no resume chain evaluation.
    if r is None:
        findings.add(NO_RESUME_ARG)
    else:
        # Rule 2
        if not f["swaps"]:
            findings.add(NO_ACTIVE_SWAP)
        if f["resume_swapfile"] is not None:
            if o is None:
                findings.add(OFFSET_MISSING)
            if o is not None and f["map_swapfile_offset"] is not None \
                    and o != f["map_swapfile_offset"]:
                findings.add(OFFSET_MISMATCH)
            if f["swapfile_attrs"] is not None and "C" not in f["swapfile_attrs"]:
                findings.add(SWAPFILE_COW)
        # Rule 3
        if f["resume_dev_majmin"] is not None \
                and f["resume_dev_majmin"] != f["sys_power_resume"]:
            findings.add(SYSFS_DEVICE)
        # Rule 4
        if o is not None and o != f["sys_power_resume_offset"]:
            findings.add(SYSFS_OFFSET)
        hooks = f["hooks"]
        # Rule 5
        if "resume" not in hooks and "systemd" not in hooks:
            findings.add(NO_RESUME_HOOK)
        # Rule 6
        if "resume" in hooks and "encrypt" in hooks \
                and hooks.index("resume") < hooks.index("encrypt"):
            findings.add(HOOK_BEFORE_ENCRYPT)
        # Rule 7
        if f["swaps"]:
            free = sum((s["size_kib"] - s["used_kib"]) * 1024 for s in f["swaps"])
            if free < f["image_size"]:
                findings.add(SWAP_TOO_SMALL)
        # Rule 8
        if "disk" not in f["sys_power_state"].split():
            findings.add(NO_DISK_STATE)

    return sorted(findings)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--facts", required=True)
    args = ap.parse_args()
    try:
        with open(args.facts, "r", encoding="utf-8") as fh:
            doc = json.load(fh)
    except (OSError, ValueError):
        doc = None
    if not valid(doc):
        print(json.dumps({"verdict": "CANNOT-EVALUATE", "findings": []}))
        return 2
    findings = evaluate(doc)
    if findings:
        print(json.dumps({"verdict": "DEGRADED", "findings": findings}))
        return 1
    print(json.dumps({"verdict": "HEALTHY", "findings": []}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
