VERDICT: defect-found

# F-11 — final `## Gate` section of `corpus/lessons/round-44.md` for S242-S245 (seat SrcGateFinal, round 44 w2)

Item: draft the final `## Gate` section for S242-S245 — re-open each URL now (`curl` into scratch), record URL,
access date, ≤25-word located quote, and the `used-by` old→new log for S237/S240
(`git diff 98020ece0674e0b569ee23aed10ffbee355b248e 8eee79db608b5815c325a5af7cbfdeac50eda9f4 -- corpus/SOURCES.md`,
column 11 only). The exact Markdown is §6.

The four rows, the two re-opened rows and the registry log all hold on live bytes. One real defect in the text this
section replaces (F1, a receipt the current draft names that does not exist) and two accuracy defects (F2 stale
revision in the S237/S240 log, F3 attribution nits). Nothing here falsifies C1 or C2.

## 1. Live re-open (this seat, 2026-10-26T22:03:38–22:05:49-0300 = 2026-10-27T01:03:38–01:05:49Z UTC)

Scratch `/fast/scratch/hyaku/tsukuroi-r44/SrcGateFinal/`, `curl -sS -m 90..120`, `TMPDIR` inside it. Every response
HTTP 200; every digest compared against the frozen snapshot it must equal. Receipt: `fetch-log.txt`
(`.ufo/waves/round-44/w2/SrcGateFinal/fetch-log.txt`).

| Row | URL opened now | HTTP | bytes | sha256 | = frozen |
|---|---|---|---|---|---|
| S242 | `git.kernel.org/…/tree/fs/btrfs/scrub.c?h=v7.2.11` (HTML) | 200 | 234951 | `8c880e68…64b10` | n/a (rendered view) |
| S242 | `git.kernel.org/…/plain/fs/btrfs/scrub.c?h=v7.2.11` | 200 | 100417 | `f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8` | yes |
| S242 | `raw.githubusercontent.com/gregkh/linux/v7.2.11/fs/btrfs/scrub.c` | 200 | 100417 | `f347931b…938ca5b8` | yes (mirror) |
| S243 | `git.kernel.org/…/tree/fs/btrfs/sysfs.c?h=v7.2.11` (HTML) | 200 | 181619 | `7ccb7888…70453` | n/a (rendered view) |
| S243 | `git.kernel.org/…/plain/fs/btrfs/sysfs.c?h=v7.2.11` | 200 | 72925 | `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43` | yes |
| S243 | `raw.githubusercontent.com/gregkh/linux/v7.2.11/fs/btrfs/sysfs.c` | 200 | 72925 | `ce146120…4f731c43` | yes (mirror) |
| S244 | `gitlab.archlinux.org/…/btrfs-progs/-/tree/7.1-1` (HTML) | 200 | 45421 | `b5f94a05…badc44` | n/a (rendered view) |
| S244 | `…/-/raw/7.1-1/btrfs-scrub%40.timer` | 200 | 160 | `9a0b6cc23f7bd97b83b6c38dd2b4e4373fead8bd3ccfb82a47c72971e9d6f8ad` | yes |
| S244 | `…/-/raw/7.1-1/btrfs-scrub%40.service` | 200 | 190 | `eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252` | yes |
| S244 | `…/-/raw/7.1-1/PKGBUILD` | 200 | 3057 | `3b803e8b05d84900fcdab3513720c8005345acd1fe34ded6eaa3b7596c10ce98` | yes |
| S244 | `gitlab.archlinux.org/api/v4/…/repository/tags/7.1-1` | 200 | 1360 | `00c25cfa…a72254` | `"name":"7.1-1"`, commit `0c0a4d77b318084ecd35aeeb6888d8a5b4d6e3e0`, committed 2026-07-15T09:15:06+02:00 |
| S245 | no URL (own-work) — re-read `.ufo/waves/round-44/frozen/hostcap/` | — | 649 / 1429 | `efb523889035cba62235d904b9e254068a7083dd07e7bb338ce2a803a3e84900` (capture.txt) / `6a297e4ff9c7030c6cfe10feeb6c9198ccf31a574fbe6ce1b755dbf318376f6d` (capture.sh) | matches the S245 registry cell |
| S237 | `raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c` | 200 | 57034 | `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801` | yes (round-42 snapshot) |
| S237 | `github.com/kdave/btrfs-progs/blob/v7.1/cmds/scrub.c` (HTML) | 200 | 853943 | `68ec2b2d…c03726` | n/a (rendered view) |
| S240 | `git.kernel.org/…/plain/fs/btrfs/ioctl.c?h=v7.2.11` | 200 | 145999 | `7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01` | yes (round-43 snapshot) |
| S240 | `git.kernel.org/…/tree/fs/btrfs/ioctl.c?h=v7.2.11` (HTML) | 200 | 367878 | `594a9a5e…8ac545` | n/a (rendered view) |

Tag pins read live in the same window (receipt `tag-pins.txt`): `git.kernel.org/…/tag/?h=v7.2.11` (HTTP 200) prints
tag object `8316c24ec1b77dba19ba072ca4fe251b36dc65d3` tagged object commit
`a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea`; `git ls-remote https://github.com/kdave/btrfs-progs 'refs/tags/v7.1*'`
prints `0a919c7d6e389c07920675b7fad3f793b92aa78b refs/tags/v7.1` and
`4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b refs/tags/v7.1^{}` (the S237 anchor's peel); the GitLab tag API (above)
gives the same `7.1-1` commit as the S244 anchor. The two kernel mirrors are byte-identical to the `plain
?h=v7.2.11` bytes (equal sha256, not just equal
size). The HTML `tree`/`blob` views are *not* digest-compared — their digests above are of the rendered pages and are
recorded only so a re-run can tell a changed page from a re-rendered one.

## 2. Located quotes — read byte-exact at the line named

Receipt `quotes.txt` (produced by `gatecheck.py`, both under `.ufo/waves/round-44/w2/SrcGateFinal/`); `mismatches 0`.

| Row | line (frozen path) | quote | words |
|---|---|---|---|
| S242 | `.ufo/waves/round-44/frozen/src/scrub.c:3336` | `return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;` | 10 |
| S242 | `…/scrub.c:1380` | `bwlimit = READ_ONCE(device->scrub_speed_max);` | 3 |
| S242 | `…/scrub.c:1381` | `if (bwlimit == 0)` | 4 |
| S243 | `…/sysfs.c:2028` | `return sysfs_emit(buf, "%llu\n", READ_ONCE(device->scrub_speed_max));` | 4 |
| S243 | `…/sysfs.c:74` | `__INIT_KOBJ_ATTR(_name, 0644, _show, _store)` | 4 |
| S243 | `…/sysfs.c:2040` | `limit = memparse(buf, &endptr);` | 4 |
| S243 | `…/sysfs.c:2043` | `if (*endptr != 0)` | 4 |
| S244 | `…/btrfs-scrub@.timer:5` | `OnCalendar=monthly` | 1 |
| S244 | `…/btrfs-scrub@.timer:8` | `Persistent=true` | 1 |
| S244 | `…/btrfs-scrub@.service:10` | `ExecStart=/usr/bin/btrfs scrub start -B %f` | 5 |
| S244 | `…/btrfs-scrub@.service:9` | `KillSignal=SIGINT` | 1 |
| S244 | `…/PKGBUILD:100` | `install -Dm644 btrfs-scrub@.service "${pkgdir}/usr/lib/systemd/system/btrfs-scrub@.service"` | 4 |
| S245 | `…/hostcap/capture.txt:3` | `var_lib_btrfs absent` | 2 |
| S245 | `…/hostcap/capture.txt:4` | `mode=644 owner=root value=0` (literal substring of the line) | 3 |
| S245 | `…/hostcap/capture.txt:5` | `wants_btrfs_scrub_instances 0` | 2 |
| S237 | `.ufo/waves/round-42/frozen/src/scrub.c:421` | `ret = ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL);` | 5 |
| S240 | `.ufo/waves/round-43/frozen/src/ioctl.c:3139` | `ret = btrfs_scrub_progress(fs_info, sa->devid, &sa->progress);` | 5 |

Per-row totals (the ≤25-word bound): S242 17, S243 16, S244 12, S245 7, S237 5, S240 5. Every location sits inside
the row's own anchor range in `corpus/SOURCES.md` (`S242` 1365-1385/3140-3162/3215-3226/3321-3337; `S243`
72-74/2021-2049/2113; `S244` timer 1-11, service 1-10, PKGBUILD 99-101; `S245` capture.txt). Indentation is stripped
in the quotes — the upstream lines are tab-indented; the text after the indentation is byte-equal (the round-42/43
entries do the same).

## 3. `used-by` old→new, base → declared integrated tip, column 11 only

Command (exactly as the item asks, with the frozen base and the declaration's tip):
`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff 98020ece0674e0b569ee23aed10ffbee355b248e 8eee79db608b5815c325a5af7cbfdeac50eda9f4 -- corpus/SOURCES.md`
→ one hunk, `corpus/SOURCES.md | 8 ++++++--` (6 insertions, 2 deletions). Receipt: `registry-diff.txt`.

| Row | cell 11 old | cell 11 new |
|---|---|---|
| S237 (`:246` at both revisions) | `corpus/knowledge/btrfs-scrub-record-r42.md, corpus/knowledge/btrfs-scrub-record-r43.md` | `corpus/knowledge/btrfs-scrub-record-r42.md, corpus/knowledge/btrfs-scrub-record-r43.md, corpus/knowledge/btrfs-scrub-record-r44.md` |
| S240 (`:249` at both revisions) | `corpus/knowledge/btrfs-scrub-record-r43.md` | `corpus/knowledge/btrfs-scrub-record-r43.md, corpus/knowledge/btrfs-scrub-record-r44.md` |

Also from the same parse: rows 241 at the base → 245 at the tip; S242-S245 appended at `:251-254`; **no** row's
cells 1-10 differ between the two revisions (so `status` `mined`, `opened` `2026-10-26` and `recheck` `on-release`
are unchanged, and no other row's `used-by` moved). The added target `corpus/knowledge/btrfs-scrub-record-r44.md`
exists at the tip (`git cat-file -e`), so the new cells are not dangling.

## 4. Census at the tip (the number the section quotes)

`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`
run once at 2026-10-27T01:07Z: `tsukuroi ok`, **exit 0**, 40 `W04`, zero `E` codes, no warning naming S237-S245.
Worktree `corpus/SOURCES.md` is sha256 `4da9c02c…563b845`, identical to `git show 8eee79db:corpus/SOURCES.md` and to
`HEAD:corpus/SOURCES.md`, so the validated bytes are the tip registry. Receipts:
`sources-census-final-8eee79db.txt`, `census-w04-diff.txt` (the 40-line `W04` set is identical to
`before/sources-census-start.txt`, which also prints `tsukuroi ok`/`exit=0`). Row counts come from
`grep -cE '^\| S[0-9]{3} '` on each revision's `corpus/SOURCES.md` (241 base / 245 tip).

## 5. Findings

**F1 — defect (blocking for the section text as it stands): the draft names a census receipt that does not exist.**
`corpus/lessons/round-44.md` (working tree) ends the Gate with
"…241 rows; end exit 0, 245 rows (`.ufo/waves/round-44/before/sources-census-start.txt`, `after/sources-census-final.txt`)".
`sources-census-start.txt` exists; `.ufo/waves/round-44/after/sources-census-final.txt` does not — `after/` holds only
`c1-after-{071ab0d1,9608ebc3,8eee79db,ab8aae1}.jsonl`, and `find /home/vgpnk/Projects/shokunin -name
'sources-census-final*'` returns no file in this lane (the hits are other projects' calibration dirs). The *numbers*
in that sentence reproduce (exit 0, 40 W04, 245 rows, §4), so only the pointer was wrong. §6 replaces it with this
seat's receipt; if the L1 prefers the round's `after/` directory, `cp
.ufo/waves/round-44/w2/SrcGateFinal/sources-census-final-8eee79db.txt .ufo/waves/round-44/after/sources-census-final.txt`
makes the existing pointer true instead.

**F2 — accuracy: the S237/S240 log in the draft cites a pre-integration revision.** The draft says
"`git diff 98020ece 7e081698 -- corpus/SOURCES.md`, column 11 only". The declaration's integrated tip is `8eee79db`,
and the item asks for that diff. The cell content is identical at `7e081698` (verified: `SrcGateReopen`'s
`field-diff.txt` and my base→tip parse agree on both old and new strings), so the claim was right in substance and the
revision was stale. §6 cites `98020ece…8eee79db…` with the full hashes.

**F3 — attribution nit in the draft.** "Live re-fetches by wave-1 seats SrcGateNew/SrcGateReopen/C2ExecLiveSources
were byte-identical" merges two generations: `SrcGateNew` re-opened S242-S244 (and read S245 from the frozen capture),
`C2ExecLiveSources` re-fetched the five frozen files, `SrcGateReopen` re-opened **S237/S240**. §6 dates the final
re-open to this seat and leaves the wave-1 facts where they belong. The w1 attribution itself is not false — all three
seats exist and did what is claimed — it is the subject that is blurred.

**F4 — carried, not this item: `SrcGateNew` F1 is still unapplied at the tip.** The S242 anchor cell reads
`…lines 1365-1385, 3140-3162, 3215-3226, 3321-3337` (`corpus/SOURCES.md:251`), which does **not** cover
`scrub.c:3079-3085`, the `btrfs_scrub_dev(… bool is_dev_replace)` signature the SR7 narrowing rests on. Registry
cells are outside this seat's write scope. Same for that seat's F2 (no PKGBUILD digest in the S244 anchor) and F3
(one digest for a two-file own-work pair). My §6 does not depend on any of them: every quote I place is inside the
anchor as filed.

**Note (not a defect): access dates.** My fetches ran 2026-10-27T01:03:38–01:05:49Z = 2026-10-26T22:03–22:05 local
(UTC−3), so the local access date is 2026-10-26, the same date the registry `opened` cells carry; §6 states the
instant and the local date so neither reading is a guess. The S245 capture timestamp (`2026-10-26T23:53:22Z`) and
the Arch tag date (`2026-07-15`) are unaffected.

## 6. Proposed text — exact Markdown (replaces the whole `## Gate` section through the census line)

```markdown
## Gate

### New SOURCES rows (`corpus/SOURCES.md:251-254` at `8eee79db`; opened 2026-10-26 by this round's L1 and re-opened
live for this final section by wave-2 seat `SrcGateFinal` on 2026-10-26T22:03-22:05-0300 = 2026-10-27T01:03-01:05Z UTC
— every fetch HTTP 200, every byte digest equal to the frozen snapshot, every quote read byte-exact at the line named)

| Row | URL (access 2026-10-26) | Located quote (≤25 words) | Location |
|---|---|---|---|
| S242 | https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/fs/btrfs/scrub.c?h=v7.2.11 — raw `plain/fs/btrfs/scrub.c?h=v7.2.11`, 100417 B, sha256 `f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8`, byte-identical to https://raw.githubusercontent.com/gregkh/linux/v7.2.11/fs/btrfs/scrub.c; tag v7.2.11 peeled `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea` | "return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;"; "bwlimit = READ_ONCE(device->scrub_speed_max);"; "if (bwlimit == 0)" | `.ufo/waves/round-44/frozen/src/scrub.c:3336, 1380-1381` |
| S243 | https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/fs/btrfs/sysfs.c?h=v7.2.11 — raw `plain/fs/btrfs/sysfs.c?h=v7.2.11`, 72925 B, sha256 `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43`, byte-identical to https://raw.githubusercontent.com/gregkh/linux/v7.2.11/fs/btrfs/sysfs.c; same tag peel | "return sysfs_emit(buf, "%llu\n", READ_ONCE(device->scrub_speed_max));"; "__INIT_KOBJ_ATTR(_name, 0644, _show, _store)"; "limit = memparse(buf, &endptr);"; "if (*endptr != 0)" | `.ufo/waves/round-44/frozen/src/sysfs.c:2028, 74, 2040, 2043` |
| S244 | https://gitlab.archlinux.org/archlinux/packaging/packages/btrfs-progs/-/tree/7.1-1 — raw `…/-/raw/7.1-1/btrfs-scrub@.timer` 160 B sha256 `9a0b6cc2…f8ad`, `…/btrfs-scrub@.service` 190 B sha256 `eaa7af92…0252`, `…/PKGBUILD` 3057 B sha256 `3b803e8b…ce98`; tag 7.1-1 commit `0c0a4d77b318084ecd35aeeb6888d8a5b4d6e3e0` (GitLab tag API 200, committed 2026-07-15) | "OnCalendar=monthly"; "Persistent=true"; "ExecStart=/usr/bin/btrfs scrub start -B %f"; "KillSignal=SIGINT"; "install -Dm644 btrfs-scrub@.service "${pkgdir}/usr/lib/systemd/system/btrfs-scrub@.service"" | `.ufo/waves/round-44/frozen/src/btrfs-scrub@.timer:5, 8`; `…/btrfs-scrub@.service:9-10`; `…/PKGBUILD:100` |
| S245 | no URL — own-work capture `.ufo/waves/round-44/frozen/hostcap/`, re-read 2026-10-26 (`capture.sh` run 2026-10-26T23:53:22Z, uid 1000, `CapEff=0000000000000000`; capture.txt sha256 `efb52388…e84900`, capture.sh sha256 `6a297e4f…876f6d`) | "var_lib_btrfs absent"; "mode=644 owner=root value=0"; "wants_btrfs_scrub_instances 0" | `.ufo/waves/round-44/frozen/hostcap/capture.txt:3, 4, 5` |

Quoted words per row: S242 17, S243 16, S244 12, S245 7; every location falls inside the row's own anchor range.

Snapshot digests: `.ufo/waves/round-44/frozen/src/SHA256SUMS` (scrub.c `f347931b…938ca5b8`, sysfs.c `ce146120…4f731c43`,
timer `9a0b6cc2…9d6f8ad`, service `eaa7af92…fb240252`, PKGBUILD `3b803e8b…6c10ce98`), fetch log `FETCH.txt`; capture.txt
`efb52388…e3e84900`, capture.sh `6a297e4f…8376f6d`. The final re-open (`.ufo/waves/round-44/w2/SrcGateFinal/fetch-log.txt`)
reproduced all five frozen files and both kernel mirrors byte-for-byte, printed the kernel tag page (`v7.2.11` tagged
object `8316c24e…65d3` → commit `a2de78ee…b6ea`) and the Arch `7.1-1` tag API record.

### Rows re-opened and rows touched old→new

| Row | URL (access 2026-10-26) | Located quote (≤25 words) | Location |
|---|---|---|---|
| S237 | https://github.com/kdave/btrfs-progs/blob/v7.1/cmds/scrub.c — raw `raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c`, 57034 B, sha256 `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801`; tag v7.1 peeled `4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b` | "ret = ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL);" | `.ufo/waves/round-42/frozen/src/scrub.c:421` |
| S240 | https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/fs/btrfs/ioctl.c?h=v7.2.11 — raw `plain/fs/btrfs/ioctl.c?h=v7.2.11`, 145999 B, sha256 `7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01`; tag v7.2.11 peeled `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea` | "ret = btrfs_scrub_progress(fs_info, sa->devid, &sa->progress);" | `.ufo/waves/round-43/frozen/src/ioctl.c:3139` |

Rows touched: **S237 `used-by`** `corpus/knowledge/btrfs-scrub-record-r42.md, corpus/knowledge/btrfs-scrub-record-r43.md`
→ `corpus/knowledge/btrfs-scrub-record-r42.md, corpus/knowledge/btrfs-scrub-record-r43.md,
corpus/knowledge/btrfs-scrub-record-r44.md`; **S240 `used-by`** `corpus/knowledge/btrfs-scrub-record-r43.md` →
`corpus/knowledge/btrfs-scrub-record-r43.md, corpus/knowledge/btrfs-scrub-record-r44.md`.
`git diff 98020ece0674e0b569ee23aed10ffbee355b248e 8eee79db608b5815c325a5af7cbfdeac50eda9f4 -- corpus/SOURCES.md` is
one hunk (6 insertions, 2 deletions): those two rows differ in column 11 only, cells 1-10 byte-identical (`status`
`mined`, `opened` `2026-10-26`, `recheck` `on-release`); the four new rows are appended at `:251-254`, S237/S240 keep
`:246`/`:249`, and no other row's `used-by` moves. 241 rows at the base, 245 at the tip; the added target
`corpus/knowledge/btrfs-scrub-record-r44.md` exists at the tip
(`.ufo/waves/round-44/w2/SrcGateFinal/registry-diff.txt`).

### Census (frozen command)

`bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`: start `tsukuroi ok`, exit 0,
40 W04, 241 rows (`.ufo/waves/round-44/before/sources-census-start.txt`); end `tsukuroi ok`, exit 0, 40 W04, 245 rows,
the W04 set identical to the start receipt and no `E` code naming S237-S245
(`.ufo/waves/round-44/w2/SrcGateFinal/sources-census-final-8eee79db.txt`, `…/census-w04-diff.txt`).
```

Row counts in the census paragraph are `grep -cE '^\| S[0-9]{3} '` on each revision's `corpus/SOURCES.md`.

## 7. Touched surfaces, gates run, limits

- Wrote only `.ufo/waves/round-44/w2/SrcGateFinal.md` (this report) and receipts under
  `.ufo/waves/round-44/w2/SrcGateFinal/`: `fetch-log.txt`, `quotes.txt`, `registry-diff.txt`,
  `sources-census-final-8eee79db.txt`, `census-w04-diff.txt`, `tag-pins.txt`, `gatecheck.py` (replayable: `python3 gatecheck.py
  <outdir>` from the receipt dir; it re-reads the frozen files, `git show` and the registry, and writes only
  `<outdir>`). No tracked lane file, no fleet-root file, no `~/.local/bin`, no `corpus/` edit, no git/jj mutation.
- Gates run: 16 HTTP re-opens + 9 quote-set checks (17 quote lines, 0 mismatches, per-row word bounds), the
  base→tip registry parse + diff, and one census `validate`. Nothing else.
- Not run, by design: neither frozen counter (`score-scrub-arm-r44.py`, `check-scrub-record-r44.py`) — both are other
  seats' items and heavy; no C1/C2 verdict work; no `sources-census.sh --selftest`. No package, service, timer, sysfs,
  mount or scrub operation; `pacman` untouched (paused); no subagent dispatch (leaf seat).
- Limits: the HTML `tree`/`blob`/tag pages were fetched but only checked for HTTP 200 and content (kernel tag hash,
  GitLab tag JSON) — their bytes are not reproducible artefacts, so no digest claim is made about them. The
  "byte-identical to the GitHub mirror" clause rests on equal sha256 of the two raw fetches, taken minutes apart in
  the window above, not on a simultaneous comparison. Scratch
  `/fast/scratch/hyaku/tsukuroi-r44/SrcGateFinal/` was removed after the receipts were copied.
