# Falsify wave dispatch attempts (tsukuroi r19, recovery attempt 2)

Spec: `.ufo/waves/round-19/falsify/spec.json` (final 72 seats; earlier 100- and 88-seat
re-specs were superseded before any dispatch on the operator/orchestrator caps).
Validator: `ufo-swarm-wave.mjs plan` and `run` both exit 0 at 72 spawn, band 64-100 OK.

## Attempt 1 — 2026-10-21, immediately after wave-slot grant
Slot: `wave-slot.sh acquire tsukuroi r19-falsify 72 3600` -> `granted ... live=145 pending=0 cap=240`.
Task call: ONE call carrying the validator taskCall (72 tasks), context unchanged.
Result: **no seat started**. Every task returned
`Failed to start background task jobs: TsukuroiR19Recovery.<Name>: Background job limit
reached (100). Wait for running jobs to finish or cancel one.`
The process-wide omp background-job cap (100) was already saturated by other lanes'
waves; `proc://` listed no `TsukuroiR19Recovery.*` job afterwards, so this was an
all-or-nothing refusal, not a partial start.
