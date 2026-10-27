ROW SR7 VERDICT: holds

# C2CritSR7 — adversarial falsification of row SR7

Seat: C2CritSR7 (critic), wave w2, round 44. Task: falsify `corpus/knowledge/btrfs-scrub-record-r44.md`
row SR7 against its pinned snapshots (S242 = round-44 `fs/btrfs/scrub.c` @ v7.2.11, S240 = round-43
`fs/btrfs/ioctl.c` @ v7.2.11, S237 = round-42 btrfs-progs v7.1 `cmds/scrub.c`) and the counter's own
gates in `tools/check-scrub-record-r44.py`. Method: claim-by-claim counterexample search against the
pinned lines, plus one live fetch to test the row's explicitly-marked unpinned inference.

## Falsification attempts and outcomes

1. **"attaches its context at scrub.c:3159 after all refusal checks and before any scrub work"** —
   TRIED to contradict. All refusal returns precede 3159: `-EAGAIN` (3094), `IS_ERR` ctx alloc (3110),
   worker-get fail → `out_free_ctx` (3114-16), `-ENODEV` (3120-24), `-EROFS` (3127-34), `-EIO`
   (3138-43), `-EINPROGRESS` (3147-54). First real work after attach is `scrub_supers` (3193) /
   `scrub_enumerate_chunks` (3208); only bookkeeping (`__scrub_blocked_if_needed`, `scrubs_running`,
   `memalloc_nofs_save`) intervenes. HOLDS.

2. **"clears it at scrub.c:3222 once the scrub work has ended, before the function's finalize tail"** —
   TRIED to contradict. 3222 clears under `scrub_lock` after `atomic_dec(&scrubs_running)` (3211) and
   the finished/not-finished log (3217-19); the `need_commit` tail (3232-46) runs strictly after the
   clear. TRIED to find a return between attach (3159) and clear (3222): there is none — every post-
   attach path flows to 3221-23 or to `return ret` at 3240/3247 with the ctx already NULL. HOLDS.

3. **"every return path leaves the field as it found it"** — `dev->scrub_ctx` is NULL on entry
   (non-NULL → refused at 3147-54, untouched) and NULL at every exit: `out:`/`out_free_ctx:` free the
   unattached `sctx` without touching `dev->scrub_ctx` (3248-53); the success path clears at 3222.
   No other writer exists in the pinned file (grep `scrub_ctx`: only 3147 read, 3159 set, 3222 clear,
   3304/3310/3313 read, 3331 read). HOLDS.

4. **`btrfs_scrub_progress` tri-state** — 3328-36: devid lookup under `device_list_mutex`; `sctx` read
   only `if (dev)`; `memcpy` only `if (sctx)`; `return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV`. Exactly
   the row's three cases; an idle device answers `ENOTCONN`, never 0; no history is kept. HOLDS.

5. **ioctl handler** — S240 ioctl.c:3132-33 gates `!capable(CAP_SYS_ADMIN) → -EPERM` (the SR6 gate)
   before `memdup_user`; 3139 `ret = btrfs_scrub_progress(...)`; 3141 copies args back only under
   `ret == 0`. Row's "returns that value and copies the arguments back to the caller only when it is
   0" HOLDS (a `copy_to_user` failure after ret==0 returns `-EFAULT` — a refinement, not a
   contradiction; the gating claim is exact).

6. **`is_scrub_running_in_kernel` (SR6)** — S237 scrub.c:1190-1206 returns 1 on the first
   `BTRFS_IOC_SCRUB_PROGRESS` returning 0, 0 after all fail; `cmd_scrub_status` sets `in_progress`
   solely from it (1946), and `running` prints only from `in_progress` (r43 row SR6). Combined with #4
   and #5: privileged status answers 1 exactly when some enumerated device carries a live ctx. HOLDS.

7. **Unpinned dev-replace inference** — the row marks it "[inference ... opened ... but not pinned]".
   Tested anyway: fetched `fs/btrfs/dev-replace.c` @ v7.2.11 (sha256
   f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a, receipt in this directory).
   `btrfs_scrub_dev(fs_info, src_device->devid, 0, ..., false, true)` at 701-703 (replace start) and
   1265-1268 (replace resume after suspend) — exactly the cited lines, `is_dev_replace=true` in both.
   The only other mention (948) is a log-format string. No `scrub_ctx` writes in dev-replace.c.
   HOLDS — the inference is true.

8. **"exactly while a scrub or device-replace run is in progress on it"** — strongest counterexample
   tried: `dev_replace->is_valid = 1` is set (dev-replace.c:663) ~38 lines before `btrfs_scrub_dev`
   attaches `srcdev->scrub_ctx` (701), with a transaction start+commit and `btrfs_wait_ordered_roots`
   in between — a window where `BTRFS_IOC_DEV_REPLACE_STATUS` reports STARTED yet the progress ioctl
   on srcdev returns `ENOTCONN`. Not a contradiction: the row defines "run in progress on it" as
   carrying the ctx, and the disk-copy run on that device genuinely has not started. Recorded as a
   caveat below, not a falsification.

9. **Missing-device edge** — `btrfs_scrub_dev` skips the MISSING-state rejection only when
   `is_dev_replace` (3120-21): a missing srcdev legitimately carries a ctx during replace, matching
   "the source of a running replace". The tgtdev never carries a ctx (querying it yields ENOTCONN
   during replace) — the row says "source", precisely. HOLDS.

10. **Refusal claim completeness** — `-EINPROGRESS` also fires when `!is_dev_replace &&
    btrfs_dev_replace_is_ongoing(...)` with `dev->scrub_ctx` unset (3147-49): a plain scrub on ANY
    device is refused during an unrelated replace. The row's wording is conditional ("refuses with
    -EINPROGRESS when dev->scrub_ctx is already set"), not biconditional — accurate as stated, worth
    noting for future readers.

## Quote check

All 10 pinned quotes verified verbatim (substring-per-line, counter semantics) at the cited lines:
S242 scrub.c 3081, 3147, 3153, 3159, 3222, 3321, 3331, 3333, 3336 and S240 ioctl.c 3139, 3141.
In-window requirement satisfied (10 of 10 in frozen windows; 3081 sits outside all windows but the
rule needs only ≥1). `requires` = {S242 scrub.c, S240 ioctl.c} fully covered. Replicated counter
gates for this row: quote_ok, prop_ok (all 5 tokens present), host_ok (capture.txt:1 exists, names
`uid=1000 CapEff=0000000000000000` = "no effective capabilities") — all true.

## Host reading

"Not observable unprivileged ... the ioctl stops at the SR6 gate" — capture.txt:1 confirmed; S240
3132-33 `-EPERM` precedes any progress code. Consistent.

## Residual caveats (non-blocking)

- The `is_valid`-before-ctx window (attempt 8): a `btrfs scrub status` snapshot taken between replace
  state publication and ctx attach reports not-running although `btrfs replace status` reports
  STARTED. The row's device-level semantics are still exact; a future row could add one sentence if
  this distinction ever matters to the census arm.
- `-EINPROGRESS` has a second cause (attempt 10); and post-`ret==0` `-EFAULT` replaces the return
  value (attempt 5). Both are precision refinements, not contradictions.

## Proposed text

None. Row SR7 stands as written; no sentence contradicts a pinned quote, no claim is unsupported.

Receipts: `dev-replace.c`, `dev-replace.sha256`, `dev-replace.callsites.txt` under
`.ufo/waves/round-44/w2/C2CritSR7/` (fetched 2026-10-26 from kernel.org, h=v7.2.11).
