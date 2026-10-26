VERDICT: supports

Item C2-22 — re-open SOURCES rows S227–S236 at 9cc9aa77e30e0e23de2d4d2697b3b218ada02969.
All six checks pass for all ten rows; the census validate exits 0 with exactly the predicted
W04 for S230. No defect found. Three non-blocking boundary notes are listed at the end.

Method. Rows read at the pinned C2 commit (`git show 9cc9aa77…:corpus/SOURCES.md`, rows at
lines 236–245); the working tree (lane tip 71851d63) is byte-identical for this file
(`git diff --stat 9cc9aa77 HEAD -- corpus/SOURCES.md` → empty; `git merge-base --is-ancestor
9cc9aa77 HEAD` → ok), so the census run below read the same rows. Anchors were checked against
the pinned snapshots `.ufo/waves/round-41/frozen/src/` (`sha256sum -c SHA256SUMS` → all 9 OK)
and the host capture `.ufo/waves/round-41/frozen/hostcap/`. Receipts:
`.ufo/waves/round-41/w1/C2RevSourcesRows/{urls-curl.txt,snapshot-digests.txt,anchors-verify.txt,hostcap-verify.txt,census-validate.txt,columns-nf.txt}`.

1. URL resolves — PASS (9/9 HTTP 200; S236 own-work).
   `curl -sSfL -o /dev/null -w '%{http_code}'` per row URL → 200 rc=0 for all nine URL rows
   (S227 man.archlinux.org/man/alpm-package.7; S228–S231, S233–S235
   gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/…; S232 …/doc/PKGBUILD.5.asciidoc).
   One later re-run of the S227 URL hit a transient `curl: (35) TLS connect error … unexpected eof`
   before a 200 on immediate retry — host-side TLS flake, not a row defect (urls-curl.txt).
   S236 is own-work: its files exist (capture.sh, capture-meta.txt, MANIFEST.sha256,
   localdb-anatomy.tsv, vercmp.txt, man-pkgbuild-runinside.txt, mtree-pacman-head.txt under
   `.ufo/waves/round-41/frozen/hostcap/`).

2. URL ↔ snapshot ↔ sha256 agreement — PASS (9/9 byte-identical).
   `sha256sum -c SHA256SUMS` → all nine files OK. Re-fetching each upstream raw URL
   (pacman `-/raw/54d9411/…` for the 8 code/doc files, `man.archlinux.org/man/alpm-package.7.raw`
   for S227) and comparing sha256 against the snapshot → 9 MATCH, 0 DIFFER
   (snapshot-digests.txt). Every row's claimed snapshot sha256 equals the SHA256SUMS value
   (e.g. S228 `24e58906…`, S230 `fd313629…`, S236 manifest `632ed044…` = actual
   `sha256sum MANIFEST.sha256`).

3. Anchor line ranges vs pinned snapshot — PASS (all quotes inside their ranges; boundary
   notes for S229/S234 below). grep -n on the frozen files:
   - S227 alpm-package.7.raw 95–124: `.SH CONTENTS` at :94; required-members sentence at :100
     ("The following files must be present at the root of an ALPM based package:"), optional
     `.INSTALL` at :120, data-files sentence at :124 — range covers Metadata/Scripts/Data. ✓
   - S228 be_package.c: `_alpm_pkg_load_internal` 555–694 exact (signature :555, closing `}` :694);
     `.PKGINFO` branch 598–618 exact (:598 `if(strcmp(entry_name, ".PKGINFO")…`, :618 `continue;`);
     early stop 640–643 exact (:641 `if((!full || hit_mtree) && config) {`, :642 `break;`);
     metadata check 652–655 exact (:653 `_("missing package metadata in %s\n")`);
     `handle_simple_path` 373–385 exact (signature :373, `}` :385). ✓
   - S229 makepkg.sh.in: `list_package_files` 560–569 — function is 562–569 (signature :562,
     `}` :569); 560–561 are its two attached comment lines, and the entry's PA3 quote
     ("database files are placed at the beginning of the package regardless of") is at :560.
     `.MTREE generation` 615–620 — statements at 616–620 (:616 msg2, :617
     `list_package_files | LANG=C bsdtar -cnf - --format=mtree`, :619
     `--exclude .MTREE | gzip -c -f -n > .MTREE`, :620 touch); :615 is blank. ✓ (note below)
   - S230 add.c: `extract_db_file` 168–189 exact (signature :168, closing `}` :189 —
     `grep -n '^}'` confirms); dot-file dispatch 204–206 exact (:204 `if(*entryname == '.') {`,
     :205 `return extract_db_file(…)`, :206 `}`). Mode 0644 at :185, install/changelog/mtree
     mapping at :174/:176/:178, skip branch :179–184 — all inside. ✓
   - S231 check.c: `check_pkg_full` 295–321 — signature :295; the range ends at the no-mtree
     block close (:315 `mtree = alpm_pkg_mtree_open(pkg);`, :316 TODO, :318
     `printf(_("%s: no mtree file\n"), pkgname);`, :320 `return 0;`, :321 `}`); the function
     continues past 321, but the range is a deliberate window and fully grounds the teaches. ✓
   - S232 PKGBUILD.5.asciidoc: packaging functions 345–377 exact (`*package() Function*::` :345;
     "run inside" lines at :351 srcdir, :357 startdir, :365/:370/:377 srcdir); `epoch` 67–74
     exact (heading :67, "default value if left unspecified is '0'" :71, block ends :74);
     full version string 439–441 exact ('pkgver-pkgrel' or 'epoch:pkgver-pkgrel'). ✓
   - S233 version.c: `parseEVR` 39–75 exact (signature :39, `}` :75; "always assume 0 epoch"
     :61); `alpm_pkg_vercmp` 219–260 exact (signature :219, `}` :260; epoch→version→release-if-both
     at :249–253). ✓
   - S234 be_local.c: `_cache_mtree_open` 246–283 — function is 251–283 (signature :251, `}` :283);
     246–250 is its doc comment; the filter lines (:267 `_alpm_archive_read_support_filter_all`,
     :268 `archive_read_support_format_mtree`) are inside. ✓ (note below)
   - S235 query.c: display check dispatch 317–323 exact (:317 `if(config->op_q_check) {`,
     :318 `== 1` → :319 `check_pkg_fast`, else :321 `check_pkg_full`, closes :322/:323). ✓
   - S236 hostcap: capture.sh + capture-meta.txt + MANIFEST.sha256 with manifest sha256
     `632ed044…` (matches), captured 2026-10-26T16:14:04Z (capture-meta.txt `captured_utc`). ✓

4. Tier and kind fit CORPUS.md — PASS.
   Fleet `/home/vgpnk/Projects/shokunin/CORPUS.md:91-97`: kind enum
   spec|docs|paper|code|tool|dataset|talk|book|community|own-work; tier A = "primary or
   authoritative for that scope (spec, official docs, source code, original paper, maintainer
   statement, the lane's own re-runnable gate output)"; community never A. Rows: S227/S232
   docs A (official docs — alpm-docs 0.13.0-1, PKGBUILD(5) at pinned commit), S228–S231/S233–S235
   code A (upstream source at pinned commit 54d9411), S236 own-work A (the lane's own
   re-runnable capture: capture.sh is re-runnable — the entry's recheck line instructs
   re-running it). No community row, so E10 cannot fire. Anchors all carry revision
   (commit 54d9411 / snapshot sha256 / capture timestamp) — none is a bare homepage.

5. teaches grounded — PASS (10/10), each against its own anchor:
   S227 "names .BUILDINFO, .MTREE and .PKGINFO as required root members and .INSTALL as
   optional" ← alpm-package.7.raw:100,120. S228 "refuses a package file without .PKGINFO and
   reads .MTREE only on a full load" ← be_package.c:652-655,619,640-643. S229 "puts the dot
   files first and writes .MTREE as a gzip mtree listing that excludes itself" ←
   makepkg.sh.in:564-565 (LC_COLLATE=C, dotglob), :617-619 (--exclude .MTREE | gzip). S230
   ".INSTALL/.CHANGELOG/.MTREE kept as install/changelog/mtree; other root dot files skipped"
   ← add.c:173-184. S231 "no kept mtree adds zero errors to the full file check" ←
   check.c:315-321 (printf + `return 0;` with errors still 0). S232 "package/prepare/build/
   check in srcdir; verify in startdir" ← PKGBUILD.5.asciidoc:351,357,365,370,377. S233
   "epoch decides first, absent epoch is 0, release only when both carry one" ←
   version.c:61,249-253. S234 "opened with every decompression filter and the mtree format"
   ← be_local.c:267-268. S235 "level 1 fast check, higher level full mtree check" ←
   query.c:318-321. S236 host numbers ← localdb-anatomy.tsv (below).

6. used-by names the entry — PASS (10/10).
   Every row's used-by cell is exactly `corpus/knowledge/alpm-package-anatomy-r41.md`
   (SOURCES.md:236-245); the entry exists on disk (no E11 in the validate output) and its
   `source:` line reciprocally lists "S227 S228 S229 S230 S231 S232 S233 S234 S235 S236"
   (alpm-package-anatomy-r41.md:1).

7. 11 columns, no stray `|` — PASS.
   `awk -F'|'` NF=13 (11 cells + 2 boundary empties) for all ten rows, both at the pinned
   commit and in the working tree (columns-nf.txt). No cell contains a pipe.

8. Census validate — exit 0, lane ok, exactly the predicted W04.
   `TZ=UTC bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
   /home/vgpnk/Projects/shokunin tsukuroi` → 40 W04 lines, then
   `tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md`, exit=0
   (census-validate.txt). For S227–S236 the only W04 is:
   `tsukuroi	W04	S230 duplicate url gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/add.c across scopes`
   — as predicted: S230 shares the add.c URL (and snapshot sha256 fd313629…) with S213
   (SOURCES.md:222) under a different scope (S213 = per-package commit order, used-by
   pacman-transaction-order-r39.md; S230 = database members at install, used-by
   alpm-package-anatomy-r41.md; S230's scope cell explicitly says "distinct from S213's
   commit order scope"). W04 is a warning and does not affect the clean verdict. No E-code
   of any kind fired for these rows (or the lane).

9. S236 host values re-derived from the capture — PASS.
   `awk -F'\t'` over localdb-anatomy.tsv (9 columns; header
   entry/desc/files/mtree/install/changelog/dotfiles/mtree_gzip/mtree_lists_self):
   rows=1409, mtree=1409, install=51, changelog=0, dotfiles=0, mtree_gzip=1409,
   mtree_lists_self=0 — matches the teaches ("1409 of 1409 local entries keep a gzip mtree,
   51 keep install, none keeps a changelog or a dot file") and PA4/PA5 host cells.
   vercmp.txt carries `vercmp 1:1.0-1 2.0-1 = 1`, `vercmp 0:2.0-1 2.0-1 = 0`,
   `vercmp 1.0 1.0-5 = 0` (PA8 host). man-pkgbuild-runinside.txt: 5 "run inside" lines,
   4 `$srcdir` + 1 `$startdir` (PA7 host). mtree-pacman-head.txt lists `./.BUILDINFO` and
   `./.PKGINFO` (PA1 host). `sha256sum -c MANIFEST.sha256` → all 6 entries OK.

Minor non-blocking notes (no content misattribution; every quoted line sits inside its range):
- S229 anchor "`list_package_files` lines 560-569": the function's signature is at
  makepkg.sh.in:562; 560-561 are its attached comment lines (the PA3 quote is at :560), so the
  range is quote-anchored rather than signature-anchored. End :569 is the function's `}`.
- S229 anchor ".MTREE generation lines 615-620": the statements are at 616–620; :615 is blank.
- S234 anchor "`_cache_mtree_open` lines 246-283": the signature is at be_local.c:251; 246-250
  is the doc comment. End :283 is the function's `}`. (The entry cites the tighter
  `be_local.c:251-270`; both windows contain the filter lines :267-268.)
- S231 anchor "`check_pkg_full` lines 295-321" is a partial window of the function (it continues
  past :321); it ends exactly at the no-mtree block close that grounds the teaches.
If exact function-boundary anchoring is wanted, the S229 ranges would become 562-569 and
616-620 and the S234 range 251-283; as written they are wider-but-containing and I do not
count them as defects.

Not done (out of item scope): I did not re-run `tools/check-package-anatomy-r41.py` (the C2
counter belongs to other seats; my item is the six row checks plus the census validate), and I
did not audit the round lesson's `## Gate` block. No tool was installed or upgraded this
session (curl/gawk/git/sha256sum sufficed). Scratch /fast/scratch/hyaku/tsukuroi-r41/C2RevSourcesRows
was used for upstream fetches and removed after receipts were copied; no lane file outside
this report and its receipt directory was written.
