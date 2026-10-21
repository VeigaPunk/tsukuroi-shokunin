# DebtExecRegistry — round20 missing build report, seat ExecRegistry

Reviewed-SHA256: cc5abf6790328d685270fc3c82b5fb412d3ba00a39f078a9c126147d730fbf82
Predicate: round20-missing-report-ExecRegistry

Reviewed bytes: `.ufo/waves/round-21/snapshot/corpus/lessons/round-20.md` (pinned snapshot of baseline `corpus/lessons/round-20.md`). The digest above is the one the item supplied and that `reviews.json:306-310` records. This seat ran nothing, so it did not recompute the hash.

## Axes

- A1 identity: which role, assignment and agent identity this seat had.
- A2 absence: whether the report is missing, and which gate records that.
- A3 death record: what provider-death evidence exists for this exact seat.
- A4 disposition: an append-only round21 sentence plus a prevention test that cannot clear the red.

## Observations

1. **Role and identity.** In `.ufo/waves/round-20/build/swarm-registry.json:14-19`, member `ExecRegistry` has `kind: spawn`, `agentId: TsukuroiR19Recovery.ExecRegistry-2`, `role: executor`, `item: null`. In `dispatch.json:32-37` and `plan.json:46-50` the same member has `agentId: null`, because those files were written before spawn.
2. **Assignment.** `spec.json:13-15`: EXEC-AUTHORIZED, limited to read-only `git -C <assigned-worktree> show|diff|rev-parse`. The worktree is `/tmp/tsukuroi-r20-registry-20261021` at base `0cbc34dd6b20896085a8fb07943e3ea4027d8472`, and the only file in scope is `tools/check-registry-coverage.py`. The task was to add `--audit-live-map` (C3, `audit_live_map_errors`, `REGISTRY-AUDIT-LIVE-MAP`) plus selftests, and to run none of them. `plan.json:434-436` adds the trailers `Lane bounds: leaf member — no subagent dispatch except your single labrat.` and `Report: write your scoped findings to .ufo/waves/round-20/build/ExecRegistry.md`.
3. **Seeded overlap.** `.ufo/waves/round-20/seeded-implementation.json:7` shows that L1 (author TsukuroiR20) seeded the "finite labelled audit-live-map mode" in the same worktree file. Only the "additional contract/selftest work" was left to ExecRegistry.
4. **Report absent.** No file matching `ExecRegistry*` exists anywhere under `.ufo/waves/round-20` (glob returned 0). All three seat-scope captures list `{"id": "SCOPE-REPORT-MISSING", "role": "executor", "site": "ExecRegistry.md", "detail": "seat report absent"}`: `measure/final-r20/`, `final-r20b/` and `final-r20c/seat-scope-build.stdout`. Final `final-r20c` reports `SCOPE-REPORT-MISSING: 13`, `status: FAIL` and `evidence_class: "self-reported declarations; no independent absence-of-execution proof"`. In `results.json:503-517`, `seat-scope-build` has exit 1, expected 0, `matched_exit: false`.
5. **Provider-death evidence.** The only seat-specific death record is L1's narrative at `LOG.md:1039`: "Thirteen provider-rate-limit deaths (ExecBinder, ExecRegistry, …); no replacement." `LOG.md:1047` and `1063`, `SCORECARD.md:628`, and the snapshot lesson at lines 41 and 63 repeat this only as a count of 13. Round20 kept no per-seat death artifact (no `death-ExecRegistry.json`, no provider error string, exit status or timestamp). Round21 now keeps such artifacts, for example `round-21/build/death-ScribeDecision.json`.
6. **Records that are not this seat's death.** `build/native-task-result.json` is spawn attempt 1. It names `TsukuroiR20.ExecRegistry: Background job limit reached (100)`, which is a pre-spawn refusal, not a death. `native-task-result-retry-2.json` is attempt 2, also `refused-before-spawn` and `spawned: 0`. The third call, which `LOG.md:1039` says spawned all 64 seats, has no retained native result file.

## Inferences

- [INFERENCE] The agent identity that died is the registry's `TsukuroiR19Recovery.ExecRegistry-2`, not the attempt-1 task name `TsukuroiR20.ExecRegistry`. That name belongs to a refused call that never spawned. The registry was last updated at 09:23:13Z, but no timestamp shows when the death happened.
- [INFERENCE] C3's measured improvement (`audit_live_map_errors` went from 1 to 0, registry-coverage passed 23/23) is L1 seeding and integration evidence. It must not be attributed to ExecRegistry.

## Limits and unresolved gaps

- The provider, error text, retry budget and time of this seat's death are unknown. The LOG classification is L1's self-report, with no raw record behind it.
- The report's absence does not show that ExecRegistry executed no commands or made no edits. The seat was EXEC-AUTHORIZED for read-only git and was allowed to edit `/tmp/tsukuroi-r20-registry-20261021/tools/check-registry-coverage.py`. Whether it ran commands or changed that worktree before dying is unknown, and this seat did not inspect the worktree.
- This seat recovered no transcript (`history://`); the only evidence used is what is on disk in the lane.

## Append-only round21 debt-disposition sentence

Round21 disposition, R20-SEAT-DEBT/ExecRegistry: round20 build executor seat `ExecRegistry` (registry agentId `TsukuroiR19Recovery.ExecRegistry-2`, EXEC-AUTHORIZED for read-only `git show|diff|rev-parse` and edits only to `/tmp/tsukuroi-r20-registry-20261021/tools/check-registry-coverage.py`) never wrote `.ufo/waves/round-20/build/ExecRegistry.md`. The only death evidence is L1's `LOG.md:1039` provider-rate-limit narrative, with no retained per-seat error record. Its `SCOPE-REPORT-MISSING` red therefore stays red. The seat is not replaced and no report is manufactured. The absence is not taken as evidence that the seat did or did not execute authorized commands or edit its worktree, and the audit-live-map outcome stays credited to L1 seeding and integration.

## Prevention test (proposed; not implemented or run)

Add hermetic `tools/check-seat-scope.py --selftest` fixtures that classify a missing report without ever clearing it:

- **P1.** Registry member `ExecRegistry` (executor, agentId `X.ExecRegistry-2`), no `ExecRegistry.md`, no `death-ExecRegistry.json`. Expected: exit 1 with `{SCOPE-REPORT-MISSING, SCOPE-DEATH-UNRECORDED}`.
- **P2.** Same, but `death-ExecRegistry.json` has `agent` equal to the registry agentId, a non-empty `observed_error`, and `replacement: false`. Expected: exit 1 with `{SCOPE-REPORT-MISSING}` only. A death record classifies the gap but never turns it PASS.
- **P3.** The death record's `agent` is `TsukuroiR20.ExecRegistry`, which does not match the registry, or its `observed_error` is empty. Expected: exit 1 with `SCOPE-DEATH-INVALID`.
- **P4.** The death record has `replacement: true`, or a report exists that was written under a different agentId. Expected: exit 1 with `SCOPE-DEATH-INVALID`. Replacing a dead seat is rejected.
- **P5.** A death record and a present report with `Scope: executed=none` both exist. Expected: exit 1 with a contradiction finding. A death plus a report is never silently accepted.
- **P6.** A pre-spawn refusal record (`refused-before-spawn`, `spawned: 0`) is used as the death record. Expected: `SCOPE-DEATH-INVALID`. A refusal is not a death.

Each fixture checks the exact exit code and ID set. Wave dispatch should also write `death-<Name>.json` at the moment a seat fails, as round21 now does.

Lane bounds: leaf member — no subagent dispatch.
Scope: executed=none
