# AdmissionCritic — round 12 protocol-admission audit

Seat: critic, dispatched by the tsukuroi L1, so this file is **author-side**. It is not independent
non-author verification and earns no `[x]`. Axes: operability and depth (admission conformance only).
Base: HEAD `b76b5c377eaee3e3d8d47fdddde977828d05dbd5`, clean except untracked `.ufo/waves/round-12/`
(`git status --short --untracked-files=all`, rc 0). Read-only. I wrote only this file. No installs, no
sudo, no tests or census runs, no git mutation. C1 and C2 had not landed when I reviewed: no
`root_mode` in `tools/`, and `corpus/knowledge/root-dac-decision-r12.*` is absent. My findings
therefore cover the baseline contract and the wave evidence only.

**Outcome: no PASS. Admission is PENDING.** Under the protocol, round 12 can only be admitted by the
hyaku closure session after landing. Nothing in this wave can admit it.

## 1. Authority chain (exact anchors)

| Rule | Anchor |
|---|---|
| Seats the lane dispatched are still the lane | `/home/vgpnk/Projects/shokunin/LEARNING.md:42-46` ("A subagent the lane dispatched is still the lane.") |
| Outside spot-check: at least 1 admit and 1 reject, recorded agree/disagree | `LEARNING.md:42-45`; closure duty `scripts/hyaku/closure-prompt.md:31-34` |
| Admission requires every claim verified and no axis harmed | `AXES.md:33-37`; prompt `.ufo/prompts/tsukuroi-round-12.md:37-40` |
| Driver completion is not admission | prompt `:59`, `:128-129`; canon `PROTOCOL.md:173-174` |
| `[x]` only with a named non-author; otherwise it counts as `[~]` | `PROTOCOL.md:66-68,450-451` |
| The admitting party is a fresh hyaku closure session (`@m_opus`) that writes `round-12-verifier-spotcheck.md` and the MANIFEST row | `closure-prompt.md:1-3,35-53`; `hyaku.env:5` `JUDGE_MODEL=@m_opus` |
| Planner ruling: the L1 holds the §3 planner seat; the data-walk may ride a revenger item; record the mapping in the report | `scripts/hyaku/lane-addendum.md:33-36`; L0 answer on `.ufo/l0-questions.md` line `tsukuroi \| round-12 \| Reconcile required planner-role seat…` (fleet commit `3eb7c58`, 23:15:00 -0300) |
| Validator excludes `planner` | `~/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs:246-259` (`SWARM_ROLES`, ten roles, no planner) |

## 2. Conformance observed (measured, not a PASS)

- **One batched wave of 32 seats.** `dispatch.json` reports `counts.spawn=32` and `total=32`, with
  one `taskCall`. `record-result.json` records `exit=0` and empty stderr. The registry has 32
  members. Mix: executor 3, scout 8, connector 4, reviewer 6, critic 3, sentinel 1, revenger 2,
  mutation-tester 1, scribe 3, simplifier 1. This meets the §3 floor apart from the planner role,
  which §3 below covers.
- **Godspeed lead is byte-exact.** For all 32 tasks, the task starts with `/skill:godspeed\n` plus
  the `godspeed/SKILL.md` body (python check: 32/32). `taskCall.context` is byte-equal to
  `spec.context`, which carries the RULES.md tooling sentence (prompt §6.7).
- **SHONEN is in canonical form.** With marks and the indented evidence lines stripped, the file
  equals the `PROTOCOL.md:441-448` seed (python check `True`). There are 4 `[~]` boxes and 0 `[x]`.
- **Lane identity and upstream.** `git config user.name` is `tsukuroi-shokunin` and
  `user.email` is `tsukuroi@shokunin.local`. The upstream is `origin/master`, ahead 0 and behind 0.
- **Source census at start.** `before.json` records `source_validate_exit: 0`, `tsukuroi ok`.
- **Honesty markers in seat files.** C1Review, CensusScribe, ClaimCritic, FixtureReview,
  ScoreReview, ReportScribe, GateScribe and SourceReview each state "author-side" and/or "nothing
  here is a PASS", and they mark unrun checks as unrun.

## 3. Conformance risks (counterexample → impacted axis → smallest safe correction)

**R1 — HIGH: planner-seat accounting.** The registry seats `Planner` as `role: revenger`
(`swarm-registry.json:8-18`). Under the ruling, a revenger item satisfies nothing in the §3 planner
slot; the L1 holds that seat. The rendered prompt (`tsukuroi-round-12.md`, mtime 23:10:55) predates
the ruling (`3eb7c58`, 23:15:00), so the ruling text appears nowhere in the dispatched contract.
- Counterexample: a report line such as "L2 floor: 1× planner (Planner)" counts a revenger as a
  planner.
- Impacted axis: operability (report conformance).
- Fix: add one report line, for example: "§3 planner seat: held by the L1 per the hyaku ruling
  (`lane-addendum.md:33-36`, L0 answer committed `3eb7c58`). The bounded data-walk rode revenger
  item `Planner`. Validation was not bypassed." Do not list `Planner` under the planner role
  anywhere.

**R2 — HIGH: "pending, not pass" must survive into every artifact.**
- No outside check exists for round 12. `corpus/lessons/round-12-verifier-spotcheck.md` is absent,
  and the closure session writes it only after landing (`closure-prompt.md:35-41`).
- No seat in this wave is non-author. All 32 were dispatched by the lane.
- Counterexample: a SCORECARD row, LOG entry or report verdict saying `improved`, `admitted` or
  `verified` without a "self-assessed, pending hyaku closure" qualifier. The same applies to
  `discernment: improved`, which needs the outside agree/disagree (`LEARNING.md:35`).
- Impacted axes: calibration, and the report as a whole.
- Fix: label every per-axis verdict and trend as self-assessed. Set discernment to `unchanged
  (no outside spot-check in round)` unless a criterion grounded in a lesson lands. Keep SHONEN
  `[~]`. Follow the round-1 wording (`SCORECARD.md:184-185`, `LOG.md:406-407`).

**R3 — HIGH: the Gate must offer at least one admit and one reject the closure can sample.**
Closure step 3 samples from `corpus/lessons/round-12.md ## Gate` (`closure-prompt.md:31-34`).
GateScribe currently issues no verdict and lists only PENDING items (`GateScribe.md:5,62-75`).
- Counterexample: a Gate with only the C2 admit leaves closure no reject to sample. Discernment then
  cannot verify, and the closure may grade the round as non-conformant.
- Fix: record at least one real rejection with its reason and flip condition, opened this round.
  Candidates:
  - #6629 same-symptom≠same-cause (`Issue6629.md:116-122`);
  - the #8047 overlay-restore claim (`Issue8047.md:32-36`);
  - the R6 "pre-existing `@.snapshots` → EACCES" reading (`MountErrors.md:91-93`).
- Each must use the URL, access date and ≤25-word quote format (CORPUS SOURCES rule 1).

**R4 — HIGH: C1's counting command measures token presence, not the claimed discrimination.**
The red-before gate counts `\broot_mode=` tokens on the live `PLANE packages:` line
(`CensusScribe.md` §8: before `root_mode_count=0`, `gate_exit=1`).
- Counterexample: an arm that always prints `root_mode=0755` turns the gate 0→1 (green) while doing
  none of the 0755/0555/unreadable discrimination in the C1 claim. MutationPlan's M4 (hardcoded
  host root) and an "ignore-unknown" mutant (M3) would also keep this live gate green.
- The live gate also depends on host state, not only on the tree.
- Impacted axis: operability (measurement validity).
- Fix: pair the live 0→1 with a hermetic count of named consumer-visible fixture cases on HEAD.
  The cases are 0755 no-finding, 0555 DEGRADED, missing/dangling-link BLOCKED and non-dir BLOCKED
  (`C1Review.md:91-99`). Base must show 0 and HEAD N, with a mutant red run, so the closure can
  re-derive the claim.

**R5 — HIGH: C2's counting command measures schema completeness, not grounding.**
`before.json:C2_command` counts branches whose six fields are non-empty.
- Counterexample: 4 branches with `source_ids: ["S999"]`, or with a discriminator such as `sudo
  test -w /`, would count 4. That violates "grounded…not text-match count", the read-only rule
  (`GateScribe.md:75`) and SOURCES existence.
- Impacted axis: depth.
- Fix: extend the predicate:
  - every `source_ids` member is a `mined` row in `corpus/SOURCES.md`;
  - every discriminator has a recorded read-only run with exit code (e.g.
    `discriminator-smoke.json`);
  - the deterministic scenario inputs classify to the expected branch.
- Report the score as ScoreReview bounds it: at most 8→9, or `improved` with the score unchanged
  (`ScoreReview.md:43-44`). Planner advises against an arbitrary gain (`Planner.md:36`).

**R6 — MEDIUM: depth bar vs placement.** AXES defines depth's bar as "A reader can act on SKILL.md
alone" (`AXES.md:11`). Matrix owns only `corpus/knowledge/root-dac-decision-r12.{md,json}`, and no
seat owns `SKILL.md` or `corpus/README.md`.
- Counterexample: the closure judges "SKILL.md unchanged → depth bar not met".
- Fix: during integration, the L1 adds one SKILL.md pointer or decision row plus a README index row
  (QUALITY #10). C2 must not cite census output, to keep it separable from C1 (`ScoreReview.md:35-36`).

**R7 — MEDIUM: conflicting score tables.** The lowest-axis obligation depends on which table is
read.
- `SCORECARD.md:45-52` still reads adjacency 7, coverage 8, freshness 8.
- `SCORECARD.md:177,209-238` and the MANIFEST round-1 closure (admitted) give adjacency 8,
  coverage 9, freshness 9.
- Counterexample: a judge reading the first table finds adjacency 7 as the unique lowest. C2 (depth)
  then fails the lowest-axis rule.
- Fix: the round-12 SCORECARD append states the authoritative current vector and its sources. These
  are the post-review section `459e3ce` and MANIFEST `rounds[309]` `verdict: admitted`, with depth 8
  and adjacency 8 tied (`ScoreReview.md:13-29`). Record it as a dated supersession, not a rewrite.

**R8 — MEDIUM: round namespace and predecessor check.**
- The driver renders `PREV=11` (`slot-driver.sh:82`), so prompt §6.5 points at the absent
  `round-11-verifier-spotcheck.md`.
- The substantive predecessor is fleet round-1 (`MANIFEST rounds[309]`, `namespace: "fleet-2
  relaunch round-1 continuation"`, `lane_round: 1`). Its outside check exists:
  `corpus/lessons/round-1-verifier-spotcheck.md`.
- The tsukuroi round-1 L0 namespace question has no answer on its line (`l0-questions.md` line 42,
  checked for `ANSWER`: none).
- `.ufo/state/tsukuroi.round` reads `1` while hyaku `next/tsukuroi` reads `12`.
- Fix: the report names the namespace: hyaku lane-round 12 follows train r11 and fleet r1. It also
  handles the round-1 spot-check disagreement. That disagreement (the adjacency-recheck entry lacked
  `## QUALITY check`) was answered as "admission miss, not a criteria gap" (`corpus/lessons/round-1.md:144`).
  §6.5 allows "say why not", but the report must actually say it.
- Optional: an L0 line re-asking the namespace ratification.

**R9 — MEDIUM: seat overclaims that must not flow into admitted text.**
- `Issue6629.md:165` says "Status: PASS". `:120` says "journal records prove…". `:166` says the
  failure was "caused by `/` mode 0555 intersecting with… CAP_SYS_ADMIN".
- The admitted note keeps that mechanism `[inf]` (`snapper-eacces-mechanism.md`; `CensusScribe.md:70`).
  `discriminator-smoke.json` `limits` also says "not proof of historical service EACCES cause".
- The smoke's EACCES fixture ran as uid 1000. It does not reproduce a root process bounded to
  CAP_SYS_ADMIN.
- `Issue8047.md:32` treats an `@omarchybot` comment as "falsified". That is tier-C community
  evidence and is never sole support (QUALITY #7).
- Fix: Matrix/Sources/Gate text keeps [obs], [inf] and [unknown] separate (QUALITY #3). No PASS from
  any seat file is quoted as a verdict.

**R10 — MEDIUM: wrong idea of who is non-author.**
- ScoreReview says W3ReviewTsukuroi "do[es] not count" because it was dispatched
  (`ScoreReview.md:73`, citing `AXES.md:47-49`).
- `LEARNING.md:45-46` limits the exclusion to subagents *the lane* dispatched. W3 was dispatched by
  the orchestrator (`round-1-verifier-spotcheck.md:3-6`). The closure prompt likewise lets the
  non-author session dispatch reviewer seats (`closure-prompt.md:17`).
- ReportScribe correctly notes that no non-author re-reviewed the amended round-1 tree after
  `459e3ce`/`daa9187` (`ReportScribe.md:56-57`). Admission was the integrator's adjudication
  (`d8ec15d`).
- Fix: the round-12 report neither re-litigates round-1 admission (MANIFEST is canonical) nor
  imports ScoreReview's stricter reading as fact. If the L1 disputes it, it files an L0 line.

**R11 — MEDIUM: wave-1 reviewers saw only the contract.**
- C1Review: "Final static review … pending the Census readiness ping" (`:118`). ClaimCritic:
  "Re-review needed once … land" (`:136`). GateScribe: all PENDING.
- Counterexample: the report cites them as review of the landed C1/C2.
- Fix: either send the parent's final-revision message and get a re-review of the landed revision
  (the context allows this), or say explicitly that reviews covered the contract only. Either way,
  the reviews remain author-side.

**R12 — LOW: unattributed evidence files.** `before.json` (23:15:11) and `discriminator-smoke.json`
(23:16:44) are not `<seat>.md` files, and no seat file references them (grep: 0 hits).
- Fix: the report names their author (the parent, presumably [INFERENCE]) and commits them with the
  wave evidence.
- `discriminator-smoke.json` created and removed a temp-dir fixture (no write to the host root).
  That is consistent with its `fixture_scope`, but it is still a write and should be named.

**R13 — LOW: landing mechanics the closure checks.** Closure step 1 checks that the report is
committed by the lane identity, cited hashes are ancestors, the tree is clean and pushed
(`@{u}..HEAD`), and the prompt carries the contract (`closure-prompt.md:19-24`).
- Round-1 recorded a standing "No push" rule (`LOG.md:405`). The newer hyaku operator directive
  requires "commit and push after every round" (`lane-addendum.md:3-5,51-54`). The report should
  name which rule applies.
- Commit all 32 seat files plus `spec`, `dispatch`, `swarm-registry`, `record-result`, `before` and
  `smoke` under `.ufo/waves/round-12/` (pathspec-limited). If any are left untracked, closure
  reports "uncommitted round work".
- The lane's round-12 L0 append was committed by the orchestrator as `ci <ci@local>` in `3eb7c58`.
  That is not a lane-commit defect, but the report should name it.

**R14 — LOW: correlated reviewer model** [INFERENCE]. The closure judge (`@m_opus`) and every lane
critic/sentinel seat (`omp-overlay.yml:22-23` → `anthropic/claude-opus-5-5`) share one model. The L1
runs on `@m_strong` (`openai-codex/gpt-6.1-sol`).
- Non-authorship holds by protocol, but model-level blind spots may coincide.
- This is a tradeoff to name in the report, not a defect to fix in the lane.

**R15 — LOW: protocol copy drift.** The canon and fleet-root copies of PROTOCOL, LEARNING, MISSION,
CORPUS and PROTOCOL-APPENDIX differ (`cmp` rc 1; diff lines 71/12/42/63/2). AXES is identical.
- The LEARNING admission text differs in wording only.
- The report should cite which copy each rule comes from, because closure loads the canon copy
  (`closure-prompt.md:6`).

## 4. What would make admission conformant (minimal list)

1. Report:
   - planner mapping line (R1);
   - every verdict labelled self-assessed, pending hyaku closure; discernment unchanged; SHONEN `[~]` (R2);
   - Stale-lane line, installs line ("none" where true), namespace line and predecessor spot-check
     handling (R8);
   - each cited hash pushed and an ancestor.
2. `corpus/lessons/round-12.md`:
   - `## Gate` with at least one admit and at least one reject, each with URL, date and a ≤25-word
     quote (R3);
   - `## Mistakes` row whose fix is shown able to fail. The C1 red-before gate exit 1 is a candidate
     demonstration.
3. Counting commands the closure can re-derive at HEAD. C1 needs hermetic fixture case counts plus a
   mutant red run (R4). C2 needs a grounded predicate (R5). Before values come from `git archive`
   of `b76b5c3`.
4. A SCORECARD append that declares the current axis vector and its supersession (R7).
5. Source census exit 0 at round end.

## 5. Commands run (all read-only)

- `git rev-parse HEAD`; `git status --short --untracked-files=all`; `git log --oneline -15`: rc 0.
- `git remote`; `git rev-list --count @{u}..HEAD` → 0; `HEAD..@{u}` → 0; `git config user.name/email`: rc 0.
- jq over `spec.json`, `dispatch.json`, `swarm-registry.json`, `record-result.json`: rc 0.
- python: Godspeed prefix check 32/32; SHONEN seed check `True`; record exit 0.
- `cmp` canon vs fleet protocol files: rc 1 (differ); AXES rc 0.
- `jq` over `MANIFEST.json` `rounds[133]` (train r11) and `rounds[309]` (fleet r1, admitted): rc 0.
- Read `.ufo/state/tsukuroi.round` → `1`; `~/.local/state/shokunin-hyaku/next/tsukuroi` → `12`.
- `git -C /home/vgpnk/Projects/shokunin show 3eb7c58 --stat` and `git log` on `lane-addendum.md`: rc 0.
- Unrun: selftest, live census, sources-census, any C1/C2 artifact (absent at review time).
- Installs/updates: none.
