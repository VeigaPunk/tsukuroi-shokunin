author: hyaku closure (non-author integrator, @m_zfl)

# Round 51 — non-author verifier spot-check (tsukuroi, hyaku run 11, attempt 1)

Lane before `c0ad548a93425a3bf8813d28d92f26fe2f64b9d4`, after `912278293a5c0a2915964d53499e11e78d5d5a0b`.
Driver digest (copied from `.ufo/watchdog.log`, mutable):
`2026-10-28T17:40:46-03:00 launch tsukuroi round=51 pgid=946953 driver=hyaku-inline attempt=1` ·
`2026-10-28T18:32:55-03:00 complete tsukuroi round=51; hyaku-inline attempt=1`.
Closure ruling: **status ok, admitted=false, verdict `rejected-honest-stop`** — the report is a real, honest,
incomplete report (checkable commits, `SHONEN` heading); no claim was measured at an integrated revision; no axis
is harmed.

## 1. Step-1 conformance

| Check | Command | Observed |
|---|---|---|
| Report committed by the lane identity | `git log --format='%an %H %s' -- .ufo/reports/round-51/tsukuroi.md` (fleet repo) | `tsukuroi-shokunin daf5b626f0d45eb34b01957bc7d629d62c7cc243 round-51: tsukuroi report (incomplete: w2 not dispatched)` |
| Every cited lane hash exists and is an ancestor of `master` | `git -C tsukuroi-shokunin merge-base --is-ancestor <h> master` for `c0ad548a`, `2732ee6c`, `6d051ef0`, `6abef5d0`, `91227829` | all five: ancestor (exit 0) |
| Lane pushed | `scripts/hyaku/jj-lane.sh state tsukuroi-shokunin`; `git ls-remote origin refs/heads/master` | `local=remote=91227829… ahead=0 behind=0`; remote prints `91227829…` |
| No uncommitted round work | `git status --porcelain` in the lane | **DEFECT**: ` M .ufo/waves/round-51/before/c2-cheats-at-amend1.json`; untracked `before/c2-cheats-at-amend1.rc`, `w1.ready`, `w1.ready.dispatched`, `w1/R51MutC2/M3-counter-pass-runs-relaxed.{json,stderr.txt}`. These are live-peer seat outputs (R51MutC2 was still running at filing); not committed, so they do not count for the round |
| `SHONEN` heading, one line per box | report §SHONEN | present, four lines (`[~]`,`[ ]`,`[ ]`,`[ ]`) |
| Prompt carries the template contract | `.ufo/prompts/tsukuroi-round-51.md` (689 lines) | §1 axes binding, §2 claims, §2b frontier, §3 L2 floor (≥8), §4 report contract, §5 commit/push/L0, §6 hyaku addendum, §7 scratch discipline present |
| Marker or real report | report body | real report: five committed hashes, evidence pointers; status `ok` (a defective report is not a marker) |

Defects (status-neutral): (a) wave `w2` never dispatched, and the round's 64-128-seat total was not reached
(54 w1 seats only); `WAVE-DONE w1` not received before filing; (b) `corpus/lessons/round-51.md` (`## Gate`,
`## Mistakes`) not written; (c) no LOG.md entry for round 51; (d) SCORECARD axes block not restated, so calibration
reads mismatches (`check-self-assessment` 1 mismatch at base); (e) the amended C2 instrument has no valid control
receipt — the committed `before/c2-cheats-at-amend1.json` (1157 B) shows `r50:*` rows `ERROR` rc 2 and `r51:F2…` rc 2,
i.e. the scorer run was broken by the scratch deletion the report admits; (f) the working copy carries uncommitted
files (above); (g) one misroot (SCORECARD edit at the fleet root, reverted byte-exact per the report; I did not
re-diff the fleet SCORECARD, which is another lane's concern).

## 2. Per-claim re-check

No claim has an after-measurement; the lane says so. I re-derived the before-side and the committed evidence;
I did not execute lane-owned gates (PROTOCOL §Gate standard, Closure consequence).

| Claim / axis | Predicate | What I measured or verified | Grade |
|---|---|---|---|
| C1 depth (GR1-GR3 `btrfs-scrub-grounding-r45.md`) | `structural_ok 1, lint_ok 3, quotes_ok 3, verdicts_ok 3, seats_ok 18, marks_ok 3` at a counted w2 | **Re-measured:** `git show c0ad548a:<entry> \| wc -l` 312 → at `91227829` 447; `grep -c 'Range gaps (R51)'` 0 → 1. **Evidence-verified, not run:** `before/c1-at-base.json` (lint gap_missing S237/S240/S242/S243/S247, GR1 quote not whole line); amend1 control battery `controls/battery-summary-r51-amend1-c1.jsonl` 26 lines, 26 `as_expected:true`, 0 false, last row K-pass `PASS` with `verdicts_ok 3, seats_ok 18`. That K-pass is a synthetic cohort, i.e. capability, not a measurement. The `w2` dir/results files do not exist (`git ls-tree -r 91227829 .ufo/waves/round-51` shows only `w2-items.py`). | **unprovable-but-better** — the rows were demonstrably rewritten from attacks and the lint's base-defects are fixed on the page, but the counted cohort that the predicate requires never ran |
| C2 operability (selftest matcher / cheat scorer) | `real_pass 1, cheats 5, cheats_rejected 5, r50_cheats_rejected 0` | **Evidence-verified:** `controls/battery-summary-r51-freeze-c2.jsonl` 2/2 as expected (K0 do-nothing FAIL with `cheats_rejected 1`, K-pass PASS) for the pre-amendment instrument (4 cheats). The AMEND1 (5-cheat) scorer run is committed **broken** (rc 2 / ERROR rows). | **unprovable** — the final instrument has no valid control receipt and no measurement |
| C3 adjacency (adjacency-table counter) | r50 legs + `display_bound_ok 10, quote_specific_ok 10, digests_bound_ok 10, display_forge_fails 1, override_blocked 1, r50_blind 1` | **Evidence-verified, not run:** `battery-summary-r51-amend1-c3.jsonl` 15/15 as expected; its K-pass row shows `digests_bound_ok 10, display_bound_ok 10, display_forge_fails 1, override_blocked 1, quote_specific_ok 10, r50_blind 1, stub_fails 1, quote_at_pin_ok 9`; `before/c3-at-base.json` `r50_blind 1` (do-nothing). The `quote_at_pin_ok 9` is not a declared target leg. The run is a battery control row, not a named-revision measurement of the integrated tree; `PROVINCE.md`/registry unchanged. | **unprovable-but-better** — the instrument demonstrably separates cheat from real in committed controls; no integrated measurement at a named revision |

Owned-axis harm check: `git diff c0ad548a 91227829 -- SCORECARD.md` is a single appended "Round 51 — declaration"
section (+23 lines) with no ordinal edit; `corpus/SOURCES.md`, `corpus/lessons`, `LOG.md`, `PROVINCE.md` have no
diff (`git diff --stat` empty). Nothing was lowered.

## 3. Axis verdicts (must match the MANIFEST entry)

| Axis | Verdict | Reason |
|---|---|---|
| depth | unprovable-but-better | C1 rows rewritten and lint-clean by committed controls; the counted cohort never ran |
| operability | unprovable | C2 final scorer has no valid receipt (committed run is ERROR) |
| adjacency | unprovable-but-better | C3 counter's committed controls 15/15 incl. K-pass target legs; no integrated measurement |
| coverage | unchanged | SOURCES.md 256 → 256 rows, no diff |
| freshness | unchanged | no row recheck/status change |
| calibration | unchanged | SCORECARD axes not restated; no ordinal moved (self-assessment mismatch at base persists) |

## 4. Discernment spot-check

`corpus/lessons/round-51.md` does not exist, so there is no `## Gate` block and no admit/reject decision to
sample; likewise no `corpus/SOURCES.md` row was written (diff empty, 256 → 256). The sample below is therefore of
the lane's *re-open* evidence for already-registered rows the sourced claim (C1) rests on, plus the census.

| Item | Decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| Gate admit/reject sample | none filed | `corpus/lessons/round-51.md` | n/a — **unprovable** | file absent; the lane did not reach the Gate step |
| S237 (btrfs-progs v7.1 `cmds/scrub.c`, re-open claimed byte-identical in `w1/R51ScoutReopenS237.md`) | re-open: identical to pin | `curl https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c \| sha256sum` = `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801` | agree | equals the pin in the S237 row |
| S240 (Linux v7.2.11 `fs/btrfs/ioctl.c`, "reopened live 2026-10-28, byte-identical") | re-open: identical to pin | `git.kernel.org/.../plain/fs/btrfs/ioctl.c?h=v7.2.11`: 145999 B, sha256 `7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01`; `ioctl.c` lines 3072-3073 are `if (!capable(CAP_SYS_ADMIN))` / `return -EPERM;` | agree | hash equals the S240 pin; the GR2 statement "`-EPERM` … (ioctl.c:3072-3073)" holds. (The GitHub raw mirror returned HTTP 429 and was not used.) |
| Registry state | 256 rows, census exit 0 | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` | agree | printed 40 W04 duplicate-url warnings (same as the lane's start/end receipts) then `ok …/corpus/SOURCES.md`, rc=0; no new row, so there is no new ≤25-word quote to check |

## 5. Trend verdicts

- expansion: **unchanged** — SOURCES.md 256 → 256; no knowledge entry added (the GR rewrite is a quality change).
- quality: **unprovable-but-better** — GR1-GR3 rewritten, five lane tools hardened by 40+ named attack findings,
  with committed control batteries (C1 26/26, C3 15/15); no counted cohort confirms it.
- discernment: **unprovable-but-better** — attackers (lane-dispatched) falsified the freeze lint, C2 and C3 counters
  and the lane committed the fixes; no admit/reject Gate sample exists for an outside check. Not `improved`: nothing
  was outside-checked this round.

## 6. Routed defects (lane must fix next round)

1. Resume point is committed: dispatch `w2` (validate under policy v1 first), re-run the AMEND1 C2 scorer in an
   undisturbed scratch and commit a valid receipt, then measure all three claims at one named revision.
2. Commit or discard the uncommitted round-51 files in the lane working copy (listed in §1) before any new work.
3. Write `corpus/lessons/round-51.md` (`## Gate`, `## Mistakes`: misroot, scratch deletion), a LOG.md entry, restate
   the SCORECARD axes block (K10 lesson-file count mismatch) and add the registry-coverage receipt at the tip.
4. The report's SHONEN assessment must be re-filed in the next round's report (this one marks Box 1 `[~]` on the
   registry-rows evidence only); no box is fully checkable by a non-author yet — promotion is not indicated.
