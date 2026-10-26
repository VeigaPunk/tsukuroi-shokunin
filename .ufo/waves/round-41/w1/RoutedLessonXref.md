VERDICT: supports

Seat RoutedLessonXref — item R-5. All five routed defects of `corpus/lessons/round-40-verifier-spotcheck.md` §6
(lines 143-152) have a named round-41 artefact; both round-40 open items (R40-HOSTCELL-UNANCHORED,
R40-CONTROL-OWN-BASELINE) are NOT repeated. Gaps: one declaration-vs-disk naming drift (`controls-c1.jsonl`), the
`--scratch` fix still uncommitted at the tip, and three mid-wave pendings (lesson-Gate S220 note, the round report's
Sources & frontier line, R-1 not yet started). Method: read-only byte/receipt analysis only — no counter, census or
self-assessment run (§5). Lane tip at read time `71851d636ab1bffaf8fee5016617c88878a666f1` (`git rev-parse HEAD`).

## 1. The five routed defects → round-41 artefacts

| §6 (spotcheck line) | Routed defect | Round-41 artefact | Verification I ran |
|---|---|---|---|
| §6.1 (:143) R40-ANSWER-KEY, C1 half | counter passed by a self-reading selftest (`declare -f`/`${0}`/`${BASH_ARGV0}` prologue) and by a census missing a declared fixture; held-out H5/H6/H9 survive | Declaration d8b4d521 C1 row (SCORECARD.md:2465) + pre-data controls C1-K1/K2/K3 (:2483-2492); counter `tools/score-selftest-mounts-r41.py` frozen at e479fdc54 (decoy `DECOY_DELIM='R41DECOY'` :114, dead here-doc carrying every mutant text :122; kill attribution with `confirm_labels`/`confirmed` and a second run; `params` capture of the four declared table shapes; 13 frozen mutants incl. H5/H6/H9 **and new H10**); census change 568c397d adds the four cases (`R41-C1 H5/H6/H9/H10` labels at tools/tsukuroi-census.sh:3042,3048,3054,3061; diff vs base = 27 insertions, run_selftest only) | `git show d8b4d521:SCORECARD.md \| grep -c "Round 41 — declaration"` → 1; counter sha256 tip == freeze == `8306d9990b156ceb625eabbe942910fc0d09b20f350a7e8af1ff2237fd07355c`; `before/c1-before.jsonl` shows `baseline_pass 1, neutral_pass 3, decoy_pass 1, mutants_applied 13, survivors 4` (H10,H5,H6,H9), `params 0`, FAIL — the declared before-state byte-for-byte |
| §6.1 (:143) R40-ANSWER-KEY, C2 half | counter passed by a token-list writer and by affirmatively false rules without negations | Declaration d8b4d521 C2 row (SCORECARD.md:2466) + controls C2-K0..K8 (:2473-2481); counter `tools/check-package-anatomy-r41.py` frozen at e479fdc54: frozen source WINDOW per row (docstring :13), frozen `RELATIONS` (:97), `NEG` negation words (:117), per-row committed verdict files under `VERDICT_DIRS` (:60) read by `VERDICT_RE` (:122), ">=1 holds and 0 fails" rule (docstring :18-19) | counter sha256 tip == freeze == `c83e29a4f570422d5a975873460c4c5b061e33ac497b97d13c1383569ac1819f`; `controls/controls-c2.jsonl`: K1 token-writer FAIL `rules_verified 0`, K2 relation-literal writer FAIL `rules_verified 8, verdicts_ok 0`, K3/K4 X-false FAIL `rules_verified 6`, K5/K6/K7 verdict-gate FAILs, K8 candidate PASS — each control fails on exactly its named conjunct |
| §6.2 (:146) `first_fails` always empty; neutral flakiness under load; scratch kept after Ctrl-C | r40 counter scanned stdout; FAIL lines go to stderr | Counter e479fdc54 reads stderr (`:152` `err = p.stderr…splitlines()`, `:156` `fails = [l for l in err if l.startswith('FAIL ')]`, `:159` `'first_fails': fails[:3]`, `:284` `r['fail_count'] = …`); one serial retry for failed non-mutant runs (:248-259, comment "load flakiness"); `_cleanup` on SIGINT/SIGTERM (:128, handlers :223-224, :277). Wave items: **R-3** (`w1/RoutedFirstFails.md`, landed, first line `VERDICT: supports`), C1SentScratch (SIGINT test, in flight), C1ExecEnvMatrix (--jobs 1 vs 6 determinism, in flight) | `before/c1-before.jsonl`: every killed mutant M1-M9 carries non-empty `first_fails` (stderr `FAIL <label>…` lines) and `fail_count` 1-3; H5/H6/H9/H10 carry `first_fails: []`, `killed: false` — exactly the §6.2 defect inverted |
| §6.3 (:148) R40-TMP-MISROOT not yet shown able to fail | `check-self-assessment.py` extracted a 294 MB archive under /tmp; census child could not inherit TMPDIR | The self-assessment `--scratch` change: working-tree diff vs 71851d63 on `tools/check-self-assessment.py` — `census_case_count(repo, rev, scratch=None)` extracts under `dir=scratch` and gives the census child `TMPDIR` inside it (`child_tmp = os.path.join(work, ".census-tmp")`), threaded through `evaluate` (:441→:657) and a new `--scratch` CLI flag (:1097-1101). Wave item **R-1** (`RoutedSelfAssessScratch`) is dispatched to show the fix able to fail (base version vs working version) | `git diff 71851d636ab1… -- tools/check-self-assessment.py` shows exactly those hunks; the change is **uncommitted at the tip** (working tree only; dispatch item R-1 and wave item G-6 both say so) — see Gap 2 |
| §6.4 (:149) S220 anchor drift (110-117 vs 111-117) | registry row append-only | Wave item **R-2** (`w1/RoutedS220Anchor.md`, landed, first line `VERDICT: draft …`) with Draft A (one-line lesson-Gate note) and Draft B (appended entry sentence); **Draft B is already applied**: `corpus/knowledge/pacman-exec-environment-r40.md:118-123` "## Anchor correction (appended round 41; round-40 closure §6.4)" states `build() {` opens at :108, :110 blank, meson call :111-117, `-Dscriptlet-shell…` stays :115, row left as written per CORPUS.md rule 2 | `grep -n "110-117\|111-117" corpus/knowledge/pacman-exec-environment-r40.md` → :119,:121,:123; the lesson-Gate note (Draft A) is **not yet in** `corpus/lessons/round-41.md` (grep "110\|111" → no hit) — see Gap 3 |
| §6.5 (:151) W04 34 → 39 delta must be recorded in the report's Sources & frontier line | five same-URL rows declared distinct scopes | Wave item **R-4** (`w1/RoutedW04/` receipts landed: `census-now.txt`, `w04-delta.diff`, `attribution-controls.txt`); start receipt `.ufo/waves/round-41/before/sources-census-start.txt` = 39 W04 (`grep -c W04` → 39); live census now = **40** W04; `w04-delta.diff`: `39a40 > tsukuroi W04 S230 duplicate url …/lib/libalpm/add.c across scopes` — S230's scope cell (corpus/SOURCES.md:239) declares "distinct from S213's commit order scope" | the exact Sources & frontier line for the round report is still pending (report not yet written; lesson `## Sources census` has only the Start line) — see Gap 4 |

No R-seat exists for §6.1: it is addressed by the claims themselves (declaration + counters) and attacked by the
non-R seats C1CritDecoy/C1CritLabels/C1CritParams (C1) and C2CritXFalse + the C2RevPA<n>/<n>b verdict seats (C2) —
consistent with the spotcheck's "owner: tsukuroi, next round" routing through the planned row
(SCORECARD.md:2450-2454), which the declaration says it takes (:2457-2459).

## 2. Open item R40-HOSTCELL-UNANCHORED — NOT repeated

The round-40 mistake: a host cell written from memory ("on this host /tmp is a tmpfs") with no capture anchor
(`corpus/lessons/round-40.md:77`). Round 41's C2 entry does the opposite:

- PA2 host cell: "unmeasured: the package cache is empty and pacman transactions are paused, so the load path was
  read in source only" (`corpus/knowledge/alpm-package-anatomy-r41.md:27`); PA3: "unmeasured: the archive order
  needs a package file, and the cache is empty" (:28); PA6: "branch unreached on this host: mtree 1409 of 1409
  entries" (:31).
- Every host cell that DOES assert a host fact cites the frozen capture: PA1 → `mtree-pacman-head.txt` (:26),
  PA4/PA5 → `localdb-anatomy.tsv` (:29,:30), PA7 → `man-pkgbuild-runinside.txt` (:32), PA8 → `vercmp.txt` (:33).
- The entry's `## QUALITY check` states the split explicitly: "the host column is own-work capture only and states
  where it is unmeasured (PA2, PA3)" (:58), under QUALITY 86 (:57-58).
- The round-41 lesson's Mistakes table (:66-76: R41-LABEL-SUFFIX, R41-CAPTURE-FIFO, R41-PIPEFAIL-SIGPIPE,
  R41-LEXICAL-OVERREACH) contains no host-cell instance, and the SKILL/README draft items carry the same limit
  ("limits (PA2/PA3 unmeasured on host)", dispatch items C2-32/C2-33).

## 3. Open item R40-CONTROL-OWN-BASELINE — NOT repeated

The round-40 mistake: a pre-data control that failed its own baseline (`baseline_pass 0`), so its FAIL showed
nothing (`corpus/lessons/round-40.md:79`); the fix criterion is QUALITY 88's "violates exactly one named parameter"
— every other conjunct green. Round 41's controls:

- C1 (`controls/C1-K1-declare-f-prologue-on-base.jsonl`, `C1-K2-candidate-without-H9-case.jsonl`,
  `C1-K3-declare-f-prologue-on-candidate.jsonl`): `baseline_pass 1` and `capture_pass 1` in all three. K1/K3 fail
  only on the named parameter (`decoy_pass 0`, `decoys_failed ["D-all-mutant-texts"]`) with the other conjuncts at
  their expected values (K1 on base: `neutral_pass 3, mutants_applied 13, survivors 13, params 0` — the base's
  correct behaviour; K3 on candidate: `params 4`). K2 fails on its single named cause — the missing no-`subvol=`
  case — observed as `survivors 1` (H9) + `params 3`, i.e. one declared parameter, two observables; every other
  conjunct green (`baseline_pass 1, capture_pass 1, neutral_pass 3, decoy_pass 1, mutants_applied 13`).
- C2 (`controls/controls-c2.jsonl`, 9 rows): K1 `rules_verified 0` / verdicts_ok 8; K2 `verdicts_ok 0` / rules 8;
  K3, K4 `rules_verified 6` / verdicts_ok 8; K5, K7 `verdicts_ok 7`; K6 `verdicts_ok 0`; K8 PASS — in every FAIL
  row `host_ok 6, source_ok 1, duplicate_rows 0, duplicate_headings 0, novelty_base_hits 0` stay green, so each
  control fails on exactly its named conjunct and the counter's own machinery (host/source/duplicate checks) is
  exercised green in all of them.

## 4. Gaps

1. **`controls-c1.jsonl` declared but absent.** SCORECARD.md:2475 names the control outputs
   "`controls/controls-c1.jsonl`, `controls/controls-c2.jsonl`"; only `controls-c2.jsonl` exists — the C1 control
   receipts live in three per-control files (C1-K1/K2/K3-*.jsonl, committed at d8b4d521 per its stat) plus the
   before/after receipts. Same content, different shape than declared; a reader following :2475 finds no C1 file.
   Class: number-drift/landing (minor).
2. **The §6.3 fix is uncommitted at the tip.** `tools/check-self-assessment.py --scratch` exists only as a
   working-tree change (`git diff 71851d636ab1… -- tools/check-self-assessment.py` non-empty; tip's committed blob
   lacks `--scratch` at :1097). Until it is committed, R40-TMP-MISROOT's fix is not a lane artefact, and its
   able-to-fail demonstration (wave item R-1) had not started at my read time (no `w1/RoutedSelfAssessScratch/`
   dir). This is the weakest of the five mappings.
3. **The §6.4 lesson-Gate note is pending.** The entry correction is applied (Gap table above), but
   `corpus/lessons/round-41.md:86` says "see the appended note in this lesson's Gate" and no such note is in the
   Gate yet (no `110`/`111` hit in the lesson); R-2's Draft A supplies the text, integration pending.
4. **The §6.5 report line is pending.** R-4's receipts give the delta (39 → 40, new W04 = S230, declared distinct
   scope), but the round report's Sources & frontier line — the actual deliverable §6.5 asks for — is not written
   yet, and the lesson's `## Sources census` (:89-91) carries only the Start line.
5. **Declared residuals, not gaps** (named by the lane itself, carried here so the closure sees them):
   (a) a self-reader that strips here-documents before grepping still passes the C1 decoy (SCORECARD.md:2492-2493;
   wave item C1CritDecoy attacks it) — so §6.1's C1 selfref half is closed only up to this declared limit;
   (b) the C2 relation-literal writer still passes every lexical check (control K2 records it); the read rests on
   the per-row verdict files, of which PA3 has none yet and PA6 has only a `partly` (no `holds`) at my read time —
   `verdicts_ok` would be 6/8 now, predicate needs 8 (seats C2RevPA3/PA3b in flight);
   (c) the C1 retry covers non-mutant runs only, so a flaky mutant run can still misattribute a kill (wave item
   C1CritLabels attacks); (d) the planned row's "declare -f prologue as frozen should-fail arms" landed as pre-data
   controls K1/K3 rather than arms inside the counter's MUTANTS — functionally equivalent should-FAIL scorings, but
   they are not re-run by every counter invocation (counter-mutation coverage of them is wave item C1MutCounter's).

## 5. What I did not do

I ran no counter, no census `--selftest`, no self-assessment, and no pacman query: every claim above is a read of
committed bytes, committed receipts, or the working-tree diff, with the command shown. In particular I did NOT
re-run the C1 counter to confirm the after-state (survivors 0, params 4) — that is wave item C1-1/C1ExecRerun's
receipt, and the declaration's K4 cites `after/c1-after-568c397.jsonl`. I installed no tooling (no
install/update to record). Scratch `/fast/scratch/hyaku/tsukuroi-r41/RoutedLessonXref` was created for TMPDIR
discipline only and removed at finish; no receipts needed keeping (all evidence is cited by path per the seat
rules).
