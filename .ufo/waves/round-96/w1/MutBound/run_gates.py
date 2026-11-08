#!/usr/bin/env python3
"""Round-96 MutBound runner: one battery run per gate, receipts under the seat dir.

Usage: run_gates.py --workdir DIR --tag PREFIX GATE [GATE ...]
Each gate gets its own --work subtree and its own receipt <tag>-<stem>.json + .log under
 .ufo/waves/round-96/w1/MutBound/receipts/. Exit codes go to results-<tag>.tsv.
"""
import argparse
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
BATTERY = os.path.join(LANE, "tools", "limine-pin-battery-r96.py")
SEAT = os.path.join(LANE, ".ufo", "waves", "round-96", "w1", "MutBound")
RECEIPTS = os.path.join(SEAT, "receipts")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workdir", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("gates", nargs="+")
    a = ap.parse_args()
    os.makedirs(RECEIPTS, exist_ok=True)
    ts_rows = []
    for gate in a.gates:
        stem = os.path.splitext(os.path.basename(gate))[0]
        name = "%s-%s" % (a.tag, stem)
        work = os.path.join(os.path.abspath(a.workdir), "work-" + stem)
        os.makedirs(work, exist_ok=True)
        out_json = os.path.join(RECEIPTS, name + ".json")
        cmd = [sys.executable, BATTERY, "--gate", os.path.abspath(gate), "--runs", "1",
               "--work", work, "--json", out_json]
        p = subprocess.run(cmd, cwd=LANE, capture_output=True, text=True)
        with open(os.path.join(RECEIPTS, name + ".log"), "w", encoding="utf-8") as f:
            f.write("$ " + " ".join(cmd) + "\n")
            f.write(p.stdout)
            if p.stderr:
                f.write("--- stderr ---\n" + p.stderr)
            f.write("exit %d\n" % p.returncode)
        last = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else "<no stdout>"
        ts_rows.append("%s\t%s\t%d\t%s\n" % (stem, out_json, p.returncode, last))
        print("%s exit=%d %s" % (stem, p.returncode, last), flush=True)
    with open(os.path.join(RECEIPTS, "results-%s.tsv" % a.tag), "w", encoding="utf-8") as f:
        f.writelines(ts_rows)


if __name__ == "__main__":
    main()
