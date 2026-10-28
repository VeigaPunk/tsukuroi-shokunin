VERDICT: supports

# S243 live re-open (R49ScoutSysfs)

Opened 2026-10-28. Freeze row read from `55c07cd3f8bff2e12117c34d57b4c618de74d85c:corpus/SOURCES.md` (S243). Pin: `.ufo/waves/round-44/frozen/src/sysfs.c`. SOURCES.md was not edited.

## 1. Fetch

Registry URL (source column): `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/fs/btrfs/sysfs.c?h=v7.2.11`.
Raw bytes URL (FETCH.txt:3, the pin's fetch): `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/sysfs.c?h=v7.2.11`.

Access date: `2026-10-28` (`date -u +%F`; HTTP date `Wed, 28 Oct 2026 17:20:52 GMT` on the plain response).

| fetch | redirects | HTTP | bytes | content-type | sha256 |
|---|---|---|---|---|---|
| plain `?h=v7.2.11` | 0 (`url_effective` unchanged) | 200 | 72925 | text/plain | `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43` |
| plain `?h=a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea` | 0 | 200 | 72925 | text/plain | same |
| tree URL from the source column | 0 | 200 | 181619 | text/html | not the C file |

`cmp -s` of the plain tag fetch against the pinned snapshot: EQUAL. `cmp -s` of the tag fetch against the peeled-commit fetch: EQUAL. Pin sha256 matches `SHA256SUMS:2` and the row's anchor digest.

Upstream did not move. `v7.2.11` is an annotated tag, not a branch. Tag page (`…/tag/?h=v7.2.11`, HTTP 200, 0 redirects, accessed 2026-10-28) says "tag name v7.2.11 (8316c24ec1b77dba19ba072ca4fe251b36dc65d3)" and "tagged object" links to commit `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea` (`.ufo/waves/round-49/w1/R49ScoutSysfs/tag.html:153`, `:156`). That is the peel the row already records. Both plain URLs also shared weak etag `W/"0d14570c8bc2900bb41685a13cfbf2c4783789e8"`; the content proof is the sha256 and `cmp`, not the etag.

The tree URL is HTML and is not byte-comparable to the snapshot. The row's digest is of the plain file, as round-44 `FETCH.txt:3` and `corpus/lessons/round-44.md:21` already say.

## 2. Anchors in the live bytes

Live file is 2702 lines. Quotes are the whole live line (each under 25 words).

- store parse, line 2040: `limit = memparse(buf, &endptr);`
- store check, line 2043: `if (*endptr != 0)` — the next line is `return -EINVAL;` and the accepted store is line 2045 `WRITE_ONCE(device->scrub_speed_max, limit);`
- exclusive-operation label, line 1288: `str = "device replace\n";`
- replace_target show body, line 2015: `val = !!test_bit(BTRFS_DEV_STATE_REPLACE_TGT, &device->dev_state);` inside `btrfs_devinfo_replace_target_show` (line 2007), emitted at line 2017 and registered at line 2019 `BTRFS_ATTR(devid, replace_target, btrfs_devinfo_replace_target_show);`

## 3. Cadence and pins

The `on-release` cadence still fits this annotated tag: the peel and the raw sha256 are unchanged, and the registered ranges 72-74, 2021-2049 and 2113 still hold the `BTRFS_ATTR_RW` 0644 macro, the scrub_speed_max show/store, and `BTRFS_ATTR_PTR(devid, scrub_speed_max)`.

## 4. Proposed status / recheck / used-by

no change

`status` stays `mined`, `recheck` stays `on-release`, `used-by` stays `corpus/knowledge/btrfs-scrub-record-r44.md, corpus/knowledge/btrfs-scrub-grounding-r45.md`. At the freeze those are the only `corpus/knowledge` consumers (`git grep S243 55c07cd3… -- corpus/knowledge`). Lines 1288 and 2015 are still outside the registered anchor ranges; `btrfs-scrub-grounding-r45.md:225-226` already records that and says the registration stays as it is, so that gap is not a stale `status`/`recheck`/`used-by` cell.

## Not done

Did not edit `SOURCES.md`. Did not query git protocol (`ls-remote`); the tag-versus-branch claim is the cgit tag page plus the two plain fetches. Did not re-run host sysfs reads.

Receipts: `.ufo/waves/round-49/w1/R49ScoutSysfs/` (`sysfs.c.live`, `sha256-live.txt`, `cmp-tag-vs-pin.txt`, `tag.html`, headers). Scratch `/fast/scratch/hyaku/tsukuroi-r49/R49ScoutSysfs` removed after the copy.
