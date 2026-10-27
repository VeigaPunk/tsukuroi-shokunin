# C2ExecFinalQuotes — receipts (round 44 / w2, item C2-1)

Tested revision: `8eee79db608b5815c325a5af7cbfdeac50eda9f4` (integrated tip).
Entry under test: `corpus/knowledge/btrfs-scrub-record-r44.md`, blob
`8fb2ac7671c2b811938ba41aea2054a7cd68f1af`, sha256
`a4b975a04453405df4ed03c4a1c5fd9917f422b9bc3f146b09fa14a994308676`, 149 lines.
The same blob is present at `071ab0d1` (w1 integration) — `git diff --stat 071ab0d1
8eee79db… -- corpus/knowledge/btrfs-scrub-record-r44.md` is empty, so the quote set did not
change after w1 and this re-check covers the text w2 inherits.

## Commands

```sh
cd /fast/scratch/hyaku/tsukuroi-r44/C2ExecFinalQuotes
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show \
    8eee79db608b5815c325a5af7cbfdeac50eda9f4:<path> > snap/<wave>/<base>
# dev-replace.c corroboration (NOT a frozen snapshot, two channels, identical)
curl -sfL 'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/dev-replace.c?h=v7.2.11' -o dev-replace.c
curl -sfL 'https://raw.githubusercontent.com/gregkh/linux/v7.2.11/fs/btrfs/dev-replace.c' -o dev-replace-gh.c
cmp dev-replace.c dev-replace-gh.c           # identical
TMPDIR=$PWD python3 check_quotes.py 8eee79db608b5815c325a5af7cbfdeac50eda9f4 --extras
```

## Digest-verified snapshots (extracted from the tested rev, checked against frozen manifests)

| source id | path at rev | manifest | sha256 |
|---|---|---|---|
| S237 | `.ufo/waves/round-42/frozen/src/scrub.c` | r42 `SHA256SUMS` | `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801` OK |
| S240 | `.ufo/waves/round-43/frozen/src/ioctl.c` | r43 `SHA256SUMS` | `7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01` OK |
| S242 | `.ufo/waves/round-44/frozen/src/scrub.c` | r44 `SHA256SUMS` | `f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8` OK |
| S243 | `.ufo/waves/round-44/frozen/src/sysfs.c` | r44 `SHA256SUMS` | `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43` OK |
| S244 | `.ufo/waves/round-44/frozen/src/btrfs-scrub@.timer` | r44 `SHA256SUMS` | `9a0b6cc23f7bd97b83b6c38dd2b4e4373fead8bd3ccfb82a47c72971e9d6f8ad` OK |
| S244 | `.ufo/waves/round-44/frozen/src/btrfs-scrub@.service` | r44 `SHA256SUMS` | `eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252` OK |
| S244 | `.ufo/waves/round-44/frozen/src/PKGBUILD` | r44 `SHA256SUMS` | `3b803e8b05d84900fcdab3513720c8005345acd1fe34ded6eaa3b7596c10ce98` OK |
| S245 | `.ufo/waves/round-44/frozen/hostcap/capture.txt` | md header claim | `efb523889035cba62235d904b9e254068a7083dd07e7bb338ce2a803a3e84900` OK |

Provenance of the older snapshots re-confirmed from their own fetch logs at the tested rev:
r42 `FETCH.txt` = `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c`
(btrfs-progs v7.1); r43 `FETCH.txt` = `.../gregkh/linux/v7.2.11/fs/btrfs/ioctl.c` (Linux v7.2.11).

## Result (`run-tip.log`, reproduced 2026-10-26)

```
quotes checked: 33 (exact 8, indent-only 24, prefix 1); prose line claims: 12; support checks: 10; bad: 0
```

- 33/33 `**Quote.**` lines resolve to the named line of the digest-verified snapshot; none is
  wrong-line, wrong-file or wrong-text. 24/33 reproduce the line modulo leading indentation
  (the corpus convention in rounds 42/43); 8 reproduce it byte-for-byte.
- 1/33 is a strict prefix of its line: `md:69 S243 sysfs.c:72` quotes
  `#define BTRFS_ATTR_RW(_prefix, _name, _show, _store)` and omits the `#define` body's trailing
  `\` line continuation (`'\t\t\t\\'`). Content-accurate for the macro head; the frozen counter
  accepts it because its rule is substring containment (`q in src[n-1]`).
- 12/12 prose line-number claims resolve; 2 of them (`dev-replace.c` lines 701-703, 1265-1268)
  are outside the pinned set (see below) and are corroborated by a fresh, two-channel fetch.
- 10/10 narrowing-support checks pass (SR7 narrowed text, SR8 in-memory sentence).
- 1 NOTE, not a defect: SR7's signature quote `S242 scrub.c:3081` lies outside the frozen
  counter's SR7 windows `(3140,3165) (3215,3226) (3321,3337)`; the counter only needs one
  in-window quote per row (8 remain), so its predicate is unaffected.

## SR7 narrowed text (w1's new sentence) — support

- `scrub.c:3079-3081` is `int btrfs_scrub_dev(..., bool readonly, bool is_dev_replace)`; the
  quoted continuation line 3081 carries `bool readonly, bool is_dev_replace)`.
- `scrub.c:3148` uses the argument in the refusal branch: `(!is_dev_replace &&`.
- attach `3159` follows the last refusal `goto out` (3154) and precedes all scrub work; the
  clear `3221-3223` (`dev->scrub_ctx = NULL;` under `scrub_lock`) follows
  `scrub_enumerate_chunks` (3208) and the progress copy (3215), and precedes the finalize tail
  (`scrub_workers_put` 3225, `scrub_put_ctx` 3226, `need_commit` block 3232+).
- "every return path leaves the field as it found it": returns inside `btrfs_scrub_dev`
  (3079-3254) are 3095, 3111 and the `goto out`/`out_free_ctx` at 3116/3124/3134/3143/3154 —
  all before 3159 — plus 3240 and 3247 after the clear; there is no `return`/`goto` between
  3159 and 3222, so every path that attaches also clears. Claim holds.
- replace call sites (fresh fetch `f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a`,
  kernel.org plain and raw.githubusercontent identical, 1322 lines):
  701-703 `ret = btrfs_scrub_dev(fs_info, src_device->devid, 0, btrfs_device_get_total_bytes(src_device), &dev_replace->scrub_progress, false, true);`
  and 1265-1268 `ret = btrfs_scrub_dev(fs_info, dev_replace->srcdev->devid, dev_replace->committed_cursor_left, btrfs_device_get_total_bytes(dev_replace->srcdev), &dev_replace->scrub_progress, false, true);`
  — exactly the `is_dev_replace = true` callers the narrowed SR7 sentence cites, including the
  corrected span `1265-1268` (the pre-narrowing draft said `1265-1267`).

## SR8 in-memory sentence (w1's new sentence) — support

- store `btrfs_devinfo_scrub_speed_max_store` (sysfs.c:2031-2047): `limit = memparse(buf, &endptr);`
  2040, `endptr = skip_spaces(endptr);` 2042, `if (*endptr != 0) return -EINVAL;` 2043-2044,
  `WRITE_ONCE(device->scrub_speed_max, limit);` 2045, `return len;` 2046 — no other call on the
  write path, so "written with `WRITE_ONCE` … nothing on this write path persists it" is
  source-backed; persistence/`kzalloc_obj` is flagged `[inference]` in the entry and lies beyond
  these snapshots (`fs/btrfs/volumes.h`, `volumes.c` are not in the frozen set).
- `READ_ONCE` at sysfs.c:2028 (show) and scrub.c:1380 (throttle, `if (bwlimit == 0) return;` 1381-1382).
- `BTRFS_ATTR_RW` (sysfs.c:72-74) expands to `__INIT_KOBJ_ATTR(_name, 0644, _show, _store)`, i.e.
  the mode the entry claims; `BTRFS_ATTR_RW(devid, scrub_speed_max, …)` at 2048-2049.

## Artefacts

- `check_quotes.py` — sha256 `8f5b493b9bf01d87e1d7acfb720f0754ad13951f054232f68146a1bd0791cd00`
- `run-tip.log` — sha256 `2ca95ee4cfd2aaac40b231882ddfeb1c80960e7c2369e2eeece088d7e354b134`
