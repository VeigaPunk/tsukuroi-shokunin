VERDICT: holds
ROW: PA5
lines checked: frozen/src/makepkg.sh.in:555-651

Residual third read of PA5 at lane revision 20c327b3f1cf96ad1828792c2ae5db71b5fd9ef7. `git rev-parse
HEAD` in /home/vgpnk/Projects/shokunin/tsukuroi-shokunin -> 20c327b3f1cf96ad1828792c2ae5db71b5fd9ef7,
and `git diff --stat 20c327b3… -- corpus/knowledge/alpm-package-anatomy-r41.md` printed nothing, so the
working-tree text is the pinned revision. Snapshot integrity: `sha256sum -c SHA256SUMS` in
.ufo/waves/round-41/frozen/src/ -> 9/9 OK. Text reviewed: row PA5
(corpus/knowledge/alpm-package-anatomy-r41.md:30) together with its bullet in `## Corrections from the
round-41 wave` (:64 header; :67-68 "…is the reading that replaces the row text where they differ";
bullet :83-87), and the second reader .ufo/waves/round-41/w1/C2RevPA5b.md (first line `VERDICT: partly`;
Defects 1-2 plus two minors it did not score) with its receipts w1/C2RevPA5b/. Line numbers below are
grep -n on the pinned files.

## Row clauses vs the pinned snapshot — all supported

- "makepkg writes `.MTREE`": makepkg.sh.in:616 `msg2 … "Generating .MTREE file..."`, :617-619 pipeline
  redirects into `.MTREE`.
- "mtree-format listing": :617 `--format=mtree`; the kept file starts with `#mtree`
  (frozen/hostcap/mtree-pacman-head.txt:1).
- "compressed with gzip": :619 `| gzip -c -f -n > .MTREE`. My own read-only sweep of
  /var/lib/pacman/local/*/mtree: gzip magic `1f8b` on 1409 of 1409 (`packages_with_mtree=1409
  gzip_magic=1409`, receipt residual/C2RevPA5c/host-counts-v3.txt).
- "excludes `.MTREE` itself from that listing": :619 `--exclude .MTREE`. My reproduction of the exact
  :617-619 command on a pkgdir holding a pre-existing root `.MTREE`: 0 `./.MTREE` entries with the flag,
  the entry appears without it (receipt repro-summary.txt [4] count 0, [5] `./.MTREE time=… size=19`;
  second reader w1/C2RevPA5b/pipeline-fixture.txt sections 1-2 and fresh-order.txt
  `trials=10 self_listed_total=0`).
- "the kept database `mtree`": add.c:177-178 `strcmp(entryname, ".MTREE") == 0` -> `dbfile = "mtree"`.
- "describes `.BUILDINFO`, `.PKGINFO` and the data files but omits its own entry": my sweep — 1409 of
  1409 kept mtrees list `./.PKGINFO` and `./.BUILDINFO`, 0 list `./.MTREE` (`pkginfo_listed=1409
  buildinfo_listed=1409 self_listed=0`); frozen/hostcap/localdb-anatomy.tsv (1409 data rows of 1410
  lines) agrees: `mtree_gzip=1` on 1409, `install=1` on 51, `changelog=1` on 0, `mtree_lists_self=1` on 0.

## Correction clause 1 — `.INSTALL`/`.CHANGELOG` and directory entries: supported

Source: create_package copies `install/.INSTALL` and `changelog/.CHANGELOG` into `$pkgdir` at
makepkg.sh.in:592-603, before the :617 listing; `list_package_files` sets `dotglob globstar` (:565) and
globs `**/*` (:567), so those members are listed. My reproduction: the no-exclude listing contains
`./.INSTALL` and 5 `type=dir` entries (repro-summary.txt [6][7][8]). Host, measured independently of the
frozen capture: 51 of 1409 kept mtrees list `./.INSTALL` (`install_listed=51`), 1402 of 1409 carry at
least one `type=dir` entry, 60109 `type=dir` entries and 487124 entry lines in total
(`dir_carrying=1402 dir_entries_total=60109 entry_lines_total=487124` — the second reader's "487124
entries total" reproduced exactly; 9677 `/set` lines account for the rest of the 496801 non-header
lines). Spot check 1password-beta-8.12.42_34.BETA-1: line 4 `./.INSTALL time=1791932547.0 size=886
sha256digest=2234d8b3…`, 27 `type=dir` of 124 entries (host-counts-v3.txt; second reader
w1/C2RevPA5b/host-install-mtree.txt; w1/C2RevPA5b/host-mtree-flags.tsv row 1). The conditional phrasing
"the package carries" is right: makepkg refuses the build when a declared scriptlet file is missing
(makepkg.sh.in:596-598, `exit $E_MISSING_FILE`), so a carried `.INSTALL` is always copied before the
listing. "Also lists" is additive, not exhaustive — no overreach.

## Correction clause 2 — bare pattern at any depth, archive keeps it: supported

My reproduction with bsdtar 3.8.10 (same version the second reader used), fixture pkgdir with
usr/share/doc/demo/.MTREE plus .PKGINFO/.BUILDINFO/.INSTALL/usr/bin/foo
(residual/C2RevPA5c/repro-summary.txt, listing-*.txt, archive-members.txt):
- exact :617-619 command with `--exclude .MTREE`: no MTREE entry at any depth ([1] NONE);
- same command without the flag: `./usr/share/doc/demo/.MTREE` listed ([2] line 14);
- archive command of :625-626 (`list_package_files | LANG=C bsdtar -cnf - --null --files-from -`;
  `compress_as` approximated by gzip, build-time placeholder `@BSDTAR_NO_READ_SPARSE@` dropped): member
  `usr/share/doc/demo/.MTREE` present ([3] line 10) — the archive keeps it; :624-626 carries no
  `--exclude`.
Host-instance check: `grep -h MTREE /var/lib/pacman/local/*/files` -> 0 lines
(`files_db_lines_containing_MTREE=0`), matching the correction's "no host instance" qualifier.

## Second reader's conditions — all addressed or shown out of scope

- Defect 1 (enumeration overstated: kept mtree also lists `.INSTALL`/`.CHANGELOG` and directory
  entries) — addressed by correction clause 1, verified against source and host above.
- Defect 2 (bare `--exclude .MTREE` also drops a data file of that name at any depth while the archive
  keeps it) — addressed by correction clause 2, reproduced independently.
- Minor "makepkg writes .MTREE is unconditional" — the reader did not score it; scoping confirmed:
  `(( NOARCHIVE )) && return 0` is the first statement of create_package (makepkg.sh.in:572; option
  :1007; definition :66) and makepkg exits before packaging entirely (:1419-1423), so under --noarchive
  no ALPM package exists for PA5, a row about the package makepkg writes, to describe.
- Minor "gzip -n" — the reader affirmed the cell's "gzip" is right; no clause change needed.

## No new overreach found

Each added clause checked: "the directory entries" is categorical — for the 7 of 1409 packages without
subdirectories (e.g. base-3-3, 2 entries, dir column 0 in w1/C2RevPA5b/host-mtree-flags.tsv) there are
no directory entries to list, which leaves the claim vacuous rather than false; "an `.INSTALL` or
`.CHANGELOG` the package carries" is properly conditional; "anywhere in the tree" — at the root the name
collides with the generated `.MTREE` (overwritten at :619), so the data-file scenario arises below the
root, where the exclusion was demonstrated; the archive also keeps the generated `./.MTREE`, which no
clause denies. The correction contradicts neither the row's host cell ("gzip 1409 of 1409, self-listed
0 of 1409") nor PA4 in the same entry.

## Not run

No counter run (C1 selftest or C2 checker), no pacman transaction, no package/service/host change, no
lane file touched outside my report and receipts, no git/jj state touched, no tool installed (nothing
to record under the 2026-10-19 tooling authorization). Scratch /fast/scratch/hyaku/tsukuroi-r41/C2RevPA5c
removed after the receipts were copied to .ufo/waves/round-41/residual/C2RevPA5c/.
