VERDICT: defect-found
SECTION SHA256: 27aa7abbb20087c531e55de77a3af4259c5ee056f668085c1d5138c70815d6ed

Scope: uncounted pre-read of row GR2 of corpus/knowledge/btrfs-scrub-grounding-r45.md at 2732ee6c06108c031c4d8043239b994e0504eb2f (entry extracted with `git show`, 348 lines; GR2 = lines 56-180; Limits 240-268; Range gaps 269-276).

## Preliminaries (observed)

- `check-scrub-admission-r51.py --revision 2732ee6c… --section-hash --no-base-check` prints GR2 `27aa7abbb20087c531e55de77a3af4259c5ee056f668085c1d5138c70815d6ed`. Matches the brief.
- `lint-grounding-r51.py --revision 2732ee6c…`: verdict PASS, lint_ok 3, rows_clean 3, GR2: cites 20, quotes 39, cite_bad 0, quote_bad 0, problems []; gap_ok 1, gaps_computed 62.
- Snapshot digests (`sha256sum -c SHA256SUMS`, all OK) and S-row mapping:
  - S247 `dev-replace.c` = `.ufo/waves/round-45/frozen/src/dev-replace.c`, sha f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a
  - S242 `scrub.c` = `.ufo/waves/round-44/frozen/src/scrub.c`, sha f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8
  - S243 `sysfs.c` = `.ufo/waves/round-44/frozen/src/sysfs.c`, sha ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43
  - S240 `ioctl.c` = `.ufo/waves/round-43/frozen/src/ioctl.c`, sha 7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01
- Host capture `.ufo/waves/round-45/frozen/hostcap/capture.txt`: line 1 `CapEff=0000000000000000`; line 9 `devinfo … devids=1`.

## Defects

### D1 (certain): universal "any call" overstates the context refusal

Entry (GR2, paragraph 2 of the scrub-start discussion): "any call, replace or not, is refused the same way while its device already carries a scrub context."

Contradicted by the code order. The `dev->scrub_ctx` test (scrub.c:3147) runs only after the earlier returns:
- `scrub.c:3120-3123`: a non-replace call on a MISSING device gets `-ENODEV` (`if (!dev || (test_bit(BTRFS_DEV_STATE_MISSING…) && !is_dev_replace))`).
- `scrub.c:3127-3133`: a non-replace, non-readonly call on a not-WRITEABLE device gets `-EROFS` before the context test.
- `scrub.c:3138-3142`: any call on a device not in fs metadata or flagged REPLACE_TGT gets `-EIO` before the context test.

So a context-carrying device does not yield `-EINPROGRESS` for every call. Proposed exact replacement of the sentence:
"any call, replace or not, that gets past the earlier checks is refused the same way while its device already carries a scrub context."

### D2 (citation, medium): "reads 1 on the replace's target device" cites only the reader

Entry (Host reading): "`devinfo/<devid>/replace_target` reads 1 on the replace's target device (sysfs.c:2015)."

`sysfs.c:2015` is `val = !!test_bit(BTRFS_DEV_STATE_REPLACE_TGT, &device->dev_state);` (round-44 snapshot). It proves what the file reads, not that the replace's target carries the bit. The set sites are in the S247 snapshot and are uncited:
- `.ufo/waves/round-45/frozen/src/dev-replace.c:309` `set_bit(BTRFS_DEV_STATE_REPLACE_TGT, &device->dev_state);` (inside `btrfs_init_dev_replace_tgtdev`, lines 232-337)
- `dev-replace.c:209-210` `set_bit(BTRFS_DEV_STATE_REPLACE_TGT, &dev_replace->tgtdev->dev_state);`
- clear: `dev-replace.c:970` `clear_bit(BTRFS_DEV_STATE_REPLACE_TGT, &tgt_device->dev_state);` (inside `btrfs_dev_replace_finishing`, 859-)

Proposed replacement (keeps the claim, makes it pinned):
"`devinfo/<devid>/replace_target` reads the replace-target bit (sysfs.c:2015), which the start path sets on the target device (dev-replace.c:309) and the finish path clears (dev-replace.c:970); on the replace's target device it reads 1."
Lint note: adding 309 and 970 to the cited set changes the generated `### Range gaps (R51)` block (S247 entry); regenerate with `lint-grounding-r51.py --emit-gaps`. I did not check whether S247's declared ranges already include 309 or 970.

### D3 (citation, low): attribute names are not cited to their registrations

Entry: "the filesystem's `exclusive_operation` names `device replace`" cites only `sysfs.c:1288`; "`devinfo/<devid>/replace_target`" cites only `sysfs.c:2015`. The cited lines show the string and the bit, not the file names.
- `sysfs.c:1265` `static ssize_t btrfs_exclusive_operation_show`; `sysfs.c:1302` `BTRFS_ATTR(, exclusive_operation, btrfs_exclusive_operation_show);`
- `sysfs.c:2007` `static ssize_t btrfs_devinfo_replace_target_show`; `sysfs.c:2019` `BTRFS_ATTR(devid, replace_target, btrfs_devinfo_replace_target_show);`

Proposed: in the Host reading, write "the filesystem's `exclusive_operation` (sysfs.c:1265, :1288, registered at :1302) names `device replace`" and "`devinfo/<devid>/replace_target` (sysfs.c:2007, :2015, registered at :2019)". Same lint-gap regeneration note as D2.

### D4 (wording, low): devid list is not a reason for lack of reach

Entry: "The filesystem lists devid 1 only (capture.txt:9) and the caller has no effective capabilities (capture.txt:1), so the privileged progress query is out of its reach (the CAP_SYS_ADMIN check … ioctl.c:3132, `-EPERM` at :3133)."
The reach is set by the capability check alone (`ioctl.c:3132-3133`; `capture.txt:1` CapEff=0). The devid list does not bear on it.
Proposed replacement: "The caller has no effective capabilities (capture.txt:1), so the privileged progress query is out of its reach (the CAP_SYS_ADMIN check in the scrub-progress ioctl, ioctl.c:3132, `-EPERM` at :3133)."

## Clauses checked and found supported (read at pinned bytes)

- Statement call sites: `dev-replace.c:700` comment and `:701-703` in `btrfs_dev_replace_start` (587-858): devid `src_device->devid`, `0`, total bytes, progress, `false, true`. `:1197` comment above `btrfs_resume_dev_replace_async` (1198); `:1265-1268` in `btrfs_dev_replace_kthread` (1249-1274): `srcdev->devid`, `committed_cursor_left`, total bytes, progress, `false, true`. `scrub.c:3081` signature `bool readonly, bool is_dev_replace)`.
- Order and conditions of `btrfs_scrub_dev` (scrub.c:3094-3153): `-EAGAIN` on `btrfs_fs_closing` (3094-3095); `scrub_setup_ctx` error (3109-3111); `scrub_workers_get` error (3114-3116, `goto out_free_ctx`, returns `ret` at 3250-3253); `-ENODEV` (3120-3123); `-EROFS` (3127-3133); `-EIO` (3138-3142); `-EINPROGRESS` (3147-3153). Order in the entry matches code order.
- "a present device, writeable unless read-only, in the filesystem metadata, not the replace target" matches the checks at 3120, 3127-3128, 3138-3139 for a non-replace call.
- `btrfs_dev_replace_is_ongoing` (dev-replace.c:1276-1300): `!is_valid` → false (1278-1279); NEVER_STARTED/FINISHED/CANCELED → false; STARTED/SUSPENDED → true (1286-1287); suspended-by-unmount comment at 1288-1297. `__pure` declared at 1276.
- Scrub context lifetime: `dev->scrub_ctx = sctx` at scrub.c:3159, `dev->scrub_ctx = NULL` at 3222. No `return` or `goto` in scrub.c:3160-3214 (grep empty) and 3215-3222 is straight-line, so the attached context is cleared on every path after 3159. The sentence "while a replace copies from the source device that device carries the context the copy attached" is supported.
- Scrub-start ioctl (ioctl.c:3066-3115): `CAP_SYS_ADMIN` `-EPERM` (3072-3073); extent-tree-v2 `-EINVAL` (3075-3078); `memdup_user` error (3080-3082); `-EOPNOTSUPP` (3084-3085); `mnt_want_write_file` when not READONLY (3087-3090); call and `ret` store (3093-3095); copy-back and `-EFAULT` (3109-3110); `return ret` (3115). All as stated.
- Progress query `btrfs_scrub_progress` (scrub.c:3321-3336): reads only `dev->scrub_ctx`; `return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV` at 3336. "answers from the device's scrub context alone" is supported.
- Host: `ioctl.c:3132-3133` CAP_SYS_ADMIN and `-EPERM` in `btrfs_ioctl_scrub_progress` (3126); `capture.txt:1` CapEff=0; `capture.txt:9` devids=1.
- Resume exclusive-op: `dev-replace.c:1235` `btrfs_exclop_start(… BTRFS_EXCLOP_DEV_REPLACE)` in the resume path. Ioctl exclusive-op: `ioctl.c:3190` start, held around `btrfs_dev_replace_by_ioctl` (3193) and finished at 3194.
- `sysfs.c:1265-1296`: the exclusive_operation show function maps `BTRFS_EXCLOP_DEV_REPLACE` to `"device replace\n"` (1287-1288); no `capable()` check in the lines read, so the read needs no privilege.
- Mode and values "mode 444 and read `none` and `0`": recorded by `.ufo/waves/round-45/a2w1/C2ExecHostRecheck.md` §3 (`ls -l` shows `-r--r--r--`; `cat` gives `none` and `0`). Not re-run by me: the item's execution class names no sysfs read. The entry's sentence matches that file. The capture does not record these values, and the entry says so.
- Universal words: "alone" (progress query), "only" (devid list, capture.txt:9), "if any" (setup and workers errors) are supported; "first" does not occur in the row.
- The one `[inference: …]` mark (how `btrfs scrub start`/`status` print returns) is honest; no other unmarked sentence is an inference except the D2 replace_target claim.

## Not done

- Did not run the sysfs reads or any ioctl on the host (outside the named commands).
- Did not check whether S247's declared ranges already include dev-replace.c:309 or :970, nor the SOURCES row text.
- Did not read Limits for claims beyond the context needed for GR2; Limits and GR3/GR1 not reviewed here.
- No tool was installed.
