#!/usr/bin/env python3
"""Count a round-93 battery JSON (one run or a list of runs) against the frozen claim targets.

Usage: count-runs.py <battery.json> [--family NAME ...]
Prints one JSON summary: per run, families_passed/total, verdict, failed_families, error rows,
and per named family its passed/failed counts. Exit 0 iff every run on the landed gate meets the
frozen targets for the families named on the command line, 1 otherwise.
"""
import argparse
import json
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json")
    ap.add_argument("--family", action="append", default=[])
    a = ap.parse_args()
    with open(a.json, "r", encoding="utf-8") as f:
        data = json.load(f)
    runs = data if isinstance(data, list) else [data]
    fams = a.family or sorted({e["family"] for r in runs for e in r.get("case_log", [])})
    out = {"runs": [], "families": fams}
    ok = True
    for r in runs:
        errors = sum(1 for e in r.get("case_log", []) if e.get("error") is not None)
        per = {}
        for e in r.get("case_log", []):
            if e["family"] in fams:
                p = per.setdefault(e["family"], [0, 0])
                p[0 if e["passed"] else 1] += 1
        out["runs"].append({"verdict": r.get("verdict"),
                            "families_passed": r.get("families_passed"),
                            "families_total": r.get("families_total"),
                            "failed_families": r.get("failed_families"),
                            "cases": r.get("cases"), "error_rows": errors,
                            "named": per})
        if r.get("verdict") != "met" or errors:
            ok = False
    print(json.dumps(out, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
