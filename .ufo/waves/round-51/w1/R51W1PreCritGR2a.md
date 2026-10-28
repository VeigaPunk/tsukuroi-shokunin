VERDICT: defect-found
SECTION SHA256: 27aa7abbb20087c531e55de77a3af4259c5ee056f668085c1d5138c70815d6ed

Scope: uncounted pre-read of row GR2 of corpus/knowledge/btrfs-scrub-grounding-r45.md at 2732ee6c06108c031c4d8043239b994e0504eb2f (entry lines 56-180, plus Limits 240-267 and Range gaps 269-275). Section hash confirmed by `check-scrub-admission-r51.py --section-hash --no-base-check` (GR2 27aa7abb…d6ed, matches).

## 0. Provenance and mechanical checks (observed)
- Snapshot digests `sha256sum -c SHA256SUMS`: all OK.
  - S247 `round-45/frozen/src/dev-replace.c` = f07ef0a0…4f3a (round-45 SHA256SUMS line 2)
  - S242 `round-44/frozen/src/scrub.c` = f347931b…a5b8
  - S243 `round-44/frozen/src/sysfs.c` = ce146120…1c43
  - S240 `round-43/frozen/src/ioctl.c` = 7b3488f2…ba01
- Mapping S-row to snapshot confirmed in `tools/lint-grounding-r51.py:45-47` and `corpus/SOURCES.md:249,251,252,256`.
- All four snapshots are Linux v7.2.11 per FETCH.txt (round-45 line 1-2 tag v7.2.11 peeled a2de78ee…; round-44 same; round-43 same).
- `lint-grounding-r51.py --revision 2732…`: verdict PASS; cites 28, cite_bad 0; quotes 63, quote_bad 0; gaps_computed 62, gap_ok 1; lint_ok 3; GR2: cites 20, quotes 39, problems [].
- Host capture (`round-45/frozen/hostcap/capture.txt`): line 1 `uid=1000 CapEff=0000000000000000`; line 9 `devinfo … devids=1`. Both host claims in GR2 match.

## 1. Defects

### D1 — universal "any" is false over the pinned order
- Clause (entry line 75-76): "any call, replace or not, is refused the same way while its device already carries a scrub context."
- Contradicted by source order: `scrub.c:3127-3133` (`if (!is_dev_replace && !readonly && !WRITEABLE) … ret = -EROFS;`) runs before the `dev->scrub_ctx` test at `scrub.c:3147-3153`. A non-replace, non-read-only start on a device that is not writeable and already has a scrub context returns `-EROFS`, not `-EINPROGRESS`. Likewise `scrub.c:3120-3123` (`-ENODEV`, missing device, non-replace) and `scrub.c:3138-3142` (`-EIO`, not in fs metadata or `REPLACE_TGT`) return first.
- Replacement wording: "any call that gets past the earlier checks (scrub.c:3094-3142), replace or not, is refused with `-EINPROGRESS` while its device already carries a scrub context; a call refused by an earlier check gets that earlier error instead."

### D2 — Host reading claims "replace state" is readable through sysfs; sysfs exposes less, and not for a suspended replace
- Clause (entry line 173-177): "Replace state is still readable without privilege through sysfs, which this capture does not record: the filesystem's `exclusive_operation` names `device replace` while a replace holds the exclusive operation (sysfs.c:1288 …), and `devinfo/<devid>/replace_target` reads 1 on the replace's target device (sysfs.c:2015)."
- Pinned bytes: the only replace-related sysfs output is the exclusive-operation name in `btrfs_exclusive_operation_show` (`round-44/frozen/src/sysfs.c:1265-1302`, `:1288` = `"device replace\n"`) and `replace_target` (`:2015`). A grep of the whole sysfs.c snapshot finds no `replace_state` or `dev_replace` reference, so replace state is not exposed.
- Counterexample: `round-45/frozen/src/dev-replace.c:1235-1242`: when `btrfs_exclop_start` fails, resume sets `replace_state` to SUSPENDED without holding the exclusive operation and returns. `btrfs_dev_replace_is_ongoing` still returns true for SUSPENDED (`dev-replace.c:1286-1287`; comment `:1288-1297`, which the entry's Statement relies on). Meanwhile `exclusive_operation` shows another operation or `none`, not `device replace`.
- Supported part: the world-readable mode (444) and the `none` / `0` values on this host are in `.ufo/waves/round-45/a2w1/C2ExecHostRecheck.md:84-89`; the entry's citation of that receipt is accurate.
- Replacement wording: "Replace activity is partly readable without privilege through sysfs, which this capture does not record: `exclusive_operation` names `device replace` while a replace holds the exclusive operation (sysfs.c:1265, :1288; the resume path takes it at dev-replace.c:1235, the replace ioctl around the start at ioctl.c:3190), and `devinfo/<devid>/replace_target` reads 1 on the replace's target device (sysfs.c:2015). Neither file reports replace_state, and neither shows a replace suspended without the exclusive operation (dev-replace.c:1235-1242), which the Statement counts as ongoing. On this host both files are mode 444 and read `none` and `0` (.ufo/waves/round-45/a2w1/C2ExecHostRecheck.md §3)."
- The added `sysfs.c:1265` must also be in the gap block (see D3).

### D3 — Range-gap block omits cited lines; the lint cannot see them (registry/gap defect)
- Clause(s) with implicit-file citations that `prose_cites` does not parse (`tools/lint-grounding-r51.py:77-78,167-186`; CONT_RE needs a comma, "and", ";" or whitespace directly before the colon, so `(:NNNN)`, `ret (:NNNN)`, `returned at :NNNN` are missed):
  - entry line 66: "(:3114-3116, returned at :3250-3253)" → scrub.c:3250-3253 is outside S242's declared ranges (`corpus/SOURCES.md:251`: 1365-1385, 3140-3162, 3215-3226, 3321-3337) and is absent from the gap block.
  - entry line 79: "(:3075-3078)"; line 80: "(:3080-3082)"; line 81: "(:3087-3090)", "(:3093-3095)" → ioctl.c lines 3076-3078, 3081-3082, 3087, 3089-3090, 3094-3095 are outside S240's declared ranges (`SOURCES.md:249`: 3066-3075, 3118-3140, 5578-5584) and absent from the block.
  - entry line 65: "(:3094-3095)" (inside the already-listed 3094-3139, harmless) and line 173 "-EPERM at :3133" (declared, harmless).
- Receipt with the full computation: `.ufo/waves/round-51/w1/R51W1PreCritGR2a/gr2-gap-recount.txt`.
- Replacement: make each implicit cite explicit (`ioctl.c:3075-3078`, `ioctl.c:3080-3082`, `ioctl.c:3087-3090`, `ioctl.c:3093-3095`, `scrub.c:3094-3095`, `scrub.c:3250-3253` after "returned at"), and set the block to:
```
### Range gaps (R51)

- S240 ioctl.c: 3076-3078, 3080-3082, 3084-3085, 3087-3090, 3093-3095, 3109-3110, 3115, 3190
- S242 scrub.c: 3081, 3094-3139, 3250-3253
- S243 sysfs.c: 1265, 1288, 2015
- S247 dev-replace.c: 1197
```
  The L1 must regenerate with `tools/lint-grounding-r51.py --emit-gaps` after the explicit-cite edit and confirm the output matches (the block above is my hand computation [inference: exact compress format not re-run]).
- Lint note for the L1: `lint-grounding-r51.py` reports PASS on this entry with 20 GR2 cites, but the gap check never sees the ten ioctl.c lines (3076-3078, 3081-3082, 3087, 3089-3090, 3094-3095) and the four scrub.c lines (3250-3253) that the entry cites outside its declared ranges and that the block omits. Its PASS does not establish the "every cited line" claim in the entry's Limits (lines 260-263).

## 2. Clauses checked and found supported (pinned bytes, path:line)
- Statement, start path: `round-45/frozen/src/dev-replace.c:700` comment, `:701-703` call with `src_device->devid`, `0`, `false, true`. Supported.
- Resume path: `dev-replace.c:1197` comment, function at 1198, kthread call `:1265-1268` with `srcdev->devid`, `false, true`. Supported.
- Signature: `round-44/frozen/src/scrub.c:3079-3081` `bool readonly, bool is_dev_replace)`. Supported.
- Check order inside btrfs_scrub_dev: `:3094-3095` EAGAIN on fs_closing; `:3109-3111` setup_ctx error; `:3114-3116` workers_get error with goto out_free_ctx; return via out_free_ctx at `:3250-3253`; `:3120-3123` ENODEV (missing only for non-replace); `:3127-3133` EROFS; `:3138-3142` EIO (not IN_FS_METADATA or REPLACE_TGT); `:3147-3153` EINPROGRESS (scrub_ctx, or non-replace and is_ongoing). Order and conditions match.
- `btrfs_dev_replace_is_ongoing`: `dev-replace.c:1278-1279` returns false when `!is_valid`; `:1286-1287` STARTED/SUSPENDED break to `return true`; comment `:1288-1297` supports that a suspended-by-unmount replace still counts. Supported (the switch does not enumerate every enum value, but "true when … started or suspended" is a sufficient condition the code shows).
- Non-replace clause "gets past the earlier checks … is refused with -EINPROGRESS and no scrub is started": `scrub.c:3159` is after `:3153`; supported (qualified by D1).
- ioctl clauses: `ioctl.c:3072-3073` CAP_SYS_ADMIN → -EPERM; `:3075-3078` extent-tree-v2 → -EINVAL; `:3080-3082` memdup_user; `:3084-3085` -EOPNOTSUPP; `:3087-3090` mnt_want_write_file when not read-only; `:3093-3095` btrfs_scrub_dev return into ret; `:3109-3110` -EFAULT on copy failure; `:3115` return ret. All inside `btrfs_ioctl_scrub` (3066-3116) and in the stated order. Supported.
- Progress query: `scrub.c:3321-3336` reads only `dev->scrub_ctx`; `:3336` `return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;`. No replace-state reference in 3321-3337. Supported.
- Attach/clear: `scrub.c:3159` `dev->scrub_ctx = sctx;` and `:3222` `dev->scrub_ctx = NULL;` with no return between them (checked 3159-3222). Supported.
- Host: `ioctl.c:3132-3133` CAP_SYS_ADMIN → -EPERM in `btrfs_ioctl_scrub_progress`. `capture.txt:1` CapEff 0; `capture.txt:9` devids=1. Supported.
- Exclusive-operation takers: `dev-replace.c:1235` (resume) and `ioctl.c:3190` (replace ioctl around start). Supported.
- `sysfs.c:1288` is `"device replace\n"` inside the exclop show switch; `sysfs.c:2015` is `!!test_bit(BTRFS_DEV_STATE_REPLACE_TGT)`. Supported as quoted (the function name is at 1265, see D2).
- Inference mark, entry line 90: "[inference: how btrfs scrub start and btrfs scrub status print these returns is not pinned here]". Correctly marked (no pinned print path). I found no other unmarked inference except the D2 overreach.
- Quotes: all GR2 quote lines match the pinned bytes at the cited line (lint quote_bad 0; I spot-checked 3081, 3094-3095, 3120, 3123, 3127, 3133, 3138-3139, 3147-3149, 3153, 3159, 3222, 3336, 3072, 3075, 3080, 3084-3085, 3088, 3093, 3109-3110, 3115, 1197, 1265, 1268, 1287, 2015).
- Ranges: none of the cited ranges runs into a neighbouring function (checked 1198, 1249, 1276-1301, 3079-3254, 3066-3116, 3321-3337).
- Universals "first"/"only"/"always": none in GR2 beyond D1's "any".

## 3. Not done
- Did not open the counter scripts or the w2 seats; not in this item's scope.
- Did not run a host probe (sysfs modes come from the existing receipt, not re-read live).
- No write outside the report path and the receipt directory.

Receipts: `.ufo/waves/round-51/w1/R51W1PreCritGR2a/gr2-gap-recount.txt`
Scratch removed after this report.
