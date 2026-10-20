# Capability window — round 17

**Axes.** C1 depth, C2 freshness, C3 operability; a capability row is a claim type inside one claim, not a fourth axis (AXES.md:25-30).

**Window.** Last row `root-metadata-observer` = round 12 (SCORECARD.md:163); rounds 13–16 added none (SCORECARD.md:311-312, :367, :419, :480) — 4 > N=3 (SCORECARD.md:176-177). [obs] The nudge does not apply: its conjunct is every axis ≥9 (AXES.md:68-70), but depth 8/adjacency 8 (SCORECARD.md:178-179). Lowest-axis duty binds; C1 works depth.

**Qualification.** Yes, distinct from `host-census-gate` (per-entry UKI audit, `TSUKUROI_BOOTCHAIN`). AXES.md:60-64 requires name, one-line capability, evidence pointer, first-working round, and a passing demonstration in the round report; else pre-claiming (SCORECARD.md:165-166). `--selftest` proves only fixtures, so it cannot support a live-audit row.

**Move.** Let one L1 `bash tools/boot-chain-audit.sh --live` run supply the row's demonstration and evidence pointer, recorded as C1's claim type; it also proves `boot-chain-r17.md:3`'s `recheck:` executable and re-derives five entry verdicts. Require `TSUKUROI_BOOTCHAIN:` plus five TSV rows, path cited.

**Risks.** Premature row resets the N=3 clock (SCORECARD.md:176); `sudo -n` denial must yield `UNKNOWN`/exit 2, not `DEGRADED`.

**Unverified.** [unk] Tool absent (`ls tools/`, 12:57), no live output. [inf] Live path is `sudo -n` reads only; the pacman pause permits it.

Scope: executed=ls, find, cat, grep, awk, sed, tail, wc, git status, git log, python3
