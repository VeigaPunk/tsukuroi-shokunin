# SelftestsAfterNoHarm — no-harm re-run of the 25 `_revision`-importer `--selftest`s at f761fade (round 33, attempt 3, wave a3w2)

NO HARM: all 25 selftests of the `tools/` modules that import `_revision` were re-run at `f761fade8a452ec9dd0831be7743601b0adda3e5` through `tools/run-receipt.py` (`--revision f761fade8a452ec9dd0831be7743601b0adda3e5 --tool-revision f761fade8a452ec9dd0831be7743601b0adda3e5 -- tools/<t>.py --selftest`, parallelism ≤ 3, one run per tool) and every one exited 0 with tool stdout byte-identical to the wave-a3w1 baselines — 0 exit differences, 0 case-count differences, 25 of 25 pairs, no timeout, empty `stderr_tail` in every receipt.

## Findings

1. [obs] No finding — no difference to report. All 25 receipts exited 0 (`exits.txt` in the seat directory lists each tool with exit 0; each receipt footer carries `"exit_code": 0, "timed_out": false`), and the stdout payload (everything between the receipt header and footer) is byte-identical to the matching baseline receipt for all 25 tools, checked pairwise programmatically (`SelftestsAfterNoHarm/compare.json`, `stdout_eq: true` on every row). Byte-identical stdout implies every PASS line, case count, failure count and per-case observation line is unchanged; examples: `check-adjacency-anchors` "PASS (25 cases, 25 passed, 0 failed)" (`SelftestsAfterNoHarm/selftest-check-adjacency-anchors.jsonl:2` vs `a3w1/ExecGateBaselines/selftest-check-adjacency-anchors.jsonl:2`), `check-pause-gate` `{"status": "PASS", "cases": 24, "failed": 0, ...}`, `check-recheck-commands` `{"cases": 95, "failures": [], "passed": 95}`. The selftest output is deterministic (no tmp paths or timestamps leak into stdout), which is what makes byte identity achievable and meaningful.
2. [obs] Every new receipt is bound to the intended revision: header `revision` = `tool_revision` = `f761fade8a452ec9dd0831be7743601b0adda3e5` on all 25, and `tool_sha256` equals `sha256(git show f761fade:tools/<t>.py)` on all 25 (checked in the same comparison pass, `n_sha_ok: true` throughout). Baseline-side sanity also holds: every a3w1 baseline is bound to `9c89ff4f093d07a6f92925518310ca6a7c8a2fa0` the same way with exit 0, so the comparison pairs are like-for-like receipts, not like-for-like prose. `f761fade` is a descendant of the C1 commit `c8fcfbf662db6debc6d7128c166ced31ca3176cf` (`git merge-base --is-ancestor` → 0) and `tools/run-receipt.py` is byte-identical between `9c89ff4f` and `f761fade` (`git diff --stat` empty), so the runner itself did not change between baseline and re-run.
3. [obs] The scope is still exactly the 25 listed tools: re-deriving the importer set by AST (`ast.Import` / `ast.ImportFrom` module `_revision`) over `tools/*.py` at `f761fade` yields the same 25 files as the wave-1 manifest (normalized set difference: none), and each still has a `--selftest` mode. `git diff --stat 9c89ff4f f761fade -- tools/` shows the only changed tool files are `tools/_revision.py` (8 lines), the two sha256 pin bumps in `tools/check-pause-gate.py` and `tools/report-red-causes.py` (1 line each), and `tools/mutants-owed-statements-r29-v4shapes.py` (6 lines, no selftest, not an importer) — i.e. no selftest-bearing tool body other than the two pinned gates changed between baseline and re-run.
4. [obs] The two pin-carrying gates selftest green with the new pins: `check-pause-gate` selftest (`cases: 24, failed: 0`) and `report-red-causes` selftest (`cases: 12, failed: 0`) pass at `f761fade`, whose `tools/_revision.py` hashes to the bumped `fc861ec8…` pin values. The selftests evidently exercise fixture behaviors, not the committed pin constant, so the C1 pin bump does not disturb them. This corroborates the wave-1 measurement (finding 14 of `ExecGateBaselines.md`) that pin behavior is only observable through the gates themselves, not their selftests.
5. [obs] Hygiene: every run-receipt invocation ran with inherited `GIT_*` removed (`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE`), executed the tool from the runner's private `--no-local` clone at the tool revision with private `HOME`/`XDG_CONFIG_HOME` (`tools/run-receipt.py:44-52,100-113`), and nothing was written into the lane outside this seat's evidence directory. Wall time: one smoke run 2.5 s, the remaining 24 at parallelism 3 in 12.5 s.

## Residual risk and verification gaps

- [inf] The selftests exercise in-tool fixture logic; they do not measure what the C1 change actually targets (the environment seen by git children spawned in ordinary runs). Green selftests here are the no-harm half only; the after-value itself is the frozen probe's measurement, which this seat did not run and does not assert.
- [inf] "Case count identical" is established via byte-identical stdout rather than a separately parsed count; because comparison is byte-exact it is strictly stronger than count equality, but it also means any nondeterminism would have shown as a difference — none did.
- [unk] Behavior of the three base-red gates (pause-gate, registry-coverage, self-assessment at their registry entry forms) at `f761fade` was not re-measured here; that is outside this seat's assignment (selftests only). `check-registry-coverage`'s base red (`REGISTRY-ROW-MISSING`) should be cleared at `f761fade` since the probe row landed in that commit, but that is the gate's verdict to make, not this receipt's.

## Per-tool results (exit / case count / stdout vs a3w1 baseline — all identical)

| Tool | Exit | Cases | stdout vs baseline |
|---|---|---|---|
| check-adjacency-anchors | 0 | 25 cases | identical |
| check-appended-notices | 0 | 47 cases | identical |
| check-boot-chain | 0 | 83 cases | identical |
| check-boot-writers | 0 | 12 cases | identical |
| check-boundary-contract | 0 | 28 cases | identical |
| check-edit-contract | 0 | 102 cases | identical |
| check-freshness-r17 | 0 | 59 cases | identical |
| check-kernel-taint | 0 | 56 cases | identical |
| check-locator-clarification | 0 | 37 cases | identical |
| check-memory-pressure | 0 | 41 cases | identical |
| check-path-reconciliation | 0 | 40 cases | identical |
| check-pause-gate | 0 | 24 cases | identical |
| check-recheck-commands | 0 | 95 cases (95 passed) | identical |
| check-registry-coverage | 0 | 23 cases | identical |
| check-review-cohort | 0 | 24 cases | identical |
| check-review-snapshots | 0 | 24 cases | identical |
| check-root-dac-correction | 0 | 54 cases | identical |
| check-seat-bindings | 0 | 121 cases (73 v1, 48 v2) | identical |
| check-seat-scope | 0 | 54 cases | identical |
| check-section-citations | 0 | 68 cases | identical |
| check-selector-contract | 0 | 28 cases | identical |
| check-source-scope-correction | 0 | 29 cases | identical |
| check-storage-health | 0 | 44 cases | identical |
| measure-update-recheck | 0 | 20 cases | identical |
| report-red-causes | 0 | 12 cases | identical |

Receipts: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w2/SelftestsAfterNoHarm/selftest-<tool>.jsonl` (+ `.runlog` runner output per tool), pairwise comparison in `compare.json`, raw runner exits in `exits.txt`.

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w1/ExecGateBaselines.md and its 25 selftest-*.jsonl baselines, tools/run-receipt.py, git objects at 9c89ff4f093d07a6f92925518310ca6a7c8a2fa0 / c8fcfbf662db6debc6d7128c166ced31ca3176cf / f761fade8a452ec9dd0831be7743601b0adda3e5; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w2/SelftestsAfterNoHarm.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w2/SelftestsAfterNoHarm/ (25 selftest-*.jsonl receipts, 25 selftest-*.runlog, exits.txt, compare.json); executed=25 run-receipt invocations (tools/<t>.py --selftest at --revision f761fade8a452ec9dd0831be7743601b0adda3e5 --tool-revision f761fade8a452ec9dd0831be7743601b0adda3e5, max 3 concurrent), read-only git (rev-parse, merge-base --is-ancestor, log, diff --stat, ls-tree, show), and two local comparison scripts (AST importer set + pairwise receipt diff)
Model: not exposed
Installs: none
