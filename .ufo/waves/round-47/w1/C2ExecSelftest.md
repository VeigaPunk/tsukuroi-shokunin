VERDICT: supports

# C2ExecSelftest — item C2-K5: the frozen round-46 counter's selftest legs at the impl revision

Revision under test: `77e9e2b2e96b85d8f048ae2087e246a542b71611` (census bytes `adb1b4ce2325c38da2acbb815d820d3d8d6a0dd45b34796d808590c8ab32ce41`, 212252 bytes, 3644 lines).
Counter: `tools/score-census-identity-r46.py`, sha256 `7c406eb5f4ba1f6265649f7102e7376882483180c161a66abc68e08cad9524ba` — byte-identical at base `9160190`, at `72cc2609`, at the impl revision and in the worktree (`for r in 9160190 72cc2609 77e9e2b2; do git show $r:tools/score-census-identity-r46.py | sha256sum; done` → same digest, three times; `git status --porcelain tools/score-census-identity-r46.py` → empty).

## 1. The declared run (one execution, serialized)

```
export TMPDIR=/fast/scratch/hyaku/tsukuroi-r47/C2ExecSelftest
python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/score-census-identity-r46.py \
  --revision 77e9e2b2e96b85d8f048ae2087e246a542b71611 \
  --scratch /fast/scratch/hyaku/tsukuroi-r47/C2ExecSelftest/s
```
exit 0, wall 26 s (the item predicted ~2.5 min; this revision's selftest is 164 cases in 27 s), stderr empty. Receipt: `w1/C2ExecSelftest/counter-r46-at-impl.jsonl` (one JSON line, sha256 `65b05dbd525d84306e5f38cafb8bcbabc058865046e55c3f054fc8970896dc1f`).

`verdict = PASS`. Every leg:

| leg | declared expectation | observed | evidence |
|---|---|---|---|
| identity_ok | 1 | **1** | one `TSUKUROI_CENSUS_IDENTITY:` line, `version=census-v2 sha256=adb1b4ce… md5=cf005e9a… bytes=212252 lines=3644 planes=packages,systemd,drivers,journal,update-safety,oom exit_map=0:HEALTHY,1:DEGRADED,2:BLOCKED verified=yes`; all four digest/size fields equal the counter's own recomputation (`detail.want`) |
| tracks_ok | — | **1** | the one-appended-line copy reports `sha256=b01886f3… bytes=212274 lines=3646`, i.e. its own bytes, not a constant |
| symlink_ok | — | **1** | symlink invocation reports the target's `adb1b4ce…`, `verified=yes` |
| unverifiable_ok | — | **1** | all three cases (stdin with decoy `bash` in cwd, `<(cat F)`, replaced-after-open) exit 0 with `sha256=md5=bytes=lines=unverifiable`, `verified=no` |
| cli_ok | — | **1** | `--identity --selftest` → 2, `--identity --sample 3` → 2, `--help` → 0 and names `--identity`, `--bogus` → 2 (`detail.cli == [true,true,true,true]`) |
| nowrite_ok | — | **1** | cwd and TMPDIR snapshots unchanged across the identity and unverifiable legs |
| selftest_pass | 1 (counter tolerates the new case count) | **1** | last stdout line `TSUKUROI_CENSUS_SELFTEST: PASS (164 cases, 164 passed, 0 failed)`; `SELFTEST_RE` is `PASS \(\d+ cases, \d+ passed, 0 failed\)` (counter:65), so 164 matches — the counter is case-count agnostic |
| selftest_r46 | >= 6 | **8** | counter:231 counts `^PASS .*\(R46-C1\)`; the 8 lines are the six identity cases and the two `--identity` CLI refusals (receipt `selftest-impl-164cases.log:157-164`) |

The frozen predicate requires `selftest_r46 >= 4` (counter:66-67); observed 8 satisfies the frozen predicate and the item's stricter `>= 6`. No leg degraded.

## 2. What the counter can and cannot see about C2 (supplementary, serialized)

The counter's own selftest leg runs the census with `TMPDIR` = its own `mkdtemp` under `--scratch` (counter:145). So the C2 defect is invisible to it unless the scratch path itself carries a space. Measured both ways:

| counter run | revision | selftest_pass | last line | verdict |
|---|---|---|---|---|
| `--scratch s` (space-free) | base `9160190` | 1 | `PASS (162 cases, 162 passed, 0 failed)` | PASS (`counter-r46-at-base.jsonl`) |
| `--scratch s` (space-free) | impl `77e9e2b2` | 1 | `PASS (164 cases, 164 passed, 0 failed)` | PASS |
| `--scratch "s 2"` (space) | base `9160190` | **0** | `FAIL (162 cases, 13 passed, 149 failed)` | **FAIL** (`counter-r46-at-base-space-scratch.jsonl`, rc 1) |
| `--scratch "s 2"` (space) | impl `77e9e2b2` | **1** | `PASS (164 cases, 164 passed, 0 failed)` | **PASS** (`counter-r46-at-impl-space-scratch.jsonl`, rc 0) |

Direct census runs, same bytes, confirm the pair without the counter in the middle:
- impl census under `TMPDIR="$S/t 2"`: `rc=0`, `TSUKUROI_CENSUS_SELFTEST: PASS (164 cases, 164 passed, 0 failed)`, stderr 0 bytes (`selftest-impl-under-space-TMPDIR.log`).
- base census under `TMPDIR="$S/t 2"`: `rc=1`, `TSUKUROI_CENSUS_SELFTEST: FAIL (162 cases, 13 passed, 149 failed)`; the 149 `FAIL` lines are on **stderr** and the 13 `PASS` lines on stdout (`selftest-base-9160190-under-space-TMPDIR.{stdout,stderr}.log`). This reproduces the declaration's before-value at `SCORECARD.md:3059-3061` and `:3066` exactly, including the "13 passed / 149 failed" split.
- The impl selftest log is byte-identical space-free and under a space TMPDIR (both sha256 `f8c8acfba89b45f4a5c015d1da0f0d33b610f620b0734026bd56dae6a12eb51c`), so the repair made the fixture base independent of TMPDIR dirt at the level of observable case results.
- The two new pinning cases pass at impl: `selftest-impl-164cases.log:165` `PASS selftest: the fixture base classifies absolute even when TMPDIR contains a space (R47-C2)`, `:166` `PASS selftest: a space in a root override stays unsafe by design (R47-C2)` (source `census-at-rev.sh:3473-3483`, base derivation `:2050-2059`).

Identity-axis non-regression: the `--identity` line shape, field order, `planes` order and exit map are unchanged between base and impl; only the digest/size fields move with the bytes (base `sha256=ac4e38ff… bytes=210762 lines=3622`; impl `sha256=adb1b4ce… bytes=212252 lines=3644`; both `verified=yes`, both `planes=packages,systemd,drivers,journal,update-safety,oom`).

## 3. Findings for the L1 to adjudicate (I do not judge them)

- **F1 — stale count in the C2 kill rule.** `SCORECARD.md:3066` requires "all six `(R46-C1)` cases still pass". The base bytes already carry **eight** `(R46-C1)` PASS lines (six `id_check` + two `check_cli`; the frozen counter reports `selftest_r46 = 8` at base as well as at impl), because round-46 wave hardening `61e06740` added "a parent-held descriptor on a relinked decoy" and "`--identity` with `--help` exits 2". All eight pass, so the requirement holds a fortiori; "six" is simply stale against the base bytes. Not a regression.
- **F2 — the C2 kill rule and the /tmp fallback.** `SCORECARD.md:3066` also requires "no committed tool writes under a hardcoded /tmp". The impl census hardcodes `/tmp` as the fixture-base fallback: `census-at-rev.sh:2055-2059` (`local st_base=${TMPDIR:-/tmp}` … `*[!A-Za-z0-9._/+-]*) st_base=/tmp ;;`), and its own header documents it (`:411-412`, "or /tmp itself when TMPDIR holds characters the root-override locator refuses — R47-C2"). Under a space TMPDIR the selftest therefore does write its fixture tree under `/tmp`; `mktemp -d` creates it mode 0700 (observed `drwx------`; S252 `mktemp.html:78-79`: "Files are created u+rw, and directories u+rwx, minus umask restrictions"), and the EXIT trap `census-at-rev.sh:2062` removes it. Read literally the kill rule is contradicted by the implementation; read as "no fixed /tmp path outside mktemp" it holds. This needs an explicit ruling, not a silent pass.
- **F3 — the r46 counter's selftest leg is a C2 discriminator only with a space in `--scratch`.** Space-free, base and impl both return `selftest_pass = 1` (162 vs 164 cases), so this counter alone cannot falsify a C2 regression; the discriminating instrument is the declared C2 counting command (space TMPDIR), which I also ran and which separates base `rc 1 / 149 failed` from impl `rc 0 / 164 passed`. Anyone quoting `selftest_pass = 1` at impl as C2 evidence would be quoting a leg that base also passes.
- **Transient `/tmp/tsukuroi-r3-2-selftest.*` dirs** are visible during a run and removed by the census EXIT trap when it completes: I observed `…JOVjI0` present at 05:58Z and absent by 06:00Z, and the listing returned to its baseline count after each of my completed runs. Concurrent seats run the same census selftest on this host, so a momentary listing is not evidence of a leak. No leftover of mine.

## 4. Scope, hygiene, and what I did not do

- One selftest at a time throughout: 9 census selftests in total, never two concurrently — 4 inside the four counter runs above (1 each) and 5 direct (impl space-free, impl under a space TMPDIR twice, base under a space TMPDIR once, plus one repeated impl space run whose wrapper's listing redirect failed harmlessly and whose result is the `PASS (164 cases…)` recorded above). No lane trackfile was created, edited or deleted; no git/jj mutation in the lane; no package, service, sysfs, mount or `/etc` change; no `btrfs`/`systemctl` write; no scrub/scratch write outside `/fast/scratch/hyaku/tsukuroi-r47/C2ExecSelftest`. Scratch removed at the end.
- Read-only only: `git show`, `git rev-parse`, `git log`, `git diff --stat`, `git status`, `sha256sum`, `grep`, and the census/counter runs above. The lane's own `tools/tsukuroi-census.sh` in the worktree is byte-identical to the impl revision (`sha256sum tools/tsukuroi-census.sh` = `adb1b4ce…` = `git show 77e9e2b2:tools/tsukuroi-census.sh | sha256sum`).
- Not done by me (other seats / the L1 own them): the declared C2 counting command against the worktree path, the adjacency-anchor gate, the digit-stripped live-output comparison, the census exit-map probe, and the r47 C1 admission counter. I did not install or upgrade any tool.
- Two `/tmp/tsukuroi-r3-2-selftest.*` dirs belonging to concurrently running seats were left untouched.

Receipts in `w1/C2ExecSelftest/`: `counter-r46-at-impl.jsonl` (the declared JSON line), `counter-r46-at-base.jsonl`, `counter-r46-at-impl-space-scratch.jsonl`, `counter-r46-at-base-space-scratch.jsonl`, `selftest-impl-164cases.log`, `selftest-impl-under-space-TMPDIR.log`, `selftest-impl-under-space-TMPDIR-run2.log`, `selftest-base-9160190-under-space-TMPDIR.stdout.log`, `selftest-base-9160190-under-space-TMPDIR.stderr.log`.
