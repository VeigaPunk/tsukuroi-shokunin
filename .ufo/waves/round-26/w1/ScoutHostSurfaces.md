# Scout host surfaces — round 26, C1 storage integrity (readability split and census-arm shape)

Done: every C1 storage fact is classified on this host as readable by an unprivileged user or
privilege-gated, and the shape of a future read-only census arm is proposed; only the two NVMe
SMART facts (SH5, SH6) and any verification of counter persistence require privilege.

## Method

The frozen capture was verified against the declaration before use. Its bytes hash to
`002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd` and the script to
`81234ae10ddf197aa49cac5ba11220f5f4cca481653155e75ee12439e3675364`, both matching
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md:899`. All live probes below ran as
the ordinary user `vgpnk` (uid 1000, groups `docker`, `input`, `wheel`) with no `sudo`, no write,
no service action, no scrub start and no counter reset. Live reads happened at 2026-10-22 about
10:44 to 10:52 local time (13:44 to 13:52 UTC), roughly four to twelve minutes after the capture.

## Findings

1. [obs] The btrfs per-device error counters are fully readable unprivileged, both surfaces. The
   sysfs file `/sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/error_stats` is
   mode `-r--r--r--` and its `cat` returns five keys, `write_errs 0`, `read_errs 0`,
   `flush_errs 0`, `corruption_errs 0`, `generation_errs 0` (exit 0). `btrfs device stats /`
   returns the same five counters under the names `write_io_errs`, `read_io_errs`,
   `flush_io_errs`, `corruption_errs`, `generation_errs` (exit 0); after mapping the two naming
   schemes the outputs are value-identical. `btrfs device stats -c /` (check mode, read-only)
   exits 0, so the clean pass is machine-readable without parsing. This confirms the C1 SH1
   equivalence on this host without privilege and matches the frozen capture at
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/capture/capture.txt:35-44`
   and `:110-116`. The ioctl form needs a mountpoint: `btrfs device stats /dev/mapper/root`
   fails with `Permission denied` (exit 1) because `/dev/mapper/root` resolves to a `brw-rw----
   root:disk` node and this user is not in `disk`.

2. [obs] The allocation profiles are readable unprivileged from three independent surfaces.
   `findmnt -n -o UUID /` returns `1d02a454-c549-4a35-b567-89d60902af8e` (exit 0), which is the
   sysfs directory name. `btrfs filesystem df --raw /` prints `Data, single`,
   `System, DUP`, `Metadata, DUP` with byte totals (exit 0). The sysfs tree
   `/sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/allocation/{data,metadata,system}/`
   contains profile *directories* (`data/single`, `metadata/dup`, `system/dup`), and each holds
   only `total_bytes` and `used_bytes`; the profiles-present information is the directory name,
   not a readable file. Values agree: data single `total_bytes=229789138944`,
   metadata dup `total_bytes=38654705664`, system dup `total_bytes=8388608`. The
   `metadata_uuid` value equals the filesystem uuid, and the checksum algorithm reads
   `crc32c (crc32c-lib)` from
   `/sys/fs/btrfs/<fsid>/checksum`. This supplies the SH3 host premise (data single, metadata and
   system duplicate) with no privilege.

3. [obs] The scrub record is readable unprivileged. `btrfs scrub status --raw /` exits 0 and
   prints UUID `1d02a454-…`, `no stats available`, `Total to scrub: 187292925952`, and raw
   counters that are all zero. The same command on a submount (`/home`) reports the same
   filesystem UUID, so the query is per filesystem, not per mount. The on-disk status directory
   `/var/lib/btrfs` does not exist: `stat` returns `No such file or directory` (exit 1) and `ls`
   returns exit 2, while `/var/lib` is `drwxr-xr-x root:root`, so absence is decidable by an
   unprivileged caller (the parent is world-searchable). The timer is readable and disabled:
   `systemctl is-enabled btrfs-scrub@-.timer` prints `disabled` (exit 1), while
   `systemctl show btrfs-scrub@-.timer -p UnitFileState -p UnitFilePreset -p ActiveState
   -p LastTriggerUSec -p NextElapseUSecRealtime` exits 0 and prints `UnitFileState=disabled`,
   `UnitFilePreset=disabled`, `ActiveState=inactive`, empty `LastTriggerUSec` and empty
   `NextElapseUSecRealtime`. `systemctl list-unit-files 'btrfs*'` shows the service as `static`
   and the timer as `disabled disabled`, and `systemctl list-timers --all` does not list the
   scrub timer at all. For contrast the trim timer is active: `fstrim.timer` is `enabled`, last
   fired `Tue 2026-10-20 08:15:11 -03`, next due `Mon 2026-10-26 01:27:07 -03`. The installed
   timer unit `/usr/lib/systemd/system/btrfs-scrub@.timer:5-8` says `OnCalendar=monthly` with
   `Persistent=true`, and the service `/usr/lib/systemd/system/btrfs-scrub@.service:10` runs
   `ExecStart=/usr/bin/btrfs scrub start -B %f` with no `User=`, so it would run as root. This
   confirms the SH4 host facts unprivileged and matches the frozen capture at
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/capture/capture.txt:118-152`.

4. [obs] The kernel journal is readable unprivileged on this host, but only because of an ACL, and
   that must be treated as a property of the host, never an assumption. `/proc/sys/kernel/dmesg_restrict`
   is `1` and `dmesg` fails with `Operation not permitted` (exit 1). The journal files are mode
   `-rw-r----- root:systemd-journal`, and `getfacl` on
   `/var/log/journal/432d02b544a5459ebbff9c42ec68334d/system.journal` shows `group:wheel:r--`,
   which is why this user (member of `wheel`) can read kernel records. Measured coverage:
   `journalctl -k -b 0 | wc -l` gives 3894 lines, boot -1 gives 17331 and boot -2 gives 529, and
   `journalctl --list-boots` reports 6 retained boots. On an ordinary host without that ACL the
   same reads may return only the user's own records, so a census arm must run a positive control
   (current-boot kernel line count greater than zero) before it may report "no errors". The exact
   capture filters return zero content matches unprivileged:
   `journalctl --no-pager -o cat _TRANSPORT=kernel --grep 'BTRFS (error|critical|warning)|forced readonly'`
   prints nothing, and the `BTRFS.*errs: wr` filter likewise prints nothing; both grep counts are
   0. The retained window also contains no btrfs scrub start line at all: grepping all kernel
   records for `scrub` case-insensitively yields three lines, all of them the XFS module banner
   reading `SGI XFS with ACLs, security attributes, realtime, scrub, repair, quota, no debug
   enabled`, and the `btrfs-scrub@-.service` unit journal has no entries on any boot. The
   capture's zero result at
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/capture/capture.txt:153-174`
   is therefore reproducible without privilege.

5. [obs] A journal-format trap can manufacture false error counts. `journalctl -o short-iso
   --grep '<pattern>'` over several boots prints `-- Boot <id> --` separator lines even when the
   pattern matches nothing: the zero-match kernel error query above produced 3 output lines and
   `wc -l` said 3, while the same query with `-o cat` or `--quiet` produced 0. The existing census
   already strips these separators in `oom_keys()` at
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh:557-560`, which is
   the precedent to follow. A second self-reference trap: `--grep` without `_TRANSPORT=kernel`
   matches the `sudo` command echo lines the capture left in the live journal, for example
   `sudo[3200969] … COMMAND=/usr/bin/journalctl … --grep 'BTRFS (error|critical|warning)|forced
   readonly'`, so any future arm that greps BTRFS text without the transport filter can count its
   own invocation. Those echo lines are live journal records, not lines of the frozen capture.

6. [obs] The two NVMe SMART facts are privilege-gated, exactly as the capture's use of `sudo`
   implies. `smartctl -H -A /dev/nvme0n1` as this user prints `Smartctl open device:
   /dev/nvme0n1 failed: Permission denied` and exits 2. `nvme smart-log /dev/nvme0` exits 1 with
   `/dev/nvme0: Permission denied` and the deprecated-command warning. The cause is node
   ownership: `/dev/nvme0` is `crw------- root:root` and `/dev/nvme0n1` is `brw-rw---- root:disk`,
   and this user belongs to neither `root` nor `disk`. There is no substitute surface: no file
   under `/sys/class/nvme/nvme0` contains a SMART field (a case-insensitive listing for
   `smart|health|spare|used|media` returns none), and `/sys/kernel/debug` is `drwx------ root:root`
   and cannot be entered. Therefore SH5 (how `smartctl` derives NVMe health) and SH6 (lifetime
   counters) cannot be checked from an unprivileged shell; only the frozen capture carries them,
   at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/capture/capture.txt:175-222`
   (`PASSED`, `Critical Warning 0x00`, spare `100%` against threshold `10%`, `Percentage Used 2%`,
   media errors `0`, power cycles `325`, unsafe shutdowns `200`).

7. [obs] Persisted counter state is also privilege-gated. `btrfs inspect-internal dump-super -f
   /dev/mapper/root` fails with `ERROR: cannot open /dev/mapper/root: Permission denied` (exit 1),
   so the superblock copy of the five counters cannot be read unprivileged. Counter values are
   currently all zero, so even a privileged read could not demonstrate the SH2 persistence
   behaviour (counters surviving a mount cycle) without inducing an error. SH2's dated-incident
   half is readable unprivileged through the kernel journal (finding 4), but its persistence half
   is [unk] from a read-only position.

8. [obs] Three unprivileged btrfs outputs are traps for a census parser and must not be used as
   inputs. `btrfs filesystem show /` exits 0 but prints `devid 1 size 0 used 0 path /dev/mapper/root
   MISSING`, because it cannot open the mapper node; the `size 0` and `MISSING` are access
   artefacts, not device facts. `btrfs filesystem usage /` exits 0 but first prints `WARNING:
   cannot read detailed chunk info, per-device usage will not be shown, run as root`, so its
   per-device section is silently absent. Both should be replaced by `btrfs filesystem df --raw`
   plus the sysfs tree, which are complete unprivileged.

9. [obs] Device attribution needs the block chain, not a hardcoded name. `/sys/fs/btrfs/<fsid>/devices/`
   contains the symlink `dm-0 -> ../../../../devices/virtual/block/dm-0`; `/sys/block/dm-0/dm/name`
   is `root`, `/sys/block/dm-0/dm/uuid` is `CRYPT-LUKS2-…-root`, and
   `/sys/block/dm-0/slaves/nvme0n1p2` resolves to
   `/sys/devices/pci0000:00/0000:00:01.2/0000:02:00.0/nvme/nvme0/nvme0n1/nvme0n1p2`. The host has
   a second controller: `/sys/class/nvme/nvme1/address` is `0000:15:00.0`, and `lsblk` shows
   `nvme1n1` carrying `/tmp` and `/fast` as XFS, unrelated to the root btrfs. A census arm must
   derive the controller from the btrfs device chain, and must not attribute nvme1 health to the
   root filesystem. Readable controller attributes are `model` (`WD_BLACK SN8100 1000GB`),
   `serial`, `firmware_rev` (`830ZRR02`), `state` (`live`), `transport` (`pcie`), `address`,
   `cntlid`, `queue_count`, `sqsize`, `subsysnqn`, plus `hwmon1/temp{1,2,3}_input` (29850, 45850,
   28850 millidegrees). The serial number is readable unprivileged and should be suppressed in
   census output, matching the capture's deliberate omission of `smartctl -i`.

10. [obs] The frozen capture and the live host differ only in live numbers, not in shape. The
    counters, profiles, `no stats available`, the absent `/var/lib/btrfs` and the disabled timer
    all reproduce exactly. `Total to scrub` in `btrfs scrub status` read `174.40GiB` in the
    capture at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/capture/capture.txt:121-123`
    and `187292925952` bytes (about 174.43 GiB) live; sysfs `used_bytes` also moved. A census arm
    must compare structure and invariants, never frozen constants.

11. [inf] Mapping of the six C1 rows to privilege class. SH1: unprivileged, both surfaces agree.
    SH2: the counter-persistence premise needs the superblock or a controlled error, so privileged
    or not observable; the dated-incident premise is unprivileged through the journal. SH3: the
    host profile facts are unprivileged, and the repair rule is documentation, not a host read.
    SH4: unprivileged, all four sub-facts (no stats, absent status directory, disabled timer,
    no scrub in the retained journal). SH5: privileged, `smartctl` only. SH6: privileged,
    `nvme smart-log` only.

## Proposed census arm (proposal only; nothing implemented)

### Placement and shape

Recommendation: a seventh plane line, `PLANE storage: <VERDICT> (<note>)`, emitted between
`drivers` and `journal`, with a matching term in the `TSUKUROI_CENSUS` rollup, because storage
integrity is an independent surface with its own privilege gate and its own positive controls.
The alternative, an arm riding the `drivers` line as `storage=[…]` beside `mem=[…]`, avoids a
format change for consumers but would fold a disk-durability verdict into a line whose stated
subject is drivers and the kernel ring. Whichever is chosen, the note should name the revision
of the vocabulary it cites (the round-26 entry's SH rows), following the existing
`r6 vocab:`/`r8 vocab:` suffix style used by the existing notes at
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh:1132` and `:1285`.
The verdict vocabulary stays the census's three values, `HEALTHY`, `DEGRADED`, `BLOCKED`; the
entry's fourth value `UNVERIFIED` maps to `DEGRADED` with an explicit `unverified(...)` field,
never to `HEALTHY`. The exit map stays 0, 1, 2 and worst-plane wins, and the arm must follow the
existing rule that an unreadable probe is `BLOCKED`, never a pass
(`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh:10-24`).

### Inputs

Every input below is read-only. The third column is what the arm must do before trusting the
reading.

| Input | Privilege on this host | Positive control before use |
|---|---|---|
| `findmnt -n -o UUID,TARGET -t btrfs` | unprivileged | at least one row; the UUID must name a directory under `/sys/fs/btrfs/` |
| `/sys/fs/btrfs/<fsid>/devinfo/<devid>/error_stats` | unprivileged | exactly five known keys, all integer |
| `/sys/fs/btrfs/<fsid>/devinfo/<devid>/{missing,writeable,in_fs_metadata}` | unprivileged | each file yields 0 or 1 |
| `/sys/fs/btrfs/<fsid>/devices/` symlinks | unprivileged | at least one entry per `in_fs_metadata=1` device |
| `btrfs device stats -c /` (mountpoint form) | unprivileged | exit 0 or 1 (1 means a non-zero counter), five lines parsed; exit greater than 1 or `Permission denied` means the probe failed, not a clean pass |
| `btrfs filesystem df --raw /` | unprivileged | one line per profile, parseable `type, profile: total=N, used=N` |
| `/sys/fs/btrfs/<fsid>/allocation/<type>/` directory names | unprivileged | only profile directories and the known counter files; an empty set is `unknown` |
| `btrfs scrub status --raw /` | unprivileged by mountpoint; device path is gated | output names the same UUID; `no stats available` must be distinguished from a parse failure |
| `stat /var/lib/btrfs` existence; contents only if readable | existence unprivileged; contents privileged | `ENOENT` means no record; `EACCES` on the directory content means `unknown`, never "never scrubbed" |
| `systemctl show btrfs-scrub@-.timer -p UnitFileState -p UnitFilePreset -p ActiveState -p LastTriggerUSec -p NextElapseUSecRealtime` and the same for the service | unprivileged (exit 0 either way) | keys present; an empty `LastTriggerUSec` means never triggered only when the unit exists |
| `journalctl -o cat _TRANSPORT=kernel --grep '<btrfs error patterns>'` over all retained boots | unprivileged only with a journal ACL or group; gated elsewhere | count kernel lines for the current boot first; zero kernel lines means the journal is unreadable, not clean |
| `/sys/class/nvme/<ctrl>/{model,firmware_rev,state,address}` and `hwmon*/temp*_input`, controller resolved through `/sys/block/dm-*/slaves` | unprivileged | controller exists and `state` is `live` |
| `smartctl -H -A /dev/<ns>` | gated; exit 2 and `Permission denied` observed | parse `SMART overall-health self-assessment test result` and `Critical Warning`; missing text is `unverified(privilege)` |
| `nvme smart-log /dev/<ctrl>` | gated; exit 1 and `Permission denied` observed | parse `critical_warning`, `available_spare`, `percentage_used`, `media_errors`; missing fields are `unverified(privilege)` |
| optional companion privileged capture file, folded only when present and stamped with its sha256 | produced outside the census, never by the census | verify the file hash and the command list before use; the arm never invokes `sudo` |

The arm must never call `sudo`, never pass `-z`/`--reset`, never start a scrub, never write
`/var/lib/btrfs`, and never print the drive serial.

### Verdict mapping

- BLOCKED when the root btrfs filesystem cannot be identified (no btrfs row from `findmnt`),
  when `/sys/fs/btrfs/` cannot be listed, or when both the sysfs counters and the mountpoint
  `btrfs device stats` probe fail with an access error. A btrfs filesystem with no readable
  counter source is blocked, because the arm's core function is offline, not because the disk is
  bad.
- DEGRADED when any counter is non-zero; when `missing=1` or `writeable=0`; when a scrub record
  is absent while the timer is disabled or was never triggered (`unverified(never-scrubbed)`);
  when a scrub finished with errors, or when its timestamp is older than twice the configured
  cadence; when a status record exists but is unreadable (`unverified(status-unreadable)`); when
  SMART is unreadable unprivileged (`unverified(privilege)`); or when SMART is readable and shows
  a non-zero critical warning, `available_spare` at or below `available_spare_threshold`,
  `percentage_used` at or above 100, media or data integrity errors greater than zero, a
  non-PASSED overall result, or unsafe shutdowns rising between two recorded reads.
- HEALTHY only when every counted device has five zero counters, no device is missing, a
  completed scrub record exists with zero errors inside the cadence, and a readable SMART block
  is PASSED with critical warning 0, spare above threshold and zero media errors. Without
  privileged SMART evidence the arm can never emit HEALTHY.
- Profiles are carried as evidence, not as a defect: `data=single` alone does not degrade, but a
  detected read or checksum error on a single-profile data chunk escalates the note to
  `repair=none` and the verdict is at least DEGRADED, never "detected and repairable".
- Multiple btrfs filesystems: compute per filesystem, then take the worst, naming the UUID and
  mountpoint in the note.
- Rollup: fold into the existing worst-plane reduction at
  `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh:2659-2674`.
- Consequence of the HEALTHY rule above: without the optional companion privileged capture, this
  plane reports DEGRADED on every run on this host, because both SMART inputs are gated. That is
  the intended fail-honest behaviour under the census's never-a-fake-pass rule, and a run that is
  expected to be green must be handed the stamped companion capture rather than be given a pass
  on missing evidence.

Suggested note shape, modelled on the `mem=[…]` sub-verdict:

```
PLANE storage: DEGRADED (fs=<uuid> mounts=/ devid=1 errs=w0/r0/f0/c0/g0 devstat=ok;
profiles=data:single,metadata:dup,system:dup scrub=no-stats timer=disabled timer_preset=disabled
last=never statusdir=absent; nvme0=unverified(privilege) model=WD_BLACK_SN8100_1000GB fw=830ZRR02
temp_c=29; unknown=[smart,lifetime]; r26 vocab: storage-health-r26.md SH1-SH6)
```

### Fixtures and selftest cases

Reuse the existing hermetic mechanism: `run_selftest()` at
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh:1711`, the dispatcher
and `fx_default()` at `:1805`, `check()` at `:1912`, and the zero-mutation assertion
`fx_no_mutation()` at `:1904`. Add these seams, each with the `TSUKUROI_` prefix used by the
existing overrides documented at `:317-334`:

- `TSUKUROI_BTRFS_SYSFS` — a fixture root standing in for `/sys/fs/btrfs`, holding one or more
  UUID directories with `devinfo/<n>/{error_stats,missing,writeable,in_fs_metadata}`,
  `devices/dm-N`, `allocation/{data,metadata,system}/<profile>/{total_bytes,used_bytes}` and
  `checksum`.
- `TSUKUROI_BTRFS` — dispatcher stub for `btrfs`, answering `device stats`, `device stats -c`,
  `filesystem df --raw`, `scrub status --raw`; each answer backed by a fixture file and a fixture
  exit-code file, as the existing pacman stub does.
- `TSUKUROI_SCRUB_STATE_DIR` — a stand-in for `/var/lib/btrfs`, with cases for absent, present
  but mode 0700, and present with a readable `scrub.status.<uuid>`.
- `TSUKUROI_SMARTCTL` and `TSUKUROI_NVME` — stubs for `smartctl -H -A` and `nvme smart-log`,
  each with a stdout fixture and an exit-code fixture.
- `TSUKUROI_STORAGE_PRIV` — optional companion privileged capture path, empty by default.
- `TSUKUROI_JOURNALCTL`, `TSUKUROI_SYSTEMCTL`, `TSUKUROI_HOSTNAME_FILE` — already exist; extend
  the stub's `systemctl show` and `journalctl` replies with the storage keys and a fixture that
  contains `-- Boot <id> --` separator lines.

Minimum case set, each asserting exit code, verdict and evidence substring, and each also run
through `fx_no_mutation`:

1. healthy clean: five zero counters, no missing device, completed clean scrub inside cadence,
   timer enabled and triggered, readable SMART PASSED.
2. degraded counter: one non-zero counter, `device stats -c` exit 1, note names the counter and
   the device.
3. degraded missing device: `missing=1`, note names the devid.
4. degraded never scrubbed: `no stats available`, timer disabled, last trigger empty, status
   directory absent.
5. degraded stale scrub: readable status file older than twice the monthly cadence.
6. degraded status unknown: status directory present and unreadable, asserting the note says
   `unverified(status-unreadable)` and not `never`.
7. degraded SMART warning: PASSED plus critical warning non-zero, and a second case with spare at
   threshold and a third with media errors greater than zero.
8. degraded SMART unreadable: `smartctl` stub exit 2 with `Permission denied` on stdout, asserting
   `unverified(privilege)` and that the verdict is not HEALTHY.
9. blocked counters: sysfs tree unreadable and `btrfs device stats` stub exits 1 while printing
   `Permission denied` and no counter lines, asserting BLOCKED; a second variant keeps exit 0 but
   prints a truncated four-key sysfs file, asserting BLOCKED rather than a clean pass.
10. blocked no btrfs: `findmnt` stub returns no btrfs row.
11. blocked journal unreadable: current-boot kernel count zero while the error scan is also empty,
    asserting the arm does not report a clean error history.
12. separator trap: `journalctl` fixture that emits three `-- Boot … --` headers and no matches,
    asserting an error count of 0 and exit 0, mirroring the live observation in finding 5.
13. self-reference trap: fixture containing a `sudo` command line that quotes the BTRFS pattern,
    asserting the arm's count ignores non-kernel records.
14. dual controller: fixture with nvme0 and nvme1, asserting only the controller resolved
    through the btrfs device chain is judged, and the serial never appears in the note.
15. multi filesystem: two btrfs UUIDs, one clean and one degraded, asserting the worst is emitted
    and both are named.
16. single-profile error: data single plus a non-zero corruption counter, asserting `repair=none`.

## Remaining unknowns

- [unk] Whether a completed scrub's `/var/lib/btrfs/scrub.status.<uuid>` file is readable by an
  unprivileged user. The directory does not exist on this host, so the case cannot be measured;
  the man page `/usr/share/man/man8/btrfs-scrub.8.gz` (decompressed lines 125 to 131) states the
  status is recorded there and that `status` reads it when idle, and the installed binary carries
  the string `/var/lib/btrfs/scrub.status`. The arm must treat an unreadable record as unknown.
- [unk] The exact kernel capability check for the scrub-progress and device-info ioctls was not
  verified from source in this seat; the unprivileged success is [obs] on linux 7.2.11 with
  btrfs-progs 7.1, and the mechanism is [inf].
- [unk] Counter persistence across mounts cannot be observed while all counters are zero and the
  superblock is unreadable unprivileged.
- [inf] The `wheel` ACL on the journal is a local configuration, not a distribution default; a
  census arm that assumes it would report false clean histories elsewhere.

Scope: read=frozen round-26 capture and capture script, SCORECARD round-26 declaration, tools/tsukuroi-census.sh selected sections, round-25 routed defects, /sys/fs/btrfs and /sys/class/nvme trees, /proc/sys/kernel/dmesg_restrict, /var/log journal ACLs, btrfs-progs and smartmontools command output, systemd unit files; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w1/ScoutHostSurfaces.md; executed=read-only probes only: findmnt, lsblk, stat, cat, getfacl, ls, btrfs device stats, btrfs device stats -c, btrfs scrub status --raw, btrfs filesystem df --raw, btrfs filesystem show, btrfs filesystem usage, btrfs inspect-internal dump-super which failed with permission denied, systemctl show/is-enabled/is-active/cat/list-unit-files/list-timers/status, journalctl with read options, dmesg which failed with operation not permitted, smartctl which failed with permission denied, nvme smart-log which failed with permission denied, nvme list, nvme show-topology, sha256sum, diff, grep
Model: opencode-go/deepseek-v4.1-flash
Installs: none
