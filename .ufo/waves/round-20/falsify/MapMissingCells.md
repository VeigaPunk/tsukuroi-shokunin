# C3 exact-cell falsification review

## Result

No missing/duplicate required map entry can pass the candidate's C3 check. The Verdict-map whitelist is exact after whitespace normalization: `/tmp/tsukuroi-r20-registry-20261021/tools/check-registry-coverage.py:31-34,283-287`. It requires the full sequence `live: 0 ...;2 ...; selftest: 0 ...;1 ...; usage: 2 ...; no live DEGRADED; not operator clearance`. `.split()` followed by `' '.join(...)` normalizes whitespace only; it does not discard or deduplicate codes or clauses. Omitting or duplicating any listed live 0/2, selftest 0/1, or usage 2 entry makes the normalized cell unequal to `AUDIT_LIVE_MAP`, enters the `if` at lines 283-285, and returns `REGISTRY-AUDIT-LIVE-MAP` at lines 286-287.

A missing or duplicated `boot-chain-audit` row also cannot pass: `_audit_live_map` matches `cells[0]` and requires `len(matches) == 1`; zero or multiple rows take lines 277-280 and return the same finding. The caller adds the map finding, records `audit_live_map_errors = len(map_findings)`, and selects `FAIL` / exit 1 when findings exist (`:351-362`; constants `PASS, FAIL, CANNOT = 0, 1, 2` at `:19`). This aligns with the preregistered C3 rejection contract (`.ufo/waves/round-20/preregister.json:49-53`).

For a physically malformed row with a missing/extra table column, the earlier table parser rejects a pipe-prefixed row whose parsed field count differs from the 8-column header (`:170-182`); `main` converts that `TableError` to `E-REGISTRY-TABLE` / CANNOT_EVALUATE (`:363-368`). That is also not a pass, but it is distinct from the C3 map finding.

## Counterexample, evidence limits, and correction

Counterexample: none found in the missing/duplicate map-entry cases. Existing candidate C3 selftests cover the corrected map, legacy live-1 map, highest-table selection, and historical-row-only correction (`:565-613`), but do not include individual missing/duplicate-token mutations. This is a branch-level finding, not an executed result; no tests were run. The parser validates the complete finite Verdict cell, not arbitrary equivalent prose; that is consistent with the finite C3 contract (`preregister.json:27`).

Impacted axis: C3 calibration. Smallest safe correction: no parser change indicated; add table-driven selftest mutations removing and duplicating each required mode/code entry, expecting one `REGISTRY-AUDIT-LIVE-MAP` and `audit_live_map_errors=1`, to lock the currently exhaustive comparison against regression.

Scope: executed=none
