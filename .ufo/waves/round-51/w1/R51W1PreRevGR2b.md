VERDICT: defect-found
SECTION SHA256: 27aa7abbb20087c531e55de77a3af4259c5ee056f668085c1d5138c70815d6ed

# R51W1PreRevGR2b — uncounted pre-read of GR2 (reviewer), revision 2732ee6c06108c031c4d8043239b994e0504eb2f

Scope: row GR2 of `corpus/knowledge/btrfs-scrub-grounding-r45.md` at 2732ee6c, plus its `### Range gaps (R51)` block and Limits, checked against the pinned bytes. Uncounted; negatives go to the pre-w2 amendment.

## Pre-checks (run)

- Entry extracted to `/fast/scratch/hyaku/tsukuroi-r51/R51W1PreRevGR2b/entry.md` (348 lines; GR2 = lines 56-180, Limits 240-268, Range gaps 269-275).
- Section hash: `python3 tools/check-scrub-admission-r51.py --revision 2732ee6c… --section-hash --no-base-check` → `"GR2": "27aa7abbb20087c531e55de77a3af4259c5ee056f668085c1d5138c70815d6ed"`, `structural_ok: 1`. Matches the item's value.
- Snapshot digests, `sha256sum -c SHA256SUMS` in each snapshot directory: all OK.
  - `.ufo/waves/round-45/frozen/src/` → dev-replace.c = **S247** (f07ef0a0…), cmdline/vsprintf/kstrtox = S246, systemd.kill.xml = S248.
  - `.ufo/waves/round-44/frozen/src/` → scrub.c = **S242** (f347931b…), sysfs.c = **S243** (ce146120…), btrfs-scrub@.service/timer, PKGBUILD = S244.
  - `.ufo/waves/round-43/frozen/src/` → ioctl.c = **S240** (7b3488f2…).
  - All three FETCH.txt files name tag v7.2.11 for these files.
- `python3 tools/lint-grounding-r51.py --revision 2732ee6c…` → `verdict PASS`, `lint_ok 3`, `quotes 63`, `quote_bad 0`, `cites 28`, `cite_bad 0`, `gaps_computed 62`, `gap_ok 1`, `gap_missing []`, `gap_extra []`. GR2: 39 quotes, 20 cites, no problems. The lint is clean, but see D1: it cannot see some GR2 citations.

## Defects

### D1 — Range gaps block omits cited lines (the lint is blind to them)

Clause, entry line 79-82 and 66: "… `-EINVAL` on an extent-tree-v2 filesystem (:3075-3078) … memdup_user … (:3080-3082) … (:3084-3085) … mnt_want_write_file … (:3087-3090). It then stores the `btrfs_scrub_dev` return in `ret` (:3093-3095) …" and line 66: "the error `scrub_workers_get` returned, if any (:3114-3116, returned at :3250-3253)".

Contradicting pinned lines:
- S240 declared ranges, `corpus/SOURCES.md:249`: `ioctl.c lines 3066-3075, 3118-3140, 5578-5584`. Lines 3076-3078, 3081-3082, 3087-3090 and 3094-3095 lie outside every declared range and are cited in prose, so they belong in the S240 gap line. The current S240 gap line (entry line 272) is `3080, 3084-3085, 3088, 3093, 3109-3110, 3115, 3190`.
- S242 declared ranges, `corpus/SOURCES.md:251`: `scrub.c lines 1365-1385, 3140-3162, 3215-3226, 3321-3337`. Lines 3250-3253 lie outside them and are cited (`returned at :3250-3253`, entry line 66). The current S242 gap line (entry line 273) is `3081, 3094-3139` and omits 3250-3253.
- Why the lint passes: `tools/lint-grounding-r51.py`, `prose_cites()` resolves a colon-led continuation only when it immediately follows a `basename:line` match (`CONT_RE`). Parenthesised `(:3075-3078)` and `returned at :3250-3253` are never resolved. I confirmed this by calling `prose_cites()` on entry lines 66 and 79-82: it yields `ioctl.c` 3072-3073, 3132, 3190 only, and no `scrub.c` 3250-3253 for line 66. Consequently `gap_ok 1` is not evidence for these lines.
- The Limits statement (entry line 257-263: "The range gaps of the rows' citations are not hand-listed: … lint --emit-gaps prints the block below") therefore overstates completeness.

Exact replacement. Either (a) write the basename on every citation so the lint counts it, e.g. `(ioctl.c:3075-3078)`, `returned at scrub.c:3250-3253`; and (b) replace the two gap lines and keep the rest of the block:

```
### Range gaps (R51)

- S237 scrub.c: 421, 439, 1546
- S240 ioctl.c: 3076-3078, 3080-3082, 3084-3085, 3087-3090, 3093-3095, 3109-3110, 3115, 3190
- S242 scrub.c: 3081, 3094-3139, 3250-3253
- S243 sysfs.c: 78, 1288, 1302, 2015, 2019
- S247 dev-replace.c: 1197
```

The `S243` line is needed only if D2 is adopted; without D2 keep `- S243 sysfs.c: 1288, 2015`. The `S237` line is GR3's and was not reviewed here; leave it as is. The S247 line is re-verified: declared `1143-1144, 1235, 1256-1268, 1276-1300` (SOURCES.md:256), so 1197 is the only gap. The S242 Limits enumeration (entry lines 252-254: "`scrub.c:3081, 3123, 3133 or 3139`") should also add `3250-3253` if the Limits list is kept.

### D2 — "readable without privilege" is not supported by the lines cited for it

Clause, entry lines 171-177: "Replace state is still readable without privilege through sysfs, which this capture does not record: the filesystem's `exclusive_operation` names `device replace` … (sysfs.c:1288 …), and `devinfo/<devid>/replace_target` reads 1 … (sysfs.c:2015)."

Contradicting/unsupported: sysfs.c:1288 (`str = "device replace\n";`) and sysfs.c:2015 (`val = !!test_bit(...)`) say what the value is, not who may read it. The world-readability comes from:
- `.ufo/waves/round-44/frozen/src/sysfs.c:76-78`: `#define BTRFS_ATTR(_prefix, _name, _show) … __INIT_KOBJ_ATTR(_name, 0444, _show, NULL)`;
- `sysfs.c:1302`: `BTRFS_ATTR(, exclusive_operation, btrfs_exclusive_operation_show);`;
- `sysfs.c:2019`: `BTRFS_ATTR(devid, replace_target, btrfs_devinfo_replace_target_show);`.
None of these are cited in GR2, and none sit in S243's declared ranges (`corpus/SOURCES.md:252`: `72-74, 2021-2049, 2113`). The host reading (`.ufo/waves/round-45/a2w1/C2ExecHostRecheck.md:84-89`, §3) shows both files `-r--r--r--` and reading `none` and `0` as uid 1000, so the host fact is supported, but not by the cited source lines.

Exact replacement for entry lines 171-177:

```
Replace state is still readable without privilege through sysfs, which this capture does not record: the attributes are
registered with `BTRFS_ATTR`, whose mode is 0444 (sysfs.c:78, `__INIT_KOBJ_ATTR(_name, 0444, _show, NULL)`; registrations
at sysfs.c:1302 and :2019). The filesystem's `exclusive_operation` names `device replace` while a replace holds the
exclusive operation (sysfs.c:1288; the resume path takes it at dev-replace.c:1235, and the replace ioctl takes it around
the start, S240 ioctl.c:3190), and `devinfo/<devid>/replace_target` reads 1 on the replace's target device (sysfs.c:2015).
```

The new citations (78, 1302, 2019) make the S243 gap line in D1 necessary.

## Clauses checked and found supported (against pinned bytes)

Statement (entry 58-62):
- dev-replace.c:700 comment `/* the disk copy procedure reuses the scrub code */` at 700; call `ret = btrfs_scrub_dev(fs_info, src_device->devid, 0, …, false, true);` at 701-703 inside the replace start function (`btrfs_dev_replace_start`, dev-replace.c:587). Supported.
- dev-replace.c:1197 is the comment above `btrfs_resume_dev_replace_async` (1198); the call with `srcdev->devid, committed_cursor_left, …, false, true` is at 1265-1268 inside `btrfs_dev_replace_kthread` (1249-1274). Supported; the 1197 citation points at the resume path, not the call, but the cited span is correct.
- scrub.c:3081 signature `bool readonly, bool is_dev_replace)`. Supported.

Ordering and returns of `btrfs_scrub_dev` (scrub.c:3079-3254; entry 64-76):
- Full return list between 3094 and 3159 is: 3095 (-EAGAIN), 3111 (setup_ctx error), 3116 (workers_get error → out_free_ctx 3250-3253), 3124 (-ENODEV via 3123), 3134 (-EROFS via 3133), 3143 (-EIO via 3142), 3154 (-EINPROGRESS via 3153). The ASSERTs at 3098-3106 do not return. So the "order before a scrub context is attached" list is complete. Supported.
- 3120-3123: `if (!dev || (MISSING && !is_dev_replace))` → `-ENODEV`. Supported.
- 3127-3133: `if (!is_dev_replace && !readonly && !WRITEABLE)` → `-EROFS`. Supported.
- 3138-3142: `IN_FS_METADATA` cleared or `REPLACE_TGT` set → `-EIO`. Supported.
- 3147-3153: `dev->scrub_ctx || (!is_dev_replace && btrfs_dev_replace_is_ongoing(...))` → `-EINPROGRESS`. Supported.
- "a scrub start that is not a replace … is refused with -EINPROGRESS and no scrub is started": the attach at 3159 is after 3153 and the early returns skip it. Supported.
- "any call, replace or not, is refused the same way while its device already carries a scrub context": 3147. Supported.
- `btrfs_dev_replace_is_ongoing` (dev-replace.c:1276-1301): `!is_valid` → false (1278-1279); NEVER_STARTED/FINISHED/CANCELED → false (1282-1285); STARTED/SUSPENDED → true (1286-1287, 1300). The comment at 1288-1297 says a replace suspended by an umount is still ongoing. Supported.
- Scrub-start ioctl `btrfs_ioctl_scrub` (ioctl.c:3067 header; the name is at 3066-3067 region `static long btrfs_ioctl_scrub(struct file *file, void __user *arg)`): `!capable(CAP_SYS_ADMIN)` 3072-3073 → `-EPERM`; extent-tree-v2 → `-EINVAL` 3075-3078; `memdup_user` 3080-3082; flags 3084-3085 → `-EOPNOTSUPP`; `mnt_want_write_file` 3087-3090 when not read-only. Order matches the code. Supported.
- ioctl.c:3093-3095 `ret = btrfs_scrub_dev(...)`; 3109-3110 `copy_to_user` → `-EFAULT`; 3115 `return ret;`. Supported.
- Progress query `btrfs_scrub_progress` (scrub.c:3321-3337): reads only `dev->scrub_ctx` (3328-3336); `return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;` at 3336. "alone, not from the replace state" is the code's behaviour. Supported.
- Context lifecycle: `dev->scrub_ctx = sctx;` at 3159; `dev->scrub_ctx = NULL;` at 3222 in the success path after `scrub_enumerate_chunks`. Supported.

Quotes: every GR2 quote is whole-line and equal to the cited source line (lint `quote_bad 0`); spot-checked against 3081, 3094-3095, 3120-3123, 3127, 3133, 3138-3139, 3147-3149, 3153, 3159, 3222, 3336, ioctl 3072-3075, 3084-3085, 3088, 3093, 3109-3110, 3115, dev-replace 700-703, 1197, 1235, 1265-1268, 1287, sysfs 1288, 2015. Supported.

Ranges (none runs into a neighbouring function): scrub.c 3094-3153 inside btrfs_scrub_dev; 3321-3336 inside btrfs_scrub_progress; ioctl.c 3072-3115 inside btrfs_ioctl_scrub; 3132-3133 inside btrfs_ioctl_scrub_progress; dev-replace.c 1265-1268 inside the kthread; 1288-1297 inside btrfs_dev_replace_is_ongoing. Supported.

Universals:
- "only" (Host reading, entry 116 region): capture.txt:9 `devinfo … devids=1` — one devid. Supported.
- "alone" (progress query): see above. Supported.
- "before" / "order": see ordering list. Supported.

`[inference]` marks:
- Entry line 90 `[inference: how btrfs scrub start and btrfs scrub status print these returns is not pinned here]`: correctly marked; the pinned bytes stop at the kernel return values. The sentence is an honest undecided point.
- The sentence "so while a replace copies from the source device that device carries the context the copy attached" (entry 88-89) is a direct consequence of scrub.c:3159/3222 and needs no mark.
- "So while a replace is ongoing in that sense …" (entry 73-76) follows from 1276-1300 and 3147-3153. No unmarked inference found.

Host reading (entry 171-173, 176-179):
- capture.txt:9 `devinfo … devids=1`: devid 1 only. Supported.
- capture.txt:1 `CapEff=0000000000000000`: no effective capabilities. Supported.
- ioctl.c:3132 `if (!capable(CAP_SYS_ADMIN))` and :3133 `return -EPERM;` in `btrfs_ioctl_scrub_progress`. Supported.
- "this capture does not record" replace state: capture.txt:1-9 has no exclusive_operation or replace_target line. Supported.
- sysfs.c:1288 and 2015 as named: see D2 (the citation supports the value, not the readability).
- "C2ExecHostRecheck on 2026-10-27 (§3), both files are mode 444 and read none and 0": `.ufo/waves/round-45/a2w1/C2ExecHostRecheck.md` §3 (line 76) lines 84-89 show `-r--r--r--`, `cat … replace_target` → `0`, `cat … exclusive_operation` → `none`. Supported (the host file, not capture.txt, is the source of this claim, and the entry says so).

Limits:
- "GR2's earlier device checks … were added at the round-45 integration" and the dated integration history: historical, not a GR2 clause; not checked further.

## Not done
- Did not read GR1/GR3 or the other row sources beyond what GR2 cites.
- Did not run the mutable tool beyond read-only lint and `--section-hash`; did not run the round-51 counter or any selftest (not in this item).
- Did not inspect the pre-w2 counters or controls.
- Did not verify `btrfs scrub start/status` userspace output (the entry marks this as inference).
- Did not check whether the `S237` gap line is correct (GR3 row, outside this item).

## Tooling and scratch
- No tools installed. No writes to the fleet or lane tree. Scratch `/fast/scratch/hyaku/tsukuroi-r51/R51W1PreRevGR2b/` (holds only `entry.md`, removed at finish).
