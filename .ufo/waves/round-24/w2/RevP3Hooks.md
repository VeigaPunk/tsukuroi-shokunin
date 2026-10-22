Verdict: P3 of the round-24 pause-lift gate (premise "mkinitcpio 42 breaks the configured late hooks that still name /new_root", verdict "changed") is falsified as to its verdict word, and the cited capture lines and the plymouth inference survive with defects. "unverified" is the honest word. Using it drops claim C2 from 5 of 5 to 4 of 5, which is a recorded miss under the scorecard rules.

Method: I compared every P3 pointer with the committed capture bytes at commit 22fd1642 (sha256 87f70f82…, identical to the pin in the gate JSON). I re-read the installed hooks, init, functions and the mkinitcpio caller. I read the journal, kernel log, EFI variables, file stamps and findmnt. I extracted the booted image read-only into scratch and removed it afterwards. I compared installed files with upstream blobs, and read the plymouth source at tag 26.134.222 and merge request 482 through public URLs.

## Findings, by severity

1. [obs][inf] High. "changed" overstates P3. The honest verdict is "unverified".
   - The premise is present tense and covers both configured late hooks. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/pause-lift-gate-r24.json:84. Capture line 100 shows both hooks in the configured HOOKS list.
   - Plymouth half. Its /new_root call reached the real root on boot 0 (see the survived list). That supports "cleared" for ordinary boots only.
   - btrfs-overlayfs half. On every non-snapshot boot it returns at line 14 of /usr/lib/initcpio/hooks/btrfs-overlayfs, because the root source is /dev/mapper/root[/@] and rootflags is subvol=@ (capture line 349). Its only active branch is a read-only snapshot boot (lines 12–19). That boot has not run on a 42.2 image (see the survived list).
   - The gate says the unknown "resolves only through a read-only snapshot boot" (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/pause-lift-gate-r24.md:74). The round bans boot actions (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md:753). The corpus says the same: "that is an operator-only discriminator" (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/initramfs-v42-sysroot-recovery.md:32).
   - So "cleared" overclaims for btrfs-overlayfs. "still-holds" has no observation behind it. "changed" asserts a changed form of the breakage. The only changed-form risks in the lane are predictions (wave-1 CritHookCompat.md finding 8, labelled [inf]). "unverified" is the word that says what is known.
   - Counting effect. The checker counts only cleared, still-holds and changed (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-pause-gate.py:35). Lines 109–112 never read what a "changed" verdict says, so the checker cannot catch this. The scorecard says an unverified verdict does not count (SCORECARD.md:761) and that a miss is an honest stop with no narrowing (SCORECARD.md:751). The honest count is 4 of 5.
   - Cross-premise. The P5 rollback advice counts "the two Snapper snapshots" as remaining rollback paths (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/pause-lift-gate-r24.md:57). Those depend on the same snapshot-boot path that P3 leaves undecided. The P3 label reassures on exactly that point.
   - Strongest case for "changed" or "cleared", answered. The 42-specific mechanism, the /new_root symlink, is present in every image and resolves in every probe, and the overlay steps are not 42-specific. That is a fair argument that 42 is not the breakage. But the premise is present tense and covers the overlay hook, and the one path where that hook can still fail has no read-only decision. A restatement as "pending upgrade only" would make "cleared" defensible, but the scorecard fixes the five premises (SCORECARD.md:751), so that is a narrowing and is not available this round. The gate's own gloss, "not a pending-upgrade risk any more" (pause-lift-gate-r24.md:41), describes a cleared pending premise, not a changed one.
   - Smallest correction. Set the verdict to "unverified" at pause-lift-gate-r24.json:85 and pause-lift-gate-r24.md:41 and :66. Replace the limits at json:140 with a per-hook split, for example: "plymouth latehook (line 11) reached the real root on boot 0, one completed ordinary 42.2 boot, with boot.log and boot-duration stamped in the quit window after switch-root. btrfs-overlayfs returns at line 14 on every non-snapshot boot (root source /dev/mapper/root[/@]). Its read-only snapshot branch (lines 12–19) has not run on a 42.2 image and cannot run this round. Upstream calls the /new_root symlink an attempt to avoid issues (MR 482). Plymouth log writes after the overlay on a snapshot boot are predicted to fail (inference, not observed)." Record C2 as 4 of 5, a miss.

2. [obs] Medium. Two P3 pointers are weak, and one of them is a command echo.
   - pause-lift-gate-r24.json:124 cites capture line 321 with the text "/var/log/boot.log". Line 321 is the command echo `$ stat -c "%y %n" /var/log/boot.log …`, and the same text appears again on line 322 (count 2). The stamp value is on line 322.
   - pause-lift-gate-r24.json:119 cites line 142 with "PID 535 (plymouthd)". That text appears on lines 142, 145, 334 and 335 (count 4). These are journal lines that show a signal sender. They do not show when the daemon started.
   - pause-lift-gate-r24.json:89 cites line 63 with "mkinitcpio 42.2-1", which also appears on line 79 (count 2).
   - Six P3 pointers are unique and are not echoes (capture lines 93, 94, 117, 340, 328, 349), so the counting rule is met. The defects are confined to the cited lines.
   - Smallest correction. Change json:124 to capture line 322 with a unique substring such as "04:55:44.143429272". Keep line 142 only as signal-sender evidence and say that the line repeats. Add capture line 100 with a pointer, because the word "configured" in the premise currently has none.

3. [obs] Medium. The committed capture cannot show when boot 0 began or when plymouth quit.
   - Capture line 16 gives boot 0 as starting at 04:55:41. That is journald's start, not the kernel's. Kernel boot is btime 1792655724, which is 04:55:24 -03 (read from /proc/stat). The first journal line of boot 0 is at 04:55:41.626375.
   - Read against line 16 alone, the boot.log stamp at line 322 (04:55:44.143) looks 3 s after boot, which cannot be a write into the real root. It is actually about 20 s after kernel boot.
   - The journal shows the quit in the real root: "Starting Terminate Plymouth Boot Screen" at 04:55:44.140240, "Received SIGRTMIN+21 from PID 535 (plymouthd)" at 04:55:44.162770, and "Finished Terminate Plymouth Boot Screen" at 04:55:44.324990.
   - Smallest correction. Add the btime line and the short-precise quit lines to a new capture pinned by sha256, and cite them. Until then, boot-0 timing cannot be checked from the committed bytes.

4. [obs] Medium. Kernel-message stamps in the capture are journal receipt times, not kernel times.
   - Capture line 328 reads "[   17.542752] … scanned by mount (942)". The privileged kernel log (sudo dmesg) gives "[   16.652339] … scanned by mount (942)" for the same event, and its first line is "[    0.000000] Linux version". My own journal query gives [17.513130] for that first line. So the journal stamps are the moment journald read the backlog, about 17.5 s in, and they are not kernel event times.
   - The PID argument does not depend on the stamp. A reader would still take 17.5 s as the mount time, while the root was mounted at 16.65 s.
   - Smallest correction. Cite line 328 for PID 942 only, and say that its stamp is a receipt time. Or add the dmesg line to the new capture.

5. [obs] Medium. The S095 quote drops the hedge.
   - The gate quotes only "To avoid issues (or to at least try to avoid them), /new_root will be kept as a symlink to /sysroot" (pause-lift-gate-r24.md:37). The same merge request description (GitLab API: state merged, merge commit 00392d94…, merged 2026-08-11T17:09:08Z) opens with "The change is mostly cosmetical, but it will affect third-party hooks that interact with /new_root."
   - The author calls the symlink an attempt to avoid issues and warns that the change affects third-party hooks. That hedge is exactly why the overlay path cannot be cleared.
   - Smallest correction. Quote both sentences at pause-lift-gate-r24.md:37 and in the limits at json:140.

6. [obs][inf] Low to medium. Several labels and wording are off.
   a. pause-lift-gate-r24.md:38 marks "older than the root mount process 942" as [obs]. It is an inference from PID order. Label it [inf].
   b. md:38 says the files were "written into the real root". The stamps show when, not where. findmnt shows /var/log is the @log subvolume (/dev/mapper/root[/@log]). Label the location [inf] and name the subvolume.
   c. md:38 and json:140 say "the firmware selected Omarchy.linux". The loader writes LoaderEntrySelected, and here the loader is Limine (EFI variable LoaderInfo reads "Limine 12.9.3", which I read). Correct it to "Limine recorded Omarchy.linux in LoaderEntrySelected", and add LoaderInfo to the capture.
   d. md:39 is marked [obs], but its probe output is not in the committed capture. It used a tmpfs stand-in (wave-1 ExecSymlinkMountProbe.md finding 10b) and did not run the read-only branch. Mark it [inf] for the overlay steps.
   e. md:40 marks "the hook acts only on a read-only snapshot boot" as [unk]. The host file decides it (lines 7–19). Mark it [obs].
   f. /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/README.md:223 says "boot 0 shows plymouth reaching the real root". That is an inference. Say "boot 0 is consistent with plymouth reaching the real root through /new_root [inf]".

7. [inf] Low. The predicted snapshot-boot failure is not named in the limits.
   - Wave-1 CritHookCompat.md finding 8 predicts that on a snapshot boot, plymouth chroots into the read-only snapshot before btrfs-overlayfs moves that mount, so its later boot.log writes would fail. That is not observed, and it is not in the gate's limits.
   - Smallest correction. Add it to json:140 as a prediction, so that "plymouth cleared" is not read as covering snapshot boots.

8. [obs] Low. Several facts behind P3 are not pinned in the committed capture.
   - Not in capture.txt at 22fd1642: the hook bodies beyond lines 4 and 11 (btrfs-overlayfs lines 7–19), the booted image's identity, the snapshot-2 entries (/boot/limine.conf has 2 lines naming subvol=/@/.snapshots/2/snapshot), and LoaderInfo.
   - I checked all of these, and they hold. The booted UKI is dated 2026-10-20 09:26:22 and is 284439552 bytes. Its initramfs says "Created with mkinitcpio 42.2" and VERSION 42.2. It lists new_root as a symlink to sysroot, and LATEHOOKS is "plymouth btrfs-overlayfs". Its hook files match the host bytes (sha256 de852646… and eeac1ed…). The committed gate cannot re-check any of this.
   - Smallest correction. In the recapture, add sha256 lines for the two hook files and the UKI, an lsinitcpio line, the snapshot entry count and LoaderInfo. Or label those facts as wave-1 evidence outside the committed capture.

9. [obs] Low. The wording overgeneralizes the boot evidence.
   - "ordinary boots on 42.2 work" rests on one completed 42.2 boot (boot 0) whose plymouth quit is evidenced. Boot -1's boot.log was overwritten, so its latehook path is not evidenced. Wave-1 CritHookCompat.md finding 3 infers that boot -1 used the same image.
   - Smallest correction. Write "one completed ordinary 42.2 boot (boot 0) shows the plymouth path; boot -1 is consistent but not evidenced".

10. [obs] Low. The S097 history claim depends on a sweep with no committed row, and P3 cites superseded rows.
   - S097 (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md:103) says the plymouth hook is unchanged since the 2023 import. The wave-1 packaging sweep supports that (SrcPlymouthPackaging.md:11: the hook file has one commit in its history). The S111 note says the history claim needs that sweep (SOURCES.md:117). S111 and S112 (SOURCES.md:117–118) supersede S097 and S098, which P3 still cites.
   - Smallest correction. Cite the commits URL in S097, or add a row for the sweep. Cite S111 and S112 alongside S097 and S098.

11. [obs] Info. Wording. pause-lift-gate-r24.md:36 says "busybox init". /usr/lib/initcpio/init is a shell script with "#!/usr/bin/ash" (host line 1), and busybox ash runs it. Correct it to "the initramfs init script".

## What survived

- Every cited capture value is the text at 22fd1642. That covers lines 63, 93, 94, 117, 340, 349, the PID 942 text at 328, and the boot.log and boot-duration stamps at 322–323. The capture sha256 matches the JSON pin.
- Installed files match upstream bytes. functions has sha256 8ccfad02… (the S094 blob). The plymouth hook has de852646… (the tag 26.134.222-3 raw file). The btrfs-overlayfs hook has eeac1ed… (the S098 blob). Owners: mkinitcpio 42.2-1, plymouth 26.134.222-3, limine-mkinitcpio-hook 1.40.0-2.
- Every image gets the symlink. /usr/bin/mkinitcpio:1121 calls initialize_buildroot with no condition, and /usr/lib/initcpio/functions:1212–1213 creates sysroot and new_root -> sysroot. The booted image lists new_root -> sysroot.
- The plymouth inference [inf] holds, and its label is right. The only chroot in plymouth's daemon source is in on_newroot (src/main.c:705, with chdir at :704 and :706). The client's read-write option sends only system_is_initialized (src/client/plymouth.c:741–752). Boot 0 has no other root-change unit. PID 535 is lower than the mount's PID 942, and run_hook starts plymouthd before the mount (hook lines 3–8). The kernel mount happened at 16.65 s, and systemd's first plymouth unit started at 17.73 s (capture line 138). The boot.log and boot-duration stamps fall in the quit window after switch-root. So the write reached the real root only through a successful update-root-fs --new-root-dir=/new_root. The weak point is that boot.log has no "new root mounted" trace (zero matches). That trace is debug-only, so its absence is weak evidence either way.
- btrfs-overlayfs on boot 0 returns at line 14, because the root source is /dev/mapper/root[/@]. My probe shows findmnt resolves the symlink chain (exit 0). A non-mountpoint control fails (exit 1). btrfs property get through the symlink returns ro=false (exit 0) on the real btrfs.
- "Initramfs failures are silent under quiet loglevel=0" holds. msg() is silenced under quiet (/usr/lib/initcpio/init_functions:12–15), and run_hookfunctions ignores hook return codes (init_functions:88–103).
- No snapshot boot has run on a 42.2 image. Boots -1 and 0 both have rootflags=subvol=@. Boot -2 ran 08:58 to 09:56 on 2026-10-20, so it loaded the image from before the 09:18 UKI rebuild (/var/log/pacman.log:3046). That earlier image is not a 42.2 image [inf]; its mkinitcpio version was not read directly.
- S095 matches the GitLab API (merged, commit 00392d94). S096 holds: on_newroot is at src/main.c:688.

## Residual risk

- The snapshot-boot path is undecided: btrfs-overlayfs on a read-only snapshot, plymouth's later writes, and the overlay as the switch-root target. Deciding it needs a snapshot boot, which the round forbids. An operator-run snapshot boot is the only discriminator.
- The P5 rollback story depends on that path (pause-lift-gate-r24.md:57).
- The plymouth chroot inference is strong but has no log line.

## Verification gaps

- I did not run tools/check-pause-gate.py. I applied its pointer rule by hand with grep -c -F against the 22fd1642 bytes.
- No boot was run, and the hook was not run against a real read-only snapshot. The ro=true branch was not tested.
- My probe used the host's util-linux 2.42.4. Wave 1 reports the image carries the same version, but I did not run the hook script itself.
- Boot -2's rootflags were not read. It loaded the 41.1 image, so this does not affect the 42.2 claim.
- Upstream pages are mutable. The hashes are those observed on 2026-10-22.

Scope: read=lane files (SCORECARD.md round-24 sections; corpus/knowledge/pause-lift-gate-r24.md and .json; corpus/SOURCES.md rows S094–S112; corpus/README.md:223; corpus/knowledge/initramfs-v42-sysroot-recovery.md:32; tools/check-pause-gate.py verdict lines; capture l1-4 at the working tree and at 22fd1642; wave-1 reports CritHookCompat, ExecSymlinkMountProbe, ExecBootChainAudit, SrcPlymouthPackaging); host read-only files under /usr/lib/initcpio and /usr/bin/mkinitcpio; journal, kernel log, /proc/stat, EFI variables, file stamps, findmnt and pacman query output; /boot/limine.conf (count only); /var/log/boot.log (matching lines only); the booted UKI (a copy in scratch, since removed); upstream plymouth sources at tag 26.134.222, the MR 482 page and API JSON, and raw hook files; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/RevP3Hooks.md (scratch under /fast/scratch/hyaku/tsuku24w2-RevP3Hooks was created and removed); executed=read-only only: git show of the capture at 22fd1642 with sha256sum, grep -c and -n pointer checks, journalctl -b 0/-1/-2, stat, findmnt, pacman -Q and -Qo, EFI variable reads, sudo -n dmesg, sudo -n grep (matching lines and counts), sudo -n objcopy/lsinitcpio/bsdtar on a scratch copy of the UKI, findmnt and btrfs property get on a scratch symlink chain, curl with sha256sum for public raw files, GitLab API GET; no git write commands and no lane writes
Installs: none
