VERDICT: supports

Seat C2RevAddC, item C2-3 (tsukuroi lane round 39, hyaku run 8, wave w1). Judged rows TO3, TO4 and TO6
of `corpus/knowledge/pacman-transaction-order-r39.md` against `lib/libalpm/add.c` and `lib/libalpm/trans.c`
at pacman 54d9411, re-fetched live from gitlab.archlinux.org on 2026-10-26. All three rows hold at their
cited lines. No tool was installed (curl/sha256sum/diff preexisting); no pacman transaction run
(host-wide pause respected); read-only on lane content — only this report and the seat receipt dir written.

## 1. Live re-fetch and sha256

Scratch `/fast/scratch/hyaku/tsukuroi-r39/C2RevAddC` (mkdir -p, TMPDIR exported there). Command:

    curl -fsSL "https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/add.c" -o "$S/add.c"
    curl -fsSL "https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/trans.c" -o "$S/trans.c"
    sha256sum "$S/add.c" "$S/trans.c" .ufo/waves/round-39/frozen/src/add.c .ufo/waves/round-39/frozen/src/trans.c

Observed output:

    fd3136291885cae73ad00abab3d83de49ea0276f040e53cca3902cfb93cf58f1  <live add.c>
    637c1165790ddd1c9d80bb0bfed9d85b1f5baa9b8e5a2e323243c5764ac4ed07  <live trans.c>
    fd3136291885cae73ad00abab3d83de49ea0276f040e53cca3902cfb93cf58f1  .ufo/waves/round-39/frozen/src/add.c
    637c1165790ddd1c9d80bb0bfed9d85b1f5baa9b8e5a2e323243c5764ac4ed07  .ufo/waves/round-39/frozen/src/trans.c

`diff -q` on both pairs printed nothing and the chain echoed `LIVE-EQUALS-FROZEN`. Both live files are
byte-identical to the frozen snapshots and match `.ufo/waves/round-39/frozen/src/SHA256SUMS`
(add.c `fd313629…`, trans.c `637c1165…`). Every line number below is from these verified bytes.
Receipts kept: `.ufo/waves/round-39/w1/C2RevAddC/{add.c,trans.c,sha256sums.txt}`.

## 2. TO3 — per-package order (row: corpus/knowledge/pacman-transaction-order-r39.md:26)

Clause by clause in add.c at 54d9411:

- "Packages are added one at a time in transaction order": `_alpm_upgrade_packages` iterates
  `for(targ = trans->add; targ; targ = targ->next)` calling `commit_single_pkg(handle, newpkg, ...)`
  per package — add.c:669-686 (loop head :670, commit call :677).
- "the `pre_install`/`pre_upgrade` scriptlet runs from the package file before any file is extracted":
  `pkgfile = newpkg->origin_data.file;` add.c:463; pre scriptlet block add.c:467-474 calls
  `_alpm_runscriptlet(handle, pkgfile, scriptlet_name, newpkg->version, oldpkg ? oldpkg->version : NULL, 1)`
  (:472-473, is_archive=1). In trans.c, is_archive=1 extracts the scriptlet out of that archive:
  `_alpm_unpack_single(handle, filepath, tmpdir, ".INSTALL")` trans.c:378-381 (inside
  `_alpm_runscriptlet`, trans.c:337-421) — i.e. the .INSTALL is read from the package file. The payload
  archive is opened only afterwards (add.c:500-504) and the extraction loop runs at add.c:536-562
  (`extracting files` :536, `extract_single_file` :560), so the pre scriptlet precedes any file extraction.
- "then the files and the local database entry are written": extraction loop add.c:536-562, then
  `updating database` :596 and `_alpm_local_db_write(db, newpkg, INFRQ_ALL)` :599.
- "then `installed`/`upgraded` is logged": logaction switch add.c:617-632 (`installed %s (%s)` :618,
  `upgraded %s (%s -> %s)` :630) — strictly after the db write.
- "then the `post_install`/`post_upgrade` scriptlet runs from the local database's `install` file":
  add.c:638-647 — `/* run the post-install script if it exists */` :638,
  `char *scriptlet = _alpm_local_db_pkgpath(db, newpkg, "install");` :641,
  `_alpm_runscriptlet(handle, scriptlet, scriptlet_name, ..., 0)` :644-645 with is_archive=0, which in
  trans.c takes the copy path: `_alpm_copyfile(filepath, scriptfn)` trans.c:383 — the scriptlet body is
  the local db's `install` file, not the package archive.

Doc-cited ranges contain their anchors: pre 466-474 (code 467-474), 616-648 (comment :638, log line :630,
post block :638-647), loop 669-688 (loop :669-686). Host-column spot check (supplementary, not reproduced
counts): frozen capture `.ufo/waves/round-39/frozen/txcapture/pacman.log:123-124` shows
`installed systemd (261.1-1)` then `[ALPM-SCRIPTLET] Initializing machine ID from random generator.` —
post-scriptlet output following its own `installed` line, as the row's host column states.

## 3. TO4 — scriptlet argument order (row: corpus/knowledge/pacman-transaction-order-r39.md:27)

- Both scriptlet call sites pass the new version first: pre add.c:472-473 and post add.c:644-645 —
  both `_alpm_runscriptlet(..., newpkg->version, oldpkg ? oldpkg->version : NULL, ...)`.
- trans.c builds the shell line with ver before oldver: `. %s; %s %s %s` (scriptpath, script, ver, oldver)
  trans.c:400-402 when oldver is set → `$1` = new, `$2` = old; `. %s; %s %s` trans.c:403-405 otherwise.
- add.c passes oldver only when an old package exists (`oldpkg ? oldpkg->version : NULL`), so
  pre_install/post_install receive only the new version. Row holds.

## 4. TO6 — ldconfig once, skipped after a failed commit (row: corpus/knowledge/pacman-transaction-order-r39.md:29)

- After the per-package loop, `_alpm_ldconfig(handle)` runs exactly once, gated by
  `if(!skip_ldconfig)`: add.c:688-692 (call :691). It is the only `_alpm_ldconfig` call site in add.c
  (grep over the frozen src tree: add.c:691, remove.c:794, definition util.c:820).
- Failure path: `if(commit_single_pkg(handle, newpkg, pkg_current, pkg_count))` :677 →
  `trans->state = STATE_INTERRUPTED;` :679, `skip_ldconfig = 1;` :682, `ret = -1` :683; the next loop
  iteration returns early at add.c:673-675. A failed package commit therefore skips ldconfig and marks
  the transaction interrupted — exactly the row.
- "before the commit phase ends": `_alpm_ldconfig` runs inside `_alpm_upgrade_packages` before its
  `return ret` (add.c:691 before :694), and `_alpm_upgrade_packages` is invoked from the sync commit
  path `_alpm_sync_commit` after the removal step (sync.c:1354).
- `_alpm_ldconfig` itself no-ops when `$root/etc/ld.so.conf` or the ldconfig binary is absent
  (util.c:820-838) — the row's "runs once" is at the call level; no contradiction.

## 5. Boundary observations (not row verdicts)

- remove.c:794 also calls `_alpm_ldconfig(handle)` after the removal loop (gated by `run_ldconfig`,
  remove.c:786-795). In a sync commit that both removes and adds, ldconfig therefore runs twice — once
  after removals (remove.c:794) and once after adds (add.c:691). TO6's rule text is add-phase-scoped
  ("After all package adds, `ldconfig` runs once") and stays true, but the entry's end-to-end summary
  step "6. `ldconfig`, once (TO6)." (corpus/knowledge/pacman-transaction-order-r39.md:40) is imprecise
  for mixed remove+add transactions. Minor doc-precision note for the L1; it is not one of my rows and
  does not trigger the QUALITY 81 kill rule.
- The `installed`/`upgraded` logaction failure increments `errors` in the caller (not shown here) —
  not examined; out of my rows' scope.

## 6. What I did not do

- Did not run pacman or any transaction; did not reproduce the counter's host counts; did not judge
  TO1, TO2, TO5, TO7, TO8; did not re-verify the host columns beyond the pacman.log:123-124 spot check.
- No tools installed; no pacman transactions; no sudo; scratch removed after receipts were copied.

TO3: holds — corpus/knowledge/pacman-transaction-order-r39.md:26
TO4: holds — corpus/knowledge/pacman-transaction-order-r39.md:27
TO6: holds — corpus/knowledge/pacman-transaction-order-r39.md:29
