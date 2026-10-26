VERDICT: defect-found

Item C2-31 (attack the C2 framing: province fit, PA3/PA7 drift, novelty, expansion grade).
Read-only seat: no clone, no scratch dir created (`/fast/scratch/hyaku/tsukuroi-r41/C2CritAxis/` not needed and not
made), no counter run, no census run, no host mutation, no tool installs. Receipts: `C2CritAxis/receipts.txt`.

## 1. Is a source-reading entry on package anatomy a depth move here? — Yes for 7 of 8 rows; PA7 is not

The Core sentence the entry claims is `PROVINCE.md:8-9` — "pacman state (`pacman -Qkk` verify loops, foreign/AUR
census, `.pkg.tar.zst` receipt discipline)". Under that sentence PA1/PA2/PA5 are the package file as a receipt, PA4/PA6
are the local database and the `-Qkk` loop, PA8 is the version comparison an `-Syu`/pin question turns on. That is
host state an operator acts on, not packaging doctrine.

The strongest evidence that this is depth and not doctrine is PA6: it changes the meaning of a Core command's
silence. `check_pkg_full` opens the kept `mtree`; on `NULL` it prints and `return 0`
(`.ufo/waves/round-41/frozen/src/check.c:315-321`), so a package with no kept mtree adds **zero** errors to `-Qkk`.
An operator reading `-Qkk` clean as integrity is wrong, and the entry's decision-table row
(`corpus/knowledge/alpm-package-anatomy-r41.md:46`) gives the read-only counter-check. PA4, PA5 and PA8 are host-measured
and I re-derived their numbers: `entries=1409 mtree=1409 install=51 changelog=0 dotfiles=0 gzip=1409 self=0`
(`receipts.txt` §1, from `frozen/hostcap/localdb-anatomy.tsv`), and `vercmp 1:1.0-1 2.0-1 = 1`,
`vercmp 0:2.0-1 2.0-1 = 0`, `vercmp 1.0 1.0-5 = 0` reproduced on the host (§2). PA7's man-page counts reproduce too
(5 lines "This function is run inside", §3).

Counterweight the entry already states: PA2 and PA3 are host-unmeasured (`alpm-package-anatomy-r41.md:27-28`) and PA6's
branch is unreached. So the honest depth credit is 7 rows of content, 5 of them host-grounded, 2 source-only — not 8
host-verified rows. That is still a depth move (round 40 carried four source-only rows), but any report that says
"8/8 rows verified on the host" would be false.

## 2. Do PA3 and PA7 drift into build advice? — PA3 no, PA7 yes

**PA3: no drift, but a source gap.** Its subject is makepkg's listing order
(`makepkg.sh.in:558-569`: `export LC_COLLATE=C`, `shopt -s dotglob globstar`, `printf '%s\0' **/*` — read at
`frozen/src/makepkg.sh.in:560-569`), but its operator use is reading a package file
(`bsdtar -tf <pkg> | head -n 5`, entry `:44`). That is receipt discipline. The build-side half is explanatory, not
advice. **Defect:** PA3's second clause — "a load that is partial stops reading at the end of the first archive entry
after `.PKGINFO` has been parsed" — is not in its cited source. It is libalpm: `frozen/src/be_package.c:640-643`
(`if((!full || hit_mtree) && config) { break; }`), i.e. S228's window 595-656, not S229's 558-570. I grepped
makepkg.sh.in 560-569 for `partial|PKGINFO`: 0 matches (`receipts.txt` §7). The row cites only S229
(`alpm-package-anatomy-r41.md:28`) and the frozen counter's PA3 window is `('makepkg.sh.in', 558, 570)`
(`tools/check-package-anatomy-r41.py:80`), so the clause has no source check at all. Also imprecise as worded: the
break check is skipped for dot-file entries (`handle_simple_path` returns 1 and `continue`s, `be_package.c:373-385`), so
the stop point is the first **non-dot** entry after `.PKGINFO` — for makepkg's order the first data file, which is what
the entry means but not what it says.

**PA7: out of province.** PA7 (`alpm-package-anatomy-r41.md:32`) states PKGBUILD(5) function working directories and
fakeroot. Its subject is the build recipe, not a package file, a local database entry, a `-Qkk` loop or a version
comparison; its decision-table row (`:49`) has no host probe — `man -P cat PKGBUILD | grep -n 'This function is run
inside'` reads an installed man page, not host state. Its symptom cell ("A PKGBUILD function behaves as if in the wrong
directory") is an authoring symptom. `PROVINCE.md:25-28` owns detection and report of host state and refuses
install/upgrade/remove and restart; a build-recipe contract is the same class the lane itself refused **in this round**:
"Not taken: … the `install` directive sentence (staged `:50-51`; build-side, outside the province's read-only Core)"
(`corpus/lessons/round-41.md:50`). The same Gate admits PA7 two paragraphs later. That inconsistency is the finding, not
the province text alone.

The defence — "the round-38 flip condition demanded it" — does not hold as a scope grant. That flip condition was
written by the lane's own closure (`corpus/lessons/round-38.md:49`: "a revision that quotes PKGBUILD(5) for each
function's working directory and passes a QUALITY check"), and its purpose was to fix a **false** staged sentence
(`package()` in `$pkgdir`), i.e. a truth requirement. A self-set truth condition cannot enlarge the province; the
staged entry's in-province rows (PA1, PA4-PA6, PA8) stand on their own new sources this round regardless of PA7.

## 3. Is the novelty overstated? — the narrow claim holds; QUALITY 14's "never the rules" does not

What the base actually holds about the local mtree at `0e5805a1` (all read from `git grep`, `receipts.txt` §4-§5):
a `zcat` read of the kept file (`snapper-eacces-mechanism.md:144`, `degraded-triage-r4.md:599`) — which already
implies the gzip half of PA5; the mtree's field set and the mtree-vs-actual comparison semantics —
"The package mtree records `/set type=file uid=0 gid=0 mode=644` … the comparison is mtree-vs-actual, not privilege"
(`degraded-triage-r4.md:118-123`); `mtree present`/`local mtree files` notes (`package-state-plane.md:159,293`);
`.PKGINFO` field reads as provenance (`foreign-provenance-r6.md:97`); `vercmp` for direction (`SKILL.md:1245`) and a
downgrade/shadowing trap (`SKILL.md:2246`). No epoch-ordering statement exists at base (`receipts.txt` §6 — the three
`epoch` hits are unrelated). PA1's member list also appears at base, but only as a quoted sibling artifact marked
historical: "the sibling's second ref :140 (tarball listing '.BUILDINFO, .MTREE, .PKGINFO') is also intact at line 140.
Historical round-12 wave artifact; no operative claim" (`corpus/knowledge/adjacency-anchors-r19.json:386`). So
PA1/PA2/PA4/PA6/PA8 are new as **lane rules with their qualifiers** (must-be-present plus optional `.INSTALL` plus
zero-or-more data files; the load path; the extraction map; the missing-mtree branch; epoch-first order), and PA5's
self-exclusion is new; the *gzip* fact, the comparison semantics and the bare three-name listing are not.

`alpm-package-anatomy-r41.md:53-55` therefore overstates in one phrase: "the lane held local `mtree` reads **as a
tool** … **never the rules** PA1-PA8". The base holds at least one rule-level statement about the kept mtree
(`degraded-triage-r4.md:118-123`). The claim survives if scoped to *provenance and branches* (who writes the file, its
name in the local db, its self-exclusion, the missing-mtree branch, the load path) rather than to "the rules".

The measurement behind it is lexical: `NOVELTY` is ten exact identifiers
(`tools/check-package-anatomy-r41.py:115-116`: `extract_db_file`, `missing package metadata`, `LC_COLLATE=C`,
`exclude .MTREE`, `no mtree file`, `startdir`, `parseEVR`, `reserve all files`, `check_pkg_full`, `hit_mtree`) grepped
over `corpus SKILL.md PROVINCE.md` at BASE (`:259-266`). None of the two held mtree uses carries any of those strings,
so `novelty_base_hits 0` is near-tautological for a hand-picked identifier list. The declaration already declares the
C2 lexical checks as shape gates (`SCORECARD.md` "Round 41 — declaration"), so this is a disclosure gap in QUALITY 14,
not a false predicate.

## 4. `expansion improved` or `unchanged`? — `unchanged`; the depth axis is the one that moves

`expansion improved` is **not** defensible, on three independent grounds:

1. No coverage-map row exists. At tip `71851d63` `corpus/README.md` ends with the round-40 section; there is no round-41
   row (`tail -20 corpus/README.md`). The in-flight draft already says the opposite of improvement:
   "The C2 entry deepens the held pacman-state plane … and is **not new coverage**"
   (`.ufo/waves/round-41/w1/C2ScribeReadme/readme-round41-draft.md:5`) and "Round 41 promotes nothing, and the C2 entry
   is Core depth rather than new ground" (`:19`).
2. The lane's own stricter precedent. Round 40 graded a same-plane Core deepening `expansion: unchanged` and said so
   explicitly: "The closure agrees with the lane's grading under LEARNING.md … Note: the round-39 closure graded a
   same-plane deepening `improved`; this closure applies the stricter reading the lane itself argued"
   (`corpus/lessons/round-40-verifier-spotcheck.md:129-131`). The coverage measure is declared surfaces each linked to a
   new entry (`SCORECARD.md:192,224`), and this round declares none.
3. Nothing moves Frontier: C1 edits `run_selftest` only; the scrub record and NVMe SMART stay Frontier.

The defensible grading is **expansion: unchanged, depth: improved (ordinal stays 8)** — the shape round 40 used
(`corpus/lessons/round-40-verifier-spotcheck.md:104-105`). One wording risk in the README draft at `:24`: "so PA1–PA8
are the first text on an already-owned surface" is too strong given `degraded-triage-r4.md:118-123`; "first statement
of the archive itself on an already-owned surface" is true.

## Impacted axes

- **depth** — improved, but on 7 rows (5 host-grounded), not 8. PA7 is not a Core-depth row.
- **coverage / expansion** — must be recorded `unchanged`. A trend verdict of `expansion improved` in
  `corpus/lessons/round-41.md` or the closure would contradict the lane's README draft, its own round-40 reading, and the
  absence of a coverage row.
- **discernment** — unaffected by this item (non-author closure still pending).
- No other axis is touched; the frozen C2 predicate is not challenged by anything here (rules_verified 8, verdicts_ok 8,
  host_ok 6, source_ok 1 all stand as shape gates).

## Smallest safe correction (append-only; the frozen counter and predicate are untouched)

1. **Grade expansion `unchanged`** wherever the round's trend verdicts are written; keep `depth improved (8)`.
2. **PA7 boundary note** appended to the entry — keeps `rules_verified 8`, stops the out-of-province row from counting as
   Core deepening, and records the province tension instead of hiding it:

   > ## Boundary — PA7 is packaging-side, not host state
   > PA7 is retained because the round-38 flip condition asked for it (`corpus/lessons/round-38.md:49`), and it is the
   > one row here whose subject is a build recipe rather than a package file, a local-database entry, the `-Qkk` loop or
   > a version comparison. Its decision-table row reads an installed man page, not host state, so it grounds no operator
   > action on this host and grants no build advice. The same class was refused this round for the staged `install`
   > directive sentence (`corpus/lessons/round-41.md:50`). PA7 is not counted as Core deepening; PA1, PA4-PA6 and PA8
   > stand on the rows opened this round without it.

3. **PA3 source erratum** appended (do not edit the committed row; the counter reads its window):

   > Wave-1 correction — PA3's second clause. "a load that is partial stops reading at the end of the first archive
   > entry after `.PKGINFO` has been parsed" is libalpm, not makepkg: `be_package.c:640-643`
   > (`if((!full || hit_mtree) && config) { break; }`), row S228. The stop point is the first entry after `.PKGINFO`
   > that is not itself a dot file (`handle_simple_path`, `be_package.c:373-385`, continues without the break check), so
   > for makepkg's dot-files-first order it is the first data file. PA3's source cell names S229 only; the clause has no
   > source check in `tools/check-package-anatomy-r41.py:80` (window `makepkg.sh.in 558-570`).

4. **QUALITY 14 rewording** (replaces `alpm-package-anatomy-r41.md:53-55` first sentence):

   > QUALITY 14 (novelty stated, not overstated): the lane held the local `mtree` as a read tool
   > (`corpus/knowledge/snapper-eacces-mechanism.md:144`, `corpus/knowledge/degraded-triage-r4.md:599`), the mtree field
   > set and the mtree-vs-actual comparison (`corpus/knowledge/degraded-triage-r4.md:118-123`), `.PKGINFO` field reads
   > (`corpus/knowledge/foreign-provenance-r6.md:97`) and `vercmp` for direction (`SKILL.md:1245`). It held no statement
   > of the archive's member set, the load path, the local-database extraction map, the missing-mtree branch, the
   > packaging-function directories or the epoch-first order. The counter's novelty tokens are a lexical proxy (0 hits at
   > base `0e5805a1`); the per-row read is the verdict files.

5. **README draft `:24`**: "first text on an already-owned surface" → "first statement of the archive itself on an
   already-owned surface".

Optional precision nit, same class, not a defect: PA6's "prints a `%s: … mtree file` notice" is gated on
`!config->quiet` (`frozen/src/check.c:317-318`), so under `-q` the package is silent rather than printing; the
decision-table command does not use `-q`, so the action stands.

## What I did not do

Did not run `tools/check-package-anatomy-r41.py` (the L1's counter; my item is framing), did not run the census
`--selftest`, did not read the reviewer verdict files' contents (their first lines are the C2 predicate's input, not
mine), and did not attempt any host or lane mutation. Host values I re-derived are marked as re-run above; everything
else is quoted from a path:line or a frozen snapshot line.
