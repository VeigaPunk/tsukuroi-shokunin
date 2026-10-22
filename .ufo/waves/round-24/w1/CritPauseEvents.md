# CritPauseEvents — critic review of C2 premise P5 (round 24, wave 1)

Verdict: the P5 events are real, but four pieces of the current wording overclaim: "the cache holds 4 files", "operator-side" or "the operator's own act", the clean being dated only to 04:09–04:10, and the cache count as a falsifier. One evidence pointer also does not resolve. The five installs are new packages installed with `pacman -U` from local files, not upgrades and not `-S`, and they were not a partial upgrade. The partial-upgrade risk is the state that the later `pacman -Sy` left behind.

Target text reviewed: the P5 wording in the round-24 assignment brief and the uncommitted draft `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/pause-lift-gate-r24.md:47-52,62,69`.

## Findings

1. [obs] **All five are new installs of foreign, locally built packages. They came from three `pacman -U` transactions of files in the yay build cache. None is an upgrade and none is a `-S`.**
   Evidence: `/var/log/pacman.log` lines 3161-3187 (read-only `grep -n`, exit 0). Each transaction runs `pacman -U ... /home/vgpnk/.cache/yay/<pkg>/<pkg>-<ver>-x86_64.pkg.tar.zst` and logs only `[ALPM] installed`, never `upgraded`. Committed copy: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/capture/l1-2/capture.txt:220,222,225`.
   `pacman -Qi` for all five, exit 0, reports `Packager : Unknown Packager` and `Validated By : None`. Each build date is 7 to 66 seconds before its install date; for example zcode was built at 13:23:01 and installed at 13:23:08. That is a local makepkg build, not a repository package.
   `pacman -Si <pkg>` fails for all five (exit 1), and `capture.txt:701-706` (`pacman -Qm`) lists all five as foreign.
   - zcode was installed with `--needed`, while tizen-sdb and openssl-1.0 were not. [inf] The two use different yay invocations, possibly from different callers.
   - Between the transactions, the log has no `-S` lines and no installed dependencies. Only the named packages and their `-debug` splits were installed (log lines 3164, 3173-3174, 3182-3183).

2. [obs] **The five installs were not a partial upgrade. They followed the last full upgrade and came before the only sync refresh of the pause.**
   - Last full upgrade: `pacman.log:2462-2464`, `Running 'pacman -Syu ...'` then `starting full system upgrade` at 2026-10-20 09:15:30.
   - Refreshes since then: only `pacman.log:3188-3189`, `pacman -Sy --noconfirm` at 2026-10-21 20:32:00. This came after all three `-U` transactions (10-20 13:23, 10-21 17:55 and 18:07).
   - Arch doctrine names two unsupported patterns: `pacman -Sy package`, and "`pacman -Sy` followed by `pacman -S package`". `pacman -U` of a local file is not in that list.
     - Source: https://wiki.archlinux.org/index.php?title=System_maintenance&action=raw, opened 2026-10-22, line 105: "{{ic|pacman -Sy}} followed by {{ic|pacman -S ''package''}} (instead, {{ic|-S'''u'''}} should be used in the installation of the package)."
   - [inf] Answer to "does installing a new package count as a partial upgrade when the sync database was refreshed after the last full upgrade": yes, by doctrine, if it is a `-S` from the refreshed database. The doctrine does not distinguish new packages from upgrades; the risk is a newer library pulled in as a dependency. That did not happen here, because the refresh came after the installs.
   - [inf] The open risk is the present state. The 20:32 refresh rewrote the `omarchy.db` and `openai-chatgpt.db` sync databases. Their mtimes are 2026-10-21 19:44 and 2026-10-20 23:22, both after the 10-20 09:15 sync (`capture.txt:31-35` in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/capture/l1/capture.txt`), and 3 upgrades from those two repositories are pending (`l1/capture.txt:40-42,52-54`). So the next `pacman -S <pkg>` without `-u`, or a `makepkg -s` dependency install, would be the unsupported pattern for those two repositories.
   - Local builds carry a soname risk of their own. Source: https://wiki.archlinux.org/index.php?title=System_maintenance&action=raw line 116: "If the system has locally built packages (such as [[AUR]] packages), users will need to rebuild them when their dependencies receive a [[Wikipedia:soname|soname]] bump."
   - Building also expects an up-to-date system first. Source: https://wiki.archlinux.org/index.php?title=Arch_User_Repository&action=raw line 186: "Ensure your build environment is up-to-date by [[Pacman#Upgrading packages|upgrading]] before building anything."

3. [obs] **Overclaim: "the package cache holds 4 files". It holds 0 package files and 4 empty pacman download staging directories, and their times match the four `-U` transactions to the second.**
   - `sudo -n find /var/cache/pacman/pkg -mindepth 1` (exit 0) lists only `download-vcoq00`, `download-Lsbwhh`, `download-0jh7Uc` and `download-r5r0Ix`.
   - `sudo -n find /var/cache/pacman/pkg -type f | wc -l` prints `0`.
   - `sudo -n stat -c "%y %U %s %n"` reports owner `alpm` and size 0 for each. A size-0 directory on btrfs is empty.
   - Their mtimes are 2026-10-20 09:31:03, 2026-10-20 13:23:08, 2026-10-21 17:55:56 and 2026-10-21 18:07:37. These equal the four `pacman -U` runs, including the pre-pause elephant `-U` at 09:31:03 (`pacman.log:3092`).
   - The capture section is titled `cache-file-count`, but it runs `ls /var/cache/pacman/pkg | wc -l` (`l1-2/capture.txt:233-235`). That counts names, not package files.
   - [inf] The count of 4 is a by-product of `-U` transactions, not a measure of rollback capacity. One more `-U` makes it 5 with rollback capacity unchanged. The falsifier "P5 falls if the cache count is not 4" (`pause-lift-gate-r24.md:69`) therefore tests the wrong quantity.

4. [obs] **Overclaim by omission: the cache was not emptied only at 04:09–04:10 on 2026-10-22. Real (non-dry-run) removals began on 2026-10-20.**
   - Committed sudo lines: `paccache -r -k3` at 2026-10-20 20:48:48 (`l1-2/capture.txt:248`) and `paccache -r -u -k0` at 20:50:19 (`:253`).
   - On 2026-10-22: `paccache -r -k 1 --nocolor` at 02:59:33 (`:690`) and `paccache -r -k 3 --nocolor` at 02:59:57 (`:692`).
   - Then `paccache -rk1` and `paccache -ruk0` at 04:09:42 (`:694-695`), and `pacman -Scc --noconfirm` at 04:10:08 and `pacman -Scc` at 04:10:19 (`:696-697`).
   - [inf] With only 1.31.3 and 1.32.0 cached, `-k3` keeps both. The libinput 1.31.3 revert file therefore most likely went at the `-k 1` run at 02:59:33, not at 04:09 or 04:10. [unk] paccache's own output was not retained, so this cannot be confirmed read-only.
   - The draft's sentence "after `paccache -rk1`, `paccache -ruk0` at 04:09 and `pacman -Scc` at 04:10" (`pause-lift-gate-r24.md:49`) names only the last three steps.

5. [obs] **Overclaim: the pause-time installs, the refresh and the cache clean are "operator-side" or "the operator's own act". The evidence supports only "account vgpnk through sudo, without a terminal, outside the fleet repo".**
   - Every relevant sudo line names user vgpnk, `USER=root`, and has no `TTY=` field: `sudo -n journalctl _COMM=sudo` for 2026-10-20 13:15 to 2026-10-21 20:40 and for 2026-10-22 03:50 to 04:15, both exit 0. Committed copies are at `l1-2/capture.txt:240-261,694-697`.
   - Since 2026-10-01, only 3 sudo lines on this host carry `TTY=pts`. They are `cryptsetup` at 2026-10-20 08:24 and two `python3` runs at 2026-10-22 03:24 and 03:32. Sudo without a terminal is the normal signature of tool-driven shells on this host, so it cannot single out the operator.
   - The 02:56–03:00 window shows machine-speed, interleaved sudo bursts. Several commands start in the same second, for example 02:59:21 with 8 `btrfs inspect-internal dump-tree` calls, alongside `lsof +D`, `snapper list`, `journalctl --vacuum-size=100M`, and `find` over the agent harness log directory. The 04:06–04:10 window shows the same pattern: `/tmp` purges, `du` sweeps, `paccache`, `journalctl --vacuum-size=200M`, then `pacman -Scc`.
   - [inf] The cache clean ran inside an automated disk-space cleanup session under the operator's account. Whether the operator ordered it is [unk] from host evidence.
   - [obs] A search of the agent harness directory for the strings `paccache -ruk0` and `pacman -Scc` found no matches.
   - [obs] `paccache.timer` is enabled. Its last run was 2026-10-20 09:20:41 and its next is 2026-10-26 00:00 (`systemctl list-timers paccache.timer --all`, exit 0), so it did not cause the clean.
   - [inf] The 20:32 `pacman -Sy --noconfirm` does not match either `pacman -Sy` line in `/home/vgpnk/.local/share/omarchy/bin/omarchy-update-keyring:12,21`. Line 12 has no `--noconfirm`, and line 21 names `archlinux-keyring`. Its caller is [unk].

6. [obs] **Overclaim of strength in the verdict sentence.** The verdict "the pause held for lanes' repository upgrades but not for operator-side local installs, a refresh and a cache clean" (`pause-lift-gate-r24.md:52`) has two problems.
   - "Held for lanes' repository upgrades" is [unk] as a compliance claim. The log shows only that no `-S` or `-Su` transaction ran after 2026-10-20 09:40 (`pacman.log:3161-3191`). It cannot show that any lane wanted one and refrained.
   - "Package transactions during the pause" should be counted by kind:
     - three ALPM transactions, all `-U`, installing 5 packages;
     - six `pacman -D` install-reason edits;
     - one sync refresh, `-Sy`, which is not an ALPM transaction;
     - two `pacman -Scc` runs;
     - six `paccache -r` runs.
     - Committed lines: `l1-2/capture.txt:220-230,248,253,690,692,694-697`.
   - Calling all of these "package transactions", or calling the five packages "five transactions", overcounts.

7. [obs] **Evidence placement defect.** The C2 brief and the planned JSON name `.ufo/waves/round-24/capture/l1/capture.txt`. That file has no `pacman -U` line, no `paccache` line, no `-Scc` line, no cache count and no sudo attribution. Searching it for `Scc|paccache|pacman -U|cache-file` returns only `command continued` journal fragments. Its only P5 lines are the five `[ALPM] installed` lines at `l1/capture.txt:122-126`.
   - Every cache-clean, `-U` and attribution pointer in the draft resolves only in `l1-2/capture.txt`.
   - [inf] If the JSON's `capture` field stays on `l1`, P5's cache wording has no line to resolve against. The gate checker would then either fail P5 or count it on the `installed` lines alone, which do not support the cache claims.

8. [obs] **False provenance next to P5.** The draft gives the pause's origin as `.ufo/l0-questions.md lines 54-55` (`pause-lift-gate-r24.md:7-8`). In the lane, that file is tracked, has 2 lines, was last modified 2026-10-15 (before the pause), and is about round-1 route bindings (`git show HEAD:.ufo/l0-questions.md | wc -l` printed `2`).
   - The intended file is likely the fleet-level copy, which is outside this lane and was not read.

9. [obs] **The "keep a Snapper pre-snapshot" fallback is advice, not an existing safety net.**
   - `sudo -n snapper -c root list` (exit 0) shows only two manual snapshots: #1 `pre-nvme-baseline-2026-10-20` at 09:03:02 and #2 `pre-aur-elephant-2.22.1` at 09:29:19, both on 2026-10-20 before the pause.
   - `pacman -Q snap-pac` reports the package is not found.
   - `/usr/share/libalpm/hooks/10-limine-snapper-lock.hook` only waits for a lock (`Exec = /usr/share/libalpm/scripts/limine-snapper-lock`). It takes no snapshot.
   - No root snapshot covers the three pause-time `-U` transactions. [inf] Reverting them means `pacman -R`. Rollback by cache is gone for every package, not only the boot chain.
   - Source: https://wiki.archlinux.org/index.php?title=Pacman&action=raw, opened 2026-10-22, line 297: "This will prevent downgrading or reinstalling packages without downloading them again."

## Impacted axes

- C2 freshness: P5 is one of the 5 counted premises. Its verdict word "changed" survives, but the "4 files" premise text and the "operator" attribution do not.
- Calibration and provenance: the attribution in finding 5, the cache count in finding 3 and the pause citation in finding 8.
- Gate-check validity: the capture path in finding 7 and the brittle falsifier in finding 3.

## Smallest safe correction (draft wording for the L1)

> P5 — [obs] Since 2026-10-20 09:40 the pacman log records three `pacman -U` transactions of locally built foreign packages from the yay build cache. They are new installs, not upgrades, and none used `-S`: zcode; tizen-sdb with tizen-sdb-debug; openssl-1.0 with openssl-1.0-debug. The log also records one `pacman -Sy --noconfirm` (2026-10-21 20:32) and two `pacman -Scc` runs (2026-10-22 04:10) (`l1-2/capture.txt:220-230`). Non-dry-run `paccache -r` ran on 2026-10-20 at 20:48 and 20:50, and on 2026-10-22 at 02:59 (twice) and 04:09 (twice) (`l1-2/capture.txt:248,253,690,692,694-695`). The package cache now holds 0 package files; its 4 entries are empty pacman download directories left by `-U` transactions. Sudo attributes every step to account vgpnk without a terminal and outside the fleet repo (`l1-2/capture.txt:240-261,694-697`). Whether the operator or a tool acting under that account issued them is unknown.
> [inf] The installs came after the last full upgrade (2026-10-20 09:15) and before the only refresh, so they were not a partial upgrade. After that refresh, any `pacman -S <pkg>` without `-u` is the unsupported pattern. No package-cache rollback exists, and no root snapshot was taken after 2026-10-20 09:29.
> Verdict: **changed**.
> Falsifier: a re-capture shows at least one `*.pkg.tar.*` file in `/var/cache/pacman/pkg`, or any `upgraded` or `-S` line in the pacman log after 2026-10-20 09:40.

The `capture` field and evidence lines should point to `l1-2/capture.txt`, or the cache-file and attribution lines need to be added to the `l1` capture. A capture line counting `find /var/cache/pacman/pkg -type f -name '*.pkg.tar.*' | wc -l` would give the 0 a committed line.

## SOURCES row drafts (ids assigned by the L1)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0NN | https://wiki.archlinux.org/index.php?title=System_maintenance&action=raw | wiki | community-doc | partial upgrades, local builds | line 105: "{{ic\|pacman -Sy}} followed by {{ic\|pacman -S ''package''}} (instead, {{ic\|-S'''u'''}} should be used in the installation of the package)." | the unsupported patterns are `-Sy pkg` and `-Sy` then `-S pkg`; `-U` of a local file is not listed | active | 2026-10-22 | on wiki revision change | C2 P5 |
| S0NN | https://wiki.archlinux.org/index.php?title=System_maintenance&action=raw | wiki | community-doc | locally built packages | line 116: "If the system has locally built packages (such as [[AUR]] packages), users will need to rebuild them when their dependencies receive a [[Wikipedia:soname\|soname]] bump." | foreign `-U` installs carry a soname-rebuild risk separate from partial upgrades | active | 2026-10-22 | on wiki revision change | C2 P5 |
| S0NN | https://wiki.archlinux.org/index.php?title=Pacman&action=raw | wiki | community-doc | package cache | line 297: "This will prevent downgrading or reinstalling packages without downloading them again." | an emptied cache removes local downgrade and reinstall | active | 2026-10-22 | on wiki revision change | C2 P5 |
| S0NN | https://wiki.archlinux.org/index.php?title=Arch_User_Repository&action=raw | wiki | community-doc | AUR build precondition | line 186: "Ensure your build environment is up-to-date by [[Pacman#Upgrading packages\|upgrading]] before building anything." | AUR builds assume a fully upgraded host | active | 2026-10-22 | on wiki revision change | C2 P5 |

Scope: read=lane SCORECARD.md:740-756, .ufo/waves/round-24/capture/l1/capture.txt, .ufo/waves/round-24/capture/l1-2/capture.txt (lines 195-265 and 685-708 plus targeted searches), corpus/knowledge/pause-lift-gate-r24.md, .ufo/l0-questions.md, ~/.agents/skills/godspeed/{SKILL.md,directive.md}, /var/log/pacman.log, sudo journal, /usr/share/libalpm/hooks/10-limine-snapper-lock.hook, /home/vgpnk/.local/share/omarchy/bin/omarchy-update-keyring:1-25, a name-only search of /home/vgpnk/.omp for two command strings (no matches), three Arch wiki raw pages; wrote=.ufo/waves/round-24/w1/CritPauseEvents.md; executed=grep/awk over /var/log/pacman.log (exit 0), pacman -Qi/-Si/-Sl/-Q for the five packages and snap-pac (read-only), ls -la and sudo -n find/stat on /var/cache/pacman/pkg (exit 0), sudo -n journalctl _COMM=sudo with PWD redacted (exit 0), sudo -n snapper list-configs and -c root list (exit 0), systemctl status and list-timers paccache.timer, journalctl -u paccache.service, git status/log/ls-files/show (read-only), curl -s and curl -sI of wiki.archlinux.org raw pages (exit 0)
Installs: none
