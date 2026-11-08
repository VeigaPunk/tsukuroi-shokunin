# ScribeLesson — report (round 100, wave w1)

Seat: `ScribeLesson`. Lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Scratch
`/fast/scratch/hyaku/tsukuroi-r100/ScribeLesson` (created with `mkdir -p`, passed to `--work`,
removed before yield with a path assertion ending in `/ScribeLesson`). Every receipt cited below
was written by this seat under `.ufo/waves/round-100/w1/ScribeLesson/receipts/`; nothing under
`/tmp` is cited. No tool installed or upgraded (`python3`, `curl`, `sha256sum`, `diff`, `grep` from
the base system); `pacman` not invoked; `sudo` never used. No git/jj mutation of any kind; the one
`git archive` extraction went into my own scratch.

## Commands, raw output (trimmed to the relevant lines), PASS/FAIL

### A. Harm guard — instrument manifest

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
$ sha256sum -c .ufo/waves/round-100/before/instruments.sha256
.ufo/plans/round-100.md: FAILED
sha256sum: WARNING: 1 computed checksum(s) did NOT match
$ sha256sum -c .ufo/waves/round-100/before/instruments.sha256 2>/dev/null | grep -c ': OK$'
15
$ sha256sum .ufo/plans/round-100.md
b7b163eac51e8d237e912e0616eadb7c6664748cc972332b3debc490ba9b2624  .ufo/plans/round-100.md   (pinned 44ae97d8…)
$ grep -v '^.ufo/plans' <manifest> | grep -v 'claims.json' > tools-only.sha256 ; sha256sum -c tools-only.sha256 | grep -c ': OK$'
14
```

Expected: 16/16 OK. **Measured: 15 OK + 1 FAILED (the plan file). FAIL**, and the failure is the
declaration file, not an instrument — routed as `R100-MANIFEST-PINS-THE-DECLARATION`.
Receipt `receipts/28-manifest-split.txt`.

Afterwards the L1 removed the `claims.json` and `.ufo/plans/round-100.md` lines from the manifest in
the working tree (16 → 14 entries); `sha256sum -c` on that working-tree manifest prints 14/14 OK,
rc 0. That edit is the L1's, not this seat's, and the reading above is against the committed 16-line
manifest at `7961738a`.

### B. C1 — five battery legs, `--runs 3`, `count-runs.py`

```
$ python3 tools/limine-pin-battery-r99.py --gate tools/check-limine-pins.py --runs 3 --work <scratch>/work-c1-gate-r99-runs3 --json <scratch>/c1-gate-r99-runs3.json
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
$ … --gate .ufo/waves/round-100/before/controls/bends/N12-x-echo.py … --json …/c1-N12-r99-runs3.json
families_passed 103/105 verdict unmet failed EXPLICIT-VERSION-ECHO,REFUSAL-VERSIONS-9DIGIT     (×3)
$ … --gate .ufo/waves/round-100/before/controls/bends/N13-y-echo.py … --json …/c1-N13-r99-runs3.json
families_passed 104/105 verdict unmet failed REFUSAL-VERSIONS-9DIGIT-Y                          (×3)
$ python3 tools/limine-pin-battery-r98.py --gate …/N12-x-echo.py … --json …/c1-N12-r98-runs3.json
families_passed 104/105 verdict unmet failed EXPLICIT-VERSION-ECHO                              (×3)
$ python3 tools/limine-pin-battery-r98.py --gate …/N13-y-echo.py … --json …/c1-N13-r98-runs3.json
families_passed 105/105 verdict met failed -                                                   (×3)
$ python3 .ufo/waves/round-95/before/controls/count-runs.py <json> --family REFUSAL-VERSIONS-9DIGIT --family REFUSAL-VERSIONS-9DIGIT-Y --family EXPLICIT-VERSION-ECHO
  gate  run1..3: met 105/105 [] cases 420 error_rows 0 named {X:[4,0], Y:[4,0], E:[4,0]}
  N12   run1..3: unmet 103/105 [EXPLICIT-VERSION-ECHO, REFUSAL-VERSIONS-9DIGIT] cases 420 error_rows 0 named {X:[0,4], Y:[4,0], E:[3,1]}
  N13   run1..3: unmet 104/105 [REFUSAL-VERSIONS-9DIGIT-Y] cases 420 error_rows 0 named {X:[4,0], Y:[0,4], E:[4,0]}
  r98/N12 1..3: unmet 104/105 [EXPLICIT-VERSION-ECHO] cases 420 error_rows 0 named {X:[4,0], Y:[4,0], E:[3,1]}
  r98/N13 1..3: met 105/105 [] cases 420 error_rows 0 named {X:[4,0], Y:[4,0], E:[4,0]}
```

PASS on every frozen C1 target line (verdict, family set, 0 error rows, 3/3 runs identical).
Receipts `receipts/10-count-runs.txt`, `receipts/10b-count-runs-summary.txt`.

### C. C1 — bend diffs and battery selftest

```
$ diff -u tools/check-limine-pins.py .ufo/waves/round-100/before/controls/bends/N12-x-echo.py
@@ -313,7 +313,7 @@
-            "limine_version": limine_version,
+            "limine_version": ("999999998.9.9" if limine_version.split(".")[0] == "999999999" else limine_version),  # N12 …
$ diff -u tools/check-limine-pins.py .ufo/waves/round-100/before/controls/bends/N13-y-echo.py
-            "limine_version": limine_version,
+            "limine_version": ("12.999999998.4" if limine_version.count(".") >= 1 and limine_version.split(".")[1] == "999999999" else limine_version),  # N13 …
$ diff -u … | grep -cE '^[+-][^+-]'      → 2 (one −/+ pair, one hunk, each bend)
$ python3 tools/limine-pin-battery-r99.py --selftest
reference-gate      skipped (no --reference)
roster-literal     PASS families_passed=105
absent             PASS families_passed=0
constant-healthy   PASS families_passed=0
non-json           PASS families_passed=0
constant-degraded  PASS families_passed=0
selftest PASS 5/5
```

PASS on "one changed line each" and on "selftest without `--reference` PASS 5/5"; the reading note
(the reference leg is excluded from the denominator) is recorded in the lesson.
Receipts `receipts/05-bend-diffs.txt`, `receipts/05-diff-N12-x-echo.txt`,
`receipts/05-diff-N13-y-echo.txt`, `receipts/07-battery-selftest.txt`.

### D. C2 — live table, selftests, twelve fixtures

```
$ for REV in ce73ccaf 743ce449 c450cd68 69474c55 7961738a; do for T in r100 r99; do
    python3 tools/check-registry-content-$T.py --revision $REV; done; done
ce73ccaf  r100 PASS 7/7 findings 0      r99 PASS 7/7 findings 0
743ce449  r100 PASS 7/7 findings 0      r99 PASS 7/7 findings 0
c450cd68  r100 CANNOT-EVALUATE: malformed registry row at line 5951
c450cd68  r99  CANNOT-EVALUATE: malformed registry row at line 5951
69474c55  r100 PASS 7/7 findings 0      r99 PASS 7/7 findings 0
7961738a  r100 PASS 7/7 findings 0      r99 PASS 7/7 findings 0
$ python3 tools/check-registry-content-r100.py --selftest | tail -1     → selftest PASS 26/26
$ python3 tools/check-registry-content-r99.py  --selftest | tail -1     → selftest PASS 17/17
$ python3 .ufo/waves/round-100/before/dev/make-fixtures.py <scratch>/fx     → 12 fixture trees
$ for TAG in 12 tags; do for T in r100 r99; do python3 tools/check-registry-content-$T.py --root <scratch>/fx/$TAG --json …; done; done
SEP-SPACE      PASS / RC-CELL-MISSING      SEP-SEMICOLON  PASS / RC-CELL-MISSING
SEP-PLUS       PASS / RC-CELL-MISSING      SEP-SLASH      PASS / RC-CELL-MISSING
SEP-AND        PASS / RC-VALUE-MISMATCH    UNION          PASS / RC-VALUE-MISMATCH
LETTER         RC-CELL-MISSING / RC-CELL-MISSING           PROSE  RC-CELL-MISSING / RC-CELL-MISSING
UNION-LIE      RC-VALUE-MISMATCH / RC-VALUE-MISMATCH       HYBRID RC-VALUE-MISMATCH / RC-CELL-MISSING
RESTATED       RC-CELL-AMBIGUOUS / RC-CELL-AMBIGUOUS       GAP    PASS / PASS
```

PASS on every frozen C2 target line, including HYBRID's r99→r100 move to the frozen
`RC-VALUE-MISMATCH`. The knowledge entry's own recheck leg run verbatim (`--runs 1`) prints
`104/105 … REFUSAL-VERSIONS-9DIGIT-Y` with `rc=1`, matching the entry's stated requirement.
Receipts `receipts/11-live-table-and-coverage.txt`, `receipts/06-selftests.txt`,
`receipts/36-knowledge-recheck-rc.txt`, `receipts/02-c2-fixture-cells.tsv`,
`receipts/01-fixture-paths.txt`, `receipts/34-final-head-readings.txt`.

### E. Registry coverage gate (harm guard), as found

```
$ python3 tools/check-registry-coverage.py --revision 743ce449490f4e9ff004f423ecc3fa456cbc77ec
{"counts":{"findings":2,"missing":2,"registered":163,"rows_total":163,"tools_total":165},
 "findings":[{"id":"REGISTRY-ROW-MISSING","site":"tools/check-registry-content-r100.py"},
             {"id":"REGISTRY-ROW-MISSING","site":"tools/make-r100-bends.py"}],"status":"FAIL"}   rc=1
$ … --revision c450cd68a18a666f7bc835bcb2e8d76119f8aff6
{"counts":{"findings":1,…},"findings":[{"detail":"malformed registry row at line 5951","id":"E-REGISTRY-TABLE"}],"status":"CANNOT_EVALUATE"}  rc=2
$ … --revision ce73ccaf75d0279385977f03ccb35945c1cf8e07
{… "registered":163,"rows_total":163,"tools_total":163 … "status":"PASS"}   rc=0
$ … --revision 69474c55eb38632f3e740923b58029dc43e01300
{… "registered":165,"rows_total":165,"tools_total":165 … "status":"PASS"}   rc=0
$ … --revision 7961738a4954f177e846e8bae34576ab71dc9833
{… "registered":165,"rows_total":165,"tools_total":165 … "status":"PASS"}   rc=0
```

PASS at the landing tip (the harm guard's requirement), FAIL-2-missing at the freeze revision,
CANNOT_EVALUATE at the intermediate landing commit. All three reported raw.
Receipts `receipts/16-coverage-at-freeze.txt`, `receipts/17-coverage-land-vs-master.txt`,
`receipts/34-final-head-readings.txt`.

### F. Byte anchors (QUALITY 141) — re-measured, not copied

```
tools/make-r100-bends.py   4471 B  7ccfe69e…   N12 clause 2615 (value 2634), N13 clause 3365 (value 3384)
tools/check-registry-content-r100.py 38009 B 7a23a522…  TOKEN 12025, SEPARATORS 12073, parse_label_set 12134
tools/check-limine-pins.py 30286 B 7d79ac29…  "limine_version": limine_version, at 11230 (line 200, 16-space) and 16931 (line 316, 12-space)
tools/limine-pin-battery-r99.py 117542 B c2e8c8fc…  "limine-version" 107815 (dict key) / 108455 (LIE_KINDS); "visibility-era" 107920 / 108473
https://docs.python.org/3/library/re.html  200  257722 B  69d64759…  id="re.fullmatch" 111489; markup-literal sentence 112171;
                                                                     de-marked-up sentence bytes.find → -1; "Last updated …" 257438;
                                                                     "\b" sentence 69787 (byte-exact, 14 words)
https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/CONFIG.md  200  27609 B  f44f3a19…
                                                                     counts limine_version/visibility_era/echo/version = 0/0/0/0
```

PASS on every offset measured; **one MISMATCH class found**: the de-marked-up S397 sentence does not
reproduce at its own offset (both the `Match` and the `match object` renderings).
Receipts `receipts/03-urls-sha256.txt`, `receipts/04-offset-remeasure.txt`,
`receipts/09-s397-quote-reproduction.txt`, `receipts/14-n13-offset-detail.txt`,
`receipts/18-liekinds-disambiguation.txt`, `receipts/24-final-gate-quote-table.txt`,
`receipts/25-s395-cited-command-ambiguity.txt`, `receipts/32-gate-emission-two-occurrences.txt`,
`receipts/35-gate-emission-context.txt`.

### G. Census

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi   (run 1 and 2)
  59 lines each, md5 37ed43e298cb8e18f06e1ee8e24fc804 (identical), exit 0
  57 × W04, 1 × W01 (S381 tierC mined), 1 × "tsukuroi ok …/corpus/SOURCES.md", 0 × E-codes
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md   → 398, exit 0
```

PASS on `exit 0` and `0 E-codes`; **the receipt's recorded output is a 2-line tail of the 59-line
run** (verified by diff), routed as `R100-CENSUS-RECEIPT-TAIL`.
Receipts `receipts/23-census-receipt-completeness.txt`, `receipts/29-census-receipt-is-a-tail.txt`,
`receipts/22-census-warning-set-drift.txt`, `receipts/27-census-isolated-root.txt`,
`receipts/12-census-and-coinflip.txt`.

### H. Brief-vs-corpus and join-grammar probes

```
$ grep -rniE '\bcoin[ -]?flip' corpus/ .ufo/plans/ .ufo/waves/round-100/claims.json | grep -v 'w1-spec.json\|w1-dispatch.json\|make-spec.py' | wc -l
0
$ python3 <scratch>/adv-check.py     # empty-token probes, built with the checker's own build_fixture
BASELINE         cell='VARIANTS N01-N03'           rc=0 PASS []
EMPTY-LEADING    cell='VARIANTS and N01-N03'       rc=0 PASS []
EMPTY-TRAILING   cell='VARIANTS N01-N03 and'       rc=0 PASS []
EMPTY-ADJACENT   cell='VARIANTS N01; ; N02; N03'   rc=0 PASS []
PROSE-THROUGH    cell='VARIANTS N01 through N03'   rc=1 FAIL [RC-CELL-MISSING]
$ python3 <bends>/N12-x-echo.py --conf <absent> --esp <dir> --limine-version 999999999.9.9
{"…","limine_version": "999999999.9.9", … "verdict": "CANNOT-EVALUATE", …}     # truth, not falsified
```

Receipts `receipts/15-coinflip-and-landed-lesson-gate.txt`, `receipts/20-a3-empty-token-probe.txt`,
`receipts/21-a1-a2-probe.txt`.

## Artifacts

| path | content |
|---|---|
| `.ufo/waves/round-100/w1/ScribeLesson/lesson-draft.md` | the lesson draft (Gate / Mistakes / Routed / Frontier) |
| `.ufo/waves/round-100/w1/ScribeLesson.md` | scoped findings report |
| `.ufo/waves/round-100/w1/ScribeLesson/report.md` | this file |
| `.ufo/waves/round-100/w1/ScribeLesson/receipts/01…35-*.txt` (39 files) | every command, raw output and derived table cited above |

```json
{"seat":"ScribeLesson","verdict":"findings","notes":"Lesson drafted at .ufo/waves/round-100/w1/ScribeLesson/lesson-draft.md: Gate with 14 candidate rows (two new tools, S396/S397 admitted with corrections, S398 rejected, knowledge entry, two bend controls, six acceptance cells, five fail-closed cells, GAP control) plus the census block; 11 Mistakes rows each with an evidence pointer and a captured-by (R100-X-DELTA-COUNTED-AS-FLIP, R100-CLONE-PATH-PREFIX, R100-REGISTRY-ROW-CELL-COUNT, R100-TOOL-WITHOUT-ROW-AT-FREEZE, R100-QUOTE-NOT-BYTE-LITERAL, R100-MANIFEST-PINS-THE-DECLARATION, R100-ANCHOR-SEARCH-NOT-DISAMBIGUATED, R100-CENSUS-RECEIPT-TAIL, R99-ONE-ANCHOR-TWO-MEMBERS, R99-STALE-LOG-HEADING, R99-CENSUS-EXIT-OMITTED); Routed 10 rows; Frontier paragraph naming only measured items. Every frozen C1 and C2 number re-derived by this seat (gate 105/105 x3; N12 103/105 two families x3; N13 104/105 one family x3; r98 control 104/105 / 105/105 x3; zero error rows; one-line diffs; selftest 26/26 and 17/17; live table PASS 7/7 at four revisions; twelve fixture cells match the frozen dev table row for row; coverage PASS 165/165 at the landing tip). Findings reported raw: the harm-guard manifest now reads 15 OK + 1 FAILED because it pins .ufo/plans/round-100.md (all 14 instrument bytes OK); S397's Gate quote is not byte-literal (bytes.find -1 for both de-marked-up variants, the marked-up form reproduces at 112171); S396 pairs the N12 clause start 2615 with the N13 value start 3384 while the clause start is 3365 and its teaches implies one family where X moves two; the gate emits limine_version twice (11230 early / 16931 main) so a naive re-measure misdirects and the early return echoes truth; the census receipt records a 2-line tail of a 59-line, exit-0, E-code-free run; the brief's coin-flip class has 0 hits in the lane's corpus/plans/claims; empty-token leniency reproduced. Nothing outside the seat dir was written; scratch removed; no tool installed; no git/jj mutation."}
```
