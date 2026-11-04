# ExecSource — round 78

Axes: depth and operability. Supporting extracted-source execution only; no production changes or outside verdict.

Detailed report: `.ufo/waves/round-78/w1/ExecSource/report.md`.

Evidence: `ExecSource/provenance.json`, `ExecSource/receipt.json`, full `ExecSource/harness.c`, exact `ExecSource/manager_determine_path_usage.c`, upstream `ExecSource/endswith_internal.c`, narrow `ExecSource/context.h`, `ExecSource/main.c`, and reproducible `ExecSource/run_harness.py` (all beneath this report's parent directory).

Pinned function bytes unchanged; SHA256 `bbbe6f656e6e4a525a114603d7a6b3e2e2f9a95268aa90f2fa9030733adb5b9a`. GCC 16.2.1 compilation exit 0, driver exit 0; all six real-filesystem calls matched lstat-based expected usage: active 4096, archived 8192, unrelated 0, symlink 0, directory 0, sparse 4096. Sparse apparent size 67108864 versus allocation 4096; symlink target allocation 4096, not counted. Full commands, exits and raw outputs retained in receipt.json.

Stat-failure branch explicitly NOT EXERCISED. Six fixtures are not frozen U1–U6 completion: sparse replaces the unstatable case; actual metadata differs from modeled descriptors. Directory allocation was zero, so that fixture alone does not discriminate removal of S_ISREG. Helper body is upstream verbatim; its const-generic return annotation is bypassed at boolean callsites. FOREACH_DIRENT_ALL shim uses real readdir but does not reproduce readdir-error policy. No installed-journald or integration claim.

No tools installed/updated, no production edits, no repository gates run. Private fixtures/executable and scratch directory removed. Parent owns integration and frozen gate execution.
