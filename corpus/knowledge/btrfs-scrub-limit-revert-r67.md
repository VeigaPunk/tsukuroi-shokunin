source: S284 S285 — btrfs-progs v7.3 `cmds/scrub.c` (https://github.com/kdave/btrfs-progs/blob/v7.3/cmds/scrub.c; anchor: tag v7.3, peeled commit afdc3a65e33f4d42f768ad50dca20c32e5ee1496, `cmds/scrub.c` lines 1640-1649) and btrfs-progs v7.3 `CHANGES` (https://github.com/kdave/btrfs-progs/blob/v7.3/CHANGES; anchor: the `scrub limit` bullet at line 20 under the release header `btrfs-progs-7.3 (2026-10-23)` at line 1); the v7.1 comparison copy is the round-42 frozen `scrub.c` pinned by S237 (`.ufo/waves/round-42/frozen/src/scrub.c`, sha256 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801); host readings are own-work probes under `.ufo/waves/round-67/probes/e1-*`
verified-at: 2026-11-03 (pinned bytes: `.ufo/waves/round-67/before/src/SHA256SUMS`, re-verified by the round-67 scout seat against live raw.githubusercontent.com bytes; host capture 2026-11-03 21:50 UTC)
recheck: on-release — `sha256sum -c SHA256SUMS` inside `.ufo/waves/round-67/before/src/` must print `scrub.c: OK` and `CHANGES: OK`; `grep -n 'Revert to the older scrub limits' .ufo/waves/round-67/before/src/scrub.c` must return one hit, at line 1640; `grep -n 'set to the original limit only after all devices finish' .ufo/waves/round-67/before/src/CHANGES` must return one hit, at line 20.

# The btrfs scrub limit is restored after all devices finish, not inside the device loop (round 67)

Scope: the storage-integrity frontier, scrub throughput limit (`PROVINCE.md` Frontier; the scrub record and `scrub_speed_max` plane held by `corpus/knowledge/btrfs-scrub-record-r42.md` and `corpus/knowledge/btrfs-scrub-record-r43.md`). This entry holds one fact the lane did not hold: **when** btrfs-progs puts the per-device scrub throughput limit back. Nothing here runs a scrub, writes `/var/lib/btrfs`, sets a scrub limit or enables a timer.

| row | claim | evidence |
|---|---|---|
| SL1 | In btrfs-progs v7.3 the per-device scrub throughput limit is restored only after every device has finished: the reset is its own loop after the per-device result loop, not inside it. | v7.3 `cmds/scrub.c` (function `scrub_start`, from line 1233): `/* Revert to the older scrub limits. */` at :1640 heads a second `for (i = 0; i < fi_args.num_devices; ++i)` at :1641 whose body calls `write_scrub_device_limit(fdmnt, di_args[i].devid, sp[i].old_limit)` at :1642 and warns `failed to reset scrub throughput limit on devid %llu: %m` at :1645-1646; the loop closes at :1648. The per-device result loop it follows closes at :1638; its `pthread_join(t_devs[i], NULL)` is at :1600. Scout-verified (`.ufo/waves/round-67/drafts/S1Scout-verify.md`, rows 234-236). |
| SL2 | In btrfs-progs v7.1 the same reset ran inside the per-device loop, first thing in each iteration and before that device's own `pthread_join`, so a device's limit could be put back before that device's scrub thread had been joined [inference from the loop order; no run]. | v7.1 frozen `cmds/scrub.c` (sha256 48df2e2f…, pinned by S237): the per-device loop header at :1596; its first statement is `/* Revert to the older scrub limit. */` at :1597, then `write_scrub_device_limit(fdmnt, di_args[i].devid, sp[i].old_limit)` at :1598; the warning `failed to reset scrub throughput limit on devid %llu: %m` at :1601-1602; then `if (sp[i].skip)` at :1605 and `pthread_join(t_devs[i], NULL)` at :1608. Scout-verified rows 237-238 (range 1596-1604 for the in-loop reset). |
| SL3 | The v7.3 release note states the change in one line: the original limit is set back only after all devices finish. | v7.3 `CHANGES` line 20: `   * scrub limit: set to the original limit only after all devices finish`, the bullet of the `btrfs-progs-7.3 (2026-10-23)` entry whose header is at line 1 (pinned sha256 5046bac1def81247a02d7442807a6d495de2caafbc1a7194637ef03ea958a249, S285). |
| SL4 | On this host the reordering is inert: one btrfs filesystem with a single device, that device's `scrub_speed_max` is 0 (no limit), and no scrub timer is enabled, so v7.3's ordering cannot change any scrub here. | own-work probe receipts `.ufo/waves/round-67/probes/e1-*` (capture 2026-11-03, unprivileged): `btrfs filesystem show` reports `Total devices 1` with `devid 1` (`e1-g2-filesystems.txt`); `cat /sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/scrub_speed_max` reads `0` (`e1-g3-sysfs-limits.txt`); `systemctl is-enabled 'btrfs-scrub@-.timer'` reads `disabled` and `list-timers` shows no scrub timer (`e1-g4-records-timers.txt`); `/var/lib/btrfs` is not listed; `btrfs scrub status /` reports `no stats available` and no running scrub (`e1-g5-scrub-status.txt`). |

## Watch

QUALITY 98 (R65-UPSTREAM-WATCH) requires a pinned upstream version to be re-read when its release trigger fires, and the fired re-read to be logged. The trigger has fired: S237 and S238, which back the round-42 and round-43 notes, pin btrfs-progs v7.1 with `recheck: on-release`, and the v7.3 `CHANGES` header dates the 7.3 release 2026-10-23 (line 1). This section is that logged re-read of the pinned v7.1 bytes against the v7.3 bytes.

`diff -u` of the two pinned `scrub.c` copies has four hunks (measured 2026-11-03, `.ufo/waves/round-67/drafts/S1Scout-verify.md`):

- `@@ -568,7 +568,7 @@` — typo fix in a warning string (`pos` becomes `position`). No behaviour.
- `@@ -1372,7 +1372,7 @@` — comment rewording (`ie.` becomes `i.e.`). No behaviour.
- `@@ -1594,14 +1594,6 @@` — removes the in-loop reset (v7.1 :1597-1604).
- `@@ -1645,6 +1637,16 @@` — adds the post-loop reset (v7.3 :1640-1649).

Only the last two hunks change behaviour. Consequences for the lane's existing notes: the hunks before line 1594 leave every line at its v7.1 position, so the lines the r42 and r43 notes cite in that range are unchanged in both text and number — including `limit = 0;` at `scrub.c:1218`, which is the line behind the round-42 statement that a failed `scrub_speed_max` read is reported as 0. `grep -c -i 'revert\|old_limit'` returns 0 for `btrfs-scrub-record-r42.md` and for `btrfs-scrub-record-r43.md`: neither note states when the limit is restored, so no existing statement is contradicted or stale; the reset timing is a new fact that belongs to neither note's scope.

## Limits

- The v7.3 claims are source-level statements about the btrfs-progs v7.3 tag alone. The host runs btrfs-progs 7.1-1, so the ordering this host executes is the v7.1 in-loop reset until the userspace is upgraded (operator-owned).
- Anchor coverage: S284's registered anchor is `cmds/scrub.c` lines 1640-1649. SL1 also cites v7.3 lines 1600, 1638 and 1233 (function header) outside that range; S237's registered ranges do not cover v7.1 lines 1596-1608 cited by SL2. CORPUS.md rule 2 forbids editing a registered anchor in place, so these citations rest on the same pinned bytes (sha256 match recorded above) and are named here rather than absorbed into the rows.
- The `MISSING` token in `btrfs filesystem show` (`devid 1 ... /dev/mapper/root MISSING`) is printed under an unprivileged view; the device is mounted and `btrfs scrub status /` resolves the same fsid. It is not read as a degraded filesystem.
- Every host reading is an unprivileged read. Nothing was run, written or enabled.

## Unknowns

- Not observable here: a multi-device filesystem with a non-zero `scrub_speed_max` — the only case where the ordering could change a scrub. Inert here is measured (SL4); the effect elsewhere is [inference] from the located lines.
- Whether the Arch btrfs-progs 7.1-1 package carries any downstream patch that already changes the reset timing is [unknown]: the packaging recipe is not reachable from this host, so a backport cannot be excluded by direct inspection.
- The upstream commit inside the v7.3 tag that introduced the reorder is [unknown]; only the tag peel afdc3a65e33f4d42f768ad50dca20c32e5ee1496 is pinned.
