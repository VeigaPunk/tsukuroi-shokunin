# C3 code-1 distinction — static falsification review

## Finding

No counterexample found in the candidate matcher: the selected operative `boot-chain-audit` row accepts the registered selftest `1 FAIL` but rejects a live `1 DEGRADED`. This is a finite exact-map check, not general parsing of arbitrary exit-code prose.

## Evidence

- Candidate `/tmp/tsukuroi-r20-registry-20261021/tools/check-registry-coverage.py:110-129,137-183` parses Markdown cells, selects only the unique highest-numbered registry table, and returns that table's rows. `_audit_live_map` then identifies the exact `boot-chain-audit` row and compares its Verdict map cell (`cells[3]`) to `AUDIT_LIVE_MAP` after whitespace normalization (`:270-288`). The required constant explicitly contains `live: 0 ...;2 ...` and separately `selftest: 0 PASS;1 FAIL` (`:31-34`); any additional live mapping, including live code 1, differs and returns `REGISTRY-AUDIT-LIVE-MAP`.
- The map check is wired only for `--audit-live-map`; its finding count is emitted as `audit_live_map_errors` (`:351-355`). Preregistration requires the selftest-1-only class to be allowed and legacy live-1 to fail (`.ufo/waves/round-20/preregister.json:49-53`).
- Positive control: the candidate's corrected fixture uses the exact constant, including selftest `1 FAIL`, and asserts PASS with zero C3 errors and no findings (`:565-581`). This is source evidence of the intended acceptance, not a run result.
- Minimal failing mutation: starting from that corrected fixture, change only the Verdict cell's live segment from `live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate;` to `live: 0 CONSISTENT/observation;1 DEGRADED;2 UNKNOWN/could-not-evaluate;`, leaving the separate `selftest: 0 PASS;1 FAIL` untouched. The candidate constructs exactly this mutation (`:569-574`) and specifies the expected FAIL, one `REGISTRY-AUDIT-LIVE-MAP`, and `audit_live_map_errors=1` (`:583-590`). Those are fixture assertions, not observed execution output.

## Axes and correction

- **Impacted axis:** C3 calibration (`audit_live_map_errors`); the check also relies on the existing operative-table parsing contract, but this review found no table-selection defect relevant to this distinction.
- **Smallest safe correction:** none indicated by static inspection. Preserve the exact mode-labelled comparison. A broad “reject any `1`” rule would wrongly reject the valid selftest failure code; digit-presence checks would wrongly admit live 1.

## Limits

Candidate source and fixture definitions only; no selftest, evaluator, or command was run. This does not establish host state, boot readiness, or safety.

Scope: executed=none
