# Round 100 lesson — tsukuroi lane (draft for `corpus/lessons/round-100.md`)

Round 100 (attempt 1; the lane's graduation round), pre-round tip
`ce73ccaf75d0279385977f03ccb35945c1cf8e07`, freeze `743ce449`, landing `c450cd68` + `69474c55`,
final tip measured here `7961738a`. Claims: C1 (depth 8) `tools/make-r100-bends.py` emits two
component-keyed echo bends (`N12-x-echo`, `N13-y-echo`) of the unchanged gate, and the unchanged r99
battery must move the accepted-cap echo families, with the r98 battery as the do-nothing control;
C2 (freshness 9) `tools/check-registry-content-r100.py` binds `RC-BEND-SPAN` as a label set,
closing the two round-99 named capture limits, with the r99 checker as the do-nothing control.

Non-author spot-check line: **pending non-author closure.**

## Gate (sources opened 2026-11-08; every offset below re-measured by this seat at byte level)

| candidate | source opened / own-work path (access 2026-11-08) | tier | located quote (≤25 words) with byte offset | admit / reject |
|---|---|---|---|---|
| `tools/make-r100-bends.py` (new, generator) | own-work, 4471 bytes, sha256 `7ccfe69e…` | A | `"limine_version": ("999999998.9.9" if limine_version.split(".")[0] == "999999999" else limine_version)` — BYTE 2615 (N12 clause; 8 words); N13 clause at BYTE 3365 (`"limine_version": ("12.999999998.4" …`, 12 words), its lie literal at BYTE 3384 | **admit** — exact-once substitution guard (`text.count(old) != 1` refuses), a no-op guard, `compile(out)` before write; two `VARIANTS` entries, each emitted bend differing from the gate by one `-`/`+` line pair. The re-emission identity test is a scratch-copy experiment, not run by this seat (the tool writes into the frozen wave dir) |
| `tools/check-registry-content-r100.py` (new, gate) | own-work, 38009 bytes, sha256 `7a23a522…` | A | `TOKEN = re.compile(r"N([0-9]+)(?:-N([0-9]+))?")` — BYTE 12025 (3 words); `SEPARATORS = …` at BYTE 12073; `def parse_label_set(expr):` at BYTE 12134 | **admit** — `--selftest PASS 26/26` (rc 0), live table `PASS 7/7 findings 0` at four revisions, twelve fixture cells reproducing the frozen dev table row for row |
| SOURCES **S396** (new, own-work) | the two files above at the freeze `743ce449` | A | generator N12 clause BYTE 2615 / N13 clause **BYTE 3365** (the row prints 3384, the value start); checker `TOKEN` 12025, `SEPARATORS` 12073, `parse_label_set` 12134 | **admit with a correction** — every offset is true, but the row pairs the N12 *clause* start with the N13 *value* start, so a re-measure of N13 the way the row measures N12 lands 19 bytes earlier; see the append-only correction note |
| SOURCES **S397** (new, docs) | https://docs.python.org/3/library/re.html — HTTP 200, 257722 bytes, sha256 `69d64759…`, footer "Last updated on Nov 08, 2026 (14:27 UTC)" at BYTE 257438 | A | `If the whole <em>string</em> matches the regular expression <em>pattern</em>, return a` — BYTE 112171 (11 words, byte-literal); `Matches the empty string, but only at the beginning or end of a word.` — BYTE 69787 (14 words); `id="re.fullmatch"` at BYTE 111489 | **admit with a correction** — the byte-literal form reproduces at 112171; the de-marked-up sentence (`… return a corresponding Match` / `… match object`) returns **-1** under `bytes.find`, so the Gate cell must name the markup split or print the literal |
| SOURCES **S398** (candidate) | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/CONFIG.md — HTTP 200, 27609 bytes, sha256 `f44f3a19…` | C | no located quote: `limine_version` / `visibility_era` / `echo` / `version` each occur 0 times | **reject** — the page documents config keys and grounds nothing about the gate's reported fields; flip: a v12.9.6 page that documents the report contract |
| knowledge entry `corpus/knowledge/limine-echo-bends-r100.md` (draft) | the two instruments + S397 | A | carries §3 "what this does not prove" (X leg is a delta; reference leg not exercised; blanket echo lie cannot attribute) | **admit** — its two recheck commands are runnable and reproduce: `--selftest` 26/26 rc 0 (`receipts/06-selftests.txt`), and the N13 leg `104/105 unmet … REFUSAL-VERSIONS-9DIGIT-Y` **rc 1** run verbatim (`receipts/36-knowledge-recheck-rc.txt`) |
| bend control `N12-x-echo.py` | `.ufo/waves/round-100/before/controls/bends/N12-x-echo.py`, 30409 bytes, sha256 `eb247e16…` | A | bent clause at BYTE 16931 of the bend (the gate's *final verdict* return) | **admit** — `diff -u` the gate: 1 hunk, 1 removed + 1 added line; measured `unmet 103/105` exactly `[EXPLICIT-VERSION-ECHO, REFUSAL-VERSIONS-9DIGIT]`, 0 error rows, ×3 |
| bend control `N13-y-echo.py` | `.ufo/waves/round-100/before/controls/bends/N13-y-echo.py`, 30446 bytes, sha256 `e1e5916f…` | A | bent clause at BYTE 16931 | **admit** — same one-line diff; measured `unmet 104/105` exactly `[REFUSAL-VERSIONS-9DIGIT-Y]`, 0 error rows, ×3 |
| fixture cells `SEP-SPACE`, `SEP-SEMICOLON`, `SEP-PLUS`, `SEP-SLASH` (acceptance) | built by the frozen `.ufo/waves/round-100/before/dev/make-fixtures.py` (the checker's own `build_fixture`) | A | cell text `VARIANTS N01 N02 N03` / `N01; N02; N03` / `N01 + N02 + N03` / `N01/N02/N03` | **admit** — r100 `PASS` rc 0, r99 `FAIL RC-CELL-MISSING` rc 1, on all four |
| fixture cells `SEP-AND`, `UNION` (acceptance) | same builder | A | `VARIANTS N01-N02 and N03` / `VARIANTS N01-N02 and N04-N05` | **admit** — r100 `PASS` rc 0, r99 `FAIL RC-VALUE-MISMATCH` rc 1, on both |
| fail-closed `LETTER`, `PROSE` | same builder | A | `VARIANTS N01a-N03` / `VARIANTS N01 through N03` | **admit (kept closed)** — r100 `FAIL RC-CELL-MISSING` rc 1 on both; the prose connector is still a finding |
| fail-closed `UNION-LIE`, `HYBRID` | same builder | A | a declared union wider than the keys / a comma-span beside a range | **admit (kept closed, one sharper)** — `RC-VALUE-MISMATCH` on r100; HYBRID moves from r99's `RC-CELL-MISSING` to r100's `RC-VALUE-MISMATCH` (the frozen id), which is the frozen "unchanged or sharper" |
| fail-closed `RESTATED` | same builder | A | `VARIANTS N01,N03 then VARIANTS N01-N03` | **admit (kept closed)** — `RC-CELL-AMBIGUOUS` rc 1 on both checkers |
| positive control `GAP` | same builder | A | a non-contiguous `VARIANTS` fixture whose own row states the comma span | **admit** — `PASS` rc 0 on both checkers; the zero-finding control the twelve cells need |

Census (frozen command `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
tsukuroi`): **before** 395 rows → **after** 398 rows, both `exit=0`, both recorded with their
command in `.ufo/waves/round-100/before/census-before-after.txt` (R99-D4's exit-code half landed).
Rows added by tier: two A (S396 own-work, S397 docs) and one C rejection (S398). The frozen command
prints **59 lines** (57 `W04` + 1 `W01` + the `ok` line), and the receipt carries the **tail** of
that output (two lines before, one after) — see `R100-CENSUS-RECEIPT-TAIL` below. Re-run twice by
this seat, byte-identical (md5 `37ed43e2…`), and a run against an isolated root holding only
tsukuroi's own `SOURCES.md` still prints **57** `W04` lines, so the warning set is file-local and
does not depend on a sibling lane's bytes.

### In-place registry changes (old → new)

None — the round adds rows; no existing row's `status`, `recheck` or `used-by` changes.

## Mistakes

Every row below names its class, an evidence pointer that exists in this wave, the criterion that
should have caught it (or `none`), and the fix. A fix is listed only where it is shown able to fail.

- **R100-X-DELTA-COUNTED-AS-FLIP** — class: `overstatement`. The X-cap echo leg is a discrimination
  *delta*, not a closure: the r98 control on `N12-x-echo` reads `unmet 104/105` with
  `failed_families [EXPLICIT-VERSION-ECHO]`, because the r96 `EXPLICIT-VERSION-ECHO` family sends the
  same `999999999.9.9` spelling. Only the Y leg is a met→unmet flip. Evidence:
  `.ufo/waves/round-100/w1/ScribeLesson/receipts/10b-count-runs-summary.txt` (all five legs, ×3, with
  per-family case counts: N12 X `0/4`, Y `4/4`, E `3/4`; N13 Y `0/4`). Captured-by: QUALITY 136
  ("a family that only re-answers a case the old roster already covered is a twin, not a boundary")
  plus the r99 N11-x-era precedent; the freeze applied it before the wave. Fix: the declaration's
  target names the two shapes separately — shown able to fail, because the X leg's frozen sentence
  reads `103/105` with two families, not `104/105` with one, and the r98 leg reads the one-family
  set.
- **R100-CLONE-PATH-PREFIX** — class: `harness/path`. The first clone-layout receipts for the four
  bend/control legs read `0/105` with every one of the 105 families failed, because the gate path
  was built as `$CLONE/$ABSOLUTE_LANE_PATH`; the canonical twin of each leg read the frozen set.
  Evidence: the quarantined runs under `.ufo/waves/round-100/after/c1/harness-fault/` and their
  canonical twins under `.ufo/waves/round-100/after/c1/`. Captured-by: `none` — no criterion said a
  leg that fails *every* family in one layout is a harness fault before it is a verdict; QUALITY 142
  is added for it. Fix: re-run with the layout's own path, keep the `0/N` under `harness-fault/`,
  cite the twin beside it. Shown able to fail: QUALITY 142's red instance is the pair
  `harness-fault/bend-N12-x-echo-clone.json` (`0/105`) against `bend-N12-x-echo-canonical.json`
  (`103/105`).
- **R100-REGISTRY-ROW-CELL-COUNT** — class: `self-application`. The first landing commit `c450cd68`
  wrote the `check-registry-content-r100` row with 7 of the 8 required cells (write-scope absent), so
  at that revision both content checkers and the coverage gate read `CANNOT_EVALUATE`
  (`E-TABLE … line 5951`, `E-REGISTRY-TABLE`). Evidence: this seat's
  `receipts/11-live-table-and-coverage.txt`, `receipts/17-coverage-land-vs-master.txt` (r100 and r99
  both `CANNOT-EVALUATE` at `c450cd68`; both `PASS 7/7` at `69474c55`), and the repair diff
  (`7 → 8` cells). Captured-by: QUALITY 70 ("a tool lands with its registry row") read together with
  QUALITY 71 ("companions agree on every verdict") — the row's *shape* was not re-parsed by the row's
  own instrument before the commit. Fix: the repair is `69474c55`, and the frozen C2 sentence's
  "landing tip" is read as the final landing tip by plan amendment A1; both named surfaces read
  PASS. Shown able to fail: the coverage gate's `CANNOT_EVALUATE` at `c450cd68` and `PASS 165/165` at
  `69474c55` are one command apart.
- **R100-TOOL-WITHOUT-ROW-AT-FREEZE** — class: `state coherence`. The freeze `743ce449` adds both
  round-100 tools but not their registry rows, so `check-registry-coverage.py --revision 743ce449`
  reads `FAIL` with two `REGISTRY-ROW-MISSING` findings (`163/163/165`). Evidence: this seat's
  `receipts/16-coverage-at-freeze.txt`. Captured-by: QUALITY 70's literal wording ("the same round")
  — the rows land in the same *round*, not in the same *commit*, so the rule's own revision check
  fails between the two. Fix: the freeze's coverage reading is quoted as FAIL-with-2-missing and the
  landing revision's as PASS; a future round should land the rows in the freeze commit or record the
  expected two-missing state in the declaration.
- **R99-ONE-ANCHOR-TWO-MEMBERS** — class: `corpus precision` (routed R99-D3). S395's anchor says
  "the two new `LIE_KINDS` members at BYTE 108455"; 108455 is `limine-version` and `visibility-era`
  starts at 108473. Evidence: this seat's `receipts/18-liekinds-disambiguation.txt` and
  `receipts/19-liekinds-grep-abo.txt` — and the row's own cited command is **ambiguous**:
  `grep -abo '"limine-version"'` returns 107815 first (the lie-application dict key) and 108455
  second (the `LIE_KINDS` member). Captured-by: QUALITY 141 — it governs the *unit* of an offset, not
  the one-anchor-per-fact rule; the narrow criterion to add is: one anchor per named fact, and an
  anchor whose search string occurs more than once names the disambiguating context. Fix: this lesson
  names both offsets, and the tuple pair `"limine-version", "visibility-era")` (one hit, 108455) is
  the disambiguated search a re-measuring gate should use.
- **R99-STALE-LOG-HEADING** — class: `bookkeeping` (routed R99-D2). The round-99 LOG headings still
  read `(pending)` / `(pending-settle)` after settle. Evidence: `LOG.md` line 4365's round-100
  append-only correction entry naming both superseded headings (`receipts/33-r99-d2-log-entry.txt`).
  Captured-by: `none` — no criterion said "do not put a status token in a heading written before the
  status exists". Fix: the correction entry lands and no heading is rewritten; shown able to fail
  because the entry quotes both stale headings verbatim while the round-99 bytes stay in place.
- **R99-CENSUS-EXIT-OMITTED** — class: `evidence completeness` (routed R99-D4). The r99 census
  receipt recorded the before count but only the after exit code. Evidence: this seat's
  `receipts/23-census-receipt-completeness.txt` and `receipts/29-census-receipt-is-a-tail.txt`.
  Captured-by: the round prompt's census clause ("paste both outputs and their exit codes") — the
  receipt did not follow it. Fix: `.ufo/waves/round-100/before/census-before-after.txt` now records
  both commands, both exit codes and both row counts; the *output* half is still a tail (see the next
  row), so the fix is partial and is stated as partial.
- **R100-CENSUS-RECEIPT-TAIL** — class: `evidence completeness` (new; the same class as R99-D4).
  The frozen census command prints **59** lines — 57 `W04`, one `W01`, one `ok` — and the before/
  after receipt records the **last two** lines of the before run and the **last one** of the after
  run. Evidence: this seat's `receipts/29-census-receipt-is-a-tail.txt` (the recorded before block
  omits `S386`, which the live run prints; the recorded after block keeps `S387` only) and
  `receipts/23-census-receipt-completeness.txt` (59 lines). Captured-by: the same prompt clause as
  R99-D4, read at the *output* level — "paste both outputs" is not satisfied by a tail. Fix: the
  receipt should either paste all 59 lines or state "tail of 59 lines; full command re-runs
  deterministically (md5 `37ed43e2…`)". Shown able to fail: the omission is visible as a diff between
  the recorded block and the live tail.
- **R100-QUOTE-NOT-BYTE-LITERAL** — class: `corpus precision` (new). The S397 Gate cell prints
  `If the whole string matches the regular expression pattern, return a corresponding Match`
  (and, before the correction, `… match object`). On the pinned 257722-byte page, `bytes.find` of
  **either** de-marked-up sentence returns **-1**; only the marked-up form
  `If the whole <em>string</em> matches the regular expression <em>pattern</em>, return a` reproduces
  at BYTE 112171. Evidence: this seat's `receipts/09-s397-quote-reproduction.txt`,
  `receipts/24-final-gate-quote-table.txt`, `receipts/30-head-s397-s396-anchor-check.txt`. Captured-
  by: QUALITY 141 is half the rule — it names the offset's *unit* and makes a receiving gate
  re-measure the *offset*; it does not require the quoted text to be findable in the pinned bytes.
  The lane already has the convention that handles this (S390/S391: "quoted sentence starts at byte
  157851, split by a code element"), so the criterion to add is: a located quote is either
  byte-literal or marked de-marked-up and paired with its byte start and the split count. Fix: print
  the byte-literal in the Gate cell (11 words, ≤25) and let the `teaches` cell carry the rendered
  reading. Shown able to fail: the same probe returns 112171 for the literal and -1 for the
  paraphrase.
- **R100-MANIFEST-PINS-THE-DECLARATION** — class: `evidence structure` (new). The freeze's
  `instruments.sha256` pins **16** paths, one of which is `.ufo/plans/round-100.md` — the declaration
  whose own amendment slot invites post-freeze writes. After the amendments landed, the harm-guard
  command reads **15 `OK` + 1 `FAILED`** (the plan, pinned `44ae97d8…`, now `b7b163ea…`), while the
  14 instrument/control/fixture/claims bytes are all `OK`. Evidence: this seat's
  `receipts/28-manifest-split.txt` (`OK count: 15`; the tools-only manifest `14/14`). Captured-by:
  `none` — the manifest's purpose ("the harm guard") and its content (a mutable declaration) are
  inconsistent, and C1's void rule ("any pinned instrument byte differs") now reads as satisfied only
  if "instrument" is narrowed to the 15 non-plan lines. Fix: keep the declaration's digest in a
  separate file (or record the expected plan drift in the declaration), so the guard command still
  reads a clean pass at scoring time. Shown able to fail: `sha256sum -c` prints the FAILED line and
  the tools-only subset prints none. Note (after this lesson's measurement, 2026-11-08): the L1
  removed the `claims.json` and plan lines from the manifest in the working tree (16 → 14 entries),
  after which `sha256sum -c` reads 14/14 OK; the finding stands for the committed 16-line manifest
  at `7961738a`.
- **R100-ANCHOR-SEARCH-NOT-DISAMBIGUATED** — class: `corpus precision` (new; same class as
  R99-D3). The gate emits `limine_version` twice — BYTE **11230** (`CANNOT-EVALUATE`, line 200,
  16-space indent) and BYTE **16931** (final verdict, line 316, 12-space indent) — and the two
  occurrences are the *same* literal, so a naive `grep -abo`/`bytes.find` for
  `"limine_version": limine_version,` returns 11230 while the rows that cite 16931 mean the second
  one. Evidence: this seat's `receipts/32-gate-emission-two-occurrences.txt` and
  `receipts/35-gate-emission-context.txt` (indent widths and preceding lines of both sites). The
  bends' one-line diffs are at 16931 in each bend, so the claim is true; only a re-measurer is
  misdirected. Captured-by: QUALITY 141 again (unit, not multiplicity). Fix: name the site ("the
  final verdict return") beside the offset. Shown able to fail: `bytes.find` returns 11230 for the
  bare literal and the row means 16931.

## Routed

| item | treatment | evidence |
|---|---|---|
| R99-D2 stale LOG headings | **landed** — an append-only LOG correction entry quotes both superseded headings; no heading rewritten | `LOG.md:4365`; `receipts/33-r99-d2-log-entry.txt` |
| R99-D3 S395 anchor, one offset for two facts | **landed as a lesson note** — both offsets named (108455 `limine-version`, 108473 `visibility-era`), and the row's cited search is shown ambiguous (107815 also matches) | this lesson; `receipts/18-liekinds-disambiguation.txt`, `receipts/25-s395-cited-command-ambiguity.txt` |
| R99-D4 census exit code | **landed for exit codes, partial for output** — both commands and both exit codes are in the receipt; the output is still a 2-line tail of 59 lines | `before/census-before-after.txt`; `receipts/29-census-receipt-is-a-tail.txt` |
| R100-QUOTE-NOT-BYTE-LITERAL (new) | **open** — S397's Gate cell must print the byte-literal or name the markup split; a superseding row takes S399+ (ids are never reused) and the lesson's cell is corrected in place | `receipts/09-s397-quote-reproduction.txt`, `receipts/30-head-s397-s396-anchor-check.txt` |
| R100-S396-UNIT-PAIRING (new) | **open** — S396's anchor pairs BYTE 2615 (N12 clause start) with BYTE 3384 (N13 value start); the clause-start pair is 2615 / 3365; the row's `teaches` also says "exactly the family" where the X bend's measured set is two families. A superseding row must take S399+ | `receipts/14-n13-offset-detail.txt`, `receipts/10b-count-runs-summary.txt` |
| R100-MANIFEST-PINS-THE-DECLARATION (new) | **open** — separate the declaration's digest from the instrument manifest, or the harm guard reads a FAILED line at scoring time by design | `receipts/28-manifest-split.txt` |
| R100-CENSUS-RECEIPT-TAIL (new) | **open** — record all 59 lines or state the tail and the re-run determinism | `receipts/29-census-receipt-is-a-tail.txt` |
| R100-ANCHOR-SEARCH-NOT-DISAMBIGUATED (new) | **open** — name the site beside the offset wherever a search string occurs twice (gate emissions; `LIE_KINDS` members) | `receipts/32-gate-emission-two-occurrences.txt`, `receipts/25-s395-cited-command-ambiguity.txt` |
| owed `--selftest --reference` leg (r99 A6a) | **carried, unchanged** — this round's reading is `reference-gate skipped (no --reference)` and the tally `PASS 5/5` *excludes* that leg from the denominator, so it is neither passed nor failed here | `receipts/07-battery-selftest.txt` |
| C5 always-ok ancestor survivor's compound witness | **carried, unchanged** — the r99 compound M07 probe stands as filed | `corpus/README.md` Frontier (round-100 addition) |
| unbound registry rows and the three r98 C2 gaps | **carried, unchanged** | `corpus/README.md` Frontier (round-100 addition) |

## Frontier moved this round

- The round-99 sentence "The X/Y **echo** legs have no spelling-targeted committed bend" is
  **closed on the Y side** by a met→unmet flip (r98 control `met 105/105`, r99 `unmet 104/105`,
  exactly `REFUSAL-VERSIONS-9DIGIT-Y`, ×3) and **narrowed on the X side** to a one-family delta
  (r98 `unmet 104/105` on `EXPLICIT-VERSION-ECHO`, r99 `unmet 103/105` adding
  `REFUSAL-VERSIONS-9DIGIT`). A later claim that wants the X leg as a flip needs a spelling no other
  family sends.
- The round-99 sentence "the `unique` rule is fail-closed … the capture's alphabet is still
  `N<digits>` with no space token" is **closed**: six separator/union cells bind on r100 where r99
  reads a finding (four `RC-CELL-MISSING`, two `RC-VALUE-MISMATCH`), and the five forged classes plus
  the `GAP` control keep their readings.
- Still open, by name — and named only where a seat measured it:
  - the owed `--selftest --reference` leg (r99 A6a): this round's `PASS 5/5` **excludes** it, as the
    selftest's own line says `reference-gate skipped`;
  - the C2 join grammar is **wider than the "joined only by" sentence**: an empty token is skipped,
    so `VARIANTS and N01-N03`, `VARIANTS N01-N03 and` and `VARIANTS N01; ; N02; N03` read `PASS`
    (measured, `receipts/20-a3-empty-token-probe.txt`), while a prose connector still reads
    `RC-CELL-MISSING`;
  - the C1 "exactly when" is **main-return-only**: the gate's early `CANNOT-EVALUATE` return also
    emits `limine_version` (BYTE 11230) and is untouched, so a cap spelling on an unreadable conf is
    not falsified (measured, `receipts/21-a1-a2-probe.txt`);
  - the blanket echo lie is not attributable (it moves every echo-reading family at once);
  - the unbound registry rows and the three r98 C2 gaps (uncovered cells, tool+cell co-doctoring,
    printed-tally parsing);
  - the r96 launcher residuals, the r93 probe pre-release caveat, and the r89 blank/ESP/empty-label
    classes;
  - the new evidence-structure items this lesson routes: S397's quote form, S396's silent
    unit-pairing, the declaration pinned inside the instrument manifest, the census tail, and anchors
    whose search string occurs twice.
- Note on the seat brief: the brief names a "coin-flip class", but the phrase has **no referent in
  this lane's own corpus** — `grep -rniE '\bcoin[ -]?flip'` over `corpus/`, `.ufo/plans/` and
  `claims.json` returns **0** hits (`receipts/15-coinflip-and-landed-lesson-gate.txt`); the phrase
  occurs only in the round-100 wave spec/dispatch files. The Frontier paragraph above therefore names
  the lane's carried limits, not the brief's phrase.
