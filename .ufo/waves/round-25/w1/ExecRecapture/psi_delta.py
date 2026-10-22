#!/usr/bin/env python3
"""PSI two-read difference inside one capture file.

MP2 says the `total` field is cumulative stall time, so a dated incident needs
two reads and a difference. This computes that difference for the system-level
memory PSI of a capture file, and reports the stall fraction over the elapsed
wall-clock interval.
"""
import json
import re
import sys
from datetime import datetime

LINE = re.compile(r"^(some|full)\s+(.*)$")
KV = re.compile(r"(\w+)=([0-9.]+)")


def parse(path):
    """Return the two system-level /proc/pressure/memory readings, in order."""
    readings = []
    cur = None
    active = False
    for raw in open(path, encoding="utf-8", errors="replace"):
        raw = raw.rstrip("\n")
        if raw.startswith("$ "):
            # Only the system-level PSI file counts; per-cgroup memory.pressure
            # files carry the same `some`/`full` shape and must not be mixed in.
            active = raw.strip() == "$ cat /proc/pressure/memory"
            if active:
                cur = {}
                readings.append(cur)
            continue
        if not active or cur is None:
            continue
        m = LINE.match(raw)
        if m:
            cur[m.group(1)] = {k: float(v) for k, v in KV.findall(m.group(2))}
    return [r for r in readings if "some" in r and "full" in r]


def psi_stall_fraction(delta_us, elapsed_s):
    """Cumulative stall microseconds over the elapsed wall-clock microseconds."""
    if not elapsed_s:
        return None
    return delta_us / (elapsed_s * 1_000_000.0)


def main():
    path = sys.argv[1]
    readings = parse(path)
    if len(readings) < 2:
        print(f"{path}: fewer than two system PSI readings found")
        return 1
    a, b = readings[0], readings[1]
    out = {"file": path, "readings": len(readings), "lines": {}}
    for line in ("some", "full"):
        d_total = b[line]["total"] - a[line]["total"]
        out["lines"][line] = {
            "read1_total_us": a[line]["total"],
            "read2_total_us": b[line]["total"],
            "delta_total_us": d_total,
            "read1_avg": {k: a[line][k] for k in ("avg10", "avg60", "avg300")},
            "read2_avg": {k: b[line][k] for k in ("avg10", "avg60", "avg300")},
        }
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
