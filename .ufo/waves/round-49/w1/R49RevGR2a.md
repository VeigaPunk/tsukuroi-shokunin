ROW GR2 VERDICT: holds
SECTION SHA256: d4296085a574e29296fb9baba5a8722766a832a0b15809ccee72ea019ebd027f
Seat R49RevGR2a (reviewer, C1-COUNTED). Read-only on lane content; every claim below is backed by the pinned
snapshot bytes at the paths named. Receipt: `.ufo/waves/round-49/w1/R49RevGR2a/verify.txt` (digest check, section
hash recompute, checker output, 29-Quote exactness sweep). Entry extracted to scratch once with
`git -C <lane> show 55c07cd3…:corpus/knowledge/btrfs-scrub-grounding-r45.md` (blob sha256
81ce009f09aea02b6523a8c3ad4a5a5074d0e2e9eedee6fb1e88a8645ce20546); row = file lines 56–151, the 96 lines from
`## GR2` through the blank line before `## GR3`.

Identity and conventions
- My hash convention: section lines joined with LF, **no** trailing LF, recomputed in Python →
  d4296085a574e29296fb9baba5a8722766a832a0b15809ccee72ea019ebd027f, byte-for-byte the frozen GR2 hash.
  Adding one trailing LF gives 72d6f2b89055b8844380885780306dd54fd8401165a86dd2a0b10ed6b3327f25, so the
  checker's convention is the no-trailing-LF one and mine agrees; no convention gap.
  `check-scrub-admission-r49.py --revision 55c07cd3… --section-hash` prints the same GR2 hash with
  `"problems": []`, `"structural_ok": 1`.
- Snapshot digests: `sha256sum -c SHA256SUMS` exits 0 in all three directories (round-45: dev-replace.c OK;
  round-44: scrub.c OK, sysfs.c OK; round-43: ioctl.c OK). S-row mapping: **S247** =
  `.ufo/waves/round-45/frozen/src/dev-replace.c` (f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a),
  **S242** = `.ufo/waves/round-44/frozen/src/scrub.c` (f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8),
  **S243** = `.ufo/waves/round-44/frozen/src/sysfs.c` (ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43),
  **S240** = `.ufo/waves/round-43/frozen/src/ioctl.c` (7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01).
  All four are tag v7.2.11 (round-45 FETCH.txt:2 `…dev-replace.c?h=v7.2.11`; round-44 FETCH.txt:2 `scrub.c … (tag
  v7.2.11, peeled a2de78ee…)`; round-43 FETCH.txt:1 `tag v7.2.11 = 8316c24e…`), so the row's "Linux v7.2.11"
  scope is the bytes under test, not a nearby release.

Clause checks against the pinned bytes (all citations exist; each line supports its clause)
1. Both replace paths reach the scrub code with `readonly=false, is_dev_replace=true`. Start path, inside
   `btrfs_dev_replace_start` (dev-replace.c:587): comment at :700, call spanning :701-:703 ending
   `&dev_replace->scrub_progress, false, true);`. Resume path, inside `btrfs_dev_replace_kthread`
   (dev-replace.c:1249): :1265-:1268 ends `&dev_replace->scrub_progress, false, true);`, and :1265 passes
   `dev_replace->srcdev->devid`. "the last two parameters of btrfs_scrub_dev" is exact: the signature spans
   scrub.c:3079-3081, `bool readonly, bool is_dev_replace)` at :3081.
2. Error order inside `btrfs_scrub_dev` (scrub.c:3079): `-EAGAIN`-only prelude `btrfs_fs_closing` at :3094 →
   `return -EAGAIN;` :3095 is the first error return (everything before it is the `progress->last_physical`
   store at :3091-3092); context then workers: `scrub_setup_ctx` :3109 (error returns at :3110-3111, before any
   device lookup), `scrub_workers_get` :3114 (`goto out_free_ctx` :3116). The three device checks follow in the
   stated order: `!dev || (MISSING && !is_dev_replace)` :3120-3121 → `ret = -ENODEV;` :3123;
   `!is_dev_replace && !readonly && !WRITEABLE` :3127-3128 → `ret = -EROFS;` :3133;
   `!IN_FS_METADATA || REPLACE_TGT` :3138-3139 → `ret = -EIO;` :3142.
3. EINPROGRESS gate: `if (dev->scrub_ctx || (!is_dev_replace && btrfs_dev_replace_is_ongoing(&fs_info->dev_replace)))`
   at :3147-:3149 → `ret = -EINPROGRESS;` :3153. It is genuinely after the three device checks (it is the next
   block), the `dev->scrub_ctx` disjunct applies to *any* call (so a replace's own second call is refused too),
   and the is_dev_replace-false disjunct carries `down_read(&…dev_replace.rwsem)` at :3146.
4. `btrfs_dev_replace_is_ongoing` (dev-replace.c:1276-1301): `if (!dev_replace->is_valid) return false;`
   :1278-1279 (returns `false`, not just "skips"), switch NEVER_STARTED/FINISHED/CANCELED :1282-1284 return
   false, STARTED/SUSPENDED :1286-1287 break to `return true;` :1300. So it is exactly
   `is_valid && (STARTED || SUSPENDED)` — the row's "valid … and started or suspended" is complete, and it
   correctly does **not** require a present tgtdev (the comment :1288-`*/` at :1297 says true even when tgtdev is
   missing after an unmount-suspension). Range 1288-1297 ends on the closing `*/` at :1297, before `break;` :1298
   — no bleed into the next construct.
5. "no scrub is started": the EINPROGRESS branch jumps to `out:` at :3248 (`scrub_workers_put`, then
   `out_free_ctx:` `scrub_free_ctx(sctx)` :3250-3251, `return ret` :3253), which is before `sctx->readonly = readonly`
   / `dev->scrub_ctx = sctx` :3158-:3159, before `atomic_inc(&fs_info->scrubs_running)` :3167 and before
   `scrub_enumerate_chunks` :3208. The ctx attached during the copy is real: :3159, and the copy path itself is
   `scrub_setup_ctx` wiring `sctx->wr_tgtdev = fs_info->dev_replace.tgtdev` (scrub.c:484-486) with the
   dev-replace submit block at :1982.
6. Cancel call sites — the row attributes each to the right function. `btrfs_dev_replace_cancel` spans
   dev-replace.c:1085-1169. STARTED case: `ret = btrfs_scrub_cancel(fs_info);` :1111. SUSPENDED case:
   `case …SUSPENDED:` :1126, comment :1127-`*/` :1130 starting `Scrub doing the replace isn't running so we need to
   do the` :1128, `btrfs_scrub_cancel(fs_info);` :1144 with its own comment :1143. Range 1126-1144 is inside the
   same function (next `}` :1169) and contains the call; `grep -n btrfs_scrub_cancel dev-replace.c` returns only
   :1111 and :1144, so nothing is misattributed. The clause "the pinned code says the replace scrub is not running
   in that state" is what :1128 says; `btrfs_scrub_cancel` (scrub.c:3277-3296) would return `-ENOTCONN` when
   `scrubs_running` is 0, and :1144 discards the value — consistent with, and not contradicted by, the row.
7. Unmount-suspend function: `btrfs_dev_replace_suspend_for_unmount` is exactly dev-replace.c:1171-1195
   (signature :1171, closing brace :1195; the next function's comment is :1197). Its only state effect is
   STARTED :1184 → `replace_state = SUSPENDED` :1185-1186, `time_stopped` :1187, `item_needs_writeback = 1` :1188,
   plus a log :1189; the other four states only `break` :1179-1183. It contains no `btrfs_scrub_cancel`
   (grep above), so "does not call btrfs_scrub_cancel" holds. "state set at :1184-1188" is exactly that block.
8. Progress query: `btrfs_scrub_progress` (scrub.c:3321-3337) reads `sctx = dev->scrub_ctx` :3332 and returns
   `dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV` :3336; :3222 is the completion-path `dev->scrub_ctx = NULL;` (under
   scrub_lock, :3221-3223) that produces the absent-context state. Both cited lines exist and support the two
   outcomes the row names; an unknown devid is `-ENODEV`, an existing one with no context is `-ENOTCONN`.
9. Host reading. `capture.txt` is `.ufo/waves/round-45/frozen/hostcap/capture.txt` (sha256 f5958a83…, the S249
   artifact): line 1 `captured … uid=1000 CapEff=0000000000000000` and line 9 `devinfo
   1d02a454-…/devinfo devids=1` are quoted correctly. The privilege claim is source-checked, not just asserted:
   `BTRFS_IOC_SCRUB_PROGRESS` dispatches to `btrfs_ioctl_scrub_progress` (ioctl.c:5582-5583), whose
   `if (!capable(CAP_SYS_ADMIN))` :3132 / `return -EPERM;` :3133 decide it for CapEff=0. The sysfs claim is
   also source-checked: `exclusive_operation` is registered `BTRFS_ATTR(, exclusive_operation, …)` sysfs.c:1302 and
   `replace_target` `BTRFS_ATTR(devid, replace_target, …)` sysfs.c:2019, and `BTRFS_ATTR` is
   `__INIT_KOBJ_ATTR(_name, 0444, _show, NULL)` (sysfs.c:76-78) — mode 0444, i.e. readable without privilege, which
   independently supports the row's "readable without privilege". `BTRFS_EXCLOP_DEV_REPLACE → str = "device
   replace\n"` is sysfs.c:1287-1288, the resume path takes the exclop at dev-replace.c:1235, the replace ioctl
   takes/finishes it around `btrfs_dev_replace_by_ioctl` at S240 ioctl.c:3190/:3194, and `replace_target` is
   `!!test_bit(BTRFS_DEV_STATE_REPLACE_TGT, …)` sysfs.c:2015. The measured `none`/`0` and mode 444 are attributed
   to the dated in-repo receipt `.ufo/waves/round-45/a2w1/C2ExecHostRecheck.md` §3, which I read and which does
   record `-r--r--r--` for both files and the values `0` and `none`. The row states plainly that the capture does
   not record these attributes, so no capture-derived claim is smuggled in, and the userspace/ioctl-printing half
   is explicitly bracketed `[inference …]`.
10. Quotes: all 29 `**Quote.**` lines of GR2 are present on the cited line (machine sweep, 0 missing). Two are not
    byte-identical to the line because the leading indentation (and, at :1128, the ` * ` comment marker) is
    stripped — :1128 and :1259 — which is the entry-wide display convention, not altered text; :1259 is the source
    line's own string literal, which is why it renders with doubled quotes.

Defects: none found. No contradicted clause, no range that runs into a neighbouring function, no citation that
fails to support its clause, no unmarked inference, and the only universal words ("Only after those checks",
"only moves") are true of the code: nothing else returns before that point and the suspend path's sole state
effect is STARTED→SUSPENDED with the three fields named.

Non-blocking precision observations (docs-only; they do not change the verdict because the deciding content and
every citation are correct)
- Clause 8 names the referent "the replace context"; the code tests `dev->scrub_ctx`, which is shared with plain
  scrub. Optional tighter wording: replace "When the replace context is absent, the progress query returns
  `-ENOTCONN` for a devid that exists (`scrub.c:3222, :3336`)" with "When that scrub context is absent — the
  completion path clears it at `scrub.c:3222` — the progress query returns `-ENOTCONN` for a devid that exists
  (`scrub.c:3336`)". The referent is recoverable from the preceding sentence ("the scrub context the copy
  attached"), so this is clarity, not error.
- The Host reading's "lists devid 1 only (capture.txt:9)": line 9 gives `devids=1`; the identity of the devid as 1
  comes from line 8's `…/devinfo/1/scrub_speed_max` path. Optional: cite `capture.txt:8-9`.

Verified but not re-derived
- SR7 (the cross-reference "by SR7") and `btrfs_scrub_cancel`'s internal stop semantics beyond what is needed to
  show the two call sites and that a no-running-scrub call returns `-ENOTCONN` (scrub.c:3277-3296). I did not
  re-derive the cancel handshake or the `lock_finishing_cancel_unmount` interaction.
- The host measurements themselves (`none`, `0`, mode 444): I checked the source level (0444 attributes, sysfs
  case mapping) and the receipt's recorded output, but did not re-run the sysfs reads — that is outside this
  item's EXEC-AUTHORIZED command list.
- I did not re-fetch S240/S242/S243/S247 from their URLs; I verified their local digests against each directory's
  SHA256SUMS and their v7.2.11 provenance in FETCH.txt.

What I did not do
- No counter beyond `--section-hash` (no `--selftest`, so no 5-10 min C1/C3 counter run), no mutation, no git/jj
  mutation anywhere, no write to any tracked lane or fleet file, no package install or upgrade (nothing needed),
  no spawn of agents. Wrote only this report and `w1/R49RevGR2a/verify.txt`; scratch under
  `/fast/scratch/hyaku/tsukuroi-r49/R49RevGR2a` was removed after copying the receipt.
