VERDICT: holds
ROW: PA7
lines checked: frozen/src/PKGBUILD.5.asciidoc:345-404

Judged row PA7 (`corpus/knowledge/alpm-package-anatomy-r41.md:32`) together with its correction bullet
(`:92-97`, section `## Corrections from the round-41 wave` at `:64-67`) at lane revision
20c327b3f1cf96ad1828792c2ae5db71b5fd9ef7 — `git rev-parse HEAD` → that hash; `git status --porcelain --
corpus/knowledge/alpm-package-anatomy-r41.md` → clean, so the working-tree text is the committed text.
Second reader: `.ufo/waves/round-41/w1/C2RevPA7b.md` (verdict `partly`). Snapshot integrity re-verified by
me: `sha256sum -c .ufo/waves/round-41/frozen/src/SHA256SUMS` → nine OK; `sha256sum -c
.ufo/waves/round-41/frozen/hostcap/MANIFEST.sha256` → six OK. Receipts:
`.ufo/waves/round-41/residual/C2RevPA7c/receipts.txt`. Additional windows read beyond :345-404:
PKGBUILD.5.asciidoc:45-60 (pkgver passage), :307-344 (Packaging Functions heading+intro), makepkg.sh.in
:185-196, :404-428, :449-475, :852-885, :1239-1273, :1369-1423.

## Row clauses — all supported by the pinned snapshot

1. package/prepare/build/check each `$srcdir`: PKGBUILD.5.asciidoc:351, :365, :370, :377 — each the exact
   sentence "This function is run inside `$srcdir`." inside the respective function block (`*package()
   Function*` :345, `*prepare() Function*` :359, `*build() Function*` :367, `*check() Function*` :372).
2. verify `$startdir`: :357 inside `*verify() Function*` :353; `$startdir` defined at :391-394 ("usually
   the output of `$(pwd)` when makepkg is started").
3. package() under fakeroot, others as calling user: :348-349 "The packaging stage is run using / fakeroot
   to ensure correct file permissions", :350 "All other functions will be run as the user calling makepkg."
4. Value cell `$srcdir: package prepare build check; $startdir: verify` matches 1-2 exactly.
5. Host cell (5 lines, 4 `$srcdir`, 1 `$startdir`, pacman 7.1.0.r9.g54d9411-3): frozen
   hostcap/man-pkgbuild-runinside.txt has exactly 5 grep hits (rendered lines 360, 366, 373, 378, 384;
   4 srcdir, 1 startdir); `pacman -Q pacman` → `pacman 7.1.0.r9.g54d9411-3`; live re-run
   `LC_ALL=C MANWIDTH=80 man -P cat PKGBUILD | grep -n 'This function is run inside'` is byte-identical to
   the frozen capture (`diff` → empty, LIVE_REPRO_IDENTICAL). The width pin is `capture.sh:7`
   (`export LC_ALL=C MANWIDTH=80`) — C2RevPA7b cited :8; the pin is real, its line number is :7.

Document-wide check that nothing else carries a cwd sentence: `grep -in 'run in\b|run inside|runs in\b'
PKGBUILD.5.asciidoc` → :350, :351, :356, :357, :365, :370, :377 only (:350/:356 are the loose pattern's
"run as the user"/"run before sources" matches, not cwd statements). Nothing in Package Splitting
(:399-430) or the pkgver passage (:50-55).

## Correction clauses — all supported

1. "The working-directory sentences cover the five functions PKGBUILD(5)'s Packaging Functions section
   names": heading `Packaging Functions` at :329-330; the section names exactly package (intro :331-335
   and block :345), verify (:353), prepare (:359), build (:367), check (:372), and the five cwd sentences
   sit one per block. Nothing else is named as a function in that section (the entries from :383 on are
   variables: srcdir, pkgdir, startdir).
2. "It states no directory for the split-package `package_<name>()` functions (`PKGBUILD.5.asciidoc:400-404`)":
   Package Splitting heading :399-400; :403-404 "Each split package uses a corresponding packaging function
   with name / `package_foo()`, where `foo` is the name of the split package." No cwd sentence in the block
   (grep above). Citation window checks out.
3. "or for `pkgver()` (`:51-56`)": the pkgver() passage is :50-55 — :50 "The `pkgver` variable can be
   automatically updated by providing a `pkgver()`", :52-54 "This is run after downloading and extracting
   the sources and running the / `prepare()` function …". No cwd statement anywhere in it. The cited
   window :51-56 starts one line into the sentence and ends on a blank line; tighter would be :50-55.
   The clause itself (doc states no directory for pkgver()) is fully supported — precision note, not a defect.
4. "makepkg runs both inside `$srcdir` (… `pkgver` at `makepkg.sh.in:192`; `run_function_safe` defaults its
   directory to `$srcdir`, `local workingdir="${2:-$srcdir}"` at `:414`)": verified verbatim —
   makepkg.sh.in:192 `newpkgver=$(run_function_safe pkgver)` inside `update_pkgver()` :190-196; :414
   `local workingdir="${2:-$srcdir}"` inside `run_function()` :409, applied by :419 `cd_safe "$workingdir"`.
   Split side of "both": `run_package()` :468-469 `run_function_safe "package${1:+_$1}"` — no directory
   argument, so the same :414 default; chain `run_split_packaging` :869 → `run_single_packaging $pkgname`
   :880 → `run_package $1` :862, all live code (dispatched at :1260 in the `INFAKEROOT` branch :1247-1267);
   pkgver is live too (`update_pkgver` called at :1387 in the main flow). I additionally confirmed only
   `run_verify` passes a directory (`:452-453` `$startdir`); `run_prepare/build/check` :456-465 pass none.
5. "so the decision-table command finds no line for them" (decision-table row at corpus :49): the command
   greps `This function is run inside`, whose only five occurrences are the five function blocks (grep
   above), so no line exists for `package_<name>()` or `pkgver()` — confirmed by the live run's 5-line
   output.

## Second reader's conditions — every one addressed

- Universal quantifier "each packaging function" (false under the doc's own use of "packaging function" for
  `package_foo()`): the correction re-scopes to "the five functions PKGBUILD(5)'s Packaging Functions
  section names" and says explicitly where the doc is silent. Addressed.
- Missing split-package condition: named, cited (:400-404), makepkg behavior given. Addressed.
- pkgver() instance: named, cited (:51-56), makepkg behavior given. Addressed.
- Decision-table silent miss for those two: stated ("finds no line for them") and true. Addressed.
- C2RevPA7b's MANWIDTH caveat (only width 80 reproduces 5/4/1): pinned by capture.sh:7 and enforced by the
  entry's own `recheck:` header (corpus :4-6, "re-run … capture.sh"). Addressed.

No new overreach: the adopted correction drops C2RevPA7b's proposed "the split ones under fakeroot"
claim (an omission, not an assertion — the row's fakeroot clause stays scoped to `package()`, supported by
:348-350); it attributes `$srcdir` for the two extra functions to makepkg's behavior, not to PKGBUILD(5),
which is exactly what the sources show. The row's source cell remains S232 `:345-377`; the correction's
new clauses carry their citations inline (`:400-404`, `:51-56`, `makepkg.sh.in:192`, `:414`), so no clause
rests on an uncited window — C2RevPA7b's optional widening to `:345-377,403-404` was not adopted and is
not needed for support.

## Residual risk / verification gaps

- I did not run the frozen counter (`tools/check-package-anatomy-r41.py`); it consumes this file's first
  line. I ran no lane counter at all (single-flight host rule; not needed for a verdict seat).
- The split-chain line numbers in C2RevPA7b's receipts (`:860`, `:878`) are off by two against the pinned
  snapshot (`run_package $1` is :862, `run_single_packaging $pkgname` is :880); the correction does not
  cite those lines, so no clause is affected. My chain citations above are from the snapshot as re-read.
- C2RevPA7b noted `verify()`'s upstream caller (`check_source_integrity`, libmakepkg) is outside the frozen
  snapshot; unchanged here, and no clause of row+correction depends on it.

Constraints observed: read-only on lane content — the only writes were this report and
`residual/C2RevPA7c/receipts.txt`; read-only git (`rev-parse`, `status`, no add/commit/checkout/stash);
read-only host reads (`man`, `grep`, `pacman -Q`, `sha256sum -c`, `diff`); no pacman transaction, no sudo,
no service/mount/host change; no scratch clone, mutant or fixture was needed, so no scratch dir was
created and none remains to remove; no tool installed or upgraded; no subagents.
