# ScoutFrontier — the round-100 limit-closure ledger

Seat: `ScoutFrontier` (scout, leaf member — no subagent dispatch). Lane
`tsukuroi-shokunin`, branch `master`, git HEAD detached; **no mutating git/jj command was run**
(`git clone --shared`, `git show`, `git rev-parse`, `git cat-file -e`, `git diff`, `git status`
only). Scratch: `/fast/scratch/hyaku/tsukuroi-r100/ScoutFrontier` (own clone + own work dirs;
deleted before this report was written).

All receipts cited here were written by this seat and live under
`.ufo/waves/round-100/w1/ScoutFrontier/receipts/`. Nothing was written outside that seat dir.
The L1's numbers were re-derived, not trusted.

Target: does round 100 actually close the sentences the round-99 Frontier names, and do the
carried items land or stay owed?

## 0. Instrument integrity (re-derived first, so no measurement below is void)

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
$ sha256sum -c .ufo/waves/round-100/before/instruments.sha256
... 16 files OK ...            rc=0
```
Receipt: `receipts/13-no-work-control.txt` (16 `: OK` lines, rc 0). **PASS** — every pinned
instrument byte-identical; the kill rule ("void if any pinned instrument byte differs") does not
fire.

## 1. The two frontier sentences, quoted at the pre-round tip

`git show ce73ccaf:corpus/README.md | grep -n` (receipt `receipts/10-frontier-sentences.txt`):

```
1274:- The X/Y **echo** legs have no spelling-targeted committed bend: N09/N11 falsify `visibility_era`
1275:  only. The blanket `lie-limine-version` wrapper covers them, and it proves the battery sees the
1276:  field, not that a named family asserts it.
1281:- The `unique` rule is fail-closed: a registry cell that legitimately states two spans in one cell
1282:  must be rewritten to one span; the capture's alphabet is still `N<digits>` with no space token.
```

### 1a. Sentence 1 — "The X/Y **echo** legs have no spelling-targeted committed bend"

| field | value |
|---|---|
| closed by | **C1** — `tools/make-r100-bends.py` (`7ccfe69e…`) emits `N12-x-echo` (first component `999999999`) and `N13-y-echo` (second component `999999999`); the unchanged r99 battery (`c2e8c8fc…`) asserts the echo field at byte `99430` (`if c.check_echo and not (got[8] == c.version and got[9] == "flag")`) |
| instrument leg that carries it | the r99 battery's `meta_ok` echo assertion, exercised per family; the five `c.check_echo = True` sites at bytes `79015/79893/81666/83173/84390` (X-cap `REFUSAL-VERSIONS-9DIGIT` at `79015`, Y-cap `REFUSAL-VERSIONS-9DIGIT-Y` at `81666`) |
| wave receipt that would prove it | `.ufo/waves/round-100/w1/ExecBends/receipts/c1-bend-N12-x-echo-canonical.json` / `c1-bend-N13-y-echo-canonical.json` (+ `count-N12-canonical.json`, `count-N13-canonical.json`, `diff-N12-x-echo.txt`, `diff-N13-y-echo.txt`, `one-clause-check.txt`); the L1's `.ufo/waves/round-100/after/c1/` matrix |
| **verdict** | **landed — partially.** The Y leg is a genuine met→unmet closure; the X leg is a **one-family delta, never a flip** (the r96 `EXPLICIT-VERSION-ECHO` family sends the same `999999999.9.9` spelling). The round states this itself in `corpus/README.md` § "Round 100" ("The X echo leg is a **delta**, never a flip") and in `corpus/lessons/round-100.md` mistake `R100-X-DELTA-COUNTED-AS-FLIP`. The sentence "no spelling-targeted committed bend exists" is therefore **closed on the Y side and narrowed (not closed) on the X side** |

### 1b. Sentence 2 — "the `unique` rule is fail-closed … the capture's alphabet is still `N<digits>` with no space token"

| field | value |
|---|---|
| closed by | **C2** — `tools/check-registry-content-r100.py` (`7a23a522…`) binds `RC-BEND-SPAN` as a **label set**: `parse_label_set` at byte `12134`, `TOKEN` at `12025`, `SEPARATORS` at `12073`; the unchanged r99 checker (`b489f5b8…`) is the do-nothing control |
| instrument leg that carries it | the r100 `RC-BEND-SPAN` capture: tokens `N<digits>` / `N<digits>-N<digits>` (range expanded) joined only by `,` whitespace `;` `+` `/` `and`; declared set must equal the set of the tool's `VARIANTS` keys |
| wave receipt that would prove it | `.ufo/waves/round-100/w1/ExecRegistry/receipts/08-fixture-cells-and-variants.txt`, `05-selftest-r100.txt`, `06-selftest-r99.txt`, `01–04-live-*.txt`; `.ufo/waves/round-100/after/c2/content-tip.json` + `content-tip-r99.json` |
| **verdict** | **landed.** Six separator/union cells bind on r100 where r99 finds (`SEP-SPACE`, `SEP-SEMICOLON`, `SEP-PLUS`, `SEP-SLASH` → r99 `RC-CELL-MISSING`; `SEP-AND`, `UNION` → r99 `RC-VALUE-MISMATCH`); five forged shapes stay closed (`LETTER`/`PROSE` → `RC-CELL-MISSING`, `UNION-LIE`/`HYBRID` → `RC-VALUE-MISMATCH`, `RESTATED` → `RC-CELL-AMBIGUOUS`); `GAP` PASS on both |

My own re-derivation of the twelve fixture cells (fixtures rebuilt by the committed
`.ufo/waves/round-100/before/dev/make-fixtures.py`, receipts `receipts/fixture-cells.txt`,
`receipts/fixture-cells-ids.txt`, `receipts/fx-{r100,r99}-*.json`):

```
SEP-SPACE     r100: PASS []            r99: FAIL ['RC-CELL-MISSING']
SEP-SEMICOLON r100: PASS []            r99: FAIL ['RC-CELL-MISSING']
SEP-PLUS      r100: PASS []            r99: FAIL ['RC-CELL-MISSING']
SEP-SLASH     r100: PASS []            r99: FAIL ['RC-CELL-MISSING']
SEP-AND       r100: PASS []            r99: FAIL ['RC-VALUE-MISMATCH']
UNION         r100: PASS []            r99: FAIL ['RC-VALUE-MISMATCH']
LETTER        r100: FAIL ['RC-CELL-MISSING']      r99: FAIL ['RC-CELL-MISSING']
PROSE         r100: FAIL ['RC-CELL-MISSING']      r99: FAIL ['RC-CELL-MISSING']
UNION-LIE     r100: FAIL ['RC-VALUE-MISMATCH']    r99: FAIL ['RC-VALUE-MISMATCH']
HYBRID        r100: FAIL ['RC-VALUE-MISMATCH']    r99: FAIL ['RC-CELL-MISSING']
RESTATED      r100: FAIL ['RC-CELL-AMBIGUOUS']   r99: FAIL ['RC-CELL-AMBIGUOUS']
GAP           r100: PASS []            r99: PASS []
```
Every frozen clause of C2's target re-derives literally. Note the one *intended* difference:
`HYBRID` reads `RC-CELL-MISSING` on r99 and `RC-VALUE-MISMATCH` on r100 — the frozen target names
`RC-VALUE-MISMATCH` for r100, so this is the sharper reading, not a discrepancy.

Live table, both checkers, at the freeze tip and at the landing tip (my runs):

```
$ python3 tools/check-registry-content-r100.py --revision 743ce449   -> PASS bindings 7/7 findings 0
$ python3 tools/check-registry-content-r100.py --revision ce73ccaf   -> PASS bindings 7/7 findings 0
$ python3 tools/check-registry-content-r99.py  --revision 743ce449   -> PASS bindings 7/7 findings 0
$ python3 tools/check-registry-content-r99.py  --revision ce73ccaf   -> PASS bindings 7/7 findings 0
$ python3 tools/check-registry-content-r100.py --selftest            -> selftest PASS 26/26  rc=0
$ python3 tools/check-registry-content-r99.py  --selftest            -> selftest PASS 17/17  rc=0
```

## 2. My own re-derivation of the C1 matrix (both layouts)

Receipts: `receipts/15-c1-matrix-mine.txt`, `receipts/r99-on-*.json`, `receipts/r98-on-*.json`,
`receipts/clone-*.json`. Runs: `python3 tools/limine-pin-battery-r{99,98}.py --gate <ARTICLE> --runs 1
--work <scratch> --json <out>`, articles = the committed frozen bend controls
`.ufo/waves/round-100/before/controls/bends/{N12-x-echo,N13-y-echo}.py` (never a generator run).

```
canonical layout                          clone layout (own clone at 60b5636f)
landed gate   met 105/105 []            0 err   (clone: met 105/105 [] — see L1's after/c1/gate-clone.json)
r99 on N12    unmet 103/105             0 err   clone: unmet 103/105 [EXPLICIT-VERSION-ECHO, REFUSAL-VERSIONS-9DIGIT] 0 err
r99 on N13    unmet 104/105             0 err   clone: unmet 104/105 [REFUSAL-VERSIONS-9DIGIT-Y] 0 err
r98 on N12    unmet 104/105             0 err   clone: unmet 104/105 [EXPLICIT-VERSION-ECHO] 0 err
r98 on N13    met 105/105 []            0 err   clone: met 105/105 [] 0 err
```
420 cases per run, 0 error rows everywhere. Bend diffs are exactly one changed line each
(`diff -u tools/check-limine-pins.py <bend>.py` → 1 hunk, −1/+1; receipt
`receipts/12-freeze-diff-evidence.txt` context and the frozen
`.ufo/waves/round-100/before/controls/bends/*` files).

Battery selftest **without** `--reference` (my run, `receipts/battery-selftest-noref.txt`):
`selftest PASS 5/5`, and the receipt's first line is literally
`reference-gate      skipped (no --reference)` — the owed reference leg is *not* silently claimed.

**Harness fault found in the L1's clone-layout legs (not an instrument defect).** The L1's first
clone receipts (`after/c1/*-clone.json` before the re-run) read `0/105` with all 105 families in
`failed_families` and every case row `error: "gate absent"` — the gate path had been built by
prefixing the clone root onto the *absolute lane path* (`$CLONE/home/vgpnk/Projects/...`), which
does not exist inside the clone. The L1 quarantined those four files under
`after/c1/harness-fault/` and re-ran them with the clone-relative path; the re-run receipts read
the frozen sets (`bend-N12-x-echo-clone.json` 103/105, `bend-N13-y-echo-clone.json` 104/105,
`control-N12-x-echo-clone.json` 104/105, `gate-clone.json` 105/105). My independent clone-layout
re-runs (`receipts/clone-*.json`) reproduce the same four readings, so the instrument is fine and
the first clone batch was a path defect. This is now captured as lesson `R100-CLONE-PATH-PREFIX`
+ QUALITY 142 in the lane's in-flight corpus edits (uncommitted at the time of this reading).

## 3. The round-99 spot-check's routed items (R99-D2/D3/D4)

Source: `corpus/lessons/round-99-verifier-spotcheck.md` §7.

| id | what the spot-check required | pointer | verdict |
|---|---|---|---|
| **R99-D2** | LOG.md round-99 headings still read `(pending)`/`(pending-settle)` — append a correction entry naming the superseded headings (never rewrite) | `LOG.md:4304` `## Round 99 — freeze (\`pending\`)` and `LOG.md:4339` `## Round 99 — measured (\`pending-settle\`)` are **still present, unchanged**; the correction is the append-only entry `LOG.md:4365` `## Round 100 — routed correction R99-D2 (append-only; supersedes two round-99 heading status labels)`, committed at `c450cd68` (`git show c450cd68:LOG.md | grep -c "routed correction R99-D2"` → 1) | **landed** |
| **R99-D3** | S395's anchor names one byte offset for two `LIE_KINDS` members — 108455 = `limine-version`, 108473 = `visibility-era`; a narrow correction may land as a superseding row **or a lesson note** | lesson note `corpus/lessons/round-100.md` mistake `R99-ONE-ANCHOR-TWO-MEMBERS` names **both** offsets (committed, `c450cd68`); the S395 row itself is *not* rewritten (append-only) | **landed** (as the lesson note the spot-check allows) |
| **R99-D4** | record the census **BEFORE** command's exit code, not only the AFTER's | `.ufo/waves/round-100/before/census-before-after.txt` — the BEFORE block now carries `exit=0` after both its commands (the `sources-census.sh validate` line and the `grep -cE` line), and the AFTER block likewise | **landed** |

### 3a. R99-D3's byte offsets, measured at the byte level

The spot-check's claim (108455 = `limine-version`, 108473 = `visibility-era`) is **confirmed** on
the pinned bytes at `ce73ccaf:tools/limine-pin-battery-r99.py` (receipt
`receipts/11-lie-kinds-offsets.txt`):

```
$ git show ce73ccaf:tools/limine-pin-battery-r99.py | grep -abo '"limine-version"'
107815:"limine-version"
108455:"limine-version"
$ git show ce73ccaf:tools/limine-pin-battery-r99.py | grep -abo '"visibility-era"'
107920:"visibility-era"
108473:"visibility-era"
$ git show ce73ccaf:tools/limine-pin-battery-r99.py | grep -abo 'LIE_KINDS'
108277:LIE_KINDS
110431:LIE_KINDS
```
`bytes.find` on the same pinned bytes gives the same numbers; `LIE_KINDS = (` opens at byte
`108277` (line 2369), and the **two new members sit on line 2370** at bytes **108455**
(`"limine-version"`) and **108473** (`"visibility-era"`). The earlier pair (107815 / 107920) is
the `LIE_KINDS` *handler* (`elif KIND == "limine-version":`), not the tuple member — so the
one-offset-for-two-members confusion in the S395 anchor is fully explained, and the lesson note's
two offsets are the right ones. (QUALITY 141: byte-level `grep -abo`/`bytes.find` throughout, no
decoded-string index anywhere.)

## 4. Carried items the plan names — does round 100 touch each?

Plan pointer: `.ufo/plans/round-100.md` § "Limits (named, not claimed)" (lines 96–105).

| carried item | touched by round 100? | pointer | verdict |
|---|---|---|---|
| **owed `--selftest --reference` leg** (r99 A6a/A7) | **No.** The battery's reference leg was not exercised; my own `--selftest` receipt's first line reads `reference-gate      skipped (no --reference)`, and the L1's `.ufo/waves/round-100/after/c1/selftest.txt` reads the same | `corpus/lessons/round-100.md` § Routed ("carried, unchanged — not run this round"); `corpus/README.md:1305` ("The selftest `--reference` leg … stays owed from r99 (A6a)"); `.ufo/waves/round-100/after/c1/selftest.txt` | **owed (carried, not closed)** |
| **C5 always-ok ancestor survivor's compound witness** | **No.** The r100 checker *keeps* the `ancestor` case (selftest `ancestor PASS`, 26/26) and the M8 mutant that skips the ancestor refusal is **killed** — but that is the r99 M07 branch re-probed on the successor, not a fresh compound witness for the always-ok survivor | `corpus/lessons/round-100.md` § Routed ("carried, unchanged — the r99 compound M07 probe stands as filed"); `corpus/README.md:1307` ("the carried C5 compound witness"); r99 evidence `.ufo/waves/round-99/w1/MutRegistry/receipts/C5-selftest.txt` + `C5M07-selftest.txt` | **owed (carried, not closed)** |
| **unbound registry rows** | **No.** C2 binds the same 7 cells of 4 rows; the other operative rows stay presence-only. The operative table body has **163 rows** at `ce73ccaf`/`743ce449` and **165** at the landing tip `69474c55` (the two new tools' rows); 163 − 4 bound rows = **159 unbound rows** | `corpus/README.md:1307`; `.ufo/plans/round-100.md:100` ("The other 158 operative registry rows stay presence-only") — note the plan's figure is one off my measured 159 at the pre-round tip and two off the landing tip's 161; the *substance* (the unbound rows stay presence-only) is unchanged | **owed (carried, not closed)** |
| **the three r98 C2 gaps** (uncovered cells, tool+cell co-doctoring, printed-tally parsing) | **No.** C2 changes the capture's granularity only; none of the three gaps is addressed | `corpus/README.md:1307`; `corpus/lessons/round-100.md` § Routed ("carried, unchanged") | **owed (carried, not closed)** |
| **r96/r93/r89 residuals** (r92 launcher residuals, r93 probe pre-release caveat, r89 blanks-before-CRLF / ESP containment / empty labels) | **No.** They are re-listed verbatim in the round-100 Frontier addition | `corpus/README.md:1308-1310` | **owed (carried, not closed)** |
| *(carried from r99 §7 but **not** in the plan's Limits list: the dead `("ANCESTOR", None, None)` fixture sentinel (A4))* | **Partly.** The r100 checker still lists `("ANCESTOR", None, None)` in its `special` doctor tuple (`tools/check-registry-content-r100.py:572`) — but the r100 checker *does* have a live `ancestor_case` that calls `build_fixture(case, None)` (not the sentinel), so the sentinel is still a dead branch and A4 is **not** closed | `tools/check-registry-content-r100.py:572` vs `:651` (`build_fixture(case, None)`); `corpus/lessons/round-99.md` A4 | **owed (carried, not closed)** |

**Net:** round 100 closes the two named frontier sentences (one fully, one narrowed) and lands all
three routed spot-check defects. Every other carried item the plan names — the reference leg, the
C5 compound witness, the unbound rows, the three C2 gaps, the r96/r93/r89 residuals — is
**carried unchanged** and is still named as open in the round-100 Frontier addition
(`corpus/README.md:1304-1310`) and the lesson's Routed table. Nothing was absorbed silently.

## 5. The freeze harms no axis (evidence)

Receipt: `receipts/12-freeze-diff-evidence.txt`.

```
$ git diff ce73ccaf 743ce449 --stat -- SCORECARD.md PROVINCE.md SHONEN.md corpus/
(no output — empty)
$ git diff ce73ccaf 743ce449 --numstat -- SCORECARD.md PROVINCE.md SHONEN.md corpus/
(no output — empty)
$ git diff ce73ccaf 69474c55 --stat -- PROVINCE.md SHONEN.md
(no output — byte-identical at the landing tip)
$ git diff ce73ccaf 69474c55 --numstat -- SCORECARD.md corpus/
26	0	SCORECARD.md
25	0	corpus/README.md
3	0	corpus/SOURCES.md
88	0	corpus/knowledge/limine-echo-bends-r100.md
83	0	corpus/lessons/round-100.md
```
The freeze commit `743ce449` touches **no axis document and no corpus file** — its 22 paths are
all `.ufo/waves/round-100/before/**`, `.ufo/plans/round-100.md`, `.ufo/waves/round-100/claims.json`
and the two new `tools/` files. `SCORECARD.md` gained **26 lines and lost 0** (pure append) between
`ce73ccaf` and the landing tip `69474c55`; `PROVINCE.md` and `SHONEN.md` are byte-identical.
The corpus delta is **additive only** (5 files, +225, −0).

The freeze also left every pre-existing instrument untouched:
`git diff ce73ccaf 743ce449 --stat -- tools/check-limine-pins.py tools/limine-pin-battery-r99.py
tools/limine-pin-battery-r98.py tools/check-registry-content-r99.py tools/check-registry-coverage.py`
→ empty.

**Registry coverage gate** (the task's "must keep reading PASS after the landing rows are added"):

```
$ python3 tools/check-registry-coverage.py --revision 69474c55
{"branch":"master","branch_tip":"69474c55…","counts":{"findings":0,"missing":0,"registered":165,
 "rows_total":165,"tools_total":165},"findings":[],"revision":"69474c55…","status":"PASS"}
```
**PASS** at the landing tip — as found. Note the intermediate state honestly: at the **freeze**
tip `743ce449` the gate reads `FAIL findings 2 missing 2` (the two new tools had no `SKILL.md`
registry rows yet — rows land in `c450cd68`, so `tools_total` 165 vs `registered` 163), and at
`c450cd68` it read `CANNOT_EVALUATE` because the `check-registry-content-r100` registry row was
malformed (7 of 8 cells) — fixed by the L1's `69474c55` ("round-100: fix — the
check-registry-content-r100 registry row was missing its write-scope cell"). The lane's final
state is PASS; the intermediate FAIL/CANNOT_EVALUATE states are the ordinary
"tool lands before its registry row" window, and `69474c55` closes it.

## 6. No-work control: the two new tools did not exist before this round

Receipt: `receipts/13-no-work-control.txt`.

```
$ git cat-file -e ce73ccaf:tools/make-r100-bends.py
fatal: path 'tools/make-r100-bends.py' exists on disk, but not in 'ce73ccaf'
rc=128      (nonzero — absent at the pre-round tip)
$ git cat-file -e ce73ccaf:tools/check-registry-content-r100.py
fatal: path 'tools/check-registry-content-r100.py' exists on disk, but not in 'ce73ccaf'
rc=128      (nonzero — absent at the pre-round tip)
$ git cat-file -e ce73ccaf:tools/check-registry-content-r99.py
rc=0        (control: the r99 checker IS present at the pre-round tip)
```
Both probes exit nonzero at `ce73ccaf`; the r99 control is present. The capability (a
component-keyed echo bend generator; a label-set registry binder) did not exist before this round,
so the two frontier sentences could not have been closed earlier by these instruments.

## 7. One precision finding on the round's own new corpus row

Receipt: `receipts/14-s396-anchor-check.txt`.

`corpus/SOURCES.md:407` (S396, committed at `c450cd68`) anchors the generator as
"generator emission lines at BYTE 2615 (N12) and BYTE 3384 (N13)". Measured on the pinned
generator (`tools/make-r100-bends.py`, 4471 bytes, `7ccfe69e…`), the two anchors point at
**different constructs**:

```
N12 emission-line start (bytes.find of the whole quoted clause): 2615
N13 emission-line start (bytes.find of the whole quoted clause): 3365
N12 lie literal start ("999999998.9.9"):                        2634
N13 lie literal start ("12.999999998.4"):                       3384
```
So 2615 is N12's **emission line**, while 3384 is N13's **lie literal** — the N13 *emission
line* is at **3365**, which is exactly what the wave's own scribe measured
(`.ufo/waves/round-100/w1/ScribeLesson/receipts/08-n13-offset.txt`: "N13 substitution byte 3365 /
N12 substitution byte 2615"). The row's N13 anchor is therefore off by 19 bytes from the anchor
kind its N12 sibling uses. This is a corpus-precision nit (QUALITY 141 asks for byte-level
measurement, which the row does use; the unit is right, the *target* is one construct off), it
changes no claim reading, and the row is append-only. I report it rather than edit it — the fix
belongs to the scribe/L1 as a superseding row or lesson note (ids are never reused, so a new row
would take S399).

Two smaller precision notes, same class, neither claim-bearing:
- `corpus/lessons/round-100.md` (S396 Gate row) repeats the pair as "BYTES 2615/3384" and calls
  them "both N12/N13 emission sites"; per the measurement above, 3384 is the lie literal, not the
  emission site.
- `.ufo/plans/round-100.md:100` says "The other 158 operative registry rows stay presence-only";
  the operative table body measures **163** rows at `ce73ccaf`/`743ce449` (159 unbound) and **165**
  at `69474c55` (161 unbound). The substance (unbound rows stay presence-only) is unchanged; the
  count is stale.

## 8. Ledger summary

| frontier sentence / carried item | closed by | pointer | verdict |
|---|---|---|---|
| "The X/Y **echo** legs have no spelling-targeted committed bend" | C1 (`make-r100-bends.py` N12/N13 × unchanged r99 battery) | `corpus/README.md:1274-1276` (r99) → `corpus/README.md:1293-1294` (r100); `corpus/knowledge/limine-echo-bends-r100.md` | **landed (Y closed as a flip; X narrowed to a one-family delta)** |
| "the `unique` rule is fail-closed … the capture's alphabet is still `N<digits>` with no space token" | C2 (`check-registry-content-r100.py` label-set capture × unchanged r99 checker) | `corpus/README.md:1281-1282` (r99) → `corpus/README.md:1295-1296`; `corpus/knowledge/limine-echo-bends-r100.md` §4 | **landed** |
| R99-D2 (stale round-99 LOG headings) | append-only LOG correction | `LOG.md:4365` | **landed** |
| R99-D3 (one offset for two `LIE_KINDS` members) | lesson note naming both offsets | `corpus/lessons/round-100.md` `R99-ONE-ANCHOR-TWO-MEMBERS` | **landed** (as a lesson note) |
| R99-D4 (census before exit code) | before/after receipt with both exit codes | `.ufo/waves/round-100/before/census-before-after.txt` | **landed** |
| owed `--selftest --reference` leg | — | `corpus/README.md:1305`; `.ufo/plans/round-100.md:98-100` | **owed** |
| C5 always-ok ancestor survivor's compound witness | — | `corpus/README.md:1307` | **owed** |
| unbound registry rows | — | `corpus/README.md:1307` | **owed** |
| three r98 C2 gaps (uncovered cells / co-doctoring / printed-tally) | — | `corpus/README.md:1307` | **owed** |
| r96/r93/r89 residuals | — | `corpus/README.md:1308-1310` | **owed** |
| A4 dead `("ANCESTOR", None, None)` sentinel | — | `tools/check-registry-content-r100.py:572` | **owed** |
| freeze harms no axis | — | `receipts/12-freeze-diff-evidence.txt` | **PASS** (0 axis/corpus paths in the freeze; SCORECARD +26/−0; PROVINCE/SHONEN byte-identical) |
| registry coverage gate at the landing tip | — | `receipts/13-no-work-control.txt` | **PASS 165/165** (freeze tip FAIL 2 missing; `c450cd68` CANNOT_EVALUATE; fixed by `69474c55`) |
| no-work control (tools absent pre-round) | — | `receipts/13-no-work-control.txt` | **PASS** (both `git cat-file -e` probes exit nonzero at `ce73ccaf`) |
| S396's N13 byte anchor kind (finding, not a claim defect) | — | `receipts/14-s396-anchor-check.txt` | **finding** |

## 9. Commands run by this seat (exact)

```
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
git show ce73ccaf:corpus/README.md | grep -n "echo\*\* legs have no spelling-targeted committed bend"
git show ce73ccaf:corpus/README.md | grep -n "unique\` rule is fail-closed"
git show ce73ccaf:corpus/README.md | grep -n "alphabet is still"
git show ce73ccaf:corpus/README.md | sed -n '1274,1276p'; … sed -n '1281,1282p'
git show ce73ccaf:tools/limine-pin-battery-r99.py | grep -abo '"limine-version"'
git show ce73ccaf:tools/limine-pin-battery-r99.py | grep -abo '"visibility-era"'
git show ce73ccaf:tools/limine-pin-battery-r99.py | grep -abo 'LIE_KINDS'
git diff ce73ccaf 743ce449 --stat -- SCORECARD.md PROVINCE.md SHONEN.md corpus/
git diff ce73ccaf 743ce449 --numstat -- SCORECARD.md PROVINCE.md SHONEN.md corpus/
git diff ce73ccaf 743ce449 --name-only
git diff ce73ccaf 69474c55 --stat -- PROVINCE.md SHONEN.md
git diff ce73ccaf 69474c55 --numstat -- SCORECARD.md corpus/
git cat-file -e ce73ccaf:tools/make-r100-bends.py            # rc=128
git cat-file -e ce73ccaf:tools/check-registry-content-r100.py # rc=128
git cat-file -e ce73ccaf:tools/check-registry-content-r99.py  # rc=0
sha256sum -c .ufo/waves/round-100/before/instruments.sha256   # 16 OK, rc=0
python3 tools/check-registry-coverage.py --revision 69474c55   # PASS 165/165
python3 tools/check-registry-coverage.py --revision 743ce449   # FAIL (2 missing)
python3 tools/check-registry-content-r100.py --revision 743ce449|ce73ccaf ; --selftest
python3 tools/check-registry-content-r99.py  --revision 743ce449|ce73ccaf ; --selftest
python3 .ufo/waves/round-100/before/dev/make-fixtures.py <scratch>/fixtures
python3 tools/check-registry-content-r{100,99}.py --root <scratch>/fixtures/<TAG> --json <out>
python3 tools/limine-pin-battery-r99.py --gate tools/check-limine-pins.py --runs 1 --work <scratch> --json <out>
python3 tools/limine-pin-battery-r99.py --gate .ufo/waves/round-100/before/controls/bends/N12-x-echo.py --runs 1 --work <scratch> --json <out>
python3 tools/limine-pin-battery-r99.py --gate .ufo/waves/round-100/before/controls/bends/N13-y-echo.py --runs 1 --work <scratch> --json <out>
python3 tools/limine-pin-battery-r98.py --gate .ufo/waves/round-100/before/controls/bends/N1{2,3}-*-echo.py --runs 1 --work <scratch> --json <out>
python3 tools/limine-pin-battery-r99.py --selftest                 # PASS 5/5, reference leg skipped
git clone --shared <lane> <scratch>/clone ; git -C <scratch>/clone checkout 60b5636f
python3 <scratch>/clone/tools/limine-pin-battery-r{99,98}.py --gate <scratch>/clone/.ufo/…/bends/<bend>.py --runs 1 --work <scratch> --json <out>
diff -u tools/check-limine-pins.py .ufo/waves/round-100/before/controls/bends/<bend>.py
```
No generator (`make-r100-bends.py`, `make-r9*-bends.py`) was run; no mutating git/jj command was
run; no file outside this seat dir and this seat's scratch was written. Scratch deleted.

## 10. Tooling

No tool was installed or upgraded for this seat — every measurement used the repo's pinned
instruments plus coreutils, `git` (read-only subcommands only) and `python3` already on the host.
No `pacman` transaction, no `sudo`, no `~/.local/bin` write, no host sysctl/service/boot change.

{"seat":"ScoutFrontier","verdict":"findings","notes":"Limit-closure ledger: the r99 Frontier's two named sentences are closed — 'the X/Y echo legs have no spelling-targeted committed bend' by C1's N12/N13 component-keyed bends against the unchanged r99 battery (Y leg a met-to-unmet flip; X leg a one-family delta, narrowed by the round itself, not a flip) and 'the unique rule is fail-closed / the alphabet is still N<digits> with no space token' by C2's label-set capture (6 cells bind on r100 where r99 finds, 5 forged shapes stay closed, selftest 26/26 vs 17/17). All three routed spot-check items landed: R99-D2 as the append-only LOG correction (LOG.md:4365), R99-D3 as the lesson note naming both LIE_KINDS offsets (measured at byte level: limine-version 108455, visibility-era 108473, both line 2370; the tuple opens at 108277, the earlier pair 107815/107920 is the handler, not the member), R99-D4 as the before/after census receipt with both exit codes. Every carried item the plan names — the owed --selftest --reference leg, the C5 compound witness, the unbound rows, the three r98 C2 gaps, the r96/r93/r89 residuals, plus the A4 dead ANCESTOR sentinel — stays OWED, each still named open in the round-100 Frontier addition. Freeze harms no axis: git diff ce73ccaf 743ce449 over SCORECARD/PROVINCE/SHONEN/corpus is empty (0 paths); SCORECARD +26/-0 append-only; PROVINCE/SHONEN byte-identical; corpus additive (+225/-0); manifest sha256sum -c 16/16 OK. Coverage gate PASS 165/165 at 69474c55 (freeze tip FAIL 2 missing, c450cd68 CANNOT_EVALUATE — both closed by the L1's 69474c55 fix). No-work control PASS: git cat-file -e ce73ccaf:tools/make-r100-bends.py rc=128 and ce73ccaf:tools/check-registry-content-r100.py rc=128 (both absent pre-round), r99 checker rc=0. Findings: (1) the L1's first clone-layout receipts read 0/105 'gate absent' — a $CLONE/$ABS_PATH harness fault, quarantined under after/c1/harness-fault/ and re-run; my independent clone re-runs reproduce the frozen readings; (2) corpus/SOURCES.md:407 (S396) anchors the N13 generator site at BYTE 3384, which is the lie literal, while its N12 sibling 2615 is the emission line (N13 emission line = 3365, as the wave scribe measured) — a one-construct-off anchor, append-only, needs a superseding row or lesson note (next id S399); (3) plan:100's '158 operative registry rows' measures 159 unbound at ce73ccaf/743ce449 (163 body rows) and 161 at 69474c55 (165 rows)."}
