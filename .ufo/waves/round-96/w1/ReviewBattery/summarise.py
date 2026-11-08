#!/usr/bin/env python3
"""Summarise every battery receipt under this seat dir into one table (read-only)."""
import glob
import json
import os

SEAT = os.path.dirname(os.path.abspath(__file__))
rows = []
for path in sorted(glob.glob(os.path.join(SEAT, "*.json"))):
    try:
        data = json.load(open(path, encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        rows.append((os.path.basename(path), "UNREADABLE: %s" % e))
        continue
    runs = data if isinstance(data, list) else [data]
    for i, r in enumerate(runs, 1):
        if not isinstance(r, dict) or "case_log" not in r:
            continue
        errs = sum(1 for e in r["case_log"] if e.get("error") is not None)
        fams = sorted({e["family"] for e in r["case_log"]})
        rows.append((os.path.basename(path), i, r.get("verdict"), r.get("families_passed"),
                     r.get("families_total"), r.get("failed_families"), errs, len(fams),
                     r.get("cases")))
print("receipt | run | verdict | passed | total | failed_families | error_rows | families_in_log | cases")
for row in rows:
    print(" | ".join(str(x) for x in row))
