VERDICT: supports

# C2-29 — `list_package_files` order measured (PA3, empirically)

Item C2-29. Hypothesis under test: makepkg's `list_package_files` lists `.BUILDINFO .INSTALL .MTREE
.PKGINFO` before `usr/...` and before data dirs named `A` or `_x`; and: does any legal top-level name
sort before a dot file under `LC_COLLATE=C`, i.e. does PA3's "dot files sort ahead of the data files"
need a condition?

Short form: the hypothesis holds on this host; the *mechanism* is a C-collation byte sort of the full
paths, not a dotglob special case; 15 legal top-level first-byte classes measured below `'.'` (0x2E)
do sort ahead of the four metadata members; PA3's tail clause "the metadata sits at the beginning of
the archive" therefore needs the first-byte condition, and the four-metadata-head statement needs no
other top-level dot file ahead of `.BUILDINFO` either.

## Source under test (verified)

- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-41/frozen/src/makepkg.sh.in`
  sha256 `d588222586b2432b4169c82e6ebcd464acfdc20a663172fd444b8f98e1104e86`, `sha256sum -c SHA256SUMS`
  → `makepkg.sh.in: OK` (all nine frozen files OK).
- Body, verbatim: `:562-569` — `list_package_files() { ( export LC_COLLATE=C; shopt -s dotglob
  globstar; printf '%s\0' **/* ); }`; the comment above it at `:558-561` says "build a sorted
  NUL-separated list … database files are placed at the beginning of the package regardless of
  sorting". Consumers: `:617` (.MTREE) and `:625` (archive), both
  `| LANG=C bsdtar … --null --files-from -`.
- Corpus claim: `corpus/knowledge/alpm-package-anatomy-r41.md:28` (PA3); source row
  `corpus/SOURCES.md:238` (S229, window "`list_package_files` lines 560-569").
- Host tools: `/usr/bin/bash` `GNU bash, version 5.3.20(1)-release` (makepkg's shebang is
  `#!/bin/bash`, `makepkg.sh.in:1`); `bsdtar 3.8.10 / libarchive 3.8.10`; glibc 2.44;
  `LANG=en_US.UTF-8`, `LC_COLLATE` unset in the environment.

Method: every measurement ran in a script file under `/fast/scratch/hyaku/tsukuroi-r41/C2LabratOrder/`
driven by `/usr/bin/bash` (bash 5.3.20); no lane file was modified; no host state touched. The exact
body was used as the function, both as `%s\0` (as shipped) and as `%s\n` (the assignment's literal
form) — identical order, see `receipt.out` and `lab_body.sh` in the receipts dir.

## 1. The requested fixture — hypothesis holds

Tree: `.BUILDINFO` `.INSTALL` `.MTREE` `.PKGINFO` `usr/bin/hello` `A/data` `_x/f` `Zeta/g`.
Body output (`%s\0`, rendered per line; `receipt.out` §1):

```
 1 .BUILDINFO   2 .INSTALL   3 .MTREE   4 .PKGINFO
 5 A            6 A/data     7 Zeta     8 Zeta/g
 9 _x          10 _x/f      11 usr     12 usr/bin  13 usr/bin/hello
```

So the four dot files precede `usr/...`, `A` and `_x`, and the order is exactly the C byte order of the
names: `.BUILDINFO < .INSTALL < .MTREE < .PKGINFO < A < A/data < Zeta < Zeta/g < _x < _x/f < usr`.
`od -c` of the NUL stream shows plain names with no `./` prefix and no trailing slash (`receipt.out` §1
second block); directories are listed *as members* (`A`, `usr`, `usr/bin`), and bsdtar adds the
trailing `/` at archive time (`receipt.out` §5). 40-byte `od` sample:
`.BUILDINFO\0.INSTALL\0.MTREE\0.PKGINFO\0A\0A/data\0Zeta\0Zeta/g\0_x\0_x/f…`.

## 2. Byte-order answer — yes, legal top-level names sort before a dot file

`'.'` is 0x2E. On this filesystem only NUL and `/` are excluded from a filename, so any top-level name
whose first byte is in 0x01–0x2D precedes `.BUILDINFO`. Measured with real files (treeB; first 22
entries, `%q`, from `treeB.order.txt` / `receipt.out` §2):

```
 1 $'\ttabname'       byte=9
 2 $'\nnewname'       byte=10
 3 \ spaces           byte=32
 4 \!bang  5 \"dq  6 \#hash  7 \$dollar  8 %pct  9 \&amp 10 \'quote
11 \(open 12 \)close 13 \*star 14 +plus 15 \,comma 16 -dash          (33..45)
17 .BUILDINFO  18 .INSTALL  19 .MTREE  20 .PKGINFO                   (46)
21 0digit  22 9nine  23 \;semi  24 =eq  25 @at  26 A  27 A/data  28 Zeta  29 Zeta/g
30 \^caret  31 _x  32 _x/f  33 \`tick\`  34 usr  35 usr/bin  36 usr/bin/hello  37 \~tilde
```

15 distinct top-level first-byte classes below `'.'` were materialised (tab, newline, space, and
`! " # $ % & ' ( ) * + , -`); all 15 come first, `.BUILDINFO` is 17th. `+` (0x2B) and `-` (0x2D) behave
as the item predicted. So the answer is **yes**, and PA3's "dot files sort ahead of the data files"
cannot be left unqualified for arbitrary legal names.

The body also *totals* to the byte sort of the same names, NUL-safe compared:
`LC_ALL=C sort -z` of the body stream `cmp`-identical to the body stream (`IDENTICAL`, `receipt.out`
§2) — i.e. the sort applies to the full path, and dotglob is not a separate "dot files first" rule.

## 3. The mechanism (treeD): byte sort of full paths, not a per-directory walk

Root: `.PKGINFO`, dir `A` with child `b`, files `A-b`, `A.b`. Body order (`receipt.out` §3):

```
1 .PKGINFO  2 A  3 A-b  4 A.b  5 A/b  6 A/b.c
```

A per-directory grouped walk would have produced `.PKGINFO A A/b A-b A.b`; the observed interleaving is
the full-path byte order (0x2D `-` < 0x2E `.` < 0x2F `/`). This is a bash 5.3.20 property, and PA3's
root-level conclusion does not depend on it: a per-directory walk still sorts root entries among
themselves first, so root-level dot files still precede root-level `A`/`_x`/`usr`.

## 4. `LC_COLLATE=C` is load-bearing (supports the clause)

Same treeA glob without the in-function export, under the host's `LANG=en_US.UTF-8` (glibc collation
ignores punctuation at the primary level): `A, A/data, .BUILDINFO, .INSTALL, .MTREE, .PKGINFO, usr,
usr/bin, …` (`receipt.out` §4). The four dot files drop below `A`. So the export at `makepkg.sh.in:564`
is the reason the metadata leads, and the host's own default locale would not produce PA3's order.

## 5. End-to-end: archive head, and the package still loads

Built a scratch package with the exact `create_package` commands (`:617-620` mtree, `:625-626`
bsdtar|zstd) over a tree containing a top-level file `-dash` and dir `-lib/` (treeE; `lab_pkg.out`,
`receipt.out` §5). Archive member order:

```
1 -dash  2 -lib/  3 -lib/child  4 .BUILDINFO  5 .INSTALL  6 .MTREE  7 .PKGINFO
8 A/  9 A/data  10 _x/  11 _x/f  12 usr/  13 usr/bin/  14 usr/bin/hello
```

The metadata is no longer at the beginning. The `.MTREE` is still well formed and still excludes itself
(`grep -c MTREE` in `zcat .MTREE` = 0; entries `./-dash`, `./.BUILDINFO`, …; control/space names are
escaped by bsdtar as `./\011…`, `./\012…`, `./\040…`). Read-only queries on that package
(`--dbpath` in scratch) all succeed: `pacman -Qp …` → `demo 1-1` rc=0; `pacman -Qip …` prints the full
info block rc=0; `pacman -Qlp …` (full load via `.MTREE`) → `demo /-dash`, `demo /-lib/`, …,
`demo /usr/bin/hello` rc=0. This matches `be_package.c:595-644`: the load loop scans headers until
`.PKGINFO` (so leading data members are harmless; the break at `:641` happens on the first entry after
`.PKGINFO`), and `handle_simple_path` (`:373-385`) skips every dot file when building the file list
regardless of position. The inversion is therefore a *layout/diagnostic* fact, not a load failure.

## 6. Does PA3 need a condition? — yes, on the first byte

- The row's existing clamp ("whose names begin with a letter, a digit or an underscore") is true for
  exactly those classes (measured: `0digit`, `9nine`, `A`, `_x`, `usr` all after `.PKGINFO`), but it is
  an enumeration of convenient cases, not the predicate that the code gives. The predicate is the
  first byte: `≥ 0x2E` for every top-level name.
- The clause "and the metadata sits at the beginning of the archive" is stated unconditionally; it is
  false for a legal top-level name beginning with a space, a control byte, or punctuation below `.`
  (`! " # $ % & ' ( ) * + , -`), as §5 shows with `-dash`.
- Even among dot files, the four metadata members are the first four only if no other top-level dot
  file sorts ahead of `.BUILDINFO` (e.g. `.AAA`, `.-x`); a stray `.Z` sorts after `.PKGINFO` and keeps
  them at positions 1–4. Worth stating once if the row wants "the four dot files come first" rather
  than "dot files lead the data files".
- Scope note for the entry's diagnostic table (`alpm-package-anatomy-r41.md:44`, "the first members
  should be the dot files"): with a below-`.` name the metadata is still the leading *dot* members, just
  not the first members — the check should read on the metadata being at the head of the dot-file
  group, not on member 1.

### Proposed replacement text (PA3 rule cell, `corpus/knowledge/alpm-package-anatomy-r41.md:28`)

> makepkg lists package files with `LC_COLLATE=C` and bash `dotglob`, and the list is a byte-order sort
> of the full paths, so the dot files sort ahead of every data file whose first byte is `.` (0x2E) or
> above — a letter, a digit or an underscore — and the metadata sits at the beginning of the archive; a
> legal top-level name whose first byte is below `.` (a space, a control byte, or punctuation such as
> `!`, `+`, `-`, `,`) sorts ahead of the metadata, so the head-of-archive guarantee is on the first
> byte and not on `dotglob`; a load that is partial stops reading at the end of the first archive entry
> after `.PKGINFO` has been parsed

Value cell `LC_COLLATE=C dotglob` and source cell S229 (`makepkg.sh.in:560-569`) are unchanged. The
host cell stays as it is: my package is a scratch fixture, not a host capture of installed packages, so
it does not turn PA3's "unmeasured" host value into a host observation.

## Retained evidence

Seat dir `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-41/w1/C2LabratOrder/`:

- `receipt.out` — consolidated run: fixture orders, NUL-safe byte comparison, byte table, locale
  sensitivity, archive order, mtree self-exclusion (bash/bsdtar/glibc versions on line 1–2).
- `treeB.order.txt` — the 37-entry full order with `%q` names.
- `lab_pkg.out` — end-to-end: archive order, `.MTREE` head, `pacman -Qp/-Qip/-Qlp` output and rcs.
- `lab_body.sh`, `lab_receipt.sh`, `lab_pkg.sh`, `lab_order.sh`, `lab_sort.sh` — the runnable scripts
  (each takes the scratch root as `$B`/argument; no host writes inside).

Scratch `/fast/scratch/hyaku/tsukuroi-r41/C2LabratOrder/` was removed after copying; nothing was built
under `/tmp`. No tools were installed or upgraded for this item.

## Not run / limits

- Nothing was installed, removed or restored: no `pacman -U`, no transaction, no service or `/etc`
  touch. `pacman -Qkk` was not run (it needs a local-db entry for an installed package); the `-Qp`
  family was run only against the scratch package with `--dbpath` inside scratch.
- Only bash 5.3.20 (host `/usr/bin/bash`) was measured. The bash 5.2 ordering split I did not test —
  no 5.2 binary exists on the host, and the harness's inline interpreter (`BASH_VERSION` 5.2.37) is
  not a usable stand-in: it reports `globstar on` yet expands `**/*` as `*/*` (4 entries in treeA, no
  dot files, no recursion), reproducibly. Every number here comes from `/usr/bin/bash`; a reader who
  runs these globs through the harness's inline shell will get a false "no dot files" result.
- No real `makepkg` run: the `create_package` commands were replayed by hand (`create_package:605-626`);
  fakeroot was not involved, which does not affect glob order.
