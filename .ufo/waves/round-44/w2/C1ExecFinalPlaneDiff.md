VERDICT: supports

# C1-3 — live back-to-back PLANE / rollup / exit-code diff, base `98020ece` vs integrated tip `8eee79db`

Kill rule under test (SCORECARD Round-44 declaration, C1 row): *"any PLANE line, the rollup line or the
census exit code changes on the live host between base and the measured revision; … the arm writes or
creates a file in live mode."* This item owns the first three legs plus a bounded measurement of the last;
the predecessor-storage-counter leg is another seat's.

Result: **the kill rule does not fire.** After dropping the timestamped header and the `SCRUB` line the two
revisions are indistinguishable: the only differing line in the whole capture is `PLANE drivers`, the only
differing tokens on it are six kernel memory/PSI readings, and every one of those six also differs between
two runs of the *same* revision with the same magnitudes. The rollup line is byte-identical in all six runs
and the exit code is `2` in all six. One traced tip run created no file, and no write-intent syscall touched
any scrub-arm path.

This is a re-measurement at the real integrated tip. The wave-1 seat (`w1/C1ExecPlaneDiff.md`) measured
`7e081698`; the arm's live body changed twice after that (`071ab0d1` hardening, `9608ebc3` sysfs-unreadable /
timer-dir branches), so only a measurement at `8eee79db` binds.

## 1. Provenance of the two scripts (read-only export, identity verified)

Exported with `git show <rev>:tools/tsukuroi-census.sh` into `/fast/scratch/hyaku/tsukuroi-r44/C1ExecFinalPlaneDiff/bin/`;
both copies are in the receipt dir, and `git hash-object` of each copy equals the blob the lane names:

| copy | revision | blob (`rev-parse <rev>:tools/tsukuroi-census.sh`) | sha256 of copy | lines |
|---|---|---|---|---|
| `base.sh` | `98020ece0674e0b569ee23aed10ffbee355b248e` | `18a1db6448358d7ecf4634570fcd2bf075eccb1b` | `7c9f79036782de951a69325fe6f5cc742d8acac4de389626026bc33d8f7877f9` | 3220 |
| `tip.sh` | `8eee79db608b5815c325a5af7cbfdeac50eda9f4` | `8a2a665c8c9ac1795ea52819ee565ae4f0b65b00` | `2ef86357c14aec3f4346f7ac9013cdda3b399d38bae67f4ca2e286e5a37c4639` | 3441 |

`SELF=${BASH_SOURCE[0]}` is used only on the selftest path (`tip.sh:455`, consumers `:2289` and `:2336`;
`check_cli` at `:2329` merely documents it); live mode
never reads it, so the scratch copies execute exactly the live-mode code the lane would run.

## 2. Run protocol

Driver `probe.sh` (in the receipt dir): `cd` into scratch, `TMPDIR` under scratch, then
`/usr/bin/bash bin/<rev>.sh > out-<rev>-<n>.txt 2> err-<rev>-<n>.txt`, three each, alternating
base → tip → base → tip → base → tip. Order is proven by the header timestamps, not by file names:

```
base-1  2026-10-27T00:55:40Z  rc=2  lines=12  stderr=0
tip-1   2026-10-27T00:55:43Z  rc=2  lines=13  stderr=0
base-2  2026-10-27T00:55:45Z  rc=2  lines=12  stderr=0
tip-2   2026-10-27T00:55:48Z  rc=2  lines=13  stderr=0
base-3  2026-10-27T00:55:51Z  rc=2  lines=12  stderr=0
tip-3   2026-10-27T00:55:53Z  rc=2  lines=13  stderr=0
```

Whole batch `real 0m16.033s` (`/usr/bin/time`, shell `time`); all six stderr captures are 0 bytes. Two extra
tip runs were traced with `strace -f` for the write audit (§7); they are not part of the 3+3 comparison.

## 3. Normalisation

The header is the **only** line carrying a timestamp: the analyser rejects the header with
`^tsukuroi-census census-v2 — host=\S+ — \d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ — read-only$` and then asserts no
remaining line matches `\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ`. That assertion held for all six captures
(`extra-timestamp-lines=0`). Lines starting `SCRUB ` are then dropped (base: 0 per run; tip: exactly 1 per
run). What remains is 11 lines per run for both revisions.

## 4. Line sequence — identical shapes, one inserted line only

```
PLANE packages / PLANE systemd / PLANE drivers / PLANE journal / PLANE update-safety / PLANE oom
HANDOFF ADJ-04 mori class=kill-events / HANDOFF ADJ-04 mori class=coredumps
DRIFT pacnew-plane / STORAGE btrfs-device-stats / TSUKUROI_CENSUS
```

All six normalised files have this exact line-kind sequence (`[structure] every kept file has the same line
kinds`). The tip emits one extra line between `STORAGE` and the rollup, exactly the declared addition, and it
is byte-identical in its three runs:

```
SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0
```

Those values are what this host allows: `/var/lib/btrfs` is absent (`dir=absent`), `/sys/fs/btrfs` has one
fsid with one device whose `scrub_speed_max` reads `0` (`limited=0`), and
`/etc/systemd/system/timers.target.wants` holds only `fstrim`, `paccache`, `snapper-cleanup`,
`snapper-timeline` (`timers=0`).

## 5. Diff after dropping header and SCRUB

### 5a. Exactly one line ever differs, and only in live counters

Token diff over all 15 pairs: the only differing line is `PLANE drivers`, 3–6 substituted `key=value` tokens
per pair. Derived field union over all 15 pairs:

```
{C5_pswp, C6_psi_some_avg300, C6_psi_full_avg300, C6_psi_full_total_us, C6_avail_kb, C6_shmem_kb}
```

Every other line — the other five PLANE lines with their notes, both HANDOFF lines, `DRIFT`, `STORAGE`, the
rollup — is byte-identical in all six runs. Masking exactly those six tokens and sha256-ing the remaining body
gives **one digest for all six runs**:

```
bfb313f33e3ea55f5ca0f9c2bb3aea685b56fed789d58f07d0e56f6e51b47dcb   base-1, base-2, base-3, tip-1, tip-2, tip-3
```

So the PLANE verdict words (`BLOCKED`/`HEALTHY`/`DEGRADED`) and PLANE notes, the rollup and its parentheses,
and the line count (after the declared insertion) carry no revision signal at all.

### 5b. The leftover differences recur between two runs of one revision

Field-set test: the cross-rev union and the same-rev union are **the same six fields**; the set difference
(cross minus same) is **empty** — there is no field that moves only when the revision changes. The same holds
per-pair in kind: the six same-rev pairs produce field sets of size 3–6, the nine cross-rev pairs 4–5, and
every cross-rev pair's field set is contained in a same-rev pair's field set.

Magnitude test — all 15 pairs with elapsed seconds from the header timestamps (`rate.txt`):

```
pair                kind         dt(s)  d_pswpin    d_psi_us     d_avail_kb
base-1-tip-1        cross-rev        3         8        3778        162968
base-1-base-2       same-rev         5      2132        4291        377136
base-1-tip-2        cross-rev        8      2133        7428        836512
base-1-base-3       same-rev        11      2140       44840        441076
base-1-tip-3        cross-rev       13      2154       73280        188508
tip-1-base-2        cross-rev        2      2124         513        214168
tip-1-tip-2         same-rev         5      2125        3650        673544
tip-1-base-3        cross-rev        8      2132       41062        278108
tip-1-tip-3         same-rev        10      2146       69502         25540
base-2-tip-2        cross-rev        3         1        3137        459376
base-2-base-3       same-rev         6         8       40549         63940
base-2-tip-3        cross-rev        8        22       68989       -188628
tip-2-base-3        cross-rev        3         7       37412       -395436
tip-2-tip-3         same-rev         5        21       65852       -648004
base-3-tip-3        cross-rev        2        14       28440       -252568
```

The class ranges are indistinguishable, and the extremes sit in the same-rev class as often as in the
cross-rev one:

```
same-rev : n=6  dt=[5..11]   d_pswpin=[8..2146]     d_psi_us=[3650..69502]   d_avail=[-648004..673544]
cross-rev: n=9  dt=[2..13]   d_pswpin=[1..2154]     d_psi_us=[513..73280]    d_avail=[-395436..836512]
largest |d_pswpin|:   same-rev 2146  vs  cross-rev 2154
largest |d_psi_us|:   same-rev 69502 vs  cross-rev 73280
```

`avail_kb` moves in both directions inside *both* classes. `psi full total` is non-decreasing over the batch
(`55759178, 55762956, 55763469, 55766606, 55804018, 55832458`) and an independent read right after the batch
gives `full … total=56902412`, i.e. still advancing — the values are the host's clocks, not the script's.
The interpretation is therefore direct: the six tokens are the live readings the drivers arm reports, and the
revision cannot move them — the widest `pswpin` and `psi` swings in the batch occur between two runs of the
same revision.

Ordering argument (static, `tip.sh`): the mem arm is probed at `:3380` and `PLANE drivers` printed at `:3388`,
while `probe_scrub_record` runs at `:3420` and `SCRUB_LINE` is printed at `:3421` — the added arm cannot
influence any PLANE value in its own run.

## 6. Exit code and rollup — identical

```
rc-base-1=2 rc-base-2=2 rc-base-3=2 rc-tip-1=2 rc-tip-2=2 rc-tip-3=2
```

One distinct rollup line across all six runs (base and tip byte-identical):

```
TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=BLOCKED oom=DEGRADED)
```

`2` is BLOCKED from `packages` + `update-safety`; it is the same on base and on tip, and the arm is not a
rollup term (`main-diff.txt`: the rollup and the `case` mapping are untouched, §8).

## 7. Live-mode write audit of the arm (kill-rule leg)

Three independent checks at tip, beyond the six compared runs:

1. **Filesystem snapshot** of `/var/lib/btrfs` (absent before and after), `/sys/fs/btrfs`,
   `/etc/systemd/system/timers.target.wants` and `/var/lib` (`btrfs*` entries) taken before and after the
   batch: `diff snap-before.txt snap-after.txt` is empty. A dedicated `TMPDIR` was empty after the batch
   (`tmpdir-entries-after=0`), and the scratch root holds no stray files.
2. **`strace -f` of a live tip run**, `trace=openat,open,creat,mknod,mknodat,mkdir,mkdirat,unlink,unlinkat,
   rename,renameat,renameat2,link,linkat,symlink,symlinkat,truncate,ftruncate,chmod,fchmod,fchmodat`
   (14 239 lines, gzipped in the receipt): **zero** write-intent opens on any scrub-arm path, **zero**
   successful create/mutate syscalls anywhere in the process tree. The only file syscalls on scrub paths are
   read-only — the census process itself opens `/sys/fs/btrfs/` and `…/devinfo/` as `O_DIRECTORY`,
   `…/devinfo/1/scrub_speed_max` as `O_RDONLY`, and the wants directory as `O_DIRECTORY`; `/var/lib/btrfs`
   is never opened at all (absent). The create attempts in the trace belong to `nvidia-smi` (drivers arm:
   `mkdir /dev/nvidia-caps`, `symlink ../nvidia* → /dev/char/*`) and all failed `EEXIST`/`EACCES`.
3. The census process's own write-intent opens in that trace are 11 shell redirections to the `/dev/null`
   character device (`O_WRONLY|O_CREAT|O_TRUNC` on an existing device creates nothing) and one `ENXIO` open
   of `/dev/tty`. None belongs to `probe_scrub_record`.

## 8. Static corroboration of "no PLANE change possible"

`git diff 98020ece 8eee79db -- tools/tsukuroi-census.sh` has **exactly one removed line** in the whole file —
the usage sentence that lists the printed lines. Everything else is additive: the header contract block, two
env-var entries, the two `SCRUB_DIR`/`TIMER_WANTS` defaults, the `probe_scrub_record` function, the four-line
`main()` wiring, and the selftest cases. No existing probe body, no rollup term and no `case "$roll"` arm was
edited, so no PLANE line, the rollup or the exit code can change except through live host state — which §5
measures.

For completeness on provenance of the tip: `8eee79db` itself only adds `btrfs-scrub.timer` to one selftest
fixture line; the live-body edits since wave 1 are `071ab0d1` and `9608ebc3` — the
`sysfs:unreadable`/`not-directory`/`absent` decision under `probe_scrub_record` (`tip.sh:2017-2022`) and the
`[ -d "$e" ] && continue` timer-directory exclusion (`tip.sh:2032`), both inside the arm, plus the hardening
selftest cases.

## 9. Limits and risks (what this measurement does *not* cover)

- One host, one btrfs filesystem, `scrub_speed_max=0`. The `dir=present`, records/`_tmp`/socket and
  `limited>0` branches of the arm are not exercised live here — they are selftest/counter territory, not
  this item's.
- `/var/lib/btrfs` is absent on this host, so `dir=absent` is the only live value seen; a host with records
  present is not covered.
- The hosts's counters move fast (psi full total advanced ~73 ms of stall across the 16 s batch); three runs
  per revision is enough to show the *same* drift appears within a revision, which is the required
  comparison, but not to estimate a rate.
- `strace -f` perturbs timing; it is used only for the write audit, never for the 3+3 diff.
- The predecessor-storage-counter leg of the kill rule (`score-storage-arm-r38.py`, `-r38-q82.py`,
  `score-storage-hidden-r39.py`, `score-size-invariance-r42.py`) is not measured here — separate seat.

## 10. Proposed text

No change. The kill rule stays as declared; this item passes at `8eee79db` and the wave-1 result at
`7e081698` is superseded by this measurement. If the L1 wants the evidence cited, the receipt path is
`.ufo/waves/round-44/w2/C1ExecFinalPlaneDiff/` (37 files, 760 KB) and this report.

## 11. Receipts

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-44/w2/C1ExecFinalPlaneDiff/`:
`base.sh`, `tip.sh` (exported copies), `script-sha256.txt`, `probe.sh`, `analyze.py`, `drift.py`, `rate.py`,
`out-{base,tip}-{1,2,3}.txt` (raw stdout), `rc-*.txt`, `rc.txt`, `headers.txt`, `timing.txt`,
`snap-before.txt`, `snap-after.txt`, `tmpdir.txt`, `analysis.txt`, `analysis.json`, `drift.txt`, `rate.txt`,
`containment.txt`, `main-base.txt`, `main-tip.txt`, `main-diff.txt`, `write-audit.txt`,
`trace-tip-write.log.gz`, `trace-tip-pids.log.gz`, `SHA256SUMS`. Scratch
`/fast/scratch/hyaku/tsukuroi-r44/C1ExecFinalPlaneDiff/` removed at exit.

No tool installs or updates; no pacman/sudo/service/mount/btrfs-scrub commands; no lane git/jj mutation
(only read-only `git show`/`git diff`/`git hash-object`/`git log`); no write outside this report, the receipt
dir above and the scratch dir.
