# C2 `--selftest` — E2GateSelftest (round 72, w1)

Draft seat: this report is the only advisory output; the L1 owns the lane tree. Two drafts are
recorded here: **v1** (9 cases), whose bytes are now the live worktree tool, and **v2** (10 cases,
38-line delta) which closes the case-set hole found by the mutation tester after v1 landed.

## Frozen digests (read this before quoting any figure)

| version | sha256 | cases | state |
|---|---|---|---|
| committed base `a7015d27` | `b0f839e3955529caf560576f02f5c4137a98317d82c90cf1225dffe45d366c6d` | 0 (`--selftest` rc 2, usage) | declared do-nothing control |
| pre-existing worktree variant | `e47baa781ed4f45c9b5d6fcbc384718ad13db0bc376e9152f0ab98b45e25274d` | 7 | replaced by v1; **not** the report's patch base any more |
| **v1 draft** (= live worktree tool at 22:47) | `af46203c8ca983841ae5f049e706e5037e416013e72bca03333cbbbfbd5a2abb` | 9 | landed in the worktree; `selftest.patch` base was `e47baa78`, result is this |
| **v2 draft** (delta on v1) | `f22eb94f1ed86157d94875d0943b5ec62fba8214dd520e7eb4d645969b283464` | 10 | `selftest-v2.patch`, not applied |

## Artifacts

| path | what |
|---|---|
| `…/w1/E2GateSelftest/selftest.patch` | v1 unified diff, 189 lines (+103/−40), base `e47baa78` → `af46203c` |
| `…/w1/E2GateSelftest/selftest-after.txt` | v1 green run (9 cases), r70 self-demo, `/tmp` audit |
| `…/w1/E2GateSelftest/redbefore.txt` | v1 9-mutant matrix (M1 = the declared red-before) |
| `…/w1/E2GateSelftest/selftest-v2.patch` | v2 delta, 38 lines, base `af46203c` → `f22eb94f` |
| `…/w1/E2GateSelftest/selftest-v2-after.txt` | v2 green run (10 cases), apply audit, unchanged self-demo |
| `…/w1/E2GateSelftest/redbefore-v2.txt` | v2 11-mutant matrix, incl. M10/M11 row-deletion |

## Axes

- **operability (9).** A real hermetic gate: one `mkdtemp` root under `$TMPDIR`, receipt/diff
  fixtures written and read back per case, 10 named case lines, exact final line, exit 0 only when
  every case passes.
- **C2 (nothing harmed).** Scoring semantics, the `SWEEP …` summary line, `OK`/`SKIP` forms and the
  r70 self-demo are byte-identical; finding ids are appended after the existing tokens.

## Touched functions and line ranges (v2, 215 lines)

| lines | function | change vs committed base |
|---|---|---|
| 13–22 | module docstring | `--selftest` in Usage/Exit, TMPDIR/fixture/id paragraph, `SELFTEST-CASES` sentence |
| 30–36 | imports | `os`, `shutil`, `tempfile` |
| 42–44 | `FINDING` (new), `DECLARED` (new) | three stable finding ids; the 9 declared case ids |
| 45–85 | `sweep()` (moved out of `main`) | body unchanged; ids appended at 49, 76, 81 |
| 87–91 | `score_files()` (new) | read a receipt file + a `-U0` diff file, score via `sweep` |
| 93–189 | `selftest()` (new) | TMPDIR 95–101, root 102, case table 104–149, fixture writer 137–141, runner 151–165, cleanup 167, hermetic 169–177, case-set guard 178–181, reporting 183–189 |
| 192–211 | `main()` | `--selftest` branch 193–194; everything else is the committed base logic |

All scoring output goes through `out` (`print` count inside `sweep`/`score_files` = 0), which is
what lets the suite assert exact lines.

## Cases (10) and the mutant that kills each

| case | pins | killed by |
|---|---|---|
| `MATCH` | matching cases figure → `OK`, rc 0 | M8, M9 |
| `MISMATCH` | rc 1, `SWEEP-MISMATCH`, anchor `tally-fixture.md:2` | M1 (declared red-before), M8, M9 |
| `LABEL` | rc 1, `SWEEP-LABEL`, `label_figure=3 receipt=4` | M2, M9 |
| `SUPERSEDED` | rc 0, `SKIP`, `skipped_superseded=1`, no `cases_figure` | M3, M9 |
| `OUT-OF-SCOPE` | battery "11 cases" never scored, rc 0 | M4 |
| `NO-RECEIPT` | rc 2, `SWEEP-NO-RECEIPT` | M5 |
| `GREEN-DIFF` | rc 0 **and** the exact `SWEEP added_figures_mismatched=0 … receipt_cases=218 receipt_labels=4` line | M6, M8 |
| `MIXED` | one OK + one bad → rc 1, `added_figures_mismatched=1` | M1, M9 |
| `HERMETIC` | root under `$TMPDIR`, all fixtures under the root, none under `/tmp`, root removed | M7 |
| `CASES` | executed id list equals the pinned `DECLARED` manifest, ids unique | M10, M11 |

`redbefore-v2.txt`: **11 mutants, 11 caught, cases_covered=10, vacuous_cases=none**.

## Case-set size is not self-verifiable (M1Mutation's finding, and what v2 does about it)

M1Mutation measured, correctly, that in v1 deleting any single case row was invisible: `total`
re-derives from `results`, so a truncated suite still printed `SELFTEST: PASS (8 cases, 8 passed,
0 failed)` — including when the only rc-2 case (`NO-RECEIPT`) was removed.

v2 answers the measured mutation: `DECLARED` pins the nine ids at module level, and the tenth case
compares the executed id list against it, so M10 (delete the `NO-RECEIPT` row) and M11 (delete the
hermetic append) both fail `SELFTEST-CASES` with `observed=… declared=…` and rc 1.

The limit is honest and must be stated in any closure check: deleting a row **and** its `DECLARED`
entry is still invisible, because completeness of a test suite cannot be proven from inside it. The
authoritative count is external and cheap:

```
python3 tools/check-selftest-tally.py --selftest | grep -c '^PASS (SELFTEST-'   # -> 10
python3 tools/check-selftest-tally.py --selftest | tail -1                       # -> SELFTEST: PASS (10 cases, 10 passed, 0 failed)
```

That count against the round's declared `N` (frozen predicate `N >= 7`, declared 9 in v1, 10 in v2)
is the closure guard; the `CASES` line only makes accidental single-row loss loud.

## Evidence

- v1 (`af46203c`) `--selftest` rc 0, 9 case lines, `SELFTEST: PASS (9 cases, 9 passed, 0 failed)`.
- v2 (`f22eb94f`) `--selftest` rc 0, 10 case lines, `SELFTEST: PASS (10 cases, 10 passed, 0 failed)`;
  root under `$TMPDIR`, removed before exit.
- v2 patch applies to the live bytes: `git apply --check` rc 0, applied file byte-equal to the
  tested file, applied copy `--selftest` rc 0.
- existing mode unchanged, from the lane root read-only:
  `SWEEP added_figures_mismatched=0 skipped_superseded=0 receipt_cases=214 receipt_labels=18`, rc 0.
- `/tmp` audit: `selftest-tally-*` entries before/after = 0; fixtures lived in `$TMPDIR` and the
  tree was deleted.

## Risks / hand-off

- v1 already landed; v2 is a 38-line delta on those exact bytes (three hunks: docstring, manifest
  line, guard block). On drift use `patch -p1 --fuzz=3`, then re-run `--selftest` and the self-demo.
- Any closure receipt for C2 must count case lines externally and quote the digest it measured
  (`af46203c` → 9, `f22eb94f` → 10); the two are not interchangeable.
- Exit map: `0` all cases pass, `1` a case fails, `2` usage or an unusable `TMPDIR`.
- No tools installed or upgraded; no pacman transaction; no writes outside this seat's paths and its
  scratch tree (removed at exit).
