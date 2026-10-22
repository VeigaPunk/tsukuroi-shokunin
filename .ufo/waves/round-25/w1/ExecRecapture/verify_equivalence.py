#!/usr/bin/env python3
"""Check two specific structural facts inside a capture file.

1. The second system-level /proc/pressure/memory reading is byte-identical to
   the root cgroup's /sys/fs/cgroup/memory.pressure reading taken afterwards.
   That is the host fact behind MP3: the root cgroup's memory.pressure file is
   the same accounting as the system-wide /proc/pressure/memory file.

2. The number of "active" lines systemd-analyze cat-config reports for
   systemd/oomd.conf is accounted for: which lines they are, and how many of
   them are actual settings rather than section headers.
"""
import json
import re
import sys

CMD = re.compile(r"^\$ (.*)$")
PSI = re.compile(r"^(some|full)\s+(.*)$")
KV = re.compile(r"(\w+)=([0-9.]+)")


def blocks(path):
    out = {}
    cur = None
    for raw in open(path, encoding="utf-8", errors="replace"):
        raw = raw.rstrip("\n")
        if raw.startswith("### "):
            cur = raw[4:].strip()
            out.setdefault(cur, [])
        elif raw.startswith("$ "):
            out[cur].append((raw[2:].strip(), [], None))
        elif raw.startswith("[exit ") and out[cur] and out[cur][-1][2] is None:
            cmd, body, _ = out[cur][-1]
            out[cur][-1] = (cmd, body, int(raw[6:-1]))
        elif out[cur] and out[cur][-1][2] is None:
            cmd, body, _ = out[cur][-1]
            out[cur][-1] = (cmd, body + [raw], None)
    return out


def main():
    path = sys.argv[1]
    b = blocks(path)
    result = {"file": path}

    # --- fact 1: root cgroup memory.pressure == system /proc/pressure/memory
    sys_psi = [body for cmd, body, _ in b.get("system-memory-psi-read-2", [])
               if cmd == "cat /proc/pressure/memory"]
    root_psi = [body for cmd, body, _ in b.get("root-cgroup-memory-pressure", [])
                if cmd == "cat /sys/fs/cgroup/memory.pressure"]
    if sys_psi and root_psi:
        a, c = sys_psi[0], root_psi[0]
        result["root_cgroup_equals_system_psi"] = {
            "identical": a == c,
            "system_read2": a,
            "root_cgroup": c,
        }

    # --- fact 2: which lines count as "active" in the oomd.conf dump
    cfg = [body for cmd, body, _ in b.get("oomd-config", [])
           if cmd.strip() == "systemd-analyze cat-config systemd/oomd.conf"]
    if cfg:
        active = [ln for ln in cfg[0] if ln.strip() and not ln.startswith(("#", ";", "["))]
        headers = [ln for ln in cfg[0] if ln.strip() and ln.startswith("[")]
        result["oomd_conf_active_lines"] = {
            "settings_count": len(active),
            "settings": active,
            "section_headers": headers,
        }

    # --- fact 3: the PSI two-read difference, per line
    def psi_of(block, cmd):
        for c, body, _ in b.get(block, []):
            if c == cmd:
                d = {}
                for ln in body:
                    m = PSI.match(ln)
                    if m:
                        d[m.group(1)] = {k: float(v) for k, v in KV.findall(m.group(2))}
                return d
        return None

    r1 = psi_of("system-memory-psi-read-1", "cat /proc/pressure/memory")
    r2 = psi_of("system-memory-psi-read-2", "cat /proc/pressure/memory")
    if r1 and r2:
        result["psi_two_read_delta_us"] = {
            line: r2[line]["total"] - r1[line]["total"] for line in ("some", "full")
        }

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
