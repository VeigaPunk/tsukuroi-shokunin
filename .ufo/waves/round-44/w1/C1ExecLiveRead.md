VERDICT: supports

# C1ExecLiveRead — item C1-3: kill rule "the arm creates a file in live mode"

Measured at syscall level on the live host at revision `7e081698d4fc3c4ea944884fd093058de9909de1`
(census sha256 `fca419b4714f7d24314b8d5877f0992c7f326aa8ff80045743990d058e8eaa1c`).
The scrub-record arm creates nothing: in its complete syscall window it makes 29 calls, all read-only.
Across the whole live census no write-class syscall creates a file, and the revision's write profile is
identical to base `98020ece` (369 write-class rows each, same paths, same results).
Two live runs print the same SCRUB line in the same position (after STORAGE, before the rollup).

## A. Setup (evidence identities)

- `git clone --shared` of the lane into scratch, `remote remove origin`, `checkout 7e08169…`;
  `git -C clone rev-parse --show-toplevel` → `/fast/scratch/hyaku/tsukuroi-r44/C1ExecLiveRead/clone`;
  `rev-parse HEAD` → `7e081698d4fc3c4ea944884fd093058de9909de1`.
- Base clone `98020ec…`: census sha256 `7c9f79036782de951a69325fe6f5cc742d8acac4de389626026bc33d8f7877f9`.
- 7 live executions at the revision (2 plain, 5 under `strace`), 1 at base; `TMPDIR` and cwd inside
  `/fast/scratch/hyaku/tsukuroi-r44/C1ExecLiveRead`. **Every** run exited 2 (BLOCKED, host-state driven; see G.2),
  base also 2.
- Traced class set as specified: `openat,open,creat,mkdir,mkdirat,rename,renameat,renameat2,unlink,unlinkat,symlink,link`.
  Two runs widened this (`+write`; then `+newfstatat,statx,access,faccessat,faccessat2,getdents64,ftruncate,truncate,chmod,fchmodat,utimensat`)
  to bracket and enumerate the arm completely; `execve` was added in two runs **only** to map pid→program.
- Receipts: `.ufo/waves/round-44/w1/C1ExecLiveRead/` (commands.txt, 3 raw `strace` archives, 5 census outputs,
  `arm-window-29-syscalls.txt`, `write-syscall-summary.txt`).

## B. Write-class inventory of the whole live census, revision vs base

`write-syscall-summary.txt` (rows = program, syscall, flags, path, result). Totals **revision 369 = base 369**:

| # | program | syscall/flags | path | result | creates a file? |
|---|---|---|---|---|---|
| 308 | `bash` | `openat O_WRONLY\|O_CREAT\|O_TRUNC` | `/dev/null` | ok | no — pre-existing char device; `O_CREAT` is a no-op on an existing node |
| 18 | `bash` | `openat O_RDWR` | `/dev/null` | ok | no |
| 11 | `awk` | `openat O_RDWR` | `/dev/null` | ok | no |
| 2+1 | `nvidia-smi` | `openat O_RDWR [\|O_NONBLOCK]` | `/dev/nvidia0` | ok | no — existing device node, ioctl |
| 2 | `nvidia-smi` | `openat O_RDWR` | `/dev/nvidia-uvm` | ok | no |
| 1 | `nvidia-smi` | `openat O_RDWR` | `/dev/nvidiactl` | ok | no |
| 1 | `nvidia-smi` | `openat O_WRONLY\|O_CREAT\|O_TRUNC` | `/proc/self/task/<tid>/comm` | ok (fd 9) | no — procfs, the process's own thread name, kernel memory |
| 3 | `gpg` (under `pacman`) | `openat` | `/etc/pacman.d/gnupg/trustdb.gpg` | **-1 EACCES** | no |
| 3 | `gpg` (under `pacman`) | `openat O_WRONLY\|O_CREAT\|O_EXCL` | `/etc/pacman.d/gnupg/.#lk0x…plazir27.<pid>` | **-1 EACCES** | no — pacman's keyring lock; denied, so no lock file appeared |
| 8 | `nvidia-smi` | `unlink` | `/dev/char/195:0` ×3, `/dev/char/195:255`, `237:0`, `237:1`, `240:1`, `240:2` | **-1** | no |
| 8+2 | `nvidia-smi` | `symlink` / `mkdir` | `../nvidia0` ×3, `../nvidiactl`, `../nvidia-uvm`, `../nvidia-uvm-tools`, `../nvidia-caps/nvidia-cap{1,2}`, `/dev/nvidia-caps` ×2 | **-1 EACCES/ENOENT** | no |
| 1 | `bash` | `openat O_RDWR` | `/dev/tty` | **-1 ENXIO** | no |

**Zero successful `mkdir/mkdirat/unlink/unlinkat/rename/renameat/renameat2/symlink/symlinkat/link/linkat`** in the
revision trace *and* in the base trace:
`grep -hE '^[0-9:.]+ +(mkdir|mkdirat|unlink|unlinkat|rename|renameat|renameat2|symlink|symlinkat|link|linkat)\(' trb/t.* | grep -v '= -1' | wc -l` → `0`; same over `trbase/t.*` → `0`.
`git -C clone status --porcelain` after all 7 runs → empty: the census wrote nothing into the tree it ran in.

The bare `O_CREAT` opens are the census's own `2>/dev/null` / `>/dev/null` redirects
(`grep -c '2>/dev/null'` → 25, `'>/dev/null'` → 27 in the script; repeated inside loops), and
`clone/tools/tsukuroi-census.sh:348` states "Live mode creates no files (two find sweeps into shell variables, no mktemp)"
— the trace confirms that line at syscall level.

## C. The arm's own window — the decisive measurement

`write(1, "STORAGE …")` lands at `21:09:22.388089`, `write(1, "SCRUB …")` at `21:09:22.388924`;
the whole arm executes between them. **29 syscalls, all read-only** (`arm-window-29-syscalls.txt`, verbatim):

```
newfstatat /sys/fs/btrfs {IFDIR|0755}                     = 0
faccessat2  /sys/fs/btrfs R_OK / X_OK                     = 0
newfstatat  /sys/fs/btrfs                                 = 0
openat      /sys/fs/btrfs/ O_RDONLY|O_DIRECTORY           = 3
getdents64  /sys/fs/btrfs/ (4 entries, then 0)            = 136 / 0
newfstatat  /sys/fs/btrfs/1d02a454-…-89d60902af8e {IFDIR} = 0
openat      …/1d02a454-…/devinfo/ O_RDONLY|O_DIRECTORY    = 3
getdents64  …/devinfo/ (3 entries, then 0)                = 72 / 0
newfstatat  …/devinfo/1 {IFDIR}                           = 0
newfstatat  …/devinfo/1/scrub_speed_max {IFREG|0644,4096} = 0
faccessat2  …/devinfo/1/scrub_speed_max R_OK              = 0
openat      …/devinfo/1/scrub_speed_max O_RDONLY          = 3
newfstatat  /sys/fs/btrfs/features {IFDIR}                = 0
newfstatat  /var/lib/btrfs                                = -1 ENOENT
newfstatat  /var/lib/btrfs (AT_SYMLINK_NOFOLLOW)          = -1 ENOENT
newfstatat  /etc/systemd/system/timers.target.wants {IFDIR,st_size=138} = 0 (×2)
faccessat2  /etc/systemd/system/timers.target.wants R_OK / X_OK         = 0
openat      /etc/systemd/system/timers.target.wants/ O_RDONLY|O_DIRECTORY = 3
getdents64  /etc/systemd/system/timers.target.wants (6 entries, then 0)   = 216 / 0
newfstatat  /etc/systemd/system/timers.target.wants/btrfs-scrub@*.timer  = -1 ENOENT (×2)
```

No `O_CREAT`, no `O_WRONLY`, no `O_RDWR`, no `mkdir`, no `unlink`, no `rename`, no `symlink`, no `link`.
Over the entire run, syscalls naming the three scrub paths reduce to
`3 faccessat2( 6 getdents64( 9 newfstatat( 4 openat(` — every `openat` is `O_RDONLY`.

Source agrees by construction: `probe_scrub_record()` (`tools/tsukuroi-census.sh:1967`) contains only
`[ -e/-d/-r/-x/-f/-L/-S ]` tests, shell globbing, and `while … read … done < "$f"` (read-only open);
it runs no command and redirects nothing; its two path constants are `:494` (`SCRUB_DIR`), `:495` (`TIMER_WANTS`);
the line is assembled at `:2036-2038` and printed at `:3375-3376`.

## D. Attribution of the remaining write-class rows, by probe

- **Arm:** exactly the window in C — 0 write-class syscalls, 0 `/dev/null` opens. It is the only probe whose
  boundary I can bracket exactly, because it emits the two adjacent lines itself.
- **`bash` `/dev/null` opens (326):** the census's own `2>/dev/null` redirects inside the six plane probes and the
  DRIFT/STORAGE arms; `/dev/null` is pre-existing, so these create nothing.
- **`gpg` under `pacman` (6 opens, all EACCES):** packages / update-safety planes (`pacman -Qkk`, `pacman -Qu`) —
  it *tries* to create its keyring lock `/etc/pacman.d/gnupg/.#lk…` and the kernel refuses; no file appears.
- **`nvidia-smi` (drivers plane):** opens existing `/dev/nvidia*` nodes, one self-`comm` write, and failed
  `unlink`/`symlink`/`mkdir` on `/dev/char/*`, `/dev/nvidia-caps` (EACCES/ENOENT) — all present identically at base.
- **`awk` `/dev/null` `O_RDWR` (11):** awk invocations inside the plane probes; same count at base.
- Honest limit: I did **not** attribute each of the 337 `/dev/null` opens to one named probe — they are shell
  redirects emitted from loops, and bucketing them by the next stdout line is not sound (the next line can belong to a
  different child). What is exact is (i) the arm's window and (ii) the program class of every row.

## E. Two live runs — SCRUB line and line order (nl: DRIFT, STORAGE, SCRUB, rollup)

Run a (`live-run-a.txt`, 00:07:44Z) and run b (`live-run-b.txt`, 00:07:47Z) lines 9-13, identical in both:

```
HANDOFF ADJ-04 mori class=coredumps value=83 kind=dated-event state=prepared scope=boot0-merged selector=SYSLOG_IDENTIFIER
DRIFT pacnew-plane pacnew=3 pacsave=0 pacorig=0 unreadable=11 log_pacnew=3 log_pacsave=0 unlogged=0 gone=0 log=ok
STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0
SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0
TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=BLOCKED oom=DEGRADED)
```

- Same SCRUB line in **all 7** revision runs, `sha256(a891c3424a76c918132b90a980bd83e3d7af27f516f6112b620408da8056eb3e)`.
- Base `98020ec` (`live-base-98020ec.txt`): `grep -c '^SCRUB '` → `0`; `diff` of the two outputs shows exactly one added
  line (the SCRUB line) in the revision, everything else equal except the header stamp and the live memory counters of G.1.
- Order per `:3371-3384`: STORAGE (`probe_storage_arm` `:3371`, `printf "$STORAGE_LINE"` `:3372`) → `probe_scrub_record` (`:3375`) → `printf "$SCRUB_LINE"` (`:3376`)
  → `local roll=HEALTHY` (`:3378`) → six `worse` calls (`:3379-3384`) → rollup. Confirmed live.

## F. What the arm measured on this host (facts, for C2's rows; no counted verdicts here)

- `/var/lib/btrfs` → `ls -ld` "No such file or directory"; traced `newfstatat` ENOENT → `dir=absent records=0`.
- `/sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/scrub_speed_max` → mode `-rw-r--r--` (0644),
  content `0`, read `O_RDONLY` → `limited=0` / no `speed_max=` detail. This live host corroborates SR8's 0644 RW
  attribute and "0 = no limit".
- `/etc/systemd/system/timers.target.wants` has 4 links (`fstrim`, `paccache`, `snapper-cleanup`, `snapper-timeline`),
  none `btrfs-scrub@*.timer` → `timers=0` (SR9's enable path is not in place here).
- Therefore `state=NONE` on this host means "no record dir, no enabled scrub timer, no throttle", not "a record exists".

## G. Risks / notes for the L1 (outside my item; no verdict claimed)

1. **The kill rule "a PLANE line changes … between base and the measured revision" cannot be a byte compare.**
   `PLANE drivers` carries live memory counters that move between two runs of the *same* revision:
   run a → run b (both `7e08169`): `C5_pswp=484418→484425`, `C5_sock_throttled=67758→68001`,
   `C6_psi_full_total_us=51218172→51236606`, `C6_avail_kb=18610068→18733744`. Whoever owns that kill rule must
   normalise those fields (or compare verdict tokens only), or it will fire spuriously.
2. **Host state, not the revision, drives the verdicts:** `PLANE packages: BLOCKED` because of
   `error: openai-chatgpt: missing required signature` from `pacman -Qkk`; `PLANE update-safety: BLOCKED`
   (`pacman -Qu` rc=1/2). Identical at base, so the rollup and exit code (2) are equal → the exit-code kill rule does not fire.
3. Verdict-neutrality is visible in the same trace (not my item): `SCRUB_LINE` is referenced only at `:2036`, `:2038`,
   `:3376`, and `roll` is computed solely from `PKG_V SYS_V DRV_V JRN_V UPD_V OOM_V` (`:3378-3384`).

## H. Not done / limits

- Did not run either frozen counter (`score-scrub-arm-r44.py`, `check-scrub-record-r44.py`) — parent owns the gates.
- Did not exercise the populated record branch live (`/var/lib/btrfs` present): impossible without a host mutation;
  it stays covered by the nine `(R44-C1)` fixture cases.
- Did not attribute the 337 `/dev/null` redirects to individual probes (see D); one host, one seat session.
- No tool installs/upgrades: `strace -- version 7.2` was already present (`/usr/bin/strace`).
- I did not write to, or run any mutating git/jj command in, the lane; the only writes are this report and the
  receipt directory. Scratch `/fast/scratch/hyaku/tsukuroi-r44/C1ExecLiveRead` removed after copying receipts.

Files changed in the lane: none (read-only seat).
Report path: `.ufo/waves/round-44/w1/C1ExecLiveRead.md`; receipts: `.ufo/waves/round-44/w1/C1ExecLiveRead/`.
