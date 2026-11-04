## Round-72 registry row update — `selftest-tally`, the Self-test column

Append-only replacement row for the `## Gate and probe registry — round71 superseding current rows`
table. The r71 row stays as written; this row is the round-72 continuation and carries the tool's own
`--selftest` mode in the Self-test column (the r71 cell's "self-demo on the r70 added lines" is the mode
it replaces). Everything else in the row is carried, with the fixture root named in the pinned-values and
write-scope cells.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| selftest-tally | gate | `python3 tools/check-selftest-tally.py --receipt <FILE> --label <TOKEN> --range <A>..<B> -- <paths>` | 0 every added figure equals the receipt line; 1 mismatch; 2 no receipt line or usage | `python3 tools/check-selftest-tally.py --selftest` — hermetic, seven cases over fixtures it builds under one `$TMPDIR` root (match; mismatch printing `MISM <file>:<line>`; label-mismatch; superseded-figure quote printed as `SKIP`; out-of-scope battery figure not scored; receipt with no `PASS (N cases, ...)` line whose core returns 2; green control), one named `PASS (SELFTEST-<id>)`/`FAIL (SELFTEST-<id>)` line per case and last line `SELFTEST: PASS (7 cases, 7 passed, 0 failed)`; exit 0 when all cases pass, 1 when a case fails — the core keeps its 0/1/2 map (2 on no receipt line or usage), and the no-receipt-line case asserts the core's 2 | R71 added-line scope; figures read from `PASS (N cases, N passed, N failed)` and the label count; `--selftest` builds and removes its own fixtures under `$TMPDIR` (fallback `/fast/scratch/hyaku`) | committed reads; `git diff -U0` read-only; selftest fixtures under `$TMPDIR` | tsukuroi |

Landing notes for the L1 (not part of the row): the case count and the printed summary were observed on
the working-tree instrument (sha256 `e47baa781ed4f45c9b5d6fcbc384718ad13db0bc376e9152f0ab98b45e25274d`,
`--selftest` rc 0) at 2026-11-03, not on a committed blob; if the landed instrument's case set differs,
the two figures in the Self-test cell move with it. The seven case ids observed were `SELFTEST-match`,
`SELFTEST-mismatch`, `SELFTEST-label-mismatch`, `SELFTEST-superseded-skip`, `SELFTEST-out-of-scope`,
`SELFTEST-no-receipt-line` and `SELFTEST-green-control`.
