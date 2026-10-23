# ExecProbeNoHarmBase — no-harm baselines for the earlier probe target sets (round 34, wave 1)

Verdict: both baselines MATCH their expected after-values at the declaration commit
`6de666c427ba9aa6b4350561980bde8d0e7c261d` — `--set r33claim` reads `leaking` 0 of `pairs` 15,
`harness_errors` [], exit 0; `--set regression` reads `leaking` 0 of `pairs` 33,
`harness_errors` [], exit 0. Neither run is a control variant of the C1 target set, so neither is a
finding against C1: neither set contains any of the nine tools named in C1, and no pair fired any
predicate rule. The frozen probe bytes were used in both runs (`probe_sha256`
`35a87374eb89239af841a015965518d63e40de7ac556041f1b0f366a993fa5a8`, `probe_version` 4,
`predicate_label` `leaking`).

## 1. r33claim (five round-33 targets) — 0 of 15

Command (exit code 0; wall clock 58 s):

    cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin && timeout 2950 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 tools/run-receipt.py --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --revision 6de666c427ba9aa6b4350561980bde8d0e7c261d --tool-revision 6de666c427ba9aa6b4350561980bde8d0e7c261d --out /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/ExecProbeNoHarmBase/r33claim.jsonl --timeout 2900 -- tools/probe-child-env-allowlist-r34.py --revision '{rev}' --lane '{lane}' --set r33claim

Summary line, verbatim from the receipt (`.ufo/waves/round-34/w1/ExecProbeNoHarmBase/r33claim.jsonl`,
line 17; receipt sha256 `4eef4d92a005385e71251fd5cc392660add38bceecc59b809416a9a9de2aad40`, 18221 bytes):

    {"revision": "6de666c427ba9aa6b4350561980bde8d0e7c261d", "targets": 5, "channels": ["names", "quiet", "source"], "pairs": 15, "leaking": 0, "leaking_pairs": [], "harness_errors": [], "probe_sha256": "35a87374eb89239af841a015965518d63e40de7ac556041f1b0f366a993fa5a8", "probe_version": 4, "target_set": "r33claim", "scratch": "/fast/scratch/hyaku/sdfa4519181c1-6mgch9oj", "predicate_label": "leaking"}

Footer, verbatim (line 18):

    {"receipt_end": 1, "exit_code": 0, "timed_out": false, "stderr_tail": "", "finished_utc": "2026-10-23T08:44:12Z"}

Per pair, the evidence that fired (from `r33claim.jsonl`); no rule fired on any of the 15 pairs, so
every `evidence` list is `[]`:

| target | names | quiet | source |
|---|---|---|---|
| `tools/_revision.py` | `leak=false`, `git_missing_kept=0` of 279 git children, `parity_diffs=[]` | same, 279 | `scanned=['tools/_revision.py']`, `findings=[]` |
| `tools/check-adjacency-anchors.py` | `leak=false`, `git_missing_kept=0` of 335, `parity_diffs=[]` | same, 335 | `scanned=['tools/_revision.py','tools/check-adjacency-anchors.py']`, `findings=[]` |
| `tools/check-boot-writers.py` | `leak=false`, `git_missing_kept=0` of 203, `parity_diffs=[]` | same, 203 | `scanned=['tools/_revision.py','tools/check-boot-writers.py']`, `findings=[]` |
| `tools/check-root-dac-correction.py` | `leak=false`, `git_missing_kept=0` of 226, `parity_diffs=[]` | same, 226 | `scanned=['tools/_revision.py','tools/check-root-dac-correction.py']`, `findings=[]` |
| `tools/mutants-owed-statements-r29-v4shapes.py` | `leak=false`, `git_missing_kept=0` of 1176, `parity_diffs=[]` | same, 1176 | `scanned=['tools/mutants-owed-statements-r29-v4shapes.py']`, `findings=[]` |

1. [obs] All ten run pairs exited 0 in both the channel run and its control (`control_rc=0`,
   `channel_rc=0`), each run injected the full 10-name value channel
   (`value_channel` has 10 entries), and no injected name reached any child (`reached={}`,
   `values_reached` empty). Evidence: `r33claim.jsonl` lines 2-16; the summary above.
2. [obs] The kept-settings clause did not fire either: `git_missing_kept=0` for every run pair, so
   every traced git child carried `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null`, and no
   run showed a parity difference in exit code, normalised stdout digest or successful-git count.
3. [obs] These bytes reproduce the round-33 tip value exactly, including git-child counts
   `279 / 335 / 203 / 226 / 1176`, the same counts the round-33 after receipt reports
   (`corpus/lessons/round-33-verifier-spotcheck.md:54`: "git children 279/335/203/226/1176 and the
   stdout digests equal to the before"; the after receipt it cites is
   `.ufo/waves/round-33/a3/after/c1-after-c8fcfbf6.jsonl`). The round-33 change is therefore intact
   and unmoved at the round-34 declaration commit.
4. [obs] Receipt header pins the run: `revision` = `tool_revision` =
   `6de666c427ba9aa6b4350561980bde8d0e7c261d`, `tool_sha256`
   `35a87374eb89239af841a015965518d63e40de7ac556041f1b0f366a993fa5a8`, `argv` ends
   `--set r33claim`, `started_utc` `2026-10-23T08:43:15Z`, and the recorded branch state has
   `refs/heads/master 6de666c427ba9aa6b4350561980bde8d0e7c261d`. Evidence: `r33claim.jsonl:1`.
5. [inf] Because none of the five `r33claim` targets is one of the nine C1 tools, a 0 of 15 here
   cannot discriminate the C1 change; it only shows the predicate does not smear onto the round-33
   surface and that no regression was introduced before the change.

## 2. regression (eleven round-32 targets) — 0 of 33

Command (exit code 0; wall clock 4 min 31 s):

    cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin && timeout 2950 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 tools/run-receipt.py --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --revision 6de666c427ba9aa6b4350561980bde8d0e7c261d --tool-revision 6de666c427ba9aa6b4350561980bde8d0e7c261d --out /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/ExecProbeNoHarmBase/regression.jsonl --timeout 2900 -- tools/probe-child-env-allowlist-r34.py --revision '{rev}' --lane '{lane}' --set regression

Summary line, verbatim (`.ufo/waves/round-34/w1/ExecProbeNoHarmBase/regression.jsonl`, line 35;
receipt sha256 `be53671941a9ab2955b43a46b3a8b667d0f31a65039f8fbe9f3c099b55cc0322`, 39130 bytes):

    {"revision": "6de666c427ba9aa6b4350561980bde8d0e7c261d", "targets": 11, "channels": ["names", "quiet", "source"], "pairs": 33, "leaking": 0, "leaking_pairs": [], "harness_errors": [], "probe_sha256": "35a87374eb89239af841a015965518d63e40de7ac556041f1b0f366a993fa5a8", "probe_version": 4, "target_set": "regression", "scratch": "/fast/scratch/hyaku/sdb3ab6fdf441-si14xk1t", "predicate_label": "leaking"}

Footer, verbatim (line 36):

    {"receipt_end": 1, "exit_code": 0, "timed_out": false, "stderr_tail": "", "finished_utc": "2026-10-23T08:47:45Z"}

Per pair, the evidence that fired (from `regression.jsonl`); again no rule fired, every `evidence`
list is `[]`, and `harness_errors` is empty:

| target | names / quiet (`git_execs`, `git_missing_kept`, `parity_diffs`) | source (`scanned`) |
|---|---|---|
| `tools/check-adjacency-overlap.py` | 1263, 0, [] | `['tools/check-adjacency-overlap.py']`, `findings=[]` |
| `tools/check-freshness-r17.py` | 116, 0, [] | `['tools/_revision.py','tools/check-freshness-r17.py']` |
| `tools/check-kernel-taint.py` | 933, 0, [] | `['tools/_revision.py','tools/check-kernel-taint.py']` |
| `tools/check-memory-pressure.py` | 390, 0, [] | `['tools/_revision.py','tools/check-memory-pressure.py']` |
| `tools/check-registry-coverage.py` | 324, 0, [] | `['tools/_revision.py','tools/check-registry-coverage.py']` |
| `tools/check-storage-health.py` | 717, 0, [] | `['tools/_revision.py','tools/check-storage-health.py']` |
| `tools/mutants-adjacency-overlap.py` | 991, 0, [] | `['tools/mutants-adjacency-overlap.py']` |
| `tools/mutants-kernel-taint.py` | 635, 0, [] | `['tools/mutants-kernel-taint.py']` |
| `tools/check-self-assessment.py` | 331, 0, [] | `['tools/check-self-assessment.py']` |
| `tools/mutants-owed-statements-r29.py` | 900, 0, [] | `['tools/mutants-owed-statements-r29.py']` |
| `tools/mutants-owed-statements-r29-landed.py` | 1044, 0, [] | `['tools/mutants-owed-statements-r29-landed.py']` |

6. [obs] Every one of the 22 run pairs exited 0 in channel and control (`control_rc=0`,
   `channel_rc=0`), each injected the full 10-name value channel, and nothing reached a child
   (`reached={}`, `values_reached` empty). Every one of the 11 source pairs returned an empty
   `findings` list. Evidence: `regression.jsonl` lines 2-34.
7. [obs] The kept-settings clause fired on no pair (`git_missing_kept=0` everywhere), including the
   two mutants tools and `check-adjacency-overlap` that do not import `tools/_revision.py`, so the
   clause is state, not evidence, at this revision.
8. [obs] This clears the five source leaks the round-33 development run saw on the same set at
   `1f521b93387590666bfbe7534708d8f416898424`
   (`.ufo/waves/round-33/l1/dev-a2/R-regression-base.jsonl`, last line: `"pairs": 33, "leaking": 5`,
   all five `:source` of the tools that import `tools/_revision.py`). The cause it recorded there was
   `tools/_revision.py:63 ambient-read .environ`, and `tools/_revision.py`'s own source pair now scans
   clean in `r33claim.jsonl` (finding 1), so the round-33 `clean_env()` allow-list is what removed
   them. This is the same 0 of 33 that the round-32 claim reports at its own tip
   (`SCORECARD.md:1242`, `13ca52d0` and `b304b8ea`), reached again at a later revision.
9. [obs] The eleven targets do start git: between 116 and 1263 git children per run pair, exit 0 on
   both run channels, so the set is exercised, not skipped.
10. [inf] A `--set regression` value of 0 of 33 does not by itself show the nine C1 tools are
    unchanged; the eleven regression targets and the nine claim targets are disjoint (compare
    `tools/probe-child-env-allowlist-r34.py:147-171` for `CLAIM_TARGETS` and `REGRESSION_TARGETS`). It
    only shows the earlier repair surfaces are unmoved at the declaration commit, which is the
    no-harm property this seat was asked to record.
11. [unk] Whether the L1's C1 change keeps these two sets at 0: not measurable by me — the change
    does not exist at `6de666c` and this seat is forbidden to write it.

## 3. Method notes and limits

12. [obs] Both runs used the frozen probe bytes and the frozen predicate: `probe_sha256`
    `35a87374eb89239af841a015965518d63e40de7ac556041f1b0f366a993fa5a8` in both summaries equals
    `sha256sum tools/probe-child-env-allowlist-r34.py` at the declaration commit and
    `git cat-file -p 6de666c:tools/probe-child-env-allowlist-r34.py | sha256sum`, which I checked
    before launching (both `35a87374…`, exit 0).
13. [obs] No probe, strace or run-receipt process from my two runs survived; the only matching
    processes at check time belong to seat `C06HostSnapshotNames`
    (`pgrep -af 'probe-child-env-allowlist-r34|run-receipt|strace -f'`, exit 0). Both scratch roots
    the receipts name (`/fast/scratch/hyaku/sdfa4519181c1-6mgch9oj`,
    `/fast/scratch/hyaku/sdb3ab6fdf441-si14xk1t`) are run-private and were left to their owners.
14. [obs] I read the probe's docstring, target sets and main loop, the declaration section of
    `SCORECARD.md`, the round-33 spot-check lesson and the round-33 dev receipts; I edited no lane
    file, ran no git or jj write command and touched no host state. No source fetch and no registry
    row applies to this seat: nothing was fetched, so no `SOURCES.md` duplicate question arises.

Scope: read=`SCORECARD.md` round-34 declaration at `6de666c`, `tools/probe-child-env-allowlist-r34.py`, `tools/run-receipt.py`, `corpus/lessons/round-33-verifier-spotcheck.md`, `.ufo/waves/round-33/l1/dev-a2/README.md` and `R-regression-base.jsonl`, `.ufo/waves/round-34/l1/dev-base/README.md`; wrote=`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/ExecProbeNoHarmBase/r33claim.jsonl`, `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/ExecProbeNoHarmBase/regression.jsonl`, `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/ExecProbeNoHarmBase.md`; executed=`sha256sum` on the probe at the declaration commit and the two receipts, `run-receipt.py` with the frozen probe and `--set r33claim` (exit 0, 58 s), `run-receipt.py` with the frozen probe and `--set regression` (exit 0, 4 m 31 s), `pgrep -af` for leftover processes
Model: not exposed
Installs: none
