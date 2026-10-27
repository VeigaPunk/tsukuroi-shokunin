ROW GR2 VERDICT: holds

Seat ResRevGR2 — residual (not counted; the depth gate already failed on binding) source check of row GR2 of
corpus/knowledge/btrfs-scrub-grounding-r45.md as committed at revision
194a4523288759b4b73248d1ebcce53e43d0eec7 (round 45, residual wave a2r1, hyaku run 9, tsukuroi lane).

Method and integrity (before any source reading)
- Snapshots digest-verified against their SHA256SUMS: round-45 frozen src (S246 cmdline.c/vsprintf.c/kstrtox.c,
  S247 dev-replace.c, S248 systemd.kill.xml — all OK), round-44 frozen src (S242 scrub.c, S243 sysfs.c, S244 — all
  OK), round-43 frozen src (S240 ioctl.c — OK; consulted only to test the honesty of the row's [inference] bracket
  and the capability gate, it is not registered by this entry), hostcap capture.txt sha256
  f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70 — matches. Receipt: ResRevGR2/digests.txt.
- Row text read via `git show 194a4523…:corpus/knowledge/btrfs-scrub-grounding-r45.md` (## GR2 section quoted in
  full below in the per-sentence items). All 19 GR2 Quote lines re-verified byte-exact (entry convention: leading
  indentation stripped) against the pinned snapshot at the cited line number — 19/19 OK.
  Receipt: ResRevGR2/quotes-bytecheck.txt.
- Host evidence: read-only `stat` + `cat` of /sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/exclusive_operation
  (mode 444, value "none") and /sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/replace_target
  (mode 444, value "0"), run by this seat on 2026-10-27 — independently reproduces the row's cited
  C2ExecHostRecheck §3 values. Nothing was written, started or stopped. Receipt: ResRevGR2/host-sysfs-read.txt.
- No tools were installed or upgraded (coreutils/git sufficed); no host mutation of any kind.

Per-sentence judgment — Statement

S1. "In Linux v7.2.11 a device replace copies the source device through the scrub code: both the replace start path
    (the comment "the disk copy procedure reuses the scrub code") and the path that continues an interrupted replace
    call btrfs_scrub_dev on the source device's devid with readonly false and is_dev_replace true, the last two
    parameters of btrfs_scrub_dev." — holds.
    - Start path: S247 dev-replace.c:700 is the comment, inside btrfs_dev_replace_start (587); 701-703:
      `ret = btrfs_scrub_dev(fs_info, src_device->devid, 0, btrfs_device_get_total_bytes(src_device),
      &dev_replace->scrub_progress, false, true);` — the source devid, false, true in the last two positions.
    - Continue path: S247 dev-replace.c:1259 is the "continuing dev_replace from %s (devid %llu) …" log inside
      btrfs_dev_replace_kthread (1249, launched by the resume path 1245); 1265-1268:
      `btrfs_scrub_dev(fs_info, dev_replace->srcdev->devid, dev_replace->committed_cursor_left, …,
      &dev_replace->scrub_progress, false, true)` — again source devid, false, true.
    - Parameter positions: S242 scrub.c:3079-3081 — `bool readonly, bool is_dev_replace` are the function's last
      two parameters; both calls pass false, true in exactly those positions.

S2. "Inside btrfs_scrub_dev, a call with is_dev_replace false is refused with -EINPROGRESS while
    btrfs_dev_replace_is_ongoing is true for the filesystem, which it is for a replace in state started or
    suspended (a replace suspended by an unmount still counts), and any call is refused with -EINPROGRESS while the
    device already carries a scrub context." — holds.
    - Gate: S242 scrub.c:3146-3155 under `down_read(&fs_info->dev_replace.rwsem)`: `if (dev->scrub_ctx ||
      (!is_dev_replace && btrfs_dev_replace_is_ongoing(&fs_info->dev_replace)))` → `ret = -EINPROGRESS;` (3153).
      The first disjunct (3147) carries no is_dev_replace qualifier, so "any call … while the device already
      carries a scrub context" is exact. "for the filesystem" — fs_info->dev_replace is per-fs.
    - Started-or-suspended: S247 dev-replace.c:1276-1300 — !is_valid → false (1278-1279);
      NEVER_STARTED/FINISHED/CANCELED → false (1282-1285); STARTED (1286) and SUSPENDED (1287) fall through the
      comment block to `return true` (1300). "Suspended by an unmount still counts":
      btrfs_dev_replace_suspend_for_unmount (1171-1195) sets STARTED → SUSPENDED at 1184-1186 (log 1189
      "suspending dev_replace for unmount"); SUSPENDED is still true per 1287→1300.

S3. "Both refusals come after three earlier device checks in the same function, which answer first: an unknown
    devid, or a missing device on a non-replace call, gives -ENODEV; a non-writeable device on a non-replace,
    non-readonly call gives -EROFS; a device outside the filesystem metadata, or the replace's own target device,
    gives -EIO." — holds.
    - Ordering: the three checks sit at S242 scrub.c:3118-3144, the refusal gate at 3146-3155 — strictly earlier.
    - -ENODEV: 3119-3124 `if (!dev || (test_bit(BTRFS_DEV_STATE_MISSING, &dev->dev_state) && !is_dev_replace))`
      → `ret = -ENODEV;` (3123). Unknown devid = !dev; missing-on-non-replace = MISSING && !is_dev_replace.
    - -EROFS: 3127-3134 `!is_dev_replace && !readonly && !test_bit(BTRFS_DEV_STATE_WRITEABLE, …)` → 3133
      `ret = -EROFS;`.
    - -EIO: 3137-3143 `!test_bit(BTRFS_DEV_STATE_IN_FS_METADATA, …) ||
      test_bit(BTRFS_DEV_STATE_REPLACE_TGT, …)` → 3142 `ret = -EIO;` (3139 quoted in the row).
    - The target really is the second disjunct's case: btrfs_init_dev_replace_tgtdev sets IN_FS_METADATA (S247
      dev-replace.c:308) and REPLACE_TGT (309), lists the device in fs_devices->devices (321), with devid
      BTRFS_DEV_REPLACE_DEVID (241) and WRITEABLE (295) — so a scrub aimed at the target passes lookup/ENODEV and
      EROFS and dies at the REPLACE_TGT disjunct with -EIO.

S4. "So while a replace is ongoing, a scrub start that reaches btrfs_scrub_dev for a present, writeable member
    device other than the replace target is refused with EINPROGRESS although no scrub was started, and the
    replace's source device carries a scrub context for the copy, which by SR7 makes a privileged progress query
    for that devid answer 0 [inference for the ioctl and btrfs-progs side: that the scrub-start ioctl hands this
    return to userspace unchanged, and how `btrfs scrub start` and `btrfs scrub status` print these answers, are
    not pinned here]." — holds.
    - Each scope word maps to a refusal it defeats: "present" = found by devid and not MISSING → passes 3119-3124;
      "writeable" = WRITEABLE set → passes 3127-3128; "member … other than the replace target" = IN_FS_METADATA
      set and REPLACE_TGT clear → passes 3138-3139. With a replace ongoing (S2), the second disjunct
      (3148-3149) fires and 3153 returns -EINPROGRESS with dev->scrub_ctx NULL for that device — "although no
      scrub was started" is exactly the causal content (the refusal needs no scrub context).
    - Source device carries the context: the replace's own call (is_dev_replace=true) passes the gate and
      installs at 3159 `dev->scrub_ctx = sctx;` on the source devid (both call sites address the source, S247
      701/1265); SR7's row at this revision (corpus/knowledge/btrfs-scrub-record-r44.md ## SR7) and S242
      scrub.c:3321-3336 decide the query: `return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;` (3336) — 0 with the
      context attached, cleared at 3222 when the copy ends.
    - [inference] bracket honest: the row's snapshot set contains no ioctl.c and no btrfs-progs source; the row
      claims neither the ioctl handoff nor the printing anywhere else (the triage bullet, lines "How this changes
      OS triage" ¶2, restates only kernel-level, pinned claims). Cross-check against the corpus's own pinned
      round-43 S240 ioctl.c (not cited by the row, correctly): btrfs_ioctl_scrub 3066-3116 calls btrfs_scrub_dev
      with `sa->flags & BTRFS_SCRUB_READONLY, false` (3093-3095 — is_dev_replace=false, confirming sentence S2's
      caller class) and returns that ret (3115); btrfs_ioctl_scrub_progress 3126-3145 gates on CAP_SYS_ADMIN
      (3132-3133). The bracket could be dropped if S240 were registered, but as committed it is accurate.

Per-sentence judgment — Host reading

H1. "The filesystem lists devid 1 only (capture.txt:9) and the caller has no effective capabilities (capture.txt:1),
    so the privileged progress query is out of its reach." — holds.
    - S249 capture.txt:9 `devinfo 1d02a454-…/devinfo devids=1`; capture.txt:1
      `captured 2026-10-27T02:09:52Z uid=1000 CapEff=0000000000000000`. Capability gate for the progress ioctl:
      S240 ioctl.c:3132-3133 (EPERM without CAP_SYS_ADMIN), also pinned by the SR7 row's Host reading ("the ioctl
      stops at the SR6 gate"), which GR2 references.

H2. "Replace state is still readable without privilege through sysfs, which this capture does not record: the
    filesystem's exclusive_operation names `device replace` while a replace holds the exclusive operation
    (sysfs.c:1288; the resume path takes it at dev-replace.c:1235), and `devinfo/<devid>/replace_target` reads 1 on
    the replace's target device (sysfs.c:2015)." — holds.
    - Naming: S243 sysfs.c:1265-1300 btrfs_exclusive_operation_show maps BTRFS_EXCLOP_DEV_REPLACE →
      `str = "device replace\n";` (1287-1288).
    - Holding: the resume path takes the exclop at S247 dev-replace.c:1235 (cited) and releases it at 1272 after
      the copy; the fresh start takes it in the ioctl handler at S240 ioctl.c:3190 and releases at 3194 — in the
      corpus's pinned S240 though not cited by the row. Citation-strength note, not an overreach: the sentence is
      conditional ("while a replace holds the exclusive operation"), the naming half is exactly sysfs.c:1288, and
      the kernel's own refusal message at dev-replace.c:1240-1241 ("cannot resume dev-replace, other exclusive
      operation running") corroborates the take semantics. The exclop setter itself (fs/btrfs/super.c) is pinned
      by no corpus snapshot — small residual, does not decide any row sentence.
    - replace_target: S243 sysfs.c:2007-2019 `val = !!test_bit(BTRFS_DEV_STATE_REPLACE_TGT, &device->dev_state);`
      (2015) — reads 1 exactly on the device flagged at S247 dev-replace.c:309.
    - "which this capture does not record": S249 capture.txt has 9 lines, recording scrub_speed_max and the devid
      list only — no exclusive_operation, no replace_target line.

H3. "Read on this host by wave seat C2ExecHostRecheck on 2026-10-27 (…/a2w1/C2ExecHostRecheck.md §3), both files
    are mode 444 and read `none` and `0`." — holds.
    - C2ExecHostRecheck.md §3 shows replace_target 0 and exclusive_operation none, both world-readable
      (-r--r--r-- = 444). Independently reproduced by this seat on 2026-10-27, read-only: exclusive_operation
      mode=444 value "none"; devinfo/1/replace_target mode=444 value "0" (ResRevGR2/host-sysfs-read.txt).

H4. "The kernel rules of the row are read from source." — holds. Every kernel-side sentence above ties to a
    digest-verified snapshot line; the host-side sentences are tied to S249 and to the two reproducible sysfs reads.

a2w1 objection check (each must be answered by the committed row)
1. C2RevGR2.md sentence 4 (the universal "any device of that filesystem returns EINPROGRESS" is contradicted by
   the earlier checks: replace target → -EIO, missing device → -ENODEV) — ANSWERED. S3 now enumerates all three
   earlier checks with exact conditions and errnos, and S4 narrows the EINPROGRESS claim to "a present, writeable
   member device other than the replace target". Both counterexample classes the objection named are covered
   (target via REPLACE_TGT→-EIO, S242 3139/3142; missing via MISSING→-ENODEV, 3120-3123), plus the -EROFS class.
2. C2CritGR2.md sentence 3 (same quantifier defect; also names -EROFS and the non-replace ioctl caller) —
   ANSWERED by the same narrowing; the -EROFS condition "non-replace, non-readonly call" (S242 3127-3128) is in
   S3 verbatim in substance. The ioctl caller's is_dev_replace=false (S240 ioctl.c:3093-3095) stays outside the
   row's pinned set, which the [inference] bracket discloses rather than asserts.
3. C2CritGR2.md Host reading ("no replace or scrub state is observable to this caller" overreaches; sysfs
   exclusive_operation and replace_target are world-readable) — ANSWERED. The old claim is gone; H2/H3 now name
   both attributes, cite their show functions (sysfs.c:1288, 2015), and record the §3 recheck, which this seat
   reproduced. The corrected text correctly does NOT claim scrub state is observable: exclusive_operation has no
   scrub case in its switch (sysfs.c:1271-1298) — consistent with C2ExecHostRecheck §3's stated scope.

Secondary finding (entry "## Limits" section — outside the Statement/Host-reading sections this verdict governs;
no effect on the verdict above)
- Committed text at 194a4523: "the S242 row's declared line ranges do not list `scrub.c:3081`, 3123-3142 or 3147".
- Fact: corpus/SOURCES.md S242 row (identical at 18389f44 and 194a4523) declares "fs/btrfs/scrub.c lines
  1365-1385, 3140-3162, 3215-3226, 3321-3337". Therefore 3142 and 3147-3153 ARE declared (inside 3140-3162);
  the GR2 quote lines NOT declared are 3081, 3123, 3133 and 3139 (3139 < 3140). The caveat's "3123-3142" is wrong
  for 3140-3142 and "or 3147" is wrong; it also omits 3139. Deciding evidence: SOURCES.md S242 row at
  194a4523; scrub.c line numbers of the row's own quotes.
- Additionally unflagged by the entry: S247 declares only "dev-replace.c lines 700-703, 1256-1268", so GR2's
  quotes dev-replace.c:1235 and 1287 are outside; S243 declares "sysfs.c lines 72-74, 2021-2049, 2113", so GR2's
  quotes sysfs.c:1288 and 2015 are outside. The file digests cover the whole snapshots, so every quote stays
  verifiable; only the declared-range bookkeeping lags.
- Exact replacement text for the caveat sentence: "Two registrations stay as they are: the S242 row's declared
  ranges (1365-1385, 3140-3162, 3215-3226, 3321-3337) do not list `scrub.c:3081`, 3123, 3133 or 3139 (3142 and
  3147-3153 sit inside 3140-3162), and the S237 row's do not list `scrub.c:421`; the integration's new quotes also
  sit outside the declared ranges of S247 (`dev-replace.c:1235` and 1287; declared 700-703, 1256-1268) and S243
  (`sysfs.c:1288` and 2015; declared 72-74, 2021-2049, 2113); the file digests cover the whole snapshots
  (`a2w1/C2ExecQuotes.md` F1-F2)."

Residual risk and verification gaps
- What was not done: rows GR1/GR3 (out of scope for this seat); no re-derivation of SR6; no privileged query, no
  write, no service/unit interaction, no sysfs write — the only host actions were read-only stat/cat of the two
  world-readable files named in the seat spec. The [inference] items (ioctl→userspace handoff wording,
  btrfs-progs printing) remain unpinned by the corpus, as the row itself states; S240 could pin the handoff but is
  not registered by this entry.
- The exclop setter (fs/btrfs/super.c btrfs_exclop_start) is pinned by no corpus snapshot; GR2's H2 claim about
  the exclop rests on its take/release call sites (dev-replace.c:1235/1272 cited; ioctl.c:3190/3194 in-corpus,
  uncited) plus the sysfs.c mapping — judged sufficient here, recorded as residual.
- Verdict is source-only plus the frozen capture and my two read-only host reads, exactly as the row declares.

Receipts (this seat dir): digests.txt, quotes-bytecheck.txt (19/19 OK), deciding-excerpts.txt, host-sysfs-read.txt.
Scratch /fast/scratch/hyaku/tsukuroi-r45/ResRevGR2 removed at exit; no lane file written except this report and
these receipts.
