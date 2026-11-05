# ExecTimeoutRed — round 83 w1 findings

Scope: red-before proof for the timeout arm of the mutation harness (R82-V4). Scratch only; no lane file edited. Full commands and verbatim outputs: `.ufo/waves/round-83/w1/ExecTimeoutRed/receipts.txt`.

## Verdicts

- **RED confirmed in the round-82 harness.** `tools/mutation-kill-r82.py` maps a timed-out selftest to `rc=124` and `run_selftest` returns that rc; `measure` counts `rc != 0` as killed. A selftest that does not finish is therefore scored as a kill. Reproduced with a 2 s copy of the harness (`killed=1`, record `killed: true, rc: 124`, detail `selftest-did-not-finish`) against a 30 s sleep mutant. Receipt (a).
- **Repair holds in the round-83 harness.** `tools/mutation-kill-r83.py --fixture <fx> --timeout 2` scores the same sleep mutant `killed=false, observed=false`, `unobserved=["T1-sleep"]`, `killed 0`. Receipt (b). Its `--selftest` is 6/6 (`SELFTEST total=6 passed=6 failed=0`, rc 0), including the timeout-is-not-a-kill case.

## Observations (not defects in the frozen instruments)

- The r83 harness's timeout arm works as specified at the lane's frozen commit. Its `run_selftest` returns `observed=False` on `TimeoutExpired` and `OSError`, and `measure` excludes unobserved records from `killed`.
- The r82 recipe file and r83 recipe file are not identical at the lane tip; this test used a fixture with the same recipe content under both paths, so it does not exercise the re-encoded `C16`/`M06` cells. That is outside this seat's claim.

## Limits

- Only the timeout arm was exercised, with one synthetic recipe. Did not run the 26-recipe battery or `round83-battery.py`.
- The 2 s bound is a test-only value. The default 300 s is unchanged in the frozen harness.

## Tooling

No installs or updates. Used system `/usr/bin/python3`.

## Checks for the L1 to run

- `python3 tools/round83-battery.py --instrument r83 --revision <REV>` (the timeout-arm repair is uncredited; this proof is supporting evidence only).
- Optionally: `python3 tools/mutation-kill-r83.py --selftest` in the landed lane (expect 6/6).
