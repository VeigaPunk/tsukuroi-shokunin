VERDICT: defect-found

# Round-50 report-contract checklist for L1

Evidence basis: round-50 prompt §4 and its pre-report instructions (§4 at prompt lines 118 onward; gates at lines 499–504); template `templates/round-prompt.md` §4; round-49 filed report; `corpus/lessons/round-49-verifier-spotcheck.md` §6; current draft `.ufo/reports/round-50/tsukuroi.md`; `SHONEN.md`; frozen claims `round-50/frozen/FROZEN.md`. Supporting excerpts and the role-count calculation are in `w1/R50ReviewerReport/`.

## Required report sections, in order

- [ ] **Work performed.** Start by naming each of the 1–3 declared claims and its target axis or capability. Then give one bullet per work item, each with a resolvable evidence pointer (path:line, command output, or commit hash). The current draft names C1–C3 but still has `Work items ...: TBD` (`.ufo/reports/round-50/tsukuroi.md:14-31`). Its round-shape summary should also report dispatched/results/reports/dead-seat counts and explicitly state whether there was a residual call; do not leave values as `TBD`.
- [ ] **Landed changes.** Account for every landed change, tying each to its `LOG.md` entry and the commit hash that carries it. The draft currently says `TBD` (`.../tsukuroi.md:39-41`).
- [ ] **Before → after measurements.** One row per claim. Each must identify claim → axis, the counting command, before value and revision, after value and measured revision/commit, and verdict; cite the before/after receipts. Report a failed predicate honestly, including its blocking legs; do not narrow a frozen target. The frozen predicates are in `tsukuroi-shokunin/.ufo/waves/round-50/frozen/FROZEN.md` (C1–C3 table); the section is currently `TBD` (`.../tsukuroi.md:43-45`).
- [ ] **Sources & frontier.** Record the exact census command and start/end outputs plus exit codes; rows before→after; rows added by tier; each touched row old→new; rows opened this round; and frontier rows advanced (or explicitly none). Include required Gate/admit/reject and curation evidence and state assimilation/considerthese outcome. End-of-round census exit 0 is required. This section is currently `TBD` (`.../tsukuroi.md:47-49`).
- [ ] **Trend verdicts.** Give exactly one evidence-backed verdict for each of expansion, quality, discernment, using `improved`, `harmed`, `unchanged`, or `unprovable-but-better`; no scalar. This section is currently `TBD` (`.../tsukuroi.md:51-53`).
- [ ] **SHONEN.** Exactly one `## SHONEN` heading and one status line per box in `SHONEN.md` (there are 4 boxes: `SHONEN.md:5,7,9,11`). `[x]` only with a named non-author verifier; `[~]` needs a resolvable evidence pointer; `[ ]` means untouched. Draft heading count is currently 1, but the content is only `TBD` (`.../tsukuroi.md:55-57`), not four box lines.

Also retain the round-50 §6 report extras after the required sections: a `Stale-lane` line and any tool installs (or explicitly state none). Report installed/updated tool, version, channel, and reason if applicable. The current draft has a Stale-lane line (`.../tsukuroi.md:59`) but it must not be mistaken for a residual-risk/verification-gap statement.

## Claim fields and traceability checklist

For **each** claim, make the chain explicit and mutually consistent across the report, frozen record, SCORECARD, LOG, and receipts:

- [ ] Claim ID and declared target: one concrete, falsifiable before→after value.
- [ ] Axis and changed surface (not merely the counter output); identify sourced claim/source when applicable.
- [ ] Frozen counter command, predicate and kill rule; state the frozen measurement revision.
- [ ] Before value + base revision + receipt; after value + measured commit/revision + receipt; verdict (PASS/FAIL or exploratory verdict, as declared).
- [ ] Landed changes have their LOG entry and carrying commit; the report's final cited lane hash is pushed and the cited measurement commit is on its ancestry.

The exact frozen claim axes, counters, before values and predicates are `frozen/FROZEN.md` lines 15–35. Required measurement shape follows prompt §4 and prompt §9 claim-sizing rules (prompt lines 529–551). Do not conflate integration/final-tip hash with the revision against which a counter was actually measured.

## SHONEN and pre-report gates

- [ ] Run `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin ls-remote origin refs/heads/master` before writing the report; its output MUST be the final lane hash. If it is older, the lane commits are not pushed. Cite the final pushed hash in the report. Binding text: round-50 prompt lines 499–502.
- [ ] Before fleet-report commit, run `grep -c '^## SHONEN' /home/vgpnk/Projects/shokunin/.ufo/reports/round-50/tsukuroi.md`; it must print `1`, followed by four SHONEN status lines, one per checklist box. Binding text: prompt lines 503–504. Current draft heading count is 1, but its `TBD` does not meet the four-line requirement.
- [ ] Wait for WAVE-DONE and the results JSON before finalizing seat counts/report (round-50 prompt lines 229–230; run-9 lesson in prompt §6).
- [ ] Complete the §3 misroot sweep before report writing; record any lane/round seat files copied from fleet root under `## Mistakes` (prompt lines 436–443).
- [ ] Confirm the end-of-round SOURCES census exits 0 (prompt §2b and lines 624–625).
- [ ] Commit/push the lane via the lane helper, then commit/push the fleet report via `fleet-commit.sh --as tsukuroi`; report lands last and cites the pushed lane hash (prompt lines 444–454, 493–504).

## Round-49 spot-check lessons this report must avoid

- [ ] **V1 — do not rewrite a filed report in place.** Spot-check §6 says report `85becaa2` was filed and `de2a8b75` later rewrote a line; protocol permits correction only in the correcting round's report or an appended erratum naming superseded text. Resolve every placeholder and proofread before the first fleet filing; if a correction is needed after filing, append a clearly labeled erratum rather than editing filed bytes (`corpus/lessons/round-49-verifier-spotcheck.md:170-176,220-221`).
- [ ] **V6 — state the attack-share basis and make arithmetic match it.** Spot-check §6 requires the counted role set to be named (`...spotcheck.md:191-196`). The current round-50 draft names reviewer+critic+sentinel+mutation-tester but claims `44/71 = 62.0%` (`.ufo/reports/round-50/tsukuroi.md:8-11`). The frozen dispatch has reviewer 19, critic 18, sentinel 2, mutation-tester 4, revenger 1 (`w1-spec.json`, 71 items; receipt `w1/R50ReviewerReport/role-histogram.txt`): the named set is 43/71 = 60.6%; 44/71 = 62.0% only if revenger is included. Correct the numerator/percentage or explicitly include revenger if it qualifies under the round's policy.
- [ ] **State residuals and verification gaps explicitly.** Do not let a `Stale-lane` sentence stand in for them, or leave a residual call/count as an implication. State remaining unverified obligations/known limits and whether there was a residual call. Round-49's report has no explicit residual-risk/verification-gaps heading (its headings are at `.ufo/reports/round-49/tsukuroi.md:14,64,79,94,116,126,144`; `Stale-lane` is only at :144), although it does mention specific C1 and SHONEN gaps at :89 and :131–138. For round 50, make residual risk and verification gaps a clearly labeled, evidence-backed closing statement; distinguish them from the required Stale-lane line.

Additional round-49 defects V2–V5 and V7 are also relevant to honest reporting: preserve the disclosed freeze amendment; keep a needed repin with the triggering edit; do not overstate a counter whose citation leg rejects valid reports; report C3's content check rather than a shape-only result; and disclose any selftest flake rather than suppressing it (`corpus/lessons/round-49-verifier-spotcheck.md:176-210`).

## Current-draft findings

1. **Defect — attack-share arithmetic/basis mismatch:** `44/71 = 62.0%` is inconsistent with the parenthesized role set, whose dispatch counts sum to 43. Correct before filing.
2. **Incomplete — report still contains placeholders:** work items, all result counts, landed changes, measurements, sources/frontier, trend verdicts and SHONEN lines remain `TBD` (`.ufo/reports/round-50/tsukuroi.md:10-11,31,41,45,49,53,57`). This is a skeleton, not a filing-ready report.
3. **Checklist risk — residual statement:** current `no residual call` is a useful count, but add explicit residual risks and verification gaps once evidence is settled; retain the separate Stale-lane line.

Verification scope: I inspected the contract, round-49 report and spot-check, frozen claim record, SHONEN checklist, current round-50 draft and 71-item spec. I did not run any claim counters, census, lane `ls-remote`, wave completion check or report commit; those are L1 gates, not verified here. No tools were installed.