# RevRowSH2 review: storage-health entry row SH2 at revision 7dfea9244a84a0e2439f0698e54491e5d7b7c467

Verdict: partly holds. The kernel mechanics, the cited line numbers, the six-boot count and the HEALTHY reading all check out. Two universal words overreach the kernel code ("clears them only on an explicit reset" and "Only the error-level line dates an incident"). The frozen capture's regex cannot see the main kernel error text, so the capture does not prove the second count. The action gives no way to pick out error-level lines. No step of the action changes the host.

## What I checked

- Entry rows: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/storage-health-r26.md lines 27-40 (SH2) and /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/storage-health-r26.json lines 85-127 (SH2 row). SKILL row: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SKILL.md line 2364 (read raw).
- Source rows: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md line 134 (S128) and line 138 (S132).
- Snapshots: sha256 of .ufo/waves/round-26/sources/S132.c is f3400af8e924bc7743d28f43b45f02be1bc84e25de00ac99d2bfc8bab19a4fbf, and of S128.rst is 0d4f425a49c1483f1cc598695d9a456e6d5542e5c59df4946fd471e5d4f7a0e6. Both match SOURCES.md. Both are byte-identical to the upstream files at tag v7.2 (fs/btrfs/volumes.c) and tag v7.1 (Documentation/btrfs-device.rst), which I fetched with curl into /fast/scratch/hyaku/tsuku26/w2/RevRowSH2/. "Upstream" below means those fetched files. [obs]
- Frozen capture: sha256 002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd matches the pinned value. I read all 241 lines.
- Live recheck, read-only, at 2026-10-22T15:24-15:25Z: same boot ID (6a7f4fdf-ac62-4e2e-a6c1-b3c55d6f94f4), six retained boots, all five counters zero, no error-level or warning-level BTRFS lines in any retained boot.

## Findings

1. The cited line numbers are correct. [obs]
   - S132.c line 8352 holds "called from commit_transaction. Writes all changed device stats to disk." The quote is exact.
   - S132.c line 8429 holds the error-level format string, and line 8446 holds "return; /* all values == 0, suppress message */". Both quotes are exact.
   - S128.rst line 231 holds "The device stats keep persistent record of several error classes related to" (exact).
   - capture.txt line 41 is "read_errs 0". Line 116 is "[/dev/mapper/root].generation_errs  0". Lines 155 and 158 are the two zero counts, and line 161 is 6 (boots). Lines 156 and 159 are grep exit status 1, meaning no match.
   - The six boots are confirmed live. Both `journalctl --list-boots` (with and without sudo) list six boots, indexes -5 to 0.

2. "Clears them only on an explicit reset" is false as a universal. [medium] The sentence appears at Markdown line 29, JSON line 87, and in the SOURCES.md line 138 teaching, which says "cleared only by an explicit reset".
   - S132.c lines 2294-2324 define btrfs_remove_dev_stat_item, which deletes the stored DEV_STATS item for a devid. Upstream volumes.c line 2405 calls it from btrfs_rm_device (volumes.c line 2326). So removing a device deletes its stored counters.
   - Upstream dev-replace.c line 1024 deletes the devid 0 stats item inside btrfs_dev_replace_finishing (dev-replace.c line 858). I did not trace whether the replaced device's counters move to the new device. [unk]
   - S132.c lines 8203-8205 and 8220 set counters to zero in memory when the stored item is missing or too short. That is a zero reading, not a deletion. [obs]
   - On this host, device removal of the only writable device is refused by volumes.c lines 2372-2374 (BTRFS_ERROR_DEV_ONLY_WRITABLE). The capture shows one device (capture.txt lines 36-37). So this host is not affected today. [inf]
   - Suggested fix: say "cleared by an explicit reset, or deleted with the device's stats item on device removal", or drop "only".

3. The capture's regex misses the main kernel error text, so the frozen capture cannot prove the second count. [medium, evidence only; the verdict still holds live]
   - The main filesystem-error path prints "BTRFS: error (device %s%s) in %s:%d: errno=%d %s (%pV)" at critical level (upstream fs/btrfs/messages.c lines 150 and 154). The colon after BTRFS means the capture's pattern "BTRFS (error|critical|warning)|forced readonly" (capture.txt line 157) cannot match it. The forced-readonly message is "forced readonly" (messages.c line 176), which the pattern does match.
   - Live and read-only, at 2026-10-22T15:25:43Z: `sudo -n journalctl --no-pager -o short-iso _TRANSPORT=kernel -p warning --grep BTRFS` over all retained boots printed only boot header lines and "-- No entries --", so zero entries. The same happened with `--grep "BTRFS: error"` at any priority. So the host has no such line now, but the frozen capture does not show it.
   - The SKILL row command (SKILL.md line 2364) repeats only the errs-wr count. It does not repeat the second count the row reports.
   - Suggested fix: change the capture pattern to "BTRFS:? (error|critical|warning)|forced readonly", or add `-p warning`.

4. The action cannot pick out error-level lines as written. [low-medium] The action (Markdown line 35; SKILL line 2364) asks for error-level lines, but the command returns info-level and error-level lines together. The short output format has no priority column. The level word is in the text instead: messages.c lines 223 and 236 build "BTRFS %s (device", so an error line reads "BTRFS error (device" and a mount line reads "BTRFS info (device" (capture.txt line 168 shows the info form). The row does not say which filter to use. A `-p err` priority filter, or a grep for "BTRFS error \(device", would do it. [obs]

5. "Only the error-level line dates an incident" and the action's "to date the errors" overreach, because the error-level line is rate limited. [medium] Markdown line 29 and line 35 carry the claim.
   - S132.c lines 8422-8436 count the error, then call btrfs_err_rl at line 8428.
   - Upstream messages.h lines 56-57 define btrfs_err_rl at LOGLEVEL_ERR through btrfs_printk_rl_in_rcu. Lines 90-100 give each call site its own static ratelimit state. Upstream include/linux/ratelimit_types.h lines 9-10 set DEFAULT_RATELIMIT_INTERVAL to 5*HZ (5 seconds) and DEFAULT_RATELIMIT_BURST to 10. So each call site prints at most 10 such lines in 5 seconds, and counted errors beyond that print nothing. [obs]
   - Every counting site I fetched goes through the printing function: upstream bio.c lines 367-371 and 993, scrub.c lines 1114-1120 and 1284, inode.c line 3569, and disk-io.c lines 3834 and 4036. volumes.c lines 8426-8427 skip the print when the device stats are not valid. [obs]
   - So the error line dates only the errors that printed. The row says "(rate limited)" once, but its verdict and action text do not carry the consequence. Suggested fix: say that dating covers printed errors only, and that a burst can hide counted errors.

6. Two true clauses have no citation in the row. [low] The statement's mount-time load and its logged reset are both true, but the row cites no line for either.
   - "Loads them from the device tree at mount": the load body is S132.c lines 8186-8228, with the device tree key at lines 8198-8201. The caller is upstream disk-io.c line 3634, inside open_ctree (which starts at disk-io.c line 3354). The S132 snapshot does not contain the caller. [obs]
   - "Which it logs": the reset branch is S132.c line 8477, and it logs "device stats zeroed by %s (%d)" at info level (lines 8485-8486). The row cites no line for it, and the action never tells the reader to search for that line. The reset flag needs CAP_SYS_ADMIN (upstream ioctl.c line 3150). [obs]

7. "Persistence across mounts cannot be observed" holds only for the allow-listed commands. [low] A root read of the device tree could show whether a DEV_STATS item is stored (S132.c line 8198 uses that key). That read is not on the allow-list and I did not run it. The sentence should read "cannot be observed with the allow-listed commands". [inf]

8. The HEALTHY verdict follows for the host signal, but the label covers only the counters. [low] The counters are zero and no error lines exist, both live and in the frozen capture. The row says the persistence mechanism rests on the source, which is honest. A reader could still take HEALTHY to cover that mechanism. [inf]

9. The action changes nothing on the host. [obs] Its only commands are read-only journal queries. "Resetting counters stays an operator decision" matches the reset needing CAP_SYS_ADMIN (ioctl.c line 3150).

10. The SKILL row matches the Markdown and JSON rows. [low] SKILL.md line 2364 host reading, verdict and action match the Markdown and JSON rows word for word. Only the statement column is abbreviated. Its "A non-zero counter is a stored total, not an event" is loose, because a counter is a stored total of events. Its "Date errors only from error-level ... lines" repeats finding 5.

## Residual risk and verification gaps

- [unk] journald's own rate limits and retention settings were not checked. A dropped kernel line would not appear in the journal.
- [unk] Whether a device replace moves counters to the new device was not traced. I read only part of upstream dev-replace.c.
- [unk] capture.sh was not read or re-run.
- [obs] Outside SH2 scope: the live unfiltered query `journalctl -k -p err` across retained boots returned 146 output lines, including boot headers. The same query filtered to BTRFS returned no entries, so none of them is a BTRFS line. I did not examine the rest.

Scope: read=storage-health-r26.md lines 1-40 and 114, storage-health-r26.json lines 1-27 and 85-127, SKILL.md lines 2363-2375 (line 2364 raw), corpus/SOURCES.md lines 134 and 138 (raw), sources S128.rst and S132.c (cited ranges and call sites), capture.txt all 241 lines, upstream v7.2 and v7.1 files fetched read-only (volumes.c, messages.h, messages.c, disk-io.c, ioctl.c, dev-replace.c, ratelimit_types.h, btrfs_tree.h, bio.c, scrub.c, inode.c, btrfs-device.rst); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w2/RevRowSH2.md and /fast/scratch/hyaku/tsuku26/w2/RevRowSH2/ (downloaded upstream copies only); executed=sha256sum; diff; cat /proc/sys/kernel/random/boot_id; journalctl --list-boots with and without sudo; curl GET of raw.githubusercontent.com files; grep, sed, awk; sudo -n btrfs device stats /; sudo -n journalctl read queries (_TRANSPORT=kernel with --grep and -p filters, and counts); date -u. No lane, git or jj write.
Model: anthropic/claude-haiku-5-5 (stated in the workstation context block; not independently confirmed from inside this run)
Installs: none
