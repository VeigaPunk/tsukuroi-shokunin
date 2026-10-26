VERDICT: holds
ROW: PA1
lines checked: frozen/src/alpm-package.7.raw:95-124

# C2RevPA1b — adversarial read of PA1 (alpm-package-anatomy-r41.md:26 @ 9cc9aa77)

Rule cell under test, verbatim from `corpus/knowledge/alpm-package-anatomy-r41.md:26`:
"The package format document names three metadata files that must be present at the root of an ALPM
package, `.BUILDINFO`, `.MTREE` and `.PKGINFO`, and an optional install scriptlet named `.INSTALL`
at the same root, beside zero or more data files."

I tried to break each clause with the strongest counterexample the pinned snapshot admits. None
falsified a clause; the row survives on all four, with two boundaries that a later edit should close
(citation range, and the scope word "document").

Probe receipt: `.ufo/waves/round-41/w1/C2RevPA1b/pa1-probe.txt` (all commands below, with their output).

## Provenance first (the row's premise is the page, so the page had to be the one claimed)

- Frozen snapshot is intact: `cd .ufo/waves/round-41/frozen/src && sha256sum -c SHA256SUMS` → nine
  `OK`, exit 0 (`alpm-package.7.raw` = `b551bb392f6899c89c4c0d5778c89ad482f0c1251260ccf336bd5b5ed2693c45`).
- The snapshot is the alpm-docs 0.13.0-1 rendering, not a stale or edited copy: a fresh
  `curl -sS https://man.archlinux.org/man/alpm-package.7.raw | sha256sum` returns the same
  `b551bb39…c45` on 2026-10-26, and the HTML page footer names `0.13.0-1`
  (`alpm-package.7.html:281`, `grep -n -A1 "<dt>Package</dt>\|<dd>0\.13\.0-1"`). So the row is talking
  about the document it says it is talking about.

## Clause 1 — "three metadata files that must be present at the root"

`frozen/src/alpm-package.7.raw:98` is the heading `Metadata`; `:100` is "The following files must be
present at the root of an ALPM based package:"; the three bullets are `:102` `.BUILDINFO`, `:108`
`.MTREE`, `:114` `.PKGINFO`. The sentence is unconditional — it carries no "when installed", "if the
package has data" or builder qualifier — and `:9` repeats the modality ("mandatory metadata files").
Counterexample tried: is there a package category the document exempts? `alpm-meta-package(7)`
(fetched from the same site) says meta packages "do not provide files, but instead only define
package relations" and are "handled like any other ALPM based package"; it grants no exemption from
the metadata sentence, and `alpm-package.7.raw:124` points at it only for the zero-data case, which
the row already covers. Clause holds.

## Clause 2 — the three names and their order

`:102` `\f(CR.BUILDINFO\fR`, `:108` `\f(CR.MTREE\fR`, `:114` `\f(CR.PKGINFO\fR` — the rule lists the
same three in the same order, and the value cell `.BUILDINFO .MTREE .PKGINFO; optional .INSTALL`
matches the counter's derivation from exactly this bullet run
(`tools/check-package-anatomy-r41.py:169-174`, `man[i:j]` between "must be present at the root" and
"Optionally, an"). No extra name appears in the Metadata section (grep of the whole page for
`CHANGELOG` exits 1). Clause holds.

## Clause 3 — "an optional install scriptlet named `.INSTALL` at the same root"

`:120` "Optionally, an `alpm-install-scriptlet` named `.INSTALL` may be present at the root of an ALPM
based package." Both attributes the rule asserts are stated: optional, and root placement. The
sibling page in the same doc set spells the root rule out again, `alpm-install-scriptlet(5):12`
"Such files are located at the root of ALPM packages and are named `.INSTALL`". Counterexample tried:
does the scriptlet page make the name conditional (e.g. a second accepted name)? No — line 12 is the
only naming sentence, and it is singular. Clause holds.

## Clause 4 — "beside zero or more data files"

`:124` "Zero or more `data` files may be present in an ALPM based package (refer to
`alpm-meta-package` for details on why packages may not contain any `data` files)." The rule does not
claim the data files sit at the root (they do not: `:134`'s example data file is
`usr/share/example/data.txt`, `:157-161`), so "beside" is accurate as written. Clause holds.

## Counterexamples that do *not* falsify, and why

1. **Enforcement reading.** libalpm loads a package that carries only `.PKGINFO` (PA2,
   `be_package.c:598-654`), so "must be present" is not what the loader enforces. This does not make
   the rule false because the rule subject is "the package format document", and the entry states the
   divergence itself ("Spec and implementation differ on purpose… A package missing `.BUILDINFO` or
   `.MTREE` still loads", `alpm-package-anatomy-r41.md` QUALITY section, last bullet). A reader who
   takes "must be present" as a load requirement is reading PA2's job into PA1; the fix, if any, is
   editorial, not a correction.
2. **`.CHANGELOG` exists in the format but not in the page.** makepkg stages it
   (`makepkg.sh.in:592` `for i in 'changelog/.CHANGELOG' 'install/.INSTALL'`), be_package.c opens it
   (`:76`), add.c keeps it as `changelog` (`:175-176`), yet alpm-package.7 never names it (grep exits
   1). Under a reading of PA1 as "the format's exhaustive root set" that would be an omission; under
   the reading the row actually writes — what *the document* names — it is not. PA4 already carries
   `.CHANGELOG` in the entry, so the corpus is not missing the fact; only the row's enumeration is
   narrower than the implementation. Not a falsification; a candidate for one added clause.
3. **Sibling pages contradicting "must".** Checked PKGINFO(5):9, BUILDINFO(5):34, ALPM-MTREE(5):202
   from the same site: all three say the file "is located/such files are located at the root of ALPM
   packages" and none calls it optional or conditional, so they reinforce the rule rather than relax
   it. (BUILDINFO(5):34 says "found in the root of a package created by `makepkg`", which is where
   makepkg always writes it — `makepkg.sh.in:589` — not an exemption.)
4. **Host cell not being necessity evidence.** The host column ("the local `mtree` of pacman
   7.1.0.r9.g54d9411-3 lists `./.BUILDINFO` and `./.PKGINFO` as package members") is an existence
   demonstration, not a necessity test, so on its own it could not prove "must be present". It is
   nevertheless true and exactly reproducible: `zcat /var/lib/pacman/local/pacman-7.1.0.r9.g54d9411-3/mtree
   | sed -n 1,4p` returns the same four lines as `frozen/hostcap/mtree-pacman-head.txt`, digests
   included, and `localdb-anatomy.tsv:1028` records `mtree=1 install=0 changelog=0 dotfiles=0
   mtree_gzip=1 mtree_lists_self=0` for that entry. The host column is declared own-work capture, and
   the necessity claim rests on the document, which is where the row puts it.

## Impacted axes

- C2 depth (PA1): supported; the rule is a faithful, non-quoting paraphrase of `:100`, `:102`,
  `:108`, `:114`, `:120`, `:124`.
- Counter predicate (C2): no impact — the verdict is `holds`, which is what
  `check-package-anatomy-r41.py` needs for `verdicts_ok` (one holds, zero fails). Note the counter's
  PA1 relations (`tools/check-package-anatomy-r41.py:98`) are shape gates only; this file is the read,
  and the read agrees with the gates for once.
- Provenance: the cited range is the one weakness found (below).

## Smallest safe correction (not required for the verdict)

1. Cited range: the row's source cell cites `alpm-package.7.raw:100-120`, but its last clause comes
   from `:124`; four lines of the rule sit outside their own citation. The counter's window is 95-124
   (`tools/check-package-anatomy-r41.py:78`) so the row passes, and S227 independently records
   "lines 95-124" (`corpus/SOURCES.md:236`). Minimal fix: change the entry's citation to
   `:100-124` so the citation covers the data clause it already asserts. No rule text changes.
2. Optional, if a later round wants PA1 to describe the format rather than the page: append one
   clause "the implementation additionally stages an optional `.CHANGELOG` at the same root
   (`makepkg.sh.in:592`), unnamed by the document", keeping PA4 as the keeping-side statement. This
   is an extension, not a correction; the current cell is true without it.

## What I did not do

- I did not run `tools/check-package-anatomy-r41.py` against the entry (that run belongs to the
  counter seats; my evidence is the frozen source plus the page at its pinned version).
- I did not exercise the load path with a hand-built package missing `.BUILDINFO`/`.MTREE`: pacman
  transactions are paused and the rule under test is a document statement, so the source read of
  `be_package.c` (already PA2's row) is the ceiling of what this item needs.
- I fetched `alpm-package.7.raw`, `alpm-install-scriptlet.5.raw`, `alpm-meta-package.7.raw`,
  `PKGINFO.5.raw`, `BUILDINFO.5.raw` and `ALPM-MTREE.5.raw` from man.archlinux.org read-only on
  2026-10-26; the fetched `alpm-package.7.raw` hash equals the frozen one, and the other five live
  only as their sha256 and the quoted lines in the probe receipt (my scratch dir is removed).
