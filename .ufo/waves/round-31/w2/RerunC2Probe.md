# RerunC2Probe — independent re-derivation of C2's after-value (round 31, wave 2)

Verdict: **holds** — the frozen probe, run from a fresh sandbox clone at the revision under attack `f3a5723a988bf1c2835985880e7a38d477462cd0`, reads `leaking` 0 of `pairs` 33, `harness_errors` empty, exit 0: byte-for-byte the declared C2 after-value (SCORECARD.md:1203), identical to the committed after receipt `c2-declared.jsonl` on every behavioural field, and opposite to the before receipt (`c2-before-…f4861f4d…jsonl`, 11/33 leaking, exit 1).

## Setup

1. [obs] Sandbox: `/fast/scratch/hyaku/tsukuroi-r31/RerunC2Probe/repo`, cloned with `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-local` from `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, checked out at `f3a5723a988bf1c2835985880e7a38d477462cd0` (`git rev-parse HEAD` → `f3a5723a988bf1c2835985880e7a38d477462cd0`; `git status --porcelain` → empty). No git write anywhere; no `GIT_*` set to lane/fleet paths.
2. [obs] Frozen probe byte-identity: `sha256sum` of `tools/probe-git-child-env-r31.py` both in the lane working tree and in the sandbox clone at f3a5723 → `b168b9b86cc125e5207cd359a37e6d7dad6fc2b1d1c601836ddbe4cc7a68d8b0`, matching `probe_sha256` in both committed receipts.

## Command and output

3. [obs] `cd /fast/scratch/hyaku/tsukuroi-r31/RerunC2Probe/repo && python3 tools/probe-git-child-env-r31.py --revision f3a5723a988bf1c2835985880e7a38d477462cd0 --lane /fast/scratch/hyaku/tsukuroi-r31/RerunC2Probe/repo > /fast/scratch/hyaku/tsukuroi-r31/RerunC2Probe/rerun2.jsonl 2>…/rerun2.stderr; echo EXIT=$?` → `EXIT=0`; wall `1096.64s`; stderr empty (0 bytes).
4. [obs] `rerun2.jsonl` (sha256 `3ac0a96fdf3a40f9f8d3b5b819886b4c36c979346816b72129b94b3596ef9899`, 34 lines = 33 pair lines + 1 summary line). Summary line 34: `{"revision": "f3a5723a988bf1c2835985880e7a38d477462cd0", "targets": 11, "channels": ["loader-env", "child-contract", "dotgit-pointer"], "pairs": 33, "leaking": 0, "leaking_pairs": [], "harness_errors": [], "probe_sha256": "b168b9b86cc125e5207cd359a37e6d7dad6fc2b1d1c601836ddbe4cc7a68d8b0", "scratch": "/fast/scratch/hyaku/git-child-env-47zep8cp"}`.
5. [obs] Every one of the 33 pair lines carries `"leak": false` and `"evidence": []`; all 11 controls started git children (`control_git_execs` 1263 / 116 / 933 / 390 / 324 / 717 / 991 / 635 / 331 / 900 / 1044) and all `control_rc` / `channel_rc` are 0.

## Comparison with the committed receipts (programmatic, field-by-field)

6. [obs] Full JSONL comparison of my run vs `.ufo/waves/round-31/measure/after-13ca52d0/c2-declared.jsonl` (36 lines: header, 33 pairs, summary, receipt_end): pair sets identical (33/33); **0 behavioural diffs** on `control_rc`, `control_git_execs`, `channel_rc`, `git_execs`, `evidence`, `leak`. The only 12 diffs are `argv` revision placeholders — mine carry `--base/--counter-rev f3a5723…` (and `--counter-rev f3a5723…` for `mutants-owed-statements-r29.py` whose `--base` is pinned `81a061a…`), the after receipt carries `13ca52d0…`. The after receipt independently reports `leaking` 0, `harness_errors` [], exit 0 (`receipt_end` line 36), `probe_sha256` b168b9b8… — same verdict.
7. [obs] Comparison vs `.ufo/waves/round-31/measure/c2-before-f4861f4d5c0d03ad769a74e0bcab61b5c6f0877c.jsonl`: exactly the 11 `loader-env` pairs differ (leak True→False, evidence `["N descendant execs carry the injection path"]`→`[]`): `check-adjacency-overlap.py` 1263 (line 2), `check-freshness-r17.py` 124 (line 5), `check-kernel-taint.py` 933 (line 8), `check-memory-pressure.py` 390 (line 11), `check-registry-coverage.py` 324 (line 14), `check-storage-health.py` 717 (line 17), `mutants-adjacency-overlap.py` 1057 (line 20), `mutants-kernel-taint.py` 659 (line 23), `check-self-assessment.py` 348 (line 26), `mutants-owed-statements-r29.py` 938 (line 29), `mutants-owed-statements-r29-landed.py` 1073 (line 32). The before receipt's summary reads `leaking` 11, exit 1; mine reads 0, exit 0.
8. [obs] No dotgit-pointer flake in this campaign: all 11 `dotgit-pointer` pairs clean (wave-1 `MutProbeC2.md` §5 reported 2 spurious `canary fingerprint changed` verdicts in 121 runs; none reproduced here). A first attempt at this probe was killed by my 900 s command deadline after emitting 27/33 pair lines — also all clean — so the dotgit-pointer pairs were observed clean in two independent runs [obs].

## Findings

- F1 [obs] Re-derived after-value at the attacked revision: `leaking` 0/33, `harness_errors` empty, `pairs` 33, exit 0 — the declared after-value (`</ORECARD.md:1203`) holds at the lane tip `f3a5723…`, and equals the after receipt measured at the integration commit `13ca52d0…`.
- F2 [obs] The lane tip therefore behaves identically to the integration commit under the frozen probe: per-pair field equality (F6) holds across all 33 pairs on all three channels.
- F3 [obs] The fix direction is confirmed against the before state: the 11 `loader-env` leaks of the before receipt (11 targets, 33 pairs, exit 1) are exactly the pairs that now read clean; `child-contract` and `dotgit-pointer` remain clean in both.
- F4 [obs] Probe authenticity and unchanged byte: `probe_sha256` b168b9b8… matched in all three artefacts; the run tool is byte-identical to the frozen copy (F2). No frozen rule, counter, probe or receipt was modified.
- F5 [obs] Tooling: full probe wall time 1096.6 s under host load vs the ~7-min estimate; the first attempt was killed at 900 s (27/33 pairs, all clean). Not a verdict factor; noted for L1 scheduling if reruns are needed.
- F6 [unk] Not re-derived here: the content of the C2 fix diff itself (tools between `f4861f4d…` and the tip), claim sizing, and other seats' claims — out of scope for this reviewer seat, which re-derived the measured value only.

## Residual risk / verification gaps

- Single-shot verdict with no flake: wave-1 `MutProbeC2.md` §5 established the dotgit-pointer channel is not run-to-run deterministic (2 spurious in 121). This seat's two independent full/partial runs both read all dotgit-pointer pairs clean; the unidentified flake mechanism (background `git maintenance` vs fingerprint hashing) remains open [unk].
- The comparison normalises only the scratch-derived `argv` lane path and revision placeholders; receipt field sets were asserted equal (33/33 pair identity) before comparing [obs].

Scope: read=`SCORECARD.md` round-31 declaration + errata (1196-1224), `.ufo/waves/round-31/measure/c2-before-f4861f4d5c0d03ad769a74e0bcab61b5c6f0877c.jsonl`, `.ufo/waves/round-31/measure/after-13ca52d0/c2-declared.jsonl`, `tools/probe-git-child-env-r31.py`, `.ufo/waves/round-31/w1/MutProbeC2.md`, sandbox rerun outputs; wrote=`.ufo/waves/round-31/w2/RerunC2Probe.md`; executed=`git clone`/`checkout` in sandbox (read-only lane), `python3 tools/probe-git-child-env-r31.py --revision f3a5723… --lane <clone>` (twice; first killed at 900 s, second completed with exit 0), `sha256sum`, `strace -V`, Python comparison script.
Model: not exposed
Installs: none
