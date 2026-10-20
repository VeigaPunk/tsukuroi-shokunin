# R17 Seat-Scope Falsifier

Axes: count agreement; wave identity; revision provenance.

**SURVIVES — the recorded discrepancy is real; the canonical final tally is UNPROVEN.**

- [obs] The lesson says 29 of 72 wave-1 build seats were unauthorized, based on `--worktree`; it repeats “29 r17 breaches” (`corpus/lessons/round-17.md:45,51`).
- [obs] The named measurement `measure/seat-r17.json:1` identifies revision `dd15c183f2f2481db67d0234038117a0d5b7034c`, wave `.ufo/waves/round-17/build`, 74 seats, and 30 `SCOPE-EXEC-UNAUTHORIZED` findings (plus 2 missing-report findings).
- [obs] Final build measurement `measure/final/seat-r17-build.json:1` also says 30, but identifies `revision=worktree`, 74 seats, and no branch tip. It does not establish the count at the final landed revision.
- [obs] `measure/final/seat-r17-falsify.json:1` is a different wave: 81 falsify seats, 16 unauthorized, 52 missing reports, also `revision=worktree`. The 16 neither reconciles nor contradicts the wave-1 count.
- [obs] The verifier spot-check records the same 30-vs-29 discrepancy and says the two final files are worktree measurements, not named revisions (`corpus/lessons/round-17-verifier-spotcheck.md:221-224`).
- [inf] The 74-seat measurement denominator also differs from the lesson’s 72, so these records show a real reporting inconsistency but do not determine which tally accurately describes the intended 72-seat wave at final landing. No execution or remeasurement performed.

Scope: executed=none