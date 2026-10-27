VERDICT: defect-found

C2-3 / GR2 call paths, wave a2w1. All line numbers are Linux v7.2.11 `fs/btrfs/*` at tag v7.2.11 (peeled
a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea, the commit `frozen/src/FETCH.txt` pins). GR2's core propositions hold; its
universal "any device of that filesystem" does not. Receipts: `.ufo/waves/round-45/a2w1/C2ExecKernelGR2/`.

## 0. Sources, and that the pinned snapshots are the real files

Fetched `fs/btrfs/{ioctl.c,dev-replace.c,scrub.c,volumes.c}?h=v7.2.11` from git.kernel.org stable plain/ (access
2026-10-27) into scratch, and separately took a `--depth 1 --single-branch -b v7.2.11` clone whose HEAD is
`a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea`. Then:

- sha256 of the fetched files equal the blobs at that HEAD (`git show HEAD:fs/btrfs/<f>`): ioctl.c
  `7b3488f2f8356313…`, dev-replace.c `f07ef0a0d260cf67…`, scrub.c `f347931b795c738d…`, volumes.c
  `ff93893dedc4df9b…`.
- The pinned snapshots are byte-identical to those: `diff -q` pinned-vs-fetched is silent and the digests match the
  counter's `SNAP` table — S242 `scrub.c` = `f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8`,
  S247 `dev-replace.c` = `f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a`
  (`C2ExecKernelGR2/sha256-and-diff.txt`).

So the comparison the item asks for is: identical, no drift, and the GR2 quotes below are checked against the
authoritative blob rather than only against the frozen copy.

## 1. Every caller of `btrfs_scrub_dev`, with `readonly` and `is_dev_replace`

`git grep -n btrfs_scrub_dev HEAD` over the whole tree: 9 hits, all inside `fs/btrfs`, of which exactly three are
calls (the rest are the declaration `fs/btrfs/scrub.h:12`, the definition `fs/btrfs/scrub.c:3079`, two strings in
`dev-replace.c:948` and a comment `volumes.c:2748`). Tree-wide, nothing outside `fs/btrfs` calls it
(`C2ExecKernelGR2/callers-treewide.txt`).

| # | Site | devid | start / end | progress | `readonly` | `is_dev_replace` |
|---|------|-------|-------------|----------|-----------|------------------|
| 1 | `dev-replace.c:701-703` in `btrfs_dev_replace_start` | `src_device->devid` | `0` / `btrfs_device_get_total_bytes(src_device)` | `&dev_replace->scrub_progress` | `false` | `true` |
| 2 | `dev-replace.c:1265-1268` in `btrfs_dev_replace_kthread` (1249) | `dev_replace->srcdev->devid` | `dev_replace->committed_cursor_left` / total bytes | `&dev_replace->scrub_progress` | `false` | `true` |
| 3 | `ioctl.c:3093-3095` in `btrfs_ioctl_scrub` (3066) | `sa->devid` | `sa->start` / `sa->end` | `&sa->progress` | `sa->flags & BTRFS_SCRUB_READONLY` | `false` |

Signature confirms the last two parameters: `scrub.c:3079-3081` — `int btrfs_scrub_dev(struct btrfs_fs_info *fs_info,
u64 devid, u64 start, u64 end, struct btrfs_scrub_progress *progress, bool readonly, bool is_dev_replace)`.

Reading 1 and 2 as GR2 states them is correct, and additionally: caller 2 is reached from
`btrfs_resume_dev_replace_async` (1198), which only starts the kthread after `btrfs_exclop_start(fs_info,
BTRFS_EXCLOP_DEV_REPLACE)` succeeds (1235-1243); the two `is_dev_replace` true callers are the only ones, and the
only `readonly` true case is the ioctl with `BTRFS_SCRUB_READONLY` (`include/uapi/linux/btrfs.h:190`, and it is the
sole supported flag, `:191`).

## 2. `btrfs_dev_replace_is_ongoing`: which states count

`dev-replace.c:1276-1300`:

- 1278-1279 — `if (!dev_replace->is_valid) return false;` (`is_valid` set when the on-disk item is read at mount,
  150; at replace start, 667; cleared in init, 120).
- 1282-1285 — `NEVER_STARTED` (0), `FINISHED` (2), `CANCELED` (3) → `return false`.
- 1286-1287 — `STARTED` (1) and `SUSPENDED` (4) → `break`, falling through to `return true` at 1300 (state numbers:
  `include/uapi/linux/btrfs.h:212-216`).

So **both started and suspended count**, and the comment at 1288-1297 says so deliberately ("return true even if
tgtdev is missing"). Consequences the row's "while a replace runs" misses:

- a replace suspended by unmount (1171-1195, state → SUSPENDED at 1184-1186) and remounted still refuses scrubs;
- a replace whose resume found another exclusive op is put back to SUSPENDED (1235-1239) while no copy is running,
  and still refuses scrubs;
- conversely `STARTED` is set at 661 (`is_valid` 667) before the copy is even attempted at 701, so the window
  between the two also refuses.

## 3. Does `EINPROGRESS` reach userspace unchanged?

Yes. `btrfs_ioctl_scrub`, `ioctl.c:3066-3116`:

- 3072-3073 `EPERM` without `CAP_SYS_ADMIN`; 3075-3077 `EINVAL` for `EXTENT_TREE_V2`; 3084-3085 `EOPNOTSUPP` for
  flags outside `BTRFS_SCRUB_SUPPORTED_FLAGS`; 3087-3091 `mnt_want_write_file(file)` for a non-readonly request
  (a read-only mount is refused here, before `btrfs_scrub_dev` is entered).
- 3093-3095 the call; 3109-3110 `copy_to_user(arg, sa)` overrides `ret` only with `-EFAULT`; 3112-3113
  `mnt_drop_write_file` (void); **3115 `return ret;`** — no remap of `-EINPROGRESS`.

Userspace therefore sees `ioctl(BTRFS_IOC_SCRUB)` fail with `errno == EINPROGRESS` (dispatch `ioctl.c:5578-5579`),
with the args copied back carrying `progress.last_physical = sa->start` (`scrub.c:3091-3092` sets it before any gate).
Nothing was started: the `-EINPROGRESS` branch (`scrub.c:3147-3155`) jumps to `out:` (3248) →
`scrub_workers_put` (3249) → `scrub_free_ctx` (3251), and `dev->scrub_ctx` is only assigned later, at 3159.

## 4. Everything `btrfs_scrub_dev` can answer before `EINPROGRESS`, in order

`scrub.c:3079-3155`:

| line | return | condition | fires first during a replace? |
|------|--------|-----------|-------------------------------|
| 3094-3095 | `-EAGAIN` | `btrfs_fs_closing` (`fs.h:1173-1176`, `BTRFS_FS_CLOSING_START`) | yes, if the fs is closing (unmount / remount-ro) while the replace exists |
| 3109-3111 | `-ENOMEM` | `scrub_setup_ctx` alloc failure | unrelated |
| 3114-3116 | `-ENOMEM` | `scrub_workers_get` | unrelated |
| 3120-3123 | `-ENODEV` | devid not found, **or** device `MISSING` and `!is_dev_replace` | yes, for an unknown devid and for a **missing source device** (degraded mount is allowed during a replace, `dev-replace.c:180-187`) |
| 3127-3134 | `-EROFS` | `!is_dev_replace && !readonly && !BTRFS_DEV_STATE_WRITEABLE` | only for a non-readonly request on a non-writeable device |
| 3138-3143 | `-EIO` | device not `IN_FS_METADATA`, **or** `BTRFS_DEV_STATE_REPLACE_TGT` | **yes — the replace target, see §5** |
| 3147-3155 | `-EINPROGRESS` | `dev->scrub_ctx` (set 3159, cleared 3222) **or** (`!is_dev_replace && is_ongoing`) | the answer under discussion |

**Exclusive operations: none.** `scrub.c` contains no `btrfs_exclop_start`/`btrfs_exclop_start_try_lock` call at all,
and `btrfs_ioctl_scrub` (3066-3116) takes no exclusive op either; the only `EAGAIN` in the file is 3095. So a held
`EXCLOP_DEV_REPLACE` (or `EXCLOP_BALANCE`) refuses nothing *by itself*: the refusal comes from the replace state
alone, and — a consequence the row leaves implicit — **a running balance does not refuse a scrub at all** in
v7.2.11, so `EINPROGRESS` must not be read as "something exclusive is running". (A balance can instead *pause* a
scrub after it passes these gates: `__scrub_blocked_if_needed` at `scrub.c:3166`, whose pause is requested on every
transaction commit, `transaction.c:2419`, and around block-group relocation, `volumes.c:3650` — a stall, not an
errno.)

## 5. Is GR2's "any device of that filesystem" right? — No, it is overbroad

(a) **The replace target is answered `EIO`, not `EINPROGRESS`.** The target is allocated with `devid =
BTRFS_DEV_REPLACE_DEVID` (`dev-replace.c:241`, 285), and that constant is `0ULL`
(`include/uapi/linux/btrfs_tree.h:136`; `volumes.h:680` notes it "is 0"). It is marked
`BTRFS_DEV_STATE_REPLACE_TGT` (309), `IN_FS_METADATA` (308) and `WRITEABLE` (295), and linked into
`fs_devices->devices` (321). `btrfs_find_device` matches by devid alone (`volumes.c:7391-7414`, matcher
7365-7382), so a scrub ioctl with `sa->devid == 0` during a replace finds the *target* and is refused at
`scrub.c:3138-3143` with `-EIO` — before the `EINPROGRESS` check is reached. (On finishing, 970-972 clear the bit
and give the target the source's devid, so this window is exactly the replace's lifetime.)

(b) **`ENODEV` precedes it** for a devid that is not in the filesystem (3120-3123) and for a missing source device
(3121-3123 with `!is_dev_replace`). A replace on a degraded mount whose source is gone refuses scrub with
`ENODEV`, not `EINPROGRESS`.

(c) **`EROFS` precedes it** for a non-readonly scrub of a device whose `WRITEABLE` bit is clear (3127-3134), and
above the function: `mnt_want_write_file` (ioctl.c:3088) on an ro mount, `EPERM` (3072), `EOPNOTSUPP` (3085).

(d) **"although no scrub was started" is inexact for the source devid.** There the replace's own copy holds a scrub
context (`scrub.c:3159`), so that devid's `EINPROGRESS` comes from the first disjunct `dev->scrub_ctx`, not from
`is_ongoing`; and `btrfs_scrub_progress` (3321-3337) copies that context's `stat`, which is what makes the SR7
"progress query answers 0" inference work.

(e) **"while a replace runs" is too narrow in time**: see §2 — suspended counts as ongoing.

What survives unchanged: the two `is_dev_replace`-true callers and their argument values (§1), the `is_ongoing`
guard applying to every `is_dev_replace`-false call, the per-device `scrub_ctx` guard, and `EINPROGRESS` reaching
userspace untouched (§3). On *this* host, which lists devid 1 only (`frozen/hostcap/capture.txt:9`), a replace of
devid 1 puts the scrub context on devid 1, so a `btrfs scrub start` on the only device still gets `EINPROGRESS`:
the host-level consequence holds, and only the general wording is wrong.

## 6. Proposed narrow text for the GR2 statement

Replace the GR2 sentence "Inside `btrfs_scrub_dev`, a call with `is_dev_replace` false … [inference for the
btrfs-progs side …]" (entry lines 60-66) with:

> Inside `btrfs_scrub_dev` the refusals are ordered: `-EAGAIN` when the filesystem is closing (scrub.c:3094-3095),
> `-ENODEV` for an unknown devid or a missing device (scrub.c:3120-3123), `-EROFS` for a non-readonly request on a
> device without `BTRFS_DEV_STATE_WRITEABLE` (scrub.c:3127-3134), `-EIO` for a device outside fs metadata or
> carrying `BTRFS_DEV_STATE_REPLACE_TGT` (scrub.c:3138-3143), and only then `-EINPROGRESS`, when the device carries a
> scrub context or, for a call with `is_dev_replace` false, while `btrfs_dev_replace_is_ongoing` is true
> (scrub.c:3146-3153); that function counts the states STARTED and SUSPENDED and no other (dev-replace.c:1281-1300).
> So while a replace is started or suspended — not only while its copy runs — a scrub-start ioctl for a device of
> that filesystem that exists, is in fs metadata, is not the replace target and is either writeable or
> readonly-flagged returns `EINPROGRESS` although no scrub was started on that device; the replace target, which
> holds devid `BTRFS_DEV_REPLACE_DEVID` 0 for the duration of the replace (dev-replace.c:241, 309, 321), is answered
> `EIO` first, and a missing or unknown device `ENODEV`. The replace's source device carries a scrub context for the
> copy (scrub.c:3159), so its own `EINPROGRESS` comes from that context, and by SR7 a privileged progress query for
> that devid answers 0. No exclusive operation is consulted: the scrub code takes no exclusive lock, so a held
> replace or balance exclusive op refuses nothing by itself (a running balance instead pauses a scrub after it
> passes these gates, scrub.c:3166). [inference for the btrfs-progs side: how
> `btrfs scrub start` and `btrfs scrub status` print these answers is not pinned here]

This keeps every GR2 proposition token (`btrfs_scrub_dev`, `is_dev_replace`, `btrfs_dev_replace_is_ongoing`,
`EINPROGRESS`, `scrub context`) and every file the row requires. The `How this changes OS triage` bullet ("check
the replace first") stays right and is strengthened: `EIO` on a scrub start during a replace means the devid named
is the replace target, not a disk fault.

## 7. Evidence index

- `C2ExecKernelGR2/callers-treewide.txt` — tree-wide `git grep` for `btrfs_scrub_dev`, `btrfs_dev_replace_is_ongoing`,
  `btrfs_exclop_start` at HEAD.
- `C2ExecKernelGR2/sha256-and-diff.txt` — fetched vs clone vs pinned digests, `diff -q` result, clone HEAD.
- `C2ExecKernelGR2/scrub-dev-refusals.txt` — numbered `scrub.c:3079-3160`.
- `C2ExecKernelGR2/ioctl-scrub-3066-3116.txt` — numbered `btrfs_ioctl_scrub`.
- `C2ExecKernelGR2/is-ongoing.txt` — numbered `dev-replace.c:1276-1300`.
- `C2ExecKernelGR2/replace-start-call.txt`, `replace-resume-call.txt` — numbered caller sites.
- `C2ExecKernelGR2/tgtdev-init.txt` — numbered `dev-replace.c:232-330` (devid 0, REPLACE_TGT, list_add).

## 8. Not done

- No replace, scrub, ioctl or sysfs write was run; the host was not mutated. The `EIO`-on-devid-0 reading is from
  source only; it would need a multi-device fs with a live replace to observe, which is out of bounds here.
- No C2 counter run (this item does not score a row); no C1 counter run.
- The btrfs-progs printing of `EIO`/`EINPROGRESS` was not pinned (the row already marks it `[inference]`); S237 was
  not re-read for this item.
- No tools were installed or upgraded for this seat.
