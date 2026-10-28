ROW GR2 VERDICT: holds
SECTION SHA256: a2e955cefbd110ced928407c79b2cedb3cc431734487aa29e74682b23aeb7f3f

# R50RevGR2a — counted reviewer verdict on row GR2

Claim C1, row GR2 of `corpus/knowledge/btrfs-scrub-grounding-r45.md` at the freeze revision
`8029cdba1049df25632c91a23c8db4eefb54be5f`. I did not write the row and am not its author.

## 0. Evidence base

- Entry extracted with the item's exact command to `/fast/scratch/hyaku/tsukuroi-r50/R50RevGR2a/entry.md`
  (307 lines); GR2 spans lines 56-152 (97 lines, 6012 bytes, last row line blank before `## GR3` at 153).
- Section hash recomputed independently in python (`hashlib.sha256`, row lines joined with LF, no trailing LF):
  `a2e955cefbd110ced928407c79b2cedb3cc431734487aa29e74682b23aeb7f3f` — matches the frozen claim; the
  trailing-LF variant gives `67023d9f…`, so the declared convention is the one that reproduces the hash.
- `tools/check-scrub-admission-r50.py --revision 8029cdba… --section-hash` prints the same GR2 hash and
  `structural_ok: 1` (receipt §3). Only this counter mode was run (see §6).
- Snapshot identity, `sha256sum -c SHA256SUMS` in each directory, all OK: **S247** =
  `.ufo/waves/round-45/frozen/src/dev-replace.c` (`f07ef0a0…4f3a`); **S242** =
  `.ufo/waves/round-44/frozen/src/scrub.c` (`f347931b…a5b8`); **S243** =
  `.ufo/waves/round-44/frozen/src/sysfs.c` (`ce146120…1c43`); **S240** =
  `.ufo/waves/round-43/frozen/src/ioctl.c` (`7b3488f2…ba01`, the digest the entry's `source:` line quotes).

## 1. Clause-by-clause against the pinned bytes

**Replace copies through scrub, both entry points.** `.ufo/waves/round-45/frozen/src/dev-replace.c:700` is the
comment `/* the disk copy procedure reuses the scrub code */` and :701-703 the call
`btrfs_scrub_dev(fs_info, src_device->devid, 0, … , &dev_replace->scrub_progress, false, true)`, so the last two
arguments are `readonly=false, is_dev_replace=true` as stated. The resume path,
`.ufo/waves/round-45/frozen/src/dev-replace.c:1265-1268`, calls the same function on
`dev_replace->srcdev->devid` from `committed_cursor_left` with `false, true`. Clause holds.

**`-EAGAIN` first.** `.ufo/waves/round-44/frozen/src/scrub.c:3094-3095` (`if (btrfs_fs_closing(fs_info))` /
`return -EAGAIN;`) is the first error return; the only code before it is the `progress->last_physical` store at
:3091-3092, which returns nothing. Clause holds.

**Context and workers before the device checks.** `.ufo/waves/round-44/frozen/src/scrub.c:3109-3111`
(`scrub_setup_ctx` → `PTR_ERR`) and :3114-3116 (`scrub_workers_get` → `out_free_ctx`), both before the
`device_list_mutex` block at :3118. Clause holds.

**The three device checks, in the stated order and with the stated conditions.**
`.ufo/waves/round-44/frozen/src/scrub.c:3120-3124` is `!dev || (MISSING && !is_dev_replace)` → `-ENODEV`;
:3129-3134 is `!is_dev_replace && !readonly && !WRITEABLE` → `-EROFS`;
:3138-3143 is `!IN_FS_METADATA || REPLACE_TGT` → `-EIO`. Each condition matches the row's wording exactly,
including that a missing device is tolerated only on a replace call and that the `-EIO` test is unconditional.
Clause holds.

**`-EINPROGRESS` last, both disjuncts.** `.ufo/waves/round-44/frozen/src/scrub.c:3147-3154`:
`dev->scrub_ctx || (!is_dev_replace && btrfs_dev_replace_is_ongoing(...))` → `ret = -EINPROGRESS`. The first
disjunct carries no `is_dev_replace` guard, so "any call is refused … while the device already carries a scrub
context" is exact; the second is guarded, matching "a call with `is_dev_replace` false". "Only after those
checks" holds — the refusal sits below all three device checks. "and no scrub is started" holds: the `goto out`
path is :3251-3256 (`scrub_workers_put`, `scrub_free_ctx`, `return ret`), above the attach at :3159.

**`btrfs_dev_replace_is_ongoing` semantics.** `.ufo/waves/round-45/frozen/src/dev-replace.c:1278-1279`
(`!is_valid` → `false`), the switch at :1281-1287 (NEVER_STARTED/FINISHED/CANCELED → `false` at :1285;
STARTED at :1286 and SUSPENDED at :1287 fall through), the comment :1288-1297 (a replace suspended by an
umount still counts; it needs manual cancellation), and `return true` at :1300. So "true iff valid and
started-or-suspended" is exactly the code. Clause holds.

**Copy-time context on the source device.** `.ufo/waves/round-44/frozen/src/scrub.c:3159` attaches
`dev->scrub_ctx = sctx` before the copy loop and :3222 clears it on completion, so the source device carries the
context while the copy runs. Clause holds.

**Cancel paths.** `.ufo/waves/round-45/frozen/src/dev-replace.c:1111` calls `btrfs_scrub_cancel` in the STARTED
arm; the SUSPENDED arm :1126-1144 calls it at :1144 under the comment at :1143, while :1128 says the replace
scrub "isn't running" in that state. The row states both facts and the tension instead of resolving it, which is
what the bytes support. Clause holds.

**Progress query.** `.ufo/waves/round-44/frozen/src/scrub.c:3330-3336`: `sctx = dev->scrub_ctx`, copy when
present, `return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;` — so a present devid without a context gives
`-ENOTCONN` and an unknown devid `-ENODEV`. The :3222 citation supplies the reachable "context absent" state.
Clause holds.

**Unmount suspend path.** `.ufo/waves/round-45/frozen/src/dev-replace.c:1171-1195` is exactly
`btrfs_dev_replace_suspend_for_unmount` (next function at :1197), and the range does not run into it. The switch
:1177-1191 breaks on the four terminal states and on STARTED at :1184-1188 sets SUSPENDED, `time_stopped` and
`item_needs_writeback`. There is no `btrfs_scrub_cancel` call anywhere in :1171-1195. "only moves a STARTED
replace to SUSPENDED" is exact. Clause holds.

**`[inference]` block.** `.ufo/waves/round-43/frozen/src/ioctl.c:3093-3095` calls `btrfs_scrub_dev` with
`is_dev_replace=false` and the caller's `readonly` flag; :3109-3110 overrides `ret` with `-EFAULT` only when the
args copy-back fails; :3115 is `return ret;`. So "returns the `btrfs_scrub_dev` value unless the argument copy
fails" is exact for the post-call path. The mark's scope — how `btrfs scrub start`/`status` *print* — is correct:
no pinned snapshot contains btrfs-progs userspace source (the r44 snapshot holds only the two units and
`PKGBUILD`), so the printing consequence is genuinely undecided here.

**Host reading.** `.ufo/waves/round-45/frozen/hostcap/capture.txt:1` is `uid=1000 CapEff=0000000000000000` and
`:9` is `devinfo …/devinfo devids=1`, matching "no effective capabilities" and "lists devid 1 only". The 9-line
capture records neither `exclusive_operation` nor `replace_target`, so "which this capture does not record" is
true. The privileged query's refusal is `.ufo/waves/round-43/frozen/src/ioctl.c:3132-3133`
(`capable(CAP_SYS_ADMIN)` → `-EPERM`) in `btrfs_ioctl_scrub_progress`. The sysfs half is source-decided:
`.ufo/waves/round-44/frozen/src/sysfs.c:1288` (`str = "device replace\n";`), registered at :1302 as a
`BTRFS_ATTR` whose mode is `0444` (`sysfs.c:76-78`), and :2015 (`val = !!test_bit(BTRFS_DEV_STATE_REPLACE_TGT…)`)
registered at :2019 as `BTRFS_ATTR(devid, replace_target, …)`; `.ufo/waves/round-45/frozen/src/dev-replace.c:1235`
takes the exclusive op on resume and `.ufo/waves/round-43/frozen/src/ioctl.c:3190-3194` takes and releases it
around the replace start (`btrfs_exclop_start` → `btrfs_dev_replace_by_ioctl` → `btrfs_exclop_finish`), which is
"around the start". The row's dated receipt exists and says what it is quoted for: `a2w1/C2ExecHostRecheck.md`
§3 (2026-10-27) and its `host-recheck-probes.txt` §6 lines 32-37 show `-r--r--r--` on both files and reads
`none` / `0`. Clause holds.

## 2. The four round-49 corrections, checked against bytes rather than the sentence

1. *`[inference]` narrowed to btrfs-progs printing* — the bracket now reads "how `btrfs scrub start` and
   `btrfs scrub status` print these returns is not pinned here", and the rest of the bracket states only what
   `ioctl.c:3093-3095, :3109-3110, :3115` decides. Verified.
2. *S240 named in the `source:` line and QUALITY item 7* — `source:` line 1 names `S240` with the ioctl.c
   snapshot path and its `7b3488f2…ba01` digest (the digest I verified), and QUALITY item 7 (line 261) names
   `S240`. Verified.
3. *the `dev-replace.c:1128` quote carries its `* ` prefix* — the Quote is
   `"* Scrub doing the replace isn't running so we need to do the"`, which is the exact text of line 1128 from
   the `*` onward. Verified.
4. *S247/S240 range gaps declared in Limits* — the round-50 Limits bullets declare S247's gaps
   `:1111`, `:1126-1142`, `:1171-1195`, `:1184-1188` and S240's `:3093-3095`, `:3109-3110`, `:3115`, `:3190`.
   Verified, with one reading note in §3 below.

All 29 Quote lines were checked by script, not by eye: each quoted string is an exact substring of the line it
names (29/29), and all 42 distinct `file:line` tokens in the row resolve inside the pinned snapshot they belong
to (no out-of-range citation). Spot examples: `scrub.c:3139` is
`test_bit(BTRFS_DEV_STATE_REPLACE_TGT, &dev->dev_state))) {`; `sysfs.c:2015` is the `REPLACE_TGT` `val`
assignment; `dev-replace.c:1259` is the `@%u%%` info string.

## 3. Universal words and wording nits (non-blocking)

- "Only after those checks", "any call", "only moves a STARTED replace" — all three are borne out by the
  ordering and the switch structure above. No universal word overreaches the quoted code.
- Nit, not a defect: "the replace context" (progress-query clause) is shorthand for the scrub context the
  replace attaches at `scrub.c:3159`; the field actually tested is `dev->scrub_ctx` (`scrub.c:3331`). The row's
  preceding sentence defines the referent, so no reader is misled, and the verdict does not turn on it.
- Nit, not a defect: Limits declares the S247 gap as `:1126-1142` while the row cites `:1126-1144`; the missing
  `1143-1144` sit inside S247's declared range `(1143-1144, 1235, 1276-1300)`, so the cited span is fully
  covered by the union of the two declarations — no undeclared gap, only a split that is easy to misread.
- Nit, not a defect: "unless the argument copy fails" refers to the copy-*back* at `ioctl.c:3109-3110`, not the
  `memdup_user` input copy at :3081-3083; the citations resolve the ambiguity.
- The host values `none` / `0` are an observation, not a pinned-byte fact; they are carried by a dated seat
  receipt rather than an `[inference]` mark. I judge that adequate (the 0444 mode itself is pinned at
  `sysfs.c:76-78`, and the values are re-runnable), and I flag it only because a stricter reading of the
  convention would want the mark.

No defect was found, so no replacement text is proposed and the verdict stays `holds`.

## 4. Verified but not re-derived

- The `corpus/SOURCES.md` registry rows and their declared ranges for S242/S243/S237 — I checked only that the
  Limits text declares the S247/S240 gaps, not that the registry matches those declarations (that is the C3
  adjacency counter's axis).
- The counter's full predicate (`structural_ok/corr_ok/quotes_ok/verdicts_ok/seats_ok/marks_ok`) — I ran
  `--section-hash` only.
- GR1 and GR3 content; I read them not at all, and the front matter only by `grep -n 'S240\|S247'`.
- I read the Limits section (outside GR2) solely to check correction 4, as the item instructs.

## 5. What I did not do

- No live host probe: I did not `cat` the sysfs attributes or re-run `capture.sh`; I read the frozen capture
  (digest-registered) and the seat's receipt. The `none` / `0` values are therefore second-hand to this seat.
- No upstream re-fetch; all source claims rest on the digest-verified snapshots above.
- No evaluation of btrfs-progs printing (correctly marked `[inference]` in the row and out of this row's scope).
- No git/jj mutation, no fixture repo, no selftest-bearing command; scratch
  `/fast/scratch/hyaku/tsukuroi-r50/R50RevGR2a` was removed after the receipt was copied to
  `.ufo/waves/round-50/w1/R50RevGR2a/receipt.txt`.
