## Round-72 registry row update — `selftest-tally`, the Self-test column

Append-only replacement row for the `## Gate and probe registry — round71 superseding current rows`
table. The r71 row stays as written; this row is the round-72 continuation and carries the tool's own
`--selftest` mode in the Self-test column (the r71 cell's "self-demo on the r70 added lines" is the mode
it replaces). The other cells are carried, with the fixture root named in the pinned-values and
write-scope cells.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| selftest-tally | gate | `python3 tools/check-selftest-tally.py --receipt <FILE> --label <TOKEN> --range <A>..<B> -- <paths>` | 0 every added figure equals the receipt line; 1 mismatch; 2 no receipt line or usage | `python3 tools/check-selftest-tally.py --selftest` — hermetic, nine cases over fixtures written under one `$TMPDIR` root: MATCH, MISMATCH (finding `SWEEP-MISMATCH` with `file:line`), LABEL (`SWEEP-LABEL`), SUPERSEDED (printed as `SKIP`), OUT-OF-SCOPE battery figure (not scored), NO-RECEIPT (`SWEEP-NO-RECEIPT`, core returns 2), GREEN-DIFF, MIXED, and HERMETIC (every fixture under `$TMPDIR`, away from `/tmp`, root removed); one `PASS (SELFTEST-<id>)`/`FAIL (SELFTEST-<id>)` line per case and last line `SELFTEST: PASS (9 cases, 9 passed, 0 failed)`; exit 0 when all cases pass, 1 when a case fails, 2 when `$TMPDIR` is set but is not a directory (`SELFTEST: FAIL (1 cases, 0 passed, 1 failed)`) — the core keeps its 0/1/2 map (2 on no receipt line or usage), and the NO-RECEIPT case asserts the core's 2 | R71 added-line scope; figures read from `PASS (N cases, N passed, N failed)` and the label count; `--selftest` writes its fixtures under `$TMPDIR` and removes the root, no hardcoded `/tmp` | committed reads; `git diff -U0` read-only; selftest fixtures under `$TMPDIR` | tsukuroi |

Landing notes for the L1 (not part of the row): the case set and summary were observed on the
working-tree instrument (sha256 `af46203c8ca983841ae5f049e706e5037e416013e72bca03333cbbbfbd5a2abb` at
2026-11-03T22:43; `--selftest` rc 0, `SELFTEST: PASS (9 cases, 9 passed, 0 failed)`; a
`TMPDIR=/nonexistent-not-a-dir` run printed `FAIL (SELFTEST-TMPDIR)` and `SELFTEST: FAIL (1 cases, 0
passed, 1 failed)`, rc 2). The instrument changed twice during the wave (seven cases at 22:38, nine at
22:42), so re-read the committed blob at landing and move the case count and summary line with it.
Observed case ids: `MATCH`, `MISMATCH`, `LABEL`, `SUPERSEDED`, `OUT-OF-SCOPE`, `NO-RECEIPT`,
`GREEN-DIFF`, `MIXED`, `HERMETIC`.
