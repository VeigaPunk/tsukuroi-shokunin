# ExecSudoAttribution — C2/P5 evidence: sudo journal attribution of pacman/paccache records

Verdict: attributed 459 sudo package-tool records in the pause window
(2026-10-20 09:40 -03 to 2026-10-22) to pacman.log events and to cache
state changes, identified 11 transaction records and 29 paccache records
(as 22 dry runs and 7 other runs, one of which is `--version`), and found
the "4 entries" cache count consists of four empty alpm `download-*`
staging directories, not package archives.

Command executed: `journalctl _COMM=sudo --since '2026-10-20 09:40' --no-pager -o short-iso`
(exit 0); then keeping only lines whose COMMAND base name is pacman,
paccache, makepkg, yay or paru. Snapshot time 2026-10-22T08:47:25Z.
A full per-record table of all 459 records (time, user, target user, PWD
class, sanitized command) is in the companion appendix
`ExecSudoAttribution/sudo-records.tsv` in this seat's draft directory.

## Findings

1. [obs] Total records in window: 459. Breakdown: 419 read-only queries
   (418 `pacman -Q` + 1 `pacman -Qq`), 11 pacman transaction/database
   records, 29 paccache records. All 459 invoked by user `vgpnk` as target
   `root` (USER=root). Zero `makepkg` records, zero `yay` records, zero
   `paru` records; yay appears only as the source path prefix
   `/home/vgpnk/.cache/yay/` inside the three `pacman -U` commands.
2. [obs] The 11 pacman transaction records map 1:1 to the 11
   `[PACMAN] Running` lines in /var/log/pacman.log in the pause window
   (lines 3161, 3169, 3170, 3177, 3178, 3179, 3186, 3187, 3188, 3190,
   3191), and thereby to the ALPM `installed` lines and hook runs produced
   by the three `pacman -U` transactions (zcode; tizen-sdb + tizen-sdb-debug;
   openssl-1.0 + openssl-1.0-debug) and by `pacman -Sy --noconfirm`
   (line 3189 "synchronizing package lists"). No other sudo record in the
   window explains any pacman.log line; `pacman -Q/-Qq` and `paccache`
   produce no pacman.log entries (grep of the log for `Running 'pacman -Q`
   and for `paccache` returns zero).
3. [obs] The five foreign packages installed during the pause (zcode,
   tizen-sdb, tizen-sdb-debug, openssl-1.0, openssl-1.0-debug) are exactly
   the five `[ALPM] installed` lines in the window (3164, 3173, 3174,
   3182, 3183). The sudo records with the timestamps matching the
   `[PACMAN] Running` lines are the causal attribution for each.
4. [obs] 29 paccache records: 22 are dry runs (`-d`/`--dryrun`), 6 are
   actual removals (`-r` without `-d`: 2026-10-20T20:48:48 `-r -k3`;
   2026-10-20T20:50:19 `-r -u -k0`; 2026-10-22T02:59:33 `-r -k 1`;
   2026-10-22T02:59:57 `-r -k 3`; 2026-10-22T04:09:42 `-rk1`;
   2026-10-22T04:09:42 `-ruk0`), and 1 is `--version` (no operation).
   The two `pacman -Scc` records (2026-10-22T04:10:08 with
   `--noconfirm`, 2026-10-22T04:10:19 without) also remove cached packages.
5. [obs] The current cache `/var/cache/pacman/pkg` holds exactly 4
   entries, and all four are empty `download-*` directories owned by
   `alpm` (0700), created at 2026-10-20T09:31, 13:23, and 2026-10-21T17:55,
   18:07 respectively. There are zero `*.pkg.tar*` archives in the cache
   (find as root returns nothing). The L1 capture's "cache-file-count 4"
   (`ls /var/cache/pacman/pkg | wc -l`) counts those directories, not
   package archives, so rollback-by-cache is not merely limited to the boot
   chain: there is no cached package at all.
6. [obs] The L1 capture's own `sudo-package-commands-since-pause` section
   (`.ufo/waves/round-24/capture/l1-2/capture.txt` lines 238-699) used the
   reduced `sed` pipeline `s/PWD=\/home\/vgpnk\/Projects\/shokunin[^;]*/PWD=inside-fleet-repo/; s/PWD=[^;]*/PWD=outside-fleet-repo/`
   and `cut -c1-220`; because the second substitution also matches the
   first's output, it reports every line as `outside-fleet-repo` and can
   never show `inside-fleet-repo` (0 matches when re-run). The one record
   whose PWD is inside the fleet repository root (2026-10-22T05:41:45 -03,
   `paccache -d -k1`, dry run) happened after both l1 and l1-2 captures
   (captures at 2026-10-22T08:19:59Z / 08:30:48Z), so it is absent from
   the committed capture; it is present in this run and in the appendix.
7. [obs] The pause window start used here (2026-10-20 09:40 -03) matches
   the L1 capture and the claim text. Twenty-four package-tool sudo records
   precede that bound on the same day, including the 2026-10-20T04:25:16
   `pacman -S --needed --noconfirm libinput libinput-tools` partial upgrade
   named in the corpus as the pause trigger, and the operator's
   2026-10-20T09:15:30 `pacman -Syu` full upgrade; they are outside the
   window and are listed in the appendix context for completeness.
8. [obs] The three `pacman -U` transactions used package files under
   `/home/vgpnk/.cache/yay/` (sandboxed here to package names per the
   privacy rule). No makepkg/yay/paru sudo invocation is recorded, so the
   build step that produced those archives is not observable in the sudo
   journal ([unk] who built them and when).

## Fix for the L1 capture's PWD reduction

The two-step sed in the capture collapses (fix should capture a marker or
use `PWD=(/home/vgpnk/Projects/shokunin/tsukuroi-shokunin|...)/`; the
current output makes inside/outside indistinguishable and visibly claims 0
inside records even though the 2026-10-22T05:41:45 record is inside the
fleet root).

Report: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecSudoAttribution.md
Companion appendix: .ufo/waves/round-24/w1/ExecSudoAttribution/sudo-records.tsv

Scope: read=/var/log/pacman.log, journalctl _COMM=sudo window, .ufo/waves/round-24/capture/l1-2/capture.txt, /var/cache/pacman/pkg; wrote=.ufo/waves/round-24/w1/ExecSudoAttribution.md, .ufo/waves/round-24/w1/ExecSudoAttribution/sudo-records.tsv; executed=journalctl queries, grep/sed/awk/python on those outputs, sudo -n ls/find on the cache (read-only).
Installs: none
