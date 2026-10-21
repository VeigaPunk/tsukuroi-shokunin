# DebtOwnAnchor08 — round20 build missing seat OwnAnchor08

Reviewed-SHA256: cc5abf6790328d685270fc3c82b5fb412d3ba00a39f078a9c126147d730fbf82
Predicate: round20-missing-report-OwnAnchor08

Target: `.ufo/waves/round-21/snapshot/corpus/lessons/round-20.md` (baseline source `corpus/lessons/round-20.md`; digest as supplied in the item, not recomputed — NO-EXEC).

Axes: (A) seat identity/assignment exactness; (B) report-absence exactness; (C) death-cause provenance; (D) disposition honesty (no invented report, no replacement, no execution-absence claim).

## Observations (exact, read-only)

| # | Source | Observation |
|---|---|---|
| O1 | `.ufo/waves/round-20/build/swarm-registry.json` lines 92–97 | Member `OwnAnchor08`: `"kind": "spawn"`, `"agentId": "TsukuroiR19Recovery.OwnAnchor08-2"`, `"role": "scout"`, `"item": null`. Registry `wave` `tsukuroi-r20-build`, `createdAt` 2026-10-21T08:18:06.158Z, `updatedAt` 2026-10-21T09:23:13.585Z; no status/death/exit field exists for any member |
| O2 | `.ufo/waves/round-20/build/spec.json` lines 78–80 | `name` OwnAnchor08, `role` scout; prompt is NO-EXEC (“read/grep/glob only plus writing your report. End with literal Scope: executed=none”) and assigns “C1 source/ownership review of OUT-008 ONLY in PROVINCE portable anchors and adjacency-anchors-r19.json/sibling snapshot … recommend whether R20-OUT009 clarification affects this row” |
| O3 | `.ufo/waves/round-20/build/dispatch.json` lines 110–114, 494–496 | Dispatch member `OwnAnchor08` has `"agentId": null`, role scout; dispatched prompt ends “Report: write your scoped findings to .ufo/waves/round-20/build/OwnAnchor08.md” |
| O4 | glob `*OwnAnchor*` under `.ufo/waves/round-20` | `OwnAnchor01`–`07` and `09` reports exist; `OwnAnchor08.md` (and `OwnAnchor10.md`) absent |
| O5 | `.ufo/waves/round-20/measure/final-r20c/seat-scope-build.stdout` (revision `fc2a0085088cedb3ab59dc3fff16523c0f42a6b4`) | `{"detail": "seat report absent", "id": "SCOPE-REPORT-MISSING", "role": "scout", "site": "OwnAnchor08.md"}`; counts `SCOPE-REPORT-MISSING: 13`, `seat_count: 64`, `status: FAIL`; `evidence_class`: “self-reported declarations; no independent absence-of-execution proof”. Same finding in `final-r20` and `final-r20b` |
| O6 | `.ufo/waves/round-20/build/native-task-result.json` | One aggregate launch failure: “TsukuroiR20.OwnAnchor08: Background job limit reached (100). Wait for running jobs to finish or cancel one.” (all 64 `TsukuroiR20.*` seats listed); `details.results: []`, `totalDurationMs: 0` |
| O7 | glob `death-*` under `.ufo/waves`; grep `OwnAnchor08` under `/home/vgpnk/.omp`; grep `TsukuroiR19Recovery.OwnAnchor08` in repo | Only death record anywhere is round21 `build/death-ScribeDecision.json`. No round20 per-seat death file; no harness-store match; `TsukuroiR19Recovery.OwnAnchor08` occurs only in the registry |
| O8 | grep `OUT-008` in `.ufo/waves/round-20/**/*.md` | No match — no other round20 report covers the OUT-008 anchor question |
| O9 | snapshot lesson lines 41, 63 | Aggregate attribution only: “13 build reports missing from provider-rate-limit deaths”; “Do not rewrite trailers, replace dead seats or infer actual execution absence; preserve this process red” |

## Inferences

- I1 (A): Identity is split across three namespaces: dispatch `agentId: null` (O3), failed native launch `TsukuroiR20.OwnAnchor08` (O6), registry-recorded spawn `TsukuroiR19Recovery.OwnAnchor08-2` (O1). The registry identity is the only one recorded as spawned; the job-limit failure belongs to a different identity and is a launch refusal, not a provider rate-limit death. [INFERENCE: the `-2` spawn was a re-dispatch after the job-limit failure.]
- I2 (B): Report absence is exact and mechanically retained (O4, O5). It is a report absence only — not evidence that the seat ran or did not run commands, and not a substantive OUT-008 verdict in either direction (O5 `evidence_class`, O8).
- I3 (C): The available provider-death record for this seat is **none**. The lesson's “provider-rate-limit deaths” cause for OwnAnchor08 rests on the aggregate statement in O9 alone; no retained round20 artifact binds `TsukuroiR19Recovery.OwnAnchor08-2` to a 429/rate-limit error. Cause for this seat stays UNKNOWN-retained, not disproven. [INFERENCE: the aggregate claim may come from unpersisted runtime observation.]

## Limits

No transcript (`history://`) access through this seat's read tools; no recomputation of the reviewed digest; the round20 registry carries no per-member status, so delivery/death cannot be read from it.

## Round21 debt-disposition sentence (append-only)

R21-DEBT-OwnAnchor08: round20 build seat `OwnAnchor08` (scout, registry agentId `TsukuroiR19Recovery.OwnAnchor08-2`, assignment C1 OUT-008 source/ownership review, report `.ufo/waves/round-20/build/OwnAnchor08.md`) remains SCOPE-REPORT-MISSING red at `fc2a0085088cedb3ab59dc3fff16523c0f42a6b4`; no seat-specific provider-death record was retained (the only per-seat launch evidence is a `TsukuroiR20.OwnAnchor08` background-job-limit refusal under a different identity), so its cause is UNKNOWN beyond the round20 lesson's aggregate rate-limit attribution, the OUT-008 anchor question stays unanswered, and the seat is neither replaced, backfilled, nor read as proof that no commands ran.

## Prevention test (proposed; not implemented — no production edits)

Add to `tools/check-seat-scope.py` `selftest()` a retained-death classification that keeps the wave red but requires a bound cause:

- `report-missing-unattributed`: registry member `Alpha` with `agentId` `W.Alpha-2`, no `Alpha.md`, no `death-Alpha.json` → FAIL with `SCOPE-REPORT-MISSING` plus `SCOPE-DEATH-UNRECORDED`.
- `report-missing-dead-bound`: same, plus `death-Alpha.json` `{"agent": "W.Alpha-2", "observed_error": "… 429 …", "replacement": false}` → FAIL with `SCOPE-REPORT-MISSING` only (still red; cause bound).
- `death-identity-mismatch`: `death-Alpha.json` `agent` `W0.Alpha` ≠ registry `agentId` `W.Alpha-2` (the OwnAnchor08 shape: `TsukuroiR20.*` launch refusal versus `TsukuroiR19Recovery.*-2` spawn) → FAIL with `SCOPE-DEATH-UNRECORDED`; a launch refusal for another identity must not attribute a death.
- `death-replacement-forbidden`: `replacement: true` or a present `Alpha.md` alongside the death record → FAIL (`SCOPE-DEATH-CONFLICT`).

Required complement at dispatch: the launcher writes `death-<Name>.json` (shape of round21 `death-ScribeDecision.json`) bound to the exact registry `agentId` whenever a seat terminates without a report.

Lane bounds: leaf member — no subagent dispatch.
Tools installed: none.

Scope: executed=none
