# Round 98 lesson — tsukuroi lane (seat draft; the L1 integrates into `corpus/lessons/round-98.md`)

Round 98 (attempt 1), pre-round tip `b3be3f90c2e32400d4e2692b2656ec9a1ba14a8a`; freeze `1cfeb5d5`.
C1 (depth 8, tied lowest): `tools/limine-pin-battery-r98.py` — the r97 battery with
`check_echo` and `check_era` set on `REFUSAL-VERSIONS-9DIGIT-Z` and `LEADING-ZERO-NORMALIZE` plus
the corrected LZ docstring (R97-D3/A6) — closing the r97 A7 limit, where a field-only lie and a
normalized echo each read `met 105/105` (`.ufo/waves/round-97/w1/ReviewBattery/attack-1-field.json`,
`attack-2.json`); roster unchanged at 105.
C2 (freshness 9): `tools/check-registry-content-r98.py` — the `RC-BEND-SPAN` capture extended to the
comma form and two selftest cases for the non-contiguous `VARIANTS` branch (the r97 MutRegistry
M08 class); selftest 12 → 14.

Every number below was run by this seat; the receipts are under
`.ufo/waves/round-98/w1/ScribeLesson/receipts/`. `sha256sum -c
.uufo/waves/round-98/before/instruments.sha256` → 27/27 `OK`, exit 0, before any measurement.

## Gate (sources opened this round; contract `CORPUS.md` §SOURCES.md)

| row | source opened 2026-11-08 | tier | located quote (≤25 words) | admit / reject |
|---|---|---|---|---|
| S393 (new, own-work) | `tools/check-limine-pins.py` at the round-98 freeze (sha256 `7d79ac29…`) | A | `resolved \`limine_version\` and \`limine_version_source: "probe"\`` (BYTE 4425 → line 47; the field lines `"limine_version": limine_version` at BYTE 11230 → line 200 and `"visibility_era": "12.9.5+" if era_b else "pre-12.9.5"` at BYTE 11344 → line 202 are the **CANNOT-EVALUATE early return**; the main return's copies are at BYTE 16931 → line 316 and BYTE 17037 → line 318) | **admit** — the gate's own report contract, re-derived this round by running the gate on the LZ and Z spellings: the flag spelling is echoed verbatim with source `flag`, and `visibility_era` follows the numeric tuple. The row's own anchor cell labels the early-return pair "main return after parsing"; the corrected row (S394) carries both pairs |
| S394 (new, own-work) | same file, same freeze bytes | A | the MAIN return's field lines at BYTE 16931 / 17037 (lines 316-318) with the early return's copies at BYTE 11230 / 11344 (lines 200-202), plus the docstring phrase at BYTE 4425 | **admit** — supersedes S393; the teaches is unchanged, the anchor now names both sites |
| S392 (re-open) | https://docs.python.org/3/library/functions.html#int | A | "have leading zeros, be surrounded by whitespace," (BYTE 157767 of the 331 022-byte pin, sha256 `d92580dd…`; `id="int"` at BYTE 153202, the base-0 contrast `disallows leading zeros` at BYTE 159315) | **admit** (re-open, **byte-identical, no drift**) — the live fetch is byte-identical to the r97 pin `.ufo/waves/round-97/after/gate/functions.html` (`d92580dd…`, 331 022 bytes) and all three offsets re-measure exactly |
| rejected candidate | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/CONFIG.md | — | HTTP 200, 27 609 bytes, sha256 `f44f3a19133cb3dc14d6d8b402ed585feb98a36bc4b263c37aa92f621f603763`; token counts over those bytes: `limine_version` 0, `limine_version_source` 0, `visibility_era` 0, `echo` 0, `int(` 0, `leading zero` 0, `version` 0, `JSON` 0 | **reject** — upstream's *limine.conf* reference documents config keys and their values; it says nothing about the gate's JSON report contract, the echo semantics or the era label, so it grounds none of this round's propositions (the `version` token occurs 0 times, so it cannot ground S392's `int()` statement either) |

Census (frozen command `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate
--root /home/vgpnk/Projects/shokunin tsukuroi`): **exit 0**, `tsukuroi ok`, **0 E findings**
(57 W04 + 1 W01, the same warning set as r97). Row counts by
`grep -cE '^\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md`: **392** at the pre-round base
(`git show b3be3f90:corpus/SOURCES.md`), **393** at the freeze commit
(`git show 1cfeb5d5:corpus/SOURCES.md`), **394** in the working tree at the time of this draft
(S394 supersedes S393; S393's status cell is `queued` and its used-by cell `—`, S394's used-by
cell names `corpus/knowledge/limine-metadata-assertions-r98.md, corpus/lessons/round-98.md`).
Rows added by tier: **two A (own-work)** — S393 (superseded, `queued`) and S394 (`mined`).
Rows touched old → new in place: S393 `status` `mined` → `queued` and S393 `used-by` →
`corpus/knowledge/limine-metadata-assertions-r98.md, corpus/lessons/round-98.md` → `—`.

## Mistakes

- **R98-FIELD-NOT-ASSERTED** — class: a family that asserts the pin consequence but not every
  field its own case's answer names. The r97 families `REFUSAL-VERSIONS-9DIGIT-Z` and
  `LEADING-ZERO-NORMALIZE` sent the spellings and read rc/pins, leaving `limine_version` and
  `visibility_era` unread, so a field-only lie and a normalized echo each read `met 105/105`.
  Evidence pointer: `.ufo/waves/round-97/w1/ReviewBattery/attack-1-field.json` and `attack-2.json`
  (re-read this round: 3 runs each, `met 105/105`, `failed_families []`, 0 non-null error rows)
  and the r97 wave's amendment A7. Captured-by: **QUALITY 122** ("a declaration sentence of the
  form 'a candidate that reaches the target must X' is written only if a committed control that
  lacks X reads below target at the freeze") — the criterion exists but no one applied it to a
  family's *field* coverage, so the wave found the gap after the freeze.
  Fix: r98 sets `check_echo`/`check_era` on both families (byte-level: set at BYTE 81747/81771
  (Z family) and 82964/82988 (LZ family); asserted in `meta_ok` at BYTE 98004/98097).
  **Red-before** = the r97 do-nothing battery — byte-identical to the r97 landed battery
  (`git show b3be3f90:tools/limine-pin-battery-r97.py | sha256sum` = `e678c34f…` = the control's
  digest) — reads `met 105/105` ×3 with 0 error rows on **both** bends
  (`receipts/dn-n07-r97-runs3.json`, `dn-n08-r97-runs3.json`).
  **Green-after** = the r98 battery reads `103/105` unmet ×3 with failed families exactly
  `[LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT-Z]` on N07 (`receipts/c1-n07-r98-runs3.json`,
  `c1-n07-count.txt`) and `104/105` unmet ×3 with failed families exactly
  `[LEADING-ZERO-NORMALIZE]` on N08 (`receipts/c1-n08-r98-runs3.json`, `c1-n08-count.txt`), 0
  error rows on every run, measured with the claim's counting command
  `python3 .ufo/waves/round-95/before/controls/count-runs.py <out> --family
  REFUSAL-VERSIONS-9DIGIT-Z --family LEADING-ZERO-NORMALIZE`.
  **Proposed criterion text** (for the L1 to accept or reject as an appended criterion, never an
  in-place edit of `corpus/QUALITY.md`): *"a battery family that names a reported field asserts
  that field — when a family's expected answer names a field of the tool's JSON report, the
  family's assertion reads that field, and a near-miss control that lies in exactly that field and
  implements everything else reads below target at the freeze."*

- **R98-SPAN-BRANCH-UNTESTED** (the r97 M08 class) — class: a derivation branch with no fixture.
  `derive_variant_span` returns the comma form for non-contiguous labels, but no r97 selftest
  fixture carried such a label set, so the first-label-only mutant M08 survived
  (`.ufo/waves/round-97/w1/MutRegistry/receipts/M08.diff`). Evidence pointer: that diff plus the
  mutation battery's `receipts/M08-on-r97-selftest.txt`. Captured-by: **none** — the mutation
  battery was the only thing that saw it, and nothing required a case per derivation branch.
  Fix: the `span-gap` and `span-gap-lie` selftest cases in the r98 checker.
  **Red-before** = the same one-line mutation on the r97 checker reads `selftest PASS 12/12`
  (my re-derivation, `receipts/m08-r97-selftest.txt`; the frozen `before/dev/c2-selftest-r97.txt`
  is the *pristine* r97 checker's own selftest and shows the same tally but no mutant).
  **Green-after** = the same mutation on the r98 checker reads `selftest FAIL 12/14`, with
  `span-gap FAIL ['RC-VALUE-MISMATCH']` and `span-gap-lie FAIL []`
  (`receipts/m08-r98-selftest.txt`; identical in content to the frozen
  `before/dev/c2-m08-selftest.txt`), and the D2/D2lie inversion follows (r98 `PASS` on D2 /
  M08 `FAIL`; r98 `FAIL` on D2lie / M08 `PASS` — `receipts/08-c2-doctored-legs.txt`).

- **R98-Y-FIELD-LIE-UNASSERTED** — class: a claim sentence universal over spellings where the
  instrument is bound to a subset. A field-only `visibility_era` lie for the Y-cap spellings
  `12.999999999.4` / `0.999999999.0`, pins correct, reads `met 105/105` with 0 error rows on the
  r98 battery **and** on the r97 battery (`w1/ReviewBattery/g6-y-era-r98.json`,
  `g6-y-era-r97.json`; `w1/CriticClaims/receipts/batt-y2.txt`). C1's predicate sentence says "a
  gate that answers every pin correctly but lies in either field reads `unmet` on the r98
  battery" — false for the Y spellings. Captured-by: QUALITY 122 again (the control that lacks X
  was never run for the Y spellings); the plan's Limits section already declares that the X/Y
  families set neither flag, so the *limit* is named and the *claim sentence* is wider than the
  limit. Fix: narrow the sentence to the Z/LZ spellings the two families send and carry the
  Y-spelling field lie as a named limit. Red-before: `met 105/105` ×3 on both batteries; green-
  after: the Z/LZ legs read `103/105` and `104/105` unmet with the exact frozen family sets.

- **R98-ANCHOR-FIRST-SITE** — class: a located anchor names the first byte match, and that match
  is a different code path. S393's anchor cell called the gate's echo/era emission lines "the main
  return after parsing"; measured, BYTE 11230/11344 is the CANNOT-EVALUATE early return
  (lines 200/202) and the main return's copies are at BYTE 16931/17037 (lines 316/318).
  Evidence pointer: `w1/ScoutSources/report.md` §2 and my own re-measure
  (`receipts/06-gate-emission-sites.txt`). Captured-by: none — QUALITY 141 fixes the offset
  *unit* (byte vs character), not which code site a byte pair belongs to, and no lane gate reads
  an anchor's site. Fix: S394 supersedes S393 and names both pairs with their line numbers.
  Red-before: S393's cell text naming 11230/11344 as the main return; green-after: S394's cell
  naming 16931/17037 as the main return and 11230/11344 as the early return, both re-measured.

- **R98-ASSERTION-WITHOUT-LIE-KIND** — class: an assertion with no control that can falsify it.
  The battery's `--selftest` lie set (`LIE_KINDS`, 12 members) contains no member that mutates
  `limine_version` or `visibility_era`, so *removing* either assertion is unobservable to the
  selftest by construction: mutant B01 (`meta_ok` ignores `check_echo`) reads `met 105/105` on N08
  where the claim requires `unmet 104/105`, and B02 (`meta_ok` ignores `check_era`) reads `met
  105/105` on N07 where the claim requires `unmet 103/105`; B03 (the Z family's `check_echo`
  reset) is invisible to both committed legs. Evidence pointer:
  `w1/MutRegistry/receipts/B01.diff`, `B02.diff`, `B03.diff`, `lie-kind-coverage.txt`.
  Captured-by: none. Fix (a later round): add a `("echo",)` and a `("era",)` lie kind to
  `LIE_KINDS` — the one-line fix the mutation seat names. Red-before: B01/B02 read `met 105/105`
  on the bend that must kill them; green-after: with the lie kinds present, the pristine battery
  reads `unmet` with the three `check_echo` (or three `check_era`) families failing while the
  mutants pass them.

## Counter-attack scoreboard (revives QUALITY 115, `corpus/QUALITY.md:226`)

Seats and whether a `report.md` exists at draft time: `ExecBends` **no report (receipts only)**,
`ExecDoNothing` yes, `ExecGateRuns` **no report (receipts only)**, `ExecLints` yes, `ExecRegistry`
yes, `MutRegistry` yes, `ReviewBattery` yes, `ReviewRegistry` yes, `ScoutSources` yes, `ScoutDrift`
**no report (receipts only)**, `ScribeKnowledge` **no report (receipts only)**, `CriticClaims`
**no report (ledger + receipts only)**, `ConnectorOverlap` yes, `ScribeLesson` this seat.

| claim | attack fielded | receipt | outcome |
|---|---|---|---|
| C1 | era lie for every version | `w1/ReviewBattery/g1-era-all-r98.json` | killed: `unmet 102/105`, failed `[EXPLICIT-VERSION-ERA, LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT-Z]`, 0 error rows |
| C1 | fixed echo `7.7.7` for every explicit flag | `w1/ReviewBattery/g2b-fixed-echo-{r97,r98}.json` | killed: r98 `unmet 100/105` vs r97 `unmet 102/105` |
| C1 | era lie only for the X-cap `999999999.9.9` | `w1/ReviewBattery/g3-xcap-r98.json` | killed, weakly: `unmet 104/105`, only `EXPLICIT-VERSION-ERA`, 1 failed case of 420 |
| C1 | source `probe` for an explicit flag | `w1/ReviewBattery/g4-probe-source-r98.json` | killed: `unmet 102/105`, failed `[EXPLICIT-VERSION-ECHO, LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT-Z]` |
| C1 | echo truncated to 3 chars | `w1/ReviewBattery/g5b-trunc3-{r97,r98}.json` | killed: r98 `unmet 100/105` vs r97 `unmet 102/105` |
| C1 | **era lie only for the Y-cap spellings** | `w1/ReviewBattery/g6-y-era-{r97,r98}.json`, `w1/CriticClaims/receipts/batt-y2.txt` | **survives** `met 105/105` on both batteries — narrows C1's field sentence to Z/LZ |
| C1 | N07 era-field-lie bend | `w1/ExecBends/count-N07-*-{canonical,clone}.txt`, `w1/ScribeLesson/receipts/c1-n07-count.txt` | killed: `103/105` unmet ×3 in both layouts, failed exactly `[LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT-Z]`, 0 error rows |
| C1 | N08 echo-norm bend | `w1/ExecBends/count-N08-*-{canonical,clone}.txt`, `w1/ScribeLesson/receipts/c1-n08-count.txt` | killed: `104/105` unmet ×3 in both layouts, failed exactly `[LEADING-ZERO-NORMALIZE]`, 0 error rows |
| C1 | blindness: r97 battery on the landed gate and both bends | `w1/ExecDoNothing/dn-*.json`, `w1/ScribeLesson/receipts/dn-*-r97-runs3.json` | blindness holds: `met 105/105` ×3, 0 error rows on all three gates |
| C1 | layout: canonical vs `git clone --shared` | `w1/ExecGateRuns/03-canonical.txt`, `06-clone-run.txt`, `11-agree.txt`, `w1/ScribeLesson/receipts/c1-gate-r98-runs3.txt` | agrees: `met 105/105` ×3 in both layouts, per-run schema and verdict agree |
| C1 | battery mutant B01 (`meta_ok` ignores `check_echo`) | `w1/MutRegistry/B01-N08.json` | **survives**: N08 reads `met 105/105` where the claim requires `unmet 104/105` |
| C1 | battery mutant B02 (`meta_ok` ignores `check_era`) | `w1/MutRegistry/B02-N07.json` | **survives**: N07 reads `met 105/105` where the claim requires `unmet 103/105` |
| C1 | battery mutant B03 (Z family `check_echo` reset) | `w1/MutRegistry/B03-*.json` | **survives**: both committed legs identical to pristine |
| C1 | battery mutant B04 (LZ family `check_era` reset) | `w1/MutRegistry/B04-N07.json` | killed: N07 `104/105 [Z]` where pristine is `103/105 [LZ, Z]` |
| C1 | battery mutant B05 (`era_b()` inverts for the 9-digit Z spelling) | `w1/MutRegistry/B05-landed.json` | killed: landed `104/105 [Z]` where the claim requires `met 105/105` |
| C2 | checker mutants M01, M02, M04, M06 | `w1/MutRegistry/M0{1,2,4,6}-*` | killed (selftest `FAIL 3/14`, `FAIL 4/14`, crash on `row-missing`, `FAIL 0/7` on every revision leg) |
| C2 | checker mutant M07 (ancestor check skipped) | `w1/MutRegistry/receipts/probe-nonancestor.txt` | **survives** — outside `--selftest`'s construction; proved non-equivalent (non-ancestor commit: pristine rc 2, M07 rc 0); the r97 class, unchanged |
| C2 | checker mutant M08 (`derive_variant_span` first label only) | `w1/MutRegistry/receipts/M08-on-r97-selftest.txt`, `w1/ScribeLesson/receipts/m08-r{97,98}-selftest.txt` | killed: `FAIL 12/14` on the r98 selftest where the same mutation reads `PASS 12/12` on the r97 checker; D2/D2lie invert |
| C2 | checker mutants M09 (capture reverted), M10 (comma branch) | `w1/MutRegistry/M09-*`, `M10-*` | killed (`FAIL 13/14` and `FAIL 12/14` plus the D2/D2lie inversion) |
| C2 | covered cell doctored (D1) | `w1/ExecRegistry/D1-*.json`, `w1/ReviewRegistry/03-D1*`, `w1/ScribeLesson/receipts/08-c2-doctored-legs.txt` | killed: r98 `FAIL` with exactly one `RC-VALUE-MISMATCH`; the r97 do-nothing checker reads `RC-CELL-MISSING` |
| C2 | gap keys + comma row (D2) | `w1/ExecRegistry/D2-*.json`, `w1/ScribeLesson/receipts/08-c2-doctored-legs.txt` | r98 `PASS 7/7`; M08 `FAIL` one `RC-VALUE-MISMATCH` |
| C2 | gap keys + contiguous row (D2lie) | `w1/ExecRegistry/D2lie-*.json`, `w1/ScribeLesson/receipts/08-c2-doctored-legs.txt` | r98 `FAIL` one; M08 `PASS 7/7` — the inversion |
| C2 | coverage-gate blindness on each doctored revision | `w1/ExecRegistry/*-coverage`, `w1/ScribeLesson/receipts/09-c2-coverage-doctored.txt` | `PASS 157/157`, 0 findings, ×3 — satisfied, but vacuous as evidence of a caught doctor |
| C2 | **hybrid cell `VARIANTS N01-N04,N05`** | `w1/ReviewRegistry/receipts/17-f-mixed.txt` | **survives** — the hyphen arm of the alternation wins before the comma tail, so the cell truncates and reads `PASS 7/7` (M08 and the coverage gate read PASS too) |
| C2 | a second, contradictory mention in the same cell | `w1/ReviewRegistry/receipts/16-extra-probes.txt` | **survives** — `re.search` binds the first mention; the stated limit is narrower than the behaviour |
| C2 | whitespace / lowercase variants | `w1/ReviewRegistry/receipts/16-extra-probes.txt`, `w1/CriticClaims/receipts/capture-audit.txt` | fail-closed: `RC-CELL-MISSING`, rc 1 |
| C2 | derivation forced to the declared value | `w1/ExecRegistry`, `w1/ReviewRegistry` doctored legs | flips `FAIL → PASS` — the comparison is real |
| — | registry coverage at the tip | `w1/ScoutSources/report.md` (incidental), `w1/ScribeLesson/receipts/coverage-at-tip.txt` | **FAIL at the tip** (3 × `REGISTRY-ROW-MISSING`; `tools_total 160` vs `registered 157`); `PASS 157/157` at `b3be3f90` — a settle item |

QUALITY 115's question — converging, or only moving the hole? C1's two bends and 3 of 5 battery
mutants are killed; B01, B02, B03 and the Y-cap field lie survive, and the class behind all four
is the same one: *a field no lie kind can mutate is asserted but never exercised*. C2's M08 is
closed, M07 survives unchanged, and the extended capture carries two new false-PASS shapes.

## Routed (r97 → r98)

| r97 routed item | r98 treatment | evidence |
|---|---|---|
| R97-D1 doctored-leg revision attribution | each receipt cites its own revision; the revision-bearing file is `before/fixtures/doctored-r98-revision.txt` (base / D1 `aab954f1…` / D2 `d17ebc56…` / D2lie `3155fd3d…`), the verdict file is `before/dev/c2-doctored-summary.txt` | `before/fixtures/doctored-r98-revision.txt`, `before/dev/c2-doctored-revisions.txt` |
| R97-D2 numeric decomposition of the r96-tool diff | the diff is stated as numstat, **6 insertions / 2 deletions** (diffstat total 8 changed lines) | `git diff --numstat f48d1642 9c4b7b16 -- tools/limine-pin-battery-r96.py` → `6 2` (`w1/ScribeLesson/receipts/routed-defects.txt`) |
| R97-D3/A6 LZ docstring names the wrong text-comparer member | closed in the successor: `fam_leading_zero_normalize` names `12.000000009.000000005` and the era-A-by-text / era-B-by-int direction (BYTE 5723; correction marker at BYTE 82590); the r97 bytes stay as filed | `tools/limine-pin-battery-r98.py`; `w1/ScribeLesson/receipts/04-a6-docstring-offsets.txt` |
| R97-D4 C2's three measured gaps (uncovered cells, co-doctoring, printed tally) | carried as named limits, not closed: re-measured this round on the r98 checker — the printed-tally fake (a gate whose `--selftest` prints `selftest PASS 39/39` and executes no case) reads `PASS 7/7`, and an unbound-cell doctor reads `PASS 7/7` | `w1/ScribeLesson/receipts/10-gap-printed-tally.txt`, `11-gap-unbound-cell.txt`; `corpus/README.md` § "Frontier (round-98 addition)" |

## Frontier moved this round

Closed: the r97 A7 field/echo limit (the Z/LZ families assert the fields their own calls emit) and
the r97 M08 survivor (two selftest cases + the D2 inversion). Open and carried: the assertion is
bound to two families only, so the X/Y families' field lies stay uncertified; the battery's own
selftest cannot see a metadata assertion (no echo/era lie kind), so B01–B03 survive; the C2
checker's 150 unbound rows and its three measured gaps; M07 (the ancestor check); and the capture's
two new false-PASS shapes (the hybrid cell, the same-cell restatement). The registry-coverage
gate reads FAIL at the tip until the three r98 registry rows are committed.

{"seat":"ScribeLesson","verdict":"findings","notes":"Seat lesson draft for round 98 (the L1 integrates): Gate with S393/S394 admits, the S392 byte-identical re-open and one reject; Mistakes R98-FIELD-NOT-ASSERTED (red-before = the r97 battery reads met 105/105 x3 on both bends, green-after = 103/105 and 104/105 unmet x3), R98-SPAN-BRANCH-UNTESTED (M08 PASS 12/12 on the r97 checker -> FAIL 12/14 on the r98 checker), R98-Y-FIELD-LIE-UNASSERTED and R98-ANCHOR-FIRST-SITE and R98-ASSERTION-WITHOUT-LIE-KIND; census exit 0, 0 E, 57 W04 + 1 W01, rows 392 (b3be3f90) -> 393 (freeze 1cfeb5d5) -> 394 (working tree after S394); a Counter-attack scoreboard covering all 14 wave seats with the five receipt-only seats named; Routed R97-D1..D4 with the D2 numstat 6/2 measured. 35 receipts under w1/ScribeLesson/receipts/."}
