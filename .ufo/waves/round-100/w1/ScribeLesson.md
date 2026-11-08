# ScribeLesson — round 100, wave w1 — scoped findings

Seat: `ScribeLesson` (scribe; leaf member — no subagent dispatch). Lane root
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, git HEAD detached; **no mutating git or jj
command was run** (read-only `git show`, `git log`, `git diff`, `git status`, `git rev-parse`,
`git archive` only; `git archive` extracted into my own scratch). No git commit was made anywhere.
Nothing under `tools/`, `SKILL.md`, `corpus/`, `SCORECARD.md`, `LOG.md`, `.ufo/plans/`,
`.ufo/waves/round-100/before/`, `claims.json` or any sibling lane was written. Scratch
`/fast/scratch/hyaku/tsukuroi-r100/ScribeLesson` was removed before this file was written; nothing
under `/tmp` is cited. No tool was installed or upgraded (only `python3`, `curl`, `sha256sum`,
`diff`, `grep` from the base system); `pacman` was not invoked (host-wide pause) and `sudo` was
never used.

Files written (this seat only, all under `.ufo/waves/round-100/w1/ScribeLesson/`):

| artifact | path | what it is |
|---|---|---|
| the lesson draft | `ScribeLesson/lesson-draft.md` | `## Gate` (14 candidate rows + census), `## Mistakes` (11 rows, each with an evidence pointer and a `captured-by`), `## Routed` (10 rows), `## Frontier moved this round` |
| this report | `ScribeLesson.md` | scoped findings, commands, raw output, PASS/FAIL per expected line |
| command/receipt log | `ScribeLesson/report.md` | the same measurements in the binding-rule `report.md` shape, with the final JSON line |
| receipts | `ScribeLesson/receipts/` (39 files) | every number below, written by this seat |

## 0. Harm guard and instrument identity

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
$ sha256sum -c .ufo/waves/round-100/before/instruments.sha256
.ufo/plans/round-100.md: FAILED
sha256sum: WARNING: 1 computed checksum(s) did NOT match
OK count: 15
```

The manifest has **16** lines. At the tip I measured (`7961738a`) **15 read `OK` and the single
`FAILED` line is `.ufo/plans/round-100.md`** — pinned `44ae97d8…`, now `b7b163ea…` — because the
plan's own amendment slot invited post-freeze writes (plan amendments A1 … A2-A7). The 14
instrument/control/fixture/claims bytes (everything except the plan and `claims.json`) verify
`14/14 OK` from a tools-only subset of the manifest. **No instrument byte has moved**: the gate is
`7d79ac29…`, the r99 battery `c2e8c8fc…`, the r98 battery `8198bd84…`, the r99 checker
`b489f5b8…`, the r100 checker `7a23a522…`, the generator `7ccfe69e…`, both bends `eb247e16…` /
`e1e5916f…`.
Receipt: `ScribeLesson/receipts/28-manifest-split.txt`.

This drift is a **finding, not a void**: C1's void rule names "any pinned *instrument* byte", and the
declaration is not an instrument. It is reported as `R100-MANIFEST-PINS-THE-DECLARATION` because the
harm-guard command printed a FAILED line by design.

**Observed after that measurement (adapting to the L1's own repair, not mine):** the L1 has since
edited the manifest in the working tree (`git diff -- .ufo/waves/round-100/before/instruments.sha256`
removes the `claims.json` and `.ufo/plans/round-100.md` lines, 16 → 14 entries), and
`sha256sum -c` on the working-tree manifest now prints **14/14 `OK`, rc 0, no FAILED line**. My
measured reading above is stated against the committed 16-line manifest at `7961738a`; the repair
resolves the finding for the working tree only and is the L1's edit, not this seat's.

## 1. What this seat re-derived (every number, not trusted from the brief or from a sibling)

### 1.1 C1 — the two bends against the r99 battery and the r98 control

Command per leg (`--runs 3`, own work dir, own JSON):

```
$ python3 tools/limine-pin-battery-r99.py --gate <ARTICLE> --runs 3 --work <scratch>/work-<leg> --json <scratch>/<leg>.json
$ python3 tools/limine-pin-battery-r98.py --gate <ARTICLE> --runs 3 --work <scratch>/work-<leg> --json <scratch>/<leg>.json
$ python3 .ufo/waves/round-95/before/controls/count-runs.py <leg>.json \
    --family REFUSAL-VERSIONS-9DIGIT --family REFUSAL-VERSIONS-9DIGIT-Y --family EXPLICIT-VERSION-ECHO
```

| leg | article | runs | verdict | failed_families (exact) | cases | error rows | named X / Y / E |
|---|---|---|---|---|---|---|---|
| landed gate | `tools/check-limine-pins.py` `7d79ac29…` | 3 | `met 105/105` | `[]` | 420 | 0 | 4/0 · 4/0 · 4/0 |
| N12, r99 | `…/bends/N12-x-echo.py` | 3 | `unmet 103/105` | `[EXPLICIT-VERSION-ECHO, REFUSAL-VERSIONS-9DIGIT]` | 420 | 0 | **0/4** · 4/0 · **3/4** |
| N13, r99 | `…/bends/N13-y-echo.py` | 3 | `unmet 104/105` | `[REFUSAL-VERSIONS-9DIGIT-Y]` | 420 | 0 | 4/0 · **0/4** · 4/0 |
| N12, r98 control | `…/bends/N12-x-echo.py` | 3 | `unmet 104/105` | `[EXPLICIT-VERSION-ECHO]` | 420 | 0 | 4/0 · 4/0 · **3/4** |
| N13, r98 control | `…/bends/N13-y-echo.py` | 3 | `met 105/105` | `[]` | 420 | 0 | 4/0 · 4/0 · 4/0 |

Every run of a leg is identical; the failed-family **order** varies between runs in the JSON array
(the instrument emits a set), and the set is compared as a set. Raw: `receipts/10-count-runs.txt`
(full `count-runs.py` payloads) and `receipts/10b-count-runs-summary.txt` (one line per run).

**PASS/FAIL against C1's frozen target:** landed gate `105/105 met []` 0 errors ×3 → **PASS**;
N13 `unmet 104/105` exactly `[REFUSAL-VERSIONS-9DIGIT-Y]` ×3 → **PASS**; N12 `unmet 103/105` exactly
`[EXPLICIT-VERSION-ECHO, REFUSAL-VERSIONS-9DIGIT]` ×3 → **PASS**; r98 N13 `met 105/105` ×3 → **PASS**;
r98 N12 `unmet 104/105` exactly `[EXPLICIT-VERSION-ECHO]` ×3 → **PASS**; battery `--selftest`
without `--reference` `PASS 5/5` → **PASS** (see the note below).

Bend diffs (`diff -u tools/check-limine-pins.py <bend>`): each is **one hunk, one removed + one
added line** (2 non-header `+`/`-` lines), and the changed clause sits at BYTE **16931** in each
emitted bend — the gate's *final verdict* return. Receipts `receipts/05-bend-diffs.txt`,
`receipts/05-diff-N12-x-echo.txt`, `receipts/05-diff-N13-y-echo.txt`, `receipts/14-n13-offset-detail.txt`.

Battery selftest (raw):

```
reference-gate      skipped (no --reference)
roster-literal     PASS families_passed=105
absent             PASS families_passed=0
constant-healthy   PASS families_passed=0
non-json           PASS families_passed=0
constant-degraded  PASS families_passed=0
selftest PASS 5/5
```

Reading note, measured not assumed: the `reference-gate` leg is printed but **excluded from the
denominator**, so `PASS 5/5` is 5 of the 5 non-reference checks and says nothing about the owed
`--selftest --reference` leg. Receipt `receipts/07-battery-selftest.txt`.

### 1.2 C2 — live table, selftests, twelve fixture cells

```
$ python3 tools/check-registry-content-r100.py --revision <REV>
$ python3 tools/check-registry-content-r99.py  --revision <REV>
$ python3 tools/check-registry-content-r100.py --selftest
$ python3 tools/check-registry-content-r99.py  --selftest
```

| revision | r100 | r99 |
|---|---|---|
| `ce73ccaf` (pre-round tip) | `PASS bindings 7/7 findings 0` | `PASS 7/7` |
| `743ce449` (freeze) | `PASS 7/7` | `PASS 7/7` |
| `c450cd68` (first landing commit) | `CANNOT-EVALUATE: malformed registry row at line 5951` | same |
| `69474c55` (land fix) | `PASS 7/7` | `PASS 7/7` |
| `7961738a` (tip measured here) | `PASS 7/7` | `PASS 7/7` |

Selftests at the tip: `selftest PASS 26/26` (rc 0) and `selftest PASS 17/17` (rc 0). Receipts
`receipts/06-selftests.txt`, `receipts/11-live-table-and-coverage.txt`,
`receipts/34-final-head-readings.txt`.

Twelve fixture cells, rebuilt by the frozen builder (`.ufo/waves/round-100/before/dev/make-fixtures.py`,
which calls the checker's own `build_fixture`) and then read by both checkers with `--root`:

| tag | r100 rc/status/finding | r99 rc/status/finding | frozen expectation |
|---|---|---|---|
| SEP-SPACE | 0 PASS — | 1 FAIL RC-CELL-MISSING | PASS / CELL-MISSING → **PASS** |
| SEP-SEMICOLON | 0 PASS — | 1 FAIL RC-CELL-MISSING | PASS / CELL-MISSING → **PASS** |
| SEP-PLUS | 0 PASS — | 1 FAIL RC-CELL-MISSING | PASS / CELL-MISSING → **PASS** |
| SEP-SLASH | 0 PASS — | 1 FAIL RC-CELL-MISSING | PASS / CELL-MISSING → **PASS** |
| SEP-AND | 0 PASS — | 1 FAIL RC-VALUE-MISMATCH | PASS / VALUE-MISMATCH → **PASS** |
| UNION | 0 PASS — | 1 FAIL RC-VALUE-MISMATCH | PASS / VALUE-MISMATCH → **PASS** |
| LETTER | 1 FAIL RC-CELL-MISSING | 1 FAIL RC-CELL-MISSING | CELL-MISSING → **PASS** |
| PROSE | 1 FAIL RC-CELL-MISSING | 1 FAIL RC-CELL-MISSING | CELL-MISSING → **PASS** |
| UNION-LIE | 1 FAIL RC-VALUE-MISMATCH | 1 FAIL RC-VALUE-MISMATCH | VALUE-MISMATCH → **PASS** |
| HYBRID | 1 FAIL **RC-VALUE-MISMATCH** | 1 FAIL RC-CELL-MISSING | VALUE-MISMATCH → **PASS** (moved, "unchanged or sharper") |
| RESTATED | 1 FAIL RC-CELL-AMBIGUOUS | 1 FAIL RC-CELL-AMBIGUOUS | AMBIGUOUS → **PASS** |
| GAP | 0 PASS — | 0 PASS — | PASS on both → **PASS** |

This reproduces the frozen dev table `.ufo/waves/round-100/before/dev/c2-fixtures.txt` cell for cell,
including HYBRID's move from `RC-CELL-MISSING` (r99) to `RC-VALUE-MISMATCH` (r100). Receipt
`receipts/02-c2-fixture-cells.tsv`; fixture paths `receipts/01-fixture-paths.txt`.

**PASS/FAIL against C2's frozen target:** live table PASS 7/7 findings 0 at both named surfaces
(`743ce449`, final tip) → **PASS**; six acceptance cells PASS on r100 with a finding on r99 →
**PASS**; five fail-closed cells keep their frozen ids and `GAP` passes on both → **PASS**;
`--selftest` 26/26 and the r99 control 17/17 → **PASS**.

### 1.3 The registry coverage gate, reported as found

```
$ python3 tools/check-registry-coverage.py --revision 743ce449490f4e9ff004f423ecc3fa456cbc77ec
{"counts":{"findings":2,"missing":2,"registered":163,"rows_total":163,"tools_total":165},
 "findings":[{"id":"REGISTRY-ROW-MISSING","site":"tools/check-registry-content-r100.py"},
             {"id":"REGISTRY-ROW-MISSING","site":"tools/make-r100-bends.py"}],"status":"FAIL"}  rc=1
$ … --revision c450cd68a18a666f7bc835bcb2e8d76119f8aff6
{"counts":{"findings":1,…},"findings":[{"detail":"malformed registry row at line 5951","id":"E-REGISTRY-TABLE"}],
 "status":"CANNOT_EVALUATE"}                                                                    rc=2
$ … --revision ce73ccaf75d0279385977f03ccb35945c1cf8e07
{"counts":{"findings":0,"missing":0,"registered":163,"rows_total":163,"tools_total":163},"status":"PASS"}  rc=0
$ … --revision 69474c55eb38632f3e740923b58029dc43e01300
{"counts":{"findings":0,"missing":0,"registered":165,"rows_total":165,"tools_total":165},"status":"PASS"}  rc=0
$ … --revision 7961738a4954f177e846e8bae34576ab71dc9833
{"counts":{"findings":0,"missing":0,"registered":165,"rows_total":165,"tools_total":165},"status":"PASS"}  rc=0
```

Receipts `receipts/16-coverage-at-freeze.txt`, `receipts/17-coverage-land-vs-master.txt`,
`receipts/11-live-table-and-coverage.txt`, `receipts/34-final-head-readings.txt`. **PASS at the final
tip, as required by the harm guard; FAIL (2 rows missing) at the freeze revision, CANNOT_EVALUATE at
the intermediate landing commit — both reported raw, not smoothed over.**

## 2. Findings (routed to the lesson draft and to the L1)

1. **S397's located quote is not byte-literal** (both before and after its correction). `bytes.find`
   of `If the whole string matches the regular expression pattern, return a corresponding Match`
   and of the earlier `… match object` returns **-1** on the pinned 257722-byte page; only
   `If the whole <em>string</em> matches the regular expression <em>pattern</em>, return a`
   reproduces at BYTE **112171**. `id="re.fullmatch"` at 111489 and the `\b` sentence at 69787 do
   reproduce byte-exactly. Receipts `09`, `24`, `30`.
2. **S396's anchor pairs two different units, silently**: BYTE 2615 is the N12 *clause* start and
   BYTE 3384 is the N13 *value* start; the N13 clause start is **3365**. Secondarily, S396's
   `teaches` cell says "exactly the family" (singular) while the X bend's measured failed set is two
   families. Receipts `14`, `10b`.
3. **The gate emits `limine_version` twice** (BYTE 11230, line 200, 16-space indent — the
   `CANNOT-EVALUATE` return; BYTE 16931, line 316, 12-space indent — the final verdict return), so a
   naive re-measure of the string lands on 11230 while the rows mean 16931. The bends change 16931
   only, and the early return echoes the **true** value (measured: `N12 --conf <absent>
   --limine-version 999999999.9.9` prints `999999999.9.9`). Receipts `32`, `35`, `21`.
4. **The harm-guard manifest pins the declaration file** whose amendment slot invites post-freeze
   writes: `sha256sum -c` now reads 15 OK / 1 FAILED (the plan), while all 14
   instrument/control/fixture/claims bytes read OK. Receipt `28`.
5. **The census receipt records a tail, not an output**: the frozen command prints 59 lines
   (57 `W04` + 1 `W01` + `ok`), the receipt's before block keeps the last two and the after block the
   last one. Both exit codes and both row counts (395 → 398) *are* recorded, so R99-D4's exit-code
   half landed and its output half did not. The command is deterministic (two runs md5-identical,
   `37ed43e2…`), and a run against an isolated root containing only tsukuroi's `SOURCES.md` still
   prints 57 `W04` lines, so the warning set is file-local. Receipts `23`, `29`, `22`, `27`.
6. **The seat brief's "coin-flip class" has no referent in the lane**: `grep -rniE '\bcoin[ -]?flip'`
   over `corpus/`, `.ufo/plans/` and `claims.json` returns **0** hits; the phrase occurs only in the
   round-100 wave spec/dispatch. The lesson's Frontier names the lane's own carried limits instead.
   Receipt `15`.
7. **The C2 join grammar is wider than the frozen wording** (plan amendment A6, independently
   reproduced here): empty tokens are skipped, so `VARIANTS and N01-N03`, `VARIANTS N01-N03 and`
   and `VARIANTS N01; ; N02; N03` all read `PASS` (rc 0), while `VARIANTS N01 through N03` reads
   `RC-CELL-MISSING` (rc 1). Receipt `20`.
8. **R99-D3's cited command is ambiguous**: `grep -abo '"limine-version"'` on the battery returns
   **107815 first** (the lie-application dict key) and 108455 second (the `LIE_KINDS` member); the
   disambiguated search `'"limine-version", "visibility-era")'` is a single hit at 108455, and
   `"visibility-era"` likewise first occurs at 107920 with the member at 108473. So the lesson's
   claim is true but its pointer misdirects a re-measurer. Receipts `18`, `19`, `25`.

## 3. PASS/FAIL per expected line (the brief's "MEASURED SO FAR" list, re-derived)

| expected (brief) | this seat's reading | verdict |
|---|---|---|
| landed gate `105/105 met` one run | `met 105/105`, `[]`, 0 error rows, ×3 | PASS |
| r99 on N12 `103/105 [EXPLICIT-VERSION-ECHO, REFUSAL-VERSIONS-9DIGIT]` | exactly, ×3 | PASS |
| r99 on N13 `104/105 [REFUSAL-VERSIONS-9DIGIT-Y]` | exactly, ×3 | PASS |
| r98 on N12 `104/105 [EXPLICIT-VERSION-ECHO]` | exactly, ×3 | PASS |
| r98 on N13 `105/105 met` | exactly, ×3 | PASS |
| r100 checker `--selftest PASS 26/26`, r99 `17/17` | 26/26 rc 0; 17/17 rc 0 | PASS |
| live table `PASS 7/7` for both at `ce73ccaf` | both `PASS 7/7 findings 0` | PASS |
| twelve fixture readings in `before/dev/c2-fixtures.txt` | reproduced cell for cell | PASS |
| instrument manifest clean | 15 OK / 1 FAILED (the plan) — see §0 | **FINDING** |
| registry coverage gate keeps PASS after the landing rows | PASS 165/165 at `69474c55` and `7961738a`; FAIL 2-missing at `743ce449`; CANNOT_EVALUATE at `c450cd68` | PASS at the landing tip, as required |

## 4. Lesson draft

`ScribeLesson/lesson-draft.md` carries the three required sections plus the frontier paragraph, one
Gate row per candidate (14: the two new tools, the three SOURCES rows, the knowledge entry, the two
bend controls, the six acceptance cells, the five fail-closed cells, the positive control — with the
acceptance/fail-closed/positive rows grouped as the brief groups them), 11 mistake rows each with an
evidence pointer and a `captured-by` (4 new this round, 4 carried from the round's own record, 3
carried from round 99), and a Routed table of 10 rows. The spot-check line reads
`pending non-author closure`. No seat name, receipt or number in it is unmeasured by this seat
except where a row says in terms which artifact it points at (the quarantined clone runs, which
exist under `.ufo/waves/round-100/after/c1/harness-fault/`).

## 5. Honest scope statement

- Not measured by this seat: any clone-layout battery run (two layouts are executor/reviewer
  surfaces); the generator's own re-emission identity test (the tool writes into the frozen wave
  directory, so the test belongs to a seat with a scratch copy); the `--selftest --reference` leg
  (owed); the C5 compound-witness probe; the twelve fixtures' JSON beyond `status`/`findings`/`rc`.
- The four off-roster/counterexample shapes a reviewer built are not re-run here; the lesson cites
  them only through the round's own records and names them as such.
- One scratch path was used
  (`/fast/scratch/hyaku/tsukuroi-r100/ScribeLesson`) and it was removed; the removal asserted the
  path ends in `/ScribeLesson` before running.

```json
{"seat":"ScribeLesson","verdict":"findings","notes":"Lesson drafted at .ufo/waves/round-100/w1/ScribeLesson/lesson-draft.md (Gate 14 candidate rows + census, 11 mistake rows with evidence pointers and captured-by, Routed 10 rows, Frontier paragraph). Re-derived by this seat: gate met 105/105 x3; N12 r99 103/105 [EXPLICIT-VERSION-ECHO, REFUSAL-VERSIONS-9DIGIT] x3; N13 r99 104/105 [REFUSAL-VERSIONS-9DIGIT-Y] x3; r98 control N12 104/105 [EXPLICIT-VERSION-ECHO], N13 105/105, all 0 error rows; one-line bend diffs; battery selftest 5/5 with the reference leg excluded from the denominator; r100 selftest 26/26 and r99 17/17; live table PASS 7/7 at ce73ccaf/743ce449/69474c55/7961738a and CANNOT_EVALUATE at c450cd68; twelve fixture cells reproduce the frozen dev table exactly incl. HYBRID's CELL-MISSING->VALUE-MISMATCH move; coverage PASS 165/165 at the landing tip, FAIL 2-missing at the freeze, CANNOT_EVALUATE at c450cd68. Findings: (1) S397's Gate quote is not byte-literal - bytes.find of both de-marked-up variants returns -1 while the marked-up form reproduces at 112171; (2) S396 pairs the N12 clause start 2615 with the N13 value start 3384 (clause start 3365) and its teaches says one family where X moves two; (3) the gate emits limine_version twice (11230 early / 16931 main) so a naive re-measure lands on the wrong one, and the early return echoes truth; (4) instruments.sha256 pins .ufo/plans/round-100.md, so the harm guard now reads 15 OK + 1 FAILED by design while all 14 instrument bytes are OK; (5) the census receipt keeps a tail of a 59-line output (both exit codes and both row counts are recorded, so R99-D4's exit-code half landed and its output half did not); (6) the brief's coin-flip class has no referent in the lane (0 hits in corpus/plans/claims); (7) empty-token leniency reproduced (3 cells PASS, prose connector still CELL-MISSING); (8) R99-D3's cited grep is ambiguous (107815 matches first). No instrument, corpus, record or frozen byte was written by this seat; scratch removed; no tool installed."}
```
