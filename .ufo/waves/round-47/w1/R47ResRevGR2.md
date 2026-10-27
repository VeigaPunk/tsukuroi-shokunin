ROW GR2 VERDICT: partly
SECTION SHA256: 909830c83cbcf0a02264153fa6f179415fb8388d3e08c43d79fbf33c8cfa11a2

Seat R47ResRevGR2, round 47 wave w1 (counted). Row GR2 of `corpus/knowledge/btrfs-scrub-grounding-r45.md` read at
revision 77e9e2b2e96b85d8f048ae2087e246a542b71611 (`git show 77e9e2b2…:corpus/knowledge/btrfs-scrub-grounding-r45.md`,
dumped to scratch). Section hash from the frozen counter equals the value re-derived independently below.

## Hash and digest verification

- `python3 tools/check-scrub-admission-r47.py --revision 77e9e2b2e96b85d8f048ae2087e246a542b71611 --section-hash` →
  GR2 `909830c83cbcf0a02264153fa6f179415fb8388d3e08c43d79fbf33c8cfa11a2`, `structural_ok: 1`. Matches.
- Independent re-derivation: sha256 over the LF-joined extent from the `## GR2` line up to (exclusive) `## GR3`
  (86 lines) in the dumped file prints the same value `909830c83cbcf0a02264153fa6f179415fb8388d3e08c43d79fbf33c8cfa11a2`.
- Snapshot digests verified with `sha256sum -c SHA256SUMS` before use:
  `.ufo/waves/round-45/frozen/src` → dev-replace.c OK (S247); `.ufo/waves/round-44/frozen/src` → scrub.c OK (S242),
  sysfs.c OK (S243). S249 capture.txt sha256 `f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70`
  matches the entry header.
- Quote verification: all 28 `**Quote.**` lines of the row match their cited snapshot lines after stripping leading
  indentation (the counter's normalizer `' '.join(s.split())` does the same); no quote text is altered. Receipt:
  `.ufo/waves/round-47/w1/R47ResRevGR2/quotes-check.txt`.

## Statement — clause evidence

- Replace start path copies through the scrub code: dev-replace.c:700 `/* the disk copy procedure reuses the scrub code */`
  and :701-703 `btrfs_scrub_dev(fs_info, src_device->devid, 0, …, &dev_replace->scrub_progress, false, true)` inside
  `btrfs_dev_replace_start`. Supported.
- Continuing path: dev-replace.c:1259 `"continuing dev_replace from %s (devid %llu) to target %s @%u%%"` and
  :1265-1268 `btrfs_scrub_dev(fs_info, dev_replace->srcdev->devid, …, false, true)` inside `btrfs_dev_replace_kthread`,
  reached from `btrfs_resume_dev_replace_async`. Supported.
- `readonly` false, `is_dev_replace` true are the last two parameters of `btrfs_scrub_dev`: scrub.c:3081
  `bool readonly, bool is_dev_replace)`. Supported.
- Filesystem-closing check returns `-EAGAIN` first: scrub.c:3094 `if (btrfs_fs_closing(fs_info))` → :3095
  `return -EAGAIN;`, preceding all setup and device checks (scrub.c:3094-3160 read). Supported — this is the
  round-47 amendment and it is correct.
- Setup and workers before the device checks, errors return first: scrub.c:3109 `sctx = scrub_setup_ctx(fs_info, is_dev_replace);`
  → :3114 `ret = scrub_workers_get(fs_info);`, error paths `goto out_free_ctx` / `out` (:3110-3116). Supported.
- Three device checks in order: unknown devid or missing-on-non-replace → scrub.c:3123 `ret = -ENODEV;`
  (condition :3119-3122); non-replace, non-readonly, non-writeable → :3133 `ret = -EROFS;` (:3127-3134);
  outside metadata or replace target → :3142 `ret = -EIO;` (:3138-3139). Supported.
- `-EINPROGRESS` refusal only after those checks: scrub.c:3147 `if (dev->scrub_ctx ||` :3148 `(!is_dev_replace &&`
  :3149 `btrfs_dev_replace_is_ongoing(&fs_info->dev_replace))) {` → :3153 `ret = -EINPROGRESS;`. Supported; the
  refusal path exits without attaching a context (attach is scrub.c:3159 `dev->scrub_ctx = sctx;`, after the block),
  so "no scrub is started" holds.
- Ongoing covers started and suspended, unmount-suspended counts: dev-replace.c:1287
  `case BTRFS_IOCTL_DEV_REPLACE_STATE_SUSPENDED:` in `btrfs_dev_replace_is_ongoing` (:1276-1300), true for STARTED
  and SUSPENDED, false for NEVER_STARTED/FINISHED/CANCELED; `btrfs_dev_replace_suspend_for_unmount` (:1171-1196) flips
  STARTED→SUSPENDED (:1183-1185). Supported.
- Copy running → source device carries the attached context and a privileged progress query answers 0:
  scrub.c:3159 `dev->scrub_ctx = sctx;` attached before any scrub work; scrub.c:3336
  `return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;`. Supported.
- Inference bracket placement is correct: the ioctl passthrough and btrfs-progs printing are marked unpinned
  (`[inference for the ioctl and btrfs-progs side: …]`); nothing else in the row leans on unpinned code.

## The defective clause (this is what keeps the row at `partly`)

- **"When the unmount suspend path runs, it calls `btrfs_scrub_cancel`"** — false against the pinned source. The row's
  own quotes for it, dev-replace.c:1143 `/* Scrub for replace must not be running in suspended state */` and :1144
  `btrfs_scrub_cancel(fs_info);`, sit inside `btrfs_dev_replace_cancel` (function head dev-replace.c:1085,
  `case BTRFS_IOCTL_DEV_REPLACE_STATE_SUSPENDED:` at :1126) — the path where a user cancels a suspended replace
  (ioctl `BTRFS_IOCTL_DEV_REPLACE_CMD_CANCEL`). The actual unmount suspend path,
  `btrfs_dev_replace_suspend_for_unmount` (dev-replace.c:1171-1196, body read whole), only flips STARTED→SUSPENDED
  (:1183-1185), logs `suspending dev_replace for unmount` (:1186), and calls no `btrfs_scrub_cancel`. The only other
  call site in the pinned file, dev-replace.c:1111, is also inside `btrfs_dev_replace_cancel` (STARTED case). No
  pinned source shows any code cancelling the replace's scrub at unmount. The second half of the sentence is fine:
  once that scrub has returned and cleared the context (scrub.c:3222 `dev->scrub_ctx = NULL;`), the query answers
  `-ENOTCONN` (scrub.c:3336). This is the same defect the round-46 residual reviewer documented
  (`.ufo/waves/round-46/r1/V46ResRevGR2.md`); the round-47 amendment adopted the round-46 critic's proposed wording
  (`.ufo/waves/round-46/r1/V46ResCritGR2.md`), which that reviewer's report had already shown to misattribute the
  call. The row's core (replace copies through `btrfs_scrub_dev` with `is_dev_replace` true; non-replace scrubs
  refused `-EINPROGRESS` during a replace; ordering of the early checks) is fully supported, so the verdict is
  `partly`, not `fails`.

Exact replacement text for the defective sentence (replaces "When the unmount suspend path runs, it calls
`btrfs_scrub_cancel`;"):

> Cancelling a suspended replace asks for the cancellation of its scrub (the cancel path's suspended case calls
> `btrfs_scrub_cancel`, dev-replace.c:1143-1144); the unmount path that suspends the replace
> (`btrfs_dev_replace_suspend_for_unmount`, dev-replace.c:1171-1196) only flips the state and calls no scrub cancel,
> so what cancels the replace's scrub at an unmount is not pinned here. Once that scrub has returned and cleared the
> device's scrub context, the query answers `-ENOTCONN`

Bookkeeping for that fix, if adopted: add a Quote for the suspend body (e.g. dev-replace.c:1186
`"suspending dev_replace for unmount"`) and widen S247's declared ranges (`corpus/SOURCES.md` row S247, currently
700-703, 1143-1144, 1235, 1256-1268, 1276-1300) to cover 1171-1196, updating the Limits note that now lists only
(1143-1144, 1235, 1276-1300).

## Host reading — clause evidence

- "The filesystem lists devid 1 only (capture.txt:9)": capture.txt:9 `devinfo 1d02a454-c549-4a35-b567-89d60902af8e/devinfo devids=1`. Supported.
- "the caller has no effective capabilities (capture.txt:1)": capture.txt:1 `captured 2026-10-27T02:09:52Z uid=1000 CapEff=0000000000000000`. Supported; the privileged progress query being out of reach follows from S240's registered finding (scrub ioctls return EPERM without CAP_SYS_ADMIN).
- "`exclusive_operation` names `device replace` while a replace holds the exclusive operation (sysfs.c:1288)": sysfs.c:1287-1288 `case BTRFS_EXCLOP_DEV_REPLACE: str = "device replace\n";` in `btrfs_exclusive_operation_show`. Supported.
- "the resume path takes it at dev-replace.c:1235": `if (!btrfs_exclop_start(fs_info, BTRFS_EXCLOP_DEV_REPLACE)) {` inside `btrfs_resume_dev_replace_async` ("resume dev_replace procedure that was interrupted by unmount", dev-replace.c:1197-1198). Supported.
- "the replace ioctl takes it around the start, S240 ioctl.c:3190": the claim was verified against the round-43 S240 snapshot by the round-46 residual reviewer; S240 is not in this entry's declared `source:` list and its SOURCES.md ranges (3066-3075, 3118-3140, 5578-5584) do not include 3190 — an imprecision worth a Limits line, but the underlying fact holds. Supported.
- "`devinfo/<devid>/replace_target` reads 1 on the replace's target device (sysfs.c:2015)": sysfs.c:2007-2018
  `btrfs_devinfo_replace_target_show`, :2015 `val = !!test_bit(BTRFS_DEV_STATE_REPLACE_TGT, &device->dev_state);`. Supported.
- "Read on this host by wave seat C2ExecHostRecheck on 2026-10-27 (…§3), both files are mode 444 and read `none` and `0`": `.ufo/waves/round-45/a2w1/C2ExecHostRecheck.md` §3 shows `-r--r--r--` for both `exclusive_operation` and `devinfo/1/replace_target` and `cat` results `none` and `0` as uid 1000. Supported.
- "which this capture does not record": capture.txt is 9 lines; none records either attribute. Supported.

## Residual risk and verification gaps

- Kernel clauses are verified from the digest-checked snapshots only; nothing was executed against the host (no sysfs
  write, no unit start/stop, no scrub, no replace, no privileged ioctl), matching the row's own scope.
- Upstream URLs were not re-fetched; verification rests on the pinned snapshots (all SHA256SUMS verified this run)
  and the frozen capture digest.
- What cancels the replace's scrub at an unmount (close_ctree / disk-io.c) is outside every declared source; the row
  cannot pin it, and the replacement text says so explicitly instead of repeating the false attribution.
- GR1 and GR3 were not reviewed (out of this seat's item); Limits and the gate-status sections were read as context
  only.
