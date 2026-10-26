VERDICT: defect-found

The collision check and the guard proof reproduce exactly as declared (226 / 147 / 27, guard 1 vs 0),
and both staged documents map onto the lane rows as the lesson says. The defect is in the provenance of
the two unlabelled assimilation artifacts: `assimilation/reg-ids` (236 ids) and `assimilation/collisions`
(37 ids) sit in the declaration commit whose own `corpus/SOURCES.md` holds 226 rows; they cannot be
derived from the tree that contains them.

Receipts: `.ufo/waves/round-41/w1/AsmCollision/` (id lists, collisions, `guard/`, `doc-map.tsv`,
`doc-map-counts.txt`, `live-man-pages.txt`, `pattern-notes.txt`, `commands.txt`, `BINDING.txt`).
Scratch `/fast/scratch/hyaku/tsukuroi-r41/AsmCollision` was removed after copying; no lane write, no git
mutation, no host change, no counter run.

## 1. Ids and collisions (0-3-space row pattern)

Patterns (recorded in `commands.txt` and `pattern-notes.txt`):

- 0-3-space: `^ {0,3}\|[[:space:]]*(S[0-9]{3})[[:space:]]*\|`
- column-zero control: `^\|[[:space:]]*(S[0-9]{3})[[:space:]]*\|`

| set | source (read-only) | count | range |
|---|---|---|---|
| registry @ base `0e5805a1` | `git show 0e5805a1:corpus/SOURCES.md` (sha256 `108b14d9…be31`) | 226 | S001-S226 |
| registry @ `9cc9aa77` | `git show 9cc9aa77:corpus/SOURCES.md` (sha256 `afcfd949…0676`) | 236 | S001-S236 |
| registry @ tip `71851d63` | same sha256 as above (`afcfd949…0676`) | 236 | S001-S236 |
| staged | `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md` (sha256 `7914d3b9…8406`, 178472 B) | 147 | S200-S346 |

All four sequences are contiguous with no duplicate id (`sort | uniq -d` = 0 each).

Collisions (staged id also a registry id):

- at base: **27**, exactly S200-S226 (`AsmCollision/collisions-base`).
- at `9cc9aa77`: **37**, exactly S200-S236 (`AsmCollision/collisions-c2`); the delta is the ten ids this
  round added, S227-S236 (`comm -13 reg-ids-base reg-ids-c2`).
- non-colliding staged ids: 110, S237-S346.
- document test on the colliding ids: 0 of 27 (base) and 0 of 37 (c2) share a URL with the lane row of the
  same id, and 0 of 37 share a title. So the round-41 lesson sentence "every colliding id names a different
  document in the lane" (`corpus/lessons/round-41.md:53-55`) holds for these pairs.
  Caveat: URL inequality is not a proof of different documents — the S217/S232 pair below is the same
  document under two URLs. The title+URL check is a shape guard, not an identity proof.

My extraction at `9cc9aa77` is byte-identical to the committed `assimilation/reg-ids` and
`assimilation/collisions` (`diff -q` clean), and my base extraction is byte-identical to
`assimilation/reg-ids-base` / `collisions-base`.

## 2. Guard proof

Scratch registry (`AsmCollision/guard/registry.md`):

```
| id | source |
|---|---|
  | S227 | indented scratch registry row |
```

Scratch staged row: `| S227 | staged scratch row |`.

| read | 0-3-space pattern | column-zero pattern |
|---|---|---|
| ids from the scratch registry | 1 (S227) | 0 |
| collisions with the staged row | 1 (S227) | 0 |

Bound control: the same row at four spaces is not captured by the 0-3-space pattern (0 matches) — the
allowance is bounded, `AsmCollision/guard/reg-4sp-0to3`.
Equivalence control on the real files: 226/226, 236/236 and 147/147 rows under both patterns, so the 0-3
allowance widens capture only for indented rows, which do not exist in any of the four files today
(`grep -cE '^ {1,3}\|[[:space:]]*S[0-9]{3}'` = 0 in base, c2, tip and staged).

The loose alternative fails: bare `grep -oE 'S[0-9]{3}'` over the staged file gives 152 unique ids,
because five lane ids are named in staged row bodies — S008 in staged row S201 (`SOURCES.append.md:8`,
"a non-overlapping complement to S008") and S096/S097/S110/S111 in staged row S211
(`SOURCES.append.md:18`, "the lane's existing plymouth rows S096, S097, S110 and S111"). Those five inflate
collisions from 27 to 32 at base and 37 to 42 at c2 (5 spurious collisions; all five ids exist in the lane
registry).

## 3. By-document map for the two staged documents re-opened this round

Full machine-readable copy: `AsmCollision/doc-map.tsv`; counts: `AsmCollision/doc-map-counts.txt`.

| staged id (line) | staged document / URL | lane id (line) | lane document / URL | same document? | same URL? |
|---|---|---|---|---|---|
| S215 (`SOURCES.append.md:22`) | alpm-package(7) — `https://man.archlinux.org/man/alpm-package.7`, `extra/alpm-docs 0.13.0-1` | S227 (`corpus/SOURCES.md:236` @ `9cc9aa77`) | alpm-package(7), `extra/alpm-docs 0.13.0-1` — `https://man.archlinux.org/man/alpm-package.7`, pinned to `alpm-package.7.raw` sha256 `b551bb39…3c45` | **yes** | **yes** |
| S217 (`SOURCES.append.md:24`) | PKGBUILD(5) — `https://man.archlinux.org/man/PKGBUILD.5`, "Pacman 7.1.0, man date 2026-10-15, core/pacman 7.1.0.r9.g54d9411-3" | S232 (`corpus/SOURCES.md:241` @ `9cc9aa77`) | PKGBUILD(5) source at pacman 54d9411 — `https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/doc/PKGBUILD.5.asciidoc`, pinned sha256 `15e8007b…1154` | **yes** | **no** |

Counts: staged rows re-opened 2; lane rows assigned 2; same document 2 of 2; same URL 1 of 2; lane id equal
to staged id 0 of 2 (S215→S227, S217→S232, so no id reuse).

Evidence that the pinned PKGBUILD(5) asciidoc is the document the staged man-page URL renders:

- live `https://man.archlinux.org/man/PKGBUILD.5`, GET 200, accessed 2026-10-26T18:10:32Z, page sha256
  `af56d689…8529`: title `PKGBUILD(5) — Arch manual pages`; located quote "Package information: Package
  name: core/pacman Version: 7.1.0.r9.g54d9411-3"; footer "2026-10-15 Pacman 7.1.0"
  (`AsmCollision/live-man-pages.txt`).
- frozen source `frozen/src/PKGBUILD.5.asciidoc:1-5` reads `PKGBUILD(5)` / `PKGBUILD - Package build
  description file`; sha256 matches `frozen/src/SHA256SUMS:1` (`15e8007b…`).
- live `https://man.archlinux.org/man/alpm-package.7`, GET 200, accessed 2026-10-26T18:10:33Z, page sha256
  `05ce740e…57b1`: title `alpm-package(7) — Arch manual pages`; quote "Package information: Package name:
  extra/alpm-docs Version: 0.13.0-1" — the same package and version as lane S227 and staged S215.
- `frozen/src/alpm-package.7.raw:1-6` is the troff rendering (`.TH "" "7" ""`; NAME "package - a package
  based on Arch Linux ALPM concepts"), sha256 `b551bb39…` matching the lane row.

`curl` to the same URLs failed with `TLS connect error: … unexpected eof while reading` (rc 35); the GETs
above were made with Python `urllib` (200). Recorded, not hidden.

## 4. Defect: declaration-commit artifacts are bound to a later tree

`assimilation/reg-ids` and `assimilation/collisions` were committed in `d8b4d521` (the only commit touching
`assimilation/`, `git log --oneline -- .ufo/waves/round-41/assimilation` = one line). That commit's own
registry holds 226 rows and contains no S227/S236 row:

```
$ git show d8b4d521:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3}[[:space:]]*\|'
226
$ git show d8b4d521:corpus/SOURCES.md | grep -c '^| S227 '   -> 0
$ git show d8b4d521:corpus/SOURCES.md | grep -c '^| S236 '   -> 0
$ git show d8b4d521:.ufo/waves/round-41/assimilation/reg-ids | wc -l          -> 236 (last S236)
$ git show d8b4d521:.ufo/waves/round-41/assimilation/collisions | wc -l       -> 37 (S200..S236)
```

They match, byte for byte, what the registry yields at `9cc9aa77` (S227-S236 added in `c7c40c0f`), so they
were computed against a working tree that already carried the C2 rows, then committed with the declaration
before those rows were committed. Consequence: at the declaration commit the "current" collision picture is
an after-C2 number sitting in a before-C2 tree, and `reg-ids`/`collisions` are unreproducible from their own
revision. The lesson's collision paragraph cites only `reg-ids-base`/`staged-ids`/`collisions-base`
(226/147/27, all reproducible), so no declared number is wrong; the fix is to label or regenerate the two
unlabelled files against `9cc9aa77`.

## 5. Secondary finding: document-level overlap is larger than the id collision count

Keying collisions on ids understates the overlap, because the same document can be staged under a
non-colliding id. Of the 111 staged rows that carry a URL, 10 have a URL already present in the lane at
`9cc9aa77` (`AsmCollision/doc-map-counts.txt`):

| staged | document | lane | note |
|---|---|---|---|
| S201 (`:8`) | alpm-hooks(5) | S008 (`corpus/SOURCES.md:14`) | same title, same URL |
| S215 (`:22`) | alpm-package(7) | S227 (`:236`) | this round's intentional re-open |
| S220 (`:27`) | Btrfs filesystem ioctl handlers (`fs/btrfs/ioctl.c` v7.2) | S201 (`:210`) | same title, same URL |
| S279, S280, S281, S288, S301, S319 | errno(3) (`man7.org/…/errno.3.html`) | S204 (`:213`) | same title, same URL, six staged rows |
| S282 (`:89`) | asm-generic/errno-base.h | S205 (`:214`) | same title, same URL |

So a merge keyed on ids would still append nine already-held documents in addition to the one deliberate
re-open; the by-document map, not the id intersection, is the merge-safe check.

## 6. Not done / limits

- No counter, census, selftest, build, lint or test was run — outside this item and owned by other seats.
- No lane content written; the only lane writes are this report and `w1/AsmCollision/`. The lane's
  pre-existing dirty paths (`M tools/check-self-assessment.py`, untracked `w1*` files) were not touched.
- Live pages were read; the frozen snapshot is the evidence for the lane anchors, and no claim here rests on
  a page I did not fetch.
