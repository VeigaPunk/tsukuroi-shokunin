VERDICT: defect-found
SECTION SHA256: 27aa7abbb20087c531e55de77a3af4259c5ee056f668085c1d5138c70815d6ed

# R51W1PreCritGR2b — uncounted pre-read of GR2 (critic), revision 2732ee6c06108c031c4d8043239b994e0504eb2f

Scope: row `## GR2` of corpus/knowledge/btrfs-scrub-grounding-r45.md (entry lines 56-180 of the revision bytes), the `### Range gaps (R51)` block (lines 269-275), and Limits (240-267). Entry line numbers below are from `git show 2732ee6c…:corpus/knowledge/btrfs-scrub-grounding-r45.md`.

## 0. Preconditions checked

- Section hash: `python3 tools/check-scrub-admission-r51.py --revision 2732ee6c… --section-hash --no-base-check` → GR2 `27aa7abbb20087c531e55de77a3af4259c5ee056f668085c1d5138c70815d6ed`. Matches the stated hash.
- Snapshot digests, `sha256sum -c SHA256SUMS` in each frozen directory, all OK. Row-source mapping:
  - S247 = `.ufo/waves/round-45/frozen/src/dev-replace.c` (sha f07ef0a0…34f3a), fetched from tag v7.2.11 per round-45 FETCH.txt.
  - S242 = `.ufo/waves/round-44/frozen/src/scrub.c` (sha f347931b…38ca5b8), tag v7.2.11 per round-44 FETCH.txt.
  - S243 = `.ufo/waves/round-44/frozen/src/sysfs.c` (sha ce146120…1c43), tag v7.2.11.
  - S240 = `.ufo/waves/round-43/frozen/src/ioctl.c` (sha 7b3488f2…4ba01), tag v7.2.11 per round-43 FETCH.txt.
- `python3 tools/lint-grounding-r51.py --revision 2732ee6c…` → `verdict PASS`, `lint_ok 3`, `quotes 63 / quote_bad 0`, `cites 28 / cite_bad 0`, GR2 `quotes 39`, GR2 `cites 20`, `gaps_computed 62`, `gap_ok 1`, `gap_missing []`, `gap_extra []`. The lint checks quotes whole-line and gap-block consistency with what it parses; it does not check clause truth (see defect 2 for where its cite parser is blind).
- Host capture: `.ufo/waves/round-45/frozen/hostcap/capture.txt:1` CapEff=0 uid=1000; `:9` `devinfo … devids=1`. Both match the entry.

## 1. Defects (exact replacement wording given)

### D1 — the universal "any call … is refused the same way" drops the earlier-check qualifier (entry lines 75-76)

Entry words: "any call, replace or not, is refused the same way while its device already carries a scrub context."

Contradicting pinned lines (`S242 scrub.c`, round-44 snapshot). The `dev->scrub_ctx` test (`scrub.c:3147`) comes after the earlier refusals, so a call that fails one of them gets that errno, not `-EINPROGRESS`:
- `scrub.c:3120-3123`: `if (!dev || (test_bit(BTRFS_DEV_STATE_MISSING, &dev->dev_state) && !is_dev_replace)) { … ret = -ENODEV;` → a non-replace call on a missing device returns `-ENODEV`, even when that device has a context.
- `scrub.c:3127-3133`: `if (!is_dev_replace && !readonly && !test_bit(BTRFS_DEV_STATE_WRITEABLE, …)) … ret = -EROFS;`
- `scrub.c:3138-3142`: `if (unlikely(!test_bit(BTRFS_DEV_STATE_IN_FS_METADATA, …) || test_bit(BTRFS_DEV_STATE_REPLACE_TGT, …))) … ret = -EIO;`

The sentence before the defect already has the qualifier ("gets past the earlier checks"); the "any call" sentence does not.

Exact replacement for entry line 75-76 (the sentence after "no scrub is started;"):
"any call that gets past the earlier checks above, replace or not, is refused the same way while its device already carries a scrub context."

### D2 — the `### Range gaps (R51)` block omits lines GR2 cites (entry lines 66, 79-82, 271-275)

The lint's cite parser (`tools/lint-grounding-r51.py:78`, `CONT_RE`) chains a bare `:NNN` only when it directly follows a `file:NNN` cite and only through `,`, `;` or whitespace. In GR2 the bare cites after prose ("…filesystem (:3075-3078), the error…", "returned at :3250-3253") are not chained, so they never reach the gap computation. I confirmed with `prose_cites` over entry lines 56-180: lines 66, 79, 80, 81, 82 yield no cite for their bare `:NNN` cites. `lint --emit-gaps` therefore prints a block that omits them. The lint's `gap_ok 1` is not evidence that the block covers every line GR2 cites.

Uncovered cited lines, against the declared ranges at the revision (`corpus/SOURCES.md:249` S240 `ioctl.c lines 3066-3075, 3118-3140, 5578-5584`; `corpus/SOURCES.md:251` S242 `scrub.c lines 1365-1385, 3140-3162, 3215-3226, 3321-3337`):
- S242 `scrub.c:3250-3253` — entry line 66: "the error `scrub_workers_get` returned, if any (:3114-3116, returned at :3250-3253)". Pinned: `scrub.c:3248-3253` is the `out:`/`out_free_ctx:` tail that `goto out_free_ctx` (`scrub.c:3116`) lands on, then `return ret;`. Not declared, not in the block.
- S240 `ioctl.c:3076-3078` — entry line 79: "(:3075-3078)" (`ioctl.c:3075` is `if (btrfs_fs_incompat(fs_info, EXTENT_TREE_V2)) {`; 3076-3078 are the `btrfs_err`/`return -EINVAL` body). Not declared.
- S240 `ioctl.c:3081-3082` — entry line 80: "(:3080-3082)" (`if (IS_ERR(sa)) return PTR_ERR(sa);`). Only 3080 is in the block.
- S240 `ioctl.c:3087, 3089-3090` — entry line 81: "(:3087-3090)" (`if (!(sa->flags & BTRFS_SCRUB_READONLY)) { ret = mnt_want_write_file(file); if (ret) return ret;`). 3088 is in the block by quote; 3087, 3089, 3090 are not.
- S240 `ioctl.c:3094-3095` — entry line 82: "(:3093-3095)" (3093 `ret = btrfs_scrub_dev(fs_info, sa->devid, sa->start, sa->end,`; 3094 `&sa->progress, sa->flags & BTRFS_SCRUB_READONLY,`; 3095 `false);`). Only 3093 is in the block.

Exact replacement for the block at entry lines 271-273 (the other three lines stay as they are):
- S240 ioctl.c: 3076-3078, 3080-3082, 3084-3085, 3087-3090, 3093-3095, 3109-3110, 3115, 3190
- S242 scrub.c: 3081, 3094-3139, 3250-3253

Check: 3132-3133 (entry line 173, host reading) is inside the declared 3118-3140 and needs no gap line. 3159 and 3222 (entry lines 87-88) are inside the declared 3140-3162 and 3215-3226. 3336 and 3321-3336 are inside 3321-3337. 3072-3073 and 3075 are inside 3066-3075. These four are unchanged.

The lint fix itself (for the L1's counter, not for the entry): let `CONT_RE` chain `:N` after any `,`/`;`/`(`/`at ` continuation on the same line that follows a file cite. Otherwise the regenerated block will again omit these lines.

### D3 — two sysfs names are asserted without a cited line that names them (entry lines 174-177)

- Entry line 174: "the filesystem's `exclusive_operation` names `device replace`". The cite on that clause is `sysfs.c:1288`, which carries only the string `"device replace\n"` (`sysfs.c:1288`, inside the switch of `btrfs_exclusive_operation_show`, `sysfs.c:1265-1301`). The attribute name `exclusive_operation` is registered at `.ufo/waves/round-44/frozen/src/sysfs.c:1302`: `BTRFS_ATTR(, exclusive_operation, btrfs_exclusive_operation_show);`. Not in the block, not cited.
- Entry line 177: "`devinfo/<devid>/replace_target` reads 1 on the replace's target device (sysfs.c:2015)". `sysfs.c:2015` is the body `val = !!test_bit(BTRFS_DEV_STATE_REPLACE_TGT, …)`. The attribute name is registered at `sysfs.c:2019`: `BTRFS_ATTR(devid, replace_target, btrfs_devinfo_replace_target_show);`. Not in the block, not cited.

Exact replacement for entry line 174, first clause: "the filesystem's `exclusive_operation` (sysfs.c:1302) names `device replace`"
Exact replacement for entry line 177, first clause: "`devinfo/<devid>/replace_target` (sysfs.c:2019) reads 1 on the replace's target device (sysfs.c:2015)"
Gap block line 274 becomes: "- S243 sysfs.c: 1288, 1302, 2015, 2019".

## 2. Clauses checked and found supported (pinned bytes)

Statement (entry 58-62):
- "each call btrfs_scrub_dev with the source device's devid, readonly false and is_dev_replace true": `dev-replace.c:701-703` (`src_device->devid, 0, …, &dev_replace->scrub_progress, false, true`) and `dev-replace.c:1265-1268` (`dev_replace->srcdev->devid, …, false, true`). Those are the only two `btrfs_scrub_dev` callers in `dev-replace.c` (grep, lines 701 and 1265; line 948 is a log string). "each" is therefore true over this file.
- The start path is `btrfs_dev_replace_start` (`dev-replace.c:587`), which contains line 701. The continue path is `btrfs_dev_replace_kthread` (`dev-replace.c:1249`), spawned only by `btrfs_resume_dev_replace_async` (`dev-replace.c:1198`, `kthread_run` at `:1245`). "the path that continues a replace interrupted by an unmount" holds. `dev-replace.c:1197` is the comment that names it.
- "the last two parameters … (scrub.c:3081)": `scrub.c:3081` = `bool readonly, bool is_dev_replace)`. Supported.
- The `-EAGAIN` clause: `scrub.c:3094-3095` (`if (btrfs_fs_closing(fs_info)) return -EAGAIN;`). Supported.
- `scrub_setup_ctx` error (`scrub.c:3109-3111`): supported.
- `scrub_workers_get` error (`scrub.c:3114-3116`): the `goto out_free_ctx` lands at `scrub.c:3250-3253` (`out_free_ctx: scrub_free_ctx(sctx); return ret;`). Supported as to the return. The range is missing from the block (D2).
- `-ENODEV` (`scrub.c:3120-3123`): the condition is `!dev || (MISSING && !is_dev_replace)`. Supported.
- `-EROFS` (`scrub.c:3127-3133`): supported.
- `-EIO` (`scrub.c:3138-3142`): `IN_FS_METADATA` absent or `REPLACE_TGT` set. Supported.
- `-EINPROGRESS` (`scrub.c:3147-3153`): `dev->scrub_ctx || (!is_dev_replace && btrfs_dev_replace_is_ongoing(…))`. Supported.
- `btrfs_dev_replace_is_ongoing` (`dev-replace.c:1278-1279`, `1286-1287`, comment `1288-1297`): `is_valid` gate, STARTED/SUSPENDED → true. The comment at `1288-1297` says it stays true for a suspended-by-unmount replace and "does not stop the dev_replace procedure". Supported. The enum switch covers all five states, so no unlisted-state case.
- "a scrub start that is not a replace and gets past the earlier checks … is refused with `-EINPROGRESS` and no scrub is started": `scrub.c:3147-3154` `goto out` before `sctx->readonly`/`dev->scrub_ctx =` at `3158-3159`. Supported. (The qualifier is present in this sentence; the defect is only in the next one, D1.)
- The ioctl clause (entry 78-83): `ioctl.c:3072-3073` (`if (!capable(CAP_SYS_ADMIN)) return -EPERM;`), `:3075-3078` (`EXTENT_TREE_V2` → `-EINVAL`), `:3080-3082` (`memdup_user` → `PTR_ERR`), `:3084-3085` (`flags & ~BTRFS_SCRUB_SUPPORTED_FLAGS` → `-EOPNOTSUPP`), `:3087-3090` (`mnt_want_write_file` when not READONLY), `:3093-3095` (`ret = btrfs_scrub_dev(…)`), `:3109-3110` (`copy_to_user` → `-EFAULT`), `:3115` (`return ret;`). All supported. "copies the argument structure back" is `:3109`.
- The progress clause (entry 85-89): `scrub.c:3321-3336` (`return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;`), `scrub.c:3159` (`dev->scrub_ctx = sctx;`), `scrub.c:3222` (`dev->scrub_ctx = NULL;`). The grep of `scrub.c` shows exactly these two writes in `btrfs_scrub_dev`, and no error path between `:3159` and `:3222` skips `:3222`. "clears it when that call's scrub run ends" is supported. The progress function reads no replace state.
- Line 90 `[inference: …]` is marked and is not pinned by the bytes. Fine.
- Quotes: all 39 GR2 quotes are whole-line matches (lint); spot-checked against the bytes: `dev-replace.c:700, 701, 703, 1197, 1265, 1268, 1287`; `scrub.c:3081, 3094, 3095, 3109, 3114, 3120, 3123, 3127, 3133, 3138, 3139, 3142, 3147, 3148, 3149, 3153, 3159, 3222, 3336`; `ioctl.c:3072, 3075, 3080, 3084, 3085, 3088, 3093, 3109, 3110, 3115`; `sysfs.c:1288, 2015`; `dev-replace.c:1235`. All match.
- Host reading (entry 171-177): `capture.txt:9` `devids=1` and `:1` `CapEff=0000000000000000` match. `ioctl.c:3132` (`if (!capable(CAP_SYS_ADMIN))` in `btrfs_ioctl_scrub_progress`) and `:3133` (`return -EPERM;`) match. `dev-replace.c:1235` (`btrfs_exclop_start(…DEV_REPLACE)` in the resume path) and `ioctl.c:3190` (`btrfs_exclop_start` around the replace ioctl start) match. `sysfs.c:1288` and `2015` match.
- Host readability claim (entry 178-179): `.ufo/waves/round-45/a2w1/C2ExecHostRecheck.md` exists (14303 B, Oct 27 00:28). Its §3 (lines 84-89) shows `replace_target` and `exclusive_operation` as `-r--r--r--` and reads `0` and `none`. The entry's "both files are mode 444 and read `none` and `0`" matches that. `capture.txt` does not record either attribute, and the entry says so.
- Limits (entry 242-243): the `[inference]` on `fs/`/`lib/` is marked.
- Limits (entry 248-256, 257-267): not checked. These are process history (round-45/46/47/50 integration), not pinned bytes. I did not read the cited round artifacts.

## 3. Not checked

- `btrfs scrub start`/`status` printing (marked [inference] in the entry).
- The `exclusive_operation` attribute's mode in C2ExecHostRecheck beyond §3 lines 84-89.
- Process-history claims in Limits (round-45/46/47/50 seat files).
- The `dev-replace.c:1143-1144` narrowing cited in Limits (not a GR2 clause).

## 4. Receipts

- Entry extraction and the section hash: `/fast/scratch/hyaku/tsukuroi-r51/R51W1PreCritGR2b/entry.md` (scratch, removed at finish; copy in `.ufo/waves/round-51/w1/R51W1PreCritGR2b/entry.md` if the L1 wants it).
- Lint output JSON (verbatim, one line) is in `.ufo/waves/round-51/w1/R51W1PreCritGR2b/lint-r51.json`.
- The registry used for declared ranges: `git show 2732ee6c…:corpus/SOURCES.md`, rows S240 (line 249), S242 (line 251), S243 (line 252), S247 (line 256).
