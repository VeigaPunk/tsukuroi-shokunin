#!/usr/bin/env python3
"""Summarize every battery JSON in this seat scratch into one machine-readable matrix."""
import glob
import json
import os
import sys

rows = {}
for path in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "battery-*.json"))):
    name = os.path.basename(path)[len("battery-"):-len(".json")]
    data = json.load(open(path))
    runs = data if isinstance(data, list) else [data]
    out = []
    for r in runs:
        fam = [e for e in r["case_log"] if e["family"] == "REFUSAL-VERSIONS-9DIGIT"]
        out.append({
            "verdict": r["verdict"],
            "families_passed": r["families_passed"],
            "families_total": r["families_total"],
            "failed_families": r["failed_families"],
            "cases": r["cases"],
            "error_rows": sum(1 for e in r["case_log"] if e.get("error") is not None),
            "nine_digit_rows": len(fam),
            "nine_digit_passed": sum(1 for e in fam if e["passed"]),
            "nine_digit_got_limine_version": sorted({(e["got"] or [None] * 7)[5] for e in fam if e["got"]}),
            "nine_digit_got_on_panic": sorted({(e["got"] or [None] * 7)[4] for e in fam if e["got"]}),
        })
    rows[name] = out
print(json.dumps(rows, indent=1, sort_keys=True))
