# RerunC1Counters — independent re-run of every C1 counting command

Seat: RerunC1Counters (wave 2, falsify). Sandbox: clone of the lane repo at
`/fast/scratch/hyaku/tsukuroi-r30/RerunC1Counters/repo`, HEAD
`29bf87fa3971df04cb96e4ad9a28805d8154ed2f` (verified with `git rev-parse HEAD`).
All commands ran with `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE`.

Tool bytes used (sha256, all identical to the receipts' `tool_sha256`/`counter_sha256`):

- counter v1 (`git show 8fb2cef0:tools/check-btrfs-space-r30.py` → `ctr-v1.py`):
  `1bf7ee14467accac5281e6ebd881db24c8ab682066e9f50ddbb0fe76a931c079`
- counter v2 (`repo/tools/check-btrfs-space-r30.py` at tip):
  `4953203d2b03fe5e5153441ba9fdc9193683e4b38f2613322a401616b6e55eba`
- battery v1 (`git show 8fb2cef0:tools/mutants-btrfs-space-r30.py` → `bat-v1.py`):
  `ac0fbd2c51a22f166aedebc7746f19e40908600543702d63ef58a17bcb56be25`
- battery v2 (`repo/tools/mutants-btrfs-space-r30.py` at tip):
  `6d4e5a0a2ece6b2d83a665d22bbde600f806826af730bb4e88d00216fc74296c`

## Results — measured by this seat vs receipts

| # | Command | Receipt (file → claimed value) | My re-run | Exit | Match |
|---|---|---|---|---|---|
| 1 | `python3 ctr-v1.py --revision 8fb2cef0… --lane <repo>` | `measure/c1-before-8fb2cef0….jsonl` → verified 0 of 10, all D01–D10 unverified "R1 json missing" | verified **0** of 10, identical failure strings | 1 | yes |
| 2 | `python3 ctr-v1.py --revision 29bf87fa… --lane <repo>` | `measure/after-a3f19372/c1-declared-v1.jsonl` → verified 10 of 10 (at a3f19372) | verified **10** of 10, exit 0 | 0 | yes |
| 3 | `python3 repo/tools/check-btrfs-space-r30.py --revision 29bf87fa… --lane <repo>` | `measure/after-a3f19372/c1-v2.jsonl` → verified 10 of 10, `counter_version: 2` | verified **10** of 10, `counter_version: 2` | 0 | yes |
| 4 | `python3 bat-v1.py --counter ctr-v1.py` | `measure/c1-battery-8fb2cef0….jsonl` and `after-a3f19372/c1-battery-v1-counter-v1.jsonl` → control 10, should_fail 0/46, should_pass 0/6 | control **10**, should_fail_accepted **0**/46, should_pass_refused **0**/6 | 0 | yes |
| 5 | `python3 repo/tools/mutants-btrfs-space-r30.py --counter ctr-v1.py` (battery v2 + counter v1) | `after-a3f19372/c1-battery-v2-counter-v1.jsonl` → control 10, should_fail_accepted 20/72 (same 20 shape names), should_pass_refused 5/11 (P07–P11) | control **10**, should_fail_accepted **20**/72 — accepted_shapes list byte-identical to receipt — should_pass_refused **5**/11, refused shapes P07, P08, P09, P10, P11 (identical) | 1 | yes |
| 6 | `python3 repo/tools/mutants-btrfs-space-r30.py` (battery v2, default counter = v2) | `after-a3f19372/c1-battery-v2-counter-v2.jsonl` → control 10, should_fail 0/72, should_pass 0/11 | control **10**, should_fail_accepted **0**/72, should_pass_refused **0**/11 | 0 | yes |
| 7 | `python3 bat-v1.py --counter repo/tools/check-btrfs-space-r30.py` (battery v1 + counter v2) | **no receipt exists** — the combination is absent from `measure/after-a3f19372/` (verified: directory lists only v1+v1, v2+v1, v2+v2) | control **7** (not 10), should_fail_accepted **0**/46, should_pass_refused **6**/6 (P01–P06 all refused), counter_sha256 v2 | 1 | n/a — new data |

Note on rows 2–3: the receipts were taken at revision `a3f19372`, mine at tip
`29bf87fa`. Between them only one commit landed (`29bf87f`), touching SKILL.md
(two registry-table rows: `run-receipt` reworded, `report-receipts` added) and
`tools/check-report-receipts.py`. The R30 decision-table lines the counter
parses are untouched, so identical counts are expected and observed.

## Findings

1. **Every published C1 number reproduces exactly.** The declared counter v1
   reads 0/10 at the declaration commit and 10/10 at the tip; counter v2 reads
   10/10 at the tip; battery v1 is clean with counter v1 (0/46, 0/6); battery
   v2 exposes counter v1 (20/72 accepted, 5/11 refused, identical shape-name
   lists) and is clean with counter v2 (0/72, 0/11). No disagreement with any
   receipt in `measure/` or `measure/after-a3f19372/`.

2. **[obs] Receipt coverage gap, not a claim defect:** no receipt exists for
   battery v1 × counter v2. Re-running it here shows the v1 fixture itself is
   over-rejected by v2 (control 7/10, all six P01–P06 should-pass shapes
   refused, exit 1). This is the asymmetry the v2 battery's P07–P11 shapes were
   built to pin down; it does not weaken C1, which is judged on declared
   counter v1 and on the v2 battery pairs that do have receipts.

3. **[obs] Claim arithmetic confirmed:** goal-stated battery numbers (0 of 72
   / 0 of 11 with v2; 20 of 72 / 5 of 11 with v1) and the C1 before/after
   (0 of 10 at 8fb2cef0, 10 of 10 declared) are all exactly what the tools
   emit. Exit codes also match receipts (1 on failure, 0 on pass).

## Verdict

C1 counting **holds** under independent re-run; the only novelty is the
unreceipted battery-v1 × counter-v2 pair (control 7, 6/6 refused), consistent
with the documented v2-strictness direction and harmless to the claim.

Scope: read=SCORECARD round-30 declaration, measure/ receipts, tool docstrings/CLIs, SKILL.md diff a3f19372..29bf87fa; wrote=.ufo/waves/round-30/w2/RerunC1Counters.md, /fast/scratch/hyaku/tsukuroi-r30/RerunC1Counters/{repo,ctr-v1.py,bat-v1.py}; executed=git clone/checkout/rev-parse/log/diff/show/sha256sum, 3 counter runs, 4 battery runs (all env -u GIT_*)
Model: devin/swe-2
Installs: none
