# L1 development runs of the amended C1 probe (not receipts)

Probe bytes: `tools/probe-child-env-allowlist-r34.py` VERSION 5, sha256 `5231dbaf…` (amendment 1), run from the
lane working tree against the L1 scratch clone `/fast/scratch/hyaku/tsukuroi-r34/L1/repo`, 2026-10-23 ~08:50Z.

| file | candidate | pairs | leaking | base-parity lists |
|---|---|---|---|---|
| `e1bec24154cf40aa64d0bc5a0bc49a1f2daf04ce.jsonl` | the claimed change as drafted (`candidate-change-e1bec241.patch`) | 27 | 0 | all empty |
| `6de666c427ba9aa6b4350561980bde8d0e7c261d.jsonl` | declaration commit (do-nothing) | 27 | 27 | all empty |
| `b3242da6ed8eda91c1bc71c99af20015a83f0411.jsonl` | dummy: work replaced by one clean `git --version` and `PASS` (`dummy-b3242da6.patch`) | 27 | 18 | non-empty for all nine |

`../dev-after-declaration-bytes/` holds the same candidate change scored per target (`--only`) with the declaration
bytes (`35a87374…`): 0 of 27. The binding receipts come from the residual pre-data control call.
