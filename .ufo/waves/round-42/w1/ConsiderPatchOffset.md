VERDICT: defect-found

# K-1 — Downstream patch-offset check (round 42, w1, seat ConsiderPatchOffset)

Item: `considerthese/2026-10-26.md:23` — "*Downstream patch-offset check.* Round 40 found an Arch patch
shifts util.c lines after :675 by +5. I could flag any knowledge anchor that cites upstream line numbers
for code the host runs as a patched Arch build, so line pins don't silently drift."

Result: the check exists now (`patch-offset.py`, 108 cited pins, 15 drifting) and it falsifies the implicit
assumption that only util.c drifts. Three of the newest entries' line pins point at lines that do not exist
at those numbers in the build the host runs:

| note | cited | built line | cause |
|---|---|---|---|
| r39 `pacman-transaction-order` | `add.c:466-474` (and 6 more rows) | `:489-497` (+23) | `patch-reproducible-builds.patch` |
| r41 `alpm-package-anatomy` | `makepkg.sh.in:560-569` | `:678-687` (+118) | reversed `revertme-…libdepends` patch |
| r41 `alpm-package-anatomy` | `PKGBUILD.5.asciidoc:345-377` | `:354-386` (+9) | same reversed patch |
| r40 `pacman-exec-environment` | `util.c:677-687` | `:682-692` (+5) | `0001-libalpm-invalidate-curl-data-in-child.patch` — **already recorded** in r40 |

The r40 annex's own statement is reproduced exactly, including its boundary (`:675` itself does not move);
what is missing is the same treatment for `add.c`, `makepkg.sh.in` and `PKGBUILD.5.asciidoc`, which no note
records. btrfs-progs and systemd pins come out clean (F5, F6).

## What the check does

`python3 .ufo/waves/round-42/w1/ConsiderPatchOffset/patch-offset.py --cache <scratch>/cache`
(23 s warm cache, ~2 min cold; stdlib only, `patch` and `pacman -Qi`; read-only — it copies pinned blobs
into the cache and applies patches only there).

1. `pacman -Qi <pkg>` (read-only) gives the installed version, which is also the Arch packaging tag.
2. The PKGBUILD at that tag gives `source=()`: the upstream ref plus the patch list, applied in array order
   (`PKGBUILD:90-102` of the pacman build). A source name starting with `revertme-` is applied as
   `patch -RNp1` (PKGBUILD:97-99), so its hunks are reversed before use.
3. Each cited file is copied from the pinned upstream ref into the cache and the patches that name it are
   applied there; the cited line is then located by its own text. `shift +N -> :M` in the table is observed,
   not modelled (18 rows). A hunk replay with the offsets `patch` reports covers the remaining rows (4).
4. Cited pins are extracted from the note set the seat was given: `corpus/knowledge/*-r38..r41.md`
   (pacman), `btrfs-scrub-record-r42.md` (btrfs-progs), `journalctl-v262-field-filter-r36.md`
   (systemd v262, the only systemd source pins in the corpus; flagged as outside the r38-r42 window).

Columns are the ones the item asked for: `pkg | upstream pin | cited file:line | arch tag |
patches touching it | line-shift risk`.

## Host builds and their packaging (F1)

```
$ pacman -Qi pacman btrfs-progs systemd | grep -E '^(Name|Version)'
Name : pacman        Version : 7.1.0.r9.g54d9411-3
Name : btrfs-progs   Version : 7.1-1
Name : systemd       Version : 262-1
```
receipt `w1/ConsiderPatchOffset/host-and-packaging.txt`.

The pacman PKGBUILD at tag `7.1.0.r9.g54d9411-3` pins `_git_tag=7.1.0` **and**
`_git_patch_level_commit=54d94116164b0b2202c6061c4a59c6f3e70820d8` (PKGBUILD:8-9) and rebases onto that
commit (PKGBUILD:80-86) — so the commit the lane cites is an Arch patch-level commit, and the pinned
tree the notes read is exactly the tree the four packaging patches are applied to next (PKGBUILD:51-55,
four `.patch` entries, two fetched from pacman commits, two shipped in the packaging repo). The host's
source tree is therefore `54d9411 + 4 patches`, never bare upstream.

## Pacman drift (F2, F3, F4)

**F2 — `lib/libalpm/add.c` shifts +23 (r39, 7 distinct line pins).** `patch-reproducible-builds.patch` (commit
f4bdb77, `w1/ConsiderPatchOffset/patches/pacman-remote-f4bdb77.patch`) has `@@ -412,6 +412,29 @@` on
`lib/libalpm/add.c`: 23 inserted lines at :412, no offset reported by `patch`. Every add.c row of
`pacman-transaction-order-r39.md` sits after that (the note's only early anchor, `add.c:168-189` in r41,
is before it and does not move; the note's `add.c:616-636` shares the :616 start and moves the same +23):

| r39 cited (upstream 54d9411) | built line |
|---|---|
| `add.c:466-474` | `:489-497` |
| `add.c:468-469` | `:491-492` |
| `add.c:470-474` | `:493-497` |
| `add.c:616-648` | `:639-671` |
| `add.c:669-688` | `:692-711` |
| `add.c:670-687` | `:693-710` |
| `add.c:676-692` | `:699-715` |

Spot check (`w1/ConsiderPatchOffset/evidence.txt`): pinned `add.c:616` is `\tswitch(event.operation) {`
and so is built `:639`; the same text does not sit at built :616.

**F3 — `scripts/makepkg.sh.in` shifts +118 and the built makepkg is not the pinned makepkg (r41, 3 rows).**
The packaging *reverts* commit 354a300 ("makepkg: remove libdepends and libprovides") with
`patch -RNp1` (PKGBUILD:97-99). Applied to the r41 frozen snapshot, `patch` reports
`offsets [6, 8]` — the patch's own anchors are stale against 54d9411 — and the result restores
`find_libdepends()` at :472 and `find_libprovides()` at :537, called from `write_pkginfo` at :628-629.
The pinned r41 snapshot contains **zero** occurrences of either function. Consequently:

| r41 cited | built line |
|---|---|
| `makepkg.sh.in:560-569` | `:678-687` |
| `makepkg.sh.in:565` | `:683` |
| `makepkg.sh.in:615-620` | `:733-738` |

This is more than an offset: the host's makepkg computes `depends`/`provides` from the built binaries, and
any note that describes `write_pkginfo` from the pinned file describes a function the host does not run in
that form. The lane mentions none of this — `grep -rn 'libdepends\|libprovides\|revertme' corpus/ tools/
SCORECARD.md LOG.md` returns 0 (`evidence.txt`).

**F4 — `doc/PKGBUILD.5.asciidoc` shifts +9 (r41, 2 rows).** Same reversed patch, `offsets [-7, -7]`:
`:345-377` → `:354-386`, `:400-404` → `:409-413`; `:67-74` is before both hunks and does not move.
The r40 util.c claim is reproduced (`0001…` applies clean, `util.c:677-687` → `:682-692`, `:688-698` →
`:693-703`, `:698-700` → `:703-705`, and `:675` identical at `:675` because the insertion follows it), so
the r40 annex needs no correction; the defect is that the same paragraph was never written for r39 and r41.

## Clean packages (F5, F6)

**F5 — btrfs-progs 7.1-1 patches nothing.** The packaging tree at tag `7.1-1` has no `*.patch`
(`host-and-packaging.txt`), `source=()` holds only the git tag plus `initcpio-*`, `btrfs-scrub@.{service,timer}`,
and `prepare()` applies a patch only when a source entry ends in `.patch`. The pinned blobs are byte-identical
to what is built: fetched `?h=v7.1` digests equal the round-42 frozen `SHA256SUMS` —
`scrub.c 48df2e2f468f7db79…`, `CHANGES bd881ab899ba4f4f…`. So every `S237 scrub.c:NNN` / `S238 CHANGES:NNN`
row in `btrfs-scrub-record-r42.md` (28 pins) is exact for the binary the host runs, and the note's own
`verified-at` commit `4ab0e80b…` is the peeled commit of that tag.

**F6 — systemd 262-1 patches no cited file.** Its single patch
`0001-Use-Arch-Linux-device-access-groups.patch` touches `meson.build`, `meson_options.txt`,
`rules.d/50-udev-default.rules.in`, `sysusers.d/basic.conf.in`. The v262 pins the corpus cites
(`src/journal/journalctl.c`, `src/journal/journalctl-filter.c`, `src/shared/options.[ch]`,
`man/journalctl.xml`) are untouched. Caveat for future pins: the systemd patch *does* rewrite
`meson_options.txt` (`@@ -287,12 +287,8 @@`, `@@ -305,18 +301,22 @@`: lines :287-:298 and :305-:322 are
rewritten in place, :299-:304 moves −4, and the net after :322 is 0), so a pin on systemd's own
`meson_options.txt` would need the same treatment as pacman's util.c.

## Summary table (drifted rows only; 108 rows total, 15 with a non-zero risk)

```
pkg    | cited file:line                    | arch tag            | patch                                   | risk
pacman | lib/libalpm/add.c:466-474          | 7.1.0.r9.g54d9411-3 | patch-reproducible-builds.patch         | +23 -> :489
pacman | lib/libalpm/add.c:468-469          | 7.1.0.r9.g54d9411-3 | patch-reproducible-builds.patch         | +23 -> :491
pacman | lib/libalpm/add.c:470-474          | 7.1.0.r9.g54d9411-3 | patch-reproducible-builds.patch         | +23 -> :493
pacman | lib/libalpm/add.c:616-648          | 7.1.0.r9.g54d9411-3 | patch-reproducible-builds.patch         | +23 -> :639
pacman | lib/libalpm/add.c:669-688          | 7.1.0.r9.g54d9411-3 | patch-reproducible-builds.patch         | +23 -> :692
pacman | lib/libalpm/add.c:670-687          | 7.1.0.r9.g54d9411-3 | patch-reproducible-builds.patch         | +23 -> :693
pacman | lib/libalpm/add.c:676-692          | 7.1.0.r9.g54d9411-3 | patch-reproducible-builds.patch         | +23 -> :699
pacman | lib/libalpm/util.c:677-687          | 7.1.0.r9.g54d9411-3 | 0001-libalpm-invalidate-curl-data-…      | +5 -> :682
pacman | lib/libalpm/util.c:688-698          | 7.1.0.r9.g54d9411-3 | 0001-libalpm-invalidate-curl-data-…      | +5 -> :693
pacman | lib/libalpm/util.c:698-700          | 7.1.0.r9.g54d9411-3 | 0001-libalpm-invalidate-curl-data-…      | +5 -> :703
pacman | scripts/makepkg.sh.in:560-569       | 7.1.0.r9.g54d9411-3 | revertme-makepkg-remove-libdepends-…    | +118 -> :678
pacman | scripts/makepkg.sh.in:565           | 7.1.0.r9.g54d9411-3 | revertme-makepkg-remove-libdepends-…    | +118 -> :683
pacman | scripts/makepkg.sh.in:615-620       | 7.1.0.r9.g54d9411-3 | revertme-makepkg-remove-libdepends-…    | +118 -> :733
pacman | doc/PKGBUILD.5.asciidoc:345-377     | 7.1.0.r9.g54d9411-3 | revertme-makepkg-remove-libdepends-…    | +9 -> :354
pacman | doc/PKGBUILD.5.asciidoc:400-404     | 7.1.0.r9.g54d9411-3 | revertme-makepkg-remove-libdepends-…    | +9 -> :409
```
Full stdout `w1/ConsiderPatchOffset/run.txt`, machine copy `out.json` (adds a `method` key: 18 `anchor`,
4 `model`, 86 unpatched). `METHOD anchor=18, model=4` is printed by the script; the four model rows are
short or blank anchors (`add.c:676`, `util.c:659-668`, `util.c:675`, `makepkg.sh.in:615`) and agree with the
anchored rows on the same files.

## Limits — what I did not do

- I did not build or install any package, and did not verify the installed binaries against source
  (extracting a compiled line mapping from `libalpm.so` was out of reach read-only). The claim is about
  the source tree the package is built from, which is what the notes pin.
- `alpm-package.7.raw` (r41 PA1) is an `alpm-docs` man-page rendering, not installed on this host
  (`pacman -Qi alpm-docs` → not found); the script skips `.raw` pins and this row is unassessed.
- The packaging tags were fetched live (GitLab API, 2026-10-26); a repackaged tag would need a re-run.
  Digests of every downloaded PKGBUILD/patch are in `w1/ConsiderPatchOffset/SHA256SUMS`.
- I did not run any counter, the census, or the lane's tests (out of scope for this seat).

## Proposed text (draft only — not applied; the L1 owns the notes)

For `corpus/knowledge/pacman-transaction-order-r39.md` and `corpus/knowledge/alpm-package-anatomy-r41.md`,
next to the existing provenance lines:

> **Packaging offset (round 42, K-1).** The host's pacman 7.1.0.r9.g54d9411-3 applies four patches to
> 54d9411. `patch-reproducible-builds.patch` inserts 23 lines at `lib/libalpm/add.c:412`, so every add.c
> line cited here after :417 is 23 lower in the built tree (`add.c:466-474` reads `:489-497`,
> `add.c:616-648` reads `:639-671`). `revertme-makepkg-remove-libdepends-and-libprovides.patch` is applied
> reversed (PKGBUILD:97-99) and restores 118 lines to `scripts/makepkg.sh.in` (`:560-569` reads `:678-687`,
> `:615-620` reads `:733-738`) and 9 lines to `doc/PKGBUILD.5.asciidoc` (`:345-377` reads `:354-386`); the
> built makepkg also carries `find_libdepends`/`find_libprovides` (:472, :537), which the pinned file does
> not. `0001-libalpm-invalidate-curl-data-in-child.patch` shifts util.c after :678 by +5 (:675 does not
> move). Re-run `python3 .ufo/waves/round-42/w1/ConsiderPatchOffset/patch-offset.py` before citing a new
> line.

## Receipts

`w1/ConsiderPatchOffset/` — `patch-offset.py` (the check), `run.txt` (stdout), `out.json`,
`host-and-packaging.txt` (pacman -Qi, btrfs --version, packaging trees at the installed tags),
`evidence.txt` (pinned-vs-built text, restored functions, lane grep = 0), `pkg/` (three PKGBUILDs),
`patches/` (four pacman patches + the systemd one), `SHA256SUMS`.

Tooling: nothing installed or upgraded; system `python3`, `patch`, `curl` only. Scratch
`/fast/scratch/hyaku/tsukuroi-r42/ConsiderPatchOffset` removed after the receipts were copied.
