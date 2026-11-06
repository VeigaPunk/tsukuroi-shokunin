#!/usr/bin/env python3
"""Read-only capture of this host's hibernate-resume facts (round 84; lockdown added round 85).

Writes two files into --out DIR:
  receipt.txt  every command, its exit code and its raw output, in order
  facts.json   the resume-facts/2 document the gate reads (resume-facts/1 plus `lockdown`)

Read-only: it reads /proc and /sys, stats device nodes, sources the
mkinitcpio configuration in a child bash to print the effective HOOKS, and
runs `sudo -n` only for three read-only inspection commands
(btrfs inspect-internal map-swapfile -r, lsattr, filefrag -v). It never
writes /sys, never swaps on/off and never hibernates. No temp files.

Usage: capture-resume-facts-r84.py --out DIR
"""
import argparse
import datetime
import json
import os
import subprocess
import sys

SCHEMA = "resume-facts/2"
ENV = {"PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "LC_ALL": "C", "LANG": "C"}


def run(argv):
    try:
        p = subprocess.run(argv, capture_output=True, text=True, env=ENV, timeout=30)
        return p.returncode, p.stdout, p.stderr
    except (OSError, subprocess.TimeoutExpired) as e:
        return 127, "", str(e)


def read(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return 0, fh.read(), ""
    except OSError as e:
        return 1, "", str(e)


HOOKS_SH = (
    'source /etc/mkinitcpio.conf; '
    'for f in /etc/mkinitcpio.conf.d/*.conf; do [ -e "$f" ] && source "$f"; done; '
    'printf "%s\\n" "${HOOKS[@]}"'
)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    os.makedirs(a.out, exist_ok=True)
    log = []

    def rec(label, rc, out, err):
        log.append(f"### {label}\nrc={rc}\n{out}{('[stderr] ' + err) if err else ''}\n")
        return out

    stamp = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat(timespec="seconds")
    log.append(f"# resume-facts capture {stamp}\n")
    cmdline = rec("cat /proc/cmdline", *read("/proc/cmdline")).strip()
    swaps_raw = rec("cat /proc/swaps", *read("/proc/swaps"))
    swaps = []
    for line in swaps_raw.splitlines()[1:]:
        f = line.split()
        if len(f) >= 4:
            swaps.append({"path": f[0], "type": f[1], "size_kib": int(f[2]), "used_kib": int(f[3])})
    swapfile = next((s["path"] for s in swaps if s["type"] == "file"), None)
    mapoff = attrs = None
    if swapfile:
        rc, out, err = run(["sudo", "-n", "btrfs", "inspect-internal", "map-swapfile", "-r", swapfile])
        rec(f"sudo -n btrfs inspect-internal map-swapfile -r {swapfile}", rc, out, err)
        mapoff = int(out.strip()) if rc == 0 and out.strip().isdigit() else None
        rc, out, err = run(["sudo", "-n", "lsattr", swapfile])
        rec(f"sudo -n lsattr {swapfile}", rc, out, err)
        attrs = out.split()[0] if rc == 0 and out.split() else None
        rec(f"sudo -n filefrag -v {swapfile}", *run(["sudo", "-n", "filefrag", "-v", swapfile]))
        rec(f"stat -c '%W %i %s' {swapfile}", *run(["stat", "-c", "%W %i %s", swapfile]))
    # Boot words as the kernel sees them: parse_args() stops at a bare `--` (kernel/params.c
    # v7.2 raw 182-183), the last `resume=` wins (kernel/power/hibernate.c raw 1402-1409), and
    # next_arg()/repair_env_string() strip the quotes (lib/cmdline.c raw 237-284, init/main.c
    # raw 463-476), so `resume=""` leaves an empty resume_file (hibernate.c raw 984).
    words = cmdline.split()
    if "--" in words:
        words = words[:words.index("--")]
    resume = None
    for t in words:
        if t.startswith("resume="):
            resume = t.split("=", 1)[1]
            if resume.startswith('"'):
                resume = resume[:-1] if resume.endswith('"') and len(resume) > 1 else resume[1:]
    devmm = None
    if resume and resume.startswith("/dev/"):
        rc, out, err = run(["stat", "-L", "-c", "%t %T", resume])
        rec(f"stat -L -c '%t %T' {resume}", rc, out, err)
        if rc == 0 and len(out.split()) == 2:
            ma, mi = out.split()
            devmm = f"{int(ma, 16)}:{int(mi, 16)}"
    sysres = rec("cat /sys/power/resume", *read("/sys/power/resume")).strip()
    sysoff = rec("cat /sys/power/resume_offset", *read("/sys/power/resume_offset")).strip()
    state = rec("cat /sys/power/state", *read("/sys/power/state")).strip()
    disk = rec("cat /sys/power/disk", *read("/sys/power/disk")).strip()
    img = rec("cat /sys/power/image_size", *read("/sys/power/image_size")).strip()
    hooks = rec("bash -c <source mkinitcpio.conf + conf.d; print HOOKS>",
                *run(["bash", "-c", HOOKS_SH])).split()
    rec("systemctl --version", *run(["systemctl", "--version"]))
    # round 85: hibernation availability (kernel lockdown). An absent securityfs file means the
    # lockdown LSM is not present; that is recorded as rc 0 "absent", not as a failed probe.
    lockdown = None
    if os.path.exists("/sys/kernel/security/lockdown"):
        lockdown = rec("cat /sys/kernel/security/lockdown", *read("/sys/kernel/security/lockdown")).strip() or None
    else:
        rec("test -e /sys/kernel/security/lockdown", 0, "absent\n", "")
    facts = {
        "schema": SCHEMA,
        "captured_at": stamp,
        "cmdline": cmdline,
        "swaps": swaps,
        "resume_swapfile": swapfile,
        "map_swapfile_offset": mapoff,
        "swapfile_attrs": attrs,
        "resume_dev_majmin": devmm,
        "sys_power_resume": sysres,
        "sys_power_resume_offset": int(sysoff) if sysoff.isdigit() else -1,
        "sys_power_state": state,
        "sys_power_disk": disk,
        "image_size": int(img) if img.isdigit() else -1,
        "hooks": hooks,
        "lockdown": lockdown,
    }
    with open(os.path.join(a.out, "receipt.txt"), "w", encoding="utf-8") as fh:
        fh.write("".join(log))
    with open(os.path.join(a.out, "facts.json"), "w", encoding="utf-8") as fh:
        json.dump(facts, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps(facts, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
