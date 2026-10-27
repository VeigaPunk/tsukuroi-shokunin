VERDICT: no-finding
Assimilation verdict: none — no staged theme in the corpus-expansion-1 merge package fits this round's surfaces (btrfs scrub grounding / census TMPDIR contract); and the package as staged would collide with 53 existing lane S-ids, including this round's own frozen sources.

# AsmGate — F-2 assimilation check, round 47 w1

Read-only; shokuknow touched only by read/grep. No campaign tool run. No tools installed (none needed).

## 1. What the merge package says about itself

`/home/vgpnk/Projects/shokuknow/merge/tsukuroi/MERGE-REPORT.md`:
- Staged by `corpus-expansion-1`; "**Nothing was written into the lane repo.**"
- 147 proposed rows accepted, 0 refused; 70 knowledge entries; rows by round round1..round16.
- Claim (MERGE-REPORT.md:9): "lane registry currently holds **199** rows; first staged id is **S200**".
- Adopt checklist step 3: append `SOURCES.append.md` to `corpus/SOURCES.md`; steps 5-6: amendments append-only, duplicate targets folded.
- Flagged duplicate-target table: staged `S201` vs lane's own `S008` (aspects differ; operator check advised).

`/home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md` header (observed lines 2-3):
```
<!-- corpus-expansion-1 :: staged rows for lane tsukuroi -->
<!-- Review before appending. Each row was opened in the round that wrote it. -->
```
then the 11-column schema (`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`) and 147 data rows. First staged id S200, last S346 (observed).

## 2. Re-derived tsukuroi slice of the absent-defect register

Source: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` (data rows whose lane cell is `` `tsukuroi` ``; the per-lane count line `| `tsukuroi` | 2 |` at register line 253 is a totals row, not a data row).

**12 data rows** (verified two ways: `grep -c '^| `tsukuroi` |'` = 13 minus 1 totals row; independent awk field parse = 12):
- `payload-absent` (2) — register's fabrication class; hand-verify then correct or refuse:
  - line 229: round1 `S211` — plymouth GitLab repository tags API; quote `name: 26.134.222 ... created_at: 2026-05-14T05:21:12.000Z` in none of source/companions/local artifacts.
  - line 230: round1 `S213` — Oracle Linux 8 Snapper doc; quote `has a newer release appeared?` in none of them.
- `never checked` (10) — source unreachable or gate block named no locator; unverifiable as fetched:
  - line 366: round3 `S225`` — ArchWiki Translation_Team zh URL unfetchable.
  - lines 367-368: round3 `S230``, `S231`` — gate blocks named no locator.
  - lines 369-371: round4 `S242``, `S243``, `S244`` — gate blocks named no locator.
  - lines 372-375: round5 `S249``, `S250``, `S251``, `S252`` — gate blocks named no locator.

Receipt: `.ufo/waves/round-47/w1/AsmGate/register-tsukuroi-slice.txt` (all 13 `tsukuroi` lines incl. the totals row, with register line numbers).

Register ids are corpus-expansion staged ids; see §4 — in the lane's own S-space the same numbers name different rows.

## 3. Collision check (frozen command form, re-run)

Commands (run in seat scratch, cwd `/fast/scratch/hyaku/tsukuroi-r47/AsmGate`):
```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' <lane>/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort   # lane-ids.txt
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' <shokuknow>/merge/tsukuroi/SOURCES.append.md | grep -oE 'S[0-9]+' | sort   # append-ids.txt
comm -12 lane-ids.txt append-ids.txt
```
Observed:
- lane `corpus/SOURCES.md`: **252** ids, continuous **S001-S252** (corroborated by counting actual table rows `grep -cE '^\| S[0-9]{3} \|'` = 252, first S001, last S252).
- staged `SOURCES.append.md`: **147** ids, **S200-S346** (actual table rows = 147).
- **Intersection: 53 ids — S200 through S252.**
- staged-only: 94 (S253-S346). lane-only: 199 (S001-S199).

Receipts: `.ufo/waves/round-47/w1/AsmGate/{lane-ids.txt, append-ids.txt, sid-collision.txt}`.

Consequence: MERGE-REPORT.md's "lane registry currently holds 199 rows; first staged id is S200" is **stale** against the current lane registry (252 rows). Appending as-is would overlay 53 ids. Worse, the colliding band covers this round's own frozen sources — same id, unrelated content, e.g.:
- lane S242 = `Linux v7.2.11 fs/btrfs/scrub.c` (C1 source S242) vs staged S242 = `/boot writers for /boot/limine.conf` own-work.
- lane S243 = `fs/btrfs/sysfs.c` (C1 source S243) vs staged S243 = `Btrfs space allocation and ENOSPC` own-work.
- lane S244 = `btrfs-progs packaging 7.1-1` (C1 source S244) vs staged S244 = `Btrfs repair and maintenance decisions` own-work.
- lane S249 = `Round-45 host scrub-service stop capture` (C1 source S249) vs staged S249 = zh_TW kernel-translation index.
- lane S252 = `mktemp(1)` (the C2 source S252) vs staged S252 = `check-boot-writers.py --selftest`.

So assimilation is blocked on id-rebasing (or lane-side renumbering) regardless of theme fit.

## 4. Theme fit against this round's surfaces

Round 47 surfaces: C1 = btrfs scrub grounding (kernel scrub.c semantics, sysfs `scrub_speed_max` write parser, dev-replace scrub exclusion with -EAGAIN/EINPROGRESS ordering, systemd v262 kill semantics for btrfs-scrub@.service); C2 = census TMPDIR contract (mktemp(1) template placement, classifiable fixture base, `tsukuroi-census.sh --selftest` 164-case grid).

Term census of the staged package (`/home/vgpnk/Projects/shokuknow/merge/tsukuroi/`):
- `scrub`: 1 hit, in staged row S269 (ext4 jbd2 journal doc) — comparative clause only ("a different class of claim from btrfs's checksum-plus-scrub detection"). Not a scrub-grounding row.
- `mktemp`: 0. `TMPDIR`: 0. `census`: 0 (SOURCES.append.md). `BTRFS_IOC_SCRUB|SCRUB_IOCTL|btrfs_ioctl_scrub|systemd.kill|dev-replace|dev_replace`: 0 rows.
- `sysfs`: 4 hits, all `sysfs.txt` inside kernel zh_CN/zh_TW filesystem-translation directory listings (S260, S262-S264) — unrelated to the btrfs sysfs scrub interface.
- No file under `merge/tsukuroi/knowledge/` matches scrub/mktemp/TMPDIR/census/sysfs except `lane-harness-selftest-r29.md` (via "harness" filename match; content read in full).

Closest staged items, and why they still miss:
- `knowledge/corpus/knowledge/lane-harness-selftest-r29.md` — the lane's harness, but it is `tools/check-boot-writers.py` (12-case hermetic selftest, round-19 writer-attribution frontier). Round 47 C2 is a different harness, `tools/tsukuroi-census.sh` (162→164 cases, TMPDIR-with-space fixture base). Different tool, different contract; no fit.
- Staged btrfs rows (S204 subvolume(8), S220 ioctl.c snapshot handlers, S223 btrfs.h uapi, S243/S244 lane ENOSPC/repair own-work recaps) — subvolume/snapshot/space-accounting surface; none touches the scrub path, `scrub_speed_max`, dev-replace, or the scrub service unit.
- Staged systemd content: none (no systemd.kill(5)/systemd.exec rows at all).

Staged themes overall (70 knowledge files): mkinitcpio hook API, alpm hooks/scriptlets, overlayfs mount contract, errno vocabulary, snapper rollback, plymouth release watch, btrfs ioctl/subvolume, ext4 journal, East-Asian kernel-doc/wiki translation coverage, zhwiki mirror, cmpp historic corpus, lane own-work recaps. None is a scrub-grounding or census-TMPDIR theme.

## 5. Gate conclusion

- Assimilation verdict: **none** for round 47's surfaces. The package holds nothing that grounds C1's scrub claims or C2's TMPDIR contract; the one harness file covers the wrong checker.
- Package-level blocker independent of theme: **53-id collision (S200-S252)** with the current lane registry, including the lane's own C1/C2 frozen source ids; MERGE-REPORT's "199 rows / first staged S200" premise is stale.
- Outstanding register debt on the tsukuroi slice (for whenever assimilation is revisited): 2 payload-absent rows (staged S211, S213) need hand verification — correct the quote or refuse the row per the register's own doctrine; 10 never-checked rows (staged S225, S230, S231, S242, S243, S244, S249, S250, S251, S252) need re-fetch or an explicit unverifiable mark.

## Evidence index
- `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/MERGE-REPORT.md` (full read).
- `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md:1-153` (header + all 147 rows).
- `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:229,230,253,366-375` (tsukuroi slice).
- Commands and observed outputs: §3 (collision check), §4 (term greps). Receipts under `.ufo/waves/round-47/w1/AsmGate/`.
- Not done: no re-fetch of the 10 unreachable register URLs (network fetch of staged-row sources is outside this gate item); no campaign tool run (prohibited; not needed).
