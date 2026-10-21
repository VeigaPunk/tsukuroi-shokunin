# C1 ownership-corrections mode scope

## Conclusion

The bound adjacency candidate is `/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py` (`.ufo/waves/round-20/worktree-bindings.json:2-7`). The preregistered C1 command is the explicit `--ownership-corrections` flag (`.ufo/waves/round-20/preregister.json:5-11`). The correction calculation is opt-in: `evaluate(..., ownership_corrections=False)` defaults off, the helper runs only under `if ownership_corrections`, and `main` forwards the parsed flag (`candidate:450-454,761-766,783-789,838-840`). The helper only returns count 1 after the exact appended section, pinned source, and retained arbitration checks; absent or invalid correction paths return 0 with findings (`candidate:135-175,178-196`). Thus the **numeric correction check** is gated by the explicit R20 flag. The measurement source also distinguishes C1 runs with that flag from `adjacency-legacy` without it (`.ufo/waves/round-20/measure/run.py:70-84`).

## Finding — MEDIUM: default R19 output publishes an unmeasured C1 metric

The candidate adds `"ownership_corrections": 0` to `_empty_counts()` unconditionally (`candidate:363-374`). `evaluate()` always starts from `_empty_counts()` (`candidate:450-454`); when the flag is false it never computes or replaces that value (`candidate:761-766`). `emit()` serializes the entire `result.counts` object (`candidate:769-775`). Therefore the ordinary `--revision` path, including the explicitly retained no-flag `adjacency-legacy` invocation (`.ufo/waves/round-20/measure/run.py:83-84`), emits `ownership_corrections: 0` even though the R20 check did not run.

That differs from the R19 baseline output shape: its `_empty_counts()` ends at `live_object_match` and has no ownership metric (`tools/check-adjacency-anchors.py:207-217`); its emitter likewise serializes all counts (`tools/check-adjacency-anchors.py:603-610`). Consequently the R19 *calculation* remains on the legacy path, but the default observable JSON is not unchanged, and the new default-mode zero represents “not evaluated,” not a measured zero. This is the mode/metric mismatch: an R20-only metric is published as a numeric result in a mode that skips its measurement.

## Residual risk and verification gaps

- Source-only review. No candidate or census command, tests, build, lint, formatter, smoke, or runtime was executed; no 0→1 result is asserted.
- `xd://lsp` was unavailable (`No such tool`; mounted devices were `ast_edit` and `debug`). No LSP status, references, definition, or diagnostics were available. Literal source searches were locator-only; conclusions above rely on the directly read definitions and call sites, not grep as semantic proof.
- No tools were installed or updated. No host, boot-safety, or clearance claim is made; boot images remain UNKNOWN.

Scope: executed=none
