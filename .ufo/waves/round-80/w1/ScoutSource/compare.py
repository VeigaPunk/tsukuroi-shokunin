#!/usr/bin/env python3
"""Compare the independently extracted matrix against the frozen expected object.

Reports: cell-level diff (42 cells), metadata fields, and settings-order
sensitivity (does the expected ordering match the XML header order?).
"""
import json
import sys

indep = json.load(open(sys.argv[1]))
exp = json.load(open(sys.argv[2]))

ok = True
notes = []

# settings order
if indep["settings"] == exp["settings"]:
    notes.append(f"settings order MATCHES XML header: {exp['settings']}")
else:
    ok = False
    notes.append(f"settings order DIFFERS: indep={indep['settings']} exp={exp['settings']}")

# rows
ir = {r["cause"]: r["restart"] for r in indep["rows"]}
er = {r["cause"]: r["restart"] for r in exp["rows"]}
if set(ir) != set(er):
    ok = False
    notes.append(f"cause set differs: only-indep={set(ir)-set(er)} only-exp={set(er)-set(ir)}")
else:
    notes.append("cause labels identical (6 rows)")

diffs = []
for cause in er:
    for i, setting in enumerate(exp["settings"]):
        a, b = ir[cause][i], er[cause][i]
        if a != b:
            diffs.append((cause, setting, a, b))
if diffs:
    ok = False
    for d in diffs:
        notes.append(f"CELL DIFF cause={d[0]!r} setting={d[1]!r} indep={d[2]} exp={d[3]}")
else:
    notes.append("all 42 cells MATCH (indep == expected)")

# metadata
for k in ("source", "url", "snapshot_sha256"):
    notes.append(f"expected.{k} = {exp.get(k)!r}")
notes.append(f"indep.source_url = {indep.get('source_url')!r}")

# counts
n_true_exp = sum(sum(1 for v in r if v) for r in er.values())
n_true_ind = sum(sum(1 for v in r if v) for r in ir.values())
notes.append(f"true-cell count: expected={n_true_exp} independent={n_true_ind}")

# order sensitivity: if settings were reordered, would the matrix still 'match'?
settings_exp = exp["settings"]
swapped = ["no", "always", "on-failure", "on-success", "on-abnormal", "on-abort", "on-watchdog"]
if settings_exp != swapped:
    notes.append("expected settings order is NOT the alphabetical/semantic-listing order "
                 "'no,always,on-success,on-failure,...' -> matrix is order-sensitive by construction")

print("\n".join(notes))
print("VERDICT:", "MATCH" if ok else "MISMATCH")
sys.exit(0 if ok else 1)
