ROW SC5 VERDICT: partly

# C2CritSC5 — adversarial read of row SC5 (item V-5b)

Seat C2CritSC5, lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, row SC5 of
`corpus/knowledge/btrfs-scrub-record-r42.md` at freeze commit `78abb8b5cdc9da511b4fc523e661517a68dd33d3`
(line 122-140). Row text unchanged at the dispatch tip (`git diff 78abb8b5 a968393c --
corpus/knowledge/btrfs-scrub-record-r42.md` = 0 lines); the file has no `Corrections` section
(`grep '^## '` → SC1-SC5, "How this changes OS triage", "Limits", "QUALITY check"), and SC5 carries no
appended correction after its Host reading. Receipt:
`.ufo/waves/round-42/w2/C2CritSC5/receipt.txt`.

Nothing below is a wrong line: all five Quote lines parse and their text occurs on the named line and inside
the row's frozen window (scrub.c 1208-1220, CHANGES 460-470; receipt, "SC5 quotes parse/occur/window check").
The defect is an overreaching clause in the Statement (sentence 2) plus a branch the row omits that changes
the operational reading.

## Verification performed

- `cd .ufo/waves/round-42/frozen/src && sha256sum -c SHA256SUMS` → `scrub.c: OK`, `CHANGES: OK` (receipt:2-3).
- Provenance: refetched `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c` and
  `.../CHANGES` (access 2026-10-26); sha256 `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801`
  and `bd881ab899ba4f4fba820207c4cb671eacbb34843db4cf95fd7d90aaff2a0d22`, `cmp` IDENTICAL to the frozen files
  (receipt:8-11). Line pins below are therefore upstream v7.1 lines, not a local edit.
- Kernel side: `https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/sysfs.c` (access 2026-10-26,
  sha256 `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43`) and
  `.../v7.2/fs/btrfs/scrub.c`; btrfs-progs helper `common/sysfs-utils.c` from the v7.1 raw URL.
- Host, read-only: `/sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/scrub_speed_max` = `0`;
  `btrfs scrub status -d /` → exit 0, prints `Scrub device /dev/mapper/root (id 1)` then
  `no stats available` and no limit line; `btrfs scrub limit /` → exit 0, table row `1  -  /dev/mapper/root`
  (receipt:31-46).

## Per-sentence finding

### Statement sentence 1 — holds
"Each device has a scrub throughput limit in sysfs, `/sys/fs/btrfs/<fsid>/devinfo/<devid>/scrub_speed_max`
(bytes per second; 0 means no limit)."
- The attribute is a per-devid RW attribute: kernel `sysfs.c:2021-2028` (show emits
  `device->scrub_speed_max`), `:2031-2046` (store via `memparse`, `WRITE_ONCE`), `:2048-2049`
  `BTRFS_ATTR_RW(devid, scrub_speed_max, ...)`, registered in `devid_attrs` at `:2113`; the path comment is
  `sysfs.c:2105` "Path: /sys/fs/btrfs/<uuid>/devinfo/<devid>/".
- Unit and 0: kernel `scrub.c:1361-1363` "Throttling of IO submission, bandwidth-limit based, the timeslice
  is 1 second.  Limit can be set via /sys/fs/UUID/devinfo/devid/scrub_speed_max." and `:1374-1376`
  `bwlimit = READ_ONCE(device->scrub_speed_max); if (bwlimit == 0) return;` — bytes per second, 0 = no
  throttle. The same semantics are in the pinned snapshot: `" (limit %s/s)"` at scrub.c:216-218/230-232,
  `--limit` help "(0 for unlimited), restored afterwards" at scrub.c:1747, and `-l` help "or 0 to reset to
  unlimited" at scrub.c:2017.

### Statement sentence 2 — partly (overreaches)
"`btrfs scrub status` and `btrfs scrub start` read it and report a set limit, and `btrfs scrub limit` shows
or sets it; all three arrived in btrfs-progs 6.6.3."
- True parts: status reads at scrub.c:1954 (per-device) and :1977 (summary); the limit command is
  scrub.c:2011-2013 with show at :2194-2202 and set at :2125/:2156; start/status/limit all sit in the 6.6.3
  block — CHANGES:460 header, :467 status, :468 limit, :469 "scrub start: report the limit if set".
- Where it overreaches: the clause "report a set limit" is stated for both commands without the conditions
  the code imposes, and the two commands do not report the same thing.
  - status reports nothing when the device has no record line: scrub.c:1957-1961 passes `p = NULL` to
    `print_scrub_dev`, and the limit reaches the printer only inside `if (p)` at scrub.c:357-376; the host
    demonstrates the branch: `btrfs scrub status -d /` prints the device header and `no stats available`
    with no limit line (receipt:35-40). A limit is also printed numerically only when `limit > 1`
    (scrub.c:216-218, 230-232); a limit of exactly 1 prints `(some device limits set)`
    (scrub.c:219-220, 233-234), and the multi-device summary collapses any set limit to that note
    (scrub.c:396-397).
  - start reports the limit it writes, not the value read from sysfs: it reads the old value only to restore
    it (scrub.c:1413), unconditionally writes `throughput_limit` — `u64 throughput_limit = 0;` at
    scrub.c:1275, parsed from `--limit` at :1319 — at :1414, reads back at :1449, and prints
    `(limit %s/s)` only when that value is > 0 at :1560-1563. Thus a limit pre-set with
    `btrfs scrub limit --all --limit …` is not reported by a plain `btrfs scrub start` (it reports its own 0),
    while a `--limit X` run reports X. The restore at scrub.c:1598 runs inside the same loop *before*
    `pthread_join` at :1608, and the scrub thread blocks in `ioctl(BTRFS_IOC_SCRUB, …)` at scrub.c:965 until
    the kernel scrub ends, so after the restore the kernel throttles with `old_limit`, not with the value the
    command reported [inference from scrub.c:965 + :1596-1608]. Upstream devel later moved the same block
    out of the join loop (`https://raw.githubusercontent.com/kdave/btrfs-progs/devel/cmds/scrub.c`, access
    2026-10-26, devel:1640-1648 "Revert to the older scrub limits." after the joins), which corroborates that
    the v7.1 placement is the anomalous one.
- Therefore the sentence is true only under the charitable reading "start reports the limit it was told to
  set"; read against the sysfs value the row is about, it claims a report that does not happen, and it omits
  the v7.1 restore-before-join branch that makes the reported value differ from the throttling value.

### Statement sentence 3 — holds
"A failed read is reported as 0, so the status command cannot tell 'no limit' from 'limit unreadable' (on a
kernel without the file the limit silently reads as none)."
- scrub.c:1216-1218: `ret = sysfs_read_fsid_file_u64(fd, path, &limit); if (ret < 0) limit = 0;`. The helper
  returns the negative open/read error without printing anything (btrfs-progs v7.1
  `common/sysfs-utils.c:171-190`), so an absent attribute (pre-6.6 kernel) or an unreadable one is
  indistinguishable from a genuine 0 at scrub.c:216-234/396-397. "Silently" is exact: no warning on this
  path.

### Statement sentence 4 — holds as advice, wording qualified by the correction
"A scrub that looks slow should be checked against this file before the device is blamed."
- The throttle reads this file during the scrub (kernel `scrub.c:1374-1375`), so the advice is grounded.
  The timing caveat is the same v7.1 branch as above: scrub.c:1598 restores `old_limit` before the join at
  :1608, so the file read after that point holds the restored value, not the `--limit` value the command
  reported. As written ("before the device is blamed") the advice survives; the correction makes it explicit.

### Host reading — holds
"The root's only device (devid 1) reads `scrub_speed_max` 0, no limit (capture.txt:9)."
- Frozen capture line 9 is
  `scrub_speed_max 1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1 0`; the capture file's sha256 is
  `942edc91a6b8fcda3ef29e88c3d54e7a9a48ec4cce302b8c1edcc89c8710643c` as pinned in the entry header and the
  frozen counter. Live repeat: `findmnt -no FSTYPE,UUID /` → `btrfs 1d02a454-…`; `/sys/fs/btrfs/` holds one
  fsid; its `devinfo/` holds only `1`; `cat …/devinfo/1/scrub_speed_max` → `0` (receipt:31-34). "Only device"
  is supported by the single devinfo entry and the single-device summary path (kernel scrub.c:396-397 comment
  "If there's only one device").

## Strongest counterexample (code + host)

1. `btrfs scrub limit --all --limit 100M /` writes 100M per device (scrub.c:2156 → :1228-1229).
2. `btrfs scrub start /` (no `--limit`) then writes `throughput_limit` = 0 over it at scrub.c:1414 *before*
   any scrub thread exists (threads are created at scrub.c:1565), reads back 0 at :1449, and prints no limit
   at :1560-1563; the 100M is restored at :1598. So "scrub start … report a set limit" reports nothing for a
   limit that is set in sysfs exactly as the row's first sentence defines it.
3. Conversely `btrfs scrub start --limit 200M /` reports 200M at scrub.c:1560-1561 and again in the summary
   (scrub.c:1664-1669 → :216-232), but the restore at :1598 rewrites `old_limit` before the join at :1608
   while the kernel scrub is still blocked in :965, so the value in force after the restore — and the value a
   reader of `scrub_speed_max` sees during that scrub — is `old_limit`, not the reported 200M.
4. Independently, status's report is gated on a device record: with no record the command prints the header
   and `no stats available` and no limit (scrub.c:1957-1961 + :357-376; observed live, receipt:35-40), and a
   limit of exactly 1 is printed as the multi-device note (scrub.c:219-220, 233-234). A running scrub whose
   recording was disabled (the SC3 case) is exactly the state where status shows neither rate nor limit.

## Smallest safe correction

Replace Statement sentence 2 with:

> `btrfs scrub status` reads the value per device but prints it only inside a stats block of a device that has
> a record line: a device without one prints the header and `no stats available` and no limit
> (scrub.c:1957-1961, 357-376); the value is printed numerically only when it exceeds 1 byte/s, and exactly 1
> prints `(some device limits set)` (scrub.c:216-220, 230-234), which is also all the multi-device summary
> prints (scrub.c:396-397). `btrfs scrub start` reads the existing value only to restore it (scrub.c:1413,
> 1596-1598) and reports the limit it writes for the run — its `--limit` value, 0 (unlimited) when absent
> (scrub.c:1275, 1319, 1414, 1449, 1560-1563, 1747); in v7.1 that restore runs before the join
> (scrub.c:1598 vs :1608), so once it lands the kernel throttles with the old value, not the reported one.
> `btrfs scrub limit` shows the per-device values (`-` for 0, scrub.c:2194-2202) or sets them with `--all`
> or `--devid` plus `--limit` (scrub.c:2125, 2156); the status report, the start report and the command all
> arrived in btrfs-progs 6.6.3.

Add the missing arrival quote inside the frozen CHANGES window (460-470):

> `**Quote.** `S238` CHANGES:469: "* scrub start: report the limit if set"`

Qualify Statement sentence 4:

> A scrub that looks slow should be checked against this file while it runs (the v7.1 restore at
> scrub.c:1598 puts the previous value back before the scrub finishes) before the device is blamed.

No change is needed to sentence 1, sentence 3 or the Host reading.

## What I did not do

- Did not run `btrfs scrub start/cancel/resume`, did not set or write any `scrub_speed_max`, did not touch
  `/var/lib/btrfs`, `/etc`, `/var/lib` or any mount; no sudo. All host evidence is read-only.
- Did not run either frozen counter (the C1 counter is CPU-heavy and this item does not call for it) and did
  not edit any lane, fleet or sibling file. Scratch `/fast/scratch/hyaku/tsukuroi-r42/C2CritSC5` is removed
  after the receipt was copied into the seat dir.
- The claim that the kernel throttles with the restored value after scrub.c:1598 is an inference (labelled
  as such) from the blocking ioctl at scrub.c:965 and the restore-before-join order; it was not demonstrated
  by starting a scrub, which the host guard forbids.
