VERDICT: defect-found

# R50RevGR2Deep — GR2 errno-order deep read

## Finding: the `scrub_ctx` clause drops earlier-gate scope

The operative ordering and the replace-ongoing conclusion match the frozen code. For a present, writeable, in-metadata, non-target device with `is_dev_replace=false` while replace is ongoing, `btrfs_scrub_dev` reaches the `-EINPROGRESS` arm after the `-ENODEV`, `-EROFS`, and `-EIO` checks: S242 `scrub.c:3120-24`, `3127-34`, `3138-43`, then `3146-55`. The row’s prose order matches that evaluation order (GR2 lines 61-72); the only ordering inversion is that code tests `dev->scrub_ctx` first at `scrub.c:3147`, whereas prose names the ongoing-replace arm first at GR2 lines 67-72. Both OR operands lead to the same `-EINPROGRESS`, so that inversion is immaterial. Full return/assignment list and exact source checks are in `R50RevGR2Deep/receipts-scrub-dev.txt`; gate trace is in `R50RevGR2Deep/gate-trace.txt`.

The row accurately says the `dev->scrub_ctx` disjunct is not restricted to `is_dev_replace=false`: `scrub.c:3147-49` has `dev->scrub_ctx || (!is_dev_replace && ongoing)`. The replace-start call passes `false, true` at S247 `dev-replace.c:701-703`; a resulting `-EINPROGRESS` is mapped to `BTRFS_IOCTL_DEV_REPLACE_RESULT_SCRUB_INPROGRESS` at `dev-replace.c:705-707`, corroborated by the comment at `:754`. The row’s ongoing-state description also matches S247 `dev-replace.c:1278-1300`; its suspend-path description matches `:1171-1195`. All quoted lines checked in the GR2 row match the pinned snapshots; S242 and S247 digests match their frozen hashes (receipt).

However, GR2 line 74’s parenthetical says “as is a start on any device that already carries a scrub context.” This drops the earlier-check scope. The code only reaches the context test after the `-ENODEV`, `-EROFS`, and `-EIO` gates (`scrub.c:3120-24`, `3127-34`, `3138-55`), so the unconditional “any device” statement is broader than the implementation: a call that fails an earlier gate returns that earlier error, not `-EINPROGRESS`. The preceding prose at lines 66-72 can be read as scoped by “Only after those checks”; the parenthetical at line 74 is not so qualified. Whether a failing-gate state can coexist with an attached context is not established by the frozen sources available here, so this is a wording/contract overreach, not a claim that a particular runtime combination was observed.

**Suggested replacement for GR2 line 74 parenthetical:** “(and, after those same device checks, a call on a device that already carries a scrub context is also refused with `-EINPROGRESS`, regardless of `is_dev_replace`)”. This preserves the true all-call-flag behavior while making the precedence explicit.

## Other scoped checks

- Scrub ioctl line 83-85: S240 `ioctl.c:3093-95` passes `is_dev_replace=false`; `:3109-11` copies the scrub args back to userspace and overwrites `ret` with `-EFAULT` on copy-back failure. Its input copy is separately at `:3080-82`. “Argument copy fails” is understandable but could be made explicit as “copying the scrub args back to userspace fails.”
- `progress->last_physical = start` is written at S242 `scrub.c:3091-92`, before the `btrfs_fs_closing` `-EAGAIN` return at `:3094-95`; this does not mean a scrub was started, but is a pre-return progress-field mutation.
- Progress query returns `-ENOTCONN` for an existing device with no context and `-ENODEV` for an unknown devid at S242 `scrub.c:3328-36`; clearing `dev->scrub_ctx` is at `:3221-23`.
- No runtime/test/counter command was run; this seat was a read-only source review.

## Evidence pointers

- `R50RevGR2Deep/receipts-scrub-dev.txt`: digest checks, all `return`/`ret =` lines in `btrfs_scrub_dev`, exact GR2 quote-to-source checks.
- `R50RevGR2Deep/gate-trace.txt`: per-gate outcome for the requested device profile and the scope audit.
- `R50RevGR2Deep/receipts-devrep.txt`: replace-start mapping, target state flags, ongoing-state and unmount-suspend excerpts.
- Frozen GR2 row: `corpus/knowledge/btrfs-scrub-grounding-r45.md:56-85`; frozen source paths named inline above.
