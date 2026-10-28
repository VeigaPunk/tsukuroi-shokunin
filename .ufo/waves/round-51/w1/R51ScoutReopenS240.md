VERDICT: supports

Live `fs/btrfs/ioctl.c` at Linux v7.2.11 is byte-identical to the pin and to the round-43 snapshot. Every inspected line equals the same snapshot line. The freeze's S240 range-gap bullet matches `lint-grounding-r51.py --emit-gaps`.

## Re-open

- Access (UTC): start `2026-10-28T21:13:18Z`, end `2026-10-28T21:13:21Z`. Access date: 2026-10-28.
- Command: `curl -sSfL --max-time 120 'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/ioctl.c?h=v7.2.11' -o /fast/scratch/hyaku/tsukuroi-r51/R51ScoutReopenS240/live.bin` (cwd was that scratch dir). Observed `curl_rc=0`.
- Size: 145999 bytes. Lines: 5678.
- sha256: `7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01`
- Pin named by the item: the same digest.
- Snapshot `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-43/frozen/src/ioctl.c` sha256 is that digest (145999 bytes). `SHA256SUMS` in that directory is the line `7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01  ioctl.c`.
- `cmp -s` of live.bin and that snapshot: identical. Python byte compare: `bytes_equal=True`. No differing lines, so no diff.
- Freeze SOURCES row (`git show 2732ee6c06108c031c4d8043239b994e0504eb2f:corpus/SOURCES.md` line 249) already says `reopened live 2026-10-28, byte-identical` and the same sha256. This fetch is a separate live read of the stable-tree URL and agrees.

Receipts (copied before scratch removal): `.ufo/waves/round-51/w1/R51ScoutReopenS240/` (`live.bin`, `live.sha256`, `access-start.txt`, `access-end.txt`, `curl-rc.txt`, `cited-lines.txt`, `emit-gaps.txt`, `s240-row.txt`). The copied `live.bin` rehashes to the same digest.

No tool was installed.

## Cited lines (live == snapshot)

Anchor cell on SOURCES line 249, cell "tag v7.2.11 …": `fs/btrfs/ioctl.c lines 3066-3075, 3118-3140, 5578-5584`.

`in` means the line number sits in one of those three ranges. `eq=yes` means the live line equals the snapshot line. Text is the live line; a leading tab is written as `\t`. Blank lines are empty.

| line | anchor | eq | live text |
| --- | --- | --- | --- |
| 3072 | in | yes | `\tif (!capable(CAP_SYS_ADMIN))` |
| 3073 | in | yes | `\t\treturn -EPERM;` |
| 3074 | in | yes | (empty) |
| 3075 | in | yes | `\tif (btrfs_fs_incompat(fs_info, EXTENT_TREE_V2)) {` |
| 3076 | out | yes | `\t\tbtrfs_err(fs_info, "scrub: extent tree v2 not yet supported");` |
| 3077 | out | yes | `\t\treturn -EINVAL;` |
| 3078 | out | yes | `\t}` |
| 3079 | out | yes | (empty) |
| 3080 | out | yes | `\tsa = memdup_user(arg, sizeof(*sa));` |
| 3081 | out | yes | `\tif (IS_ERR(sa))` |
| 3082 | out | yes | `\t\treturn PTR_ERR(sa);` |
| 3083 | out | yes | (empty) |
| 3084 | out | yes | `\tif (sa->flags & ~BTRFS_SCRUB_SUPPORTED_FLAGS)` |
| 3085 | out | yes | `\t\treturn -EOPNOTSUPP;` |
| 3086 | out | yes | (empty) |
| 3087 | out | yes | `\tif (!(sa->flags & BTRFS_SCRUB_READONLY)) {` |
| 3088 | out | yes | `\t\tret = mnt_want_write_file(file);` |
| 3089 | out | yes | `\t\tif (ret)` |
| 3090 | out | yes | `\t\t\treturn ret;` |
| 3093 | out | yes | `\tret = btrfs_scrub_dev(fs_info, sa->devid, sa->start, sa->end,` |
| 3109 | out | yes | `\tif (copy_to_user(arg, sa, sizeof(*sa)))` |
| 3110 | out | yes | `\t\tret = -EFAULT;` |
| 3115 | out | yes | `\treturn ret;` |
| 3132 | in | yes | `\tif (!capable(CAP_SYS_ADMIN))` |
| 3133 | in | yes | `\t\treturn -EPERM;` |
| 3190 | out | yes | `\t\tif (!btrfs_exclop_start(fs_info, BTRFS_EXCLOP_DEV_REPLACE)) {` |

26 lines, all `eq=yes` (`cited-lines.txt`).

Inspected lines outside the declared ranges: 3076-3090, 3093, 3109-3110, 3115, 3190.
Inspected lines inside: 3072-3075 (range 3066-3075) and 3132-3133 (range 3118-3140).

On the live file those statements sit in `btrfs_ioctl_scrub` (line 3066; body through 3116), `btrfs_ioctl_scrub_progress` (the 3132-3133 check), and `btrfs_ioctl_dev_replace` (the 3190 call). Cancel's own check, not in the inspected set, is live line 3120 `if (!capable(CAP_SYS_ADMIN))` / 3121 `return -EPERM;`, inside 3118-3140. The dispatch cases `BTRFS_IOC_SCRUB`, `BTRFS_IOC_SCRUB_CANCEL`, and `BTRFS_IOC_SCRUB_PROGRESS` are live lines 5578-5583, inside 5578-5584.

## Range gaps vs the inspected lines

`python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/lint-grounding-r51.py --revision 2732ee6c06108c031c4d8043239b994e0504eb2f --emit-gaps` (rc 0) printed:

```
### Range gaps (R51)

- S237 scrub.c: 421, 439, 1546
- S240 ioctl.c: 3080, 3084-3085, 3088, 3093, 3109-3110, 3115, 3190
- S242 scrub.c: 3081, 3094-3139
- S243 sysfs.c: 1288, 2015
- S247 dev-replace.c: 1197
```

The S240 bullet equals the freeze entry's `### Range gaps (R51)` bullet (`git show 2732ee6c06108c031c4d8043239b994e0504eb2f:corpus/knowledge/btrfs-scrub-grounding-r45.md` line 272). The five bullets equal the whole emitted list.

That S240 bullet is the subset of the inspected outside-anchor lines that the rows pin: 3080, 3084-3085, 3088, 3093, 3109-3110, 3115, 3190. Each of those is outside 3066-3075, 3118-3140, and 5578-5584. GR2's Quote pins are at grounding lines 144-162 (3072, 3075, 3080, 3084, 3085, 3088, 3093, 3109, 3110, 3115); the 3190 pin is the host-reading cite at grounding line 176.

Inspected lines outside the anchor that the S240 bullet does not list: 3076-3079, 3081-3083, 3086-3087, 3089-3090. GR2's prose at grounding line 79 names the span `:3075-3078` and `:3080-3082` and `:3087-3090`; the Quote pin for the extent-tree check is line 3075, which is inside 3066-3075. The gap bullet follows the Quote pins plus the 3190 cite, not every integer in those prose spans.

## Gate

Accessed 2026-10-28 (UTC window 2026-10-28T21:13:18Z to 2026-10-28T21:13:21Z).
URL: https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/ioctl.c?h=v7.2.11
sha256: 7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01
Quote. ioctl.c:3072: "if (!capable(CAP_SYS_ADMIN))"

The live line is that statement with one leading tab (2 words). GR2 rests on it: grounding line 78 cites `ioctl.c:3072-3073` for `-EPERM` without `CAP_SYS_ADMIN`, and grounding line 144 quotes `S240` ioctl.c:3072 as that same statement. Live line 3073 is `return -EPERM;`.

## Axes

Byte identity, cited-line equality, gap-bullet membership, and a row-pinned quote. The live fetch confirmed identity and line equality together; the gap check matched the freeze bullet. No move was dropped.

## Not done

No line diff (the files matched). No admission counter, no C2 scorer, no second fetch. Scratch `/fast/scratch/hyaku/tsukuroi-r51/R51ScoutReopenS240` was removed after the receipts were copied.
