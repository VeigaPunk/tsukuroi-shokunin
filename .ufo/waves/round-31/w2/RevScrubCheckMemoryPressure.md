# Round 31 wave 2 — RevScrubCheckMemoryPressure (C2 review of tools/check-memory-pressure.py)

Verdict: **holds**. The C2 fix in tools/check-memory-pressure.py is a single-line environment-builder change that drops GIT_/LD_/PYTHON names in every spawn site, the frozen probe reports leaking 0 on all three channels, the probe argv (--selftest) is byte-identical in exit code and stdout between 8cff9e7c and f3a5723a, and no hollow fix (output replay, early exit, or skipped work) was found.

## Findings

1. [obs] The diff between 8cff9e7c and f3a5723a988bf1c2835985880e7a38d477462cd0 for tools/check-memory-pressure.py is exactly one hunk, one line: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff 8cff9e7c f3a5723a988bf1c2835985880e7a38d477462cd0 -- tools/check-memory-pressure.py` shows `-           if not key.startswith('GIT_')}` replaced by `+           if not key.startswith(('GIT_', 'LD_', 'PYTHON'))}` at line 107 of the file (read of /fast/scratch/hyaku/tsukuroi-r31/RevScrubCheckMemoryPressure/repo/tools/check-memory-pressure.py:106-107). The parent process environment is filtered by prefix, so LD_PRELOAD, LD_LIBRARY_PATH, PYTHONPATH, GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE and every other GIT_* name cannot reach the git children.

2. [obs] Every subprocess spawn site in tools/check-memory-pressure.py passes an environment built by git_env() (lines 103-120), which applies that filter and then sets the round-30 contract keys GIT_CONFIG_NOSYSTEM=1, GIT_CONFIG_GLOBAL=/dev/null, GIT_CONFIG_SYSTEM=/dev/null, GIT_CEILING_DIRECTORIES, GIT_OPTIONAL_LOCKS=0, GIT_PAGER=cat, LC_ALL=C, HOME, XDG_CONFIG_HOME and PATH=/usr/bin:/bin. The spawn sites, found by grep for subprocess/Popen/os.system/os.popen/execv/spawn/check_output/getoutput (hits only at the lines below), are:
   - git_reader: `subprocess.run(['git', '--no-pager', '-C', repo, 'show', ...], env=git_env(tmp))` (lines 142-144);
   - run_fixture: `subprocess.run(['git', 'init', ...], env=env)`, `git add -A`, `git commit`, `git rev-parse HEAD` (lines 905, 910-913, 914-915) where `env = git_env(tmp)` (line 904);
   - revision_bind (lines 123-131): temporarily replaces `_revision.clean_env` with `lambda: dict(env)` where `env = git_env(tmp)` before calling `_revision.bind`, so every git child spawned by `_revision._git` (tools/_revision.py lines 72-74) and `_revision.validate_branch` (tools/_revision.py lines 90-92) during the --revision path inherits the same filtered contract environment. No other subprocess call exists in the file (grep confirmed); e.g. pointer_findings runs no process.

3. [obs] Frozen probe at tip, only this tool: `python3 tools/probe-git-child-env-r31.py --revision f3a5723a988bf1c2835985880e7a38d477462cd0 --lane /fast/scratch/hyaku/tsukuroi-r31/RevScrubCheckMemoryPressure/repo --only check-memory-pressure.py` exited 0 and printed:
   - loader-env: {"control_rc": 0, "control_git_execs": 390, "channel_rc": 0, "git_execs": 390, "evidence": [], "leak": false}
   - child-contract: {"control_rc": 0, "control_git_execs": 390, "evidence": [], "leak": false}
   - dotgit-pointer: {"control_rc": 0, "control_git_execs": 390, "channel_rc": 0, "git_execs": 390, "evidence": [], "leak": false}
   - summary: {"targets": 1, "pairs": 3, "leaking": 0, "leaking_pairs": [], "harness_errors": [], "probe_sha256": "b168b9b86cc125e5207cd359a37e6d7dad6fc2b1d1c601836ddbe4cc7a68d8b0", "scratch": "/fast/scratch/hyaku/git-child-env-046r700g"}
   The probe file sha256 matches the frozen b168b9b8… prefix. 390 git children ran per control; all 390 carried the full contract (no missing key in any envp), none of the descendant execs carried the injected LD_PRELOAD/LD_LIBRARY_PATH/PYTHONPATH paths, and the dotgit-pointer canary fingerprint did not change (no spurious verdict this run, so no re-run was needed).

4. [obs] Probe-argv parity across revisions. TARGETS argv for this tool is `['--selftest']`. Runs from the two sandboxes:
   - tip f3a5723a: `python3 tools/check-memory-pressure.py --selftest` → exit 0, stderr empty, stdout sha256 dcb09f8dd7bf619190c31c4f9b3759129b204cacd4ee73ead5eee8a63fb32b9e (file /fast/scratch/hyaku/tsukuroi-r31/RevScrubCheckMemoryPressure/selftest-tip.out);
   - base 8cff9e7c: same command in /fast/scratch/hyaku/tsukuroi-r31/RevScrubCheckMemoryPressure/repo-base → exit 0, stderr empty, stdout sha256 dcb09f8dd7bf619190c31c4f9b3759129b204cacd4ee73ead5eee8a63fb32b9e (selftest-base.out).
   The two stdout streams are byte-identical, so no normalization (40/64-hex or scratch paths) was required; exit codes and normalized stdout match, i.e. the fix is behavior-neutral.

5. [obs] No hollow fix. The output is a live 41-case selftest JSON (`{"cases": 41, "failed": 0, ...}` in selftest-tip.out) rather than replayed bytes; the probe observed 390 real git child execs per run under strace (control and channel runs agree on git_execs), so no early exit or skipped work occurred; the diff adds no exit path, no guard, and no output replay code. The only change is the env filter, and its observable effect is exactly what the loader-env channel verified.

## Residual risk and verification gaps

1. [unk] The frozen probe drives the tool's `--selftest` mode (its TARGETS argv), not the `--revision` mode. The `--revision` path is covered only by static inspection of revision_bind's clean_env patch and `_revision._git`/`validate_branch` (finding 2); it was not executed end-to-end in this review. No evidence of a leak there: the patch wraps every git call during bind.
2. [inf] The probe's parity and leak evidence covers 390 git children per run; the dotgit-pointer channel produced no spurious "canary fingerprint changed" verdict, so the known wave-1 flake did not recur here.
3. [inf] Nothing actionable remains in scope: no spawn site lacks the filtered contract environment, no channel leaks, behavior is unchanged across the revision pair.

Scope: read=tools/check-memory-pressure.py (full, grep for spawn sites), tools/_revision.py (grep, key bodies), tools/probe-git-child-env-r31.py (TARGETS, one_run, main), git diff of the two revisions for the file, selftest outputs at both revisions, probe output; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w2/RevScrubCheckMemoryPressure.md (this report); executed=git diff (read-only), git clone/checkout in /fast/scratch/hyaku/tsukuroi-r31/RevScrubCheckMemoryPressure/ (read-only git in sandboxes), python3 tools/check-memory-pressure.py --selftest at both revisions, python3 tools/probe-git-child-env-r31.py (--only check-memory-pressure.py).
Model: not exposed
Installs: none
