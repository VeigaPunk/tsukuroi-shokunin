# Crit23Dead — dead-seat replacement, missing-final inference, cohort denominator shrink

Seat: Crit23Dead (critic, leaf). NO-EXEC, NO-FETCH. I read only the five bound files: `preregister.json`, `sources/godspeed-directive.txt` (used in place of `skill://godspeed`), `sources/r22-closure.json`, `sources/structured-edit-observations.json`, and this report path, which did not exist before this write. The preregister digest is the one supplied by the assignment. I did not compute it.

## Verdict

The preregister has no cohort ledger for round 23 and no rule for dead seats or replacement seats. Both C2 and C3 count at a level coarse enough that a smaller denominator, or an inferred final state, can still reach the target unnoticed. All three counterexamples below can be fixed without changing a claim's target. Only one condition requires the canonical judge to reject: a C2 or C3 pass computed from a population that leaves out declared seats or their events.

## Axes

- Operability (C2, `structured_edit_mode` 0→1): exposed to denominator shrink and to finality inferred from recorded starts.
- Calibration (C3, `unexplained_cohorts` 2→0): exposed to a coarse metric unit and to deltas explained away as dead seats.
- Discernment trend: false provenance would be at risk if report-file presence stands in for a seat's terminal status.
- Depth (C1): not affected by this seat's subject, except for the secondary edit-target note in counterexample 3.

## Counterexample 1 — denominator shrink passes C2 untouched

Evidence:
- `preregister.json` lines 37–44: the C2 metric is a binary mode (`before 0`, `target 1`), and the command's inputs are `.ufo/waves/round-23/<WAVE>/bindings.json` and `events.json` with `<WAVE>` left free.
- The preregister declares no round-23 seat count, registry digest, list of waves, or dead-seat or replacement policy. Its `limits` and `separability` fields are silent on this too.
- `r22-closure.json` `verification.rechecks`: round 22 had `seats_bound 64/64` in build even though `notes` records "128 seats, 7 build deaths (6 Codex capacity, 1 Haiku 429), no replacements". In round 22 the dead seats stayed bound, and the denominator was protected only by the closure verifier's independent recount ("128 declared, 121 report files, 7 absent").

Falsifier: in round 23, build `bindings.json` from the seats that produced a report (or from replacement seats only), or run the command on only one `<WAVE>`. The checker still reports `structured_edit_mode 1`, because a mode flag does not depend on how many seats are bound. Seats left out contribute no events, so they cannot contribute violations. That turns death into silent conformance.

Smallest safe correction, in scope for C2 as a new audit authority without changing its target:
- Have the C2 checker print and enforce a cohort ledger. The ledger declares the wave set explicitly (build and falsify), and the declared seat count N per wave comes from the dispatch registry, not from report files.
- It enforces `bound == N`.
- Each row carries `seat`, `agent`, `transcript_sha256`, and `terminal` ∈ {final, died, missing_final}.
- It enforces `N == final + died + missing_final`.
- Any `<WAVE>` that is absent, or whose bindings leave out a declared seat, exits non-zero.

## Counterexample 2 — replacement seats change identity under a seat-keyed report path

Evidence:
- Report paths are keyed by seat name, for example `.ufo/waves/round-23/build/<Seat>.md`.
- `structured-edit-observations.json` already carries both `seat` and `agent` (for example `TsukuroiR22.OraclePathArtifact-3`) and `transcript_sha256`. The preregister's C2 and C3 scopes require neither the agent identity nor the transcript identity.
- Round 22 had "no replacements". Round 23 makes no commitment either way.
- [INFERENCE] Live agent ids carry dispatch-generation suffixes, so a respawn under the same seat name gets a different agent id.

Falsifier: seat X dies after emitting an out-of-binding request, and a replacement X′ writes `X.md` cleanly. A seat-keyed report census then counts one conformant seat. A seat-keyed event join either merges X's violation into X′, which changes identity, or drops X's transcript because its seat "has a final", which hides a violation.

Smallest safe correction:
- Make the replacement an added ledger row with `replaces: <agent of X>`. The dead original keeps `terminal: died`, and its events are still audited against its own binding.
- Key every join on `agent` plus `transcript_sha256`, never on seat name alone.
- A replacement never lowers N and never inherits or absorbs another seat's events.
- If round 23 does not replace seats, state "no replacements" in the closure ledger, as round 22 did.

## Counterexample 3 — missing-final inferred from recorded starts and from report presence

Evidence:
- `structured-edit-observations.json` records only `recorded_starts` (line, tool, path). There is no completion or result record, and no `call_id` on the starts.
- The link from a start to its request is therefore inferred from line position, and that inference fails on its own data:
  - CritRuntime: request at line 15, starts at lines 12 and 13, which is before the request.
  - OraclePathArtifact: each start is at request line + 1.

  A "next lines after the request" join therefore orphans CritRuntime's read and write, or attaches them to an earlier request.
- The round-22 closure equates "121 report files, 7 absent" with "7 native failures" by matching counts, not by a per-seat join. It also says "no completion line observed" for the dispatch digest.

Falsifier:
- A seat writes its report and then dies before its final message. Report presence counts it as final.
- A seat reaches its final message but its report write is refused. The count-based rule calls it a native failure.

Both errors cancel in the total, so 128 − 121 = 7 still "matches". Separately, C2 may count an edit as performed because start events exist, even though no result was observed.

Secondary C1 overlap, for other critics: CritRuntime's adapter read path ends in `.md:raw`. That is an alternate spelling of the target, and the `EDIT_TRAVERSAL` row ("No dot-segment or alternate spelling expands the target list") does not say whether a selector suffix is normalized or treated as a distinct target.

Smallest safe correction:
- Derive `terminal` per seat from that seat's transcript (final message present, error or capacity termination, or neither, which is `missing_final`). Report presence is a separate column and is never a substitute.
- In C2 output, mark recorded starts as `start_only, result=unobserved` unless a result record is joined by `call_id`. When no call_id exists, mark the association `UNKNOWN`, matching the `OPAQUE_PATCH` stance, rather than inferring it from line order.
- Treat the dispatch-level "no completion line" as `missing_final`, not as completed.

## Counterexample 4 — C3 counts whole cohorts, so it can absorb per-event deltas

Evidence:
- `preregister.json` lines 46–51: the metric is `unexplained_cohorts`, going from 2 to 0. The scope promises "exhaustive per-event/component explanation".
- The deltas are build 25 − 23 = 2 and falsify 33 − 29 = 4 (lines 14–21). The preregister does not give the unit (events, distinct paths, or seats).
- Round 22 itself labels 25/33 an "approximate own path-binding census … selector-normalization differences, not decisive". The preregister promotes that number to `path_counts_as_reported`.
- The build cohort had 7 deaths. The falsify cohort had 0 (`build54/3/7/0 falsify59/5/0/0`).

Falsifier:
- A reconciliation attributes the build delta of 2 to "dead-seat transcripts excluded by the lane checker" and the falsify delta of 4 to "selector normalization", then marks both cohorts explained. The metric reaches 0 although no event has been matched.
- The dead-seat story also cannot be the universal explanation, because falsify has a delta of 4 with zero deaths. If the build delta does come from leaving dead seats out, that is a quiet shrink from 64 to 57 seats inside the "explanation".
- Switching units (events to distinct paths) can also close the gap arithmetically.

Smallest safe correction:
- C3 output lists every rough-census event per cohort. Each event is either matched one-to-one to a lane event, or assigned exactly one named cause, such as dead-seat transcript, `:raw` or other selector suffix, an additional recorded start (the 35 starts, 19 build and 16 falsify, that reconcile 359+979 with 378+995), internal URI, or typo path.
- Each event row carries `agent` and `transcript_sha256` from the frozen 128-transcript set.
- The unit is declared once and is the same on both sides.
- Exit non-zero if any event is unmatched, if `rough == lane + Σ named deltas` fails, or if any declared seat is absent from the rows. This keeps the cohort-level target but makes it impossible to reach without per-event closure.

## What the canonical judge should reject, as opposed to what can be fixed

- Fixable defects: counterexamples 3 and 4, and the ledger in counterexample 1. Each adds output and invariants and changes no target.
- Reject outright: a claimed C2 or C3 pass whose population leaves out any declared seat, or any dead seat's events, or whose replacement rows reuse an original's identity. That is false provenance, not a tradeoff.

Lane bounds: leaf member — no subagent dispatch. No installs, commands, or fetches.

Reviewed-SHA256: 8f3f33eaa6e9cd1c3af369955420a13e6d5b339cc5970bec04560de2c08767e8
Predicate: r23-crit23dead
Scope: executed=none
