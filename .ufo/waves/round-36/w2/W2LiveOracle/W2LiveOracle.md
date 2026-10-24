# QUALITY-82 live-view rerun (C1)

## Scope and invocation

The real lane checkout was at `c052bb7d41ced49aa888817069afd804eccfecf1` (`git rev-parse HEAD`); the initial `git status --short` showed untracked wave artifacts only. The supplied `w1/ExecLiveViewDesign/run-live-view.sh` hardcodes its capture output under W1, outside this seat's write scope. I therefore ran a faithful copy at `run-live-view-bounded.sh`, redirecting `SEAT` to this W2 seat (and the wrapper fallback log path likewise); its five tool commands, arguments, environment isolation, 10-canary generation, and `strace`/wrapper capture follow the supplied runner and `view-spec.md`.

Command:

```sh
/usr/bin/bash /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w2/W2LiveOracle/run-live-view-bounded.sh c052bb7d41ced49aa888817069afd804eccfecf1 quality82-liveview-c052-W2LiveOracle
```

The capture records the real lane path and requested revision in `capture/quality82-liveview-c052-W2LiveOracle/context.txt`. The ten newly generated canaries are in `capture/quality82-liveview-c052-W2LiveOracle/canary-names.txt`.

## Per-tool result

All five records have `canary_leaked_to_child: false` and `leaking_children: []` in `capture/quality82-liveview-c052-W2LiveOracle/dev-run.jsonl`:

| Tool | Exit code | Canary leakage to child |
|---|---:|---|
| `check-revision-binding.py` (`binding`) | 0 | No; `leaking_children: []` |
| `check-report-receipts.py` (`receipts`) | 0 | No; `leaking_children: []` |
| `score-census-handoff-r32.py` (`handoff`) | 1 | No; `leaking_children: []` |
| `mutants-btrfs-space-r30.py` (`mutants`) | 0 | No; `leaking_children: []` |
| `run-receipt.py` (`runner`) | 0 | No; `leaking_children: []` |

The runner's captured aggregate was `tools: 5`, `leaked_tools: 0`, with exit codes `{binding: 0, handoff: 1, mutants: 0, receipts: 0, runner: 0}`. Thus the requested live-view leakage result is 0/5 tools, while the overall command set was not all-green because handoff returned 1.

Handoff stdout's final summary reports `consistent: false`, `live_consistent: false`, `predicate_label: "routed"`, `routed: 24`, `unrouted: []`, `harness_errors: 0`, `scenarios: 24`, and `revision: c052bb7d41ced49aa888817069afd804eccfecf1`. This is a separate handoff consistency failure, not a canary leak; stderr was empty. I did not investigate or remediate that adjacent result.

## Retained evidence

All files are under this seat's `capture/quality82-liveview-c052-W2LiveOracle/`:

- `dev-run.jsonl` — per-tool child-leak records and exit codes.
- `canary-names.txt`, `context.txt`, `commands.tsv`, `exitcodes.tsv` — generated names, target revision/path, exact outer commands, and codes.
- `*.execve.log`, `wrappers/*.env`, `*.stdout`, `*.stderr` — exec trace, interposed environment captures, and tool output; `run-receipt.receipt.jsonl` retained.
- `handoff.stdout` ends with the consistency summary cited above.

No package/tool installs or production-file edits were made. The run used the read-only modes and scratch handling described in `w1/ExecLiveViewDesign/view-spec.md`; the evidence does not establish that every nested program ran directly from the checkout (binding and receipt runner use scratch clones per that spec).
