VERDICT: supports

Item C2-A7 (round 48, wave w2, uncounted scout seat). Re-read the host-state half of GR2 and GR3
read-only on 2026-10-28 and compared each observation with the "Host reading" lines of
`corpus/knowledge/btrfs-scrub-grounding-r45.md` at freeze `ae99f021b76f8eb1c8805d32d80644464afb1ff6`
and with `.ufo/waves/round-45/frozen/hostcap/capture.txt` (captured 2026-10-27T02:09:52Z).

Every assigned command ran; `systemctl show` reached the system manager normally (no user-bus
failure under this environment). All observed values match the frozen rows; nothing differs.

## Observations vs the rows

### Identity of the filesystem under test
- `ls /sys/fs/btrfs/` → `1d02a454-c549-4a35-b567-89d60902af8e` and `features`. Same UUID the capture
  names for `scrub_speed_max` and `devinfo` (capture.txt:8-9). **matches.**

### GR2 host reading — replace state readable without privilege
Row text (frozen file, GR2 "Host reading"): the filesystem lists devid 1 only (capture.txt:9);
`exclusive_operation` names `device replace` while a replace holds the exclusive operation and reads
`none` otherwise; `devinfo/<devid>/replace_target` reads 1 on the target; both files mode 444, read
`none` and `0` on this host (read by C2ExecHostRecheck 2026-10-27); caller has no effective
capabilities (capture.txt:1).

- `cat /sys/fs/btrfs/*/exclusive_operation` → `none`
  (`cat: /sys/fs/btrfs/features/exclusive_operation: No such file or directory` on the pseudo-entry,
  expected: `features` is not a filesystem UUID dir). Value `none` → **matches** (no replace holds
  the exclusive operation).
- `cat /sys/fs/btrfs/*/devinfo/*/replace_target` → `0`. **matches** (no replace target on devid 1).
- `ls /sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/` → `1` only. **matches** capture.txt:9
  (`devids=1`).
- `stat -c '%a %U'` → `exclusive_operation` 444 root, `devinfo/1/replace_target` 444 root.
  **matches** the row's mode-444 claim.
- `id -u` → `1000`; `grep CapEff /proc/self/status` → `CapEff: 0000000000000000`. **matches**
  capture.txt:1 and the row's "no effective capabilities".

### GR3 host reading — unit kill behaviour
Row text (frozen file, GR3 "Host reading"): `systemctl show btrfs-scrub@-.service` reports
`KillMode=control-group KillSignal=2 SendSIGKILL=yes TimeoutStopUSec=5s FinalKillSignal=9`
(capture.txt:3); the stop default comes from `10-faster-shutdown.conf` line 2 (capture.txt:4), a
drop-in no installed package lists (capture.txt:5); systemd is 262-1-arch (capture.txt:2).

- `systemctl show btrfs-scrub@-.service -p KillMode,KillSignal,TimeoutStopUSec,FragmentPath` →
  `FragmentPath=/usr/lib/systemd/system/btrfs-scrub@.service`, `TimeoutStopUSec=5s`,
  `KillMode=control-group`, `KillSignal=2`. **matches** capture.txt:3 on all four properties.
- Supplementary (same command family, read-only):
  `-p SendSIGKILL,FinalKillSignal,DropInPaths` → `SendSIGKILL=yes`, `FinalKillSignal=9`,
  `DropInPaths=` (empty). **matches** capture.txt:3 and capture.txt:7 (`unit_dropins` empty) — the
  effective values come from the packaged unit plus the manager default, not a unit drop-in.
- `cat -n /etc/systemd/system.conf.d/10-faster-shutdown.conf` → line 2 `DefaultTimeoutStopSec=5s`.
  **matches** capture.txt:4.
- `pacman -Qo /etc/systemd/system.conf.d/10-faster-shutdown.conf` →
  `error: No package owns /etc/systemd/system.conf.d/10-faster-shutdown.conf` (exit 1). **matches**
  capture.txt:5 (`dropin_owner ... none`).
- `systemctl --version` → `systemd 262 (262-1-arch)`; `uname -r` → `7.2.11-arch1-1`. **matches**
  capture.txt:2 and the row's verified-at header.

### Out-of-scope freshness note (GR1, depth only)
GR1's host half (`scrub_speed_max` 0, mode 644, owner root, capture.txt:8) re-read today:
`stat` → 644 root; `cat` → `0`. **matches** — the limit is still unset; C2-A7 assigns GR2/GR3 only,
recorded here because the same read covered it.

## Freshness
Capture.txt was taken 2026-10-27T02:09:52Z; this re-read ran 2026-10-28 (~1 day later). Every host
value the GR2 and GR3 host-reading lines assert is byte-identical today: UUID, devid set {1},
`exclusive_operation`=`none`, `replace_target`=`0`, modes 444/644, uid 1000 with CapEff 0,
KillMode=control-group, KillSignal=2 (SIGINT), TimeoutStopUSec=5s, SendSIGKILL=yes,
FinalKillSignal=9, empty unit DropInPaths, drop-in line 2 `DefaultTimeoutStopSec=5s` with no package
owner, systemd 262-1-arch on kernel 7.2.11-arch1-1.

## Differs
None. No host-state value asserted by GR2 or GR3 differs from today's read (in value or in
presence/absence).

## Method notes
- All commands read-only; no `btrfs`, `mount`, unit start/stop, or privileged command run; nothing
  written outside this report. No scratch dir was needed (no fixture, no clone).
- The `features` glob noise (`cat:`/`ls:` errors on `/sys/fs/btrfs/features/...`) is the glob
  matching a non-filesystem sysfs entry, not a host difference; the per-UUID reads all succeeded.
- `systemctl show` was run against the system manager and answered fully; no user-bus failure was
  observed under this environment.
