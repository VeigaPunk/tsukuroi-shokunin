# C3 historical-row mutation design

Axes: C1 adjacency (8), C2 operability (9), C3 calibration (9). This assignment covers C3 only; preregistered ordinal deltas are all 0, and none was measured here.

## Finding — a historical-row-only correction must remain red

The operative selector is by exact registry heading: `_operative_rows()` chooses the unique highest round number and errors on duplicate highest headings (`tools/check-registry-coverage.py:133–145`). `SKILL.md:1997–1999` says lower tables are historical/non-operative; round19 is the current higher table (`SKILL.md:2060–2062`). Its `boot-chain-audit` probe cell still advertises `0 CONSISTENT; 1 DEGRADED; 2 UNKNOWN` (`SKILL.md:2073`). The round18 cell at `SKILL.md:1965` instead has the corrected live `0/2` map and separates selftest failure `1` already. Thus repairing that older cell cannot change the selected round19 row.

**Red fixture delta:** use a structurally valid, otherwise generic-coverage-clean fixture with distinct round18 and round19 complete tables and one `boot-chain-audit` probe row in each. Starting from a lower row that advertises live `0 CONSISTENT; 1 DEGRADED; 2 UNKNOWN`, change only that round18 row to live `0 CONSISTENT/observation; 2 UNKNOWN/could-not-evaluate`, keeping its selftest `0 PASS; 1 FAIL` separate. Leave the unique highest round19 row advertising live `1 DEGRADED`. Expected C3 result remains exactly `REGISTRY-AUDIT-LIVE-MAP`, `audit_live_map_errors=1`, exit `1`—the preregistered `historical_row_only_fix` expectation (`.ufo/waves/round-20/preregister.json:49–53`). Keep unrelated findings out of the fixture so they cannot mask this result.

**Green/control fixture:** change the unique highest row's live map to explicit `0 CONSISTENT (observation); 2 UNKNOWN (could-not-evaluate)`, with no live `1`; preserve selftest `0 PASS; 1 FAIL` as a separate map. Expected `audit_live_map_errors=0`, exit `0`, no C3 finding. A live `1` must fail even though selftest failure `1` is valid.

## Why historical-row or digit-presence checks are inadequate

The generic probe check only requires the verdict cell to contain numeric tokens `0` and `2` (`tools/check-registry-coverage.py:229–236`, patterns at `:28–30`). A cell containing all of `0`, `1`, and `2` satisfies that presence check; it does not establish which mode owns `1`, or whether `1 DEGRADED` is an invalid live verdict. Likewise, checking or rewriting any lower row says nothing about the unique highest selected table. The finite C3 check must inspect the selected `boot-chain-audit` live/selftest map, not “some row” or token presence.

Source pin S079 identifies `tools/boot-chain-audit.sh` at baseline `0cbc34dd6b20896085a8fb07943e3ea4027d8472` (`corpus/SOURCES.md:86`). Its v2 header says live exit `1` is never emitted and no v2 verdict maps to `DEGRADED` (`tools/boot-chain-audit.sh:81–86`); the live summary returns only `UNKNOWN`/2 or `CONSISTENT`/0 (`:794–806`). Selftest is a separate mode: assertion success returns 0 and failed assertions return 1 (`:1216–1221`). These source facts support the semantic distinction, not host readiness. The exact ID/count/exit expectations above come from preregistration; they were not observed by execution.

## Residual risk and verification gaps

No candidate diff or measurement result was reviewed, and no evaluator or fixture was run. The baseline checker parser shown here has no `--audit-live-map` option (`tools/check-registry-coverage.py:281–292`); the preregistered CLI behavior is an oracle contract for the later evaluator, not an observed baseline result. No `lsp` device/tool was exposed, so status/references/definition/diagnostics were unavailable; grep was used only for locating, with conclusions grounded in direct source reads.

Scope: executed=none
