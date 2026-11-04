## Capability refresh (round 73, append-only) — gate-selftest is ten cases

The `gate-selftest` capability row above (round 72) still says "nine named cases" and `PASS 9/9`. The
landed instrument prints ten cases — `SELFTEST: PASS (10 cases, 10 passed, 0 failed)`, rc 0, receipt
`.ufo/waves/round-72/after/selftest-selftest-after.txt` — with named ids SELFTEST-MATCH,
SELFTEST-MISMATCH, SELFTEST-LABEL, SELFTEST-SUPERSEDED, SELFTEST-OUT-OF-SCOPE, SELFTEST-NO-RECEIPT,
SELFTEST-GREEN-DIFF, SELFTEST-MIXED, SELFTEST-HERMETIC and SELFTEST-CASES; the tenth is the case-count
guard that fails when a declared case row is deleted. The row text stays as filed; read it with this
block as its current count.

Counted by `python3 tools/check-r72-routed-r73.py --revision <REV>` (item CAPABILITY).
