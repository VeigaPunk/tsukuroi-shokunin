VERDICT: defect-found

Seat R50ExecCensusSources (EXEC-AUTHORIZED, item S-4). Freeze read: `8029cdba1049df25632c91a23c8db4eefb54be5f`; lane tip at my start `39e694934cf6c56434987edc730e8b3580a251f3`. Every byte below was read through `git -C …/tsukuroi-shokunin archive/show <REV>:<path>` or from an archive extraction under scratch — never from the mutable working tree.

Two independent findings, both reproducible:

1. **The frozen registry fails `validate` on its own bytes: 1 E-code (E11) and 40 warnings (W04), rc=1.** The E11 is a dangling `used-by` at `corpus/SOURCES.md:265` — row S256 (GNU grep(1), the C2 source row opened this round) cites `corpus/lessons/round-50.md`, which does not exist at the freeze and does not exist at the lane tip either. It clears the moment the L1 commits the round-50 lesson file.
2. **The assimilation collision guard fires 57 times, and all 57 are true id collisions with different sources** — 0 of 57 have an identical `source` cell. The staged append file reuses the lane's S200–S256 numbering for unrelated rows. The staged package cannot be appended as-is.

---

## (a) Census over the lane registry at the freeze

Command (exact):

```
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin archive 8029cdba1049df25632c91a23c8db4eefb54be5f | tar -x -C <scratch>/full
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <scratch>/full/corpus/SOURCES.md
```

`validate` was first run against a `corpus`-only extraction, which produced 24 spurious E11 rows for `tools/…` and `SKILL.md` (those paths are outside the extracted subtree). The reported numbers below are from the **full-tree** extraction, where E11 resolution has every lane path available. Both runs are in the receipts.

| metric | value | source |
|---|---|---|
| `validate` rc | **1** | `validate-full.out` (last line class: E-code present ⇒ 1) |
| rows in `## Registry` (heading at `corpus/SOURCES.md:3`) | **256** | `census-full.out: file rows 256` |
| warnings | **40**, all W04 (`same URL across scopes`); **zero** W01/W02/W03 | `grep -c $'\tW04\t' validate-full.out` = 40 |
| E-codes | **exactly one**: `file E11 S256 missing used-by corpus/lessons/round-50.md` | `validate-full.out` |
| tier split | A 240 / B 5 / C 11 / invalid 0 | `census-full.out` |
| status split | mined 229 / queued 5 / rejected 22 / invalid 0 | `census-full.out` |
| `census` rc (row metrics only) | 0 | `census-full.out` |

Frozen registry identity: `sha256 0e9ac687f5e4c6473eb21a546da38c2e4e5eaf10397a5c0ed27cca224d42d388`, 358 lines.

### E11 detail — the only defect in the frozen bytes

`corpus/SOURCES.md:265` (row S256, status `mined`):

```
| S256 | GNU grep(1) manual page — https://man7.org/linux/man-pages/man1/grep.1.html | docs | A | `grep -q` exit semantics: the immediate exit at the first selected line, … | … | mined | … | … | corpus/lessons/round-50.md |
```

Existence probe at both revisions:

```
git cat-file -e 8029cdba…:corpus/lessons/round-50.md   -> ABSENT
git cat-file -e 39e69493…:corpus/lessons/round-50.md   -> ABSENT
```

`corpus/lessons/` at the freeze holds `round-45.md … round-49.md` plus the two verifier spotchecks — no `round-50.md`. So the S256 row is a **forward reference to a file wave 1 has not produced yet**. This is not a fabrication in the registry; it is a live E-code that the freeze's own validator reports. It is fixed by landing `corpus/lessons/round-50.md`, not by editing the S256 row.

Cross-check at the end of my seat: the lane working tree now shows `?? corpus/lessons/round-50.md` (untracked, `git status --porcelain`). A sibling has materialised the file during this wave, which is exactly the discharge this E11 needs — but it is untracked and therefore still absent from every committed revision, so `validate` against any commit still exits 1. The L1 must confirm the committed file exists before the C2 counter or any freeze is taken on the new bytes.

W04 is uniform and benign: 40 rows share a URL with another row under a different scope (e.g. S038/S149/S182 all `man7.org/…/access.2`-family and `mm/oom_kill.c` under distinct scopes). W04 never changes lane status by contract (`sources-census.sh:30-32`).

## (b) Assimilation id-collision guard

Commands (exact, 0–3 leading-space pattern as the round prompt specifies):

```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' <REV>:corpus/SOURCES.md | sed -E 's/^ *\|[[:space:]]*//' | sort -u > reg-ids
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md | sed -E 's/^ *\|[[:space:]]*//' | sort -u > staged-ids
comm -12 reg-ids staged-ids
```

| metric | value |
|---|---|
| `reg-ids` | **256** unique ids, contiguous S001–S256 |
| `staged-ids` | **147** unique ids, contiguous S200–S346 (no internal duplicate ids) |
| **collision count (`comm -12`)** | **57** |
| **first five colliding ids** | **S200, S201, S202, S203, S204** |
| collision range | S200–S256 (57 ids = 256−200+1, exactly the lane's top 57) |
| lane-only ids | 199 (S001–S199) |
| staged-only ids | 90 (S257–S346) |

Receipts: `reg-ids`, `staged-ids`, `collisions` (the 57 ids), `id-collision-compare.txt`.

### The 57 are real collisions, not shared sources

`id-collision-compare.txt`:

```
reg rows: 256 staged rows: 147 collisions: 57
identical source cell: 0 different source cell: 57
  S200 | lane: mount(2) — https://man7.org/linux/man-pages/man2/mount.2.html || staged: mkinitcpio(8) — https://man.archlinux.org/man/mkinitcpio.8
  S201 | lane: Btrfs filesystem ioctl handlers — https://raw.githubusercontent.com/to || staged: alpm-hooks(5) — https://man.archlinux.org/man/alpm-hooks.5
  S202 | lane: errno(3) — https://man7.org/linux/man-pages/man3/errno.3.html || staged: On scripts and hooks (Arch Linux Dev Blog) — https://devblog.archlinux
  S203 | lane: errno(3) — … || staged: Overlay Filesystem (Linux kernel documentation) — https://raw.githubus
  S204 | lane: errno(3) — … || staged: btrfs-subvolume(8) (btrfs-progs) — https://raw.githubusercontent.com/k
```

Zero of the 57 share a `source` cell with the lane row of the same id. A blind append would create 57 E03 (`duplicate id`) findings and silently overwrite the semantics of the lane's S200–S256 block (which includes the round-50 C2 source S256 = grep(1), `corpus/SOURCES.md:265`, and the S200 mount(2) row the boot-plane knowledge cites).

### Secondary guard result — URL duplication after renumbering

`url-duplication.txt`: of the staged package's 147 rows, 108 carry a URL and **39 carry a `corpus/…` path instead of a URL** (first: S230 `Snapper /.snapshots EACCES mechanism … — corpus/knowledge/snapper-eac…`). Of the 108, **10 duplicate a URL already in the lane registry**:

```
staged S201 https://man.archlinux.org/man/alpm-hooks.5      -> lane S008
staged S215 https://man.archlinux.org/man/alpm-package.7    -> lane S227
staged S220 https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btr… -> lane S201
staged S279/S280/S281/S288/S301/S319 https://man7.org/linux/man-pages/man3/errno.3.html -> lane S202,S203,S204
staged S282 https://raw.githubusercontent.com/torvalds/linux/v7.2/incl…    -> lane S205
```

3 of those 10 sit inside the colliding range; **7 sit at fresh ids ≥ S257**. `e04-potential.txt` checks the 7 against the E04 predicate (URL **and** scope):

```
non-colliding staged rows whose URL+scope already exists in lane: 0
```

So renumbering the 57 solves E03 without opening an E04, but the 7 fresh-id URL duplicates remain **semantic** duplicates the L1 must decide on (re-point `used-by` at the existing lane id, or justify a second scope).

## (c) Proof that the guard can fail — 0–3 spaces vs column-zero only

Scratch fixture, `guard2.sh` + `guard-transcript.txt` (deterministic, two demos):

```
### DEMO 1 — staged set = fixture with S002 (item-specified)
staged ids: S002
0-3-space pattern ids: S001 S002 S999
col0-only pattern ids : S001 S999
collisions 0-3 : S002 count=1
collisions col0: count=0

### DEMO 2 — staged set = real append ids (S200..S346), indented row S200
collisions 0-3 : S200 count=1
collisions col0: count=0
```

The registry fixture is a well-formed 3-row registry whose **middle row is written with two leading spaces**:

```
| S001 | fixture row one — https://example.invalid/one | … |
  | S002 | fixture indented row — https://example.invalid/two | … |
| S999 | fixture row three — https://example.invalid/three | … |
```

The 0–3-space pattern captures S001/S002/S999; the column-zero-only pattern (`^\|[[:space:]]*S[0-9]{3,}`) captures only S001/S999, so a collision guard narrowed to column zero reports **0 collisions** while one indented colliding row is present. Demo 2 repeats it with a real staged id (S200) and the real staged set, so the demonstration is not an artefact of a synthetic id.

**The indented row is live, not inert.** The maintained parser accepts 0–3 leading spaces by design (`scripts/sources-census.sh:38-40`: "Maintained parser accepts 0–3 leading ASCII spaces before Markdown rows/headings; 4 or more spaces are indented code and ignored"), and the fixture proves it end-to-end:

```
census --file <fixture>   -> rc=0, file rows 3   (the indented S002 row IS counted)
validate --file <fixture> -> rc=0, file ok …
```

So an indented colliding row passes `validate` clean and is counted by `census`; the collision guard is the **only** control that sees it. Narrowing that guard's pattern to column zero is therefore a silent miss, which is exactly the failure mode this item asks to exclude. (Corroborating: the same script's own selftest exercises `indent-invalid-{0..3}` used-by fixtures at `sources-census.sh:295-336`, i.e. indentation tolerance is a tested property, not an accident.)

## Findings for the L1 (ordered by what blocks what)

1. **BLOCKER for assimilation** — 57 id collisions (S200–S256), 0 with a matching source. The staged package needs renumbering from S257 (staged ids S257–S346 are free) before any append. Guard pattern must stay `^ {0,3}\|[[:space:]]*S[0-9]{3,}`; a column-zero-only pattern is proven to miss an indented collision (demo 1 and 2, count 1 → 0).
2. **E-code in the frozen registry** — `corpus/SOURCES.md:265` S256 `used-by corpus/lessons/round-50.md` dangles at the freeze **and** at the tip. `validate --file corpus/SOURCES.md` therefore exits 1 on the frozen bytes. This is an expected forward reference for a wave-1 artefact, but it must be discharged by landing `corpus/lessons/round-50.md`; if wave 1 does not land it, C2's source row S256 is left with a broken `used-by` and the next round's census inherits the E11.
3. **Semantic duplicates at fresh ids** — 7 staged rows (S279/S280/S281/S282/S288/S301/S319) reuse lane URLs at ids ≥ S257 under different scopes; not E04, but they would double-count sources the lane already mined (errno(3) ×4 against lane S202–S204).
4. **Staged package mixes internal pointers** — 39 of 147 staged rows carry a `corpus/…` path in the `source` cell instead of a URL (S230, S231, S242, S243, S244, …). If appended verbatim these will read as internal rows in a table whose contract is external sources; the L1 should either drop them or restate them with the underlying external URL.
5. **40 W04 warnings** are pre-existing and uniform (same URL, different scope). No action; recorded so the next round does not mistake them for regressions.

## Freshness evidence

| item | observation |
|---|---|
| freeze bytes | `sha256 0e9ac687…` over `8029cdba…:corpus/SOURCES.md`, 358 lines, read via `git archive`/`git show`, not the working tree |
| staged package | `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md`, 178472 bytes, mtime `2026-10-24 23:33:20 -0300` (4 days before the round date 2026-10-28) |
| S256 row | fetched today by the lane: anchor reads `page fetched 2026-10-28T (sha256 d6f0…)` |
| lane tip vs freeze | tip `39e69493…` ≠ freeze `8029cdba…`; all census/collision evidence is from the freeze, and the `round-50.md` absence was checked at both |

## What I did not do

- I did not run `sources-census.sh selftest` or `overdue` — not in this item's authorized command list (C2's counter owns the selftest).
- I did not validate the lane's **working tree** registry, only the freeze revision, per the round rule that the working tree is not the bytes under test.
- I did not modify, add or remove any lane file, and ran no git/jj mutation anywhere: the only git calls were `rev-parse`, `cat-file -e`, `archive`, `show`, `ls-tree`. No fixture repo was needed (no commit was made).
- I did not open the staged package's cited targets; I read `SOURCES.append.md` read-only and ran nothing in shokuknow.
- No tool was installed or upgraded (nothing was needed); no pacman transaction was attempted.
- I did not judge whether the 57 collisions are the L1's intended renumbering plan — that is a planner decision, and I report the measurement only.

## Receipts

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-50/w1/R50ExecCensusSources/`

| file | contents |
|---|---|
| `validate-full.out` | full `validate` over the full-tree freeze extraction (rc=1; 1 E11, 40 W04) |
| `census-full.out` | `census --file` row/tier/status metrics for the freeze registry |
| `reg-ids`, `staged-ids` | the two id sets (256 / 147), `sha256` recorded above |
| `collisions` | the 57 colliding ids, S200–S256 |
| `id-collision-compare.txt` | source-cell comparison: 0 identical / 57 different, with the first 5 side by side |
| `url-duplication.txt` | 108 staged rows with URL, 39 without, 10 URL duplicates vs the lane |
| `e04-potential.txt` | E04 (URL+scope) check on the 7 fresh-id duplicates → 0 |
| `guard-transcript.txt` | demos 1 and 2, plus `census`/`validate` proving the indented row is live |
| `commands.txt` | exact reproduction commands |

Scratch `/fast/scratch/hyaku/tsukuroi-r50/R50ExecCensusSources/` was removed after the receipts were copied; `/fast` had 542 G free at start (33% used).
