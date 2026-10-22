# SrcPacmanQuery — pacman(8) source for C2/P1 and C2/P2

Verdict: the pacman(8) page opened 2026-10-22 documents `-Qu` as a
**version-only, local-sync-database delta** that explicitly does not check
replacements, and documents `-Sy` as a metadata refresh and `-Scc` as a cache
clean that removes all cached package files. These facts bound what the
round-24 capture's `pacman -Qu` count of 3 can prove about a pending full
upgrade, and they support P1 and P2.

## How the page was opened

- The `read` tool failed on https://man.archlinux.org/man/pacman.8 with
  `ECONNRESET` twice (not a page absence). The page was then fetched with
  `curl -sL --max-time 40 https://man.archlinux.org/man/pacman.8 -o /tmp/pacman.8.html`:
  exit 0, 41121 bytes, sha256
  `531ebf4868faf7674a24ba0d9e4bb8af9ab99511ba86a5df87645ce0403fd495`.
- The same sha256 and byte count are recorded in `corpus/SOURCES.md`'s Search
  log for the round-15 re-open of the same URL on 2026-10-20, so this fetch is
  byte-identical to the page already opened this month; footer reads
  "2026-10-15 / Pacman 7.1.0", matching the host's installed `pacman` v7.1.0
  (`pacman --version`) and the local `/usr/share/man/man8/pacman.8.gz`
  (`.TH "PACMAN" "8" "2026\-10\-15" "Pacman 7\&.1\&.0"`).
- I also read the local `pacman.8.gz` (`zcat ... | col -b`), which contains the
  same sentences at the same option anchors; the quotes below are copied from
  the fetched HTML and cross-checked against the local man page.

## Exact quotes (fetched page)

1. `-Q, --query` (OPERATIONS, line 106):
   "Query the package database. This operation allows you to view installed
   packages and their files, as well as meta-information about individual
   packages (dependencies, conflicts, install date, build date, size)."

2. `-u, --upgrades` (QUERY OPTIONS (APPLY TO -Q), lines 513-518):
   "Restrict or filter output to packages that are out-of-date on the local
   system. Only package versions are used to find outdated packages;
   replacements are not checked here. This option works best if the sync
   database is refreshed using -Sy."

3. `-y, --refresh` (SYNC OPTIONS (APPLY TO -S), lines 613-619):
   "Download a fresh copy of the master package databases (repo.db) from the
   server(s) defined in pacman.conf(5). This should typically be used each
   time you use --sysupgrade or -u. Passing two --refresh or -y flags will
   force a refresh of all package databases, even if they appear to be
   up-to-date."

4. `-c, --clean` (SYNC OPTIONS (APPLY TO -S), lines 551-562):
   "Remove packages that are no longer installed from the cache as well as
   currently unused sync databases to free up disk space. ... Use one --clean
   switch to only remove packages that are no longer installed; use two to
   remove all files from the cache. In both cases, you will have a yes or no
   option to remove packages and/or unused downloaded databases." (ellipsis
   marks a skipped middle sentence, "When pacman downloads packages, it saves
   them in a cache directory. In addition, databases are saved for every sync
   DB you download from and are not deleted even if they are removed from the
   configuration file pacman.conf(5).")

5. `-S, --sync` provider/replacement handling (OPERATIONS, lines 143-148):
   "Packages that provide other packages are also handled. For example,
   pacman -S foo will first look for a foo package. If foo is not found,
   packages that provide the same functionality as foo will be searched for."

6. `-u, --sysupgrade` (SYNC OPTIONS, lines 598-605):
   "Upgrades all packages that are out-of-date. Each currently-installed
   package will be examined and upgraded if a newer package exists. A report
   of all packages to upgrade will be presented, and the operation will not
   proceed without user confirmation. Dependencies are automatically resolved
   at this level and will be installed/upgraded if necessary."

7. Version comparison rules (OPERATIONS, line 150):
   "When upgrading, pacman performs version comparison to determine which
   packages need upgrading." followed by the alphanumeric/numeric ordering
   lists and "Additionally, version strings can have an epoch value defined
   that will overrule any version comparison, unless the epoch values are
   equal."

## Finding 1 — what `-Qu` checks and what it does not check

- [obs] `-Qu` is `-Q --query` combined with the `-u, --upgrades` filter
  (quotes 1 and 2). It queries the **local** package database and restricts
  output to packages that are out-of-date "on the local system".
- [obs] The comparison is **version-only**: "Only package versions are used to
  find outdated packages". No other criterion (dependencies, conflicts,
  provides, build date, install reason) enters the filter.
- [obs] Replacements are explicitly **not** checked: "replacements are not
  checked here" (quote 2). The sync-side `-S` operation, by contrast, does
  handle providers/replacements: "Packages that provide other packages are
  also handled ... packages that provide the same functionality as foo will
  be searched for" (quote 5). So a package that a full upgrade would satisfy or
  replace via a *different* package name (a provider or rename) is invisible to
  `-Qu`.
- [obs] The page states the filter "works best if the sync database is
  refreshed using -Sy" (quote 2), so the result is a delta against the local
  sync database snapshot, not against upstream.
- [obs] The page contains **no** occurrence of the word "partial"
  (`grep -c -i partial /tmp/pacman.8.txt` → 0). The unsupported-partial-upgrade
  doctrine is not in pacman(8); it lives in ArchWiki System maintenance
  (existing rows S010/S047, opened 2026-10-19/2026-10-20). The man page only
  says `-y` "should typically be used each time you use --sysupgrade or -u".

## Finding 2 — what `-Sy` does

- [obs] `-y, --refresh` under SYNC OPTIONS (quote 3) downloads "a fresh copy
  of the master package databases (repo.db) from the server(s) defined in
  pacman.conf(5)". It is a metadata refresh only: the quoted text describes no
  package install or upgrade. `-Sy` therefore changes the local sync-database
  snapshot that `-Qu` compares against, without changing installed packages.
- [obs] Two `-y`/`--refresh` flags "will force a refresh of all package
  databases, even if they appear to be up-to-date"; a single `-y` does not
  promise a forced rewrite. The page does not document any mtime-preservation,
  download-skip or mirror-snapshot behaviour; the explanation for the
  core/extra/multilib db mtimes staying at 2026-10-17 after the 2026-10-21
  20:32 `pacman -Sy --noconfirm` belongs to the P4 seat (ExecMirrorTimestamps),
  not to this page.

## Finding 3 — what `-Scc` does

- [obs] `-c, --clean` is a SYNC option (quote 4): it removes from the package
  cache packages "that are no longer installed", plus "currently unused sync
  databases". `pacman -Scc` is `-S` with two `--clean` switches, which per the
  same quote removes "all files from the cache"; both forms present "a yes or
  no option to remove packages and/or unused downloaded databases" (so
  `--noconfirm` bypasses the prompt). It is not an upgrade and does not touch
  installed packages.
- [obs] The capture's `pacman -Scc --noconfirm` (2026-10-22 04:10:08) and
  `pacman -Scc` (04:10:19) are this documented all-files cache clean.
- [obs] A read-only probe of `/var/cache/pacman/pkg` (2026-10-22) shows **4
  directory entries, all empty `download-*` scratch directories owned by
  `alpm` (mode 700), and 0 regular files**:
  `ls -1 /var/cache/pacman/pkg | wc -l` → 4; `find -maxdepth 1 -type f |
  wc -l` → 0; the four `download-*` directories are the only entries. The
  capture's cache count of 4 therefore counts those directories, not package
  files; the cache holds no `*.pkg.tar.*` file. This is consistent with the
  `-Scc` documented all-files removal and is reported as an observation for the
  P5 seat (SrcPaccache) to fold into the rollback-by-cache analysis.

## Finding 4 — what a `pacman -Qu` count can and cannot prove about a pending full upgrade

Given quotes 1, 2, 5, 6 and 7:

- [obs] It **can** prove: the number of installed packages whose version in the
  local sync database is newer than the installed version, per pacman's version
  comparison (quote 7), evaluated against the local sync-database snapshot as of
  its last refresh. The capture's `pacman -Qu | wc -l` → 3 (capture lines
  39-47) is exactly such a count: 3 version-out-of-date rows against the local
  sync DBs.
- [obs] It **cannot** prove that a full upgrade touches exactly that many
  packages. `-Su`/`-Syu` "examine[s]" each installed package but "Dependencies
  are automatically resolved at this level and will be installed/upgraded if
  necessary" (quote 6), so the transaction set of a full upgrade can be larger
  than the `-Qu` row count (extra dependency installs/upgrades).
- [obs] It **cannot** prove the absence of replacement/provider-driven changes:
  "replacements are not checked here" (quote 2), while `-S` does search
  providers (quote 5). A package that an upgrade would satisfy through a
  different package name is invisible to `-Qu`, so `-Qu` output is not a
  complete upgrade plan.
- [obs] It **cannot** prove anything about upstream freshness: the page ties
  the filter to the local sync DB ("works best if the sync database is
  refreshed using -Sy", quote 2). A count of 3 against local metadata is not a
  statement that upstream has only 3 pending packages.
- [obs] It **cannot** prove that the pending set is safe to apply: the page
  contains no statement about boot-chain hooks, initramfs regeneration, or
  package-news checks. The host's `libinput 1.32.0-1` installed == sync
  (capture lines 73 and 88) is a separate observation, not a `-Qu` result.
- [obs] For P2 (partial-upgrade residue): `-Qu` lists only packages that are
  out-of-date. A package installed *newer* than its sync-database entry does
  not appear in `-Qu` output at all, so `-Qu` cannot prove the absence of
  installed-newer-than-sync residue. The capture's `local-newer-than-sync`
  probe (capture lines 57-59) is a separate comparison (`pacman -Sl` piped
  through `vercmp`), and the man page's version-comparison rules (quote 7) are
  the documented semantics that such a comparison must follow to be meaningful.
  The empty residue probe is therefore the right evidence, and its emptiness is
  not a `-Qu` property.

## Draft SOURCES rows

Column order matches the registry header in `corpus/SOURCES.md`:
`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`.
Ids are placeholders (S0NN-A/S0NN-B); the L1 assigns the next free registry
numbers (S086 is the last existing row, so S087 onward). Both rows duplicate
the pacman(8) URL already registered as S048/S049 (opened 2026-10-20); this is
intentional scope-separated reuse and will surface the disclosed W04
duplicate-URL warning. The new rows are required because the round-24 gate
demands a source row whose `opened` cell contains 2026-10-22, and the registry
treats `opened` as immutable for existing rows.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0NN-A | pacman(8) — https://man.archlinux.org/man/pacman.8 | docs | A | upgrade query limits: what `pacman -Qu` (the `-Q` query with the `-u, --upgrades` filter) compares and does not compare, and the version-comparison rules it relies on | QUERY OPTIONS (APPLY TO -Q) > `-u, --upgrades`: "Only package versions are used to find outdated packages; replacements are not checked here." and "This option works best if the sync database is refreshed using -Sy."; OPERATIONS > `-S, --sync` version comparison paragraph; Pacman 7.1.0 page dated 2026-10-15, opened 2026-10-22 (sha256 531ebf4868faf7674a24ba0d9e4bb8af9ab99511ba86a5df87645ce0403fd495) | `-Qu` reports only a version delta against the local sync database and explicitly does not check replacements, so a `pacman -Qu` row count is not the transaction set of a full upgrade and cannot prove upstream status or absence of replacement/provider-driven changes | queued | 2026-10-22 | on-release | corpus/knowledge/pause-lift-gate-r24.json |
| S0NN-B | pacman(8) — https://man.archlinux.org/man/pacman.8 | docs | A | refresh and cache clean semantics: `-Sy` (sync `-y, --refresh`) and `-Scc` (sync `-c, --clean` twice) and their documented effects | SYNC OPTIONS (APPLY TO -S) > `-y, --refresh`: "Download a fresh copy of the master package databases (repo.db) from the server(s) defined in pacman.conf(5)."; SYNC OPTIONS > `-c, --clean`: "Use one --clean switch to only remove packages that are no longer installed; use two to remove all files from the cache."; Pacman 7.1.0 page dated 2026-10-15, opened 2026-10-22 (sha256 531ebf4868faf7674a24ba0d9e4bb8af9ab99511ba86a5df87645ce0403fd495) | `-Sy` refreshes the local repo.db snapshot without installing packages; `-Scc` removes all cached package files (plus unused downloaded databases), so after it the cache holds no package files for rollback | queued | 2026-10-22 | on-release | corpus/knowledge/pause-lift-gate-r24.json |

Note for the L1: S049 (opened 2026-10-20) already carries the same `-u`
quote with scope "The installed/out-of-date query and `--needed` transaction
semantics...". The new S0NN-A row is scoped to the *upgrade query limits*
claim (what the count can and cannot prove), which is a distinct scope string,
so it does not collide with S049's scope; S0NN-B is new. If the L1 prefers to
avoid the W04 duplicate-URL warnings, the alternative is re-dating S049's
`opened` cell — which the registry treats as immutable — so new rows are the
clean route.

## Limits and out-of-scope items

- This seat quotes pacman(8) only. The partial-upgrade doctrine, downgrade
  semantics and mirror-snapshot cadence belong to the SrcSystemMaintenance and
  ExecMirrorTimestamps seats; I only record that pacman(8) is silent on
  "partial" and on download-skip/mtime-preservation behaviour (grep of the
  fetched page found zero "partial" occurrences and no mtime mechanism).
- I did not run any pacman command; every host probe was read-only (`ls`,
  `find`, `vercmp --help`, `pacman --version`, `zcat` of the local man page).
- The cache-directory observation (4 `download-*` directories, 0 package
  files) is a live read-only probe from this seat and is offered to the P5
  seat as an observation; the `-Scc` cache-clean consequence is already
  documented by quote 4.

## Optional Search log paragraph (draft)

Round-24 C2/P1-P2 source open (2026-10-22, SrcPacmanQuery seat): opened
https://man.archlinux.org/man/pacman.8 (via `curl`, after two `ECONNRESET`
failures of the read tool) — sha256
`531ebf4868faf7674a24ba0d9e4bb8af9ab99511ba86a5df87645ce0403fd495`, 41121
bytes, footer "2026-10-15 / Pacman 7.1.0", byte-identical to the round-15
re-open of the same URL. Located quotes: "Only package versions are used to
find outdated packages; replacements are not checked here." and "Use one
--clean switch to only remove packages that are no longer installed; use two
to remove all files from the cache." Identified/screened/included 1 source
object (packman(8)) at two scopes (upgrade query limits; refresh and cache
clean semantics); excluded 0. Stop rationale: the two requested scopes are
both fully answered by this single page; the uncached `vercmp(8)` URL failed
with a TLS error (curl exit 35) but vercmp semantics were not required for
these two premises.

Scope: read=https://man.archlinux.org/man/pacman.8 (curl), /usr/share/man/man8/pacman.8.gz, /var/cache/pacman/pkg (ls/find), pacman --version, vercmp --help, and the lane capture .ufo/waves/round-24/capture/l1/capture.txt and l1-2/capture.txt; wrote=.ufo/waves/round-24/w1/SrcPacmanQuery.md; executed=curl -sL --max-time 40 https://man.archlinux.org/man/pacman.8 -o /tmp/pacman.8.html, sha256sum /tmp/pacman.8.html, python3 HTML-to-text extraction, zcat /usr/share/man/man8/pacman.8.gz, grep/grep -c on /tmp/pacman.8.txt, ls -1 /var/cache/pacman/pkg, find /var/cache/pacman/pkg -maxdepth 1 -type f, pacman --version, vercmp --help
Installs: none
