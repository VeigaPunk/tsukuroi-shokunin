VERDICT: defect-found

Seat ResCritGR2 — adversarial read (not counted) of row GR2 of
`corpus/knowledge/btrfs-scrub-grounding-r45.md` at `194a4523288759b4b73248d1ebcce53e43d0eec7`.
Method: all snapshot digests verified against their `SHA256SUMS` before use (receipt `ResCritGR2/digests.txt`;
round-45 src: 5/5 OK incl. dev-replace.c; round-44 src: 5/5 OK incl. scrub.c, sysfs.c; round-42 src scrub.c/CHANGES
OK; capture.txt sha256 `f5958a83…`). Every GR2 Quote line verified verbatim at its cited line number
(receipt `ResCritGR2/deciding-lines.txt`). The narrowed row diff `18389f44 → 194a452` was read; the L1 added the
three earlier checks, the SUSPENDED case, and the sysfs host reading.

## Finding 1 (deciding): the "carries a scrub context … query answers 0" clause is false for the suspended case the row itself now claims

Row text (entry lines 66-71 at 194a452): "So while a replace is ongoing, a scrub start that reaches
`btrfs_scrub_dev` for a present, writeable member device other than the replace target is refused with
`EINPROGRESS` although no scrub was started, and the replace's source device carries a scrub context for the copy,
which by SR7 makes a privileged progress query for that devid answer 0".

Counterexample: a replace in state SUSPENDED is "ongoing" by the row's own definition — the row says "which it is
for a replace in state started or suspended (a replace suspended by an unmount still counts)", and
`btrfs_dev_replace_is_ongoing` returns true for `BTRFS_IOCTL_DEV_REPLACE_STATE_SUSPENDED` even when the target is
missing after a degraded remount (S247 dev-replace.c:1287, comment 1288-1297; `is_valid` restored from the
persisted item at dev-replace.c:150, state restored at :138). But in SUSPENDED state the source device carries no
scrub context: the kernel's own invariant is the comment at dev-replace.c:1143 — "Scrub for replace must not be
running in suspended state" — enforced by the explicit `btrfs_scrub_cancel(fs_info)` at :1144, and
`btrfs_scrub_cancel_dev` waits until `dev->scrub_ctx == NULL` (S242 scrub.c:3310-3315). Across the
suspend-for-unmount + remount case the row names, the restore path sets `dev_replace->srcdev`/`tgtdev`
(dev-replace.c:172-174) but no `btrfs_device` gets a `scrub_ctx` there; the field is assigned only inside
`btrfs_scrub_dev` at scrub.c:3159 and cleared at scrub.c:3222. So for a suspended replace (or the window after a
remount before `btrfs_dev_replace_kthread` re-enters `btrfs_scrub_dev`), `btrfs_scrub_progress(srcdev->devid)`
returns `-ENOTCONN`, not 0 — `return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;` (S242 scrub.c:3336). The EINPROGRESS
half of that sentence survives on the fs-wide disjunct alone (`!is_dev_replace && btrfs_dev_replace_is_ongoing`,
scrub.c:3148-3149), but the consequence clause — "carries a scrub context … answers 0" — does not hold in exactly
the suspended subcase the integration added. The Observation cell's "a privileged `scrub status` shows the source
device of a replace as running" inherits the same overclaim for a suspended replace.

Smallest exact replacement (entry lines 66-71 tail): replace
"and the replace's source device carries a scrub context for the copy, which by SR7 makes a privileged progress
query for that devid answer 0"
with
"and while the copy runs, the replace's source device carries a scrub context (attached at scrub.c:3159, cleared
at scrub.c:3222) — for a suspended replace the context is gone and that query answers -ENOTCONN instead
(scrub.c:3336; dev-replace.c:1143-1144)".
Optionally tighten the Observation to "…shows the source device of a running replace as running".

## Finding 2 (weaker, non-fatal): `exclusive_operation` reads `none` for a started replace

The Host reading says "the filesystem's `exclusive_operation` names `device replace` while a replace holds the
exclusive operation (sysfs.c:1288; the resume path takes it at dev-replace.c:1235)". The parenthetical is
literally true, and the row's own evidence is complete on this point: within pinned S247 the only
`btrfs_exclop_start(fs_info, BTRFS_EXCLOP_DEV_REPLACE)` is on the resume path at dev-replace.c:1235 (grep: sole
occurrence); `btrfs_dev_replace_start` (:587-703) and `btrfs_dev_replace_by_ioctl` (:733-760) claim no exclusive
operation. So while a started replace holds the machinery (state STARTED, `is_valid`), `exclusive_operation`
still reads `none` — the sysfs file names a replace only during the resumed kthread's run or if `btrfs_exclop_start`
is invoked from code outside the pinned file [unpinned]. `replace_target` (sysfs.c:2015, bit set at
dev-replace.c:309 and re-set after remount at :209-210) is the reliable unprivileged indicator in the pinned
evidence. Smallest safe correction, optional: in the triage bullet "Read the unprivileged `exclusive_operation`
and `replace_target` sysfs files first", reorder to "`replace_target` and `exclusive_operation`", or add "(`none`
there does not rule out a replace; `replace_target` answers it)".

## Assigned candidates — checked, all hold

- Order of checks vs EINPROGRESS: exact. ENODEV :3120-3124 → EROFS :3127-3134 → EIO :3137-3143 →
  EINPROGRESS :3146-3153 (S242, cat -n in receipt). The row's "three earlier device checks … answer first" is
  scoped to device checks; `btrfs_fs_closing` -EAGAIN and `scrub_workers_get` precede them but are not device
  checks.
- 'missing on non-replace' and 'unknown devid' both -ENODEV: `!dev || (MISSING && !is_dev_replace)` → -ENODEV
  (:3120-3123). Matches row.
- -EROFS needs readonly false: `!is_dev_replace && !readonly && !WRITEABLE` (:3127-3128). Row's
  "non-replace, non-readonly" exact.
- SUSPENDED still refuses: `is_ongoing` true for STARTED/SUSPENDED (dev-replace.c:1286-1298, incl. the
  suspended-by-umount/missing-tgtdev comment the row paraphrases). Holds.
- Replace target in the searched device list: `list_add(&device->dev_list, &fs_devices->devices)` under
  `device_list_mutex` (dev-replace.c:320-324) with `REPLACE_TGT` set (:309); `btrfs_find_device` searches that
  list (scrub.c:3119) and the -EIO branch tests the bit (:3138-3139). Row exact.
- sysfs claims: `str = "device replace\n"` at sysfs.c:1288; `val = !!test_bit(BTRFS_DEV_STATE_REPLACE_TGT, …)` at
  :2015; resume path takes the exclop at dev-replace.c:1235. Exact (see Finding 2 for the caveat).
- Call sites: dev-replace.c:701-703 and :1265-1268 both `btrfs_scrub_dev(…, false, true)`; signature last two
  params `bool readonly, bool is_dev_replace` (scrub.c:3081). Quote at :1259 is the kthread log line. Exact.
- Host reading: capture.txt:1 (uid 1000 CapEff 0), :9 (devids=1) verified; mode-444/`none`/`0` reading matches
  `a2w1/C2ExecHostRecheck.md` §3 (its ls -l/cat transcripts).

Not done (declared): no ioctl.c pinned in these snapshots, so the scrub-start ioctl's own gates (capability,
possible exclop) were not re-verified beyond the row's existing `[inference]` mark; no live ioctl run
(host guard). The remaining inference marks are appropriately scoped.

No tools installed; `sha256sum -c`, `git show/diff`, `cat`/`grep` only. No files written outside this seat's
report dir and scratch; lane untouched.
