source: round-24 L1 read-only capture `.ufo/waves/round-24/capture/l1-4/capture.txt` (script `.ufo/waves/round-24/capture/capture.sh`; temporary-database output `l1-4/checkupdates.out`); SOURCES S087-S103, all opened 2026-10-22; machine-readable twin `pause-lift-gate-r24.json`.
verified-at: 2026-10-22 (capture taken 2026-10-22T08:46:28Z, `capture.txt:3`).
recheck: after any package transaction, database refresh, reboot or omarchy release. Procedure: `bash .ufo/waves/round-24/capture/capture.sh <new-empty-dir>` (host-read-only; it writes only inside the new directory and a temporary checkupdates database under /fast/scratch), update the JSON pointers, then `python3 tools/check-pause-gate.py --revision <commit>`.

# Pause-lift update-safety gate — round 24

The fleet paused every pacman transaction on 2026-10-20 after a lane ran a partial
upgrade (fleet `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md` lines 54-55). The
pause rested on five host premises. This entry gives each premise a dated verdict
from one read-only capture and sources opened on 2026-10-22. It is evidence for the
operator's decision. It is not permission to lift the pause, and it authorizes no
lane to run a transaction.

Verdict words: **cleared** (the premise no longer holds), **still-holds**,
**changed** (the premise holds in a different form, or partly), **unverified** (no
read-only evidence decides it). Line numbers below are `capture.txt` lines of the
`l1-4` capture unless another file is named.

## P1 — the host is far behind its upgrade target (413 pending rows on 2026-10-20)

- [obs] Against the local sync databases `pacman -Qu` lists 3 rows: `1password-beta`, `chatgpt-bin`, `claude-code` (`:40-42`), from the third-party `omarchy` and `openai-chatgpt` repositories (`:52-54`).
- [obs] Against the current omarchy stable snapshot, pacman-contrib `checkupdates` (a temporary database copy under /fast/scratch; the host databases are not touched) lists 134 rows (`:374`). Boot-chain rows: `limine 12.9.3-1 -> 12.9.4-1` and `systemd 262-1 -> 262.1-1` (`:375-376`). No mkinitcpio, linux, linux-lts, plymouth or nvidia row is pending.
- [obs] The list includes `ca-certificates-mozilla 3.131-1 -> 3.131.1-1` (`checkupdates.out:6`). The Arch security notice of 2026-10-21 asks everyone to reach at least 3.131.1-1 (S088); the archive shows only one other item in October, for php, which is not installed (S087).
- [inf] The 413 figure was discharged by the operator's full upgrade of 2026-10-20 09:15 -03 (round-17 notices). A `-Qu` count compares versions against the local databases only and does not check replacements (S089); here it understates the pending set because the mirror moved after the last refresh (P4).
- Verdict: **changed**. The host is no longer 413 rows behind, but it is 134 rows behind the current target, including two boot-chain packages and a security fix that the pause now withholds.

## P2 — partial-upgrade residue from the 2026-10-20 libinput install

- [obs] No installed package is newer than its sync-database entry (empty block, `:57-59`); an independent sweep of all 1399 installed packages agreed (wave seat RevIndependentP1P2).
- [obs] `libinput 1.32.0-1` is installed (`:73`) and is the sync version (`:88`).
- [inf] The libinput partial upgrade of 2026-10-20 04:25 -03 is reconciled by the later full upgrade. Packages with no sync entry (21 foreign packages) are outside this probe. Since the `pacman -Sy` of 2026-10-21 20:32 -03 (`:221`) the host sits in the state Arch doctrine warns about: any later single-package `pacman -S` would be an unsupported partial upgrade; the repair is a full upgrade (S092).
- Verdict: **cleared** — no residue observed.

## P3 — mkinitcpio 42 breaks the configured late hooks that still name `/new_root`

- [obs] mkinitcpio 42.2-1 is installed (`:63`); busybox init mounts root at `/sysroot` (`:104-113`). The configured late hooks still name `/new_root`: `btrfs-overlayfs:4` and `plymouth:11` (`:93-94`).
- [obs] mkinitcpio creates `new_root` as a relative symlink to `sysroot` in every image (`/usr/lib/initcpio/functions:1213`, `:117`; S094). Upstream added it on purpose: "To avoid issues (or to at least try to avoid them), /new_root will be kept as a symlink to /sysroot." (S095). Neither hook has an upstream or packaging change for 42 (S097, S098).
- [obs] Plymouth: the daemon handles `update-root-fs --new-root-dir=DIR` with `chdir` then `chroot(".")`, which follows a symlink (S096). On boot 0 the firmware selected `Omarchy.linux` (`:340-341`, `rootflags=subvol=@` at `:349`); plymouthd ran as PID 535 (`:142`), older than the root `mount` process 942 (`:328`), and `/var/log/boot.log` and `boot-duration` were written into the real root at 04:55:44 (`:321-323`). [inf] The initramfs plymouth daemon reached the real root through `/new_root`.
- [obs] btrfs-overlayfs: an unprivileged namespace probe with the image's own util-linux showed `findmnt --mountpoint`, `mount --move` and the overlay mount all resolve through the symlink (wave seats ExecSymlinkMountProbe and CritHookCompat).
- [unk] The hook acts only on a read-only snapshot boot. The snapshot-2 entry boots the same 42.2 image into a read-only subvolume, and no such boot has run. Initramfs failures are silent here: hook return codes are ignored and the command line has `quiet loglevel=0` (`:346-347`).
- Verdict: **changed** — not a pending-upgrade risk any more; ordinary boots on 42.2 work and plymouth's path is evidenced; the snapshot-boot overlay path stays unverified.

## P4 — the local sync databases show how far the host is from its target

- [obs] core, extra and multilib use one server, `https://stable-mirror.omarchy.org/$repo/os/$arch` (`:194`), written there by the omarchy installer from its stable template (S103).
- [obs] The local core and extra files keep mtime 2026-10-17 22:37 -03 (`:31-32`) and birth 2026-10-18 14:11 -03 (`:354-356`), although `pacman -Sy --noconfirm` ran on 2026-10-21 20:32 -03 (`:221`). Only the two third-party databases were rewritten then (`:357-358`).
- [obs] pacman sets a database mtime from the server's Last-Modified on a real download and leaves the file untouched on a not-modified reply (S099). The stable mirror's core.db now reports `last-modified: Thu, 22 Oct 2026 04:40:03 GMT` (`:363`; S101); the stable mirror "changes only when a release ships" (S100).
- [inf] The upgrade target is the omarchy stable snapshot. The local mtime is the mirror's publication time of 2026-10-18 01:37 UTC, not a snapshot date. Whether the 2026-10-21 refresh got a not-modified reply or failed is not recorded: a failed download leaves the same file state and writes nothing to pacman.log. The mirror published a new snapshot at 2026-10-22 04:40 UTC, after that refresh.
- Verdict: **changed** — the local databases now understate the gap; the mirror's current snapshot, measured through a temporary database, is the honest target (P1).

## P5 — rollback by package cache, and package transactions during the pause

- [obs] The package cache holds 0 package files (`:284-286`); its 4 entries are empty `download-*` directories owned by alpm (`:290-297`).
- [obs] Six `paccache -r` runs (2026-10-20 20:48 and 20:50; 2026-10-22 02:59 twice and 04:09 twice, `:302-307`) and two `pacman -Scc` runs at 04:10 (`:222-223`, `:270-271`) emptied it. paccache `-k1` keeps one version per package and `-u -k0` drops uninstalled ones; `-Scc` removes all cached files (S091, S090). The sudo journal shows account vgpnk, working outside the fleet repo and without a terminal (`:233-271`); [unk] who ordered these runs.
- [obs] During the pause the log shows three `pacman -U` installs of five locally built foreign packages (zcode; tizen-sdb and its debug package; openssl-1.0 and its debug package; `:122-126`, `:276-281`), one `pacman -Sy`, and no `-S` or `-Su` (`:211-223`).
- [obs] `snap-pac` is not installed (`:317`). Snapper lists only two read-only root snapshots, both from 2026-10-20 before the pause (wave seat ExecRollbackPaths; unprivileged `snapper list` returns "No permissions.", `:312`).
- [inf] Rollback by cache is gone for every package, including the libinput 1.31.3 revert named in the L0 question. The remaining paths are the Arch Linux Archive (S093; it holds the installed and previous boot-chain versions, wave seat ExecRollbackPaths) and the two Snapper snapshots; the omarchy update path takes a Snapper snapshot before upgrading (S102).
- Verdict: **changed** — no cache rollback exists, and the pause did not stop operator-account installs, a refresh or the cache cleans.

## Gate summary for the operator

| Premise | Verdict | What it means for lifting the pause |
|---|---|---|
| P1 | changed | A full upgrade now moves 134 packages, including systemd 262.1, limine 12.9.4 and the ca-certificates-mozilla security fix; no initramfs-generator or kernel change. |
| P2 | cleared | No partial-upgrade residue. Do not install single packages before a full upgrade. |
| P3 | changed | Ordinary boots on 42.2 images work; the snapshot-boot overlay path is untested. |
| P4 | changed | The local databases are older than the mirror; measure the target with a temporary database, not `-Qu`. |
| P5 | changed | No cache rollback. Take a Snapper pre-snapshot first (the omarchy update does), and keep the Archive as the downgrade source. |

## Falsifiers

- P1 falls if a fresh temporary-database check shows a mkinitcpio, linux or plymouth row, or the security fix is already installed.
- P2 falls if a re-capture shows any installed-newer row.
- P3's "ordinary boots work" falls if a boot on a 42.2 image fails at switch-root; its unknown resolves only through a read-only snapshot boot.
- P4 falls if the stable mirror's core.db Last-Modified equals the host file's mtime.
- P5 falls if the cache holds any package file or the cited log lines are absent.

## Supersedes (append-only; old bytes are not rewritten)

- `corpus/knowledge/package-state-plane.md:39-40` open question whether the stable mirror lags upstream: answered by P4 and S100/S101.
- `corpus/README.md:10` "sync dbs born 2026-10-11, `-Sy` never run since" and `:38` "Pending `mkinitcpio` 42 upgrade strands two `/new_root` hooks": superseded by P4 and P3.
- `corpus/knowledge/update-safety-note.md:281-282` and `SKILL.md:382` 1password-beta downgrade trap: the installed BETA is now behind its channel (`:40`).
- `corpus/knowledge/partial-upgrade-recheck-r15.md` "413 pending" and the round-18 "pending count UNKNOWN" notes: superseded by P1.

## Corrections after wave-2 falsification

The JSON now cites correction rows S104-S114 where relevant; old rows S087-S103 remain historical. The new rows supersede source overreach without changing a verdict or the after-target 5.

- P1: 134 is the combined configured-repository set, 130 from the stable Arch snapshot and 4 from third-party repositories. S105 states only the article's requested version; the full-upgrade route is doctrine from S092, not a claim in the news article. The checkupdates output is now separately sha256-pinned by the checker.
- P3: the relative symlink's construction is S109; mounted-root behavior comes from separate init and probe evidence. S110 quotes the three daemon statements separately and corrects the client function locator to lines 724-754. Plymouth reaching the real root remains an inference. btrfs-overlayfs has not been boot-tested on a snapshot. The upstream-release watch for removal of the compatibility symlink is still open.
- P5: S113 pins the installed Omarchy v3.8.4 helper, not master. With configured Snapper configs the wrapper snapshots before its git and package steps and stops on helper failure; with zero configs it creates nothing but can return success. Existing snapshot counts and contents come from the read-only privileged wave-1 `ExecRollbackPaths.md`, not the unprivileged failed capture command. Archive HTTP availability does not prove an authentic, dependency-consistent restore or a successful boot.
- Supersession locators corrected: `SKILL.md:386-388`, `update-safety-note.md:280-284` (also lines 29-32, 353, 374, 397). The pending-count UNKNOWN notes are `host-health-report-r3.md:628` and `freshness-recheck-r18.json:90`, not the round-15 entry. Round-17 had already marked 413 historical at `partial-upgrade-recheck-r15.md:176` and the pending-upgrade wording historical at `README.md:149-151`; round 24 is not the first correction. The old capture time was 07:44 UTC and the subsequent full upgrade 09:15 -03.

recheck: `python3 tools/check-pause-gate.py --revision <commit>` validates committed evidence links only. A new live host capture requires explicit read-only authorization. The revised capture script uses a private temporary checkupdates database, cleans only that private directory, and writes checkupdates.out inside its output directory. The pinned l1-4 capture was generated by the earlier script at commit 22fd1642; later script privacy fixes do not retroactively reproduce or rewrite those bytes. Recheck cadence: on-release.

### Premise precision from fresh re-derivations

P1: “linux” in the no-kernel-change sentence means the exact package `linux`, not a prefix: `linux-api-headers` 7.2→7.3 is pending. The boot-related pending set also includes `systemd-libs`, `systemd-sysvcompat` and `lib32-systemd`; “two packages” above was shorthand for the systemd and limine update families, not an exhaustive dependency inventory. The 134-row file is a fresh temporary-database download, not a copy of the local databases. RevP1Pending reran it at 09:06 UTC and obtained identical bytes; local third-party target versions were already stale relative to that file.

P2: cleared means only 0 installed-newer rows among 1378 sync-covered packages of 1399 installed; 21 foreign packages have no matching sync entry. It does not certify absence of dependency, integrity or ABI problems. The recent refresh rewrote only the two third-party databases, while the historical 2026-10-18 post-sync window for core/extra/multilib was closed by the 2026-10-20 full upgrade. A missing `/etc/cryptsetup-keys.d/` directory was separately reported by RevP2Residue; cause and boot relevance remain unknown and it is not claimed repaired here.

P5: “outside the fleet repo” refers to the eight removal commands, not every journal row; a later inside-fleet dry-run is harmless and separate. The five foreign packages were installed from yay-cache files; their build process is unobserved, so “locally built” was inference, not observation. The Archive rollback observation covers Arch-repository packages, not the Omarchy-specific limine hook and snapper-sync packages, whose older bytes need a snapshot or rebuild. Existing image/menu consistency is not proof that a snapshot restore can boot.

### Final P3 verdict — unverified, not counted

RevP3Hooks falsified the combined premise's `changed` verdict. The Plymouth mechanism is supported as an inference from an ordinary boot; the btrfs-overlayfs read-only snapshot branch remains untested. A namespace probe does not establish that boot path. P3 is therefore **unverified**, superseding the P3 word in the earlier sections and summary table. The original after-target remains 5; the checker now counts **4**, so C2 misses its target honestly.

LoaderEntrySelected records Limine's chosen entry, not an independent firmware attestation. PID order and Plymouth reaching its post-switch-root filesystem are inferences; `/var/log` is the @log subvolume. Journal kernel timestamps are receipt timestamps, so line 328 is cited for mount PID 942, not exact mount timing. Snapshot-boot Plymouth writes after an overlay move are a prediction, not an observed failure. MR !482 explicitly says the change affects third-party hooks and only tries to avoid issues; the compatibility symlink alone does not clear the snapshot boot risk.
