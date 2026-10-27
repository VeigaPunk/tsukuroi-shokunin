VERDICT: supports

# C1ExecHandRepro — independent namespace reproduction of the round-44 scrub-record arm (C1-7)

Seat: C1ExecHandRepro (leaf). Lane: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin.
Article under test: `probe_scrub_record` in `tools/tsukuroi-census.sh` at implementation revision
`7e081698d4fc3c4ea944884fd093058de9909de1` (lane tip during w1: `ff2c264a`).
Host: `7.2.11-arch1-1`, `unshare from util-linux 2.42.4`, hostname `plazir27`.
Reproduced WITH the private user+mount namespace only — the frozen counter
(`tools/score-scrub-arm-r44.py`) was never invoked, no selftest was run, and no lane git/jj
state was touched. Everything below is the arm's own output on a hand-built fixture.

Prediction was written before any run: `.ufo/waves/round-44/w1/C1ExecHandRepro/prediction.txt`
(mtime `2026-10-26 21:09:54 -0300`), first run log `run-A.log` mtime `21:10:10 -0300`.

## 1. What was built

`cd /fast/scratch/hyaku/tsukuroi-r44/C1ExecHandRepro && export TMPDIR=$PWD`.

Article extraction (byte-identical to the revision):
```
$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 7e081698:tools/tsukuroi-census.sh > census-rev7e081698.sh
$ git -C .../tsukuroi-shokunin cat-file -p 7e081698:tools/tsukuroi-census.sh | sha256sum
fca419b4714f7d24314b8d5877f0992c7f326aa8ff80045743990d058e8eaa1c  -
$ sha256sum census-rev7e081698.sh
fca419b4714f7d24314b8d5877f0992c7f326aa8ff80045743990d058e8eaa1c  census-rev7e081698.sh
$ head -n -1 census-rev7e081698.sh > census-nomain.sh   # drops the final `main "$@"` (3396 lines)
```
The source has no trailing newline, so `head -n -1` removes exactly `main "$@"`; the copy now ends
at the closing brace of `run_selftest` (verified `tail -2 census-nomain.sh`).

Namespace invocation (verbatim, the one in the seat brief):
```
$ unshare -m --map-users=1000,0,1 --map-users=100000,1,65535 \
            --map-groups=1000,0,1 --map-groups=100000,1,65535 \
            bash ./run.sh 0755 0600 1 'A dir=0755 tmp=0600'
```
Observed inside it (run-A.log): `uid_map` = `0 1000 1` / `1 100000 65535`, builder `id -u` = 0,
probe caller `uid=1(bin) gid=1(bin)`. So /var/lib/btrfs and the record files are owned by ns root
(host uid 1000) and the probe runs as inner uid 1 = host uid 100000, i.e. a real non-root reader
of a root-created tree.

Builder (`run.sh`, receipted): `mount -t tmpfs -o mode=0755 tmpfs` over `/var/lib`,
`/sys/fs/btrfs`, `/etc/systemd/system` (after `mount --make-rprivate /`); then
`/var/lib/btrfs` with `scrub.status.<fsid>` (0600 root), `scrub.status.<fsid>_tmp`,
`scrub.progress.<fsid>` via `python3 -c 'socket.bind'`, `<fsid>/devinfo/1/scrub_speed_max=0`,
`<fsid>/devinfo/2/scrub_speed_max=52428800`, and
`/etc/systemd/system/timers.target.wants/btrfs-scrub@-.timer` symlink to
`/usr/lib/systemd/system/btrfs-scrub@.timer`. Fixture fsid `5f9d1c2e-3b4a-4c6d-8e7f-0a1b2c3d4e5f`.

Probe invocation inside the ns:
```
setpriv --reuid=1 --regid=1 --clear-groups bash -c \
  ". $S/census-nomain.sh; probe_scrub_record; printf '%s\n' \"\$SCRUB_LINE\""
```
(`printf '%s\n'` instead of the brief's `echo`: identical bytes for this string, and it avoids
`echo` escape interpretation on `-n`/`-e`-looking text.)

Fixture receipt, run A:
```
drwxr-xr-x 0:0 /var/lib
drwxr-xr-x 0:0 /var/lib/btrfs
-rw------- 0:0 /var/lib/btrfs/scrub.status.5f9d1c2e-3b4a-4c6d-8e7f-0a1b2c3d4e5f
-rw------- 0:0 /var/lib/btrfs/scrub.status.5f9d1c2e-3b4a-4c6d-8e7f-0a1b2c3d4e5f_tmp
srwxr-xr-x 0:0 /var/lib/btrfs/scrub.progress.5f9d1c2e-3b4a-4c6d-8e7f-0a1b2c3d4e5f
-rw-r--r-- 0:0 /sys/fs/btrfs/5f9d1c2e-.../devinfo/1/scrub_speed_max      (<0>)
-rw-r--r-- 0:0 /sys/fs/btrfs/5f9d1c2e-.../devinfo/2/scrub_speed_max      (<52428800>)
lrwxrwxrwx 0:0 /etc/systemd/system/timers.target.wants/btrfs-scrub@-.timer
```

## 2. Hand prediction vs observed

Derived only from the header contract `tools/tsukuroi-census.sh:384-407` (rev 7e081698) and
`probe_scrub_record` `:1967-2039` — "unreadable: records and tmp files the caller cannot read
(a root scrub writes mode-0600 files)" (`:394-395`), "timers: entries `btrfs-scrub@<instance>.timer`
… the bare template name is not an instance and is not counted" (`:398-400`), "state: BLOCKED when
a reading is unavailable — an existing dir … the caller cannot list (dir:unreadable …) … else
RECORDED when records+tmp+sockets > 0; else NONE" (`:400-407`).

| run | fixture | predicted line | observed | match |
|---|---|---|---|---|
| A | dir 0755, record 0600, tmp 0600, socket, devinfo/1=0, devinfo/2=52428800, instance timer | `state=RECORDED dir=present records=1 tmp=1 sockets=1 unreadable=2 orphan=0 limited=1 timers=1 detail=5f9d1c2e:2:speed_max=52428800` | identical | YES |
| A' | as A, tmp widened to 0644 | `… unreadable=1 …` (only the 0600 record unreadable) | `state=RECORDED dir=present records=1 tmp=1 sockets=1 unreadable=1 orphan=0 limited=1 timers=1 detail=5f9d1c2e:2:speed_max=52428800` | YES |
| B | as A but `/var/lib/btrfs` mode 0700 | `state=BLOCKED dir=unreadable records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=1 timers=1 detail=dir:unreadable,5f9d1c2e:2:speed_max=52428800` | identical | YES |
| C | A + one record for a fsid absent from sysfs | `records=2 … unreadable=3 orphan=1 …` | `state=RECORDED dir=present records=2 tmp=1 sockets=1 unreadable=3 orphan=1 limited=1 timers=1 detail=5f9d1c2e:2:speed_max=52428800` | YES |
| D | A + a `btrfs-scrub@.timer` bare-template link | `timers=1` (template not counted) | `… timers=1 …`, unchanged vs A | YES |
| E | A, probe caller ns root (uid 0) | `unreadable=0`, rest as A | `state=RECORDED … unreadable=0 …` | YES |

Verbatim outputs (receipts `run-A.log`, `run-B.log`):
```
$ unshare -m --map-users=1000,0,1 --map-users=100000,1,65535 --map-groups=1000,0,1 --map-groups=100000,1,65535 bash ./run.sh 0755 0600 1 'A dir=0755 tmp=0600'
=== A dir=0755 tmp=0600 : caller identity (probe runs as) ===
uid=1(bin) gid=1(bin) groups=1(bin)
=== A dir=0755 tmp=0600 : probe output ===
SCRUB btrfs-scrub-record state=RECORDED dir=present records=1 tmp=1 sockets=1 unreadable=2 orphan=0 limited=1 timers=1 detail=5f9d1c2e:2:speed_max=52428800
=== A dir=0755 tmp=0600 : probe rc=0 ===

$ unshare -m --map-users=1000,0,1 --map-users=100000,1,65535 --map-groups=1000,0,1 --map-groups=100000,1,65535 bash ./run.sh 0700 0600 1 'B dir=0700 tmp=0600'
=== B dir=0700 tmp=0600 : caller identity (probe runs as) ===
uid=1(bin) gid=1(bin) groups=1(bin)
=== B dir=0700 tmp=0600 : probe output ===
SCRUB btrfs-scrub-record state=BLOCKED dir=unreadable records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=1 timers=1 detail=dir:unreadable,5f9d1c2e:2:speed_max=52428800
=== B dir=0700 tmp=0600 : probe rc=0 ===
```
Run E (root caller, `run.sh 0755 0600 0`) isolates causality: same fixture, `unreadable=2` becomes
`unreadable=0`, so the field is a genuine permission reading, not a naming artefact.

Attribute hygiene: emitted SCRUB lines never echo a record name or a full fsid —
`grep -h '^SCRUB ' run-*.log | grep -c '5f9d1c2e-3b4a'` = 0, and in run C
`grep -c '11111111'` on the emitted line = 0. Only the 8-hex `detail=` prefix appears, as the
contract's QUALITY-84 sentence (`:394`) requires.

No-write check (`run-F-nowrite.log`, `NOWRITE=1`): `find /var/lib/btrfs /sys/fs/btrfs
/etc/systemd/system -printf '%p|%y|%m|%u|%g|%s|%T@\n'` snapshotted before and after the probe in
one namespace, `diff -u` clean → `NOWRITE: fixture trees byte-identical before/after (14 entries)`.
(Reads do bump atime on tmpfs; mtime/size/mode/owner are unchanged, which is the assertion the
selftest makes.)

## 3. Verdict-neutrality in situ (full census, one namespace)

`census-ns.sh` runs the whole census (`bash census-rev7e081698.sh`, last line `main "$@"`,
`census-rev7e081698.sh` sha256 `fca419b4…`) four times inside ONE namespace as uid 1: twice with
the scrub fixture, then `rm -rf /var/lib/btrfs` and twice without. Same mounts, same `/sys/fs/btrfs`,
same `/etc/systemd/system` in all four — the record directory is the only variable.

```
$ diff census-with-fixture-1.out census-without-fixture-1.out
1c1  header timestamp only      (2026-10-27T00:12:01Z vs 00:12:02Z)
4c4  PLANE drivers … C6_psi_full_total_us / C6_avail_kb / C6_shmem_kb   (live counters)
10c10
< SCRUB btrfs-scrub-record state=RECORDED dir=present records=1 tmp=1 sockets=1 unreadable=2 orphan=0 limited=1 timers=1 detail=1d02a454:2:speed_max=52428800
> SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=1 timers=1 detail=1d02a454:2:speed_max=52428800
```
The two with-fixture runs and the two without-fixture runs each differ only on line 4
(`C6_psi_full_total_us` 51458287 → 51458291, `C6_avail_kb` 18566032 → 18505220, `C6_shmem_kb`
5364 → 5372) — that is the noise floor, and it is the same line that moves in the A/B. No PLANE
line, no DRIFT/STORAGE/HANDOFF line, and no rollup term changes with the fixture:

```
TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=BLOCKED drivers=BLOCKED journal=BLOCKED update-safety=BLOCKED oom=BLOCKED)   ×4
exit=2 ×4
```
Placement is exactly as declared — line 9 STORAGE, line 10 SCRUB, line 11 rollup — matching the
call site `probe_storage_arm; printf "$STORAGE_LINE"; probe_scrub_record; printf "$SCRUB_LINE";
local roll=HEALTHY` at `tools/tsukuroi-census.sh:3371-3378` (rev 7e081698). The all-BLOCKED rollup
and `exit=2` are an artefact of my namespace (it hides `/var/lib/pacman` and `/etc/systemd/system`
and refuses the user bus), not a host reading; `PLANE packages` even records the caller as
`root_euid=1`, confirming the unprivileged run.

## 4. Live host cross-check (independent of the counter)

Unprivileged live probe on the host (`. census-nomain.sh; probe_scrub_record; echo "$SCRUB_LINE"`,
receipt `live-line.log`):
```
SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0
```
Host facts behind it: `/var/lib/btrfs` does not exist (`ls -ld` → No such file or directory);
`/etc/systemd/system/timers.target.wants` holds 4 links, none of them `btrfs-scrub@*`; and
`/sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/scrub_speed_max` reads `0`, so
`limited=0` is a real reading rather than the absent-sysfs default. So today's live arm says "no
scrub has ever run on this host" — which is what the C1 claim's NONE branch predicts, and it is the
state the fusion node expects to change once a scrub runs.

## 5. Findings (contract/claim notes; none falsify the article)

F1 — Observed detail order is not bytewise across reason classes. The header says "Globs run under
LC_ALL=C, so the detail order is bytewise" (`tools/tsukuroi-census.sh:407`). In run B the emitted
detail is `dir:unreadable,5f9d1c2e:2:speed_max=52428800`, and `1d02a454…`/`5f9d1c2e…` sort before
`dir:unreadable` under LC_ALL=C, so the sentence can only be read as "glob order" (blocked reasons
are appended first by construction, `:2037` `detail+=$info`). Proposed narrowing for the wave's
plan/counter fixtures: `# NONE. Globs run under LC_ALL=C, so glob-derived detail order is bytewise;
blocked reasons are emitted before speed_max entries.`

F2 — BLOCKED-dir readings zero the counters. With `dir=unreadable` every scrub.* counter reads 0
because the `for e in "$dir"/scrub.*` loop sits in the `else` branch of the readability test
(`:2000-2020`, glob loop at `:2002` and `:2018`). That is contract-consistent ("BLOCKED when a reading is unavailable") but the
emitted line cannot be distinguished from an empty readable dir except via `dir=` and `detail=`.
Nothing to fix in the arm; the counter's fixtures must expect `records=0 tmp=0 sockets=0
unreadable=0 orphan=0` in that shape.

F3 — Reality mapping for the state machine. btrfs-progs creates the record directory with
`mkdir(path, 0777)` (`S237 / .ufo/waves/round-42/frozen/src/scrub.c:1151-1160`, called at `:1335`),
so a root scrub under the default umask 0022 leaves `/var/lib/btrfs` at 0755 with 0600 files
(`open(datafile, m, 0600)` at `:483`; the `_tmp` is opened by `scrub_open_file_w` `:517`). The
realistic post-scrub live reading is therefore run A's shape (`state=RECORDED`, `unreadable=1`, or
`unreadable=2` while a killed update's `_tmp` is still there) — never `BLOCKED`; the 0700 shape
(run B) needs umask 077. Any future live receipt that shows `unreadable>0` alongside
`state=RECORDED` is the documented normal, not a defect.

F4 — Live host has no record dir at all (`dir=absent`), so the arm's first live RECORDED reading on
this host will also be the first evidence that a scrub has run; the C2 row SR9's canceled-record
reasoning applies only once that directory exists.

## 6. Host-guard compliance

- Wrote only `/fast/scratch/hyaku/tsukuroi-r44/C1ExecHandRepro/` (removed at the end), the seat
  receipt dir `.ufo/waves/round-44/w1/C1ExecHandRepro/` (68 KB) and this report. No tracked lane
  file, no fleet-root file, no PATH dir, no shim.
- No `git add/commit/stash/checkout/reset/push`, no jj command, no index or state write. Lane files
  were read with `git show`/`cat-file` only.
- No host mutation: mounts were only inside `unshare -m` after `mount --make-rprivate /`; after all
  runs `mount | grep -E ' /var/lib | /sys/fs/btrfs | /etc/systemd/system '` is empty,
  `/var/lib/btrfs` still absent, `/etc/systemd/system/timers.target.wants` still the same 4 links.
  No package manager (pacman is paused host-wide and was not invoked), no service/systemctl/unit
  change, no sysfs write, no `btrfs` subcommand, no sudo.
- No tool installed or upgraded (util-linux 2.42.4, python3, setpriv, diff already present).
- Process hygiene: nothing was signalled; every child exited on its own.
- Not run, by design: the frozen C1 counter `score-scrub-arm-r44.py` (independence required by the
  item), `--selftest`, the C2 counter, any sibling lane tooling.

## 7. Receipts

`.ufo/waves/round-44/w1/C1ExecHandRepro/`: `prediction.txt`, `run.sh`, `census-ns.sh`,
`run-A.log`, `run-Ap.log`, `run-B.log`, `run-C.log`, `run-D.log`, `run-E.log`,
`run-F-nowrite.log`, `snap-before-F nowrite.txt`, `snap-after-F nowrite.txt`, `live-line.log`,
`census-with-fixture-{1,2}.out`, `census-without-fixture-{1,2}.out`.
