VERDICT: supports

# C1-9 — independent namespace reproduction of the INTEGRATED scrub-record arm (round 44, w2)

Seat: `C1ExecHandReproFinal`. Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Wave base/state at run time: `HEAD = 3a1c6b5c958c4f289a8b12551f96d843877b700e`; declared measured tip
`8eee79db608b5815c325a5af7cbfdeac50eda9f4`.

Answer to the assignment: four independent, private-namespace views of the arm's **default** paths each
produced **exactly** the line the `tools/tsukuroi-census.sh` header contract (lines 383–401, "Round-44
addition (C1)") prescribes — as the arm's own `$SCRUB_LINE` **and** as the single line the integrated
script prints — with the rollup term and exit code unchanged across `RECORDED` / `NONE` / `BLOCKED`.
No clause contradicted the contract; nothing was taken from `--selftest` as an oracle (the expected lines
below were derived from the header prose, then compared).

## 0. Object under test is the declared tip

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
$ git show 8eee79db608b5815c325a5af7cbfdeac50eda9f4:tools/tsukuroi-census.sh | sha256sum
2ef86357c14aec3f4346f7ac9013cdda3b399d38bae67f4ca2e286e5a37c4639  -
$ sha256sum tools/tsukuroi-census.sh
2ef86357c14aec3f4346f7ac9013cdda3b399d38bae67f4ca2e286e5a37c4639  tools/tsukuroi-census.sh
$ git status --porcelain -- tools/tsukuroi-census.sh      # (no output: file unmodified)
$ git diff 8eee79db… 3a1c6b5c… -- tools/tsukuroi-census.sh | wc -l
0
```

So the file reproduced is byte-identical at the declared measured commit `8eee79db` and at the wave
tip `3a1c6b5c` (the commits in between touch registry/promotion docs only).

Because `/home` is not traversable by the caller uid inside the namespace, the executed script is a
scratch copy; the copy is asserted byte-identical every run:

```
### COPY_IDENTICAL: YES
```

Extracted arm text (read from the integrated file with
`awk '/^probe_scrub_record\(\) \{/,/^\}$/' $CENSUS`): 79 lines, sha256
`b40d378c07c05f5178640680f9057b13ca573ec5cb7af68462d8293c84a4c729` (identical in all four runs).

## 1. Namespace construction (no sudo, no host mutation)

```
$ unshare -U --map-users=1000,0,1 --map-users=100000,1,1 \
          --map-groups=1000,0,1 --map-groups=100000,1,1 \
          -m --propagation private bash .../inner.sh <view>
### namespace identity (inner root):
uid=0(root) gid=0(root) groups=0(root),65534(nobody)
### uid_map:
         0       1000          1
         1     100000          1
### gid_map:
         0       1000          1
         1     100000          1
```

Inside the namespace, as inner root (tmpfs mounts are private to the new mount namespace):

```
mount -t tmpfs tmpfs /var/lib
mount -t tmpfs tmpfs /etc/systemd/system
mount -t tmpfs tmpfs /sys/fs/btrfs     # views rootscrub / control / orphan
mount -t tmpfs tmpfs /sys/fs           # view sysfsnotdir (btrfs replaced by a regular file)
```

The caller is a genuine non-root uid/gid in that namespace (outer subordinate uid 100000):

```
### caller identity:
uid=1(bin) gid=1(bin) groups=1(bin)
```

and the whole census — not only the arm — ran as that caller: the packages line reports
`root_euid=1` (`PLANE packages: … root_status=ok root_mode=0755 root_uid=0 root_gid=0 root_euid=1 …`).

Host state after all four runs (private namespace, no propagation):

```
### host mount table unchanged (private namespace, no propagation):
0
ls: cannot access '/var/lib/btrfs': No such file or directory
```

## 2. Views, exact commands, exact lines

Run per view:

```
$ setpriv --reuid=1 --regid=1 --clear-groups -- id
uid=1(bin) gid=1(bin) groups=1(bin)

$ setpriv --reuid=1 --regid=1 --clear-groups -- \
    bash -c '. arm-probe.sh; SCRUB_DIR=/var/lib/btrfs; BTRFS_SYSFS=/sys/fs/btrfs;
             TIMER_WANTS=/etc/systemd/system/timers.target.wants; probe_scrub_record;
             printf "%s\n" "$SCRUB_LINE"'

$ setpriv --reuid=1 --regid=1 --clear-groups -- \
    env PATH=<stub-bin>:/usr/bin:/bin <non-scrub seams only> /bin/bash <census copy>
    # NOTE: TSUKUROI_BTRFS_SYSFS, TSUKUROI_SCRUB_DIR and TSUKUROI_TIMER_WANTS are NOT set:
    # the arm reads its documented defaults, which the namespace has masked.
```

### View A — `rootscrub` (root-scrub-like: 0600 record, `_tmp`, socket, speed_max 0 and 52428800, wants link)

Inputs (built as inner root on the arm's default paths):

```
/var/lib/btrfs/scrub.status.11111111-2222-3333-4444-555555555555      -rw-------  (root scrub's 0600 record)
/var/lib/btrfs/scrub.status.11111111-2222-3333-4444-555555555555_tmp  -rw-r--r--  (in-progress/killed update)
/var/lib/btrfs/scrub.progress.11111111-2222-3333-4444-555555555555    srwxr-xr-x  (scrub start progress socket)
/var/lib/btrfs/scrub.readme                                           -rw-r--r--  (a name btrfs-progs never writes)
/sys/fs/btrfs/11111111-…/devinfo/1/scrub_speed_max                    '0\n'
/sys/fs/btrfs/11111111-…/devinfo/2/scrub_speed_max                    '52428800\n'
/etc/systemd/system/timers.target.wants/btrfs-scrub@-.timer      -> …/btrfs-scrub@.timer   (an enabled instance)
/etc/systemd/system/timers.target.wants/btrfs-scrub@.timer       -> …/btrfs-scrub@.timer   (bare template)
/etc/systemd/system/timers.target.wants/ai-usage.timer           -> …/ai-usage.timer       (unrelated timer)
```

Readability of the record by the caller (this is where `unreadable=1` comes from):

```
### record present mode=600; readable by inner root? (expect yes)
root-read OK
### record (mode=600) readable by caller uid=1 gid=1? (0600 => denial)
head: cannot open '/var/lib/btrfs/scrub.status.11111111-2222-3333-4444-555555555555' for reading: Permission denied
```

Arm variable (printed by the caller):

```
SCRUB_LINE_VAR: SCRUB btrfs-scrub-record state=RECORDED dir=present records=1 tmp=1 sockets=1 unreadable=1 orphan=0 limited=1 timers=1 detail=11111111:2:speed_max=52428800
```

Expected from the header contract (derived, not copied from the selftest):

```
SCRUB btrfs-scrub-record state=RECORDED dir=present records=1 tmp=1 sockets=1 unreadable=1 orphan=0 limited=1 timers=1 detail=11111111:2:speed_max=52428800
### CONTRACT_MATCH: YES
```

Printed by the integrated script (one line only):

```
### SCRUB line(s) printed by the integrated script:
1
SCRUB btrfs-scrub-record state=RECORDED dir=present records=1 tmp=1 sockets=1 unreadable=1 orphan=0 limited=1 timers=1 detail=11111111:2:speed_max=52428800
### rollup line:
TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
### census_rc=1
### line order STORAGE < SCRUB < rollup:
     STORAGE at line 9, SCRUB at line 10, rollup at line 11
### SCRUB_LINE_VAR == line printed by the integrated script? -> YES
```

### View B — `control` (same sysfs, no record/tmp/socket, no enabled instance)

```
SCRUB_LINE_VAR: SCRUB btrfs-scrub-record state=NONE dir=present records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=1 timers=0 detail=11111111:2:speed_max=52428800
### CONTRACT_MATCH: YES
### rollup line:
TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
### census_rc=1
```

### View C — `sysfsnotdir` (sysfs root exists but is not a directory)

```
-rw-r--r-- 1 root root  2 /sys/fs/btrfs            # regular file, not a directory
-rw-r--r-- 1 root root  0 /var/lib/btrfs/scrub.status.11111111-…

SCRUB_LINE_VAR: SCRUB btrfs-scrub-record state=BLOCKED dir=present records=1 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0 detail=sysfs:not-directory
### CONTRACT_MATCH: YES
### rollup line:
TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
### census_rc=1
```

### View D — `orphan` (extra clause probe: record whose fsid is not under the sysfs root)

```
SCRUB_LINE_VAR: SCRUB btrfs-scrub-record state=RECORDED dir=present records=1 tmp=0 sockets=0 unreadable=0 orphan=1 limited=0 timers=0
### CONTRACT_MATCH: YES
### rollup line:
TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
### census_rc=1
```

### Cross-view invariants (all four views)

```
$ for s in rootscrub control sysfsnotdir orphan; do grep -c '^SCRUB ' out-$s.txt; done
1  1  1  1
$ cat out-*.txt | grep '^TSUKUROI_CENSUS: ' | sort -u
TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
```

One SCRUB line per run; identical rollup term and identical exit code (rc=1) across `RECORDED`,
`NONE` and `BLOCKED` — the verdict-neutrality claim holds inside the namespace as well. (The
`packages=DEGRADED` term is an artefact of my deliberately minimal stub fixture, not of the arm; it is
constant, so the comparison is sound.)

## 3. Contract clause-by-clause against the reproduced output

| Header-contract clause (`tools/tsukuroi-census.sh:383-401`) | Reproduced evidence |
|---|---|
| one line, after STORAGE, before the rollup | `SCRUB at line 10`, STORAGE 9, rollup 11; `grep -c = 1` in all views |
| `dir:` from `TSUKUROI_SCRUB_DIR` default `/var/lib/btrfs` | all four views read `/var/lib/btrfs` with no `TSUKUROI_SCRUB_DIR` set; `dir=present` |
| records `scrub.status.<fsid>`, by name and stat, never content | strace: 3 `newfstatat` on the record name, **0** `openat` on any record/tmp/socket name |
| tmp `scrub.status.<fsid>_tmp` counted apart | `tmp=1` (View A) while `records=1`; `_tmp` alone → `tmp=1`, `records=0` in the committed case set |
| sockets `scrub.progress.<fsid>` read as a reading, not running state | `sockets=1` for a real `AF_UNIX` socket; no ioctl, no `btrfs`/`systemctl` call in the arm text |
| unreadable: records/tmp the caller cannot read | mode 0600 record → `unreadable=1`, and the caller's own `read` is `Permission denied` |
| orphan: record whose fsid has no sysfs entry | View D → `orphan=1` with `state=RECORDED` |
| limited: nonzero `scrub_speed_max`, listed as `<fsid8>:<devid>:speed_max=<v>` | devinfo/1 `0` → no-limit; devinfo/2 `52428800` → `limited=1 detail=11111111:2:speed_max=52428800` |
| timers: `btrfs-scrub@<instance>.timer` under `timers.target.wants`; bare template not an instance | instance link + bare template + unrelated timer → `timers=1` |
| other names ignored, no name ever echoed | `scrub.readme` present, not counted, not echoed |
| state BLOCKED when a reading is unavailable (`sysfs:not-directory`) | View C → `state=BLOCKED … detail=sysfs:not-directory` |
| verdict-neutral: no PLANE text, no rollup term, no exit-code change | identical rollup and rc=1 in `RECORDED`/`NONE`/`BLOCKED` |
| live mode creates no files | pre/post view snapshot hashes equal in all four views (below) |

## 4. "By name and stat, never by content" — strace of the arm as the caller

```
$ setpriv --reuid=1 --regid=1 --clear-groups -- \
    strace -f -qq -e trace=openat,newfstatat,getdents64 -o strace-rootscrub.log bash -c '<arm>'
### strace log lines: 84
### openat on a record/tmp/socket NAME (expect none: stat only):
none
### newfstatat count on record/tmp/socket names:
9
      2 newfstatat(AT_FDCWD, "/var/lib/btrfs"
      3 newfstatat(AT_FDCWD, "/var/lib/btrfs/scrub.progress.11111111-2222-3333-4444-555555555555"
      1 newfstatat(AT_FDCWD, "/var/lib/btrfs/scrub.readme"
      3 newfstatat(AT_FDCWD, "/var/lib/btrfs/scrub.status.11111111-2222-3333-4444-555555555555"
      3 newfstatat(AT_FDCWD, "/var/lib/btrfs/scrub.status.11111111-2222-3333-4444-555555555555_tmp"
### openat of scrub_speed_max (the only content the arm reads):
      1 openat(AT_FDCWD, "/sys/fs/btrfs/"
      1 openat(AT_FDCWD, "/sys/fs/btrfs/11111111-2222-3333-4444-555555555555/devinfo/"
      1 openat(AT_FDCWD, "/sys/fs/btrfs/11111111-2222-3333-4444-555555555555/devinfo/1/scrub_speed_max"
      1 openat(AT_FDCWD, "/sys/fs/btrfs/11111111-2222-3333-4444-555555555555/devinfo/2/scrub_speed_max"
```

View C (`sysfsnotdir`): `openat of scrub_speed_max → none` (the regular-file sysfs root is never
opened; `-d` fails and the arm blocks on `sysfs:not-directory`).

## 5. Zero mutation in live mode (independent check of the C1 kill rule)

Per view, a `find -printf '%y %m %U %G %s %p'` snapshot of `/var/lib/btrfs`, `/sys/fs/btrfs`
(or `/sys/fs` for view C) and `/etc/systemd/system` is taken before and after the census run:

```
0e45602f250df7fad51c29c09ceb18f82cda8596dba74aaf2372a82619f06397  pre-control.snap   = post-control.snap
2c81cdd41259dda47db2a61280c4bcb294044dd3daa58f209234f430a62463c5  pre-orphan.snap    = post-orphan.snap
c55b053e52d914a62c37d1736f1e349f0646606b8f98e23efbe05279b3bb6e77  pre-rootscrub.snap = post-rootscrub.snap
60ac0c66ef424db800413a893bcfbc3b4ae4f263835b821bf04715d8c6b3f15d  pre-sysfsnotdir.snap = post-sysfsnotdir.snap
### ZERO_MUTATION: YES (view byte/type/mode/owner-identical after the live run)
```

The arm creates no record, no `_tmp`, no socket, and touches no mode/owner.

## 6. What this reproduction deliberately does NOT cover

These clauses were exercised by the committed hermetic cases, not by my namespace views (listed so
the integrator can see the split; 16 cases carry `R44-C1` in `tools/tsukuroi-census.sh`):

`dir:absent + sysfs absent` (3232, 3288) · `dir:unreadable` (3266) · `dir:absent, records present,
sysfs absent` (3288) · `tmp:not-regular` / `record:not-regular` / `progress:not-socket` and the
newline-name never echoed (3281) · `speed-malformed` / `speed-unreadable` / empty line / zero-padded
zero (3260, 3302, 3307) · `detail` join order evidence-before-info (3319) · `timers:unreadable` and a
directory named like a timer (3274, 3330) · `LC_ALL=C` collation-inflated name (3297) · `_tmp` alone
reads RECORDED (3313) · two devices on one fs with one limit (3316/3254). My views cover the
"root-scrub-like" combination, the sysfs-not-a-directory block, the orphan counter and the
`timers`/`limited`/`unreadable` counters together — the combination the target host actually shows.

Also not covered by design: the running-scrub state needs `CAP_SYS_ADMIN` (contract: a progress
socket is a reading, not the running state) — my caller has no capabilities, so the observation stays
at the documented unprivileged level.

## 7. Risks / limits of this evidence

- The views are tmpfs, not a live btrfs mount: they prove the arm's *reading* semantics and the
  emitted grammar, not the kernel's scrub-record binary content (the arm never reads content — §4).
- `strace` is my own child under my own pid tree; no other process was traced or signalled.
- The non-scrub planes were pinned to stub seams so that nothing live entered the run; that makes the
  rollup term an artefact (`packages=DEGRADED`) but keeps it constant across views, which is what the
  neutrality comparison needs.
- No `sudo`, no `pacman`, no scrub command, no service/timer/sysfs/mount outside the private
  namespaces, no writes to any lane tracked file; scratch was removed after the receipts were copied.
  No tool was installed or upgraded for this seat (`unshare`/`setpriv`/`strace` 7.2 were already
  present; `newuidmap`/`newgidmap` with `/etc/subuid` `vgpnk:100000:65536` enabled the two-id mapping).

## 8. Proposed text (for the L1 / SCORECARD evidence row)

> C1-9 (independent repro, w2): four private user+mount-namespace views of the arm's default paths
> (`/var/lib/btrfs`, `/sys/fs/btrfs`, `/etc/systemd/system/timers.target.wants`) as a non-root caller
> (inner uid/gid 1, outer subuid 100000) reproduce the header line byte-for-byte:
> `state=RECORDED dir=present records=1 tmp=1 sockets=1 unreadable=1 orphan=0 limited=1 timers=1
> detail=11111111:2:speed_max=52428800` (0600 record + `_tmp` + progress socket + speed_max 0/52428800
> + one enabled instance), `state=NONE … limited=1` (control), `state=BLOCKED … detail=sysfs:not-directory`
> (sysfs regular file), `state=RECORDED … orphan=1` (unmounted fsid). `$SCRUB_LINE` equals the single
> printed line, STORAGE precedes SCRUB precedes the rollup, rollup term and exit code are identical
> across RECORDED/NONE/BLOCKED, the view tree is byte/mode/owner-identical after each live run, and
> strace shows 0 `openat` on any record/tmp/socket name (stat only) with `scrub_speed_max` the only
> content read. Object under test is byte-identical at `8eee79db` and at wave tip `3a1c6b5c`
> (census sha256 `2ef86357c14aec3f4346f7ac9013cdda3b399d38bae67f4ca2e286e5a37c4639`).

## 9. Receipts

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-44/w2/C1ExecHandReproFinal/`:
`transcript.txt` (full stdout of all four runs, verbatim), `outer.sh`, `inner.sh`,
`stub-bin/.dispatch`, `arm-probe.sh`, `out-{rootscrub,control,sysfsnotdir,orphan}.txt`,
`pre-*.snap`, `post-*.snap`, `strace-*.log`, `SHA256SUMS`.
