VERDICT: holds
ROW: PA4
lines checked: frozen/src/add.c:168-206

Adversarial row verdict on PA4 of `corpus/knowledge/alpm-package-anatomy-r41.md` at 9cc9aa77,
source cell `S230 add.c:168-189`. Cell under test: *"During install libalpm stores three root members
inside the local database entry `<name>-<version>/`: `.INSTALL` becomes `install`, `.CHANGELOG` becomes
`changelog` and `.MTREE` becomes `mtree`, each with mode 0644; every other root dot file, `.PKGINFO` and
`.BUILDINFO` included, is skipped and kept for future use"* — value `.INSTALL=install .CHANGELOG=changelog
.MTREE=mtree`.

I could not construct a reading of the pinned source under which the cell is false. Each candidate
falsifier I could raise is listed below with the reason it fails, and the last three are conditions the
cell states only implicitly (they do not change its value). Pinned snapshot integrity first:
`sha256sum -c .ufo/waves/round-41/frozen/src/SHA256SUMS` → all nine files `OK`, so `add.c` is the
54d9411 revision the row cites (`FETCH.txt`: `.../pacman/-/raw/54d9411/lib/libalpm/add.c -> add.c`).

## What the source says, line by line

- `add.c:173-178` — exact-name map `.INSTALL`→`install`, `.CHANGELOG`→`changelog`, `.MTREE`→`mtree`.
- `add.c:179-183` — any *other* pathname whose first byte is `.` is logged at DEBUG, data-skipped and
  returns 0: `.PKGINFO` and `.BUILDINFO` land here and are not stored.
- `add.c:185` — `archive_entry_set_perm(entry, 0644)` runs on the entry *before* extraction, and
  `perform_extraction` (`add.c:113-130`) writes it with `ARCHIVE_EXTRACT_PERM`, so the mode is forced
  regardless of the archive's own mode.
- `add.c:186-188` — path `"%s%s-%s/%s"` = dbpath + `newpkg->name` + `-` + `newpkg->version` + `/` + dbfile;
  `be_local.c:669-682` (`_alpm_local_db_pkgpath`) builds the same shape for readers.
- `add.c:204-206` — `extract_single_file` routes every dot entry to `extract_db_file` **before** the
  filelist check (`:208`) and before NoExtract (`:224`), so both are irrelevant to the three stored names.

## Counter-readings tried, and why each fails

1. **A flag that bypasses the store — `ALPM_TRANS_FLAG_DBONLY`.** `add.c:525-531`: the db-only branch
   loops the archive and calls `extract_db_file` for `entryname[0] == '.'`, skipping only data entries.
   The three are still stored, so the cell holds under the flag; DBONLY changes what happens to *data*
   files, not to the dot files. The normal branch (`add.c:559-560`) reaches the same function through
   `extract_single_file`. There is no third caller: `grep -n 'extract_db_file\|extract_single_file' add.c`
   gives exactly `:168`, `:191` (definitions), `:205`, `:530`, `:560`.
2. **A second writer that renames or regenerates these files.** `_alpm_local_db_write`
   (`be_local.c:974-1095`) writes only `desc` (`:989`) and `files` (`:1095`); `grep -n '"mtree"\|"install"\|"changelog"' be_local.c`
   yields only *readers* (`:213` changelog, `:256` mtree, `:915` install existence test). So `install`,
   `changelog` and `mtree` have exactly one writer, `extract_db_file`.
3. **A dead branch (would make the skip clause vacuous).** A real makepkg artifact carries bare root dot
   names, so `*entryname == '.'` fires. `bsdtar -tvf sudo-1.9.17.p2-6-x86_64.pkg.tar.zst`:
   `-rw-r--r-- 0 root root 245 Jun 16 06:31 .INSTALL` (also `.MTREE` 7611, `.PKGINFO` 580, `.BUILDINFO` 6249,
   all mode 644, all without `./`); `licenses-20240728-1-any.pkg.tar.zst` shows the same shape with
   3 dot members and `0` dot-prefixed members outside the root. This matches `makepkg.sh.in:562-569`
   (`LC_COLLATE=C`, `dotglob`, `printf '%s\0' **/*` → relative bare names).
4. **"each with mode 0644" being wrong in practice.** Source forces it (`add.c:185`) and the host agrees:
   `find /var/lib/pacman/local -maxdepth 2 -name install -printf '%m\n' | sort | uniq -c` → `51 644`;
   the same for `mtree` → `1409 644`; entry dirs are `1409 755` (`_alpm_local_db_prepare` mkdir 0755,
   `be_local.c:933-953`).
5. **"skipped" being false, i.e. `.PKGINFO`/`.BUILDINFO` actually stored.** Host census over
   `/var/lib/pacman/local`: 1410 entries = 1409 package dirs + `ALPM_DB_VERSION`; `mtree` 1409, `install` 51,
   `changelog` 0, and **dot files inside entries 0** (`find … -mindepth 2 -maxdepth 2 -name '.*' | wc -l`
   → `0`). Those numbers reproduce the row's host column exactly.
6. **A stored copy that is not the archive member (so the mapping would be nominal only).** Direct
   byte comparison for the installed package whose archive I fetched:
   `/var/lib/pacman/local/sudo-1.9.17.p2-6/install` is 245 bytes, mode 644, sha256
   `8c764c770a40d169c1cc53c0a84977795fb514ae54c7f56a4b5a9f5e2dbf0c48`, identical to
   `bsdtar -xOf sudo-1.9.17.p2-6-x86_64.pkg.tar.zst .INSTALL | sha256sum`; the db `mtree` (7611 bytes, 644)
   sha256 `811958fab…ecc74` is identical to the archive's `.MTREE`. The entry holds only `desc`, `files`,
   `install`, `mtree` — no `.PKGINFO`, no `.BUILDINFO`.
7. **Corroboration from upstream's own reader (`-Qkk`), independent of add.c.** `check.c:333-337` strips a
   leading `./` and `check.c:341-345` maps `.INSTALL`→`install`, `.CHANGELOG`→`changelog` against
   `dbpath/local/<name>-<version>/`. The kept mtree of the sudo package lists
   `./.INSTALL … sha256digest=8c764c770a40d169c1cc53c0a84977795fb514ae54c7f56a4b5a9f5e2dbf0c48` — the same
   digest as the stored `install` — so the checker itself expects exactly the mapping the cell states.
   (`.CHANGELOG` is source-only: `add.c:175-176`, `check.c:343-344`, 0 host instances.)
8. **Error path.** `perform_extraction` on failure logs and returns 1 (`add.c:146-153`), which is summed
   into `errors` (`add.c:530`, `:560`) and aborts the transaction (`:576-600`); there is no fallback that
   writes a different name or a fallback mode. Failure loses the file, it does not alter the rule.

## Conditions the cell states only implicitly (not falsifiers; possible sharpening)

- **Skip scope is a pathname prefix, not "root".** `*entryname == '.'` (`add.c:179`, `:204`, `:529`) also
  swallows every entry below a root dot directory (`.<dir>/child`), which is broader than "root dot file".
  It is unreachable for makepkg artifacts (0 dot-prefixed non-root members in both sampled archives), so
  the cell is not wrong — it just describes the reachable domain.
- **`<name>-<version>` is the full version, epoch included.** 107 of 1409 host dirs carry a colon
  (`alsa-card-profiles-1:1.6.9-1`), consistent with `newpkg->version` in `add.c:186-187`; this agrees with
  PA8's full-version reading, so it is a notation, not an error.
- **"kept for future use" is the paraphrase of the comment at `add.c:180`** ("reserve all files starting
  with '.' for future possibilities"): the *names* are reserved, the files are not stored. The cell's own
  "is skipped" carries the meaning; if this row is ever re-edited, "skipped, the name reserved" removes the
  last ambiguity.
- **Storage is conditional on presence**: only a member the archive actually carries is stored (a package
  without `.MTREE` still loads, as the entry's own closing QUALITY bullet says).

Verdict: **holds**. Impacted axes: none (C2 depth only); no correction proposed, since the smallest safe
correction would be a wording sharpening of a clause that is already true.

## What I did not do

No package install/upgrade (`pacman` transactions are paused; no sudo), no build, no counter run, no census
run, no lane or git/jj mutation. Two packages were downloaded read-only from
`https://geo.mirror.pkgbuild.com/core/os/x86_64/` (accessed 2026-10-26) into scratch solely to compare
archive members with the host's local database; the sweep was read-only (`ls`, `find`, `stat`, `sha256sum`,
`bsdtar -t/-xO` from a scratch copy). No tool was installed or upgraded. Receipts:
`.ufo/waves/round-41/w1/C2RevPA4b/evidence.txt` (digest check, archive listings, host census, the two
sha256 pairs). Scratch `/fast/scratch/hyaku/tsukuroi-r41/C2RevPA4b/` removed.
