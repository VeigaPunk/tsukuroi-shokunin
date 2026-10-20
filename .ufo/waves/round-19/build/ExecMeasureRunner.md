# ExecMeasureRunner

Model: openai-codex/gpt-6-luna

Files changed: `.ufo/waves/round-19/measure/run.py`, its copy `.ufo/waves/round-19/build/files/measure-run.py`, this report, and retained run artifacts under `.ufo/waves/round-19/measure/dryrun-base/`. `/tmp/measure-run.py` was the temporary compile copy.

Behavior: the runner clones without hardlinks, removes origin, detaches at TARGET and pins `master`; it records tool selftests, C1–C3, the three capture rechecks, both seat-scope checks, live-lane source census, stdout/stderr/exit results, and per-tool digests. Absent gate tools are recorded `skipped-absent`, not passed. [obs] `.ufo/waves/round-19/measure/run.py:11-26,45-90,94-169`

Evidence:
- [obs] `python3 -m py_compile /tmp/measure-run.py` completed without diagnostics; compiled copy is `/tmp/measure-run.py:1-169`.
- [obs] The one authorized BASE dry run retained revision identity and 14 evaluator digests; all 14 selftests exited 0: `.ufo/waves/round-19/measure/dryrun-base/results.json:2-3,5-186`; `evaluator-digests.json:2-18`.
- [obs] C1/C2/C3 are explicitly skipped-absent at BASE: `.ufo/waves/round-19/measure/dryrun-base/results.json:187-281`.
- [obs] Three round-19 capture checks exited 2 / CANNOT_EVALUATE because each capture is absent at BASE: `results.json:283-330`; `recheck-exec-log-r19.stdout:1`, `recheck-exec-log-r19b.stdout:1`, `recheck-exec-log-r19c.stdout:1`.
- [obs] Build and falsify seat-scope checks exited 2 / CANNOT_EVALUATE because neither seat registry nor spec exists at BASE: `results.json:331-361`; `seat-scope-build.stdout:1`, `seat-scope-falsify.stdout:1`.
- [obs] Live-lane sources census exited 0 with W04 duplicate-URL warnings: `results.json:363-377`; `sources-census-live-lane.stdout:1-9`.

Risk/limit: the authorized dry run measured BASE, where round-19 gates/captures/seat declarations are absent; its nonzero CANNOT_EVALUATE results are retained, not acceptance failures. This is author-side evidence only; no claim admission. No blockers.

Scope: executed=python3 -m py_compile /tmp/measure-run.py, python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/measure/run.py 452a054677f6b18284917d7c08c45361f91c25ac dryrun-base
