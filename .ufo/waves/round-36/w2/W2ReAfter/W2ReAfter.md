# W2ReAfter — round 36 C1 after-battery findings

## Files and behavior

Only this seat report and `probe-results.json` were written; no implementation files changed. No tools were installed. The requested probe was run against `c052bb7d41ced49aa888817069afd804eccfecf1`. Successful summaries all report VERSION 7, predicate label `leaking`, and `probe_sha256=a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a` (matching the requested freeze digest).

## Exact evidence

| Set | Targets / pairs | Leaking / pairs | Harness errors | Exit |
|---|---:|---:|---:|---:|
| `r33claim` | 5 / 20 | 0 / `[]` | `[]` | 0 |
| `claim` | 9 / 36 | 0 / `[]` | `[]` | 0 |
| `regression` | 11 / 44 | 6 / see below | `[]` | 1 |
| `livefive` requested full run | no summary emitted | unknown | exception before results | 1 |
| `livefive` remaining-four selection | 4 / 16 | 1 / `tools/score-census-handoff-r32.py:source` | `[]` | 1 |

Full-set per-target leaking-channel counts (`0` means no channel for that target leaked):

- `r33claim`: `_revision.py` 0; `check-adjacency-anchors.py` 0; `check-boot-writers.py` 0; `check-root-dac-correction.py` 0; `mutants-owed-statements-r29-v4shapes.py` 0.
- `claim`: `check-boot-chain.py` 0; `check-btrfs-repair-r31.py` 0; `check-btrfs-space-r30.py` 0; `check-locator-clarification.py` 0; `check-recheck-commands.py` 0; `check-section-citations.py` 0; `check-seat-scope.py` 0; `check-source-scope-correction.py` 0; `measure-update-recheck.py` 0.
- `regression`: `check-adjacency-overlap.py` 0; `check-freshness-r17.py` 0; `check-kernel-taint.py` 0; `check-memory-pressure.py` 0; `check-registry-coverage.py` 0; `check-storage-health.py` 0; `mutants-adjacency-overlap.py` 3; `mutants-kernel-taint.py` 3; `check-self-assessment.py` 0; `mutants-owed-statements-r29.py` 0; `mutants-owed-statements-r29-landed.py` 0.
- `livefive` remaining-four selection: `check-report-receipts.py` 0; `score-census-handoff-r32.py` 1; `mutants-btrfs-space-r30.py` 0; `run-receipt.py` 0. The sole finding was `tools/score-census-handoff-r32.py:489 inheriting-spawn subprocess.Popen env name env bound by arg` in the `source` channel.

Regression's six pairs are `mutants-adjacency-overlap.py` and `mutants-kernel-taint.py`, each on `names`, `quiet`, and `untraced`. All six report the base-parity `git_argv_sha256` difference, not another evidence item: adjacency-overlap `7be6a8e461423df7c1bf66ad5d2c5f3ce837be4416be1601ae4fd0d515c01a08` vs claim-base `232b981a26ef4f8bf54f77efea67c606cf6d5786b9076b35e7add27d8689367b`; kernel-taint `718448322c9fd870a90baf9855868a0cf777914b14c4ff0030f18be274a02e58` vs claim-base `18e1277b07d8c194f5dc2e9c970b5c8176c45660c235bde7ead3e00b95e37a74`.

The exact full `livefive` command raised `RuntimeError: cannot create local master branch` in the first target, `tools/check-revision-binding.py`, before emitting any result JSON. Retained scratch evidence: the bare clone HEAD is `refs/heads/master`, and the `--no-checkout` worktree already has `refs/heads/master` at the requested C1 commit; the probe's subsequent `git branch master <master-tip>` therefore fails. The separate four-target run completed, but does not replace the missing full-set result.

## Risks / blockers

- Full `livefive` is not measured: the probe crashes on the pre-existing `master` branch collision. Consequently, no `check-revision-binding.py` leaking count or full-set `leaking`/`harness_errors` summary is available.
- The remaining-four livefive run diverges from expected zero because the source scan reports the `score-census-handoff-r32.py` finding above.
- `regression` diverges from expected zero with six base-parity findings on two mutant targets.
- `untraced_record_count` was 0 for every target that completed. Per the probe's documented limit, zero wrapper records are uninformative and are not evidence of safety.

Machine-readable summaries and per-target counts are in `probe-results.json`.