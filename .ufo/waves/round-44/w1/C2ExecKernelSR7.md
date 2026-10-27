VERDICT: defect-found — the SR7 invariant itself (one attach site, clear on every exit path) is CONFIRMED true; the row's two derived labels (`-ENOTCONN idle`, and success(0) read as "a scrub is running") are not true as written, and the row must narrow them. Details and exact line numbers below; proposed replacement text in §10.

Seat: C2ExecKernelSR7 (L2, round 44 / hyaku run 9, wave w1). Item C2-4. Kernel under test: Linux v7.2.11 = tag `v7.2.11`, peeled commit `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea`.

---

## 0. Provenance and scope of what I actually read

Receipts (all under `w1/C2ExecKernelSR7/`): `kernel-tree-receipt.txt`, `scrub_ctx-sites.txt`, `progress-callers.txt`, `scrubdev-order.txt`, `io-join.txt`, `ioctl-surface.txt`, `progs-consumers.txt`, `fetch-receipt.txt`.

- Full `fs/btrfs` of v7.2.11 checked out in scratch (131 entries incl. `tests/`): `git clone --depth 1 --filter=blob:none --sparse --branch v7.2.11 https://github.com/gregkh/linux linux-v7211 && git sparse-checkout set fs/btrfs`; `git rev-parse HEAD` = `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea`, `git describe --tags` = `v7.2.11`. See `kernel-tree-receipt.txt:6-8`.
- The wave's frozen copies are byte-identical to that tree: `fs/btrfs/scrub.c` = `f347931b795c…5b8` = `round-44/frozen/src/scrub.c`; `fs/btrfs/ioctl.c` = `7b3488f2f835…ba01` = `round-43/frozen/src/ioctl.c` (`kernel-tree-receipt.txt:11-14`).
- Extra fetches from the same tag (git.kernel.org `?h=v7.2.11`, 2026-10-26/27, sha256 in `fetch-receipt.txt`): `fs/btrfs/dev-replace.c` (`f07ef0a0d260…4f3a`), `fs/btrfs/volumes.h` (`2750c05115…ba1`), `include/uapi/linux/btrfs.h`, `include/trace/events/btrfs.h`.
- Userspace consumer read from S237 (btrfs-progs v7.1 `cmds/scrub.c`, sha256 `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801`, matching the round-42 frozen copy; provenance `round-42/frozen/src/FETCH.txt:1-2`).
- Line numbers are for `fs/btrfs/scrub.c` of v7.2.11 unless prefixed with a file name.

---

## 1. Every read and write of `scrub_ctx` (asked in the item)

The token `scrub_ctx` occurs **40 times on 40 lines in `fs/btrfs/scrub.c`** and once in `fs/btrfs/volumes.h` (`scrub_ctx-sites.txt`). The *per-device field* `dev->scrub_ctx` — the one the row is about — has exactly **two writes and five reads**:

| line | kind | context | lock held |
|---|---|---|---|
| `scrub.c:3159` | **write (attach)** `dev->scrub_ctx = sctx;` | `btrfs_scrub_dev`, after all rejections | `device_list_mutex` (3118) **and** `scrub_lock` (3137) |
| `scrub.c:3222` | **write (detach)** `dev->scrub_ctx = NULL;` | same function, straight-line after the scan | `scrub_lock` (3221) **only** |
| `scrub.c:3147` | read | start-time exclusion: `if (dev->scrub_ctx \|\| …)` → `-EINPROGRESS` (3153) | `device_list_mutex` + `scrub_lock` + `dev_replace.rwsem` read |
| `scrub.c:3304` | read | `btrfs_scrub_cancel_dev`: take ctx, `-ENOTCONN` if NULL (3305-3307) | `scrub_lock` |
| `scrub.c:3310` | read | `btrfs_scrub_cancel_dev`: wait loop condition | `scrub_lock` (released across the wait, 3311) |
| `scrub.c:3313` | read | `wait_event(…, dev->scrub_ctx == NULL)` predicate | none (wait) |
| `scrub.c:3331` | read | `btrfs_scrub_progress`: `sctx = dev->scrub_ctx` | `device_list_mutex` (3328) **only** |

Declaration: `volumes.h:193` (`struct scrub_ctx *scrub_ctx;` under the comment `/* per-device scrub information */`, `volumes.h:192`). Every other `scrub_ctx` occurrence in `scrub.c` is the *type* name in prototypes/parameters (40, 193, 397, 431, 444, 450, 665, 996, 1144, 1163, 1299, 1341, 1371, 1596, 1873, 1933, 1955, 2029, 2077, 2109, 2159, 2302, 2397, 2431, 2593, 2652, 2945, 2974, 3084, 3301, 3326 — full grep in `scrub_ctx-sites.txt`).

**Conclusion (invariant): the field is written nowhere except `btrfs_scrub_dev`, twice: attach at 3159, detach at 3222. There is no second attach site, no attach outside the two-lock region, and no writer in `dev-replace.c`, `volumes.c`, `disk-io.c` or `tests/`.**

---

## 2. "Cleared at its end on every path, including early error returns after it is set" — TRUE, structurally

- Between the attach (3159) and the clear (3222) there is **no `return` and no `goto out`/`goto out_free_ctx`**. Every error jump is *before* the attach: `3116` (`goto out_free_ctx`, `scrub_workers_get` failure), `3124` (`-ENODEV`), `3134` (`-EROFS`), `3143` (`-EIO`), `3154` (`-EINPROGRESS`). Receipt: `scrubdev-order.txt` (`scrub.c:3080-3255` numbered) — the run 3159-3222 contains only `if` tests (3180, 3202, 3207, 3214, 3217), no exits.
- The only early `return` after the clear is `3240` (the `need_commit` path), i.e. already past `3222`. On that path `scrub_put_ctx` (3226) has also already run, so no leak of the context either.
- Therefore: attach ⇒ exactly one detach, on the single straight-line exit, for success, `-EIO`, `-ENOMEM`, `-ECANCELED` and dev-replace alike. **No path can leave `dev->scrub_ctx` dangling.**
- Two qualifications that matter for the row's semantics (not for the invariant):
  1. the clear is taken **under `scrub_lock` only** (3221-3223) while the attach is under `device_list_mutex` **and** `scrub_lock` (3118/3137/3159), and the only reader of the field that takes `device_list_mutex` (3328-3331) takes **no `scrub_lock`** → the reader and the writer share no lock (§7);
  2. "at its end" is *before* the function's end: 3222 precedes `scrub_workers_put` (3225), `scrub_put_ctx` (3226) and the optional super-error transaction commit (3232-3245).

---

## 3. Window A — success(0) with the scan not started (attach → `scrubs_running++`)

`dev->scrub_ctx = sctx;` (3159) → `__scrub_blocked_if_needed(fs_info)` (3166) → `atomic_inc(&fs_info->scrubs_running)` (3167).

- `__scrub_blocked_if_needed` (`scrub.c:399-407`) loops while `atomic_read(&fs_info->scrub_pause_req)` (401), **dropping `scrub_lock`** (402) and waiting on `scrub_pause_wait` (403-404). It is set by `btrfs_scrub_pause` (`scrub.c:3256-3269`, `atomic_inc(&scrub_pause_req)` at 3259) and cleared by `btrfs_scrub_continue` (3271-3275, `atomic_dec` at 3273). Pause windows are the whole transaction commit (`transaction.c:2144`) and the whole block-group relocation (`volumes.c:3650-3652`).
- During that wait `dev->scrub_ctx` is non-NULL and `scrubs_running` is still 0, so **`btrfs_scrub_progress` returns 0 with a context that has not read a single byte**: `sctx` is `kvzalloc`ed (459) so `sctx->stat` is all zeros, with `last_physical` pre-set to `start` at 3112.
- Consequence #1 (consumer): btrfs-progs decides "a scrub is running in the kernel" purely from that success code — `is_scrub_running_in_kernel()` returns 1 on the first device whose `BTRFS_IOC_SCRUB_PROGRESS` succeeds (`progs-consumers.txt`, S237 `cmds/scrub.c:1197-1202`), and uses it for `btrfs scrub status` → `in_progress` (1946, 1962) and for the stale-status-file override in `scrub start` (1378-1379). In window A that flag is already 1.
- Consequence #2 (defect, action direction): inside window A, `BTRFS_IOC_SCRUB_CANCEL` cannot cancel. `btrfs_ioctl_scrub_cancel` (`ioctl.c:3123`) calls `btrfs_scrub_cancel`, which tests **`scrubs_running`, not `scrub_ctx`** (`scrub.c:3280-3282`) and returns `-ENOTCONN` while `scrubs_running` is 0 — and it returns *without* setting `scrub_cancel_req` (3285). The SIGINT handler of `btrfs scrub start -B` (`cmds/scrub.c:421`, installed per §SR9) only does `perror("Scrub cancel failed")` (`cmds/scrub.c:422-423`). So a `SIGINT` landing in window A is **dropped** and the scrub then runs to completion uncancelled. `btrfs_scrub_cancel_dev` (3298-3319) would have worked (it keys on `scrub_ctx`), but the ioctl does not use it.

---

## 4. Window B — success(0) after the work has ended, before the clear

`atomic_dec(&fs_info->scrubs_running)` (3211) → `wake_up` (3212) → `memcpy(progress, &sctx->stat, …)` (3214-3215) → `btrfs_info` (3217-3219) → `dev->scrub_ctx = NULL` (3222).

- In this window the scan is finished (all I/O joined, §6), `scrubs_running` is 0, and `dev->scrub_ctx` is still set. The two "is it idle?" signals that a caller can observe **disagree**: `btrfs_scrub_progress` = 0 ("attached") while `btrfs_scrub_cancel` = `-ENOTCONN` ("not running", 3280-3282) and `btrfs_scrub_cancel_dev` = 0 (3304-3314, it waits for the clear).
- `btrfs scrub status` run in this window reports `in_progress=1` from the finished scrub (1946 + 1962).

## 5. Window C — `-ENOTCONN` while the scrub's own ioctl is still executing

- `3222` (clear) → `3225` `scrub_workers_put` → `3226` `scrub_put_ctx` (the refcount is 1 from 462 and `refs` is only ever decremented once, 444-448, so `scrub_free_ctx`/`kvfree` happens **here**) → `3232-3245` optional `btrfs_start_transaction`/`btrfs_commit_transaction` for super-block errors (`need_commit` set at 3202-3203) → `3247 return ret`.
- Throughout that tail, `btrfs_scrub_progress` returns `-ENOTCONN`, and a **new** scrub start on the same device is now accepted (the 3147 test passes) even though the previous `btrfs_scrub_dev` has not returned. So `-ENOTCONN` does not mean "the start ioctl has returned", and it does not mean "the device has no scrub in flight" once the previous start is in its commit tail: it means exactly "no context attached at this instant".
- Window C is unbounded in principle: `btrfs_commit_transaction` (3242) can wait arbitrarily long on a busy filesystem, and on `IS_ERR(trans)` the function returns a *new* error code (3236-3240) after the context is gone.

**Answer to "ENOTCONN while one runs?":** not while scrub I/O is in flight (§6 proves the ordering), but yes while the scrub's start ioctl is still running, and yes for a cancel that arrives in window A (which is the harmful direction).

## 6. Why no I/O or worker outlives the clear (so no use-after-free of `sctx` by I/O)

- All repair work runs on `fs_info->scrub_workers` (`queue_work` at 1271 and 1869, worker `scrub_stripe_read_repair_worker` at 1160) and signals completion with `SCRUB_STRIPE_FLAG_REPAIR_DONE` (`set_bit` at 1247).
- `flush_scrub_stripes` (1955-2022) submits the pending stripes (1968-1972), **waits for `REPAIR_DONE` on every stripe** (1974-1979), submits dev-replace writes (1982-2007) and then **waits for all bios** (`wait_scrub_stripe_io`, 2010-2018).
- `scrub_stripe`'s single `out:` (2567) calls `flush_scrub_stripes` unconditionally (2568), so every exit from a chunk — success, `-EIO`, cancel — flushes; `flush_scrub_stripes` is also called when the stripe ring fills (2066). raid56 parity stripes join at 2240-2258 (`wait_event(… REPAIR_DONE …)`).
- Hence by the time `scrub_enumerate_chunks` returns (3208) no scrub-owned bio or worker can still touch `sctx`, and the clear at 3222 cannot race with scrub I/O. (`io-join.txt`.)

## 7. The reader/writer race on the field itself (depth finding; consequence is [INFERENCE])

- Writer: `mutex_lock(&fs_info->scrub_lock); dev->scrub_ctx = NULL;` (3221-3223), then free at 3226.
- Reader: `mutex_lock(&fs_info->fs_devices->device_list_mutex); … sctx = dev->scrub_ctx; … memcpy(progress, &sctx->stat, …)` (3328-3334).
- The two paths share **no lock** for the field (lock order elsewhere is `device_list_mutex` → `scrub_lock`, 3118 then 3137, so there is no inversion, just no exclusion), and there is no `READ_ONCE`/`WRITE_ONCE`. Two consequences: (a) a reader can observe a stale non-NULL pointer after the clear, i.e. report progress for a finished scrub; (b) [INFERENCE] a reader that loaded the pointer and is inside the `memcpy` can race the `kvfree` at 3226 — the read is not protected by `scrub_lock` and `sctx->refs` has no second reference holder (462/444-448). I did not run KASAN/SyzKaller, so (b) is a code-shape inference, not an observed crash.
- The copied stat is also not a consistent snapshot: the reader's `memcpy` (3333, and the start path's at 3215) takes no `sctx->stat_lock`, while the writers update `stat` under it (2014-2016, 2341-2343, 2539-2542, 2563-2565, 2989-2991, 3007-3009, 3021-3023, 3183-3185, 3196-3204). Counters can therefore be mutually inconsistent by one stripe, and individual `u64`s can tear on a 32-bit kernel [INFERENCE].

## 8. `-ENODEV` and what a caller actually receives on failure

- `btrfs_scrub_progress` returns `dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV` (`scrub.c:3336`). So `-ENODEV` ⇔ the `devid` is not in `fs_devices` at all; a **missing-but-registered** device (`BTRFS_DEV_STATE_MISSING` still on the list) yields `-ENOTCONN`, not `-ENODEV`. (Contrast the start path, which returns `-ENODEV` for `!dev` too but additionally for a `MISSING` device when not replacing: 3120-3126.)
- On any non-zero return the progress ioctl does **not** touch user space — `if (ret == 0 && copy_to_user(arg, sa, sizeof(*sa)))` (`ioctl.c:3141`). So `-ENOTCONN`/`-ENODEV` carry no data, while success(0) carries the possibly-all-zero snapshot of window A.
- The **start** ioctl copies back even on error (`ioctl.c:3109`, with the explanatory comment at 3097-3107), and `btrfs_scrub_dev` pre-sets `progress->last_physical = start` at 3092 before any context exists. `sa` is a `memdup_user` copy (`ioctl.c:3080`) — the other progress fields are whatever the caller passed. A failed start therefore looks exactly like "resume point = start, zero bytes scrubbed", which is the same shape as window A.

## 9. Caller inventory of `btrfs_scrub_progress` at v7.2.11

- **Exactly one caller in the tree**: `ioctl.c:3139` inside `btrfs_ioctl_scrub_progress` (`ioctl.c:3126-3143`), reached from the dispatch at `ioctl.c:5582-5583` (`BTRFS_IOC_SCRUB_PROGRESS`, uapi `btrfs.h:1196-1197`). Declaration only at `scrub.h:19-20` (`progress-callers.txt`).
- Not exported: `grep -c EXPORT_SYMBOL fs/btrfs/scrub.c` = 0, and the prototype lives in the private `fs/btrfs/scrub.h`, so no other module can bind the symbol. `fs/btrfs` (131 entries incl. `tests/`) was grepped exhaustively; the caller claim is "no caller outside `fs/btrfs`" by construction (private header + unexported symbol), not by a completed whole-tree content sweep — see §11 for the exact scope of the sweep I attempted.
- The other user of the same machinery needs no progress ioctl at all: device replace calls `btrfs_scrub_dev(…, srcdev->devid, …, &dev_replace->scrub_progress, readonly=false, is_dev_replace=true)` at `dev-replace.c:700-703` and `dev-replace.c:1264-1268`; the progress is then reported through `BTRFS_IOC_DEV_REPLACE`.
- **Window D (dev-replace) is a full-lifecycle zero, not a window**: the context attaches to the **source** device (devid = `srcdev`), because the target is explicitly rejected at `scrub.c:3140-3143` (`BTRFS_DEV_STATE_REPLACE_TGT` → `-EIO`). So `BTRFS_IOC_SCRUB_PROGRESS(srcdevid)` returns 0 for the whole copy — with `stat` filled by the copy — although no scrub is running, and `BTRFS_IOC_SCRUB_PROGRESS(tgtdevid)` returns `-ENOTCONN`. btrfs-progs' `is_scrub_running_in_kernel` therefore reports "running" during a replace (it iterates all devices and stops at the first success, `cmds/scrub.c:1197-1202`).

## 10. What SR7's statement must narrow — exact proposed text

Two changes are needed: (i) say that the return code classifies **context attachment**, not I/O or the start ioctl's lifetime; (ii) list the windows. Suggested replacement for the SR7 clause (length-constrained; keep the two source pointers):

> SR7 — `btrfs_scrub_progress` (`scrub.c:3321-3337`) classifies **attachment**, not activity: `0` while `dev->scrub_ctx` is non-NULL, `-ENOTCONN` when no context is attached, `-ENODEV` when the `devid` is absent from `fs_devices` (`scrub.c:3336`; a missing-but-registered device gives `-ENOTCONN`). `scrub_ctx` is attached at exactly one site, `scrub.c:3159`, under `device_list_mutex`+`scrub_lock`, and cleared at `scrub.c:3222` under `scrub_lock` only, with no `return`/`goto` between the two, so the context is never left attached — but `0` also covers (a) the attach-to-start window `3159→3167`, in which `__scrub_blocked_if_needed` (399-407, called at 3166) can block for a whole transaction commit before `scrubs_running` is incremented, leaving `stat` all-zero with `last_physical = start` (3112, `kvzalloc` at 459); (b) the post-scan window `3211→3222`; and (c) a device replace, which attaches to the **source** device (`dev-replace.c:700-703`, `1264-1268`; the target is rejected at `scrub.c:3140-3143`). `-ENOTCONN` does **not** mean the start ioctl has returned (the clear precedes `scrub_workers_put`/`scrub_put_ctx` at 3225-3226 and the optional super-error commit at 3232-3245), and it is what `BTRFS_IOC_SCRUB_CANCEL` → `btrfs_scrub_cancel` returns (`scrub.c:3280-3282`, keyed on `scrubs_running`) inside window (a), where the cancel request is dropped (`cancel_req` is not set, 3285) and the scrub proceeds; `btrfs_scrub_cancel_dev` (3298-3319, keyed on `scrub_ctx`) is the per-device variant. On non-zero the ioctl does not copy the struct to user space (`ioctl.c:3141`); on `0` the copy at `scrub.c:3333` is taken without `stat_lock` and is not an atomic snapshot.

(If the row has a hard word budget, the minimum narrowing is: replace `-ENOTCONN idle` with `-ENOTCONN = no context attached (idle, or the start ioctl's own tail after the clear at 3222, or a cancel that arrives between 3159 and 3167 and is dropped)`, and add `0 also covers 3159→3167 (can block before start), 3211→3222, and a dev-replace source device`.)

## 11. What I did NOT do

- No host mutation of any kind: no scrub start/cancel/resume/limit, no sysfs write, no sysfs write to `scrub_speed_max`, no mount, no service/unit/timer action, no sudo, no package transaction. All work was on a scratch clone under `/fast/scratch/hyaku/tsukuroi-r44/C2ExecKernelSR7/` plus read-only reads of lane files.
- No counter run: `tools/check-scrub-record-r44.py` scores md rows and needs wave-2 verdicts; the item asked for a kernel-path reading, and wave 1 must not produce counted verdicts. I did not run `score-scrub-arm-r44.py` either (unrelated to C2, ~30 s heavy).
- Whole-tree content sweep beyond `fs/btrfs` was **attempted and not completed**: `git grep --cached -n "btrfs_scrub_progress|btrfs_scrub_dev|btrfs_scrub_cancel_dev" -- include/` in the blobless clone hit my 240 s cap (`timeout 240`, exit 124, killed by me) because blobs outside the sparse set must be fetched on demand. What I did instead, and stand on for §9: (i) the declaration exists only in the private `fs/btrfs/scrub.h:19-20`, (ii) `fs/btrfs/scrub.c` has zero `EXPORT_SYMBOL`, so no module outside `fs/btrfs` can bind the symbol, and (iii) the two `include/` headers that could plausibly name it were fetched by curl and grepped: `include/trace/events/btrfs.h` has **no** `scrub` reference at all and `include/uapi/linux/btrfs.h` has only the struct and ioctl numbers (`progress-callers.txt`). My first-pass `git grep -- ':!fs/btrfs'` on the sparse clone was **vacuous** (no blobs outside the sparse set) and is not used as evidence anywhere in this report.
- No kernel build, no KASAN/SyzKaller run, no runtime reproduction: §3/§5 windows and §7 item (b) are established from code ordering, with the crash consequence explicitly marked [INFERENCE].
- I did not inspect `/sys` or the live host: the claims here are kernel-source claims at tag `v7.2.11`, deliberately independent of this host's kernel version.

## 12. One-line answer to the item

`scrub_ctx` is set only in `btrfs_scrub_dev` (3159) and cleared on every exit after that (3222, no paths in between); but success(0) and `-ENOTCONN` are *attachment* signals, not activity signals — progress returns 0 with no scan running for three reasons (attach→start, scan-end→clear, dev-replace source device), and `-ENOTCONN` coexists with a still-executing start ioctl and with a dropped `BTRFS_IOC_SCRUB_CANCEL` in the attach→start window. SR7 must narrow accordingly (§10).

---

## 13. Cross-check against the sibling SR7 pre-read (`w1/C2DraftCritSR7.md`, item C2-12) — one of its conclusions does not survive this reading

That seat read the same sources and concluded (`w1/C2DraftCritSR7.md:24`, item 5): "The device-with-context interval [3159, 3222] is exactly the actively-scrubbing interval, so the momentary reading is faithful even though the function's own lifetime is longer." Its own earlier bullet (`:22`-ish for item 1) had already flagged only the *pre-attach* / *post-detach* prefix and tail, i.e. it treats `[3159, 3222]` as the active interval.

That is the one point where this seat disagrees, on the same code:

- `[3159, 3222]` contains three sub-intervals with **no scan activity at all**:
  - `3159 → 3167`: attached, `scrubs_running` still 0, and `__scrub_blocked_if_needed` (called at 3166, defined 399-407) may block for an entire transaction commit or block-group relocation before the increment (§3). So the "actively-scrubbing" interval can start arbitrarily late inside the attach interval.
  - `3211 → 3222`: scan finished and `scrubs_running` decremented, context still attached (§4).
  - the whole dev-replace case, where the "scrub" is a read pass for the copy and the context is on the **source** device (§9): not a scrub at all, yet `is_scrub_running_in_kernel` (S237 `cmds/scrub.c:1197-1202`) reports it as one.
- The sibling's "an idle device answers `ENOTCONN`, never 0" is true only if "idle" means "no context attached"; a device that is not being scanned can answer 0 in all three cases above.
- The sibling is right that no return path leaves the field set, and right about the lookup/return logic (`scrub.c:3328-3336`), the `ret == 0` copy-back gate (`ioctl.c:3141`), the `-EFAULT` micro-corner, and the two `dev-replace.c` call sites (`701-703`, `1265-1267` with `is_dev_replace = true`, source device). No disagreement on those.

Practical consequence for the row: the "faithful momentary reading" sentence must be dropped or narrowed to "0 means a context is attached; it can also be 0 from attach up to the first read (possibly for a whole transaction commit), after the scan has finished, and for the source device of a device replace".
