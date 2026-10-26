VERDICT: defect-found

# AsmCollision — Item A-1, §10 id-collision guard re-run

Scope: re-run the §10 id-collision check (`/home/vgpnk/Projects/shokunin/.ufo/prompts/tsukuroi-round-39.md:492-515`) myself in scratch, prove the 0–3-space guard on a **census-valid** fixture holding a real staged id, compare with the L1's `.ufo/waves/round-39/assimilation/`, and re-derive the quarantine slice (`:536-543`) plus its intersection with the ids the round-39 entry cites.

Headline: **the guard holds (proven below), but the L1's committed collision evidence is stale against its own pinned dispatch tip** — it records 13 collisions where the pinned registry yields 19, and its guard fixture is not a census-valid registry, so it proves regex reach only.

## 1. Inputs, pinned

| input | identity | rows |
|---|---|---|
| `corpus/SOURCES.md` at `2e1c2a40c13dc52e155d89e72f3fdd560db7399a` (dispatch tip) | `git show` blob sha256 `c2e4598670c50a69a5694b616928f7011199ea1be2dcae73b9b7c440540af34e` | 218 |
| same file in the working tree / at `HEAD` `394e1ba4` | identical sha256; `git status --porcelain corpus/SOURCES.md` empty; `git diff --stat 2e1c2a40 HEAD -- corpus/SOURCES.md` empty | 218 |
| `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md` | read-only source | 147 |

Receipts: `.ufo/waves/round-39/w1/AsmCollision/compare/SOURCES.pre-C2.md`, `urls/reg.rows`, `urls/staged.rows`.

## 2. The check, re-run (scratch `/fast/scratch/hyaku/tsukuroi-r39/AsmCollision/`)

Exactly the prompt's extractor (`grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` → `grep -oE 'S[0-9]+'` → `sort` → `comm -12`), run on the `2e1c2a40` blob:

```
reg-ids:     218 lines  S001 … S218   (gapless, duplicate-free)
staged-ids:  147 lines  S200 … S346   (gapless, duplicate-free)
collisions:   19 lines
```

Both lists (compact form; both verified consecutive and duplicate-free by an awk gap scan — `last=218, count=218` / `last=346, count=147`):

- **reg-ids**: `S001 S002 … S218` — every integer 1–218 present exactly once (`rerun/reg-ids`).
- **staged-ids**: `S200 S201 … S346` — every integer 200–346 present exactly once (`rerun/staged-ids`).

`rerun/collisions` (verbatim):

```
S200
S201
S202
S203
S204
S205
S206
S207
S208
S209
S210
S211
S212
S213
S214
S215
S216
S217
S218
```

**Collision count: 19.** No staged id above S218 collides (registry max is S218, staged min is S200, so the collision set is exactly `S200–S218 ∩ staged`).

Both files today are column-zero: `grep -cE '^ {1,3}\|[[:space:]]*S[0-9]{3,}'` returns `0` for the registry and `0` for the staged file. So indentation changes neither list **today** — it is a latent false-green, which is what the guard proof has to close.

## 3. Guard proof (mine — census-valid fixture, real staged id)

Fixture = a complete registry: `## Registry` heading, the 11-column header, the separator, one normal row `S001`, and **one indented row carrying staged id `S300`** (`guard/SOURCES.indent<N>.md`, `<N>` leading spaces). Real staged set from `shokuknow` is the comm operand throughout (`guard/staged-ids`).

| indent | `sources-census.sh census --file` rows | `sources-census.sh validate --file` | `collisions` with `^ {0,3}\|` | `collisions` with `^\|` (column-zero) |
|---|---|---|---|---|
| 0 | 2 | `file ok`, exit 0 | S300 | S300 |
| 1 | 2 | `file ok`, exit 0 | **S300** | **empty** |
| 2 | 2 | `file ok`, exit 0 | **S300** | **empty** |
| 3 | 2 | `file ok`, exit 0 | **S300** | **empty** |
| 4 | **1** (row not a registry row) | `file ok`, exit 0 | empty | empty |

`guard/guard-proof.txt`, `guard/census-rows.txt`. Reads: at every indentation the census parser itself counts (0–3 — `scripts/sources-census.sh:614-616` gates and strips `^ {0,3}`, and its own selftest sweeps widths 0–3 at `:287-339`), the prompt's extractor catches the staged id and the column-zero pattern misses it. At 4 spaces the row is **not** a registry row for the census either, so extractor and parser agree on the contract boundary — no false green in either direction. The guard is not broken; the 0–3 pattern is the correct one and is the one I used.

## 4. Comparison with `.ufo/waves/round-39/assimilation/`

| artifact | L1 | mine | relation |
|---|---|---|---|
| `staged-ids` | 147 lines | 147 lines | `diff` empty — identical |
| `reg-ids` | 212 lines, `S001–S212` | 218 lines, `S001–S218` | L1 set is **byte-identical to the `4078eb2^` state** (`compare/reg-ids.L1` vs `compare/reg-ids.pre-C2`, `diff` empty) |
| `collisions` | 13 lines, `S200–S212` | 19 lines, `S200–S218` | delta `S213 S214 S215 S216 S217 S218` (`compare/collisions.delta`) |
| `guard-proof/SOURCES.md` | 3 lines, 2-column header `| id | t |`, one indented `| S200 | indented fixture row |` | census-valid fixture, staged id `S300` | L1 fixture is **not a census-valid registry** |

Why the L1 set is stale — timing, not arithmetic:

- `git log -1 --format=%ci 4078eb2` → `2026-10-26 02:59:39 -0300` (the C2 commit that appended `S213–S218`); `2e1c2a4` → `03:00:47 -0300` (dispatch tip, 68 s later). Row counts per revision: `4078eb2^` → 212, `4078eb2` → 218, `2e1c2a40` → 218, `HEAD` → 218.
- The L1's `assimilation/*` files are stamped `02:50` (`ls -la .ufo/waves/round-39/assimilation/`), i.e. nine minutes **before** the lane's own C2 registry append, and were never regenerated against the pinned dispatch tip. `4078eb2` is an ancestor of `2e1c2a40` (`git merge-base --is-ancestor 4078eb2 2e1c2a40` → exit 0).

L1 guard fixture, measured: `sources-census.sh census --file assimilation/guard-proof/SOURCES.md` → `file rows 0`; `validate --file` → `file E12 S200 row outside Registry section`, exit 1 (transcript in `compare/l1-guard-fixture/`). It proves the regex sees an indented S-row in a non-registry file; it does **not** prove the guard against a row the census accepts as a registry row.

Consequence, stated plainly: **nothing was wrongly appended.** The registry rows `S213–S218` are C2's own-work libalpm rows, not adoptions of staged `S200+` rows, so no staged document was shadowed. What is defective is the *evidence file*: it understates the collision set by exactly the six ids the same wave added, and no counter covers `assimilation/` so nothing flagged it.

## 5. Renumber map

**None applied** — this round adopts nothing from the package, so no staged row needs an id. Findings that bind any future adopting round:

- **0 of 19** colliding staged ids may keep its id: each colliding staged id names a *different document* than the registry row at that id (`rerun/collision-map.txt`, spot values below). A shift-by-one map would break every citation (the prompt's own fleet lesson), so the map must be document-keyed.
- Next free lane id: **S219** (registry gapless to S218).

```
staged S208  Snapper（Arch Linux 中文维基）wiki.archlinuxcn.org/zh-hk/Snapper
             vs registry S208  libalpm hook.c @54d9411
staged S211  plymouth release tags (GitLab API)
             vs registry S211  libalpm alpm.c @54d9411
staged S213  Oracle Linux 8 Btrfs, Snapper 日本語 docs.oracle.com/cd/F22978_01/...
             vs registry S213  libalpm add.c @54d9411   <-- entry cites this id
staged S217  PKGBUILD(5) man.archlinux.org/man/PKGBUILD.5
             vs registry S217  libalpm trans.c @54d9411
staged S218  SLES 15 SP7 storage guide, filesystem overview
             vs registry S218  round-39 host transaction capture (own-work)
```

Full 19-row table: `rerun/collision-map.txt`.

Adjacent, and it constrains adoption too: 4 URLs already in the registry, so those staged rows would trip census `E04` (duplicate URL within scope) rather than a bare id clash — `urls/url-overlap`:
`man.archlinux.org/man/alpm-hooks.5` (reg S008 ↔ staged S201), `man7.org/linux/man-pages/man3/errno.3.html` (reg S202–S204 ↔ staged S279, S280, S281, S288, S301, S319), `raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/ioctl.c` (S201 ↔ staged S220), `.../include/uapi/asm-generic/errno-base.h` (S205 ↔ staged S282).

## 6. Quarantine slice re-derived (`prompt:536-543`)

`awk -F'|' -v l='tsukuroi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}'` on `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` → **12 data rows** (`quarantine/quarantine-slice`, ids in `quarantine/slice-ids`):

```
S211  payload-absent
S213  payload-absent
S225  the cited source could not be fetched, so no quote was checked
S230  the gate block named no locator, so no quote was checked
S231  the gate block named no locator, so no quote was checked
S242  the gate block named no locator, so no quote was checked
S243  the gate block named no locator, so no quote was checked
S244  the gate block named no locator, so no quote was checked
S249  the gate block named no locator, so no quote was checked
S250  the gate block named no locator, so no quote was checked
S251  the gate block named no locator, so no quote was checked
S252  the gate block named no locator, so no quote was checked
```

Two register defects reproduced (both already warned about in the prompt, now measured): the `## By lane` summary reads `| `tsukuroi` | 2 |` (`absent-defect-register.md:253`) against 12 data rows — stale, so the slice must be derived, never read; and the id cell of the ten "no locator" rows is malformed, the id glued to the class cell's opening backtick (raw `S230`` — `absent-defect-register.md:366-375`), so `$4` carries a backtick that must be stripped before any join. `quarantine/slice.tsv` carries the cleaned `id\tclass\tsource`.

**Intersection with the ids the round-39 entry cites.** Entry `corpus/knowledge/pacman-transaction-order-r39.md:1` cites `S208, S213, S214, S215, S216, S217, S218` (`quarantine/cited-ids`); intersection = **`S213`** (`quarantine/intersection`).

That single id is a **false friend across two id spaces**, and the report should say so before anyone quarantines the round's entry:

- The register's id space is the campaign's staged-id space. Register `S213` URL `https://docs.oracle.com/cd/F22978_01/btrfs/btrfs-UsingtheSnapperUtilityWithBtrfsSubvolumes.html` == staged `S213` source URL (`SOURCES.append.md:20`, Oracle Snapper 日本語) — same document, same id. Register `S211` (plymouth tags) == staged `S211` (`:18`) likewise. All 12 slice ids map 1:1 onto staged rows by document (`quarantine/slice-staged-map.tsv`).
- The lane registry's `S213` is a different document entirely: `corpus/SOURCES.md:222` = libalpm `add.c` at pacman `54d9411`, the C2 row the round-39 entry cites and the counter verifies against the frozen snapshots.

So: the entry's `S213` is **not** quarantined; and the quarantined campaign row `S213` is, separately, **unadoptable at its own id** because lane `S213` is already occupied — a double blocker on one string.

## 7. Proposed text (L1 record repair)

Replace `.ufo/waves/round-39/assimilation/collisions` with the 19 lines in `rerun/collisions` and `reg-ids` with the 218-line `rerun/reg-ids` (both pinned at `2e1c2a40`), swap `assimilation/guard-proof/` for `w1/AsmCollision/guard/` (census-valid, real staged id), and carry this line in the round-39 lesson's `## Gate` block:

```
Id collision: 19 (S200–S218) against corpus/SOURCES.md at 2e1c2a40 (was recorded as 13 before the
round's own S213–S218 append); 0 of the 19 may keep its id — every colliding staged id names a
different document than the registry row at that id, so any adoption is document-keyed from S219
upward, never arithmetic; 4 staged URLs already sit in the registry (E04 risk). Guard proven on a
census-valid fixture at indent 0–3 (column-zero pattern empty, 0–3 pattern catches the staged id;
census counts 2 rows at 0–3 and 1 at 4 spaces). Adoption closed this round → no renumber applied.
```

## 8. Evidence retained

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-39/w1/AsmCollision/`
- `rerun/` — `reg-ids` (218), `staged-ids` (147), `collisions` (19), `collision-map.txt` (19 rows, staged vs registry document).
- `guard/` — `SOURCES.indent{0..4}.md`, `reg03.*`, `reg00.*`, `collisions03.*`, `collisions00.*`, `staged-ids`, `guard-proof.txt`, `census-rows.txt`.
- `compare/` — `reg-ids.L1`, `reg-ids.pre-C2`, `collisions.L1`, `collisions.delta` (`S213–S218`), `SOURCES.pre-C2.md`, `l1-guard-fixture/`.
- `quarantine/` — `quarantine-slice` (verbatim prompt awk output), `slice.tsv`, `slice-ids`, `cited-ids`, `intersection` (`S213`), `slice-staged-map.tsv`.
- `urls/` — `reg.rows`, `staged.rows`, `reg.urls`, `staged.urls`, `url-overlap` (4).

Scratch `/fast/scratch/hyaku/tsukuroi-r39/AsmCollision/` removed after copying (nothing under `/tmp` was used as evidence).

## 9. What I did not do

- I judged **no** TO row, so I append no `TO<n>:` line — the C2 kill rule is not in play for this seat.
- No hand-check of the 12 quarantined payloads: adoption is closed this round by construction (nothing appended from the package), so the slice's rows stay refused; a future adopting round owes each row a fetch-and-locate.
- No network fetch, no census run against the lane (`--root` gate is not my item), no lane file written outside my report and seat dir, no git/jj mutation.
- Tools installed/upgraded: **none** (nothing needed; `git`, `coreutils`, `gawk` and the lane's `sources-census.sh` sufficed).

## 10. Risks

1. A future adopting round reading only `assimilation/collisions` would believe 13 ids are blocked and could assign `S213–S218` to staged rows — colliding a second time with libalpm `add.c`/`sync.c`/`remove.c`/`util.c`/`trans.c` and the round-39 capture.
2. The campaign register and the lane registry share the `Snnn` string space with different meanings; any join not mediated by URL/document will mis-quarantine (my `S213` case) or miss a quarantine.
3. Nothing automated covers `assimilation/` staleness — the round's counters score `before`/`after` receipts only, so this class of drift is invisible unless a seat re-runs it.
