Verdict: none of the nine C1 claim targets still copy the ambient environment (0 hits); 11 other `tools/*.py` builders at 879daa95 still do, including both files the declaration's "13" missed.

Command (full stdout, no truncation): `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin grep -n -E 'os\.environ|environ\b|getenv' 879daa95b898b5c624c609eced31f7d0d5b933e8 -- tools/`
Output count: 34 lines, 11 files. Raw stdout: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/ScoutRemainingAmbient/grep-879daa95.txt` (34 lines, `wc -l`). HEAD is `879daa95b898b5c624c609eced31f7d0d5b933e8` and `git diff --stat` of the cited `tools/` files against that commit is empty, so path:line below is that blob.

Nine claim targets, second grep restricted to those nine paths, exit 1, empty: `check-boot-chain.py`, `check-btrfs-repair-r31.py`, `check-btrfs-space-r30.py`, `check-locator-clarification.py`, `check-recheck-commands.py`, `check-section-citations.py`, `check-seat-scope.py`, `check-source-scope-correction.py`, `measure-update-recheck.py`. Each former copy site is now a fixed dict (`PATH` plus `GIT_CONFIG_*`), commented "round-34 C1: fixed allow-list, no ambient copy": `tools/check-boot-chain.py:802`, `tools/check-btrfs-repair-r31.py:108`, `tools/check-btrfs-space-r30.py:96`, `tools/check-locator-clarification.py:448` and `:577`, `tools/check-recheck-commands.py:799`, `tools/check-section-citations.py:406` and `:568`, `tools/check-seat-scope.py:174`, `tools/check-source-scope-correction.py:355`, `tools/measure-update-recheck.py:438` and `:485`. [obs]

Declaration naming. `SCORECARD.md:1427` at `6de666c4` says a full sweep found "(13 files)" and that the four exclusions are in the probe docstring. The probe at `tools/probe-child-env-allowlist-r34.py:8-16` (same sentence at `6de666c4:10-11`) names the nine above plus four exclusions: `probe-git-env-leak`, `check-report-receipts`, `check-revision-binding`, `mutants-btrfs-space-r30`. [obs] That those 9+4 are the "13" is the only reading that adds up; SCORECARD does not list thirteen paths. [inf] It does not name `tools/run-receipt.py` or `tools/probe-git-env-residual-r30.py`. Wave-1 `/.ufo/waves/round-34/w1/RevProbeR34Diff.md:53-60` already reported those two missed. [obs]

1. Remaining builders that still copy `os.environ.items()` into a child. None is a claim target. [obs]

Named by the declaration (the four exclusions), still present at the same lines:

- `tools/check-report-receipts.py:311` copies ambient minus `GIT_*` and passes it to `git` (`:324-328`, `env=env`). Named exclusion ("starts no git child" was the probe control of `--selftest`, not this function).
- `tools/check-revision-binding.py:104` `clean_env()` copies ambient minus `GIT_*`; `git()` at `:110-115` passes `env=clean_env()` to `git`.
- `tools/mutants-btrfs-space-r30.py:362` copies ambient minus `GIT_*` into a Python child (`sys.executable` plus the counter, `:363`), not `git`.
- `tools/probe-git-env-leak.py:58` `clean_env()` copies ambient minus `GIT_*`; `run()` at `:63-64` defaults `env=clean_env()` for `git` children (`:70-71`, `:86`).

Not named (wave-1 misses), still present, still git children:

- `tools/run-receipt.py:39` `env()` copies ambient minus `GIT_*`. Passed to `git` at `:51-52`, `:80-86` and to the scored tool at `:102` (`subprocess.run(argv, ..., env=env(home))`).
- `tools/probe-git-env-residual-r30.py:75` `probe_env()` copies ambient minus `GIT_*`. `git()` at `:85-86` feeds `make_canary_repo` (`:112-119`) and `fingerprint` (`:92-93`); `export_tree` calls it at `:148`.

Not the declared "minus `GIT_*`" shape, still an ambient copy into a child, not named as one of the 13:

- `tools/probe-child-env-allowlist-r32.py:111`, `tools/probe-child-env-allowlist-r33.py:184`, `tools/probe-child-env-allowlist-r34.py:240`, `tools/probe-git-child-env-r31.py:88`: `hermetic_env` keeps every ambient name except `GIT_*`, `LD_*` and `PYTHON*`, then overwrites `PATH`, `LC_ALL`, `HOME`, `XDG_CONFIG_HOME`, `TMPDIR`. The r34 copy (the frozen counter) is passed to plumbing `git` at `:255` and to the target process in `one_run` at `:353` and `:361`. The r31 and r32 copies are used the same way (`probe-git-child-env-r31.py:103` and `:216-224`).
- `tools/score-census-handoff-r32.py:786` copies ambient minus `TSUKUROI_*` only (so `GIT_*`, `HOME`, `PATH` and the rest stay) and `run_census` at `:489-490` passes that dict to `/usr/bin/bash`.

2. The other 23 of the 34 hits are not child-env builders. [obs] Docstring or predicate text: `probe-child-env-allowlist-r32.py:7`; `probe-child-env-allowlist-r33.py:47`, `:48`, `:52`, `:53`, `:81`, `:157`; `probe-child-env-allowlist-r34.py:10`, `:67`, `:68`, `:72`, `:73`, `:101`, `:212`. Scan-rule constants: r33 `:455`, `:456`, `:468`; r34 `:552`, `:553`, `:565`. `set(os.environ)` used only to avoid injected names, not as a child environment: r32 `:391`, r33 `:832`, r34 `:945` (each also calls `hermetic_env('/h','/t')` and keeps only the key set).

3. Of the declaration's 13, the nine claim-target copies are gone and the four named exclusions remain. The two files wave-1 said the "13" missed (`run-receipt.py:39`, `probe-git-env-residual-r30.py:75`) still hand ambient-minus-`GIT_*` to git children at this tip. No third `GIT_*`-only comprehension showed up in this grep. [obs] This sweep did not run any tool, so it does not show whether an ambient name reaches a child in an untraced process. [unk]

Scope: read=<SCORECARD.md round-34 declaration at 6de666c4; tools/probe-child-env-allowlist-r34.py header and each grep hit's function at 879daa95; .ufo/waves/round-34/w1/RevProbeR34Diff.md:26-68; allow-list lines in the nine claim targets at 879daa95>; wrote=</home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/ScoutRemainingAmbient.md, .../ScoutRemainingAmbient/grep-879daa95.txt, .../ScoutRemainingAmbient/hit-context.txt>; executed=<read-only git grep/show/diff/rev-parse at 879daa95 and 6de666c4; python extract of hit windows; no probe, no receipt, no git write>
Model: xai-oauth/grok-4.7-build-fast
Installs: none
