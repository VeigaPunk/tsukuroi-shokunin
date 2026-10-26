source: S227 S228 S229 S230 S231 S232 S233 S234 S235 S236 (rows in `corpus/SOURCES.md`; pinned snapshots `.ufo/waves/round-41/frozen/src/`, digests in its `SHA256SUMS`; host capture `.ufo/waves/round-41/frozen/hostcap/`, `MANIFEST.sha256`)
verified-at: 2026-10-26 (pacman 54d9411 as built by Arch 7.1.0.r9.g54d9411-3; alpm-package(7) from extra/alpm-docs 0.13.0-1 on man.archlinux.org; host capture 2026-10-26T16:14:04Z)
recheck: on-release — re-fetch the nine snapshot URLs in `.ufo/waves/round-41/frozen/src/FETCH.txt` and compare `sha256sum` with `SHA256SUMS`; re-run `bash .ufo/waves/round-41/frozen/hostcap/capture.sh <dir>` and compare the local-database counts; `python3 tools/check-package-anatomy-r41.py --revision <REV>`

# ALPM package anatomy: what a package file carries, what libalpm requires of it, and what it keeps (round 41)

Scope: the package-file side of the pacman-state plane (`PROVINCE.md` Core, "`.pkg.tar.zst` receipt
discipline"). The lane already holds how a transaction orders scriptlets and hooks
(`corpus/knowledge/pacman-transaction-order-r39.md`), which environment they run in
(`corpus/knowledge/pacman-exec-environment-r40.md`) and how `backup` files become `.pacnew`/`.pacsave`
(`corpus/knowledge/pacman-backup-files-r35.md`). It held no statement of the package archive itself: which
root members the format names, which of them libalpm actually requires when it loads a file, which it keeps
in the local database after install, and how `pacman -Qkk` and version comparison use what was kept. This
entry is that statement. Rules only describe upstream code and documents at the pinned revisions; the host
column records what this host's local database shows. Nothing here builds, installs or removes a package.

Assimilation: theme "alpm package anatomy" from `merge/tsukuroi/` (`alpm-package-anatomy-r26.md`, rejected in
round 38 with the flip condition "a revision that quotes PKGBUILD(5) for each function's working directory
and passes a QUALITY check", `corpus/lessons/round-38.md:49`). PA7 quotes each function's working directory;
the staged sentence "`package()` runs inside `$pkgdir` under `fakeroot` and the others run inside
`$srcdir`" is refused (it is false for `package()` and for `verify()`). No staged row, id or sentence is
adopted; every row below was re-opened this round.

| id | rule | value | source | host |
|---|---|---|---|---|
| PA1 | The package format document names three metadata files that must be present at the root of an ALPM package, `.BUILDINFO`, `.MTREE` and `.PKGINFO`, and an optional install scriptlet named `.INSTALL` at the same root, beside zero or more data files | `.BUILDINFO .MTREE .PKGINFO; optional .INSTALL` | S227 alpm-package.7.raw:100-120 “The following files must be present at the root of an ALPM based package:” | the local `mtree` of pacman 7.1.0.r9.g54d9411-3 lists `./.BUILDINFO` and `./.PKGINFO` as package members (`mtree-pacman-head.txt`) |
| PA2 | When libalpm loads a package file, only `.PKGINFO` sets the metadata flag; a file whose archive lacks `.PKGINFO` fails with "missing package metadata", an empty name or version fails, and a version string lacking a dash fails, while `.MTREE` is read only on a full load to build the file list and `.BUILDINFO` is passed over like every other unhandled dot file | `.PKGINFO` | S228 be_package.c:598-654 “_("missing package metadata in %s\n"), pkgfile);” | unmeasured: the package cache is empty and pacman transactions are paused, so the load path was read in source only |
| PA3 | makepkg lists package files with `LC_COLLATE=C` and bash `dotglob`, so the dot files sort ahead of the data files whose names begin with a letter, a digit or an underscore and the metadata sits at the beginning of the archive; a load that is partial stops reading at the end of the first archive entry after `.PKGINFO` has been parsed | `LC_COLLATE=C dotglob` | S229 makepkg.sh.in:560-569 “database files are placed at the beginning of the package regardless of” | unmeasured: the archive order needs a package file, and the cache is empty |
| PA4 | During install libalpm stores three root members inside the local database entry `<name>-<version>/`: `.INSTALL` becomes `install`, `.CHANGELOG` becomes `changelog` and `.MTREE` becomes `mtree`, each with mode 0644; every other root dot file, `.PKGINFO` and `.BUILDINFO` included, is skipped and kept for future use | `.INSTALL=install .CHANGELOG=changelog .MTREE=mtree` | S230 add.c:168-189 “/* reserve all files starting with '.' for future possibilities */” | local database: mtree 1409 of 1409, install 51 of 1409, changelog 0 of 1409, dot-files 0 of 1409 entries (`localdb-anatomy.tsv`) |
| PA5 | makepkg writes `.MTREE` as an mtree-format listing of the package files, compressed with gzip, and excludes `.MTREE` itself from that listing, so the kept database `mtree` describes `.BUILDINFO`, `.PKGINFO` and the data files but omits its own entry | `gzip mtree without .MTREE` | S229 makepkg.sh.in:615-620 “LANG=C bsdtar -cnf - --format=mtree” | local database mtree files: gzip 1409 of 1409, self-listed 0 of 1409 (`localdb-anatomy.tsv`) |
| PA6 | `pacman -Qkk` (check level 2) runs `check_pkg_full`, which opens the kept local `mtree`; when that file is absent, or present but failing to open (libalpm then also logs "error while reading file"; a TODO in check.c says the two cases are left unseparated), it prints a "%s: ... mtree file" notice and returns 0, so such a package adds zero errors to the check, while `-Qk` (level 1) runs the fast check | `no mtree file` | S231 check.c:295-321 “printf(_("%s: no mtree file\n"), pkgname);” | branch unreached on this host: mtree 1409 of 1409 entries (`localdb-anatomy.tsv`) |
| PA7 | PKGBUILD(5) states the working directory of each packaging function: `package()`, `prepare()`, `build()` and `check()` each run inside `$srcdir` and `verify()` runs inside `$startdir`; `package()` also runs under fakeroot while the other functions run as the calling user | `$srcdir: package prepare build check; $startdir: verify` | S232 PKGBUILD.5.asciidoc:345-377 “This function is run inside `$startdir`.” | host `man PKGBUILD` (pacman 7.1.0.r9.g54d9411-3): 5 lines "This function is run inside", 4 `$srcdir` and 1 `$startdir` (`man-pkgbuild-runinside.txt`) |
| PA8 | libalpm compares two full versions in three steps: the epoch first, an absent epoch counting as 0, then the version, and the release only when both strings carry one; so any epoch 1 build outranks every epoch 0 build and `1.0` equals `1.0-5` | `epoch, then version, then release when both carry one` | S233 version.c:39-255 “/* different from RPM- always assume 0 epoch */” | host `vercmp`: `vercmp 1:1.0-1 2.0-1 = 1`, `vercmp 0:2.0-1 2.0-1 = 0`, `vercmp 1.0 1.0-5 = 0` (`vercmp.txt`) |

Supporting rows: S234 (`be_local.c:251-270`, the local `mtree` is opened with every filter and the mtree
format, so the kept gzip file reads back) supports PA4-PA6; S235 (`query.c:317-321`, check level 1 runs
`check_pkg_fast`, any higher level `check_pkg_full`) supports PA6; S232 also carries the `epoch` field text
(`PKGBUILD.5.asciidoc:67-74`) and the full version string form (`:439-441`) behind PA8.

## Decision table — symptom → row → read-only command

| Symptom | Row | Command (read-only) |
|---|---|---|
| `pacman -U` or a sync install reports "missing package metadata" | PA2 | `bsdtar -tf <pkg> \| head -n 5` — the first members should be the dot files; `.PKGINFO` absent means the archive is not a package |
| "invalid package version" on load | PA2 | `bsdtar -xOf <pkg> .PKGINFO \| grep '^pkgver'` — the value must be `pkgver-pkgrel` (with an optional `epoch:`) |
| `pacman -Qkk <pkg>` prints "no mtree file" and reports the package clean | PA6, PA4 | `ls /var/lib/pacman/local/<name>-<version>/` — without `mtree` the full check verified nothing for that package |
| A package's install scriptlet cannot be found after install | PA4 | `ls /var/lib/pacman/local/<name>-<version>/install` — the kept copy is `install`, not `.INSTALL` |
| An upgrade goes to a lower-looking version | PA8 | `pacman -Qi <pkg> \| grep ^Version; vercmp <installed> <offered>` — an epoch prefix decides first |
| A PKGBUILD function behaves as if in the wrong directory | PA7 | `man -P cat PKGBUILD \| grep -n 'This function is run inside'` |

## QUALITY check

- QUALITY 14 (novelty stated, not overstated): the lane held local `mtree` reads as a tool
  (`corpus/knowledge/snapper-eacces-mechanism.md:144`, `corpus/knowledge/degraded-triage-r4.md:599`) and
  `vercmp` for direction (`SKILL.md:1245`), never the rules PA1-PA8; the novelty tokens of
  `tools/check-package-anatomy-r41.py` have 0 hits at base `0e5805a1`.
- QUALITY 86 (rule rows verify on upstream rows): every rule cites a pinned upstream row (S227-S233); the
  host column is own-work capture only and states where it is unmeasured (PA2, PA3).
- QUALITY 81 (non-author verdict per row): each row is credited only with a committed reviewer verdict file
  under `.ufo/waves/round-41/`; the counter reads them.
- Spec and implementation differ on purpose and the entry keeps both: PA1 is the format document's "must be
  present", PA2 is what libalpm enforces. A package missing `.BUILDINFO` or `.MTREE` still loads.

## Corrections from the round-41 wave (append-only; the rows above stay as measured)

Five second-read seats returned `partly` (`.ufo/waves/round-41/w1/C2RevPA{2,3,5,6,7}b.md`); every first-read seat
returned `holds`. No row was judged wrong. Each correction below adds the condition the second reader found missing,
grounded on the pinned snapshot, and is the reading that replaces the row text where they differ.

- **PA2 — exact name, a fourth error, a later check.** The root entry must be named exactly `.PKGINFO`: the loader
  compares member names with `strcmp` (`be_package.c:598`), so a repack whose members carry a `./` prefix is refused
  with the same "missing package metadata" (seat C2RevPA2b, probe p4, `.PKGINFO` bytes identical to a loading
  package). A `.PKGINFO` that fails to parse is refused with "could not parse package description file"
  (`:600-604`). After the archive loop, `_alpm_pkg_check_meta` (`:678-680`; body outside the snapshot) can still
  refuse a package whose version passed the dash test (seat probe P13: a version with a second dash fails with
  "invalid metadata for package"). Decision-table row 1 reads accordingly: the listing must show a line that is
  exactly `.PKGINFO`; `./.PKGINFO` alone means the file will not load.
- **PA3 — `globstar`, and where the partial load stops.** `list_package_files` sets `globstar` as well as `dotglob`
  (`makepkg.sh.in:565`); the metadata sits first so long as no root name sorts before `.` in byte order. A partial load
  skips every `.`-prefixed entry before its stop test (`handle_simple_path`, `be_package.c:373-385`, then `continue`)
  and stops at the end of the first entry after `.PKGINFO` that is not `.`-prefixed, or at the end of the archive when
  no such entry follows (seat C2RevPA3b).
- **PA5 — what the kept `mtree` lists, and the bare pattern.** Besides `.BUILDINFO`, `.PKGINFO` and the data files the
  kept `mtree` also lists an `.INSTALL` or `.CHANGELOG` the package carries and the directory entries (host: 51 of
  1409 kept mtree files list `./.INSTALL`, seat C2RevPA5b receipts). `--exclude .MTREE` is a bare pattern that bsdtar
  matches at any depth, so a data file named `.MTREE` anywhere in the tree is also left out of the listing while the
  archive keeps it (seat reproduction; no host instance: 0 such files in `/var/lib/pacman/local/*/files`).
- **PA6 — `--quiet`, and `-Qp`.** The notice is printed only without `--quiet` (`check.c:317`); the return value is 0
  either way. The same `check_pkg_full` runs for `pacman -Qpkk <file>`: a loaded package file keeps libalpm's default
  mtree opener, so the archive's own `.MTREE` is never opened there and the "no mtree file" notice is printed although
  the file carries one (seat C2RevPA6b, `query.c:467-470`, receipts `C2RevPA6b/qkk-fixture-receipts.txt`).
- **PA7 — five named functions; two more run in `$srcdir` by makepkg.** The working-directory sentences cover the five
  functions PKGBUILD(5)'s Packaging Functions section names. It states no directory for the split-package
  `package_<name>()` functions (`PKGBUILD.5.asciidoc:400-404`) or for `pkgver()` (`:51-56`); makepkg runs both inside
  `$srcdir` (seat C2RevPA7b: `pkgver` at `makepkg.sh.in:192`; `run_function_safe` defaults its directory to `$srcdir`,
  `local workingdir="${2:-$srcdir}"` at `:414`), so the decision-table command finds no
  line for them.
- **PA6 — a third NULL path (residual seat C2RevPA6c).** `_cache_mtree_open` returns NULL by three paths
  (`be_local.c:251-283`): the file absent (`:258-261`, silent), the archive handle not allocatable (`:263-265`, no
  "error while reading file" log), and the open failing (`:270-275`, logged). All three reach the notice (unless
  `--quiet`) and `return 0`; the TODO at `check.c:316` conflates the three, not two. Appended after the residual
  verdict, which therefore did not judge this bullet.

## Round-42 note — packaging offset of the host build (appended 2026-10-26; considerthese/2026-10-26.md "Downstream patch-offset check")

The line pins above are upstream pacman 54d9411. The host runs the Arch build 7.1.0.r9.g54d9411-3, which applies four
packaging patches (wave-1 seat ConsiderPatchOffset, `.ufo/waves/round-42/w1/ConsiderPatchOffset.md`; check script and
output `.ufo/waves/round-42/w1/ConsiderPatchOffset/patch-offset.py`, `run.txt`): `patch-reproducible-builds.patch`
inserts 23 lines in `lib/libalpm/add.c` at :412, so every add.c line cited here after :417 is 23 lower in the built
tree (`add.c:466-474` reads `:489-497`); the reversed `revertme-makepkg-remove-libdepends-and-libprovides.patch`
restores 118 lines to `scripts/makepkg.sh.in` (`:560-569` reads `:678-687`) and 9 lines to
`doc/PKGBUILD.5.asciidoc` (`:345-377` reads `:354-386`). The statements are unchanged (the patched hunks do not touch
the cited logic, per the seat's pinned-vs-built comparison, `evidence.txt`); only the line numbers differ in the
binary's source. Re-run the check before citing a new line of a patched Arch build.
