VERDICT: falsifies

Seat CritTrend, item G-5 (trend verdict attack). Lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, read at tip
`71851d63` with two in-flight working-tree edits (`git status --porcelain` → ` M corpus/knowledge/pacman-exec-environment-r40.md`,
` M tools/check-self-assessment.py`; `corpus/lessons/round-41.md` untracked). Every verdict below is scoped to that state
and says so. Nothing under `/tmp` is used as evidence; I created no scratch, clone or fixture, so there is no scratch dir to
remove and no seat dir receipt.

Read-only throughout: no counter was executed, no census selftest, no `tools/*.py`, no pacman transaction, no git mutation.
The counters are slow on a shared host and their receipts are already committed (`before/`, `after/`), so I read receipts
and snapshots instead — "not run by me" is stated per conjunct below. I made no edit anywhere except this report.

## Summary of verdicts

| Trend | Strongest attack | Verdict the evidence supports (at tip) | Flips on |
|---|---|---|---|
| expansion | the entry is held Core depth by its own first line and cites no coverage-map row; no Frontier move; no new source kind | **unchanged** | a README coverage-map row / Frontier→Core promotion for the package-file surface, or a new source kind |
| quality | zero existing entries re-verified in committed bytes at tip, the C2 read has no passing committed receipt, and the round's one over-general sentence (PA6) is still unmarked | **unchanged at tip; improved once the two in-flight items land** — `harmed` if PA6 lands as written | the S220 anchor correction committed + eight verdict files with ≥1 `holds`/0 `fails`; `harmed` if PA6 is left unqualified |
| discernment | the outside spot-check does not exist; the eight C2 verdict files are lane seats; three `Mistakes` rows name criterion gaps and `QUALITY.md` gained nothing | **unchanged** (not improved) | the closure's non-author spot-check of round-41 gate decisions **and** a grounded criterion for the R41-LABEL-SUFFIX class |

## 1. expansion — strongest case against `improved`

**The entry classifies itself as held Core depth, in its own scope sentence.**
`corpus/knowledge/alpm-package-anatomy-r41.md:7` — "Scope: the package-file side of the pacman-state plane (`PROVINCE.md`
Core, "`.pkg.tar.zst` receipt discipline")"; `PROVINCE.md:9` already names "`.pkg.tar.zst` receipt discipline" as owned
Core. The province file did not wait for this entry to own the surface; it declared it Core earlier. An entry that says
"this is the package-file side of a plane I hold" is a depth claim, and the round files it as one — `SCORECARD.md:2454`
gives C2 the axis `depth (sourced)`, and `SCORECARD.md` contains no capability row added this round
(`grep -c 'round 41' SCORECARD.md` → 0 outside the declaration).

**No coverage-map row and no Frontier move, so the LOOKING clause is unmet on its own terms.**
LEARNING.md's expansion bar is "net new admitted entries on uncovered ground, each citing its coverage-map row". Observed:

| Check | Command | Observed |
|---|---|---|
| entry cites a coverage-map row | `grep -n 'README\|coverage' corpus/knowledge/alpm-package-anatomy-r41.md` | no match (`none`) — the `source:` line (:1) cites S227–S236 only |
| README gained a map row | `grep -n 'Round 41' corpus/README.md` | `none` (last section is `## Round 40 — the libalpm execution environment…`, README:319) |
| note count | `git ls-tree -r --name-only <rev> corpus/knowledge/ \| grep -c '\.md$'` | base `0e5805a1` **61**, tip **62** (+1, the new entry; no existing note touched: `git diff --numstat 0e5805a1 HEAD -- corpus/knowledge/` → `62 0 corpus/knowledge/alpm-package-anatomy-r41.md` only) |
| sources | `git show <rev>:corpus/SOURCES.md \| grep -cE '^ {0,3}\| *S[0-9]{3,} *\|'` | 226 → 236 (+10 mined rows) |
| new kind of source | `git show <rev>:corpus/SOURCES.md \| grep -c 'man.archlinux.org'` | 35 → 36 — the man page is the 36th of its kind, not a new kind; the nine upstream rows are `code`/`docs` at pacman `54d9411`, the same pin rounds 38–40 opened, and the tenth is `own-work` (28 such rows at base) |

**One-round-old precedent, and it is the stricter reading the lane itself argued.** `corpus/lessons/round-40-verifier-spotcheck.md:129-133`:
"The entry is admitted and new relative to the base, but it deepens held update-safety Core ground; the coverage map gains
no uncovered area and no Frontier area moves … Note: the round-39 closure graded a same-plane deepening `improved`; this
closure applies the stricter reading the lane itself argued." Round 41 is the fourth pacman-plane entry in four rounds
(hook order r38 → transaction order r39 → exec environment r40 → package anatomy r41). Grading it `improved` reinstates the
reading corrected one round ago, on a shape the closure already refused.

**How expansion has actually moved before** (steelman, then why it does not apply): rounds 26 and 27 moved expansion by
entering Frontier areas — `corpus/README.md:233` "Round 26 — storage integrity (frontier area of the OS substrate)" with its
`### Frontier (round-26 addition)` at :241, and :250 "Round 27 — kernel taint (deeper entry inside the driver and firmware
area)". The round-26 condition for a Frontier area to become Core is a read-only census arm (`corpus/README.md:243`), and
round 40 restated this round's non-move with it (`corpus/README.md:333-336`). Round 41 adds no census arm and no Frontier
bullet; the only census change is four selftest fixture cases (`tools/tsukuroi-census.sh` +27 lines, one hunk), which are
gate cases, not a new plane arm.

**Contrary case, stated at full strength:** no note in the coverage map states the archive's own anatomy, and PA1, PA4, PA5
and PA6 have no held neighbour — `package-state-plane.md` holds *host measurements* (census, `-Qkk` rc semantics), not
upstream format rules. If "the coverage map did not hold" is read at note granularity, the ground is new. That reading is
not the one in force: it is exactly the reading round 40's closure rejected for a move of the same shape, and the province
(Core, `PROVINCE.md:9`) had already declared the surface owned.

**Verdict: expansion `unchanged`.** What would change it, in order of cost: (a) a README coverage-map row (a map-table row,
not a round section) naming the package-file surface as held, so the entry can cite it; (b) a Frontier area entered and
promoted with the round-26 read-only census arm (~`corpus/README.md:243`), e.g. package-file integrity or AUR build-side;
(c) a genuinely new source kind — a real `.pkg.tar.zst` opened (blocked by the pacman pause; a build inside
`unshare -rm` is the only route) or upstream test-suite/arena data; (d) an explicit retraction of the round-40 strict
reading, argued rather than assumed.

## 2. quality — strongest case against `improved`

**The one committed strengthening is a tool, and the round's entry-level work is not committed.** Round 40's closure
credited C1's kills to quality; taking that precedent seriously, round 41 does have one instance:

| Check | Command | Observed |
|---|---|---|
| C1 before | `before/c1-before.jsonl` at `0e5805a1` | `baseline_pass 1, neutral_pass 3, decoy_pass 1, mutants_applied 13, survivors 4, params 0`, exit 1 |
| C1 after | `after/c1-after-568c397.jsonl` at `568c397d` | `baseline_pass 1, neutral_pass 3, decoy_pass 1, mutants_applied 13, survivors 0, params 4` — predicate met |
| the four cases are fixture-driven, arm untouched | `git diff 0e5805a1 HEAD -- tools/tsukuroi-census.sh` (one +27 hunk in `run_selftest`, four `check` cases H5/H6/H9/H10); awk-extract `probe_storage_arm() {`…`^}` at base and tip, `sha256sum` | diff adds only the four cases; arm `71e6007e566e1af32feb495e04e4f291c75fdddb2b521d9822b7363fcdf34d56` at **both** revisions |
| frozen tool digests match the declaration | `sha256sum tools/score-selftest-mounts-r41.py tools/check-package-anatomy-r41.py` | `8306d999…07355c`, `c83e29a4…ac1819f` — equal to `SCORECARD.md:2454` |
| two tool registry rows landed | `git diff 0e5805a1 HEAD -- SKILL.md` | +2 rows (`selftest-mounts-r41`, `package-anatomy-r41`) at `SKILL.md:3119-3120` |
| existing entries re-verified / deepened | `git diff --numstat 0e5805a1 HEAD -- corpus/knowledge/` | only the new 62-line entry — **zero** existing notes in committed bytes |
| quality bar sharpened | `git diff --numstat 0e5805a1 HEAD -- corpus/QUALITY.md` | empty |

So at tip the quality instance is a held *gate* (the census is held ground: README map rows "`../tools/tsukuroi-census.sh`
(round-2 gate, TSUKUROI-R2-1)" and "(round-3 gate, TSUKUROI-R3-2)"), and zero knowledge entries were re-verified. LEARNING's
quality observable is "entries re-verified, deepened, or superseded by stronger ones"; a selftest gaining four cases is
neither supersession nor re-verification, which is why round 40's own outcome table files the same artifact under
`operability` (`SCORECARD` round-40 outcome: "operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS
(124 cases…)"). Crediting one artifact to two axes is the drift to name, not to repeat.

**What the round does have, but has not committed:** the one entry-level re-verification is the round-40 entry's appended
S220 anchor correction. `git status --porcelain` → ` M corpus/knowledge/pacman-exec-environment-r40.md`; the tree copy is
123 lines, `git show HEAD:corpus/knowledge/pacman-exec-environment-r40.md | wc -l` → 115, and the added note
(`pacman-exec-environment-r40.md:117-123`) re-measures the pinned PKGBUILD (`32d40dfd…`) and says to read the meson call as
111-117. At tip that is not in the round's bytes; the committed registry row still reads "`build()` meson call lines
110-117…" (`corpus/SOURCES.md:229`). On landing it is a real `entries re-verified` instance with a re-measured digest.

**The C2 read is not on record at tip.** `after/c2-impl-9cc9aa7.jsonl` (revision `9cc9aa77`) → `rules_verified 8, verdicts_ok 0`,
`verdicts` for all eight rows `{"holds": [], "partly": [], "fails": []}`; the predicate therefore does not pass at the only
committed C2 receipt. Eight lane verdict files can still fill it (the tool is designed to read them, `tools/check-package-anatomy-r41.py`
`VERDICT:` parse), but "no admitted entry fails its re-check" has no committed instance yet.

**My own counterexample test (the strongest available from local evidence) — the entry mostly survives.** I read every rule
cell against the pinned snapshots rather than trusting the writer:

| Row | Claim tested | Snapshot | Result |
|---|---|---|---|
| PA2 | only `.PKGINFO` sets metadata; version without a dash fails; `.MTREE` read only on a full load | `frozen/src/be_package.c:598` `.PKGINFO` branch, `:612-615` `strchr(version,'-')` → "invalid package version", `:604` `else if(full && …".MTREE")`, `:653` "missing package metadata" | **holds** |
| PA3 | partial load stops at the end of the first entry after `.PKGINFO` | `be_package.c:641` `if((!full || hit_mtree) && config) break;` reached only after `archive_read_data_skip` of the following entry (the `.PKGINFO` branch `continue`s at :620) | **holds** (precise to the line) |
| PA4 | three members kept as `install`/`changelog`/`mtree`, mode 0644, every other dot file skipped | `frozen/src/add.c:174-189` (`dbfile` map, `archive_entry_set_perm(entry, 0644)`), `:180` reserve comment, `:204-206` `*entryname == '.'` → `extract_db_file` | **holds** |
| PA6 | missing/failing mtree → notice and return 0 | `frozen/src/check.c:315-320`: `if(mtree == NULL) { /* TODO… */ if(!config->quiet) { printf("%s: no mtree file\n") } return 0; }` | **partly** — the notice is gated on `!config->quiet` (`check.c:317`); see defect below |
| PA7 | `package()`+`prepare()`+`build()`+`check()` in `$srcdir`, `verify()` in `$startdir`, `package()` under fakeroot | `frozen/src/PKGBUILD.5.asciidoc:348-351` (fakeroot, "All other functions will be run as the user calling makepkg", `$srcdir`), `:357` `$startdir`, `:365,:370,:377` `$srcdir` | **holds** |

**Defect found (smallest safe correction at the end):** PA6 states the notice unconditionally
(`corpus/knowledge/alpm-package-anatomy-r41.md:31` "it prints a "%s: ... mtree file" notice and returns 0"), and the
decision table repeats it (`:46` "`pacman -Qkk <pkg>` prints "no mtree file" and reports the package clean"). Under
`--quiet` nothing prints: a reader who detects the branch by its output is misled in exactly the mode a scripted audit
would use. This is `partly`, not `fails` — the error count (zero added) is right. Secondary nit, not part of the
correction: `:44` "the first members should be the dot files" is makepkg's ordering (PA3), not a format requirement — a
hand-built package may put `.PKGINFO` anywhere and still load (PA2 scans for it).

**Why that `partly` matters to the predicate:** the frozen rule is "a row counts only with >=1 holds and 0 fails"
(`SCORECARD.md:2454`; implemented at `tools/check-package-anatomy-r41.py:281-286`), a disjunction, so one lenient
`VERDICT: holds` file credits PA6 even if an honest reader files `VERDICT: partly` beside it. QUALITY 81 asks for *a*
committed non-author verdict, so the counter is not wrong — but "no admitted entry fails its re-check" is then weaker
than it reads for a row whose defect is a missing qualifier rather than a wrong fact. The closure should read PA6's
verdict files itself rather than trusting `verdicts_ok 8`.

**Verdict: quality `unchanged` at tip; `improved` once (a) the S220 anchor correction is committed and (b) the eight
verdict files land with ≥1 `holds` and 0 `fails` each; `harmed` if PA6 lands as written**, since the round then holds an
admitted sentence a lane critic found over-general and left unmarked (LEARNING: "an entry is found false or stale and left
unmarked"). If the closure instead adopts the round-40 loose reading (C1's four kills suffice), quality is already
`improved` at `568c397d` — but then say which artifact carries it and stop scoring the same selftest under operability.

## 3. discernment — strongest case against `improved`

**The outside spot-check does not exist at tip, and the round says so itself.**
`corpus/lessons/round-41.md:5-6` — "Seats are the lane, not outside reviewers (LEARNING.md); this round's non-author closure
is pending", and `:62-65` — "### Spot-check / Non-author closure pending. Candidates for it: one admit (S232 / PA7, or S230 /
PA4 with the host column) and the staged reject `:53-54`." LEARNING.md: "Each round a non-author — a fresh reviewer or the
operator — spot-checks a sample of that round's gate decisions, at least one admit and one reject, and records
`agree`/`disagree` with a reason in the round's lesson. **A subagent the lane dispatched is still the lane.**" The eight C2
verdict files this round's predicate demands are wave seats, so they satisfy QUALITY 81 (a per-row read) and cannot satisfy
the trend — by construction, not by accident: the counter reads only `C2Rev(PA<n>)*.md` under
`.ufo/waves/round-41/w1` and `residual` whose first line matches `^VERDICT: (holds|partly|fails)$`
(`tools/check-package-anatomy-r41.py:60,122,277-286`), so the predicate's read evidence is the lane's own seat output by
definition. Round 40's `discernment: improved` rested on the closure's own §4 table
(`corpus/lessons/round-40-verifier-spotcheck.md:112-126`), not on any lane artifact; a lane grading its own round
`improved` on the strength of a prior round's closure is self-attestation across rounds.

**The gate's own record shows three blind classes and the bar did not move.**
`corpus/lessons/round-41.md:71-73` — R41-LABEL-SUFFIX "none — no criterion asks a counter to be scored on a known-killed
mutant before freezing"; R41-CAPTURE-FIFO "QUALITY 82 (fixture views) does not cover instrumentation that reads fixtures";
R41-PIPEFAIL-SIGPIPE "none". Three mined mistakes, three criterion gaps, and `corpus/QUALITY.md` is byte-unchanged this
round (`git diff --numstat 0e5805a1 HEAD -- corpus/QUALITY.md` → empty; last row is 88). LEARNING step 3: "Mistakes are
mined too: each becomes a row in the round lesson's `## Mistakes` and, when no criterion caught it, a `QUALITY.md` criterion
citing that lesson." The rows landed; the criteria did not. That is the same omission class as "a disagreement is left
unlearned", self-found instead of spot-check-found.

**Evidence FOR the gate's taste (does not cure the gap, but tells the closure where to look).** I re-opened the round's
sampled reject myself: the staged sentence "`package()` runs inside `$pkgdir` under `fakeroot` and the others run inside
`$srcdir`" is false twice over — `frozen/src/PKGBUILD.5.asciidoc:348-351` puts `package()` in `$srcdir` under fakeroot, and
`:357` puts `verify()` in `$startdir`. The reject stands. So does the admit candidate PA7's quote
(`PKGBUILD.5.asciidoc:357` "This function is run inside `$startdir`."). But I am a lane seat: this is an input to the
closure's §4, not a substitute for it.

**Verdict: discernment `unchanged`** (not `improved`, not `harmed` — the round has not left a *spot-check* disagreement
unlearned because it has no spot-check yet). What would change it: the closure records a §4-style table for **round 41**
(≥1 admit, ≥1 reject, `agree`/`disagree` with reasons, in `corpus/lessons/round-41.md`) — then `improved` if it agrees; and
independently, one grounded criterion closes the R41-LABEL-SUFFIX gap. If the closure disagrees on a sampled decision and no
lesson lands, discernment is `harmed`.

## Smallest safe corrections (exact proposed text)

1. PA6 qualifier — `corpus/knowledge/alpm-package-anatomy-r41.md:31`, replace "it prints a "%s: ... mtree file" notice and
   returns 0" with "it returns 0 and, unless `--quiet` suppresses it (`check.c:317`), prints a `%s: … mtree file` notice";
   and `:46`, "`pacman -Qkk <pkg>` prints "no mtree file"" → "`pacman -Qkk <pkg>` prints "no mtree file" (nothing under
   `--quiet`)". Append-only alternative if the cell is already frozen: a one-line note after the table
   ("PA6 correction: the notice is gated on `!config->quiet`, `check.c:317`; the zero-error result is not").
2. QUALITY row for the R41-LABEL-SUFFIX class (`corpus/QUALITY.md`, next number):

> 89. **A counter that attributes kills is scored on a known-killed mutant before it is frozen (R41-LABEL-SUFFIX):** where a
> frozen counter decides a mutant was killed by matching a run against the baseline case's label, the counter's own
> pre-freeze run records at least one mutant the scored code provably kills under the label the counter expects, so the
> able-to-fail case exists before the predicate is declared; a reader that keys on `FAIL <label>:` from stderr and
> `PASS <label> (…)` from stdout compares two different keys, and a predicate requiring `survivors == 0` then scores a
> working selftest as vacuous (round 41's first C1 draft: `survivors 13` of 13 while nine mutants actually failed; 13 kills
> after `LABEL_TAIL` normalisation, `score-selftest-mounts-r41.py` at `e479fdc5`). The same class covers an exit-status
> assumption: a pipeline whose early-exiting consumer (`grep -q`, `head`) makes `pipefail` report a match as a failure reads
> a present fact as absent (R41-PIPEFAIL-SIGPIPE, `frozen/hostcap/capture.sh` first run exit 1, no `capture-meta.txt`).

3. Disposition wording — `corpus/lessons/round-41.md` "Round-40 routed defects" item 4 already points at "the appended note
   in this lesson's Gate", but no such note exists in the lesson at tip; the correction it means is the
   `pacman-exec-environment-r40.md:117-123` note. Until one of the two lands committed, round-40 §6.4 reads as unclosed and
   quality cannot claim an entry re-verified.

## What I did not do

- No counter, selftest, gate or `tools/*.py` run (host load; receipts read instead). C2's `verdicts_ok == 8` is
  therefore unverified by me beyond the receipt showing `0` at `9cc9aa77`, and the eight verdict files are still being
  written by wave seats.
- I did not read PA1, PA5 or PA8 against their snapshots (`be_local.c`, `makepkg.sh.in`, `version.c`) — my PA sample is
  PA2/PA3/PA4/PA6/PA7; the remaining three rows rest on the reviewer verdicts the predicate demands.
- I did not fetch any upstream URL; all source evidence is from `.ufo/waves/round-41/frozen/src/` (whose digests I did not
  re-check against `SHA256SUMS`), plus `frozen/hostcap/` only via the committed receipts.
- I did not inspect `.ufo/waves/round-41/w1/` seat reports beyond the directory listing (2 of 11 entries were directories
  with no content yet at read time), so no seat's read is vouched for here.
