VERDICT: supports

## Gate

- Access date: 2026-10-28T21:13:23Z (curl finished 2026-10-28T21:13:24Z, exit 0)
- URL: https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/dev-replace.c?h=v7.2.11
- sha256: f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a
- Quote (live `fs/btrfs/dev-replace.c:700`, 10 tokens): `/* the disk copy procedure reuses the scrub code */`

The frozen entry rests on that line: `corpus/knowledge/btrfs-scrub-grounding-r45.md:92` at `2732ee6c06108c031c4d8043239b994e0504eb2f` is `**Quote.** `S247` dev-replace.c:700: "/* the disk copy procedure reuses the scrub code */"`.

## Re-open

Command (cwd fleet root; output path absolute):

`curl -sSfL --max-time 120 'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/dev-replace.c?h=v7.2.11' -o /fast/scratch/hyaku/tsukuroi-r51/R51ScoutReopenS247/live.bin`

Observed: `CURL_EXIT:0`, `2026-10-28T21:13:23Z` then `2026-10-28T21:13:24Z`, `39841` bytes, sha256 `f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a`, `1322` lines. Receipt copy: `.ufo/waves/round-51/w1/R51ScoutReopenS247/dev-replace.c` (same size and sha256).

Pin `f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a` matches. Snapshot `.ufo/waves/round-45/frozen/src/dev-replace.c` hashes to the same digest. `SHA256SUMS` line 2 in that directory is `f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a  dev-replace.c`. `cmp -s` of live bytes and the snapshot exited 0. A line-split compare reported `identical_file=True`. Byte-identical, so no differing-line diff was run.

No tools were installed.

## Cited lines (live bytes)

Each line below is from the live fetch. `EQ=True` means the same line of the snapshot is the same byte string. Leading whitespace is a tab.

| line | vs snapshot | text |
|---|---|---|
| 700 | EQ=True | `	/* the disk copy procedure reuses the scrub code */` |
| 701 | EQ=True | `	ret = btrfs_scrub_dev(fs_info, src_device->devid, 0,` |
| 702 | EQ=True | `			      btrfs_device_get_total_bytes(src_device),` |
| 703 | EQ=True | `			      &dev_replace->scrub_progress, false, true);` |
| 1197 | EQ=True | `/* resume dev_replace procedure that was interrupted by unmount */` |
| 1235 | EQ=True | `	if (!btrfs_exclop_start(fs_info, BTRFS_EXCLOP_DEV_REPLACE)) {` |
| 1259 | EQ=True | `		"continuing dev_replace from %s (devid %llu) to target %s @%u%%",` |
| 1260 | EQ=True | `		btrfs_dev_name(dev_replace->srcdev),` |
| 1261 | EQ=True | `		dev_replace->srcdev->devid,` |
| 1262 | EQ=True | `		btrfs_dev_name(dev_replace->tgtdev),` |
| 1263 | EQ=True | `		(unsigned int)progress);` |
| 1264 | EQ=True | (empty) |
| 1265 | EQ=True | `	ret = btrfs_scrub_dev(fs_info, dev_replace->srcdev->devid,` |
| 1266 | EQ=True | `			      dev_replace->committed_cursor_left,` |
| 1267 | EQ=True | `			      btrfs_device_get_total_bytes(dev_replace->srcdev),` |
| 1268 | EQ=True | `			      &dev_replace->scrub_progress, false, true);` |
| 1278 | EQ=True | `	if (!dev_replace->is_valid)` |
| 1279 | EQ=True | `		return false;` |
| 1280 | EQ=True | (empty) |
| 1281 | EQ=True | `	switch (dev_replace->replace_state) {` |
| 1282 | EQ=True | `	case BTRFS_IOCTL_DEV_REPLACE_STATE_NEVER_STARTED:` |
| 1283 | EQ=True | `	case BTRFS_IOCTL_DEV_REPLACE_STATE_FINISHED:` |
| 1284 | EQ=True | `	case BTRFS_IOCTL_DEV_REPLACE_STATE_CANCELED:` |
| 1285 | EQ=True | `		return false;` |
| 1286 | EQ=True | `	case BTRFS_IOCTL_DEV_REPLACE_STATE_STARTED:` |
| 1287 | EQ=True | `	case BTRFS_IOCTL_DEV_REPLACE_STATE_SUSPENDED:` |
| 1288 | EQ=True | `		/*` |
| 1289 | EQ=True | `		 * return true even if tgtdev is missing (this is` |
| 1290 | EQ=True | `		 * something that can happen if the dev_replace` |
| 1291 | EQ=True | `		 * procedure is suspended by an umount and then` |
| 1292 | EQ=True | `		 * the tgtdev is missing (or "btrfs dev scan") was` |
| 1293 | EQ=True | `		 * not called and the filesystem is remounted` |
| 1294 | EQ=True | `		 * in degraded state. This does not stop the` |
| 1295 | EQ=True | `		 * dev_replace procedure. It needs to be canceled` |
| 1296 | EQ=True | `		 * manually if the cancellation is wanted.` |
| 1297 | EQ=True | `		 */` |

## S247 anchor and range gaps

`git show 2732ee6c06108c031c4d8043239b994e0504eb2f:corpus/SOURCES.md` line 5 names the anchor column. Line 256:

`| S247 | Linux v7.2.11 fs/btrfs/dev-replace.c — https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/fs/btrfs/dev-replace.c?h=v7.2.11 | code | A | How a btrfs device replace copies data and which scrub entry point it uses | tag v7.2.11 (peeled commit a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea), fs/btrfs/dev-replace.c lines 700-703, 1143-1144, 1235, 1256-1268, 1276-1300; raw bytes sha256 f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a | Both the replace start and the continue path call btrfs_scrub_dev on the source devid with is_dev_replace true | mined | 2026-10-27 | on-release | corpus/knowledge/btrfs-scrub-grounding-r45.md |`

Declared ranges in that anchor cell: 700-703, 1143-1144, 1235, 1256-1268, 1276-1300.

Of the lines checked:

- 700-703 are inside 700-703.
- 1235 is the declared singleton 1235.
- 1259-1268 are inside 1256-1268.
- 1278-1297 are inside 1276-1300.
- 1197 is outside every declared range.

`python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/lint-grounding-r51.py --revision 2732ee6c06108c031c4d8043239b994e0504eb2f --emit-gaps` printed, for this row only, `- S247 dev-replace.c: 1197`. The frozen entry's `### Range gaps (R51)` block at `corpus/knowledge/btrfs-scrub-grounding-r45.md:275` is the same bullet. The outside-line list matches the emitter.
