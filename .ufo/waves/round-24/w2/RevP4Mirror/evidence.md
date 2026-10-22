# RevP4Mirror evidence (round 24, wave 2)

Checked 2026-10-22, roughly 09:04 to 09:25 UTC. Host and lane access was read-only. Downloads and a private clone sit in /fast/scratch/hyaku/tsuku24w2-RevP4Mirror/ (outside the fleet repo). No pacman transaction or refresh was run.

## 1. Public mirror headers and markers (curl, UTC)

| Endpoint | Value | Time |
|---|---|---|
| stable core.db | Last-Modified Thu, 22 Oct 2026 04:40:03 GMT; ETag 6e77c7680b16e86a9214b047c2325d53 (equals body MD5) | HEAD 09:04:38Z |
| stable extra.db | Last-Modified 04:40:04 GMT; ETag 8dbc3bdfe0a7860a38d2f39eb7989087 (equals body MD5) | HEAD 09:04:39Z |
| stable multilib.db | Last-Modified 04:40:04 GMT; ETag 812d307cd94480b91e0d1385da7c1491 (equals body MD5) | HEAD 09:04:39Z |
| stable /lastsync | 1792636269 = 2026-10-22T02:31:09Z (unchanged at 09:04Z and 09:11Z) | |
| stable /lastupdate | 1792635447 = 2026-10-22T02:17:27Z | |
| rc-mirror core.db | Last-Modified 02:42:02Z; /lastsync 1792636269 (same as stable) | 09:11Z |
| mirror.omarchy.org (edge) core.db | Last-Modified 05:28:34Z; ETag 6026d499fb811d38dd10cff613d50361; /lastsync 1792657777 = 08:29:37Z; /lastupdate 1792656367 = 08:06:07Z | 09:11Z |
| geo.mirror.pkgbuild.com (official) core.db | Last-Modified 05:18:24Z; ETag "6ad99ca0-2022a" (hex 6ad99ca0 = 2026-10-22T05:18:24Z); body MD5 6026d499fb811d38dd10cff613d50361 (identical to edge) | 09:0x Z |
| official /lastsync, /lastupdate | 1792659793 = 09:03:13Z; 1792659711 = 09:01:51Z | 09:0x Z |

## 2. Conditional GET against stable core.db (HEAD, 09:08Z; equivalent to the libalpm time condition)

- If-Modified-Since Sun, 18 Oct 2026 01:37:29 GMT gives HTTP 200 (content-length 131604).
- If-Modified-Since Thu, 22 Oct 2026 04:40:03 GMT gives HTTP 304.
- If-Modified-Since Thu, 22 Oct 2026 04:40:04 GMT gives HTTP 304.

## 3. Host sync files (stat, re-read at about 09:05Z; unchanged from capture lines 29-36 and 352-358)

| File | Size | mtime (-0300) | birth (-0300) |
|---|---|---|---|
| core.db | 130249 | 2026-10-17 22:37:29.000000000 | 2026-10-18 14:11:00.026135178 |
| extra.db | 8881002 | 2026-10-17 22:37:30.000000000 | 2026-10-18 14:11:00.026135178 |
| multilib.db | 85764 | 2026-10-17 22:37:29.000000000 | 2026-10-18 14:11:00.026135178 |
| omarchy.db | 52786 | 2026-10-21 19:44:39.000000000 | 2026-10-21 20:32:00.056568686 |
| openai-chatgpt.db | 1393 | 2026-10-20 23:22:02.000000000 | 2026-10-21 20:32:00.056568686 |
| openai-chatgpt.db.sig | 566 | 2026-10-20 23:22:02.000000000 | 2026-10-21 20:32:00.282569368 |

The sync directory has mtime and ctime 2026-10-21 20:32:00.482581466 (-0300). pacman 7.1.0.r9.g54d9411-3 is installed (`pacman -Q pacman`, exit 0).

## 4. Content identity (md5sum)

- Host core.db e96d1a0fed34b2245280d39bad1901d8 equals archive repos/2026/10/18/core/os/x86_64/core.db (130249 bytes, archive Last-Modified Sat, 17 Oct 2026 17:36:57 GMT).
- Host multilib.db 8e3bc2efa7344914cabc83014d897778 equals archive 2026/10/18 multilib.db (Last-Modified Sat, 17 Oct 2026 17:37:55 GMT).
- Host extra.db 6ae3ab01dc16504115c2a424578e4c37 (8881002 bytes) matches no archive extra.db for 2026/10/16 to 10/21 by size (8888175, 8881835, 8881048, 8863050, 8867356, 8845240).
- Archive core.db by day: 10/16 0c3d235b..., 10/17 ab49bb23..., 10/19 acb678f7..., 10/20 14e38c50..., 10/21 ca2547ef...; 10/22 returns 404.
- Stable core.db 6e77c7680b16e86a9214b047c2325d53 matches no archive day through 10/21.

## 5. pacman sources (gitlab raw, commit 54d9411; sha256)

- lib/libalpm/dload.c a4c8b6070ce540e7d9ea7f2a39b828141cc828f186e90a723cc8cc94c76449c8 (identical to the wave-1 copy).
- lib/libalpm/util.c 381618b6054859ec76807956328b78b330237273bebe10022a559b243cb5bdd2.
- lib/libalpm/be_sync.c 9219f022a6a96579b9ec009a61715d09b406796dd707a2eb1b22e40c1df2683b.
- lib/libalpm/log.c 1133b633a3bcf16971a77d5cc0bc1ee6a66132c7d4eb6f8812a1e17caf950558.
- lib/libalpm/sync.c 6b297364eaba94e82a1e30b50dde9b3b96f88075855b66ff455aca1e24995d46.
- src/pacman/sync.c af6f1104093c033ae90986d1861649506c8cdcf6031ef1c2138b4d9e0fae78c8; src/pacman/callback.c 9dadcc56465888f4fbd8e6bf69036296359f12ccc15d79f8e367d2506f7c2ce6.
- doc/pacman.8.asciidoc: 595 lines; refresh text at lines 474-479 ("Passing two --refresh or -y flags will force a refresh").

Key lines: dload.c 347-349 (utimes_long, no-op when the time is -1), 387 (CURLOPT_FILETIME), 419-425 (time condition), 607 and 610 (remote time and condition-unmet), 675-681 (not-modified branch), 704 (mtime from remote time), 717-720 (unlink on failure), 792 (fopen of temporary file), 1035-1044 (parent maps child return 1 to 1), 1104-1131 (finalize moves only existing files), 1165-1173 (mtime_existing_file only when the destination exists and is non-empty), 1209 (prepare before fork), 1289-1291 (finalize and temporary directory removal). be_sync.c 139 (alpm_db_update), 156 (temporary directory inside the sync directory), 169 and 208 (force passed through), 199-200 (temporary paths). util.c 959-1003 (download directory created as download-XXXXXX). log.c 101-111 (_alpm_log goes only to the callback). sync.c (frontend) 730-731 and 933-934 (alpm_logaction for "synchronizing package lists"). util.c 527 (scriptlet log). callback.c 1139-1155 (cb_log writes to stderr only).

## 6. Mirror scripts (raw.githubusercontent.com/omacom/omarchy-mirror/master/bin/...; all HTTP 200)

- omarchy-mirror-stage: rsync -rlptH from upstream (line 31), then `date +%s > $STAGE/lastsync` after the rsync (lines 34-35).
- omarchy-mirror-copy-stage: rsync -a --delete FROM TO (line 69), then omarchy-mirror-upload (line 70).
- omarchy-mirror-upload: rclone copy of *.db* and *.files* to R2 (lines 51-54), with lastsync and lastupdate.
- omarchy-mirror-sync-stable-from-rc: "lastsync comes along from rc" (lines 6-7).
- README (S100), line 7 quote, and the ARM section sentence "compared by time against the time R2 received its copy".

## 7. Release feed (https://github.com/omacom/omarchy/releases.atom, read at about 09:10Z)

- v4.0.5 published 2026-10-18T02:51:35Z.
- v4.0.6 published 2026-10-19T22:55:11Z.
- v4.5.0-rc1 published 2026-10-20T21:53:56Z.
- No later entry at the time of reading.

## 8. Gate checker (committed bytes)

- Lane working tree at HEAD 22fd1642e7fa4dfbdfba4419a443f06ffbb0b6c0: `python3 tools/check-pause-gate.py --revision 22fd1642...` exits 2 with {"status": "CANNOT_EVALUATE", "findings": [{"id": "GATE-SELF-BINDING", "site": "working-tree checker differs from the revision blob"}]}.
- `git --no-optional-locks status --short`: M corpus/SOURCES.md, M corpus/knowledge/pause-lift-gate-r24.json, M tools/check-pause-gate.py. Diff stat: 3 files, 46 insertions, 14 deletions. Blob at 22fd1642 is 697c834f...; working tree is e5ec638f....
- Working-tree gate JSON: P4 sources are S099, S100, S101, S114 (committed: S099, S100, S101, S103). Other uncommitted source-list changes: P1, P2, P3, P5, and P5 limits text.
- Clean clone at 22fd1642 (/fast/scratch/hyaku/tsuku24w2-RevP4Mirror/lane): exit 0; status PASS; premises_verified 5 of 5; P4 sources S099, S100, S101, S103; no problems reported (/fast/scratch/hyaku/tsuku24w2-RevP4Mirror/gate-clean-22fd1642.json).

## 9. Host mirrorlist and installer

- sha256 of /etc/pacman.d/mirrorlist and of omarchy v3.8.4 default/pacman/mirrorlist-stable are both 6c4a944bed4bb1c104ed53da8856e5440c22c143511b9989c0e3125697476091 (cmp exit 0).
- Installer v3.8.4 line 3: `sudo cp -f .../default/pacman/mirrorlist-${OMARCHY_MIRROR:-stable} /etc/pacman.d/mirrorlist`.

## 10. Target composition (temporary-database rows, capture checkupdates.out, 134 rows)

- Name match against stable core, extra and multilib downloaded at 09:0x Z: 130 rows.
- Only in the omarchy sync database: 3 rows (1password-beta, 1password-cli, claude-code).
- Only in the openai-chatgpt sync database: 1 row (chatgpt-bin).
- Name-based count from a small python tarfile reader over the stable DBs and the host omarchy.db and openai-chatgpt.db (read-only).

## 11. Not done and not recorded

- No pacman refresh or transaction ran on the host, because the rules forbid it. The not-modified and failure paths were checked by code and by server responses only.
- The 2026-10-21 refresh result (not-modified or failed) is not recorded in any log. libalpm logs download results only to the terminal.
