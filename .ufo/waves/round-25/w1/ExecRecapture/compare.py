#!/usr/bin/env python3
"""Compare the frozen round-25 capture against a re-capture.

Value classes:
  same     - the value is byte-identical in both readings
  changed  - the value is a counter or a moving gauge, so it is expected to move
  different - the value is configuration, so any difference is a real difference

Parses both files in the `### block` / `$ cmd` / output / `[exit N]` format
produced by capture.sh and recapture.sh.
"""
import json
import re
import sys


def parse(path):
    """Return {block: [(cmd, [outlines], exitcode), ...]}."""
    blocks = {}
    cur_block = None
    cur = None
    for raw in open(path, encoding="utf-8", errors="replace").read().splitlines():
        if raw.startswith("### "):
            cur_block = raw[4:].strip()
            blocks.setdefault(cur_block, [])
            cur = None
        elif raw.startswith("$ "):
            cur = (raw[2:].strip(), [], None)
            if cur_block is not None:
                blocks[cur_block].append(cur)
        elif raw.startswith("[exit ") and cur is not None:
            cur = (cur[0], cur[1], int(raw[6:-1]))
            blocks[cur_block][-1] = cur
        elif cur is not None:
            cur[1].append(raw)
    return blocks


def key_for(block, cmd):
    """A stable identity for one measured value."""
    c = cmd.strip()
    if c.startswith("systemctl show"):
        unit = c.rsplit("--", 1)[-1].strip()
        return f"{block}|show|{unit}"
    if c.startswith("systemctl is-active"):
        return f"{block}|is-active|{c.rsplit(None, 1)[-1]}"
    if c.startswith("systemctl is-enabled"):
        return f"{block}|is-enabled|{c.rsplit(None, 1)[-1]}"
    if c.startswith("systemctl cat"):
        unit = c[len("systemctl cat"):].strip()
        unit = unit.replace("(paths only)", "").strip()
        return f"{block}|cat|{unit}"
    if c.startswith("grep -hE"):
        unit = c.rsplit("for ", 1)[-1].strip()
        return f"{block}|dropin-grep|{unit}"
    if c.startswith("grep -rlE"):
        return f"{block}|kill-search"
    if c.startswith("ls -1"):
        return f"{block}|ls|{c[5:].split()[0]}"
    if c.startswith("cat "):
        return f"{block}|cat-file|{c[4:]}"
    if c.startswith("grep -E") or c.startswith("grep -vcE"):
        return f"{block}|grep|{c}"
    if c.startswith("systemd-analyze cat-config"):
        return f"{block}|cat-config|{c.rsplit(None, 1)[-1]}"
    if c in ("date -u +%Y-%m-%dT%H:%M:%SZ", "uname -r", "systemctl --version"):
        return f"{block}|{c}"
    if c == "sleep 10":
        return f"{block}|sleep"
    return f"{block}|cmd|{c}"


# Configuration values: a difference here is a real configuration difference.
CONFIG_TOKENS = (
    "uname -r",
    "systemctl --version",
    "is-active",
    "is-enabled",
    "systemctl show",
    "systemd-analyze cat-config",
    "cat-config",
    "ls ",
    "systemctl cat",
    "grep -rlE",
)

# Counter/gauge values: these are expected to move between two readings.
COUNTER_TOKENS = (
    "cat /proc/pressure/memory",
    "memory.pressure",
    "memory.events",
    "memory.swap.events",
    "/proc/vmstat",
    "/proc/meminfo",
)


def classify(block, cmd, old, new):
    if old == new:
        return "same"
    c = cmd.strip()
    if c.startswith("date "):
        return "changed"  # the wall clock of the reading, not a host property
    if any(t in c for t in CONFIG_TOKENS):
        return "different"
    if any(t in c for t in COUNTER_TOKENS):
        return "changed"
    # unknown class -> treat as different so it cannot be silently smoothed
    return "different"


NUM = re.compile(r"(-?\d+(?:\.\d+)?)")


def numeric_delta(old, new):
    """If both readings are a single number, report the signed difference."""
    def one(lines):
        if len(lines) != 1:
            return None
        m = NUM.fullmatch(lines[0].strip())
        return float(m.group(1)) if m else None
    a, b = one(old), one(new)
    if a is None or b is None:
        return None
    return b - a


def kv_delta(old, new):
    """If both readings are `key value` or `key=value` pairs, report the per-key differences."""
    def d(lines):
        out = {}
        for line in lines:
            parts = line.split()
            if len(parts) == 2:
                try:
                    out[parts[0]] = float(parts[1])
                    continue
                except ValueError:
                    pass
            if "=" in line:
                for tok in line.split():
                    if "=" in tok:
                        k, _, v = tok.partition("=")
                        try:
                            out[k] = float(v)
                        except ValueError:
                            pass
        return out or None
    a, b = d(old), d(new)
    if a is None or b is None:
        return None
    return {k: b.get(k, 0) - a.get(k, 0) for k in sorted(set(a) | set(b))}


def main():
    frozen_path, new_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    old_blocks = parse(frozen_path)
    new_blocks = parse(new_path)

    rows = []
    seen = set()
    for block in list(old_blocks) + [b for b in new_blocks if b not in old_blocks]:
        old_items = {key_for(block, c): (c, o, e) for c, o, e in old_blocks.get(block, [])}
        new_items = {key_for(block, c): (c, o, e) for c, o, e in new_blocks.get(block, [])}
        for k in list(old_items) + [k for k in new_items if k not in old_items]:
            if (block, k) in seen:
                continue
            seen.add((block, k))
            o = old_items.get(k)
            n = new_items.get(k)
            if o is None:
                rows.append({
                    "block": block, "key": k, "cmd": n[0],
                    "frozen": None, "recapture": n[1], "exit_frozen": None,
                    "exit_recapture": n[2], "verdict": "new",
                    "note": "value present only in the re-capture",
                })
                continue
            if n is None:
                rows.append({
                    "block": block, "key": k, "cmd": o[0],
                    "frozen": o[1], "recapture": None, "exit_frozen": o[2],
                    "exit_recapture": None, "verdict": "absent",
                    "note": "value present only in the frozen capture",
                })
                continue
            verdict = classify(block, o[0], o[1], n[1])
            note = ""
            delta = numeric_delta(o[1], n[1])
            if delta is None:
                delta = kv_delta(o[1], n[1])
            if o[2] != n[2]:
                verdict = "different"
                note = f"exit code moved {o[2]} -> {n[2]}"
            rows.append({
                "block": block, "key": k, "cmd": o[0],
                "frozen": o[1], "recapture": n[1], "exit_frozen": o[2],
                "exit_recapture": n[2], "verdict": verdict, "note": note,
                "delta": delta,
            })

    summary = {}
    for r in rows:
        summary[r["verdict"]] = summary.get(r["verdict"], 0) + 1

    result = {
        "frozen": frozen_path,
        "recapture": new_path,
        "summary": summary,
        "rows": rows,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print("SUMMARY", json.dumps(summary, sort_keys=True))
    for r in rows:
        if r["verdict"] in ("different", "absent", "new"):
            print(f"[{r['verdict']}] {r['block']} :: {r['key']}")
            if r["note"]:
                print(f"    note: {r['note']}")
            print(f"    frozen:    {r['frozen']}")
            print(f"    recapture: {r['recapture']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
