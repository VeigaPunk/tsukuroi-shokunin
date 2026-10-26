VERDICT: partly
ROW: PA5
lines checked: frozen/src/makepkg.sh.in:615-620

Adversarial read of PA5 at 9cc9aa77e30e0e23de2d4d2697b3b218ada02969. I followed every caller/callee the
cell depends on in the pinned snapshot, not just the cited window: `list_package_files` (makepkg.sh.in:558-569),
the metadata writes and the `.INSTALL`/`.CHANGELOG` copies (:586-603), the mtime normalisation (:613-614), the
package-archive command (:624-626), `NOARCHIVE` (:66, :572, :1007), `create_srcpackage` (:737), and on the
libalpm side `handle_simple_path` / `build_filelist_from_mtree` (be_package.c:373-385, 400-540) and
`extract_db_file` (add.c:168-189, the `.MTREE`→`mtree` map the word "kept" rests on).

## What survives (why this is `partly`, not `fails`)

1. `mtree-format`: `--format=mtree` is on the generating command (makepkg.sh.in:617); the kept file starts
   with `#mtree` (`frozen/hostcap/mtree-pacman-head.txt:1`).
2. `gzip`: `| gzip -c -f -n > .MTREE` (makepkg.sh.in:619). Independent host measurement over all 1409 local
   database entries: gzip magic `1f8b` on 1409 of 1409 (receipt `w1/C2RevPA5b/host-mtree-flags.tsv`, column 2;
   matches `frozen/hostcap/localdb-anatomy.tsv` column `mtree_gzip`).
3. "excludes `.MTREE` itself … omits its own entry": the exclusion is load-bearing and works. Fixture with a
   `.MTREE` already present in the pkgdir, exact :617-619 command: the listing has no `./.MTREE` entry; delete
   `--exclude .MTREE` and the same stream lists `./.MTREE time=… size=5 sha256digest=a03f23…`
   (`w1/C2RevPA5b/pipeline-fixture.txt`, sections 1-2). Real build ordering (fresh pkgdir, `.MTREE` written in
   place, 10 trials): self-listed 0 (`w1/C2RevPA5b/fresh-order.txt`). Host: 0 of 1409 kept mtrees list
   `./.MTREE `, measured independently of the frozen tsv (`host-mtree-flags.tsv`, column 3).

## Defect 1 — the enumeration is overstated (host-observable, 51 of 1409 packages)

The cell closes with "the kept database `mtree` describes `.BUILDINFO`, `.PKGINFO` and the data files". It also
describes `.INSTALL` and `.CHANGELOG` and the directory entries:

- Source: `create_package` copies `install/.INSTALL` and `changelog/.CHANGELOG` into `$pkgdir` at
  makepkg.sh.in:592-603, i.e. before the listing at :617; `list_package_files` sets `dotglob` (:565) and
  globs `**/*` (:567), so root dot files are members. The pinned glob returns them (scratch run:
  `.BUILDINFO .INSTALL .MTREE .PKGINFO usr usr/bin usr/bin/foo usr/share …`, 12 entries, identical to
  `find . -mindepth 1` on the same tree) and directories are members too.
- Host: of the 1409 kept mtrees, 51 list `./.INSTALL ` and 51 entries carry an `install` file (both counts 51;
  `host-mtree-flags.tsv` column 4 vs `frozen/hostcap/localdb-anatomy.tsv` column `install`). Example,
  `/var/lib/pacman/local/1password-beta-8.12.42_34.BETA-1/mtree` decompressed, line 4:
  `./.INSTALL time=1791932547.0 size=886 sha256digest=2234d8b3…` (`w1/C2RevPA5b/host-install-mtree.txt`).
  0 of 1409 list `./.CHANGELOG` only because no host package sets `changelog=`; makepkg still copies it.
- Directory entries: 1402 of 1409 kept mtrees carry at least one `type=dir` entry (487124 entries total;
  `host-mtree-flags.tsv` columns 6-7). The same package's mtree has 27 `type=dir` of 124 entries, e.g.
  `./opt time=1791932547.0 mode=755 type=dir` — the format the row calls "the package files" is
  files-plus-directories.

So the enumeration is complete for a package with no scriptlet and incomplete otherwise; PA1 and PA4 in the
same entry both name `.INSTALL`/`.CHANGELOG`, so PA5 contradicts its neighbours.

## Defect 2 — missing condition: the exclusion is not root-only (source + reproduction)

`--exclude .MTREE` is a bare pattern, and bsdtar matches it against the basename at any depth, so the row's
"excludes `.MTREE` itself" also drops a *data file* named `.MTREE` anywhere in the tree, while the package
archive command at makepkg.sh.in:625-626 carries no `--exclude` and keeps it. Reproduced with the host's
bsdtar 3.8.10 on the exact command (`w1/C2RevPA5b/pipeline-fixture.txt`):

- fixture `usr/share/doc/demo/.MTREE` → absent from the `--exclude .MTREE` listing (section 1),
  present in the listing with the flag removed (section 2);
- package-archive form (:625) lists `usr/share/doc/demo/.MTREE` (section 3), and with `--exclude .MTREE`
  added the same tar loses it (section 4).

Consequence: for any package shipping a file of that name below the root, the kept `mtree` is a proper subset
of the package members, so "mtree-format listing of the package files" / "describes … the data files" is
overstated and carries a condition the row omits. Host instances: none on this host — `grep -h MTREE` over all
`/var/lib/pacman/local/*/files` returns 0 lines — so this defect is source-plus-reproduction, not
host-observed; it is exactly the kind of condition a rule row is supposed to state.

## Minor, non-blocking

- "makepkg writes `.MTREE`" is unconditional in the cell, but `create_package` returns at :572 when
  `NOARCHIVE` (:1007) and only the binary-package path writes one; `create_srcpackage` (:737) writes
  `${pkgbase}-${fullver}${SRCEXT}` with no `.MTREE`. Both are outside an ALPM package (PA1 scope), so I do
  not score this.
- `gzip -c -f -n`: the `-n` keeps name and mtime out of the header (`frozen/hostcap/capture.sh:20` reads only
  the magic); the cell's "gzip" is right but the flag is the reason the file is byte-reproducible.

## Gates the correction must respect (read, then confirmed by a run)

`python3 tools/check-package-anatomy-r41.py --revision 71851d63… --repo <lane>` → `rules_verified 8`,
`host_ok 6`, `source_ok 1`, and `PA5: verified true, reasons []`, `verdicts {holds:[],partly:[],fails:[]}`
(no verdict file at that revision). So the row currently passes every lexical gate; the defects are semantic.
Two constraints bind any correction: (a) `RELATIONS['PA5']` (tools/check-package-anatomy-r41.py:105-106)
requires the literals `mtree-format listing`, `gzip`, `excludes .MTREE itself`, `omits its own entry` in that
order, plus no negation word and >= 12 words; (b) any `makepkg.sh.in:<A>-<B>` in the source cell must lie
inside the frozen WINDOW 615-620 (:82, :363-367) — the evidence for Defect 1 sits at :592-603 and :565-569,
so the added conditions must be expressed in the rule cell, not as a second citation.

## Smallest safe correction

Smallest (fixes Defect 1 only; keeps all four literals, no negation word, does not contain the row's quote):

| PA5 | makepkg writes `.MTREE` as an mtree-format listing of the package's files and directory entries, compressed with gzip `-n`, and excludes `.MTREE` itself from that listing, so the kept database `mtree` describes `.BUILDINFO`, `.PKGINFO`, an optional `.INSTALL` or `.CHANGELOG`, the directory entries and the data files but omits its own entry | `gzip mtree without .MTREE` | S229 makepkg.sh.in:615-620 “LANG=C bsdtar -cnf - --format=mtree” | local database mtree files: gzip 1409 of 1409, self-listed 0 of 1409 (`.INSTALL`-listed 51 of 1409, directory entries 1402 of 1409, own-work receipt `w1/C2RevPA5b/host-mtree-flags.tsv`) |

Recommended additionally (fixes Defect 2, one clause appended after `omits its own entry`):

> …, and the bare `--exclude .MTREE` pattern also drops a data file of that name at any depth, which the package archive keeps

Host-cell addition keeps both frozen substrings (`gzip 1409 of 1409`, `self-listed 0 of 1409`,
tools/check-package-anatomy-r41.py:227), so `host_ok` stays true.

## Not run

No counter run of the C1 selftest and no pacman transaction; no lane file edited, no git/jj state touched; no
tool installed, so there is no tool/version/channel entry to record. Scratch
`/fast/scratch/hyaku/tsukuroi-r41/C2RevPA5b` removed after the receipts above were copied.
