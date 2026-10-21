# JudgeOriginalNine — R20 C2 scope audit

## Findings

### High — `--object-selectors` cannot produce a nine-tool result

In `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py`, `accepted` accepts four positional arguments (`:393-400`), but nested `exact_accept` calls it with five (`:479-481`): `accepted(sandbox, name, revision, expected_sha, branch)`. The first success case invokes `exact_accept` for `real_prefix_shadow_branch` (`:594`). Thus a populated selector probe raises `TypeError` before recording the per-tool selector results. `main` catches the exception as `E-INTERNAL` and returns `CANNOT` (`:1114-1118`); with object selectors requested, `cannot_payload` reports `object_selector_tools: 0`, `object_selector_total: TOTAL`, and `object_selector_status: CANNOT_EVALUATE` (`:739-743`). This blocks the claimed nine-tool measurement; it is not a `0/9` evaluated failure result.

### Medium — a discovered-tool execution exception can suppress the original-nine metric

`measure` appends discovered tools to the probe list (`:643-645`) and calls `probe_tool` for each non-absent entry without a per-tool exception boundary (`:663`). A tool timeout or launch `OSError` raises `Cannot` in `run_tool` (`:367-370`), which reaches the global `main` handler (`:1110-1113`) and returns the same whole-measurement `CANNOT_EVALUATE` payload. Therefore discovered tools do not enter `object_selector_tools`, but a discovered tool that cannot be run can still prevent the original-nine selector metric from being emitted. This is a scope leak on the cannot-evaluate path, distinct from counting an extra tool in the numerator. The current argument-count failure occurs earlier for populated selector probes, so this conditional path is source-derived, not dynamically exercised.

## Scope checks

- **Denominator and membership:** `TOOLS` is the five legacy names plus the four R17 gates, and `TOTAL = len(TOOLS)` (`:61-80`), matching the preregistered original nine. `discover` explicitly excludes names in `TOOLS` (`:245-256`). Selector probes are run only when `name in TOOLS` (`:664-666`); `named` and `additional` are split by that name set (`:676-677`); `selector_count`, `object_selector_total`, and `object_selector_per_tool` use `named` only (`:703-713`). On a completed measurement, discovered tools are excluded from the nine-tool numerator, denominator, and per-tool selector list.
- **Absent original tool:** the absent branch sets `object_selector_ok = False` for a missing original member (`:652-662`); it remains in `named` and only truthy flags count (`:676,704`). So the intended path fails closed rather than awarding credit for absence. The existing absent-tool selftest calls `measure(fx4, tip4)` without `object_selectors=True` (`:952-958`), so it does not exercise this selector-specific path. The object-selector scope selftest instead uses all nine originals plus one discovered extra (`:1021-1030`); it is also blocked by the argument-count error above if run.
- **Aggregate cannot-evaluate:** `cannot_payload` explicitly reports zero tools out of nine, `CANNOT_EVALUATE`, and an empty selector per-tool list (`:733-744`); a selftest checks the shape (`:1078-1085`). This correctly does not count an unevaluated tool as passing, although the helper-arity defect makes this the actual result for populated selector runs.

## Verification gaps and limits

Source inspection only; no tests or candidate commands were run under the NO-EXEC contract. LSP was not available within the permitted read/grep/glob/write tool set; grep was used to locate symbols, and conclusions above are from direct source reads, not semantic-reference proof. No host or boot-safety claim is made.

Scope: executed=none
