source: round-24 L1 read-only capture `.ufo/waves/round-24/capture/l1-4/capture.txt` (taken 2026-10-22T08:46:28Z; `capture.txt:3`), pinned by `tools/check-pause-gate.py` (`CAPTURE`, `:36`); sha256 `87f70f82f05956ce5de60abe8bfdd748f38d716483a491cfe7c183939884a56f`; SOURCES rows opened 2026-10-22 listed per premise below (placeholder ids `S0NN-<topic>`; the L1 assigns numbers).
verified-at: 2026-10-22
recheck: before the next pause-lift decision, whenever a pacman transaction, sync or reboot occurs, or after the stable mirror publishes a new snapshot; procedure: run `bash .ufo/waves/round-24/capture/capture.sh <new-dir>`, then `python3 tools/check-pause-gate.py --revision <REV>` after the L1 integrates this gate file and the l1-4 capture. Read-only; no package-manager write.

# Pause-lift update-safety gate — round 24

The host-wide pacman pause started on 2026-10-20 after a lane ran a partial upgrade
(`.ufo/l0-questions.md` lines 54-55). This entry gives each of the five pause
premises a dated verdict from one committed read-only L1 capture and sources opened
on 2026-10-22. It is evidence for the operator's decision, not permission to lift
the pause, and it authorizes no lane to run a transaction.

Verdict words: **cleared** (the premise no longer holds), **still-holds**,
**changed** (the premise holds in a different form), **unverified** (no read-only
evidence can decide it).

All capture citations below use `capture.txt:<line>` numbering of the pinned
committed file `.ufo/waves/round-24/capture/l1-4/capture.txt`; every cited line
exists in that file and contains the cited substring.

## P1 — pending upgrades (the corpus says 413)

- [obs] `pacman -Qu` against the host's local sync DBs lists exactly 3 packages: `1password-beta`, `chatgpt-bin`, `claude-code` — `capture.txt:40-42`; the count is `3` — `capture.txt:47`.
- [obs] Those local sync DBs are stale: core/extra/multilib carry mtimes 2026-10-17 22:37 -03 (`capture.txt:31-33`).
- [obs] The same capture's `checkupdates` against freshly synced temporary metadata reports `checkupdates exit=0 rows=134` — `capture.txt:374` — including `limine 12.9.3-1 -> 12.9.4-1` (`capture.txt:375`) and `systemd 262-1 -> 262.1-1` (`capture.txt:376`).
- [obs] The three pending packages' repositories are `omarchy`, `openai-chatgpt` and `omarchy` — `capture.txt:52-54`; none is a boot-chain package (boot-chain versions match installed, `capture.txt:63`, `capture.txt:73`, `capture.txt:79`, `capture.txt:88`).
- [inf] The 413-row figure of 2026-10-20T07:44Z (`corpus/knowledge/partial-upgrade-recheck-r15.md`) was discharged by the operator's full upgrade at 2026-10-20 09:15 -03. `pacman -Qu` compares versions against the local sync database only and does not check replacements (pacman(8) `-Q`/`-u`, SOURCES row opened 2026-10-22), so 3 is the version-pending count against stale metadata, not the upstream delta.
- Verdict: **changed** — the pending-upgrade count is no longer 413 and no longer simply 3: 3 against the stale 2026-10-17 sync DBs, 134 against freshly synced temporary metadata (checkupdates).
- Falsifier: a re-capture changing either number (pending rows against the sync DBs, or `checkupdates` rows against fresh metadata).

## P2 — partial-upgrade residue

- [obs] No installed package is newer than its sync-database version: the `local-newer-than-sync` probe prints nothing between its command and `exit=0` — `capture.txt:57-59`.
- [obs] `libinput 1.32.0-1` is installed and is also the sync version — `capture.txt:73`, `capture.txt:88`.
- [inf] The libinput partial upgrade of 2026-10-20 04:25 -03 is now consistent with the sync database because the later full upgrade reached the same version. A `pacman -Sy --noconfirm` ran on 2026-10-21 20:32 -03 without `-u` (`capture.txt:221`); because core and extra kept their 2026-10-17 mtimes (P4), that refresh changed no core or extra target, but any later `pacman -S <pkg>` is still a partial-upgrade pattern by Arch doctrine (ArchWiki System maintenance, SOURCES row opened 2026-10-22).
- Verdict: **cleared** (no residue observed); the `-Sy` pattern is recorded under P5.
- Falsifier: a re-capture where `local-newer-than-sync` prints any row.

## P3 — mkinitcpio 42 hooks that still name `/new_root`

- [obs] mkinitcpio 42.2-1 is installed (`capture.txt:63`); busybox init mounts root at `/sysroot` (`capture.txt:106-107`, `capture.txt:112`).
- [obs] The configured late hooks still name `/new_root`: `btrfs-overlayfs:4` and `plymouth:11` (`capture.txt:93-94`); the omarchy hooks config includes both `plymouth` and `btrfs-overlayfs` (`capture.txt:100`).
- [obs] mkinitcpio's build root creates `new_root` as a relative symlink to `sysroot` (`/usr/lib/initcpio/functions:1213`, `capture.txt:117`); round 17 typed that symlink inside every 42.2 image.
- [obs] Two boots on 42.2 images completed: boot -1 from 2026-10-20 09:57 -03 and boot 0 from 2026-10-22 04:55 -03 (`capture.txt:15-16`); Plymouth started (`capture.txt:139`, `capture.txt:152`), received SIGRTMIN+20 (`capture.txt:142`, `capture.txt:155`), and finished terminate (`capture.txt:146`, `capture.txt:159`) in both.
- [unk] A read-only snapshot boot — the only path where `btrfs-overlayfs` acts — has not been exercised on a 42.2 image. Whether `findmnt --mountpoint /new_root` resolves through the symlink inside the initramfs is decided only by such a boot.
- Verdict: **changed** — no longer a pending-upgrade risk; ordinary boots work; the snapshot-boot path stays unverified.
- Falsifier: a boot after 2026-10-22 on a 42.2 image failing at switch-root, or a snapshot boot that cannot resolve `/new_root`.

## P4 — sync database freshness and the upgrade target

- [obs] core, extra and multilib all `Include` `/etc/pacman.d/mirrorlist` (`capture.txt:201`, `capture.txt:203`, `capture.txt:205`), and that mirrorlist has one server: `https://stable-mirror.omarchy.org/$repo/os/$arch` (`capture.txt:194`). The `omarchy` repo points at `https://pkgs.omarchy.org/stable/$arch` (`capture.txt:207`) and openai-chatgpt is an include (`capture.txt:208`).
- [obs] The core, extra and multilib database files carry mtimes 2026-10-17 22:37 -03 (`capture.txt:31-33`) although `pacman -Sy --noconfirm` ran on 2026-10-21 20:32 -03 (`capture.txt:221`, sync marker `capture.txt:133`).
- [obs] The stable mirror's server-side `core.db` Last-Modified is `Thu, 22 Oct 2026 04:40:03 GMT` (`capture.txt:363`), newer than the host file's mtime.
- [inf] The upgrade target of a full upgrade on this host is the omarchy stable mirror's snapshot, not the current Arch repositories; the host database mtimes record an older snapshot's age, and the server's newer Last-Modified explains why a successful `pacman -Sy` did not rewrite the local files unless served data changed (libalpm `dload.c`, SOURCES row opened 2026-10-22).
- Verdict: **changed** — "the sync database is far ahead of the host" is false today; the gap is set by the omarchy snapshot cadence.
- Falsifier: the stable mirror's `core.db` Last-Modified equalling the host file's mtime, or a core/extra/multilib mtime newer than 2026-10-17 22:37.

## P5 — rollback by package cache, and package transactions during the pause

- [obs] `/var/cache/pacman/pkg` holds no package files: `cache-package-files` prints `0` (`capture.txt:284-287`) and `cache-entries` prints `total 0` (`capture.txt:289-292`); the earlier `cache-file-count` of 4 (`capture.txt:226-229`) counts directory entries (download staging dirs), not package files.
- [obs] The sudo journal records `paccache -rk1` and `paccache -ruk0` at 2026-10-22 04:09 -03 and `pacman -Scc --noconfirm` and `pacman -Scc` at 04:10 (`capture.txt:268-271`), all under account `vgpnk` with PWD mostly outside the fleet repo (one `inside-fleet-repo` paccache -d -k1 at 05:41, `capture.txt:272`).
- [obs] During the pause the pacman log records five `[ALPM] installed` lines after 2026-10-20T09:40: `zcode`, `tizen-sdb`, `tizen-sdb-debug`, `openssl-1.0`, `openssl-1.0-debug` (`capture.txt:121-126`); all five are foreign packages (`capture.txt:277-281`) and were installed by `pacman -U` from locally built package files (`capture.txt:213`, `capture.txt:215`, `capture.txt:218`).
- [inf] The libinput 1.31.3 cache file named as a revert option in the L0 question is gone; rollback by cache is unavailable because no package files remain. Remaining rollback paths are the Arch Linux Archive and Snapper snapshots; the capture records snapper as `No permissions.` (`capture.txt:312`) and `snap-pac` not installed (`capture.txt:317`).
- Verdict: **changed** — the pause held for lanes' repository upgrades but not for operator-side local installs, a refresh and a cache clean that emptied the package cache.
- Falsifier: a re-capture showing any package file in the cache, a cache count other than 0/4 as described, or the cited log/sudo lines absent.

## Gate summary for the operator

| Premise | Verdict | What it means for lifting the pause |
|---|---|---|
| P1 | changed | 3 pending against stale sync DBs, 134 against fresh metadata; none in the boot chain. |
| P2 | cleared | No partial-upgrade residue; the libinput incident is reconciled. |
| P3 | changed | Ordinary boots on 42.2 images work; a snapshot boot is untested. |
| P4 | changed | The target is the omarchy stable snapshot; the next snapshot advance brings the real core/extra delta. |
| P5 | changed | The package cache holds no package files; keep a Snapper pre-snapshot or the Archive as the fallback. |

## Sources (opened 2026-10-22; placeholder ids — the L1 assigns numbers)

- P1: `S0NN-pacman-query` (pacman(8) `-Q`/`-u` semantics), `S0NN-archwiki-maintenance` (ArchWiki System maintenance, partial-upgrade doctrine), `S0NN-checkupdates` (checkupdates temp-DB mechanism).
- P2: `S0NN-archwiki-maintenance` (partial-upgrade doctrine), `S0NN-pacman-vercmp` (vercmp semantics).
- P3: `S0NN-mkinitcpio-functions` (v42.2 `functions` line 1213 symlink), `S0NN-plymouth-rootfs` (plymouth `update-root-fs`), `S0NN-arch-news-v42` (v42 release notes).
- P4: `S0NN-pacman-dload` (libalpm `dload.c` Last-Modified/If-Modified-Since), `S0NN-omarchy-mirror` (stable mirror list and headers).
- P5: `S0NN-paccache` (paccache(8)), `S0NN-pacman-sc` (pacman(8) `-Sc`/`-Scc`), `S0NN-ala` (Arch Linux Archive).

## Supersedes

- `corpus/knowledge/partial-upgrade-recheck-r15.md`: the "413 pending" table row is historical as of 2026-10-20 09:15 -03; this gate replaces it as the current-use pending-upgrade statement.
- `corpus/README.md` `## Frontier` (line 38): "Pending `mkinitcpio` 42 upgrade strands two `/new_root` hooks" — the upgrade is installed; ordinary boots work; see P3. This gate supersedes that Frontier statement for the host.

## Limits

- `pacman -Qu` compares installed packages against the local sync DB (stale, 2026-10-17); `checkupdates` rows=134 measure the delta against a freshly synced temporary DB, so the true upstream delta is ~134, not 3.
- No running-process mapping, `-Qkk` integrity check, journal/UI health probe, or snapshot-boot test was made; no boot-path verdict beyond the two completed boots is possible.
- Cache numbers are counts only; the cache holds no package files (0), and the four counted directory entries are download staging dirs.
- The gate links committed capture bytes and SOURCES rows; it is not a host re-measurement and not pause-lift clearance.
