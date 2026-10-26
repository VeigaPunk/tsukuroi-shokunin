## Package anatomy and the local database — round 41

Appended 2026-10-26 (round-41 C2; drafted by wave seat C2ScribeSkill, integrated by the L1). The `-Qkk`
subsection above classifies what a sweep prints; this section answers the question underneath it: what a package
file carries, what libalpm requires of one on load, what install keeps in `/var/lib/pacman/local/`, and what the
kept copy is worth to `-Qkk` and to version comparison. Rules PA1-PA8 with their quotes:
`corpus/knowledge/alpm-package-anatomy-r41.md` (source rows S227-S236 — alpm-package(7) from alpm-docs 0.13.0-1,
pacman `54d9411` as built by `7.1.0.r9.g54d9411-3`, an own-work host capture; snapshots
`.ufo/waves/round-41/frozen/src/`, digests in its `SHA256SUMS`; capture `.ufo/waves/round-41/frozen/hostcap/`,
MANIFEST sha256 `632ed0443cfb26ef002ebfd2a3a99971221f9129836b63135e0ca6ea41874f89`, captured
2026-10-26T16:14:04Z). Entry carried by commit `9cc9aa77e30e0e23de2d4d2697b3b218ada02969`. Detection and report
only: nothing below installs, builds, removes or re-packs a package.

Measured on this host, 2026-10-26, read-only, `pacman 7.1.0.r9.g54d9411-3`, `ALPM_DB_VERSION` 9: 1409 local
entries (`pacman -Q | wc -l`) and 1409 kept `mtree` files, 51 kept `install` files, 0 `changelog`, 0 other root
dot files; all 1409 `mtree` files gzip (`1f 8b`), none listing `./.MTREE`; the kept `mtree` of `pacman` opens
with `./.BUILDINFO` and `./.PKGINFO` and holds 428 entries; kept `mtree` and `install` are mode `0644 root:root`;
`man -P cat PKGBUILD` prints 5 `This function is run inside` lines (4 `$srcdir`, 1 `$startdir`); `vercmp
1:1.0-1 2.0-1` = 1, `vercmp 0:2.0-1 2.0-1` = 0, `vercmp 1.0 1.0-5` = 0, `vercmp 1.0-1 1:0.1-1` = -1.
`/var/cache/pacman/pkg` holds 0 files (`pacman-conf CacheDir` = that directory) and a bounded `find` over
`/var/cache`, `/var/lib`, `~/Downloads` and `~/Projects` (`-maxdepth 3 -name '*.pkg.tar.*'`) found no package
file, so the `bsdtar` commands below ran only on a synthetic four-member archive built in scratch: they read
member order and `.PKGINFO` fields there, but their rule content is the pinned source, not that fixture.

### Symptom → PA row → read-only command → what the output means

| Symptom (verbatim string or observation) | Row | Command (read-only, paste-ready) | What the output means |
|---|---|---|---|
| An archive is called invalid because `.BUILDINFO` or `.MTREE` is missing | PA1 (S227 `alpm-package.7.raw:100-120`) | `bsdtar -tf <pkg-file> \| sed -n '1,4p'` | The document requires `.BUILDINFO .MTREE .PKGINFO` at the root and allows an optional `.INSTALL`; a missing `.BUILDINFO` or `.MTREE` is a format defect, **not** a load failure, because libalpm needs only `.PKGINFO` (PA2). The dot members survive where the kept `mtree` shows them: `./.BUILDINFO` and `./.PKGINFO` |
| `missing package metadata in <file>`, or `invalid package version`, on `pacman -U` or a sync install | PA2 (S228 `be_package.c:598-654`) | `bsdtar -xOf <pkg-file> .PKGINFO \| grep -e '^pkgname' -e '^pkgver'` | `.PKGINFO` present means the archive loads at all; its `pkgver` must carry the release after a dash with an optional `epoch:` prefix, and an empty name or version is refused at the same point. `.MTREE` is read only on a full load to build the file list; `.BUILDINFO` is passed over like every other unhandled dot file |
| A package built under a non-C locale starts with data files, or a partial read never saw `.MTREE` | PA3 (S229 `makepkg.sh.in:560-569`; `be_package.c:640-643`) | `bsdtar -tf <pkg-file> \| head -n 3` | makepkg lists members under `LC_COLLATE=C` with bash `dotglob`, so the dot files sort ahead of the data files and sit at the archive's start; a load that is not full stops at the end of the first entry after `.PKGINFO`, so order decides whether `.MTREE` is ever read. Data files first means the archive was not built by the pinned makepkg, or was re-packed |
| A scriptlet cannot be found after install, or `pacman -Qi` prints `Install Script : No` although the PKGBUILD has one | PA4 (S230 `add.c:168-189`) | `pacman -Qi <pkg> \| grep -E '^(Name\|Version\|Install Script)'; ls /var/lib/pacman/local/<name>-<version>/` | Install keeps `.INSTALL` as `install`, `.CHANGELOG` as `changelog` and `.MTREE` as `mtree`, each mode 0644, and skips every other root dot file — `.PKGINFO` and `.BUILDINFO` are never in the entry. `Install Script : No` is the absence of a kept `.INSTALL`, not of a scriptlet in the PKGBUILD. Measured: 51 of 1409 entries carry `install`, 0 `changelog`, 0 any other dot file |
| A kept `mtree` opens as binary, or an installed file is not listed in it | PA5 (S229 `makepkg.sh.in:615-620`) | `head -c2 /var/lib/pacman/local/<name>-<version>/mtree \| od -An -tx1; zcat /var/lib/pacman/local/<name>-<version>/mtree \| sed -n '1,3p'` | The first two bytes are `1f 8b` (gzip) on all 1409 here, and the listing opens with `#mtree` and a `/set` line; every file line carries a `sha256digest`, and `.MTREE` is excluded from its own listing (0 of 1409 list it) |
| `pacman -Qkk <pkg>` prints `<pkg>: no mtree file` and nothing else | PA6 (S231 `check.c:295-321`) with PA4 | `pacman -Qkk <pkg>; echo rc=$?` | The full check opens the kept `mtree`; with the file absent it prints the notice and returns 0, so the package adds zero errors and its clean result verified nothing. The same return covers a file that fails to open (a TODO leaves the two cases unseparated). `-Qk` (level 1) still checks file existence |
| A packaging function edits files as if in the wrong directory | PA7 (S232 `PKGBUILD.5.asciidoc:345-377`) | `man -P cat PKGBUILD \| grep -n 'This function is run inside'` | `package()`, `prepare()`, `build()` and `check()` run inside `$srcdir`, `verify()` inside `$startdir`, and `package()` also under fakeroot while the others run as the calling user. Host: 5 lines, 4 `$srcdir` and 1 `$startdir` — a `verify()` that assumes `$srcdir` is the documented exception, not a bug |
| An upgrade offers a version that looks lower than the installed one | PA8 (S233 `version.c:39-255`) | `pacman -Qi <pkg> \| grep '^Version'; vercmp <installed> <offered>` | Epoch first (an absent epoch counts as 0), then the version, then the release only when both strings carry one — any `1:` build outranks every epoch-0 build, `1.0` equals `1.0-5`, and `1.0-1` sorts below `1:0.1-1`. `vercmp` prints `1` / `0` / `-1` for greater / equal / lower and its exit status was `0` for all three on this host (measured 2026-10-26) — read the printed value, never `$?` |

### Checklist step — count local entries without mtree before trusting a clean `-Qkk`

Run this as step 4a of the update-safety checklist, before its integrity sample and full sweep, and whenever a
sweep or the census returns `0 altered` or `drift=0`:

```bash
for d in /var/lib/pacman/local/*/; do [ -f "$d/mtree" ] || echo "$d"; done | wc -l
```

- `0` (this host, 2026-10-26: 1409 entries, 1409 `mtree` files) — every local entry carries the kept `mtree`, so
  a clean `-Qkk` on it verified file contents instead of reporting a vacuous pass.
- `N > 0` — each printed entry's full check verified nothing: `-Qkk` prints `<pkg>: no mtree file` and returns 0
  (PA6), so that entry contributes zero errors to the sweep and cannot be cited as clean. `-Qk` still checks it.
- Run the loop under bash: GNU bash 5.3.20 (`/usr/bin/bash`) and `/bin/sh` print `0` here; a shell whose
  trailing-slash pattern also expands regular files printed `1`, and its one word was
  `/var/lib/pacman/local/ALPM_DB_VERSION/` — the database-version file, not a package entry. A word that is not a
  `<name>-<version>` directory is not a finding.

Reproduce the branch on a copy, never on the live database (measured 2026-10-26):

```bash
S=$(mktemp -d); mkdir -p "$S/db/local"
cp /var/lib/pacman/local/ALPM_DB_VERSION "$S/db/local/"
cp -r /var/lib/pacman/local/7zip-26.04-1 "$S/db/local/"
rm "$S/db/local/7zip-26.04-1/mtree"
pacman -Qkk --dbpath "$S/db" 7zip; echo "rc=$?"
```

Without the `mtree`: `7zip: no mtree file`, `rc=0`. With it: `7zip: 17 total files, 0 altered files`, `rc=0`.
`pacman -Qk --dbpath "$S/db" 7zip` prints `7zip: 17 total files, 0 missing files` in both states. The version
file must sit inside `local/`; beside it, `--dbpath` answers `database is incorrect version`.

The census sample inherits the blind spot: `tools/tsukuroi-census.sh:684` runs `pacman -Qkk` over a bounded
sample (8 by default, `--sample N`), and `:698-700` sums only `N total files, M altered files` summaries, so a
sampled entry without `mtree` adds 0 to `drift=` and its `no mtree file` line is counted nowhere. Read the
sample's `drift=` next to this count, never alone.

### Limits of this section

- **PA2 and PA3 are unmeasured on this host**, as the entry states: `/var/cache/pacman/pkg` holds 0 files
  (`pacman-conf CacheDir` = that directory, measured 2026-10-26) and pacman transactions are paused, so no package
  file could be opened. Those rows rest on the pinned snapshot, and their `bsdtar` commands ran only on a
  synthetic archive (member order and two `.PKGINFO` fields, not a makepkg-built package). PA1's host cell is the
  kept `mtree` of `pacman` — the members that survive install, not the archive.
- **The PA6 reproduction is a copy of one entry** (`7zip-26.04-1`) in a scratch `--dbpath`, not a live sweep. It
  shows the branch and its return code; it does not say what a mixed sweep prints, and it does not explain why an
  `mtree` would be missing on a real host — no local entry here lacks one.
- **Counts are a snapshot.** 1409 entries / 1409 `mtree` / 51 `install` / 0 `changelog` / 0 other dot files were
  true on 2026-10-26 and move with every install; the pinned form is capture S236
  (`.ufo/waves/round-41/frozen/hostcap/`, MANIFEST sha256 `632ed044…`). `ALPM_DB_VERSION` is 9.
- **Entry directories carry the epoch colon** (`blender-17:5.2.2-3`, `alsa-card-profiles-1:1.6.9-1`), so quote a
  `/var/lib/pacman/local/<name>-<version>/` path wherever it is used in a loop or a shell word.
- **A `desc`/`files`/`mtree` entry is not an incomplete install.** All 1409 entries carry `desc` and `files`
  beside `mtree`; `.PKGINFO` and `.BUILDINFO` are skipped by design (PA4), so their absence from the local entry,
  and a missing `install` or `changelog`, are the normal shape.
- **`-Qkk` is only as good as the kept `mtree`.** The kept file is opened with every decompression filter and the
  mtree format (S234), so a gzip header is not itself a failure mode; and the full check reports `N total files,
  M altered files` over the files that listing names.
- **The counter scores the entry, not this section.** `package-anatomy-r41` (gate registry, `SKILL.md:3121`)
  verifies PA1-PA8's rule cells, quotes inside frozen source windows and six host values from the frozen capture;
  it does not read this table, and its lexical half is a shape gate — a relation-literal writer passes it (control
  C2-K2), so the per-row reviewer verdicts are the read (QUALITY 81).

Counting: `python3 tools/check-package-anatomy-r41.py --revision <REV> [--repo <PATH>]` — 0 when PA1-PA8 each
carry the source-derived value, the frozen proposition relations and no negation word, a 4-25 word quote inside
the row's frozen source window on a new mined upstream row opened 2026-10-26, no duplicate row or heading, the six
capture-derived host values, 0 base hits of the novelty tokens and a committed non-author verdict per row; 1
otherwise; 2 on revision, git or frozen-input failure. Frozen sha256
`c83e29a4f570422d5a975873460c4c5b061e33ac497b97d13c1383569ac1819f`.
