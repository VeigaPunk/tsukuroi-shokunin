ROW SC5 FIRST-READ: holds

Seat C2DraftRevSC5, wave-1 first falsifier for row SC5 of `corpus/knowledge/btrfs-scrub-record-r42.md` (read at f50c28d83e1832ecd7eba765caace531f45d6b27 via `git show f50c28d8…:corpus/knowledge/btrfs-scrub-record-r42.md`). No tool installs were made (preexisting curl/git/grep/sha256sum only). Scratch `/fast/scratch/hyaku/tsukuroi-r42/C2DraftRevSC5` removed after receipts were copied.

## Provenance (all pass)

- `cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-42/frozen/src && sha256sum -c SHA256SUMS` → `scrub.c: OK` / `CHANGES: OK`.
- Live fetch 2026-10-26: https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c → sha256 `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801`, identical to the frozen scrub.c; https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/CHANGES → `bd881ab899ba4f4fba820207c4cb671eacbb34843db4cf95fd7d90aaff2a0d22`, identical to the frozen CHANGES. The snapshot is byte-identical to the live tag.
- `sha256sum .ufo/waves/round-42/frozen/hostcap/capture.txt` → `942edc91a6b8fcda3ef29e88c3d54e7a9a48ec4cce302b8c1edcc89c8710643c`, the digest the corpus header claims (corpus-r42.md:3 of my extraction).
- FETCH.txt says tag v7.1 = `0a919c7d6e389c07920675b7fad3f793b92aa78b`; GitHub API `git/ref/tags/v7.1` returns object sha `0a919c7d6e389c07920675b7fad3f793b92aa78b` (type tag) — matches.

## Statement, sentence by sentence

1. "Each device has a scrub throughput limit in sysfs, `/sys/fs/btrfs/<fsid>/devinfo/<devid>/scrub_speed_max`" — HOLDS.
   - progs: frozen scrub.c:1214 `/* /sys/fs/btrfs/FSID/devinfo/1/scrub_speed_max */`, :1215 builds `"devinfo/%llu/scrub_speed_max"`.
   - kernel v7.2 fs/btrfs/sysfs.c:36 comment maps `devid_attrs` to `/sys/fs/btrfs/<uuid>/devinfo/<devid>`; :2021-2049 define `btrfs_devinfo_scrub_speed_max_show`/`_store` registered by `BTRFS_ATTR_RW(devid, scrub_speed_max, …)`.
   - host (kernel 7.2.11-arch1-1): `ls /sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1` → `error_stats fsid in_fs_metadata missing replace_target scrub_speed_max writeable`.
2. "(bytes per second; 0 means no limit)" — HOLDS.
   - kernel v7.2 fs/btrfs/scrub.c:1362-1363: "Throttling of IO submission, bandwidth-limit based, the timeslice is 1 second.  Limit can be set via /sys/fs/UUID/devinfo/devid/scrub_speed_max."; :1374-1377 `bwlimit = READ_ONCE(device->scrub_speed_max); if (bwlimit == 0) return;` — 0 disables throttling; the slice math sums bio bytes against `bwlimit` per 1 s, i.e. bytes/second.
   - progs prints raw bytes with a `/s` suffix: scrub.c:216-218 `pr_default(" (limit %s/s)", pretty_size_mode(limit, UNITS_RAW));` (same at :230-232).
3. "`btrfs scrub status` and `btrfs scrub start` read it and report a set limit, and `btrfs scrub limit` shows or sets it; all three arrived in btrfs-progs 6.6.3" — HOLDS.
   - status reads: scrub.c:1954 and :1977 (`read_scrub_device_limit`); prints only when set: :216-218 for `limit > 1`, :219-220 `limit == 1` → "(some device limits set)".
   - start reads: :1413 (`sp[i].old_limit`), :1449 (`sp[i].limit`, read after the :1414 write, so the effective run limit); reports: :1560-1561 `if (sp[i].limit > 0) pr_default(" (limit %s/s)\n", pretty_size(sp[i].limit));`.
   - limit shows/sets: `cmd_scrub_limit` :2022; reads :2118/:2149/:2194, writes :2125/:2156; registered :2215 `DEFINE_SIMPLE_COMMAND(scrub_limit, "limit")`.
   - all three in 6.6.3: CHANGES:460 heading `btrfs-progs-6.6.3 (2023-12-14)`, :467 (status), :468 (limit), :469 (start).
4. "A failed read is reported as 0" — HOLDS: scrub.c:1216-1218 `ret = sysfs_read_fsid_file_u64(fd, path, &limit); if (ret < 0) limit = 0;`; the helper returns the open error for a missing file (common/sysfs-utils.c v7.1:176-178: `fd = sysfs_open_fsid_file(fd, name); if (fd < 0) return fd;`).
5. "so the status command cannot tell 'no limit' from 'limit unreadable' (on a kernel without the file the limit silently reads as none)" — HOLDS: `read_scrub_device_limit` (scrub.c:1208-1220) returns a bare u64 with no error channel, and every print site gates on a nonzero value (:216-218, :230-232, :1560-1561), so both cases print nothing.
6. "A scrub that looks slow should be checked against this file before the device is blamed." — grounded: the kernel throttles scrub IO whenever the limit is nonzero (kernel fs/btrfs/scrub.c:1374 ff.), so a slow scrub can be the configured limit rather than the device.

## Quotes

- scrub.c:1215 text exact (grep -n match at 1215; the write-side twin at :1228 is correctly not the cited one — the row cites the read path).
- scrub.c:1218 `limit = 0;` exact.
- CHANGES:460, :467, :468 exact.
- Gap (not an error): the Statement's "scrub start … report a set limit" and "all three arrived in 6.6.3" rest on CHANGES:469, which the row does not quote. Proposed addition below.

## Host reading

- capture.txt:9 is `scrub_speed_max 1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1 0` — exactly what the row states ("The root's only device (devid 1) reads `scrub_speed_max` 0, no limit").
- capture.sh (frozen/hostcap/capture.sh) emits that line only when the file exists (`[ -e "$d/scrub_speed_max" ]`) and prints `$(cat "$d/scrub_speed_max" 2>&1)` — so the captured 0 is the file's content, a genuine read, not a failed read; the loop printed one line, so only devinfo/1 existed.
- Independent live re-check 2026-10-26: the same sysfs file still exists and the devinfo directory still lists only devid 1.

## Kernel file at the running kernel 7.2

Exists, verified two ways: the host sysfs listing above, and kernel v7.2 source `fs/btrfs/sysfs.c:2021-2049` (fetched 2026-10-26 from https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/fs/btrfs/sysfs.c?h=v7.2, 2702 lines; the raw.githubusercontent.com/torvalds/linux attempt returned HTTP 429 and was retried at git.kernel.org).

## Findings

1. [no defect] No sentence of the Statement, no Quote line number or text, and not the Host reading is wrong or overreaching. Row SC5 holds as written.
2. [strengthening] Add the missing changelog quote so the "scrub start" and "all three" claims are pinned like the others (insert after the CHANGES:468 quote line):
   **Quote.** `S238` CHANGES:469: "* scrub start: report the limit if set"
3. [observation, no row change needed] `btrfs scrub start` writes the limit unconditionally (scrub.c:1414) with `throughput_limit` defaulting to 0 (:1275, set from `-l` at :1319) and restores the previous value afterwards (:1597-1598) — i.e. a start without `-l` temporarily forces "no limit" for the run's duration. Consistent with the row; worth knowing for triage since the sysfs value read during such a run is not the standing limit.
4. [verification gaps] (a) The Arch build 7.1-1's packaging patches were not compared against upstream v7.1 (the row's Limits section already declares this; I did not compare either). (b) I did not run `btrfs scrub status` itself; the host reading was verified against the frozen capture plus a direct read-only sysfs listing. (c) The kernel-side introduction version of the sysfs attribute was not determined; the row makes no claim about it.

## Receipts

`.ufo/waves/round-42/w1/C2DraftRevSC5/`: `live-scrub.c`, `live-CHANGES` (v7.1 fetches, sha256-equal to the frozen snapshots), `kernel-sysfs-7.2.c`, `kernel-scrub-7.2.c` (kernel v7.2), `progs-sysfs-utils.c` (v7.1 helper), `corpus-r42.md` (row source at f50c28d8).
