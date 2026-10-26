VERDICT: partly
ROW: PA7
lines checked: frozen/src/PKGBUILD.5.asciidoc:345-377

Judged the cell as committed at 9cc9aa77: `git -C tsukuroi-shokunin show 9cc9aa77:corpus/knowledge/alpm-package-anatomy-r41.md | grep -n '^| PA7'` → line 32, the same text as the working tree. Snapshot integrity: `sha256sum -c .ufo/waves/round-41/frozen/src/SHA256SUMS` → nine OK (PKGBUILD.5.asciidoc OK, makepkg.sh.in OK). Receipts: `.ufo/waves/round-41/w1/C2RevPA7b/receipts.txt` and `…/man-runinside-manwidth80.txt`.

## What survives the attack (the five enumerated statements are exact)

1. `package()` → `$srcdir`, fakeroot: PKGBUILD.5.asciidoc:348-351 — "The packaging stage is run using / fakeroot to ensure correct file permissions … All other functions will be run as the user calling makepkg. / This function is run inside `$srcdir`." The rule cell's fakeroot half paraphrases :348-350 without distortion.
2. `verify()` → `$startdir`: :356-357 — "… before sources are extracted. / This function is run inside `$startdir`." (`$startdir` defined at :393 "located, which is usually the output of `$(pwd)` when makepkg is started").
3. `prepare()` → `$srcdir`: :365; `build()` → `$srcdir`: :370; `check()` → `$srcdir`: :377. The doc's extra conditions (:363-364 "skipped when source extraction / is skipped", :374-375 "run between the `build()` and / `package()` functions") are about *when*, not *where*, so their omission does not touch a working-directory cell.
4. Code agrees, including the default rather than a special case: `makepkg.sh.in:414` `local workingdir="${2:-$srcdir}"` + `:419` `cd_safe "$workingdir"`; `:452-453` `run_verify() { run_function_safe "verify" "$startdir"; }`; `:457/:461/:465` prepare/build/check pass no second argument, so `$srcdir`; `:468-469` `run_package() { run_function_safe "package${1:+_$1}"; }`, so `$srcdir`. Only `:453` overrides the directory (`grep -n 'run_function_safe' makepkg.sh.in` → :192, :453, :457, :461, :465, :469).
5. Fakeroot split holds in the code too: `enter_fakeroot` re-execs makepkg under fakeroot (`:183-185`), the `INFAKEROOT` branch runs only packaging (`:1247-1265`, exit at :1265), and prepare/build/check run in the outer process *before* it (:1377 `run_prepare`, :1409 `run_build`, :1410 `run_check`, :1414 `enter_fakeroot`).
6. Host cell reproduces exactly: `LC_ALL=C MANWIDTH=80 man -P cat PKGBUILD | grep -n 'This function is run inside'` → 5 lines, 4 `srcdir`, 1 `startdir`, byte-identical to `frozen/hostcap/man-pkgbuild-runinside.txt` (`diff -u` empty). Host `pacman -Q pacman` = `pacman 7.1.0.r9.g54d9411-3`, as the cell says.

## Counterexample: the universal quantifier is false under the document's own term

The rule cell says "PKGBUILD(5) states the working directory of **each** packaging function: …". The pinned document calls a second, differently named class of function a "packaging function" and states no working directory for it:

- PKGBUILD.5.asciidoc:403-404 — "Each split package uses a corresponding packaging function with name / `package_foo()`, where `foo` is the name of the split package." No cwd sentence exists for it: every working-directory statement in the whole document is one of the five lines already cited — `grep -n "run in\b\|run inside\|runs in\b" PKGBUILD.5.asciidoc` → :351, :357, :365, :370, :377 only, all inside the single-package "Packaging Functions" block (:345-377). The "Package Splitting" block (:400-425) carries none.
- makepkg nonetheless runs it exactly like `package()`: `run_split_packaging` → `run_single_packaging $pkgname` (:878) → `run_package $1` (:860) → `run_function_safe "package_$1"` (:469) → default `workingdir` `$srcdir` (:414) → `cd_safe` (:419), inside the `INFAKEROOT` branch (:1258-1260). So the value cell `$srcdir: package prepare build check; $startdir: verify` omits a function that is `$srcdir` **under fakeroot**, i.e. the row's own two assertions, unstated.
- Second instance: `pkgver()` — PKGBUILD.5.asciidoc:51-57 "The `pkgver` variable can be automatically updated by providing a `pkgver()` / function in the PKGBUILD that outputs the new package version. / This is run after downloading and extracting the sources and running the / `prepare()` function …" — again no directory statement, while makepkg runs it through the same default: `update_pkgver` → `newpkgver=$(run_function_safe pkgver)` (`:190-192`) → `$srcdir` (:414, :419).

Why it matters operationally, not just lexically: the entry's decision table routes "A PKGBUILD function behaves as if in the wrong directory" to `man -P cat PKGBUILD | grep -n 'This function is run inside'`. For `pkgver()` or a split-package `package_<name>()` that command returns no line for the function in question, so the reader gets a silent miss while the row's "each" has promised coverage. That is an overstated universal plus a missing condition (split packaging), the smallest defect class that keeps the five verified statements intact.

## Tested and not falsifying

- Flags: `--noextract`, `--nobuild`, `--repackage`, `--cleanbuild` only skip or recreate functions (makepkg.sh.in:1355-1411); none bypasses `cd_safe "$workingdir"` (:419).
- Caller bypass: none for the five; only `run_verify` passes `$startdir` (:453).
- `verify()`'s own call site is outside the snapshot: `grep -n 'run_verify' makepkg.sh.in` returns only the definition (:452); `check_source_integrity` (:1367) lives in libmakepkg, which is not in `frozen/src/`. Not counted against the row (the cell claims only what the document states), recorded as unmeasured.
- Width caveat on the host cell (not a defect, but the recheck must keep the width): at `MANWIDTH=200` the justified `package()` line puts `$srcdir.` on the next line and a strict single-space grep yields 4 lines / 3 `srcdir` / 1 `startdir` (observed). `frozen/hostcap/capture.sh:8` pins `MANWIDTH=80`, the only width at which the cited 5/4/1 reproduces; the cell is correct as cited.

## Smallest safe correction (exact proposed text)

Rule cell, replace with:

> PKGBUILD(5)'s Packaging Functions section states the working directory of each of the five functions it names: `package()`, `prepare()`, `build()` and `check()` each run inside `$srcdir` and `verify()` runs inside `$startdir`; `package()` also runs under fakeroot while the other four run as the calling user. PKGBUILD(5) states no working directory for the split-package `package_<name>()` functions (`:403-404`) or for `pkgver()` (`:51-57`); makepkg runs both inside `$srcdir` (`makepkg.sh.in:192,414,419,469`), the split ones under fakeroot (`:1258-1260`)

Value cell, append: `; package_<name> (split), pkgver: $srcdir by makepkg, unstated in PKGBUILD(5)`

Source cell stays S232 `PKGBUILD.5.asciidoc:345-377` for the five sentences; if the correction is taken, widen to `:345-377,403-404` (or cite the two ranges separately) so the split-package clause is inside the frozen window. This is a scoping fix, not a new row: PA7's five statements, the fakeroot split and the host figure all stand as written.

Axis impact: C2 rule cell (overstated universal + missing split-package condition) and the decision-table command's reach; PA7's core claim, PA1-PA6, PA8 and the QUALITY claims are untouched.

Constraints observed: read-only on lane content (only this report and the seat receipt dir were written); no git/jj mutation (`git show` only); no pacman transaction, no sudo, no service or mount change; the only host reads were `man`, `pacman -Q`, `grep`; scratch `/fast/scratch/hyaku/tsukuroi-r41/C2RevPA7b` removed. No tool installed or upgraded.
