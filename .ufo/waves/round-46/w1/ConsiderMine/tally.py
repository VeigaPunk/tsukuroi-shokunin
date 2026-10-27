#!/usr/bin/env python3
"""Tally the hand-keyed LOG-vs-spot-check extraction (log-vs-spotcheck.jsonl).

One row per statement both documents can speak to. Post-closure-only findings
(a defect the spot-check routes after the LOG entry was written) are out of the
denominator by construction: the LOG cannot carry them.

Prints per-round and per-class counts plus every mismatch, then a single
machine line. Exit 1 when a mismatch exists, 0 otherwise.
"""
import json
import sys
from collections import Counter, defaultdict

PATH = sys.argv[1] if len(sys.argv) > 1 else "log-vs-spotcheck.jsonl"
rows = [json.loads(line) for line in open(PATH) if line.strip()]

per_round = defaultdict(lambda: {"rows": 0, "match": 0, "mismatch": 0})
per_class = defaultdict(lambda: Counter())
mismatches = []
for r in rows:
    b = per_round[r["round"]]
    b["rows"] += 1
    b["match" if r["match"] else "mismatch"] += 1
    per_class[r["class"]]["rows"] += 1
    per_class[r["class"]]["mismatch" if not r["match"] else "match"] += 1
    if not r["match"]:
        mismatches.append(r)

for rnd in sorted(per_round):
    b = per_round[rnd]
    print(f"round {rnd}: comparable {b['rows']:2d}  match {b['match']:2d}  mismatch {b['mismatch']}")
print()
for cls in sorted(per_class):
    c = per_class[cls]
    print(f"class {cls:14s} rows {c['rows']:2d}  mismatch {c['mismatch']}")
print()
for m in mismatches:
    print(f"MISMATCH {m['row']} ({m['class']})")
    print(f"  LOG   {m['log_ref']}: {m['log']}")
    print(f"  SPOT  {m['spot_ref']}: {m['spot']}")
print()
total = len(rows)
bad = len(mismatches)
print(
    f"TSUKUROI_BURST_READ: rows={total} mismatch={bad} "
    f"rounds={len(per_round)} mismatch_rounds={len({m['round'] for m in mismatches})}"
)
sys.exit(1 if bad else 0)
