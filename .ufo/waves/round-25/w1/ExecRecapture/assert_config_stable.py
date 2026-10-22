#!/usr/bin/env python3
"""Assert that no configuration-class value drifted between the two captures.

Configuration-class values are the ones that must NOT move: unit states,
enablement, the oomd.conf body, the ManagedOOM*/MemoryPressure* properties of
the four units, the manager defaults, the kernel release and the systemd
version. A byte difference in any of them would be a real configuration
change; the counters and gauges are expected to move and are checked
separately.
"""
import json
import sys

CONFIG_KEYS = [
    "header|uname -r",
    "header|systemctl --version",
    "oomd-unit|is-active|systemd-oomd.service",
    "oomd-unit|is-enabled|systemd-oomd.service",
    "oomd-unit|is-enabled|systemd-oomd.socket",
    "oomd-config|cat-config|systemd/oomd.conf",
    "managed-oom-properties|show|user@1000.service",
    "managed-oom-properties|show|user-1000.slice",
    "managed-oom-properties|show|user.slice",
    "managed-oom-properties|show|-.slice",
    "manager-defaults|show|systemctl show -p DefaultMemoryPressureWatch -p DefaultMemoryPressureThresholdUSec",
]

COUNTER_KEYS = [
    "system-memory-psi-read-1|cat-file|/proc/pressure/memory",
    "system-memory-psi-read-2|cat-file|/proc/pressure/memory",
    "root-cgroup-memory-pressure|cat-file|/sys/fs/cgroup/memory.pressure",
    "user-slice-memory-pressure|cat-file|/sys/fs/cgroup/user.slice/memory.pressure",
    "user-slice-memory-pressure|cat-file|/sys/fs/cgroup/user.slice/user-1000.slice/memory.pressure",
    "user-slice-memory-pressure|cat-file|/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/memory.pressure",
    "user-slice-memory-events|cat-file|/sys/fs/cgroup/user.slice/user-1000.slice/memory.events",
    "user-slice-memory-events|cat-file|/sys/fs/cgroup/user.slice/user-1000.slice/memory.swap.events",
    "kernel-oom-counter|grep|grep -E ^oom_kill  /proc/vmstat",
    "swap|grep|grep -E ^(SwapTotal|SwapFree|MemTotal|MemAvailable): /proc/meminfo",
]


def main():
    comp = json.load(open(sys.argv[1]))
    rows = {r["key"]: r for r in comp["rows"]}

    failures = []
    for k in CONFIG_KEYS:
        r = rows.get(k)
        if r is None:
            failures.append(f"MISSING configuration key: {k}")
            continue
        if r["verdict"] != "same":
            failures.append(
                f"CONFIGURATION DRIFT at {k}: verdict={r['verdict']}\n"
                f"    frozen:    {r['frozen']}\n"
                f"    recapture: {r['recapture']}"
            )

    # The kernel OOM kill counter must be identical: no OOM happened between
    # the two readings, so this one counter must NOT move even though it is a
    # counter. It is listed here rather than under COUNTER_KEYS.
    k = "kernel-oom-counter|grep|grep -E ^oom_kill  /proc/vmstat"
    r = rows.get(k)
    if r is not None and r["verdict"] != "same":
        failures.append(f"KERNEL OOM KILL COUNTER MOVED: {r['frozen']} -> {r['recapture']}")

    moved = [k for k in COUNTER_KEYS if rows.get(k, {}).get("verdict") == "changed"]
    not_moved = [k for k in COUNTER_KEYS if rows.get(k, {}).get("verdict") == "same"]

    result = {
        "configuration_keys_checked": len(CONFIG_KEYS),
        "configuration_failures": failures,
        "configuration_stable": not failures,
        "counter_keys_expected_to_move": len(COUNTER_KEYS),
        "counter_keys_that_moved": len(moved),
        "counter_keys_that_did_not_move": not_moved,
        "verdict": "PASS" if not failures else "FAIL",
    }
    print(json.dumps(result, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
