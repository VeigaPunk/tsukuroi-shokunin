VERDICT: supports

# S242 and S243 re-opened at Linux v7.2.11

Axes checked: byte identity against the round-44 pin, and whether each listed window still supports the GR2 clause that uses it. GR3's `scrub.c` cites are S237 (btrfs-progs), not these files.

Fetched 2026-10-28 (HTTP `date: Wed, 28 Oct 2026 19:04:40 GMT` on scrub.c, `19:04:41 GMT` on sysfs.c). URLs are the plain-file URLs in `.ufo/waves/round-44/frozen/src/FETCH.txt:2` and `:3`. Row text is `8029cdba1049df25632c91a23c8db4eefb54be5f:corpus/knowledge/btrfs-scrub-grounding-r45.md` (blob `f2a849169bebc05de11f514d08de26e8941a6a3e`, 307 lines). No tool was installed.

## Identity

| file | URL | HTTP | redirects | bytes | lines | sha256 | pin | cmp |
|---|---|---|---|---|---|---|---|---|
| S242 `fs/btrfs/scrub.c` | `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/scrub.c?h=v7.2.11` | 200 | 0 | 100417 | 3337 | `f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8` | `SHA256SUMS:1` | 0 |
| S243 `fs/btrfs/sysfs.c` | same host, `plain/fs/btrfs/sysfs.c?h=v7.2.11` | 200 | 0 | 72925 | 2702 | `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43` | `SHA256SUMS:2` | 0 |

`content-type: text/plain; charset=UTF-8`. No CR. `last-modified` equals the response `date` on both, so it is the cgit clock, not an upstream mtime. Etag `W/"9db8f8b6d3d544565bbd35a16e8a3b612f06d38c"` (scrub.c) and `W/"0d14570c8bc2900bb41685a13cfbf2c4783789e8"` (sysfs.c). Identity is the sha256 and `cmp -s` against `.ufo/waves/round-44/frozen/src/scrub.c` and `sysfs.c` (both exit 0). **Byte-identical. Not drifted.**

All 18 GR2 `**Quote.**` lines that name S242 or S243 are substrings of the live line at the cited number (`quotes ok=18 fail=0`).

## GR2 — each listed window

Row statement: `btrfs-scrub-grounding-r45.md:58-85`. Host reading: `:143-149`. Every window below is supported.

| window | clause | live bytes |
|---|---|---|
| scrub.c:3081 | Last two parameters of `btrfs_scrub_dev` are `readonly` and `is_dev_replace` (`:61`, quote `:99`). | `bool readonly, bool is_dev_replace)` at the end of the signature (`:3079-3081`). The `false, true` call arguments are S247, not this file. |
| scrub.c:3094-3095 | First return is `-EAGAIN` when `btrfs_fs_closing` (`:61-62`, quotes `:100-101`). | `:3094-3095` are that check and `return -EAGAIN;`. Earlier `:3091-3092` only stores `progress->last_physical`. |
| scrub.c:3109-3111 | `scrub_setup_ctx` runs next; its error returns before the device checks (`:62-64`, quote `:135`). | `:3109` assigns `scrub_setup_ctx(fs_info, is_dev_replace)`; `:3110-3111` `return PTR_ERR(sctx)` on `IS_ERR`. |
| scrub.c:3114-3116 | `scrub_workers_get` likewise; its error returns first (`:62-64`, quote `:137`). | `:3114` calls it; `:3115-3116` `goto out_free_ctx` when `ret` is set. `:3250-3253` frees the context and returns that `ret`. |
| scrub.c:3120-3123 | Unknown devid, or a missing device on a non-replace call, returns `-ENODEV` (`:64-65`, quote `:111`). | `:3120-3121` `!dev` or (`MISSING` and `!is_dev_replace`); `:3123` `ret = -ENODEV`; `:3124` `goto out`. |
| scrub.c:3127-3133 | Non-writeable device on a non-replace, non-readonly call returns `-EROFS` (`:65-66`, quote `:113`). | `:3127-3128` `!is_dev_replace && !readonly && !WRITEABLE`; `:3133` `ret = -EROFS`; `:3134` `goto out`. |
| scrub.c:3138-3142 | Device outside filesystem metadata, or the replace target, returns `-EIO` (`:66-67`, quotes `:115`, `:117`, `:139`). | `:3138-3139` `!IN_FS_METADATA` or `REPLACE_TGT`; `:3142` `ret = -EIO`; `:3143` `goto out`. |
| scrub.c:3146-3155 | Only after those checks: `is_dev_replace` false is `-EINPROGRESS` while a replace is ongoing, and any call is `-EINPROGRESS` while `dev->scrub_ctx` is set (`:67-74`, quotes `:103-109`). | `:3147-3149` is `dev->scrub_ctx \|\| (!is_dev_replace && btrfs_dev_replace_is_ongoing(...))`; `:3153-3154` sets `-EINPROGRESS` and `goto out`. The four refusal gotos (`:3124`, `:3134`, `:3143`, `:3154`) are all before the context is attached. |
| scrub.c:3158-3159 | The copy's source device carries the context this call attached (`:75-76`). | `:3159` `dev->scrub_ctx = sctx;` after the refusal checks. `scrub_enumerate_chunks` is later, at `:3208`. |
| scrub.c:3167 | Not a numbered cite. It is the `scrubs_running` increment on the path that got past `:3159`. A refused call does not reach it, which is the "no scrub is started" half of `:72-75`. | `:3167` `atomic_inc(&fs_info->scrubs_running);`. |
| scrub.c:3222 | When the copy finishes, the context is cleared, so a later progress query sees it absent (`:79-80`, quote `:141`). | `:3222` `dev->scrub_ctx = NULL;` under `scrub_lock`, after `scrub_enumerate_chunks` (`:3208`) and before `return ret` (`:3247`). |
| scrub.c:3277-3283 | `btrfs_dev_replace_cancel` calls `btrfs_scrub_cancel` (`:76-78`). This window is the idle arm: nothing running yields `-ENOTCONN`. | `:3277` `btrfs_scrub_cancel`; `:3280-3282` if `scrubs_running` is 0, `return -ENOTCONN`. The running arm is the next lines: `:3285` `atomic_inc(&fs_info->scrub_cancel_req)`, `:3286-3291` waits until `scrubs_running` is 0, `:3295` `return 0`. Call sites stay S247. |
| scrub.c:3321-3336 | Progress returns 0 only when the devid exists and `scrub_ctx` is set, `-ENOTCONN` when the devid exists and the context is absent, `-ENODEV` for an unknown devid (`:79-80`, quote `:133`). | `:3321` `btrfs_scrub_progress`; `:3329-3331` looks up the device and reads `dev->scrub_ctx`; `:3332-3333` copies `sctx->stat` only when `sctx` is set; `:3336` `return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;`. |
| sysfs.c:76-78 | The two GR2 attributes are registered with `BTRFS_ATTR`, so mode 0444 and no store (`:146-149`). | `:76-78` `#define BTRFS_ATTR` → `__INIT_KOBJ_ATTR(_name, 0444, _show, NULL)`. `scrub_speed_max`'s `BTRFS_ATTR_RW` 0644 macro is `:72-74` (GR1), not this window. |
| sysfs.c:1288 | `exclusive_operation` names `device replace` for `BTRFS_EXCLOP_DEV_REPLACE` (`:146-148`, quote `:123`). | `:1288` `str = "device replace\n";` in that case. `:1300` emits it with `sysfs_emit`. Who sets the enum is S247 `:1235` / S240, not this line. |
| sysfs.c:1302 | That string is the `exclusive_operation` attribute. | `:1302` `BTRFS_ATTR(, exclusive_operation, btrfs_exclusive_operation_show);`. |
| sysfs.c:2015 | `replace_target` reads 1 on the replace target (`:149`, quote `:125`). | `:2015` `val = !!test_bit(BTRFS_DEV_STATE_REPLACE_TGT, ...)`; `:2017` `sysfs_emit(buf, "%d\n", val)`. |
| sysfs.c:2019 | The show is published as `replace_target`. | `:2019` `BTRFS_ATTR(devid, replace_target, btrfs_devinfo_replace_target_show);`. |
| sysfs.c:2112 | The attribute sits on `devinfo/<devid>/`. | `:2112` `BTRFS_ATTR_PTR(devid, replace_target),` inside `devid_attrs` (`:2107`). The comment at `:2105` is `Path: /sys/fs/btrfs/<uuid>/devinfo/<devid>/`. `:2113` is `scrub_speed_max`, a different attribute. |

## GR3

GR3 (`:153-192`) cites no S243 line. Its `scrub.c` cites are S237: prose `:165` says btrfs-progs `scrub.c:1512` and `:1546`, and the quotes at `:188`, `:190`, `:192` are tagged `` `S237` `` (`:421`, `:1546`, `:439`). Those are not lines of S242. This seat did not re-fetch S237 (the item names the two kernel URLs only). No GR3 clause is carried by the bytes re-opened here, and none is withdrawn by them.

## Clauses the live bytes no longer support

None. The files are the pinned bytes, and each listed GR2 window still matches the clause above.

## Not done

Did not re-fetch S237, S247, or S240. Did not run `tools/check-scrub-admission-r50.py`. Did not edit `SOURCES.md`.

Receipts: `.ufo/waves/round-50/w1/R50ScoutReopenS242/` (`scrub.c.live`, `sysfs.c.live`, `scrub.headers`, `sysfs.headers`, `scrub.curlstats`, `sysfs.curlstats`, `identity.txt`, `cited-lines.txt`). Scratch `/fast/scratch/hyaku/tsukuroi-r50/R50ScoutReopenS242` removed after the copy.
