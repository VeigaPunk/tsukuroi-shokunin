VERDICT: supports

Seat C2DraftCritSR8 — Item C2-13, SR8 pre-read (wave 1; no `ROW … VERDICT`
line). Scope: SR8 of `corpus/knowledge/btrfs-scrub-record-r44.md` at revision
7e081698d4fc3c4ea944884fd093058de9909de1 (verified identical via
`git show 7e081698…:corpus/knowledge/btrfs-scrub-record-r44.md` lines 55-84)
against S243 `frozen/src/sysfs.c` and S242 `frozen/src/scrub.c`, read line by
line. Frozen digests verified to match the counter's `SNAP` (sha256sums in
receipt `C2DraftCritSR8/sr8-source-evidence.md`).

## Sentence-by-sentence marking (statement, KB lines 57-63)

S1 "Each btrfs device's scrub bandwidth limit is the sysfs attribute
`devinfo/<devid>/scrub_speed_max` under `/sys/fs/btrfs/<fsid>/`, declared with
`BTRFS_ATTR_RW`, which builds the attribute with mode 0644: any user can read
it, and only its owner (root) can write it."
- **holds** — deciding line: 'any user can read it, only its owner (root) can
  write it'. Evidence: `sysfs.c:72` `#define BTRFS_ATTR_RW(_prefix, _name,
  _show, _store)`; `sysfs.c:74` `__INIT_KOBJ_ATTR(_name, 0644, _show,
  _store)` (mode 0644 = owner rw, group r, others r); `sysfs.c:2048`
  `BTRFS_ATTR_RW(devid, scrub_speed_max, btrfs_devinfo_scrub_speed_max_show,`
  and `sysfs.c:2113` `BTRFS_ATTR_PTR(devid, scrub_speed_max)` inside
  `devid_attrs[]` (`sysfs.c:2107-2116`) exposed via
  `devid_ktype.default_groups = devid_groups` (`sysfs.c:2128-2132`); kobject
  path built at `sysfs.c:2165-2166`
  (`kobject_init_and_add(&device->devid_kobj, &devid_ktype, devinfo_kobj,
  "%llu", device->devid)`), i.e. `…/devinfo/<devid>/`. Owner root confirmed by
  host capture `capture.txt:4` (`mode=644 owner=root value=0`).

S2 "Reading prints the device's in-memory `scrub_speed_max` as one decimal
number followed by a newline."
- **holds** — deciding line: `sysfs.c:2028`
  `return sysfs_emit(buf, "%llu\n", READ_ONCE(device->scrub_speed_max));`
  (`sysfs_emit` prints decimal `%llu` + `\n`; `READ_ONCE` reads the in-memory
  field, no persistence, no unit text).

S3a "Writing parses the text with `memparse`, so a size suffix such as `K`,
`M` or `G` is accepted,"
- **holds** — deciding line: 'a size suffix such as K, M or G is accepted'.
  Evidence: `sysfs.c:2040` `limit = memparse(buf, &endptr);`. memparse at
  Linux v7.2.11 accepts K/M/G (and T/P/E), case-insensitive — verified from
  `lib/cmdline.c` (URL and verbatim body in receipt): switch cases `'K'/'k'`,
  `'M'/'m'`, `'G'/'g'`, … each `shl += 10;`. The "such as" phrasing is
  non-exhaustive, so the extra T/P/E suffixes do not make it wrong.

S3b "skips trailing whitespace including the newline,"
- **holds** — deciding line: 'skips trailing whitespace including the
  newline'. Evidence: `sysfs.c:2042` `endptr = skip_spaces(endptr);` with the
  author comment at `sysfs.c:2041` ("There could be trailing '\n', also catch
  any typos after the value."). `skip_spaces` is declared in
  `include/linux/string.h:182` (v7.2.11); its definition (kernel lib, not part
  of the pinned S242/S243 sources) loops `while (isspace(*str)) ++str;`, so it
  skips the newline and other ASCII whitespace.

S3c "and rejects anything else after the number with `-EINVAL`."
- **holds** — deciding line: 'rejects anything else after the number with
  -EINVAL'. Evidence: `sysfs.c:2043-2044`
  `if (*endptr != 0) return -EINVAL;`. Precision note: whitespace itself is
  consumed by `skip_spaces`; only a non-whitespace remnant after the number
  (e.g. `10Kjunk`) reaches the test and returns `-EINVAL`.

S4 "The scrub throttle reads the value as bytes per second and returns at once
when it is 0, so 0 means no limit."
- **holds** — deciding line: '0 means no limit'. Evidence: `scrub.c:1380`
  `bwlimit = READ_ONCE(device->scrub_speed_max);` and `scrub.c:1381-1382`
  `if (bwlimit == 0) return;`. The "bytes per second" unit is not spelled out
  in either pinned file; it is an inference from the throttle arithmetic: the
  1 s slice `time_slice = 1000` (`scrub.c:1374`) counts `bio_size` bytes
  (onescrub.c:1400`, `sctx->throttle_sent += bio_size;`) against `bwlimit`
  (`scrub.c:1401`, `div_u64(bwlimit, div)`), so the value is consumed as
  bytes per 1-second slice. Sound inference; kept explicit in the replacement
  text. The throttle is on the regular scrub IO path: callers
  `submit_initial_group_read` (`scrub.c:1942`) ← `flush_scrub_stripes`
  (`scrub.c:1971`) and `queue_scrub_stripe` (`scrub.c:2061`).

## Host reading (KB lines 83-84) — verified

"mode 644, owner root, value 0: no limit (capture.txt:4), read as uid 1000
with no effective capabilities (capture.txt:1)" — matches `capture.txt:4`
(`scrub_speed_max 1d02a454-…/devinfo/1/scrub_speed_max mode=644 owner=root
value=0`) and `capture.txt:1` (`captured 2026-10-26T23:53:22Z uid=1000
CapEff=0000000000000000`). **holds**.

## Quotes — verified line-for-line

All nine SR8 quote lines match their named files/lines exactly (checked by
reading the pinned files; the counter's `QUOTE_RE` window check also passes per
`ROWS['SR8']['windows']` — not run here, read-only inspection):
`sysfs.c:72,74,2028,2040,2042,2044,2048`, `scrub.c:1380,1381`.

## Verdict on the row

No sentence overreaches or is wrong; all six statement claims (and the host
reading) hold against S243/S242 and the S245 capture. SR8 is accurate as
written. Replacement text below is a tightening only: it (a) anchors the
"bytes per second" unit to the 1 s timeslice arithmetic, (b) names the extra
memparse suffixes (T/P/E) and the base-0 parsing behaviour, (c) states the
success return (`len`), and (d) sharpens the rejection clause to
non-whitespace remnants. All five frozen proposition tokens (`scrub_speed_max`,
`0644`, `memparse`, `EINVAL`, `no limit`) are preserved; every `**Quote.**`
and the `**Host reading.**` line are unchanged.

## Exact proposed replacement text (SR8 statement, KB lines 57-63)

**Statement.** Each btrfs device's scrub bandwidth limit is the sysfs attribute
`devinfo/<devid>/scrub_speed_max` under `/sys/fs/btrfs/<fsid>/`, declared with
`BTRFS_ATTR_RW`, which builds the attribute with mode 0644: any user can read
it, and only its owner (root) can write it. Reading prints the device's
in-memory `scrub_speed_max` as one decimal number followed by a newline.
Writing parses the text with `memparse` (base 0, so `0x…` hex and leading-`0`
octal forms parse too; suffixes `K`, `M`, `G`, `T`, `P`, `E` are accepted,
case-insensitively), then skips trailing whitespace including the newline, and
rejects anything else after the number with `-EINVAL`; on success the store
writes the parsed value and returns the input length. The scrub throttle reads
the value as bytes per second — the 1 s timeslice `time_slice = 1000` counts
submitted bytes against `bwlimit` — and returns at once when it is 0, so 0
means no limit.

## What I did not do

- Did not run `check-scrub-record-r44.py` or any counter (wave-1 pre-read;
  verdicts are not produced this wave).
- Did not write to sysfs, start/cancel a scrub, touch systemd, or modify any
  lane/fleet file other than this report and its receipts.
- Did not fetch a definition body for `skip_spaces` (kernel lib, outside the
  pinned sources); its semantics are cited from the declaration and the
  inline call site/comment.

Receipt: `.ufo/waves/round-44/w1/C2DraftCritSR8/sr8-source-evidence.md`
(memparse v7.2.11 body + string.h declaration + digest verification, fetched
2026-10-26).
