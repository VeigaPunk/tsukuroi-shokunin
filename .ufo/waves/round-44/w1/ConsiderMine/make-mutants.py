#!/usr/bin/env python3
"""Single-field mutants of the seat-harm ledger, one per claim the checker makes.

Each mutant is the real ledger with exactly one field altered so that one check
must go red. The checker is only a control if it can fail on the shape it
claims to detect, so the driver asserts the expected finding code per mutant
and that the unmutated ledger stays green.

  python3 make-mutants.py --ledger seat-harm.jsonl --out mutants/
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.dont_write_bytecode = True

# (mutant, row id, field, new value, expected finding code)
MUTANTS = [
    ("K01-cite-line-drift", "R39-SEAT-PKILL", "cite",
     "corpus/lessons/round-39.md:75", "SH-CITE-QUOTE"),
    ("K02-quote-paraphrase", "R40-TMP-MISROOT", "quote",
     "each run wrote a 294 MB lane archive under /tmp", "SH-CITE-QUOTE"),
    ("K03-id-tamper", "R39-SEAT-PKILL", "id", "R39-SEAT-KILL", "SH-ID-NOT-ON-LINE"),
    ("K04-class-unknown", "R44-PYCACHE-RECUR", "class",
     "lane-dirt", "SH-CLASS-UNKNOWN"),
    ("K05-id-duplicate", "R41-TMP-MISROOT-REPEAT", "id",
     "R40-TMP-MISROOT", "SH-ID-DUPLICATE"),
    ("K06-closed-without-proof", "R42-C1-SCRATCH-FALLBACK-TMP", "fix_quote",
     "", "SH-CLOSED-NO-PROOF"),
    ("K07-round-out-of-window", "R37-MISROOT-NOTE-DRAFT", "round",
     30, "SH-ROUND-OUT-OF-WINDOW"),
    ("K08-cite-missing-file", "R43-L1-SCRATCH-STRAY", "cite",
     "corpus/lessons/round-99.md:108", "SH-CITE-MISSING"),
    ("K09-fix-quote-invented", "R39-SEAT-PKILL", "fix_quote",
     "never signal another seat's process", "SH-FIX-QUOTE"),
    ("K10-observation-sha-tamper", "R44-PYCACHE-RECUR", "obs_sha256",
     "0" * 64, "SH-OBS-SHA"),
    ("K11-citation-escapes-lane", "R40-TMP-MISROOT", "fix_cite",
     "/tmp/receipt.md:1", "SH-FIX-ABSOLUTE"),
    ("K12-id-basis-unknown", "R44-FLEETROOT-FX", "id_basis",
     "assumed", "SH-ID-BASIS"),
    ("K13-minted-id-reuses-lesson-id", "R44-FLEETROOT-FX", "id",
     "R37-MISROOT-NOTE-DRAFT", "SH-ID-ALREADY-IN-LESSONS"),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rows = [json.loads(s) for s in open(a.ledger, encoding="utf-8") if s.strip()]
    by_id = {r["id"]: r for r in rows}
    os.makedirs(a.out, exist_ok=True)
    index = []
    for name, rid, field, value, code in MUTANTS:
        if rid not in by_id:
            print(f"CANNOT: {rid} absent from {a.ledger}", file=sys.stderr)
            return 2
        mutated = [dict(r) for r in rows]
        for r in mutated:
            if r["id"] == rid:
                r[field] = value
        path = os.path.join(a.out, name + ".jsonl")
        with open(path, "w", encoding="utf-8") as fh:
            for r in mutated:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        index.append({"mutant": name, "row": rid, "field": field,
                      "value": value, "expected": code, "path": path})
    with open(os.path.join(a.out, "index.jsonl"), "w", encoding="utf-8") as fh:
        for item in index:
            fh.write(json.dumps(item) + "\n")
    print(f"wrote {len(index)} mutants to {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
