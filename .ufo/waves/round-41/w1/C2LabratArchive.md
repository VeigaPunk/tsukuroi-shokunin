VERDICT: supports

# C2LabratArchive — item C2-28 (PA2 empirical labrat)

Hypothesis under test (item text): libalpm loads a package file that has `.PKGINFO` but neither
`.BUILDINFO` nor `.MTREE`, and refuses one without `.PKGINFO` with "missing package metadata" and one
whose pkgver lacks a dash with "invalid package version"; member order is also checked.

Result: all three legs held on the host binary, and the order question is answered (order does not
matter for `-Qpi`, because `-Qpi` performs a *full* load — measured, see F4). The corpus row
`corpus/knowledge/alpm-package-anatomy-r41.md:27` (PA2) is empirically supported, and its host cell
currently reading "unmeasured: the package cache is empty and pacman transactions are paused, so the
load path was read in source only" can be replaced by a measured statement (proposed text at the end).

## Binding the host binary to the pinned source

- `pacman -Q pacman` → `pacman 7.1.0.r9.g54d9411-3`; `pacman --version` → `Pacman v7.1.0 - libalpm v16.0.1`;
  `pacman -Q libarchive` → `libarchive 3.8.10-1`; `bsdtar 3.8.10 - libarchive 3.8.10`.
  The installed pacman is the pinned commit 54d9411 (corpus header names 7.1.0.r9.g54d9411-3).
- `strings -a /usr/lib/libalpm.so.16.0.1 | grep 'missing package\|invalid package version'` →
  `missing package name in %s`, `missing package version in %s`, `invalid package version in %s`,
  `missing package metadata in %s` — the four strings the pinned `be_package.c` emits, present in the
  loaded shared object.
- `sha256sum .ufo/waves/round-41/frozen/src/be_package.c` →
  `24e5890647f80dd953586d8add314b396d0276a37e2f1468f685e90b809db4d7`, equal to
  `frozen/src/SHA256SUMS:5`. The pinned source I cite and the binary I ran are therefore the same code.
- No transaction was opened and no lock file was created: `pacman -Qpi --debug` output contains zero
  lines matching `transaction|committing|installing`, and `/var/lib/pacman/db.lck` does not exist after
  the runs. Only `-Qpi`/`-Qpl` file queries were issued (read-only; sync and local db opened for reading).

## Method

17 bsdtar-built archives plus one genuine makepkg-built package, all under
`/fast/scratch/hyaku/tsukuroi-r41/C2LabratArchive/` (removed at the end; exact recipe saved as
`build-probes.sh` in this seat's receipt dir). Each was queried with `pacman -Qpi <file>` (and `-Qpl`
where the file list matters). Nothing was installed; no `-U`, no `-S`, no sudo.

## Observed results (exact)

| # | archive (members) | `-Qpi` | rc |
|---|---|---|---|
| A | `.PKGINFO`, `usr/share/toy/data.txt` — no `.BUILDINFO`, no `.MTREE` | prints full info, `Name : toy`, `Version : 1.0-1`, `Install Script : No`, `Validated By : None` | 0 |
| B | `usr/share/toy/data.txt` only | `error: missing package metadata in …/B-nometa.pkg.tar` + `error: could not load package '…': invalid or corrupted package` | 1 |
| C | `.PKGINFO` with `pkgver = 1.0` (no dash) | `error: invalid package version in …/C-badver.pkg.tar` + `could not load package … invalid or corrupted package` | 1 |
| D | data file first, `.PKGINFO` **last** | same info block as A | 0 |
| E | `.PKGINFO`, `.BUILDINFO`, data (no `.MTREE`) | same info block as A | 0 |
| F | `.PKGINFO`, gzip `.MTREE` listing only `usr/share/toy/phantom.txt`, data | info ok; `-Qpl` → `toy /usr/share/toy/phantom.txt` | 0 |
| G | `.PKGINFO`, gzip `.MTREE` with no entries, data | info ok; `-Qpl` → *(empty)* | 0 |
| H | `.PKGINFO`, plain-text garbage `.MTREE`, data | info ok; `-Qpl` → `toy /usr/share/toy/data.txt` | 0 |
| I | `.PKGINFO`, `.INSTALL`, data | `Install Script  : Yes` | 0 |
| J | `.PKGINFO` without `pkgname` | `error: missing package name in …` | 1 |
| K | `.PKGINFO` with `pkgver = ` (empty) | `error: missing package version in …` | 1 |
| L | member named `.pkginfo` (lower case) + data | `error: missing package metadata in …` | 1 |
| M | `.PKGINFO` with an unknown key `desc = …` | `warning: toy: unknown key 'desc' in package description`, then normal info | 0 |
| N | `.PKGINFO` with `pkgver = 1:1.0` (epoch, no dash) | `error: invalid package version in …` | 1 |
| P | `-`.MTREE (phantom mtree) first, `.PKGINFO`, data | info ok; `-Qpl` → `toy /usr/share/toy/phantom.txt` | 0 |
| R | makepkg's own `.PKGINFO`, `.MTREE`+`.BUILDINFO` stripped, `usr/` tree, zstd | info ok (`Name : toyl`, `Version : 1.0-1`); `-Qpl` → `/usr/`, `/usr/share/`, `/usr/share/toyl/`, `/usr/share/toyl/data.txt` | 0 |
| S | same tree with `.PKGINFO` removed, zstd | `error: missing package metadata in …S-real-shape-no-pkginfo.pkg.tar.zst` | 1 |
| real | `makepkg` output `toyl-1.0-1-any.pkg.tar.zst`, members in order `.BUILDINFO`, `.MTREE`, `.PKGINFO`, `usr/`, `usr/share/`, `usr/share/toyl/`, `usr/share/toyl/data.txt` | info ok; `-Qpl` lists the tree | 0 |

Receipts: `qpi-all.txt`, `qpl-all.txt`, `alpm-debug-and-real-order.txt`, `probe-sha256.txt`,
`build-probes.sh` (same directory as this report).

## Findings

**F1 — the minimal package really is `.PKGINFO` + data (A, R).** An archive carrying only `.PKGINFO`
(120 bytes: `pkgname`, `pkgver`, `arch`, `pkgdesc`, `url`, `size`) and one data file loads with rc 0
and a complete info block. `.BUILDINFO` and `.MTREE` are both absent. Corroboration: for the toy
archives `-Qpi` prints `Build Date : Wed 31 Dec 1969 09:00:00 PM -03` (no `builddate` key → epoch 0)
and `Packager : None`, `Validated By : None` — every key except name+version is optional. This is the
empirical form of `corpus/knowledge/alpm-package-anatomy-r41.md:62` ("A package missing `.BUILDINFO` or
`.MTREE` still loads") and of the source at `frozen/src/be_package.c:598-617` (only the `.PKGINFO`
branch sets `config = 1`).

**F2 — no `.PKGINFO` → "missing package metadata" (B, S, L).** Observed on both a one-member bsdtar
archive (B) and a zstd, real-shaped archive (S). Source: `be_package.c:652-653`
(`if(!config) { _alpm_log(… _("missing package metadata in %s\n"), pkgfile); }`). The second line
pacman prints, `invalid or corrupted package`, is `alpm_strerror(ALPM_ERR_PKG_INVALID)` — the row's
quoted string is the first line, and it is the one a user reads.

**F3 — a pkgver without a dash → "invalid package version" (C), and an epoch does not excuse it (N).**
`pkgver = 1.0` is refused (C). The additional probe `pkgver = 1:1.0` is refused with the *same*
message (N), because the check is a literal `strchr(newpkg->version, '-')` on the whole raw value
(`be_package.c:613-614`), not a parse of the epoch/version/release split. This sharpens the decision
table row at `corpus/knowledge/alpm-package-anatomy-r41.md:45`, which says the value must be
`pkgver-pkgrel` (with an optional `epoch:`) — the release and its dash remain mandatory even when an
epoch prefix is present. Empty values take their own messages (J: "missing package name", K: "missing
package version", `be_package.c:605-611`).

**F4 — `-Qpi` is a FULL load, and that is why the order question dissolves (D, P, F, G, H).**
`frozen/src/query.c:468` is the only call site of `alpm_pkg_load` in `frozen/src/` and it passes
`full = 1`:

```
alpm_pkg_load(config->handle, strname, 1, 0, &pkg);
```

with the signature at `be_package.c:725-726` (`int full, int level`). In the read loop the early exit is
`if((!full || hit_mtree) && config) break;` (`be_package.c:641-642`), so with `full = 1` the scan runs
to EOF unless a `.MTREE` was already seen. Consequence, measured:

- D (`.PKGINFO` last) and P (`.MTREE` before `.PKGINFO`) both return the full metadata block, rc 0 —
  **member order does not matter for `-Qpi`**.
- F proves the full load really consumes `.MTREE`: a gzipped mtree naming only
  `usr/share/toy/phantom.txt` makes `-Qpl` report that phantom file and stops the loader from scanning
  the real member (`be_package.c:619-623` rebuilds the file list from the mtree).
- G (valid mtree, zero entries) yields an empty `-Qpl` — the archive's own entries are never added
  because `hit_mtree` is already set.
- H (garbage `.MTREE`) degrades to the expensive path — `-Qpl` shows the real member, rc 0. The debug
  channel shows the failure and even the source location:
  `error while reading mtree of package … : Unrecognized archive format` then
  `got error 51 at build_filelist_from_mtree (../lib/libalpm/be_package.c: 497) : libarchive error`.
  Line 497 of the pinned snapshot is exactly that `GOTO_ERR(handle, ALPM_ERR_LIBARCHIVE, error)` — the
  installed library names the line I read. The user-visible result is silence: no error, rc 0.

**F5 — every other dot file is skipped, `.INSTALL` is not (I, L, M).**
`handle_simple_path` (`be_package.c:373-385`) sets `scriptlet = 1` for `.INSTALL` (I: `Install Script :
Yes`) and returns 1 for any other name beginning with `.`, which is why `.BUILDINFO` is passed over
(E loads without it) and why a lower-case `.pkginfo` is just another skipped dot file (L). An unknown
key inside `.PKGINFO` only warns (M: `warning: toy: unknown key 'desc' in package description`) and
the load proceeds with `Description : None` — the key is `pkgdesc`, and a bad key does not fail a load.

**F6 — the toy shape is the real shape (real package, R, S).** A genuine `makepkg -f -d --nocheck
--nodeps --nosign` build (offline PKGBUILD, no sources, run under the seat scratch, fakeroot only)
produced members in the order `.BUILDINFO`, `.MTREE`, `.PKGINFO`, `usr/`, `usr/share/`,
`usr/share/toyl/`, `usr/share/toyl/data.txt` — dot files first, matching PA3
(`corpus/knowledge/alpm-package-anatomy-r41.md:28`) without me having to trust a hand-made order.
Repacking that package with `.MTREE` and `.BUILDINFO` removed but makepkg's own `.PKGINFO` kept (R,
zstd) still loads, rc 0, and reproduces the file list; removing only `.PKGINFO` from the same tree (S)
gives the F2 error. Toy and real artifacts therefore agree, and compression (none vs zstd) is
irrelevant to the metadata scan.

## What this changes for the corpus (proposals only — I edited nothing)

1. PA2 host cell (`corpus/knowledge/alpm-package-anatomy-r41.md:27`, last column) is currently
   "unmeasured"; it can become a measured cell, for example:

   > measured on pacman 7.1.0.r9.g54d9411-3 with `pacman -Qpi` on scratch archives: a `.PKGINFO`+data
   > archive with neither `.BUILDINFO` nor `.MTREE` loads (rc 0), the same archive minus `.PKGINFO`
   > fails "missing package metadata" (rc 1), `pkgver = 1.0` fails "invalid package version" (rc 1),
   > and `.MTREE` is consumed on the `-Qpi` full load (a stale mtree's file list wins)

2. Decision table, "invalid package version" row (`corpus/knowledge/alpm-package-anatomy-r41.md:45`):
   append one clause so the epoch cannot be read as a substitute for the release —

   > — the value must be `pkgver-pkgrel` (with an optional `epoch:` prefix; the release and its dash
   > are required even with an epoch: `pkgver = 1:1.0` is refused as "invalid package version")

## Not done / limits

- No `full = 0` (partial) load was exercised: no caller in the pinned snapshot passes `full = 0`
  (`query.c:468` is the only `alpm_pkg_load` call site in `frozen/src/`), so PA3's "a partial load stops
  at the first entry after `.PKGINFO`" (`be_package.c:641`) remains source-read only here. It was not
  claimed as measured.
- `pacman -U` / sync-install paths were not run (transactions are paused host-wide by rule). The
  `-Qpi` path shares `_alpm_pkg_load_internal`, but the add path's own load flags were not observed.
- No signature verification was in play: `-Qpi` on an unsigned file prints `Validated By : None` and
  `Signatures : None` (see receipts), so nothing here speaks to signing.
- The package cache is empty (`ls /var/cache/pacman/pkg/` → no files), so no distribution-built package
  was used; R/S are makepkg-built on this host, not distro-built.
- I did not run any build, lint, test or counter for the wave; counters and gates belong to the L1.
