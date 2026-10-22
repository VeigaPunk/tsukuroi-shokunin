# RevRowSH4: review of SH4 at revision 7dfea9244a84a0e2439f0698e54491e5d7b7c467

Verdict: partly holds. The four host readings (capture lines 121, 127, 131 and 134) are exact, and the UNVERIFIED verdict follows from the verdict vocabulary. The statement is false as written in its checksum sentence, because NOCOW (the chattr +C attribute, which turns off data checksums) applies to journal data on this host. Its "no scrub record exists on this host" and SKILL SE4's "no scrub has run" reach further than the frozen capture or the status channel can show. The action names two host-changing commands without their side effects.

Pinned bytes: the SH4 files (storage-health-r26.md and .json, SKILL.md, SOURCES.md, the S129, S131 and S139 snapshots, and capture.txt) are byte-identical to 7dfea92, checked by comparing sha256 with `git show <rev>:<path>`. The lesson file differs in the working copy, but its SH4 Gate rows (lines 28-32) are identical at 7dfea92. The lane HEAD is 7f9f088, one commit ahead. [obs]

## Findings, by severity

1. [high] Statement sentence 3 is false as written. storage-health-r26.md line 57 says that ordinary reads verify checksums, so data that was read has been checked. Both universals fail for NOCOW data, which has no data checksums.
   - S139 (.ufo/waves/round-26/sources/S139.rst) lines 21-24 say NOCOW implies NODATASUM, and that scrub validates the metadata but "the actual file data is not". Lines 29-31 say NOCOW files are "not protected by checksums". Line 35 says systemd sets +C on journals by default.
   - Host, live and read-only (`lsattr -d /var/log/journal /var/log/journal/*`, exit 0): `/var/log/journal` and `/var/log/journal/432d02b544a5459ebbff9c42ec68334d` both show the C flag. /var/log is the @log subvolume (capture line 23). Journal data this host writes is therefore NOCOW and unchecksummed. [inf] New files inherit the directory flag; the flags on the existing journal files need root and were not read [unk].
   - Upstream Linux v7.2 fs/btrfs/bio.c lines 836-838 skip data checksum generation when NODATASUM is set.
   - The same entry already says this for SH3 (storage-health-r26.md line 43: NOCOW file data "has no checksums"), so SH4 contradicts SH3.
   - Fix: scope the sentence to data that carries checksums, and say that NOCOW file data is neither verified on read nor by scrub, with the journal directories as the host example.

2. [medium] The only support cited for sentence 3 says something else. The S139 quote at line 17 ("Such automatic repair is also carried out when reading metadata or data from a") sits in the replicated-profile paragraph (S139 lines 13-18, which begins "On filesystems that use replicated block group profiles (e.g. RAID1)"). It describes repair on read for replicated profiles. It does not say that reads verify checksums, and this host uses the single profile. The general read-path claim is plausible [inf: bio.c line 303, btrfs_check_read_bio], but the row cites no source for it. The Gate checker (tools/check-storage-health.py, rule R4 at lines 14-18, code at lines 663-722) only tests that a quote appears in the snapshot and in the lesson Gate table, so a quote that does not support its sentence passes.

3. [medium] "No scrub record exists on this host" is wider than the frozen capture. The capture checked only `btrfs scrub status /` (line 121) and `/var/lib/btrfs` (line 127). Its kernel-journal queries (lines 153-159) look for errs and BTRFS error lines, and lines 163-173 list mount lines, but none searches for scrub.
   - Upstream fs/btrfs/scrub.c logs at info level "scrub: started on devid" (line 3181) and "scrub: ... finished on devid" with a status (lines 3212-3213).
   - Live check: `sudo -n journalctl -k --grep 'BTRFS.*scrub'` returned "No entries" (exit 1) over the six retained boots (`journalctl --list-boots`; the earliest starts 2026-10-19 18:55:14 -03). The same journal holds info-level BTRFS mount lines (capture lines 167-173), so info-level lines are captured.
   - So the claim holds for the status channel and for the retained window only. The status channel alone does not prove absence: btrfs-progs cmds/scrub.c lines 1335-1338 turn status recording off if the directory cannot be created, and the status file can be deleted [inf]. "On this host" for the whole host life is not shown.
   - Fix: say "no scrub status record in /var/lib/btrfs and no scrub start or finish kernel line in the six retained boots".

4. [medium] The action would change the host, and it omits effects that its own sources state. The SH4 action (storage-health-r26.md line 63; SKILL.md line 2366) says "run `btrfs scrub start /` once or enable `btrfs-scrub@-.timer`". The lane never runs either (capture.sh header lines 3-6; SKILL.md Authority line 2359), so there is no lane violation. As operator instructions, though, they are incomplete.
   - `btrfs scrub start /` reads the whole filesystem (capture line 122: "Total to scrub: 174.40GiB"). S139 lines 68-69 estimate device bandwidth use at about 80% on an idle filesystem. S139 lines 49-54 say a read-only scrub on a read-write filesystem causes some writes.
   - It changes stored state. btrfs-progs cmds/scrub.c line 1250 turns status recording on by default. Line 1335 creates /var/lib/btrfs (mkdir_p, lines 1151-1163). Lines 1501-1503 write a status file at start and lines 1701-1703 at the end. The SH4 reading therefore goes stale after one run.
   - `enable btrfs-scrub@-.timer` creates an enablement link (S131 lines 10-11, WantedBy=timers.target). S131 lines 6-8 set AccuracySec=1d, RandomizedDelaySec=1w and Persistent=true, so the first run can land up to a week late, and a missed run catches up at boot.
   - The SH4 action also says to read the corrected versus uncorrectable split. For file data on this single-profile host the corrected count cannot rise, because corrected means repaired from another copy (S129 line 191; SH3) [inf].
   - Fix: list these effects next to the action.

5. [low-medium] The verdict follows from the vocabulary, but the row does not rule out DEGRADED. The JSON verdict_vocabulary defines UNVERIFIED as evidence that "does not exist on the host" and defines DEGRADED as "a limit or fault that reduces what the host can detect or repair". The row's own reading of a disabled monthly timer (lines 131 and 134) limits detection of latent errors in cold data. The vocabulary has no precedence rule, and SH3 uses DEGRADED for a repair limit on the same host. Either state the precedence rule or say why the timer state is not a detection limit.

6. [low] SKILL SE4 (line 2375) says "no scrub has run". The status channel cannot show that (finding 3). The phrase "not a health reading" for the Error summary line is correct on the upstream code: cmds/scrub.c lines 320-322 print "no stats available", and print_fs_stat (lines 384-398) then prints the summary unconditionally from zeroed counters [inf for the zeroing]. The row cites no source for this. S129 lines 165-180 show "Error summary: no errors found" as the output for a filesystem without errors, which reads the other way without the code.

7. [low] Citation and pointer precision.
   - The host reading says the Error summary line is printed "beside" "no stats available". That line is capture line 124. Lines 122 and 123 sit between, and line 124 is not cited.
   - S129 line 133 ("Show status of a running scrub ...") describes running-scrub status. The sentence that supports the no-stats reading is S129 lines 136-138 ("The status is read from the file located in /var/lib/btrfs"), which the row does not cite.
   - capture_pointers list lines 121 and 127 only. The timer readings at lines 131 and 134 appear in the host reading but are not pointers, so the checker never checks them.

8. [low] The SKILL row's command column (line 2366) lists only `sudo -n btrfs scrub status /` and `systemctl is-enabled btrfs-scrub@-.timer`. Its readings also come from `sudo -n ls -la /var/lib/btrfs` (capture lines 126-128) and `systemctl is-active` (capture lines 133-135), which are not listed. Apart from that, the SKILL row matches the MD and JSON rows word for word on statement, host reading, verdict and action.

9. [obs] Limits line 112 of the entry says "which files carry NOCOW on this host was not measured". Directory attributes are readable without privilege and do show C (finding 1). File-level attributes need root [unk]. The Limits line should say that directories were measured and files were not.

## What holds (checked)

- The capture file sha256 is 002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd, as pinned. The header facts in the JSON capture block match capture lines 3 and 9-14.
- Capture line 121 is "\tno stats available". Line 127 is "ls: cannot access '/var/lib/btrfs': No such file or directory" (exit 2). Line 131 is "disabled" (exit 1). Line 134 is "inactive" (exit 3). Line 124 is the Error summary line.
- The S139 quotes at lines 17, 68 and 71 are exact substrings of the snapshot. S131 line 5 ("OnCalendar=monthly") and S129 line 133 are exact. The five SH4 quotes in the MD, JSON and lesson Gate rows match one another.
- The S131 snapshot is byte-identical to the installed /usr/lib/systemd/system/btrfs-scrub@.timer (sha256 9a0b6cc23f7bd97b83b6c38dd2b4e4373fead8bd3ccfb82a47c72971e9d6f8ad; cmp reports IDENTICAL). `pacman -Qo` says it is owned by btrfs-progs 7.1-1, so "packaged" holds.
- `systemd-escape -p /` returns "-", so btrfs-scrub@-.timer is the instance for /. Live, `systemctl show` reports UnitFileState=disabled and ActiveState=inactive.
- The status file name: cmds/scrub.c line 67 defines SCRUB_DATA_FILE as "/var/lib/btrfs/scrub.status", and lines 459-460 append "." and the fsid. S139 lines 71-72 agree. `scrub status` opens the file read-only (cmd_scrub_status, line 1930). Only `scrub start` creates it.
- Live `sudo -n btrfs scrub status /` (exit 0) still prints "no stats available" with "Total to scrub: 174.19GiB". The row does not cite that figure.
- The verdict UNVERIFIED is the same in storage-health-r26.md line 61, the JSON row line 182 and SKILL.md line 2366.

## Residual risk and verification gaps

- I did not run tools/check-storage-health.py. I read its rule text and code only, so its R4 and R5 results for SH4 are not replicated here.
- The live host checks came after the frozen capture. If a scrub start or finish line appears in the journal, or a status file appears, the SH4 readings change.
- The flags on the existing journal files were not read, because that needs root [unk].
- The read-path claim in finding 2 rests on S139 and the function name; I did not read the body of btrfs_check_read_bio [inf].
- Upstream copies were fetched from raw.githubusercontent.com: btrfs-progs v7.1 cmds/scrub.c and Documentation/btrfs-scrub.rst, and Linux v7.2 fs/btrfs/scrub.c and bio.c. The fetched btrfs-scrub.rst is byte-identical to the S129 snapshot. Copies are under /fast/scratch/hyaku/tsuku26/w2/RevRowSH4/.
- The lane working copy showed three changed entries at my check. I did not inspect them; the SH4 files match 7dfea92.

Scope: read=the SH4 row in storage-health-r26.md and .json, SKILL.md section Storage integrity round 26 and its SE4 entry, SOURCES.md rows S128-S139, lesson round-26.md Gate rows, source snapshots S129, S131 and S139, frozen capture.txt and capture.sh, tools/check-storage-health.py rule text, and upstream btrfs-progs v7.1 and Linux v7.2 scrub, bio and status code; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w2/RevRowSH4.md and /fast/scratch/hyaku/tsuku26/w2/RevRowSH4/ (four fetched upstream files); executed=read-only git log, git status, git show (sha256 comparison of pinned bytes), sha256sum, cmp, curl of four public raw URLs, journalctl --list-boots, journalctl -k --grep with and without sudo -n, sudo -n btrfs scrub status /, systemd-escape -p /, pacman -Qo and pacman -Q btrfs-progs, systemctl show, stat, lsattr -d, findmnt, ls -ld /var/lib/btrfs
Model: not exposed
Installs: none
