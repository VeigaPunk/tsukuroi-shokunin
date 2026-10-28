ROW GR2 VERDICT: holds
SECTION SHA256: d4296085a574e29296fb9baba5a8722766a832a0b15809ccee72ea019ebd027f

# ROW GR2 — reviewer read at the freeze (C1-COUNTED)

Entry: `corpus/knowledge/btrfs-scrub-grounding-r45.md` at `55c07cd3f8bff2e12117c34d57b4c618de74d85c`,
row lines 56-151 extracted with `git show 55c07cd3:…` into scratch (`entry.md`, 287 lines). I did not write
the row and am not its author.

## Snapshot provenance and digests (checked first)

`sha256sum -c SHA256SUMS` in each snapshot directory: round-45 `src/` 5/5 OK (incl. `dev-replace.c` =
`f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a`), round-44 `src/` 5/5 OK
(`scrub.c` = `f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8`,
`sysfs.c` = `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43`), round-43 `src/`
1/1 OK (`ioctl.c` = `7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01`). S-row map,
from `round-45/frozen/src/FETCH.txt` and `round-44/frozen/src/FETCH.txt`: **S247 = dev-replace.c**,
**S242 = scrub.c**, **S243 = sysfs.c** (`FETCH.txt`: "`fs/btrfs/scrub.c … -> S242`",
"`fs/btrfs/sysfs.c … -> S243`"); **S240 = ioctl.c** (`round-43/frozen/src/FETCH.txt`: "ioctl.c <- …
v7.2.11/fs/btrfs/ioctl.c"). All four are v7.2.11 per those FETCH files (tag `v7.2.11`, peeled
`a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea`).

## Section hash, my convention (checked, and it differs from a literal reading)

`python3 tools/check-scrub-admission-r49.py --revision 55c07cd3… --section-hash` prints
`"GR2": "d4296085a574e29296fb9baba5a8722766a832a0b15809ccee72ea019ebd027f"`, `"problems": []`,
`structural_ok: 1`. My independent recomputation: taking the section as **lines 56-151** (line 151 is the
blank line before `## GR3` at 152) and joining with LF gives **d4296085…** exactly; taking lines 56-150
and stripping the empty tail gives `75d24ea6635bcb916dadafd6439a85ad5c68f822141ef8e92f475870681d9a02`.
So the counter's "joined with LF and no trailing LF" **includes the blank line that precedes the next
heading**; a seat that also drops that blank line will print `75d24ea6…` and should not read it as a row
change. Receipt: `R49RevGR2b/receipts-digests-and-hash.txt`.

## Clause-by-clause against the pinned bytes

All 29 **Quote** lines of the row were machine-compared to the cited snapshot line (exact substring match
after stripping the quote delimiter and the source's leading tab/space run); **29/29 match, 0 miss**.
Every `file:line` in the Statement and Host reading was resolved to its snapshot line. Receipt:
`R49RevGR2b/receipts-quotes-and-citations.txt`.

1. **Both replace paths call the scrub code.** `dev-replace.c:700` is the comment
   `/* the disk copy procedure reuses the scrub code */`, immediately above `dev-replace.c:701-703`
   `ret = btrfs_scrub_dev(fs_info, src_device->devid, 0,` / `btrfs_device_get_total_bytes(src_device),` /
   `&dev_replace->scrub_progress, false, true);` inside `btrfs_dev_replace_start` (`dev-replace.c:587`).
   The continuation path is `dev-replace.c:1265-1268` inside `btrfs_dev_replace_kthread`
   (`dev-replace.c:1249`), same devid/`false, true` tail. `grep -n btrfs_scrub_dev dev-replace.c` returns
   exactly 701 and 1265 (plus a message at 948), so "both" is complete, and `dev-replace.c:3081`
   `bool readonly, bool is_dev_replace)` confirms those are the last two parameters. **Holds.**
2. **Return order inside `btrfs_scrub_dev`.** `scrub.c:3094-3095` `if (btrfs_fs_closing(fs_info))` /
   `return -EAGAIN;` is the first error return; then `scrub.c:3109` `sctx = scrub_setup_ctx(fs_info,
   is_dev_replace);` (error → `return PTR_ERR(sctx)` at 3110-3111) and `scrub.c:3114`
   `ret = scrub_workers_get(fs_info);` (error → `goto out_free_ctx`, 3115-3116, tail at 3249-3251) both
   precede every device check. Then the three device checks in the row's order: ENODEV (3120-3123),
   EROFS (3127-3133), EIO (3138-3142), each condition quoted exactly as the row states it — `!dev ||
   (test_bit(BTRFS_DEV_STATE_MISSING…) && !is_dev_replace)`; `!is_dev_replace && !readonly &&
   !test_bit(…WRITEABLE…)`; `!test_bit(…IN_FS_METADATA…) || test_bit(…REPLACE_TGT…)`. **Holds.**
3. **EINPROGRESS ordering and the `is_ongoing` gate.** `scrub.c:3146-3155`: `down_read(&…dev_replace.rwsem)`,
   `if (dev->scrub_ctx ||` / `(!is_dev_replace &&` / `btrfs_dev_replace_is_ongoing(&…dev_replace))) {` →
   `ret = -EINPROGRESS`. So the refrigerator is reached only after the three device checks, the
   `is_dev_replace`-false branch is guarded by `is_ongoing`, and the `dev->scrub_ctx` branch applies to
   **any** call — exactly as written. `dev-replace.c:1276-1300` confirms the predicate: `if
   (!dev_replace->is_valid) return false;` (1278-1279), STARTED and SUSPENDED fall through to
   `return true;` (1286-1287, 1300), NEVER_STARTED/FINISHED/CANCELED return false (1282-1285), and the
   comment at 1288-1297 says a replace suspended by an umount still returns true. **Holds.**
4. **Net refusal.** With those checks passed, a scrub start on a present, writeable, in-metadata device
   that is not the replace target reaches 3147 and returns EINPROGRESS; `goto out` (3154) runs
   `scrub_workers_put` and `scrub_free_ctx` (3249-3251) — no scrub context is attached (`dev->scrub_ctx
   = sctx` at 3159 is inside the success path), so "no scrub is started" is decided, not inferred.
   **Holds.**
5. **Cancel paths.** `dev-replace.c:1111` `ret = btrfs_scrub_cancel(fs_info);` sits in the STARTED arm
   (1107-1125) of `btrfs_dev_replace_cancel` (`dev-replace.c:1085`); the SUSPENDED arm (1126-1144) calls
   `btrfs_scrub_cancel(fs_info);` at 1144 after the comment `/* Scrub for replace must not be running in
   suspended state */` (1143) and `Scrub doing the replace isn't running so we need to do the` (1128).
   The row states the tension (cancel is called although the pinned comment says the scrub is not
   running) instead of hiding it. Range 1126-1144 starts at the case label and ends at the call, inside
   the function that ends at 1169 — it does not run into the next function. Note 1127-1129 stops one line
   before the comment's `*/` at 1130; the quoted words are all inside. **Holds.**
6. **Unmount suspend.** `dev-replace.c:1171-1195` is the exact extent of
   `void btrfs_dev_replace_suspend_for_unmount(struct btrfs_fs_info *fs_info)` (signature 1171, closing
   brace 1195). All 25 lines read: only the STARTED arm acts — `case …STATE_STARTED:` (1184),
   `replace_state = …STATE_SUSPENDED` (1185-1186), `time_stopped = ktime_get_real_seconds()` (1187),
   `item_needs_writeback = 1` (1188), one `btrfs_info` (1189); every other case (1179-1183) `break`s
   without action. No `btrfs_scrub_cancel` anywhere in 1171-1195. The old out-of-function range
   `1171-1199` is gone. **Holds.**
7. **Progress query.** `scrub.c:3321-3337` `btrfs_scrub_progress` looks the devid up under
   `device_list_mutex`, copies the stat only when a context exists, and returns
   `return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;` (3336). The "absent" premise is grounded at
   `scrub.c:3222` `dev->scrub_ctx = NULL;` (the clear on the scrub's exit path, 3221-3223). **Holds.**
8. **Host reading.** `capture.txt:1` = `captured 2026-10-27T02:09:52Z uid=1000 CapEff=0000000000000000`
   and `capture.txt:9` = `devinfo 1d02a454-…/devinfo devids=1` (the devid number 1 itself appears on
   `capture.txt:8` as `…/devinfo/1/scrub_speed_max`; the row cites :9 for the one-device fact).
   `ioctl.c:3132` `if (!capable(CAP_SYS_ADMIN))` / `:3133` `return -EPERM;` is the scrub-progress
   handler `btrfs_ioctl_scrub_progress` (3126-3139), so the privileged query is out of this caller's
   reach — decided by capture + pin, not inferred. The sysfs half is correctly attributed rather than
   denied: `sysfs.c:1288` `str = "device replace\n";` is inside `btrfs_exclusive_operation_show`
   (`sysfs.c:1265`, switch on `READ_ONCE(fs_info->exclusive_operation)` at 1271, registered at 1302);
   `sysfs.c:2015` `val = !!test_bit(BTRFS_DEV_STATE_REPLACE_TGT, &device->dev_state);` is
   `btrfs_devinfo_replace_target_show`. The resume path really takes the exclusive op at
   `dev-replace.c:1235` and the replace-start ioctl at `ioctl.c:3190` (finish at 3194). The row's
   "Read on this host by wave seat C2ExecHostRecheck … §3, both files are mode 444 and read `none` and
   `0`" checks out against `.ufo/waves/round-45/a2w1/C2ExecHostRecheck.md` §3, which shows
   `-r--r--r--` for both attributes and `cat` values `none` (exclusive_operation) and `0`
   (replace_target). This is the corrected form of the round-45 defect ("no replace state is
   observable"), not a repeat of it. **Holds.**
9. **Universal words.** The two "only" uses are scoped and true: "Only after those checks is a call with
   `is_dev_replace` false refused with `-EINPROGRESS`" (gates 3120/3127/3138 all precede 3147), and "The
   unmount suspend path itself only moves a STARTED replace to SUSPENDED" (effects enumerated above).
   "any call … while the device already carries a scrub context" matches the unguarded `dev->scrub_ctx`
   test at 3147. No "never"/"always"/"exact" overreach in the row.

## Defects

**None found.** No clause is contradicted by the pinned bytes; no citation is out of range or points at
the wrong construct; no quote is inexact; no range crosses a function boundary. Nothing here justifies
`partly`.

## Non-blocking notes (do not block; no verdict change)

1. `capture.txt:9` gives the **count** (`devids=1`); the devid **number** is only in `capture.txt:8`.
   Optional tightening: "lists one device, devid 1 (`capture.txt:9`, `:8`)".
2. "present" carries weight: a device flagged `BTRFS_DEV_STATE_MISSING` on a non-replace call is refused
   `-ENODEV` at `scrub.c:3120-3123` *before* the `is_ongoing` test, so the EINPROGRESS sentence holds for
   a device that is not flagged missing. Optional tightening: "for a device that exists and is not
   flagged missing".
3. The row's "stops it with `btrfs_scrub_cancel` for a started replace" compresses a case the pins
   decide: `btrfs_scrub_cancel` returns `-ENOTCONN` when `scrubs_running` is 0 (`scrub.c:3280-3282`), and
   the STARTED arm turns that into `BTRFS_IOCTL_DEV_REPLACE_RESULT_NOT_STARTED`
   (`dev-replace.c:1112-1113`); the SUSPENDED arm ignores the return (`dev-replace.c:1131`, 1144).
   Optional tightening: "calls `btrfs_scrub_cancel`, which returns `-ENOTCONN` if no scrub is running
   (scrub.c:3280-3282)".
4. The sysfs-readability sentence is a host observation carried by an attributed, dated seat receipt, not
   by `capture.txt`, and it is not marked `[inference]`. In substance that is stronger than an inference
   (and the row says "which this capture does not record"), so I do not call it a defect; a reader who
   applies the `[inference]` rule literally should know the basis is `C2ExecHostRecheck.md` §3, not the
   frozen capture.
5. Comment range `1127-1129` omits the `*/` at 1130 — cosmetic only.

## What I verified but did not re-derive

Line→function extents outside the cited ranges were taken from the snapshots as read (I confirmed the
enclosing functions of 587/701, 1085/1111, 1171-1195, 1249/1265, 1276, 3308/3336 and of the sysfs
functions at 1265/2015, but did not re-scan the whole files for other call sites). I trusted the
`SHA256SUMS` digests and the FETCH provenance instead of re-fetching `v7.2.11` from git.kernel.org. The
host capture was not re-run; the sysfs permissions/values come from the round-45 seat receipt's §3.

## What I did not do

I did not run the full C1 counter (only its `--section-hash` mode, as the item authorized); I did not run
any census `--selftest`; I did not read the live sysfs files myself; I did not review GR1 or GR3; I did
not edit, stage or commit anything in the lane. Scratch `/fast/scratch/hyaku/tsukuroi-r49/R49RevGR2b/` is
removed at exit; receipts are in `.ufo/waves/round-49/w1/R49RevGR2b/`.
