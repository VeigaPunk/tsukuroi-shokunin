# R19 in-place registry correction and false live-map claim

**Axis:** C3 calibration. **Scope:** committed R19 evidence and ordinary source only; no execution or host/boot inference.

## Reconstructed historical-row change

The exact prior cell is preserved in the R18 committed operative-registry snapshot: `.ufo/waves/round-18/measure/final/operative-registry.json:76-82` records the `boot-chain-audit` probe map as `0 CONSISTENT;1 DEGRADED;2 UNKNOWN; not operator clearance`. R19 carried that same map into its new table (`.ufo/waves/round-19/build/drafts/ScribeRegistry19.table.md:14`; delivered-source row `SKILL.md:2073`).

R19 then changed the *existing historical R18 cell* at `SKILL.md:1965` to `0 CONSISTENT;2 UNKNOWN (the live summary never emits 1; 1 is only a selftest assertion failure); not operator clearance`. The committed outside spotcheck identifies this as an in-place correction: §2 row 30 says SKILL alone failed baseline-prefix preservation; §5 item 3 records `SKILL +80/−1` and that historical row 1965 was corrected (`corpus/lessons/round-19-verifier-spotcheck.md:30,148`). This was not append-only, contrary to the R19 report's append-only assertion. The preceding selector text itself said historical cells must not be annotated in place (`SKILL.md:1997-2003`; R18 closure `corpus/lessons/round-18-verifier-spotcheck.md:67-75,177-183`).

## Why the false operative assertion remained

The selector makes the newer R19 table operative: its heading and supersession rule are at `SKILL.md:2060-2065`; its `boot-chain-audit` cell at `:2073` still says `0 CONSISTENT;1 DEGRADED;2 UNKNOWN`. The historical correction at `:1965` therefore did not change the selected current row. The R19 closure explicitly confirmed this divergence and rejected the erratum's broader repair claim (`round-19-verifier-spotcheck.md:79-92,147-148`): only historical row 1965 changed; operative row 2073 still advertised live `1 DEGRADED`.

The source contract supports the corrected live map, not the operative cell. `tools/boot-chain-audit.sh:81-85` says no schema-v2 verdict maps to `DEGRADED` and live exit 1 is never emitted; its summary code selects only `UNKNOWN`/2 or `CONSISTENT`/0 (`:795-800`). Its selftest returns 1 only on failed assertions (`:1216-1221`). Thus the row conflated the live summary with the separate selftest-failure code.

The R19 registry gate explains why this semantic mismatch passed: for a `probe`, `tools/check-registry-coverage.py:229-236` only requires that the verdict cell contain code 0 and code 2; it does not reject an extra code 1 or validate code-to-meaning against the tool. Its accepted `clean_row` fixture is itself a `probe` whose map says `0 ok; 1 fail; 2 could-not-evaluate` (`:431-440`). Accordingly, structural registry coverage could be green while the selected R19 map remained false. The closure records that exact limitation (`round-19-verifier-spotcheck.md:90-92,147`).

**Bounded causal account:** Observed: the historical cell was edited, the selected R19 cell retained the old map, and the generic gate accepted a probe map containing 0/2 plus an unsupported 1. [INFERENCE] The operative assertion persisted because the repair was applied to the lower, historical row and the generic coverage predicate did not test map semantics. The evidence does not establish whether this was deliberate or an oversight.

## Confidence and limits

High confidence in the exact before/after row distinction and the operative-vs-historical divergence: the R18 captured cell, R19 outside spotcheck, R19 table/source, and source return paths agree. High confidence in the structural-gate blind spot from its source predicate and accepted fixture. Authorial intent remains unknown. No live audit, selftest, gate, boot image, or host state was examined or executed. No LSP device was exposed in the permitted read-only tool inventory; conclusions above cite direct source and committed evidence rather than treating grep matches as semantic proof.

Scope: executed=none