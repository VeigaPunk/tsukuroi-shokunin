# FxSeparateC1 — C1/C3 isolation

**Axes:** C1 independence; C3 failure sensitivity; C2 checker preservation.

**Finding — SURVIVES (C1).** In no-hardlinks clone `/tmp/fxseparatec1.SXcG8A`, based at `68a8ae035fde33360cbbe21dc92ca0eacf0a5b33` with origin removed, removed the C3 registry and restored its 17 distinct target paths from `842a5312b704b5cda10fd80ec1fdee5fb381ba97`. Commit on `master`: `0257fe05719017f30ea53e5d8c20294af2a75e4a` (18 files changed). C1's boot-chain correction registry, corrected document, and tools were not reverted.

- `/tmp/fxseparatec1.SXcG8A/tools/check-boot-chain.py --revision 842a5312b704b5cda10fd80ec1fdee5fb381ba97 --statement-corrections --registry-from 68a8ae035fde33360cbbe21dc92ca0eacf0a5b33`: **exit 1**, `status=FAIL`, `correction_count=0`; exactly `CORR-R18-CORR-01-UNRESOLVED` through `-04-UNRESOLVED` (baseline notices absent).
- Same gate at `--revision 0257fe0`: **exit 0**, `status=PASS`, `correction_count=4`, `findings=[]`. C1 remains 4/4 despite C3 removal.
- `/tmp/fxseparatec1.SXcG8A/tools/check-appended-notices.py --revision 0257fe0`: **exit 1**, `status=FAIL`, `NOTICE-MISSING`, `record_count=0`, `distinct_paths=0` (expected absent default C3 registry).
- Same gate with `--registry-from 68a8ae035fde33360cbbe21dc92ca0eacf0a5b33`: **exit 1**, `status=FAIL`, `record_count=88`, `resolved_records=0`, `distinct_paths=17`; 88 `STALE-UNFLAGGED` findings.
- `/tmp/fxseparatec1.SXcG8A/tools/check-revision-binding.py --tools-revision 0257fe0`: **exit 0**, `status=PASS`, original-nine `total=9`, `bound_tools=9`, `consistent_tools=9`. The separately discovered notice checker raises `all_total` to 10 and is outside the original-nine grade.

**Residual risk / verification gap:** isolated local clone only; no runtime/host behavior claimed. LSP route unavailable (`read xd://lsp` returned “No such tool”); no semantic references/definition/diagnostics were available and no grep was used. Initial clone-branch setup attempts failed (`switch -c`: 128; two checkout attempts: 1); corrected setup and final commit succeeded. No production changes.

Scope: executed=clone/setup (exit 0), setup retries (128,1,1), scoped restore+commit (exit 0), C1 baseline/target gates (1,0), C3 default/pinned gates (1,1), C2 gate (0), static reads; no production changes.