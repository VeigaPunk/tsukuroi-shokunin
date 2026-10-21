# C3 historical-row-only repair

**Axis:** C3 calibration — `audit_live_map_errors` (expected legacy high-row error remains 1; an older-row-only correction must not reduce it to 0).

**Counterexample/control:** The candidate already declares the required red control as `audit-live-map-historical-only-fix`. It puts a corrected `boot-chain-audit` row in round 1, leaves the round 2 row at the legacy live-1 map, then requires exit `FAIL`, `audit_live_map_errors == 1`, and exactly `REGISTRY-AUDIT-LIVE-MAP` (`/tmp/tsukuroi-r20-registry-20261021/tools/check-registry-coverage.py:604-613`). A faulty implementation that accepts any corrected historical row (or selects the first/oldest table) would instead pass this fixture with metric 0, violating the declared assertion. The paired control reverses the maps—legacy round 1, corrected round 2—and requires PASS with metric 0 (`.../tools/check-registry-coverage.py:592-603`).

**Evidence:** `_operative_rows` selects the maximum numbered exact registry heading, rejects duplicate headings at that number, parses only that section, and returns its rows (`.../tools/check-registry-coverage.py:137-183`). `main` passes those selected rows to `_audit_live_map` and sets `audit_live_map_errors` to the resulting finding count only under `--audit-live-map` (`.../tools/check-registry-coverage.py:345-355`); the audit requires exactly one matching row with the exact expected map (`.../tools/check-registry-coverage.py:270-288`). The negative selftest therefore exercises the precise historical-only failure mode, not merely an old-row parser case.

**Finding / smallest safe correction:** No selector or selftest defect found in the inspected declarations. Preserve the existing `audit-live-map-historical-only-fix` fixture and its exact metric/finding assertions; no additional source correction is indicated. Source inspection only: the declared test was not run. No host, runtime, or boot-safety claim.

Scope: executed=none.