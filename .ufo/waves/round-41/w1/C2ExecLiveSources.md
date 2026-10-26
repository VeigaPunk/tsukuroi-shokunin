VERDICT: supports

Item C2-24 — live sources equal snapshots. Every URL in the frozen FETCH.txt re-fetched on 2026-10-26 returns bytes identical to `.ufo/waves/round-41/frozen/src/`, and every cited function body (plus the five PKGBUILD.5 function blocks) is unchanged between the pinned commit 54d9411 and pacman master. One correction to the working model, not to the claim: **54d9411 is not an ancestor of master** — it lives on `release/7.1.x`; that branch's tip has *zero* changes to any of the eight pinned files.

## 1. Live re-fetch vs snapshot

Method: `curl -sSfL --retry 3 -o <name> <url>` for all 9 URLs in `FETCH.txt` into `/fast/scratch/hyaku/tsukuroi-r41/C2ExecLiveSources/`, then `sha256sum -c` against a copy of the frozen `SHA256SUMS`, plus `cmp` against the frozen files.

```
PKGBUILD.5.asciidoc: OK   add.c: OK   alpm-package.7.raw: OK   be_local.c: OK
be_package.c: OK          check.c: OK makepkg.sh.in: OK        query.c: OK      version.c: OK
```
`cmp -s` on each of the 9 pairs: `IDENTICAL` for all 9 (receipt `.ufo/waves/round-41/w1/C2ExecLiveSources/receipts.txt` §1). Fresh digests, e.g. `15e8007bb11829b4d0474e647b0d08c2bffdf5191ceac949336de3d14a621154  PKGBUILD.5.asciidoc` and `24e5890647f80dd953586d8add314b396d0276a37e2f1468f685e90b809db4d7  be_package.c`, match `.ufo/waves/round-41/frozen/src/SHA256SUMS:1,5`.

The pin is the shipped binary's commit, not an arbitrary revision: `pacman -Q pacman` → `pacman 7.1.0.r9.g54d9411-3`; `git describe --tags 54d9411` → `v7.1.0-9-g54d94116`. Upstream confirms it is still current: `https://archlinux.org/packages/search/json/?name=pacman` → `core pacman 7.1.0.r9.g54d9411-3` (last_update `2026-10-15T13:42:46`), accessed 2026-10-26.

## 2. Topology correction (freshness-relevant)

From a filtered clone of `https://gitlab.archlinux.org/pacman/pacman.git` (receipts §2):

- `54d9411` = `54d94116164b0b2202c6061c4a59c6f3e70820d8` "libmakepkg: fix linting of xdata", author date 2026-01-07.
- master = `a6f7467d8c7c4d7e9cc846884e74c0ab7215c48d` "Prevent overflow when sorting package download order", author date 2026-01-25.
- `git merge-base --is-ancestor 54d9411 a6f7467d` → **rc=1**; merge base is `2df7c407` (v7.1.0). `git branch -r --contains 54d9411` → `origin/release/7.1.x`. `rev-list --count a6f7467d..54d9411` = 8, `rev-list --count 54d9411..a6f7467d` = 17: the two lines diverged at v7.1.0.
- `git diff --stat 54d9411 origin/release/7.1.x -- <the 8 pinned paths>` → **empty**. The only commit on the shipped branch after the pin is `cb7452f6` "Prevent overflow when sorting package download order", which touches none of the pinned files.

So the corpus cites a commit on the 7.1.x release branch, and everything it quotes is frozen on that branch. The `master` comparison that follows is therefore a *forward-compatibility* check, not a same-line check.

## 3. Cited functions: pinned 54d9411 → pacman master

Method: whole-body extraction on both sides — brace matching that skips C strings/chars/`//`/`/* */` for the C functions, `name() {` … matching `}` for the bash function, and the asciidoc definition-list body (label line … last tab-indented line) for the PKGBUILD.5 blocks — then byte comparison. Sanity of the extractor was asserted by markers that must be inside each body (`missing package metadata in %s`, `reserve all files starting with`, `no mtree file`, `different from RPM`, `always assume 0 epoch`, `LC_COLLATE=C`), all present on both sides, and by checking the byte after each extracted body is the next declaration (`be_package.c:695` starts `_alpm_pkg_load`, `add.c:190` starts `extract_single_file`).

| cited surface | pinned | master | body changed? |
|---|---|---|---|
| `_alpm_pkg_load_internal` (PA2) | `be_package.c:555-694` | `be_package.c:544-683` | **no** (140 lines both) |
| `extract_db_file` (PA4) | `add.c:168-189` | `add.c:168-189` | **no** (22 lines both) |
| `check_pkg_full` (PA6) | `check.c:295-435` | same | **no** — file byte-identical |
| `parseEVR` (PA8) | `version.c:39-75` | same | **no** — file byte-identical |
| `alpm_pkg_vercmp` (PA8) | `version.c:219-260` | same | **no** — file byte-identical |
| `list_package_files` (PA3/PA5) | `makepkg.sh.in:562-569` | `:562-569` | **no** (8 lines both) |
| `*package() Function*::` (PA7) | `PKGBUILD.5.asciidoc:345-351` | `:350-356` | **no** (415 chars both) |
| `*verify() Function*::` (PA7) | `:353-357` | `:358-362` | **no** (285 chars) |
| `*prepare() Function*::` (PA7) | `:359-365` | `:364-370` | **no** (362 chars) |
| `*build() Function*::` (PA7) | `:367-370` | `:372-375` | **no** (204 chars) |
| `*check() Function*::` (PA7) | `:372-377` | `:377-382` | **no** (300 chars) |

`check.c`, `query.c` and `version.c` are byte-identical to master at all (`cmp`), so nothing in PA6/PA8 moves at all.

What *did* change in the eight files since 54d9411 (receipts §3), all outside every cited body:

- `lib/libalpm/be_package.c` +0/−11 — `bdedf621` "Drop md5sum support from repo databases" (2025-11-17), one hunk in `_alpm_pkg_validate_internal`, pinned lines `318-328` → master `317`, removing the `syncpkg->md5sum` branch. `_alpm_pkg_load_internal` is untouched.
- `lib/libalpm/be_local.c` +0/−5 — same commit, hunks at `:796` (`local_db_read`, validation keyword parsing) and `:1061` (`_alpm_local_db_write`). The PA4-PA6 supporting window `be_local.c:251-270` is untouched and still at `251-270`.
- `lib/libalpm/add.c` +24/−1 — `f4bdb774` "lib: support reproducible install date" (2024-08-17): adds a new `get_install_time()` before `commit_single_pkg` and swaps `newpkg->installdate = time(NULL)` for it. No effect on `extract_db_file`.
- `scripts/makepkg.sh.in` +2/−2 — `2c3146dc` "Add Sccache support." and `fd97639c` "makepkg: fix generation of \"--allsource\" packages with VCS sources", both at the `prepare_buildenv` call sites (`:1254`, `:1406`), not in `list_package_files`.
- `doc/PKGBUILD.5.asciidoc` +5/−0 — `2c3146dc`, an `*sccache*;;` options entry inserted at `:289`; the five function blocks are unchanged but shifted +5.

Cited-window drift (receipts §6): every window still holds its exact text; only offsets after a deletion move — `be_package.c:598-654` → master `587-643`, `PKGBUILD.5.asciidoc:345-377` → `350-382`, `:439-441` → `444-446`. The other windows (`add.c:168-189`, `be_local.c:251-270`, `version.c:39-255`, `check.c:295-321`, `query.c:317-321`, `makepkg.sh.in:560-569`, `:615-620`, `alpm-package.7.raw:100-120`) sit at unchanged line numbers.

## 4. alpm-package(7) row (PA1) — the one non-pacman URL

The FETCH URL `https://man.archlinux.org/man/alpm-package.7.raw` carries no commit pin, so it is the only genuinely moving target in the set; today it still hashes to the frozen `b551bb392f6899c89c4c0d5778c89ad482f0c1251260ccf336bd5b5ed2693c45`.

Provenance checked one step further than the byte compare:
- `https://archlinux.org/packages/search/json/?name=alpm-docs` → `extra alpm-docs 0.13.0-1`, last_update `2026-10-15T16:10:43` — the version the declaration names is current.
- `archlinux/packaging/packages/alpm-docs` `PKGBUILD:4-21` (`https://gitlab.archlinux.org/archlinux/packaging/packages/alpm-docs/-/raw/main/PKGBUILD`, accessed 2026-10-26): `pkgver=0.13.0`, source tag `$_upstream_project/$pkgver` with `_upstream_project=alpm-types`, i.e. tag `alpm-types/0.13.0` of `https://gitlab.archlinux.org/archlinux/alpm/alpm.git`.
- In that monorepo (project 84858, default branch `main`): `git log alpm-types/0.13.0..origin/main -- resources/docs/src/specifications/alpm-package.7.md` → **no commits**, and both `resources/docs/src/specifications/alpm-package.7.md` and `alpm-package/resources/specification/alpm-package.7.md` are byte-identical at the tag and at `main`. The sentence PA1 quotes is at line 56 of the tag's markdown: "The following files must be present at the root of an ALPM based package:".
- Caveat recorded: `alpm-docs` is not installed here (`pacman -Q alpm-docs` → `error: package 'alpm-docs' was not found`), so PA1's text is verified against the Arch man rendering plus upstream source, not against a local installed page.

## 5. What this does and does not settle

- Settles: the snapshots are faithful to live upstream today; the pin is the shipped 7.1.0.r9.g54d9411-3 commit; no cited C function or PKGBUILD.5 function block has changed since the pin on either the release branch or master; the only upstream movements in those files are md5sum removal, reproducible install date, and sccache, none of which touch a claim row.
- Does not settle: semantics. Identical bytes say nothing about whether PA1-PA8 *read* the source correctly — that is the row-verdict seats' job. I also did not diff functions outside the cited set, and did not verify the pinned snapshot against a signed dist tarball (`v7.1.0` tag only anchors the branch point).
- Risk for anyone re-citing: master line numbers are not the pinned line numbers after `:316` in `be_package.c` and after `:289` in `PKGBUILD.5.asciidoc`. Cite the pinned commit, as the corpus does.

## Scope and hygiene

Read-only throughout: no lane file written except this report and `.ufo/waves/round-41/w1/C2ExecLiveSources/receipts.txt`; no git/jj mutation in the lane, no host change, no pacman transaction, no unshare; all clones and downloads under `/fast/scratch/hyaku/tsukuroi-r41/C2ExecLiveSources/` (removed at the end, receipts copied out first). No tool installed or upgraded.
