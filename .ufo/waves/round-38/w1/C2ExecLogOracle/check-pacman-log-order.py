#!/usr/bin/env python3
"""C2-1 kill-rule oracle: check the host's real pacman.log hook run order against
the r38 effective-hook-order table.

Read-only. Inputs:
  --log  /var/log/pacman.log
  --table corpus/knowledge/pacman-hook-order-r38.md  (section
          '## Effective hook order (r38 capture)')

Model (from S210 trans.c:201-204 and :212-240, verified below by structure):
  PreTransaction hooks are logged BEFORE 'transaction started';
  PostTransaction hooks are logged AFTER 'transaction completed'.
Therefore, for one transaction, the 'running' lines preceding 'transaction started'
(form (c)) are the Pre phase and those following 'transaction completed' are the
Post phase.

Checks:
  T1 every Pre-phase name sequence is a subsequence of the table's PreTransaction
     order (pos 1..N)          -> HO7
  T2 every Post-phase name sequence is a subsequence of the PostTransaction order
     -> HO7
  T3 no hook name repeats within one phase of one transaction (a total order has
     no duplicates)
  T4 every observed hook name's phase equals the phase the table records
  T5 every observed hook name exists in the table; unknowns are reported as
     'in log, not in table' (with the on-disk hook dirs consulted for existence)
Exit 0 when no T1..T4 finding, 1 when any T1..T4 finding, 2 on harness failure.
"""
import argparse
import json
import os
import re
import sys

RUNNING_RE = re.compile(r"^\[(?P<ts>[^\]]+)\] \[ALPM\] running '(?P<name>[^']+)'\.\.\.$")
PACMAN_CMD_RE = re.compile(r"^\[(?P<ts>[^\]]+)\] \[PACMAN\] Running '(?P<cmd>.*)'$")
TX_START_RE = re.compile(r"^\[(?P<ts>[^\]]+)\] \[ALPM\] transaction started$")
TX_DONE_RE = re.compile(r"^\[(?P<ts>[^\]]+)\] \[ALPM\] transaction (completed|failed|interrupted)$")
TABLE_ROW_RE = re.compile(
    r"^\|\s*(?P<when>PreTransaction|PostTransaction)\s*\|\s*(?P<pos>\d+)\s*\|"
    r"\s*`(?P<name>[^`]+)`\s*\|\s*(?P<dir>usr|etc)\s*\|"
    r"\s*(?P<abort>yes|no)\s*\|\s*(?P<needs>yes|no)\s*\|\s*`(?P<exec>[^`]+)`\s*\|\s*$"
)


def parse_table(path):
    """Return {phase: [(pos, name)]} sorted by pos, and {name: phase}."""
    orders = {"PreTransaction": [], "PostTransaction": []}
    with open(path, encoding="utf-8") as fh:
        inside = False
        for line in fh:
            if line.startswith("## Effective hook order"):
                inside = True
                continue
            if inside and line.startswith("## "):
                break
            if not inside:
                continue
            m = TABLE_ROW_RE.match(line.rstrip("\n"))
            if m:
                orders[m.group("when")].append((int(m.group("pos")), m.group("name")))
    for phase, rows in orders.items():
        rows.sort()
        pos = [p for p, _ in rows]
        if pos != list(range(1, len(pos) + 1)):
            raise SystemExit(f"harness: {phase} positions are not 1..N: {pos}")
    if not orders["PreTransaction"] or not orders["PostTransaction"]:
        raise SystemExit("harness: table section not found or empty")
    phase_of = {}
    for phase, rows in orders.items():
        for _, name in rows:
            if name in phase_of:
                raise SystemExit(f"harness: duplicate name in table: {name}")
            phase_of[name] = phase
    return orders, phase_of


def parse_log(path):
    """Group hook runs into transactions by phase.

    Returns (transactions, orphans, anomalies) where a transaction is
    {idx, ts, cmd, start_line, end_line, status, pre:[(line,name)], post:[(line,name)]}.
    orphans: hook runs that precede a 'transaction started' that never happened.
    """
    transactions = []
    orphans = []
    anomalies = []
    pending = []      # hook runs seen before a 'transaction started'
    last_tx = None
    state = "idle"    # idle | post | in_tx
    cmd = None
    cmd_line = None
    with open(path, encoding="utf-8", errors="replace") as fh:
        for lineno, raw in enumerate(fh, 1):
            line = raw.rstrip("\n")
            m = RUNNING_RE.match(line)
            if m:
                if state == "in_tx":
                    anomalies.append({"line": lineno, "name": m.group("name"),
                                      "kind": "hook-run-inside-transaction-body"})
                elif state == "post" and last_tx is not None:
                    last_tx["post"].append((lineno, m.group("name")))
                else:
                    pending.append((lineno, m.group("name")))
                continue
            m = PACMAN_CMD_RE.match(line)
            if m:
                if pending:
                    orphans.append({"cmd": cmd, "cmd_line": cmd_line, "hooks": pending})
                    pending = []
                state = "idle"
                cmd = m.group("cmd")
                cmd_line = lineno
                continue
            m = TX_START_RE.match(line)
            if m:
                last_tx = {"idx": len(transactions) + 1, "ts": m.group("ts"),
                           "cmd": cmd, "cmd_line": cmd_line,
                           "start_line": lineno, "end_line": None, "status": None,
                           "pre": pending, "post": []}
                transactions.append(last_tx)
                pending = []
                state = "in_tx"
                continue
            m = TX_DONE_RE.match(line)
            if m:
                if last_tx is None or last_tx["end_line"] is not None:
                    anomalies.append({"line": lineno, "kind": "orphan-transaction-end",
                                      "status": m.group(2)})
                    state = "post"
                    continue
                last_tx["end_line"] = lineno
                last_tx["status"] = m.group(2)
                state = "post"
                continue
    if pending:
        orphans.append({"cmd": cmd, "cmd_line": cmd_line, "hooks": pending})
    return transactions, orphans, anomalies


def subsequence_check(seq, order_pos, phase, label):
    """Greedy subsequence test of seq=[(line,name)] against order_pos={name: pos}.

    Returns list of violations; each names the log line, the hook, the last
    matched position and the table position that breaks monotonicity.
    """
    violations = []
    last_pos = 0
    last_name = None
    for line, name in seq:
        pos = order_pos.get(name)
        if pos is None:
            continue  # unknown names are reported by T5
        if pos <= last_pos:
            violations.append({
                "check": "subsequence", "phase": phase, "line": line, "hook": name,
                "table_pos": pos, "previous_hook": last_name, "previous_pos": last_pos,
            })
        else:
            last_pos = pos
            last_name = name
    return violations


def hook_coverage(transactions, orders, phase_of):
    """Which table rows never appear in the log, and the first/last log sighting
    of every observed hook (for 'hook added/removed during the log' reading)."""
    seen = {}
    for tx in transactions:
        for phase, key in (("PreTransaction", "pre"), ("PostTransaction", "post")):
            for line, name in tx[key]:
                s = seen.setdefault(name, {"phase": phase, "count": 0,
                                           "first_line": line, "last_line": line,
                                           "first_ts": tx["ts"], "last_ts": tx["ts"]})
                s["count"] += 1
                if line < s["first_line"]:
                    s["first_line"], s["first_ts"] = line, tx["ts"]
                if line > s["last_line"]:
                    s["last_line"], s["last_ts"] = line, tx["ts"]
    never = [{"phase": phase, "pos": pos, "name": name}
             for phase, rows in orders.items() for pos, name in rows if name not in seen]
    return {"observed_distinct": len(seen), "table_rows": len(phase_of),
            "never_observed": never, "observed": dict(sorted(seen.items()))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", default="/var/log/pacman.log")
    ap.add_argument("--table", required=True)
    ap.add_argument("--hooks-dirs", default="/usr/share/libalpm/hooks:/etc/pacman.d/hooks")
    ap.add_argument("--json", default="-")
    args = ap.parse_args()

    orders, phase_of = parse_table(args.table)
    order_pos = {phase: {name: pos for pos, name in rows} for phase, rows in orders.items()}
    on_disk = set()
    for d in args.hooks_dirs.split(":"):
        if os.path.isdir(d):
            on_disk.update(f for f in os.listdir(d) if f.endswith(".hook"))

    transactions, orphans, anomalies = parse_log(args.log)

    findings = []
    for tx in transactions:
        for phase, key in (("PreTransaction", "pre"), ("PostTransaction", "post")):
            seq = tx[key]
            if not seq:
                continue
            findings.extend(subsequence_check(seq, order_pos[phase], phase, tx["idx"]))
            seen = {}
            for line, name in seq:
                if name in seen:
                    findings.append({"check": "duplicate-in-phase", "phase": phase,
                                     "line": line, "hook": name,
                                     "first_line": seen[name], "tx": tx["idx"]})
                else:
                    seen[name] = line

    # T4 phase agreement, T5 unknown names
    observed = {"PreTransaction": {}, "PostTransaction": {}}
    for tx in transactions:
        for phase, key in (("PreTransaction", "pre"), ("PostTransaction", "post")):
            for line, name in tx[key]:
                observed[phase].setdefault(name, []).append(line)

    for phase, names in observed.items():
        for name, lines in names.items():
            if name not in phase_of:
                continue
            if phase_of[name] != phase:
                findings.append({"check": "phase-mismatch", "phase_observed": phase,
                                 "phase_table": phase_of[name], "hook": name,
                                 "lines": lines[:10], "occurrences": len(lines)})

    unknown = {}
    for phase, names in observed.items():
        for name, lines in names.items():
            if name in phase_of:
                continue
            unknown[name] = {"phases": sorted({p for p, n in observed.items() if name in n}),
                             "occurrences": len(lines), "lines": lines,
                             "on_disk_now": name in on_disk}

    phases_checked = sum(1 for tx in transactions
                         for key in ("pre", "post") if tx[key])
    hook_runs = sum(len(tx["pre"]) + len(tx["post"]) for tx in transactions)
    result = {
        "log": args.log,
        "table": args.table,
        "table_sizes": {p: len(r) for p, r in orders.items()},
        "transactions": len(transactions),
        "phases_checked": phases_checked,
        "phases_empty": [{"tx": tx["idx"], "start_line": tx["start_line"],
                          "missing": [k for k in ("pre", "post") if not tx[k]]}
                         for tx in transactions
                         if not tx["pre"] or not tx["post"]],
        "hook_coverage": hook_coverage(transactions, orders, phase_of),
        "hook_runs_in_transactions": hook_runs,
        "orphan_hook_runs": orphans,
        "anomalies": anomalies,
        "findings": findings,
        "unknown_hooks": unknown,
        "per_transaction": [
            {"idx": tx["idx"], "ts": tx["ts"], "cmd": tx["cmd"], "status": tx["status"],
             "start_line": tx["start_line"], "end_line": tx["end_line"],
             "pre": [{"line": l, "name": n} for l, n in tx["pre"]],
             "post": [{"line": l, "name": n} for l, n in tx["post"]]}
            for tx in transactions
        ],
    }
    out = json.dumps(result, indent=2, sort_keys=False)
    if args.json == "-":
        print(out)
    else:
        with open(args.json, "w", encoding="utf-8") as fh:
            fh.write(out + "\n")

    print(f"transactions={len(transactions)} phases_checked={phases_checked} "
          f"hook_runs={hook_runs} orphans={len(orphans)} anomalies={len(anomalies)} "
          f"findings={len(findings)} unknown_hooks={len(unknown)}", file=sys.stderr)
    for f in findings:
        print("FINDING " + json.dumps(f), file=sys.stderr)
    for name, info in unknown.items():
        print(f"UNKNOWN {name} occurrences={info['occurrences']} "
              f"on_disk_now={info['on_disk_now']} lines={info['lines'][:12]}", file=sys.stderr)
    if orphans:
        for o in orphans:
            print("ORPHAN " + json.dumps(o), file=sys.stderr)
    for a in anomalies:
        print("ANOMALY " + json.dumps(a), file=sys.stderr)
    return 1 if (findings or orphans or anomalies) else 0


if __name__ == "__main__":
    sys.exit(main())
