#!/usr/bin/env python3
"""Hibernate gate: availability (round 85), resume chain (round 84), kernel token parse (round 86). Read-only.

Usage:
  check-hibernate-resume.py --facts FILE     gate a resume-facts/2 document
  check-hibernate-resume.py --live           capture this host read-only, then gate it
  check-hibernate-resume.py --selftest       run the gate on itself over built-in fixtures (rc + finding IDs)

Prints one JSON object {"verdict": HEALTHY|DEGRADED|CANNOT-EVALUATE,
"findings": [...]} and exits 0 / 1 / 2.

Availability rules (round-85 declaration; Linux v7.2 kernel/power/hibernate.c hibernate_setup,
noresume_setup, nohibernate_setup, hibernation_available; include/linux/security.h
enum lockdown_reason; security/lockdown/lockdown.c), always evaluated:
  HR-HIBERNATE-DISABLED     a `nohibernate` token, or `hibernate=V` with V starting `no` but
                            not `noresume`/`nocompress` (the kernel tests those prefixes first)
  HR-LOCKDOWN-BLOCKS        /sys/kernel/security/lockdown selects `integrity` or
                            `confidentiality` (LOCKDOWN_HIBERNATION < LOCKDOWN_INTEGRITY_MAX)
  HR-NORESUME-ARG           a `noresume` token or `hibernate=noresume...`, unless
                            HR-HIBERNATE-DISABLED fired (nohibernate already sets noresume)
Resume-chain rules (round-84 declaration; o = resume_offset= on the cmdline):
  HR-NO-RESUME-ARG          no resume= on the cmdline (no other resume-chain rule is evaluated)
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
Token parse (round-86 declaration; Linux v7.2 init/main.c obsolete_checksetup raw 201-228, kernel/params.c
parameqn raw 86-95, kernel/power/hibernate.c raw 1402-1465): a token selects a boot option when its first
len(option) characters equal the option with '-' read as '_'; `noresume` and `nohibernate` ignore the rest of the
token (`noresume=1` counts), the last `resume=` / `resume_offset=` wins, an empty `resume=` means no resume
device, and a `resume_offset=` whose value has no leading decimal digit is skipped (sscanf "%llu").
Sources and host rows: corpus/knowledge/hibernate-resume-plane-r84.md (resume chain) and
corpus/knowledge/hibernation-availability-r85.md (availability), corpus/knowledge/hibernation-boot-parse-r86.md (parse).
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

SCHEMA = "resume-facts/2"
LOCKDOWN_BLOCKING = ("integrity", "confidentiality")
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
    lockdown = need(f, "lockdown", str, nullable=True)
    if lockdown is not None:
        selected = [w for w in lockdown.split() if len(w) > 2 and w[0] == "[" and w[-1] == "]"]
        if len(selected) != 1:
            raise Malformed("lockdown-selection")
    return cmdline


def lockdown_mode(lockdown):
    if lockdown is None:
        return None
    return next(w[1:-1] for w in lockdown.split() if len(w) > 2 and w[0] == "[" and w[-1] == "]")


def matches(tok, setup):
    """obsolete_checksetup: the first len(setup) characters equal setup, '-' read as '_' (parameqn)."""
    n = len(setup)
    return len(tok) >= n and tok[:n].replace("-", "_") == setup.replace("-", "_")


def availability(cmdline, lockdown):
    """Findings of hibernation_available() and the noresume switch, parsed as the kernel does."""
    disabled = noresume = False
    for tok in cmdline.split():
        if matches(tok, "nohibernate"):
            disabled = True  # nohibernate_setup ignores its argument
        elif matches(tok, "noresume"):
            noresume = True  # noresume_setup ignores its argument
        elif matches(tok, "hibernate="):
            v = tok[len("hibernate="):]
            if v.startswith("noresume"):
                noresume = True
            elif v.startswith("nocompress"):
                pass
            elif v.startswith("no"):
                disabled = True
    found = set()
    if disabled:
        found.add("HR-HIBERNATE-DISABLED")
    elif noresume:
        found.add("HR-NORESUME-ARG")
    if lockdown_mode(lockdown) in LOCKDOWN_BLOCKING:
        found.add("HR-LOCKDOWN-BLOCKS")
    return found


def arg(cmdline, setup):
    """Rest of the last token matching setup (each matching token overwrites; the kernel keeps the last)."""
    val = None
    for tok in cmdline.split():
        if matches(tok, setup):
            val = tok[len(setup):]
    return val


def resume_offset(cmdline):
    """resume_offset_setup: sscanf("%llu") needs a leading decimal digit; otherwise the value is kept."""
    val = None
    for tok in cmdline.split():
        if matches(tok, "resume_offset="):
            rest = tok[len("resume_offset="):]
            digits = len(rest) - len(rest.lstrip("0123456789"))
            if digits:
                val = int(rest[:digits])
    return val


def gate(f):
    cmdline = validate(f)
    found = availability(cmdline, f["lockdown"])
    if not arg(cmdline, "resume="):  # absent, or empty: resume_file stays "" and find_resume_device fails
        return sorted(found | {"HR-NO-RESUME-ARG"})
    o = resume_offset(cmdline)
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
        found.add("HR-NO-DISK-STATE")
    return sorted(found)


def emit(verdict, findings, rc, **extra):
    print(json.dumps({"verdict": verdict, "findings": findings, **extra}, sort_keys=True))
    return rc


def failed_probes(receipt):
    """Labels of capture probes whose recorded rc is not 0 (receipt `### label` then `rc=N`)."""
    failed, label = [], None
    try:
        with open(receipt, encoding="utf-8") as fh:
            for line in fh:
                if line.startswith("### "):
                    label = line[4:].strip()
                elif label is not None and line.startswith("rc="):
                    if line.strip() != "rc=0":
                        failed.append(label)
                    label = None
    except OSError:
        return ["receipt-unreadable"]
    return failed


SELFTEST_BASE = {
    "schema": SCHEMA, "cmdline": "quiet resume=/dev/mapper/root resume_offset=4096 rw",
    "swaps": [{"path": "/swap/swapfile", "type": "file", "size_kib": 8388608, "used_kib": 0}],
    "resume_swapfile": "/swap/swapfile", "map_swapfile_offset": 4096, "swapfile_attrs": "---------------C------",
    "resume_dev_majmin": "254:0", "sys_power_resume": "254:0", "sys_power_resume_offset": 4096,
    "sys_power_state": "freeze mem disk", "image_size": 1024, "hooks": ["base", "udev", "encrypt", "resume"],
    "lockdown": "[none] integrity confidentiality",
}
SELFTEST_CASES = [
    # (name, cmdline or None, field overrides, expected rc, expected findings)
    ("positive", None, {}, 0, []),
    ("noresume-valued", "noresume=0 quiet resume=/dev/mapper/root resume_offset=4096", {}, 1, ["HR-NORESUME-ARG"]),
    ("nohibernate-valued", "quiet nohibernate=1 resume=/dev/mapper/root resume_offset=4096", {}, 1,
     ["HR-HIBERNATE-DISABLED"]),
    ("empty-resume-last", "resume=/dev/mapper/root resume_offset=4096 resume=", {}, 1, ["HR-NO-RESUME-ARG"]),
    ("offset-nondigit-skipped", "resume=/dev/mapper/root resume_offset=4096 resume_offset=abc", {}, 0, []),
    ("offset-dash-digit-prefix", "resume=/dev/mapper/root resume-offset=4096k", {}, 0, []),
    ("offset-last-wins", "resume=/dev/mapper/root resume_offset=4096 resume_offset=8192", {}, 1,
     ["HR-OFFSET-MISMATCH", "HR-SYSFS-OFFSET-MISMATCH"]),
    ("decoys", "noresum no_resume xnoresume nohibernat resume=/dev/mapper/root resume_offset=4096", {}, 0, []),
    ("hibernate-nox", "hibernate=noxyz resume=/dev/mapper/root resume_offset=4096", {}, 1, ["HR-HIBERNATE-DISABLED"]),
    ("boundary-equal", None, {"image_size": 8388608 * 1024}, 0, []),
    ("lockdown-integrity", None, {"lockdown": "none [integrity] confidentiality"}, 1, ["HR-LOCKDOWN-BLOCKS"]),
    ("bool-for-int", None, {"image_size": True}, 2, []),
    ("schema-v1", None, {"schema": "resume-facts/1"}, 2, []),
]


def selftest():
    """Self-invocation: run this file as a subprocess on each fixture; assert rc and the finding IDs."""
    work = tempfile.mkdtemp(prefix="hibernate-resume-selftest-")
    bad = []
    try:
        for name, cmdline, over, want_rc, want in SELFTEST_CASES:
            facts = dict(SELFTEST_BASE, **over)
            if cmdline is not None:
                facts["cmdline"] = cmdline
            path = os.path.join(work, name + ".json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(facts, fh)
            p = subprocess.run([sys.executable, os.path.abspath(__file__), "--facts", path],
                               capture_output=True, text=True, timeout=20)
            try:
                got = json.loads(p.stdout).get("findings")
            except ValueError:
                got = None
            ok = p.returncode == want_rc and got == want
            print(json.dumps({"case": name, "rc": p.returncode, "want_rc": want_rc, "findings": got,
                              "want": want, "pass": ok}, sort_keys=True))
            if not ok:
                bad.append(name)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(json.dumps({"selftest": "PASS" if not bad else "FAIL", "cases": len(SELFTEST_CASES), "failed": bad},
                     sort_keys=True))
    return 0 if not bad else 1


def main(argv=None):
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--facts")
    g.add_argument("--live", action="store_true")
    g.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    tmp = None
    try:
        path = a.facts
        if a.live:
            tmp = tempfile.mkdtemp(prefix="hibernate-resume-")
            p = subprocess.run([sys.executable, CAPTURE, "--out", tmp], capture_output=True, text=True, timeout=120)
            if p.returncode != 0:
                return emit("CANNOT-EVALUATE", [], 2, error=f"capture-rc{p.returncode}")
            failed = failed_probes(os.path.join(tmp, "receipt.txt"))
            if failed:
                # round-84 ReviewGate F1: a failed probe leaves a null/-1 field the rules would read as
                # "not applicable"; the live path fails closed instead of reporting HEALTHY.
                return emit("CANNOT-EVALUATE", [], 2, error="probe-failed", failed=failed)
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
