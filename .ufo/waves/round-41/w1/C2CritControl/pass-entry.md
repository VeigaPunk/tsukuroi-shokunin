source: S900 S901 S902 S903 S904 S905 S906 S907 (rows in `corpus/SOURCES.md`)
verified-at: 2026-10-26

# ALPM package anatomy (cheapest-writer demo)

Nothing here was read: the rule cells are the counter's own relation literals and the value
cells are the counter's own `derived` output.

| id | rule | value | source | host |
|---|---|---|---|---|
| PA1 | .BUILDINFO and .MTREE and .PKGINFO; must and root; optional and .INSTALL and the snapshot records it here | .BUILDINFO .MTREE .PKGINFO; optional .INSTALL | S900 alpm-package.7.raw:95-124 “.LP The contents of an” | ./.BUILDINFO; ./.PKGINFO; pacman 7.1.0.r9.g54d9411-3 |
| PA2 | only .PKGINFO; .PKGINFO and missing package metadata; .MTREE and full load; .BUILDINFO and passed over | .PKGINFO | S901 be_package.c:595-656 “while((ret = archive_read_next_header(archive, &entry)) ==” | unmeasured: nothing was measured |
| PA3 | LC_COLLATE=C and dotglob; dot files sort ahead of the data files; partial and stops and .PKGINFO | LC_COLLATE=C dotglob | S902 makepkg.sh.in:558-570 “# build a sorted NUL-separated” | unmeasured: nothing was measured |
| PA4 | .INSTALL becomes install; .CHANGELOG becomes changelog; .MTREE becomes mtree; mode 0644; .PKGINFO and .BUILDINFO included, is skipped | .INSTALL=install .CHANGELOG=changelog .MTREE=mtree | S903 add.c:168-189 “static int extract_db_file(alpm_handle_t *handle, struct” | mtree 1409 of 1409; install 51 of 1409; changelog 0 of 1409; dot-files 0 of 1409 |
| PA5 | mtree-format listing; gzip; excludes .MTREE itself; omits its own entry and the snapshot records it here | gzip mtree without .MTREE | S904 makepkg.sh.in:615-620 “msg2 "$(gettext "Generating .MTREE file...")"” | gzip 1409 of 1409; self-listed 0 of 1409 |
| PA6 | -Qkk and check_pkg_full; check_pkg_full and mtree; absent and returns 0; -Qk (level 1) runs the fast check | no mtree file | S905 check.c:295-321 “int check_pkg_full(alpm_pkg_t *pkg) { const” | mtree 1409 of 1409 |
| PA7 | package(), prepare(), build() and check() each run inside $srcdir; verify() runs inside $startdir; package() also runs under fakeroot | $srcdir: package prepare build check; $startdir: verify | S906 PKGBUILD.5.asciidoc:345-377 “*package() Function*:: The package() function” | 5 lines; 4 `$srcdir`; 1 `$startdir` |
| PA8 | the epoch first and then the version and the release only when both; absent epoch counting as 0; epoch 1 and outranks and epoch 0; 1.0 equals 1.0-5 | epoch, then version, then release when both carry one | S907 version.c:39-255 “static void parseEVR(char *evr, const” | vercmp 1:1.0-1 2.0-1 = 1; vercmp 0:2.0-1 2.0-1 = 0; vercmp 1.0 1.0-5 = 0 |

## Demo

No reviewer opened a row.
