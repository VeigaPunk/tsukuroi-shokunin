# FxRegistry — scoped no-harm review

Review target: `68a8ae035fde33360cbbe21dc92ca0eacf0a5b33`.

## Findings (lowest severity first)

- **Low — C1 baseline invocation is under-documented.** `SKILL.md:1964` says the boot-chain entry command uses `--revision <REV>` and C1 adds `--statement-corrections`, but omits the comparison-specific `--registry-from <TARGET>`. The CLI describes that option at `tools/check-boot-chain.py:820-822`; absent it, registry revision defaults to the evaluated revision (`:1514-1515`), and a baseline lacking the registry returns `CORR-REGISTRY-MISSING` (`:1526-1528`, `:654-658`) rather than the four named unresolved corrections. Document `--revision <BASE|TARGET> --statement-corrections --registry-from <TARGET>` for the baseline/target comparison. Target-only invocation remains valid.

## Verdicts

- **SKILL supersession: SURVIVES.** `SKILL.md:1954` explicitly marks 53/44/five-tools/probe/23 as historical, supersedes those rows, and points current counts/exits to `measure/final/results.json`; `:1956-1974` supplies the current registry and revision error classes. That ledger was absent when read, so current R18 tallies/exits remain **UNKNOWN/pending**, not a pass; no scripts were run.
- **Capability count: SURVIVES.** `SCORECARD.md:554` explicitly supersedes the historical `:164` 44/44 with the landed round-17 measurement; `measure/final/selftests.txt:11` records `TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=45 failed=0` (also `SCORECARD.md:520`). No new capability credit is claimed.

## Residual risk / verification gaps

No LSP device was mounted (`read xd://lsp` reported “No such tool”); reads ground the findings, and grep was only used to locate source lines. Final R18 execution ledger remains pending.

Scope: executed=none