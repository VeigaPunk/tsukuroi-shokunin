ROW GR2 VERDICT: holds
SECTION SHA256: e0b391e198f67ff57ce7971e2dd589faaa9390ebf2d2fd49dc6d103c163a52ce
Reviewer R48RevGR2c, row GR2 of corpus/knowledge/btrfs-scrub-grounding-r45.md at revision ae99f021b76f8eb1c8805d32d80644464afb1ff6. I read it as a stranger, against the pinned snapshots.

HASH. The section-hash command printed GR2 = e0b391e1...52ce. My own derivation (sha256 over the LF-joined lines from the GR2 header up to, excluding, the GR3 header, no trailing newline) gave the same value. The two variants with a trailing newline or with a blank-line difference gave other values, so the frozen convention is the no-trailing-newline join.

SNAPSHOT DIGESTS. sha256sum matched the SHA256SUMS lines for dev-replace.c (round 45, f07ef0a0...), scrub.c (round 44, f347931b...), sysfs.c (round 44, ce146120...) and ioctl.c (round 43, 7b3488f2...). The round-42 SHA256SUMS lists a different scrub.c (48df2e2f...); the row cites S242, which is the round-44 file, and I used that one.

QUOTES. All 29 Quote lines sit on the cited line numbers. Spot-read: dev-replace.c:700, 701, 703, 1259, 1265, 1268, 1128, 1143, 1144, 1235, 1287; scrub.c:3081, 3094, 3095, 3109, 3114, 3123, 3133, 3138, 3139, 3142, 3147-3149, 3153, 3222, 3336; sysfs.c:1288, 2015.

CLAUSE BY CLAUSE.
1. Start and resume both reach btrfs_scrub_dev with the source devid, readonly false, is_dev_replace true. Start: dev-replace.c:701-703. Resume kthread: dev-replace.c:1265-1268, launched from the async resume function at dev-replace.c:1245. The last two parameters are the signature at scrub.c:3081. Supported.
2. EAGAIN on btrfs_fs_closing is the first return (scrub.c:3094-3095). The context allocation and the worker get follow (scrub.c:3109-3116) and their errors return or goto the out_free_ctx exit (scrub.c:3250-3253) before any device lookup. Supported.
3. Three device checks, in this order. ENODEV: no device, or MISSING with !is_dev_replace (scrub.c:3120-3123). EROFS: !is_dev_replace && !readonly && !WRITEABLE (scrub.c:3127-3133). EIO: not IN_FS_METADATA, or REPLACE_TGT (scrub.c:3138-3142). Supported exactly.
4. Only after those: EINPROGRESS if dev->scrub_ctx, or if !is_dev_replace and btrfs_dev_replace_is_ongoing (scrub.c:3146-3153). is_ongoing is true for STARTED and SUSPENDED, and the in-source comment says a replace suspended by umount still counts (dev-replace.c:1286-1297). Supported. The is_valid guard at dev-replace.c:1278 is not named, but a replace in STARTED state has is_valid set (dev-replace.c:667), so the clause is not overreaching.
5. The conclusion for a non-replace start on a present, writeable, in-metadata, non-target device: EINPROGRESS, no scrub started. dev->scrub_ctx is assigned only after the check passes (scrub.c:3159), and the failure goto leads to the exit that frees the ctx (scrub.c:3248-3253). Supported. The writeable condition is sufficient but not necessary for a readonly call, which only narrows the stated set.
6. The copy's call attaches its ctx to the source device (scrub.c:3159, found by devid at scrub.c:3119) and clears it on exit (scrub.c:3222). The cancel ioctl handles SUSPENDED by calling btrfs_scrub_cancel (dev-replace.c:1126, 1144) and the comment says the replace scrub is not running (dev-replace.c:1127-1129, 1143). Supported. The "SR7" pointer is a cross-reference to another row and is not checkable inside these snapshots.
7. Progress query returns -ENOTCONN when the device is found and its ctx is NULL, otherwise -ENODEV when the device is missing (scrub.c:3336; the function head is at scrub.c:3321). The row states only the ENOTCONN branch, which is correct for the source device that exists.
8. Unmount suspend path (dev-replace.c:1171-1195) changes STARTED to SUSPENDED and contains no scrub cancel call. Supported for the "does not cancel the scrub" part.

INFERENCE MARK. The bracketed [inference] covers only the ioctl hand-off and btrfs-progs printing, which none of the pinned lines in this row decide. It is correctly placed. No unmarked clause rests on unpinned bytes.

HOST READING. capture.txt:9 shows devids=1; capture.txt:1 shows CapEff=0000000000000000. Both match. The sysfs claims match: exclusive_operation prints "device replace" for the DEV_REPLACE case (sysfs.c:1288, in the show function at sysfs.c:1265-1301); replace_target prints the REPLACE_TGT bit (sysfs.c:2015); resume takes the exclop at dev-replace.c:1235; the ioctl start takes it at ioctl.c:3190 and releases it at ioctl.c:3194. The mode-444 and none/0 readings are attributed to a prior seat's receipt (C2ExecHostRecheck, section 3); I read that file and it carries the ls and cat output, so the attribution is accurate. The capture does not record them, as the row says.

NITS (not material, no replacement required for holds).
a. The cited range dev-replace.c:1171-1199 runs 4 lines past the function end at dev-replace.c:1195 (lines 1196-1199 are a blank line, a comment, and the next function's head). The content claim is unaffected.
b. "only sets the state to SUSPENDED" is literal-word imprecise: for STARTED the function also writes time_stopped, item_needs_writeback and a log message (dev-replace.c:1185-1189), only under STARTED. The point of the clause, that no scrub is cancelled, holds.
c. The sentence "the replace's source device carries the scrub context the copy attached, which by SR7 ..." has an unclear relative clause; its facts are supported as listed in clause 6.
d. "privileged progress query" rests on a capable() check in the scrub progress ioctl, ioctl.c:3132-3133 in the pinned S240; the row does not cite that line, but the pinned bytes do support it.

NOT DONE. I did not run any census or kernel code, and did not check the SR7 row text.
