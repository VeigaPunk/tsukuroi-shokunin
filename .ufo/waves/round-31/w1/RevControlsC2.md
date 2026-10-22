# RevControlsC2 — re-derived C2 controls vs committed receipts

Verdict: holds — all three probe runs (H1, H2, before f4861f4) reproduce the committed receipts
per-channel on leak, evidence, samples, summary fields and exit code; header fields agree.

## Findings

1. [obs] Probe file identity: `sha256sum tools/probe-git-child-env-r31.py` at the sandbox clone
   (8cff9e7) is `b168b9b86cc125e5207cd359a37e6d7dad6fc2b1d1c601836ddbe4cc7a68d8b0`, equal to
   `tool_sha256`/`probe_sha256` in all three committed receipts. `tools/check-kernel-taint.py`
   blob is `0da3b0fe71ec0b9f30775ee5ea1510969625d2a8` at both f4861f4 and 8cff9e7, so the
   target bytes are identical at the base the controls were built on.

2. [obs] The two patches applied cleanly as detached sandbox commits on base f4861f4
   (`git am`): H1 -> `3738752934b2ecccd424f0231181fca92aded40f`, H2 ->
   `889edcba7b6b1dbafd1f3c0a621661c61b50b7f1`. Resulting `tools/check-kernel-taint.py` blobs
   are `9a5acbb50313c66821d16e26e8ffc9a3721fc318` (H1) and
   `5400bceaab8e98541559fc609f384553b08ce4ab` (H2), exactly the `index` lines of the patch
   headers (`0da3b0f..9a5acbb`, `0da3b0f..5400bce`). The committed control commits de9a5786 /
   d69ea7f0 therefore carry the same tree content (same parent f4861f4, same single-file delta).

3. [obs] H1 probe run (`--revision 37387529… --only check-kernel-taint.py --lane <clone>`):
   exit 1; `targets` 1, `pairs` 3, `leaking` 1, `leaking_pairs` ["tools/check-kernel-taint.py:loader-env"],
   `harness_errors` []. loader-env leaks with evidence exactly
   `["stdout_sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 differs from control f028f84706254b2ca142d224df3f93a59a993759eb96b000d21038ec8ecb2446", "git_execs 0 differs from control 933"]`,
   `git_execs` 0 vs control 933; child-contract and dotgit-pointer clean. Byte-identical to
   c2-H1.jsonl rows 2-5 (modulo scratch path).

4. [obs] H2 probe run (`--revision 889edcba…`): exit 0; `leaking` 0; all three channels clean
   (`git_execs` 933 on loader-env and dotgit-pointer). Byte-identical to c2-H2.jsonl rows 2-5.

5. [obs] Before probe run (`--revision f4861f4d…`): exit 1; check-kernel-taint.py loader-env
   leaks with evidence `["933 descendant execs carry the injection path"]`, sample `git init
   --quiet --initial-branch=master`; child-contract and dotgit-pointer clean. Matches committed
   c2-before-f4861f4d5c0d03ad769a74e0bcab61b5c6f0877c.jsonl rows 8-10 and the summary's
   leaker list (the committed full-11-tool run reports 11 of 33, all loader-env; this run's
   `--only` reports the same single pair).

6. [obs] Receipt headers: `revision` (de9a5786 / d69ea7f0) are the control builder's sandbox
   commit ids and differ as SHAs from the derived commits because committer identity/date of the
   original control commits differ; probed tree contents are equal (finding 2).
   `tool_revision` f4861f4 and `tool_sha256` b168b9b8… are consistent with the probe file taken
   from the declaration commit and unchanged since.

7. [obs] Exit codes match the receipts: H1 1, H2 0, before 1. `control_git_execs` 933 stable
   across all runs and receipts, confirming deterministic fixtures.

## Residual risk / verification gaps

- [inf] Comparison is semantic (leak flags, evidence, samples, summary, exit code) plus
  tree-content equality; literal JSON equality of headers is impossible (timestamps, scratch
  paths, commit SHAs are per-run values).
- [unk] The original control commits' exact committer timestamps/identities are not observable
  from the lane; nothing depends on them.
- [inf] H2's fix changes only the child env scrubbing predicate; the probe's control-A parity
  (rc, normalised stdout digest, git exec count) and the unchanged 933 git execs show no
  output/exit-code drift.

Scope: read=lane receipts c2-H1.jsonl/c2-H2.jsonl/c2-before-f4861f4….jsonl, control patches,
probe + run-receipt sources, SCORECARD round-31 declaration; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w1/RevControlsC2.md;
executed=sandbox clone at 8cff9e7, git am of both patches on f4861f4, 3 probe runs (H1/H2/before).
Model: not exposed
Installs: none
