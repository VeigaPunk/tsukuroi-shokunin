# SCOUT — SH6 journal boot-end context (round 26, wave 1)

Verdict: done — six boots are retained, five of them completed, and none of the five carries a
persisted orderly system-shutdown record; only one (boot -2) shows a journal that simply stops
with no shutdown activity, one (boot -1) shows a reboot that started and lost its tail, and the
three oldest have no system journal left at all, so their end state cannot be assessed from the
journal as retained.

## Findings

1. [obs] Retention now covers six boots on a three-day window, and the lane note describes an
   entirely different, older set. `journalctl --list-boots --no-pager` returns 7 lines (header plus
   six boot rows); the oldest row is `be045967…` starting 2026-10-19 18:55:14 and the current boot is
   `6a7f4fdf-ac62-4e2e-a6c1-b3c55d6f94f4` (`cat /proc/sys/kernel/random/boot_id`, `uptime -s` =
   2026-10-22 04:55:40). The note `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/journal-boot-plane.md:26`
   is titled "The 13 retained boots" and tables boots from 2026-10-03 17:42 to 2026-10-14, with boot
   0 id `d7f0bc8d`; no boot id from that table survives in the current journal files, so every count
   in that section is now unreproducible rather than wrong. [obs] The journal itself records why old
   boots are gone: at 2026-10-20 08:58:00 `systemd-journald[1023]` printed "System Journal
   (/var/log/journal/432d02b544a5459ebbff9c42ec68334d) is 252.6M, max 256M, 3.3M free", and
   `journalctl --disk-usage` now returns 86.4M, so the directory sat at a 256M cap and older files
   were rotated out.

2. [obs] The six boots are not equally backed by journal files. Boots -5, -4, -3 (`be045967`,
   `430d3038`, `84755511`) contain zero records with `_PID=1` and zero kernel-transport records, and
   their only surviving content is the rotated user journal
   `/var/log/journal/432d02b544a5459ebbff9c42ec68334d/user-1000@00065e452b3ff661-df579458cb209800.journal~`,
   whose own boot list is exactly those three boots plus `ed8819b0`. Counts from
   `journalctl -b <idx> --no-pager -o json _TRANSPORT=kernel | wc -l`: -5 = 0, -4 = 0, -3 = 0,
   -2 = 513, -1 = 17324, 0 = 3894. The rotated system file
   `system@00065e452b2f38ea-bac3f4488c2cf8d4.journal~` lists only `ed8819b0` (boot -2) for
   2026-10-20 08:58:00 to 09:56:15. Consequence: for the three oldest boots the system-side record is
   absent, not the shutdown.

3. [obs] Those three boots each end with a complete user-manager shutdown sequence. Each has exactly
   one `Reached target Exit the Session` record (count from `journalctl -b <idx> -o cat -g 'Reached
   target Exit the Session' | wc -l`: -5 = 1, -4 = 1, -3 = 1, -2 = 0, -1 = 1, 0 = 0), and their last
   records are the user manager's `Reached target Shutdown`, `Finished Exit the Session`, `Reached
   target Exit the Session` at 22:47:26, 06:37:07 and 08:54:20 respectively. [inf] A clean user
   session exit is consistent with an orderly reboot, but it says nothing about the system-side
   shutdown, which was not persisted for those boots.

4. [obs] Boot -2 (`ed8819b0`, 2026-10-20 08:58:00 to 09:56:15) is the one completed boot whose system
   journal is present and whose end shows no shutdown activity of any kind. Its last PID 1 record is
   a coredump unit deactivation at 09:56:13 and its last record overall is a kernel firewall line at
   09:56:15. A sweep inside that boot for shutdown wording
   (`journalctl -b -2 -o short-iso -g 'powering down|Powering off|reboot|Reboot|shutdown|Shutdown|halt|Halt'`)
   returns only the boot-time `Starting Record System Boot/Shutdown in UTMP` and its `Finished`
   counterpart; there is no logind power or reboot message, no unit unmount, and no user-session
   exit. [obs] Inside the same boot journald was restarted once, `systemd-journald[1023]` at 08:58:00
   and `systemd-journald[152664]` printing `Journal stopped` at 09:16:53; that is a daemon restart,
   not a system shutdown, and logging continued for another 39 minutes afterwards.

5. [obs] Boot -1 (`3e7084f4`, 2026-10-20 09:57:09 to 2026-10-22 04:54:50) began an orderly reboot and
   lost the final records. `systemd-logind[1388]` printed "System is rebooting." at 04:54:48, PID 1
   unmounted `/fast` at 04:54:48, stopped the UTMP recorder at 04:54:50, then unmounted `/boot`,
   `/home`, `/tmp` and the package cache, and the last system record is `Stopping Flush Journal to
   Persistent Storage` at 04:54:50. No `systemd-shutdown` record and no `Reached target System
   Reboot` record was persisted. [inf] The shutdown was in progress when journal persistence stopped,
   so the missing tail is a persistence artifact of an orderly reboot. This boot is the proof case
   that "no final shutdown record" does not mean "unclean shutdown".

6. [obs] Zero records anywhere in the retained journal match a final-shutdown marker. The sweep
   `journalctl --no-pager -o short-iso -g 'Reached target System (Power Off|Reboot|Shutdown|Halt)|Reached target (Reboot|Power-Off|Halt)|Shutting down\.|systemd-shutdown'`
   prints `-- No entries --`, and a piped `grep -c .` returns 0 with exit status 1. Trap observed
   first-hand and already documented by the lane note at
   `journal-boot-plane.md:151-175`: `journalctl … | wc -l` counts the `-- No entries --` line as 1,
   so my first pass reported one `systemd-shutdown` record where there are none.

7. Answer to the assigned question, in two readings. If "ended without an orderly shutdown record"
   means no persisted final system-shutdown record, the count is five of five completed boots
   (boots -5, -4, -3, -2, -1; boot 0 is live and excluded). If it is restricted to boots whose system
   journal survives at all, the count is two of two (boots -2 and -1). The split inside the five is
   one boot ending mid-shutdown with the shutdown begun (boot -1), one boot ending with no shutdown
   activity at all (boot -2), and three boots whose system journal was rotated away (boots -5, -4,
   -3), which are unassessable rather than negative.

8. [obs] Gaps between a boot's last record and the next boot's first record, from the
   `--list-boots` rows: 58 s (-5 to -4), 48 s (-4 to -3), 220 s (-3 to -2), 54 s (-2 to -1), 51 s
   (-1 to 0). [inf] The 48 to 58 second gaps fit a normal reboot cycle on this host (about 18 s
   firmware, 5 to 10 s loader and tens of seconds of kernel), which supports an orderly reboot
   reading for boots -5, -4 and -3; the 220 second gap before boot -2 is the outlier and is not
   explained by anything in the retained journal. [unk]

9. [obs] SH6 framing is unaffected either way, and I make no dated-incident or causal claim. The
   frozen capture records the counters as lifetime values:
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/capture/capture.txt:194`
   "Power Cycles: 325" and `:196` "Unsafe Shutdowns: 200", with the file's sha256 confirmed as
   `002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd`. The retained journal spans
   five completed boots in about three days, which is a negligible window against a lifetime counter,
   and finding 5 shows a clean reboot can also leave no final record, so a missing shutdown record in
   this window must not be read as an unsafe shutdown. [unk] Whether any retained boot corresponds to
   an increment of that counter; the device counter is monotonic and undated and I did not re-probe
   the device.

10. [obs] The lane note already carries the correction for its failed-service section, and my re-run
    confirms the mechanism. `journal-boot-plane.md:416-425` records the round-4 erratum that §4's
    "zero unit-activation failures in 13 retained boots" was superseded, with four failure records
    found by a case-insensitive sweep, and attributes the miss to the lowercase `failed with result`
    against systemd's capitalised form. The documented rule behind it, from `man journalctl`
    (systemd 262, entry `-g, --grep=`): "If the pattern is all lowercase, matching is case
    insensitive. Otherwise, matching is case sensitive." Measured on current retention:
    `journalctl -b -2 -p warning -o cat -g 'Failed to (start|load)|failed with result'` counts 3
    records (portal only), while the same command with `|Failed with result'` counts 4 and the extra
    record is a user unit failure at priority 4; `-g 'failed with result'` alone counts 1. So the
    note's pattern is mixed case, not "strict lowercase", which is why the whole alternation is
    case-sensitive, and one real unit failure in current retention is invisible to the pattern as
    written. The note's body at `:163` still carries the unsuperseded sentence, with the erratum as
    the only pointer.

11. [obs] Secondary divergence from the note worth one line for the SH6 prose: the note's
    failed-service section characterises its positive set as "the only `Failed to` lines are
    user-session portal warnings" (`journal-boot-plane.md:163`). In current retention the same
    priority-limited sweep also returns two `run-…service: Failed to set up mount namespacing` records
    at 2026-10-20 17:49:56 and 17:50:35, alongside fifteen portal records, so the class description
    holds only for the note's own capture window.

## Method notes

- All probes were read-only `journalctl` reads; no sudo was needed and none was used. The journal
  directory is readable through the `wheel` ACL, as the lane note records at
  `journal-boot-plane.md:1-23`.
- Journal file inventory from `ls -la /var/log/journal/432d02b544a5459ebbff9c42ec68334d/`:
  `system.journal` (boots -1, 0), `system@…2c70cb….journal` (boot -1, 2026-10-20 09:57:09 to
  2026-10-21 18:27:20), `system@…bac3f4488c2cf8d4.journal~` (boot -2 only), `user-1000.journal`,
  and three rotated or archived `user-1000@…` files. Boot -1 is spanned by two system files under
  one boot id, so a per-file reading alone would understate that boot.
- Journal text was read only through timestamp, unit and identifier fields; no user data is quoted
  here beyond unit names and one unit failure line.

Scope: read=journalctl --list-boots/--disk-usage/-b/-g/-p sweeps and per-file --list-boots over /var/log/journal/432d02b544a5459ebbff9c42ec68334d/, man journalctl, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/journal-boot-plane.md (lines 1-300, 404-438), /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/capture/capture.txt (grep), /proc/sys/kernel/random/boot_id; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w1/ScoutJournalBoots.md; executed=journalctl (list-boots, disk-usage, -b sweeps, --file --list-boots), ls, cat, man, grep, python3 gap arithmetic, sha256sum, uptime
Model: opencode-go/deepseek-v4.1-flash
Installs: none
