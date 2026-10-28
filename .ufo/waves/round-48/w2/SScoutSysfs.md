VERDICT: supports

# S243 live re-open (row: corpus/SOURCES.md line 252 at ae99f021b76f8eb1c8805d32d80644464afb1ff6)

## (1) Fetch, access date, digest, identity

- Row URL (verbatim from S243): `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/fs/btrfs/sysfs.c?h=v7.2.11`
- Access date (UTC): **2026-10-28**
- The row URL is a cgit *view* URL: `curl -fsSL` followed **no redirect** (final URL identical, HTTP 200) and returns an HTML page (181619 bytes, `content_type` text/html). The pinned snapshot digest in the row's anchor (`raw bytes sha256 ce146120f2…`) refers to the raw file, so for byte comparison I fetched the cgit `plain/` form of the same URL:
  - `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/sysfs.c?h=v7.2.11` — HTTP 200, `text/plain; charset=UTF-8`, 72925 bytes, no redirect.
  - sha256 of fetched bytes: `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43`
  - `cmp` vs pinned snapshot `.ufo/waves/round-44/frozen/src/sysfs.c` (sha256 identical): **BYTE-IDENTICAL**. 2702 lines.
- Upstream movement: none on the pinned ref. `h=v7.2.11` is a **tag, not a branch tip**. cgit `/refs/tags` lists v7.2.11 (tagged 2026-10-15, Greg Kroah-Hartman) and `/tag/?h=v7.2.11` resolves the tag object to `tagged object … commit a2de78ee6e…` — the peeled commit `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea` matches the row's pin exactly.
- Receipt: fetched raw bytes copied to `.ufo/waves/round-48/w2/SScoutSysfs/sysfs.c`.

## (2) Anchors located in the LIVE bytes (v7.2.11 plain fetch)

- `device replace\n`: located at **line 1288** — verbatim: `str = "device replace\n";` — matches the row-item snapshot line exactly (context: inside a `case BTRFS_DEV_STATE_IN_FS_METADATA` switch in `btrfs_devinfo_state_show`).
- `btrfs_devinfo_replace_target_show` **body** line: **line 2015** — verbatim: `val = !!test_bit(BTRFS_DEV_STATE_REPLACE_TGT, &device->dev_state);` — matches the pinned snapshot exactly. (Function definition opens at line 2007; attribute wired at line 2019 `BTRFS_ATTR(devid, replace_target, btrfs_devinfo_replace_target_show);`.)
- Row's own anchor ranges also verified live: line 73 `#define BTRFS_ATTR_RW` block (72–74); `btrfs_devinfo_scrub_speed_max_show`/`_store` span 2021–2049; line 2113 present.

## (3) Cadence and pins

The `on-release` recheck cadence and the tag/digest/line pins still read right: v7.2.11 is immutable and live-identical, and a spot check of the *newest* stable tag — `plain/…?h=v7.2.13` (tagged 2026-10-26 16:01:21 +0100) — returns the identical blob (`sha256 ce146120f2…`), so even a recheck triggered by the two newer v7.2.x releases (v7.2.12, v7.2.13 exist upstream) would find the source's content for this scope unchanged.

## (4) Proposed cell update

`no change` — status `mined`, recheck `on-release`, used-by `corpus/knowledge/btrfs-scrub-record-r44.md, corpus/knowledge/btrfs-scrub-grounding-r45.md` are all still accurate; the anchor optionally could note "verified byte-identical at v7.2.13, 2026-10-28" but that is an optional enrichment, not a staleness fix.
