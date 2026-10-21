# DebtRevSelectorMechanism — round20 build seat RevSelectorMechanism absence audit

Reviewed-SHA256: cc5abf6790328d685270fc3c82b5fb412d3ba00a39f078a9c126147d730fbf82
Predicate: round20-missing-report-RevSelectorMechanism

Target: `.ufo/waves/round-21/snapshot/corpus/lessons/round-20.md` (baseline source `corpus/lessons/round-20.md`; the SHA-256 above is the digest supplied in the assignment, not recomputed by this seat because it is NO-EXEC). Scope: only the round20 build seat `RevSelectorMechanism`.

## Axes

1. Identity: which role, assignment, and agent identity the seat had.
2. Absence: whether the report exists, and which gate observed its absence.
3. Death attribution: which retained record names the cause.
4. Claim discipline: what the absence does and does not prove.
5. Prevention: a finite test that would catch this class of gap.

## Observations (all files under `.ufo/waves/round-20/build/` unless stated)

- O1 Role and assignment. `spec.json` lines 322–325 declare `name: RevSelectorMechanism`, `role: revenger`. The prompt is NO-EXEC, read/grep/glob plus the report only: "reconstruct _commit ref-first hex alias mechanism and independent judge blindspot; distinguish absence in live repo from contract correctness". `plan.json` lines 744–746 and `dispatch.json` line 739 carry the same prompt plus "Report: write your scoped findings to .ufo/waves/round-20/build/RevSelectorMechanism.md".
- O2 Identity. `plan.json` lines 418–423 and `dispatch.json` lines 404–409 record `kind: spawn`, `role: revenger`, `agentId: null`. These are the pre-spawn records. `swarm-registry.json` lines 386–391 record `kind: spawn`, `agentId: "TsukuroiR19Recovery.RevSelectorMechanism-2"`, `role: revenger`, `item: null`. The registry itself was created at 2026-10-21T08:18:06.158Z and updated at 09:23:13.585Z (lines 4–5).
- O3 Report absence. A glob of `Rev*` under `.ufo/waves/round-20/` returns only `build/RevErratumHistory.md` and `build/RevNoWriteRule.md`, so `build/RevSelectorMechanism.md` does not exist. The seat name appears nowhere in `round-20/falsify`.
- O4 Gate observation. `measure/final-r20/`, `final-r20b/` and `final-r20c/` `seat-scope-build.stdout` each contain the finding `{"detail": "seat report absent", "id": "SCOPE-REPORT-MISSING", "role": "revenger", "site": "RevSelectorMechanism.md"}`. The final run at `fc2a0085088cedb3ab59dc3fff16523c0f42a6b4` reports `SCOPE-REPORT-MISSING: 13`, `status: FAIL`, `seat_count: 64` and `evidence_class: "self-reported declarations; no independent absence-of-execution proof"`. The finding is emitted by `tools/check-seat-scope.py` lines 71–74.
- O5 Dispatch-refusal records, which are not death records. `native-task-result.json` (attempt 1) lists "TsukuroiR20.RevSelectorMechanism: Background job limit reached (100)" with `results: []`. `native-task-result-retry-2.json` records `attempt: 2`, `spawned: 0`, `status: refused-before-spawn`. Both describe the failure to start jobs before any spawn. They name job label `TsukuroiR20.RevSelectorMechanism`, not the registry agentId. No machine-readable result file exists for the third, successful spawn call.
- O6 Death record. The only retained death record is the narrative at `LOG.md` line 1039: "the third unchanged call spawned all64 … Thirteen provider-rate-limit deaths (… AdjBoundary02, RevSelectorMechanism); no replacement." `LOG.md` lines 1047 and 1063, and the lesson's `R20-SEAT-DEBT` row plus its §Final measured outcome, repeat the 13 provider-rate-limit deaths, the absence of replacement, and the retained red.
- O7 No transcript found. A read-only grep for `RevSelectorMechanism` under `/home/vgpnk/.omp` matched nothing. No per-seat transcript, exit reason, timestamp or provider error payload for `TsukuroiR19Recovery.RevSelectorMechanism-2` was located in the repo or that directory.

## Inferences

- I1 [INFERENCE] The seat was spawned in the third dispatch call as `TsukuroiR19Recovery.RevSelectorMechanism-2` (registry) and exited without writing its report. The attribution to a provider rate limit rests only on the author-side LOG narrative (O6). No per-seat machine record corroborates it (O5, O7).
- I2 [INFERENCE] The attempt-1/2 `Background job limit reached (100)` records concern an earlier local job ceiling, not this seat's death. Citing them as the death cause would conflate two events.
- I3 The assigned question was left unanswered by this seat: the `_commit` ref-first hex alias mechanism and the independent-judge blindspot. Lesson rows `R20-HEX-REF` and `R20-C2-ORACLE` rest on other seats' evidence and the outside spotcheck. Nothing here makes them substitutes for this seat's report.

## Limits

- The seat's absence does not show that it executed nothing, and does not show that it executed something. Neither proof commands nor a `Scope:` declaration exist for it. This audit does not claim either.
- No report is invented, the dead identity `TsukuroiR19Recovery.RevSelectorMechanism-2` is not replaced, and no round20 file is edited.
- The reviewed digest was supplied by the assignment and not recomputed (NO-EXEC).
- This audit claims no non-author closure and no outside promotion.

## Append-only round21 debt-disposition sentence

Round21 retains round20 build seat `RevSelectorMechanism`, a revenger registered as `TsukuroiR19Recovery.RevSelectorMechanism-2` with prescribed report `.ufo/waves/round-20/build/RevSelectorMechanism.md`, as an unreplaced dead seat. Its `SCOPE-REPORT-MISSING` red remains open across final-r20, final-r20b and final-r20c. The only death record is the author-side `LOG.md` line 1039 provider-rate-limit narrative, without a per-seat machine record. The attempt-1/2 `Background job limit reached (100)` refusals are pre-spawn events, not its death cause. The absence is neither evidence that proof commands were absent nor evidence that they executed, and its assigned `_commit` hex-alias question remains unanswered by this seat.

## Prevention test (proposal only; not implemented or run)

Add a reconciliation case to `tools/check-seat-scope.py --selftest`, alongside the existing `report-missing` and `both-merged` fixtures. It reads a wave-local per-seat death ledger whose entries are `{name, agentId, cause, observed_at, source}`. The ledger is written at the moment of death and records the registry agentId.

| Fixture | Expected |
|---|---|
| Report missing, matching ledger entry (same name and registry agentId) | FAIL; `SCOPE-REPORT-MISSING` is retained and attributed to the ledger cause, never suppressed |
| Report missing, no ledger entry | FAIL with an additional unattributed-death finding |
| Ledger agentId differs from the registry agentId, or a second spawn exists for the same name | FAIL as a replacement or identity mismatch |
| Report present and a ledger entry exists | FAIL as a contradiction |
| Ledger cause cites only a pre-spawn `refused-before-spawn` or dispatch-refusal record | FAIL as a misattributed cause |
| Any missing-report seat | Output never emits `executed=none` or any absence-of-execution claim for that seat |

Lane bounds: leaf member — no subagent dispatch.

Tool installs or updates: none; source review needed none, and NO-EXEC forbids them.

Scope: executed=none
