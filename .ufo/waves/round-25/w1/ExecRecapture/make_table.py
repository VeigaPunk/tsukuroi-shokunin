#!/usr/bin/env python3
"""Render the frozen-vs-recapture comparison as a markdown value-class table."""
import json
import sys

LABEL = {
    "system-memory-psi-read-1|cat-file|/proc/pressure/memory": "system memory PSI, read 1 (`/proc/pressure/memory`)",
    "system-memory-psi-read-2|cat-file|/proc/pressure/memory": "system memory PSI, read 2 (`/proc/pressure/memory`, 10 s later)",
    "system-memory-psi-read-2|date -u +%Y-%m-%dT%H:%M:%SZ": "wall clock at second PSI read",
    "root-cgroup-memory-pressure|cat-file|/sys/fs/cgroup/memory.pressure": "root cgroup `memory.pressure`",
    "user-slice-memory-pressure|cat-file|/sys/fs/cgroup/user.slice/memory.pressure": "`user.slice` `memory.pressure`",
    "user-slice-memory-pressure|cat-file|/sys/fs/cgroup/user.slice/user-1000.slice/memory.pressure": "`user-1000.slice` `memory.pressure`",
    "user-slice-memory-pressure|cat-file|/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/memory.pressure": "`user@1000.service` `memory.pressure`",
    "user-slice-memory-events|cat-file|/sys/fs/cgroup/user.slice/user-1000.slice/memory.events": "`user-1000.slice` `memory.events`",
    "user-slice-memory-events|cat-file|/sys/fs/cgroup/user.slice/user-1000.slice/memory.swap.events": "`user-1000.slice` `memory.swap.events`",
    "kernel-oom-counter|grep|grep -E ^oom_kill  /proc/vmstat": "kernel `oom_kill` counter (`/proc/vmstat`)",
    "swap|grep|grep -E ^(SwapTotal|SwapFree|MemTotal|MemAvailable): /proc/meminfo": "`/proc/meminfo` memory and swap gauges",
    "oomd-unit|is-active|systemd-oomd.service": "`systemctl is-active systemd-oomd.service`",
    "oomd-unit|is-enabled|systemd-oomd.service": "`systemctl is-enabled systemd-oomd.service`",
    "oomd-unit|is-active|systemd-oomd.socket": "`systemctl is-active systemd-oomd.socket`",
    "oomd-unit|is-enabled|systemd-oomd.socket": "`systemctl is-enabled systemd-oomd.socket`",
    "oomd-config|cat-config|systemd/oomd.conf": "`systemd-analyze cat-config systemd/oomd.conf` body",
    "managed-oom-properties|show|user@1000.service": "`systemctl show` ManagedOOM*/MemoryPressure* on `user@1000.service`",
    "managed-oom-properties|show|user-1000.slice": "`systemctl show` ManagedOOM*/MemoryPressure* on `user-1000.slice`",
    "managed-oom-properties|show|user.slice": "`systemctl show` ManagedOOM*/MemoryPressure* on `user.slice`",
    "managed-oom-properties|show|-.slice": "`systemctl show` ManagedOOM*/MemoryPressure* on `-.slice`",
    "manager-defaults|show|systemctl show -p DefaultMemoryPressureWatch -p DefaultMemoryPressureThresholdUSec": "manager defaults `DefaultMemoryPressureWatch`/`DefaultMemoryPressureThresholdUSec`",
    "header|uname -r": "kernel release (`uname -r`)",
    "header|systemctl --version": "systemd version (`systemctl --version`)",
}

CLASS = {
    "same": "same",
    "changed": "changed (counter or gauge moves)",
    "different": "different (configuration)",
    "new": "new in the re-capture",
}


def main():
    comp = json.load(open(sys.argv[1]))
    out = []
    out.append("| Value | Class | Frozen | Re-capture |")
    out.append("|---|---|---|---|")
    for r in comp["rows"]:
        if r["verdict"] == "absent":
            continue
        label = LABEL.get(r["key"], f"`{r['key']}`")
        frozen = "<br>".join(r["frozen"]) if r["frozen"] else "_(not captured)_"
        rec = "<br>".join(r["recapture"]) if r["recapture"] else "_(not captured)_"
        if len(frozen) > 220:
            frozen = frozen[:217] + "..."
        if len(rec) > 220:
            rec = rec[:217] + "..."
        out.append(f"| {label} | {CLASS[r['verdict']]} | {frozen} | {rec} |")
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
