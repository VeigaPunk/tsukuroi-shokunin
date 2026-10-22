P1 verdict "changed" and its limits text (corpus/knowledge/pause-lift-gate-r24.json:48; corpus/knowledge/pause-lift-gate-r24.md:19-25): the verdict survives; the limits text survives with defects. No finding changes the verdict.

# RevP1Pending: premise P1 re-derivation (round 24, wave 2)

Seat: TsukuroiR24.RevP1Pending (leaf reviewer). Target: premise P1 only.

## Method

- Ran `checkupdates` myself with `CHECKUPDATES_DB=/fast/scratch/hyaku/tsuku24w2-RevP1Pending/db` at 2026-10-22 09:06Z. Exit 0, 134 rows, empty stderr. Its internal refresh touched only the temporary database. The output is byte-identical to the capture `.ufo/waves/round-24/capture/l1-4/checkupdates.out` (sha256 `0a33e3e4a7dae15910e4f914089bb3d7259e16e177da433cfbecc2ca9cfccee7`, both files). Copy: `w2/RevP1Pending/checkupdates-fresh-0906Z.out`.
- Recomputed the pending sets from the raw sync databases and the 1,399 installed package records, using `vercmp`. Host databases give 3 rows, the same as `pacman -Qu` (exit 0). Temporary databases give 134 rows with identical names and versions to checkupdates. Output: `w2/RevP1Pending/p1-recompute.json`.
- Compared the temporary databases with the bytes the mirrors serve now. `core.db`, `extra.db` and `omarchy.db` are byte-identical to the served files (sha256 prefixes `7015ab85`, `6fe33bbb`, `5806e652`). So the 134 rows describe the currently served core, extra and omarchy repositories. multilib and openai-chatgpt were not byte-compared.
- Read the 2026-10-20 transaction in `/var/log/pacman.log`, the S088 notice, the Arch news feed and archive, and the local pacman(8) page.
- No package transaction, sync, cache write or host configuration write was run. The host databases, cache directory and sync file change times were unchanged after my run.

## Re-derived rows

### The 3 local rows (host sync databases)

| Package | Installed | Target in host DB (`pacman -Qu`) | Target in fresh temporary DB | Repository | checkupdates line |
|---|---|---|---|---|---|
| 1password-beta | 8.12.42_34.BETA-1 | 8.12.44_25.BETA-1 | 8.12.44_25.BETA-1 (same) | omarchy | :1 |
| chatgpt-bin | 26.1013.40934-1 | 26.1016.51333-1 | 26.1016.61520-1 (moved) | openai-chatgpt | :7 |
| claude-code | 2.1.304-1 | 2.1.307-1 | 2.1.308-1 (moved) | omarchy | :10 |
| 1password-cli (not in local `-Qu`) | 2.41.0-1 | none | 2.41.1-1 | omarchy | :2 |

The host omarchy database was downloaded on 2026-10-21 (file mtime 19:44 -03). That is before the omarchy repository's 2026-10-22 08:07:53Z publish, so `pacman -Qu` cannot see 1password-cli.

### The 134 rows by source (fresh temporary databases)

- Stable mirror: 130 rows (core 13, extra 114, multilib 3).
- omarchy repository: 3 rows (1password-beta, 1password-cli, claude-code).
- openai-chatgpt repository: 1 row (chatgpt-bin).

### Boot-chain, kernel and security rows

| Package | Installed | Fresh DB | Pending | checkupdates line |
|---|---|---|---|---|
| limine | 12.9.3-1 | 12.9.4-1 (extra) | yes | :97 |
| systemd | 262-1 | 262.1-1 (core) | yes | :127 |
| systemd-libs | 262-1 | 262.1-1 (core) | yes | :128 |
| systemd-sysvcompat | 262-1 | 262.1-1 (core) | yes | :129 |
| lib32-systemd | 262-1 | 262.1-1 (multilib) | yes | :76 |
| linux-api-headers | 7.2-1 | 7.3-1 (core; userspace kernel headers) | yes | :98 |
| ca-certificates-mozilla | 3.131-1 | 3.131.1-1 (core) | yes | :6 |
| nss | 3.131-1 | 3.131.1-1 (core) | yes | :106 |
| lib32-nss | 3.131-1 | 3.131.1-1 (multilib) | yes | :75 |
| mkinitcpio | 42.2-1 | 42.2-1 | no | none |
| linux | 7.2.11.arch1-1 | 7.2.11.arch1-1 | no | none |
| linux-lts | 6.18.57-2 | 6.18.57-2 | no | none |
| plymouth | 26.134.222-3 | 26.134.222-3 | no | none |
| nvidia-open-dkms, nvidia-utils | 615.78.08-1 | 615.78.08-1 | no | none |
| linux-firmware | 20260916-1 | 20260916-1 | no | none |
| limine-mkinitcpio-hook, limine-snapper-sync | 1.40.0-2, 1.32.1-2 | same | no | none |
| snapper, btrfs-progs, cryptsetup, glibc, pacman, dkms, libinput | as installed | same | no | none |

Line numbers refer to `.ufo/waves/round-24/capture/l1-4/checkupdates.out`, which my fresh output matches byte for byte.

### ca-certificates-mozilla

- Installed version: 3.131-1 (`pacman -Q`, exit 0). It was upgraded from 3.128-1 at 2026-10-20 09:16:28 (`/var/log/pacman.log:2499`).
- The fresh core database offers 3.131.1-1 (`checkupdates.out:6`).
- Notice S088, published 2026-10-21: "The compromised certificates have been removed/invalidated with ca-certificates-mozilla ≥ 3.131.1-1." (`w2/RevP1Pending/s088-article.html` lines 62-63; publish date lines 46-48). The fix is not installed.

## Findings

Severity: medium means a checker or an operator could be misled. Low means precision. Info means a note for another premise owner or a verified item.

1. [obs, medium] The limits text says "No mkinitcpio, linux or plymouth change is pending" (JSON :48). The falsifier says "a mkinitcpio, linux or plymouth row" (md :72). Read literally, both are wrong. `linux-api-headers 7.2-1 -> 7.3-1` is pending (`checkupdates.out:98`). It is the userspace kernel headers package. The kernel `linux` and `linux-lts` are not pending.
   Correction: JSON :48 becomes "No mkinitcpio, linux, linux-lts or plymouth package is pending; linux-api-headers 7.2-1 -> 7.3-1 (userspace kernel headers, not the kernel) is pending." md :72 becomes "P1 falls if a fresh temporary-database check lists mkinitcpio, linux, linux-lts or plymouth, or if ca-certificates-mozilla 3.131.1-1 or later is installed."

2. [obs, medium] "Against the current omarchy stable snapshot … lists 134 rows" (md :22) and "against the current stable mirror snapshot … 134 rows" (JSON :48) name one source. The 134 come from three: 130 from the stable mirror, 3 from the omarchy repository and 1 from openai-chatgpt. The fresh temporary database gives 134, which is right. The source label is not. Four rows come from third-party repositories with their own publish times: omarchy 2026-10-22 08:07:53Z, openai-chatgpt 2026-10-22 01:18:17Z, and the stable mirror core and extra 2026-10-22 04:40:03Z and 04:40:04Z (temporary-database file times).
   Correction: md :22 and JSON :48 become "against the repositories as served now (checkupdates temporary database; host databases untouched) 134 rows are pending: 130 from the stable mirror (core 13, extra 114, multilib 3), 3 from the omarchy repository and 1 from openai-chatgpt."

3. [obs, medium] The boot chain is under-listed. The systemd family has four pending rows: systemd, systemd-libs, systemd-sysvcompat and lib32-systemd (`checkupdates.out:127`, `:128`, `:129`, `:76`). md :25 says "including two boot-chain packages". The gate does not define "boot chain". apparmor 4.1.7-1 -> 4.1.8-2 (`:3`) and dbus 1.16.2-1 -> 1.16.2-2 (`:12`) are also pending. They look like early-boot services [inf], but the gate's list does not mention them [unk].
   Correction: md :22 and :25 become "limine 12.9.4 and the systemd 262.1 family (systemd, systemd-libs, systemd-sysvcompat, lib32-systemd)". Add one sentence that defines boot chain (bootloader, initramfs generator, kernel, plymouth, init) and says whether apparmor and dbus are in or out.

4. [obs, low] The 413 discharge is observed, not inferred. md :24 marks it "[inf]" and cites round-17 notices. `/var/log/pacman.log` lines 2464 ("starting full system upgrade", 2026-10-20T09:15:31) to 2941 ("transaction completed", 09:16:47) contain 413 "upgraded" and 35 "installed" actions. The four deltas in the round-15 record appear there: systemd 261.2-1 -> 262-1 (`:2531`), mkinitcpio 41.1-1 -> 42.2-1 (`:2539`), linux 7.2.3.arch1-3 -> 7.2.11.arch1-1 (`:2855`) and plymouth 26.134.222-2 -> 26.134.222-3 (`:2898`). The round-15 record lists those deltas (`corpus/knowledge/partial-upgrade-recheck-r15.json:23`) and was taken at 2026-10-20T07:44:39Z.
   Correction: md :24 becomes "[obs] The 09:15:31 full upgrade (pacman.log:2464-2941) applied 413 upgrades and 35 installs, the same 413 that the 07:44:39Z record counted." Keep JSON :48 as written. `tools/check-pause-gate.py` anchors evidence only to the pinned capture (lines 92-126), so the pacman.log citation belongs in the markdown only.

5. [obs and inf, low] md :24 says "the operator's full upgrade". The journal shows a `pacman -Syu --needed --noconfirm …` record at 2026-10-20 09:15:30, run through sudo by account vgpnk, with a working directory outside the fleet repo. Command: `journalctl _COMM=sudo --since "2026-10-20 09:15:29" --until "2026-10-20 09:15:31"`, exit 0 (path not copied). "Operator" is an inference.
   Correction: "the full upgrade that account vgpnk ran through sudo at 09:15:30 (working directory outside the fleet repo)."

6. [obs, low] md :21 is right that three rows are pending locally. Two of those targets are stale against the fresh database: chatgpt-bin (26.1016.51333-1 locally, 26.1016.61520-1 fresh) and claude-code (2.1.307-1 locally, 2.1.308-1 fresh). 1password-cli 2.41.0-1 -> 2.41.1-1 is pending only in the fresh omarchy database, so the local count misses one third-party row.
   Correction: md :21 gains "Two of these three targets are older than the fresh database (chatgpt-bin 26.1016.61520-1, claude-code 2.1.308-1), and 1password-cli 2.41.1-1 is pending only there."

7. [inf, low] The summary row "A full upgrade now moves 134 packages" (md :64) and the caveat "-Qu does not check replacements" (JSON :48, md :24). A database check supports the count on this host. No changed package adds a dependency (0 added, 0 unresolved). No changed package conflicts with an installed one (0). The sync databases hold 32 replacement entries that name installed packages, and none applies because the version constraint fails. Example: xdg-desktop-portal-gnome 51.0-1 REPLACES xdg-desktop-portal-gtk<1.10.0-2, and 1.15.3-1 is installed. This is a database approximation, not a pacman simulation, because the host guard forbids `-S`.
   Correction: keep "134 packages" but write "134 same-name upgrades; a database check found no added dependencies, conflicts or applicable replacements." Keep the `-Qu` caveat and add "(none applies on this host today)".

8. [obs, low, for the P4 owner] The mirror's `lastsync` value 1792636269 is 2026-10-22T02:31:09Z (`date -u -d @1792636269`; `capture.txt:366`). core.db Last-Modified is 04:40:03 GMT (`capture.txt:363`; my HEAD request agrees). P4's "published a new snapshot at 04:40 UTC" (md :47-48) does not mention the earlier lastsync value. P1 is not affected, because the served bytes match the temporary copy.
   Correction (P4 owner): cite both timestamps and mark the publish time [unk] until they are reconciled.

9. [unk, info] Notice S088 names only ca-certificates-mozilla. nss 3.131-1 -> 3.131.1-1 (`checkupdates.out:106`) and lib32-nss (`:75`) are pending too. Whether the eMudhra removal needs NSS 3.131.1 is not established. The P1 wording "the ca-certificates-mozilla security fix" is accurate as written.
   Correction (optional): JSON :48 gains "nss and lib32-nss 3.131.1-1 are also pending; the notice does not name them."

10. [obs, low] The P1 source list (JSON :43-47: S087, S088, S089) does not cite the mirror measurement that the "current snapshot" claim rests on (`capture.txt:363-366`, S101). It also does not cite the mtime semantics that the publish times above depend on (S099).
    Correction: add S099 and S101 to the P1 sources.
11. [obs, low] md :22 calls the source "a temporary database copy under /fast/scratch". `checkupdates` does not copy the host databases. It downloads fresh sync databases into the temporary directory. The temporary files' birth times are the 2026-10-22 06:06 -03 run (my `stat`), and their mtimes are the mirror's Last-Modified times, so they are fresh downloads.
    Correction: md :22 reads "a temporary database refreshed from the mirrors under /fast/scratch". The JSON limit at :48 already says "checkupdates temporary database" and needs no change.

## Checks that pass as written

- Verdict "changed". It survives. The 413 form is discharged by an observed transaction (finding 4), and the host's local database now shows three third-party rows. The snapshot form is not cleared: 134 same-name upgrades remain, including limine, the systemd family and the CA fix. "still-holds" would hide the discharge. "cleared" would ignore the 134 rows. "changed" matches the gate's own definition (the premise holds in a different form, or partly).
- The 3 local rows: `pacman -Qu` (exit 0) and the raw host database agree on the same three rows. Targets are covered in finding 6.
- The 134 rows: checkupdates is identical to the capture, the raw-database recompute is identical, and the served core, extra and omarchy databases are byte-identical to the temporary copies.
- Boot-chain rows: limine 12.9.3-1 -> 12.9.4-1 and systemd 262-1 -> 262.1-1 are real (`capture.txt:375-376`). mkinitcpio, linux, linux-lts, plymouth, nvidia-open-dkms, nvidia-utils, linux-firmware, limine-mkinitcpio-hook, limine-snapper-sync, snapper, btrfs-progs, cryptsetup, glibc, pacman, dkms and libinput are at their sync versions.
- ca-certificates-mozilla row: real (`checkupdates.out:6`). The notice text matches S088 (`corpus/SOURCES.md:94`).
- S089 quote: the local pacman(8) page (pacman 7.1.0) says "Only package versions are used to find outdated packages; replacements are not checked here." (`corpus/SOURCES.md:95`).
- S087: exactly two October 2026 news items, both dated 2026-10-21 (php and ca-certificates-mozilla). The feed `lastBuildDate` is 2026-10-21 19:29:36 +0000. The archive page (`w2/RevP1Pending/news-index.html`, lines 139 and 148) matches wave 1's saved copy byte for byte (sha256 `e6a75889…`). `pacman -Q php php-legacy` exits 1, so neither is installed.
- Falsifier: not triggered today with exact package names. Finding 1 covers the wording.
- Side check for P2: 21 installed packages have no sync entry (elephant family, openssl-1.0, tizen-sdb, zcode and others). They are outside the 134 count, as P2 says.
- Wave 1 agrees on the 413+35 split (`w1/ConnSiblingOverlap.md:45`) and on the two October items (`w1/SrcArchNews.md`).

## Residual risk

- The count is a snapshot. A later publish from the stable mirror, omarchy or openai-chatgpt changes it. The gate's recheck rule covers this.
- The dependency, conflict and replacement checks are database approximations. Optional dependencies and file conflicts were not checked.
- multilib and openai-chatgpt served bytes were not byte-compared.
- The boot-chain list depends on a definition the gate does not give (finding 3).
- The news feed is dated 2026-10-21 19:29:36Z. The archive page was fetched at about 09:10Z on 2026-10-22, and no later item appeared.

## Verification gaps

- Did not run `tools/check-pause-gate.py`, which is outside P1.
- Did not read the openai-chatgpt repository's served bytes. Its server address is in host configuration, and I kept it out of this report.
- Who ran the sudo commands is known only by account and working-directory class.

Scope: read=corpus/knowledge/pause-lift-gate-r24.md and .json; .ufo/waves/round-24/capture/l1-4/capture.txt, checkupdates.out and capture.sha256; capture.sh; corpus/SOURCES.md rows S087-S103; corpus/knowledge/partial-upgrade-recheck-r15.md and .json (413 origin); tools/check-pause-gate.py (anchor rules, by search); /etc/pacman.conf (ignore and hold directives only); /var/log/pacman.log lines 2455-2941 plus its line count; local package and sync databases (read-only); wave-1 reports (search only); public URLs (S088 article, Arch news feed and archive, mirror headers, served core, extra and omarchy databases); local pacman(8) page; wrote=/fast/scratch/hyaku/tsuku24w2-RevP1Pending/ (db/, checkupdates.out and .err, served-core-now.db, served-extra-now.db, served-omarchy-now.db, news-index.html, news-feed.xml, s088-article.html, p1-recompute.json, p1-replacements.json, p1-depclosure.json, p1-conflicts.json), .ufo/waves/round-24/w2/RevP1Pending/ (checkupdates-fresh-0906Z.out and .err, news-feed.xml, news-index.html, s088-article.html, p1-recompute.json, p1-replacements.json, p1-depclosure.json, p1-conflicts.json), and this report at .ufo/waves/round-24/w2/RevP1Pending.md; executed=checkupdates with CHECKUPDATES_DB under /fast/scratch; pacman -Qu; pacman -Q (boot-chain, CA, NSS, php); pacman -V; journalctl _COMM=sudo (read-only window); stat; sha256sum; diff; cp; ls; date; curl (HEAD and GET of public URLs); python3 (reads of local and temporary databases with zstd and vercmp; reads of pacman.log and the pacman(8) page).
Installs: none.
