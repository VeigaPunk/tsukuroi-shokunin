# FxCritNoHarm — adversarial no-harm review (read-only)

Axes attacked: calibration (scope gate), freshness/depth (stale author registry cells), disclosure-vs-repair. Strongest counterexample is the first; it is byte-observable in this wave, not hypothetical.

## Counterexample A — seat-scope calibration is mis-calibrated in both directions [obs]

`tools/check-seat-scope.py:77-80`: `executed != "none"` → `SCOPE-EXEC-UNAUTHORIZED`. The gate cannot distinguish truthful trailer values from command lists, and cannot see undeclared execution at all.

1. A declared value that literally begins `none` is flagged: `.ufo/waves/round-18/build/CritDepth.md:29` and `CritOperability.md:23` end `Scope: executed=none (read-only …)`. These seats are *counted as unauthorized executors* — conflating an honest none-qualified trailer with `ConnL0.md:17`'s `executed=python3 -c …` (genuinely unauthorized; no EXEC-AUTHORIZED in `.ufo/waves/round-18/build/spec.json` items — authorized set is the 17 Mig/Rerun/Mutate/Build/Final names).
2. The symmetric hole: any seat that executes unauthorized commands but ends `Scope: executed=none` produces zero findings — the count measures trailer honesty, not execution. `ReviewMtime.md:24`, `NoticeBootCorrections.md:24`, `NoticeForeign.md:31`, `SrcZswap.md:22` show the disclosure pattern proliferating; every declared non-`none` value is punished, incentivizing omission. `round-18.md:84` admits qualitatively ("parser cannot establish absence") but the calibration defect — honest `none`-prefixed declarations inflating the violation count — is not recorded. Impacted axes: calibration, operability.
Smallest safe correction: normalize the scope value (split on first whitespace/parenthesis) before the `!= "none"` test, and stop reporting the count as "executions" in any no-harm ledger — it is a count of *declared non-none trailers*.

## Counterexample B — stale author registry cells still read as authoritative [obs]

`SKILL.md:1895-1902` retains the round-17 gate table verbatim: `:1897` "53 cases", `:1898` "44 assertions"/probe, `:1900` omits `--exec-log` and resolves only `## R17-RECHECK`, `:1902` "all five"/"23 cases". `ReviewRegistry.md:7-10` measured three of those cells as FAILS against receipts (`selftests.txt` 61/45/40/28). The repair is a *second* table at `:1956-1970` — disclosure, not repair: no `recheck:`-style operative-line convention applies to tables, the stale cells carry no per-row superseded marker, and the nearest notice (`:1919`, :1902→:1919 gap ~15 lines) names only :118/:120/:129-133/:135/:1833. Any consumer reading the first table — or the unmarked `:1902` row — re-derives wrong counts and the wrong resolution heading. Compare `aur-risk-plane.md:347` (stale pointer cell) whose repair (`:431`) relies on the `section()` last-heading convention (`check-recheck-commands.py:58-60,449`); that convention is bespoke, not general.
Impacted axes: calibration, freshness. Smallest correction: strike or annotate the four stale cells in place, or move the R18 table to the table's own position.

## Weaker candidates (listed, not counted)

- Wave registries are spawn-time snapshots: `swarm-registry.json`/`record-result.json` `item: null` for all members and `spawn-result.json` `"status":"pending"` ×81 (`q=` count) while `outcome.json` says delivered 80/1 dead. A cell is stale the moment the seat settles. UNPROVEN that the pending final ledger re-derives rather than re-uses them — flagged for the verifier, not a claim of harm.
- C3 is structural-only by design (`check-appended-notices.py`); e.g. `R18-FRESH-SUPPLEMENT-03`'s `now` "active/enabled atR18" passes the gate. Bounded, consistent with `SKILL.md:1967`.

## Unknowns

- Whether the final execution ledger will read `item`/`status` cells or re-census reports (pending by design).
- Whether `executed=none`-vs-body contradictions exist in this wave: verification requires execution; I did not execute.

FAILS the calibration axis on Counterexample A; FAILS freshness/calibration on B unless the ledger treats cell-location staleness as covered.

Scope: executed=none
