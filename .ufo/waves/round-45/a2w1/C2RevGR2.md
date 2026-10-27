ROW GR2 VERDICT: partly

Seat C2RevGR2 — counted depth review of row GR2, corpus/knowledge/btrfs-scrub-grounding-r45.md, judged as
committed at implementation revision 18389f44cf6ce414d7be205998b29c79fb0b490c (round 45, wave a2w1, hyaku run 9).

Method and snapshot integrity (verified before any source reading)
- S247 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-45/frozen/src/dev-replace.c: sha256
  f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a — equal to its line in
  .ufo/waves/round-45/frozen/src/SHA256SUMS (command: sha256sum on both files; receipt hashes.txt).
- S242 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-44/frozen/src/scrub.c: sha256
  f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8 — equal to its line in
  .ufo/waves/round-44/frozen/src/SHA256SUMS.
- Row text read via `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show
  18389f44…:corpus/knowledge/btrfs-scrub-grounding-r45.md`; all 10 Quote lines verified verbatim at their cited
  line numbers (line numbers hard-anchored by line-numbered search output on the frozen files: dev-replace.c
  691, 1245, 309, 321, 1276; scrub.c 3123, 3139, 3148, 3149, 3153, 3159).
- No `lsp` device is mounted in this seat; checks are pinned-snapshot reads of frozen data, not a live index.
  No host state was queried; the only host evidence used is the frozen capture S249, read-only.

Per-sentence judgment — Statement

1. "In Linux v7.2.11 a device replace copies the source device through the scrub code: both the replace start path
   (the comment …) and the path that continues an interrupted replace call btrfs_scrub_dev on the source device's
   devid with readonly false and is_dev_replace true, the last two parameters of btrfs_scrub_dev." — holds.
   - Start path: S247 dev-replace.c:700 is the comment "/* the disk copy procedure reuses the scrub code */"
     inside btrfs_dev_replace_start (defined at 587; its error branch anchored at 691); 701-703:
     btrfs_scrub_dev(fs_info, src_device->devid, 0, btrfs_device_get_total_bytes(src_device),
     &dev_replace->scrub_progress, false, true).
   - Continuation path: S247 dev-replace.c:1259 logs "continuing dev_replace from %s (devid %llu) to target %s
     @%u%%" inside btrfs_dev_replace_kthread (1249), launched by btrfs_resume_dev_replace_async (1197 comment
     "resume dev_replace procedure that was interrupted by unmount"; kthread_run at 1245); 1265-1268:
     btrfs_scrub_dev(fs_info, dev_replace->srcdev->devid, dev_replace->committed_cursor_left, …,
     &dev_replace->scrub_progress, false, true).
   - Parameter positions: S242 scrub.c:3079-3081 — `bool readonly, bool is_dev_replace` are the last two
     parameters; both calls pass false, true in exactly those positions.

2. "Inside btrfs_scrub_dev, a call with is_dev_replace false is refused with -EINPROGRESS while
   btrfs_dev_replace_is_ongoing is true for the filesystem," — holds.
   - S242 scrub.c:3146-3153: under `down_read(&fs_info->dev_replace.rwsem)`, the disjunct
     `(!is_dev_replace && btrfs_dev_replace_is_ongoing(&fs_info->dev_replace))` leads to `ret = -EINPROGRESS`
     at 3153. btrfs_dev_replace_is_ongoing (S247 dev-replace.c:1276-1287) is true exactly for replace states
     STARTED/SUSPENDED (set at 661; suspend/resume 1184-1216), i.e. while a replace runs; fs_info->dev_replace
     is per-filesystem.

3. "and any call is refused with -EINPROGRESS while the device already carries a scrub context." — holds.
   - S242 scrub.c:3147 first disjunct `dev->scrub_ctx ||` carries no is_dev_replace qualifier; the shared branch
     returns -EINPROGRESS at 3153.

4. "So while a replace runs, the scrub-start ioctl for any device of that filesystem returns EINPROGRESS although
   no scrub was started," — overreaches; this decides the verdict.
   - Core direction holds: for an ordinary member device (present, writable, not the replace target) the
     fs-wide disjunct at scrub.c:3148-3149 fires while a replace runs, returning -EINPROGRESS; "although no
     scrub was started" is right — the refusal needs no scrub context.
   - Overreach: the universal "any device of that filesystem" is contradicted inside the same cited function.
     Two member-device classes are refused earlier with a different errno while a replace runs:
     (a) the replace's own target device — registered into the filesystem's device list with
         BTRFS_DEV_STATE_REPLACE_TGT (S247 dev-replace.c:309 set_bit; 321 list_add into fs_devices->devices;
         devid = BTRFS_DEV_REPLACE_DEVID at 241; removed only at finishing/destroy, 712/958/1160) — hits
         S242 scrub.c:3138-3143 first: test_bit(BTRFS_DEV_STATE_REPLACE_TGT, …) → ret = -EIO at 3142, before
         the 3147 check. A scrub-start addressed at that devid returns EIO, not EINPROGRESS.
     (b) a missing member device — S242 scrub.c:3120-3125: test_bit(BTRFS_DEV_STATE_MISSING, …) &&
         !is_dev_replace → ret = -ENODEV at 3123, also before 3147.
   - Deciding source line: S242 scrub.c:3139 (REPLACE_TGT test feeding -EIO at 3142), with the target's
     membership pinned by S247 dev-replace.c:309 and 321.
   - Minor caveat folded into this same sentence: no frozen snapshot pins the ioctl→btrfs_scrub_dev return
     plumbing (S242/S247 contain no ioctl.c), so "the scrub-start ioctl returns" is pinned at function
     granularity, not ioctl granularity. Caveat only; the quantifier is the defect.

5. "and the replace's source device carries a scrub context for the copy, which by SR7 makes a privileged progress
   query for that devid answer 0 [inference …]" — holds.
   - During the copy the source device's context is attached (S242 scrub.c:3159 `dev->scrub_ctx = sctx;`; both
     replace calls address the source devid, S247 701/1265), and SR7 (corpus/knowledge/btrfs-scrub-record-r44.md,
     row SR7, same revision) pins: btrfs_scrub_progress "returns 0 only when the device exists and carries a
     context" (-ENOTCONN idle, -ENODEV unknown devid). So the privileged progress query for that devid answers 0
     while the replace runs; "answer 0" reads correctly as the success return per SR7's success-direction wording.
   - The [inference] bracket honestly scopes only the btrfs-progs printing side and is not restated as fact
     elsewhere in the row (full row text checked).

Host reading
- "The filesystem lists devid 1 only (capture.txt:9)" — holds: S249 capture.txt:9 is
  `devinfo 1d02a454-c549-4a35-b567-89d60902af8e/devinfo devids=1`.
- "the caller has no effective capabilities (capture.txt:1)" — holds: capture.txt:1 is
  `captured 2026-10-27T02:09:52Z uid=1000 CapEff=0000000000000000`.
- "no replace or scrub state is observable to this caller, and the row is read from source." — holds: with
  CapEff=0 the privileged progress ioctl is out of reach (SR6/SR7 CAP_SYS_ADMIN gate per
  btrfs-scrub-record-r44.md), and the row's kernel claims are framed as source-read. capture.txt:8
  (scrub_speed_max, mode 644, value 0) is an attribute value, not scrub/replace state.

Worked examples
- Both call sites checked in full including argument values (readonly=false, is_dev_replace=true; source devids
  src_device->devid at S247:701 and dev_replace->srcdev->devid at S247:1265) — see per-sentence item 1.

Exact proposed replacement text (for the overreaching sentence only; rest of the row unchanged)

"So while a replace runs, the scrub-start ioctl for any ordinary member device of that filesystem returns
`EINPROGRESS` although no scrub was started; two members are refused earlier with a different error: the
replace's own target device (registered with `BTRFS_DEV_STATE_REPLACE_TGT` and listed in the filesystem's device
list, S247 dev-replace.c:309,321) with `-EIO` (S242 scrub.c:3138-3143) and a missing device with `-ENODEV`
(S242 scrub.c:3120-3125). The replace's source device carries a scrub context for the copy, which by SR7 makes a
privileged progress query for that devid answer 0 [inference for the btrfs-progs side: how `btrfs scrub start`
and `btrfs scrub status` print these two answers is not pinned here]."

Residual risk and verification gaps
- The BTRFS_IOC_SCRUB wrapper's errno plumbing is not pinned by any snapshot in this round; nothing here
  confirms it beyond btrfs_scrub_dev-level behavior. Freezing ioctl.c would let the row pin the ioctl naming.
- The numeric value of BTRFS_DEV_REPLACE_DEVID is a header constant not present in the pinned snapshots; the
  finding does not depend on it (the target is reachable by its devid lookup whatever the value).
- Verdict is source-only plus the frozen capture, exactly as the row declares; no privileged query, no host
  mutation, no timer/service interaction was attempted.
- What was not done: no independent re-derivation of SR7's own row (taken as committed at this revision; only
  its success-direction sentence is load-bearing here), and no check of sibling rows GR1/GR3 (out of scope).
- Receipts (this seat dir): hashes.txt, s247-quote-lines.txt, s242-quote-lines.txt, gr2-row-and-capture.txt.
  Scratch /fast/scratch/hyaku/tsukuroi-r45/C2RevGR2 removed at exit; no other path written.
