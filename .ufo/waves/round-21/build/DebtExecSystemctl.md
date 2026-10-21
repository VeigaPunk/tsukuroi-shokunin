# DebtExecSystemctl — round20 build missing seat ExecSystemctl

Reviewed-SHA256: cc5abf6790328d685270fc3c82b5fb412d3ba00a39f078a9c126147d730fbf82
Predicate: round20-missing-report-ExecSystemctl

Reviewed snapshot: `.ufo/waves/round-21/snapshot/corpus/lessons/round-20.md` (digest as assigned in `.ufo/waves/round-21/reviews.json:320-324`; not recomputed — NO-EXEC). Seat scope only: ExecSystemctl. Author-dispatched debt audit, not non-author closure.

## Axes

- A1 identity/assignment: what the registry, spec and plan bind to the seat.
- A2 report absence: what proves the report is missing.
- A3 death/provenance: which provider-death record is actually available.
- A4 disposition: append-only round21 sentence and prevention test, without repair or replacement.

## Observations

| # | Evidence | Fact |
|---|---|---|
| O1 | `.ufo/waves/round-20/build/swarm-registry.json:26-31` | `"ExecSystemctl": {"kind": "spawn", "agentId": "TsukuroiR19Recovery.ExecSystemctl-2", "role": "executor", "item": null}`; registry `updatedAt` `2026-10-21T09:23:13.585Z`, `reportDir` `.ufo/waves/round-20/build` |
| O2 | `.ufo/waves/round-20/build/dispatch.json:44-49`, `plan.json:58-63` | Same member, role executor, `agentId: null` (pre-spawn) |
| O3 | `.ufo/waves/round-20/build/spec.json:22-25`; `plan.json:444-446`; `dispatch.json:439-441` | Assignment: EXEC-AUTHORIZED read-only `git -C <worktree> show|diff|rev-parse` only; edit ONLY `tools/check-recheck-commands.py` in `/tmp/tsukuroi-r20-execscope-20261021` (base `0cbc34dd…`); systemctl argv classifier for `assess_exec_log` (read verbs cat/show/status/list-units/list-unit-files/list-timers/is-active/is-enabled/is-system-running; reject mutating/unknown verbs and `--now`/`--force`), exact exit/id selftests, NEVER run tests. Plan/dispatch add `Lane bounds: leaf member — no subagent dispatch except your single labrat.` and `Report: … .ufo/waves/round-20/build/ExecSystemctl.md` |
| O4 | `.ufo/waves/round-20/seeded-implementation.json:8` | L1 (author TsukuroiR20) seeded the classifier in that worktree; "review, exact fixtures and limitations assigned to ExecSystemctl"; verification "Not run" |
| O5 | Glob `**/*Systemctl*` under `.ufo/waves` → 0 files | No `ExecSystemctl.md` anywhere in waves |
| O6 | `.ufo/waves/round-20/measure/final-r20c/seat-scope-build.stdout` (also `final-r20`, `final-r20b`) | `{"detail": "seat report absent", "id": "SCOPE-REPORT-MISSING", "role": "executor", "site": "ExecSystemctl.md"}`; counts `SCOPE-REPORT-MISSING: 13`, `seat_count: 64`, `status: FAIL`, revision `fc2a0085…`; evidence_class "self-reported declarations; no independent absence-of-execution proof" |
| O7 | `.ufo/waves/round-20/build/native-task-result.json`; `native-task-result-retry-2.json` | Two start refusals naming `TsukuroiR20.ExecSystemctl` (attempt 1) and the whole wave (attempt 2: `"spawned": 0`, `"status": "refused-before-spawn"`, `"error": "Background job limit reached (100)"`). These are pre-spawn refusals under a different ID prefix, not a death of `TsukuroiR19Recovery.ExecSystemctl-2` |
| O8 | Grep `rate[- _]?limit|provider[- _]?death|deaths?` over `.ufo/waves/round-20` → no matches; `TsukuroiR19Recovery\.ExecSystemctl` / `ExecSystemctl-2` over `~/.omp`, `~/.local/share` → no matches; `~/.omp/agent` lists only `config.yml` | No provider-death record for the bound identity is readable in lane or agent-store paths searched |
| O9 | Snapshot `round-20.md:41`, `:63` | The only "provider-rate-limit deaths" attribution is lesson prose covering 13 build reports collectively, with "Do not … replace dead seats or infer actual execution absence; preserve this process red" |
| O10 | `.ufo/waves/round-20/build/ExecMutating.md:1,9,15-23,29` | A separate seat reviewed the seeded systemctl classifier (allowlist omits `list-dependencies` versus `host-capture-r19.txt:215`), ending `Scope: executed=none` |

## Inferences

- [INFERENCE] The bound agent `TsukuroiR19Recovery.ExecSystemctl-2` was spawned by a later attempt than O7 (registry binding at/before 09:23:13Z) and produced no report. Whether it ran any authorized `git` command or edited the worktree is unknown; the classifier that landed (lesson R20-SYSTEMCTL, 95/95 recheck selftest at `fc2a0085…`) cannot be attributed to this seat from available evidence. O4 shows L1 seeded it.
- [INFERENCE] The cause "provider rate limit" rests only on the L1 lesson assertion (O9). No per-seat death record is available (O8), and the job-limit refusals (O7) are a different failure class and identity. Cause remains UNKNOWN at seat granularity, not disproven.
- O10 is adjacent coverage by a different seat with a different predicate. It does not substitute for the missing ExecSystemctl review/fixtures/limitations report.

## Limits

- Negative searches used ripgrep-backed Grep/Glob. A parent-path search for the registry ID returned no matches even though O1 contains it, so ignored/hidden paths are skipped and agent-store absence (O8) is bounded, not exhaustive. `history://` transcripts are not readable from this seat.
- The reviewed SHA-256 is the assigned value. Byte equality between the snapshot and `corpus/lessons/round-20.md` was not recomputed. The snapshot lines read match the baseline lines seen by Grep at :41/:51/:53/:63.
- A missing report is not proof that commands were absent. A missing report is not proof of execution either.

## Round21 debt disposition (append-only sentence)

Round20 build seat ExecSystemctl (role executor, registry agentId `TsukuroiR19Recovery.ExecSystemctl-2`, assignment: systemctl exec-log classifier review/fixtures in `/tmp/tsukuroi-r20-execscope-20261021` `tools/check-recheck-commands.py`, report `.ufo/waves/round-20/build/ExecSystemctl.md`) remains SCOPE-REPORT-MISSING as a retained historical red; no per-seat provider-death record exists in lane artifacts (only the wave-level "Background job limit reached (100)" pre-spawn refusals under `TsukuroiR20.*` and the lesson's collective rate-limit attribution), so its cause stays UNKNOWN, its execution or edits stay UNKNOWN, no report is reconstructed, no identity is replaced, and the landed systemctl classifier is attributed to L1 seeding plus integrated measurement only.

## Prevention test

`seat-scope` (or a sibling gate) MUST emit, for every registry member whose report is absent, a finding carrying the bound `agentId` and one death-evidence class: `RECORDED` (a path to a per-agentId provider/terminal record) or `UNRECORDED`. Lessons/LOG text claiming a death cause MUST be rejected unless every counted seat is `RECORDED`.

Fixtures:
1. A registry member with a non-null agentId, no report and no record yields `SCOPE-REPORT-MISSING` with `death_evidence=UNRECORDED`, and a lesson saying "rate-limit death" for it fails.
2. The same member with a per-agentId record file yields `RECORDED` and the claim is admitted.
3. A pre-spawn refusal record under a different agentId prefix (the O7 shape) MUST NOT satisfy `RECORDED` for the bound ID.
4. A present report clears the missing-report finding without altering trailers.

Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
