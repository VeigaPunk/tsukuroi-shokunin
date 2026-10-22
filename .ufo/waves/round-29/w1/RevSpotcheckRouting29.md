# RevSpotcheckRouting29 — routed-item → round-29 disposition map

Seat: TsukuroiR29.RevSpotcheckRouting29 (reviewer, wave 1). Read-only check of the round-29
declaration (`SCORECARD.md`, last section "## Round 29 — declaration, attempt 1",
declaration commit `81a061a67466c5e1be812814a895a4b5ed89b4ff`, claim base `16e9ab2a…`).

## Verdict

Partly holds: every round-28 routed defect 1–7 and every carried round-27 item (routed 4,
5, 6) has a named round-29 disposition, and the item-1 receipt is committed at the tip and
records the tip counter `99f35675…` with 0 of 5 and control 6; residual gaps are the two
sub-parts of routed items 1 and 6 the declaration does not name.

## Findings

1. **Routed 1 (C2 receipt revision gap) — dispositioned, receipt verified, one sub-part
   unaddressed.** [obs] The declaration dispositions it as a non-claim item: "1 a C2 battery
   receipt at the tip counter `99f35675…` (`.ufo/waves/round-29/measure/r28-c2-battery-at-16e9ab2a.jsonl`,
   run during screening from an export of the base: 0 of 5, control 6)"
   (`SCORECARD.md`, round-29 "Routed items … that are not claims" paragraph). The receipt is
   committed at the tip: `git ls-tree 81a061a…` shows blob `2bf74d24…` at
   `.ufo/waves/round-29/measure/r28-c2-battery-at-16e9ab2a.jsonl`, and its content sha256 is
   `4c41ed9e…` identical in the commit and the working tree. Its summary line records
   `"counter_sha256": "99f35675315d89d7feeac55d0500c3520651ddc842b15d0b2d6cb752415a64e7"`,
   `"counter_rev": "16e9ab2a"`, `"base": "16e9ab2a…"`, `"should_fail_total": 5`,
   `"should_fail_accepted": 0`, `"control_verified_rows": 6`, `"harness_errors": []`.
   Independently re-hashed: `git show 81a061a…:tools/check-kernel-taint.py | sha256sum`
   = `99f35675315d89d7feeac55d0500c3520651ddc842b15d0b2d6cb752415a64e7` — so the receipt's
   `counter_sha256` IS the tip counter bytes, and 0 of 5 with control 6 is recorded.
   [obs] Residual: routed 1 also asked to "record a revision in the selftest receipts" and
   that the report "must not state `Gates at <rev>` without a committed receipt for that
   revision". The battery receipt now carries `counter_rev`/`base`, but the declaration names
   no disposition for selftest-receipt revision fields or for the `Gates at <rev>` citation
   rule. Both halves remain unverified/unclaimed. [inf]

2. **Routed 2 (battery environment leak) — claimed as C2, widened.** [obs] The declaration's
   C2 claim names "routed defect 2 of the round-28 spot-check, widened from the two batteries
   to every tool with a sandbox git write", frozen list of eight tools in
   `tools/probe-git-env-leak.py` (committed at the tip, blob `3c3d86ed…`), declared after
   `leaking` 0 of `targets` 8. The before receipt
   `.ufo/waves/round-29/measure/c2-before-81a061a67466c5e1be812814a895a4b5ed89b4ff.jsonl`
   measures `leaking` 3 of 8 (`check-adjacency-overlap.py`, `mutants-adjacency-overlap.py`,
   `mutants-kernel-taint.py`) — a real defect to fix, consistent with SentinelBattery finding
   3. The routed item's "add a selftest that can fail" is subsumed by the probe's canary-run
   design (`canary_rc`/`canary_changed` fields per target). [inf]

3. **Routed 3 (R4a 2-word half unanchored; MutC2Counter m1, m7) — non-claim routed item.**
   [obs] Declaration: "3 the R4a two-word half gets selftest cases that kill MutC2Counter m1
   and m7". Disposition present; verification is a wave-1 concern, not mine.

4. **Routed 4 (C1 padding shapes) — non-claim routed item.** [obs] Declaration: "4 the C1
   padding shapes". Named, not claimed.

5. **Routed 5 (carried round-27 defects 4, 5, 6) — split across C1 and non-claim items.**
   [obs] Carried 4 and 5 are claimed under C1: "the twelve owed statements of the round-27
   spot-check routed defects 4 and 5 (`corpus/lessons/round-27-verifier-spotcheck.md:102-103`),
   frozen as O01 to O12". The frozen anchors in `tools/check-owed-statements-r29.py`
   (docstring lines 8-10, anchor table lines 48-70) map them: O01–O04 = routed 5's
   "+200 band scanned first" reading (`oom-event-plane.md` ×2, `kill-event-deep-r8.md` ×2;
   `KERNEL_MECHANISM = {'O01'..'O04'}` at line 73, M7 requires a new `S###` source);
   O05–O07 + O08 + O09–O12 = routed 4's companion debt (MP4 qualifier in `SKILL.md` and
   `memory-pressure-r25.json`, `driver-firmware-plane.md` `[unk]`, four
   `storage-health-r26.json` statements SH1/SH3/SH4/SH5). Carried 6 (`check-self-assessment.py`:
   hyphenated headings, stale docstring, missing MutSelfAssessQ65 cases) is named as
   non-claim item "5 carried round-27 defect 6 (self-assessment tool)" — dispositioned but
   not a claim; whether it lands this round depends on wave work. [inf]

6. **Routed 6 (seat findings outside the report) — partially dispositioned.** [obs]
   Declaration: "6 RevFamilyB2's lost B2-family review is redone in wave 1" — the RevFamilyB2
   sub-item is named. SentinelBattery is effectively folded: its finding 3 is C2's basis and
   is cited in the declaration's Sizing paragraph
   ("`.ufo/waves/round-28/w1/SentinelBattery.md` finding 3"). [obs] Residual: the third
   sub-item — MutC1Counter "absent by design, frozen while still running" — has no named
   disposition anywhere in the declaration. Lowest-severity gap; arguably moot because C1's
   claimed counter is a different instrument, but the routed item named it and nothing
   answers it.

7. **Routed 7 (lowest-axis duty contested) — answered by framing.** [obs] Declaration: "7 is
   answered by the framing above", i.e. "each claim is placed on the axis its counting
   command measures" (C1 → depth via sourced-statement count; C2 → operability via
   runnable-artifact behaviour). The dispute stays open for the operator; the routed item is
   dispositioned as answered, not resolved. [obs]

## Routed items with no disposition

None of the seven round-28 items and none of the three carried round-27 items is wholly
undispositioned. The only unhandled sub-parts: (a) routed 1's selftest-receipt revision
fields and the "no `Gates at <rev>` without receipt" citation rule; (b) routed 6's
MutC1Counter absence. [obs]

## Cross-checks run

- `git ls-tree 81a061a… -- .ufo/waves/round-29/measure/r28-c2-battery-at-16e9ab2a.jsonl
  tools/check-kernel-taint.py tools/probe-git-env-leak.py tools/check-owed-statements-r29.py`
  → all four present at the tip (receipt `2bf74d24`, counter `41fd0cdb`, probe `3c3d86ed`,
  owed-checker `31000e9f`).
- `git show 81a061a…:tools/check-kernel-taint.py | sha256sum` → `99f35675…a64e7`, equal to
  the receipt's `counter_sha256`.
- Committed vs working receipt bytes: sha256 `4c41ed9e…` both ways.

## Residual risk / verification gaps

- Item-1 receipt was "run during screening from an export of the base" — it covers the tip
  counter bytes over base data, not a post-change revision; that is the correct scope for
  closing the round-28 gap but a closure reviewer may want a run at the final revision too.
- Carried round-27 item 6 and routed items 3, 4, 6 are non-claims; their disposition is "wave
  work", so "done" for the mapping ≠ "fixed".
- C2's before-value is already 3 of 8 (not the ≤1 the declaration's sizing note feared), so
  the declared direction is honest.

Scope: read=SCORECARD.md round-29 declaration, corpus/lessons/round-28-verifier-spotcheck.md §5, corpus/lessons/round-27-verifier-spotcheck.md routed list, the two round-29 measure receipts, tools/check-owed-statements-r29.py anchor table; wrote=.ufo/waves/round-29/w1/RevSpotcheckRouting29.md; executed=read-only git ls-tree/show/hash plus grep and sha256sum in the lane repo
Model: devin/swe-2
Installs: none
