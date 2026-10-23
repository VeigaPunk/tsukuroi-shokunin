# Round 31 wave 2 — RevScrubCheckFreshnessR17 (falsify seat)

**Verdict: holds.** The C2 fix in `tools/check-freshness-r17.py` (8cff9e7c → f3a5723a988bf1c2835985880e7a38d477462cd0) closes the loader-env leak for this tool with no hollow-fix signature: the frozen probe reads leaking 0 (before: leaking 1), every spawn site drops GIT_/LD_/PYTHON names while keeping the round-30 child contract, and the tool's behavior (exit code, normalised stdout, git work done) is unchanged between the two revisions.

## Findings

1. [obs] The patch is a single-line filter change in `git_env` (`tools/check-freshness-r17.py:329-330`): `if not key.startswith("GIT_")` → `if not key.startswith(("GIT_", "LD_", "PYTHON"))`. Nothing else in the file changed (`git diff 8cff9e7c f3a5723a… -- tools/check-freshness-r17.py` shows one hunk, +1/−1). The base blob is identical at 8cff9e7c and the declaration commit f4861f4d (blob d86a1605a0b887499998407855aa89592f414227 at both).

2. [obs] Spawn-site audit (every site that starts a subprocess in this tool):
   - `git_in` → `subprocess.run(["git", …], env=env)` (`tools/check-freshness-r17.py:360-362`), env from `git_env` + `GIT_OPTIONAL_LOCKS/GIT_PAGER/LC_ALL`.
   - `binding_sandbox.run` → delegates to `git_in` (line 499-500), same env.
   - `expect_cli` → `subprocess.run([sys.executable, tool, *args], cwd=root, env=git_env(env_tmp))` (`tools/check-freshness-r17.py:537-540`), the selftest Python child.
   - `_revision._git` → `subprocess.run(…, env=clean_env())` (`tools/_revision.py:72-74`); inside this tool every `_revision` call runs through `revision_call` (`tools/check-freshness-r17.py:342-351`), which replaces `clean_env` with `lambda: dict(env)` where `env` is the `git_env` dict; the default `_revision.clean_env` also drops `GIT_`/`LD_`/`PYTHON` and adds the contract (`tools/_revision.py:62-67`).
   - No other spawn sites: grep for `subprocess|Popen|os.system|os.popen|check_output|check_call|communicate|execv|spawn` hits only line 360 and 537; `os.environ` is read only at line 329 inside `git_env`.
   - `git_env` drops the three prefixes, then sets the round-30 contract explicitly: `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`, private `HOME`, `XDG_CONFIG_HOME`, `PATH=/usr/bin:/bin`, and a non-empty `GIT_CEILING_DIRECTORIES` (lines 331-339). No spawn site bypasses it. All four sites conform.

3. [obs] Frozen probe at the attacked revision (run from the sandbox clone, `--only check-freshness-r17.py`, probe sha256 b168b9b86cc125e5207cd359a37e6d7dad6fc2b1d1c601836ddbe4cc7a68d8b0 = declared):
   ```
   {"tool": "tools/check-freshness-r17.py", "channel": "loader-env", "argv": ["--selftest"], "control_rc": 0, "control_git_execs": 116, "channel_rc": 0, "git_execs": 116, "evidence": [], "leak": false}
   {"tool": "tools/check-freshness-r17.py", "channel": "child-contract", "argv": ["--selftest"], "control_rc": 0, "control_git_execs": 116, "evidence": [], "leak": false}
   {"tool": "tools/check-freshness-r17.py", "channel": "dotgit-pointer", "argv": ["--selftest"], "control_rc": 0, "control_git_execs": 116, "channel_rc": 0, "git_execs": 116, "evidence": [], "leak": false}
   {"revision": "f3a5723a988bf1c2835985880e7a38d477462cd0", "targets": 1, "channels": ["loader-env", "child-contract", "dotgit-pointer"], "pairs": 3, "leaking": 0, "leaking_pairs": [], "harness_errors": [], "probe_sha256": "b168b9b86cc125e5207cd359a37e6d7dad6fc2b1d1c601836ddbe4cc7a68d8b0", "scratch": "/fast/scratch/hyaku/git-child-env-4lb5fbkd"}
   ```
   Exit 0, leaking 0, no harness errors.

4. [obs] Same probe at the base 8cff9e7c (run from the base sandbox clone):
   ```
   {"tool": "tools/check-freshness-r17.py", "channel": "loader-env", "argv": ["--selftest"], "control_rc": 0, "control_git_execs": 116, "channel_rc": 0, "git_execs": 116, "sample": {"exec": "/usr/bin/git", "argv_head": ["git", "--no-pager", "-C", "/fast/scratch/hyaku/git-child-env-ny77xx7r/loader-env-1/tmp/freshness-r17-dqotv18d"]}, "evidence": ["124 descendant execs carry the injection path"], "leak": true}
   ```
   Summary: leaking 1 (loader-env), harness_errors [], exit 1. This reproduces the committed before-receipt at f4861f4d (`measure/c2-before-f4861f4d….jsonl`: same tool, same "124 descendant execs carry the injection path" sample, control_git_execs 116; 11 of 33 leaking overall). The integration after-receipt `measure/after-13ca52d0/c2-declared.jsonl` reads exit_code 0 with 0 of 33 leaking — our tip run agrees.

5. [obs] Tool-level before/after comparison (TARGETS argv `["--selftest"]` run directly under the probe's hermetic env: banned prefixes unset, PATH=/usr/bin:/bin, LC_ALL=C, private HOME/XDG_CONFIG_HOME/TMPDIR) — base 8cff9e7c and tip f3a5723a both exit 0 with byte-identical stdout `CHECK_FRESHNESS_R17_SELFTEST: PASS (59 cases, 59 passed, 0 failed)`. No hex/scratch strings appear in the output, so normalisation is moot; outputs are identical.

6. [obs] Hollow-fix check:
   - No output replay: stdout identical at base and tip (finding 5), and the channel runs at the tip match their control runs in exit code, normalised stdout digest and git exec count (all `evidence` arrays empty in finding 3 — the probe's parity gate compares exactly these three per `tools/probe-git-child-env-r31.py:36-42,240-245`).
   - No early exit / skipped work: control runs at both revisions start the same 116 git children (`control_git_execs` 116 at base and tip), i.e., the full selftest + binding-sandbox git work executes; the probe flags "control run started no git child" as a harness error, and none occurred. The selftest still runs its 59 cases.
   - The probe distinguishes hollow from genuine fixes: committed controls `measure/controls/c2/c2-H1.jsonl` (hollow exit-0-when-LD_PRELOAD-set) exits 1, `c2-H2.jsonl` (genuine drop) exits 0; our base/tip runs split the same way (1 vs 0).

## Residual risk and verification gaps

- [inf] The rule is a prefix filter `startswith(("GIT_", "LD_", "PYTHON"))`; it deliberately re-adds canonical GIT_* names (NOSYSTEM/GLOBAL/SYSTEM/CEILING/OPTIONAL_LOCKS/PAGER), which is the round-30 contract surface, not ambient injection. No ambient GIT_/LD_/PYTHON value can survive into children via `git_env` or `_revision.clean_env`.
- [unk] I reviewed only `tools/check-freshness-r17.py` (this seat's scope); the other ten C2 targets and the shared `_revision.py` change (also in the diff set) are covered by the 0-of-33 integration receipt, which my single-target run does not re-derive.
- [obs] No dotgit-pointer spurious "canary fingerprint changed" verdict appeared in either run (both dotgit-pointer pairs read leak false), so the wave-1 MutProbeC2 re-run caveat did not trigger.

Scope: read=git diff 8cff9e7c f3a5723a -- tools/check-freshness-r17.py; tools/check-freshness-r17.py and tools/_revision.py at f3a5723a and 8cff9e7c; tools/probe-git-child-env-r31.py (blob identical at both revisions, sha256 b168b9b8…); measure/c2-before-f4861f4d….jsonl, measure/after-13ca52d0/c2-declared.jsonl, measure/controls/c2/c2-H1.jsonl, c2-H2.jsonl; corpus/lessons/round-31.md, round-30-verifier-spotcheck.md. wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w2/RevScrubCheckFreshnessR17.md. executed=git clone/checkout (read-only sandbox clones at f3a5723a and 8cff9e7c); probe-git-child-env-r31.py --only check-freshness-r17.py at both revisions; check-freshness-r17.py --selftest at both revisions; sha256sum; grep/glob.

Model: not exposed

Installs: none
