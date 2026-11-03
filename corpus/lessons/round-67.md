# Round 67 — lesson (tsukuroi, hyaku run 15, attempt 1)

Declared claims (frozen at `071a55c9`, SCORECARD "Round 67 — declaration"):
C1 depth (lowest tied, 8; SOURCED — S284, S285) and C2 calibration (9; overreach caught).
Wave w1: one v1 wave, 11 seats (`.ufo/waves/round-67/w1-spec.json`, `w1-dispatch.json`,
`w1/swarm-registry.json`, `w1-results.json`); attack share 4/11 (reviewer 2, critic 1, mutation-tester 1).

## Gate

Candidates considered (C1 frontier, btrfs-progs v7.3; the QUALITY 98 watch fired on the installed
btrfs-progs 7.1-1 pin):

- **Admitted — S284** `cmds/scrub.c` at tag v7.3 (peeled `afdc3a65e33f4d42f768ad50dca20c32e5ee1496`), lines
  1640-1649, sha256 `b58942ccaff74cf2300f5d25b99624ba8e9cfcb59eda5897639f1928b277d528`. Gate:
  URL `https://github.com/kdave/btrfs-progs/blob/v7.3/cmds/scrub.c`; access date 2026-11-03 (fetch log
  `.ufo/waves/round-67/before/src/FETCH.txt`, scout re-fetch `.ufo/waves/round-67/drafts/S1Scout-verify.md`
  rows 1-3); located quote `/* Revert to the older scrub limits. */` (8 words, `wc -w`) at `scrub.c:1640`,
  verified by `grep -c 'Revert to the older scrub limits' scrub.c` → 1 (v7.1 singular `limit.` → 1, both
  copies). Scout result ALL_MATCH.
- **Admitted — S285** `CHANGES` at tag v7.3, sha256 `5046bac1def81247a02d7442807a6d495de2caafbc1a7194637ef03ea958a249`.
  Gate: URL `https://github.com/kdave/btrfs-progs/blob/v7.3/CHANGES`; access date 2026-11-03; located quote
  `scrub limit: set to the original limit only after all devices finish` (12 words) at `CHANGES:20`
  under `btrfs-progs-7.3 (2026-10-23)` at line 1. Scout: `grep -n` → 20, MATCH.
- **Admitted — knowledge entry** `corpus/knowledge/btrfs-scrub-limit-revert-r67.md`, rows SL1–SL4; its
  `source:` cites S284 and S285 (provenance trio first).
- **Rejected — scribe Watch count (draft).** The first draft said "47 distinct scrub.c lines cited by the
  r42/r43 notes: 42 byte-identical, 5 shifted by +2". No command backs it; the count was not re-derived.
  Rejected at landing and replaced by the measured facts: `diff -u` of the two pinned copies has 4 hunks
  (`@@ -568,7 +568,7 @@`, `@@ -1372,7 +1372,7 @@`, `@@ -1594,14 +1594,6 @@`, `@@ -1645,6 +1637,16 @@`), and
  `grep -c -i 'revert\|old_limit'` returns 0 for both r42 and r43 (negative claim; the positive control
  `grep -c -i limit` on r42 returns 21, so the pattern is not vacuous).
- **Rejected — "not inside the device loop" as an unqualified statement about the code path.** Kept only
  as SL2, marked [inference from the loop order] with no run behind it.
- **Frozen-counter rejections (not admissions).** The frozen C1 predicate admits a sourceless S284 row and
  a fake SL note (R1Reviewer controls B and C pass; K1 attack A1 FALSIFIED). This is recorded as a named
  limit, not hidden behind the PASS. See Mistakes R67-COUNTER-SHAPE-ONLY.

C2 gate evidence (patch `drafts/c2-patch.diff`, two hunks, `tools/check-adjacency-anchors.py`):
the base gate's outbound loop calls `_live_object_hash`, which returns `None` for an unresolved
`sibling_commit`; the caller simply skipped it. Measured: base mutant PASS with `live_object_checked 9`
(`probes/e2-mutant-base.json`); patched mutant FAIL with `ANCHOR-LIVE-OBJECT-UNRESOLVED`
(`probes/e2-mutant-patched.json`); honest base PASS 10/10 both base and patched
(`probes/e2-honest-base.json`, `e2-honest-patched.json`); absent sibling directory PASS with no finding
(`probes/e2-absent-sibling.json`); `--selftest` base 25/25 → patched 26/26 (`probes/e2-selftest.txt`).

Spot-check (LEARNING.md "Discernment is checked from outside"): the lane's own admits and rejects are
recorded above (2 admits, 2 rejects). The non-author closure owes its own spot-check. Suggested sample:
re-open S284 and S285 (URL, sha256, the two located lines) and the SL2 inference; and the C2 mutant
(re-run `probes/c2-mutant-battery.sh` against the landed tool). The two attack seats that disagree with the
lane's own readings are named here so the closure does not have to rediscover them: R1Reviewer FAILS the
C1 counter (controls B, C pass), K1Critic FALSIFIES C1 attack A1 (wrong URL passes the row predicate).

## Mistakes

- **R67-FLEET-MISROOT-SCORECARD** — class `landing`. Evidence: the lane edit call with the relative path
  `SCORECARD.md` wrote a 29-line round-67 declaration into the FLEET-root `SCORECARD.md`
  (`git -C /home/vgpnk/Projects/shokunin diff --stat -- SCORECARD.md` → `1 file changed, 29 insertions(+)`).
  The relative path resolves at the fleet root; the round prompt warned of exactly this (§6, "Seat paths
  are absolute"). Captured-by: `none` — nothing in the edit path checks the resolved target before a
  write. Fix: a guarded truncation removed the 29 lines (asserted to be exactly the inserted block first;
  the trailing blank line restored). Shown able to fail: before the fix the fleet diff stat reads
  `29 insertions`; after it, the same command prints nothing (rc 0). The declaration was re-applied at the
  lane path and frozen at `071a55c9`. Carried forward: every lane edit uses an absolute lane path, and a
  fleet-root `git diff --stat` follows any edit that could resolve there.

- **R67-FIXTURE-SED-NON-ROW** — class `vacuous`. Evidence: in the round-start control run
  (`/fast/scratch/hyaku/tsukuroi-r67/l1/controls/`), a `sed` meant to fabricate one AR row's HEAD also
  replaced the sibling cell, so the row stopped matching the frozen regex; the frozen count read 9, which
  looked like a kill of the fabricated-HEAD mutant but came from a malformed fixture. Captured-by: `none`.
  Fix: fixtures are built by splitting the row into its cells and rewriting one cell; the battery asserts
  the unmutated fixture still counts the baseline before any mutant is scored. Shown able to fail: the
  malformed fixture reads 9 against a baseline of 10, so the baseline assertion would fire.

- **R67-NUMBER-DRIFT-WATCH** — class `number-drift`. Evidence: the S1Scribe draft's Watch section stated
  "47 distinct scrub.c lines ... 42 byte-identical ... 5 shift by +2" with no command; the count was not
  re-derivable from the committed bytes. Captured-by: CORPUS.md "A count carries its command" (the rule
  existed; the drafting seat did not apply it, and the L1 accepted the paragraph before landing). Fix:
  the paragraph was replaced by the four measured hunks and the grep counts in the landed note's Watch
  section, each with its command. Shown able to fail: the same positive control (`grep -c -i limit` on
  r42 → 21) proves the pattern can return nonzero; the negative count is 0 for a reason, not by default.

- **R67-COUNTER-SHAPE-ONLY** — class `vacuous`, routed, not fixed in-round. Evidence: `probes/m1-c1-counter-battery.txt`
  (mutation-tester M1). The frozen counter `grep -cE '^\| SL[0-9]+ \|'` PASSes 4 of 5 fixtures: a
  header-row-only control (Ma) is killed, but four-row files with duplicate ids (Mb), a row inside a
  fenced code block (Mc), a prose row (Md) and empty evidence cells (Me) all pass. A strict counter
  (distinct ids, a non-empty line-number evidence cell, no fenced-block rows) kills all five, and the
  control K0 still reads PASS. Captured-by: `none` (the frozen predicate is shape-only; R1 control C and
  the sourceless S284 control show the same gap for the SOURCES side). Fix: the strict counter is the next
  frozen-counter amendment, declared before data next round; it is NOT applied to C1 this round (frozen
  predicate, CORPUS.md rule: a rule changed after scoring is not the claim's rule). Shown able to fail:
  Ma/Mb/Mc/Md/Me are the red fixtures.

## Seat-harm incident log (standing per-round tally; considerthese 2026-10-26.md:19 adopted r66)

- Seats spawned 11; settled 11; dead 0; provider errors 0.
- Seat-owned trees left on disk: `/fast/scratch/hyaku/tsukuroi-r67/E3Fixture/` (an empty directory after
  the seat's trap ran — a defect of the seat's own, minor; removed by the L1 at landing).
- Misroot writes by seats: 0 (N1Sentinel SWEEP1-3 PASS). The one misroot in this round was the L1's own
  edit (R67-FLEET-MISROOT-SCORECARD above).
- `/tmp` citations: 0 (N1Sentinel SWEEP6 PASS).
- Relative-path incidents by seats: 0.

## Routed (from the round-66 closure, `corpus/lessons/round-66-verifier-spotcheck.md` §6)

1. **R66-M3 (AR counter resolve-then-count) — not applied.** This round's C2 fix changes the gate, not the
   frozen `AR` row regex in the round-66 declaration. The regex remains shape-only (a fabricated 40-hex
   HEAD still counts). Routed to the next round's frozen-counter amendment, with the gate now as the
   live-HEAD check that does resolve.
2. **R66-M4 (CB header-row inflation) — not re-run this round.** The proposed `^\| CB[0-9]+ \|` counter is
   the same class as the SL result above; carried.
3. **Gate gap: `source:` value unvalidated** (round-66 closure defect 2; critic K1 C1 Attack 2). Not
   addressed; routed.
4. **Display cell** in `adjacency-recheck-r66.md` §4 (one leading space; no predicate reads it). Not touched
   (knowledge file, cosmetic, routed).
5. **r65 C2 A/B sensitivity demonstration; L0 `tsukuroi | round-64` id-drift question** — still open; routed
   around. Assimilation: none (no operator answer in `.ufo/l0-questions.md`).
6. **considerthese:** the 2026-10-22 "Self-improvement ideas (proposals only, nothing acted on)" block and
   the earlier blocks were not mined this round; the round's budget went to C1 and C2. Routed.

## Trend verdicts (author-side; non-author verdict pending the closure judge)

- **expansion: improved.** One sourced entry on uncovered ground (scrub-limit restore timing, S284/S285, `mined`).
- **quality: improved.** The adjacency gate now fails an unresolved commit instead of silently uncounting it
  (QUALITY 100); the existing scrub notes are re-read against the v7.3 bytes and nothing in them is contradicted.
- **discernment: unchanged.** The two attack seats found real gaps in the lane's own C1 counter (routed as
  R67-COUNTER-SHAPE-ONLY); the lane did not catch them at write time. One round of self-assessed admits does
  not demonstrate improved discernment, and nothing shows harm.
