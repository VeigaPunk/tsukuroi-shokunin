# RerunBeforeIndependent — round 34 wave 2, attack:rerun-before

**Verdict: the before tree DOES NOT MEET the C1 after-value, exactly as declared — leaking 27 of 27, harness_errors [], exit 1.** The frozen probe v6 rerun under a separate receipt reproduces the L1's before receipt pair for pair, so the C1 before value is independently confirmed and the after-value 0 of 27 is not an artifact of a one-off before run.

## Findings

1. [obs] **The rerun receipt binds the mandated command.** Header: `revision` `6de666c427ba9aa6b4350561980bde8d0e7c261d`, `tool_revision` `3457f287e04f34e73f8e70d4417b14b96f903f56`, `tool` `tools/probe-child-env-allowlist-r34.py`, `tool_sha256` `5d0d568901c0eeb1c301b3bf825a839d4f41af68bc51e4de40f0706f15d1aa92` (the frozen VERSION 6 bytes), argv `["--revision","6de666c4…","--lane","/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"]`. Footer: `exit_code` 1, `timed_out` false, `stderr_tail` `""`, finished 2026-10-23T09:18:58Z. Receipt `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/RerunBeforeIndependent/before-6de666c4.jsonl:1` and `:30`; sha256 `6e80176c95cc5fd3e3501f30d0e0353a30ad7f124878c0807e453f2201ba34c1`. Command: `cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin && timeout 3000 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 tools/run-receipt.py --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --revision 6de666c427ba9aa6b4350561980bde8d0e7c261d --tool-revision 3457f287e04f34e73f8e70d4417b14b96f903f56 --out …/before-6de666c4.jsonl --timeout 2900 -- tools/probe-child-env-allowlist-r34.py --revision '{rev}' --lane '{lane}'` — exit 1 (the probe's declared exit for a leaking pair), wall 114.65 s.

2. [obs] **The declaration commit carries the claim-base target bytes.** All nine target blobs are identical at `2641591e` and `6de666c4`; `git diff --name-only 2641591e 6de666c4 -- tools/` prints only `tools/probe-child-env-allowlist-r34.py`. Evidence: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/RerunBeforeIndependent/target-blob-identity.txt:1-17` (nine `same=yes` lines, e.g. `check-boot-chain.py base=81d331b8… decl=81d331b8… same=yes`; sha256 `ea7aae3dee25824f772734f12c212337c834b78e6d7972b9375f253a63df9c61`). Therefore this rerun measures the same nine tool files as the claim base, and its comparability with the L1's before receipt at `3457f287` (finding 6) is legitimate.

3. [obs] **Summary line.** `targets` 9, `channels` `["names","quiet","source"]`, `pairs` 27, `leaking` 27, `harness_errors` `[]`, `probe_version` 6, `target_set` `claim`, `base` `2641591e303057cd0f67e190a6bdf7fa91a45c31`, `predicate_label` `leaking`; `leaking_pairs` lists all 27 tool:channel pairs. Pointer: `before-6de666c4.jsonl:29`. Per-pair transcription: `before-6de666c4-per-pair.txt` (sha256 `7bee193152aef2291f88d1604800f06ada74783177e6cc39189ef0403b5b1dd6`).

4. [obs] **Per-pair clause attribution.** Columns: N = injected-name clause (reached/injected), V = exact value-channel `NAME=VALUE` (of 10), A = amendment-2 any-name run-unique value (child env strings), K = amendment-2 kept git settings missing/successful git execs, P = parity with control A, BP = base parity with the claim-base control, S = source findings (line).

| target | channel | N | V | A | K | P | BP | S |
|---|---|---|---|---|---|---|---|---|
| check-boot-chain | names | 12/12 | 10/10 | 42 | 18/75 | none | none | - |
| check-boot-chain | quiet | 8/8 | 10/10 | 36 | 18/75 | none | none | - |
| check-boot-chain | source | - | - | - | - | - | - | 1: 802 |
| check-btrfs-repair-r31 | names | 12/12 | 9/10 | 20 | 0/28 | none | none | - |
| check-btrfs-repair-r31 | quiet | 8/8 | 9/10 | 17 | 0/28 | none | none | - |
| check-btrfs-repair-r31 | source | - | - | - | - | - | - | 1: 108 |
| check-btrfs-space-r30 | names | 12/12 | 10/10 | 21 | 35/35 | none | none | - |
| check-btrfs-space-r30 | quiet | 8/8 | 10/10 | 18 | 35/35 | none | none | - |
| check-btrfs-space-r30 | source | - | - | - | - | - | - | 1: 96 |
| check-locator-clarification | names | 12/12 | 10/10 | 42 | 17/59 | none | none | - |
| check-locator-clarification | quiet | 8/8 | 10/10 | 36 | 17/59 | none | none | - |
| check-locator-clarification | source | - | - | - | - | - | - | 3: 381, 448, 577 |
| check-recheck-commands | names | 12/12 | 10/10 | 42 | 474/953 | none | none | - |
| check-recheck-commands | quiet | 8/8 | 10/10 | 36 | 474/953 | none | none | - |
| check-recheck-commands | source | - | - | - | - | - | - | 1: 799 |
| check-section-citations | names | 12/12 | 10/10 | 84 | 32/95 | none | none | - |
| check-section-citations | quiet | 8/8 | 10/10 | 72 | 32/95 | none | none | - |
| check-section-citations | source | - | - | - | - | - | - | 5: 790, 792, 406, 568, 797 |
| check-seat-scope | names | 12/12 | 10/10 | 63 | 35/123 | none | none | - |
| check-seat-scope | quiet | 8/8 | 10/10 | 54 | 35/123 | none | none | - |
| check-seat-scope | source | - | - | - | - | - | - | 2: 539, 174 |
| check-source-scope-correction | names | 12/12 | 10/10 | 63 | 12/48 | none | none | - |
| check-source-scope-correction | quiet | 8/8 | 10/10 | 54 | 12/48 | none | none | - |
| check-source-scope-correction | source | - | - | - | - | - | - | 2: 473, 355 |
| measure-update-recheck | names | 12/12 | 10/10 | 63 | 2/75 | none | none | - |
| measure-update-recheck | quiet | 8/8 | 10/10 | 54 | 2/75 | none | none | - |
| measure-update-recheck | source | - | - | - | - | - | - | 3: 537, 438, 485 |

   Clause reading:
   - The **name clause** fired on all 18 run pairs (12 of 12 injected names in every `names` run, 8 of 8 in every `quiet` run).
   - The **exact value-channel clause** fired on all 18 run pairs: 10 of 10 value names for 16 pairs, and 9 of 10 for `check-btrfs-repair-r31` in both runs (`PATH` is the one not carried).
   - The **amendment-2 any-name clause** fired on all 18 run pairs (17 to 84 child environment strings carrying a run-unique ambient value under some name) — e.g. `check-boot-chain.py` names run: 42 strings carrying `BASH_ENV, ENV, GCONV_PATH, HOME, LANG, …`; `before-6de666c4.jsonl:2`.
   - The **amendment-2 kept-settings clause** fired on 16 of 18 run pairs (8 of 9 targets; `check-btrfs-repair-r31` is 0/28 in both runs). E.g. `check-btrfs-space-r30`: 35 of 35 git children lack `GIT_CONFIG_NOSYSTEM=1` or `GIT_CONFIG_GLOBAL=/dev/null`; `check-recheck-commands`: 474 of 953.
   - **Parity** with control A was empty on all 18 run pairs; **base parity** with the claim-base control was empty on all 18. The amendment-1 clause therefore contributed nothing at the before tree — expected, because the target bytes equal the claim base — and did not produce the 27 of 27.
   - `execveat` 0 and unparsed exec records 0 on all 18 run pairs.
   - The **source channel** fired on all nine targets, each with the ambient read at its own builder line (`check-boot-chain.py:802`, `check-btrfs-repair-r31.py:108`, `check-btrfs-space-r30.py:96`, `check-locator-clarification.py:448` and `:577`, `check-recheck-commands.py:799`, `check-section-citations.py:406` and `:568`, `check-seat-scope.py:174`, `check-source-scope-correction.py:355`, `measure-update-recheck.py:438` and `:485`), plus hiding-construct or inheriting-spawn findings in five targets (`check-locator-clarification.py:381 getattr`, `check-section-citations.py:790,792,797 globals()`, `check-seat-scope.py:539 subprocess.run without env`, `check-source-scope-correction.py:473 subprocess.run without env`, `measure-update-recheck.py:537 subprocess.run without env`). The `ambient-read .environ` anchors match the base builders `{k: v for k, v in os.environ.items() if not k.startswith("GIT_")}` confirmed by read-only `git show 2641591e:tools/<name>.py` (e.g. `check-boot-chain.py:802`, `check-recheck-commands.py:799`, `measure-update-recheck.py:438,485`).

5. [obs] **Harness soundness.** `harness_errors` is `[]`, so for every target control runs A and B agreed on exit code, normalised stdout digest and successful-git count, A started at least one git child, and the claim-base control run exited 0. The 27 of 27 is therefore a target-behaviour reading, not a broken-harness reading (`before-6de666c4.jsonl:29`).

6. [obs] **Pair-for-pair agreement with the L1's before receipt at `3457f287`.** Comparing my 27 pair records with `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/after/c1-before-a2-3457f287.jsonl`: identical `leaking_pairs` set (27 names), identical clause family per pair (name-reach count 12/12 or 8/8, value-name set, any-name presence, kept-settings firing incl. the 0/28 repair exception, empty parity and base parity), identical successful-git counts per target (75, 28, 35, 59, 953, 95, 123, 48, 75 in both `names` and `quiet` runs), and footer `exit_code` 1. Only the per-run random injection names/values and scratch paths differ. Diff of the two receipts' pair records: 0 clause-family differences.

7. [inf] **What the rerun does and does not establish.** Because every run pair trips three independent run channels (name, exact value, any-name) and every target trips the source scan, a 0 of 27 at the after tree cannot be produced by an ambient-copy builder surviving in these nine files unseen by these channels; the after reading at `df661507` is therefore a real silence of the channels, not a detection gap of the before reading. What this rerun cannot see is anything outside the frozen probe: argv, file, pipe and fork-without-exec channels, and the named S181 read side — those remain outside the C1 claim by the declaration, and the wave-2 mutant seats carry them.

8. [inf] **Independence caveat.** This is a same-bytes rerun by a different seat through a fresh `run-receipt` sandbox clone (the probe ran from a private `--no-local` clone under `/fast/scratch/hyaku/run-receipt-*`, with every inherited `GIT_*` removed), not a differently-written counter. It rules out a one-off receipt and reproduces the declared direction, but it cannot expose a defect shared by the frozen probe bytes themselves; the wave-1 code-reading controls and wave-2 mutants carry that burden. Under hyaku addendum §9 the expected value here is not shortcut-reachable: it is the pre-registered before direction read by the frozen probe on fixed committed bytes, and a content-free output would have to fake the 27 per-pair evidence records the probe prints.

9. [unk] **Repetition bound.** One rerun cannot exclude load-dependent flakiness; no second repetition was run by this seat. The receipt's control-pair agreement (finding 5) is the only within-run stability evidence.

10. [obs] **Containment.** No lane tool, probe, predicate, SCORECARD, SOURCES or state file was edited; nothing was written to the fleet repo, a sibling lane repo, `MANIFEST.json`, `.ufo/state` or the watchdog log. Written files are the three under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/RerunBeforeIndependent/` and this report. The probe's scratch tree is created and removed by `tools/probe-child-env-allowlist-r34.py` itself under `/fast/scratch/hyaku/`; `df -h /fast` read 158G available before the run.

Scope: read=round-34 declaration in SCORECARD.md at 6de666c4, pre-data amendments 1 and 2 in SCORECARD.md at 3457f287, frozen probe tools/probe-child-env-allowlist-r34.py at 3457f287 (docstring, PREDICATE, CLAIM_TARGETS, main), tools/run-receipt.py, the nine target builders at 2641591e, receipts before-6de666c4.jsonl (mine), .ufo/waves/round-34/after/c1-before-a2-3457f287.jsonl and c1-after-df661507.jsonl, QUALITY.md 1-161, check-seat-scope.py header; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/RerunBeforeIndependent.md, .ufo/waves/round-34/w2/RerunBeforeIndependent/before-6de666c4.jsonl, .ufo/waves/round-34/w2/RerunBeforeIndependent/before-6de666c4-per-pair.txt, .ufo/waves/round-34/w2/RerunBeforeIndependent/target-blob-identity.txt; executed=timeout 3000 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 tools/run-receipt.py --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --revision 6de666c427ba9aa6b4350561980bde8d0e7c261d --tool-revision 3457f287e04f34e73f8e70d4417b14b96f903f56 --out …/before-6de666c4.jsonl --timeout 2900 -- tools/probe-child-env-allowlist-r34.py --revision '{rev}' --lane '{lane}' (exit 1); read-only git show/diff/rev-parse/log on the lane; local python3 parsing of the saved receipts (no lane tool invoked); sha256sum; df -h /fast (exit 0)
Model: opencode-go/deepseek-v4.1-flash
Installs: none
