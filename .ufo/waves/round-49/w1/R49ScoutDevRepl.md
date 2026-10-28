VERDICT: supports

# S247 live re-open (R49ScoutDevRepl)

Opener of record for row S247. Freeze `55c07cd3f8bff2e12117c34d57b4c618de74d85c` `corpus/SOURCES.md:256` (working tree differs from that commit only at S255; S247 text is the freeze row). GR2 is freeze-identical: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff 55c07cd3f8bff2e12117c34d57b4c618de74d85c -- corpus/knowledge/btrfs-scrub-grounding-r45.md` printed no hunks. Receipts: `.ufo/waves/round-49/w1/R49ScoutDevRepl/`.

## 1. Fetch

- Registry URL (`corpus/SOURCES.md:256`): `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/fs/btrfs/dev-replace.c?h=v7.2.11`
- Fetched raw URL (same ref as `.ufo/waves/round-45/frozen/src/FETCH.txt:3`): `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/dev-replace.c?h=v7.2.11`
- Redirects: none. `curl -fsSL --max-time 60` recorded `http_code=200 redirects=0 url_effective=` the plain URL above, `size=39841` (`curl-meta.txt`). Response start: `HTTP/2 200`, `content-type: text/plain; charset=UTF-8`, `content-disposition: inline; filename="dev-replace.c"` (`headers.txt`).
- Access date: 2026-10-28. `date -u` printed `2026-10-28T17:20:52Z` (`access-date.txt`). Response `date: Wed, 28 Oct 2026 17:20:52 GMT`.
- sha256: `f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a` (`sha256-live.txt`). Same digest on the pinned file (`sha256-pin.txt`) and on `.ufo/waves/round-45/frozen/src/SHA256SUMS:2`.
- Byte equality: `cmp -s` of the live file against `.ufo/waves/round-45/frozen/src/dev-replace.c` printed `CMP_IDENTICAL` (`cmp.txt`). Both files are 1322 lines (`wc.txt`). Live copy kept as `dev-replace.c.live`.
- Upstream did not move. `h=v7.2.11` is a tag, not a branch, and the file at that ref is byte-identical to the 2026-10-27 pin (`FETCH.txt:1`). The peeled commit named on the row, `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea`, was not re-resolved over the git protocol this round.

## 2. Anchors

Live bytes equal the pin, so these line numbers are the snapshot's. Quotes are the source line with indentation removed; each is under 25 words (`anchors.tsv`, word counts in column 2).

- STARTED cancel, line 1111, inside `int btrfs_dev_replace_cancel(struct btrfs_fs_info *fs_info)` (line 1085), arm `case BTRFS_IOCTL_DEV_REPLACE_STATE_STARTED:` (line 1107): `ret = btrfs_scrub_cancel(fs_info);`
- Suspended cancel, line 1144, arm `case BTRFS_IOCTL_DEV_REPLACE_STATE_SUSPENDED:` (line 1126): `btrfs_scrub_cancel(fs_info);` — this line does not assign `ret`. The only `ret = btrfs_scrub_cancel(fs_info);` in the file is line 1111. `SCRUB_CANCEL_LINES` is `1111,1144`.
- `is_valid` gate, lines 1278-1279, in `bool __pure btrfs_dev_replace_is_ongoing` (line 1276): `if (!dev_replace->is_valid)` and `return false;`
- `is_ongoing` suspended arm, line 1287 (paired with `case BTRFS_IOCTL_DEV_REPLACE_STATE_STARTED:` at 1286; both fall through to `return true;` at 1300): `case BTRFS_IOCTL_DEV_REPLACE_STATE_SUSPENDED:`
- Unmount-suspend body, lines 1171-1195: `void btrfs_dev_replace_suspend_for_unmount(struct btrfs_fs_info *fs_info)`. Effects at 1184-1188: `case BTRFS_IOCTL_DEV_REPLACE_STATE_STARTED:`, then `dev_replace->replace_state =` / `BTRFS_IOCTL_DEV_REPLACE_STATE_SUSPENDED;`, `dev_replace->time_stopped = ktime_get_real_seconds();`, `dev_replace->item_needs_writeback = 1;`. `SUSPEND_BODY_HAS_SCRUB_CANCEL` is `False` (no `btrfs_scrub_cancel` in 1171-1195). An already-suspended replace hits `case BTRFS_IOCTL_DEV_REPLACE_STATE_SUSPENDED:` at 1182 and `break;` at 1183.

Other GR2 `S247` quotes locate on the same bytes and match the row text: line 700 `/* the disk copy procedure reuses the scrub code */`; 701 `ret = btrfs_scrub_dev(fs_info, src_device->devid, 0,`; 703 `&dev_replace->scrub_progress, false, true);`; 1128 `Scrub doing the replace isn't running so we need to do the`; 1143 `/* Scrub for replace must not be running in suspended state */`; 1235 `if (!btrfs_exclop_start(fs_info, BTRFS_EXCLOP_DEV_REPLACE)) {`; 1259 `"continuing dev_replace from %s (devid %llu) to target %s @%u%%",`; 1265 `ret = btrfs_scrub_dev(fs_info, dev_replace->srcdev->devid,`; 1268 `&dev_replace->scrub_progress, false, true);`.

## 3. Cadence and pins

The row's `on-release` recheck, tag `v7.2.11`, and whole-file sha256 still read right, because today's tag bytes match the pin; the anchor line list `700-703, 1143-1144, 1235, 1256-1268, 1276-1300` still does not name GR2's lines 1111, 1128, or 1171-1195, which are inside that same digest.

## 4. Proposed status / recheck / used-by

no change

Freeze row fields (`corpus/SOURCES.md:256`): status `mined`, recheck `on-release`, used-by `corpus/knowledge/btrfs-scrub-grounding-r45.md`.

## Not done

Did not re-resolve `refs/tags/v7.2.11^{}` (the authorized command was the file `curl`). Did not edit `SOURCES.md`. No tools installed.
