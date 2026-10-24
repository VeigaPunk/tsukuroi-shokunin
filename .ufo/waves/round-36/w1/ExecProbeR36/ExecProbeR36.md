# ExecProbeR36 — C1 counter draft

## Files and behavior

- `probe-child-env-allowlist-r36.py`: VERSION 5 draft based on the checked-in r34 probe. Adds `livefive` (four viable targets; census scorer excluded), an `untraced` channel, proc-environment wrappers, and the V6-calibrated path/hash normalisation. The original `names`, `quiet`, `source`, static scan, execveat/unparseable handling and predicate remain; the old sets retain their one-git-child control gate.
- This report and `probe-evidence.json` are the only other seat artifacts. No production file was changed.

The repository's r34 file at the requested base actually has `VERSION = 6` (and the round-35 calibration receipts report `probe_version: 6`), despite the assignment identifying it as VERSION 4. The draft uses the requested successor label VERSION 5. The round-36 `CLAIM_BASE` default is `6d76fb20f6ecbc940e5c8fff36c74060c885e161`; `--base` remains overridable.

Wrapper PATH note: the original ambient value places `/usr/bin:/bin` before the injected directory, so shims in the final entry cannot be selected. The untraced run therefore uses `<inject>/<random>:/usr/bin:/bin`; names/quiet preserve the original path order. Each shim logs its own `/proc/self/environ` record to `untraced.log`, then execs its `/usr/bin` binary. Shim and shebang-interpreter execve records are filtered from strace attribution; the real-binary execve remains. The fixed-PATH child never selects a shim.

## livefive viability

All times below are control measurements at `6d76fb20f6ecbc940e5c8fff36c74060c885e161`. Direct times are the observed shell `time` results; child counts are from the probe's traced control A. Expected exit is 0 for every included target.

| Target | Exact argv template | Direct control | Probe control evidence | Status |
|---|---|---:|---|---|
| `check-revision-binding.py` | `--tools-revision {rev} --object-target-types` (run from a worktree cloned from `{clone}`; this CLI roots at its script) | 7.62 s, exit 0; target-type mode PASS, 9/9 | control A: 2,542 successful child execs (2,397 git); A/B and base control passed in the partial probe | Target invocation is viable. The isolated probe run was SIGTERM'd at 81.98 s after names/quiet/source and before its untraced result/summary; full channel completion is unverified. |
| `check-report-receipts.py` | `--report .ufo/waves/r36-probe-report.md --lane {clone} --revision {rev}` | 0.53 s, exit 0; cited 1 pair, receipt found at `.ufo/waves/round-32/measure/c1-before-v2-f28442cbe34a3b18003c94b96ecf7051e67c0a61.jsonl` | control A: 366 git children; one-target probe completed without harness errors | Included. |
| `mutants-btrfs-space-r30.py` | no arguments (default battery mode) | 2.91 s, exit 0; control verified 10, rejected 0/72 should-fail and 0/11 should-pass | control A: 84 child execs, 0 git; one-target probe completed without harness errors using the livefive child-exec gate | Included. |
| `run-receipt.py` | `--revision {rev} --tool-revision {rev} --lane {clone} --out {clone}/../run-receipt-livefive.jsonl -- tools/check-report-receipts.py --selftest` | 0.75 s, exit 0; inner receipt exit 0 | control A: 10 git children; completed in the five-target development run without a harness error | Included. |

Excluded from `LIVE_FIVE_TARGETS`: `score-census-handoff-r32.py`, template `--revision {rev} --lane {clone} --scenarios 1 --budget 180 --seed 36`. Its direct control completed in 16.77 s, but the instrumented A/B controls still disagreed in normalised stdout (`403dbcd5…` versus `b985323a…`) with the fixed seed. It is therefore not viable under the inherited parity rule and is not silently counted as a fifth target.

## Development runs

- `--set claim` at revision 6d: summary `targets=9`, `pairs=36`, `leaking=0`, `harness_errors=[]`, exit 0. Captured probe hash `bdfb2e50f5e7faa45bdc99df109998e0018c331bc4a0c5f3ac4ed6e68499ca75`; this run preceded the final `/fast/scratch/hyaku` path-normaliser addition.
- Final-byte `--set r33claim` at revision 6d: `targets=5`, `pairs=20`, `harness_errors=[]`, but `leaking=3`, exit 1: `check-boot-writers.py:{names,quiet,untraced}` still differ in `git_argv_sha256`. Other r33 targets, including `_revision.py` and `mutants-owed-statements-r29-v4shapes.py`, were clean after the targeted normalisation checks. This no-harm criterion is **not met**; remaining check-boot-writers argv variation is a blocker to claiming the expected zero.
- Full `--set regression` was run at revision 6d on the earlier VERSION-5 draft with default base 264159. It reported `leaking=12`, `harness_errors=[]`; the 12 pairs were names/quiet/untraced for four mutant tools. This run predates the final claim-base and scratch-path normalisation changes and is not evidence that final regression is clear. A final full regression rerun was not completed.
- The r34 mutation receipt revisions `7e624d9b34331272c0089c184332c45ea302ab8e` and `d0cf31b0189a4e1cc503678dba10eebe4a509ce0` are not present in the lane object database (`git cat-file -t` failed for both). Scratch clones at their receipt's r34 tip `3457f287e04f34e73f8e70d4417b14b96f903f56` were created, but checking out either mutant revision failed with `fatal: unable to read tree`. The committed `variant.patch` and `mutant.patch` are present. The executor seat cannot create commits or mutate Git objects, so the requested mutant sensitivity runs are blocked; no mutant >0 result is claimed.

The round-35 calibration artifacts read were `ExecV6Calibration/byte-invariance.txt`, `r33claim-v6.jsonl` and `regression-v6.jsonl`. In the latter, `regression-clause-summary.txt` attributes false positives to `GIT_CEILING_DIRECTORIES`; the draft exempts that computed setting and HOME-derived paths. The trace comparison also exposed 4-hex `git rev-parse --disambiguate` prefixes (`be33` vs `701f`), so the draft normalises those prefixes specifically in addition to 7–64-hex IDs, run scratch/fixture/work-tree paths, and `/fast/scratch/hyaku` scratch trees.

## Diffstat, risks, and blockers

`git diff --no-index --stat r34.py probe-child-env-allowlist-r36.py`: **1 file changed, 274 insertions(+), 45 deletions(-)**. Final probe SHA-256: `081d2a5199f08b136f4aadd7fd2823bcb35817f93ddd71b29c723b0d81d623ff`.

Risks: `livefive` names four of the five declared tools; the scorer is excluded for unstable A/B output, and the revision-binding probe's full untraced channel was interrupted. Final r33claim still has three argv-parity leaks; final regression and mutant sensitivity are not certified. The PATH ordering adjustment is required for the wrappers to be reachable. LSP was unavailable in this tool inventory. No tools were installed; no build, test suite, linter or formatter was run (only the requested control/development probe runs).

Report: .ufo/waves/round-36/w1/ExecProbeR36
