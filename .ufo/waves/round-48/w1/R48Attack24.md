# R48Attack24 — C2 cleanup/failure-path falsifier

Verdict: **KILLED**

Surface: pinned `HEAD` blob of `tools/tsukuroi-census.sh` at `5fdf062f969292736e36513e39f98b1b8de43635`, copied to seat scratch and invoked there. This is not the round-start SHA in the assignment; it was the readable pinned tip during this run. No lane working-copy execution or mutation.

Observed:
- `TMPDIR=$S`, default PATH, `--selftest`: `TSUKUROI_CENSUS_SELFTEST: PASS (164 cases, 164 passed, 0 failed)`; shell status 0. (This inspected tip does not match the frozen 166-case target.)
- Replaced `mktemp` in a scratch-only PATH with a stub exiting 73: selftest propagated status 73, emitted no fixture entry in TMPDIR, no descriptor evidence was collected.
- TMPDIR set to a regular file and to a mode-000 directory (effective uid root): both failed with status 1 and mktemp diagnostics; no test verdict. Permission denial in mode-000 case is observable, though root privileges mean this does not model an ordinary unreadable directory.
- No fixture tree matching `tsukuroi-r3-2-selftest.*` remained in seat scratch after successful/failing runs.
- Found three pre-existing matching fixture directories in `/tmp`: `tsukuroi-r3-2-selftest.vmgCEp`, `...aC4yw0`, `...GULcpE`. I did not inspect or delete these because ownership is unknown. Thus the required no-stray-/tmp condition is not demonstrated; the successful run used explicit scratch TMPDIR and the observed failure runs had no fallback.
- The harness installs `trap ... EXIT INT TERM` after successful `mktemp`, removing `$work`; mktemp failure occurs before trap installation. No signal/normal-exit cleanup or descriptor-leak measurement was performed in this run.

Rationale: the inspected revision fails the frozen C2 exact output/count requirement (164 vs 166), so the claim is killed for this tested blob. Failure-path observations are limited to normal mktemp failure and bad TMPDIR. Caller cwd/environment and descriptor leak remain unverified. No tools installed.