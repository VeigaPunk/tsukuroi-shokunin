# C1 falsification item 4 — source-channel parameter `env`

**Axis:** operability (C1 source-channel parameter false-positive repair). **Distinct item:** 4.

## Finding

I did not establish a variant that skips the repair and still satisfies the frozen C1 predicate. The strongest grounded control is the known parameter false positive, which a no-op/reverted source-channel fix should fail. The round-36 evidence documents that it is real and reproducible, not merely hypothetical:

- `.ufo/waves/round-36/w2/W2RevCounter/W2RevCounter.md:58-65, 67-76` identifies `score-census-handoff-r32.py:489`, where `run_census(script, env, timeout)` passes `env` to `subprocess.Popen`; V7 reports `env bound by arg`. The report records a livefive result of `leaking: 1`, that exact source pair, no harness errors, exit 1. Its `livefive4-c052bb7.jsonl` artifact lines 45-49 records the same one-leak summary.
- The V7 mechanism is explicit at `tools/probe-child-env-allowlist-r36.py:904-909, 944-957`: `env_ok` accepts checked dicts/builders, while `ast.Name` bindings that are parameters become `env name ... bound by arg`. The frozen source predicate is at lines 301-305.
- `corpus/lessons/round-36-verifier-spotcheck.md:37-40, 52-57, 100-103` independently records the after-commit one-source-pair failure and the repair-commit zero-pair/exit-0 result. The repair is `env=dict(env)` at the Popen call; the observed commit diff is `c052bb7d..4b2d2636` in `tools/score-census-handoff-r32.py:489` (old call passed `env`; repaired call wraps it in `dict`).
- The frozen round-37 declaration, `SCORECARD.md:1881-1883, 1895-1902`, says V8 must resolve parameter values from ambient attribute reads rather than parameter-name matches, and states the kill rule for a skipped fix.

## Minimal should-fail control and falsifier

**Control input:** restore only the V7 source rule that treats a parameter-bound `env` name as an ambient read, while leaving the repaired `run_census(..., env=dict(env), ...)` shape and all other V8 behavior unchanged; run the frozen V8 `--set livefive` at the same revision. Prediction: the pair `tools/score-census-handoff-r32.py:489` is again reported, so summary is nonzero (`leaking_pairs` includes that source pair), with no harness errors; it cannot meet C1's required clean result. This is the minimal counterfactual because the spot-check records that exact location as the sole source leak on the change commit and that the wrapper repair clears it.

**Evidence that would falsify this attack / rule out the control prediction:** a run receipt pinned to the exact V8 hash and revision showing that this parameter-shaped fixed dictionary yields no source finding, plus an isolated true ambient-parameter control (e.g. `env = os.environ` in a builder, passed as the `env` argument to a spawn) that V8 does flag. Without both, a blanket exemption of parameters could make the known false-positive disappear while also concealing a genuine ambient read. The V7 receipts are not evidence that V8 has this property; they only establish the baseline and counterfactual target.

## Evidence status / scope

Observed this round: opened V7 source/version-7 implementation, the W2RevCounter catalogue and its skip-work artifact, the livefive receipt, the round-36 verifier spot-check, and the round-37 declaration. I did not execute a probe or mutate source/lane content. The round-37 V8 target is named in the declaration but is not present in the opened `tools/` listing, so V8 outcome and the proposed control remain unobserved. No sources requiring URL citations were used. No installs or updates.
