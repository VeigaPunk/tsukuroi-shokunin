ROW SC5 VERDICT: holds

Seat C2RevSC5, wave-2 counted reviewer for row SC5 of `corpus/knowledge/btrfs-scrub-record-r42.md`. Row read from the working tree, which is byte-identical to the dispatch tip for this file: `git diff 78abb8b5cdc9da511b4fc523e661517a68dd33d3 -- corpus/knowledge/btrfs-scrub-record-r42.md` → 0 lines, `git status --porcelain` on the file → empty; no `Corrections` section exists anywhere in the file (grep for `Corrections|correction`: no matches) and the file ends at the QUALITY check (:164-168). I did not write this row. No tool installs were made (preexisting curl/git/grep/sed/sha256sum only). Scratch `/fast/scratch/hyaku/tsukuroi-r42/C2RevSC5` (TMPDIR pointed there) removed after receipts were copied.

## Provenance (all pass)

- `cd .ufo/waves/round-42/frozen/src && sha256sum -c SHA256SUMS` → `scrub.c: OK`, `CHANGES: OK`.
- Kernel side fetched 2026-10-26: https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/sysfs.c (2702 lines) and https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/scrub.c (3331 lines); both saved as receipts.
- btrfs-progs v7.1 helper fetched 2026-10-26: https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/common/sysfs-utils.c.
- Frozen capture digests: `sha256sum capture.txt capture.sh` → `942edc91a6b8fcda3ef29e88c3d54e7a9a48ec4cce302b8c1edcc89c8710643c` / `3ece27d0afb1d7b24884c677c8db1aef84db666a0e9f60f62357d8ba1dae077b`.

## Statement, sentence by sentence

1. "Each device has a scrub throughput limit in sysfs, `/sys/fs/btrfs/<fsid>/devinfo/<devid>/scrub_speed_max` (bytes per second; 0 means no limit)." — TRUE.
   - Path form, progs side: frozen scrub.c:1214 comment `/* /sys/fs/btrfs/FSID/devinfo/1/scrub_speed_max */`, :1215 `snprintf(path, sizeof(path), "devinfo/%llu/scrub_speed_max", devid);`; the relative name resolves under the fsid dir because `sysfs_open_fsid_file_flags` (progs v7.1 common/sysfs-utils.c:29-47) does `path_cat3_out(sysfs_file, "/sys/fs/btrfs", fsid_str, filename)` after reading the fsid from the mount fd.
   - Path form and per-device existence, kernel side: v7.2 fs/btrfs/sysfs.c:36 maps `devid_attrs` to `/sys/fs/btrfs/<uuid>/devinfo/<devid>`; :2105-2106 comment `Path: /sys/fs/btrfs/<uuid>/devinfo/<devid>/`; :2107-2116 `devid_attrs[]` includes `BTRFS_ATTR_PTR(devid, scrub_speed_max)` at :2113, registered for every device kobject; :2021-2029 show (`sysfs_emit(buf, "%llu\n", READ_ONCE(device->scrub_speed_max))` at :2028), :2031-2047 store, :2048-2049 `BTRFS_ATTR_RW(devid, scrub_speed_max, …)`.
   - Units and 0-means-no-limit: kernel v7.2 fs/btrfs/scrub.c:1362-1363 comment "Throttling of IO submission, bandwidth-limit based, the timeslice is 1 second.  Limit can be set via /sys/fs/UUID/devinfo/devid/scrub_speed_max."; :1368 `time_slice = 1000` (ms); :1374-1376 `bwlimit = READ_ONCE(device->scrub_speed_max); if (bwlimit == 0) return;` (0 disables throttling); :1382 `div = clamp(bwlimit / (16 * 1024 * 1024), 1, 64)` and :1395 `if (sctx->throttle_sent <= div_u64(bwlimit, div))` — bytes accumulated against the limit within a 1 s slice, i.e. bytes per second. Progs prints the value with a `/s` suffix: frozen scrub.c:216-218 (raw) and :230-234 (non-raw) `pr_default(" (limit %s/s)", …)`; `btrfs scrub limit` prints 0 as "unlimited" (:2121-2123, :2152-2154).
2. "`btrfs scrub status` and `btrfs scrub start` read it and report a set limit, and `btrfs scrub limit` shows or sets it; all three arrived in btrfs-progs 6.6.3." — TRUE.
   - status reads: frozen scrub.c:1954 and :1977 call `read_scrub_device_limit`; the value reaches the output via `print_scrub_dev` (:347-350, `u64 limit` parameter) → `print_scrub_summary`, which prints ` (limit %s/s)` only when `limit > 1` (:216-218 raw, :230-234 non-raw) and ` (some device limits set)` when `limit == 1` (the multi-device marker set at :396 `if (nr_devices != 1 && limit) limit = 1;`).
   - start reads and reports: :1413 `sp[i].old_limit = read_scrub_device_limit(fdmnt, devid);`, :1414 writes a `-l` limit if given, :1449 `sp[i].limit = read_scrub_device_limit(fdmnt, devid);` (read after the write, so the effective run limit), reported at :1559-1563 `pr_default("Starting scrub on devid %llu", devid); if (sp[i].limit > 0) pr_default(" (limit %s/s)\n", …)`; restored afterwards (:1597-1598, and the `--limit` OPTLINE at :1747 says "restored afterwards").
   - limit shows or sets: usage :2012-2013 "Show or set scrub limits on devices of the given filesystem."; set path reads the old value then writes (:2118-2125 single devid, :2149-2156 all devices); show path builds a table from `read_scrub_device_limit` (:2194-2200); registered :2215 `DEFINE_SIMPLE_COMMAND(scrub_limit, "limit")`.
   - all three in 6.6.3: CHANGES:460 heading `btrfs-progs-6.6.3 (2023-12-14)` with :467 (status), :468 (limit), :469 `* scrub start: report the limit if set`. Note: :469 is not quoted by the row (see Findings 1) but is present in the pinned snapshot and carries the start leg.
3. "A failed read is reported as 0, so the status command cannot tell "no limit" from "limit unreadable" (on a kernel without the file the limit silently reads as none)." — TRUE.
   - frozen scrub.c:1216-1218: `ret = sysfs_read_fsid_file_u64(fd, path, &limit); if (ret < 0) limit = 0; return limit;` — every failure mode collapses to 0.
   - The helper fails negative on a missing file: progs v7.1 common/sysfs-utils.c:171-178 `fd = sysfs_open_fsid_file(fd, name); if (fd < 0) return fd;` (open failure → `-errno`, :29-47), also read failure (:180-182) and parse failure (:184-186) return negative.
   - Indistinguishability: `read_scrub_device_limit` returns a bare u64 (frozen scrub.c:1208-1220) with no error channel, and every print site gates on a nonzero value (:216-218, :230-234, :1560-1561), so a failed read and a stored 0 produce identical output — nothing is printed in either case.
4. "A scrub that looks slow should be checked against this file before the device is blamed." — grounded triage advice, no overreach: the kernel throttles scrub IO whenever the limit is nonzero (kernel v7.2 fs/btrfs/scrub.c:1374-1395), so a slow scrub can be the configured limit rather than the device; the row's triage bullet (:150) repeats it consistently.

## Host reading

"The root's only device (devid 1) reads `scrub_speed_max` 0, no limit (capture.txt:9)." — TRUE.
- capture.txt:9 (digest-pinned, above) is `scrub_speed_max 1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1 0`; the fsid equals `root_fsid` on capture.txt:5.
- "only device": capture.sh (frozen/hostcap/capture.sh) loops over `/sys/fs/btrfs/*/devinfo/*` and prints one line per devinfo dir that has the file; exactly one line was printed, so exactly one devinfo dir existed at capture time. Independent live re-check 2026-10-26 (receipt `live-devinfo.txt`): `ls /sys/fs/btrfs/*/devinfo/` → only `1d02a454-c549-4a35-b567-89d60902af8e/devinfo/: 1`; `cat …/devinfo/1/scrub_speed_max` → `0`; `findmnt -no UUID /` → `1d02a454-c549-4a35-b567-89d60902af8e`.
- "no limit": 0 disables kernel throttling (kernel v7.2 fs/btrfs/scrub.c:1374-1376) and progs prints 0 as "unlimited" (frozen scrub.c:2121-2123).
- The captured 0 is a genuine read of the file content, not a failed read: capture.sh emits `$(cat "$d/scrub_speed_max" 2>&1)` only when `[ -e "$d/scrub_speed_max" ]`.

## Quote checks (all five verbatim at the cited line)

- `S237` scrub.c:1215 — `	snprintf(path, sizeof(path), "devinfo/%llu/scrub_speed_max", devid);` — occurs exactly (receipt `quotes-check.txt`). The write-side twin at :1228 is correctly not the cited line; the row cites the read path.
- `S237` scrub.c:1218 — `		limit = 0;` — occurs exactly.
- `S238` CHANGES:460 — `btrfs-progs-6.6.3 (2023-12-14)` — occurs exactly.
- `S238` CHANGES:467 — `   * scrub status: report limit if set in sysfs/../scrub_speed_max` — occurs exactly (the row's quote omits the leading indentation; the text occurs on the line).
- `S238` CHANGES:468 — `   * scrub limit: new command to show or set the per-device scrub limits` — occurs exactly.

## Findings

1. [strengthening, not an error — verdict unaffected] The Statement's "scrub start … report a set limit" leg and half of the "all three arrived in btrfs-progs 6.6.3" claim rest on CHANGES:469, which the row does not quote (its quotes pin :460/:467/:468). The line is present in the pinned, digest-checked snapshot, immediately after quoted :468, so nothing asserted is unsupported; the row family tolerates unquoted minor legs (SC3 likewise leaves its "failed to record the result" clause unquoted). Recommended insertion after the CHANGES:468 quote line:
   **Quote.** `S238` CHANGES:469: "* scrub start: report the limit if set"
2. [observation, no row change] `btrfs scrub start` writes the limit unconditionally (frozen scrub.c:1414) with `throughput_limit` defaulting to 0 and restores the previous value afterwards (:1597-1598; :1747 "restored afterwards") — a start without `-l` temporarily forces "no limit" for the run's duration, so the sysfs value read during such a run is not the standing limit. Consistent with the row; worth knowing for the triage reading.
3. [verification gaps] (a) I did not compare the Arch 7.1-1 packaging against upstream v7.1 (the row's Limits section declares the no-patch claim from wave-1 C2ExecLiveSources; I did not re-derive it). (b) I did not run `btrfs scrub status` myself; the host reading was verified against the frozen capture plus my own read-only sysfs listing. (c) I did not determine the kernel version that introduced the sysfs attribute; the row makes no claim about it.

## Receipts

`.ufo/waves/round-42/w2/C2RevSC5/`: `kernel-sysfs-7.2.c`, `kernel-scrub-7.2.c` (Linux v7.2 fetches, 2026-10-26), `progs-sysfs-utils-v7.1.c` (btrfs-progs v7.1 helper), `quotes-check.txt` (the five cited lines printed verbatim), `live-devinfo.txt` (live read-only re-check + capture digests).
