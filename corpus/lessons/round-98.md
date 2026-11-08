# Round 98 lesson — tsukuroi lane

Round 98 (attempt 1), pre-round tip `b3be3f90c2e32400d4e2692b2656ec9a1ba14a8a`; freeze `1cfeb5d5`.
Claims: C1 (depth 8) `tools/limine-pin-battery-r98.py` — the r97 A7 limit closed: the two r97
families assert the echo and the era label their own calls emit, roster unchanged at 105, plus the
A6/R97-D3 docstring correction; C2 (freshness 9) `tools/check-registry-content-r98.py` — the
`RC-BEND-SPAN` capture binds the comma form and two selftest cases pin the non-contiguous
`VARIANTS` branch (12 -> 14), closing the r97 MutRegistry M08 survivor.

## Gate (sources opened this round; contract `CORPUS.md` §SOURCES.md)

| row | URL opened 2026-11-08 | tier | located quote (≤25 words) | admit / reject |
|---|---|---|---|---|
| S394 (new, own-work) | `tools/check-limine-pins.py` at the round-98 freeze (sha256 `7d79ac29…`) | A | `resolved \`limine_version\` and \`limine_version_source: "probe"\`` (BYTE 4425); the MAIN return's field lines at BYTE 16931 / 17037, the CANNOT-EVALUATE early return's copies at BYTE 11230 / 11344 | **admit** — supersedes S393, whose anchor cell labelled the early-return byte pair as "main return after parsing"; the teaches is unchanged and now names both sites |
| S392 (re-open) | https://docs.python.org/3/library/functions.html#int | A | pinned bytes byte-identical to the r97 pin: 331022 bytes, sha256 `d92580dd…`; offsets 157767 / 153202 / 159315 re-measured with `grep -abo` | **admit** (re-open, no drift) — leading-zero components are legal decimal spellings for an explicit base |
| rejected candidate | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/CONFIG.md | — | HTTP 200, 27609 bytes, sha256 `f44f3a19…`; `grep -c` for the gate's four JSON fields, for `echo` and for `version` → 0 / 0 / 0 | **reject** — the page documents config keys and their values; it states nothing about the gate's JSON fields, echo semantics or the era label, so it grounds none of this round's propositions |

Census (frozen command `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
tsukuroi`): before `git show b3be3f90:corpus/SOURCES.md` → exit 0, 392 rows
(`grep -cE '^\|[[:space:]]*S[0-9]{3,}'`); after the landed tree → **394 rows, exit 0, 0 E
findings** (57 W04 + 1 W01, the standing warning set). Rows added by tier: two A (own-work, S393
and its correction S394). Rows touched old→new in place: the table below — S393's `status` and
`used-by` (supersession), and nothing else. Frontier rows advanced: the r97 Frontier's "field/echo
coverage of the new members (A7)" and "MutRegistry's M08 selftest case" are closed; its "unbound
registry rows" (153 of 157 at the base, 156 of 160 at the tip — amendment A6) and its three
measured C2 gaps remain open and are carried into the Frontier section below.

### In-place registry changes (old → new)

| row | field | old | new |
|---|---|---|---|
| S393 | status | `mined` | `queued` (superseded by S394) |
| S393 | used-by | `corpus/knowledge/limine-metadata-assertions-r98.md, corpus/lessons/round-98.md` | `—` (S394 carries the citations) |

## Mistakes

- **R98-FIELD-NOT-ASSERTED** — class: a family that asserts the pin consequence but not every
  field its claim names. The r97 families `REFUSAL-VERSIONS-9DIGIT-Z` and
  `LEADING-ZERO-NORMALIZE` sent the spellings and read rc/pins, leaving `limine_version` and
  `visibility_era` unread, so a field-only lie and a normalized echo each read `met 105/105`
  (`.ufo/waves/round-97/w1/ReviewBattery/attack-1-field.json`, `attack-2.json`; amendments A7).
  Captured-by: QUALITY 122 (a declaration sentence of the form "a candidate that reaches the
  target must X" needs a control that lacks X) — the rule existed but was never applied to a
  family's field coverage. Fix: r98 sets `check_echo`/`check_era` on both families; red-before =
  the r97 battery reads `met 105/105` on N07 and N08 (`before/dev/c1-dn-N07-runs1.json`,
  `c1-dn-N08-runs1.json`; `w1/ExecDoNothing/`), green-after = `103/105` and `104/105` unmet with
  the frozen family sets (`w1/ExecBends/c1-bend-N07-era-field-lie-{canonical,clone}.json`,
  `c1-bend-N08-echo-norm-{canonical,clone}.json`).
  **PROPOSED criterion for QUALITY** (drafted here; the round may not promote it, so it stays a
  proposal): *"A battery family that claims to certify a clause asserts every field of the
  subject's output that the clause names — not only the exit code and the pin list — and one
  committed one-clause bend lies in each asserted field, so that removing the assertion changes a
  leg's reading."* Captured-by: this mistake and the r97 A7 amendment.
- **R98-ANCHOR-FIRST-SITE** — class: a located anchor names the first byte match, and that match is
  a different code path. S393's anchor cell said the gate's echo/era emission lines sit at BYTE
  11230 / 11344 "in the main return"; measured, that pair is the CANNOT-EVALUATE early return
  (conf unreadable) and the main return's copies are at BYTE 16931 / 17037. Evidence:
  `w1/ScoutSources/report.md` §2 and its `receipts/03-*` (both pairs re-measured with `grep -abo`).
  Captured-by: none — QUALITY 141 fixes the offset UNIT (byte vs character), not which site a byte
  pair belongs to, and the lane has no gate that reads an anchor's site. Fix: S394 supersedes S393
  and states both pairs with their line numbers; red-before = S393's cell text naming 11230/11344
  as the main return, green-after = S394's cell naming 16931/17037 as the main return and
  11230/11344 as the early return, both re-measured this round.
- **R98-SPAN-BRANCH-UNTESTED** (the r97 M08 class, mined to closure) — class: a derivation branch
  with no fixture. `derive_variant_span` returns the comma form for non-contiguous labels, but no
  selftest fixture carried such a label set, so the first-label-only mutant M08 survived all three
  legs (`.ufo/waves/round-97/w1/MutRegistry/receipts/M08.diff`). Captured-by: none — the mutation
  battery was the only thing that saw it, and nothing required a case per branch. Fix: `span-gap`
  and `span-gap-lie` in the r98 selftest; red-before = the same mutation on the r97 checker reads
  `PASS 12/12` (`w1/MutRegistry/receipts/M08-on-r97-selftest.txt`; `before/dev/c2-selftest-r97.txt`
  is the pristine control), green-after = `FAIL 12/14` on the r98 checker with exactly `span-gap`
  and `span-gap-lie` red (`before/dev/c2-m08-selftest.txt`, independently reproduced in
  `w1/ExecRegistry/report.md` and `w1/ScribeLesson/receipts/m08-r98-selftest.txt`).
- **R98-MUTANT-DIRECTION-READ** — class: a kill/survive call read in the wrong direction. Two seats
  classified battery mutants B01 (`meta_ok` ignores `check_echo`) and B02 (`meta_ok` ignores
  `check_era`) as *survivors* because the leg reads `met` where the claim requires `unmet`; that
  difference is exactly the leg detecting the mutant — a mutant is killed when a leg's reading
  changes away from the frozen expectation, so B01 is killed by N08 (`met 105/105` vs `unmet
  104/105`) and B02 by N07 (`met 105/105` vs `unmet 103/105`). Evidence:
  `w1/MutRegistry/receipts/B01-N08.txt`, `B02-N07.txt`; the same tables call them survivors
  (`w1/MutRegistry/report.md`, `w1/ScribeLesson/round-98.review.md` (c)). Captured-by: none — the
  item's kill sentence ("a mutant is KILLED when at least one leg changes status/findings in the
  direction the clause protects") did not say which direction the *reading* moves. Fix: this row
  plus the corrected classifications in the round report; the technique rule belongs in QUALITY
  next round (a mutant that makes a leg read *better* than frozen is killed, not surviving).
- **R98-RECEIPT-NAME-MISMATCH** — class: a receipt's name states a different subject than its
  contents. `w1/CriticClaims/receipts/15-m08-selftest.txt` is named for M08 but reads `FAIL 2/14`
  with an extra `RC-VALUE-MISMATCH` on almost every case — the signature of a comma-always mutant,
  not the frozen `numbers[:1]` first-label-only M08 (whose reading is `FAIL 12/14` with exactly the
  two gap cases red). Captured-by: the reviewer's per-case table (the two readings do not match).
  Fix: amendment A2 records the distinction and the M08 kill is cited from the L1 receipt and
  ExecRegistry's independent run, never from that file.

The round's own limits name the rules it works under: QUALITY 139 (a published numeric bound is
certified at its boundary on both legs — the X/Y legs that stay unasserted, A5) and QUALITY 140 (a
target clause is re-read against one development run before the freeze — the pre-freeze runs in
`before/dev/`). Two files in `before/dev/` carry no information and must not be cited as receipts:
`c1-battery-selftest-reference.txt` holds only `rc=143` (the L1 killed a reference-selftest run
that stalled under fleet load) and `c1-bend-N08-runs3.txt` is empty (that batch was killed with
its parent shell); the 3-run N08 readings live in `w1/ExecBends/c1-bend-N08-echo-norm-*.json` and
`w1/ScribeLesson/receipts/c1-n08-r98-runs3.json`.

## Counter-attack scoreboard (QUALITY 115)

`w1/` = `.ufo/waves/round-98/w1/`. Outcomes use the round's kill direction: a mutant is killed when
a leg's reading moves away from the frozen expectation.

| claim | attack fielded | receipt | outcome |
|---|---|---|---|
| C1 | era lie for every version | `ReviewBattery/g1-era-all-r98.json` | killed — `unmet 102/105`, three families, 0 error rows |
| C1 | fixed echo for every explicit flag | `ReviewBattery/g2b-fixed-echo-r98.json` (r97 `g2b-…-r97.json`) | killed — r98 `100/105` vs r97 `102/105`, the delta exactly the two sharpened families |
| C1 | era lie only for the X-cap `999999999.9.9` | `ReviewBattery/g3-xcap-r98.json` | killed weakly — `104/105`, only `EXPLICIT-VERSION-ERA`, 1 case (amendment A5) |
| C1 | source `probe` for an explicit flag | `ReviewBattery/g4-probe-source-r98.json` | killed — `102/105`; the echo assertion covers version and source |
| C1 | echo truncated to 3 chars | `ReviewBattery/g5b-trunc3-r98.json` | killed — `100/105`; all 20 failed cases are meta-only |
| C1 | **era lie only for the Y-cap spellings** | `ReviewBattery/g6-y-era-r98.json`; `CriticClaims/receipts/batt-y2.txt` | **SURVIVES** — `met 105/105` on both batteries; narrowed by amendment A4 to the Z/LZ scope, routed r99 |
| C1 | N07 era-field-lie bend | `ExecBends/c1-bend-N07-*-{canonical,clone}.json` | killed — `103/105` x3 both layouts, exact set, 0 error rows |
| C1 | N08 echo-norm bend | `ExecBends/c1-bend-N08-*-{canonical,clone}.json` | killed — `104/105` x3 both layouts, exact set, 0 error rows |
| C1 | blindness: r97 battery on the gate and both bends | `ExecDoNothing/dn-*.json` | blindness holds — `met 105/105` x3 each, control `e678c34f…` = `b3be3f90:tools/limine-pin-battery-r97.py` |
| C1 | battery mutant B01 (`check_echo` ignored) | `MutRegistry/B01-N08.txt` | killed — N08 reads `met 105/105` vs frozen `unmet 104/105` |
| C1 | battery mutant B02 (`check_era` ignored) | `MutRegistry/B02-N07.txt` | killed — N07 reads `met 105/105` vs frozen `unmet 103/105` |
| C1 | battery mutant B03 (Z family's `check_echo` reset) | `MutRegistry/B03-{landed,N07,N08}.txt` | **SURVIVES** — both bends byte-identical to pristine; no committed bend lies in the echo of a Z spelling (routed r99) |
| C1 | battery mutants B04/B05 | `MutRegistry/B04-N07.txt`, `B05-landed.txt` | killed — `104/105 [Z]` on N07 and on the landed gate |
| C1 | class behind B01-B03: `--selftest` cannot see an assertion removal | `MutRegistry/receipts/lie-kind-coverage.txt` | structural gap — `LIE_KINDS` has 12 members, none `limine_version`/`visibility_era`; the fix is an echo/era lie kind (r99) |
| C2 | checker M01/M02/M04/M06/M09/M10 | `MutRegistry/M0x-selftest.txt`, revision legs | killed (M09 only via `span-gap`; M06 via the revision legs) |
| C2 | checker M08 (first-label-only span) | `MutRegistry/M08-on-r97-selftest.txt`, `M08.diff`; `before/dev/c2-m08-selftest.txt` | killed — `FAIL 12/14` on r98 vs `PASS 12/12` on r97; D2/D2lie invert |
| C2 | checker M07 (ancestor check skipped) | `MutRegistry/probe-nonancestor.txt` | **SURVIVES** — outside `--selftest`'s construction; non-ancestor probe reads rc 2 pristine vs rc 0 on the mutant (r97 class, routed r99) |
| C2 | D1 (row `N01-N04` -> `N01,N03`) | `ExecRegistry/D1-*`, `ReviewRegistry/03-D1*` | killed — r98 `FAIL` one `RC-VALUE-MISMATCH`; r97 `RC-CELL-MISSING` |
| C2 | D2 / D2lie (gap keys) | `ExecRegistry/D2*`, `D2lie*` | discrimination — r98 PASS / M08 FAIL on D2; r98 FAIL / M08 PASS on D2lie |
| C2 | **hybrid cell `VARIANTS N01-N04,N05`** | `ReviewRegistry/receipts/17-f-mixed.txt` | **SURVIVES** — the hyphen arm wins, the extra label is dropped, `PASS 7/7` (amendment A1, routed r99) |
| C2 | second contradictory mention in the same cell | `ReviewRegistry/receipts/16-extra-probes.txt` | **SURVIVES** — first mention wins (amendment A1, routed r99) |
| C2 | whitespace / lowercase forms | `CriticClaims/receipts/capture-audit.txt` | fail-closed — `RC-CELL-MISSING`, rc 1 (amendment A3) |
| C2 | derivation forced to the declared value | `ReviewRegistry` patch, `ExecRegistry` legs | flips `FAIL -> PASS`: the comparison is real |
| — | registry-row coverage at the tip | `ScoutDrift/report.md`, `w1/ScribeLesson/receipts/coverage-at-tip.txt` | FAIL at the freeze tip (3 rows missing, as designed), PASS after the settle rows |

**Converging, or moving the hole?** C1: the two committed bends and 3 of 5 battery mutants are
killed; the survivors are one *spelling class* (Y-cap fields) and one *assertion* (Z echo) with no
witness, plus a structural selftest gap that cannot see assertion removal. C2: M08 is closed by two
cases and a doctored inversion, while M07 and two capture shapes (hybrid, same-cell restatement)
survive. The survivors share one class — *a property asserted but never exercised by a committed
adversary* — which is the same class the round's own mistake table names; r99's queue is to give
each survivor a witness rather than to widen the roster again.

## Frontier moved this round

The r97 A7 field/echo limit and the r97 M08 selftest case are closed as described in the mistakes
above. What remains, by name (all recorded in `corpus/README.md` § "Frontier (round-98 addition)"):
Y-cap and X-cap field fidelity where the sending family does not assert the fields (A4/A5; the X leg
rides on one EXPLICIT case); the Z-family echo with no witness (B03); the battery selftest's lack of
an echo/era lie kind; the checker selftest's untested `GitWorkspace`/ancestor branch (M07); the
hybrid and same-cell-restatement capture shapes (A1); the spaced/lowercase forms (A3); the r98
battery's unchanged JSON schema token (A7); and the carried r97 items (unbound rows, co-doctoring,
printed-tally parsing) and r96/r89 items.

## Routed (r97 -> r98)

| r97 routed item | r98 treatment | evidence |
|---|---|---|
| R97-D3/A6 LZ docstring names the wrong text-comparer member | closed — the r98 successor's `fam_leading_zero_normalize` names `12.000000009.000000005` and the era-A-when-int-says-B direction; the r97 bytes stay as filed with their manifest relation stated | `tools/limine-pin-battery-r98.py` docstring; `w1/ScribeLesson/receipts/04-a6-docstring-offsets.txt` |
| R97-D4 C2's three measured gaps | carried as named Limits (uncovered cells, co-doctoring, printed tally); the unbound-row count is corrected 150 -> 153 at `b3be3f90` / 156 at the settled tip (amendment A6) | `corpus/README.md` § "Frontier (round-98 addition)"; amendment A6 |
| r97 M08 survivor | closed by two selftest cases + the D2/D2lie inversion | `before/dev/c2-*`; `w1/ExecRegistry/report.md` |
| R97-D1 doctored-leg revision attribution | each receipt's own revision is cited from `before/fixtures/doctored-r98-revision.txt` and the seats' scratch revisions | `before/dev/c2-doctored-summary.txt`; `w1/ExecRegistry/report.md` §4 |
| R97-D2 numeric decomposition | the r98 report quotes `git diff --numstat`-style counts, not diffstat totals | `w1/ScribeLesson/receipts/routed-defects.txt` |
