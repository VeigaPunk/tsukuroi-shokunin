VERDICT: holds
ROW: PA5
lines checked: frozen/src/makepkg.sh.in:615-620

Row under review — corpus/knowledge/alpm-package-anatomy-r41.md:30 at 9cc9aa77e30e0e23de2d4d2697b3b218ada02969 (read via `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 9cc9aa77e30e0e23de2d4d2697b3b218ada02969:corpus/knowledge/alpm-package-anatomy-r41.md | grep -n PA5`):

| PA5 | makepkg writes `.MTREE` as an mtree-format listing of the package files, compressed with gzip, and excludes `.MTREE` itself from that listing, so the kept database `mtree` describes `.BUILDINFO`, `.PKGINFO` and the data files but omits its own entry | `gzip mtree without .MTREE` | S229 makepkg.sh.in:615-620 “LANG=C bsdtar -cnf - --format=mtree” | local database mtree files: gzip 1409 of 1409, self-listed 0 of 1409 (`localdb-anatomy.tsv`) |

Rule cell, clause by clause, against the pinned snapshot (frozen/src/makepkg.sh.in):

1. "writes .MTREE as an mtree-format listing of the package files" — supported. frozen/src/makepkg.sh.in:617 `list_package_files | LANG=C bsdtar -cnf - --format=mtree \` and :619 `--null --files-from - ... > .MTREE`: bsdtar in mtree format consumes the file list. list_package_files (frozen/src/makepkg.sh.in:560-569) emits every pkgdir file — `export LC_COLLATE=C; shopt -s dotglob globstar; printf '%s\0' **/*` — so the listing covers the package files including the root dot files.
2. "compressed with gzip" — supported. frozen/src/makepkg.sh.in:619 `| gzip -c -f -n > .MTREE`.
3. "excludes .MTREE itself from that listing" — supported. frozen/src/makepkg.sh.in:619 `--exclude .MTREE`.
4. "so the kept database mtree describes .BUILDINFO, .PKGINFO and the data files but omits its own entry" — supported as the direct consequence of clauses 1-3 (dotglob puts .BUILDINFO/.PKGINFO into the listing; only .MTREE is excluded), and independently corroborated by (a) frozen/src/be_local.c:246-283 `_cache_mtree_open`, which opens the local-db mtree with `archive_read_support_format_mtree` plus `_alpm_archive_read_support_filter_all` — i.e. libalpm consumes it as a (compressed) mtree archive — and (b) the frozen capture below.

Non-material observation: create_package early-returns under `(( NOARCHIVE ))` (frozen/src/makepkg.sh.in:569-570), so .MTREE generation is conditional on archiving being enabled. The rule claims the artifact's shape when written, not unconditional creation, so this omitted gate does not change the meaning of any clause.

Quote check: source cell cites S229 with quote “LANG=C bsdtar -cnf - --format=mtree” — present verbatim at frozen/src/makepkg.sh.in:617, inside the cited 615-620 window (616 msg2 "Generating .MTREE file...", 617-619 generation, 620 `touch -d @$SOURCE_DATE_EPOCH .MTREE`). S229 (corpus/SOURCES.md:238 at 9cc9aa77) also pins snapshot sha256 d588222586b2432b4169c82e6ebcd464acfdc20a663172fd444b8f98e1104e86, which matches the frozen/src/SHA256SUMS line `d5882225...e86  makepkg.sh.in`.

Live-source check (access date 2026-10-26): `curl -fsSL https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/scripts/makepkg.sh.in` → sha256 d588222586b2432b4169c82e6ebcd464acfdc20a663172fd444b8f98e1104e86, equal to SHA256SUMS and S229. `cmp` of the fetched file against frozen/src/makepkg.sh.in → IDENTICAL, so the cited line numbers hold on the live file too. Located quote at line 617 of the fetched file: "list_package_files | LANG=C bsdtar -cnf - --format=mtree".

Host cell vs the frozen capture (frozen/hostcap/): "local database mtree files: gzip 1409 of 1409, self-listed 0 of 1409 (localdb-anatomy.tsv)" — stated as measured, and true:
- `awk -F'\t' 'NR>1{...}' localdb-anatomy.tsv` → rows=1409 mtree=1409 gzip=1409, mtree_but_not_gzip=0, self_listed=0 (mtree_lists_self is 0 in every row).
- Method is a real read-only measurement (capture.sh:15-19): gzip decided by magic bytes (`head -c 2 ... = 1f8b`), self-listing by `zcat -- "$d/mtree" | grep -c '^\./\.MTREE '`; no sudo, no pacman transaction, writes only into its outdir (capture.sh:1-7).
- Integrity: MANIFEST.sha256 entry for localdb-anatomy.tsv d10ae8445ba37ef5e85a1e0e1127ef6f7e450fd276729b6cbd0f982e06d1734e equals the recomputed sha256sum of the file.
- Direct artifact evidence: mtree-pacman-head.txt (head of pacman's kept mtree) lists `./.BUILDINFO ...` and `./.PKGINFO ...` entries and no `./.MTREE` entry — the kept mtree describes the metadata files and omits itself, exactly as the rule's consequence clause states.
- Scope honesty: capture-meta.txt records pacman 7.1.0.r9.g54d9411-3 (the declared pacman 54d9411 package) and alpm_db_version 9, captured 2026-10-26T16:14:04Z; the host cell presents the numbers as counts of this capture ("1409 of 1409"), not as a universal claim.

Consistency with alpm-package(7) (frozen/src/alpm-package.7.raw): line 108 lists `.MTREE: an ALPM-MTREE file` among the root members; the man page makes no gzip or self-exclusion claim, so the rule cell's extra detail is correctly sourced to S229 (code) rather than overclaimed from the man page.

Not done: did not run check-package-anatomy-r41.py (not this seat's item); did not review any row other than PA5; did not build a package locally — the host capture was used as the measured evidence instead.

Receipts: .ufo/waves/round-41/w1/C2RevPA5/ (makepkg.sh.in.upstream — the fetched live file; receipts.txt — command outputs).
