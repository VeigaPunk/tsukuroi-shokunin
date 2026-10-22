Partly holds — the counter patch adds refusal rules and should-fail selftests for the 15 routed shapes; after-scores below are inferred, not measured, because this seat did not run the counter, battery, or selftest.

1. [obs] The sandbox patch changes only `tools/check-adjacency-overlap.py`; the selftest `git(repo, ...)` helper is untouched. The patch artifact is `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecPaddingShapes/ExecPaddingShapes.patch`. The new rules and implementation are at `/fast/scratch/hyaku/tsukuroi-r29/ExecPaddingShapes/repo/tools/check-adjacency-overlap.py:24-47,77-95,100-111,145-209,231-358`; the new should-fail cases are at `:516-536`.

2. [obs] The routed residual records all 15 shapes at 6 rows before these edits (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-28/residual/RevC1Repairs.md:17`). The residual's measured revision is 9a0654ba; a read-only comparison of that revision with 81a061a for `tools/check-adjacency-overlap.py` emitted no diff output. I did not rerun the original shape driver at 81a061a.

3. [inf] Per-shape before/after `anchored_rows` (before 6 is the residual's recorded result; after is inferred from the new refusal checks, not command output):

| Shape | Before | After |
|---|---:|---:|
| same-anchor-six-times | 6 | 1 |
| lane-from-counter-source | 6 | 5 |
| lane-from-province-own-summary | 6 | 5 |
| lane-from-lessons | 6 | 5 |
| lane-from-scorecard | 6 | 5 |
| unrelated-lane-quote-agrees | 6 | 5 |
| mid-word-fragments | 6 | 4 |
| generic-four-word-quotes | 6 | 3 |
| placeholder-actions | 6 | 0 |
| rows-marked-withdrawn | 6 | 0 |
| consistent-false-class | 6 | 4 |
| province-html-comment | 6 | 0 |
| province-withdrawn-subsection | 6 | 0 |
| province-no-delimiter-prose | 6 | 0 |
| province-pointer-contradicts | 6 | 5 |

4. [obs] Selftest cases were added for unique anchors, the row-specific lane source, the five-word floor, token boundaries, action length, row schema, visible delimited PROVINCE structure, frozen OV4/OV5 decisions, and pointer/class contradiction. The cases are at `/fast/scratch/hyaku/tsukuroi-r29/ExecPaddingShapes/repo/tools/check-adjacency-overlap.py:516-536`. Per the wave executor instruction, I did not execute the selftest, live counter, or C1 battery; therefore `control_live_anchored_rows: 6` and `should_fail_accepted: 0/24` remain unverified here. Main should run those gates.

5. [inf] Risks: the five-word minimum may reject legitimate shorter future anchors; the lane-source allow-list and frozen OV4/OV5 conflict pairs are intentionally specific to this round-27 register, not semantic proof; the pointer check is a lexical contradiction guard. No implementation blocker remains; measured acceptance evidence is pending the parent gate.

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md:1097-1110, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-28/residual/RevC1Repairs.md:17, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-28/w1/CritC1NewShapes.md:28-39, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-28/w1/CritC1NewShapes/driver.py, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-adjacency-overlap.py, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/mutants-adjacency-overlap.py, and /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-adjacency-overlap.py:372-562 (selftests); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecPaddingShapes/ExecPaddingShapes.patch, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecPaddingShapes.md; executed=isolated `git clone --no-local` and checkout of 81a061a67466c5e1be812814a895a4b5ed89b4ff; env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git diff -- tools/check-adjacency-overlap.py to generate the patch; read-only env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git diff --exit-code 9a0654ba8eb053a39e6374a97a25d91f6464b965 81a061a67466c5e1be812814a895a4b5ed89b4ff -- tools/check-adjacency-overlap.py (no diff output); no tests/counter/battery run
Model: not exposed
Installs: none
