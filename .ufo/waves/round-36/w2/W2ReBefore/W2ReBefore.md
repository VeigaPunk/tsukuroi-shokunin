# W2ReBefore — round 36 C1 before evidence

## Finding

The requested direct `livefive` invocation exited 1 at its first target, `tools/check-revision-binding.py`, with `RuntimeError: cannot create local master branch` (trace points to probe line 499), before emitting a summary. A `tools/run-receipt.py` repeat at the same frozen base and probe bytes completed all five targets: 18/20 pairs leaked, with `harness_errors: []`, exit 1, and every target above zero. The direct failure and receipt-backed success are an observed divergence; its cause is unknown. A separate receipt-backed `--only` run of the remaining four also completed with 14/16 leaking pairs.

## Live-view BEFORE capture

The existing capture at `.ufo/waves/round-36/w1/ExecLiveViewDesign/capture/base-final-6d76fb20/` records `canary_leaked_to_child: true` and exit code 0 for all five targets. The machine records and their summed `leaking_children.process_count` values are:

| Target | Canary reached child | Leak groups | Processes in leak groups |
|---|---:|---:|---:|
| `check-revision-binding.py` | true | 4 | 469 |
| `check-report-receipts.py` | true | 1 | 2 |
| `score-census-handoff-r32.py` | true | 29 | 3050 |
| `mutants-btrfs-space-r30.py` | true | 1 | 84 |
| `run-receipt.py` | true | 5 | 13 |

Evidence: `dev-run.jsonl:1-5` (each record names the tool and capture file); `commands.tsv:1-5` maps those targets; `exitcodes.tsv:1-5` records all five runners at exit 0. This verifies the separate live-view BEFORE canary capture, not a successful full `livefive` probe run.

## Probe evidence

### Full `livefive`

Command attempted: `python /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/probe-child-env-allowlist-r36.py --revision 6d76fb20f6ecbc940e5c8fff36c74060c885e161 --set livefive --scratch /tmp/w2-before`. Direct output is retained in `livefive.stdout` and `livefive.exit` (exit 1). The traceback reaches `one_run()` and raises `cannot create local master branch`; there is no summary JSON, so full-set `leaking`, `harness_errors`, and per-target counts are unavailable. The captured error is a harness failure, not a pass/fail leak count.

### Full receipt-backed `livefive`

`livefive.receipt.jsonl` is the complete `tools/run-receipt.py` receipt. Header: revision `6d76fb20f6ecbc940e5c8fff36c74060c885e161`, tool revision `c052bb7d41ced49aa888817069afd804eccfecf1`, tool `tools/probe-child-env-allowlist-r36.py`, tool SHA-256 `a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a`. Summary JSON: 5 targets, 20 pairs, 18 leaking, `harness_errors: []`, probe version 7, predicate `leaking`; footer exit 1, `timed_out: false`.

| Target | Leaking channels | Leaking pairs |
|---|---|---:|
| `check-revision-binding.py` | names, quiet, source, untraced | 4/4 |
| `check-report-receipts.py` | names, quiet, source | 3/4 |
| `score-census-handoff-r32.py` | names, quiet, source, untraced | 4/4 |
| `mutants-btrfs-space-r30.py` | names, quiet, source | 3/4 |
| `run-receipt.py` | names, quiet, source, untraced | 4/4 |
| **Full set total** |  | **18/20** |

This receipt-backed run supports the expected base result of more than zero leaks on each of the five targets. It differs from the direct invocation's early harness abort; no cause for that divergence is established.

### Remaining four livefive targets (`--only`)

`livefive-rest.receipt.jsonl` is a `tools/run-receipt.py` JSON-lines receipt. Header: revision `6d76fb20f6ecbc940e5c8fff36c74060c885e161`, tool revision `c052bb7d41ced49aa888817069afd804eccfecf1`, tool `tools/probe-child-env-allowlist-r36.py`, tool SHA-256 `a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a`; probe version 7, predicate label `leaking`. The receipt reproduces stdout and ends with exit code 1 (leaks), `timed_out: false`, and empty stderr tail.

| Target | Leaking channels | Leaking pairs |
|---|---|---:|
| `check-report-receipts.py` | names, quiet, source | 3/4 |
| `score-census-handoff-r32.py` | names, quiet, source, untraced | 4/4 |
| `mutants-btrfs-space-r30.py` | names, quiet, source | 3/4 |
| `run-receipt.py` | names, quiet, source, untraced | 4/4 |
| **Partial set total** |  | **14/16** |

Summary JSON records `targets: 4`, `pairs: 16`, `leaking: 14`, `harness_errors: []`, and exit 1. The source-channel findings are included by the probe's frozen predicate; the table therefore reports canonical probe leak pairs, not only child-environment carriers. The missing `check-revision-binding.py` target has no measured pair.

### `regression` set

Command: `python /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/probe-child-env-allowlist-r36.py --revision 6d76fb20f6ecbc940e5c8fff36c74060c885e161 --set regression --scratch /tmp/w2-before`. Direct output is retained in `regression.stdout` (`regression.exit` is 1). Summary: revision/base `6d76fb20f6ecbc940e5c8fff36c74060c885e161`, probe version 7, predicate `leaking`, 11 targets, 44 pairs, 6 leaking, `harness_errors: []`, exit 1. The run-receipt repeat has the same summary and target/channel results. Two mutant targets leak in the `names`, `quiet`, and `untraced` channels; the other nine targets have 0/4:

| Target | Leaking channels | Leaking pairs |
|---|---|---:|
| `check-adjacency-overlap.py` | — | 0/4 |
| `check-freshness-r17.py` | — | 0/4 |
| `check-kernel-taint.py` | — | 0/4 |
| `check-memory-pressure.py` | — | 0/4 |
| `check-registry-coverage.py` | — | 0/4 |
| `check-self-assessment.py` | — | 0/4 |
| `check-storage-health.py` | — | 0/4 |
| `mutants-adjacency-overlap.py` | names, quiet, untraced | 3/4 |
| `mutants-kernel-taint.py` | names, quiet, untraced | 3/4 |
| `mutants-owed-statements-r29.py` | — | 0/4 |
| `mutants-owed-statements-r29-landed.py` | — | 0/4 |

This falsifies the requested regression-set zero-leak expectation at the frozen base: both the direct run and receipt-backed repeat report six leaks in the same six pairs and no harness errors. This is a real observed divergence from the expected zero-leak control, not a harness error.

## QUALITY 77 and scope

`livefive.receipt.jsonl`, `livefive-rest.receipt.jsonl`, and `regression.receipt.jsonl` each have a `tools/run-receipt.py` header naming revision `6d76fb20f6ecbc940e5c8fff36c74060c885e161`, tool revision `c052bb7d41ced49aa888817069afd804eccfecf1`, the probe tool, and SHA-256 `a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a`; each reproduces probe stdout and has a footer with exit code 1, `timed_out: false`, and empty stderr tail. These seat receipts are not yet committed; under `corpus/QUALITY.md:147`, they become admissible for revision-cited claims only after the parent integrates/commits them. The direct stdout/exit files are retained separately. No production files were changed; no tools were installed.

Scope: read the Godspeed skill, probe v7 target/runner code, QUALITY 77, and the round-36 wave-1 BEFORE capture; executed the requested direct livefive and regression probes, receipt-backed full `livefive`, `livefive --only` partial, and regression runs; wrote only this seat directory and the probe's `/tmp` scratch roots.
