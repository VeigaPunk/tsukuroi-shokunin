ROW PA6 VERDICT: holds

Item R-1 — round-41 routed defect R41-PA6-UNJUDGED, round-42 disposition (wave w1, seat PA6Verdict).
This verdict does not change round 41's outcome (see Disposition at the end).

# Judged text and its three corrections

Row PA6 is `corpus/knowledge/alpm-package-anatomy-r41.md:31`. The corrections preamble (`:63-68`) states each
correction "is the reading that replaces the row text where they differ". PA6 has three amendment events, all
verified in the lane's git history (read-only `git show`; no mutation):

1. `9cc9aa77` — pre-dispatch refinement folded into the row text: "when that file is absent" became "when that
   file is absent, or present but failing to open (libalpm then also logs \"error while reading file\"; a TODO in
   check.c says the two cases are left unseparated)" (`git show 9cc9aa77 -- corpus/knowledge/alpm-package-anatomy-r41.md`,
   PA6 hunk).
2. `20c327b3` — appended the `--quiet`/`-Qp` bullet, now `:88-91`.
3. `6cc927df` — appended the third-NULL-path bullet, now `:98-102` ("Appended after the residual verdict, which
   therefore did not judge this bullet" — the unjudged text this seat now judges).

The file's corrections section carries two PA6 bullets; the third PA6 correction is the pre-dispatch refinement
folded into the row itself. The verdict below applies all three.

# Snapshot integrity

`sha256sum -c SHA256SUMS` in `.ufo/waves/round-41/frozen/src/` → 9/9 OK (receipt `PA6Verdict/sha256sums-check.txt`).
`be_local.c` = `52fc17e6a34209ca93c65413f8f8b1cda863c943154626ccb60fbc6d705bb1bc`, matching its SHA256SUMS line;
`check.c` = `3f86aa04…c4d217`, `query.c` = `1e13d329…0ad6a`, both matching. Snapshot pinned at upstream `54d9411`
(`FETCH.txt`), host pacman 7.1.0 / libalpm 16.0.1 (`pacman --version`, matches).

# Evidence per sentence (row as corrected)

1. **"`pacman -Qkk` (check level 2) runs `check_pkg_full`"** — `query.c:317-321`:
   `if(config->op_q_check) { if(config->op_q_check == 1) { ret = check_pkg_fast(pkg); } else { ret = check_pkg_full(pkg); } }`
   (S235 verified verbatim). The numeral "2" is set by pacman.c's option parsing, outside the snapshot; the
   dispatch semantics (1 → fast, else → full) plus the observed split support the operational claim: first-hand
   P1 (`-Qkk` → full-check notice) vs P3 (`-Qk` → `foo: 3 total files, 0 missing files`, rc=0) below; receipts
   §1/§7 agree.
2. **"which opens the kept local `mtree`"** — `check.c:314` `mtree = alpm_pkg_mtree_open(pkg);`, which dispatches
   through `pkg->ops->mtree_open(pkg)` (package.c:462-466, fetched this round, see Grounding note). Local-db
   packages get `local_pkg_ops` (`be_local.c:621-623`) whose `.mtree_open = _cache_mtree_open` (`:334`, `:363`);
   it builds `<dbpath>/local/<name>-<version>/mtree` (`be_local.c:255-256`) and opens it with
   `_alpm_archive_read_support_filter_all` + `archive_read_support_format_mtree` (`:267-268` — S234's "every
   filter and the mtree format, so the kept gzip file reads back").
3. **"when that file is absent"** — `be_local.c:258-261` `if(access(mtfile, F_OK) != 0) { /* there is no mtree
   file for this package */ goto error; }` → `error:` `:280-282` `free(mtfile); return NULL;` — silent, no log.
   First-hand P1: `pacman -Qkk --dbpath <S>/fix/db --root <S>/fix/root foo` → `foo: no mtree file`, rc=0.
4. **"or present but failing to open (libalpm then also logs \"error while reading file\")"** —
   `be_local.c:270-275`: open failure → `_alpm_log(… _("error while reading file %s: %s\n"), mtfile,
   archive_error_string(mtree))` at `:271-272`, then free + `GOTO_ERR` → NULL. First-hand P4: stderr
   `error: error while reading file …/fix/db/local/foo-1.0-1/mtree: Unrecognized archive format`, stdout
   `foo: no mtree file`, rc=0.
5. **TODO gloss — as corrected, three cases not two** — `check.c:316` `/* TODO: check error to confirm failure
   due to no mtree file */` treats any NULL as "no mtree file". `_cache_mtree_open` (function spans
   `be_local.c:251-283`; `return NULL;` at `:282`, closing brace `:283`) returns NULL by exactly three paths:
   absent (`:258-261`, silent), `archive_read_new() == NULL` (`:263-265`, `GOTO_ERR`, no "error while reading
   file" log — no such call exists in that branch), open failing (`:270-275`, logged). The row text still reads
   "the two cases"; bullet 2 (`:98-102`) explicitly corrects "the TODO at `check.c:316` conflates the three, not
   two", and under the preamble that correction is the replacing reading. As corrected: accurate.
6. **"it prints a \"%s: ... mtree file\" notice" — as corrected, only without `--quiet`** — `check.c:317-318`:
   `if(!config->quiet) { printf(_("%s: no mtree file\n"), pkgname); }`; `:317` is the only gate on that printf.
   Value cell `no mtree file` matches the format string verbatim; source cell S231 `check.c:295-321` covers the
   function head through the NULL branch with the quoted printf at `:318`. First-hand: P1 (notice) vs P2
   (`--quiet` → no notice; only unrelated sync-db warnings), rc=0 both.
7. **"and returns 0"** — `check.c:320` `return 0;`, outside the quiet gate (bullet 1's "the return value is 0
   either way").
8. **"so such a package adds zero errors to the check"** — `check.c:320` returns before any error counting (the
   only error-bearing exit is `:434` `return (errors != 0 ? 1 : 0);`); the caller sets `ret = 1` only when
   `value != 0` (`query.c:441-444`, `:503-505`). First-hand: P1 rc=0; P8 (whole-db `-Qkk`, no target) rc=0;
   positive control P9 (valid kept mtree, tampered root file) → Size/SHA256 mismatch warnings,
   `foo: 3 total files, 1 altered file`, rc=1 — the zero is specific to the NULL-mtree path.
9. **"while `-Qk` (level 1) runs the fast check"** — `query.c:318-319`. First-hand P3: same absent-mtree state,
   `foo: 3 total files, 0 missing files`, rc=0 — the fast path never touches the mtree.
10. **Bullet 1 `-Qp` clause** — "The same `check_pkg_full` runs for `pacman -Qpkk <file>`: a loaded package file
    keeps libalpm's default mtree opener, so the archive's own `.MTREE` is never opened there and the "no mtree
    file" notice is printed although the file carries one". `query.c:467-468`:
    `if(config->op_q_isfile) { alpm_pkg_load(config->handle, strname, 1, 0, &pkg); }` (full=1, validation=0);
    the loaded package flows through the same `display()` (`:503`) and check dispatch (`:317-321`).
    `be_package.c:140-152`: `get_file_pkg_ops()` copies `default_pkg_ops` and replaces only
    `changelog_open/read/close`; wired at `be_package.c:658-660` (`newpkg->origin = ALPM_PKG_FROM_FILE; …
    newpkg->ops = get_file_pkg_ops();`). Grounding closed this round (below): the default opener is
    `_pkg_mtree_open`, an unconditional NULL stub — so the check never opens the archive's `.MTREE` and no
    "error while reading file" can be logged on this path. First-hand: P5 (`-Qpl` on the same archive lists
    `usr/`, `usr/bin/`, `usr/bin/foo` — the archive's `.MTREE` is present and parsed for the filelist via
    `be_package.c:447`, called at `:623`) vs P6 (`-Qpkk` on the same archive → `foo: no mtree file`, rc=0, no
    "error while reading file" on stderr) and P7 (`-Qpkk --quiet` → no notice, rc=0). Committed receipts:
    `.ufo/waves/round-41/w1/C2RevPA6b/qkk-fixture-receipts.txt` §9 (three variants — local entry present with
    valid mtree / local entry moved away / archive without `.MTREE` — all `foo: no mtree file`, rc=0).
11. **Bullet 2 (third NULL path)** — verified clause by clause from the frozen file: three paths (`:258-261`
    silent, `:263-265` unlogged `GOTO_ERR`, `:270-275` logged), all converging at `error:` → NULL (`:280-282`),
    all reaching `check.c:315-320` (notice unless `--quiet`, `return 0`). The correction's line citations
    (`be_local.c:251-283`, `:258-261`, `:263-265`, `:270-275`; `check.c:316`) are all exact.
12. **Host cell "branch unreached on this host: mtree 1409 of 1409 entries"** — receipt verified:
    `.ufo/waves/round-41/frozen/hostcap/localdb-anatomy.tsv` = header + 1409 entries; awk count
    `entries=1409 mtree_present=1409 mtree_missing=0`.

# Grounding note closed this round

Both round-41 seats disclosed that `default_pkg_ops` is defined outside the pinned snapshot (package.c was not
pinned), leaving bullet 1's mechanism clause resting on `be_package.c:140-152` plus observed behavior
(`.ufo/waves/round-41/residual/C2RevPA6c.md`, "Grounding note"; `w1/C2RevPA6b.md`, "What I did not do"). I
fetched package.c at the same pinned commit — read-only HTTPS GET,
`https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/package.c`, same channel as `FETCH.txt`,
sha256 `08a8061b14e25f3e42100eeb4565c5e27efc102aeb7f73f1474fef5e96ed0433` (receipt `PA6Verdict/package-c-fetch.txt`):
`default_pkg_ops` at `:143` sets `.mtree_open = _pkg_mtree_open` (`:173`), and `_pkg_mtree_open` (`:121-123`) is
`return NULL;` unconditionally. The clause is now source-grounded, and the observed behavior (receipts §9; my
P5-P7) matches it exactly — including why no "error while reading file" appears on the `-Qpkk` path.

# Residual disclosures (not defects)

1. The `archive_read_new()` allocation-failure path (`be_local.c:263-265`) is cited from source only; not
   exercised at runtime (needs an injected OOM). `GOTO_ERR`'s macro body is outside the snapshot; the verdict
   does not depend on its logging behavior — the claim on that path is only the absence of an "error while
   reading file" log, verifiable from `:263-265` alone. Carried unchanged from both prior seats.
2. The "check level 2" numeral rests on pacman.c's option parsing (outside the snapshot); the dispatch semantics
   (`query.c:318-321`) and the observed split (P1/P3; receipts §1/§7) support the operational claim.
3. Citation slip in the round-41 receipts file (not in any correction bullet): `C2RevPA6b/qkk-fixture-receipts.txt`
   says the isfile load is at "query.c:487"; the load is at `query.c:468` (`:487` is the `pm_printf` for
   "package '%s' was not found"). Both correction bullets cite `:467-470`/`:467-468` correctly. No effect.
4. My fixture wrote `pkgarch` in `.PKGINFO` (pacman expects `arch`), producing a harmless
   `warning: foo: unknown key 'pkgarch' in package description`; the package loaded, the mtree parsed (P5) and
   the check ran (P6/P7) — no PA6 claim affected.
5. The decision-table row (`:46`, symptom "`pacman -Qkk <pkg>` prints \"no mtree file\"…", triage
   `ls /var/lib/pacman/local/<name>-<version>/`) stays accurate for its stated symptom; the `-Qp` gap C2RevPA6b
   noted applies to a different symptom and is covered by bullet 1's clause. Not part of this verdict proper.

# What I did not do

- Did not run `tools/check-package-anatomy-r41.py`, the census, or the census selftest (not this item;
  planner/exec seats own the measurement).
- Did not exercise the allocation-failure path at runtime (disclosure 1).
- Did not rerun receipts §3-§8 of C2RevPA6b as such; my P1-P4, P8, P9 cover the same ground first-hand.
- No tool installs or upgrades (none needed). No host state touched: every pacman call was a read-only query
  with `--dbpath`/`--root` pointing into `/fast/scratch/hyaku/tsukuroi-r42/PA6Verdict/fix`; the only network
  action was the read-only GET of package.c at the pinned commit. No lane file written except this report and
  the receipts below.

# Disposition

R41-PA6-UNJUDGED asked for "a committed row verdict on PA6 with all three corrections" (`corpus/lessons/
round-41-verifier-spotcheck.md:150-152`). This file is that verdict: with the pre-dispatch refinement and both
appended bullets applied, every clause of row PA6 is supported by the pinned snapshot and first-hand
reproduction; nothing in it is false or missing a condition. Round 41's outcome is unchanged — the kill rule
fired at `6cc927df` and C2 stays "does not verify: depth `unchanged`" (`corpus/lessons/round-41-verifier-spotcheck.md:88-94,113`);
this verdict is the round-42 disposition only.

Receipts: `.ufo/waves/round-42/w1/PA6Verdict/` — `sha256sums-check.txt`, `repro.sh`, `repro-output.txt` (P1-P9),
`package-c-fetch.txt`, `package.c` (fetched bytes), `line-pins.txt`.
