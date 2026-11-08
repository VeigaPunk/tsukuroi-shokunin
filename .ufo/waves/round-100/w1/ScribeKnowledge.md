# ScribeKnowledge — round 100, wave w1 (knowledge entry candidate)

Seat: `ScribeKnowledge` (scribe, leaf member — no subagent dispatch).
Target: draft the round's knowledge entry `corpus/knowledge/limine-echo-bends-r100.md`; the L1 lands
it; this seat writes the **candidate** under its own seat dir.

Files written (all under the seat dir, the only paths this seat created):

- `.ufo/waves/round-100/w1/ScribeKnowledge/knowledge-draft.md` — the candidate entry.
- `.ufo/waves/round-100/w1/ScribeKnowledge/census-check.txt` — word counts of every located quote
  the candidate places (≤25 words each).
- `.ufo/waves/round-100/w1/ScribeKnowledge/receipts/*.txt` — 34 receipts, every number below.
- `.ufo/waves/round-100/w1/ScribeKnowledge.md` — this report.

No file outside the seat dir was created, modified or deleted. `git status --porcelain` over the
seat dir shows only `?? .ufo/waves/round-100/w1/ScribeKnowledge/` (untracked, new). No `git`/`jj`
mutation was run: the only git calls were `rev-parse`, `log`, `ls-tree`, `show`, `status`,
`diff` (read-only).

---

## 0. Harm guard — instrument integrity before any citation

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin && sha256sum -c .ufo/waves/round-100/before/instruments.sha256
tools/check-limine-pins.py: OK
tools/limine-pin-battery-r99.py: OK
tools/limine-pin-battery-r98.py: OK
tools/check-registry-content-r99.py: OK
tools/check-registry-content-r100.py: OK
tools/make-r100-bends.py: OK
tools/make-r96-bends.py: OK
tools/check-registry-coverage.py: OK
.ufo/waves/round-100/before/controls/do-nothing-battery-r98.py: OK
.ufo/waves/round-100/before/controls/do-nothing-battery-r99.py: OK
.ufo/waves/round-100/before/controls/do-nothing-checker-r99.py: OK
.ufo/waves/round-100/before/controls/bends/N12-x-echo.py: OK
.ufo/waves/round-100/before/controls/bends/N13-y-echo.py: OK
.ufo/waves/round-100/before/dev/make-fixtures.py: OK
.ufo/waves/round-100/claims.json: OK
.ufo/plans/round-100.md: OK
manifest rc=0
```

**PASS** — 16/16 pinned entries OK at 12:14 (receipt `receipts/00-instrument-manifest.txt`).

### 0a. The plan file's manifest line now fails — reported, not smoothed over

The L1 appended the **A1** amendment to `.ufo/plans/round-100.md` at 12:28 (commit `ef12af4c`,
"round-100: after receipts … plan A1"), and that file is one of the manifest's 16 pinned entries. A
re-run of the manifest at 12:28 therefore reads **15 OK / 1 FAILED** — the FAILED line is
`.ufo/plans/round-100.md` (pinned `44ae97d8…`, now `f4c7cbe7…`); every one of the 15 *instrument*
bytes (the eight `tools/` files, the three do-nothing controls, the two bend articles, the fixture
builder and `claims.json`) still verifies, rc 0 on the tools-only manifest
(`receipts/00b-manifest-after-A1.txt`). The plan is an append-only declaration the L1 owns and the
amendment slot explicitly invites this write; the drift is a consequence of the lane's own
bookkeeping, not a change to any instrument this seat measured, and it is disclosed here rather than
re-quoted as a pass. **Every measurement in this report was taken against the 15 instrument bytes,
which are unchanged.**

## 0b. Tooling

No tool was installed or upgraded this round: the work needed only `python3`, `curl`, `diff`,
`grep` and `sha256sum`, all already present (`python3` 3.14 per the `__pycache__` tag; `curl`,
`diffutils`, `coreutils` from the base system). `pacman` was **not** touched (host-wide pause);
`sudo` was never used.

---

## 1. C1 — the two echo bends (depth 8)

### 1.1 What I ran (exact commands)

```
$ python3 tools/limine-pin-battery-r99.py --gate tools/check-limine-pins.py --runs 3 --work $SC/work/gate --json $SC/gate-r99.json
$ python3 tools/limine-pin-battery-r99.py --gate .ufo/waves/round-100/before/controls/bends/N12-x-echo.py --runs 3 --work $SC/work/N12-x-echo-r99 --json $SC/N12-x-echo-r99.json
$ python3 tools/limine-pin-battery-r99.py --gate .ufo/waves/round-100/before/controls/bends/N13-y-echo.py --runs 3 --work $SC/work/N13-y-echo-r99 --json $SC/N13-y-echo-r99.json
$ python3 tools/limine-pin-battery-r98.py --gate .ufo/waves/round-100/before/controls/bends/N12-x-echo.py --runs 3 --work $SC/work/N12-x-echo-r98 --json $SC/N12-x-echo-r98.json
$ python3 tools/limine-pin-battery-r98.py --gate .ufo/waves/round-100/before/controls/bends/N13-y-echo.py --runs 3 --work $SC/work/N13-y-echo-r98 --json $SC/N13-y-echo-r98.json
$ python3 .ufo/waves/round-95/before/controls/count-runs.py <json> --family REFUSAL-VERSIONS-9DIGIT --family REFUSAL-VERSIONS-9DIGIT-Y --family EXPLICIT-VERSION-ECHO
$ python3 tools/limine-pin-battery-r99.py --selftest          # no --reference
$ diff -u tools/check-limine-pins.py .ufo/waves/round-100/before/controls/bends/<bend>.py
```

`SC=/fast/scratch/hyaku/tsukuroi-r100/ScribeKnowledge` (created, and deleted before yield).
`tools/make-r100-bends.py` was **not** run (it writes into the lane's frozen wave dirs); the bends
were read from the pinned control files and their bytes verified by the manifest above.

### 1.2 Raw readings (trimmed to the relevant lines)

```
== gate, r99 battery (3 runs) ==
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
rc=0
== N12-x-echo, r99 battery (3 runs) ==
families_passed 103/105 verdict unmet failed EXPLICIT-VERSION-ECHO,REFUSAL-VERSIONS-9DIGIT   (×3)
rc=1
== N13-y-echo, r99 battery (3 runs) ==
families_passed 104/105 verdict unmet failed REFUSAL-VERSIONS-9DIGIT-Y                        (×3)
rc=1
== N12-x-echo, r98 control battery (3 runs) ==
families_passed 104/105 verdict unmet failed EXPLICIT-VERSION-ECHO                            (×3)
rc=1
== N13-y-echo, r98 control battery (3 runs) ==
families_passed 105/105 verdict met failed -                                                   (×3)
rc=0
== r99 battery --selftest (no --reference) ==
reference-gate      skipped (no --reference)
roster-literal     PASS families_passed=105
absent             PASS families_passed=0
constant-healthy   PASS families_passed=0
non-json           PASS families_passed=0
constant-degraded  PASS families_passed=0
selftest PASS 5/5
rc=0
```

Per-run error rows: **0** in all five legs (each JSON's `case_log` counted for non-null `error`;
`cases: 420`, `families_total: 105` in every run). Receipts `receipts/01`, `02-…`, `03-…`,
`10-count-runs-gate.txt`, `11-count-runs-bends.txt`, `11b-count-runs-n13-control.txt`,
`40-battery-selftest.txt`.

### 1.3 PASS/FAIL per expected line (C1)

| expected line (claims.json C1 target) | measured | verdict |
|---|---|---|
| landed gate `105/105 met`, `failed_families []`, 0 error rows | `met 105/105 []` ×3, 0 error rows | **PASS** |
| `N13-y-echo` under r99: `unmet 104/105`, exactly `[REFUSAL-VERSIONS-9DIGIT-Y]`, 0 error rows | `unmet 104/105 [REFUSAL-VERSIONS-9DIGIT-Y]` ×3, 0 error rows | **PASS** |
| `N12-x-echo` under r99: `unmet 103/105`, exactly `[EXPLICIT-VERSION-ECHO, REFUSAL-VERSIONS-9DIGIT]`, 0 error rows | exactly that set ×3, 0 error rows | **PASS** |
| r98 control on `N13-y-echo`: `met 105/105` (blind) | `met 105/105 []` ×3 | **PASS** |
| r98 control on `N12-x-echo`: `unmet 104/105` exactly `[EXPLICIT-VERSION-ECHO]` (one-family delta) | exactly that set ×3 | **PASS** |
| each bend's diff vs the gate is exactly one changed line | `grep -c '^<'` = 1, `grep -c '^>'` = 1 for each bend | **PASS** |
| battery `--selftest` without `--reference` = `PASS 5/5` | `selftest PASS 5/5`, rc 0 | **PASS** |

**C1: met**, on the seat's own runs. The development-run readings committed at
`.ufo/waves/round-100/before/dev/` (`c1-gate-runs1.json`, `c1-bend-N12-x-echo.json`,
`c1-bend-N13-y-echo.json`, `c1-control-N12-x-echo.json`, `c1-control-N13-y-echo.json`) reproduce
the same verdicts, failed-family sets and 0 error rows — receipt `receipts/12-dev-receipt-readings.txt`.

### 1.4 The X-leg delta, proven rather than asserted

The candidate states the X leg as a **one-family delta**, not a met-to-unmet flip, and the state
rests on two measurements this seat took:

- the r98 control reads `unmet 104/105 [EXPLICIT-VERSION-ECHO]` on the X article — it is **not**
  blind there (receipt `03-N12-x-echo-r98-control-stdout.txt`);
- the r96 `EXPLICIT-VERSION-ECHO` family sends the same spelling — `EXPLICIT_VERSION_META = ("12.9.4",
  "12.9.5", "12.9.6", REFUSAL_DIGIT9)` with `REFUSAL_DIGIT9 = "9" * 9 + ".9.9"` — measured from
  `tools/limine-pin-battery-r99.py` (receipt `41-version-spellings.txt`);
- `c.check_echo = True` is set on five r99 families and only three r98 families; the two the r99
  battery added are `fam_refusal_versions_9digit` (X) and `fam_refusal_versions_9digit_y` (Y)
  (receipt `39-check-echo-owners.txt`).

The Y leg *is* a met-to-unmet closure: the r98 control reads `met 105/105` on the Y article, and
the only Y-cap spellings in the battery are `12.999999999.4` and `0.999999999.0`
(`Y_DIGIT9`), so no r96–r98 family reads the echo on them (same receipt).

## 2. C2 — RC-BEND-SPAN as a label set (freshness 9)

### 2.1 What I ran

```
$ python3 tools/check-registry-content-r100.py --revision <ce73ccaf|743ce449|69474c55> --json <out>
$ python3 tools/check-registry-content-r99.py  --revision <same three> --json <out>
$ python3 tools/check-registry-content-r100.py --selftest
$ python3 tools/check-registry-content-r99.py  --selftest
$ python3 .ufo/waves/round-100/before/dev/make-fixtures.py $SC/fixtures
$ python3 tools/check-registry-content-<r100|r99>.py --root $SC/fixtures/<TAG>      # for all 12 tags
$ python3 tools/check-registry-coverage.py --revision <ce73ccaf|743ce449|69474c55>
```

`make-fixtures.py` writes only under the given `--outdir`; it was pointed at the seat's scratch.
The fixtures are the frozen checker's own `build_fixture` bytes, not a hand copy.

### 2.2 Raw readings

```
== live table ==
r100 --revision ce73ccaf : registry-content: status PASS bindings 7/7 findings 0   rc=0
r99  --revision ce73ccaf : registry-content: status PASS bindings 7/7 findings 0   rc=0
r100 --revision 743ce449 : registry-content: status PASS bindings 7/7 findings 0   rc=0
r99  --revision 743ce449 : registry-content: status PASS bindings 7/7 findings 0   rc=0
r100 --revision 69474c55 : registry-content: status PASS bindings 7/7 findings 0   rc=0  (rows 165)
r99  --revision 69474c55 : registry-content: status PASS bindings 7/7 findings 0   rc=0  (rows 165)
== selftests ==
r100: selftest PASS 26/26   rc=0
r99 : selftest PASS 17/17   rc=0
== registry coverage gate ==
--revision ce73ccaf : status PASS  registered 163  tools_total 163  findings 0   rc=0
--revision 743ce449 : status FAIL  findings 2  REGISTRY-ROW-MISSING tools/check-registry-content-r100.py,
                                 REGISTRY-ROW-MISSING tools/make-r100-bends.py                rc=1
--revision 69474c55 : status PASS  registered 165  rows_total 165  tools_total 165  findings 0   rc=0
```

### 2.3 The twelve fixture cells, both checkers (own runs)

```
TAG            | CHECKER  | STATUS | FINDINGS
SEP-SPACE      | r100     | PASS   | none (rc=0)
SEP-SPACE      | r99      | FAIL   | FINDING RC-CELL-MISSING  (rc=1)
SEP-SEMICOLON  | r100     | PASS   | none (rc=0)
SEP-SEMICOLON  | r99      | FAIL   | FINDING RC-CELL-MISSING  (rc=1)
SEP-AND        | r100     | PASS   | none (rc=0)
SEP-AND        | r99      | FAIL   | FINDING RC-VALUE-MISMATCH  (rc=1)
SEP-SLASH      | r100     | PASS   | none (rc=0)
SEP-SLASH      | r99      | FAIL   | FINDING RC-CELL-MISSING  (rc=1)
SEP-PLUS       | r100     | PASS   | none (rc=0)
SEP-PLUS       | r99      | FAIL   | FINDING RC-CELL-MISSING  (rc=1)
UNION          | r100     | PASS   | none (rc=0)
UNION          | r99      | FAIL   | FINDING RC-VALUE-MISMATCH  (rc=1)
LETTER         | r100     | FAIL   | FINDING RC-CELL-MISSING  (rc=1)
LETTER         | r99      | FAIL   | FINDING RC-CELL-MISSING  (rc=1)
PROSE          | r100     | FAIL   | FINDING RC-CELL-MISSING  (rc=1)
PROSE          | r99      | FAIL   | FINDING RC-CELL-MISSING  (rc=1)
UNION-LIE      | r100     | FAIL   | FINDING RC-VALUE-MISMATCH  (rc=1)
UNION-LIE      | r99      | FAIL   | FINDING RC-VALUE-MISMATCH  (rc=1)
HYBRID         | r100     | FAIL   | FINDING RC-VALUE-MISMATCH  (rc=1)
HYBRID         | r99      | FAIL   | FINDING RC-CELL-MISSING  (rc=1)
RESTATED       | r100     | FAIL   | FINDING RC-CELL-AMBIGUOUS  (rc=1)
RESTATED       | r99      | FAIL   | FINDING RC-CELL-AMBIGUOUS  (rc=1)
GAP            | r100     | PASS   | none (rc=0)
GAP            | r99      | PASS   | none (rc=0)
```

Each cell's registry text was read from the fixture's own `SKILL.md` bytes (receipt
`36-fixture-cells.txt`), e.g. `SEP-SPACE` = `VARIANTS N01 N02 N03`, `UNION` = `VARIANTS N01-N02 and
N04-N05`, `HYBRID` = `VARIANTS N01-N04,N05`, `RESTATED` = `VARIANTS N01,N03 then VARIANTS N01-N03`.

### 2.4 PASS/FAIL per expected line (C2)

| expected line (claims.json C2 target) | measured | verdict |
|---|---|---|
| live table r100: `PASS`, findings 0, 7/7 bindings | PASS 7/7 findings 0 at `ce73ccaf`, `743ce449`, `69474c55` | **PASS** |
| r99 control reads `PASS 7/7` on the same table | PASS 7/7 at all three revisions | **PASS** |
| `SEP-SPACE` PASS on r100, r99 `RC-CELL-MISSING` | PASS / `RC-CELL-MISSING` | **PASS** |
| `SEP-SEMICOLON` PASS on r100, r99 `RC-CELL-MISSING` | PASS / `RC-CELL-MISSING` | **PASS** |
| `SEP-PLUS` PASS on r100, r99 `RC-CELL-MISSING` | PASS / `RC-CELL-MISSING` | **PASS** |
| `SEP-SLASH` PASS on r100, r99 `RC-CELL-MISSING` | PASS / `RC-CELL-MISSING` | **PASS** |
| `SEP-AND` PASS on r100, r99 `RC-VALUE-MISMATCH` | PASS / `RC-VALUE-MISMATCH` | **PASS** |
| `UNION` PASS on r100, r99 `RC-VALUE-MISMATCH` | PASS / `RC-VALUE-MISMATCH` | **PASS** |
| `LETTER` r100 `RC-CELL-MISSING` | `RC-CELL-MISSING` | **PASS** |
| `PROSE` r100 `RC-CELL-MISSING` | `RC-CELL-MISSING` | **PASS** |
| `UNION-LIE` r100 `RC-VALUE-MISMATCH` | `RC-VALUE-MISMATCH` | **PASS** |
| `HYBRID` r100 `RC-VALUE-MISMATCH` | `RC-VALUE-MISMATCH` | **PASS** |
| `RESTATED` r100 `RC-CELL-AMBIGUOUS` | `RC-CELL-AMBIGUOUS` | **PASS** |
| `GAP` PASS on both | PASS on r100 and r99 | **PASS** |
| r100 `--selftest` PASS 26/26 | `selftest PASS 26/26` rc 0 | **PASS** |
| r99 control `--selftest` PASS 17/17 | `selftest PASS 17/17` rc 0 | **PASS** |

**C2: met**, on the seat's own runs.

### 2.5 The coverage gate, reported as found

`python3 tools/check-registry-coverage.py --revision 69474c55` reads **PASS** (165 rows, 165 tools,
0 findings) at the landing tip — the harm guard holds. At the *freeze* revision `743ce449` the same
gate reads **FAIL** with exactly two `REGISTRY-ROW-MISSING` findings (`tools/check-registry-content-r100.py`,
`tools/make-r100-bends.py`), because the two new tools landed before their registry rows. That is
the pre-landing state of the same revision, not a defect at the tip; it is reported here as found
rather than smoothed over. Receipt `23-coverage-gate.txt`.

---

## 3. Provenance trio and the source rows

The candidate opens with the required three lines:

```
source: tools/make-r100-bends.py @ 743ce449 + tools/check-registry-content-r100.py @ 743ce449 (S396, S397)
verified-at: 2026-11-08
recheck: <one battery leg> ; <one checker fixture leg>
```

Both recheck legs were **executed verbatim** before being written down (receipts
`42-recheck-battery-leg.txt` and `38-recheck-checker-leg.txt`):

```
$ python3 tools/limine-pin-battery-r99.py --gate .ufo/waves/round-100/before/controls/bends/N13-y-echo.py --runs 1 --work $SC/work/recheck-n13
families_passed 104/105 verdict unmet failed REFUSAL-VERSIONS-9DIGIT-Y
rc=1
$ python3 tools/check-registry-content-r100.py --root $SC/fixtures/SEP-SPACE
registry-content: status PASS bindings 7/7 findings 0     rc=0
$ python3 tools/check-registry-content-r99.py --root $SC/fixtures/SEP-SPACE
FINDING RC-CELL-MISSING SKILL.md:10 make-r96-bends cell 5 no longer states 'VARIANTS (N[0-9]+(?:-N[0-9]+|(?:,N[0-9]+)+))(?![0-9,-])'
registry-content: status FAIL bindings 6/7 findings 1     rc=1
```

### S397 — the external row: available, and independently reproduced

The scout's fetch **succeeded**; this seat reproduced it twice with byte-identical results
(`receipts/37-s397-fetch-and-quotes.txt`):

```
$ curl -sS -o re.html -w 'http=%{http_code} bytes=%{size_download}\n' https://docs.python.org/3/library/re.html
http=200 bytes=257722
$ sha256sum re.html
69d64759ed7e269bd617470594dfb8c7970b61fa4def81530a5ea2953d42493b  re.html
$ cmp re.html re2.html   # two independent fetches
cmp: identical to the first fetch
```

Byte-level anchors on the fetched bytes (`bytes.find`, QUALITY 141): `id="re.fullmatch"` at **111489**,
the `fullmatch` sentence at **112171**, the `\b` word-boundary sentence at **69787**. So the
candidate cites **both S396 and S397**; no "cite S396 alone" fallback was needed. The same sha256
appears in the wave's own scout receipt (a sibling seat's file, cited read-only:
`.ufo/waves/round-100/w1/ScribeLesson/receipts/03-urls-sha256.txt`) and in `corpus/SOURCES.md` row
S397.

**No credential material** appears in the candidate or in any receipt (no tokens, cookies, secret
values or vault paths; only public URLs and sha256 digests).

## 4. Census check — word counts of my own Gate quotes

`census-check.txt` lists every located quote the candidate places, with its byte offset, the file's
sha256 prefix and the measured word count. All are ≤25 words:

| row | quote | BYTE | words |
|---|---|---|---|
| S396 | generator N12 emission clause | 2615 | 18 |
| S396 | generator N12 lie literal | 2634 | 17 |
| S396 | generator N13 emission clause | 3365 | 22 |
| S396 | generator N13 lie literal | 3384 | 21 |
| S396 | checker `TOKEN` regex | 12025 | 3 |
| S396 | checker `SEPARATORS` regex | 12073 | 3 |
| S396 | checker `parse_label_set` | 12134 | 2 |
| S396 | gate `limine_version` emission | 16931 | 2 |
| S396 | gate `visibility_era` emission | 17037 | 6 |
| S397 | `re.fullmatch` sentence (de-tagged from the HTML) | 112171 | 13 |
| S397 | `\b` word-boundary sentence | 69787 | 14 |

All counts come from a `bytes.find` + whitespace split over the pinned bytes (receipt
`30-quote-word-counts.txt`).

**One anchor discrepancy found and reported, not edited.** The landed S396 row's anchor cell says
"generator emission lines at BYTE 2615 (N12) and BYTE 3384 (N13)". Measured on the pinned bytes:
2615 is the start of the N12 clause's `"limine_version": (` token, and the N13 clause's
`"limine_version": (` token starts at **3365**; 3384 is the falsified literal `"12.999999998.4"`
*inside* the same N13 clause (both offsets are on the same source line, whose start is 3344). The
row is not wrong about which code it points at — it points into the N13 clause — but it names the
clause's interior literal where the parallel N12 offset names the clause's token start, so the
candidate records both offsets explicitly and quotes each one at its own offset. `corpus/SOURCES.md`
is append-only and out of this seat's write scope, so the row was **not** edited. **The lane
independently reached the same measurement**: the L1's commit `7961738a` ("wave amendments A2-A7 and
corpus corrections (S397 quote verbatim, S396 clause-start pair, tool-without-row mistake)") records
in `corpus/lessons/round-100.md` that "BYTE 2615 is the N12 *emission clause* start; BYTE 3384 is
the N13 *lie literal* start, while the N13 emission clause starts at **BYTE 3365**", with the
lie literals at 2634 / 3384. My measurement (clause starts 2615 / 3365, literals 2634 / 3384)
agrees with it byte for byte. The candidate's offsets are therefore the corrected pair, not a
competing claim.

**The S397 quote form.** This seat's first draft of the S397 quote read "return a corresponding match
object". The page does not say that: `bytes.find(b"return a corresponding match object")` on the
fetched bytes returns **-1**, and `match object` occurs at BYTE 57131 in an unrelated table cell.
The verbatim sentence, de-tagged from the HTML at BYTE 112171, is "If the whole string matches the
regular expression pattern, return a corresponding Match." — 13 words, confirmed by this seat's own
measurement (receipt `46-s397-fullmatch-sentence.txt`) and by the L1's independent correction
(same commit `7961738a`). The candidate quotes the verbatim form.

## 5. Absence claims and their sweeps

Every "nothing else" statement in the candidate carries a sweep receipt:

| claim in the candidate | sweep receipt |
|---|---|
| the r100 generator is the only `tools/` file naming the bend names | `31-absence-sweeps.txt` S1 (1 of 1 match is `tools/make-r100-bends.py`) |
| no pre-r100 generator bends the *echo value* (a mention is not a bend) | `33-echo-bend-classification.txt`: only r96 (`N01-echo-wrong`, a blanket `limine_version_source == "flag"` lie, not component-keyed) and r100 bend the echo value; r93/r94/r95/r97/r98/r99 bend `visibility_era` or other fields only |
| the r99 battery sets `check_echo` on five families; the r98 control on three | `39-check-echo-owners.txt` |
| the Y-cap spellings and the X-cap spelling in the battery | `41-version-spellings.txt` (r99), `42-r98-spellings.txt` (r98) |
| the six/five/one fixture cells' exact registry text | `36-fixture-cells.txt` |
| the coverage gate's scope is the content gate's other rows | the r100 checker's own docstring "Named limits" (read, quoted) |

## 6. Corpus-contract conformance of the candidate

- Opens with `source:` / `verified-at:` / `recheck:` (CORPUS.md §Shape).
- Every number carries its command and date; every absence carries its sweep (CORPUS.md
  "A count carries its command", "A negative claim carries its sweep").
- Every quote names its location and its byte offset, measured at the byte level (QUALITY 141).
- No `>>` claim is made about any file this seat did not read: the files cited are
  `tools/check-limine-pins.py`, `tools/make-r100-bends.py`, `tools/check-registry-content-r100.py`,
  `tools/check-registry-content-r99.py` (the live-table and selftest control),
  `tools/limine-pin-battery-r99.py`, `tools/limine-pin-battery-r98.py`,
  `tools/check-registry-coverage.py`, the two pinned control bends, `before/dev/make-fixtures.py`
  and the twelve fixture trees this seat built — all read or executed here.
- No credential material.

## 7. Out of scope (deliberately not done)

- The candidate is **not** landed by this seat: `corpus/knowledge/limine-echo-bends-r100.md` and
  `corpus/SOURCES.md` are the L1's to write. (A version of the entry already exists in the tree,
  landed by the L1 at `c450cd68` and amended at `ef12af4c` / `7961738a`; this seat's candidate is
  independent, is written under the seat dir, and cites the receipts above.)
- No `git`/`jj` mutation, no commit, no push.
- `tools/make-r100-bends.py` and every earlier generator were **not** run.
- The owed `--selftest --reference` leg (r99 A6a), the C5 compound witness and the unbound-row
  class are not claimed; the candidate names them as limits.

## 8. Receipt index (all under this seat dir)

| receipt | content |
|---|---|
| `00-instrument-manifest.txt` | `sha256sum -c` of the frozen manifest, rc 0 (12:14) |
| `00b-manifest-after-A1.txt` | the manifest re-run after the L1's A1 plan amendment (15 OK / 1 FAILED on the plan line) |
| `01-gate-r99-stdout.txt` | landed gate, r99 battery, 3 runs |
| `02-N12-x-echo-r99-stdout.txt` | N12 under r99, 3 runs |
| `02-N13-y-echo-r99-stdout.txt` | N13 under r99, 3 runs |
| `03-N12-x-echo-r98-control-stdout.txt` | N12 under the r98 control, 3 runs |
| `03-N13-y-echo-r98-control-stdout.txt` | N13 under the r98 control, 3 runs |
| `10-count-runs-gate.txt` | `count-runs` over the gate JSON |
| `11-count-runs-bends.txt` | `count-runs` over the three bend/control legs |
| `11b-count-runs-n13-control.txt` | `count-runs` over the blind N13 control |
| `12-dev-receipt-readings.txt` | the freeze's committed dev readings, re-read |
| `13-bend-diffs.txt` | each bend's diff vs the gate (one changed line) |
| `14-census-count.txt` | SOURCES row count (398) |
| `20-fixtures-built.txt` | the twelve fixtures built in scratch |
| `21-live-table.txt` | live table, both checkers, three revisions |
| `22-fixture-matrix.txt` | twelve fixtures × two checkers |
| `23-coverage-gate.txt` | the registry coverage gate, three revisions |
| `30-quote-word-counts.txt` | byte offsets and word counts |
| `31-absence-sweeps.txt` | absence sweeps S1–S6 |
| `32-prev-generator-field-sweep.txt` | which field each earlier generator bends |
| `33-echo-bend-classification.txt` | echo-value bend classification across generators |
| `34-echo-family-sweep.txt` | the echo families' roster sites |
| `35-echo-family-spellings.txt` | the three families' docstrings/flags |
| `36-fixture-cells.txt` | each fixture's exact registry cell text |
| `37-s397-fetch-and-quotes.txt` | the S397 fetch, its sha256 and its byte anchors |
| `38-recheck-checker-leg.txt` | the checker's recheck leg, verbatim |
| `39-check-echo-owners.txt` | which families set `check_echo`, r98 and r99 |
| `40-battery-selftest.txt` | battery `--selftest` (no `--reference`) = 5/5 |
| `41-version-spellings.txt` | r99's version spellings |
| `42-recheck-battery-leg.txt` | the battery's recheck leg, verbatim |
| `42-r98-spellings.txt` | r98's version spellings |
| `44-gate-emission-sites.txt` | the gate's four emission sites, byte level and line numbers |
| `45-named-limits-and-derivation.txt` | the r100 checker's own "Named limits" and its `variant_labels` derivation |
| `46-s397-fullmatch-sentence.txt` | the `re.fullmatch` sentence: raw HTML vs de-tagged text, and the word count |
| `census-check.txt` | the row-cell word-count census |

Scratch (`/fast/scratch/hyaku/tsukuroi-r100/ScribeKnowledge`) held the battery JSONs, the fixture
trees and the two `re.html` fetches. It was deleted at the end of this seat's run with
`rm -rf /fast/scratch/hyaku/tsukuroi-r100/ScribeKnowledge` (the path was asserted to end in
`/ScribeKnowledge` first); the shared parent `/fast/scratch/hyaku/tsukuroi-r100` was left in place
and still holds only sibling seats' dirs.

{"seat":"ScribeKnowledge","verdict":"findings","notes":"Knowledge-entry candidate written under the seat dir (knowledge-draft.md + census-check.txt) with the required provenance trio (S396+S397; S397's external fetch reproduced independently: HTTP 200, 257722 bytes, sha256 69d64759..., byte anchors 111489/112171/69787). C1 re-derived on the seat's own runs: gate 105/105 met, N12 103/105 [EXPLICIT-VERSION-ECHO,REFUSAL-VERSIONS-9DIGIT], N13 104/105 [REFUSAL-VERSIONS-9DIGIT-Y], r98 control N12 104/105 [EXPLICIT-VERSION-ECHO] and N13 105/105 met, 0 error rows, one changed line per bend, battery selftest 5/5. C2 re-derived: live table PASS 7/7 findings 0 for both checkers at three revisions, r100 selftest 26/26, r99 17/17, twelve fixture cells match the frozen reading (six acceptance PASS, five fail-closed with the frozen ids, GAP PASS on both). Every expected line of both claims verified PASS on the seat's own runs; the verdict is 'findings' because two disclosed discrepancies were found, neither edited by this seat: (1) the manifest's .ufo/plans/round-100.md line now FAILS (15 OK / 1 FAILED) after the L1 appended amendment A1 at 12:28 and further amendments at 7961738a — all 15 instrument bytes are unchanged and every measurement was taken against them; (2) S396's anchor names BYTE 3384 for the generator's N13 emission line while that clause starts at 3365 (3384 is the lie literal inside it; N12 clause 2615, literal 2634) — the lane reached the same measurement independently in commit 7961738a, and this seat's candidate carries the corrected pair. Registry coverage gate reads PASS at the landing tip 69474c55 (165/165) and FAIL with two REGISTRY-ROW-MISSING at the pre-landing freeze revision 743ce449 (reported as found). All 11 located quotes are <=25 words."}
