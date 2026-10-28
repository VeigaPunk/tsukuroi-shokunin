VERDICT: defect-found

Entry under audit: `corpus/knowledge/btrfs-scrub-grounding-r45.md` at freeze `8029cdba1049df25632c91a23c8db4eefb54be5f` (307 lines). Registry: `corpus/SOURCES.md` at the same revision. Bytes read with `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 8029cdba1049df25632c91a23c8db4eefb54be5f:<path>`. No language server was available for these markdown tables; the freeze blobs are the evidence. Snapshot sha256 values are `hashlib.sha256` of those blobs. Receipts: `.ufo/waves/round-50/w1/R50ScoutProvenance/per-row.json`, `source-line.txt`. Upstream URLs were not re-fetched.

Nine `S###` tags appear. The header list on line 1 is `S246 S247 S248 S249 S242 S243 S244 S237 S240`. The same nine are the only tags in the body (lines 2–307). Body tags absent from the header: none. Header tags absent from the body: none. Round-49 defect 2 (S240 missing from the `source:` line) is not present in these bytes: line 1 names S240 and the ioctl.c snapshot, and QUALITY item 7 (line 261) names S240. Line 300 recounts that old defect in the past tense.

One check fails. S240's `used-by` does not name this entry.

## Header coverage

`source:` line 1 names each id and the snapshot the rows use (full line in `source-line.txt`, 915 characters):

- S246 — `.ufo/waves/round-45/frozen/src/` `cmdline.c`, `vsprintf.c`, `kstrtox.c`, digests in that directory's `SHA256SUMS`
- S247 — same directory, `dev-replace.c`
- S248 — same directory, `systemd.kill.xml`
- S240 — `.ufo/waves/round-43/frozen/src/ioctl.c`, sha256 `7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01`
- S249 — `.ufo/waves/round-45/frozen/hostcap/capture.txt`, sha256 `f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70`
- S242 — `.ufo/waves/round-44/frozen/src/scrub.c`
- S243 — `.ufo/waves/round-44/frozen/src/sysfs.c`
- S244 — that directory's `btrfs-scrub@.service`
- S237 — `.ufo/waves/round-42/frozen/src/scrub.c`

Body token lines: S246 at 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 261. S243 at 47, 49, 123, 125, 226. S247 at 87, 89, 91, 93, 95, 97, 119, 121, 127, 129, 131, 224, 229, 301. S242 at 99–101, 103, 105, 107, 109, 111, 113, 115, 117, 133, 135, 137, 139, 141, 225. S240 at 148, 233, 261, 300 (twice on 300). S244 at 170, 172. S248 at 174, 176, 178, 180, 182, 184, 186, 261. S237 at 188, 190, 192, 227. S249 at 261 only.

GR1 (lines 14–55) cites S246 and S243. GR2 (lines 56–152) cites S247, S242, S243, and S240 (line 148: "the replace ioctl takes it around the start, S240 ioctl.c:3190"). GR3 (lines 153–198) cites S244, S248, and S237. S249 is not tokenised inside GR1–GR3. The host-reading paragraphs cite `capture.txt` by filename (lines 51, 143, 194). The S249 tag itself is on QUALITY item 7, line 261: "S249 is own-work and carries host values only". That is a body citation, so S249 is not a header row cited nowhere.

Line 261 also writes the range `S246-S248`, which names S246 and S248 as tokens and S247 only inside the range. S247 is tokenised on its own quote lines, so the range is not the sole citation.

## Per row

Each row exists once in `corpus/SOURCES.md`. Status on every row is `mined` (none is a rejection). Digest column: registry anchor sha256, then sha256 of the snapshot the `source:` line names, at the freeze. They match. Round-45/44/43/42 `SHA256SUMS` lines for these files match the same digests (`git show` of those four `SHA256SUMS` files).

| id | SOURCES.md | used-by names this entry | status | digest vs named snapshot |
|---|---|---|---|---|
| S237 | 246 | yes | mined | match |
| S240 | 249 | no | mined | match |
| S242 | 251 | yes | mined | match |
| S243 | 252 | yes | mined | match |
| S244 | 253 | yes | mined | match (service) |
| S246 | 255 | yes | mined | match (three files) |
| S247 | 256 | yes | mined | match |
| S248 | 257 | yes | mined | match |
| S249 | 258 | yes | mined | match (`capture.txt`) |

### S237

`used-by`: `corpus/knowledge/btrfs-scrub-record-r42.md, corpus/knowledge/btrfs-scrub-record-r43.md, corpus/knowledge/btrfs-scrub-record-r44.md, corpus/knowledge/btrfs-scrub-grounding-r45.md`. Anchor sha256 `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801` equals `.ufo/waves/round-42/frozen/src/scrub.c`. Spot-check: that file line 421 is `ret = ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL);`, the quote at entry line 188. The entry's Limits (line 227) already say S237's declared ranges do not list `scrub.c:421`. The whole-file digest still matches. Not a second defect under this item's four checks.

### S240 — defect

`used-by` (SOURCES.md:249): `corpus/knowledge/btrfs-scrub-record-r43.md, corpus/knowledge/btrfs-scrub-record-r44.md, corpus/lessons/round-48.md`. The string `corpus/knowledge/btrfs-scrub-grounding-r45.md` is absent. The entry cites S240 in GR2 (line 148), Limits (lines 233–235), and QUALITY item 7 (line 261), and the header names it.

Status is `mined`. Anchor sha256 `7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01` equals the header's stated digest and the blob `.ufo/waves/round-43/frozen/src/ioctl.c`. Spot-check of lines the entry cites: ioctl.c:3093 `ret = btrfs_scrub_dev(fs_info, sa->devid, sa->start, sa->end,`; :3132 `if (!capable(CAP_SYS_ADMIN))`; :3190 `if (!btrfs_exclop_start(fs_info, BTRFS_EXCLOP_DEV_REPLACE)) {`. The anchor's declared ranges are `3066-3075, 3118-3140, 5578-5584`, the same gap the entry declares at lines 233–235. Whole-file digest matches. The failed check is `used-by` only.

### S242

`used-by` includes `corpus/knowledge/btrfs-scrub-grounding-r45.md`. Anchor sha256 `f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8` equals `.ufo/waves/round-44/frozen/src/scrub.c`. Spot-check line 3081 contains `bool readonly, bool is_dev_replace`, the quote at entry line 99. Limits line 225 already records that the declared ranges omit `scrub.c:3081`, 3123, 3133, and 3139.

### S243

`used-by` includes this entry. Anchor sha256 `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43` equals `.ufo/waves/round-44/frozen/src/sysfs.c`. Spot-check line 2040 is `limit = memparse(buf, &endptr);` (entry line 47) and line 1288 contains `device replace` (entry line 123). Limits line 226 already records that the declared ranges omit `sysfs.c:1288` and 2015.

### S244

`used-by` includes this entry. The `source:` line names `btrfs-scrub@.service` only. That blob's sha256 `eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252` is the service digest in the anchor. The anchor also pins `btrfs-scrub@.timer` sha256 `9a0b6cc23f7bd97b83b6c38dd2b4e4373fead8bd3ccfb82a47c72971e9d6f8ad`, which equals `.ufo/waves/round-44/frozen/src/btrfs-scrub@.timer`. The entry does not name the timer. The named snapshot matches. Spot-check: the service file line 9 is `KillSignal=SIGINT` (entry line 170). The anchor mentions PKGBUILD lines 99–101 and gives no PKGBUILD digest; the entry does not name PKGBUILD.

### S246

`used-by` is this entry only. Three anchor digests equal the three named blobs: `cmdline.c` `1af5ad98fface0b59694e7565c33be2e37c089cc9a1a841285414ee94546ca9d`, `vsprintf.c` `cabb648a2c72fcbd4a1b00cbbf442ad11235f3224071f5e662db4a77993469ca`, `kstrtox.c` `0c52ae02259f06adaf0a72a572e31ede4d8d6519e1b5625cb6b18d74db8d1ee4`. Spot-check: cmdline.c:147 contains `potentially suffixed with K, M, G, T, P, E.`; vsprintf.c:86 contains `_parse_integer_fixup_radix`; kstrtox.c:29 is `if (s[0] == '0') {`.

### S247

`used-by` is this entry only. Anchor sha256 `f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a` equals `.ufo/waves/round-45/frozen/src/dev-replace.c`. Spot-check line 700 contains `the disk copy procedure reuses the scrub code` and line 1128 contains `Scrub doing the replace isn't running so we need to do the` (entry line 127). Limits lines 229–232 declare that the widened ranges still omit `dev-replace.c:1111`, `:1126-1142`, `:1171-1195`, and `:1184-1188`. Whole-file digest matches.

### S248

`used-by` is this entry only. Anchor sha256 `448322830dbbd02c64cca99941ba92705afe9648241fc917db7a8d6ae7910e72` equals `.ufo/waves/round-45/frozen/src/systemd.kill.xml`. Spot-check line 115 contains `SIGCONT` (entry line 186).

### S249

`used-by` is this entry only. The `source:` line names `capture.txt` and sha256 `f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70`, which equals the freeze blob. The anchor also pins `capture.sh` sha256 `c6d2c448c83de3326109a29638d55d7083ee93edd4242a845b050bc180a751fc`, which equals `.ufo/waves/round-45/frozen/hostcap/capture.sh`. The entry's `source:` line does not name `capture.sh`. The named snapshot matches. `capture.txt` line 1 is `captured 2026-10-27T02:09:52Z uid=1000 CapEff=0000000000000000`.

## Not done

No live re-fetch of the URLs in `.ufo/waves/round-45/frozen/src/FETCH.txt`. No line-by-line check of every `**Quote.**` row beyond the spot-checks above. No tool was installed.
