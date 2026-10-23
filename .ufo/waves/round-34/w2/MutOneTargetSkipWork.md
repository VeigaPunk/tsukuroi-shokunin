# Round 34 w2 — MutOneTargetSkipWork (after-mutant, C1 kill check)

KILLED — the variant DOES NOT MEET the C1 after-value: leaking 2 of 27 pairs, harness_errors empty, exit 1. Scored once with the frozen probe (sha256 5d0d5689…, VERSION 6, tool revision 3457f287) on variant f4a10945. Separately, the mutant as specified keeps the allow-list. In an ordinary untraced run, no ambient name or value reaches its git child, so it is not a leak and the kill rule is not in play.

## Mutant

In `tools/check-btrfs-space-r30.py`, on top of the lane tip 879daa95b898b5c624c609eced31f7d0d5b933e8 in the sandbox clone `/fast/scratch/hyaku/tsukuroi-r34/MutOneTargetSkipWork/repo`, one commit f4a10945caf2a8ff49ad260918ba8601f947b3e5 (branch `mut-one-target-skip-work`) inserts nine lines after line 385 of `main()`. The `--revision` branch keeps its one `git rev-parse --verify REV^{commit}` child (lines 380-381). It then prints the ten `{"id": "Dnn", "verified": true, "failures": []}` lines and the summary line (the rev-parse hash, 10 of 10, its own sha256, counter_version 2) and returns 0. No `ls-tree` or `show` child is reached. `clean_env()` (lines 95-98, the landed allow-list) is unchanged. Patch: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/MutOneTargetSkipWork/mut-one-target-skip-work-f4a10945.patch` (sha256 c464cbe76f40d5ffcce664831a9c56e7b839546ee68a6beab39d33e3e3986aa3).

Expected detector: amendment 1's base parity (`base_parity()` at probe `tools/probe-child-env-allowlist-r34.py@3457f287:398-405`, keys rc, stdout_sha256, git_execs, git_argv_sha256), firing on the git-exec count and the git-argv multiset. Exit code and normalised stdout match the base by construction.

## Findings

1. [obs] The variant's single score is a full claim set, scored once (wall time 95 s), receipt `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/MutOneTargetSkipWork/mut-one-target-skip-work-f4a10945.jsonl` (sha256 22ed0bb88b760dd7e5112d8615eb86ca138e8d0352e2b92f94d5d5d3fe4c30cf). Header line 1: revision f4a10945, tool_revision 3457f287, tool_sha256 5d0d568901c0eeb1c301b3bf825a839d4f41af68bc51e4de40f0706f15d1aa92. Summary at line 29: `pairs` 27, `leaking` 2, `leaking_pairs` [`tools/check-btrfs-space-r30.py:names`, `tools/check-btrfs-space-r30.py:quiet`], `harness_errors` [], `probe_sha256` 5d0d5689…, `probe_version` 6, `predicate_label` `leaking`. Footer at line 30: `exit_code` 1, `timed_out` false. Verdict: KILLED.

2. [obs] On the names and quiet pairs of the receipt (lines 8 and 9), only base parity fired. The evidence reads `base parity: git_execs 1 differs from claim-base control 35` and `base parity: git_argv_sha256 758302457ef878bf… differs from claim-base control abd125dcf346032a…`. Nothing else fired on either pair:
   - names: `reached` {} and `values_reached` {}.
   - Value channel: `anyname_values_reached` [], with `execveat` 0 and `unparsed_exec_records` 0.
   - Kept git settings: `git_missing_kept` 0. The one git child carries GIT_CONFIG_NOSYSTEM=1 and GIT_CONFIG_GLOBAL=/dev/null.
   - Run parity: `parity_diffs` [], with control A at 1 git exec and each channel run at 1.
   - `channel_rc` is 0 and `bashenv_log_exists` is false.

   The rc and stdout keys of base parity did not fire. The mutant's `channel_stdout_sha256` 0107930bf41b1572f629cd74b290ca6418f53f0d50d6f6af03611d5ed6453b0e equals the real tool's in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/after/c1-after-df661507.jsonl:8-9`.

3. [obs] Source finding: the source pair of the receipt (line 10) has 0 findings, scanned [`tools/check-btrfs-space-r30.py`], and does not leak. The other eight targets' 24 pairs show no evidence. Their control git exec counts are boot-chain 75, btrfs-repair-r31 28, locator-clarification 59, recheck-commands 953, section-citations 95, seat-scope 123, source-scope-correction 48 and measure-update-recheck 75.

4. [obs] The pristine and restored baselines pass, so the kill is real and not caused by a failing baseline. After the clone was restored to 879daa95, the same command form scored it once: receipt `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/MutOneTargetSkipWork/pristine-restored-879daa95.jsonl` (sha256 92aefee62341b2d06f093ad1bd145651315ade268d266927da63dffeaec1df7b). At line 29 it reads `leaking` 0 of `pairs` 27 with `harness_errors` []. Line 30 has `exit_code` 0. Lines 8-9 give check-btrfs-space-r30 control git_execs 35, `base_parity_diffs` [] and the same stdout digest 0107930b….

5. [obs] Restoration evidence:
   - Target file sha256: pristine 3539c41dd71a094b336dabdaa8b70281537ee29f50236c0a5e10daf7666740d1 (blob f8eb9a2a724d9fbb8e1e909b1517be5d8646d5f3). Mutant ea369aae0597e1630b36760dc9d5d94fd274fe9079f11636ea5af91b52a9b2b7 (blob 67e61ec60cc8bd9acbfb0e2928cd443b738f55cf).
   - After `git checkout -q --detach 879daa95…` in the clone: HEAD is 879daa95, `git status --short` prints 0 lines, and the working-tree file hashes back to 3539c41d…. That equals the lane's own blob at 879daa95, per `git -C <lane> rev-parse 879daa95:tools/check-btrfs-space-r30.py` → f8eb9a2a….
   - The lane was never written: lane HEAD is 879daa95 and `git -C <lane> status --short -- tools/` prints 0 lines.

6. [obs] Ordinary-run check: no ambient path reaches the mutant's child. Results are in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/MutOneTargetSkipWork/ordinary-run-check.json` (sha256 48531a39db75a103131cf2ea171697d31504eee0952a5fabbcb42871c7a88c7d). The harness is copied under `.../MutOneTargetSkipWork/harness/`.
   - Command: `timeout 900 python3 /fast/scratch/hyaku/tsukuroi-r34/MutOneTargetSkipWork/ordinary_check.py <json>`, exit 0.
   - Setup: each of three byte sets of the one target runs with `ZZ_R34_AMBIENT=1` in the ambient environment and `--revision f4a10945… --lane <clone>`. Run P is plain, with a `git` wrapper first on the ambient PATH; the wrapper records argv, the `ZZ_R34_AMBIENT` line and the env names. Run H uses a `sys.addaudithook` `subprocess.Popen` observer, which records the exact env mapping handed to each child.
   - Untraced: every run has `TracerPid: 0`.

   Results:
   - **Claim-base bytes `2641591e`** (ambient copy, the method's positive control): rc 0. 35 git children, and all 35 carry `ZZ_R34_AMBIENT=1`. The wrapper ran 35 times through the ambient PATH; the hook saw 261 names.
   - **Pristine tip `879daa95`:** rc 0. 35 children, 0 carry it. The child env names are exactly `GIT_CONFIG_GLOBAL GIT_CONFIG_NOSYSTEM GIT_OPTIONAL_LOCKS LC_ALL PATH`, and the wrapper ran 0 times.
   - **Mutant `f4a10945`:** rc 0. 1 child (`git -C <clone> rev-parse --verify f4a10945…^{commit}`), and 0 carry it. The env has the same five fixed names, and the wrapper ran 0 times.
   - All three byte sets print the same normalised stdout, sha256 0107930b….

7. [inf] The mutant as specified does not keep an ambient path, so it is not a "real leak". The item asked for an ordinary-run check showing an ambient name reaching a child, but the item's own wording "keep the allow-list" rules that out, and finding 6 shows it does not happen. The kill rule (SCORECARD amendment 2) applies only to a variant that keeps an ambient path, so this probe neither tests nor can trigger it. What it does test is hyaku addendum §9: a single-target skip-work replay cannot reach the after-value under these bytes. The counter refused it. I built no second variant to add a leak, because the contract allows scoring the variant once.

8. [inf] Only amendment 1's base parity refused this mutant. The replay matched the claim base on exit code and normalised stdout. Run parity against control A cannot see it, because the mutant sets its own control baseline (`parity()` at probe :390-395). Either of the two base-parity keys that fired (git_execs, git_argv_sha256) would kill it alone. Under the declaration bytes, which lack base parity, nothing in the predicate text would have fired, consistent with R1DummyBothBytes reading 0 of 27 there (SCORECARD amendment 1 disclosure).

9. [inf, not built, not scored] A coverage note for the skip-work family, not a finding against C1. A replay that still issued the identical multiset of 35 git argv and discarded the outputs would match all four base-parity keys at this revision. It would keep the allow-list, so it is outside the C1 kill rule. It bears only on §9.

Scope: read=round-34 declaration and pre-data amendments 1-2 (SCORECARD at 6de666c4 and 3457f287), C1 diff 3457f287..df661507 for check-btrfs-space-r30, the target at 879daa95, frozen probe bytes at 3457f287 (parity, base_parity, one_run, main), run-receipt.py header, after receipt c1-after-df661507.jsonl; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/MutOneTargetSkipWork.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/MutOneTargetSkipWork/{mut-one-target-skip-work-f4a10945.jsonl, mut-one-target-skip-work-f4a10945.patch, pristine-restored-879daa95.jsonl, ordinary-run-check.json, harness/ordinary_check.py, harness/hookrun.py, harness/git-wrapper.sh}, /fast/scratch/hyaku/tsukuroi-r34/MutOneTargetSkipWork/{repo (sandbox clone; commit f4a10945 on branch mut-one-target-skip-work; restored to detached 879daa95), probe-3457f287.py, wrapbin/git, hookrun.py, ordinary_check.py, ordinary/}; executed=git clone --no-local/checkout/commit/diff --output in the sandbox clone only; read-only git show/diff/rev-parse/status in the lane; timeout 300 python3 tools/check-btrfs-space-r30.py --revision 879daa95 --lane <clone> (exit 0); timeout 3000 python3 tools/run-receipt.py … --revision f4a10945 … -- tools/probe-child-env-allowlist-r34.py --revision '{rev}' --lane '{lane}' (exit 1, the single variant score); the same at --revision 879daa95 (exit 0, pristine/restored baseline); timeout 900 python3 ordinary_check.py (exit 0); no process left running
Model: anthropic/claude-opus-5-5
Installs: none
