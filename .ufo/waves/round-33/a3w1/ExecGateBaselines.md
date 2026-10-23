# ExecGateBaselines — no-harm baselines for the C1 change (round 33, attempt 3, wave a3w1)

VERDICT: baselines complete and usable — at revision `9c89ff4f093d07a6f92925518310ca6a7c8a2fa0` three of the six assigned gates are red at the base (pause-gate exit 1, registry-coverage exit 1, self-assessment exit 1), all 25 `_revision`-importing selftests exit 0, and the one measured no-harm constraint is that any byte change to `tools/_revision.py` flips `check-pause-gate` and `report-red-causes` to exit 2 unless both digest pins are bumped in the same commit. This seat is a baseline, not a C1 control, so no MEETS / DOES NOT MEET is asserted against the C1 after-value.

## 1. What was run and how it is bound

1. [obs] All 33 receipts (six gate, 25 selftest, two pin-simulation) were issued through the lane's `tools/run-receipt.py` (bytes identical at `9c89ff4f` and at the working-copy HEAD `5a967ce2`; `git diff --stat 9c89ff4f HEAD -- tools/run-receipt.py` printed nothing, exit 0), invoked from `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` with `--lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --revision 9c89ff4f093d07a6f92925518310ca6a7c8a2fa0 --tool-revision 9c89ff4f093d07a6f92925518310ca6a7c8a2fa0`, so each tool ran from a private clone checked out at that revision with every inherited `GIT_*` removed and global/system git config off.
2. [obs] Every one of the 31 gate and selftest receipt headers names `revision` = `tool_revision` = `9c89ff4f093d07a6f92925518310ca6a7c8a2fa0` (the two pin-simulation receipts name their own variant `eb73d5d9…`, section 4), and every one of those receipts' `tool_sha256` equals `sha256(git show 9c89ff4f:tools/<tool>.py)`; checked programmatically over all 31 gate and selftest receipts: `digest mismatches: []`. The receipts are therefore byte-bound to the revision, not to the working copy.
3. [obs] Each gate ran the entry form the lane registry gives it (`SKILL.md`, heading `## Gate and probe registry — round32 superseding current rows`, near line 2756): `--revision <REV>` only; optional flags (`--baseline-tools`, `--audit-live-map`, `--paths`, `--exec-log`, `--registry-from`, `--ownership-corrections`) were omitted, so the baseline is the minimal registry form. No gate was run with a loosening flag.
4. [obs] `1f521b93` (the claim base) is an ancestor of `9c89ff4f` (`git merge-base --is-ancestor 1f521b93 9c89ff4f`, exit 0), so the bound revision contains the base and adds only the round-33 declaration and probe-amendment commits.

## 2. Gate table (six assigned gates, revision `9c89ff4f`)

| Tool | Exit | One-line result | Receipt (absolute) |
|---|---|---|---|
| `tools/check-adjacency-anchors.py` | 0 | PASS: `inbound_total` 114 all classified (97 RESOLVES, 17 DRIFTED, 0 UNRESOLVABLE), `live_object_match` 10 of 10, `outbound_portable` 10 of 10, `findings` [] | `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w1/ExecGateBaselines/base-check-adjacency-anchors.jsonl:2` |
| `tools/check-pause-gate.py` | 1 | FAIL: 4 of 5 premises verified; P3 `unverified` with problem `verdict-unverified-not-counted`; P1, P4, P5 `changed`, P2 `cleared` | `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w1/ExecGateBaselines/base-check-pause-gate.jsonl:2` |
| `tools/check-registry-coverage.py` | 1 | FAIL: one finding `REGISTRY-ROW-MISSING` at `tools/probe-child-env-allowlist-r33.py`; `registered` 47, `rows_total` 47, `tools_total` 48 | `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w1/ExecGateBaselines/base-check-registry-coverage.jsonl:2` |
| `tools/check-recheck-commands.py` | 0 | PASS: `file_count` 52, `clean_count` 36, `flagged_count` 0, `invocation_count` 81, `resolved_count` 16, `pointer_section_count` 42, `findings` [] | `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w1/ExecGateBaselines/base-check-recheck-commands.jsonl:2` |
| `tools/check-self-assessment.py` | 1 | FAIL: 26 of 27 checks match; K10 mismatch, depth row states 40 lesson files, `corpus/lessons` holds 41 | `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w1/ExecGateBaselines/base-check-self-assessment.jsonl:99-106` |
| `tools/report-red-causes.py` | 0 | PASS: 268 of 268 findings attributed (267 with a recorded operation, 1 seat-level), `preserved` true, `pin_mismatches` [], `split_matches` true, `unattributed` [], frozen checker `CANNOT_EVALUATE` and the incomplete seat `ConnFxPlanner` preserved, 14 causes | `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w1/ExecGateBaselines/base-report-red-causes.jsonl:2` |

### 2.1 Red gates at the base, with their finding

5. [obs] `check-pause-gate` is red for a substantive premise, not for a byte pin: `premises_verified` 4 of `premises_total` 5, finding `{"id": "GATE-PREMISE", "site": "P3:verdict-unverified-not-counted"}` (`base-check-pause-gate.jsonl:2`). P3's sources are S109, S095, S110, S111, S112 and its verdict is `unverified`. At this revision `tools/_revision.py` hashes to `06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf`, which is exactly the value pinned in `tools/check-pause-gate.py:245`, so the red is not `GATE-BINDER-BYTES` and the pin is currently satisfied.
6. [obs] `check-registry-coverage` is red because the round-33 probe has no operative row: `{"id": "REGISTRY-ROW-MISSING", "site": "tools/probe-child-env-allowlist-r33.py", "detail": "no operative row names this regular tools/ file"}`, 47 rows against 48 tool files. `git show 9c89ff4f:SKILL.md | grep -c probe-child-env-allowlist-r33` → 0. This is the base state that the C1 after-work must not be blamed for, and it is the L1's row to add (QUALITY 70: a tool lands with its row); I did not edit `SKILL.md`.
7. [obs] `check-self-assessment` is red on one check: K10, `stated` 40, `observed` 41, reason "depth row states 40 lesson files; corpus/lessons holds 41 files", `stated_line` 1303 (`base-check-self-assessment.jsonl:99-106`). The stated value is at `git show 9c89ff4f:SCORECARD.md | sed -n '1303p'` → the depth row containing "`corpus/lessons/` (40 files)"; the observed value is `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin ls-tree 9c89ff4f corpus/lessons/ | wc -l` → 41. K01 to K09 and K11 to K27 match. [inf] The 41st file is the round-32 lesson added after the depth row was written; the row was not re-counted at `9c89ff4f`.
8. [obs] The other three gates are green at the base with the exact verdict lines in section 2. Together, the before-state the C1 change is compared against is: pause-gate 1 (P3), registry-coverage 1 (missing probe row), self-assessment 1 (K10), adjacency-anchors 0, recheck-commands 0, report-red-causes 0.

## 3. Selftests of every `tools/` file that imports `_revision` (25 tools)

9. [obs] The importer set was derived by AST (`ast.Import` / `ast.ImportFrom` with module `_revision`) over `tools/*.py`, not by substring: 25 files, every one of which has a `--selftest` mode. `tools/check-self-assessment.py`, `tools/check-report-receipts.py`, `tools/check-revision-binding.py` and `tools/probe-child-env-allowlist-r33.py` mention `_revision` in text or strings but do not import it; `check-self-assessment` is therefore in the gate table above, not in this set. `tools/_revision.py` itself imports nothing and is not in the set.
10. [obs] All 25 selftest receipts exited 0 and printed a PASS summary with zero failures. Each ran as `tools/<tool>.py --selftest` at `9c89ff4f`, `--out selftest-<tool>.jsonl`, maximum 3 concurrent `run-receipt.py` processes.

| Tool | Exit | Cases (from the receipt) |
|---|---|---|
| check-adjacency-anchors | 0 | PASS, 25 cases, 0 failed |
| check-appended-notices | 0 | PASS, 47 cases, 0 failed |
| check-boot-chain | 0 | PASS, 83 cases, 0 failed |
| check-boot-writers | 0 | PASS, 12 cases, 0 failed |
| check-boundary-contract | 0 | PASS, 28 cases, 0 failed |
| check-edit-contract | 0 | PASS, 102 cases, 0 failed |
| check-freshness-r17 | 0 | PASS, 59 cases, 0 failed |
| check-kernel-taint | 0 | 56 cases, `failed` 0 |
| check-locator-clarification | 0 | PASS, 37 cases, 0 failed |
| check-memory-pressure | 0 | 41 cases, `failed` 0 |
| check-path-reconciliation | 0 | PASS, 40 cases, 0 failed |
| check-pause-gate | 0 | PASS, 24 cases, 0 failed |
| check-recheck-commands | 0 | PASS, 95 of 95 |
| check-registry-coverage | 0 | PASS, 23 cases, 0 failed |
| check-review-cohort | 0 | PASS, 24 cases, 0 failed |
| check-review-snapshots | 0 | PASS, 24 cases, 0 failed |
| check-root-dac-correction | 0 | PASS, 54 cases, 0 failed |
| check-seat-bindings | 0 | PASS, 121 cases (73 v1, 48 v2), 0 failed |
| check-seat-scope | 0 | PASS, 54 cases, 0 failed |
| check-section-citations | 0 | PASS, 68 cases, 0 failed |
| check-selector-contract | 0 | 28 cases, `failures` [] |
| check-source-scope-correction | 0 | PASS, 29 cases, 0 failed |
| check-storage-health | 0 | 44 cases, `failed` 0 |
| measure-update-recheck | 0 | PASS, 20 cases, 0 failed |
| report-red-causes | 0 | PASS, 12 cases, 0 failed |

11. [obs] Receipt files are `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w1/ExecGateBaselines/selftest-<tool>.jsonl`; the five tools that also have a gate receipt (`check-adjacency-anchors`, `check-pause-gate`, `check-registry-coverage`, `check-recheck-commands`, `report-red-causes`) keep both files, so the gate receipt name `base-<tool>.jsonl` is not overwritten by a selftest.
12. [obs] Selftests are hermetic only by their own fixtures; every one runs in the runner's private clone with a private `HOME` and `XDG_CONFIG_HOME` (`tools/run-receipt.py:44-52,100-113`), and no selftest wrote into the lane. The only files this seat created are listed in the Scope line.

## 4. The no-harm constraint the C1 change must satisfy (measured, not inferred)

13. [obs] Two gates pin the exact bytes of `tools/_revision.py`: `tools/check-pause-gate.py:244-246` compares `sha256(tools/_revision.py)` to `06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf` and exits 2 with `GATE-BINDER-BYTES` on mismatch; `tools/report-red-causes.py:202-205` compares the same digest and exits 2 with `RED-CAUSES-READ` ("revision binder differs from the claim-base bytes"). The pinned value equals the file's bytes at `9c89ff4f` (`sha256sum tools/_revision.py` and `git show 9c89ff4f:tools/_revision.py | sha256sum` both `06b71e8c…`).
14. [obs] Measured consequence, in my own sandbox clone (`/fast/scratch/hyaku/tsukuroi-r33a3/ExecGateBaselines/repo`, push URL disabled, commit `eb73d5d9e9c941a9f65aa8f05eb1861e49dc4418` = `9c89ff4f` plus one appended comment line in `tools/_revision.py`, new digest `55f808af6a6a1d9756353d302ba14e8251fe63ac871fdb34311175939d4f484a`, patch at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w1/ExecGateBaselines/pinsim.patch`, sha256 `4243eed227ea81d058a8f922739d3692f70497206db34078b775695c680c24b1`): `check-pause-gate` → exit 2, `{"status": "CANNOT_EVALUATE", "findings": [{"id": "GATE-BINDER-BYTES", ...}]}` (`pinsim-check-pause-gate.jsonl:2,3`) and `report-red-causes` → exit 2, `{"status": "CANNOT_EVALUATE", "findings": [{"id": "RED-CAUSES-READ", "site": "revision binder differs from the claim-base bytes"}]}` (`pinsim-report-red-causes.jsonl:2,3`). This is a pin-behaviour simulation for the baseline, not a score of the C1 change, which does not exist yet.
15. [obs] Therefore the no-harm condition on the C1 commit is exact: `tools/_revision.py` changing bytes requires bumping both pins in the same commit, and the pinned digest after the change must be the sha256 of the committed `_revision.py`. If the pins are bumped, the comparison to this baseline is exit 1 for pause-gate (P3 still unverified) and exit 0 for report-red-causes; if they are not bumped, both are exit 2 and the P3 red is masked rather than preserved.
16. [obs] The second builder named by C1, `tools/mutants-owed-statements-r29-v4shapes.py`, is not pinned by any gate: `grep -rn mutants-owed-statements-r29-v4shapes tools/*.py` finds only a docstring mention at `tools/check-owed-statements-r29.py:38` and the frozen probe's target list at `tools/probe-child-env-allowlist-r33.py:19,125`. No digest pin has to follow that file's bytes. [obs] It also has no `--selftest` and does not import `_revision`, so it is outside both tables in sections 2 and 3; its independent entry form in the registry is `--base <REV> (--counter-rev <REV> | --counter-file <PATH>)`.
17. [inf] The 25 selftest results and the three green gates are the clean-set the C1 change must preserve: a change to `clean_env()` feeds the git children of `check-adjacency-anchors`, `check-boot-writers`, `check-root-dac-correction` selftests and of the gates that call `_revision.bind`, so a regression there would first show as a non-zero exit in these receipts. A dropped git setting (`GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`) would also be caught by the frozen probe's kept-settings clause, which is the L1's measurement, not this seat's.

## 5. Observations, inferences, unknowns

18. [obs] The three base reds (section 2.1) are pre-existing at `9c89ff4f` and none is attributable to this seat: I wrote no lane file, set no git variable to a lane path and ran no git write in the lane or in a sibling repository. The only git write was the simulation commit in my own sandbox clone under `/fast/scratch/hyaku/tsukuroi-r33a3/ExecGateBaselines/repo`.
19. [obs] The receipts record `lane_branches` from the real lane at run time; `check-adjacency-anchors` and `check-recheck-commands` report `branch_tip` `5a967ce26f60161e32304d4ec77420d2218b8fcb` (the lane's branch tip while bound at `9c89ff4f`), so the branch state at measurement time is pinned in the receipt header and the tool body.
20. [obs] `report-red-causes` legitimately runs its frozen checker at exit 2 (`checker_status` `CANNOT_EVALUATE`) while the gate itself exits 0, because its verdict is attribution completeness, not the checker's health; `preserved` true and `pin_mismatches` [] are the invariant lines.
21. [inf] The missing registry row for the round-33 probe (finding 6) will keep `check-registry-coverage` red until the L1 adds the row, so a post-C1 run of this gate is not comparable to the base unless the row lands first or the same finding is expected.
22. [unk] Whether the C1 change, once written, keeps the exact git-child counts of the base (279, 335, 203, 226, 1176 for the five frozen targets, per the declaration) is not measurable here: the change does not exist at `9c89ff4f` and this seat does not run the frozen probe.

## 6. Files written by this seat

- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w1/ExecGateBaselines.md` (this report)
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w1/ExecGateBaselines/base-check-{pause-gate,report-red-causes,registry-coverage,recheck-commands,self-assessment,adjacency-anchors}.jsonl` (6 receipts) plus the matching `base-*.runlog` runner outputs
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w1/ExecGateBaselines/selftest-<tool>.jsonl` (25 receipts) plus the matching `selftest-*.runlog` runner outputs
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w1/ExecGateBaselines/pinsim-{check-pause-gate,report-red-causes}.jsonl` + runlogs and `pinsim.patch` (pin-behaviour simulation)
- `/fast/scratch/hyaku/tsukuroi-r33a3/ExecGateBaselines/repo` (seat sandbox clone at `9c89ff4f` plus the simulation commit) and `selftest-tools.txt`

Scope: read=round-33 declaration and amendments at 9c89ff4f, SKILL.md gate registry near line 2756, SCORECARD.md axes row at 1303, tools/run-receipt.py, the six assigned gates and 25 selftest tools at 9c89ff4f, tools/_revision.py digest pins in check-pause-gate.py and report-red-causes.py; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w1/ExecGateBaselines.md, 6 base receipts + runlogs, 25 selftest receipts + runlogs, 2 pinsim receipts + runlogs and pinsim.patch under /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w1/ExecGateBaselines/, and the sandbox clone plus selftest-tools.txt under /fast/scratch/hyaku/tsukuroi-r33a3/ExecGateBaselines/; executed=33 run-receipt invocations (6 gates, 25 selftests, 2 pinsim) plus read-only git show/ls-tree/diff/merge-base and sha256sum in the lane, one git commit inside the sandbox clone only
Model: not exposed
Installs: none
