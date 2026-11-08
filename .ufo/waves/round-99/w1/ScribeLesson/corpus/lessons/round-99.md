# Round 99 lesson — tsukuroi lane

Round 99 (attempt 1), pre-round tip `f107da3afe511f7db8cdc30235a992b774903158`. Claims: C1
(depth 8) `tools/limine-pin-battery-r99.py` — the X-cap `REFUSAL-VERSIONS-9DIGIT` and the Y-cap
`REFUSAL-VERSIONS-9DIGIT-Y` set `check_echo`/`check_era`, and `LIE_KINDS` gains `limine-version`
and `visibility-era`; C2 (freshness 9) `tools/check-registry-content-r99.py` — the guarded
`RC-BEND-SPAN` capture with the `unique` mark and the `span-hybrid`/`span-restated`/`ancestor`
selftest cases (14 -> 17).

This draft is written by the `ScribeLesson` seat into its own seat dir
(`.ufo/waves/round-99/w1/ScribeLesson/`). Every number below was re-derived by this seat against
the pinned bytes; the receipts are under `.ufo/waves/round-99/w1/ScribeLesson/receipts/`.
Where a wave seat had not filed its report when this was written, the row is marked `owed`
rather than filled from an assumption.

## Gate (sources opened this round; contract `CORPUS.md` §SOURCES.md)

| row | URL / path opened 2026-11-08 | tier | located quote (≤25 words) | admit / reject |
|---|---|---|---|---|
| S395 (new, own-work) | `tools/limine-pin-battery-r99.py` (sha256 `c2e8c8fc…`) and `tools/check-limine-pins.py` (sha256 `7d79ac29…`), in the working tree | A | `if c.check_echo and not (got[8] == c.version and got[9] == "flag")` (BYTE 99430, line 2181 of the r99 battery); the era assertion `if c.check_era and got[10] !=` at BYTE 99523 (line 2183); `def meta_ok` at BYTE 99305 (line 2179) | **admit** — the row's anchor names both assertion sites, the five `c.check_echo` sites (BYTEs 79015, 79893, 81666, 83173, 84390) and the five `c.check_era` sites (79039, 80414, 81690, 83197, 84414), the two new `LIE_KINDS` members (BYTE 108455, line 2370), and the gate's MAIN-return emission sites (16931 / 17037; the early-return pair 11230 / 11344). Every one of those offsets was re-measured here with `grep -abo` on the pinned bytes (receipt `14-byte-anchors.txt`); the unit is the byte, never a decoded-string index (QUALITY 141) |
| S392 (re-open) | https://docs.python.org/3/library/functions.html#int (301 -> `https://docs.python.org/3/builtins/functions.html`) | A | `have leading zeros, be surrounded by whitespace` (BYTE 157767, line 1330); the `id="int"` heading at BYTE 153202 (line 1302); `disallows leading zeros` at BYTE 159315 (line 1340) | **admit** (re-open, no drift) — the fetched page is 331022 bytes with sha256 `d92580dd0e7a02aab9b51fe30885ae59fd924c639324c7e07a90799e8bc721d7`, byte-identical to the r97/r98 pin, and all three offsets re-measure exactly (receipt `15-external-sources.txt`). The URL now 301-redirects; the row's `source` cell keeps its original URL, the content bytes are unchanged |
| rejected candidate | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/CONFIG.md | — | `# Limine configuration file` (BYTE 0); `Limine scans for the config file on` (BYTE 61) | **reject** — HTTP 200, 27609 bytes, sha256 `f44f3a19133cb3dc14d6d8b402ed585feb98a36bc4b263c37aa92f621f603763`, byte-identical to the r98 measurement; `grep -c` for the gate's own field names returns 0 for `limine_version`, 0 for `visibility_era`, 0 for `echo`, 0 even for the bare token `version` (receipts `15-external-sources.txt`, `15b-config-md-quotes.txt`). The page documents Limine's *config keys*, not the JSON report contract this round's claims rest on, so it grounds no proposition of this round |

### Census (before -> after)

Frozen command (unchanged from r98): `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
validate --root /home/vgpnk/Projects/shokunin tsukuroi`.

| when | rows | exit | errors | warnings |
|---|---|---|---|---|
| **before** — the pre-round tree `f107da3a` extracted read-only with `git archive` into scratch and validated under the same command and the same lane name | **394** | **0** (`EXIT_BEFORE=0`) | 0 (`E##` rows empty) | 58 = 1 W01 + 57 W04 (the standing set) |
| **after** — the landed working tree | **395** | **0** (`EXIT_AFTER=0`) | 0 | 58 = 1 W01 + 57 W04 (the standing set) |

Row count measured with `grep -cE '^\|[[:space:]]*S[0-9]{3,}'` on the pre-round registry and on the
working-tree registry. The one row added this round is **S395** (own-work, tier A); no existing
row was edited in place (`git diff --numstat corpus/SOURCES.md` -> `1  0`, i.e. one insertion and
zero deletions). Receipts `09b-census-before.txt` (exit 0) and `09-census.txt` (exit 0).

## Mistakes

- **R99-TWIN-BEND** — class: `vacuous`. A near-miss control that the do-nothing instrument already
  rejects witnesses the predecessor, never the round. The drafted third bend `N10-z-echo` (the
  echoed `limine_version` falsified for the Z spellings, `12.9.999999999` / `0.9.999999999`) was
  re-derived and measured against the r98 do-nothing battery: the r98 control already reads
  `unmet 104/105` with `failed_families ["REFUSAL-VERSIONS-9DIGIT-Z"]`, and the r99 battery reads
  the *same* `unmet 104/105 ["REFUSAL-VERSIONS-9DIGIT-Z"]` — a delta of zero, so the article
  discriminates nothing that r99 added. The bend was dropped before the freeze, and only the two
  bends that do discriminate (N09, N11) are committed under
  `.ufo/waves/round-99/before/controls/bends/`. Captured-by: QUALITY 136 ("a family that only
  re-answers a case the old roster already covered is a twin, not a boundary") — the rule existed
  and this round applied it *before* the freeze, which is the improvement over r98, where the
  equivalent survivor was discovered after the wave. Red-before: the r98 control already rejects
  the article (`unmet 104/105 [REFUSAL-VERSIONS-9DIGIT-Z]`, 0 error rows) — receipts
  `11-N10-twin-diff.txt` (the one-clause diff) and `12-N10-twin-batteries.txt` (both readings,
  count-runs output included). Fix: the bend is not in `tools/make-r99-bends.py`'s `VARIANTS`
  (only N09 and N11 are), and the instrument's docstring names the drop and the reason
  ("a Z-echo bend was drafted and DROPPED as a twin (QUALITY 136)"). **Proposed criterion for
  QUALITY** (drafted here; the round may not promote it, so it stays a proposal): *"a near-miss
  control is committed only when the do-nothing instrument reads a different verdict on it; a
  control whose reading the predecessor already produces is a twin and is dropped, and the
  freeze records the twin's reading so the drop is auditable."*
- **R99-X-LIMIT-DELTA** — class: `scope`. A named limit can close as a *delta* rather than a
  flip, and the claim must say which. The r98 Frontier's X-cap bullet said the X leg "rides on
  one `EXPLICIT-VERSION-ERA` case" (r98 amendment A5). The committed bend `N11-x-era` (era label
  swapped exactly when the FIRST component is `999999999`) therefore reads `unmet 104/105` on the
  r98 do-nothing control — one failed family, `EXPLICIT-VERSION-ERA` — and `unmet 103/105` on
  r99, which adds `REFUSAL-VERSIONS-9DIGIT`. Counting N11 as a met-to-unmet closure would have
  overstated the round by one family, and a "the X leg is now covered" sentence would have
  implied a discrimination the r98 instrument already had. Captured-by: QUALITY 125 (every clause
  of a predicate maps to a family whose expected answer changes) read together with QUALITY 136;
  the lane had no rule that a closure's *direction and size* must be named, only that it changes.
  Red-before: the r98 control reads `unmet 104/105 ["EXPLICIT-VERSION-ERA"]` on N11 (receipt
  `05-N11-r98-control.txt`) — the X family is not in its failed set. Green-after: r99 reads
  `unmet 103/105 ["EXPLICIT-VERSION-ERA","REFUSAL-VERSIONS-9DIGIT"]` (receipt
  `04-N11-r99.txt`), i.e. exactly one additional failed family and no other change. Fix: the
  declaration's C1 target states N11's failed set literally, and the do-nothing leg for N11 is a
  committed receipt, so the delta is visible rather than asserted. **The rule that follows:** a
  limit is closed by the *marginal* discrimination the new instrument adds over the do-nothing
  control on the same article — the delta in the failed-family set, not the verdict — and a
  closure sentence that names a family must name the family whose *reading changed*, never the
  family that merely appears in a failed set.
- **R99-TWIN-RECEIPT-ABSENT** — class: `provenance`. A reading may be true and still have no
  committed receipt behind it. The plan names the dropped bend's r98-control reading at
  `before/dev/c1-N10-twin-r98.json` (BYTE 5640 of `.ufo/plans/round-99.md`), the knowledge entry
  names `before/dev/c1-N10-twin-r98-control.json` (BYTE 3609 of
  `corpus/knowledge/limine-metadata-cap-families-r99.md`), and the L1's draft lesson names the
  same file (BYTE 3418 of `corpus/lessons/round-99.md`) — but **neither file exists in the tree**:
  `ls` on both paths returns "No such file or directory", `find .ufo -name 'c1-N10*'` returns no
  output, and the dev dir's 32 files are all named `c1-N09-*`, `c1-N11-*`, `c1-gate-*`,
  `c1-lie-*`, `c1-selftest-*` or `c2-*`. So the twin's reading is asserted in three landed files
  with nothing behind it. The r98 lesson's `MutRegistry/probe-nonancestor.txt` (BYTE 12138 of
  `corpus/lessons/round-98.md`) is the same defect one round older, still uncorrected. Captured-by:
  the r98 mistake `R98-RECEIPT-NAME-MISMATCH` (a receipt's name states a different subject than
  its contents) — but the sharper form here is that the receipt is *absent*, not mismatched, and
  the plan's own `before/dev/c1-*` glob reads as if it covered it. Red-before: the three cited
  paths resolve to nothing (receipt `17-twin-receipt-existence.txt`). Fix: this seat re-derived
  the twin from the pinned bytes (a one-clause gate substitution in scratch, receipt
  `11-N10-twin-diff.txt`) and measured it under both batteries (receipt
  `12-N10-twin-batteries.txt`); the reading the three files assert is therefore confirmed, but
  the *citation* stays broken and the committed receipt must be added under `before/dev/` (or the
  three citations re-pointed at a receipt that exists) by the L1, which owns that directory.

## Counter-attack scoreboard (QUALITY 115)

`w1/` = `.ufo/waves/round-99/w1/`. Direction: a mutant is **killed** when a leg's reading moves
*away* from the frozen expectation, in either direction (r98's `R98-MUTANT-DIRECTION-READ`: a
mutant that makes a leg read *better* is killed, not surviving). A do-nothing control that reads
the same as the landed instrument proves nothing and is not a kill.

Rows marked `met` cite a receipt this seat read; rows marked `owed` name an attack whose wave
seat had not filed its report when this lesson was written, so no reading is asserted for it.

| claim | attack fielded | receipt | outcome |
|---|---|---|---|
| C1 | landed gate, r99 battery, 3 runs | `ScribeLesson/receipts/06-gate-r99.txt`, `18-own-battery-counts.txt` | **met** — `105/105 met`, `failed_families []`, 0 error rows, 420 cases, in each of 3 runs; X/Y/Z/EXPLICIT-VERSION-ERA each `[4,0]` |
| C1 | `N09-y-era` bend (Y-cap era lie), r99 battery, 3 runs | `ScribeLesson/receipts/02-N09-r99.txt`, `18-own-battery-counts.txt` | **met** — `unmet 104/105`, failed exactly `["REFUSAL-VERSIONS-9DIGIT-Y"]`, that family `[0,4]`, X and Z `[4,0]`, 0 error rows, x3 |
| C1 | `N09-y-era` bend under the r98 do-nothing battery, 3 runs | `ScribeLesson/receipts/03-N09-r98-control.txt` | **met (blindness)** — the control reads `met 105/105`, `failed_families []`, 0 error rows, x3: it never looks at the era label on the Y spellings, so N09 is r99's alone |
| C1 | `N11-x-era` bend (X-cap era lie), r99 battery, 3 runs | `ScribeLesson/receipts/04-N11-r99.txt`, `18-own-battery-counts.txt` | **met** — `unmet 103/105`, failed exactly `["EXPLICIT-VERSION-ERA","REFUSAL-VERSIONS-9DIGIT"]` (the instrument's sorted order), X `[0,4]`, EXPLICIT-VERSION-ERA `[3,1]`, 0 error rows, x3 |
| C1 | `N11-x-era` bend under the r98 do-nothing battery, 3 runs | `ScribeLesson/receipts/05-N11-r98-control.txt` | **met (the delta)** — the control already reads `unmet 104/105` with failed exactly `["EXPLICIT-VERSION-ERA"]` (X `[4,0]`): N11's marginal discrimination is the one extra failed family, not a met-to-unmet flip |
| C1 | the drafted `N10-z-echo` twin bend, under both batteries (this seat's own re-derivation) | `ScribeLesson/receipts/11-N10-twin-diff.txt`, `12-N10-twin-batteries.txt` | **not a witness — twin** — the r98 control reads `unmet 104/105 ["REFUSAL-VERSIONS-9DIGIT-Z"]` and r99 reads the identical set; zero discrimination, so the bend was dropped before the freeze |
| C1 | the new `limine-version` lie kind (blanket echo lie) | `ScribeLesson/receipts/13-dev-receipt-counts.txt` over `before/dev/c1-lie-limine-version.json` | **met** — `unmet 93/105`, 0 error rows, 12 families named including `REFUSAL-VERSIONS-9DIGIT` (X) and `REFUSAL-VERSIONS-9DIGIT-Y` (Y) |
| C1 | the new `visibility-era` lie kind (blanket era lie) | `ScribeLesson/receipts/13-dev-receipt-counts.txt` over `before/dev/c1-lie-visibility-era.json` | **met** — `unmet 95/105`, 0 error rows, 10 families named including X and Y |
| C1 | battery assertion-removal mutants (X/Y `check_echo`/`check_era` deleted) | `ScoutFrontier/receipts/mut-no{X,Y}{echo,era}-*.log`; `ReviewBattery-9/receipts/mut-M{a,b,c,d}-*.json` | **met (killed, each removal drops its own family out of the failed set)** — `noXecho` on the `g2b` fixed-echo gate reads `unmet 99/105` with X absent from the failed set (the landed battery reads `98/105` with X *in* it); `noXera` on N11 reads `unmet 104/105 ["EXPLICIT-VERSION-ERA"]` with X `[4,0]` (the landed battery reads `103/105` with X `[0,4]`); `noYera` on N09 reads `met 105/105 []` — the reading the claim needs to be unmet, killed in the "reads better" direction; `noYecho` on `g2b` reads `unmet 99/105` with Y absent. The matching `lie`-kind legs read `94/105` / `96/105` with the removed family likewise absent. The four mutants' digests are byte-identical across the two seats (`551f9b14…`, `fc691ef5…`, `c910366e…`, `63e3439e…`) |
| C1 | X-echo-only and Y-echo-only echo lies (spelling-targeted, r99-local gates) | `CriticClaims/receipts/21-ex-echolie-r98-runs1.txt`, `22-ey-echolie-r98-runs1.txt`, `23-ey-echolie-r99-runs1.txt` | **met for Y, twin for X** — the Y-spelling echo lie reads `met 105/105` on the r98 control and `unmet 104/105 ["REFUSAL-VERSIONS-9DIGIT-Y"]` on r99 (new discrimination); the X-spelling echo lie already reads `unmet 104/105 ["EXPLICIT-VERSION-ECHO"]` on the r98 control, so the X echo leg is a twin of r98's `EXPLICIT-VERSION-ECHO` coverage |
| C1 | per-family assertion removal under the blanket lie kinds (the B03 class) | `CriticClaims/receipts/17-b03-on-lieversion-runs1.txt` | **survives — carried limit** — the B03-class mutant (Z's `check_echo` deleted) still reads `unmet 94/105` on `lie-limine-version` with the Z family `[4,0]` green: the blanket kind proves the battery *sees* the field, not that a per-family assertion removal is visible |
| C2 | the landed checker, `--selftest` | `ScribeLesson/receipts/07-c2-selftests.txt` | **met** — `selftest PASS 17/17`, rc 0 (the r98 control in the same environment reads `PASS 14/14`) |
| C2 | the hybrid capture fixture (`VARIANTS N01-N04,N05`), both checkers | `ScribeLesson/receipts/08-c2-fixture-legs.txt` | **met** — r98 control `PASS bindings 7/7 findings 0` rc 0; r99 `FAIL bindings 6/7 findings 1` with exactly `RC-CELL-MISSING`, rc 1 |
| C2 | the restated capture fixture (`VARIANTS N01,N03 then VARIANTS N01-N03`), both checkers | `ScribeLesson/receipts/08-c2-fixture-legs.txt` | **met** — r98 control `PASS 7/7 findings 0`; r99 `FAIL 6/7 findings 1` with exactly `RC-CELL-AMBIGUOUS`, rc 1 |
| C2 | the `clean` and `gap` fixtures, both checkers | `ScribeLesson/receipts/08-c2-fixture-legs.txt` | **met** — both read `PASS 7/7 findings 0` on both: the new cases do not disturb the r97 branch |
| C2 | the M07 mutant (ancestor check skipped), own re-derivation, both checkers | `ScribeLesson/receipts/10-c2-M07-mutant.txt` | **met (killed on r99, survives on r98)** — on r99 `ancestor FAIL rc=0 registry-content: status PASS bindings 7/7 findings 0` and `selftest FAIL 16/17` with exactly `ancestor` red; the same mutation on the r98 control reads `PASS 14/14`. The mutant reads *better* (rc 0 `PASS` where the frozen expectation is rc 2 `CANNOT-EVALUATE`), which is the kill direction |
| C2 | capture escapes beyond the two frozen shapes (a second `VARIANTS` mention the capture cannot match, an extra label after a non-`[0-9,-]` separator, a prose span, a truncated token) | `ReviewRegistry/report.md` §2 and §6 (F1–F5); `CriticClaims/receipts/10-xv1..xv3` | **survives — findings, routed** — 34 forged cells were run; 8 that r98 read `PASS` are now rejected by r99 (a, b, f, x7, y6, y7, y8, z2), but 5 classes still read `PASS` while stating a span the tools do not derive: a hybrid span paired with one clean mention (x2, x3), any non-`[0-9,-]` separator (x1, y1–y4), a prose span outside the token (x10), an alphabetic suffix truncating the token (g3, x6), and an un-capturable second mention defeating `unique` (x4, x5). Narrowed by amendment A1 |
| C2 | forged revisions on the `--revision` leg | `ReviewRegistry/report.md` §5 (R1–R13) | **met (fail-closed)** — a non-ancestor revision reads rc 2 `CANNOT-EVALUATE`; the M07 mutant reads rc 0 `PASS` (killed, reads better); a doctored revision's own tool bytes are used for the derivation (R12 `RC-VALUE-MISMATCH`), so the derivation does not read the worktree |
| C2 | the coverage gate at the pre-round tip | `ScribeLesson/receipts/16-coverage-tip.txt` | **met** — `PASS`, `registered 160 / rows_total 160 / tools_total 160`, `findings []`, `missing 0`, rc 0 |
| — | the R99-D1 pointer sweep at the pre-round tip | `ScribeLesson/receipts/20-r99-d1-pointer-sweep.txt` | **met (repair landed)** — two committed artifacts still cite the non-existent `.ufo/waves/round-98/after/c2/coverage-tip.json` (`.ufo/waves/round-98/after/report-draft.md:110`, `SCORECORD.md:7984`; `git cat-file -e` rc 128), and the round commits fresh coverage receipts under `before/` instead of editing the r98 history |
| — | census | `ScribeLesson/receipts/09b-census-before.txt`, `09-census.txt` | **met** — exit 0 before and after, 0 E findings, 394 -> 395 rows |
| C1 | battery mutants M1–M8 (r99 battery, `check_echo`/`check_era`/lie-kind removals) | `MutRegistry/receipts/M1.diff` … `M8.diff`; the seat's own result receipts | **owed** — `MutRegistry/receipts/` holds the diffs and the M07/M5 results, but that seat had filed no report when this lesson was written, so no reading is asserted here beyond the diffs' presence |
| C1 | sibling-lane overlap and the `considerthese` batch | `ConnectorOverlap/report.md` | **owed** — that seat's report exists but its tables were not read line by line before this draft was frozen; carried, not scored here |
| — | the frontier clause map (QUALITY 125/136) | `ScoutFrontier.md` | **owed** — the seat's report is filed at the wave level only (`w1/ScoutFrontier.md`), not under its seat dir; its readings are not asserted here |

## Routed (r98 -> r99)

| r98 routed item | r99 treatment | evidence |
|---|---|---|
| R99-D1 — the r98 report/SCORECARD cite `PASS 160/160` with no committed receipt | **closed** — coverage receipts for the pre-round tip `f107da3a` and for the r98 settle `270ca298` are committed under `.ufo/waves/round-99/before/`, plus the three cited intermediate revisions (`5eb475cd`, `b492f17f`, `839954b7`, 157/157/160/160). The r98 `after/report-draft.md` pointer stays as filed history (append-only); it and `SCORECARD.md:7984` still cite the absent path, which the pointer sweep names rather than edits | `before/r99-d1-coverage-tip-f107da3a.txt`, `before/r99-d1-coverage-r98settle-270ca298.txt`, `before/r99-d1-coverage-cited-figures.txt`; `ScribeLesson/receipts/20-r99-d1-pointer-sweep.txt` |
| Y-cap field fidelity (the r98 G6 survivor, `met 105/105`) | **closed** — the Y family sets `check_echo`/`check_era`; `N09-y-era` reads `unmet 104/105 ["REFUSAL-VERSIONS-9DIGIT-Y"]` on r99 while the r98 control reads `met 105/105` | `before/dev/c1-N09-r99.json`, `c1-N09-r98-control.json`; `ScribeLesson/receipts/02-N09-r99.txt`, `03-N09-r98-control.txt` |
| X-cap field fidelity (r98 amendment A5: "rides on one `EXPLICIT-VERSION-ERA` case") | **closed as a delta** — r99's N11 reading adds exactly one failed family (`REFUSAL-VERSIONS-9DIGIT`) over the control's `unmet 104/105 ["EXPLICIT-VERSION-ERA"]`; the closure is the marginal family, not a verdict flip | `before/dev/c1-N11-r99.json`, `c1-N11-r98-control.json`; `ScribeLesson/receipts/04-N11-r99.txt`, `05-N11-r98-control.txt` |
| the battery selftest's missing echo/era lie kind (the r98 "lie-kind coverage" structural gap) | **closed at the field level** — `LIE_KINDS` 12 -> 14 with `limine-version` and `visibility-era`; both wrappers read `unmet` (93/105 and 95/105) with X and Y named. **Carried, narrowed:** a *per-family* assertion removal is still invisible to a blanket kind (the B03-class mutant keeps Z green) | `before/dev/c1-lie-*.json`; `ScribeLesson/receipts/13-dev-receipt-counts.txt`; `CriticClaims/receipts/17-b03-on-lieversion-runs1.txt` |
| the checker M07 ancestor branch | **closed** — the `ancestor` selftest case runs the file's real CLI on a non-ancestor revision; the mutant reads rc 0 `PASS` where the case expects rc 2 `CANNOT-EVALUATE`, so it is killed in the "reads better" direction. The same mutation on the r98 checker still reads `PASS 14/14` | `before/dev/c2-m07-r99-selftest.txt`, `c2-m07-r98-selftest.txt`; `ScribeLesson/receipts/10-c2-M07-mutant.txt` |
| hybrid cell and same-cell restatement capture shapes | **closed in their frozen shapes** — both fail closed in r99 (`RC-CELL-MISSING` / `RC-CELL-AMBIGUOUS`) where r98 read `PASS 7/7`. **Carried, narrowed by amendment A1:** the capture's guard alphabet is `[0-9,-]`, so other separators, a prose span, a truncated token and an un-capturable second mention still read `PASS` | `before/dev/c2-r99-hybrid.txt`, `c2-r99-restated.txt`; `ScribeLesson/receipts/08-c2-fixture-legs.txt`; `ReviewRegistry/report.md` §6 |
| the X/Y **echo** legs have no spelling-targeted committed bend (r98's B03, no committed witness) | **carried unchanged** — N09/N11 falsify `visibility_era` only; the blanket `lie-limine-version` wrapper and the r98-carried `g2b-fixed-echo.py` cover the echo, and a spelling-targeted echo lie is not committed | `corpus/README.md` § "Frontier (round-99 addition)"; `ScoutSources`/`ScoutFrontier` receipts |
| the r98 battery's unchanged JSON schema token | **carried unchanged** — the r98 control still emits `tsukuroi-limine-pin-battery-r97-v1` (BYTE 104316) while r99 emits `tsukuroi-limine-pin-battery-r99-v1` (BYTE 105742); a reader comparing the two batteries' receipts by schema token will see `r97-v1` on the control leg | `ScribeLesson/receipts/19-schema-tokens.txt` |
| unbound registry rows, tool+cell co-doctoring, printed-tally parsing; the spaced/lowercase capture forms; the r96/r93/r89 items | **carried unchanged** | `corpus/README.md` § "Frontier (round-99 addition)" |

## Frontier moved this round

The two r98 field-fidelity limits close — one as a full flip (the Y family: the r98 control is
blind, `met 105/105` on N09, while r99 reads `unmet 104/105`) and one as a discrimination delta
(the X family: the r98 control already reads `unmet 104/105`, r99 adds exactly one failed
family). The lie-kind gap closes at the field level, with the per-family assertion-removal limit
named and carried. The hybrid, restatement and ancestor survivors close in their frozen shapes,
and the capture's guard alphabet is measured to be `[0-9,-]` — five further classes of cell
still read `PASS`, which amendment A1 names and routes to r100 rather than leaving implicit.
What remains, by name: the X/Y echo legs have no spelling-targeted committed bend; the capture's
separator alphabet and its token truncation; the per-family assertion removal under a blanket
lie kind; the unbound registry rows and the three r98 C2 gaps; the carried r96/r93/r89 items.

### Note on the seat harm of this wave (disclosure, not attribution)

At ~11:24 a sibling seat ran `rm -rf /fast/scratch/hyaku/tsukuroi-r99`, the shared parent of the
wave's scratch roots, which removed this seat's scratch tree mid-measurement. Every receipt this
seat cites was therefore **re-derived after the wipe** and written straight into
`.ufo/waves/round-99/w1/ScribeLesson/receipts/`; the re-derived readings agree with the committed
`before/dev/` receipts wherever the same leg exists there (N09, N11, the landed gate, both lie
kinds, the r98-control readings), which is itself a second, independent confirmation. The
sibling disclosed the deletion to the L1 and in its own seat report (`w1/CriticClaims.md` §7b).
