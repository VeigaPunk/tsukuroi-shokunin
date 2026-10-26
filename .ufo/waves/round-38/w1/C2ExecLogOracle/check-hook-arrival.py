#!/usr/bin/env python3
"""Second oracle axis: no hook may be logged before the package that ships its
file was ever installed/upgraded in the log.

For every hook name observed in /var/log/pacman.log:
  owners  = pacman -Qoq for every file with that basename in the two HookDirs
  arrival = first log line installing/upgrading/reinstalling/downgrading an owner
  first   = first 'running' line for the name
Rule checked: first > arrival (a hook cannot run before its file exists; a Post
hook installed in a transaction may run in that same transaction's Post phase,
which still gives first > arrival because the install line precedes 'completed').

Read-only: pacman -Qoq is a query (no transaction, no database write).
Exit 1 if any observed hook precedes its owner's first appearance.
"""
import importlib.util
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKER = os.path.join(HERE, "check-pacman-log-order.py")
LOG = "/var/log/pacman.log"
DIRS = ("/usr/share/libalpm/hooks", "/etc/pacman.d/hooks")

spec = importlib.util.spec_from_file_location("chk", CHECKER)
chk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chk)

OP_RE = re.compile(r"^\[[^\]]+\] \[ALPM\] (installed|upgraded|reinstalled|downgraded) "
                   r"([^ ]+) \(")


def owners_of(name):
    out = set()
    for d in DIRS:
        p = os.path.join(d, name)
        if os.path.exists(p):
            r = subprocess.run(["pacman", "-Qoq", p], capture_output=True, text=True)
            if r.returncode == 0 and r.stdout.strip():
                out.add(r.stdout.strip().splitlines()[0])
    return sorted(out)


def main():
    txs, orphans, anomalies = chk.parse_log(LOG)
    first = {}
    for tx in txs:
        for key in ("pre", "post"):
            for line, name in tx[key]:
                if name not in first or line < first[name]["line"]:
                    first[name] = {"line": line, "ts": tx["ts"], "tx": tx["idx"],
                                   "phase": "PreTransaction" if key == "pre" else "PostTransaction"}

    arrivals = {}
    with open(LOG, encoding="utf-8", errors="replace") as fh:
        for lineno, raw in enumerate(fh, 1):
            m = OP_RE.match(raw.rstrip("\n"))
            if m:
                arrivals.setdefault(m.group(2), []).append((lineno, m.group(1)))

    rows, violations = [], []
    for name in sorted(first):
        owners = owners_of(name)
        cand = []
        for o in owners:
            for line, op in arrivals.get(o, [])[:1]:
                cand.append((line, o, op))
        arrival = min(cand) if cand else None
        row = {"hook": name, "first_line": first[name]["line"], "first_ts": first[name]["ts"],
               "phase": first[name]["phase"], "owners": owners,
               "owner_arrival_line": arrival[0] if arrival else None,
               "owner_arrival_ts": None, "owner_arrival_pkg": arrival[1] if arrival else None}
        if not owners:
            # unowned file in a HookDir (operator file) - arrival is not a pacman
            # operation, so the rule cannot apply; reported, not a violation
            row["verdict"] = "unowned-operator-file"
        elif arrival is None:
            row["verdict"] = "owner-not-in-log"
            violations.append(row)
        elif first[name]["line"] <= arrival[0]:
            row["verdict"] = "ran-before-owner-installed"
            violations.append(row)
        else:
            row["verdict"] = "ok"
        rows.append(row)

    out = {"rows": rows, "violations": violations,
           "observed": len(rows), "ok": sum(1 for r in rows if r["verdict"] == "ok")}
    path = os.path.join(HERE, "hook-arrival.json")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(out, indent=2) + "\n")
    print(f"hooks={len(rows)} ok={out['ok']} violations={len(violations)}")
    for v in violations:
        print("VIOLATION " + json.dumps(v))
    for r in rows:
        print(f"{r['verdict']:26s} {r['hook']:45s} first={r['first_line']:5d} "
              f"owner={','.join(r['owners']) or '?':22s} arrival={r['owner_arrival_line']}")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
