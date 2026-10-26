VERDICT: holds
ROW: PA3
lines checked: frozen/src/makepkg.sh.in:558-570
also read: frozen/src/makepkg.sh.in:548-593 and :594-643 (create_package: the `.MTREE` call at :617-619 and the package-archive call at :625-626, both fed by `list_package_files`; the srcpackage call at :737); frozen/src/be_package.c:369-393 (`handle_simple_path`) and :589-656 (the load loop, the break test, "missing package metadata"); row PA3 and its correction bullet in corpus/knowledge/alpm-package-anatomy-r41.md at revision 20c327b3f1cf96ad1828792c2ae5db71b5fd9ef7 (row line 28, correction lines 78-82)
pinned: `cd .ufo/waves/round-41/frozen/src && sha256sum -c SHA256SUMS` → `be_package.c: OK`, `makepkg.sh.in: OK` (receipts: residual/C2RevPA3c/receipts.txt)
seat: C2RevPA3c (residual third read, item PA3-c); second reader .ufo/waves/round-41/w1/C2RevPA3b.md returned `partly`; its receipts re-read in w1/C2RevPA3b/

# The correction answers each defect the second reader raised

1. **Missing `globstar` (counterexample 2) — addressed, citation exact.** The correction says
   "`list_package_files` sets `globstar` as well as `dotglob` (`makepkg.sh.in:565`)". Line 565 is
   verbatim `shopt -s dotglob globstar` (grep anchor; receipts §3). The rule reading now names all
   three settings of :564-567; receipt 01 case C shows the row's old two-setting account reproduces
   no listing at all, so the added word is required, and it is now there.
2. **Wrong stop rule (counterexample 1) — addressed, clause by clause.** The correction replaces the
   row's "stops reading at the end of the first archive entry after `.PKGINFO` has been parsed" with:
   a partial load "skips every `.`-prefixed entry before its stop test (`handle_simple_path`,
   `be_package.c:373-385`, then `continue`) and stops at the end of the first entry after `.PKGINFO`
   that is not `.`-prefixed, or at the end of the archive when no such entry follows". Checked
   directly against the snapshot: `handle_simple_path` returns 1 for `.INSTALL` (sets
   `pkg->scriptlet`, :375-377) and for every name whose first byte is `.` (:378-381); its call site
   at :625-626 `continue`s, so dot-prefixed entries never reach the stop test. The stop test sits at
   the loop bottom, :641-642 `if((!full || hit_mtree) && config) { break; }`, reached only by an
   entry that falls through every `continue` branch — i.e. a non-`.`-prefixed entry — after
   `archive_read_data_skip` (:633), so the break is at the end of that entry. If every successor is
   dot-prefixed (or `.PKGINFO` is last), the loop exits at EOF (:644) and the load still succeeds
   because `config` is 1 (:652-655 errors only when `!config`) — "stops at the end of the archive".
   A non-dot entry placed before `.PKGINFO` breaks nothing (config still 0), exactly as the
   "after `.PKGINFO`" scoping says. Receipt 03's mirror (stop after `0digit/`, the first non-dot
   entry after `.PKGINFO`, `.config` consumed) matches this rule and is what the uncorrected row got
   wrong. Every shape the second reader listed is covered.
3. **Unconditional archive claim (note 3) — addressed, hedge correctly scoped.** The correction adds
   "the metadata sits first so long as no root name sorts before `.` in byte order". Under
   `LC_COLLATE=C` (`:564`) bash sorts by byte, `.` is 0x2E and digits/letters/`_` start at 0x30 and
   above, so the only way a root name precedes the metadata is a first byte below `.` — exactly the
   hedge. Both consumers take the listing unsorted: the mtree call :617-619 and the archive call
   :625-626 use `bsdtar -cnf … --null --files-from -` (`-n` = do not sort), and receipt 02 (19
   members, bsdtar 3.8.10) shows archive order equal to glob order. The source's own comment :558-561
   ("database files are placed at the beginning of the package regardless of / sorting") states the
   same intent.

# Remaining clauses of row+correction

- "the dot files sort ahead of the data files whose names begin with a letter, a digit or an
  underscore" (unchanged): true under `LC_COLLATE=C` byte order — receipt 01 case A orders
  `.BUILDINFO … .PKGINFO .config` ahead of `0digit`, `Zebra`, `_under`, `apple`, `usr`; case B
  (`en_US.utf8`) breaks it, confirming the attribution to `LC_COLLATE=C` rather than to bash.
- The correction's "then `continue`" parenthetical covers the `.INSTALL` nuance: the loader records
  the scriptlet (:376) and then skips the entry like every other dot name; the stop behavior is what
  the clause claims, and PA4 already carries `.INSTALL`'s retention in the local db. No conflict.
- Value cell `LC_COLLATE=C dotglob` is left unchanged by design (the correction carries the
  `globstar` word in the rule text); the pair in the cell is the one that decides the order, exactly
  as the second reader concluded. Nothing in the row's other cells needs to move.

# New overreach scan

None found. The hedge is no wider than the source; the stop rule covers the EOF and dot-only
shapes; both line citations in the correction (`makepkg.sh.in:565`, `be_package.c:373-385`) are
exact against grep anchors (receipts §3); the corrected reading says what the pinned sources say
and nothing more.

# Not done

No counter run (`tools/check-package-anatomy-r41.py` not executed — this item asks for a verdict
report, not a score). No package built and no `makepkg` run (transactions are paused host-wide; the
archive-order clause rests on the snapshot's own bsdtar invocations plus the second reader's
receipts, which I re-read, not on a fresh package file). Receipts kept in residual/C2RevPA3c/ are
only the hash verification, the revision check and the grep anchors. No scratch dir was created —
no clone, copy, mutant or fixture was needed; all evidence is read-only lane content, so there is
nothing to clean up.
