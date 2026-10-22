Verdict: partly holds. Every leak in the C2 before receipt is real, and the declared after-value (0 of 33, no harness errors) can be reached by a genuine fix. But the probe also reports 0 for two hollow fixes, misses one real leak and one enclosing-repository write, measures only the `--selftest` path for 7 of the 11 targets, and its control environment inherits the caller's PATH.

Seat: TsukuroiR30.CritProbeDesign. Revision attacked: 8976ca92ec3c2e6a2aef07b7065a24ff84a1291b. The probe was run unmodified (sha256 c8f61996f0cea828c9b88f509a29bb6e09fc6de23ccd2b7f4084efb0d84cb68c, the same as `probe_sha256` in the receipt). The sandbox clone is /fast/scratch/hyaku/tsukuroi-r30/CritProbeDesign/repo. All harness files and outputs are in /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w1/CritProbeDesign/.

## Findings

1. [obs] The ignore file alone causes every exit-code leak in the user-files channel. Hooks, attributes and identity cause none of them. The harness `CritProbeDesign/ablate.py` runs each target under the probe's control environment and then under each user-files ingredient on its own, with an rc-logging git wrapper first on PATH in every variant. Outputs are in `ablate-out.jsonl`, `ablate2-out.jsonl` and `ablate3-out.jsonl`. The 6 targets that leak by exit code (check-kernel-taint, check-adjacency-overlap, check-memory-pressure, check-registry-coverage, check-storage-health, mutants-kernel-taint) show this pattern:
   - Variants `ignore`, `ignore+identity` and `full` give rc 1.
   - Variants `hooks`, `attrs` and `identity` give rc 0, with stdout byte-equal to control.

   Identity is never a factor. Every target passes an explicit identity: `-c user.name=…` on the command line, or a repo-local `git config user.*` in mutants-kernel-taint.py:95-96. Adding an identity to the user files changes nothing, since `ignore+identity` gives the same result as `ignore`.

2. [obs] First reproduced user-files leak: check-kernel-taint. The git command that diverges is call #2 in `ablate-out.jsonl` line 2:
   - Command: `git -C <TMPDIR>/tsukuroi-sh-st-*/repo -c user.name=selftest -c user.email=selftest@invalid -c commit.gpgsign=false commit --quiet -m fixture`, which returns rc 1 instead of the control's 0.
   - Source: tools/check-kernel-taint.py:992-994 (`check=True`).
   - Cause: `git add -A` succeeds but stages nothing, because the user's ignore file pattern `*` matches the fixture files.
   - Standalone reproduction (in /fast/scratch/hyaku/tsukuroi-r30/CritProbeDesign/hs/repro): `add rc=0`, then commit prints "nothing to commit (create/copy files and use "git add" to track)" with `commit rc=1`. `git check-ignore -v f` prints `…/hs/h1/.config/git/ignore:1:*	f`.
   - This happens even though `GIT_CONFIG_GLOBAL=/dev/null` is set. `man git-config` (line 2418-2421) says core.excludesFile "Defaults to $XDG_CON…", so the XDG ignore and attributes files are read without any config file pointing at them.
   - The same blind spot appears in two existing helpers that claim global config is ignored: `tools/_revision.py:62-66` (`clean_env`) and tools/mutants-kernel-taint.py:32-36 ("global and system git config (hooks, templates) ignored").

3. [obs] Second reproduced user-files leak: mutants-kernel-taint. The diverging call is #7: `git -C <TMPDIR>/mut-kt-*/repo commit -q -m base export 8976ca92…`, rc 1 versus 0 (`ablate-out.jsonl`, `mutants-kernel-taint.py` `ignore` row). Only 8 git calls run, against 609 in control. The tool aborts before running any mutant.

4. [obs] Path-wrapper leak, reproduced on check-freshness-r17. All 113 of its git calls resolve `git` through PATH. The first is `git --no-pager -C <TMPDIR>/freshness-r17-*/ init -q -b master` (from `abl/ablate-*/check-freshness-r17.py-control/git-calls.log` line 1, which matches the receipt's `log_head`). No exit code diverges in this channel: the leak is that the wrapper ran at all, because the probe's wrapper just re-executes /usr/bin/git.
   - [obs] This is a live hazard on this host. The caller's PATH has 18 user-writable entries ahead of /usr/bin (fnm_multishells, ~/.local/bin, mise shims and others), seen in `env` output.

5. [obs] The probe misses a real leak (a false negative). Under the ignore file, mutants-owed-statements-r29-landed silently hollows its own shape N19 ("path:LINE at a file fabricated in the same commit (notes/trust-me.md:1)"):
   - The commit succeeds without the new file.
   - `git -C …/repo show <N19>:notes/trust-me.md` then exits 128, where control exits 0 (`abl2/ablate-*/mutants-owed-statements-r29-landed.py-{ignore,control}/git-calls.log` line 708).
   - The verdict is still "refused", the exit code is still 0, and stdout is identical to control after normalizing 40-hex SHAs and scratch paths.
   - So the receipt's "no leak" on `mutants-owed-statements-r29-landed.py:user-files` is wrong. [inf] Shape N19 is refused for a different reason than the one it was designed to test.

6. [obs] The probe gives 0 for hollow fixes. It compares only exit codes and the canary log (probe lines 239-251); it never compares stdout with control. Both hollow mutants were committed in the sandbox and run through the unmodified probe:
   - `hollow-swallow` (`mut-hollow-swallow.diff`, commit 292ab7e4): check-kernel-taint sets `os.environ['PATH']='/usr/bin:/bin'` and wraps `main()` in `except BaseException: pass; sys.exit(0)`. Probe result: `pairs 3, leaking 0, harness_errors []`, exit 0 (`probe-hollow-swallow.jsonl`). Its selftest still fails internally under the user's files: the base tool with the same HOME gives rc 1 and 21767 stdout bytes, against 8706 in control (`hs/kt-h1.out`).
   - `hollow-skip` (`mut-hollow-skip.diff`, commit ba5e5646): check-storage-health exits 0 without running anything when HOME contains more than `.config`, or when `which git` is not /usr/bin/git. Probe result: `leaking 0`, exit 0 (`probe-hollow-skip.jsonl`). Direct run: control gives rc 0 with 6859 bytes, user-files gives rc 0 with 0 bytes.
   - Comparing stdout digests between control and channel would catch both mutants. [inf] A tool that replays its control stdout cannot be caught by any black-box probe; only a diff review can catch that.

7. [obs] The probe measures only the selftest path for 7 of the 11 targets. Mutant `genuine-selftest-only` (`mut-genuine-selftest-only.diff`, commit c38b058d) applies the round-30 contract environment only inside check-kernel-taint's `run_fixture` and its fixture `GitReader`. Its production `--revision` path still uses `_revision.clean_env()`, which inherits PATH and HOME. The probe reports `leaking 0` of 3 (`probe-genuine-selftest-only.jsonl`).
   - So a lane can reach 0 of 33 while the 6 selftest-only check tools (not the mutants batteries) still follow all three channels in real runs.
   - [obs] `_revision.clean_env` is shared with about 30 tools outside the eleven (`grep -ln clean_env tools/*.py`). Fixing it there breaks the declared separability "C2 changes only the eleven target tools" (SCORECARD.md:1151). Fixing it inside each tool creates eleven copies of the git environment rule.

8. [obs] The enclosing-repo channel can fail, but it has two blind spots:
   - **It can fire.** Mutant `encl-ref` (commit 9d94607a) adds an unchecked `git -C $TMPDIR update-ref refs/heads/leak HEAD`. The probe reports `canary fingerprint changed`, leaking 1, exit 1 (`probe-encl-ref.jsonl`).
   - **Config writes are invisible.** Mutant `encl-config` (commit 24a93845) runs `git -C $TMPDIR config core.hooksPath /dev/null/leak`, which persistently sets a hooks path in the enclosing repository. The probe reports leaking 0 (`probe-encl-config.jsonl`). The fingerprint (probe lines 89-103) covers only HEAD, refs, the object and ref file names, index and packed-refs; it does not cover `.git/config`, `hooks/`, `info/` or `logs/`.
   - **Two targets are out of reach.** Both owed-statements batteries hard-code `/fast/scratch/hyaku` as their temp parent and ignore TMPDIR (tools/mutants-owed-statements-r29.py:35-36, tools/mutants-owed-statements-r29-landed.py:36-37). Their sandbox therefore never sits inside the canary, and 2 of the 11 enclosing-repo pairs cannot fail.
   - **Why the other 8 read 0.** [inf] They all `git init` or clone a fresh repository before writing, so git's repository discovery stops at the nested `.git`. The 0 of 10 before-value is consistent with those tools really being safe in this channel. It does not show the channel is broken, but the channel is weak.

9. [obs] The control environment is not fully hermetic (probe lines 74-78 and 157):
   - **PATH is inherited.** It is the caller's PATH, including per-shell fnm directories, so it differs between sessions.
   - **Other inherited variables.** LANG is inherited, but `LC_ALL=C` overrides it. XDG_CACHE/DATA/STATE/RUNTIME and PYTHON* are also inherited; git does not read those XDG variables for config.
   - **Shared state.** One HOME and one TMPDIR are shared by every target's control run and by its path-wrapper and user-files runs, so a tool that writes into HOME or TMPDIR contaminates later runs.
   - **System config is untested.** `GIT_CONFIG_NOSYSTEM=1` is set in the control, so the system-config channel is never exercised. [obs] /etc/gitconfig is absent on this host.
   - HOME and XDG_CONFIG_HOME are private and empty, as declared.

10. [obs] The before-value undercounts. Mutant `selfassess-dispatch` (`mut-selfassess-dispatch.diff`, commit 1990e296) moves `--selftest` ahead of the `.git` check in tools/check-self-assessment.py:1075-1083. Its control then passes, and two more pairs leak (`probe-selfassess-dispatch.jsonl`):
    - path-wrapper: 312 log lines.
    - user-files: rc 1 against 0, plus a `pre-commit` hook line. The cause is the ignore file again: the fixture commit `… self-assessment-selftest-*/clean … commit -q -m fixture: clean` gets rc 1 (`ablate3-out.jsonl`). The tool's `-c core.excludesFile=/dev/null` (line 95-100) is on its read helper, not on the fixture commit. In the hooks-only variant, 38 hook lines fire.

    Counting these and finding 5, the measurable before-state is at least 20 real leaking pairs of 33. The receipt says 17 of 30.

11. [obs] The after-value is reachable without weakening the tools, at least for one target. The `genuine-selftest-only` mutant gives 0 of 3 with no harness error, and its control stdout is byte-identical to the base tool (`cmp hs/gen-h0.out hs/kt-h0.out` succeeds). [inf] Every target can reach 0 by applying the contract's HOME/XDG replacement, the `/usr/bin:/bin` PATH and the devnull config to every git child and to the `sys.executable` children that run git. For check-self-assessment this also needs the dispatch reorder, which is a behaviour change outside "otherwise byte-identical": `--selftest` in a non-repository no longer returns CANNOT_EVALUATE. That is the judge's call.

## Impacted axes
Operability (C2 integrity: hollow fixes pass, one leak missed, coverage is selftest-only) and calibration (the before-value undercounts, and the 0 of 10 enclosing-repo reading is low-power).

## Smallest safe correction
The probe is frozen at the declaration, so changing it is a re-declaration and the L1 decides. Until then, the judge can add:

1. **Stdout comparison.** Compare each channel's stdout digest with control, after normalizing 40-hex SHAs and scratch paths. `ablate2` shows this output is deterministic. This catches both hollow mutants.
2. **Wider fingerprint.** Add `.git/config`, `hooks/`, `info/` and `logs/` to the canary fingerprint. This catches `encl-config`.
3. **Hermetic control.** Set the control PATH to `/usr/bin:/bin`; the probe calls `sys.executable` by absolute path. Use a fresh HOME and TMPDIR per run.
4. **Diff review of the eleven tools:**
   - No new `except` clause around `main` or the selftest.
   - No change to exit or return paths.
   - No HOME, PATH or `which` sniffing.
   - Every git subprocess routes through one contract-environment builder per tool, including the non-selftest path.
   - No remaining `env=_revision.clean_env()` or `os.environ`-derived git environment.
5. **Scope of the claim.** Either state that the probe covers selftest paths only, or add one non-selftest invocation per check tool.

Scope: read=probe tools/probe-git-env-residual-r30.py, c2-before receipt, SCORECARD.md:1140-1152, target tool sources (git env and temp-dir sites), tools/_revision.py:62-87, man git-config; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w1/CritProbeDesign.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w1/CritProbeDesign/{ablate.py,ablate-out.jsonl,ablate2-out.jsonl,ablate3-out.jsonl,mut-*.diff,probe-*.jsonl}, sandbox under /fast/scratch/hyaku/tsukuroi-r30/CritProbeDesign/ (clone with 6 sandbox-only mutant commits, exports, ablation runs); executed=sandbox git clone/checkout/commit/archive with GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset, python3 ablate.py (3 runs), python3 probe.py --lane <sandbox clone> on 6 mutant revisions, direct selftest runs under crafted HOME, a standalone git init/add/commit/check-ignore repro; no git write in the lane or fleet repo
Model: not exposed
Installs: none
