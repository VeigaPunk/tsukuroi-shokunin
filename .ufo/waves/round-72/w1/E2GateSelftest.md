# C2 `--selftest` draft — E2GateSelftest (round 72, w1)

Status: **draft patch, not applied.** This seat wrote only
`.ufo/waves/round-72/w1/E2GateSelftest/` (three artifacts) and this report; the L1 owns the lane tree.

## Artifacts and digests

| path | what | sha256 |
|---|---|---|
| `…/w1/E2GateSelftest/selftest.patch` | unified diff, 189 lines (+103 / −40), `a/tools/check-selftest-tally.py` → `b/…` | `e7895cf695db93e3…4706ed` |
| `…/w1/E2GateSelftest/selftest-after.txt` | green `--selftest` run, unchanged r70 self-demo, `/tmp` audit | `3351c24fe26e04e3…dc411c` |
| `…/w1/E2GateSelftest/redbefore.txt` | 9-mutant matrix (M1 = the declared red-before) | `0a611df0cb18372e…2848bb0` |

Patch base: the **uncommitted worktree** bytes of `tools/check-selftest-tally.py`,
sha256 `e47baa781ed4f45c9b5d6fcbc384718ad13db0bc376e9152f0ab98b45e25274d` (the L1's 7-case
version, re-hashed against the live lane file just before filing). Patched bytes
`af46203c8ca98384…bd5a2abb`. Checked in scratch: `git apply --check` OK, `patch -p1 --dry-run`
OK, applied copy is byte-identical to the tested copy, that copy runs `--selftest` rc 0. The
patch does **not** apply to the committed base `a7015d27` (digest `b0f839e3…`); if that version
is restored, transplant the tested file instead.

## Delta against the worktree version (why the patch is still needed)

1. **No fixture is ever written.** The worktree `selftest()` contains **0** `write_text` calls:
   the temp root is created and immediately removed, so "builds every fixture under `$TMPDIR`"
   is not met and a verifier finds an empty root. The patch writes each case's receipt and diff
   as files under one root, reads them back, and scores them through `score_files()`.
2. **No stable finding id.** Worktree mismatch lines are `MISM A.md:1 cases_figure=217
   receipt=218` with no id, and the no-receipt line has none. The frozen C2 predicate requires
   "a mismatched figure (fail with a stable finding id)". The patch appends
   `[SWEEP-MISMATCH]`, `[SWEEP-LABEL]`, `[SWEEP-NO-RECEIPT]` **after** the existing tokens, so
   every prior substring match still holds.
3. **Host hardcode.** Worktree: `base = os.environ.get("TMPDIR") or "/fast/scratch/hyaku"`, and
   a set-but-missing `TMPDIR` silently falls through to the platform temp dir. The patch uses
   `$TMPDIR` when set (named `FAIL (SELFTEST-TMPDIR)` + rc 2 when it is not a directory) and
   `tempfile.gettempdir()` only when `TMPDIR` is unset — no host path anywhere.

## Touched functions and line ranges (patched file)

| lines | function | change |
|---|---|---|
| 13–21 | module docstring | adds the `--selftest` line to Usage/Exit and the TMPDIR/id paragraph |
| 30–36 | imports | `os`, `shutil`, `tempfile` |
| 42 | `FINDING` (new) | one table for the three stable finding ids |
| 45–85 | `sweep()` (moved out of `main`) | body unchanged; ids appended at 49, 76, 81 |
| 87–91 | `score_files()` (new) | read one receipt file + one `-U0` diff file, score through `sweep` |
| 93–186 | `selftest()` (new) | TMPDIR resolution 95–101, root 102, case table 104–149, fixture writer 137–141, runner 151–165, cleanup 167, hermetic evaluation 169–177, reporting 180–186 |
| 189–208 | `main()` | `--selftest` branch at 190–191; every other line is the committed base's logic |

All scoring output goes through `out` (`print` count inside `sweep`/`score_files` = 0), which is
what lets the selftest assert on exact lines.

## Cases (9) and the mutant that kills each

| case | pins | killed by |
|---|---|---|
| `MATCH` | a matching cases figure scores `OK`, rc 0 | M8 inverted predicate, M9 all-skip |
| `MISMATCH` | rc 1, `SWEEP-MISMATCH`, anchor `tally-fixture.md:2` from the hunk header | M1 (declared red-before), M8, M9 |
| `LABEL` | rc 1, `SWEEP-LABEL`, `label_figure=3 receipt=4` | M2, M9 |
| `SUPERSEDED` | rc 0, `SKIP`, `skipped_superseded=1`, no `cases_figure` | M3, M9 |
| `OUT-OF-SCOPE` | battery "11 cases" not scored, rc 0 | M4 |
| `NO-RECEIPT` | rc 2, `SWEEP-NO-RECEIPT` | M5 |
| `GREEN-DIFF` | rc 0 **and** the exact `SWEEP added_figures_mismatched=0 … receipt_cases=218 receipt_labels=4` line | M6, M8 |
| `MIXED` | one OK + one bad → rc 1, `added_figures_mismatched=1` | M1, M9 |
| `HERMETIC` | root under `$TMPDIR`, every fixture under the root, none under `/tmp`, root removed | M7 |

`redbefore.txt` records the full matrix: **9 mutants, 9 caught, cases_covered=9,
vacuous_cases=none** — no case passes vacuously. M1 is the receipt the declaration names:
`ok = v == n` → `ok = True` in the CASE loop gives rc 1 with `SELFTEST-MISMATCH` failing.

## Evidence

- base `a7015d27` (tool `b0f839e3…`): `--selftest` rc **2**, **0** case lines — matches the
  declaration's do-nothing control.
- worktree `e47baa78…`: `--selftest` rc 0, 7 case lines, 0 fixture writes.
- patched `af46203c…`: `--selftest` rc **0**, 9 case lines,
  `SELFTEST: PASS (9 cases, 9 passed, 0 failed)`; root under `$TMPDIR`, removed before exit.
- existing mode unchanged, run from the lane root read-only:
  `SWEEP added_figures_mismatched=0 skipped_superseded=0 receipt_cases=214 receipt_labels=18`,
  rc **0** (frozen r70 verdict).
- `/tmp` audit: `selftest-tally-*` entries before and after = 0; fixtures lived in
  `$TMPDIR=/fast/scratch/hyaku/tsukuroi-r72/E2GateSelftest/tmp` and the tree was deleted.

## Risks / hand-off

- Apply against the worktree bytes above; the diff context comes from that file. On drift,
  `patch -p1 --fuzz=3` then re-check the 9 cases (the added block is self-contained; the only
  in-`sweep` edits are the three appended ids).
- If the worktree 7-case version is kept instead, at minimum add the three finding ids and
  make the cases write and read fixtures on disk — otherwise the frozen C2 wording (stable id,
  fixtures under `$TMPDIR`) is not met on inspection.
- Exit map is exactly `0` all cases pass, `1` a case fails, `2` usage or unusable `TMPDIR`;
  `--selftest` never returns 2 for a passing suite.
- No tools installed or upgraded; no pacman transaction; no writes outside this seat's paths and
  its scratch tree.
