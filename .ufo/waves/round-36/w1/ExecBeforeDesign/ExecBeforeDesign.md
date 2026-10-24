# ExecBeforeDesign — C1 before-receipt procedure

## Deliverables

- `run-before.sh` — executable, takes one probe path, pins the runner receipt revision to `6d76fb20f6ecbc940e5c8fff36c74060c885e161`, requires the probe file to match its committed `HEAD` blob, and runs each probe invocation through `tools/run-receipt.py`. Receipts go to the invoking directory. It schedules the `livefive --json` run, `claim`/`r33claim`/`regression` baseline runs, then the two `claim` mutant runs. Expected probe status 1 is accepted only for the before and mutant runs; baseline sensitivities must exit 0. Each probe receipt's runner `tool_sha256` is therefore the committed probe hash, and its runner `revision` is the declaration base.
- `harness-dry.jsonl` — actual `run-receipt.py` receipt for the existing `tools/check-recheck-commands.py` at the base.
- `expected-output.md` — expected final-summary key order/schema, base sensitivity counts and predicates, and the five-target before criterion.

## Retained evidence

The harness receipt was produced with:

```text
python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/run-receipt.py --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --revision 6d76fb20f6ecbc940e5c8fff36c74060c885e161 --out /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1/ExecBeforeDesign/harness-dry.jsonl --timeout 2400 -- tools/check-recheck-commands.py --revision 6d76fb20f6ecbc940e5c8fff36c74060c885e161
```

The runner printed `{"out": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1/ExecBeforeDesign/harness-dry.jsonl", "revision": "6d76fb20f6ecbc940e5c8fff36c74060c885e161", "tool": "tools/check-recheck-commands.py", "exit_code": 0}`. The retained receipt header names that revision and has `tool_revision` equal to it, `tool` equal to `tools/check-recheck-commands.py`, and `tool_sha256` `1c6f349d4c298a3867c7163c7c3fb32f1c768adb0df7110fc7b216a4656b8cd1`. Its command argv is `tools/check-recheck-commands.py --revision 6d76fb20f6ecbc940e5c8fff36c74060c885e161`. The tool emitted `status: PASS`, `clean_count: 39`, `file_count: 55`, `findings: []`, `flagged_count: 0`, `invocation_count: 81`, `pointer_section_count: 42`, `resolved_count: 16`, and the expected revision. The footer records `exit_code: 0`, `timed_out: false`, and empty `stderr_tail`.

`run-receipt.py --help` reported the interface `--revision REVISION [--tool-revision TOOL_REVISION] --out OUT [--lane LANE] [--timeout TIMEOUT] ...`; the harness invocation uses its exact `-- <tool> [args...]` form. Help was also run for every named livefive target:

- `check-revision-binding.py --help`: `--selftest` and `--tools-revision` are present.
- `check-report-receipts.py --help`: `--selftest`, `--report`, `--lane`, and `--revision` are present.
- `score-census-handoff-r32.py --help`: `--revision`, `--lane`, `--scratch`, `--seed`, `--scenarios`, `--keep-scratch`, `--timeout`, and `--budget` are present.
- `mutants-btrfs-space-r30.py --help`: `--counter` and `--keep` are present.
- `run-receipt.py --help`: `--revision`, `--tool-revision`, `--out`, `--lane`, `--timeout`, and command arguments are present.

`check-recheck-commands.py --help` confirmed the receipt dry-run's `--revision` option. No target selftest mode is named in `run-before.sh`; it delegates target selection/modes to the probe's declared sets.

## Blockers and risks

- The requested `tools/probe-child-env-allowlist-r36.py` did not exist when checked (`test -e` exit 1; the path lookup returned not found). Accordingly, `run-before.sh` and the round-36 probe battery were not executed. The script's `--set livefive --json` and inherited set invocations follow the requested interface plus the existing r34 probe pattern, but the new probe's actual help, summary field order, `--json` support, and `predicate_label` remain unverified. The expected r36 summary shape is a design expectation, not an observed result. The `claim`/`r33claim`/`regression` counts in `expected-output.md` are inferred from the existing r34 set definitions (9/5/11 targets; 27/15/33 pairs), not measured from the absent r36 probe.
- The round-34 mutant evidence folders are present, but they are not independent Git sandboxes: `git -C .../.ufo/waves/round-34/w2/MutAttrgetterCopy rev-parse --show-toplevel` and the corresponding MutPathCopy command both resolve to the lane repository. The actual historical repositories referenced by the reports, `/fast/scratch/hyaku/tsukuroi-r34/MutAttrgetterCopy/repo` and `/fast/scratch/hyaku/tsukuroi-r34/MutPathCopy/repo`, both returned `fatal: cannot change to ...: No such file or directory`. `MutPathCopy/variant.patch` is also absent at the evidence path. The script records those missing dependencies and exits 2 after its base runs rather than treating either mutant sensitivity conjunct as passed. Mutant receipts still need the real sandbox repositories or an authorized replacement artifact.
- The before state and sensitivity output shapes in `expected-output.md` are not live observations. The declaration supplies the acceptance predicates; the field order follows the existing r34 probe summary. Reconcile against the frozen r36 probe before integration.

No production files were edited and no tools were installed. No build, lint, formatter, or test suite was run; the single requested end-to-end harness proof is the retained receipt above.
