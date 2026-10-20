# FxCountC3 — freshness census

Axes: C3 record/path coverage; baseline stale-detection and family separation.

## Findings

- **SURVIVES — no actionable C3 defect found.** On landed revision `68a8ae035fde33360cbbe21dc92ca0eacf0a5b33` (`FxCountC3-evidence/landed-revision.txt:1`), the checker returned `PASS`, resolved/record count `88/88`, `distinct_paths=17`, no findings, exit 0 (`FxCountC3-evidence/target-at-68a8ae0.stdout:1`, `.exit:1`). Registry partitions: primary records 1–49 = 49 across 8 paths; supplementary 1–39 = 39 (`freshness-recheck-r18.json`, records begin at line 5 and supplementary 39 at line 876). Target PASS/no findings also means no mixed-family finding was emitted.
- **Baseline behaves as expected.** Direct baseline invocation exits 1 with `NOTICE-MISSING`: the R18 registry is absent at `842a531…` (`FxCountC3-evidence/baseline-at-842a531.stdout:1`, `.exit:1`). Using the target registry against baseline exits 1 and reports `record_count=88`, `resolved_records=0`, and 88 `STALE-UNFLAGGED` findings: each old quote remains while its notice heading is absent (`FxCountC3-evidence/baseline-compare-registry-at-68a8ae0.stdout:1`, `.exit:1`). This matches checker logic at `tools/check-appended-notices.py:256-260`.

All three exact invocations, stdout, stderr, and exit codes are retained under `.ufo/waves/round-18/falsify/FxCountC3-evidence/`; each stderr is empty. They ran from a no-hardlinks sandbox clone with origin removed.

## Residual risk and verification gaps

This structural/document checker does not independently establish the semantic truth or provenance of host observations, nor authorize package, service, or boot actions. The `lsp` device is unavailable (`xd://lsp` returned “No such tool”); references/definition/diagnostics were therefore not available. No grep was used as semantic proof.

Scope: executed=mktemp -d; git clone --no-hardlinks; git checkout --detach 68a8ae035fde33360cbbe21dc92ca0eacf0a5b33; git remote remove origin; git rev-parse HEAD; python3 tools/check-appended-notices.py (the three authorized invocations recorded in evidence)