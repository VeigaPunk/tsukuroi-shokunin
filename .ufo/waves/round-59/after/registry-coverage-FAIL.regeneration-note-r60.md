# Registry-coverage gate-failure receipt — regeneration note (round 60)

Routed defect R59-GATE-FAIL-RECEIPT-UNLANDED (r59 closure note 1): the intermediate FAIL reading of
`tools/check-registry-coverage.py` at the round-59 work revision `2913b75d` — the R59-REGISTRY-TABLE-GAP
state, narrated in `corpus/lessons/round-59.md`, the LOG and the r59 after-battery — was retained only in
the r59 round scratch, which was deleted with the round; the raw gate JSON of that failing run was never
committed. The bde06613 rule (commit gate-failure receipts under their honest names, beside the fixed
pass) applies to gate receipts, not only probe receipts.

This directory now carries:

- `registry-coverage-FAIL-at-2913b75d.regenerated-r60.json` — the raw JSON output of
  `python tools/check-registry-coverage.py --revision 2913b75d` re-run 2026-11-01 (round 60) from the
  committed gate code at lane head `5dd83fa3` (run directory: the lane repo; output redirected verbatim).
  It is a REGENERATION, not the r59 run's original bytes — byte-equality to the deleted original is NOT
  claimed and cannot be checked; it reproduces the recorded counts exactly: registered 95, rows_total 95,
  findings 1 (REGISTRY-ROW-MISSING for `tools/recheck-eventlog-r59.sh`), status FAIL — the "95/95/1"
  reading named in the r59 lesson, LOG and after-battery. The repair (rows made contiguous, no row bytes
  changed) landed at `c4aa0f5c`; the gate reads PASS 96/96/0 at the r59 final tree and at `5dd83fa3`
  (re-run this round, same command, revision `5dd83fa3`).

Going-forward rule (binding from round 60): when a gate red state is part of a repair story, the raw gate
receipt is committed beside the correction in the same round, under a name carrying FAIL, the revision it
was taken at, and whether it is an original run or a regeneration.
