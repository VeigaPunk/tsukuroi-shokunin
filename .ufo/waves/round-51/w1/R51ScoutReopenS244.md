VERDICT: supports

S244's live Arch `btrfs-scrub@.service` at tag 7.1-1 is byte-identical to the pin `eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252`. Cited lines 9 and 10 equal the snapshot and sit inside the SOURCES anchor `btrfs-scrub@.service lines 1-10`. They are not range gaps. The sibling timer and PKGBUILD at the same tag are also byte-identical to their pins.

## Re-open

Access (UTC): `date -u` printed `2026-10-28T21:13:37Z` immediately before `curl` and `2026-10-28T21:13:38Z` immediately after. `CURL_EXIT:0`. Access date: 2026-10-28.

URL: `https://gitlab.archlinux.org/archlinux/packaging/packages/btrfs-progs/-/raw/7.1-1/btrfs-scrub@.service`

Command: `curl -sSfL --max-time 120` of that URL to `/fast/scratch/hyaku/tsukuroi-r51/R51ScoutReopenS244/live.bin`.

Observed: `wc -c` = 190; `sha256sum` = `eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252`.

Pin and snapshot: `.ufo/waves/round-44/frozen/src/SHA256SUMS` line 4 is that digest for `btrfs-scrub@.service`. The snapshot `.ufo/waves/round-44/frozen/src/btrfs-scrub@.service` is 190 bytes with the same sha256. `cmp -s` printed `BYTE_IDENTICAL`. A Python byte compare printed `equal True`. `diff -u` of snapshot vs live printed no hunks. No differing lines, so no 20-line diff.

`nl -ba` of the live file (10 lines, trailing newline):

```
     9	KillSignal=SIGINT
    10	ExecStart=/usr/bin/btrfs scrub start -B %f
```

Same `nl -ba` on the snapshot. Python line compare: `L9 equal=True` (`KillSignal=SIGINT`) and `L10 equal=True` (`ExecStart=/usr/bin/btrfs scrub start -B %f`).

Multi-file remainder of the same anchor, fetched 2026-10-28T21:14:45Z–2026-10-28T21:14:47Z (`TIMER_EXIT:0`, `PKG_EXIT:0`), same raw tag URLs:

| file | bytes | sha256 | pin match | snapshot identical |
| --- | --- | --- | --- | --- |
| `btrfs-scrub@.timer` | 160 | `9a0b6cc23f7bd97b83b6c38dd2b4e4373fead8bd3ccfb82a47c72971e9d6f8ad` | yes | yes |
| `PKGBUILD` | 3057 | `3b803e8b05d84900fcdab3513720c8005345acd1fe34ded6eaa3b7596c10ce98` | yes | yes |

Timer pin is `SHA256SUMS` line 3; PKGBUILD pin is line 5. Snapshots are the same directory's `btrfs-scrub@.timer` and `PKGBUILD`.

## Anchor and range gaps

`git show 2732ee6c06108c031c4d8043239b994e0504eb2f:corpus/SOURCES.md` line 5 header: `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`.

Line 253 (`s244_lineno_check True`), anchor cell:

`tag 7.1-1 (commit 0c0a4d77b318084ecd35aeeb6888d8a5b4d6e3e0), btrfs-scrub@.timer lines 1-11 (sha256 9a0b6cc23f7bd97b83b6c38dd2b4e4373fead8bd3ccfb82a47c72971e9d6f8ad), btrfs-scrub@.service lines 1-10 (sha256 eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252), PKGBUILD lines 99-101`

Declared service range: lines 1-10. Cited lines 9 and 10 both fall inside that range. None of those two lines fall outside it. The live file has exactly those 10 lines, so the service anchor covers the whole file.

`corpus/knowledge/btrfs-scrub-grounding-r45.md` at the same revision, `### Range gaps (R51)` lines 269-275, does not list S244. `python3 tools/lint-grounding-r51.py --revision 2732ee6c06108c031c4d8043239b994e0504eb2f --emit-gaps` exited 0 and printed those same seven lines (`GAPS_BLOCK_EQ True`, `S244_IN_GAPS False`):

```
### Range gaps (R51)

- S237 scrub.c: 421, 439, 1546
- S240 ioctl.c: 3080, 3084-3085, 3088, 3093, 3109-3110, 3115, 3190
- S242 scrub.c: 3081, 3094-3139
- S243 sysfs.c: 1288, 2015
- S247 dev-replace.c: 1197
```

The entry's outside-line list for S244 is empty, and the linter's S244 list is empty. They match.

GR3 rests on both live lines. Frozen entry lines 198 and 200:

`**Quote.** `S244` btrfs-scrub@.service:9: "KillSignal=SIGINT"`

`**Quote.** `S244` btrfs-scrub@.service:10: "ExecStart=/usr/bin/btrfs scrub start -B %f"`

Those strings are the live lines.

## Gate

Access date: 2026-10-28 (fetch window 2026-10-28T21:13:37Z–2026-10-28T21:13:38Z).

URL: https://gitlab.archlinux.org/archlinux/packaging/packages/btrfs-progs/-/raw/7.1-1/btrfs-scrub@.service

sha256: `eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252`

Quote (live line 10, five words; GR3 line 200): `ExecStart=/usr/bin/btrfs scrub start -B %f`

## Not done

Did not run `check-scrub-admission-r51.py`. No tools installed. Scratch `/fast/scratch/hyaku/tsukuroi-r51/R51ScoutReopenS244` removed after the receipts below were copied.

Receipts: `.ufo/waves/round-51/w1/R51ScoutReopenS244/` (`btrfs-scrub@.service`, `btrfs-scrub@.timer`, `PKGBUILD`, `emit-gaps.txt`).
