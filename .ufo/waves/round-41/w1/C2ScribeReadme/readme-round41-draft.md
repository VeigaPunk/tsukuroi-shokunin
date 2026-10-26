## Round 41 — ALPM package anatomy; four mount-table cases in the census selftest (2026-10-26)

Append-only (drafted by wave seat C2ScribeReadme, integrated by the L1); the coverage map and Frontier bullets above
stay as written. The C2 entry deepens the held pacman-state plane (`../PROVINCE.md:8-9`, "`.pkg.tar.zst` receipt
discipline") on its package-file side and is not new coverage: it states what a package archive carries, what libalpm
requires of it on load and what install keeps in the local database, where `knowledge/pacman-transaction-order-r39.md`
(TO1–TO8) states where a package's scriptlets and files sit in a transaction, `knowledge/pacman-exec-environment-r40.md`
states the environment they run in, and `knowledge/pacman-backup-files-r35.md` states how `backup` files become
`.pacnew`/`.pacsave`. The C1 change adds four mount-table cases to the census `--selftest` (`run_selftest`;
`probe_storage_arm` untouched, commit `568c397d`, +27 lines in one hunk), a test-surface repair inside the round-38
storage arm above, not a new coverage surface.

| Note | Holds | Sources |
|---|---|---|
| `knowledge/alpm-package-anatomy-r41.md` | The package-file side of the pacman-state plane at pacman `54d9411` as built by Arch `7.1.0.r9.g54d9411-3`, with alpm-package(7) from `extra/alpm-docs 0.13.0-1`, deepening the plane whose transaction position is `knowledge/pacman-transaction-order-r39.md` (TO1–TO8), whose exec environment is `knowledge/pacman-exec-environment-r40.md` and whose `backup` handling is `knowledge/pacman-backup-files-r35.md`: the format's required root members `.BUILDINFO` `.MTREE` `.PKGINFO` plus optional `.INSTALL` (PA1); libalpm requires only `.PKGINFO` on load — a file with no `.PKGINFO` root entry fails with "missing package metadata", an empty name or version is refused, a version without a dash is refused, `.MTREE` is read only on a full load and `.BUILDINFO` is passed over like every other unhandled dot file (PA2); makepkg lists with `LC_COLLATE=C` and bash `dotglob`, so the dot files sort ahead of the data files and the metadata sits at the beginning of the archive (PA3), while the partial load's stop is the loader's — the first non-dot entry after `.PKGINFO` (`be_package.c`, S228); install keeps `.INSTALL`/`.CHANGELOG`/`.MTREE` as `install`/`changelog`/`mtree` (mode 0644) in the local database entry and skips every other root dot file, `.PKGINFO` and `.BUILDINFO` included (PA4); `.MTREE` is a gzip mtree listing that excludes itself (PA5); `pacman -Qkk` runs `check_pkg_full` on the kept mtree, and a missing or unopenable mtree returns 0 with the "no mtree file" notice (silent under `--quiet`), so the package adds zero errors (PA6); PKGBUILD(5)'s Packaging Functions section gives the working directory of the five functions it names — `package()`/`prepare()`/`build()`/`check()` in `$srcdir`, `verify()` in `$startdir`, `package()` under fakeroot — and none for the split `package_<name>()` or `pkgver()` (PA7, packaging-side); vercmp order — epoch (absent = 0), then version, then release only when both carry one, so any epoch 1 build outranks every epoch 0 build and `1.0` equals `1.0-5` (PA8); the host column reads this host's local database (1409 entries: mtree 1409 of 1409, install 51 of 1409, changelog 0, dot files 0, mtree gzip 1409 of 1409, self-listed 0), its `vercmp` and its `man PKGBUILD` | S227–S236 in `../SOURCES.md` (nine pinned upstream documents — alpm-package(7), `be_package.c`, `makepkg.sh.in`, `add.c`, `check.c`, `PKGBUILD.5.asciidoc`, `version.c`, `be_local.c`, `query.c` — plus the own-work capture `.ufo/waves/round-41/frozen/hostcap/`, `MANIFEST.sha256`); `lessons/round-41.md` Gate (rows S227–S236 and the assimilation re-grounding that meets round 38's flip); counter `../tools/check-package-anatomy-r41.py` (frozen at `e479fdc5`, sha256 `c83e29a4…`); `../SCORECARD.md` "Round 41 — declaration" |

### Frontier notice — round 41

Round 41 promotes nothing, and the C2 entry is Core depth rather than new ground. The pacman-state plane was Core before
this round — `../PROVINCE.md:8-9` owns "pacman state (`pacman -Qkk` verify loops, foreign/AUR census, `.pkg.tar.zst`
receipt discipline)" — and the row above states the package-file side of that ownership, beside the plane's older anchor
`knowledge/package-state-plane.md` (`corpus/README.md:7`). What is new is the statement, not the surface: the lane held
how a transaction orders a package's scriptlets and files, the environment they run in and how `backup` files drift
(`knowledge/alpm-package-anatomy-r41.md:7-13`), and no statement of the archive itself, so PA1–PA8 are the first statement
of it on an already-owned surface. Seven of the eight rows are host-state depth — a package file as a receipt (PA1–PA3,
PA5), the local database (PA4), the `-Qkk` loop (PA6) and the version comparison (PA8); PA7 states a build recipe, is
retained for the round-38 flip condition (`corpus/lessons/round-38.md:49`) and is not counted here as Core depth. No
Frontier area moves: the round-26 rule is that a Frontier area becomes Core only after a read-only census arm reads it
(`corpus/README.md:243`), and nothing here adds one — C1 edits `run_selftest` only and leaves `probe_storage_arm` as it
stood (`../SCORECARD.md` "Round 41 — declaration"), so the storage items are unchanged as well (the scrub record and NVMe
SMART stay Frontier, `../PROVINCE.md:234`; the namespace-sensitive STORAGE reading keeps its limit, `corpus/README.md:315`).

Three limits stay open. First, PA2 and PA3 are recorded host-unmeasured in the entry
(`knowledge/alpm-package-anatomy-r41.md:27-28`): the package cache is empty and the fleet's pacman pause stands
(`knowledge/pause-lift-gate-r24.md:11-12`, which authorizes no lane to run a transaction). Part of that moved anyway: the
wave's PA2 verdict seat measured the load path read-only on scratch package files with `pacman -Qp` — no cache and no
transaction — and found three conditions the row does not name, the loader's exact match on the `.PKGINFO` entry name
among them (`.ufo/waves/round-41/w1/C2RevPA2b.md`), so that cell records the author's method, not a limit of the
read-only lane; PA3's archive order stays unmeasured. Second, PA6's zero-error branch has no instance here — the kept
mtree is present for 1409 of 1409 entries (`knowledge/alpm-package-anatomy-r41.md:31`) — and the same check fires for a
package file queried with `-Qp`, where no kept mtree exists to check (`.ufo/waves/round-41/w1/C2RevPA6b.md`). Third, the
cache-shape anchor in the round-1 row above (`corpus/README.md:7`, "cache shape (8.6 G, never pruned)") is history, not
current state; it stays as written, and a package-file observation of PA2 or PA3 is operator-owned, not a lane action.
The round's per-row credit is the wave's read and not a promotion: a row counts only with a committed reviewer verdict
file (`QUALITY 81`, `knowledge/alpm-package-anatomy-r41.md:59`), and the round's non-author closure is pending
(`lessons/round-41.md:64`).

The Sources pointer for the new row also includes `lessons/round-41.md` Gate (rows S227–S236 and the assimilation
re-grounding of the staged `alpm-package-anatomy-r26.md` theme, which admits PA1, PA7 and PA8 re-grounded and keeps the
`package()`-in-`$pkgdir` sentence rejected).
