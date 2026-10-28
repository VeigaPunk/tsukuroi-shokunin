ROW GR2 VERDICT: holds
SECTION SHA256: e0b391e198f67ff57ce7971e2dd589faaa9390ebf2d2fd49dc6d103c163a52ce
Reviewer R48RevGR2b, row GR2 of the btrfs scrub grounding entry at revision ae99f021b76f8eb1c8805d32d80644464afb1ff6.

Hash: the checker with --section-hash printed the expected GR2 value above. I re-derived it with Python: sha256 over the LF-joined lines from the GR2 header up to (exclusive) the GR3 header gives the same value. (Adding a trailing newline gives a different hash, 3320c79e..., so the checker's convention is the plain join.)

Snapshots: sha256sum -c against the four SHA256SUMS files gave OK for dev-replace.c (round 45, f07ef0a0...), scrub.c and sysfs.c (round 44, f347931b... and ce146120...) and ioctl.c (round 43, 7b3488f2...). capture.txt digest is f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70, matching the entry header.

Quotes: a script checked all 29 Quote lines against the snapshots at the cited lines. All 29 text matches are exact (the doubled quote at dev-replace.c:1259 is only the C string's own quote).

Clause by clause (every clause checked in the snapshot):
- Replace start: dev-replace.c:700 holds the comment and dev-replace.c:701-703 calls btrfs_scrub_dev(src devid, ..., false, true). Resume kthread: dev-replace.c:1265-1268 same call, same last two arguments. The signature at scrub.c:3079-3081 shows the last two parameters are readonly and is_dev_replace. Supported.
- Order inside btrfs_scrub_dev: scrub.c:3094-3095 closing check returns -EAGAIN; scrub.c:3109-3111 scrub_setup_ctx error returns; scrub.c:3114-3116 scrub_workers_get error exits through out_free_ctx; then scrub.c:3119-3125 gives -ENODEV for unknown devid or (missing and not replace); scrub.c:3127-3135 gives -EROFS only for non-replace, non-readonly, non-writeable; scrub.c:3138-3143 gives -EIO for not-in-metadata or REPLACE_TGT. Supported, ordering correct.
- scrub.c:3146-3155: the EINPROGRESS test is dev->scrub_ctx OR (not is_dev_replace AND btrfs_dev_replace_is_ongoing), placed after the three device checks. dev-replace.c:1276-1300 shows is_ongoing is false for never-started, finished, canceled and true for STARTED and SUSPENDED; the comment at dev-replace.c:1288-1297 covers a replace suspended by an unmount. The consequence ("a scrub start that reaches btrfs_scrub_dev for a present, writeable device in metadata and not the target is refused, no scrub started") follows; the wording "writeable" is stricter than needed (a readonly start skips the EROFS test), which is safe.
- Source device carries the scrub context during the copy: the replace passes the source devid (dev-replace.c:701, :1265) and scrub.c:3159 sets dev->scrub_ctx = sctx, cleared at scrub.c:3222. Supported.
- Cancel of a suspended replace: dev-replace.c:1126-1144 handles the SUSPENDED case, the comment at dev-replace.c:1127-1129 says the scrub doing the replace isn't running, and dev-replace.c:1144 calls btrfs_scrub_cancel. Supported.
- Progress query: scrub.c:3336 returns -ENOTCONN when the device exists and has no context, -ENODEV when no device. Supported.
- Unmount suspend: dev-replace.c:1171-1195 moves STARTED to SUSPENDED and contains no btrfs_scrub_cancel call. Supported. The inference bracket (ioctl pass-through and btrfs-progs printing) marks only what the pinned bytes do not decide; correctly placed.

Host reading: capture.txt:1 gives CapEff all zeros and uid 1000; capture.txt:9 gives devids=1; capture.txt has 9 lines and records no exclusive_operation or replace_target, as the row says. sysfs.c:1271-1302 shows the exclusive_operation show function and sysfs.c:1287-1288 maps the replace exclusive operation to "device replace"; sysfs.c:2015 returns 1 for the REPLACE_TGT bit. dev-replace.c:1235 takes the exclusive operation on resume; ioctl.c:3190 takes it in the start command. The 444 modes and none/0 values come from a lane wave report (not a pinned snapshot) and are labelled as read by that seat; the row says the kernel rules are read from source. Honest labelling.

Nits (not defects, no mark needed, proposed fixes for later):
1. The sentence "the replace's source device carries the scrub context the copy attached, which by SR7 btrfs_dev_replace_cancel calls btrfs_scrub_cancel ..." has a dangling "which"; every fact in it is supported but it reads as if the context is what the cancel path calls. Suggested: "...carries the scrub context the copy attached (scrub.c:3159); by SR7 btrfs_dev_replace_cancel calls btrfs_scrub_cancel ...".
2. dev-replace.c:1171-1199 overshoots the suspend function, which ends at dev-replace.c:1195; suggest 1171-1195.
3. "only sets the state to SUSPENDED" omits that it does so only from STARTED and also sets the stop time and a writeback flag (dev-replace.c:1184-1188); the point it supports (no scrub cancel) is unaffected.
Not done: no kernel was run, no sysfs was read by me, the btrfs-progs side was not examined.
