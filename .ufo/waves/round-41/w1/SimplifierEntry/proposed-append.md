
## Round-41 surface reconciliations (append-only)

Read the four surfaces in this order: a rule cell cites an upstream row (S227-S233), the supporting-rows
paragraph adds corroboration only, the decision table applies one row to one symptom, and the QUALITY bullets
name criteria. No rule, value or host cell changes below.

- **"which it keeps in the local database after install"** (Scope) is partly held already: TO3 has the post
  scriptlet "runs from the local database's `install` file" (`corpus/knowledge/pacman-transaction-order-r39.md:26`)
  and EX5 takes the scriptlet "from the local database" (`corpus/knowledge/pacman-exec-environment-r40.md:25`).
  Read this entry's gap as PA4's mapping, mode and skip rule, not as the existence of a kept `install`; r35
  holds no package-member statement (`grep -c 'PKGINFO\|BUILDINFO\|MTREE\|mtree'
  corpus/knowledge/pacman-backup-files-r35.md` → 0).
- **What each supporting row reaches.** S234 (`_cache_mtree_open`) makes PA6's open succeed for the file PA4
  kept and PA5 gzipped; it corroborates neither the mapping (PA4) nor the listing content (PA5), so "supports
  PA4-PA6" reads as "reads the kept file back". S235 (`query.c:317-323`) sources PA6's `-Qk`/fast-check
  clause, which the S231 quote in the same row does not carry. S236 is own-work and sits in no cell: every
  host cell is a reading of `.ufo/waves/round-41/frozen/hostcap/` (`corpus/SOURCES.md:245`).
- **PA1 and PA4 name different sets.** `.CHANGELOG` is outside PA1 because the format document never names it
  (`grep -ci changelog .ufo/waves/round-41/frozen/src/alpm-package.7.raw` → 0) and inside PA4 because
  `add.c:175-176` maps it; PA1 is the format document's complete list.
- **PA2's "full load" is PA3's "partial" load.** `full` is the third parameter of `_alpm_pkg_load_internal`
  (`be_package.c:555-556`), chosen by the caller; PA3's stop is the loop test `(!full || hit_mtree) && config`
  (`be_package.c:641`), taken after the entry following `.PKGINFO` is skipped.
- **Decision rows 1-2: order is not membership, a dash is not a form.** PA3 bounds member order for makepkg
  archives, so `head -n 5` shows order and cannot show absence; test membership with
  `bsdtar -tf <pkg> | grep -qxF '.PKGINFO'` (the members are the names `list_package_files` emits,
  `makepkg.sh.in:625-626`, and the loader compares the bare name, `be_package.c:598`). The load refuses an
  absent name, an absent version and a version without `-` (`be_package.c:605-616`); `[<epoch>:]<pkgver>-<pkgrel>`
  is what makepkg writes into the one `pkgver` key (`makepkg.sh.in:498-499`,
  `/usr/share/makepkg/util/pkgbuild.sh:167-172`), not a shape the load enforces.
- **Decision row 3, read against PA4-PA6.** PA5 plus PA4 mean a makepkg-built package always installs an
  `mtree`, so the `mtree == NULL` branch is reached by an archive that carried no `.MTREE` (PA2 requires none)
  or by a local entry whose `mtree` file is gone; it is not evidence of drifted file content. `return 0`
  (`check.c:320`) is that package's error count — the held `-Qkk` reading makes it `rc=0`
  (`corpus/knowledge/package-state-plane.md:149-150`) — and the notice is printed only without `--quiet`
  (`check.c:317-319`). PA6's second trigger was not probed: the capture records `[ -f "$d/mtree" ]`
  (`capture.sh:14`), so "branch unreached on this host" covers the absent file, not a failed open.
- **QUALITY: which criterion each line answers.** 14 is novelty, 86 rule rows on upstream rows, 81 the per-row
  verdict rule, whose bypass paragraph is 87 (the lexical relations are shape gates; the verdict files are the
  read). 81 reads `.ufo/waves/round-41/w1/` and `.ufo/waves/round-41/residual/`
  (`tools/check-package-anatomy-r41.py:60`) and credits a row with at least one `VERDICT: holds` and no
  `VERDICT: fails` (`:321`). The unnumbered bullet reads as 66 — PA1's requirement and PA2's enforcement both
  kept — and states no rule of its own.
