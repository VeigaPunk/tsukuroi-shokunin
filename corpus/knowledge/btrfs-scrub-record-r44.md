source: S237 S240 S242 S243 S244 S245 (rows in `corpus/SOURCES.md`; S237 is the round-42 snapshot `.ufo/waves/round-42/frozen/src/scrub.c` (btrfs-progs v7.1); S240 is `.ufo/waves/round-43/frozen/src/ioctl.c`; S242, S243 and S244 are `.ufo/waves/round-44/frozen/src/scrub.c`, `sysfs.c`, `btrfs-scrub@.timer`, `btrfs-scrub@.service` and `PKGBUILD`, digests in that directory's `SHA256SUMS`, fetch log `FETCH.txt`; S245 is the host capture `.ufo/waves/round-44/frozen/hostcap/capture.txt`, sha256 efb523889035cba62235d904b9e254068a7083dd07e7bb338ce2a803a3e84900)
verified-at: 2026-10-26 (Linux tag v7.2.11, peeled commit a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea; btrfs-progs tag v7.1, peeled commit 4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b; Arch packaging btrfs-progs tag 7.1-1, commit 0c0a4d77b318084ecd35aeeb6888d8a5b4d6e3e0; host btrfs-progs 7.1-1, kernel 7.2.11-arch1-1; capture 2026-10-26T23:53:22Z)
recheck: on-release — re-fetch the URLs in `.ufo/waves/round-44/frozen/src/FETCH.txt` and compare `sha256sum` with its `SHA256SUMS`; re-run `bash .ufo/waves/round-44/frozen/hostcap/capture.sh <file>` (unprivileged, read-only); `python3 tools/check-scrub-record-r44.py --revision <REV>`

# The btrfs scrub record, round 44: when the kernel says "running", the per-device speed limit, and the packaged scrub timer

Scope: the storage-integrity frontier, scrub record line (`PROVINCE.md` Frontier; `corpus/README.md` `## Frontier`).
Round 43 (`corpus/knowledge/btrfs-scrub-record-r43.md`) grounded SR1, SR3 and SR6; its SR6 says an unprivileged
caller never sees `running` and leaves open what a privileged caller's "running" means. This entry adds three rows the
round-44 census arm (`SCRUB btrfs-scrub-record …`, `tools/tsukuroi-census.sh`) relies on: SR7, the success direction
of the scrub-progress ioctl; SR8, the per-device `scrub_speed_max` attribute the arm reads; SR9, the scrub timer and
service Arch ships, whose enabled instances the arm counts. Nothing here runs a scrub, writes sysfs, enables a unit
or calls a privileged ioctl.

## SR7

**Statement.** In Linux v7.2.11 a device carries a scrub context exactly while a scrub or device-replace run is
in progress on it: `btrfs_scrub_dev` refuses with `-EINPROGRESS` when `dev->scrub_ctx` is already set, attaches its
context at scrub.c:3159 after all refusal checks and before any scrub work, and clears it at scrub.c:3222 once the
scrub work has ended, before the function's finalize tail; every return path leaves the field as it found it.
`btrfs_scrub_dev` serves both a scrub and a device replace (its `is_dev_replace` argument) [inference for the replace
side: its caller is in `fs/btrfs/dev-replace.c`, opened this round at v7.2.11 lines 701-703 and 1265-1268 but not
pinned]. `btrfs_scrub_progress` looks the requested devid up under `device_list_mutex`; it copies that context's
`stat` and returns 0 only when the device exists and carries a context, returns `-ENOTCONN` when the device exists
without one, and `-ENODEV` when no device has that devid. The progress ioctl handler (after its `CAP_SYS_ADMIN`
gate, SR6) returns that value and copies the arguments back to the caller only when it is 0. So for a privileged
`btrfs scrub status`, `is_scrub_running_in_kernel` (SR6) answers 1 exactly when some device it asks about is being
scrubbed, or is the source of a running replace, at that moment: an idle device answers `ENOTCONN`, never 0, and the
answer is a momentary per-device reading, not a record of past scrubs.

**Quote.** `S242` scrub.c:3081: "bool readonly, bool is_dev_replace)"

**Quote.** `S242` scrub.c:3147: "if (dev->scrub_ctx ||"

**Quote.** `S242` scrub.c:3153: "ret = -EINPROGRESS;"

**Quote.** `S242` scrub.c:3159: "dev->scrub_ctx = sctx;"

**Quote.** `S242` scrub.c:3222: "dev->scrub_ctx = NULL;"

**Quote.** `S242` scrub.c:3321: "int btrfs_scrub_progress(struct btrfs_fs_info *fs_info, u64 devid,"

**Quote.** `S242` scrub.c:3331: "sctx = dev->scrub_ctx;"

**Quote.** `S242` scrub.c:3333: "memcpy(progress, &sctx->stat, sizeof(*progress));"

**Quote.** `S242` scrub.c:3336: "return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;"

**Quote.** `S240` ioctl.c:3139: "ret = btrfs_scrub_progress(fs_info, sa->devid, &sa->progress);"

**Quote.** `S240` ioctl.c:3141: "if (ret == 0 && copy_to_user(arg, sa, sizeof(*sa)))"

**Host reading.** Not observable unprivileged: the caller has no effective capabilities (capture.txt:1), so the ioctl
stops at the SR6 gate before this code runs (round-43 S241).

## SR8

**Statement.** Each btrfs device's scrub bandwidth limit is the sysfs attribute `devinfo/<devid>/scrub_speed_max`
under `/sys/fs/btrfs/<fsid>/`, declared with `BTRFS_ATTR_RW`, which builds the attribute with mode 0644: any user can
read it, and only its owner (root) can write it. Reading prints the device's in-memory `scrub_speed_max` as one
decimal number followed by a newline. Writing parses the text with `memparse` (sysfs.c:2040), skips trailing
whitespace including the newline, and rejects anything else after the number with `-EINVAL`; that `memparse`
accepts a size suffix such as `K`, `M` or `G` is [inference: its definition in `lib/cmdline.c` is not pinned].
The scrub throttle reads the value as bytes per second and returns at once when it is 0, so 0 means
no limit. The value is in-memory only: written with `WRITE_ONCE` into `struct btrfs_device` and read with
`READ_ONCE`; nothing on this write path persists it, so a single-device filesystem loses it on unmount and the
device's `kzalloc` initialisation restores 0 [inference: no persistence site was found in `fs/btrfs` at v7.2.11;
`kzalloc_obj` zeroes the device allocation].

**Quote.** `S243` sysfs.c:72: "#define BTRFS_ATTR_RW(_prefix, _name, _show, _store)"

**Quote.** `S243` sysfs.c:74: "__INIT_KOBJ_ATTR(_name, 0644, _show, _store)"

**Quote.** `S243` sysfs.c:2028: "return sysfs_emit(buf, "%llu\n", READ_ONCE(device->scrub_speed_max));"

**Quote.** `S243` sysfs.c:2040: "limit = memparse(buf, &endptr);"

**Quote.** `S243` sysfs.c:2042: "endptr = skip_spaces(endptr);"

**Quote.** `S243` sysfs.c:2044: "return -EINVAL;"

**Quote.** `S243` sysfs.c:2048: "BTRFS_ATTR_RW(devid, scrub_speed_max, btrfs_devinfo_scrub_speed_max_show,"

**Quote.** `S242` scrub.c:1380: "bwlimit = READ_ONCE(device->scrub_speed_max);"

**Quote.** `S242` scrub.c:1381: "if (bwlimit == 0)"

**Host reading.** The host's only visible btrfs device (fsid 1d02a454-c549-4a35-b567-89d60902af8e, devid 1) has `scrub_speed_max` mode 644, owner root, value 0: no
limit (capture.txt:4), read as uid 1000 with no effective capabilities (capture.txt:1).

## SR9

**Statement.** The scheduled scrub on Arch comes from the distribution package, not from btrfs-progs upstream: the Arch
btrfs-progs 7.1-1 `PKGBUILD` installs `btrfs-scrub@.service` and `btrfs-scrub@.timer` into
`/usr/lib/systemd/system`. The timer fires `OnCalendar=monthly` with `RandomizedDelaySec=1w`, keeps `Persistent=true`
and is `WantedBy=timers.target`, so enabling an instance creates a `timers.target.wants/btrfs-scrub@<instance>.timer`
link. The service runs `btrfs scrub start -B %f` with `KillSignal=SIGINT`. In btrfs-progs v7.1 `-B` keeps the start
in the foreground and sets `do_print`, so the later recording failures of SR3 are printed into the service's
output; the foreground start installs a SIGINT handler that issues `BTRFS_IOC_SCRUB_CANCEL`, so a SIGINT sent to it
(the service's stop signal) cancels the running scrub, and a device whose scrub ioctl returns nonzero is recorded with
`canceled` set, which `btrfs scrub resume` later takes up (SR3).

**Quote.** `S244` PKGBUILD:100: "install -Dm644 btrfs-scrub@.service "${pkgdir}/usr/lib/systemd/system/btrfs-scrub@.service""

**Quote.** `S244` PKGBUILD:101: "install -Dm644 btrfs-scrub@.timer "${pkgdir}/usr/lib/systemd/system/btrfs-scrub@.timer""

**Quote.** `S244` btrfs-scrub@.timer:5: "OnCalendar=monthly"

**Quote.** `S244` btrfs-scrub@.timer:7: "RandomizedDelaySec=1w"

**Quote.** `S244` btrfs-scrub@.timer:8: "Persistent=true"

**Quote.** `S244` btrfs-scrub@.timer:11: "WantedBy=timers.target"

**Quote.** `S244` btrfs-scrub@.service:9: "KillSignal=SIGINT"

**Quote.** `S244` btrfs-scrub@.service:10: "ExecStart=/usr/bin/btrfs scrub start -B %f"

**Quote.** `S237` scrub.c:1293: "do_background = false;"

**Quote.** `S237` scrub.c:1295: "do_print = true;"

**Quote.** `S237` scrub.c:421: "ret = ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL);"

**Quote.** `S237` scrub.c:1546: "scrub_handle_sigint_child(fdmnt);"

**Quote.** `S237` scrub.c:969: "sp->stats.canceled = !!ret;"

**Host reading.** No instance is enabled: no `btrfs-scrub@*.timer` link under `timers.target.wants`
(capture.txt:5), `btrfs-scrub@-.timer` is `disabled` (capture.txt:6); the installed unit files are byte-identical to
the pinned ones (capture.txt:7, capture.txt:8), and the timer is owned by btrfs-progs 7.1-1 (capture.txt:9); the
capture does not query the service file's package owner.

## How this changes OS triage

- "Running" from a privileged `btrfs scrub status` means a device is being scrubbed now (SR7); it says nothing about
  when the last scrub ran or how it ended — read the record for that.
- A slow scrub with `scrub_speed_max` nonzero is the configured limit at work (SR8); 0 means none. The limit is root's
  to set; the census only reports it (`limited=`).
- A monthly scrub exists only if an instance of the packaged timer is enabled (SR9); the census counts the
  `timers.target.wants` links (`timers=`). Stopping a running scrub service cancels the scrub and leaves a canceled,
  resumable record (SR9, SR3).

## Limits

- Kernel behaviour is pinned at Linux v7.2.11 source lines; the Arch kernel 7.2.11-arch1-1 patch touches no file
  under `fs/` (round-43 entry, Limits), so `fs/btrfs/scrub.c` and `sysfs.c` of the booted kernel are the pinned ones
  [inference carried from round 43; not re-measured this round].
- SR7 is read from source only: no privileged ioctl is run on this host.
- SR9's systemd side (that `KillSignal=` is the signal `systemctl stop` sends) is systemd.kill(5) behaviour and is not
  pinned here [inference]; the pinned part is the unit text and the btrfs-progs handler.

## Round-45 grounding and gate status (appended 2026-10-27, L1 TsukuroiR45)

Appended; the rows above are unchanged. **Gate status:** the round-44 depth gate for SR7-SR9 FAILED
(`tools/check-scrub-record-r44.py` at `fbfef071`: `verdicts_ok 0`; `.ufo/waves/round-44/after/c2-final-fbfef071.jsonl`),
and the SR8/SR9 narrowings made after the counted reads were judged by no counted seat
(`corpus/lessons/round-44-verifier-spotcheck.md` §2 C2, routed defect D3). Until a counted non-author read binds them,
SR7-SR9 are pending, not admitted. **Grounding:** the three `[inference]` marks above (the replace caller of
`btrfs_scrub_dev` in SR7, `memparse` suffixes in SR8, `KillSignal=` as the stop signal in SR9) are grounded on pinned
source in `corpus/knowledge/btrfs-scrub-grounding-r45.md` rows GR2, GR1 and GR3.

## Round-45 qualification — the stop outcome (appended 2026-10-27, C2 sweep)

Appended; nothing above is rewritten, and the grounding it points at is `corpus/knowledge/btrfs-scrub-grounding-r45.md`
row GR3. The block above grounds SR9's systemd side; it does not qualify the outcome sentence at `:99-101` or the
triage bullet at `:140-142`. On this host `systemctl stop btrfs-scrub@<instance>.service` is SIGINT
(`KillSignal=2`), then SIGCONT, and SIGKILL only if a process remains once `TimeoutStopUSec=5s` has passed (GR3; S248
`systemd.kill.xml:68,91,96,101,108,114-115`; S249 `capture.txt:3-5`). The SIGINT handler issues
`BTRFS_IOC_SCRUB_CANCEL` (S237 `scrub.c:416-424`, installed in the foreground start at `:1546`), but whether the start
then writes its `canceled` record before the SIGKILL is not established [inference]. "Leaves a canceled, resumable
record" therefore holds for a start that finishes that write inside the window; otherwise the record stands as it was
last written during the run, and `btrfs scrub resume` sees whatever that record says.
