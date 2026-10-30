ROW GR2 VERDICT: partly
SECTION SHA256: 9fd581a0c9d02b02100b6a15648b7c6e4be896ac746ed09303a88dc8a24f0ec5

Seat R52CritGR2c (counted critic, claim C1). Row GR2 of `corpus/knowledge/btrfs-scrub-grounding-r45.md` read only from
the freeze bytes: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0:corpus/knowledge/btrfs-scrub-grounding-r45.md`
(entry lines 103-238 are GR2; the working tree was never used as evidence). The working tree was not modified; I wrote
only this report, the receipt directory `.ufo/waves/round-52/w1/R52CritGR2c/`, and scratch under
`/fast/scratch/hyaku/tsukuroi-r52/R52CritGR2c/` (removed at end of run).

## 0. Instrument checks (run, observed)

- Section hash: `python3 tools/check-scrub-admission-r52.py --revision ff9470ea… --section-hash --no-base-check` →
  `"GR2": "9fd581a0c9d02b02100b6a15648b7c6e4be896ac746ed09303a88dc8a24f0ec5"`, `structural_ok: 1`. Matches the item's
  value (receipt `R52CritGR2c/section-hash.json`).
- `python3 tools/lint-grounding-r51.py --revision ff9470ea…` → `verdict PASS`, `lint_ok 3`, `rows_clean 3`; GR2:
  cites 41, cite_bad 0, quotes 44, quote_bad 0; `gap_ok 1`, `gaps_computed 98`, `gap_missing []`, `gap_extra []`
  (receipt `R52CritGR2c/lint-r51.json`).
- Snapshot digests `sha256sum -c SHA256SUMS`: all OK in rounds 43/44/45 `frozen/src/`
  (receipt `R52CritGR2c/digests.txt`). S-row → snapshot mapping: S240 = `.ufo/waves/round-43/frozen/src/ioctl.c`
  (7b3488f2…), S242 = `.ufo/waves/round-44/frozen/src/scrub.c` (f347931b…), S243 = `.ufo/waves/round-44/frozen/src/sysfs.c`
  (ce146120…), S247 = `.ufo/waves/round-45/frozen/src/dev-replace.c` (f07ef0a0…), S249 = capture.txt (f5958a83…).
  All three FETCH.txt files name tag v7.2.11 (peeled a2de78ee…) for the kernel files.
- Independent whole-line quote check (my own script, not the lane lint): all 44 GR2 quotes equal the cited pinned line
  after whitespace collapse, 0 mismatches.

## 1. Clauses checked and found supported (pinned bytes, file:line)

- **Call sites.** dev-replace.c:700 comment; :701-703 `btrfs_scrub_dev(fs_info, src_device->devid, 0, …,
  &dev_replace->scrub_progress, false, true)` inside `btrfs_dev_replace_start` (587-714); :1265-1268
  `btrfs_scrub_dev(fs_info, dev_replace->srcdev->devid, dev_replace->committed_cursor_left, …, false, true)` inside
  `btrfs_dev_replace_kthread` (1249-1274). scrub.c:3081 `bool readonly, bool is_dev_replace)` — those are the last two
  parameters (signature 3079-3081). "each call … with the source device's devid" holds over the file's only two
  `btrfs_scrub_dev` call sites (grep: 701, 1265; :948 is a log string).
- **Errno order.** scrub.c:3094-3095 `-EAGAIN`; :3109-3111 `PTR_ERR(sctx)`; :3114-3116 workers_get error →
  `goto out_free_ctx`, returned at :3250-3253 (`out_free_ctx:` :3250, `scrub_free_ctx` :3251, `return ret` :3253,
  skipping `scrub_workers_put` at :3249 — correct, since get failed); :3120-3123 `-ENODEV` for `!dev || (MISSING &&
  !is_dev_replace)` — "unknown devid, or a missing device on a call that is not a replace" is exact; :3127-3133
  `-EROFS` (`!is_dev_replace && !readonly && !WRITEABLE`); :3138-3142 `-EIO` (`!IN_FS_METADATA || REPLACE_TGT`);
  :3147-3153 `-EINPROGRESS` (`dev->scrub_ctx || (!is_dev_replace && btrfs_dev_replace_is_ongoing(…))`). The row's
  listed order matches the code order, the list is exhaustive between 3094 and 3159 (only the ASSERTs at 3098-3106 do
  not return), and the range 3094-3153 sits inside `btrfs_scrub_dev` (3079-3254), before the attach at :3159.
- **The round-51 D1 fix survived.** "any call that gets past the earlier checks above, replace or not, is refused the
  same way while its device already carries a scrub context" — the qualifier is present and the code order
  (3120 → 3127 → 3138 → 3147) supports it. "no scrub is started": the EINPROGRESS arm jumps to `out` (:3154) before
  the attach (:3159) and before `atomic_inc(&fs_info->scrubs_running)` (:3167). ✓
- **is_ongoing.** dev-replace.c:1278-1279 `if (!dev_replace->is_valid) return false;`; :1286-1287 STARTED/SUSPENDED
  cases (1282-1285 are the false cases) → `return true` :1300; the comment at :1288-1297 explicitly names the
  suspended-by-umount case. ✓
- **Scrub-start ioctl.** ioctl.c:3072-3073 `-EPERM`; :3075-3078 `-EINVAL` (EXTENT_TREE_V2); :3080-3082 memdup_user
  error (`PTR_ERR(sa)`); :3084-3085 `-EOPNOTSUPP`; :3087-3090 `mnt_want_write_file` when `!(sa->flags &
  BTRFS_SCRUB_READONLY)`; :3093-3095 call; :3109-3110 copy_to_user → `-EFAULT`; :3115 `return ret`. Order and ranges ✓
  (all inside `btrfs_ioctl_scrub`, 3066-3116).
- **Progress query.** scrub.c:3321-3336 reads only `dev->scrub_ctx`; `return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV`
  at :3336. "from the device's scrub context alone, not from the replace state" ✓. Context lifetime: `dev->scrub_ctx =
  sctx` at :3159, `= NULL` at :3222, with no `return`/`goto` in scrub.c:3155-3225 (grep empty), so the attached
  context is cleared on every path that attached it. For a replace call the looked-up `dev` is the source device
  (devid = srcdev->devid), so "while a replace copies from the source device that device carries the context the copy
  attached" ✓.
- **Quotes and ranges.** 44/44 quotes whole-line exact (independent check above). No cited range runs into a
  neighbouring function (checked 3079-3254, 3321-3337, 3066-3116, 3126-3145, 1249-1274, 1276-1301, 1198-1247,
  232-332, 859-, 232-337). The gap block matches the lint's computation (gap_ok 1).
- **Host reading, except D1.** capture.txt:1 `uid=1000 CapEff=0000000000000000` ✓ no effective capabilities;
  ioctl.c:3132-3133 `if (!capable(CAP_SYS_ADMIN)) return -EPERM;` in `btrfs_ioctl_scrub_progress` ✓; sysfs.c:78
  `__INIT_KOBJ_ATTR(_name, 0444, _show, NULL)` (the BTRFS_ATTR macro body, 76-78) ✓ mode 0444; registered at sysfs.c:1302
  (`BTRFS_ATTR(, exclusive_operation, …)`, wired into `btrfs_attrs[]` at :1557) and sysfs.c:2019
  (`BTRFS_ATTR(devid, replace_target, …)`, in `devid_attrs[]` at :2112) ✓; sysfs.c:1288 `str = "device replace\n";`
  under `case BTRFS_EXCLOP_DEV_REPLACE` ✓; dev-replace.c:1235 `btrfs_exclop_start(… BTRFS_EXCLOP_DEV_REPLACE)` in the
  resume path ✓; ioctl.c:3190 the replace ioctl takes the exclusive operation around `btrfs_dev_replace_by_ioctl`
  (:3193, finished :3194) ✓; sysfs.c:2015 `val = !!test_bit(BTRFS_DEV_STATE_REPLACE_TGT, …)` ✓ reads 1 when set;
  dev-replace.c:309 `set_bit(…REPLACE_TGT…)` inside `btrfs_init_dev_replace_tgtdev` ✓ "the target-device setup sets";
  dev-replace.c:970 `clear_bit(…REPLACE_TGT…)` inside `btrfs_dev_replace_finishing` ✓ "the finish path clears".
  "Neither file reports the replace state itself" ✓ — grep of the whole S243 snapshot finds no `replace_state` or
  dev-replace-state exposure (only `exclusive_operation` and `REPLACE_TGT`). "This capture does not record the two
  files" ✓ — capture.sh loops only over `scrub_speed_max` and the `devinfo` listing; capture.txt has no such lines.
  "the round-45 host recheck … read both as mode 444 on this host with the values `none` and `0`" ✓ —
  `.ufo/waves/round-45/a2w1/C2ExecHostRecheck.md` §3 shows both files `-r--r--r--` and `cat` → `0` (replace_target)
  and `none` (exclusive_operation). "The kernel rules of the row are read from source." ✓
- **The one `[inference: …]` mark** (how `btrfs scrub start`/`status` print returns) is honest — btrfs-progs source is
  not pinned (S244 pins only the packaged unit files) — and I found no other unmarked inference in GR2.

## 2. Defect D1 (Host reading, entry lines 233-235): the suspended-without-exclop replace DOES show in
`replace_target`; "shows in neither" is contradicted by the row's own preceding sentence and by pinned bytes

Row text: "Neither file reports the replace state itself: a replace that the resume path set to suspended without
taking the exclusive operation (dev-replace.c:1235-1242) shows in neither, although the Statement counts it as ongoing."

Counterexample chain, all in pinned bytes:
- dev-replace.c:209-210: at mount, `btrfs_init_dev_replace` (state STARTED or SUSPENDED, :170-171) sets
  `set_bit(BTRFS_DEV_STATE_REPLACE_TGT, &dev_replace->tgtdev->dev_state);` on the restored target device (found at
  :172 by devid `BTRFS_DEV_REPLACE_DEVID`). `dev_replace->tgtdev` is assigned only here (:172) and at :649 (start), so
  the resume path at :1218 can only test it after this init ran.
- Reaching dev-replace.c:1235 implies the target device exists with a bdev (:1218-1227 returns earlier with state
  SUSPENDED otherwise), and :1235-1243 touches only `dev_replace->replace_state` — it clears neither the target bit
  nor the target device.
- The only clear of the bit is dev-replace.c:970 (the finish path; grep: REPLACE_TGT appears at :209-210, :309 set,
  :970 clear), and the cancel path destroys the target device instead (dev-replace.c:1160).
- sysfs.c:2015 publishes that bit as `devinfo/<devid>/replace_target` (kobj named "%llu" of `device->devid`,
  sysfs.c:2166; attribute in `devid_attrs[]` sysfs.c:2112, registered :2019, mode 0444 via BTRFS_ATTR :78).

Therefore, in exactly the state the sentence names, `devinfo/<tgt devid>/replace_target` still reads 1: the replace's
target device is flagged, so the replace IS visible in one of the two files the paragraph names — only its *state*
(suspended vs started) is not exposed. The row's own preceding sentence already concedes this ("`devinfo/<devid>/replace_target`
reads 1 on the replace's target device (sysfs.c:2015), whose target bit the target-device setup sets (dev-replace.c:309)
and the finish path clears (dev-replace.c:970)"): since the suspended/resume-failure path never reaches the finish
path, that bit is still set. The two adjacent sentences thus contradict each other, and the plain reading of
"a replace … shows in neither" would tell a triage operator (entry lines 330-333 direct the operator to read these two
files) that an unmount-interrupted replace leaves no observable trace, when `replace_target` = 1 on the target device
is exactly that trace. Under the narrower reading ("neither file reveals the suspended *state*") the clause is true —
but that reading requires silently inserting "its state" as the object of "shows", and the row as written asserts the
stronger, false claim.

Exact replacement (variant A; uses only lines the row already cites, so the Range gaps block and lint stay green —
I ran the lint on a patched copy of the entry in scratch: `lint_ok 3`, `verdict PASS`, cites 97, gap_ok 1; receipt
`R52CritGR2c/lint-fix-variantA.json`):

"Neither file reports the replace state itself: a replace that the resume path set to suspended
without taking the exclusive operation (dev-replace.c:1235-1242) is not named by `exclusive_operation`, and
`replace_target` still reads 1 on its target device, whose target bit the finish path clears (dev-replace.c:970),
although the Statement counts it as ongoing."

Optional strengthening (more precise, but it adds a new citation): also cite the mount-restore set site
dev-replace.c:209-210. That line is outside S247's declared ranges, so the entry's `### Range gaps (R51)` block must be
regenerated; I verified mechanically (`--emit-gaps` on a patched copy, receipt `R52CritGR2c/lint-fix-variantB.json`):
the S247 line must become

`- S247 dev-replace.c: 209-210, 309, 970, 1197, 1236-1242`

(unpatched, the lint fails with `gap_missing ["S247 dev-replace.c: 209-210"]`, `lint_ok 0`).

## 3. Secondary observation (not counted as a defect)

"the path that continues a replace interrupted by an unmount (dev-replace.c:1197, :1265-1268) each call
`btrfs_scrub_dev` …" — under the strictest reading of "each" (every run of the resume path), the universal is false:
the resume path returns without any scrub call when the target device is missing (dev-replace.c:1218-1227) or when the
exclusive operation is busy (:1235-1243). The row's Host reading names the second branch, and rounds 50/51 read "each"
as distributing over the two call sites (both of which pass source devid, `false, true`), so I do not count it; if the
L1 wants it airtight, appending "(when it takes the exclusive operation, dev-replace.c:1235)" keeps the citation set
unchanged. Relatedly, the kthread link (`kthread_run(btrfs_dev_replace_kthread, …)` at dev-replace.c:1245) between the
cited :1197 and :1265-1268 is uncited; citing it would also require a gap-block update (1245 is outside S247's declared
ranges).

## 4. What I did not check

- Did not run any host sysfs read, ioctl, scrub, replace or unit operation; the "mode 444 / `none` / `0`" host values
  are taken from the round-45 recheck receipt the row cites, which I re-read but did not re-execute.
- Did not verify btrfs-progs printing of these returns (the row marks it `[inference]`); btrfs-progs source is not
  pinned.
- Did not re-fetch any source from its URL; I verified the local snapshot digests against each directory's SHA256SUMS
  only.
- Did not check GR1, GR3, the Limits history bullets, or the triage chapter's other bullets beyond the GR2-referencing
  sentence at entry lines 330-333 (outside GR2's section hash).
- Did not read any other R52*GR* report before writing this one, per the item.
- No tool was installed or upgraded (none was needed); no admission mark was written; the lane working tree was not
  touched.

Receipts: `.ufo/waves/round-52/w1/R52CritGR2c/` — `digests.txt`, `section-hash.json`, `lint-r51.json`,
`clause-evidence.txt` (the pinned excerpts this report relies on), `lint-fix-variantA.json`, `lint-fix-variantB.json`
(includes the required regenerated gap block for the strengthened variant). Scratch
`/fast/scratch/hyaku/tsukuroi-r52/R52CritGR2c/` removed after the receipts were copied.
