VERDICT: supports

# C1-9 — census selftest no-harm / operability (lane working tree)

Item: run `TMPDIR=/fast/scratch/hyaku/tsukuroi-r38/C1ExecSelftestTmp bash tools/tsukuroi-census.sh --selftest`
at the lane worktree, confirm the summary line (expected PASS 111/111), snapshot `ls /tmp | sort` before and
after and report any new `/tmp` entry the selftest left or used, then run the base revision's selftest
(`8bd001f58b…:tools/tsukuroi-census.sh`) and report its summary so the case delta is measured.

All four requirements hold. Head reports `PASS (111 cases, 111 passed, 0 failed)`, base reports
`PASS (105 cases, 105 passed, 0 failed)`, the delta is exactly 6 and is exactly the six R38-C1 storage cases, and
the head selftest made **zero** filesystem syscalls on any `/tmp` path (strace-verified), so the `/tmp` entries that
appeared in the snapshot window are not its own.

## 1. The file I ran is exactly the declared implementation (no drift)

```
$ sha256sum tools/tsukuroi-census.sh
8e0084f67ad4783a980d5c2eaba453f51f1fc5d75408a1c9021a7249ac9aba1c  tools/tsukuroi-census.sh
$ git show 52ffd65f868431f021b8615ab281efd87195eac6:tools/tsukuroi-census.sh | sha256sum
8e0084f67ad4783a980d5c2eaba453f51f1fc5d75408a1c9021a7249ac9aba1c  -
$ git show master:tools/tsukuroi-census.sh | sha256sum      # same 8e0084f6…
$ git show HEAD:tools/tsukuroi-census.sh   | sha256sum      # same 8e0084f6…
$ git -C <lane> diff --quiet master -- tools/tsukuroi-census.sh; echo $?
0
```

Worktree = master = HEAD (`5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf`, `2026-10-26 01:33:02 -0300`) = the
declared C1 implementation commit `52ffd65f`. The storage arm is present in the file I ran:
`probe_storage_arm()` at `tools/tsukuroi-census.sh:1848`, `STORAGE_LINE` at `:1884`, contract at `:353`, and the
six `R38-C1` selftest cases at `:2890`–`:2921`. Lane file untouched by my runs: mtime `2026-10-26 01:17:37`, size
167654, sha unchanged before and after (receipts `transcript.txt`).

## 2. Head selftest at the lane worktree: PASS 111/111

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
$ TMPDIR=/fast/scratch/hyaku/tsukuroi-r38/C1ExecSelftestTmp bash tools/tsukuroi-census.sh --selftest
exit=0
TSUKUROI_CENSUS_SELFTEST: PASS (111 cases, 111 passed, 0 failed)
```
Receipt `C1ExecSelftestTmp/selftest-head.out:114`; that file is exactly 114 lines = 111 `^PASS` + 2 `^SKIP` +
1 summary, `grep -c '^FAIL'` = 0. The two skips are the suite's own named, unconditional skips
(`tools/tsukuroi-census.sh:2729` non-root-owned root fixture, `:2732` EACCES/000 subtree), identical at base
(`base.sh:2664`, `:2667`) and identical in every run mode here — they are not passed cases and are not counted in
the 111.
Run twice independently (plain, and under strace): both `PASS (111 cases, 111 passed, 0 failed)`
(`selftest-head.out:114`, `selftest-strace.out:114`). Wall time ~20 s plain, ~48 s under `strace -f`.

## 3. `/tmp` before/after: the selftest left and used nothing in `/tmp`

Snapshots (`C1ExecSelftestTmp/tmp-before.txt` 31 entries, `tmp-after-head.txt`, `tmp-after-both.txt`):

```
$ diff tmp-before.txt tmp-after-head.txt      # window = the head --selftest run
5a6  > frc.txt
6a8  > k37-c1-bko06bvb
26c28 tabi-binding-selftest-4TkXl4 -> tabi-binding-selftest-G7W9XN
```

Attribution — the three deltas are **peers', not the selftest's**:

- `frc.txt` (`mtime 01:54:44`, in-window) is a fleet knowledge-fixture receipt, not census output:
  `head -2 /tmp/frc.txt` → `PASS     F01  knowledge/cvss-v4-severity-and-vector.md  ids=S001  exit=0`
  (the census selftest embeds no `knowledge/…` fixture and never writes to `/tmp` under a set `TMPDIR`).
- `k37-c1-bko06bvb` (`mtime 01:54:49`, in-window) is another seat's fixture tree: `ls k37-c1-bko06bvb` →
  `fx/` (66 entries) and `gates/`; name prefix `k37-`, not the census's `tsukuroi-r3-2-selftest.XXXXXX`.
- `tabi-binding-selftest-*` is a tabi-binding fixture that was renamed by its owner mid-window.

Decisive check — I traced the identical command (same `TMPDIR`) with
`strace -f -qq -e trace=mkdir,mkdirat,creat,unlink,unlinkat,rename,renameat,renameat2,link,linkat,symlink,symlinkat,openat`
(64 MB trace, receipt `trace-excerpts.txt`):

```
== head trace /tmp refs: 0 / total refs to TMPDIR: 37661
== head trace path prefixes:  165491 "/usr   37668 "/fast   35141 "/etc   11061 "/dev   4138 "/proc   3780 "/sys   1 "/nonexistent-r35
== head trace lane refs: 0
```

Zero references to any `/tmp` path. Write/delete audit of the same trace: 0 `creat()` calls, 0 `openat` with
`O_WRONLY|O_RDWR|O_CREAT` outside `/dev/*` and the scratch work dir, 0 `unlink`/`mkdir`/`rename` touching `/etc` or
`/usr`, 0 absolute unlink targets outside the work dir, and the 993 `mkdir("/fast")` calls are all
`-1 EEXIST` (component probes of `mkdir -p`, no effect). All 8,573 distinct paths live inside
`/fast/scratch/…/C1ExecSelftestTmp/stracetmp/tsukuroi-r3-2-selftest.Ue4A8n`, the work dir is removed at exit by
`trap … rm -rf` (`tools/tsukuroi-census.sh:1895`), and the only lane access in the whole trace is
`openat(AT_FDCWD, "tools/tsukuroi-census.sh", O_RDONLY)` (3× — the script reading itself). `/tmp` was noisy from
the fleet throughout (two other `/tmp/tsukuroi-r3-2-selftest.*` dirs — `NqcWvu` at 01:58:39 and `8nGutB` at ~01:59
— appeared and vanished while no census of mine was running), so a bare `ls /tmp` diff is not attributable on this
host; the trace is.

## 4. Base selftest (`8bd001f5`): PASS 105/105, and it ignores `TMPDIR`

```
$ git show 8bd001f58bfda29c92d90d2a7a413825c0ca9fcb:tools/tsukuroi-census.sh > base.sh
$ sha256sum base.sh
62c0e39a135bdda68cb6fd1a42936de2f33e15b7d5e4e49591d60aa5755482ac  base.sh
$ bash base.sh --selftest
exit=0
TSUKUROI_CENSUS_SELFTEST: PASS (105 cases, 105 passed, 0 failed)
```
Receipt `C1ExecSelftestTmp/selftest-base.out:108` (108 lines = 105 `^PASS` + 2 `^SKIP` + 1 summary), 0 `^FAIL`;
reproduced under strace (`selftest-base-strace.out:108`). This is a measured 105, not the expected one.

Delta measured by set difference of case titles, not asserted:

```
$ LC_ALL=C comm -23 h.txt b.txt   # 6 lines, only in head
healthy rollup: a missing counter is BLOCKED; the healthy sibling device still counts
healthy rollup: a mounted filesystem with no readable devinfo is BLOCKED
healthy rollup: a repeated counter or extra line is malformed, never a pass
healthy rollup: nonzero lifetime counters read DEGRADED on the STORAGE line only; 010 is ten, not octal
healthy: five zero counters on one device; features and non-fsid names ignored
healthy: no btrfs sysfs root reads as no btrfs filesystem, 0/0/0
$ LC_ALL=C comm -13 h.txt b.txt   # empty — nothing was removed from base
$ grep -c R38-C1 selftest-base.out → 0 ; selftest-head.out → 6
```
111 − 105 = 6, and the six are exactly the declared "6 selftest cases" of the storage arm. No case was dropped or
reworded (base-only set empty).

Operability delta worth naming: the **base** hardcodes the temp root and ignores `TMPDIR` —
`base.sh:1828  work=$(mktemp -d /tmp/tsukuroi-r3-2-selftest.XXXXXX)` — whereas head honours it —
`tools/tsukuroi-census.sh:1892  work=$(mktemp -d "${TMPDIR:-/tmp}/tsukuroi-r3-2-selftest.XXXXXX")`. Measured on
the base run with `TMPDIR` set to my scratch: `mkdir("/tmp/tsukuroi-r3-2-selftest.gpSpZh", 0700) = 0`
(35,495 `/tmp` refs, 8,076 distinct paths), cleaned at exit by
`unlinkat(AT_FDCWD, "/tmp/tsukuroi-r3-2-selftest.gpSpZh", AT_REMOVEDIR) = 0`. Head made 0 such refs. So the
requested `TMPDIR=…` invocation is only no-harm at head, and that is a strict improvement, not a regression.

## 5. Boundary condition observed (pre-existing at base, not a round-38 regression)

Running `--selftest` as userns-root is not green, at head *and* at base, with the same single case:

```
$ unshare -rm bash -c 'mount -t tmpfs none /tmp; TMPDIR=<scratch>/nstmp bash tools/tsukuroi-census.sh --selftest'
TSUKUROI_CENSUS_SELFTEST: FAIL (111 cases, 110 passed, 1 failed)      # selftest-ns.out:114
$ … bash base.sh --selftest
TSUKUROI_CENSUS_SELFTEST: FAIL (105 cases, 104 passed, 1 failed)      # selftest-base-ns.out:108
FAIL case in both: 'healthy: an unreadable directory is reported, and its logged target is neither present nor gone (R35-C1)'
```
Cause: that case relies on `chmod 000 "$FX/etc/k"` (`tools/tsukuroi-census.sh:2871`, base `:2806`) producing
`find: … Permission denied`, which the arm counts at `:1813` (`grep -c ': Permission denied$'`) from the `find`
stderr captured at `:1811`; inside `unshare -rm` the tester is namespace root with `CAP_DAC_OVERRIDE`, so `find`
succeeds and the expected `unreadable=1` reads `unreadable=0`. Under the namespace the delta is still exactly 6
(110 vs 104, all six new cases passing).

This contradicts the suite's own stated policy 139 lines earlier in the same selftest: `:2730`–`:2732` — "No
000-parent fixture: it would leave an unreadable subtree for find/rm, and under euid 0 DAC is bypassed so the case
would be vacuous" — a named `skip`, not a check. The R35 case builds exactly that fixture (`:2871`) and therefore
does not degrade gracefully at euid 0: it becomes one hard FAIL (not a vacuous pass, not a skip). The fix that
matches the existing convention is to guard `:2871`–`:2873` with `if [ "$EUID" -eq 0 ]; then skip '…uid 0 bypasses
DAC'; else … fi`, as the suite already does for the EACCES metadata class. None of this touches the round-38
storage arm (all six R38 cases pass in every mode), and it is pre-existing at base, so it does not falsify the C1
claim; it is recorded because the q82 amendment normalises running counters inside `unshare -rm`, and the same
framing applied to `--selftest` would read 110/111 and be mistaken for a regression.

Minor robustness note (not a defect against this item): head's `mktemp -d "${TMPDIR:-/tmp}/…"` needs `TMPDIR` to
already exist — pointing `TMPDIR` at a missing directory gives
`mktemp: failed to create directory via template '…/tsukuroi-r3-2-selftest.XXXXXX': No such file or directory` and
exit 1 (observed, recorded in my first aborted ns attempt); base with a missing `TMPDIR` is unaffected because it
ignores the variable.

## 6. No harm beyond `/tmp`

No package, service, hook, sysfs, counter, boot or `/etc` change was made; no `pacman` transaction; no sudo; no tool
installed or upgraded (nothing was needed). No git/jj mutation in the lane and no writes outside my seat dir and my
scratch; the traced census run wrote nothing under the lane — no write-flag `openat`, `mkdir`, `unlink` or `rename`
on any lane path, its only lane access being `openat(AT_FDCWD, "tools/tsukuroi-census.sh", O_RDONLY)` (3×). Scratch
`/fast/scratch/hyaku/tsukuroi-r38/C1ExecSelftestTmp/` removed after the receipts were copied.

## Receipts (all under `.ufo/waves/round-38/w1/C1ExecSelftestTmp/`)

`selftest-head.out` (111/111) · `selftest-base.out` (105/105) · `selftest-strace.out` (111/111) ·
`selftest-base-strace.out` (105/105) · `selftest-ns.out` (110/111, userns) · `selftest-base-ns.out` (104/105,
userns) · `tmp-before.txt` · `tmp-after-head.txt` · `tmp-after-both.txt` · `h.txt`/`b.txt` (head/base case-title
sets used for the delta) · `trace-excerpts.txt` (strace path accounting for both revisions) · `transcript.txt`
(commands + observed output).

## Risks / limits of this evidence

- 111/111 and 105/105 are verified on this host only (Linux 7.2.11-arch1-1, GNU bash 5.3.20) and only in the plain
  (non-root, non-userns) mode the item specifies; the userns boundary is documented in §5 as a separate observation.
- `/tmp` attribution rests on strace of the same command with the same `TMPDIR`; the host `/tmp` is shared with
  dozens of concurrent seats, so snapshot diffs alone would have mis-credited `frc.txt` and `k37-c1-bko06bvb` to
  this item.
- I did not run the lane's other counters, the q82 arm, or any build/lint gate — out of scope for C1-9 and owned by
  the L1's post-integration gate.
