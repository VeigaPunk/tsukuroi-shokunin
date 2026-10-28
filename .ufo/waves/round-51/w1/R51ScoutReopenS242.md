VERDICT: supports

## Gate

- Access (UTC): 2026-10-28T21:13:21Z. `date -u` printed `2026-10-28T21:13:18Z` immediately before `curl` and `2026-10-28T21:13:21Z` immediately after. `CURL_RC:0`. One fetch; no retry.
- URL: `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/scrub.c?h=v7.2.11`
- sha256: `f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8`
- Size: 100417 bytes, 3337 lines. Receipt: `.ufo/waves/round-51/w1/R51ScoutReopenS242/live.bin` (same sha256).
- Located quote the GR2 row rests on, verbatim from the live bytes, line 3336 (10 whitespace-separated words): `return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;` with one leading U+0009. Python repr of the live line: `'\treturn dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;'`. The frozen entry quotes that text at `corpus/knowledge/btrfs-scrub-grounding-r45.md` line 142 (`**Quote.** `S242` scrub.c:3336`) and the GR2 statement cites `scrub.c:3321-3336` (same file, lines 85-87) at revision `2732ee6c06108c031c4d8043239b994e0504eb2f`.

## Identity

Byte-identical to the pin and to the round-44 snapshot.

| bytes | sha256 | size |
|---|---|---|
| live fetch | `f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8` | 100417 |
| `.ufo/waves/round-44/frozen/src/scrub.c` | `f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8` | 100417 |
| `SHA256SUMS` in that directory, first line | `f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8  scrub.c` | |

`cmp -s` of live.bin and the snapshot returned `CMP_RC:0`. Both files split to 3337 lines. Per-line compare of the 83 located lines: `NEQ 0`. No `diff` (the files match). No tool was installed.

Command: `curl -sSfL --max-time 120 'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/scrub.c?h=v7.2.11' -o /fast/scratch/hyaku/tsukuroi-r51/R51ScoutReopenS242/live.bin`

## S242 anchor

`git show 2732ee6c06108c031c4d8043239b994e0504eb2f:corpus/SOURCES.md` line 251, anchor cell (header line 5, column `anchor`):

`tag v7.2.11 (peeled commit a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea), fs/btrfs/scrub.c lines 1365-1385, 3140-3162, 3215-3226, 3321-3337; raw bytes sha256 f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8`

Declared ranges: 1365-1385, 3140-3162, 3215-3226, 3321-3337. The cell's sha256 is the live sha256.

## Located lines (live == snapshot on every one)

`→` below is U+0009. `EQ=1` means the live line equals the same line of `.ufo/waves/round-44/frozen/src/scrub.c`. `IN_ANCHOR=1` means the line number sits in a declared range above. Full receipt: `.ufo/waves/round-51/w1/R51ScoutReopenS242/located.txt`.

Line 3081 is the last line of the signature that begins at live line 3079: `int btrfs_scrub_dev(struct btrfs_fs_info *fs_info, u64 devid, u64 start,`.

```
3081	EQ=1	IN_ANCHOR=0	→→    bool readonly, bool is_dev_replace)
3094	EQ=1	IN_ANCHOR=0	→if (btrfs_fs_closing(fs_info))
3095	EQ=1	IN_ANCHOR=0	→→return -EAGAIN;
3096	EQ=1	IN_ANCHOR=0	
3097	EQ=1	IN_ANCHOR=0	→/* At mount time we have ensured nodesize is in the range of [4K, 64K]. */
3098	EQ=1	IN_ANCHOR=0	→ASSERT(fs_info->nodesize <= BTRFS_STRIPE_LEN);
3099	EQ=1	IN_ANCHOR=0	
3100	EQ=1	IN_ANCHOR=0	→/*
3101	EQ=1	IN_ANCHOR=0	→ * SCRUB_MAX_SECTORS_PER_BLOCK is calculated using the largest possible
3102	EQ=1	IN_ANCHOR=0	→ * value (max nodesize / min sectorsize), thus nodesize should always
3103	EQ=1	IN_ANCHOR=0	→ * be fine.
3104	EQ=1	IN_ANCHOR=0	→ */
3105	EQ=1	IN_ANCHOR=0	→ASSERT(fs_info->nodesize <=
3106	EQ=1	IN_ANCHOR=0	→       SCRUB_MAX_SECTORS_PER_BLOCK << fs_info->sectorsize_bits);
3107	EQ=1	IN_ANCHOR=0	
3108	EQ=1	IN_ANCHOR=0	→/* Allocate outside of device_list_mutex */
3109	EQ=1	IN_ANCHOR=0	→sctx = scrub_setup_ctx(fs_info, is_dev_replace);
3110	EQ=1	IN_ANCHOR=0	→if (IS_ERR(sctx))
3111	EQ=1	IN_ANCHOR=0	→→return PTR_ERR(sctx);
3112	EQ=1	IN_ANCHOR=0	→sctx->stat.last_physical = start;
3113	EQ=1	IN_ANCHOR=0	
3114	EQ=1	IN_ANCHOR=0	→ret = scrub_workers_get(fs_info);
3115	EQ=1	IN_ANCHOR=0	→if (ret)
3116	EQ=1	IN_ANCHOR=0	→→goto out_free_ctx;
3117	EQ=1	IN_ANCHOR=0	
3118	EQ=1	IN_ANCHOR=0	→mutex_lock(&fs_info->fs_devices->device_list_mutex);
3119	EQ=1	IN_ANCHOR=0	→dev = btrfs_find_device(fs_info->fs_devices, &args);
3120	EQ=1	IN_ANCHOR=0	→if (!dev || (test_bit(BTRFS_DEV_STATE_MISSING, &dev->dev_state) &&
3121	EQ=1	IN_ANCHOR=0	→→     !is_dev_replace)) {
3122	EQ=1	IN_ANCHOR=0	→→mutex_unlock(&fs_info->fs_devices->device_list_mutex);
3123	EQ=1	IN_ANCHOR=0	→→ret = -ENODEV;
3124	EQ=1	IN_ANCHOR=0	→→goto out;
3125	EQ=1	IN_ANCHOR=0	→}
3126	EQ=1	IN_ANCHOR=0	
3127	EQ=1	IN_ANCHOR=0	→if (!is_dev_replace && !readonly &&
3128	EQ=1	IN_ANCHOR=0	→    !test_bit(BTRFS_DEV_STATE_WRITEABLE, &dev->dev_state)) {
3129	EQ=1	IN_ANCHOR=0	→→mutex_unlock(&fs_info->fs_devices->device_list_mutex);
3130	EQ=1	IN_ANCHOR=0	→→btrfs_err(fs_info,
3131	EQ=1	IN_ANCHOR=0	→→→"scrub: devid %llu: filesystem on %s is not writable",
3132	EQ=1	IN_ANCHOR=0	→→→→ devid, btrfs_dev_name(dev));
3133	EQ=1	IN_ANCHOR=0	→→ret = -EROFS;
3134	EQ=1	IN_ANCHOR=0	→→goto out;
3135	EQ=1	IN_ANCHOR=0	→}
3136	EQ=1	IN_ANCHOR=0	
3137	EQ=1	IN_ANCHOR=0	→mutex_lock(&fs_info->scrub_lock);
3138	EQ=1	IN_ANCHOR=0	→if (unlikely(!test_bit(BTRFS_DEV_STATE_IN_FS_METADATA, &dev->dev_state) ||
3139	EQ=1	IN_ANCHOR=0	→→     test_bit(BTRFS_DEV_STATE_REPLACE_TGT, &dev->dev_state))) {
3140	EQ=1	IN_ANCHOR=1	→→mutex_unlock(&fs_info->scrub_lock);
3141	EQ=1	IN_ANCHOR=1	→→mutex_unlock(&fs_info->fs_devices->device_list_mutex);
3142	EQ=1	IN_ANCHOR=1	→→ret = -EIO;
3143	EQ=1	IN_ANCHOR=1	→→goto out;
3144	EQ=1	IN_ANCHOR=1	→}
3145	EQ=1	IN_ANCHOR=1	
3146	EQ=1	IN_ANCHOR=1	→down_read(&fs_info->dev_replace.rwsem);
3147	EQ=1	IN_ANCHOR=1	→if (dev->scrub_ctx ||
3148	EQ=1	IN_ANCHOR=1	→    (!is_dev_replace &&
3149	EQ=1	IN_ANCHOR=1	→     btrfs_dev_replace_is_ongoing(&fs_info->dev_replace))) {
3150	EQ=1	IN_ANCHOR=1	→→up_read(&fs_info->dev_replace.rwsem);
3151	EQ=1	IN_ANCHOR=1	→→mutex_unlock(&fs_info->scrub_lock);
3152	EQ=1	IN_ANCHOR=1	→→mutex_unlock(&fs_info->fs_devices->device_list_mutex);
3153	EQ=1	IN_ANCHOR=1	→→ret = -EINPROGRESS;
3159	EQ=1	IN_ANCHOR=1	→dev->scrub_ctx = sctx;
3222	EQ=1	IN_ANCHOR=1	→dev->scrub_ctx = NULL;
3250	EQ=1	IN_ANCHOR=0	out_free_ctx:
3251	EQ=1	IN_ANCHOR=0	→scrub_free_ctx(sctx);
3252	EQ=1	IN_ANCHOR=0	
3253	EQ=1	IN_ANCHOR=0	→return ret;
3321	EQ=1	IN_ANCHOR=1	int btrfs_scrub_progress(struct btrfs_fs_info *fs_info, u64 devid,
3322	EQ=1	IN_ANCHOR=1	→→→ struct btrfs_scrub_progress *progress)
3323	EQ=1	IN_ANCHOR=1	{
3324	EQ=1	IN_ANCHOR=1	→struct btrfs_dev_lookup_args args = { .devid = devid };
3325	EQ=1	IN_ANCHOR=1	→struct btrfs_device *dev;
3326	EQ=1	IN_ANCHOR=1	→struct scrub_ctx *sctx = NULL;
3327	EQ=1	IN_ANCHOR=1	
3328	EQ=1	IN_ANCHOR=1	→mutex_lock(&fs_info->fs_devices->device_list_mutex);
3329	EQ=1	IN_ANCHOR=1	→dev = btrfs_find_device(fs_info->fs_devices, &args);
3330	EQ=1	IN_ANCHOR=1	→if (dev)
3331	EQ=1	IN_ANCHOR=1	→→sctx = dev->scrub_ctx;
3332	EQ=1	IN_ANCHOR=1	→if (sctx)
3333	EQ=1	IN_ANCHOR=1	→→memcpy(progress, &sctx->stat, sizeof(*progress));
3334	EQ=1	IN_ANCHOR=1	→mutex_unlock(&fs_info->fs_devices->device_list_mutex);
3335	EQ=1	IN_ANCHOR=1	
3336	EQ=1	IN_ANCHOR=1	→return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;
```

Outside the declared ranges, among those 83 lines: **3081, 3094-3139, 3250-3253**. Inside: 3140-3153 (range 3140-3162), 3159 (range 3140-3162), 3222 (range 3215-3226), 3321-3336 (range 3321-3337).

## Range gaps check

`python3 tools/lint-grounding-r51.py --revision 2732ee6c06108c031c4d8043239b994e0504eb2f --emit-gaps` exited 0. S242 line of that output, and of the entry's `### Range gaps (R51)` block (`corpus/knowledge/btrfs-scrub-grounding-r45.md` line 273 at the same revision):

`- S242 scrub.c: 3081, 3094-3139`

Receipt: `.ufo/waves/round-51/w1/R51ScoutReopenS242/emit-gaps.txt`.

That line matches 3081 and 3094-3139. It does not name 3250-3253. Those four lines are outside every declared range, and the GR2 statement names them: grounding line 66, `returned at :3250-3253`, on the line after `scrub.c:3094-3153` (line 65). The lint adds a colon-led span only after a `file:line` match on the same line (`tools/lint-grounding-r51.py` `CITE_RE` line 77, `CONT_RE` line 78, `prose_cites` lines 167-186, row scan lines 217-247). Line 66 has no basename, and no `**Quote.**` line cites 3250-3253 (quotes go from scrub.c:3222 at entry line 140 to scrub.c:3336 at entry line 142). The emitted gap set is the scanner's cited-outside-range set (`analyze` lines 249-259), so 3250-3253 stays out of the block.

## Not done

No second fetch, no `diff`, no package install, no write outside this report and `.ufo/waves/round-51/w1/R51ScoutReopenS242/`. Scratch `/fast/scratch/hyaku/tsukuroi-r51/R51ScoutReopenS242/` removed after the receipts were copied.
