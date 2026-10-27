VERDICT: supports

# C1-4 — kill rule "the census writes a file in live or identity mode": NOT triggered

IMPL `a44770491eb5ca15ce9f8b3207309d1af683ffaf:tools/tsukuroi-census.sh`
(sha256 `d925839cde9737fbd624ad2302671671c7ecc4e9a9331a1ff5a2ad1839112cfa`, 209208 B, 3598 lines),
BASE `2042117cfb724170772f4c128cc2ddba0b61d817:tools/tsukuroi-census.sh`
(sha256 `237b21c9d757e339943c29b0f005faf569ff997deca46dd5bce16bc631b5fcdc`, 3485 lines).
Both exported with `git show <rev>:tools/tsukuroi-census.sh` to
`/fast/scratch/hyaku/tsukuroi-r46/C1ExecLiveWrite/{impl,base}/census.sh`; `TMPDIR` inside that scratch dir.
Receipts: `.ufo/waves/round-46/w1/C1ExecLiveWrite/`.

## Method (strace 7.2, `/usr/bin/strace --version` → "strace -- version 7.2")

| run | command | out |
|---|---|---|
| live | `strace -f -e trace=%file,write -o tr/impl-live.trace /bin/bash impl/census.sh` | exit 2, `TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=BLOCKED oom=DEGRADED)` (14 lines) |
| identity | `strace -f -e trace=%file,write -o tr/impl-identity.trace /bin/bash impl/census.sh --identity` | exit 0, one identity line |
| stdin | `strace -f -e trace=%file,write -o tr/impl-stdin.trace /bin/bash -s -- --identity < impl/census.sh` | exit 0, `verified=no` |
| base live | `strace -f -e trace=%file,write -o tr/base-live.trace /bin/bash base/census.sh` | exit 2, same BLOCKED line |
| identity execs | `strace -f -e trace=execve -o tr/impl-identity-exec.trace … --identity` | exec set below |
| live execs | `strace -f -e trace=execve,%file -o tr/impl-live-exec.trace …` (live) | attribution + plane probes |

Filter (`OPEN=open|openat|openat2|creat` carrying `O_CREAT|O_WRONLY|O_RDWR|O_TRUNC|O_APPEND`, plus every
`mkdir|mkdirat|unlink|unlinkat|rename|renameat{,2}|symlink|symlinkat|link|linkat|rmdir|truncate|ftruncate|chmod|fchmodat|chown`)
applied by `python3` to each trace, with pid prefixes stripped, heap `0x…` masked and thread tid → `TID`.

## Total per mode (receipts `impl-live.mutations.txt`, `impl-identity.mutations.txt`, `impl-stdin.mutations.txt`)

| mode | writable opens | namespace mutators (mkdir/unlink/rename/symlink/link/…) | succeeded outside /dev/null, /dev/nvidia*, /proc/self/task/TID/comm |
|---|---|---|---|
| live | 367 (13 distinct) | 18 (13 distinct), **every one `-1`** | **none** |
| `--identity` | 8, all `/dev/null` | **0** | **none** |
| `bash -s -- --identity` (stdin) | 2, both `/dev/null` | **0** | **none** |

## Live mode: complete writable-open / mutator list by path

```
  18  openat(AT_FDCWD, "/dev/null", O_RDWR) = 0
  11  openat(AT_FDCWD, "/dev/null", O_RDWR) = 3
 324+2 openat(AT_FDCWD, "/dev/null", O_WRONLY|O_CREAT|O_TRUNC, 0666) = 3 / <unfinished>
   1  openat(AT_FDCWD, "/dev/tty", O_RDWR|O_NONBLOCK) = -1 ENXIO
   1  openat(AT_FDCWD, "/dev/nvidiactl", O_RDWR) = 9
   1  openat(AT_FDCWD, "/dev/nvidia0", O_RDWR|O_NONBLOCK|O_CLOEXEC) = 10
   1  openat(AT_FDCWD, "/dev/nvidia0", O_RDWR|O_CLOEXEC) = 11 ; 1 = 13
   1  openat(AT_FDCWD, "/dev/nvidia-uvm", O_RDWR|O_CLOEXEC) = 11 ; 1 = 13
   3  openat(AT_FDCWD, "/etc/pacman.d/gnupg/trustdb.gpg", O_RDWR) = -1 EACCES
   3  openat(AT_FDCWD, "/etc/pacman.d/gnupg/.#lk0x<heap>.plazir27.<pid>", O_WRONLY|O_CREAT|O_EXCL, 0644) = -1 EACCES
   1  openat(AT_FDCWD, "/proc/self/task/<tid>/comm", O_WRONLY|O_CREAT|O_TRUNC, 0666) = 9
   2  mkdir("/dev/nvidia-caps", 0755) = -1 EEXIST
   8  symlink("../nvidia0|../nvidiactl|../nvidia-caps/nvidia-cap1|nvidia-cap2|../nvidia-uvm|../nvidia-uvm-tools", "/dev/char/195:0|195:255|240:1|240:2|237:0|237:1") = -1 EEXIST
   8  unlink("/dev/char/195:0|195:255|237:0|237:1|240:1|240:2") = -1 EACCES
```
No `rename`, `link`, `truncate`, `chmod`, `chown`, `rmdir` call appears in any trace.

Attribution of the only `/dev` mutators: pid 3736408 `execve("/usr/bin/nvidia-smi", ["nvidia-smi", "--query-gpu=name,driver_version", "--format=csv,noheader"])`
(`tr/impl-live-exec.trace:11215`), then `unlink("/dev/char/195:255") … = -1 EACCES`, `symlink("../nvidiactl", "/dev/char/195:255") = -1 EEXIST`
(`tr/impl-live-exec.trace:11219+`). The gpg lock is a child of `pacman`: the `…/gnupg/.#lk…` line in `tr/impl-live-exec.trace` sits at line 550, 400 lines after
`execve("/usr/bin/gpg", ["gpg", "--enable-special-filenames", …, "--status-fd", "8"…])`, and `grep -c 'execve("/usr/bin/pacman"'` = 3 — matches the 3 lock attempts.
`/proc/self/task/<tid>/comm` is the kernel per-thread name write glibc performs on thread creation; it creates no file.

## Live vs base: no new mutator

Receipt `live-vs-base.diff.txt`:
```
writable-opens        impl=367 (13 distinct)   base=366 (13 distinct)
namespace-mutators    impl=18 (13 distinct)    base=18 (13 distinct)
namespace-mutator multiset identical : True
only-in-impl opens: []   muts: []
only-in-base opens: []   muts: []
namespace mutators that SUCCEEDED in impl live: []
```
The single 367-vs-366 line is an strace interleaving artifact, not a call: base records one extra
`openat(AT_FDCWD, "/dev/null", O_RDWR <unfinished ...>` fragment line that impl records only as its resumed `= 0` result.
Base `base-live.mutations.txt` shows the same 18 mutators, the same nvidia paths and the same three EACCES gpg lock attempts.

Empirical cross-check (no trace): three runs inside an empty dir `iso/` with `TMPDIR=iso/tmp` and a pre-touched `iso/.marker`,
then `find iso -newer iso/.marker -not -path 'iso/tmp*'` → **empty**; `find iso/tmp` → `iso/tmp` only (no mktemp dir); `ls -A` of the scratch root shows no stray file.
Live exit 2, `--identity` exit 0, stdin `--identity` exit 0 — the census leaves nothing behind.

## `--identity` performs no plane probe

`strace -f -e trace=execve` on `--identity`, full set (receipt `impl-identity.execs.txt`):
```
1 execve("/bin/bash"
3 execve("/usr/bin/cut"
1 execve("/usr/bin/md5sum"
2 execve("/usr/bin/readlink"
2 execve("/usr/bin/sha256sum"
2 execve("/usr/bin/wc"
```
`pacman`, `systemctl`, `journalctl`, `dmesg`, `nvidia-smi`, `findmnt`: **0 execs**. For contrast the same grep on the live run gives
`dmesg`=1, `journalctl`=10, `nvidia-smi`=1, `pacman`=3, `systemctl`=9 (`impl-live.execs.txt`). The identity path in the source is
`tools/tsukuroi-census.sh:3513-3518` (`if [ "$identity" -eq 1 ]; then` … `census_identity; exit 0`) — it returns before `probe_packages`.

## The identity bytes are the running file

`tr/impl-identity.out`:
`TSUKUROI_CENSUS_IDENTITY: version=census-v2 sha256=d925839…12cfa md5=db08a606ce128da3839457372e91e220 bytes=209208 lines=3598 planes=packages,systemd,drivers,journal,update-safety,oom exit_map=0:HEALTHY,1:DEGRADED,2:BLOCKED verified=yes`
Independently: `git show a4477049…:tools/tsukuroi-census.sh | sha256sum` = `d925839…12cfa`; `md5sum impl/census.sh` = `db08a606…220`;
`wc -lc` = `3598 209208`. Matches `ls -l` size 209208. The descriptor route is visible in the trace:
`newfstatat(AT_FDCWD, "/proc/3155917/fd/255", {st_mode=S_IFREG|0755, st_size=209208, …}, 0) = 0`, `readlink("/proc/3155917/fd/255", …)`,
then five `openat(AT_FDCWD, "/proc/3155917/fd/255", O_RDONLY) = 3` (sha256, md5, wc -c, wc -l, sha256 again) —
all `O_RDONLY`, no path is hashed on trust.
`tr/impl-stdin.out`: `sha256=unverifiable … verified=no`, exit 0, and its trace carries no writable open of any file but `/dev/null`.

## Scope note

This item is the strace half of the kill rule only. I did not run `score-census-identity-r46.py` (the other C1 seats own the counter and
its ~1.5 min selftest); I read `tools/score-census-identity-r46.py` (12408 B) only to confirm it exists and was not touched by me.

## Risks / notes (none triggers the kill rule)

1. Live mode does make **three denied** `openat(…/#lk…, O_WRONLY|O_CREAT|O_EXCL)` attempts from gpg under `pacman`
   (`tr/impl-live.trace`), all `EACCES`; identical in base, and `pacman` is unprivileged here. If a future census ran as root,
   the packages plane would create a gpg lock file in `/etc/pacman.d/gnupg` — pre-existing plane behaviour, not `--identity`,
   and still not a census-authored file. `--identity` never execs `pacman`.
2. `strace -f` shows 324+ `/dev/null` `O_WRONLY|O_CREAT|O_TRUNC` opens in live and 8 in identity, each from a child immediately
   before its `execve`; `/dev/null` is a character device that already exists, so `O_CREAT` creates nothing.
3. Not done by me: no `--selftest` run, no C1/C2 counter run, no lane git mutation (read-only `git show` only).

## Receipts (`.ufo/waves/round-46/w1/C1ExecLiveWrite/`)

`impl-live.mutations.txt`, `base-live.mutations.txt`, `impl-identity.mutations.txt`, `impl-stdin.mutations.txt`,
`live-vs-base.diff.txt`, `impl-identity.execs.txt`, `impl-live.execs.txt`, `impl-identity.out`, `impl-stdin.out`,
`impl-live.trace.gz`, `base-live.trace.gz`, `impl-identity.trace.gz`, `impl-stdin.trace.gz` (gzipped full straces, ≤237 KB each).
Scratch `/fast/scratch/hyaku/tsukuroi-r46/C1ExecLiveWrite/` removed after the copy.
No tool was installed or upgraded for this item.
