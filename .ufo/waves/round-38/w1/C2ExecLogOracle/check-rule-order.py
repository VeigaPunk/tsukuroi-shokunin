#!/usr/bin/env python3
"""Independent-order check: derive the hook order from the hook files on disk by
the HO1/HO2 rule itself (S208 hook.c:443-455 ordering, :540/:588-590 first-seen
wins over a reversed directory list; S211 alpm.c:56-62 system dir then HookDir),
then require

  A) the derived per-phase order equals the table's per-phase order in
     corpus/knowledge/pacman-hook-order-r38.md (so the table under test and the
     filesystem agree), and
  B) every transaction's Pre/Post sequence in /var/log/pacman.log is a
     subsequence of the DERIVED order (so the log corroborates the rule, not
     merely the table).

Read-only. Exit 0 when A and B hold, 1 otherwise.
"""
import functools
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKER = os.path.join(HERE, "check-pacman-log-order.py")
LOG = "/var/log/pacman.log"
TABLE = ("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/"
         "pacman-hook-order-r38.md")
USR = "/usr/share/libalpm/hooks"
ETC = "/etc/pacman.d/hooks"
SUFFIX = ".hook"
WHEN_RE = re.compile(r"^When = (PreTransaction|PostTransaction)$", re.M)

spec = importlib.util.spec_from_file_location("chk", CHECKER)
chk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chk)


def cmp_hook(a, b):
    """S208 hook.c:443-455: strncmp over the shorter length of the suffix-less
    names, then the shorter name first."""
    na, nb = a[:-len(SUFFIX)], b[:-len(SUFFIX)]
    n = min(len(na), len(nb))
    c = (na[:n].encode() > nb[:n].encode()) - (na[:n].encode() < nb[:n].encode())
    if c:
        return c
    return (len(na) > len(nb)) - (len(na) < len(nb))


def scan(d):
    return sorted(f for f in os.listdir(d) if f.endswith(SUFFIX)) if os.path.isdir(d) else []


def derive():
    """HO2: system dir is the list head, HookDir entries follow, searched from the
    LAST entry to the first, first file seen for a name wins."""
    order = [USR, ETC]
    seen = {}
    for d in reversed(order):
        for f in scan(d):
            seen.setdefault(f, os.path.join(d, f))
    hooks = []
    for name, path in seen.items():
        with open(path, encoding="utf-8", errors="replace") as fh:
            m = WHEN_RE.search(fh.read())
        if not m:
            raise SystemExit(f"harness: no When in {path}")
        hooks.append((name, m.group(1), path))
    hooks.sort(key=functools.cmp_to_key(lambda x, y: cmp_hook(x[0], y[0])))
    return hooks


def main():
    hooks = derive()
    derived = {"PreTransaction": [n for n, w, _ in hooks if w == "PreTransaction"],
               "PostTransaction": [n for n, w, _ in hooks if w == "PostTransaction"]}
    table_path = sys.argv[sys.argv.index("--table") + 1] if "--table" in sys.argv else TABLE
    table, phase_of = chk.parse_table(table_path)
    table_order = {p: [n for _, n in rows] for p, rows in table.items()}

    a_ok = True
    order_diff = {}
    for p in derived:
        if derived[p] != table_order[p]:
            a_ok = False
            mism = [(i, d, t) for i, (d, t) in
                    enumerate(zip(derived[p], table_order[p])) if d != t]
            order_diff[p] = {
                "derived_only": [n for n in derived[p] if n not in table_order[p]],
                "table_only": [n for n in table_order[p] if n not in derived[p]],
                "first_order_mismatches": [{"index": i, "derived": d, "table": t}
                                           for i, d, t in mism[:5]],
                "mismatch_count": len(mism)}

    log_path = sys.argv[sys.argv.index("--log") + 1] if "--log" in sys.argv else LOG
    txs, orphans, anomalies = chk.parse_log(log_path)
    b_viol, b_rows = [], []
    for tx in txs:
        for phase, key in (("PreTransaction", "pre"), ("PostTransaction", "post")):
            seq = tx[key]
            if not seq:
                continue
            v = chk.subsequence_check(seq, {n: i + 1 for i, n in enumerate(derived[phase])},
                                      phase, tx["idx"])
            b_viol.extend(v)
            b_rows.append({"tx": tx["idx"], "phase": phase, "hooks": len(seq)})

    out = {"derived_sizes": {p: len(v) for p, v in derived.items()},
           "derived_order": derived,
           "table_sizes": {p: len(v) for p, v in table_order.items()},
           "A_table_equals_derived": a_ok, "A_diffs": order_diff,
           "B_phases_checked": len(b_rows), "B_violations": b_viol,
           "log_orphans": len(orphans), "log_anomalies": len(anomalies)}
    with open(os.path.join(HERE, "rule-order.json"), "w", encoding="utf-8") as fh:
        fh.write(json.dumps(out, indent=2) + "\n")

    print(f"derived Pre={len(derived['PreTransaction'])} "
          f"Post={len(derived['PostTransaction'])} (files: "
          f"{len(scan(USR))} usr + {len(scan(ETC))} etc)")
    print(f"A table==derived: {a_ok}")
    if not a_ok:
        print(json.dumps(order_diff, indent=2))
    print(f"B phases={len(b_rows)} violations={len(b_viol)}")
    for v in b_viol:
        print("VIOLATION " + json.dumps(v))
    return 0 if (a_ok and not b_viol and not orphans and not anomalies) else 1


if __name__ == "__main__":
    sys.exit(main())
