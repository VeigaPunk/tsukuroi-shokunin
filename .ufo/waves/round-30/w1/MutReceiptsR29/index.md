# Round-29 committed mutation receipts

All mutants are single-file children of base `8976ca92ec3c2e6a2aef07b7065a24ff84a1291b`. Each probe receipt stores the pristine-base, mutant and restored-base outputs, exit codes, commits and file hashes.

| Mutation | Revert patch | Probe receipt | Mutant commit | Detector result |
|---|---|---|---|---|
| AdjBattery: `clean_env()` returns `os.environ` | `MutScrubAdjBattery.patch` | `MutScrubAdjBattery.probe.jsonl` | `5f8754fe81c49c08d4712fd68b02684f8354b671` | mutant leaking 1 / base and restored leaking 0 |
| KtBattery: `clean_env()` returns `dict(os.environ)` | `MutScrubKtBattery.patch` | `MutScrubKtBattery.probe.jsonl` | `f47040e48e1f2bddc7b07370bf910f39aad059da` | mutant leaking 1 / base and restored leaking 0 |
| AdjSelftest: remove `env=` from `git()` subprocess call | `MutScrubAdjSelftest.patch` | `MutScrubAdjSelftest.probe.jsonl` | `196e5dc895856b2aef2ca57d121e6e927f855e97` | mutant leaking 1 / base and restored leaking 0 |

All three mutants have `control_rc=0`, `canary_rc=1`, `leak=true`, and `harness_errors=[]`; all base/restored runs have `control_rc=0`, `canary_rc=0`, `leak=false`, and `harness_errors=[]`. Restored worktree hashes equal the pristine hashes.
