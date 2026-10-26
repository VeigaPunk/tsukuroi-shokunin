#!/usr/bin/env python3
"""Non-vacuity self-test for check-pacman-log-order.py.

Takes the real /var/log/pacman.log (read-only), writes 6 mutants under this
scratch dir, and asserts that the checker reports the planted defect and stays
silent on the pristine file. A checker that never fires is worthless as an
oracle, so each expected detection is asserted on the mutant AND absence on the
pristine baseline.

M1  swap two hook lines inside one Post phase            -> subsequence
M2  move a Pre hook line after 'transaction completed'    -> phase-mismatch
M3  move a hook line between started/completed            -> anomaly (body)
M4  duplicate a Post hook line inside the same phase      -> duplicate-in-phase
M5  rename a Post hook to zzz-gone.hook                   -> unknown (not a finding)
M6  drop the trailing '...' of one hook line              -> line ignored, no finding
"""
import importlib.util
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKER = os.path.join(HERE, "check-pacman-log-order.py")
TABLE = ("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/"
         "pacman-hook-order-r38.md")
LOG = "/var/log/pacman.log"

spec = importlib.util.spec_from_file_location("chk", CHECKER)
chk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chk)


def run(path, out_name):
    out = os.path.join(HERE, out_name)
    proc = subprocess.run([sys.executable, CHECKER, "--log", path, "--table", TABLE,
                           "--json", out], capture_output=True, text=True)
    return proc.returncode, proc.stderr, json.load(open(out))


def main():
    with open(LOG, encoding="utf-8", errors="replace") as fh:
        lines = fh.readlines()
    txs, orphans, anomalies = chk.parse_log(LOG)
    assert not orphans and not anomalies, "baseline must be structurally clean"

    base = os.path.join(HERE, "log.baseline")
    with open(base, "w", encoding="utf-8") as fh:
        fh.writelines(lines)
    results = []

    rc, err, res = run(base, "selftest-M0.json")
    results.append(("M0 pristine baseline: no findings", rc == 0 and not res["findings"]
                    and res["transactions"] == 60, rc, err.splitlines()[:1]))

    # locate a Post phase with >=3 hooks and a Pre phase with >=1 hook
    post_tx = next(t for t in txs if len(t["post"]) >= 3)
    pre_tx = next(t for t in txs if t["pre"])
    a, b = post_tx["post"][1], post_tx["post"][2]          # (1-based line, hook name)
    la, lb = a[0], b[0]                                    # line numbers

    # M1: swap the two hook lines (positions of the lines themselves are swapped)
    m1 = list(lines)
    m1[a[0] - 1], m1[b[0] - 1] = m1[b[0] - 1], m1[a[0] - 1]
    p1 = os.path.join(HERE, "log.M1")
    with open(p1, "w", encoding="utf-8") as fh:
        fh.writelines(m1)
    rc, err, res = run(p1, "selftest-M1.json")
    kinds1 = {f["check"] for f in res["findings"]}
    results.append((f"M1 swap post hooks tx{post_tx['idx']} ({lb} before {la})",
                    rc == 1 and "subsequence" in kinds1, rc, sorted(kinds1)))

    # M2: move the Pre hook line to after the same transaction's 'transaction completed'
    pre_line, pre_name = pre_tx["pre"][0]
    m2 = list(lines)
    moved = m2.pop(pre_line - 1)
    at = pre_tx["end_line"] - 1                          # just after 'completed'
    m2.insert(at, moved)
    p2 = os.path.join(HERE, "log.M2")
    with open(p2, "w", encoding="utf-8") as fh:
        fh.writelines(m2)
    rc, err, res = run(p2, "selftest-M2.json")
    kinds2 = {f["check"] for f in res["findings"]}
    results.append((f"M2 move pre hook {pre_name} (line {pre_line}) into Post phase",
                    rc == 1 and "phase-mismatch" in kinds2, rc, sorted(kinds2)))

    # M3: move a hook line into the transaction body
    m3 = list(lines)
    moved = m3.pop(b[0] - 1)
    m3.insert(post_tx["start_line"], moved)             # after 'transaction started'
    p3 = os.path.join(HERE, "log.M3")
    with open(p3, "w", encoding="utf-8") as fh:
        fh.writelines(m3)
    rc, err, res = run(p3, "selftest-M3.json")
    kinds3 = {a["kind"] for a in res["anomalies"]}
    results.append((f"M3 insert hook line inside tx{post_tx['idx']} body",
                    rc == 1 and "hook-run-inside-transaction-body" in kinds3, rc,
                    sorted(kinds3)))

    # M4: duplicate a Post hook line inside its phase
    m4 = list(lines)
    m4.insert(b[0] - 1, m4[b[0] - 1])
    p4 = os.path.join(HERE, "log.M4")
    with open(p4, "w", encoding="utf-8") as fh:
        fh.writelines(m4)
    rc, err, res = run(p4, "selftest-M4.json")
    kinds4 = {f["check"] for f in res["findings"]}
    results.append((f"M4 duplicate post hook {lb} in tx{post_tx['idx']}",
                    rc == 1 and "duplicate-in-phase" in kinds4, rc, sorted(kinds4)))

    # M5: rename to a hook that does not exist anywhere
    m5 = list(lines)
    m5[b[0] - 1] = m5[b[0] - 1].replace(f"'{b[1]}'", "'zzz-gone.hook'")
    p5 = os.path.join(HERE, "log.M5")
    with open(p5, "w", encoding="utf-8") as fh:
        fh.writelines(m5)
    rc, err, res = run(p5, "selftest-M5.json")
    results.append(("M5 rename one hook to zzz-gone.hook",
                    "zzz-gone.hook" in res["unknown_hooks"]
                    and res["unknown_hooks"]["zzz-gone.hook"]["on_disk_now"] is False,
                    rc, sorted(res["unknown_hooks"])))

    # M6: strip the '...' suffix of one hook line -> the anchored regex must ignore it
    m6 = list(lines)
    m6[b[0] - 1] = m6[b[0] - 1].rstrip("\n").removesuffix("...") + "\n"
    p6 = os.path.join(HERE, "log.M6")
    with open(p6, "w", encoding="utf-8") as fh:
        fh.writelines(m6)
    rc, err, res = run(p6, "selftest-M6.json")
    results.append(("M6 strip '...' from one hook line (must be ignored, not invented)",
                    rc == 0 and res["hook_runs_in_transactions"] == 294, rc,
                    [res["hook_runs_in_transactions"]]))

    ok = True
    for name, passed, rc, detail in results:
        ok &= bool(passed)
        print(f"{'PASS' if passed else 'FAIL'}  {name}  rc={rc}  {detail}")
    print("SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
