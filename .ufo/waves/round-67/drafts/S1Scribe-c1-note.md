2026-11-03T22:04:00Z
# S1Scribe — C1 knowledge note and registry rows (draft for the L1 to land)

Seat: **S1Scribe** (scribe). Item: **C1-SCRIBE** — draft the C1 knowledge note
`corpus/knowledge/btrfs-scrub-limit-revert-r67.md` and its two registry rows `S284` / `S285`
in `corpus/SOURCES.md`. Prose only: this seat wrote **no** file under `corpus/`. The L1
(TsukuroiR67) lands the note and both rows together.

Layout: `## NOTE` is the complete note body, from its first line (`source:`, the provenance
trio) to the end of that section. `## ROWS` holds the two registry rows. `## GATE` holds the
Gate block for both rows.

Source of every fact: the two pinned v7.3 copies named in the frozen declaration
(`.ufo/waves/round-67/before/src/scrub.c`, `.ufo/waves/round-67/before/src/CHANGES`), the
round-42 v7.1 frozen copy (`.ufo/waves/round-42/frozen/src/scrub.c`), and the E1Probe receipts
under `.ufo/waves/round-67/probes/`. Anything this seat could not observe is marked `[unknown]`.

## NOTE

source: S284 S285 — btrfs-progs v7.3 `cmds/scrub.c` (https://github.com/kdave/btrfs-progs/blob/v7.3/cmds/scrub.c; anchor: tag v7.3 peeled commit afdc3a65e33f4d42f768ad50dca20c32e5ee1496, `cmds/scrub.c` lines 1640-1649) and btrfs-progs v7.3 `CHANGES` (https://github.com/kdave/btrfs-progs/blob/v7.3/CHANGES; anchor: the `scrub limit` bullet at `CHANGES` line 20 under the release header `btrfs-progs-7.3 (2026-10-23)` at line 1); the v7.1 comparison pin is the round-42 frozen copy `.ufo/waves/round-42/frozen/src/scrub.c` (sha256 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801); the host readings are own-work probes under `.ufo/waves/round-67/probes/e1-*.txt`
verified-at: 2026-11-03 (lane work revision (filled by L1); btrfs-progs tag v7.3 peeled afdc3a65e33f4d42f768ad50dca20c32e5ee1496, compared against tag v7.1 peeled 4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b; host btrfs-progs 7.1-1, kernel 7.2.11-arch1-1; host capture 2026-11-03T21:50:21Z)
recheck: on-release — `sha256sum -c SHA256SUMS` run in `.ufo/waves/round-67/before/src/` must print `scrub.c: OK` and `CHANGES: OK`; `grep -n 'Revert to the older scrub limits' .ufo/waves/round-67/before/src/scrub.c` must return exactly one hit, at line 1640; and the S284 line check `grep -nE '^\| S28[34] \|' corpus/SOURCES.md` must show the S284 row sitting directly after the S283 row, each row carrying 11 cells.

# The btrfs scrub limit is restored after all devices finish, not inside the device loop (round 67)

Scope: the storage-integrity frontier, scrub throughput limit (`PROVINCE.md` Frontier; the scrub
record and `scrub_speed_max` plane held by `corpus/knowledge/btrfs-scrub-record-r42.md` and
`corpus/knowledge/btrfs-scrub-record-r43.md`). This entry holds one fact the lane did not hold:
**when** btrfs-progs puts the per-device scrub throughput limit back. Rows SL1 to SL4 below each
carry a located claim and the lines that carry it. Nothing here runs a scrub, writes
`/var/lib/btrfs`, sets a scrub limit or enables a timer.

| row | claim | evidence |
|---|---|---|
| SL1 | In btrfs-progs v7.3 the per-device scrub throughput limit is restored only after every device has finished: the reset is its own loop that runs after the per-device result loop, not inside it. | v7.3 `cmds/scrub.c`:1640-1649 — `/* Revert to the older scrub limits. */` at :1640 heads a second `for (i = 0; i < fi_args.num_devices; ++i)` at :1641 whose body calls `write_scrub_device_limit(fdmnt, di_args[i].devid, sp[i].old_limit)` at :1642 and warns `failed to reset scrub throughput limit on devid %llu: %m` at :1645-1646; the loop closes at :1648. The per-device result loop it follows closes at :1638, its `pthread_join(t_devs[i], NULL)` is at :1600, and the `if (do_print)` block starts at :1650 — so every device's scrub thread is joined before any limit is restored. Pinned bytes sha256 b58942ccaff74cf2300f5d25b99624ba8e9cfcb59eda5897639f1928b277d528 (S284). |
| SL2 | In btrfs-progs v7.1 the same reset ran inside the per-device result loop, ahead of that device's own thread join, so a device's limit could be put back while that device was still being scrubbed [inference from the loop order]. | v7.1 frozen `cmds/scrub.c`:1594-1608 — the per-device loop opens at :1596 and its first statement is `/* Revert to the older scrub limit. */` at :1597 followed by `write_scrub_device_limit(fdmnt, di_args[i].devid, sp[i].old_limit)` at :1598, with the `failed to reset scrub throughput limit on devid %llu: %m` warning at :1601-1602; only after that come `if (sp[i].skip)` at :1605 and `pthread_join(t_devs[i], NULL)` at :1608. The comment reads `limit` (singular) here against `limits` in v7.3. Pinned bytes sha256 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801. |
| SL3 | The v7.3 release note states the change in one line: the original limit is set back only after all devices finish. | v7.3 `CHANGES`:20 — `* scrub limit: set to the original limit only after all devices finish`, the last content bullet of the `btrfs-progs-7.3 (2026-10-23)` entry whose header sits at :1; the next entry, `btrfs-progs-7.2 (skipped)`, is at :25. Pinned bytes sha256 5046bac1def81247a02d7442807a6d495de2caafbc1a7194637ef03ea958a249 (S285). |
| SL4 | On this host the reordering is inert: one btrfs filesystem with a single device, that device's scrub limit is 0 (unlimited), and no scrub timer is enabled — so v7.3's ordering cannot change any scrub here. | own-work receipts `.ufo/waves/round-67/probes/e1-*.txt` (capture 2026-11-03T21:50:21Z): `btrfs filesystem show` reads `Total devices 1` with `devid 1` (e1-g2-filesystems.txt); `cat /sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/scrub_speed_max` reads `0` (e1-g3-sysfs-limits.txt); `systemctl is-enabled 'btrfs-scrub@-.timer'` reads `disabled` and no scrub timer is listed (e1-g4-records-timers.txt); `/var/lib/btrfs` is absent; `btrfs scrub status /` prints `no stats available` (e1-g5-scrub-status.txt). E1Probe's verdict line reads `APPLICABILITY: No` — the installed userspace is btrfs-progs 7.1-1, which still ships the old in-loop ordering (e1-applicability.md). |

## Watch

QUALITY 98 (R65-UPSTREAM-WATCH) requires a pinned upstream version to be re-read when its release
trigger fires, and the fired re-read to be logged rather than left silent. The trigger has fired:
the rows behind the round-42 and round-43 notes (S237, S238) pin btrfs-progs v7.1 with
`recheck: on-release`, and the v7.3 CHANGES header dates the 7.3 release 2026-10-23 (`CHANGES`:1).
This section is that logged re-read of the pinned v7.1 bytes against v7.3.

The diff of the two pinned `scrub.c` copies has 4 hunks. Two carry the revert move:
`@@ -1594,14 +1594,6 @@` removes the in-loop reset (v7.1:1597-1604), and `@@ -1645,6 +1637,16 @@`
adds the post-loop reset (v7.3:1640-1649). The other two touch no scrub-limit path:
`@@ -568,7 +568,7 @@` is a typo fix in a warning string (`invalid data on line %d pos ` at v7.1:571
becomes `invalid data on line %d position ` at v7.3:571), and `@@ -1372,7 +1372,7 @@` is a comment
rewording (`ie.` becomes `i.e.`, both at line 1375).

Which r42/r43 statements are unaffected: of the 47 distinct `scrub.c` lines those two notes cite,
42 are byte-identical at the same line number in v7.3, and 5 shift by exactly +2 with unchanged
text (1698 to 1700, 1706 to 1708, 1833 to 1835, 1931 to 1933, 1946 to 1948); the shift is the net
effect of the moved block. The three `CHANGES` lines they cite (460, 467, 468 of the v7.1 CHANGES)
are at 487, 494, 495 of the v7.3 CHANGES, same text. The `scrub_speed_max` semantics the round-42
note states — 0 means no limit, and a failed read is reported as 0 — rest on `scrub.c`:1215 and
:1218, byte-identical in v7.3, so SC5 stands unchanged. Neither r42 nor r43 states when the limit
is restored: the word `revert` and the token `old_limit` appear in neither file, and their
`scrub limit` mentions are the 6.6.3 feature bullets and the sysfs attribute, not the reset's
timing. Nothing in them is contradicted or withdrawn by this note; the timing of the reset is the
new fact, and it belongs to neither note's scope.

## Limits

- The v7.3 claim is a source-level statement about btrfs-progs v7.3 alone (tag v7.3, peeled
  afdc3a65e33f4d42f768ad50dca20c32e5ee1496). The host runs btrfs-progs 7.1-1, so v7.3's ordering
  is not the ordering this host executes; the installed userspace still carries the v7.1 in-loop
  reset.
- Cited lines outside the registered anchor ranges, enumerated as QUALITY 94 requires. Either the
  L1 widens the anchors of S284, S237 and S285 to cover them, or they stay enumerated here:
  - S284 (registered `cmds/scrub.c` 1640-1649): v7.3 lines 1600, 1638 and 1650 (cited in SL1 for
    the ordering argument).
  - S237 (registered ranges in its anchor do not include 1594-1608): v7.1 lines 1597, 1598,
    1601, 1602, 1605 and 1608 (cited in SL2; pin sha256 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801).
  - S285 (registered bullet at line 20): v7.3 `CHANGES` line 1, the release header (cited in
    the Watch section and in the note's source line).
- E1Probe's `MISSING` token in `btrfs filesystem show` is a privilege artefact — the
  `/dev/dm-0` open fails with `Permission denied` under `CapEff: 0000000000000000` — not a
  degraded filesystem: all four subvolumes are mounted, `df -B1` totals the device, and
  `btrfs scrub status -d /` resolves `id 1` with the matching fsid.
- Every host reading here is an unprivileged read. Nothing was run, written or enabled.

## Unknowns

- Inert on this host, so not observable here: one btrfs filesystem, one device (`devid 1`),
  `scrub_speed_max` reading 0 (unlimited), no `btrfs-scrub@-.timer` enabled, no record directory,
  no scrub running. The v7.3 ordering would only matter on a filesystem with more than one device
  and a non-zero limit — [inference] from the located lines, not measured here.
- Whether Arch's btrfs-progs 7.1-1 carries any downstream patch is [unknown]: the Arch packaging
  recipe is not reachable from this host, so a backport cannot be excluded by direct inspection.
  The installed version string is `v7.1`, pkgrel 1.
- The individual upstream commit inside the v7.3 tag that introduced the reorder is [unknown]
  here; only the tag peel afdc3a65e33f4d42f768ad50dca20c32e5ee1496 is pinned.

---

## ROWS

*Two registry rows for `corpus/SOURCES.md`, to be pasted directly after the S283 row (the C1
predicate requires S284 to sit immediately after S283). Column order is the registry's own header
(`id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`); each
row has 11 cells and no pipe character inside any cell. The fence markers are not part of the rows.*

```
| S284 | btrfs-progs v7.3 cmds/scrub.c — https://github.com/kdave/btrfs-progs/blob/v7.3/cmds/scrub.c | code | A | scrub-limit revert timing in btrfs-progs v7.3 | tag v7.3 (peeled afdc3a65e33f4d42f768ad50dca20c32e5ee1496), cmds/scrub.c lines 1640-1649 (v7.3); raw sha256 b58942ccaff74cf2300f5d25b99624ba8e9cfcb59eda5897639f1928b277d528 | the per-device scrub throughput limit is restored only after every device's scrub has finished, so no device's limit is put back while another device is still being scrubbed | mined | 2026-11-03 | on-release | corpus/knowledge/btrfs-scrub-limit-revert-r67.md |
| S285 | btrfs-progs v7.3 CHANGES — https://github.com/kdave/btrfs-progs/blob/v7.3/CHANGES | docs | A | release note for the scrub-limit revert timing in btrfs-progs 7.3 | tag v7.3, CHANGES bullet 'scrub limit' under btrfs-progs-7.3; raw sha256 5046bac1def81247a02d7442807a6d495de2caafbc1a7194637ef03ea958a249 | the upstream release note names the change in one line, so a reader can date the new reset timing to btrfs-progs 7.3 without reading the diff | mined | 2026-11-03 | on-release | corpus/knowledge/btrfs-scrub-limit-revert-r67.md |
```

Field notes for the L1 (not part of the rows):

- **id** — `S284`, `S285`: the next two free ids; S283 is the last row on disk
  (`grep -cE '^\| S[0-9]+ \|' corpus/SOURCES.md` printed 283).
- **source** — the two upstream blob URLs, one per row.
- **kind** — `code` for the source file, `docs` for the release notes; both are census-enum values.
- **tier** — `A`: read from the upstream artifact at a pinned tag with a pinned sha256, fetched
  2026-11-03 (`.ufo/waves/round-67/before/src/FETCH.txt`).
- **status** — `mined`: the note's SL1 and SL3 rows read these two sources.
- **opened** — `2026-11-03`: the fetch date (FETCH.txt records 2026-11-03T21:41:19Z).
- **recheck** — `on-release`: the next btrfs-progs release re-fires the read; the Watch section is
  the logged re-read QUALITY 98 asks for.
- **used-by** — the note this pair grounds.

Census expectations for the L1 (this seat ran no census): two new rows, 283 to 285. Both URLs are
new, so no `W04` and no `E04`. `E11` fires for both rows until the note lands, because the
`used-by` path does not exist yet — the note and the two rows must land in the same commit, and
the after-census receipt is taken after that commit. Row shape at the work revision:
`awk -F'|' '/^\| S28[45] /{print NF}' corpus/SOURCES.md` must print `13` twice, and
`grep -nE '^\| S28[34] \|' corpus/SOURCES.md` must show S284 immediately after S283.

---

## GATE

*Gate block for the two rows opened this round (CORPUS.md contract v1, "SOURCES.md — where a
shokunin learns", Rules 1-6: URL, access date, a located quote of at most 25 words, and the
location of that quote). Two rows were opened this round — S284 and S285.*

### Gate record — S284

| field | value |
|---|---|
| URL | https://github.com/kdave/btrfs-progs/blob/v7.3/cmds/scrub.c |
| access date | 2026-11-03 |
| quote | `/* Revert to the older scrub limits. */` |
| location | `cmds/scrub.c` line 1640 at tag v7.3 (peeled afdc3a65e33f4d42f768ad50dca20c32e5ee1496); the loop it heads runs at lines 1641-1648, after the per-device result loop closes at line 1638 and before the `if (do_print)` block at line 1650. Raw bytes sha256 b58942ccaff74cf2300f5d25b99624ba8e9cfcb59eda5897639f1928b277d528, fetched 2026-11-03 |
| word count | 8 words by `wc -w` (cap 25) |

Word-count command (run by this seat on the exact quote text):

```
$ printf '%s' '/* Revert to the older scrub limits. */' | wc -w
8
```

Supporting located lines (same file, same tag):

- `cmds/scrub.c:1641` — `for (i = 0; i < fi_args.num_devices; ++i) {`
- `cmds/scrub.c:1642` — `ret = write_scrub_device_limit(fdmnt, di_args[i].devid, sp[i].old_limit);`
- `cmds/scrub.c:1645` — `warning("failed to reset scrub throughput limit on devid %llu: %m",`
- `cmds/scrub.c:1648` — `}` (the restore loop closes)
- `cmds/scrub.c:1638` — `}` (the per-device result loop closes)
- `cmds/scrub.c:1600` — `ret = pthread_join(t_devs[i], NULL);`
- `cmds/scrub.c:1650` — `if (do_print) {`

The v7.1 side of the same mechanism, from the round-42 frozen pin
(`.ufo/waves/round-42/frozen/src/scrub.c`, sha256 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801):
line 1597 `/* Revert to the older scrub limit. */`, line 1598
`ret = write_scrub_device_limit(fdmnt, di_args[i].devid, sp[i].old_limit);`, line 1605
`if (sp[i].skip)`, line 1608 `ret = pthread_join(t_devs[i], NULL);`. The reset precedes the join there.

### Gate record — S285

| field | value |
|---|---|
| URL | https://github.com/kdave/btrfs-progs/blob/v7.3/CHANGES |
| access date | 2026-11-03 |
| quote | `* scrub limit: set to the original limit only after all devices finish` |
| location | `CHANGES` line 20, under the release header `btrfs-progs-7.3 (2026-10-23)` at line 1; the next entry, `btrfs-progs-7.2 (skipped)`, is at line 25. Raw bytes sha256 5046bac1def81247a02d7442807a6d495de2caafbc1a7194637ef03ea958a249, fetched 2026-11-03 |
| word count | 13 words by `wc -w` (cap 25) |

Word-count command (run by this seat on the exact quote text):

```
$ printf '%s' '* scrub limit: set to the original limit only after all devices finish' | wc -w
13
```

The quoted line is complete as it stands in the file, `* ` leader included.

### Admitted

`pending non-author verification` — the evidence pointer this section carries is the round's
non-author source-review seat's verdict on the S284 and S285 rows: a live re-open of the two blob
URLs (HTTP status, byte count, raw sha256 against the pinned digests `b58942cc…d528` and
`5046bac1…a249`), the quotes' re-count by `wc -w` (at most 25), the quotes' re-location in the
fetched bytes, and the row-shape check (`awk -F'|'` NF 13, S284 directly after S283, no duplicate
ids, no `|` inside any cell). Seat receipts land under `.ufo/waves/round-67/w1/`.

### Rejected

`pending non-author verification` — the evidence pointer this section carries is the round's
review seats' rejection verdicts, each naming the source and the reason (a rejected row reads
`REJECTED: <reason>; flip: <what would change the verdict>`). If no source is rejected this round,
the landed text states that explicitly, as rounds 63 and 64 did.

### Spot-check result

`pending non-author verification` — the round's non-author closure judge re-opens a sample of the
new rows and re-runs the counting battery (the S284 and S285 re-opens, the two quote re-counts, the
registry row shape).

---

*End of draft. This seat wrote no file under `corpus/`, ran no census, and made no git or jj
mutation in the lane or any sibling. The commands and their rc are in
`.ufo/waves/round-67/w1/S1Scribe.md`.*
