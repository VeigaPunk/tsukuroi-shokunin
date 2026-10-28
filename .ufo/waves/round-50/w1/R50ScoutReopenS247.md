VERDICT: supports

Axes: freshness (live `v7.2.11` body against the round-45 pin), fidelity (GR2's S247 quotes against those lines), support (every GR2 clause that cites `dev-replace.c`).

Byte-identical. Two GETs of `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/dev-replace.c?h=v7.2.11` on 2026-10-28 returned the same body. The hashed copy bound to headers is HTTP 200 at `2026-10-28T19:06:48Z`, `size_download=39841`, `content-type: text/plain; charset=UTF-8`, etag `W/"7e78215b2049b802b52ea3c52b5384c31088428a"`. sha256 `f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a`. That is line 2 of `.ufo/waves/round-45/frozen/src/SHA256SUMS`. `cmp` of the body with `.ufo/waves/round-45/frozen/src/dev-replace.c` is identical (39841 bytes). Git blob sha1 of the body is `7e78215b2049b802b52ea3c52b5384c31088428a`, the same id the etag carries. 1322 LF lines, no CR, trailing newline. The `last-modified` header on both saved header dumps is `Wed, 28 Oct 2026 19:04:54 GMT`; identity here is the sha256, which matches the pin recorded in `.ufo/waves/round-45/frozen/src/FETCH.txt` (same URL, fetched 2026-10-27). This seat did not re-resolve `refs/tags/v7.2.11`.

GR2 text checked is the freeze blob: `git show 8029cdba1049df25632c91a23c8db4eefb54be5f:corpus/knowledge/btrfs-scrub-grounding-r45.md`. Section hash of `## GR2` through the line before `## GR3`, sha256 of the lines joined with LF and no trailing LF, is `a2e955cefbd110ced928407c79b2cedb3cc431734487aa29e74682b23aeb7f3f` (frozen row hash).

## Line 1128

Raw bytes: `\t\t * Scrub doing the replace isn't running so we need to do the\n`. Stripped text is `* Scrub doing the replace isn't running so we need to do the`. GR2's quote (grounding line 127) is that string, `* ` prefix included. Equal.

## Requested lines (live body)

700-703, in `btrfs_dev_replace_start` (definition at 587):

```
700	/* the disk copy procedure reuses the scrub code */
701	ret = btrfs_scrub_dev(fs_info, src_device->devid, 0,
702			      btrfs_device_get_total_bytes(src_device),
703			      &dev_replace->scrub_progress, false, true);
```

1111, in `btrfs_dev_replace_cancel` (1085), `case BTRFS_IOCTL_DEV_REPLACE_STATE_STARTED` at 1107:

```
1111		ret = btrfs_scrub_cancel(fs_info);
```

1126-1144, same function, suspended arm:

```
1126	case BTRFS_IOCTL_DEV_REPLACE_STATE_SUSPENDED:
1127		/*
1128		 * Scrub doing the replace isn't running so we need to do the
1129		 * cleanup step of btrfs_dev_replace_finishing() here
1130		 */
1131		result = BTRFS_IOCTL_DEV_REPLACE_RESULT_NO_ERROR;
1132		tgt_device = dev_replace->tgtdev;
1133		src_device = dev_replace->srcdev;
1134		dev_replace->tgtdev = NULL;
1135		dev_replace->srcdev = NULL;
1136		dev_replace->replace_state =
1137				BTRFS_IOCTL_DEV_REPLACE_STATE_CANCELED;
1138		dev_replace->time_stopped = ktime_get_real_seconds();
1139		dev_replace->item_needs_writeback = 1;
1140
1141		up_write(&dev_replace->rwsem);
1142
1143		/* Scrub for replace must not be running in suspended state */
1144		btrfs_scrub_cancel(fs_info);
```

1171-1195, `btrfs_dev_replace_suspend_for_unmount`. The STARTED arm is 1184-1188. The function body contains no `btrfs_scrub_cancel`.

```
1184	case BTRFS_IOCTL_DEV_REPLACE_STATE_STARTED:
1185		dev_replace->replace_state =
1186			BTRFS_IOCTL_DEV_REPLACE_STATE_SUSPENDED;
1187		dev_replace->time_stopped = ktime_get_real_seconds();
1188		dev_replace->item_needs_writeback = 1;
1189		btrfs_info(fs_info, "suspending dev_replace for unmount");
```

1235, in `btrfs_resume_dev_replace_async` (1198):

```
1235	if (!btrfs_exclop_start(fs_info, BTRFS_EXCLOP_DEV_REPLACE)) {
```

1259-1268, in `btrfs_dev_replace_kthread` (1249):

```
1259		"continuing dev_replace from %s (devid %llu) to target %s @%u%%",
1260		btrfs_dev_name(dev_replace->srcdev),
1261		dev_replace->srcdev->devid,
1262		btrfs_dev_name(dev_replace->tgtdev),
1263		(unsigned int)progress);

1265	ret = btrfs_scrub_dev(fs_info, dev_replace->srcdev->devid,
1266			      dev_replace->committed_cursor_left,
1267			      btrfs_device_get_total_bytes(dev_replace->srcdev),
1268			      &dev_replace->scrub_progress, false, true);
```

1278-1300, in `btrfs_dev_replace_is_ongoing` (1276). NEVER_STARTED, FINISHED, and CANCELED return false at 1282-1285. STARTED and SUSPENDED share the comment and break to `return true` at 1300.

```
1278	if (!dev_replace->is_valid)
1279		return false;
1280|
1281	switch (dev_replace->replace_state) {
1282	case BTRFS_IOCTL_DEV_REPLACE_STATE_NEVER_STARTED:
1283	case BTRFS_IOCTL_DEV_REPLACE_STATE_FINISHED:
1284	case BTRFS_IOCTL_DEV_REPLACE_STATE_CANCELED:
1285		return false;
1286	case BTRFS_IOCTL_DEV_REPLACE_STATE_STARTED:
1287	case BTRFS_IOCTL_DEV_REPLACE_STATE_SUSPENDED:
1288		/*
1289		 * return true even if tgtdev is missing (this is
1290		 * something that can happen if the dev_replace
1291		 * procedure is suspended by an umount and then
1292		 * the tgtdev is missing (or "btrfs dev scan") was
1293		 * not called and the filesystem is remounted
1294		 * in degraded state. This does not stop the
1295		 * dev_replace procedure. It needs to be canceled
1296		 * manually if the cancellation is wanted.
1297		 */
1298		break;
1299	}
1300	return true;
```

Full ranges are in the receipt `lines.txt`.

## GR2 clauses at these bytes

All 11 S247 quotes in the frozen GR2 row equal the stripped source line (`quote-check.txt`): 700, 701, 703, 1128, 1143, 1144, 1235, 1259, 1265, 1268, 1287.

Clauses that cite this file, and the lines that carry them:

- Start path copies through scrub: the comment and `btrfs_scrub_dev(fs_info, src_device->devid, 0, …, false, true)` are 700-703. Continue path: `btrfs_dev_replace_kthread` logs "continuing dev_replace" at 1259 and calls `btrfs_scrub_dev` on `dev_replace->srcdev->devid` with the same final two arguments `false, true` at 1265-1268. The argument spellings are in this file. The names `readonly` and `is_dev_replace` are the S242 signature quote (`scrub.c:3081`); this seat did not re-fetch `scrub.c`.
- `btrfs_dev_replace_is_ongoing` is false when `!is_valid` (1278-1279) and true for STARTED or SUSPENDED (1286-1287, return at 1300). The comment at 1288-1297 says the function returns true when the procedure was suspended by an umount and the target is missing.
- `btrfs_dev_replace_cancel` calls `btrfs_scrub_cancel` for STARTED at 1111, and again for SUSPENDED at 1144 (arm 1126-1144). The comment at 1127-1129, line 1128, says the scrub doing the replace isn't running; line 1143 says scrub for replace must not be running in the suspended state.
- `btrfs_dev_replace_suspend_for_unmount` (1171-1195) changes state only in the STARTED arm, to SUSPENDED, and sets `time_stopped` and `item_needs_writeback` at 1184-1188. It also logs at 1189. It does not call `btrfs_scrub_cancel`.
- The resume path takes the exclusive operation at 1235: `btrfs_exclop_start(fs_info, BTRFS_EXCLOP_DEV_REPLACE)` inside `btrfs_resume_dev_replace_async`.

Every GR2 clause that cites `dev-replace.c` is supported by these lines. The Limits paragraph (grounding lines 229-232) already says the S247 registration ranges omit 1111, 1126-1142, 1171-1195, and 1184-1188. Those lines are in the live file and match the sentences that cite them.

Clauses whose citations are `scrub.c`, `sysfs.c`, `ioctl.c`, or the btrfs-progs printing inference are outside this file. This seat did not re-fetch them.

No install. Receipts: `.ufo/waves/round-50/w1/R50ScoutReopenS247/` (`dev-replace.c`, `headers.txt`, `identity.txt`, `lines.txt`, `quote-check.txt`). Scratch removed.
