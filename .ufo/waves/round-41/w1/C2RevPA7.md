VERDICT: holds
ROW: PA7
lines checked: frozen/src/PKGBUILD.5.asciidoc:345-377

Reviewed row: `corpus/knowledge/alpm-package-anatomy-r41.md` line 32 at pinned commit
9cc9aa77e30e0e23de2d4d2697b3b218ada02969 (read via
`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 9cc9aa77e...:corpus/knowledge/alpm-package-anatomy-r41.md`,
not the working tree). Receipts: `.ufo/waves/round-41/w1/C2RevPA7/`.

Live-source identity (access date 2026-10-26): fetched
https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/doc/PKGBUILD.5.asciidoc with
`curl -fsSL`; `sha256sum` gave 15e8007bb11829b4d0474e647b0d08c2bffdf5191ceac949336de3d14a621154
for both the live download and `.ufo/waves/round-41/frozen/src/PKGBUILD.5.asciidoc`, `cmp -s`
exit 0 (byte-identical), and the digest matches the PKGBUILD.5.asciidoc line in
`.ufo/waves/round-41/frozen/src/SHA256SUMS`. So the pinned snapshot is the upstream document at
54d9411 and every finding below applies to both.

Rule-cell clause check (frozen/src/PKGBUILD.5.asciidoc, cited span 345-377, verbatim):
- "`package()` ... run inside `$srcdir`" — line 351 "This function is run inside `$srcdir`." ✓
- "`prepare()` ... inside `$srcdir`" — line 365 ✓
- "`build()` ... inside `$srcdir`" — line 370 ✓
- "`check()` ... inside `$srcdir`" — line 377 ✓
- "`verify()` runs inside `$startdir`" — line 357 "This function is run inside `$startdir`.",
  which is exactly the row's quoted sentence, at the cited lines ✓
- "`package()` also runs under fakeroot" — lines 348-349 "The packaging stage is run using
  fakeroot to ensure correct file permissions in the resulting package." ✓
- "while the other functions run as the calling user" — line 350 "All other functions will be
  run as the user calling makepkg." ✓
Coverage: the five function blocks in the cited span are exactly package (345-351), verify
(353-357), prepare (359-365), build (367-370), check (372-377); each carries one directory
statement, so "the working directory of each packaging function" is complete, no overreach.
No missing condition changes the meaning: the doc's other qualifications (verify runs before
sources are extracted, line 356; prepare is skipped when source extraction is skipped,
lines 363-364) are not working-directory or privilege clauses and their omission does not alter
any stated clause. The row avoids the known false variant ("`package()` runs inside `$pkgdir`")
that the entry itself refuses in its assimilation note (blob line 19).
Value cell `$srcdir: package prepare build check; $startdir: verify` is consistent with the rule
cell and with the document.

Host cell vs frozen capture: `.ufo/waves/round-41/frozen/hostcap/man-pkgbuild-runinside.txt`
(sha256 c905f360313e5c3254534a0993ee258f5ef65b0378bfdf9f8bd9cfa1e59a3bc4, matching its
MANIFEST.sha256 line) contains 5 `grep -n` hits for "This function is run inside": man lines
360 ($srcdir), 366 ($startdir), 373 ($srcdir), 378 ($srcdir), 384 ($srcdir) — i.e. 5 lines, 4
`$srcdir` and 1 `$startdir`, in the package/verify/prepare/build/check order, exactly as the
host cell states. `capture-meta.txt` records captured_utc 2026-10-26T16:14:04Z and
"pacman pacman 7.1.0.r9.g54d9411-3", matching the cell's version attribution; `capture.sh:26`
shows the provenance (`man -P cat PKGBUILD 2>/dev/null | grep -n 'This function is run inside'`).
The cell is stated as measured (capture cited) and that is honest. Independent live re-measure
on this host 2026-10-26 (read-only): `pacman -Q pacman` -> `pacman 7.1.0.r9.g54d9411-3`;
`man -P cat PKGBUILD | grep -c 'This function is run inside'` -> 5, of which 4 `$srcdir` and 1
`$startdir` — agrees with the frozen capture.

Not done: I did not run the frozen counter `tools/check-package-anatomy-r41.py` (out of scope
for this row verdict; the verdict file is its input) and did not exercise a real makepkg run
(no package build — outside this seat's bounds); PA7's host claim is a man-page measurement,
which I both read from the capture and re-measured live.

Receipts kept under `.ufo/waves/round-41/w1/C2RevPA7/`: pa7-blob-line.txt, 
snapshot-runinside-lines.txt, live-vs-pinned-sha256.txt, man-live-recount.txt.
Scratch /fast/scratch/hyaku/tsukuroi-r41/C2RevPA7 removed (trap-equivalent cleanup done
before finishing; no other writes under the lane or fleet root). No tools installed; nothing
added to the host.
