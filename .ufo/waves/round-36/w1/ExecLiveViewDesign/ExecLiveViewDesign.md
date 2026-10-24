# ExecLiveViewDesign — round 36 wave 1

## Result

Ran all five C1 tools at `6d76fb20f6ecbc940e5c8fff36c74060c885e161` against the real lane checkout `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, with each tool's `HOME`/`TMPDIR` under a fresh mktemp scratch tree and ten random synthetic `TSQ_XXXXXXXX` environment canaries. **All five returned exit 0; all five leaked canaries to children.** This is direct live-view evidence, not the frozen C1 probe receipt or a claim verdict.

Final run capture: `.ufo/waves/round-36/w1/ExecLiveViewDesign/capture/base-final-6d76fb20/`. Exact argv: `commands.tsv`; child leak result/groups: `dev-run.jsonl`; canary names and controlled scratch context: `context.txt`; raw process evidence: `*.execve.log` plus `wrappers/*.env`; tool stdout/stderr and the nested runner receipt are alongside. The ten names were `TSQ_8366132d`, `TSQ_1adf6d31`, `TSQ_f123bfe0`, `TSQ_29627015`, `TSQ_1bcbeed0`, `TSQ_312335a2`, `TSQ_54234c0d`, `TSQ_14ce3414`, `TSQ_d2f760d7`, `TSQ_728e3b7c` (none starts with `GIT_` or `TSUKUROI_`). Representative raw `/proc/self/environ` entries are in `wrappers/git.1103887.13231.env`; the run's full child classification is in `dev-run.jsonl`.

| Tool | Exit | Canary result; leaking child classes |
|---|---:|---|
| `check-revision-binding.py` | 0 | Yes: `wrapper:git` 179, `wrapper:python3` 288, `/usr/lib/git-core/git` 1, `git-upload-pack` 1. |
| `check-report-receipts.py` | 0 | Yes: `/usr/bin/git` 2. Its child PATH is explicitly reset to `/usr/bin:/bin`, so strace—not the PATH wrapper—observed these two children. |
| `score-census-handoff-r32.py` | 0 | Yes: `wrapper:git` 2 and the live census tree's children, including the scratch `journalctl` wrapper (2), `/usr/bin/bash` (6), `pacman` (48), `journalctl` (60), `systemctl` (18), plus `awk`, `grep`, `head`, and the remaining recorded utilities. The full class/count list is in `dev-run.jsonl`. |
| `mutants-btrfs-space-r30.py` | 0 | Yes: `wrapper:python3` 84. |
| `run-receipt.py` | 0 | Yes: `wrapper:git` 6, `wrapper:python3` 1, `/usr/bin/git` 2, Git core helpers (`git` 3, `git-upload-pack` 1). Its nested checker reads the real lane path but, by the runner's contract, executes from a scratch clone. |

Other captured execution evidence: `score-census-handoff-r32.py` reported 24/24 routed, `live_consistent=true`, `harness_errors=0`; the mutation runner reported control 10/10, 0/72 should-fail accepted, 0/11 should-pass refused; the receipt checker reported `cited=0`, `unreceipted=0`; the nested receipt records the exact expanded lane/revision and exit 0. These are mode-running evidence only.

## View design and read-only proof

`view-spec.md` records the exact invocation modes, code-level read-only proof, scratch placement, wrapper/strace design, and clone/export caveats. `run-live-view.sh` plus `wrappers/` are self-contained for the wave-2 rerun; use a unique run id, e.g. `run-live-view.sh <REV> w2-after-<short-rev>`. The runner generates fresh canary names each time and summarizes only child execs, not its own launcher.

Important implementation caveats: `check-revision-binding.py` deliberately clones into its TMPDIR sandbox to mutate refs/objects while reading the real lane. `score-census-handoff-r32.py` archives the named revision into scratch, and `run-receipt.py` is itself a clone-based launcher; its nested target receives the real lane as its lane argument. These are source-defined modes, not claims that those nested tools ran from the working tree. The `/fast/scratch/hyaku` path was present, so `run-receipt` was confined with a private mount namespace binding that path to mktemp scratch, then ran as the invoking uid. No lane production files or external substrates were changed.

## Files and checks

Seat artifacts are limited to this seat directory. No tool was installed or updated. No build, lint, test suite, or formatter was run; the requested read-only dev run was the only target execution. No blockers.
