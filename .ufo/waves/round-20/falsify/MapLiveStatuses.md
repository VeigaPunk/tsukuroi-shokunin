# MapLiveStatuses — C3 live-map critic

## Counterexample: C3 metric can undercount a duplicate tool row

[INFERENCE] In a structurally parsed highest operative table, keep one `boot-chain-audit` row with the exact corrected map, then add a second row under another name whose entry or self-test also names `tools/boot-chain-audit.sh` and whose verdict advertises live `1 DEGRADED` (or another invalid map). `_audit_live_map` selects rows only by exact display name `boot-chain-audit` (`/tmp/tsukuroi-r20-registry-20261021/tools/check-registry-coverage.py:277-288`), so it checks the corrected row and produces no C3 map finding. The generic coverage pass tracks entry and self-test paths (`:208-211`, `:244-245`) and reports `REGISTRY-ROW-DUPLICATE` for this fixture (`:257-264`), so this is **not** a clean overall acceptance. However, the C3 count is assigned only from `len(map_findings)` (`:350-355`): it remains `audit_live_map_errors=0` despite an operative row for the audited tool advertising the forbidden live state. That is a fixable C3 metric undercount, not evidence of a false successful run.

**Smallest safe correction:** identify all rows that reference `tools/boot-chain-audit.sh` in entry/self-test paths and require exactly one such row, with the expected name, probe kind, entry path, and exact verdict map. Include duplicate/path-ambiguous cases in `REGISTRY-AUDIT-LIVE-MAP` so the C3 metric cannot report zero for a conflicting operative map. Retain the generic duplicate finding as well.

## Exact status contract and bounded result

The baseline audit source explicitly retains `1 DEGRADED` only as forward-compatible vocabulary and says no schema-v2 verdict maps to it, so live exit 1 is never emitted (`tools/boot-chain-audit.sh:81-86`). Its live summary returns `2 UNKNOWN` when inputs are unknown, there are no entries, or no kernel entry is evaluable; otherwise it returns `0 CONSISTENT` (`:794-806`). `0 CONSISTENT` is not a health/boot-readiness assertion: the provenance row S079 bounds the source to those summary return paths and explicitly excludes live health or readiness (`corpus/SOURCES.md:86`). Selftest is a separate mode where assertions return 0 on pass and 1 on failure (`tools/boot-chain-audit.sh:1216-1221`); main dispatches `--selftest` separately and usage/refusal returns `2 UNKNOWN` (`:1226-1266`).

For a single correctly identified row, the candidate's required constant is exact: `live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; no live DEGRADED; not operator clearance` (`/tmp/tsukuroi-r20-registry-20261021/tools/check-registry-coverage.py:31-34`). The parser requires exactly one named row, probe kind, the boot-chain-audit path, and a verdict equal to that constant after whitespace normalization (`:270-288`). Thus changes that claim live `0 HEALTHY`, live `2 CONSISTENT/healthy`, live `1 DEGRADED`, or an unqualified/otherwise altered verdict are rejected for that selected row; the permitted selftest `1 FAIL` remains explicitly separated. The candidate selftest declares a corrected-map positive case and a live-1 negative case (`:565-590`), consistent with that exact-match gate.

The claim and expected C3 metric are preregistered as calibration `audit_live_map_errors` 1→0, scoped to the highest operative map (`.ufo/waves/round-20/preregister.json:21-27,49-54`). No candidate execution or measurement was performed; the duplicate-row outcome above is a source-derived counterexample, not an observed output. No host or boot-safety conclusion follows.

Impacted axis: **calibration** — the C3 map-error metric can undercount path-duplicate operative declarations even though generic coverage still makes the overall candidate fail.

Scope: executed=none
