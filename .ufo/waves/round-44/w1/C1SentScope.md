VERDICT: defect-found

# C1-16 — safety review of the C1 counter and the scrub-record arm on this shared host

Seat C1SentScope, round 44 wave 1. Item: can `tools/score-scrub-arm-r44.py` leave mounts, files or
processes behind (SIGKILL mid-run, ENOSPC, a failing mkdir)? Does any path it writes escape
`--scratch`? Does the namespace child ever touch host `/var/lib`, `/sys` or `/etc`? Can the arm in
live mode be steered by a hostile file under `/var/lib/btrfs` into reading outside it or hanging?

Artifact under review, pinned:
`sha256(tsukuroi-shokunin/tools/score-scrub-arm-r44.py) = 1409a5fd75adaa4c0a238a7f9ad31621dd34a52ad1a40483e4a18d27c9536388`
— matches the declaration's frozen value, so this review is of the declared counter, not a later edit.
Census arm read at implementation `7e081698d4fc3c4ea944884fd093058de9909de1`
(`git -C <lane> show 7e08169…:tools/tsukuroi-census.sh`, 3396 lines; `probe_scrub_record` at
`tools/tsukuroi-census.sh:1967`, arm body 1996-2031 at that revision). No lane or fleet file was
modified; all scratch under `/fast/scratch/hyaku/tsukuroi-r44/C1SentScope/` (removed at the end).

Bottom line: **the four host-safety properties hold** — no host mount is ever created, nothing is
written outside `--scratch` (one file: `<work>/census.sh`), the namespace child cannot reach host
`/var/lib`, `/sys` or `/etc`, and a hostile record directory cannot make the arm read record content,
connect to a socket, or hang. **Six defects/limits were found**, all low severity because the first
five are confined to `--scratch` or to a private, host-invisible mount namespace.

---

## 1. Mounts, files, processes left behind

### 1.1 Cleanup path as written
`main()` creates the run dir and installs only INT/TERM handlers:

- `score-scrub-arm-r44.py:517` `os.makedirs(a.scratch, exist_ok=True)`
- `:518` `work = tempfile.mkdtemp(prefix='scrub-arm-r44.', dir=a.scratch)`
- `:523-524` `signal.signal(SIGINT/SIGTERM, on_signal)` → `SystemExit(128+signum)`
- `:527-529` `finally: subprocess.run(['chmod','-R','u+rwx',work]); shutil.rmtree(work, ignore_errors=True)`

The docstring claim is exactly this and no more: `:57` "everything the counter writes lives under it
and is removed on exit, SIGINT and SIGTERM". SIGKILL is not "exit", so the claim is not falsified —
but the item asks what SIGKILL leaves.

**SIGINT / SIGTERM: clean.** Sent while the namespace leg was live (ns child found at
`mnt:[4026533755]`, host ns `mnt:[4026531832]`):

```
--- SIGTERM: ns child at kill time [(1544891, 'mnt:[4026533755]')]
   parent rc=143 exit latency 0.02s; ns-leg survivors: [] residue: [] []
   host mounts unchanged: True
--- SIGINT:  parent rc=130 exit latency 0.02s; ns-leg survivors: [] residue: [] []
   host mounts unchanged: True
```

**SIGKILL mid-run: the work dir stays.** Kill at the moment the ns child exists
(`/proc/<pid>/cmdline` matches `r44lib`):

```
child found: [(1984326, 'PPid:\t1983401', 'mnt:[4026533752]')] at 0.09s
child lifetime after parent SIGKILL: 0.65s
residue: ['scrub-arm-r44.ihu78bky']      # census.sh + st/ inside
```

An earlier kill inside the live leg left the same shape: `work contents: ['census.sh', 'st']`,
`host mounts unchanged after kill: True`. This is **defect F1** (residue is bounded to `--scratch`
and is ~120 KB).

**Processes: normally none survive, but a grandchild can.** A user+mount-namespace child *does*
survive its parent's SIGKILL in general — control, with the counter's own flag shape:

```
control before kill: [(1960254, 'PPid: 3225996', 'mnt:[4026531832]'), (1960271, 'PPid: 1960254', 'mnt:[4026534008]')]
control after parent SIGKILL: [(1960271, 'PPid: 1494', 'mnt:[4026534008]')]
```

The counter's child died 0.65 s after the parent because its next write hit the closed stdout pipe,
not because anything kills it. And the per-case/`wired` timeouts kill only the direct `bash`
(`INNER:140-146`, `subprocess.run(..., timeout=...)`; `:149` `run(spec['call'], 60)`, `:152`
`run('bash /mnt/census.sh', 300)`, `:569` `timeout=1200`). Unit test of that exact helper extracted
from `INNER` (only `cwd` substituted, `timeout` unchanged) shows the leak:

```
A backgrounded grandchild -> ('timeout', 124) after 2.0s survivors [(4004579, 'python3 -c import time;time.sleep(45)  # R44HANG_A ')]
B foreground child      -> ('timeout', 124) after 2.0s survivors []
C exec-replaced child   -> ('timeout', 124) after 2.0s survivors []
```

So a scored revision that backgrounds a process leaves it running past the case timeout and past the
counter's own exit; while it lives it holds the private mount namespace and its four tmpfs mounts
(see §3). **Defect F2.**

### 1.2 Failing mkdir / ENOSPC
`--scratch` on an unwritable parent and on a regular file both fail *before* anything is created, but
they exit as a raw traceback, not the documented `{"verdict":"ERROR"}` + exit 2
(docstring `:58` "Output: one JSON line; exit 0 PASS, 1 FAIL, 2 usage/read/harness error"):

```
PermissionError: [Errno 13] Permission denied: '…/s/ro/sub'      rc=1
FileExistsError: [Errno 17] File exists: '…/s/notadir'           rc=1
```

By contrast the pre-flight revision check uses the documented path and *does* leave the scratch root
it created (empty):

```
{"counter": "score-scrub-arm-r44", "error": "cannot resolve deadbeef…", "verdict": "ERROR"}   rc=2
scratch entries: []            # s/pf1 exists, empty
```

**Defect F3** (contract violation on the harness-error path, no residue beyond the empty scratch root).

ENOSPC was **not exercised** (no pacman, no mount, no loop device available to this seat). The code
path is small enough to state: the only work-file write is one
`openat(…/scrub-arm-r44.k27r0998/census.sh, O_WRONLY|O_CREAT|O_TRUNC)` (`trace-parent-writes.txt`);
it is inside the `try` at `:525-529`, so ENOSPC there raises, `finally` removes `work`, and the
outcome is the same traceback-exit-1 as F3. ENOSPC *inside* the namespace (tmpfs) aborts at the
`mount`/write with `check=True` (`INNER:85-92`) → `die('namespace leg failed')` → JSON exit 2.

---

## 2. Does any path it writes escape `--scratch`?

No. Parent traced alone (`strace -y -e trace=openat,creat,unlink,unlinkat,rmdir,mkdir,mkdirat,rename,
renameat2,chmod,fchmodat,utimensat,truncate,symlink,mknodat python3 … --revision 7e08169…`; no `-f`,
so the run passed: `cases=16 correct=16 identity_ok=1 wired_ok=1 live_agree=1 selftest_pass=1
selftest_r44=9 verdict=PASS`):

```
parent openat for write: 2
  … "/fast/scratch/…/s/run3/scrub-arm-r44.k27r0998/census.sh", O_WRONLY|O_CREAT|O_TRUNC|O_CLOEXEC, 0666
  … "/dev/null", O_RDWR|O_CLOEXEC          # the chmod subprocess' DEVNULL
mutating calls: 6, all under --scratch:
  mkdir(…/run3) = -1 EEXIST; mkdir(…/scrub-arm-r44.k27r0998,0700); mkdir(…/st,0777)
  unlinkat(…, "census.sh", 0); unlinkat(…, "st", AT_REMOVEDIR); rmdir(…/scrub-arm-r44.k27r0998)
WROTE OUTSIDE SCRATCH: [] (only /dev/null)
```

The lane is only read: `git -C <lane> show` under `strace -f … -P <lane>/.git` produced no
`O_WRONLY|O_CREAT|O_RDWR` open and zero `unlink|unlinkat|rename|creat` calls; `rev-parse`/`show` are
the only git uses (`:533` `rev-parse`, `:537` `show`). `TMPDIR` is dropped from the child/live env (`clean_env`,
`:179`) and the selftest's `TMPDIR` is `<work>/st` (`:607-608`), so `tempfile` cannot fall back
to `/tmp`.

Note (not a residue): `os.makedirs(a.scratch)` respects a caller-supplied path, including a symlink —
the caller chooses it, so this is not an escape.

---

## 3. Does the namespace child touch host `/var/lib`, `/sys`, `/etc`?

No — and this is structural, not incidental.

**a. Propagation is private before any mount.** `unshare` is 2.42.4; the man page states "unshare
since util-linux version 2.27 automatically sets propagation to private in a new mount namespace".
Reproduced with the counter's exact flag shape (`unshare -m --map-users=$uid,0,1
--map-users=100000,1,65535 --map-groups=…`, no mounts):

```
inside ns: mounts=33 shared_tagged=0
host:      grep -c ' shared:' /proc/self/mountinfo = 33
```

Every host mount is `shared:N`; in the child every mount is untagged/private, so the four tmpfs mounts
cannot propagate.

**b. The child mounts tmpfs over exactly those paths, then works inside them.** `INNER:87` mounts
`r44lib` on `/mnt`, `INNER:93-95` mounts `r44view` on `/sys/fs/btrfs`, `/var/lib`,
`/etc/systemd/system`; only afterwards does `build()` chmod/rmtree entries (`INNER:103-139`). Mount
failure aborts the leg (`sh()` is `check=True`, `INNER:85-86`) *before* any removal, so a failed
mount can never expose a host directory to `shutil.rmtree`. Sampled live during a passing run:

```
child ns mnt:[4026533783] (host mnt:[4026531832]), mounts 37, tmpfs:
  '/mnt <- r44lib', '/sys/fs/btrfs <- r44view', '/var/lib <- r44view', '/etc/systemd/system <- r44view'
```

**c. Host side unchanged.** Full passing run (47 s, `run2-full-pass.json`):

```
host mounts unchanged: True  (33 -> 33)
host stat unchanged: True    # mtime/ctime/size/inode of /var/lib, /sys/fs/btrfs,
                             # /etc/systemd/system, /etc/systemd/system/timers.target.wants
leftover work dirs: []
```

**d. Not even in the orphan case.** In the SIGKILL trial the host table stayed 33 entries while the
orphan namespace was alive; a mount in a non-shared namespace is unreachable from the host table by
construction.

**Consequence worth recording (fidelity, not safety):** because `/var/lib` itself is over-mounted,
the W-leg census sees an *empty* `/var/lib` (no pacman db) and an empty `/sys/fs/btrfs`; the full
census still runs and the SCRUB/STORAGE ordering is scored, but the W leg is not a production view
for probes that read `/var/lib` or `/sys/fs/btrfs`. Only `/etc/systemd/system` is over-mounted, so
the census's `/etc` pacnew sweep (`census:1859` `find "$etc"`) still reads the host read-only.

**Limitation of this seat's tracing:** `strace -f` cannot trace the namespace leg end-to-end.
Traced children lose the setuid bit, so `newuidmap` fails and the counter reports
`{"error": "namespace leg failed: newuidmap: Could not set caps", "verdict": "ERROR"}` (rc 2,
`run1-strace-f-error.json`). This is why §2 traces the parent alone and §3 substitutes live
`/proc/<pid>/mountinfo` sampling plus the host-side diff. **Defect F4** (not a safety hole; a
verification/CI constraint — any ptrace-based supervisor or sandbox makes this counter ERROR).

---

## 4. Can a hostile file under `/var/lib/btrfs` steer the arm?

**Environment first:** `/var/lib/btrfs` does not exist on this host (`ls: cannot access
'/var/lib/btrfs': No such file or directory`; `/var/lib` is `directory 755`), and the live leg
agrees: `SCRUB btrfs-scrub-record state=NONE dir=absent …`. Creating entries there requires root, so
an unprivileged local process cannot plant anything today.

Behaviour was therefore tested against a fixture directory via the census's own override
(`TSUKUROI_SCRUB_DIR`/`TSUKUROI_TIMER_WANTS`; the *scored* live leg drops these in `clean_env`, so
the override cannot be used to steer a scored run):

Fixture: symlink record → `/etc/shadow`, mode-000 record, symlink `_tmp` → `/etc/shadow`, fifo
record, socket `scrub.progress.<fsid>`, a record name containing `\nTSUKUROI_CENSUS: BLOCKED
(forged)`, an out-of-tree fsid record. Result (0.01 s, `trace-arm-hostile-fixture.txt`):

```
SCRUB btrfs-scrub-record state=BLOCKED dir=present records=1 tmp=0 sockets=1 unreadable=1
  orphan=1 limited=0 timers=1 detail=record:not-regular,record:not-regular,tmp:not-regular
```

- **No content read:** zero `openat` of any `scrub.*` record (`grep openat trace-arm | grep 'scrub\.'
  | grep -v scrub_speed_max` → empty); the only write-capable open in the whole trace is bash's
  `/dev/tty O_RDWR|O_NONBLOCK = -1 ENXIO` — the arm creates no file (supports the "arm creates no
  file in live mode" kill rule).
- **No socket use:** zero `connect(`/`socket(` calls for the `scrub.progress.*` socket; `-S` is a
  stat (`census:2015` `[ -L "$e" ] || [ ! -S "$e" ]`).
- **No hang:** fifo, symlink-loop, `/dev/zero`, `/etc` (directory) and `/proc/self/root/…` variants
  all blocked in `elapsed 0.002s`, with `detail` reasons only — no name is ever echoed, so the
  newline-forged name cannot inject a line.
- **One residual dereference (F5):** the glob filter at `census:2003` is
  `[ -e "$e" ] || [ -L "$e" ] || continue` — `-e` *follows* a symlink before `-L` is tried. Proven:
  for the `/etc/shadow` symlink the trace shows a follow-stat returning the target's metadata
  (`{st_mode=S_IFREG|0600, st_size=942, ...}, 0`) followed by the `AT_SYMLINK_NOFOLLOW` stat. So an
  attacker who can write `/var/lib/btrfs` (root) can make the census stat arbitrary host paths —
  metadata only, never content, and nothing from it reaches the line — and could block the census
  only by pointing at a path on an already-unresponsive mount, since `stat` on a fifo/socket does not
  block. Impact is therefore bounded to (root-only) metadata probing and a theoretical stat hang;
  the arm has no internal timeout, so a hang would be stopped only by the counter's 300 s live-leg
  timeout (`:597`).

Also checked for completeness: the counter's own live oracle never opens a record — `live_model()`
uses `os.lstat` per entry and `os.access(p, os.R_OK)` for readability (`:478` `os.lstat`, `:482` `os.access`; only `:459-464` opens
`scrub_speed_max`), and opens
only `/sys/fs/btrfs/<fsid>/devinfo/<devid>/scrub_speed_max`, which is kernel-owned.

**Trust boundary (F6, by design):** the live and selftest legs run the scored revision's census with
the caller's full identity and no sandbox (`:597`, `:610` `subprocess.run(['bash', full] …)`), so
`--lane` is a code-execution input; the namespace legs are the only sandboxed ones, and there the
scored census runs as a subordinate uid with no host rights. Worth stating because it means a
candidate revision is executed before it is scored, at the scoring seat's privilege level.

---

## Findings, with the smallest remediation

| # | Sev | Finding | Evidence | Smallest remediation |
|---|-----|---------|----------|----------------------|
| F1 | low | SIGKILL mid-run leaves `<scratch>/scrub-arm-r44.*` (`census.sh`, `st/`); no trap can catch SIGKILL and no startup sweep exists | §1.1 | at start, remove `scrub-arm-r44.*` dirs under `--scratch` owned by this uid before `mkdtemp` |
| F2 | low | timeouts (`:149` 60 s, `:152` 300 s, `:569` 1200 s) kill only the direct `bash`/`unshare` child; a backgrounded grandchild survives the timeout and the counter, pinning the private mount namespace | §1.1 unit test A + control | `start_new_session=True` on the ns child and on `INNER`'s per-case `run()`, then `os.killpg(pgid, SIGKILL)` on `TimeoutExpired` |
| F3 | low | unpreparable `--scratch` (EACCES/ENOTDIR/ENOSPC) exits 1 with a traceback instead of the documented one-JSON-line exit 2 | §1.2 | wrap `:517-518` in `try/except OSError: die(f'cannot prepare scratch: {e}')` |
| F4 | info | cannot be traced end-to-end: under `strace -f`, `newuidmap` loses privilege and the ns leg returns ERROR | §3 limitation, `run1-strace-f-error.json` | state in the header that the counter must not run under a ptrace supervisor (or fall back with `--map-users` unsupported → same JSON error) |
| F5 | low | arm's `[ -e "$e" ]` follows an attacker-controlled symlink (root-planted) → metadata stat of arbitrary paths, and a stat on a path on an unresponsive mount would block | §4, `trace-arm-hostile-fixture.txt` | reorder to `[ -L "$e" ] || [ -e "$e" ] || continue` (`census:2003`) — identical accept set, no follow |
| F6 | info | live/selftest legs execute the scored revision at the caller's identity, unsandboxed | §4, `:597`, `:610` | none (by design); a header sentence naming `--lane` as code execution would make it explicit |

Verdict-neutrality of the arm itself: confirmed — the only write-capable syscall in the whole arm
trace is bash's `/dev/tty`, and all record access is `stat`/`access` by name.

## What I did not do
- No ENOSPC run (no way to fill a filesystem without mount/pacman privileges here); stated as code
  path + analogues in §1.2.
- No live hostile planting in `/var/lib/btrfs` (root-only, host mutation is forbidden); the hostile
  matrix ran against the arm's own override in scratch.
- Did not strace the full live census (only the arm alone, and the counter's parent); the child side
  rests on the mount-namespace argument plus host-side stat/mount diffs.
- Tooling: nothing installed or upgraded (no pacman, no uv, no `~/.local/bin` writes).

## Receipts
`.ufo/waves/round-44/w1/C1SentScope/`: `run2-full-pass.json` (47 s PASS run used for the mount/stat
diff), `run1-strace-f-error.json` (`strace -f` artifact), `trace-parent-writes.txt`,
`trace-arm-hostile-fixture.txt`, `trace-run1.txt`, `host-mounts.txt`, `host-stat-before.txt`.

## Proposed text (for L1; I did not edit the lane)
1. `tools/tsukuroi-census.sh:2003`, replace
   `        [ -e "$e" ] || [ -L "$e" ] || continue`
   with
   `        [ -L "$e" ] || [ -e "$e" ] || continue   # lstat first: never follow an untrusted name`
   (same accept set for regular files, broken symlinks and `-e` targets; removes the only path where
   a name under the record directory resolves outside it).
2. `tools/score-scrub-arm-r44.py` docstring `:57`, replace
   `--scratch is required; everything the counter writes lives under it and is removed on exit, SIGINT and`
   `SIGTERM.`
   with
   `--scratch is required; everything the counter writes lives under it and is removed on exit, SIGINT and`
   `SIGTERM (SIGKILL leaves the run directory; a scored revision that backgrounds a process can outlive`
   `its timeout — see the kill rules).`
