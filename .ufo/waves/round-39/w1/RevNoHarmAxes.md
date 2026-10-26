VERDICT: supports

# R-1 — six-axis no-harm sweep, base `0eff65b2` → tip `2e1c2a40` (seat RevNoHarmAxes, 2026-10-26)

Method: read-only. `git diff --numstat 0eff65b2… 2e1c2a4…` in the lane (both commits verified with
`rev-parse --verify …^{commit}`); all counters/checkers run against a `git clone -q --shared` scratch clone
(origin removed, `rev-parse --show-toplevel` verified equal to the clone) with `--revision` naming the exact
commit, outputs under `/fast/scratch/hyaku/tsukuroi-r39/RevNoHarmAxes/` (removed after receipts were copied).
Run matrix and observed fields: `.ufo/waves/round-39/w1/RevNoHarmAxes/runs.md`. No tools installed or updated.

## 1. Changed-file inventory (51 files: 46 added, 5 modified, 0 deleted, 0 renamed)

`git diff --name-status base tip` — exactly five `M`, everything else `A`:

| File | +/− | Class | Harm surface |
|---|---|---|---|
| `SCORECARD.md` | 32/0 | append-only preserved | round-39 declaration appended at `SCORECARD.md:2208` (hunk `@@ -2205,3 +2205,35`) |
| `SKILL.md` | 2/0 | append-only preserved | two gate rows appended (hunk `@@ -3113,6 +3113,8`), census row untouched |
| `corpus/SOURCES.md` | 7/1 | append-only, 1 removed line | S208 row's entry column extended (see §2a); S213–S218 added |
| `corpus/knowledge/adjacency-anchors-r19.json` | 2/2 | registry, 2 removed lines | IN-109 `found_line` repin (see §2b) |
| `tools/tsukuroi-census.sh` | 45/1 | tool | storage arm only (see §3a) |

`LOG.md`, `SHONEN.md`, `PROVINCE.md`: `git diff --exit-code base tip -- LOG.md SHONEN.md PROVINCE.md` is empty
(append-only ledgers byte-identical). All 46 additions are new files (round-39 receipts, controls, frozen
inputs, two new counters, the new knowledge entry) — no existing consumer surface among them. Frozen checker
tools are byte-identical base→tip: `git diff --stat base tip -- tools/score-storage-arm-r38.py
tools/score-storage-arm-r38-q82.py tools/check-hook-order-r38.py tools/score-census-handoff-r32.py
tools/check-adjacency-anchors.py tools/check-storage-health.py` → empty.

## 2. Removed lines in append-only surfaces (4 total, all accounted)

**a. `corpus/SOURCES.md` −1** = the old S208 row, re-emitted with one change only: its entry column gained a
second pointer, `…pacman-hook-order-r38.md, corpus/knowledge/pacman-transaction-order-r39.md`
(hunk `@@ -214,11 +214,17`); SID, url, type, class, anchors, sha256, dates, refresh are character-identical.
Consumer check: `python3 tools/check-hook-order-r38.py --revision 2e1c2a4… --repo <clone>` →
`rows_matched 69/69, mismatches 0, extra_rows 0, source_ok 1, source_ids [S208…S212], source_problems []`,
exit 0. S213–S218 do not exist at base (`grep -c '^| S21[3-8] '` → 0) and no SID is duplicated at tip
(`grep -o '^| S[0-9]*' | sort | uniq -d` → empty).

**b. `corpus/knowledge/adjacency-anchors-r19.json` −2** = IN-109 `found_line` 2425→2447 plus a note sentence
documenting the repin ("Round 39: … moved it from line 2425 to line 2447 (found_line updated in the same
commit as the census change, L1 TsukuroiR39)"). Verified exact:
`git show base:tools/tsukuroi-census.sh | grep -n "degraded: kernel ring class counts"` → `2425:`;
same at tip → `2447:`. Registry validator:
`python3 tools/check-adjacency-anchors.py --revision 2e1c2a4…` → `"findings": [], "status": "PASS"`,
`live_object_checked 10, live_object_match 10, outbound_portable 10`, exit 0 (default mode is read-only;
its only writes are the `--selftest` fixture builder).

## 3. Harm vectors

**a. Census exit codes / verdicts.** The only code change is the guard at `tools/tsukuroi-census.sh`
(hunk `@@ -1893,6 +1900,18`): it fires only when `fsn -eq 0 && blocked -eq 0`, so every populated-root,
malformed, unreadable and no-devinfo path is byte-identical; the sole removed line is a comment rewritten to
document the superseded round-38 rule. New selftest cases (hunk `@@ -2947,6 +2969,28`) expect exit 0 and
rollup HEALTHY even when the STORAGE line is BLOCKED — the line stays verdict-neutral as documented at the
storage header ("no PLANE text, rollup term or exit code changes"). Empirical: census `--selftest` at tip →
`TSUKUROI_CENSUS_SELFTEST: PASS (117 cases, 117 passed, 0 failed)`, exit 0 (matches the committed receipt
`.ufo/waves/round-39/after/selftest-49cc53c.txt`); all non-storage fails-closed cases (journal exit 2,
update-safety exit 2, …) still pass. `census_exit` is 2 in every v1-counter fixture child at both base and
tip — no exit-code drift anywhere observed.

**b. Frozen consumers pinning STORAGE/PLANE output.**
- v1 `score-storage-arm-r38.py` at tip: FAIL, `fixtures_matched 9/10, live_match 1, six_planes_all 1`,
  F06 the **only** mismatch — expected `HEALTHY 0/0/0`, got `BLOCKED 0/0/0 detail=mounts:btrfs-without-sysfs`
  (fixture defined `tools/score-storage-arm-r38.py:82` `'F06-no-btrfs-root': ([], ('HEALTHY', 0, 0, 0))`,
  absent root per `:97-98`). F01–F05 and F07–F10 match with identical lines and `census_exit: 2`.
- q82 `score-storage-arm-r38-q82.py` at tip: **PASS 3/3** (`ns_views_matched 3, ns_available 1`, exit 0) —
  its namespace views forge *populated* roots (e.g. HEALTHY 1/1/0), and a populated root never reads the
  mount table, so no flip exists there to declare. Same PASS at `b0005ae9`.
- r32 `score-census-handoff-r32.py --revision 2e1c2a4…` (the census header's named frozen consumer,
  `tools/tsukuroi-census.sh:369-370`): summary
  `"base": "58cc2e0b…", "routed": 24, "unrouted": [], "harness_errors": 0, "live_consistent": true, "consistent": true`,
  exit 0 — PLANE/TSUKUROI_CENSUS/exit parity with the frozen base census holds.
- r39 counter grammar: `tools/score-storage-hidden-r39.py:58-59` accepts the optional
  ` detail=(\S+)?$` extension; `HIDDEN_LINE` at `:60-61` equals the census output character-for-character.
- `check-storage-health.py --revision 2e1c2a4…` → `findings: []`, exit 0 (SKILL round-26 section untouched
  by the two appended rows).

**c. Round-38 v1 counter's F06 flip.** Declared before any seat: `SCORECARD.md:2232-2234` ("Predicted side
effect, declared now: the round-38 v1 counter's fixture F06 … FAILs 9/10 by construction; the round-38 claim
stays measured at `b0005ae9`"). Verified in both directions: at tip the counter FAILs exactly 9/10 with F06
alone mismatching (shape identical to the declaration), and at `b0005ae9f56f…` (verified ancestor of base) it
still PASSes `10/10, live 1, six 1`, exit 0 — the admitted round-38 measurement is reproducible today. The
search for any *undeclared* flip found none: `git grep -n '9/10\|q82' tip -- SCORECARD.md SKILL.md LOG.md
corpus/` surfaces only the declared F06 row and historical round-38 rows; q82 verified PASS at tip directly.

## 4. Per-axis verdicts

- **depth — supports.** The depth surface is purely additive: new entry `corpus/knowledge/pacman-transaction-order-r39.md`
  (+58, new file); no existing knowledge entry is in the diff (`pacman-hook-order-r38.md` untouched). The
  S210 anchor correction is layered as a new S217 row ("supersedes S210 — … not `_alpm_trans_commit` as the
  S210 anchor says"), leaving the round-38 entry and its sources unrewritten; C2's own duplicate checks
  (`duplicate_rows`, `duplicate_headings`) guard the new block (`controls.jsonl` E4: duplication FAILs).
- **coverage — supports.** Additive guard + 4 new selftest cases (113→117); no arm, plane or seam removed;
  the new seam `TSUKUROI_PROC_MOUNTS` is documented in the census env-var header (hunk `@@ -397,6 +402,7`).
- **operability — supports.** The single verdict delta is the declared C1 fix itself (absent/empty root +
  btrfs mount → BLOCKED); the mounted-populated case proves a populated root is still read and the mount
  table adds nothing (expected `HEALTHY 1/1/0`); selftest 117/117 at tip; exit codes unchanged.
- **freshness — supports.** Ledger files byte-identical; new SOURCES rows opened 2026-10-26 with declared
  refresh classes; S208's edit touches only its entry column — pinned columns (sha256, dates, url) unchanged.
- **calibration — supports.** All six pre-existing counters/checkers byte-identical base→tip; the sole
  behavior flip of a frozen counter (v1 F06) was pre-declared, is empirically exact (9/10, F06 only), and the
  round-38 claim re-verifies PASS at its pinned revision `b0005ae9`. No undeclared flip found (q82 PASS
  verified). Observation, not a defect: post-C1, the v1 counter FAILs at every future revision by
  construction, so any re-score of round-38 must pin `b0005ae9` — the declaration already says so.
- **adjacency — supports.** The only adjacency surface is the IN-109 anchor, repinned accurately (2425→2447
  verified at both revisions) with provenance recorded, and the full registry validates PASS at tip; the
  S210→S217 supersede is an additive storage/hook boundary acknowledgement, matching the round-38 closure
  route cited in the declaration.

## 5. Not done / residual risk

- No TO rows judged against source lines here (that is the C2 reviewer seats' QUALITY-81 duty); I emit no
  `TO<n>:` lines.
- I did not run a fresh live-host census myself; live coverage comes from the counters' live legs
  (`live_match 1` in my v1-at-tip run and in `.ufo/waves/round-39/after/c1-after-49cc53c.jsonl`).
- The r32 run used one fixed seed (`0000…`, 24 scenarios); other seeds sample other fixture shapes. Residual
  risk is low because the diff touches only `probe_storage_arm` and r32 compares non-storage PLANE/exit
  parity per scenario, which the guard cannot alter.
- The counters report the clone's `branch_tip 394e1ba4…` (the lane has moved past the dispatch tip); every
  measurement above read the census and corpus at the explicitly named `--revision`, so the sweep is bound to
  `2e1c2a4` regardless.
