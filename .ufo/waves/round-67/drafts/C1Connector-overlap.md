2026-11-03T22:06:00Z
# C1Connector — sibling overlap scan (round 67, wave w1, read-only)

Lane: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin, HEAD 071a55c9c0fd022890d1b255c2782e4761e7a7d8 (`git -C <lane> rev-parse HEAD`, rc 0).
Method: read-only git only (`rev-parse HEAD`, `grep HEAD`, `show HEAD:path`, `ls-tree HEAD`, `cat-file -e`). No sibling file touched, no checkout, no install, no sudo, no scrub, no fetch. Scratch scripts in /fast/scratch/hyaku/tsukuroi-r67/C1Connector/ (deleted before yield). "HEAD" below always means the sibling's committed tree at the HEAD listed.
Lane reference notes: btrfs-scrub-record-r42.md (SC1-SC5), btrfs-scrub-record-r43.md (SR1-SR9 numbering; SR8 is in btrfs-scrub-record-r44.md), PROVINCE.md.

## 0. Sibling HEADs (exact command: `git -C <dir> rev-parse HEAD`, rc 0 for all 19)

| sibling | HEAD | has tools/ | has corpus/ |
|---|---|---|---|
| audio-shokunin | f9da7ee97e0ba95da1803c2afe9c616c519bae18 | no | yes |
| chousa-shokunin | f748abbb6bf58388e732facd4ecec5612419c457 | yes | yes |
| game-dev-2d-shokunin | 1e033ef053beedf9a201daa21fbeb9c8b2f72dc3 | no | yes |
| game-dev-3d-shokunin | 39ca3973c7865456d97fae18033f3f460c6cf8c1 | no | yes |
| kagi-shokunin | cb7b9b3522d0082c84b1d8680bca71911f6f1428 (re-read 2026-11-03T22:07:35Z; an earlier read at 22a7119cf191bc734b682a2ee372a929c13fac99 had no in-scope hit either) | no | yes |
| kaidoku-shokunin | c7fe6898e9a8b3ff04486b4a1d672e9db37610c9 | yes | yes |
| kake-shokunin | a19d38ea7ce4dfe979001466e9ca9c6a14176e9a | no (scripts/ only) | yes |
| kama-shokunin | 6035e952c2521999e192d6f236331f265ac98392 | yes | yes |
| kasegi-shokunin | 15cd5771f460ba5e999af416b45edeed4fd54236 (re-read 2026-11-03T22:07:35Z; the OOS-11 hits below were read at 472737847ff31d1255bf1a0745822a5e878e9622, not re-read at this HEAD) | no | yes |
| kengaku-shokunin | dcc39ea3f5335e38d941a4dd8a780947367a28fa | no | yes |
| kotoba-shokunin | 1c8f37edf2e5ac0fb3c2be1c88e32406313fe47b | no | yes |
| kotodama-shokunin | c285b2afb19d4b64320e18df1f55e426bf2d0b0c | yes | yes |
| kumitate-shokunin | 3c369336218329e30248b5d69c41348c02658169 | no (scripts/ only) | yes |
| lore-shokunin | 0f044aa7c7e4e17cfd5b6278179709b60db45d61 | no | yes |
| mado-shokunin | 524fa1f90b1f2de44b3019bacf833d54e0af13a0 | yes | yes |
| mori-shokunin | 84c6cbc3b47c536a504aaee329c77897d389935e | yes | yes |
| revenger-shokunin | 5915ad8d71c19ad377829d130ba1c35445eb32a4 | no | yes |
| souji-shokunin | b6c6a93a6f892878da15e1de6c57ead221bd5be2 | yes | yes |
| tabi-shokunin | 67d6f70e43979bafe179d4011eafea9ca3a50b39 | no (scripts/ only) | yes |
| tameshi-shokunin | f20ba482c7441d4c75818e7cd8a3165fee7821a1 | yes | yes |

HEAD drift record: siblings are live. Two reads were taken: the first listing (about 22:00Z) and a re-read at 2026-11-03T22:07:35Z (the table above). Between them kagi moved 22a7119c→cb7b9b35, kasegi moved 47273784→15cd5771, and souji read 3ce0ba03 in the first listing and b6c6a93a at the re-read; tabi read 8a3f6f89 in the first listing and 67d6f70e at the re-read. The in-scope grep (§1a) was re-run at the re-read HEADs and returns the same result (mori only). The first-listing HEADs are not used for any verdict. Verdicts that cite OOS-11 (kasegi) rest on the earlier HEAD and are marked as such.

## 1. Btrfs scrub-limit material (item 1)

### 1a. The item's own search, scoped as written
Command, per sibling: `git -C <dir> grep -l -E 'scrub_speed_max|scrub limit|btrfs-progs|btrfs scrub' HEAD -- corpus tools PROVINCE.md SKILL.md`
Result: exactly one sibling hit, all others rc 1 (no match).
Line-level re-run: `git -C mori-shokunin grep -n -I -E '...' HEAD -- corpus tools PROVINCE.md SKILL.md` rc 0, 7 lines, all in one file.

Siblings with no hit in scope: audio, chousa, game-dev-2d, game-dev-3d, kagi, kaidoku, kake, kama, kasegi, kengaku, kotoba, kotodama, kumitate, lore, mado, revenger, souji, tabi, tameshi (19 siblings: none).

### OV-C1 rows (in-scope hits, one row per line)

Sibling: mori-shokunin, HEAD 84c6cbc3b47c536a504aaee329c77897d389935e. File: corpus/evidence/sources-r55/btrfs_sysfs.c.v7.3 (kernel fs/btrfs/sysfs.c at tag v7.3; its sha256 098cb522131501deabde61ffcdc56138a8516098f4e980f9c34cb9e62b467377, matching mori SOURCES S539).

| id | path:line | text (verbatim, trimmed) | verdict | basis |
|---|---|---|---|---|
| OV-C1-1 | mori-shokunin corpus/evidence/sources-r55/btrfs_sysfs.c.v7.3:2021 | `static ssize_t btrfs_devinfo_scrub_speed_max_show(struct kobject *kobj,` | AGREES | attribute show handler exists; lane SR8 (btrfs-scrub-record-r44.md:58-60) says the sysfs attribute is `devinfo/<devid>/scrub_speed_max` |
| OV-C1-2 | mori-shokunin corpus/evidence/sources-r55/btrfs_sysfs.c.v7.3:2028 | `return sysfs_emit(buf, "%llu\n", READ_ONCE(device->scrub_speed_max));` | AGREES | SR8 "reading prints ... one decimal number followed by a newline" |
| OV-C1-3 | mori-shokunin corpus/evidence/sources-r55/btrfs_sysfs.c.v7.3:2031 | `static ssize_t btrfs_devinfo_scrub_speed_max_store(struct kobject *kobj,` | AGREES | SR8 write path (memparse + reject trailing) is the store handler; the parse body was not re-read at v7.3 |
| OV-C1-4 | mori-shokunin corpus/evidence/sources-r55/btrfs_sysfs.c.v7.3:2045 | `WRITE_ONCE(device->scrub_speed_max, limit);` | AGREES | store sets the in-memory limit that SR8 describes |
| OV-C1-5 | mori-shokunin corpus/evidence/sources-r55/btrfs_sysfs.c.v7.3:2048 | `BTRFS_ATTR_RW(devid, scrub_speed_max, btrfs_devinfo_scrub_speed_max_show,` | AGREES | SR8 "declared with BTRFS_ATTR_RW" |
| OV-C1-6 | mori-shokunin corpus/evidence/sources-r55/btrfs_sysfs.c.v7.3:2049 | `btrfs_devinfo_scrub_speed_max_store);` | AGREES | continuation of OV-C1-5 (store handler binding) |
| OV-C1-7 | mori-shokunin corpus/evidence/sources-r55/btrfs_sysfs.c.v7.3:2113 | `BTRFS_ATTR_PTR(devid, scrub_speed_max),` | AGREES | attribute registered in the devinfo group |

Scope of these verdicts: all seven are KERNEL sysfs.c at tag v7.3. None is btrfs-progs cmds/scrub.c. They do not touch the C1 claim (the v7.3 per-device scrub-limit revert in btrfs-progs cmds/scrub.c). They agree with the lane's attribute mechanics only; they say nothing about the revert.

### Sibling copy with byte identity to a lane source (in-scope? no: under .ufo/, reported for completeness)
- mori-shokunin .ufo/waves/round-23/evidence/sources/S079-fs_btrfs_sysfs.c (HEAD 84c6cbc3…): `git show HEAD:<path> | sha256sum` = ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43. This equals the lane S243 raw-bytes digest (corpus/SOURCES.md:252, kernel v7.2.11 fs/btrfs/sysfs.c). Verdict AGREES (byte-identical copy of lane S243). Rc 0.

### C1 revert in btrfs-progs v7.3 cmds/scrub.c (sha b58942cc…, CHANGES 5046bac1…)
Search for any copy: `git -C <sib> grep -l -E 'cmds/scrub|btrfs-progs-7\.3|scrub\.c' HEAD` over all 19 siblings. Result: no btrfs-progs v7.3 scrub.c, no CHANGES copy and no `btrfs-progs-7.3` string outside the lane. The only hits are the sibling wave transcripts listed in §1c. Verdict for the revert: NONE (no sibling carries it).

### 1b. Lane notes compared
- lane btrfs-scrub-record-r42.md SC5 (sysfs limit, read by status/start, 0 = none) and r44 SR8 (mode 0644, decimal + newline): OV-C1-1..7 agree on attribute mechanics. OV-C1 agrees with r42/r43 on the sysfs attribute only; r42/r43 contain nothing about the kernel-side write handler at v7.3.
- No OV-C1 row contradicts a lane r42/r43 statement. No CONFLICTS verdict in the in-scope set.

### 1c. Out-of-scope hits (lane-wide `git -C <sib> grep -n -I -E 'scrub_speed_max|scrub limit|btrfs-progs|btrfs scrub' HEAD --`, rc 0 for these siblings; under .ufo/ wave records, not corpus/tools/PROVINCE/SKILL). Listed for the record; NOT counted as OV-C1 rows.

| ref | sibling HEAD | path:line | verdict | basis |
|---|---|---|---|---|
| OOS-1 | tabi 67d6f70e… | .ufo/waves/round-34/w2/ConnSiblingDrift/tsukuroi.diff:172, :218, :222 | CONFLICTS (stale copy) | a round-34 diff of the lane's r42 SC rows carries "never a half-written one" (SC1), "(or is resumed)" and "only the final write reports a failure" (SC3). The lane withdrew those three in r42 wave-2 and restated them as SR1/SR3 in r43 (btrfs-scrub-record-r43.md, "Corrections"). |
| OOS-2 | tabi 67d6f70e… | .ufo/waves/round-34/w2/ConnSiblingDrift.md:86 | UNRELATED | sibling-drift list naming "tsukuroi btrfs scrub/census" as a drift target |
| OOS-3 | chousa f748abbb… | .ufo/waves/round-61/w1/RevProvince.md:22 | AGREES | names lane PROVINCE.md lines 239–241 as the btrfs-progs cmds/scrub.c rename-write Frontier entry; lane PROVINCE.md:239 is the "Round-42 note — scrub record read from source" line, so the locator still resolves |
| OOS-4 | chousa f748abbb… | .ufo/waves/round-61/w1-results.json:190 | AGREES | same RevProvince verdict text (duplicate of OOS-3) |
| OOS-5 | mori 84c6cbc3… | .ufo/waves/round-48/w1/ScoutQuotaHost.md:14-15 | AGREES | host reading `btrfs --version` → `btrfs-progs v7.1`; lane host reading is btrfs-progs 7.1-1 (btrfs-scrub-record-r42.md Limits) |
| OOS-6 | mori 84c6cbc3… | .ufo/waves/round-48/w1-results.json:196 | AGREES | duplicate of OOS-5 |
| OOS-7 | mori 84c6cbc3… | .ufo/waves/round-27/w2/ConnAdjacencyCheck.md:89 | UNRELATED | "btrfs-progs and volumes.c" in an adjacency map |
| OOS-8 | kaidoku c7fe6898… | .ufo/waves/round-44/w2/R44W2Misroot.md:72-73 | AGREES | kaidoku records that the sentence "a zero-padded scrub_speed_max is still no limit" occurs in lane tools/tsukuroi-census.sh (r44). Not re-read in the current lane tree. |
| OOS-9 | mado 524fa1f9… | .ufo/waves/round-48/w2/ScoutMisroot.md:30; SentScope.md:119; SentScope/03-quarantine.txt:23 | UNRELATED | mado records a lane r44 fixture directory named ...scrub_speed_max; no claim about the limit |
| OOS-10 | kama 6035e952… | .ufo/waves/round-52/w1/out/X10Hygiene.md:57; .../X10Hygiene/hygiene.md:110; .../hygiene-sweep.txt:51,67; .ufo/waves/round-52/w1/w1-results.json:418; .ufo/waves/round-55/w1/out/Sen3/07-quarantine.out:16 | UNRELATED | kama's untracked-file listings that happen to include tags-btrfs-progs.txt / scrub.c research files |
| OOS-11 | kasegi 47273784… | .ufo/waves/round-45/wave1/R45ScoutAdjacent.md:46, :131, :447, :452, :453, :454; wave1-results.json:148 | AGREES | cites lane SOURCES rows; re-read: S240 at corpus/SOURCES.md:249, S242 at :251, S243 at :252 (match). S160 (:166) and S167 (:173) not re-read. |
| OOS-12 | kotoba 1c8f37ed… | .ufo/waves/round-71/receipts/census-after.txt:238 | UNRELATED | census line for a duplicate URL (S155) |
| OOS-13 | mado 524fa1f9… | .ufo/waves/round-44/w2/RerunCensus/census-fleet.txt:248 | UNRELATED | duplicate of OOS-12 census line |

Full-tree grep counts (rc 0 siblings): chousa 2 files, kaidoku 1, kama 5, kasegi 2, kotoba 1, mado 4, mori 5, tabi 2. Siblings with no full-tree hit: audio, game-dev-2d, game-dev-3d, kagi, kake, kengaku, kotodama, kumitate, lore, revenger, souji, tameshi.

## 2. Adjacency gate: silent-skip pattern (item 2)

Lane pattern (tools/check-adjacency-anchors.py): `_live_object_hash` (:447-463) returns None on any failure (bad input, git show failure, timeout); evaluate() at :648-651 does `if live_digest is not None: counts["live_object_checked"] += 1`. An unresolvable record is silently not counted, no finding, status PASS (predicate: ANCHOR-LIVE-OBJECT-UNRESOLVED absent).

Search (exhaustive over every tools/ file at each sibling HEAD, `git ls-tree -r --name-only HEAD tools` then `git show HEAD:<file>`, 19 siblings, rc 0): every `if <var> is not None:` / `if <var> is None:` whose guard var is assigned from a helper call and whose branch is `continue` or whose body increments a counter, with no finding/error append in that branch. Candidates were then read in source.

### OV-C2 rows (match or partial match; none exercised, all from source read)

| id | path:line | helper / guard | branch | verdict | why |
|---|---|---|---|---|---|
| OV-C2-1 | kama-shokunin tools/round46-release-recheck-audit.py:370-372 | `body = show(a.repo, tip, u)` → `if body is None: continue` | silent skip; `missing` not incremented | MATCH | A drifted/removed row whose used-by knowledge file is absent at tip is never checked for the RELEASE flag; `missing` stays 0, verdict `met` can pass. Same shape as the lane's uncounted record. |
| OV-C2-2 | kama-shokunin tools/round44-release-recheck-audit.py:326-328 | `body = show(a.repo, tip, u)` → `if body is None: continue` | silent skip; `missing` not incremented | MATCH | identical shape to OV-C2-1 in the round-44 copy |
| OV-C2-3 | kama-shokunin tools/round53-cited-path-check.py:330-331 | `text = show(lane.path, lane.rev, surf)` → `if text is None: continue` | silent skip of a whole surface | PARTIAL | a missing SURFACE yields zero citations and zero unresolved; no surface-absence finding in this branch. Consequence depends on the caller's verdict; not traced to the end. |
| OV-C2-4 | kama-shokunin tools/round54-cited-path-check.py:594-595 | same as OV-C2-3 | silent skip of a surface | PARTIAL | same as OV-C2-3 in round-54 |
| OV-C2-5 | mori-shokunin tools/mori-drift-adjudicate.py:130-132 | `copy_path = mod.find_copy(...)`; `if url is None or copy_path is None: emit("<sid> no-copy")` | row printed as no-copy, not in `adjudicated`, not in `unresolved` | PARTIAL | visible on stdout per row, documented state (mori-source-drift.py:15 "no-copy"); exit code 0 with adjudicated=0 is possible. Visible, not silent. |
| OV-C2-6 | kaidoku-shokunin tools/round-26/c1-id-identity.py:855-856 | `blob = read_blob(root, sha, path)` → `if blob is None: continue` | path omitted from `out` | PARTIAL | feeds only the non-gating `diagnostics_not_gating.tree_path_text` (line 473); no count, no gate |
| OV-C2-7 | kaidoku-shokunin tools/round-42/c2-counter.py:1659-1660 | `blob = show(root, rev, rp)` → `if blob is None: continue` | envelope omitted from `dpaths` | PARTIAL, gated | `dev_ok = len(dpaths) >= DEV_MIN and dused is not None` at :1676 is a floor on the count, so a silent skip fails closed |
| OV-C2-8 | kaidoku-shokunin tools/round-42/c2-counter.py:1726-1727 | `blob = show(root, rev, '%s/%s/envelope.json' % ...)` → `if blob is None: continue` | envelope omitted from the `dev_declared` fallback | PARTIAL | consequence of an empty `dev_declared` not traced |
| OV-C2-9 | kaidoku-shokunin tools/round-40/c2-counter.py:208-209 | `b = show(root, c, SKILL)` → `if b is None: continue` | commit dropped from the newest-first walk | PARTIAL | a dropped commit can change which revision is returned as first_without; not exercised |
| OV-C2-10 | kaidoku-shokunin tools/round-46/registry.py:362-363 | `body = gate.show(root, rev, p)` → `if body is None: continue` | file omitted from a forged-fixture repo | PARTIAL | the fixture is built without the file; graded downstream, not checked here |

OV-C2 count: 10 rows (2 MATCH, 8 PARTIAL). Other kaidoku counters with the same `show()`→`continue` shape (round-41/42/43/44/49/50 c1/c2-counter: about 20 more sites) were not each traced; they are the same family as OV-C2-7..9 and are not counted.

Considered and REJECTED (same grep, not counted):
- tameshi tools/coldread-precheck-portable.py:152-154, 221, 237: `loaded`/`hit` None means cache miss and the code refetches; not a skipped verdict.
- tameshi tools/pin-disposition.py:530-545 (`repo_identity` returns (None, reason)): reason is written into the row as status unavailable; the opposite of a silent skip.
- tameshi tools/receipt-exists.py (`resolve_rev` None → rc 2): refuses, not silent.
- chousa tools/build-spans.py:431-432 (`sfd is None`): an absent spans dir yields SPANS_FILE_STALE per row, not silence.
- kotodama tools/check-draft-ids.py:135-136, 146-147 (`find_group` None): None is the legitimate "not inside a group" answer, not a failed lookup.
- mori tools/mori-routed-r24.py:884-888: `if not commit: continue` and `if blob is None: continue`; `usable` empty appends a reason (:893-894), so the pass needs at least one positive; fail-closed.
- kotodama tools/gates/*: counters incremented on verdicts, no None guard.

Lane-pattern verdict: no sibling reproduces the lane's exact defect (a None-returning sibling-resolution helper feeding a count that a PASS verdict never compares to the record total). OV-C2-1 and OV-C2-2 are the nearest in effect (silent skip that suppresses a FAIL-able count), and are unexercised.

## 3. Ownership split check (item 3)

Lane PROVINCE.md ownership rows, read at HEAD working tree (lane is read-only here):
- ADJ-04 row: PROVINCE.md:49 → mori, locator OUT-005 at :125 (mori PROVINCE.md @ 91940fa339e3).
- ADJ-06 row: PROVINCE.md:51 → "protocol integrator — kaidoku/revenger ownership unresolved", locators OUT-008 (:128, kaidoku) and OUT-009 (:129, revenger).
- Frontier arbitration: PROVINCE.md:79 "Kaidoku and revenger both declare shipped-artifact RE. The integrator must arbitrate this shared scope"; R20 correction text near PROVINCE.md:152.
- Disk runway split: PROVINCE.md:165-167 ("disk-space runway and free-capacity reporting remain mori's (../mori-shokunin/PROVINCE.md:26)") and the round-26 correction at PROVINCE.md:176 ("Mori's disk surface covers the fleet root and /tmp; free space as an upgrade or boot precondition is this lane's"); the round-38 and round-44 notes at :216 and :283 repeat "Mori's: disk-space runway as fleet capacity".

Sibling hits touching btrfs scrub or disk runway:
- mori PROVINCE.md:25 (Kill/OOM classes) and :26 (Resource runway, `SURFACE disk` default `df -P` targets `$ROOT` and `/tmp`). Read at mori HEAD 84c6cbc3. This matches the lane's :176 description of mori's disk surface (fleet root and /tmp). ADJ-04 OUT-005 (mori owns kill/OOM classification) matches mori :25.
- mori corpus/knowledge/disk-runway-enospc-r55.md:23-58 (btrfs ENOSPC reading, S538/S539; line 43 names `/sys/fs/btrfs/<uuid>/allocation/...` counters; line 50 reads `/` btrfs free space). Verdict for the split: STANDS. This entry is a fleet-runway/ENOSPC interpretation, which PROVINCE.md:165-167 and :176 assign to mori. It reads the same `/` btrfs free space the lane uses for update safety, but by a different question (runway, not upgrade precondition), so the split by question holds.
- mori S539 (corpus/SOURCES.md:319) and btrfs_sysfs.c.v7.3 (OV-C1-1..7): kernel counters, not scrub, no ownership claim.
- chousa .ufo/waves/round-61/w1/RevProvince.md:22 (OOS-3): sibling statement that the rename-write Frontier entry is tsukuroi's. Consistent with PROVINCE.md:239-241.
- tabi round-34 diff (OOS-1): stale copy of withdrawn SC1/SC3 text; not an ownership claim.

Verdicts:
- ADJ-04 (mori): STANDS. mori's Kill/OOM class (PROVINCE.md:25) and the disk runway (:26) are the two rows mori declares; the lane's ADJ-04 row is kill/OOM and attribution only. No sibling hit moves kill/OOM attribution.
- ADJ-06 (kaidoku/revenger): UNCHANGED, unresolved. No btrfs-scrub or disk-runway sibling hit touches shipped-artifact RE. The arbitration line (PROVINCE.md:79) and the ADJ-06 integrator row (:51) still control. Kaidoku's own R44W2Misroot note (OOS-8) concerns a lane sentence, not RE ownership.
- Disk-runway split (PROVINCE.md:165-167, :176): STANDS, as read above.

## 4. Counts and gates
- OV-C1 rows (in-scope, item 1): 7 (OV-C1-1..7, all mori-shokunin, one file, all AGREES on attribute mechanics; 0 CONFLICTS; C1 revert: NONE in any sibling).
- OV-C2 rows (item 2): 10 (2 MATCH, 8 PARTIAL), all unexercised.
- Out-of-scope references: 13 (OOS-1..13), not counted.
- Sibling in-scope hits: mori only. Lane-wide hits: chousa, kaidoku, kama, kasegi, kotoba, mado, mori, tabi.
- Not run: lane census, lane selftest, any build or gate (per item). No installs (none needed). No pacman, systemctl, sudo, or privilege probes (not in item scope).
