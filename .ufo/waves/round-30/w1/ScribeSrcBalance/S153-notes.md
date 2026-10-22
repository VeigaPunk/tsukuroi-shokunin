# S153 — free work space, ENOSPC and a nearly full filesystem

All line numbers are in the saved snapshots, both fetched from raw.githubusercontent.com at tag
v7.1 (peeled commit 4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b) with plain curl, HTTP 200.

- `.ufo/waves/round-30/w1/ScribeSrcBalance/S153-balance.rst` — 274 lines, 10439 bytes, sha256
  ca245fbf145166ec24c8a84864ffd44fbef98ca66551fdf50cfb8be552d22cea. It holds the command page and
  the ENOSPC section; it does not hold the filter text itself. At line 92 it has
  `.. include:: ch-balance-filters.rst`.
- `.ufo/waves/round-30/w1/ScribeSrcBalance/S153-balance-filters.rst` — 161 lines, 7009 bytes,
  sha256 d38bc2dc13e5a84a2d08c7c7b2c1bb42f0eb834fbf2af6d6f7cc0ecfd10a784c. It holds the `usage`
  filter text.

## What the documentation says about balance needing free space

1. Lines 97-99 of S153-balance.rst: "The way balance operates, it usually needs to temporarily
   create a new block group and move the old data there, before the old block group can be
   removed. For that it needs the work space, otherwise it fails for ENOSPC reasons." [obs]
2. Lines 100-102: this ENOSPC "is not the same ENOSPC as if the free space is exhausted"; it is
   space at the block-group level. So a filesystem with free space reported as available can still
   fail a balance. [obs]
3. Lines 104-116 give the computation: the free work space is `size - used` per device from
   `btrfs filesystem show`; the worked example is 53.90GiB - 51.90GiB = 2.00GiB. [obs]
4. Line 118: "An example of a filter that does not require workspace is *usage=0*." Lines 118-120
   say it scans all unused block groups of a given type and reclaims the space, after which other
   filters may become possible. [obs]
5. Lines 124-126: profile conversions to striping profiles need work space on each device, and an
   interrupted balance "may leave partially filled block groups that consume the work space." [obs]

## What it says about running on a nearly full filesystem

Lines 52-54 of S153-balance-filters.rst, inside the `usage` filter entry: the value 0 "is allowed
and will clean up completely unused block groups", it "should not require any new work space
allocated", and "You may want to use *usage=0* in case balance is returning ENOSPC and your
filesystem is not too full." [obs]

Read carefully: the advice is offered for the case where the filesystem is *not* too full. The
documentation gives no filter and no procedure for a filesystem that is already too full; it only
notes that `usage=0` needs no new workspace. The `usage` filter entry at line 51 selects block
groups with usage under a percentage, and lines 56-59 state the single value N means "at most N
percent used" with an inclusive minimum and exclusive maximum in range form.

I did not find any statement in either file that promises the freed block group returns to
`unallocated` in so many words; lines 118-120 say "reclaim the space" and lines 97-99 say the old
block group "can be removed". [obs] The D03 statement is worded to stay inside that language.

## Non-canonical alternates (do not insert directly; one row per id)

These were verified verbatim (`sed -n '<line>p' <file> | grep -cF '<quote>'` printed 1 for each)
but are not in S153-rows.json because a corpus list must keep one row per id:

- S153-balance.rst line 118, quote "An example of a filter that does not require workspace is
  *usage=0*. This will" (14 words, contains `usage`) — closer to the reclaim wording, but it sits
  two lines above the sentence that completes the claim.
- S153-balance-filters.rst line 54, quote "in case balance is returning ENOSPC and your filesystem
  is not too full." (14 words) — carries the ENOSPC advice but not the frozen token in a form that
  names the filter.
- S153-balance-filters.rst line 29, quote "Before changing profiles, make sure there is enough
  unallocated space on" (12 words) — carries `unallocated`, relevant to D09 rather than D03.

## Provenance notes

- The assignment named `Documentation/btrfs-balance.rst` as the file to save and also the file
  holding the `usage` filter text. The named file exists at v7.1 (HTTP 200, 10439 bytes) but the
  `usage` text is in its included chapter, so both files are saved and both hashes are recorded.
  This is not a missing-file fallback: no cgit tree listing or alternate endpoint was needed.
- A second fetch of S153-balance-filters.rst returned the identical sha256, so the snapshot is
  reproducible right now.
