VERDICT: supports

# C1ExecFinalLiveRead — item C1-4: live syscall read-only read at the integrated tip

Measured at revision `8eee79db608b5815c325a5af7cbfdeac50eda9f4` (census sha256
`2ef86357c14aec3f4346f7ac9013cdda3b399d38bae67f4ca2e286e5a37c4639`). The scrub-record arm's live
window contains **29 syscalls, all read-only** (`newfstatat`/`faccessat2`/`openat O_RDONLY`/
`getdents64`/`read`), one pid, no child. Across the whole census the only write-class calls open
pre-existing nodes (`/dev/null`, `/dev/nvidia*`), procfs (`/proc/self/task/<tid>/comm`), or
system keyring paths the kernel denies (EACCES); **zero** path-creating syscall succeeds. The
SCRUB line prints at **line 12** in every live run, immediately after STORAGE and immediately
before the rollup, byte-identical across five runs; base `98020ece` prints no SCRUB line.

## A. Setup (identities and run set)

- Scratch: `/fast/scratch/hyaku/tsukuroi-r44/C1ExecFinalLiveRead`; `TMPDIR=$PWD/tmp`; every census
  execution ran with cwd inside that scratch dir (lane tree never used as cwd).
- `git clone -q --shared <lane> clone`; `remote remove origin`; `checkout -q 8eee79db…`.
  `git -C clone rev-parse --show-toplevel` → `/fast/scratch/hyaku/tsukuroi-r44/C1ExecFinalLiveRead/clone`;
  `rev-parse HEAD` → `8eee79db608b5815c325a5af7cbfdeac50eda9f4`.
- Base clone `clone-base` at `98020ece0674e0b569ee23aed10ffbee355b248e`; census sha256
  `7c9f79036782de951a69325fe6f5cc742d8acac4de389626026bc33d8f7877f9` (matches w1's base pin).
- Runs at the tip: A, B plain live; C `strace` write-class set only; D `strace` write-class set
  **plus** `write,read,newfstatat,statx,access,faccessat,faccessat2,getdents64,execve` (bracketing);
  E write-class set plus `execve` (program attribution). Base: one plain live, one E-style trace.
  **All seven executions exited 2** (BLOCKED, host-state driven; identical rollup terms at base).
- Traced write-class set: `openat,open,creat,mkdir,mkdirat,rename,renameat,renameat2,unlink,
  unlinkat,symlink,symlinkat,link,linkat`; `strace 7.2` (preinstalled, no install/upgrade).
- Receipts: `.ufo/waves/round-44/w2/C1ExecFinalLiveRead/` (7 census outputs, 3 gzipped traces,
  `arm-window-bracketed.txt`, `arm-window.txt`, `write-class-summary.txt`, `commands.txt`).

## B. Whole-run write-class inventory at the tip (373 rows)

`write-class-summary.txt` lists every group (program | syscall | flags | path | result). Totals:
355 write-intent `openat` rows + 18 path-mutating calls (`unlink` 8, `symlink` 8, `mkdir` 2), all
18 failed. **Zero** `creat`, `rename`, `renameat`, `renameat2`, `link`, `linkat`, `mkdirat`,
`unlinkat`, `symlinkat` rows exist at all (`grep -cE ' <call>\('` → 0 for each).

| count | program | syscall/flags | path | result | creates a file? |
|---|---|---|---|---|---|
| 225 | `awk` | `openat O_WRONLY\|O_CREAT\|O_TRUNC` | `/dev/null` | ok | no — pre-existing char device |
| 59 | `head` | `openat O_WRONLY\|O_CREAT\|O_TRUNC` | `/dev/null` | ok | no |
| 11 | `bash` | `openat O_WRONLY\|O_CREAT\|O_TRUNC` | `/dev/null` | ok | no |
| 10 | `stat` | `openat O_WRONLY\|O_CREAT\|O_TRUNC` | `/dev/null` | ok | no |
| 7+6 | `bash` (fork) | `openat O_RDWR` | `/dev/null` | ok | no |
| 5+2+1 | `gpgconf` | `openat O_RDWR` | `/dev/null` | ok | no |
| 4 | `awk` | `openat O_RDWR` | `/dev/null` | ok | no |
| 4 | `bash` (fork) | `openat O_WRONLY\|O_CREAT\|O_TRUNC` | `/dev/null` | ok | no |
| 3+1 | `gpg` | `openat O_RDWR` | `/dev/null` | ok | no |
| 3 | `find` | `openat O_WRONLY\|O_CREAT\|O_TRUNC` | `/dev/null` | ok | no |
| 1 | `gpgsm` | `openat O_RDWR` | `/dev/null` | ok | no |
| 1 | `nvidia-smi` | `openat O_WRONLY\|O_CREAT\|O_TRUNC` | `/proc/self/task/<tid>/comm` | ok (fd 9) | no — procfs, process's own thread name |
| 7 | `nvidia-smi` | `openat O_RDWR[|O_NONBLOCK]` | `/dev/nvidiactl`, `/dev/nvidia0` ×3, `/dev/nvidia-uvm` ×2 | ok | no — existing device nodes |
| 2+1 | `gpg` | `openat O_RDWR` | `/etc/pacman.d/gnupg/trustdb.gpg` | **-1 EACCES** | no |
| 3 | `gpg` | `openat O_WRONLY\|O_CREAT\|O_EXCL` | `/etc/pacman.d/gnupg/.#lk0x…plazir27.<pid>` | **-1 EACCES** | no — pacman keyring lock refused |
| 1 | `bash` | `openat O_RDWR\|O_NONBLOCK` | `/dev/tty` | **-1 ENXIO** | no |
| 8 | `nvidia-smi` | `unlink` | `/dev/char/{195:0 ×3,195:255,237:0,237:1,240:1,240:2}` | **-1 EACCES** | no |
| 8+2 | `nvidia-smi` | `symlink` / `mkdir` | `../nvidia0` ×3, `../nvidiactl`, `../nvidia-uvm`, `../nvidia-uvm-tools`, `../nvidia-caps/nvidia-cap{1,2}`, `/dev/nvidia-caps` ×2 | **-1 EEXIST** | no — link/dir already exists |

Zero write-class syscalls name the scrub/btrfs/timer surfaces:
`grep -E 'O_(WRONLY|RDWR|CREAT|TRUNC|APPEND)' … | grep -Eci 'scrub|/sys/fs/btrfs|timers\.target\.wants'` → `0`.
Base `98020ece` shows the same shape (355 write-intent rows, `unlink` 8 / `symlink` 8 / `mkdir` 2, all
failed); per-group child counts move a little run to run (`head` 57↔59, `find` 2↔3, `awk O_RDWR`
4↔5, `bash` fork `/dev/null` 7↔4) with **no new path class**, because they are dynamic `journalctl`
/ `find` child counts, not the arm.
No lock file appeared: `ls -la /etc/pacman.d/gnupg/ | grep -c '#lk'` → `0`.
`git -C clone status --porcelain` after all five tip runs → empty; the scratch `TMPDIR` (`tmp/`) is
still empty (`find tmp -mindepth 1 | wc -l` → `0`).

## C. The arm's own window — decisive measurement (bracketed by its two stdout writes)

`write(1, "STORAGE …")` at `21:55:43.663347`, `write(1, "SCRUB …")` at `21:55:43.664501`. The arm
runs entirely between them: **29 syscalls**, mix `12 newfstatat, 5 faccessat2, 6 getdents64,
4 openat, 2 read`; **one pid (2459546), zero `execve`** (no child), **zero write-class syscalls**
(no `O_CREAT`, `O_WRONLY`, `O_RDWR`, `O_TRUNC`; every `openat` is `O_RDONLY` or
`O_RDONLY|O_DIRECTORY`). Verbatim (`arm-window-bracketed.txt`):

```
2459546 21:55:43.663347 write(1, "STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0\n", 75) = 75
2459546 21:55:43.663437 newfstatat(AT_FDCWD, "/sys/fs/btrfs", {st_mode=S_IFDIR|0755, st_size=0, ...}, 0) = 0
2459546 21:55:43.663475 faccessat2(AT_FDCWD, "/sys/fs/btrfs", R_OK, AT_EACCESS) = 0
2459546 21:55:43.663497 faccessat2(AT_FDCWD, "/sys/fs/btrfs", X_OK, AT_EACCESS) = 0
2459546 21:55:43.663516 newfstatat(AT_FDCWD, "/sys/fs/btrfs", {st_mode=S_IFDIR|0755, st_size=0, ...}, 0) = 0
2459546 21:55:43.663538 openat(AT_FDCWD, "/sys/fs/btrfs/", O_RDONLY|O_NONBLOCK|O_CLOEXEC|O_DIRECTORY) = 3
2459546 21:55:43.663564 getdents64(3, 0x55d306d71c30 /* 4 entries */, 32768) = 136
2459546 21:55:43.663580 getdents64(3, 0x55d306d71c30 /* 0 entries */, 32768) = 0
2459546 21:55:43.663609 newfstatat(AT_FDCWD, "/sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e", {st_mode=S_IFDIR|0755, st_size=0, ...}, 0) = 0
2459546 21:55:43.663674 openat(AT_FDCWD, "/sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/", O_RDONLY|O_NONBLOCK|O_CLOEXEC|O_DIRECTORY) = 3
2459546 21:55:43.663704 getdents64(3, 0x55d306d71c30 /* 3 entries */, 32768) = 72
2459546 21:55:43.663720 getdents64(3, 0x55d306d71c30 /* 0 entries */, 32768) = 0
2459546 21:55:43.663750 newfstatat(AT_FDCWD, "/sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1", {st_mode=S_IFDIR|0755, st_size=0, ...}, 0) = 0
2459546 21:55:43.663786 newfstatat(AT_FDCWD, "/sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/scrub_speed_max", {st_mode=S_IFREG|0644, st_size=4096, ...}, 0) = 0
2459546 21:55:43.663809 faccessat2(AT_FDCWD, "/sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/scrub_speed_max", R_OK, AT_EACCESS) = 0
2459546 21:55:43.663831 openat(AT_FDCWD, "/sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/scrub_speed_max", O_RDONLY) = 3
2459546 21:55:43.663956 read(0, "0\n", 4096) = 2
2459546 21:55:43.664036 read(0, "", 4096) = 0
2459546 21:55:43.664143 newfstatat(AT_FDCWD, "/sys/fs/btrfs/features", {st_mode=S_IFDIR|0755, st_size=0, ...}, 0) = 0
2459546 21:55:43.664196 newfstatat(AT_FDCWD, "/var/lib/btrfs", 0x7ffea2d786c0, 0) = -1 ENOENT (No such file or directory)
2459546 21:55:43.664215 newfstatat(AT_FDCWD, "/var/lib/btrfs", 0x7ffea2d786c0, AT_SYMLINK_NOFOLLOW) = -1 ENOENT (No such file or directory)
2459546 21:55:43.664232 newfstatat(AT_FDCWD, "/etc/systemd/system/timers.target.wants", {st_mode=S_IFDIR|0755, st_size=138, ...}, 0) = 0
2459546 21:55:43.664251 newfstatat(AT_FDCWD, "/etc/systemd/system/timers.target.wants", {st_mode=S_IFDIR|0755, st_size=138, ...}, 0) = 0
2459546 21:55:43.664267 faccessat2(AT_FDCWD, "/etc/systemd/system/timers.target.wants", R_OK, AT_EACCESS) = 0
2459546 21:55:43.664282 faccessat2(AT_FDCWD, "/etc/systemd/system/timers.target.wants", X_OK, AT_EACCESS) = 0
2459546 21:55:43.664297 openat(AT_FDCWD, "/etc/systemd/system/timers.target.wants/", O_RDONLY|O_NONBLOCK|O_CLOEXEC|O_DIRECTORY) = 3
2459546 21:55:43.664320 getdents64(3, 0x55d306d71c30 /* 6 entries */, 32768) = 216
2459546 21:55:43.664341 getdents64(3, 0x55d306d71c30 /* 0 entries */, 32768) = 0
2459546 21:55:43.664364 newfstatat(AT_FDCWD, "/etc/systemd/system/timers.target.wants/btrfs-scrub@*.timer", 0x7ffea2d781c0, 0) = -1 ENOENT (No such file or directory)
2459546 21:55:43.664379 newfstatat(AT_FDCWD, "/etc/systemd/system/timers.target.wants/btrfs-scrub@*.timer", 0x7ffea2d781c0, AT_SYMLINK_NOFOLLOW) = -1 ENOENT (No such file or directory)
2459546 21:55:43.664501 write(1, "SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0\n", 114) = 114
```

`read(0, …)` is bash's `done < "$f"` stdin redirect on the speed_max file (read-only open on fd 3,
re-read through fd 0) — the value read is `0\n` (no limit). The **next stdout write on the census
pid is the rollup** at `21:55:43.681294` (`TSUKUROI_CENSUS: BLOCKED …`): the arm emits nothing else.
Source agrees: `probe_scrub_record()` (tip `tools/tsukuroi-census.sh:1965-2043`) contains only
index tests, shell globbing, and `while … read … done < "$f"`; `mktemp` appears only in the hermetic
selftest (`:2048`), never on the live path (`:348` comment: "Live mode creates no files").

## D. The SCRUB line and its position, twice (plain live runs A and B)

Run A (`live-run-a.txt`, header stamp `2026-10-27T00:55:08Z`), `nl -ba` lines 10-13:

```
    10	DRIFT pacnew-plane pacnew=3 pacsave=0 pacorig=0 unreadable=11 log_pacnew=3 log_pacsave=0 unlogged=0 gone=0 log=ok
    11	STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0
    12	SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0
    13	TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=BLOCKED oom=DEGRADED)
```

Run B (`live-run-b.txt`, `2026-10-27T00:55:13Z`), same lines 10-13:

```
    10	DRIFT pacnew-plane pacnew=3 pacsave=0 pacorig=0 unreadable=11 log_pacnew=3 log_pacsave=0 unlogged=0 gone=0 log=ok
    11	STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0
    12	SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0
    13	TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=BLOCKED oom=DEGRADED)
```

- **Position 12** in all five tip runs (A, B, C, D, E); exactly one SCRUB line each (`grep -c '^SCRUB '` → 1).
- The line is byte-identical in all five runs:
  `sha256` → `a891c3424a76c918132b90a980bd83e3d7af27f516f6112b620408da8056eb3e`.
- Order per source `:3412-3432`: DRIFT (`probe_pacnew_arm` :3412, print `$DRIFT_LINE` :3413) →
  STORAGE (`probe_storage_arm` :3416, print `$STORAGE_LINE` :3417) → `probe_scrub_record` :3420,
  `printf '%s\n' "$SCRUB_LINE"` :3421 → `roll=HEALTHY` :3423 → six `worse` calls :3424-3429 →
  rollup `:3431-3432`. Line 12 = after STORAGE, before rollup; confirmed live.
- Base `98020ece` (`live-base-plain.txt`): `grep -c '^SCRUB '` → **0**; the rollup sits at line 12.
  `diff` base vs tip (minus header stamp) shows exactly two changes: one volatile `PLANE drivers`
  memory-counter line and **one added line — the SCRUB line**. Exit code 2 both sides.

## E. What this means for the C1 kill rules (facts only; verdict is the counters')

- "the arm writes a file in live mode": at syscall level the arm performs no write-class call and
  creates nothing; whole-census write-class calls succeed only against pre-existing nodes
  (`/dev/null`, `/dev/nvidia*`, own `/proc` comm) and every attempted keyring lock is EACCES.
- "PLANE line / rollup / exit code change": rollup terms and exit code are equal at base and tip;
  the SCRUB line is verdict-neutral (referenced only at `:2039`, `:2041`, `:3421`), and the rollup
  is computed solely from `PKG_V SYS_V DRV_V JRN_V UPD_V OOM_V` (`:3423-3429`, printed `:3431-3432`).
- Live host facts: `/var/lib/btrfs` absent (traced ENOENT), `scrub_speed_max` = `0` mode 0644,
  `timers.target.wants` holds 4 non-scrub links → `state=NONE dir=absent … timers=0` is honest,
  not a short-circuit.

## F. Not done / limits

- Did not run either frozen counter, did not score selftests, did not mutate the lane: parent owns
  those gates. No git/jj mutation in the lane; the two clones are scratch, origin removed.
- The populated-record branch (`/var/lib/btrfs` present) cannot be exercised live without a host
  mutation; it stays covered by the `(R44-C1)` fixture cases (out of this item).
- The 84 MB full trace lives only in scratch (removed); the lane receipt keeps the bracketed window
  verbatim plus the three class-trace logs gzipped.
- Attribution caveat: 60 of 439 pids made traced calls without a preceding `execve` (bash forks
  performing redirections); they are labelled `bash(fork)`. Per-group child counts move between
  live runs (dynamic `journalctl`/`find` output), so the table is a profile, not a fixed count;
  the exact, stable facts are the 373-row total, the zero-success set, and the arm window.
- No installs/upgrades: `strace 7.2` was already present.

Files changed in the lane: only this report and its receipt directory (read-only seat).
Report path: `.ufo/waves/round-44/w2/C1ExecFinalLiveRead.md`; receipts: `.ufo/waves/round-44/w2/C1ExecFinalLiveRead/`.
