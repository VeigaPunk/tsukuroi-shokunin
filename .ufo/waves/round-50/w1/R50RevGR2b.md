ROW GR2 VERDICT: holds
SECTION SHA256: a2e955cefbd110ced928407c79b2cedb3cc431734487aa29e74682b23aeb7f3f

# R50RevGR2b — counted reviewer, row GR2 (claim C1)

Bytes under test: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 8029cdba1049df25632c91a23c8db4eefb54be5f:corpus/knowledge/btrfs-scrub-grounding-r45.md`
extracted to `/fast/scratch/hyaku/tsukuroi-r50/R50RevGR2b/entry.md` (307 lines). Row GR2 = entry lines 56-152
(`## GR2` up to the blank line before `## GR3` at :153). Section hash recomputed independently (lines 56-152 joined
with LF) = `a2e955cefbd110ced928407c79b2cedb3cc431734487aa29e74682b23aeb7f3f`, matching
`tools/check-scrub-admission-r50.py --section-hash` (`{"GR2": "a2e955ce…f3f", "structural_ok": 1}`). Stripping the
trailing blank line would give a different hash (`e41b3b6b…`), so the counter's convention is the plain join, as
the item states.

## Snapshot identity and S-row mapping (all digests verified)

`sha256sum -c SHA256SUMS` exits 0 in all three directories:

| S-row | file | snapshot | sha256 |
|---|---|---|---|
| S247 | `dev-replace.c` | `.ufo/waves/round-45/frozen/src/` | `f07ef0a0…034f3a` OK |
| S242 | `scrub.c` | `.ufo/waves/round-44/frozen/src/` | `f347931b…38ca5b8` OK |
| S243 | `sysfs.c` | `.ufo/waves/round-44/frozen/src/` | `ce146120…4f731c43` OK |
| S240 | `ioctl.c` | `.ufo/waves/round-43/frozen/src/` | `7b3488f2…d4534ba01` OK |

Version provenance: `round-45/frozen/src/FETCH.txt:3` `GET …?h=v7.2.11 -> dev-replace.c`; `round-44/frozen/src/FETCH.txt`
(`scrub.c`, `sysfs.c` at tag v7.2.11, peeled `a2de78ee…`); `round-43/frozen/src/FETCH.txt:2` `ioctl.c <- …/v7.2.11/fs/btrfs/ioctl.c`.
So "In Linux v7.2.11" (entry:58) is provenance-backed, not assumed.

## Clause-by-clause against the pinned bytes

All 29 `**Quote.**` lines were compared programmatically to the cited snapshot line (leading/trailing whitespace
stripped): 29/29 exact matches, 0 mismatches. Individually re-read clauses:

1. Replace drives the scrub code (entry:58-60). `dev-replace.c:700` comment "the disk copy procedure reuses the scrub
   code"; `dev-replace.c:701-703` `btrfs_scrub_dev(fs_info, src_device->devid, 0, …, &dev_replace->scrub_progress,
   false, true)`; resume path `dev-replace.c:1265-1268` same with `dev_replace->srcdev->devid`. Last two params of the
   signature at `scrub.c:3079-3081` are `readonly, is_dev_replace` — the row's "the last two parameters" is exact.
   A grep for `btrfs_scrub_dev(` over the four pinned files finds exactly two calls with `is_dev_replace` true
   (`dev-replace.c:701`, `:1265`) plus the ioctl call with `false` (`ioctl.c:3093-3095`); "both" (entry:59) is
   complete for the pinned replace code.
2. Errno order inside `btrfs_scrub_dev` (entry:60-66) — `scrub.c:3094-3095` `-EAGAIN` (`btrfs_fs_closing`) is the
   first return after the non-returning `progress->last_physical` store at :3091-3092; `:3109`/`:3114`
   `scrub_setup_ctx` / `scrub_workers_get` with `goto out_free_ctx`; then `:3120-3123` `-ENODEV`
   (`!dev || (MISSING && !is_dev_replace)`), `:3127-3133` `-EROFS` (`!is_dev_replace && !readonly && !WRITEABLE`),
   `:3138-3142` `-EIO` (`!IN_FS_METADATA || REPLACE_TGT`). The row's per-clause conditionals match the source
   conjuncts one for one, including "a missing device on a non-replace call" and "non-replace, non-readonly".
3. `-EINPROGRESS` ordering and conditions (entry:66-72). `scrub.c:3147-3153`: `dev->scrub_ctx || (!is_dev_replace &&
   btrfs_dev_replace_is_ongoing(...))` → `-EINPROGRESS`. The row's "Only after those checks" is the literal code
   order (the EIO test at :3138 precedes the rwsem read at :3146). `is_ongoing` itself: `dev-replace.c:1278-1279`
   (`if (!dev_replace->is_valid) return false;`), `:1286-1287` (STARTED/SUSPENDED cases break to `return true` at
   :1300), `:1288-1297` the comment that a replace suspended by an umount still returns true. The row's
   "which it is when … valid … and the state is started or suspended" is a correct restatement; no other enum value
   reaches the `break` (NEVER_STARTED/FINISHED/CANCELED return false at :1282-1285).
4. "no scrub is started" (entry:72) — both `-EINPROGRESS` exits `goto out` before `sctx->readonly = readonly;
   dev->scrub_ctx = sctx;` at `scrub.c:3158-3159`.
5. Context on the source device (entry:73-74) — `scrub.c:3159` `dev->scrub_ctx = sctx;` where `dev` is the device
   found by the source devid at :3119. Correct.
6. Cancel path (entry:74-77) — `dev-replace.c:1107-1111` STARTED case calls `btrfs_scrub_cancel(fs_info)`;
   `:1126-1144` SUSPENDED case calls it at `:1144` under the comment at `:1143` "Scrub for replace must not be
   running in suspended state"; the row's "although the pinned code says the replace scrub is not running in that
   state" cites `:1127-1129` verbatim ("Scrub doing the replace isn't running so we need to do the …"). The row does
   not claim the code is self-consistent — it reports the tension, which is what the bytes show.
7. Progress query (entry:78-80) — `scrub.c:3336` `return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;` decides both
   clauses; `scrub.c:3222` `dev->scrub_ctx = NULL;` is the site that makes the context absent after a copy. Both
   citations exist and bear on the clause.
8. Unmount suspend path (entry:81-83) — `dev-replace.c:1171-1195` is exactly `btrfs_dev_replace_suspend_for_unmount`
   (signature :1171, closing brace :1195); only the STARTED case (:1184) assigns SUSPENDED (:1185-1186),
   `time_stopped` (:1187) and `item_needs_writeback = 1` (:1188). No `btrfs_scrub_cancel` anywhere in :1171-1195.
   Range boundaries: no cited range runs into the next function (`:1126-1144`, `:1171-1195`, `:1278-1279`,
   `:1286-1287`, `:1288-1297`, `ioctl.c:3093-3095`, `:3109-3110`, `:3132-3133` all close inside their own body).
9. `[inference]` bracket (entry:84-86) — only "how `btrfs scrub start` and `btrfs scrub status` print these returns
   is not pinned here" is marked, and it is true: no btrfs-progs source is pinned anywhere in S237/S240/S242/S243/
   S246/S247/S248/S249. The ioctl conjunct is now asserted as pinned and is backed: `ioctl.c:3093-3095` call,
   `:3109-3110` `if (copy_to_user(...)) ret = -EFAULT;`, `:3115` `return ret;`.
10. Host reading (entry:88-96) — `capture.txt:1` `captured 2026-10-27T02:09:52Z uid=1000 CapEff=0000000000000000`
    (digest `f5958a83…3991e70` matches the `source:` line), `capture.txt:9` `devinfo … devids=1`. `CAP_SYS_ADMIN`
    gate at `ioctl.c:3132`, `-EPERM` at `:3133`. `sysfs.c:1288` `str = "device replace\n";` inside
    `btrfs_exclusive_operation_show` (`:1265`, registered `:1302`); `sysfs.c:2015` the `REPLACE_TGT` test;
    `ioctl.c:3190` `btrfs_exclop_start(fs_info, BTRFS_EXCLOP_DEV_REPLACE)`; `dev-replace.c:1235` the resume path's
    take. `grep -c 'exclusive_operation\|replace_target' capture.txt` = 0, so "which this capture does not record"
    is exact. The cited seat report exists: `.ufo/waves/round-45/a2w1/C2ExecHostRecheck.md:76` is "## 3", :84-89
    show both attributes `-r--r--r--` (444) reading `0` and `none` as `uid 1000, CapEff=0000000000000000` (:81),
    and :156 dates those readings 2026-10-27 — matching the row's "mode 444 and read `none` and `0`" and its date.

Universal words: "Only after those checks" (entry:66) and "only moves a STARTED replace" (entry:82) both match the
code order/branching; "does not call `btrfs_scrub_cancel`" is true of :1171-1195. No universal word overreaches.

## The four round-49 corrections, checked against bytes (not taken on trust)

1. `[inference]` scoping — now "how `btrfs scrub start` and `btrfs scrub status` print these returns is not pinned
   here" (entry:84-85); the ioctl conjunct is outside the unverifiable part and is verified at `ioctl.c:3093-3095`,
   `:3109-3110`, `:3115`. Holds.
2. S240 named — `source:` line (entry:1) carries "S240 is Linux v7.2.11 `fs/btrfs/ioctl.c`, snapshot
   `.ufo/waves/round-43/frozen/src/ioctl.c`, sha256 7b3488f2…ba01 (round 50: the row cites it at ioctl.c:3093-3095,
   :3109-3110, :3115, :3132-3133 and :3190)"; QUALITY item 7 (:261-262) reads "External claims cite S246-S248 and
   S240". The digest matches `round-43/frozen/src/SHA256SUMS`. Holds.
3. dev-replace.c:1128 prefix — the quote in GR2 (entry:128) is `* Scrub doing the replace isn't running so we need
   to do the`; snapshot line 1128 is `\t\t * Scrub doing the replace isn't running so we need to do the`, so the
   `* ` prefix is now carried (the round-49 defect was its absence). Holds.
4. S247/S240 range gaps declared — `## Limits` :229-232 declares that the widened S247 ranges do not list
   `dev-replace.c:1111`, `:1126-1142`, `:1171-1195`, `:1184-1188`, and :233-235 declares S240's ranges do not list
   `ioctl.c:3093-3095`, `:3109-3110`, `:3115`, `:3190`. Both gaps are real against the row's citations, and both are
   now stated. Holds. (Limits is outside the GR2 section, so it does not enter the section hash; I checked it because
   the item names the correction.)

## Not a defect, recorded so it is not mistaken for one

The bracket's ioctl sentence (entry:85-86) says the scrub-start ioctl "returns the `btrfs_scrub_dev` value … unless
the argument copy fails". The function also returns before the call on `sa->flags & ~BTRFS_SCRUB_SUPPORTED_FLAGS`
(`ioctl.c:3084-3085`, `-EOPNOTSUPP`), on `memdup_user` failure (`:3080-3082`) and on `mnt_want_write_file`
(`:3088-3090`). Those gates cannot intercept a start that reaches `btrfs_scrub_dev`, which is the sentence's
subject, so the clause is not false; a maximally literal reading of "unless" is incomplete. If the L1 wants it
airtight, the minimal edit is to append `(the flags check at ioctl.c:3084-3085 and mnt_want_write_file at :3088-3090
return before the call)`. I did not count this as a defect because no clause of the row's kernel claim depends on it.

## Verified but not re-derived, and not done

- I did not re-run `capture.sh` or re-read sysfs live; the host values (`none`, `0`, mode 444) are the cited seat's
  readings of 2026-10-27T03:24:32Z, checked for internal consistency, not re-measured by me.
- I did not re-fetch the kernel tag; v7.2.11 rests on the three snapshots' `FETCH.txt` plus the digest check.
- I did not census `btrfs_scrub_dev` callers outside the four pinned files (no other replace/scrub file is pinned);
  "both" is verified for the pinned replace code only.
- I did not read btrfs-progs sources (none pinned) — that is exactly what the `[inference]` mark covers.
- I ran no counter leg other than `--section-hash`; the C1 predicate as a whole is other seats' scope.
