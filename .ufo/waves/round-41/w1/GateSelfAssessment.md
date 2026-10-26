VERDICT: defect-found

The self-assessment at the round-41 lane tip fails: `check-self-assessment.py` at `71851d63` checks 27
checks and reports **6 mismatches** (exit 1). Six cells in the last axes/capabilities tables still carry
round-40 numbers. Four of them are the C1 landing (census 124 -> 128, notes 61 -> 62, `SKILL.md` 2 lines /
2 table lines) and two are earlier round-41 landings (`corpus/lessons/round-40-verifier-spotcheck.md`,
`corpus/knowledge/alpm-package-anatomy-r41.md` + the freeze's two `SKILL.md` table rows). A seventh fact is a
tooling gap: the item's `--scratch` flag does not exist at the tool revision it names, so the requested exact
invocation cannot run (it exits 2). I then proved the closure values on a scratch variant: with the six cells
corrected and the heading moved to round 41, the same tool reports **27 checks, mismatches 0, exit 0**.

## 1. What I ran

Both runs go through `tools/run-receipt.py` (tool revision = revision = `71851d636ab1bffaf8fee5016617c88878a666f1`,
lane tip at dispatch; `git rev-parse HEAD` = `71851d63`, `refs/heads/master` = `71851d63`).

1. As the item specifies, with `--scratch`:

   ```
   TMPDIR=/fast/scratch/hyaku/tsukuroi-r41/GateSelfAssessment \
   python3 tools/run-receipt.py --revision 71851d636ab1bffaf8fee5016617c88878a666f1 \
     --out .ufo/waves/round-41/w1/GateSelfAssessment/receipt-self-assessment-with-scratch.jsonl \
     -- tools/check-self-assessment.py --revision {rev} --scratch /fast/scratch/hyaku/tsukuroi-r41/GateSelfAssessment/tmp
   ```
   -> `{"exit_code": 2}`; footer `stderr_tail`:
   `check-self-assessment.py: error: unrecognized arguments: --scratch /fast/scratch/hyaku/tsukuroi-r41/GateSelfAssessment/tmp`

2. The same invocation with the flag the frozen tool actually has (the census selftest run takes ~58 s wall):

   ```
   TMPDIR=/fast/scratch/hyaku/tsukuroi-r41/GateSelfAssessment \
   python3 tools/run-receipt.py --revision 71851d636ab1bffaf8fee5016617c88878a666f1 \
     --out .ufo/waves/round-41/w1/GateSelfAssessment/receipt-self-assessment.jsonl \
     -- tools/check-self-assessment.py --revision {rev}
   ```
   -> `exit_code 1`, `timed_out false`, `stderr_tail ""`, header `tool_sha256
   1e1ab6113d665684e15d147c0f3dae519cf2d313877e1603b841ad4db85d4257`, `argv
   ["tools/check-self-assessment.py", "--revision", "71851d63..."]`; body: `"status": "FAIL", "checked": 27,
   "mismatches": 6, "declaring_round": 40, "reference_lines": 482`.
   Receipt: `.ufo/waves/round-41/w1/GateSelfAssessment/receipt-self-assessment.jsonl` (header line 1, footer
   last line; the tool prints indented JSON, so the body spans the lines between them).

3. One independent census run at tip, from a `git archive` extraction (this exercises the counting command
   for K13/K17 and confirms the checker's number):

   ```
   C=/fast/scratch/hyaku/tsukuroi-r41/GateSelfAssessment/census
   git -C <lane> archive --format=tar 71851d63 | tar -x -C $C
   cd $C && TMPDIR=<scratch>/tmp bash tools/tsukuroi-census.sh --selftest
   ```
   -> exit 0, last line `TSUKUROI_CENSUS_SELFTEST: PASS (128 cases, 128 passed, 0 failed)`.
   Receipt: `.ufo/waves/round-41/w1/GateSelfAssessment/census-selftest.txt`.

## 2. Mismatches at `71851d63` (all six; every other K01-K27 is `match`)

Line numbers are in `SCORECARD.md` at the tip; "stated" is the cell text, "observed" the value the tool
derives from the committed tree at that revision.

| Check | Cell | Stated | Observed | Reason (verbatim) |
|---|---|---|---|---|
| K07 | depth row, `SCORECARD.md:2429` | 61 notes | 62 | `depth row states 61 notes; corpus/knowledge holds 62 .md files` |
| K08 | depth row, `SCORECARD.md:2429` | 3559 `SKILL.md` lines | 3561 | `depth row states 3559 SKILL.md lines; SKILL.md holds 3561 newline characters` |
| K09 | depth row, `SCORECARD.md:2429` | 928 table lines | 930 | `depth row states 928 table lines; SKILL.md holds 930 pipe-prefixed lines` |
| K10 | depth row, `SCORECARD.md:2429` | 56 lesson files | 57 | `depth row states 56 lesson files; corpus/lessons holds 57 files` |
| K13 | operability row, `SCORECARD.md:2431` | 124 cases | 128 | `operability row states 124 cases; the census selftest at this revision prints 128 cases (TSUKUROI_CENSUS_SELFTEST: PASS (128 cases, 128 passed, 0 failed))` |
| K17 | host-census-gate row, `SCORECARD.md:2441` | 124 cases | 128 | `host-census-gate row states 124 cases; the census selftest at this revision prints 128 cases` |

Passing and relevant: K01-K06 (`depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8`,
each equal to the after-value of the last eligible transition), K11 (`corpus/README.md` 353), K12/K14/K15,
K16/K18/K19 (capability paths), K20-K23 (SHONEN paths, none marked `[x]`) and K24-K27 (cited knowledge notes,
none superseded).

Where the deltas come from (each verified with `git log`/`git diff --name-status` at the tip):
- `corpus/knowledge/alpm-package-anatomy-r41.md` added: `git diff --name-status aad01138 71851d63 -- corpus/knowledge/`
  -> `A corpus/knowledge/alpm-package-anatomy-r41.md`, `M corpus/knowledge/pacman-exec-environment-r40.md` (61 -> 62).
- `SKILL.md` +2 lines, both pipe rows: `git diff aad01138 71851d63 -- SKILL.md` -> `1 file changed, 2 insertions(+)`,
  the two added lines are the `| selftest-mounts-r41 | gate | ...` and `| package-anatomy-r41 | gate | ...` rows
  (freeze commit `e479fdc5`, `git log --oneline aad01138..71851d63 -- SKILL.md`) (3559 -> 3561, 928 -> 930).
- `corpus/lessons/round-40-verifier-spotcheck.md` added: `git diff --name-status aad01138 71851d63 -- corpus/lessons/`
  -> `A corpus/lessons/round-40-verifier-spotcheck.md` (56 -> 57).
- Census 124 -> 128: `git log -1 568c397da11339aed65181be598414f268835555` = `round-41: C1 census selftest gains
  four held-out mount tables (H5, H6, H9, H10)`, `tools/tsukuroi-census.sh | 27 +++++`; the four new case homes are
  `storage-mounts-mp-relative` (H5), `storage-mounts-src-uuid` (H6), `storage-mounts-no-subvol-opt` (H9) and
  `storage-mounts-two-btrfs` (H10) (from `git diff 568c397^ 568c397 -- tools/tsukuroi-census.sh`), and the
  independent run in §1.3 prints 128.

## 3. Tooling gap: `--scratch` is not at the tool revision the item names

- Tip blob: `git show 71851d63:tools/check-self-assessment.py | sha256sum` =
  `1e1ab6113d665684e15d147c0f3dae519cf2d313877e1603b841ad4db85d4257`; its `main()` registers only
  `--revision`, `--repo`, `--selftest` (`grep -n add_argument` on that blob: lines 1086-1089), and
  `census_case_count(repo, rev)` calls `tempfile.mkdtemp(prefix="self-assessment-census-")` with no `dir`.
- Working tree (uncommitted, not mine): `tools/check-self-assessment.py` is `M`; `git diff --numstat` = `18 7`,
  working-tree sha256 `44b474fb5401559d9a4052f04f03145cd165a688a78455694d7dd25dba5838e6`; the change adds
  `parser.add_argument("--scratch", ...)`, threads it through `evaluate`/`census_case_count` and extracts the
  archive under it. So the fix the item presupposes exists but is **not committed at the tip**.
- The lane already plans it: `SCORECARD.md:2448-2452` ("planned (next round)") names
  `tools/check-self-assessment.py --scratch` (R40-TMP-MISROOT). A version with the flag is reachable only
  outside `master`: `git for-each-ref --contains 127a28a8` -> `refs/jj/keep/127a28a8cb60e0e1de1435a2bcfb2418baa961b6`.
- Consequence of the frozen tool, observed not inferred: it extracts the `git archive` tree with `dir=None`
  and gives the census child only `git_env()` (PATH/LC_ALL/GIT_*), so with `TMPDIR` absent the run writes under
  `/tmp`. During the §1.2 run I observed `/tmp/tsukuroi-r3-2-selftest.rR8CO1` (bin/, fx/ trees, mtimes 15:07-15:08
  local); by 15:12 `ls -ld /tmp/tsukuroi-r3-2-selftest.* /tmp/self-assessment-*` printed nothing, so no cleanup of
  mine was needed. `run-receipt.py`'s child `env()` (lines 38-53) does not carry `TMPDIR` either, so even a caller
  `TMPDIR=...` does not reach the tool through it. With `TMPDIR` set directly (§1.3) the census selftest cleaned up:
  `ls /fast/scratch/hyaku/tsukuroi-r41/GateSelfAssessment/tmp/*` was empty afterwards.

## 4. Predicted cells the L1 must update, with the counting command for each

All commands are revision-pinned and mirror what the checker derives (it reads blobs through Git, never the
working tree — `check-self-assessment.py:134-140`). Replace `<REV>` with the round-41 closing commit.

| # | Cell (at tip) | Must state | Counting command | Output at `71851d63` |
|---|---|---|---|---|
| 1 | depth, notes `SCORECARD.md:2429` | 62 (was 61) | `git ls-tree --name-only <REV> corpus/knowledge/ \| grep -c '\.md$'` | 62 |
| 2 | depth, `SKILL.md` `wc -l` `SCORECARD.md:2429` | 3561 (was 3559) | `git show <REV>:SKILL.md \| wc -l` | 3561 |
| 3 | depth, table lines `SCORECARD.md:2429` | 930 (was 928) | `git show <REV>:SKILL.md \| grep -c '^\|'` | 930 |
| 4 | depth, `corpus/lessons/` files `SCORECARD.md:2429` | **58 at the closing revision** (57 at tip, was 56) | `git ls-tree -r --name-only <REV> corpus/lessons/ \| wc -l` | 57 at tip; 58 once `corpus/lessons/round-41.md` is committed (measured on a variant, §5) |
| 5 | operability, cases `SCORECARD.md:2431` | 128 (was 124) — both halves, `PASS (128 cases, 128 passed, 0 failed)` | `D=$(mktemp -d <scratch>/cen.XXXX); git archive --format=tar <REV> \| tar -x -C "$D"; TMPDIR=<scratch>/tmp bash "$D/tools/tsukuroi-census.sh" --selftest \| tail -1` | `TSUKUROI_CENSUS_SELFTEST: PASS (128 cases, 128 passed, 0 failed)`, exit 0 |
| 6 | host-census-gate, cases `SCORECARD.md:2441` | 128 (was 124) — both halves | same as #5 | same |
| 7 | axes heading `SCORECARD.md:2423` | `## Axes — current self-assessment (round 41 final measured surface)` (declaring round must be 41, and the heading must carry `round N` or the tool exits 2) | `grep -n '^## Axes — current self-assessment' SCORECARD.md \| tail -1` | line 2423, round 40 |
| 8 | axes preamble `SCORECARD.md:2425` | re-derived at the round-41 integration commit, not `aad01138` (prose; unchecked, but false otherwise) | — | `at the round-40 integration commit aad01138` |
| 9 | calibration prose `SCORECARD.md:2433` | `mismatches 0 required at the round-41 tip (the round-40 K07-K10/K13/K17 reds ...)`. Unchecked by K05 (which only compares the ordinal 9), so a stale sentence here silently falsifies the calibration claim | `python3 tools/check-self-assessment.py --revision <REV> \| tail -n +1` -> `"mismatches": 0` | currently names the round-40 tip |

Scores themselves must **not** move: K01-K06 pass at `8, 9, 9, 9, 9, 8`. `reference_lines` excludes every
section whose round is >= the declaring round (`check-self-assessment.py:392-419`, the `int(match.group(1)) >=
declaring_round` branch), so an ordinal uplift recorded in a round-41 "measured outcome" section can never be
seen by K01-K06: keep the six scores and record any uplift as the next round's reference. Verified in §5.

Also worth editing while in there (unchecked, but the text would be stale): the "planned (next round)" bullet
`SCORECARD.md:2448-2452` promises `--scratch` (R40-TMP-MISROOT) — after this round the item is either landed
and must move to the landed/retired text, or the promise moves forward.

## 5. Closure values proven on a scratch variant

`D=/fast/scratch/hyaku/tsukuroi-r41/GateSelfAssessment/var1`; `git clone -q --shared <lane> $D`;
`git -C $D remote remove origin`; toplevel check `git -C $D rev-parse --show-toplevel` = `$D`; identity
`fixture <fixture@shokunin.local>`; three commits on `master`.

- `ec330539` "variant: round-41 axes cells": heading 2423 -> round 41, depth row -> 62/3561/930/57,
  operability row -> 128, calibration prose -> round-41 tip (naming the six reds), host-census-gate row -> 128,
  preamble 2425 -> `71851d63`.
  Run: `TMPDIR=<scratch>/tmp python3 $D/tools/check-self-assessment.py --repo $D --revision HEAD`
  -> exit 0, `"status": "PASS", "checked": 27, "mismatches": 0, "declaring_round": 41` (57 s wall, 4m45 user under
  the current host load). Receipt: `.ufo/waves/round-41/w1/GateSelfAssessment/var1-result.json`, stderr empty
  (`var1-stderr.txt`, 0 bytes).
- Then `corpus/lessons/round-41.md` (the untracked file already on disk, copied into the variant) was committed:
  `git -C $D ls-tree -r --name-only HEAD corpus/lessons/ | wc -l` -> **58**. The depth row's `corpus/lessons/` value
  must therefore be 58 at the closing revision, not the tip's 57.
- `2e2e3a62` "variant: round-41 outcome probe, lessons 58": depth row set to 58 and a `## Round 41 — measured
  outcome` section appended carrying the probe line `- depth 8 -> 9`.
  Same run -> exit 0, `27 checks, mismatches 0`; K01 still `depth score 8 equals the after-value 8 of the last
  recorded transition (SCORECARD.md:2250)` — i.e. the round-41 section (and its `8 -> 9` line) was excluded, the
  round-40 line was used. `reference_lines` 482 -> 504 (the round-40 outcome sections become eligible once the
  declaring round is 41). Receipt: `var2-result.json`, stderr empty (`var2-stderr.txt`, 0 bytes).

This shows: the six corrections plus a round-41 heading and a round-41 outcome section yield a clean 27/27, and
that the outcome section cannot re-score an axis in its own round.

## 6. Risks for the closing move

- **A `[x]` in SHONEN.md needs a verifier.** All four boxes are `[~]` at tip (K20-K23: "is not marked complete").
  Marking one `[x]` without a `non-author verifier: <id>` token turns K20/K21/K22/K23 red
  (`check-self-assessment.py:745,756`).
- **New citations must resolve.** If the closure adds `corpus/knowledge/alpm-package-anatomy-r41.md` to a SHONEN
  box, K24-K27 stay green: it exists at tip and `head -20 | grep -in superseded` prints nothing.
- **`SKILL.md` may grow again at closure** (a round-41 gate/closure row would add pipe lines). Re-derive #2/#3 at
  the closing commit; do not copy the tip's 3561/930 blindly, and do not write the table before the lesson file
  lands (that is the 57 vs 58 trap).
- **K17 shares the census number** with K13: editing only the operability row leaves the capabilities table red.
- Nothing here needs a package, service or `/etc` change; no host state was touched.

## 7. Not done (and not claimed)

- No second census run beyond §1.3, and no re-run of the four round-41 counters (C1/C2); this item is the
  self-assessment gate only.
- I did not run the working-tree version of `check-self-assessment.py` (it is uncommitted sibling work): every
  value here is the committed tip tool run exactly as the item specifies minus the absent `--scratch` flag, whose
  absence is reported in §3.
- I did not edit, commit, stash or check out anything in the lane; the only writes are this report and the
  receipts under `.ufo/waves/round-41/w1/GateSelfAssessment/`
  (`receipt-self-assessment.jsonl`, `receipt-self-assessment-with-scratch.jsonl`, `var1-result.json`,
  `var2-result.json`, `var1-stderr.txt`, `var2-stderr.txt`, `census-selftest.txt`).
- No tool was installed or upgraded for this item.
- Scratch (`/fast/scratch/hyaku/tsukuroi-r41/GateSelfAssessment/`) held the census extraction and the variant
  clone; it was removed with `rm -rf` after the receipts were copied, and
  `ls -ld /tmp/tsukuroi-r3-2-selftest.* /tmp/self-assessment-*` was empty at 15:12 local.
