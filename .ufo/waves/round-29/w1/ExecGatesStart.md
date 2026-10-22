Partly holds: the start-of-round state at 81a061a67466c5e1be812814a895a4b5ed89b4ff is recorded; registry coverage and self-assessment are red, while all 31 discovered tool selftests pass.

1. [obs] The measured revision is 81a061a67466c5e1be812814a895a4b5ed89b4ff; the registry report binds it on master with branch tip 3c94d7308e561832a0df0981cbc39dda270e32d8. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/registry-coverage.txt:1-3.

2. [obs] `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` exited 0. It emitted 25 W04 duplicate-URL-across-scopes warnings for S038, S041, S042, S043, S044, S046, S049, S058, S082, S087, S089, S090, S092, S095, S098, S105, S106, S107, S108, S109, S111, S126, S136, S137 and S138; the final corpus/SOURCES.md row is `ok`. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/sources-census.txt:1-28.

3. [obs] Registry coverage exited 1 (FAIL): tools_total=35, rows_total=33, with exactly two REGISTRY-ROW-MISSING findings: tools/check-owed-statements-r29.py and tools/probe-git-env-leak.py. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/registry-coverage.txt:1-3.

4. [obs] Self-assessment exited 1 (FAIL), checked 27 checks and reported one mismatch, K10: the depth row states 32 corpus/lessons files while the revision contains 33. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/self-assessment.txt:5-6,99-103,358.

5. [obs] `bash tools/tsukuroi-census.sh --selftest` exited 0 with `TSUKUROI_CENSUS_SELFTEST: PASS (97 cases, 97 passed, 0 failed)`. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/census-selftest.txt:101-102.

6. [obs] All 31 discovered `--selftest` invocations under tools/ exited 0. Python commands were run with `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE`; each retained log records the exact command, output, and final exit code. The shell census selftest is also retained. Results and evidence pointers:

- `python3 tools/_revision.py --selftest`: exit 0, `REVISION_SELFTEST: PASS (57 cases, 57 passed, 0 failed)`; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/selftest-_revision.txt.
- `python3 tools/check-adjacency-anchors.py --selftest`: exit 0, `PASS (25 cases, 25 passed, 0 failed)`; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/selftest-check-adjacency-anchors.txt.
- `python3 tools/check-adjacency-overlap.py --selftest`: exit 0, 43 cases and 0 failed; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/selftest-check-adjacency-overlap.txt.
- `python3 tools/check-appended-notices.py --selftest`: exit 0, `PASS (47 cases, 47 passed, 0 failed)`; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/selftest-check-appended-notices.txt.
- `python3 tools/check-boot-chain.py --selftest`: exit 0, `PASS (83 cases, 83 passed, 0 failed)`; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/selftest-check-boot-chain.txt.
- `python3 tools/check-boot-writers.py --selftest`: exit 0, `PASS (12 cases, 12 passed, 0 failed)`; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/selftest-check-boot-writers.txt.
- `python3 tools/check-boundary-contract.py --selftest`: exit 0, `PASS`, 28 cases and 0 failed; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/selftest-check-boundary-contract.txt.
- `python3 tools/check-edit-contract.py --selftest`: exit 0, `PASS`, 102 cases and 0 failed; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/selftest-check-edit-contract.txt.
- `python3 tools/check-freshness-r17.py --selftest`: exit 0, `PASS (59 cases, 59 passed, 0 failed)`; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/selftest-check-freshness-r17.txt.
- `python3 tools/check-kernel-taint.py --selftest`: exit 0, 55 cases and 0 failed; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/selftest-check-kernel-taint.txt.
- `python3 tools/check-locator-clarification.py --selftest`: exit 0, `PASS (37 cases, 37 passed, 0 failed)`; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/selftest-check-locator-clarification.txt.
- `python3 tools/check-memory-pressure.py --selftest`: exit 0, 41 cases and 0 failed; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/selftest-check-memory-pressure.txt.
- `python3 tools/check-path-reconciliation.py --selftest`: exit 0, `PASS`, 40 cases and 0 failed; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/selftest-check-path-reconciliation.txt.
- `python3 tools/check-pause-gate.py --selftest`: exit 0, `PASS`, 24 cases and 0 failed; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/selftest-check-pause-gate.txt.
- `python3 tools/check-recheck-commands.py --selftest`: exit 0, `PASS`, 95 cases and no failures; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/selftest-check-recheck-commands.txt.
- `python3 tools/check-registry-coverage.py --selftest`: exit 0, `PASS (23 cases, 23 passed, 0 failed)`; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/selftest-check-registry-coverage.txt.
- `python3 tools/check-review-cohort.py --selftest`: exit 0, `PASS`, 24 cases and 0 failed; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/selftest-check-review-cohort.txt.
- `python3 tools/check-review-snapshots.py --selftest`: exit 0, `PASS`, 24 cases and no failures; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/selftest-check-review-snapshots.txt.
- `python3 tools/check-revision-binding.py --selftest`: exit 0, `PASS (78 cases, 78 passed, 0 failed)`; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/selftest-check-revision-binding.txt.
- `python3 tools/check-root-dac-correction.py --selftest`: exit 0, `PASS (54 cases, 54 passed, 0 failed)`; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/selftest-check-root-dac-correction.txt.
- `python3 tools/check-seat-bindings.py --selftest`: exit 0, `PASS`, 121 cases and 0 failed; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/selftest-check-seat-bindings.txt.
- `python3 tools/check-seat-scope.py --selftest`: exit 0, `PASS (54 cases, 54 passed, 0 failed)`; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/selftest-check-seat-scope.txt.
- `python3 tools/check-section-citations.py --selftest`: exit 0, `PASS (68 cases, 68 passed, 0 failed)`; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/selftest-check-section-citations.txt.
- `python3 tools/check-selector-contract.py --selftest`: exit 0, 28 cases and no failures; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/selftest-check-selector-contract.txt.
- `python3 tools/check-self-assessment.py --selftest --repo /fast/scratch/hyaku/tsukuroi-r29/ExecGatesStart/repo`: exit 0, `PASS`, 15 cases and no failures; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/selftest-check-self-assessment.txt.
- `python3 tools/check-source-scope-correction.py --selftest`: exit 0, `PASS (29 cases, 29 passed, 0 failed)`; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/selftest-check-source-scope-correction.txt.
- `python3 tools/check-storage-health.py --selftest`: exit 0, 44 cases and 0 failed; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/selftest-check-storage-health.txt.
- `python3 tools/measure-update-recheck.py --selftest`: exit 0, `PASS (20 cases, 20 passed, 0 failed)`; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/selftest-measure-update-recheck.txt.
- `python3 tools/report-red-causes.py --selftest`: exit 0, `PASS`, 12 cases and 0 failed; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/selftest-report-red-causes.txt.
- `bash tools/boot-chain-audit.sh --selftest`: exit 0, `TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=45 failed=0`; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/selftest-boot-chain-audit.txt.
- `bash tools/tsukuroi-census.sh --selftest`: exit 0, `TSUKUROI_CENSUS_SELFTEST: PASS (97 cases, 97 passed, 0 failed)`; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/census-selftest.txt.

Scope: read=SCORECARD.md round 29 declaration and tools/ selftest flags; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart.md and /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ExecGatesStart/*.txt (34 retained logs); executed=sandbox clone/checkout at 81a061a67466c5e1be812814a895a4b5ed89b4ff; sources-census validate; check-registry-coverage and check-self-assessment revision gates; all 31 discovered tools --selftest commands.
Model: openai-codex/gpt-6-luna
Installs: none
