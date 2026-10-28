VERDICT: draft

# R49ScribeLog — round-49 `Measured` block skeleton (F-6)

Seat class EXEC-AUTHORIZED (commands named in the item only). Nothing here is a measurement: every
number the block must carry is a `<PLACEHOLDER>`. What is supplied is the sentence skeleton, the exact
receipt paths and JSON keys the L1 reads, and the facts I read from the lane at the freeze/HEAD.

## Axes (godspeed)

1. **Format fidelity** — does the block sit in the round-45..48 house shape (one `Measured at the
   integrated revision` paragraph, then `Freshness/frontier:`, then `Landed work:`)?
2. **Fillability** — for every slot, is the producer named (command + receipt path + JSON key), so the
   L1 fills it without re-deriving anything?
3. **Non-invention** — zero free-floating numbers; anything not yet measured stays a slot.
4. **Coverage** — all six C1 legs, all six C2 legs, all four C3 legs, cohort counts, dead seats, round
   shape, the seven source re-opens, the two new rows, and the commit-by-topic list each appear once.

## Sources read (read-only)

- House format: `LOG.md:1696-1700` at HEAD `d7cfc273` (round-48 `Measured at the integrated revision
  \`76066487…\`` / `Freshness/frontier:` / `Landed work:` paragraphs); round-49 section opens
  `LOG.md:1702`, its last line `LOG.md:1723` reads `planner seat. Measured outcome and wave
  accounting: filled at integration.` — the block below **replaces the sentence after `planner
  seat.`**; `wc -l LOG.md` → 1723.
- Declaration: `git show 55c07cd3:SCORECARD.md` lines 3124-3145 (`## Round 49 — declaration …`): one
  v2 wave `w1` sized 64–128, predicate and kill-rule cells per claim.
- Frozen record: `.ufo/waves/round-49/frozen/FROZEN.md` (claims table, row hashes, cohort definition,
  C1 K0-K6/K-pass, C2 K0-K3/K-pass, C3 K0-K2/K-pass).
- Predicate/leg names and JSON keys, read from the frozen counters at `55c07cd3`:
  `tools/check-scrub-admission-r49.py:94` `PREDICATE`, out-dict keys `structural_ok`, `corr_ok`,
  `quotes_ok`, `verdicts_ok`, `seats_ok`, `marks_ok`, `section_sha256`, `per_row`, `seat_notes`;
  `tools/check-adjacency-table-r49.py:54`, keys `adj_rows`, `linked_rows`, `bare_ranges`,
  `anchors_ok`, `registry_ok`, `anchors_checker_rc`, `per_row`, `problems`;
  `tools/check-fd-band-r49.py:49`, keys `stale_ok`, `diag_ok`, `band_ok`, `cases`, `selftest_rc`,
  `case_line`, `summary`. C1 results file default: `check-scrub-admission-r49.py:350`
  `f'{WAVES}/{WAVE}-results.json'` → `.ufo/waves/round-49/w1-results.json`.
- Wave roster: `.ufo/waves/round-49/w1-spec.json` — 73 items; roles reviewer 18, critic 15, executor
  10, scout 13, scribe 7, mutation-tester 4, sentinel 4, connector 2 (attack roles 37/73 = 50.7%);
  cohort seats `R49RevGR{1,2,3}{a,b,c}` + `R49CritGR{1,2,3}{a,b,c}` = 18.
- Commits under `6256760d…`: `55c07cd3` (10 files: `corpus/knowledge/btrfs-scrub-grounding-r45.md`,
  `PROVINCE.md`, `tools/tsukuroi-census.sh`, the three counters, `frozen/FROZEN.md`, `LOG.md`,
  `SCORECARD.md`, `before/sources-census-start.txt`), `32a85560` (7 files: spec, dispatch,
  `make-w1-spec.py`, `battery.py`, `w1-validate.log` (0 bytes), `w1/swarm-registry.json`,
  `corpus/knowledge/adjacency-anchors-r19.json` — `found_line` 2642→2660 for IN-109), `d7cfc273`
  (three `controls/battery-summary-r49-c*.jsonl`, `controls/battery.py`, `frozen/FROZEN.md`).
- Source rows at the freeze (`git show 55c07cd3:corpus/SOURCES.md`): 255 data rows
  (`grep -c '^| S[0-9]'` → 255). S240 `:249`, S243 `:252`, S246 `:255`, S247 `:256`, S248 `:257`,
  S249 `:258`, S255 `:264`. No `S256+` exists at the freeze or in HEAD (both count 255).
- Round-start census: `.ufo/waves/round-49/before/sources-census-start.txt` — 41 lines, 40 `W04`
  duplicate-url notices and line 41 `tsukuroi\tok\t…/corpus/SOURCES.md`; no count line, so the start
  row count is `255` from the freeze file, not from the receipt.
- Pre-data controls: `controls/battery-summary-r49-c1.jsonl` (K0 K1 K2 K3 K4 K5 K6, K-pass),
  `-c2.jsonl` (K0 K1 K2 K3, K-pass), `-c3.jsonl` (K0 K1 K2, K-pass); K-pass C3 record carries
  `cases 167`, `case_line "PASS selftest: exhausted fd band fails the base resolver and names
  err=fd-band (R49-C3)"`.
- Point-in-time: `ls .ufo/waves/round-49/w1/*.md | wc -l` → 50, so 23 of the 73 spec seats had no
  report file when I read (wave still running); no `w1-results.json` existed yet — **not** block values.

## Draft block (verbatim text for the L1; placeholders in `<ANGLE-BRACKETS>`)

Replaces the tail of `LOG.md:1723` from `Measured outcome and wave accounting: filled at integration.`
onward. Three paragraphs, house order, no headings inside.

```
Measured at the integrated revision `<REV-INTEGRATED>`: C1 `python3 tools/check-scrub-admission-r49.py --revision <REV-INTEGRATED>` `<C1-VERDICT>` — structural_ok `<C1-STRUCTURAL_OK>`, corr_ok `<C1-CORR_OK>`, quotes_ok `<C1-QUOTES_OK>`, verdicts_ok `<C1-VERDICTS_OK>`, seats_ok `<C1-SEATS_OK>`, marks_ok `<C1-MARKS_OK>` (`.ufo/waves/round-49/after/c1-final.json`; section hashes `<C1-ROW-HASHES = unchanged 3a2ba180… / d4296085… / 43430a14…, or moved → name the row and why>`): `<C1-ROW-NARRATIVE = per-row outcome, e.g. "GR1/GR2/GR3 each `holds` with <n>/<n>/<n> credited seats and no bound `partly`" or "<row> blocked by <seat>'s `partly` on hash <…>">`. C2 `python3 tools/check-adjacency-table-r49.py --revision <REV-INTEGRATED>` `<C2-VERDICT>` — adj_rows `<C2-ADJ_ROWS>`, linked_rows `<C2-LINKED_ROWS>`, bare_ranges `<C2-BARE_RANGES>`, anchors_ok `<C2-ANCHORS_OK>`, registry_ok `<C2-REGISTRY_OK>`, anchors_checker_rc `<C2-ANCHORS_CHECKER_RC>` (`.ufo/waves/round-49/after/c2-final.json`): `<C2-NARRATIVE = "ADJ-01..07 all name OUT-002..OUT-010 and the registry digests match, checker rc 0" or "which rows still hold bare ranges and what the checker refused">`. C3 `python3 tools/check-fd-band-r49.py --revision <REV-INTEGRATED>` `<C3-VERDICT>` — stale_ok `<C3-STALE_OK>`, diag_ok `<C3-DIAG_OK>`, band_ok `<C3-BAND_OK>`, cases `<C3-CASES>`, selftest_rc `<C3-SELFTEST_RC>` (`.ufo/waves/round-49/after/c3-final.json`; case line `<C3-CASE_LINE>`, census blob sha256 `<C3-CENSUS-BLOB first7…last5>`).

Wave `w1` landed `<W1-REPORTS-LANDED>` of 73 seat reports — reviewer 18, critic 15, executor 10, scout 13, scribe 7, mutation-tester 4, sentinel 4, connector 2; attack roles reviewer+critic+mutation-tester = 37/73 (50.7%); `<W1-DEAD-SEATS = "no deaths reported" or "<n> dead (<seat>: <cause>; …)">`. Counted cohort `<COHORT-BOUND>`/18 bound `<COHORT-UNBOUND-LIST = seat names, or "none">`; `<RESIDUAL = "no residual call" or "one residual `r1` of <n> claimed seats (<scope>, <outcome>)">`. `<PRE-DATA-CATCHES = counter defects and control-fixture bugs caught before any data, with the control ids>`.

Freshness/frontier: start and end `sources-census.sh validate` exit 0 (`before/sources-census-start.txt` line 41 `ok`, `after/sources-census-end.txt`; 255→`<CENSUS-END-ROWS>` rows). Re-opened byte-identical against their `SOURCES.md` digests / `frozen/src/SHA256SUMS`, by the named seat: S246 Linux v7.2.11 `lib/cmdline.c` (`<SEAT-S246>`, `corpus/SOURCES.md:255`), S240 Linux v7.2.11 `fs/btrfs/ioctl.c` (`<SEAT-S240>`, `:249`), S243 Linux v7.2.11 `fs/btrfs/sysfs.c` (`<SEAT-S243>`, `:252`), S247 Linux v7.2.11 `fs/btrfs/dev-replace.c` (`<SEAT-S247>`, `:256`), S248 systemd v262 `man/systemd.kill.xml` (`<SEAT-S248>`, `:257`), S249 round-45 host scrub-service stop capture (`<SEAT-S249>`, `:258`) and S255 GNU Bash 5.3 Redirections re-opened by the L1 (`<S255-EVIDENCE = fetched-bytes sha256 vs the row digest, located quote>`, `:264`). Two rows were admitted after the L1's gate check (`SOURCES.md` held 255 rows at the freeze): `S<NEW-ROW-1-ID>` `<NEW-ROW-1-SUBJECT>` — `<NEW-ROW-1-URL>`, accessed `<NEW-ROW-1-DATE>`, quote `<NEW-ROW-1-QUOTE, ≤25 words, located>`; `S<NEW-ROW-2-ID>` `<NEW-ROW-2-SUBJECT>` — `<NEW-ROW-2-URL>`, accessed `<NEW-ROW-2-DATE>`, quote `<NEW-ROW-2-QUOTE>`; `used-by` for both `<OLD-USED-BY>` → `<NEW-USED-BY>`. `<REFUSED-ROWS = "no row refused" or "<candidate>: <reason>; flip condition <…>">`. Assimilation: `<ASSIMILATION = "none" + the collision reason, or what was merged and from where>`; `considerthese/` mined by `R49ScoutConsider`; `<CONSIDER-OUTCOME = "no round-49 implementation adopted from it" or the adopted item and its file>`.

Landed work: `55c07cd3` freeze — the seven r48-named GR1-GR3 corrections, the `PROVINCE.md` OUT-ownership cells, the census fd-band diagnostic with the `(R49-C3)` case, the three frozen counters, `frozen/FROZEN.md` and the round-start census receipt; `32a85560` validated 73-seat `w1` spec/dispatch (policy v2) with its battery driver, plus the IN-109 `found_line` repin 2642→2660; `d7cfc273` pre-data control batteries K0..K-pass per claim (`.ufo/waves/round-49/controls/battery-summary-r49-c{1,2,3}.jsonl`); `<SHA-W1-INTEGRATION>` `w1` integration and evidence/pending marks; `<SHA-SOURCES-APPEND>` the admitted `SOURCES.md` rows and `corpus/lessons/round-49.md`; the outcome commit carries this entry, the lesson, the `SCORECARD.md` outcome and the receipts. `<TOOLING = "No tools installed or updated." or "<tool> <version> via <channel> for <reason>">`.
```

## Fill rules (one row per slot)

| Slot | Producer (command / receipt) | Key or rule |
|---|---|---|
| `REV-INTEGRATED` | the integration commit the L1 measures | full 40-hex; the counters accept any revision |
| `C1-*` | `python3 tools/check-scrub-admission-r49.py --revision <REV> > .ufo/waves/round-49/after/c1-final.json` | keys `verdict`, `structural_ok`, `corr_ok`, `quotes_ok`, `verdicts_ok`, `seats_ok`, `marks_ok`; PASS requires the frozen predicate exactly (`:94`) |
| `C1-ROW-HASHES` | same receipt, `section_sha256` | must equal `frozen/FROZEN.md` values; any move is a frozen-byte violation, not a score item |
| `C1-ROW-NARRATIVE` | same receipt, `per_row.<row>.credited` / `.blocking` / `.row_ok` | name blocking seats verbatim; no narrowing |
| `C2-*` | `python3 tools/check-adjacency-table-r49.py --revision <REV> > .ufo/waves/round-49/after/c2-final.json` | keys `adj_rows`, `linked_rows`, `bare_ranges`, `anchors_ok`, `registry_ok`, `anchors_checker_rc`, `problems` |
| `C3-*` | `python3 tools/check-fd-band-r49.py --revision <REV> > .ufo/waves/round-49/after/c3-final.json` | keys `stale_ok`, `diag_ok`, `band_ok`, `cases`, `selftest_rc`, `case_line`; `C3-CENSUS-BLOB` from `git rev-parse <REV>:tools/tsukuroi-census.sh` |
| `W1-REPORTS-LANDED`, `COHORT-*` | `ls .ufo/waves/round-49/w1/*.md`; `.ufo/waves/round-49/w1-results.json`; `C1-SEATS_OK` | landed = files present **and** results entries; the counter's `seats_ok` is the authority for the cohort leg |
| `W1-DEAD-SEATS` | dispatch vs `w1-results.json` and the wave dir | name each dead seat and its cause; `no deaths reported` only if all 73 have both |
| `RESIDUAL` | `.ufo/waves/round-49/` (an `r1` dir if one is called) | if no residual wave exists, `no residual call` |
| `PRE-DATA-CATCHES` | `frozen/FROZEN.md` "Control outcomes" + `corpus/lessons/round-49.md` Mistakes rows | round-49 known: 2 role refusals (`labrat` items[25], `distiller` items[64]) and 2 C3 fixture bugs (K1 cut the wrong comment, K2 stale replacement did not match) |
| `CENSUS-END-ROWS` | `after/sources-census-end.txt` / `git show <REV>:corpus/SOURCES.md \| grep -c '^| S[0-9]'` | 255 + admitted rows |
| `SEAT-S24x/S255` | each seat's report under `.ufo/waves/round-49/w1/` | seat id + its digest/anchor evidence; do not credit a seat that did not report |
| `NEW-ROW-1/2-*` | the L1's `## Gate` append in `corpus/lessons/round-49.md` | ids must be > S255 and contiguous; URL + access date + ≤25-word located quote; subject must match the scope cell |
| `REFUSED-ROWS` | `R49ScoutReject.md` + the L1 gate | reason + flip condition, house style (`S254 … rejected with flip condition`) |
| `ASSIMILATION` / `CONSIDER-OUTCOME` | `R49ScribeAssim.md`, `R49ScoutConsider` report | round 48 wrote `none; the external package remains read-only and its id collisions are not resolved by this round` — keep the collision reason explicit if it recurs |
| `SHA-W1-INTEGRATION`, `SHA-SOURCES-APPEND` | `git log --oneline <base>..HEAD` | one topic per sha, short form |
| `TOOLING` | seat reports + L1's own installs | `No tools installed or updated.` only if every seat reported none |

## Notes the L1 should not lose

- The two `Measured`-paragraph candidates in house style are one paragraph for all three claims (round
  48) or per-claim sentences (rounds 45/46); the draft keeps the fused round-48 shape because the
  round-49 predecessor entry is fused.
- Round-49 declarations say C1's kill rule blocks a bound-format negative on **the current row hash**;
  so a `partly` in `per_row.*.blocking` must be written into `C1-ROW-NARRATIVE` as blocking, never
  as "narrowed".
- `cases` must read `167`; a `166` reading is a C3 FAIL even when `band_ok == 1` (frozen predicate).
- `IN-109` is `corpus/knowledge/adjacency-anchors-r19.json` `found_line` 2642→2660 (not a
  `PROVINCE.md` row); do not fold it into the C2 sentence — it belongs to the dispatch topic list.
- No `S256` exists at the freeze nor at HEAD (`grep -c '^| S[0-9]'` → 255 both), so both new-row ids
  are still the L1's to assign; do not back-fill the ids from this draft. The worktree carries one
  uncommitted `corpus/SOURCES.md` hunk at the freeze read (`git diff --stat` → `1 insertion(+),
  1 deletion(-)`), S255's `used-by` cell only — row count still 255; it must be inside the
  `SHA-SOURCES-APPEND` commit or reverted before the end census, or `S255-EVIDENCE` will cite a
  `used-by` that is not in any commit.

## What I did not do

- Ran no counter, no census `--selftest`, no control battery and no git/jj mutation (none of them is
  named in this item); every measured value in the block is therefore a slot, not a claim.
- Edited no lane file; `LOG.md` is untouched (it still ends at `LOG.md:1723` with the
  `filled at integration` sentence).
- Did not read the still-running seat reports as evidence for any slot: at read time 23 of 73 had no
  published report.
- No tool installed or updated.

## Receipts

- `.ufo/waves/round-49/w1/R49ScribeLog/facts.txt` — the observed commands and their output excerpts
  quoted above (roster counts, commit stats, SOURCES line numbers, control summary keys).
