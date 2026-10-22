# RevRowSH3: attack on entry row SH3 at 7dfea9244a84a0e2439f0698e54491e5d7b7c467

Verdict: partly holds. The single-profile limit, the rule that scrub repairs only from another replicated copy, the two-copy reading of DUP metadata and the DEGRADED verdict follow from the cited sources and from capture line 64. Four parts fail: the systemd NOCOW sentence is stale and wrong about archived journal files on the installed systemd 262; the operator action overstates what scrub can detect on this host; the claim that single-profile data is never repaired ignores inline file data; and two citations are wrong (a quote cited at line 190 that sits at line 192, and a `btrfs filesystem df` reading that the frozen capture does not contain).

Conventions. "Entry markdown" is /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/storage-health-r26.md. "Entry JSON" is /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/storage-health-r26.json. "SKILL row" is line 2365 of /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SKILL.md. "Snapshot" means a file under /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/sources/. "Capture" is /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/capture/capture.txt. Upstream checks used the sandbox at /fast/scratch/hyaku/tsuku26/w2/RevRowSH3/.

## What holds (checked)

- The capture hashes to 002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd. Capture line 64 is the token `single`, and it is unique. Capture line 26 shows `rw` and `ssd` in the root mount options, and it sets no max_inline option. Capture line 37 lists one btrfs device, devid 1. Capture lines 79 and 100 read `dup` under allocation/metadata and allocation/system. [obs]
- Snapshot digests match the SOURCES anchors and the upstream v7.1 files fetched by plain curl: S129 btrfs-scrub.rst 7900b474aebfee2be79ff168c750f282ee33803ee6914928c20117a24aefe3f0; S130 mkfs.btrfs.rst ce7c0cbca90eda4bc84040e9f5a43c227bd02d77bd50b006e481f19d918de769; S139 ch-scrub-intro.rst c3b9d344e11d842e2aed43d191b120572753bb75e8bbedd5b3e10978d24c3485. S131 and S133 also match their anchors. [obs]
- Quotes that match exactly at their cited lines: S139 lines 13, 14 and 24 (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/sources/S139.rst); S130 lines 635 and 639 (S130.rst). The S130 line 639 quote stops mid-sentence at "--thus", which is acceptable. [obs]
- Source rows S129, S130 and S139 in /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md (lines 135, 136 and 145) are status mined, tier A, opened 2026-10-22 and used-by the entry markdown. [obs]
- The entry markdown and the entry JSON give identical SH3 statement, host reading, verdict and action text. The SKILL row is the same text in a table. [obs]
- The SH3 verdict follows. The vocabulary (entry JSON lines 19-24) defines DEGRADED as a limit that reduces what the host can detect or repair. Single data with one copy (S130.rst line 518, "single | 1") and no repair from another copy for uncorrectable errors (S129.rst line 192) is that limit. The verdict does not depend on the NOCOW or DUP clauses. [obs]
- Neither the SH3 action nor the SKILL row names a host-changing command. The profile change is explicitly not proposed (entry markdown line 49). [obs]

## Findings

1. Severity high. The systemd NOCOW sentence is stale and wrong about archived journal files on the installed systemd 262.
   - Claim: "systemd sets that attribute on journal files by default" (entry markdown line 43; entry JSON line 130). The SKILL row says "NOCOW file data (systemd journals)" (line 2365). The Limits bullet at entry markdown line 112 repeats it.
   - Its only support is S139.rst line 35, which links commit 11689d2a021d95a8447d938180e0962cd9439763. I fetched that commit (saved at /fast/scratch/hyaku/tsuku26/w2/RevRowSH3/ext/systemd-11689d2a.patch). It is from January 2015, titled "journald: turn off COW for journal files on btrfs". It set FS_NOCOW_FL on each new journal file and cleared it on close for defragmented files.
   - The installed systemd 262-1 does not do that. I fetched the v262 source tarball (https://codeload.github.com/systemd/systemd/tar.gz/refs/tags/v262, extracted under /fast/scratch/hyaku/tsuku26/w2/RevRowSH3/ext/systemd-src/systemd-262/).
     - NEWS lines 18603-18607, in the "CHANGES WITH 220" section that starts at NEWS line 18424: "systemd-journald will no longer unconditionally set the btrfs NOCOW flag on new journal files. This is instead done with tmpfiles snippet using the new 'h' line type." The 2015 behaviour is NEWS line 18788, in the "CHANGES WITH 219" section.
     - src/libsystemd/sd-journal/journal-file.c lines 4010-4045 only read the attribute and warn about copy-on-write, advising "chattr +C" on the journal directory. The warning is called for newly created files at lines 4225-4226. No journal code sets the flag.
     - The flag comes from the tmpfiles snippet /usr/lib/tmpfiles.d/journal-nocow.conf. `pacman -Ql systemd` lists it, and its sha256 (b0cfe7fb70a62747fd4002a8c5945f7b2a1784a7b482e65da6512987d0ba307d) equals the upstream copy. Lines 10-12 say the flag "is inherited by their new files and sub-directories". Lines 25-27 are `h /var/log/journal`, `h /var/log/journal/%m` and `h /var/log/journal/remote` with +C. The `h` line type sets attributes on the path itself (man/tmpfiles.d.xml lines 439-440). meson.build line 10 installs the snippet unconditionally.
     - Archived journal files lose the flag. src/shared/journal-file-util.c lines 201-229 (inside journal_file_set_offline_internal, which starts at line 150) run for archived files (archive is set at sd-journal/journal-file.c line 4429). They clear FS_NOCOW_FL; if that fails they rewrite the file without it, because "on some filesystems (BTRFS), the NOCOW flag cannot be removed after data has been written to a file" (lines 204-206).
   - So on the installed systemd, the directories carry +C, and new active journal files inherit it. Archived journal files end up copy-on-write and are checksummed. The row's mechanism (journald on journal files) and its scope (all journal files) are both wrong. The only accurate part is that the shipped default sets +C on the journal directories. [obs]
   - Host state: systemd-tmpfiles-setup.service ran in this boot (systemctl show: ActiveState=active, Result=success, ExecMainStatus=0, started Thu 2026-10-22 04:55:42 -03, which is inside boot 0). [obs] So the directory flags were applied at this boot's start. [inf] Whether the active journal files are NOCOW now is not measured by me. Another wave-2 report, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w2/RevRowSH4.md line 11, reports `lsattr -d` output showing the C flag on /var/log/journal and a machine-id directory. I did not re-run lsattr because it is outside the read-only allow-list I was given. [unk]
   - Wave 1 already had this. /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w1/CritLearningFrontier.md line 34 cites the same archive re-enable and tmpfiles line. The committed row and the wave-2 corrections (entry markdown lines 116-134) do not carry it.
   - Fix: replace the sentence with the v262 mechanism (directories set by the tmpfiles snippet, inherited by active files, archived files copy-on-write), cite the v262 sources, and add those sources to SOURCES.md, which currently has none for systemd v262 tmpfiles or journald.

2. Severity high-medium. The action overstates what scrub can detect.
   - Action (entry markdown line 49; entry JSON line 133; SKILL row last cell): "a data checksum error on this host can be found but not fixed from a replica, so backups are the repair path for file data."
   - A checksum error exists only where checksums exist. The row's own statement says NOCOW data has none, and S139.rst lines 21-24 and 28-31 say NOCOW files "are not protected by checksums". The action drops that exception. If the active journal files are NOCOW (finding 1), a scrub reports nothing for them. [inf]
   - "Backups are the repair path" has no source in the row's list. Whether this host has backups was not measured. [unk]
   - Fix: "corruption of checksummed, copy-on-write data is found by scrub or by reads, and on single profile it is not repaired from a copy; NOCOW data has no btrfs checksums and is not checked by btrfs, so the host cannot detect corruption there." Recommend backups as a conditional operator choice, not as the repair path.

3. Severity medium. "With the data profile single there is one copy, so a data checksum error is detected and reported as uncorrectable, not repaired" (entry markdown line 43; entry JSON line 130; SKILL row: "`single` data: a checksum error is found but is uncorrectable"). This is universal over single-profile data, and inline file data does not fit it.
   - btrfs-progs v7.1 ch-mount-options.rst lines 272-276 (fetched to /fast/scratch/hyaku/tsuku26/w2/RevRowSH3/ext/btrfs-progs-v7.1-ch-mount-options.rst, sha256 aac3b1b68ba55259f6c2b8e6d1e30e41560eaee3b0f4863af58387271bc9985f) says max_inline defaults to min(2048, page size) and that inline data is stored "in a metadata b-tree leaf". The capture sets no max_inline (capture line 26). Metadata is dup on this host (capture lines 79 and 100).
   - [inf] Small files stored inline would therefore have a second copy in the dup metadata and could be repaired from it. The single-profile rule covers only extents outside metadata. The wave-1 critic reached the same point (CritLearningFrontier.md line 35). The mount-option rule is not a source in SH3's list, so the row cannot support the universal.
   - Fix: scope the sentence to non-inline data in single block groups, and cite the mount-option rule if it is kept.

4. Severity medium. A quote is cited at the wrong line.
   - S129.rst lines 186-194 (read raw): line 190 is blank. The quoted "*  *Uncorrectable* -- errors detected at read time but not possible to repair from other copy" is at line 192.
   - The same wrong line 190 appears at entry markdown line 51, entry JSON line 163 ("btrfs-scrub.rst line 190"), and corpus/lessons/round-26.md line 26 (the same at 7dfea924; checked in the sandbox).
   - The wave-2 erratum (entry markdown line 131) gives line 192, but the entry JSON and the lesson still say 190.
   - The gate does not catch this. tools/check-storage-health.py rule R4 (docstring lines 14-18; code lines 711-714) checks that the quote text occurs somewhere in the whole snapshot and in the lesson Gate table, not at the cited line.
   - Fix: change 190 to 192 in the entry markdown, the entry JSON and the lesson.

5. Severity medium. The host reading cites a command the frozen capture does not contain.
   - "metadata and system profiles dup (`btrfs filesystem df` and sysfs allocation directories)" (entry markdown line 45; entry JSON line 131; SKILL row). A search of /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/capture/ for "btrfs filesystem", "filesystem df", "Data, ", "Metadata, " and "System, " returns no match. The erratum at entry markdown line 134 agrees and says another wave-1 seat ran the command outside the capture.
   - The dup reading is supported by sysfs: capture lines 79 and 100. The row cites only line 64.
   - Fix: delete the df clause and add the capture pointers for lines 79 and 100, or capture the df output in capture.sh and re-pin the capture hash. I did not run the command.

6. Severity low-medium. "One NVMe SSD under LUKS" is true of the root device only.
   - The host reading (entry markdown line 45; entry JSON line 131; SKILL row) reads as a host inventory. Current lsblk (read, not in the frozen capture) shows nvme0n1p2 as crypto_LUKS under the root btrfs (mounted at /, /home, /var/log and /var/cache/pacman/pkg). It also shows a second NVMe, nvme1n1, with XFS /tmp and /fast. [obs]
   - "SSD" holds: /sys/block/nvme0n1/queue/rotational reads 0, and capture lines 26 and 170 show ssd optimizations.
   - Fix: "the root filesystem sits on one NVMe SSD (nvme0n1p2) under LUKS".

7. Severity low. Dropped qualifiers and unscoped universal words.
   - "File data with the NOCOW attribute has no checksums" (line 43): S139.rst line 21 begins "As currently implemented,". The qualifier is dropped. Also say "no btrfs data checksums": the systemd snippet (journal-nocow.conf lines 21-23) says journal files "have their own checksums", so the bare word is ambiguous.
   - "Scrub reads all data and metadata and checks checksums" (line 43): S139.rst lines 1-2 say "all filesystem data and metadata that detects data checksum errors". The same row then excludes NOCOW data, so the sentence needs "all data that has checksums".
   - "it repairs a bad block only by copying a verified good copy from another replica" (line 43): S139.rst lines 41-43 say scrub "can only repair filesystem damage by copying from other known good replicas", but the row does not quote it. S129.rst lines 198-199 describe superblock errors that "the next commit will overwrite superblock", which is a repair route that is not a copy from another replica. [inf] Scope "only" to data and metadata blocks. Repair also needs a read-write scrub without -r (S129.rst lines 78-80 and 89-90; S139.rst lines 13-15). This host is read-write (capture line 26).
   - Limits, entry markdown line 112: "NOCOW file data (systemd journals) is outside scrub". S139.rst lines 23-24 say the metadata of NOCOW files is still validated and corrected by scrub. "Outside scrub" overstates it.

8. Severity low. The DUP clause holds. S130.rst line 520 gives DUP "2 / 1 device", and lines 635-637 and 639-641 say the two copies may be one physical copy on an SSD. S139.rst line 13 and S129.rst lines 79-80 support repair from a redundant profile. S139 does not name DUP, so the repair rule rests on S129 and S130 (entry markdown line 122 and wave-2 erratum line 131 say the same). [obs]

9. Severity observation. No SH3 action changes the host. The only operator text is the backups sentence (finding 2) and the profile-change refusal (line 49).

10. Severity observation. Gate blind spots. tools/check-storage-health.py at 7dfea924 (sha256 6aadca511ca664b641c2a0b920a51c65057b53520fdf9a09108d6839d7bcf367, identical to the working copy) checks that quotes occur in snapshots and the Gate table, that capture pointers are unique and contain their token, that the verdict is in the vocabulary, and that the SKILL row id exists. It does not check quote line numbers, the content of the SKILL row, or whether a statement is true. Findings 1 to 7 all pass the six-of-six count. I did not run the checker.

11. Severity observation. Working copy and revision differ only in corpus/lessons/round-26.md. The working copy appends "Routed defect 4" and "Wave-1 findings recorded after integration" sections. Its SH3 Gate rows (lines 22-27) are identical to the committed rows at 7dfea924.

12. Severity observation. Wave-2 corrections (entry markdown lines 116-134) are append-only and do not change the SH3 row. Line 122 (SH3) and line 131 (S129 line 192; dup clause) are correct. Line 134 (df not in capture) is correct. None of them corrects finding 1, finding 2 or finding 3.

## Unknowns

- [unk] Whether this host's active journal files, and archived ones, carry NOCOW now. Not measured by me; attribute reads need root or lsattr, which is outside my allow-list.
- [unk] Whether this host has backups.
- [unk] Whether the SSD stores the DUP copies as one physical copy. The row says "may", which is the right strength. The dm-crypt note at entry markdown line 122 is another seat's inference. I did not verify it.
- [inf] No sudo journal line shows "copy-on-write is enabled" or "Creating journal file". The only matches were my own sudo command-log lines. This is weak evidence, because journal creation events may predate the six retained boots.
- [obs] The six retained boots in capture line 161 are correct. `journalctl --list-boots` prints a header line, and the capture drops it with tail. There are six boots, IDX -5 to 0.

## Fixes, in order

1. Rewrite the systemd sentence for v262 and add the v262 sources (finding 1).
2. Narrow the action's detection claim to checksummed data and make backups conditional (finding 2).
3. Scope the single-profile rule to non-inline data, or cite max_inline (finding 3).
4. Change line 190 to 192 in the entry markdown, entry JSON and lesson (finding 4).
5. Delete the df clause and add capture lines 79 and 100 (finding 5).
6. Change the NVMe wording to the root device (finding 6).
7. Restore the "As currently implemented" qualifier, scope "all data", "only", "outside scrub" and "no checksums" (finding 7).

Scope: read=entry markdown and entry JSON (SH3 rows, Limits, wave-2 corrections at lines 116-134), SKILL.md section and SH3 row, SOURCES.md rows S129, S130, S139 and the S128/S131/S133 anchors, corpus/lessons/round-26.md (committed and working copy), tools/check-storage-health.py at 7dfea924, snapshots S128, S129, S130, S131, S133 and S139, the frozen capture, wave-1 CritLearningFrontier.md, wave-2 RevRowSH4.md, RevS130.md and RevS139.md (read only), SCORECARD.md lines 897 and 911-919, upstream btrfs-progs v7.1 docs, the systemd v262 source tree and the 2015 systemd commit; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w2/RevRowSH3.md and scratch under /fast/scratch/hyaku/tsuku26/w2/RevRowSH3/ (sandbox tree at 7dfea924, downloaded upstream files, extracted systemd tree); executed=git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin archive 7dfea9244a84a0e2439f0698e54491e5d7b7c467 | tar -x into scratch; sha256sum on the capture, snapshots, entry files, SKILL.md, SOURCES.md, lessons, checker, upstream and host files; curl -fsSL of btrfs-progs v7.1 scrub, mkfs, scrub-intro and mount-option docs, the Arch btrfs-scrub@.timer (digest only), the 2015 systemd commit patch, the systemd v262 tarball and a v262 journal-file.c path; tar -xzf of the systemd tarball into scratch; pacman -Ql systemd; pacman -Q systemd; journalctl --list-boots (no sudo); sudo -n journalctl --no-pager --list-boots and with --grep for "copy-on-write is enabled" and "Creating journal file" (both output formats); journalctl --no-pager --grep counts (no sudo); lsblk -o NAME,TYPE,FSTYPE,SIZE,MOUNTPOINTS; cat /sys/block/nvme0n1/queue/rotational; systemctl show systemd-tmpfiles-setup.service -p ActiveState -p Result -p ExecMainStartTimestamp -p ExecMainStatus; diff of two lesson-file copies. I did not run lsattr, btrfs filesystem df, the lane checker, or any scrub, timer, counter or profile command.
Model: anthropic/claude-haiku-5-5 (as shown in this session's workstation context; not independently verified)
Installs: none
