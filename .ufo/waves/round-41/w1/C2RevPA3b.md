VERDICT: partly
ROW: PA3
lines checked: frozen/src/makepkg.sh.in:558-569
also read: frozen/src/makepkg.sh.in:582-634 (`create_package`: pkgdir, `.PKGINFO`/`.BUILDINFO`/`.INSTALL`/`.CHANGELOG` writes, the mtree call and the archive call), :636-663 (`create_debug_package`), :665-749 (`create_srcpackage`), :855-864 (`run_single_packaging`); frozen/src/be_package.c:373-385 (`handle_simple_path`), :560-700 (`_alpm_pkg_load_internal`, loop :595-644)
pinned: `.ufo/waves/round-41/frozen/src/` — `sha256sum -c SHA256SUMS` → 9/9 `OK` (makepkg.sh.in, be_package.c included)
seat: C2RevPA3b (second, adversarial verdict), item C2-3b

# What survived

The row's substance is stronger than I expected, and I could not break it by any route that changes
the listed artefact: the two named settings are the ones that decide the sort, `LC_COLLATE=C` is
load-bearing rather than incidental, and the archive really does carry the metadata first. Evidence,
all produced under `/fast/scratch/hyaku/tsukuroi-r41/C2RevPA3b/` (receipts in `.../w1/C2RevPA3b/`):

1. **The settings are at the cited lines, all three of them.** `makepkg.sh.in:564` `export LC_COLLATE=C`,
   `:565` `shopt -s dotglob globstar`, `:567` `printf '%s\0' **/*`, comment at `:558-561` "database files
   are placed at the beginning of the package regardless of / sorting". The listing feeds both consumers
   (`:617` mtree, `:625` archive); `create_debug_package` reaches the same `create_package` (`:662`),
   `run_single_packaging` likewise (`:864`), and `create_srcpackage` uses the same listing (`:737`), so no
   caller bypasses it for a binary package.
2. **Dot-first is caused by `LC_COLLATE=C` and not by anything else.** Control matrix on a fixture pkgdir
   (`01-glob-control-matrix.txt`, host bash 5.3.20): with `LC_COLLATE=C` the order is
   `.BUILDINFO .CHANGELOG .INSTALL .MTREE .PKGINFO .config 0digit 0digit/file Zebra _under … apple usr …`
   — every dot name ahead of every name starting with a digit (48), an upper letter (90), `_` (95) or a
   lower letter (97). The same glob with `LC_COLLATE=en_US.utf8` puts `0digit`, `0digit/file` and `apple`
   *before* `.BUILDINFO` — i.e. the row's attribution to `LC_COLLATE=C` is exact, and without it the
   metadata would not lead.
3. **bsdtar preserves the list order, so "the metadata sits at the beginning of the archive" holds.**
   `list_package_files | LANG=C bsdtar --no-fflags -cnf - --null --files-from -` yields members 1-5
   `.BUILDINFO .CHANGELOG .INSTALL .MTREE .PKGINFO` (`02-archive-member-order.txt`, 19 members, order
   identical to the glob; no re-sorting, no `./` prefix — the names are stored as `.PKGINFO`, which is
   what the `strcmp` at `be_package.c:598` needs).
4. **Host corroboration of the ordering (not of the archive):** the local `mtree` is written from the
   same listing (first call, `:617`), so its member order is the glob order minus `.MTREE`. The samples
   begin `./.BUILDINFO`, then `./.INSTALL` where the package has one, then `./.PKGINFO`, then the data
   tree (`./opt…`, `./usr…`) — `04-host-mtree-order.txt`; `bash-5.3.20-1` carries all three in byte
   order (`B` < `I` < `P`), as the row implies. This does not upgrade
   the row's host cell (it stays "unmeasured" for archive order) and I did not create a package file.

What does not survive is the **second clause's stated rule** and one **missing word in the mechanism**.

# Counterexample 1 — the partial load does not stop after the entry *following* `.PKGINFO`; it stops after the first entry that is not `.`-prefixed

`be_package.c:598-618` parses `.PKGINFO` and then `continue`s (`:617` `config = 1;`, `:618` `continue;`) —
it does not break. The break sits at the loop bottom (`:641-643` `if((!full || hit_mtree) && config) { break; }`)
and is only reached by an entry that falls through the chain at `:598/:619/:625/:627`. Every `.`-prefixed
name is swallowed one rung earlier:

```
373:static int handle_simple_path(alpm_pkg_t *pkg, const char *path)
378:	} else if(*path == '.') {
379:		/* for now, ignore all files starting with '.' that haven't
380:		 * already been handled (for future possibilities) */
381:		return 1;
```
with the call site at `:625` `} else if(handle_simple_path(newpkg, entry_name)) {` / `:626` `continue;`.

So the code's rule is "break after the first entry after `.PKGINFO` that is not `.`-prefixed, or at EOF".
The row says "the first archive entry after `.PKGINFO` has been parsed". The two coincide only when the
successor is a data entry. A root-level dot file whose name sorts after `.PKGINFO` (`'c' > 'P'`) is
produced by the same listing I verified in (2): `.config` at member 6. Mirroring `:595-644` over that
member list (`03-partial-load-sim.txt`):

```
stopped after entry 7 = 0digit/
consumed by the partial load: ['.BUILDINFO', '.CHANGELOG', '.INSTALL', '.MTREE', '.PKGINFO', '.config', '0digit/']
```
The row predicts the stop after `.config`; the load also reads `.config` and stops one entry later.
Two further shapes of the same gap: `.PKGINFO` last → the loop ends at `ARCHIVE_EOF` and `break` is
never executed (`config` is already 1, so the load still succeeds), and `.PKGINFO` followed only by
dot files → the stop is at EOF, described by the row only by accident.

Materiality: zero of the 1409 mtrees on this host carry a root-level non-metadata dot entry
(`for f in /var/lib/pacman/local/*/mtree; do zcat "$f"; done | grep -cE '^\./[!-,]'` → `0`; the
non-metadata dot scan returned `root-level non-metadata dot entries=0` for `mtrees scanned=1409`), so
for every package installed here the row's sentence and the code agree. The clause is wrong as a
statement about libalpm, not wrong about this host.

# Counterexample 2 — the mechanism names two of the three settings that make the listing work

`makepkg.sh.in:565` is `shopt -s dotglob globstar`. The row names `dotglob` and omits `globstar`, yet
without `globstar` the listing is not a listing at all: `**` degenerates to `*`, so `**/*` is `*/*` —
one level deep, every top-level name (the metadata included) gone. Control C in
`01-glob-control-matrix.txt`:

```
=== C (shopt -s dotglob; LC_COLLATE=C) ===
     1	0digit/file
     2	_under/file
     3	usr/bin
     4	usr/share
```
An archive built from that list has no `.PKGINFO`, and the partial load of it fails with "missing package
metadata" (`be_package.c:653`, PA2). The row's conclusion is caused by `LC_COLLATE=C` + `dotglob`, so
this omission does not falsify it — but the sentence as written is an incomplete account of
`:564-565`, and a reader who reproduces "`LC_COLLATE=C` and bash `dotglob`" gets no metadata at all.

# Note 3 — "the metadata sits at the beginning of the archive" is stated unconditionally

The sort clause is carefully hedged ("data files whose names begin with a letter, a digit or an
underscore"), but the archive clause is not: a root entry whose first byte is below `.` (45 or less:
`!` … `,`, `-`) leads the archive, and `bsdtar --files-from` takes such a name literally. The hedge
covers the sort claim and not this one. Host check: `grep -cE '^\./[!-,]'` over all 1409 mtrees → `0`,
so again unreached here. Recording it as the same family as the missing `globstar` word, not as a
separate defect.

# Smallest safe correction

Rule text, second half only (value cell `LC_COLLATE=C dotglob` unchanged — the pair that decides the
order is right; `globstar` decides completeness):

> makepkg lists package files with `LC_COLLATE=C`, bash `dotglob` and `globstar`, so the dot files sort
> ahead of the data files whose names begin with a letter, a digit or an underscore and the metadata sits
> at the beginning of the archive so long as no root name sorts before `.` in byte order; a load that is
> partial skips every `.`-prefixed entry (`be_package.c:373-381, 625`) and stops reading at the end of the
> first archive entry after `.PKGINFO` that is not `.`-prefixed, or at the end of the archive when
> `.PKGINFO` is its last entry.

Impacted axes: QUALITY 86 (the rule must be true of the pinned source; the window `:560-569` contains
`globstar`, and the second clause is be_package.c, not the window, so its condition belongs in the rule
text), QUALITY 14/81 untouched. Nothing in the value cell, the source row (S229), the decision table or
the host column needs to change.

# Not done

No counter run (`tools/check-package-anatomy-r41.py` was not executed — my item asks for a verdict file,
not a score), no package built or opened (the cache is empty and transactions are paused, so the archive
claim was tested with the exact `list_package_files | bsdtar` pipeline outside the lane, not with a real
`makepkg` output), no `-Qkk`/local-db check beyond reading `mtree` files, and no mutation of the frozen
snapshot.
