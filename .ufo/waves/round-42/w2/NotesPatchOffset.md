VERDICT: supports

# F-15 — Round-42 packaging-offset notes (r39 + r41) vs wave-1 ConsiderPatchOffset

Seat: NotesPatchOffset-3 (tsukuroi r42 w2, leaf, no subagents). Verified at the pinned commit
78abb8b5cdc9da511b4fc523e661517a68dd33d3 (lane tip has since moved to a968393c678171f8a5a2907da5015735396da4cc;
all note text below was read with `git show 78abb8b5:…`, receipts `r39-at-78abb8b5.md`, `r41-at-78abb8b5.md`).
The two appended blocks are byte-identical in content (r39 note lines 87-97; r41 note lines 104-114) and were
added by that commit: `git show 78abb8b5 --stat` subject ends "packaging-offset notes r39/r41" and the diff for
the two files adds exactly 2 `## Round-42 note` blocks (grep -cE '^\+## Round-42 note' → 2).

## Method

I did not trust the w1 seat's own artifacts as proof; I reconstructed the built tree independently and re-derived
every number. Provenance chain, all verified today (2026-10-26):

- Pinned sources are upstream pacman commit 54d94116164b0b2202c6061c4a59c6f3e70820d8: r39 frozen
  `.ufo/waves/round-39/frozen/src/FETCH.txt` ("base URL https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/…",
  "installed: pacman 7.1.0.r9.g54d9411-3") and r41 frozen `.ufo/waves/round-41/frozen/src/FETCH.txt` (same raw/54d9411
  URLs, fetched 2026-10-26). Local digests match both manifests: add.c `fd313629…` (identical in r39 and r41
  SHA256SUMS — same pin), util.c `381618b6…`, makepkg.sh.in `d5882225…`, PKGBUILD.5.asciidoc `15e8007b…`.
  Stronger: `git hash-object` of the frozen add.c = `1e4aaf1ee59d23d54b0cde4b74024e7030c1b5c3`, exactly the
  pre-image blob in `patches/pacman-remote-f4bdb77.patch` line 20 (`index 1e4aaf1ee..7037dec81`) — the frozen add.c
  is bit-for-bit the file the reproducible-builds patch applies to.
- Patch identity: sha256 of all four pacman patches in `w1/ConsiderPatchOffset/patches/` equal the pacman.PKGBUILD
  `sha256sums` entries (b3bce9d6…, de428b49…, 9a734e5d…, 021893dd…; `pkg/pacman.PKGBUILD:53-57`).
- Build model: `pkg/pacman.PKGBUILD` — checkout v7.1.0 rebased onto `_git_patch_level_commit=54d9411…` (:8-9, :80-86),
  then four `.patch` sources applied in array order (:51-55), with `revertme-*` applied `patch -RNp1` (:97-99).
- Reconstruction: fixture repo `/fast/scratch/hyaku/tsukuroi-r42/NotesPatchOffset/fx.pzTLVR` (git init, pristine
  commit verified `rev-parse --show-toplevel` == fixture), files = frozen snapshots + five files fetched from
  gitlab raw/54d9411 today (dload.c 1471 l, test/pacman/README 342 l, meson.build 381 l, pmrule.py 201 l,
  pmtest.py 364 l), then exactly the PKGBUILD sequence: `patch -RNp1 < pacman-remote-354a300.patch`,
  `patch -Np1 < pacman-remote-f4bdb77.patch`, `patch -Np1 < pacman-0001-…patch`, `patch -Np1 < pacman-0002-…patch`.
  All four exit 0 (`patch-logs.txt`).

## 1. The three offsets — all correct

Line counts pin→built (`battery-full.txt` §1): add.c 695→718 (**+23**), makepkg.sh.in 1427→1545 (**+118**),
PKGBUILD.5.asciidoc 547→556 (**+9**); util.c 1657→1662 (+5, the r40 annex, not re-claimed by this note's rules).

Diff hunk headers in pin numbering, `diff -U0` (`battery-full.txt` §2, full diffs `diffs-pin-to-built.txt`):
- add.c: `@@ -414,0 +415,23 @@` — the 23-line `get_install_time()` block is inserted between pin 414 and 415; the
  patch's hunk header is `@@ -412,6 +412,29 @@` (patches/pacman-remote-f4bdb77.patch:23), so the note's "inserts
  23 lines … at :412" matches the hunk start. Second hunk `@@ -594 +617 @@` is count-neutral (1:1 replacement of
  `newpkg->installdate = time(NULL);` at pin 594 — outside every cited range, see §2).
- makepkg.sh.in: `@@ -471,0 +472,115 @@` + `@@ -511,0 +627,3 @@` — 115+3 = **118** restored, matching the reverse
  of 354a300's deletions (`patches/pacman-remote-354a300.patch` hunks `@@ -463,121 +463,6 @@` = −115 and
  `@@ -617,9 +502,6 @@` = −3).
- PKGBUILD.5.asciidoc: `@@ -182,0 +183,5 @@` + `@@ -234,0 +240,4 @@` — 5+4 = **9**, matching 354a300's
  `@@ -187,11 +187,6 @@` (−5) and `@@ -245,10 +240,6 @@` (−4).

My `patch` runs reproduce w1's reported offsets exactly (`patch-logs.txt` vs `run.txt` NOTE lines):
PKGBUILD.5 `[-7, -7]`, makepkg `[6, 8]`, add.c and util.c clean.

Example mappings in the note — text identity, not just arithmetic (`battery-full.txt` §3-6, 19/19 PASS in
`battery-equality.txt`):
- `add.c:466-474` == built `:489-497` (and 468-469→491-492, 470-474→493-497, 616-636→639-659, 616-648→639-671,
  630→653, 638-647→661-670, 639-640→662-663, 669-688→692-711, 676-692→699-715).
- `makepkg.sh.in:560-569` == built `:678-687` (and 565→683, 615-620→733-738).
- `PKGBUILD.5.asciidoc:345-377` == built `:354-386` (and 400-404→409-413, 439-441→448-450).

Host corroboration, independent of the reconstruction: `pacman -Q pacman` → `pacman 7.1.0.r9.g54d9411-3` today;
the real installed `/usr/bin/makepkg` is 1545 lines (= pin 1427 + 118), has `find_libdepends()` at :472,
`find_libprovides()` at :537, the mapfile calls at :628-629, the cited `local workingdir="${2:-$srcdir}"` still at
:414, and `diff <(sed -n 560,569p r41-frozen-makepkg) <(sed -n 678,687p /usr/bin/makepkg)` is empty
(`host-checks.txt`). The installed binary's script confirms the +118 mapping on the actual host file.

## 2. "The patched hunks do not touch the cited logic" — holds, and I closed three census gaps

Every line-range citation in both notes' pre-existing text was enumerated (`r39-at-78abb8b5.md`,
`r41-at-78abb8b5.md`, including bare `:N` forms continuing a named file) and checked against the reconstruction:

- r39 cites add.c at 168-189, 466-474, 468-469, 470-474, 616-636, 616-648, 630, 638-647, 639-640, 669-688, 676-692
  and util.c at 521-528, 665-666. None falls inside an inserted block (add.c built 415-437; util.c built 676-680)
  or on the replaced pin line 594; all map with text identity (168-189, 521-528, 665-666 unshifted and identical;
  the rest +23/+5 as applicable). hook.c, trans.c, sync.c, remove.c citations are in files no patch touches
  (patch logs list only add.c, util.c, dload.c, makepkg.sh.in, PKGBUILD.5.asciidoc, test/pacman/*).
- r41 cites makepkg.sh.in at 192, 414, 560-569, 565, 615-620 and PKGBUILD.5.asciidoc at 51-56, 67-74, 345-377,
  400-404, 439-441, plus add.c 168-189. None falls inside an inserted block (makepkg built 472-586 and 627-629;
  PKGBUILD.5 built 183-187 and 240-243); all map with text identity (192, 414, 51-56, 67-74, 168-189 unshifted).
  be_local.c, check.c, query.c, version.c, be_package.c are untouched by the four patches.

**Finding F-15a (w1 census gap, closed here — no wrong number results).** `run.txt`'s 108-row census has no row
for three implicit citations: `makepkg.sh.in:414` (r41 note line 96), `PKGBUILD.5.asciidoc:51-56` (r41 line 94)
and `PKGBUILD.5.asciidoc:439-441` (r41 line 38) — the seat's extractor evidently only matched `file:N` forms, not
bare `:N`. The appended note's authority claim ("per the seat's pinned-vs-built comparison, `evidence.txt`") is
therefore broader than the comparison's census for these three rows. I verified all three myself: :414 and :51-56
are unshifted and byte-identical; :439-441 reads :448-450, identical. The note's claim survives; the gap is in
`run.txt`, not in the note's numbers.

## 3. Minor wording findings (no wrong number)

- **F-15b (boundary precision).** "every add.c line cited here after :417 is 23 lower" is conservative: the true
  first shifted pin line is 415 (insertion between 414 and 415; pin 415-417 == built 438-440, `battery-full.txt`
  §7). No r39 citation sits in 415-465, so the statement is true as written for every cited line; a future cite of
  add.c:415-417 would fall outside the note's stated rule, which is why the note's own "Re-run the check before
  citing a new line" instruction matters. Same shape for the other files: first shifted pin lines are util.c 676,
  makepkg 472, PKGBUILD.5 183 (§7).
- **F-15c (scoped wording).** "The statements are unchanged …; only the line numbers differ in the binary's
  source" is true for the cited logic (the scoped reading, verified in §2), but the built tree does differ
  functionally from the pin elsewhere: add.c gains `get_install_time()`/SOURCE_DATE_EPOCH handling and the
  installdate line changes (f4bdb77 hunk 2), and the built makepkg carries libdepends/libprovides support the pin
  lacks — w1's own report states this (`.ufo/waves/round-42/w1/ConsiderPatchOffset.md`, F2/F3). The appended note
  also drops the w1 proposal's util.c +5 sentence, the `:615-620 reads :733-738` example and the
  find_libdepends/find_libprovides mention (compare `ConsiderPatchOffset.md` "Proposed text" with the appended
  block) — omissions, not errors; r39's own util.c cites (521-528, 665-666) are all pre-insertion, so no r39
  reader is misled.
- **F-15d (r41 framing).** "The line pins above are upstream pacman 54d9411" overgeneralizes for the r41 note:
  PA1 cites `S227 alpm-package.7.raw:100-120` (r41 note line 26), a man-page rendering from extra/alpm-docs
  0.13.0-1 on man.archlinux.org, not a 54d9411 file — the r41 header itself separates the two provenances
  (r41 note lines 2-3), and w1 marked .raw pins unassessed (`ConsiderPatchOffset.md` "Limits"). The offset rules
  that follow apply only to the pacman-file pins; no alpm-docs pin is affected by pacman packaging patches.

## What I did not do

- No package was built or installed; no pacman transaction run (host guard). The add.c/PKGBUILD.5 mappings rest on
  the patch reconstruction (bit-identical add.c pre-image, clean applies, reproduced offsets), not on a compiled
  artifact; the makepkg mapping is additionally confirmed against the real installed `/usr/bin/makepkg`.
- alpm-docs/alpm-package.7.raw offsets: out of this item's scope (F-15d records the framing nit only).
- btrfs-progs/systemd pins: w1 F5/F6 territory, not re-verified here.
- The w1 seat's `patch-offset.py` was not re-executed; my reconstruction is an independent check of the same
  transformation, and its offset NOTEs were reproduced by my `patch` runs.

## Receipts

`​.ufo/waves/round-42/w2/NotesPatchOffset/` — `verify-offsets-fixed.sh` + `battery-full.txt` (29 checks: 28 PASS,
1 expected boundary FAIL), `verify-equality.sh` + `battery-equality.txt` (19/19 PASS), `patch-logs.txt`,
`diffs-pin-to-built.txt`, `host-checks.txt`, `r39-at-78abb8b5.md`, `r41-at-78abb8b5.md`, `SHA256SUMS` (all verified
`sha256sum -c` OK). Scratch `/fast/scratch/hyaku/tsukuroi-r42/NotesPatchOffset` (incl. fixture fx.pzTLVR) removed
after copying.

Tooling: nothing installed or upgraded (system git/patch/curl/diff/sed only; pacman transactions untouched).
