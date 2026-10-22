Verdict: partly holds. The fetched bytes, the anchor digest, the committed snapshot, the one Gate quote, its line and word count, the path, mode and version scope all hold, but two clauses of the S133 teaches cell go beyond what sysfs.c shows, and the entry's SH1 statement wrongly calls two counter names "shorter" when both views use the same name.

Measured revision: 7dfea9244a84a0e2439f0698e54491e5d7b7c467. A sandbox copy of that revision (git archive piped to tar, no remote) is at /fast/scratch/hyaku/tsuku26/w2/RevS133/tree. The re-open was done today, 2026-10-22.

## Findings

1. [holds] Fetch and digest. A plain curl of https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/sysfs.c exited 0. The saved copy at /fast/scratch/hyaku/tsuku26/w2/RevS133/fetch/S133-sysfs-v7.2.c is 72925 bytes, has 2702 newlines, ends with LF, and has sha256 ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43. The anchor in /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md:139 names that same digest. SOURCES.md is byte-identical between the working tree and the measured revision (sha256 9573a318737019ae, both).

2. [holds] Snapshot. The measured-revision file .ufo/waves/round-26/sources/S133.c is byte-identical to the fetch (cmp exit 0). The lane copy at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/sources/S133.c has the same digest. Mori's committed copy (blob at commit c1e8b81, and its working-tree file /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/evidence/sources/S079-fs_btrfs_sysfs.c) also hashes to ce146120..., so the note at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-26.md:53 holds.

3. [holds] Other copies. The kernel.org plain view of torvalds/linux at ?h=v7.2 and of the stable tree at ?h=v7.2.11 both return the same 72925 bytes and the same digest. The GitHub raw URL for v7.2.11 returned HTTP 404 (curl exit 22), which is expected because stable point releases are not in torvalds/linux. I used the kernel.org stable copy for the 7.2.11 check.

4. [holds] Gate quote. The only S133 Gate row is /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-26.md:16. Its quote "static ssize_t btrfs_devinfo_error_stats_show(struct kobject *kobj," is 5 words and is an exact substring of exactly one snapshot line, S133.c:2074. The stated location "fs/btrfs/sysfs.c line 2074" is therefore correct. Line 16 is identical in the measured revision and in the working tree. The working tree has an extra section appended after line 93 ("Routed defect 4"), which does not touch S133. [obs] The Gate quote proves only that the function starts at that line. It supports no counter claim, and the counter claims rest on other S133 lines that the Gate does not quote.

5. [holds] Scope cell. The path comment at S133.c:2105 reads "Path: /sys/fs/btrfs/<uuid>/devinfo/<devid>/". The attribute is registered at S133.c:2100 (BTRFS_ATTR(devid, error_stats, btrfs_devinfo_error_stats_show);) and listed at S133.c:2108. The macro at S133.c:76-78 sets the mode to 0444. The phrase "for the host kernel 7.2.11" is supported by the identical stable v7.2.11 bytes. [unk] I did not check whether Arch's 7.2.11-arch1-1 build carries patches to this file.

6. [partly] Teaches cell, ioctl equivalence. The teaches cell says: "The sysfs error_stats file prints the same five per-device counters as the device stats ioctl". S133 contains no ioctl reference. A grep for "ioctl" and "btrfs_ioctl" over S133.c returned no matches. The ioctl side is in S132: btrfs_get_dev_stats (S132.c:8458-8459, which takes "struct btrfs_ioctl_get_dev_stats *stats") fills its values with btrfs_dev_stat_read(dev, i) (S132.c:8488-8490). At entry level this is covered, because SH1 also cites S132. At row level, the S133 teaches cell asserts a cross-source comparison that its own anchor cannot carry. Fix: narrow the teaches cell, or add S132 to the row's anchor. Severity: low.

7. [partly] Teaches cell, "or the word invalid when the stats were not loaded". The only S133 code is S133.c:2080-2081: "if (!device->dev_stats_valid)" followed by "return sysfs_emit(buf, "invalid\n");". S133 does not define the flag. The "not loaded" reading comes from S132.c:8474-8475 ("get dev_stats failed, not yet valid"). Caveat: on a failed lookup, S132.c:8202-8207 zeroes the counters and still sets dev_stats_valid to 1 before returning the error. After such a failure the file would show zeros, not "invalid". The flag is set on the load success path at S132.c:8223 and on another path at S132.c:2941 [inf: a device-add path]. Whether the caller aborts the mount is in fs/btrfs/disk-io.c, which is not in the snapshots [unk]. The entry never uses the word "invalid" (0 hits in storage-health-r26.md and storage-health-r26.json), so the entry is not affected. Severity: low.

8. [obs] Teaches cell, "read through btrfs_dev_stat_read in one snapshot". The comment at S133.c:2084-2085 reads "Print all at once so we get a snapshot of all values from the same time." The code makes five separate btrfs_dev_stat_read calls (S133.c:2094-2098) and takes no lock. "Snapshot" is therefore the comment's stated intent, not a guarantee the code enforces. It is acceptable only if attributed to the comment. Severity: low.

9. [partly] Entry SH1 statement. /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/storage-health-r26.md:15 and storage-health-r26.json rows[0].statement both say the sysfs file prints the same counters "under shorter names (write_errs, read_errs, flush_errs, corruption_errs, generation_errs)". The sysfs names are at S133.c:2089-2093. The btrfs device stats names in S128 are write_io_errs, read_io_errs, flush_io_errs, corruption_errs and generation_errs (S128.rst:238-242). For corruption_errs and generation_errs both views use the same name (S128.rst:241-242 and S133.c:2092-2093), so "shorter" holds for three of the five counters only. The entry's own capture pointers already show corruption_errs in both views (storage-health-r26.md:25). Fix: say "shorter" for write, read and flush only. Severity: low.

10. [holds] "no privilege needed" (storage-health-r26.md:21 and storage-health-r26.json rows[0].action). The mode is 0444 (S133.c:76-78, "__INIT_KOBJ_ATTR(_name, 0444, _show, NULL)"), and the show function (S133.c:2074-2099) has no capability check.

11. [holds] "read by the same kernel function" (storage-health-r26.md:15) and "their identity rests on S133 and S132" (storage-health-r26.md:111). S133.c:2094-2098 and S132.c:8490 both call btrfs_dev_stat_read on the same counter set. Together the two sources support both claims.

12. [holds] Quote copies. storage-health-r26.md:23 and storage-health-r26.json rows[0].quotes[3] (json lines 55-58) carry the same 5-word quote with location "fs/btrfs/sysfs.c line 2074". Both are exact.

13. [holds] Source identity. storage-health-r26.md:1, storage-health-r26.json:26 (source_id_note) and storage-health-r26.json:35-37 identify S133 as Linux v7.2 fs/btrfs/sysfs.c, which matches the fetched file.

14. [holds] Row metadata. Status mined, opened 2026-10-22 (today), recheck on-release, used-by corpus/knowledge/storage-health-r26.md. This meets the C1 rule at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md:897. The JSON twin and the lesson also cite S133, but the S132 row also names only the md, so this follows the lane convention [obs].

15. [obs] Tier. Tier A is applied in the row and in /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-26.md:9. No written tier definition exists in SKILL.md, corpus/README.md or PROVINCE.md at 7dfea924 (grep for the word "tier" found no match). S133 is primary kernel source at a pinned tag, the same kind as the other tier A code rows [inf]. [unk] I found no formal definition to check against.

16. [obs] Anchor. The committed anchor records tag v7.2, lines 2074-2100, and the digest. The wave-1 draft at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w1/SrcKernelSysfs.md:43 also carried a peeled commit (8d3ae59288f1e7d58d76558a6ee96d533bc5019f), which the committed row drops. I did not check that commit [unk]. Lines 2074-2100 cover the function (2074-2099) and its attribute line (2100), so the range is accurate.

17. [obs] The S136 to S138 note in /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/memory-pressure-r25.md has no S133 citation at 7dfea924, so this check does not involve that file.

## Residual risk and verification gaps
- I did not run tools/check-storage-health.py. The quote and digest checks are my own exact-substring checks in Python.
- I did not open the frozen capture. I cite only the entry's own pointers to it.
- The caller of btrfs_init_dev_stats (fs/btrfs/disk-io.c) is not in the snapshots, so the consequence of a failed load is [unk].
- The Arch build of 7.2.11 was not compared with upstream [unk].

## Suggested fixes (for the integrator to decide)
- S133 row teaches cell: drop the ioctl equivalence or add S132 to the anchor, and attribute the "not loaded" reading to S132.
- Entry SH1 (storage-health-r26.md:15 and storage-health-r26.json rows[0].statement): limit "under shorter names" to write, read and flush.
- No change is needed to any digest, URL, line number, Gate quote, tier, status or used-by value.

Scope: read=SOURCES.md S133 row in the working tree and at 7dfea924, S133.c snapshot in the lane and at 7dfea924, S132.c lines 2941, 8186-8257 and 8458-8495, S128.rst lines 236-258, lessons/round-26.md, storage-health-r26.md and .json, memory-pressure-r25.md (grep only), SCORECARD.md:897, SKILL.md, corpus/README.md and PROVINCE.md (tier grep), mori S079 snapshot and commit c1e8b81 blob, kernel.org and GitHub raw copies of sysfs.c; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w2/RevS133.md, /fast/scratch/hyaku/tsuku26/w2/RevS133/tree, /fast/scratch/hyaku/tsuku26/w2/RevS133/fetch; executed=git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin archive 7dfea9244a84a0e2439f0698e54491e5d7b7c467 piped to tar -x (sandbox only), curl -fsSL to raw.githubusercontent.com v7.2 (exit 0), curl to raw.githubusercontent.com v7.2.11 (exit 22, 404), curl to git.kernel.org v7.2 and v7.2.11 plain (exit 0), sha256sum, cmp, wc, od, git -C mori cat-file -t c1e8b81 and git -C mori show c1e8b81 of the S079 path (read-only), python exact-substring and JSON checks
Model: anthropic/claude-haiku-5-5 (from the project-context workstation block; not independently confirmed by this seat)
Installs: none
