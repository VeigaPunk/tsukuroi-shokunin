# C1ReviewR — round-12 C1 root-directory metadata arm, FINAL static review

Reviewed artifact: `tools/tsukuroi-census.sh`, sha256 `efb82e2894a609d78652c84cfa76a087747bd5f3640d41df2b038f6d660ba2df`, 2665 lines (the consolidated digest from CensusR; read on disk at review time, matches). Earlier digests `74f9609e…` and `fbafa500…` are superseded and were not reviewed as final.

Method: static reading of the landed source and its selftest cases. Targeted read-only host probes only. No selftest, census run, `bash -n`, or other test was executed by this seat. No PASS is claimed on the selftest; it is for the parent to run once.

## Verdict (static)

Contract conformance: the implementation matches the parent rulings (report-only owner bits; BLOCKED on unavailable, non-directory, and empty/relative/unsafe override; root evidence composed in `main` after `probe_packages` and folded with `worse`). No blocking defect found in the root arm. Two LOW items remain open (F-F, R-3); none flips a verdict.

## Closed since the interim review (verified in source)

- **F-A (DEGRADED on owner-bit absence):** closed. `probe_root_meta` (lines ~738-816) never assigns `ROOT_V` other than HEALTHY or BLOCKED. Owner-bit absence is printed as `root_owner_write=absent`, `root_owner_search=absent`, `root_report=…`, `root_intent=not-assessed`.
- **F-B (stable keys on BLOCKED branches):** closed. Every BLOCKED branch prints `root_mode=` / `root_uid=` / `root_gid=` (value or `unknown`) and `root_owner_write/search` (value or `unknown`). Checked: override (line ~757), unavailable (~779), non-directory (~787), mode-unparseable (~793).
- **F-C (empty override reads live `/`):** closed. `ROOT_DIR=${TSUKUROI_ROOT_DIR-/}` (line 360). `root_locator_class` returns `empty` for an empty value and BLOCKs before any stat. Case `blocked-root-empty-override` asserts `root_dir=empty`.
- **F-D (no per-case isolation guard):** closed. `check()` asserts `grep -qF -- "root_dir=$root_expect"` on the packages line for every case (line 1943), with `root_expect` defaulting to `$FX/root`. A live `/` read prints `root_dir=/` and fails the assertion. `TSUKUROI_ROOT_DIR="$FX/root"` is set before `"${EXTRA_ENV[@]}"` (line ~1912).
- **F-E (selftest abort from unreadable fixture modes):** closed. `fx_hash` (line 1883) now runs `find … || true` on both the metadata listing and the content hash. The hash includes `%y %m %U %G`, so a fixture-root chmod is inside the zero-mutation proof. The trap (line 1705) runs `chmod -R u+rwx` before `rm -rf`. The 000-subtree case is dropped, so no pipefail abort path remains. `chmod -R` does not follow the loop symlinks, which is what the teardown needs.
- **Non-directory token:** the normalization at line 784 (`ftype=${ftype// /-}`) matches the case expectation `type=regular-empty-file` (line 2536). The text I first read predated this line; the final file has it.

## Verified correct (static)

- Octal: `%04a` is regex-validated (`'' | *[!0-7]*`) before `num=$((8#$mode))`. `1777`, `2755`, `1555`, `0400` produce the owner bits that the cases assert.
- `set -e` safety: `probe_root_meta` ends with `return`. The `[ … ] && report=…` lines are non-final in their lists. `cap` wraps both stat calls; no bare command substitution.
- Classifiers match GNU `stat` text with a leading `: ` anchor: `: Permission denied`, `: No such file or directory`, `: Too many levels of symbolic links`. The leading anchor keeps a path that contains the phrase from being misclassified.
- Fold placement: `probe_root_meta` runs after `probe_packages`; `PKG_V=$(worse "$PKG_V" "$ROOT_V")` is before the rollup and the PLANE print (lines ~2625, 2634). Early returns in `probe_packages` keep root evidence by composition, not via `PKG_NOTE`. Plane order, rollup, and exit map unchanged.
- Symlink reporting: `root_type=symlink(unresolved)` is only added when `stat -c %F` (no `-L`) reports `symbolic link`. Dangling and loop cases therefore report the same BLOCKED shape.
- `root_locator_class` rejects spaces, `=`, and any character outside `[A-Za-z0-9._/+-]` before stat, so the unsafe-override case cannot inject a token. The raw path is not echoed (`root_dir=unsafe`).

## Open findings — CLOSED at digest f739284b5821d5d096aedb6b36c0d021bb3d0be8706a5f7a31688759a6a1b449 (2679 lines)

- **F-F (closed):** uid/gid validated (`''|*[!0-9]*`, line ~795-796) after mode; malformed → `root_status=unavailable(parse=uid|gid)` with observed mode and unknown uid/gid/bits (line ~800-805). Static only: no hermetic case exercises the parse branch (LOW gap, recorded).
- **R-1 (closed):** check() asserts `root_dir=<expect>` followed by space or `)` via quoted `[[ ]]` on the packages line (line ~1954). Quoted RHS, no glob injection from paths. Static only.
- **R-2 (closed):** second named skip present for the EACCES case (line ~2537). Named gap now visible in run output.
- **R-3 (INFO, unchanged):** the summary `%d cases` counts only executed ok/bad results; skips are not counted. No defect.


## Case set review (static)

- Healthy: `healthy-root-0755` (owner bits present, pinned uid/gid), `healthy-root-0555-report` (owner-write absent, report-only, verdict HEALTHY), `healthy-root-0644-search`, `healthy-root-0400-both` (both named), `healthy-root-sticky` (1777), `healthy-root-setgid` (2755), `healthy-root-sticky-norewrite` (1555). Regexes anchor the four-digit `root_mode=` token, so a decimal parse or 555-vs-0555 drift fails.
- BLOCKED: missing, regular file (`non-directory(type=regular-empty-file)`), dangling symlink (`errno=missing` with `root_type=symlink(unresolved)`), loop (`errno=symlink-loop`), empty override, unsafe override (raw path not echoed), and four early-return survivals (pacman missing, db.lck, empty db, sample rc=2) each asserting `root_status=ok root_mode=0755`.
- Hermetic: fixture root is 0755 via explicit `chmod` (umask 077 would otherwise make it 0700). Every case pins `root_dir=` to the configured fixture path.
- Not fixtureable non-root (named skip): a root owned by a different uid. Recorded as a skip, not a pass.
- Note on the loop case: the two symlinks are created in `$FX` before `check`. `fx_hash` uses `find -printf '%y'` and does not follow them, so the zero-mutation proof remains valid.

## Verification gaps (for the parent)

- Selftest, census run, and `bash -n` were not executed by this seat. The run must confirm: 97 registrations plus 1 skip; every BLOCKED case's `errno=` token matches GNU `stat` 9.11 text in `LC_ALL=C` (the classifier strings are from the GNU binary observed on this host, not the spec); the loop case produces `Too many levels of symbolic links` on the host's `stat`.
- EACCES is not exercised. This is an accepted gap: under uid 0 the DAC check is bypassed, and under non-root the 000-subtree breaks the mutation hash. It is a named gap, not coverage.
- Only one live sample of `/` (`555 0 0`) exists. The live packages plane will not flip on owner bits after this revision (report-only), but the live result must be confirmed by a run, not inferred from this review.
- Host facts used: `/usr/lib/tmpfiles.d/root.conf` `z / 555 - - -` (read); GNU coreutils `stat` 9.11 at `/usr/bin/stat`; `find /root` under uid 1000 returns `Permission denied` (read-only observation of the classifier source).

## Tools

No installs, upgrades, or package operations by this seat. Read-only commands only: `stat`, `find`, `cat`, `grep`, `sha256sum`, `git diff`, pure-bash arithmetic and `read` semantics.

## Static recheck of the three final items (digest f739284b5821d5d096aedb6b36c0d021bb3d0be8706a5f7a31688759a6a1b449, 2679 lines)

- uid/gid validation: PASS (static). `case "$uid"` / `case "$gid"` reject `''|*[!0-9]*` (lines 795-796); mode is parsed first; a bad field returns `unavailable(parse=uid|gid)` with observed mode and unknown uid/gid/bits, ROOT_V=BLOCKED (line 799).
- Boundary-anchored root identity: PASS (static). `pkgline` is local to `check()`; the match is `[[ … != *"root_dir=$root_expect "* && … != *"root_dir=$root_expect)" ]]` (lines 1947, 1954). Quoted RHS: no glob or regex injection from path characters.
- Named EACCES skip: PASS (static). `skip 'C1 root arm — EACCES metadata case not built (000 subtree residue; uid 0 bypasses DAC)'` at line 2537, alongside the non-root-ownership skip (line 2534).
- Residual (LOW, unchanged): the `parse=` branch has no hermetic case.
- Not executed: selftest, census, `bash -n`. Parent runs the single post-integration check.
