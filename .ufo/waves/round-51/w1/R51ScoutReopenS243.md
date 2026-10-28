VERDICT: supports

# R51ScoutReopenS243 — S243 live re-open (fs/btrfs/sysfs.c, v7.2.11)

Live bytes match the pin and the round-44 snapshot. Cited lines 1288, 2015, 2040 and 2043 equal the snapshot. Of those, 1288 and 2015 fall outside the S243 anchor ranges; 2040 and 2043 fall inside 2021-2049. `lint-grounding-r51.py --emit-gaps` lists the same outside pair for S243.

## Re-open

Access time (UTC): `2026-10-28T21:13:39Z`. `date -u` immediately before the transfer and immediately after it both printed that timestamp. `CURL_EXIT:0`.

URL fetched: `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/sysfs.c?h=v7.2.11`

Command (cwd `/fast/scratch/hyaku/tsukuroi-r51/R51ScoutReopenS243` after `mkdir -p` of that directory):

```
curl -sSfL --max-time 120 'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/sysfs.c?h=v7.2.11' -o /fast/scratch/hyaku/tsukuroi-r51/R51ScoutReopenS243/live.bin
```

Observed: `wc -c` `72925`; `sha256sum` `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43`.

Pin (seat item and the S243 anchor cell): `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43`.

Snapshot `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-44/frozen/src/sysfs.c`: `sha256sum` the same digest; `wc -c` `72925`. Directory `SHA256SUMS` line 2: `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43  sysfs.c`.

`cmp -s` of `live.bin` against that snapshot exited 0. A full-buffer compare printed `byte_identical True`, `live_len 72925`, `snap_len 72925`, `live_nlines 2702`, `snap_nlines 2702`. The files are byte-identical, so no differing-line diff was produced.

## Cited lines in the live bytes

1-based lines of `live.bin`. Each compared equal to the same line of the snapshot (`equal=True`).

- 1288: three leading tabs, `str = "device replace\n";`. Repr `b'\t\t\tstr = "device replace\\n";'`. Outside the anchor ranges.
- 2015: one leading tab, `val = !!test_bit(BTRFS_DEV_STATE_REPLACE_TGT, &device->dev_state);`. Repr `b'\tval = !!test_bit(BTRFS_DEV_STATE_REPLACE_TGT, &device->dev_state);'`. Outside the anchor ranges.
- 2040: one leading tab, `limit = memparse(buf, &endptr);`. Repr `b'\tlimit = memparse(buf, &endptr);'`. Inside 2021-2049.
- 2043: one leading tab, `if (*endptr != 0)`. Repr `b'\tif (*endptr != 0)'`. Inside 2021-2049.

## SOURCES.md row S243

Revision `2732ee6c06108c031c4d8043239b994e0504eb2f`, `corpus/SOURCES.md:252`. Header at line 7 names the sixth column `anchor`.

Anchor cell:

`tag v7.2.11 (peeled commit a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea), fs/btrfs/sysfs.c lines 72-74, 2021-2049, 2113; raw bytes sha256 ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43`

Declared line ranges: 72-74, 2021-2049, and the single line 2113.

Of the four cited lines, 1288 and 2015 fall outside those ranges. 2040 and 2043 fall inside 2021-2049.

The row's source URL is the `tree/` form (`https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/fs/btrfs/sysfs.c?h=v7.2.11`). This re-open used the `plain/` URL named in the seat item. The peeled commit id in the anchor was not re-resolved here.

## What the entry rows rest on

Same revision, `corpus/knowledge/btrfs-scrub-grounding-r45.md` (section headings: `## GR1` at line 14, `## GR2` at line 56, `## GR3` at line 181, `### Range gaps (R51)` at line 269):

- GR1 line 47: `**Quote.** `S243` sysfs.c:2040: "limit = memparse(buf, &endptr);"`
- GR1 line 49: `**Quote.** `S243` sysfs.c:2043: "if (*endptr != 0)"`
- GR2 line 164: `**Quote.** `S243` sysfs.c:1288: "str = "device replace\n";"`
- GR2 line 166: `**Quote.** `S243` sysfs.c:2015: "val = !!test_bit(BTRFS_DEV_STATE_REPLACE_TGT, &device->dev_state);"`
- GR2 lines 175 and 177 cite `sysfs.c:1288` and `sysfs.c:2015` in prose.
- Line 274, inside `### Range gaps (R51)`: `- S243 sysfs.c: 1288, 2015`

The quote strings at lines 47, 49, 164 and 166 match the live line text after the leading tabs.

## Lint `--emit-gaps`

Command: `python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/lint-grounding-r51.py --revision 2732ee6c06108c031c4d8043239b994e0504eb2f --emit-gaps`

Exit 0. The S243 bullet in that output is `- S243 sysfs.c: 1288, 2015`. That matches the outside set computed from the anchor ranges for the four lines checked here. 2040 and 2043 are not in the emitted S243 gap list. The same bullet is the frozen entry's line 274.

## Gate

Accessed 2026-10-28 (2026-10-28T21:13:39Z).
URL: https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/sysfs.c?h=v7.2.11
sha256: ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43
Quote (live `fs/btrfs/sysfs.c:2040`, the GR1 quote at grounding line 47; the live line has one leading tab): limit = memparse(buf, &endptr);

## Not done

No mismatch diff (cmp exit 0). Tag `v7.2.11` was not peeled to confirm commit `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea`. No tools installed. Scratch `/fast/scratch/hyaku/tsukuroi-r51/R51ScoutReopenS243` removed after this report and the receipt were written.
