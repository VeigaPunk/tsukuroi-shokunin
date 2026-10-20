# AttackOrdinal — R16 depth uplift from a two-record count

Static reads at baseline `db68e62`. No R16 artifact exists yet (only `.ufo/waves/round-16/build/` is untracked), so this checks the plan, not shipped output.

**Counterexample (concrete):** this exact measure already has two admitted results at depth 8→8. R14 `resolved correction_count0→2` scored `8→8 (0)` (`SCORECARD.md:387`). R15 `0→2` also scored `8→8`, and its independent closure confirmed "Ordinal8→8" (`round-15-verifier-spotcheck.md:120`). `SCORECARD.md:248` says "No count-to-ordinal-score scale exists". `AXES.md:52-55` adds that a score no reader can re-derive is an opinion. Scoring R16's 0→2 as 9 would retroactively make R14 and R15 underscored.

**Inflation path:** R15 commit `6de977d` introduced both wrong locators: `host-health-report-r3.md:581` cites §1, but the board is §0 (`:23`, row `:31`); `update-safety-v3.md:398` cites §7, but the row is in §5 (`:208`, `:216`). Raising the score for these fixes would reward a round for repairing errors it made itself.

**Impacted axes:** depth (score not supported), calibration (would be harmed), and the lowest-axis duty (an artificial 9 would end the depth 8/adjacency 8 tie).

**Smallest correction:** record `8→8 (0)` with the verdict "improved; ordinal unchanged". Falsifier: in the R16 SCORECARD, report or lesson, any match for `depth.*(8 ?(→|->) ?9|\+1)` means the claim must be rejected.
