VERDICT: supports

# C1-2 — selftest twice at 4476620 + live census parity (base c8efaa3 vs tip 4476620)

Seat: C1ExecSelftest (L2, round 42 / hyaku 9, wave w1). Item C1-2.
Scratch: `/fast/scratch/hyaku/tsukuroi-r42/C1ExecSelftest/` (removed at finish; receipts copied here).
Receipts: `.ufo/waves/round-42/w1/C1ExecSelftest/` (`st1.log`, `st2.log`, `live-base.out`,
`live-tip.out`, `live-base2.out` — the §6 drift control, `smp-base.out`, `smp-tip.out`,
`base-tip.diff`, `qkk-live-sample8.out`, `qkk-live-sample400.out`, `sample400-names.txt`,
`pacman-Sup-live.out`, `pacman-Suu-live.out`, `sha256sums.txt`).

## 1. Revision identity (exports are byte-identical to the commits)

```
$ git -C …/tsukuroi-shokunin show 447662088dfd3155e31aed239179a79c1d1046c7:tools/tsukuroi-census.sh > c.sh
$ git -C …/tsukuroi-shokunin show c8efaa3f120834541f8de1e5e0367e8d1593bae6:tools/tsukuroi-census.sh > base.sh
$ git hash-object c.sh      -> ed83079c400594ab5ed84da045a6ed020c1a2542   (= rev-parse 4476620:tools/…)
$ git hash-object base.sh   -> dda066f48fdc296db583f4b262fd7f9f027faefd   (= rev-parse c8efaa3:tools/…)
$ sha256sum  c.sh 46d62a24…94f1b1 (3201 lines) | base.sh 646c84fc…9eb95 (3176 lines)
```
Landing tip at run time was `87c4f7c6` (w1 spec + batteries); `git show 4476620:tools/…` is what I ran, not the
working tree, so the w1 additions after 4476620 do not enter any result below.

## 2. `bash c.sh --selftest` twice (TMPDIR in scratch) — PASS, 130/130, both times

```
RUN 1 rc=0 wall_ms=27380   TSUKUROI_CENSUS_SELFTEST: PASS (130 cases, 130 passed, 0 failed)
RUN 2 rc=0 wall_ms=26128   TSUKUROI_CENSUS_SELFTEST: PASS (130 cases, 130 passed, 0 failed)
PASS lines per run: 130   FAIL lines per run: 0   log sha256 both runs = ea536b6f53f9…093a9181 (identical)
```
Observed literally (`st1.log`, `st2.log` last line): `TSUKUROI_CENSUS_SELFTEST: PASS (130 cases, 130 passed, 0 failed)`.
That matches the declared expectation exactly (`130 -> 130`, 128 `->` 130 at the two new cases). No case was skipped,
no case printed a non-PASS status. I did **not** run `base.sh --selftest` (128 cases by declaration); the frozen
counter owns the base/selftest conjunct.

## 3. The two `R42-C1` labels (both present in source and both PASS live)

| source | label | observed in `st1.log` |
|---|---|---|
| `c.sh:2357` | `blocked: a sample error ahead of a large -Qkk output still blocks (R42-C1)` | `PASS blocked: a sample error ahead of a large -Qkk output still blocks (R42-C1) (exit 2, BLOCKED)` |
| `c.sh:2564` | `degraded: 4002 update candidates keep the names and the trap row (R42-C1)` | `PASS degraded: 4002 update candidates keep the names and the trap row (R42-C1) (exit 1, DEGRADED)` |

Both are the large-output cases: `c.sh:2350-2355` builds a `qkk.out` of 1 error line + 4000 `warning:` lines
(~300 KB, i.e. ≫ the 64 KiB pipe buffer) and asserts `^PLANE packages: BLOCKED (pacman -Qkk sample probe error: …)`;
`c.sh:2556-2563` builds 4002-line `qu`/`sup`/`suu` (~100 KB each) and asserts
`candidates=4002 … names=[alpha,beta,pad00000]` plus `trap=-Suu:4002[fixture/alpha 1.1-1]`.

## 4. Live run, both censuses back to back, no arguments (read-only)

```
base.sh rc=1 wall_ms=3669  12 lines stdout, 0 lines stderr
c.sh    rc=1 wall_ms=3691  12 lines stdout, 0 lines stderr
```

Six PLANE lines, verdicts identical: `packages=DEGRADED systemd=HEALTHY drivers=DEGRADED
journal=DEGRADED update-safety=DEGRADED oom=DEGRADED`; `STORAGE btrfs-device-stats state=HEALTHY
filesystems=1 devices=1 nonzero=0` identical; rollup identical:

```
TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=DEGRADED)
```

Every differing line (`diff live-base.out live-tip.out`, 4 `<`/`>` lines total):

1. header — `… 2026-10-26T19:42:37Z …` -> `… 2026-10-26T19:42:41Z …` (run clock).
2. `PLANE drivers` — only these four live fields moved:

| field | base | tip |
|---|---|---|
| `C5_pswp` | `44792/284350` | `44792/286398` |
| `C6_avail_kb` | `20194252` | `20311360` |
| `C6_psi_full_total_us` | `18733064` | `18743384` |
| `C6_shmem_kb` | `22268` | `23464` |

`PLANE packages` (the `:692/:694` arm), `PLANE systemd`, `PLANE journal`, `PLANE update-safety`
(the `-Qu`/`-Sup`/`-Suu` arm), `PLANE oom`, both `HANDOFF` lines, `DRIFT pacnew-plane` and `STORAGE` are
byte-identical between base and tip.

## 5. Live run, both censuses back to back, `--sample 400` (read-only)

```
base.sh --sample 400 rc=1 wall_ms=12604  12 lines stdout, 0 stderr
c.sh    --sample 400 rc=1 wall_ms=12669  12 lines stdout, 0 stderr
```

`PLANE packages` with `sample=400` (400 names, first 400 of `pacman -Qq`) is **byte-identical** between base and
tip (`diff` of the two packages lines → no output), i.e. the changed `:692/:694` reader returns the same verdict
and the same note on this host. `PLANE update-safety`, `STORAGE` and the rollup are also byte-identical.
Only differing line again is the header clock plus `PLANE drivers`, with six drifting fields:

| field | base | tip |
|---|---|---|
| `C5_pswp` | `44792/308609` | `44792/316801` |
| `C6_avail_kb` | `20536848` | `20156776` |
| `C6_psi_full_avg300` | `0.01` | `0.02` |
| `C6_psi_full_total_us` | `18874529` | `18937742` |
| `C6_psi_some_avg300` | `0.01` | `0.02` |
| `C6_shmem_kb` | `22444` | `22272` |

## 6. Attribution: the residual differences are host drift, not the fix

Decisive control — the **same** script, same arguments, run twice (`live-base.out` vs `live-base2.out`,
3,631 ms), differs in the same field family, including fields that base-vs-tip happened to agree on:

```
base1 vs base2 (identical code, identical args) — differing drivers fields:
  C5_pswp: 44792/284350 -> 46382/328577      C6_avail_kb: 20194252 -> 20111136
  C6_psi_full_avg300: 0.00 -> 0.07           C6_psi_full_total_us: 18733064 -> 19479274
  C6_psi_some_avg300: 0.00 -> 0.07           C6_shmem_kb: 22268 -> 26568
```
Only `PLANE drivers` differs between the two base runs; every other line, including all five other PLANE lines,
STORAGE and the rollup, is unchanged. These fields are live kernel readings taken per run —
`pswpin`/`pswpout` from cgroup `memory.stat` (`c.sh:1169-1170`), `MemAvailable`/`Shmem` from `/proc/meminfo`
(`c.sh:1195-1196`), PSI from `/proc/pressure/memory` (`c.sh:455`, `c.sh:1205`) — so they cannot be produced by an
edit confined to `probe_packages`/`probe_update_safety`/`run_selftest`. Conclusion: **no live behavioural
difference is the fix; all observed movement is drift.** No verdict, no exit code (1/1 in all four runs) and no
plane note outside `drivers` changed between base and tip.

## 7. Why the live host cannot exercise the fixed path (headroom measurement)

The fix only matters when a probe buffer exceeds the 64 KiB pipe buffer. Measured live, in the census's own
shapes (read-only):

| probe | transcript |
|---|---|
| `pacman -Qkk` over the 8-package default sample (`qkk-live-sample8.out`) | 617 bytes |
| `pacman -Qkk` over the 400-package sample (`qkk-live-sample400.out`) | 23,425 bytes / 479 lines / **0** `^error:` lines |
| `pacman -Qu` | 136 bytes / 3 lines |
| `pacman -Sup --print-format '%r/%n %v'` (`pacman-Sup-live.out`) | 114 bytes / 3 lines |
| `pacman -Suu --print-format '%r/%n %v'` (`pacman-Suu-live.out`) | 114 bytes / 3 lines |

All well under 65,536 bytes, so the base census's `printf | grep -q` / `printf | head -n3` cannot take SIGPIPE
here — consistent with §4/§5 showing the same packages and update-safety lines from both revisions. The change's
only *exercised* evidence on this host is therefore the selftest (§2/§3) plus the frozen counter's fixture twins
(not my item; not run by me). This is a statement of headroom, not of the fix being useless: a host with a
degraded `-Qkk` and a 400+ sample, or a real 4002-candidate update set, crosses the buffer.

## 8. Diff-hunk scope (from my side of the C1 kill rule)

`diff -u base.sh c.sh` → `base-tip.diff`, six hunks: `@@ -689,9 +689,12 @@`, `@@ -1618,7 +1621,7 @@`,
`@@ -1632,14 +1635,14 @@`, `@@ -1649,7 +1652,7 @@`, `@@ -2344,6 +2347,16 @@`, `@@ -2540,6 +2553,18 @@`.
Against the function map of `c.sh` (`grep -nE '^[a-z_]+\(\) \{'`): `probe_packages` 654-813,
`probe_update_safety` 1552-1819, `run_selftest` 1931-3109. All six hunks fall inside those three functions
(689 ∈ packages; 1618, 1632, 1649 ∈ update-safety; 2344, 2540 ∈ selftest). **No hunk outside the allowed set** —
the declared kill rule's scope condition holds for the two revisions I measured.

## What I did not do

- Did not run the frozen counter `tools/score-size-invariance-r42.py` (not my item; the host is shared and the
  counter is the parent's).
- Did not run `base.sh --selftest` (128-case base count taken from the declaration, not re-measured).
- Did not run the census under `--sample` other than 400, and did not run any mutating pacman verb, service
  action, mount or scrub command; every live command was read-only (`pacman -Qq/-Qkk/-Qu/-Sup/-Suu`, `/proc` reads).
- No tools installed or upgraded (no pacman, no uv, no binary fetch). No package, service, sysfs or /etc change.
- `live-base2.out` (the drift control, §6) **is** in the receipt dir (sha256 `104203d1d01a…53e1ecfb`); §6 quotes
  its full field diff, and `live-base.out`, `live-tip.out`, `smp-base.out`, `smp-tip.out` are retained so every
  base-vs-tip comparison above is reproducible from receipts alone.
