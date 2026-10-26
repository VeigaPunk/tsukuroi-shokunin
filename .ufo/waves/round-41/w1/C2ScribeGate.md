VERDICT: draft

# C2-34 — `## Gate` block for S227-S236 (round 41)

Item: draft the round-41 lesson `## Gate` block for the ten new SOURCES rows S227-S236 — per row the URL,
access date 2026-10-26, and a ≤25-word quote located with `grep -n` in
`.ufo/waves/round-41/frozen/src/` (file:line) that grounds the row's `teaches`; for S236 the capture file and
line — then the used-by/status changes old→new. This report gives the verified draft at the end.

## What I read and re-derived

Read the ten rows at `corpus/SOURCES.md:236-245` (S227-S236), the entry `corpus/knowledge/alpm-package-anatomy-r41.md`
(PA1-PA8 and the supporting-row paragraph), the current Gate draft at `corpus/lessons/round-41.md:12-32`, the
pinned snapshot `.ufo/waves/round-41/frozen/src/` (`FETCH.txt`, `SHA256SUMS`) and the capture
`.ufo/waves/round-41/frozen/hostcap/` (`capture.sh`, `capture-meta.txt`, `MANIFEST.sha256`,
`localdb-anatomy.tsv`, `vercmp.txt`, `man-pkgbuild-runinside.txt`).

Quote checks (receipt `C2ScribeGate/quotes-check.txt`): each of the nine upstream quotes was run as
`grep -nF -- '<quote>' <file>` from `.ufo/waves/round-41/frozen/src/`; each occurs on exactly the cited line and
nowhere else in that file. Word counts (split on whitespace): S227 14, S228 6, S229 12, S230 9, S231 5, S232 6,
S233 7, S234 1, S235 3; S236 9. All ≤25.

| Row | file:line | quote (verbatim) |
|---|---|---|
| S227 | `alpm-package.7.raw:100` | The following files must be present at the root of an ALPM based package: |
| S228 | `be_package.c:653` | `_("missing package metadata in %s\n"), pkgfile);` |
| S229 | `makepkg.sh.in:560` | database files are placed at the beginning of the package regardless of |
| S230 | `add.c:180` | reserve all files starting with '.' for future possibilities |
| S231 | `check.c:318` | `printf(_("%s: no mtree file\n"), pkgname);` |
| S232 | `PKGBUILD.5.asciidoc:357` | This function is run inside `$startdir`. |
| S233 | `version.c:61` | different from RPM- always assume 0 epoch |
| S234 | `be_local.c:268` | `archive_read_support_format_mtree(mtree);` |
| S235 | `query.c:321` | `ret = check_pkg_full(pkg);` |

Supporting locations re-read for the multi-clause `teaches` cells:

- S227: `.BUILDINFO` `alpm-package.7.raw:102`, `.MTREE` `:108`, `.PKGINFO` `:114`, optional `.INSTALL` `:117-120`
  (CONTENTS `:94`, Metadata `:98`, Scripts `:118`).
- S228: `_alpm_pkg_load_internal` `be_package.c:555-694`; `.PKGINFO` branch `:598-618` (`config = 1` `:617`,
  `continue` `:618`); `.MTREE` read guarded by `full` `:619-624`; partial-load stop
  `if((!full || hit_mtree) && config)` `:641-643`;
  `if(!config)` + message `:652-655`.
- S229: `list_package_files` `makepkg.sh.in:562-568` (`LC_COLLATE=C` `:563`, `dotglob` `:564`); `.MTREE` written
  `:616-620` (`--format=mtree` `:617`, `--exclude .MTREE | gzip` `:619`).
- S230: `extract_db_file` `add.c:168-189`; `.INSTALL`→`install` `:173-174`, `.CHANGELOG`→`changelog` `:175-176`,
  `.MTREE`→`mtree` `:177-178`; other dot files skipped `:179-184`; `archive_entry_set_perm(entry, 0644)` `:185`;
  dispatch from `extract_single_file` `:204-206`.
- S231: `check_pkg_full` `check.c:295-435`; open `:314`; absent/unopenable-mtree branch `:315-320` (message
  `:318`, `return 0` `:320`).
- S232: `verify()` `:353-357` (quote `:357`), `package()` `:345-351`, `prepare()` `:359-365`, `build()` `:367-370`,
  `check()` `:372-377`.
- S233: `parseEVR` `version.c:39-75` (explicit epoch `:54-58`, absent epoch `:60-62`); `alpm_pkg_vercmp`
  `:219-260` (epoch `:249`, version `:251`, release only when both `:252-253`).
- S234: `_cache_mtree_open` `be_local.c:251-283`; no-mtree branch `:258-260`;
  `_alpm_archive_read_support_filter_all` `:267`, `archive_read_support_format_mtree` `:268`.
- S235: `display` `query.c:304`; check dispatch `:317-323`; level 1 `check_pkg_fast` `:319`, other levels
  `check_pkg_full` `:321`.

All ten `teaches` cells hold against the pinned text. S228's two clauses are both present (the flag is set only
in the `.PKGINFO` branch, and the `.MTREE` branch is gated by `full`); S231's zero-error claim is the
`return 0` at `check.c:320`; S233's three-step order is `:249-253`; S235's level dispatch is `:318-321`.

S236 aggregate (receipt `C2ScribeGate/hostcap-sums.txt`), run in `frozen/hostcap/`:

```
$ awk -F'\t' 'NR>1{t++; m+=$4; i+=$5; c+=$6; d+=$7; g+=$8; s+=$9} END{printf "entries=%d mtree=%d install=%d changelog=%d dotfiles=%d gzip=%d self=%d\n",t,m,i,c,d,g,s}' localdb-anatomy.tsv
entries=1409 mtree=1409 install=51 changelog=0 dotfiles=0 gzip=1409 self=0
```

Cross-checks: no row has `changelog != 0` or `dotfiles != 0`; no row has `mtree != 1` or `gzip != 1` (all
empty result sets). The `localdb-anatomy.tsv` header is tab-separated (`entry<TAB>desc<TAB>…`,
`quotes-check.txt`); total data rows 2-1410 = 1409, matching `wc -l` 1410 including the header. `vercmp.txt`
has six lines and `man-pkgbuild-runinside.txt` five; both match the entry's host cells (PA8, PA7).

Digests (receipt `C2ScribeGate/digests.txt`): `sha256sum -c SHA256SUMS` in `frozen/src/` returns OK for all nine
files; `sha256sum -c MANIFEST.sha256` in `frozen/hostcap/` returns OK for all six. The manifest's own digest is
`632ed0443cfb26ef002ebfd2a3a99971221f9129836b63135e0ca6ea41874f89`, equal to the S236 anchor cell. Fetch
provenance for the nine upstream files is `frozen/src/FETCH.txt` (nine read-only HTTPS GETs at commit 54d9411 plus
the man.archlinux.org rendering).

Used-by/status diff (receipt `C2ScribeGate/sources-diff.txt`):

```
$ git -C <lane> diff --numstat 0e5805a1f149bd2ed9fe0db2e0a832afb034a835 9cc9aa77e30e0e23de2d4d2697b3b218ada02969 -- corpus/SOURCES.md
10	0	corpus/SOURCES.md
```

One hunk, `@@ -233,6 +233,16 @@`; the ten added rows are S227-S236 and zero lines were removed (including no
`-` line that is not `---`), so no older row's `status`, `recheck` or `used-by` cell changed. The same `10 0`
holds from base to lane tip `71851d63`. The entry cites no row older than S227
(`grep -n 'S21[0-9]\|S22[0-6]' corpus/knowledge/alpm-package-anatomy-r41.md` returns nothing), so no older
`used-by` update is owed. All ten new rows are tier A, `mined`, `used-by
corpus/knowledge/alpm-package-anatomy-r41.md`; recheck `on-release` for S227-S235 and `30d` for S236.

## Findings in the current Gate draft

1. **S236's quote does not ground S236's `teaches`.** The current row
   (`corpus/lessons/round-41.md:27`) quotes the capture header *and* `vercmp.txt:4` (`vercmp 1.0 1.0-5 = 0`).
   S236's `teaches` is the local-database count (`corpus/SOURCES.md:245`); the `vercmp` line grounds PA8's host
   cell, not this row. My draft keeps the header and moves the other capture files into Location, with the
   aggregate command that produces the count.
2. **Single-line Location cells leave the other clauses of nine `teaches` cells unlocated.** S227 (member names),
   S228 (`.MTREE`-only-on-full-load), S229 (gzip/exclude), S230 (the three kept mappings), S231 (`return 0`),
   S232 (the four `$srcdir` functions), S233 (epoch-first and release-only-when-both), S234 (filter_all), S235
   (level 1 fast check) each need the supporting lines named; the current `:100`/`:653`/`:560`/`:180`/`:318`/
   `:357`/`:61`/`:268`/`:321` cells point only at the quoted line. My draft adds the ranges above, every one
   re-read. S236 is the separate case in finding 1.
3. **`check.c:295-321` is not the function range.** `check_pkg_full` closes at `check.c:435`; 295-321 is its head
   through the absent-mtree branch. The entry's locator window is not wrong for the quote, but calling it the
   function range in the lesson would be. My draft says `:295-435` with the branch `:315-320`. The same shorthand
   appears in the registry anchor "`check_pkg_full` lines 295-321" (`corpus/SOURCES.md:240`) and in the entry's
   PA6 source cell; both are windows around the quoted branch, not function ranges. Reported, not edited.
4. **The "census reports it as W04" sentence is unverified by this seat.** `corpus/lessons/round-41.md:31-32`
   says the census reports S230/S213 as W04. I found no post-S230 sources-census receipt in
   `.ufo/waves/round-41/` (the start census `before/sources-census-start.txt` predates S230; the after receipts
   `after/c*-*.jsonl` carry counter output and no `W04`/`S230` string). The verified part is that S230 shares its
   URL (`.../lib/libalpm/add.c`) with S213 under a distinct scope (`corpus/SOURCES.md:222`, `:239`); my draft
   states only that. If the L1 has the census run, the label can be restored with its receipt.
5. **The current intro says every quote is `grep -n`-located but S236 is a tab-separated capture header.** Not
   wrong in substance, but the method differs; my draft splits the two paths in the intro and records the
   `printf`-based `grep -nF` evidence for the header in the receipt.

No claim in the ten rows is falsified; the defects are in the lesson draft's evidence pointers, not in the
registry rows or the entry.

## Exact proposed Markdown

Replace `corpus/lessons/round-41.md:12-32` (the `## Gate` heading through the paragraph ending "…as W04.") with
the block below; the `### Assimilation` and `### Spot-check` subsections that follow are outside this item and
unchanged.

````markdown
## Gate

### New SOURCES rows

All ten were opened 2026-10-26 by this round. Each upstream quote was located with `grep -n` in the pinned snapshot
`.ufo/waves/round-41/frozen/src/` (nine files, `SHA256SUMS`; fetch log `FETCH.txt`) and occurs on exactly the line
given and nowhere else in its file. S236 is this round's own-work capture in
`.ufo/waves/round-41/frozen/hostcap/` (`MANIFEST.sha256`).

| Row | URL and access date | Located quote (≤25 words) | Location |
|---|---|---|---|
| S227 | https://man.archlinux.org/man/alpm-package.7 (raw rendering `alpm-package.7.raw`, extra/alpm-docs 0.13.0-1) — access 2026-10-26 | "The following files must be present at the root of an ALPM based package:" | `alpm-package.7.raw:100`; CONTENTS :94, Metadata :98 (`.BUILDINFO` :102, `.MTREE` :108, `.PKGINFO` :114), Scripts :118 (optional `.INSTALL` :117-120) |
| S228 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/be_package.c — access 2026-10-26 | `_("missing package metadata in %s\n"), pkgfile);` | `be_package.c:653`; `_alpm_pkg_load_internal` :555-694, `.PKGINFO` branch :598-618 (`config = 1` :617, `continue` :618), `.MTREE` read only when `full` :619-624, partial-load stop :641-643, `if(!config)` :652-655 |
| S229 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/scripts/makepkg.sh.in — access 2026-10-26 | "database files are placed at the beginning of the package regardless of" | `makepkg.sh.in:560`; `list_package_files` :562-568 (`LC_COLLATE=C` :563, `dotglob` :564), `.MTREE` written :616-620 (`--format=mtree` :617, `--exclude .MTREE` \| `gzip` :619) |
| S230 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/add.c — access 2026-10-26 | "reserve all files starting with '.' for future possibilities" | `add.c:180`; `extract_db_file` :168-189 (`.INSTALL`→`install` :173-174, `.CHANGELOG`→`changelog` :175-176, `.MTREE`→`mtree` :177-178, other dot files skipped :179-184, mode 0644 :185), dispatch :204-206 |
| S231 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/src/pacman/check.c — access 2026-10-26 | `printf(_("%s: no mtree file\n"), pkgname);` | `check.c:318`; `check_pkg_full` :295-435, mtree open :314, absent/unopenable branch :315-320 (message :318, `return 0` :320) |
| S232 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/doc/PKGBUILD.5.asciidoc — access 2026-10-26 | "This function is run inside `$startdir`." | `PKGBUILD.5.asciidoc:357`; `verify()` :353-357, `package()` :345-351, `prepare()` :359-365, `build()` :367-370, `check()` :372-377 |
| S233 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/version.c — access 2026-10-26 | "different from RPM- always assume 0 epoch" | `version.c:61`; `parseEVR` :39-75 (explicit epoch :54-58, absent epoch :60-62), `alpm_pkg_vercmp` :219-260 (epoch :249, version :251, release only when both :252-253) |
| S234 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/be_local.c — access 2026-10-26 | `archive_read_support_format_mtree(mtree);` | `be_local.c:268`; `_cache_mtree_open` :251-283, no-mtree branch :258-260, `_alpm_archive_read_support_filter_all` :267 |
| S235 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/src/pacman/query.c — access 2026-10-26 | `ret = check_pkg_full(pkg);` | `query.c:321`; `display` :304, check dispatch :317-323 (level 1 `check_pkg_fast` :319, other levels `check_pkg_full` :321) |
| S236 | own-work capture `.ufo/waves/round-41/frozen/hostcap/` (`capture.sh`; `capture-meta.txt:1` = `captured_utc 2026-10-26T16:14:04Z`) — access 2026-10-26 | `entry desc files mtree install changelog dotfiles mtree_gzip mtree_lists_self` (tab-separated header) | `localdb-anatomy.tsv:1`; data rows :2-1410; `vercmp.txt:1-6` and `man-pkgbuild-runinside.txt:1-5` carry the capture's other two measurements |

S236 counts, re-derived from the capture: `awk -F'\t' 'NR>1{t++; m+=$4; i+=$5; c+=$6; d+=$7; g+=$8; s+=$9} END{printf "entries=%d mtree=%d install=%d changelog=%d dotfiles=%d gzip=%d self=%d\n",t,m,i,c,d,g,s}' localdb-anatomy.tsv` →
`entries=1409 mtree=1409 install=51 changelog=0 dotfiles=0 gzip=1409 self=0`; no row carries a changelog or a dot
file, every mtree carries the gzip magic, and none lists `./.MTREE`.

Snapshot digests: `frozen/src/SHA256SUMS` (nine files) and `frozen/hostcap/MANIFEST.sha256` (six files; its own
sha256 `632ed044…`) both verify with `sha256sum -c`. All ten rows are tier A, `mined`, used-by
`corpus/knowledge/alpm-package-anatomy-r41.md`; recheck `on-release` for S227-S235 and `30d` for S236. Rows
touched old→new: none — `git diff --numstat 0e5805a1 9cc9aa77 -- corpus/SOURCES.md` is `10 0` (also `10 0` at
lane tip `71851d63`), so ten lines were added, none removed, and no older row's `status`, `recheck` or `used-by`
cell changed; the entry cites no row older than S227. S230 shares its URL (`…/lib/libalpm/add.c`) with S213 under
a distinct scope: S213 is commit order, S230 the local-database members.
````

## Touched surfaces

- Wrote this report and four receipts under `.ufo/waves/round-41/w1/C2ScribeGate/`
  (`quotes-check.txt`, `hostcap-sums.txt`, `digests.txt`, `sources-diff.txt`).
- Read-only everywhere else. No tracked lane file edited and no lane file written outside this report and the
  seat directory; the two modified tracked files in `git status` (`corpus/knowledge/pacman-exec-environment-r40.md`,
  `tools/check-self-assessment.py`) are not this seat's edits and were not touched here. No git write, no jj command, no host
  mutation, no package or service action, no sudo, no counter or census run, no subagent. No scratch directory
  was created (nothing to remove); no tool was installed or upgraded.

## Out of scope

- The `### Assimilation` and `### Spot-check` parts of `corpus/lessons/round-41.md`; SCORECARD, LOG, the C2
  entry's rule table, and the C1/C2 counters were not touched or run.
- The current draft's W04 sentence is neither confirmed nor used; I state only the verified S213/S230 URL
  sharing. Restoring the label needs the census receipt from whoever ran it.

## Artifacts

- `.ufo/waves/round-41/w1/C2ScribeGate.md` (this report)
- `.ufo/waves/round-41/w1/C2ScribeGate/quotes-check.txt`
- `.ufo/waves/round-41/w1/C2ScribeGate/hostcap-sums.txt`
- `.ufo/waves/round-41/w1/C2ScribeGate/digests.txt`
- `.ufo/waves/round-41/w1/C2ScribeGate/sources-diff.txt`
