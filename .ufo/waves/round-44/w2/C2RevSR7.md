ROW SR7 VERDICT: holds

Seat C2RevSR7, counted read of row SR7 in `corpus/knowledge/btrfs-scrub-record-r44.md` at
8eee79db608b5815c325a5af7cbfdeac50eda9f4 (lines 15-54). Every sentence checked against its deciding
source line in the pinned files; every quote verified verbatim at its cited line; the host reading
matched against the S245 capture. Working copy: /fast/scratch/hyaku/tsukuroi-r44/C2RevSR7/sr7-doc.md.

## Source integrity

- S242 `.ufo/waves/round-44/frozen/src/scrub.c`: `sha256sum -c SHA256SUMS` -> OK (scrub.c, sysfs.c,
  btrfs-scrub@.timer, btrfs-scrub@.service, PKGBUILD all OK).
- S237 `.ufo/waves/round-42/frozen/src/scrub.c` sha256 48df2e2f...f0801 matches SOURCES.md pin (btrfs-progs v7.1 cmds/scrub.c).
- S240 `.ufo/waves/round-43/frozen/src/ioctl.c` sha256 7b3488f2...ba01 matches SOURCES.md pin (Linux v7.2.11 fs/btrfs/ioctl.c).
- S245 `.ufo/waves/round-44/frozen/hostcap/capture.txt` sha256 efb52388...4900 matches the doc header's digest.

## Sentence-by-sentence

1. "a device carries a scrub context exactly while a scrub or device-replace run is in progress on
   it" — HOLDS. The only `scrub_ctx` writes in S242 scrub.c are 3159 (`dev->scrub_ctx = sctx;`) and
   3222 (`dev->scrub_ctx = NULL;`), both inside `btrfs_scrub_dev` (line 3313 is a wait predicate, not
   a write). `btrfs_scrub_dev` is the single engine for both scrub and replace (checked upstream
   v7.2.11 dev-replace.c: `btrfs_scrub_dev(fs_info, src_device->devid, 0, ..., false, true)` at
   lines 701-703 and `btrfs_scrub_dev(fs_info, dev_replace->srcdev->devid, ..., false, true)` at
   lines 1265-1268 — both on the source device, both `is_dev_replace=true`). The context lives for
   exactly the duration of the run on that device.
2. "btrfs_scrub_dev refuses with -EINPROGRESS when dev->scrub_ctx is already set" — HOLDS.
   scrub.c:3147 `if (dev->scrub_ctx ||` -> 3153 `ret = -EINPROGRESS;` (compound condition also covers
   a non-replace scrub racing an ongoing replace via `btrfs_dev_replace_is_ongoing`; the
   dev->scrub_ctx arm is exactly as stated).
3. "attaches its context at scrub.c:3159 after all refusal checks and before any scrub work" — HOLDS.
   Order in the pinned file: EAGAIN (3096), IS_ERR(sctx) (3106-3107), workers (3110-3112), ENODEV
   (3117-3123), EROFS (3126-3135), EIO (3139-3145), EINPROGRESS (3147-3157), then 3159
   `dev->scrub_ctx = sctx;`, then the first work call `scrub_supers` at 3190 and
   `scrub_enumerate_chunks` at 3199. Intervening lines (3158, 3160-3168) are bookkeeping/pause
   checks, not scrub work.
4. "clears it at scrub.c:3222 once the scrub work has ended, before the function's finalize tail" —
   HOLDS. 3222 `dev->scrub_ctx = NULL;` follows `scrub_enumerate_chunks` (3199) and precedes
   `scrub_workers_put` (3225), `scrub_put_ctx` (3226) and the need_commit tail (3229-3246).
5. "every return path leaves the field as it found it" — HOLDS. All returns before 3159 (the
   out:/out_free_ctx: labels and direct returns) precede the only attach, so dev->scrub_ctx is
   unchanged — including the EINPROGRESS path which preserves the existing owner's context. Every
   path after 3159 passes 3222, restoring NULL = the value the field necessarily had at entry for an
   attach to occur (a non-NULL field exits at 3153).
6. "btrfs_scrub_dev serves both a scrub and a device replace (its is_dev_replace argument)" — HOLDS.
   Signature at 3079-3081 ends `bool readonly, bool is_dev_replace)`; the is_dev_replace branches are
   visible at 3119, 3126, 3148, 3175, 3204.
7. Bracketed inference "[its caller is in fs/btrfs/dev-replace.c, opened this round at v7.2.11 lines
   701-703 and 1265-1268 but not pinned]" — correctly hedged AND correct: fetched upstream v7.2.11
   dev-replace.c (sha256 f07ef0a0...34f3a) shows exactly those call sites at exactly those lines,
   each passing `true` as the last argument on the source device.
8. "btrfs_scrub_progress looks the requested devid up under device_list_mutex; it copies that
   context's stat and returns 0 only when the device exists and carries a context, returns -ENOTCONN
   when the device exists without one, and -ENODEV when no device has that devid" — HOLDS.
   scrub.c:3328 `mutex_lock(&fs_info->fs_devices->device_list_mutex)` -> 3329 `btrfs_find_device`
   -> 3330-3331 `if (dev) sctx = dev->scrub_ctx;` -> 3332-3333 `if (sctx) memcpy(progress,
   &sctx->stat, sizeof(*progress));` -> 3336 `return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;`.
   The three-way return is verbatim from the source.
9. "The progress ioctl handler (after its CAP_SYS_ADMIN gate, SR6) returns that value and copies the
   arguments back to the caller only when it is 0" — HOLDS. S240 ioctl.c:3132-3133
   `if (!capable(CAP_SYS_ADMIN)) return -EPERM;`, 3139 `ret = btrfs_scrub_progress(fs_info,
   sa->devid, &sa->progress);`, 3141 `if (ret == 0 && copy_to_user(arg, sa, sizeof(*sa)))`, 3144
   `return ret;`. copy_to_user runs only under ret==0; the kernel value is returned (the implicit
   -EFAULT-on-copy-fault convention needs no spelling out).
10. "for a privileged btrfs scrub status, is_scrub_running_in_kernel (SR6) answers 1 exactly when
    some device it asks about is being scrubbed, or is the source of a running replace, at that
    moment: an idle device answers ENOTCONN, never 0, and the answer is a momentary per-device
    reading, not a record of past scrubs" — HOLDS. S237 cmds/scrub.c:1190-1204 iterates di_args
    devids and returns 1 on the first BTRFS_IOC_SCRUB_PROGRESS ioctl returning 0; any nonzero result
    (ENOTCONN idle, ENODEV unknown, EPERM unprivileged) is skipped. Kernel-side, ret==0 means the
    device carries a live scrub_ctx = in-progress scrub or (verified above) source of a running
    replace. Call sites 1378 (stale-status check) and 1946 (status in_progress) confirm the
    status-command context; scrub_ctx is cleared at run end so the reading is momentary, never a
    record of past scrubs.

## Quote check

All ten quotes hold verbatim at the cited lines of pinned S242 (leading whitespace stripped per the
file's quote convention, consistent across all rows): 3081, 3147, 3153, 3159, 3222, 3321, 3331,
3333, 3336 — each confirmed byte-identical after tab strip via `sed -n '<n>p' | cat -A`.
S240 quotes at ioctl.c:3139 and 3141 identical. Line numbers all land on the quoted text.

## Host reading

"Not observable unprivileged: the caller has no effective capabilities (capture.txt:1), so the ioctl
stops at the SR6 gate before this code runs (round-43 S241)" — HOLDS. capture.txt:1 reads
`captured 2026-10-26T23:53:22Z uid=1000 CapEff=0000000000000000`; the SR6 gate is S240
ioctl.c:3132-3133 `!capable(CAP_SYS_ADMIN) -> -EPERM`, before memdup_user/progress call; SOURCES.md
S241 records the round-43 EPERM observation on this host.

## Proposed text

None. Row SR7 stands as written; no narrowing needed.
