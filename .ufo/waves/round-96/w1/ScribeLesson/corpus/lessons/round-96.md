# Round 96 lesson — tsukuroi lane

Draft by the seat `ScribeLesson` (wave w1) for the L1 to integrate. Every number below carries the
command that produced it; the receipts live under
`.ufo/waves/round-96/w1/ScribeLesson/receipts/`.

Pre-round tip `73c47107e8bda79375517ee24ec3c13688586305`; freeze `38adc4ed`; the lesson's own
landed-tree reading is HEAD `a814f24dc31270bca4e8999ac3cd907ecd72f100`.

## Gate (sources opened this round; contract `CORPUS.md` §SOURCES.md)

Candidates opened 2026-11-08 by this seat. The pin bytes are under `ScribeLesson/pins/`; the fetch
log and digests are `receipts/01-gate-sources.sha256.txt`; the located quotes with their byte
offsets are `receipts/02-gate-located-quotes.txt`; the refusals are `receipts/05-gate-rejections.txt`.

| row | URL opened | tier | located quote (≤25 words) | admit / reject |
|---|---|---|---|---|
| S390 (candidate, new) | https://docs.python.org/3/library/sys.html#sys.int_info.default_max_str_digits | A | "The default value for sys.get_int_max_str_digits() when it is not otherwise explicitly configured." (raw byte 157851 of the 280632-byte pin, sha256 `a7e00587…`) | **admit** — the configured default of CPython's decimal-conversion digit limit; it names the value a parser that hands a component to `int()` must bound itself against. It states no Limine behaviour and is not offered as one. |
| S389 (re-opened) | https://docs.python.org/3.15/library/stdtypes.html#integer-string-conversion-length-limitation | A | "The default limit is 4300 digits as provided in sys.int_info.default_max_str_digits." (raw byte 785297 of the 815447-byte pin, sha256 `6bf2ce2b…`) | **admit** (re-open; byte-identical to the r95 pin) — the 4300-digit default the gate's 1-9-digit per-component cap sits under. |
| S382 (re-opened) | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.5/common/lib/config.c | A | "*(p - 1) = '\0';" (raw byte 10046, line 329; pin sha256 `a940acae…`) | **admit** (re-open) — the in-place config cut that dates the era boundary to the v12.9.5 tag. |
| S383 (re-opened) | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.5/ChangeLog | A | "Parse the config in linear time. Configs with thousands of entries were slow to load." (raw byte 168, line 8; pin sha256 `d2e08cc4…`) | **admit** (re-open) — upstream's own release note for the in-place config parse. |
| S384 (re-opened) | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.5/host/limine.c | A | "puts(\"Limine \" LIMINE_VERSION);" (raw byte 67028, line 2035; pin sha256 `4da21c7c…`) | **admit** (re-open) — the `--version` line the installed-version probe parses. |
| S386 (re-opened) | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/common/lib/config.c | A | byte-identical to the v12.9.5 file (both pins sha256 `a940acae…`) | **admit** (re-open) — the v12.9.6 tag carries the same config.c bytes. |
| S387 (re-opened) | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/ChangeLog | A | "A config whose first line is an entry has had no global options since 12.9.5." (raw byte 476, line 14; pin sha256 `ab280b45…`) | **admit** (re-open) — upstream's own sentence for the 12.9.5 visibility boundary the era families rely on. |
| S388 (re-opened) | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/host/limine.c | A | "puts(\"Limine \" LIMINE_VERSION);" (raw byte 67028, line 2035; pin sha256 `4da21c7c…`) | **admit** (re-open) — byte-identical to the v12.9.5 `host/limine.c`. |

Rejected candidates this round, with the observed status and body (`receipts/05-gate-rejections.txt`):

- `https://man.archlinux.org/man/limine.8` → **HTTP 404**, 2706 bytes, `<title>Page not found — Arch
  manual pages</title>`. No such man page exists; the body is the site's own error page and states
  no Limine behaviour. **reject.** (The same URL was refused in r94 and r95; the refusal repeats
  rather than being a new finding.)
- `https://api.github.com/repos/Limine-Bootloader/Limine/releases/tags/v12.9.6` → **HTTP 200**,
  26652 bytes, `tag_name` `v12.9.6`, body 512 characters whose first sentence is "Changelog can
  be found [here](…/blob/v12.9.6/ChangeLog)." and whose rest is the tarball-signature text. It
  states no Limine behaviour. **reject as a registry row**; it stays a wave-directory locator.
  (The same URL was refused in r94 and r95.)
- `https://man.archlinux.org/man/limine.conf.5` → **HTTP 404**, 2725 bytes. No such page.
  **reject.**

### The census, before and after

The frozen command (contract `CORPUS.md`): `bash
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census|validate --root
/home/vgpnk/Projects/shokunin tsukuroi`. Full output: `receipts/06-census-before-after.txt`,
`receipts/census-validate-pre.txt`, `receipts/census-validate-after.txt`.

- **Before** (the pre-round tree, `git archive 73c47107`): `census` → **389 rows**, `exit 0`;
  `validate` → **exit 0**, 0 E-findings, 58 W-findings, 59 output lines.
- **After** (HEAD `a814f24d`): `census` → **390 rows**, `exit 0`; `validate` → **exit 0**, 0
  E-findings, 58 W-findings, 59 output lines. The two `validate` outputs differ only in the lane
  prefix (`file` → `tsukuroi`); every code and every row id is unchanged.
- The row count straight from the committed blobs
  (`git show <rev>:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}'`): `73c47107` → 389,
  `38adc4ed` → 389, `59cbfe2f` → **390**. Exactly one row was added this round: **S390**, tier A.
- Rows touched old→new in place: **none**. S390 is new; no `status`, `recheck` or `used-by` cell of
  any earlier row was edited, so no append-only log entry is owed under `CORPUS.md` rule 2.

### A locator defect this seat found in the round's own new row

**R96-S390-LOCATOR-BYTE.** The S390 row's `anchor` cell reads "`sys.int_info.default_max_str_digits`
attribute, byte 157653 of the 2026-11-08 pin (sha256 `a7e00587…`)", and the same byte is bound to
the quoted sentence in `corpus/knowledge/limine-bound-per-component-r96.md:19` and in the
integrated `corpus/lessons/round-96.md`. Measured on that exact pin
(`receipts/03-s390-locator-byte.txt`, `receipts/check-s390-locator.py`):

| what | measured raw byte |
|---|---|
| `<dt … id="sys.int_info.default_max_str_digits">` opening tag | 157495 |
| `id="sys.int_info.default_max_str_digits"` | 157525 |
| **byte 157653, as cited** | lands inside the opening tag `<span class="sig-name descname">` (that tag opens at 157648) |
| visible name `default_max_str_digits` | 157698 |
| start of the quoted sentence "The default value for …" | 157851 |

The sibling row S389, in the same registry and the same page family, cites four bytes and **all
four are exact** (780197 → `<section id="integer-string-conversion-length-limitation">`; 780256 →
`<span id="int-max-str-digits">`; 785297 → "The default limit is 4300 digits"; 782228 → "When an
operation would exceed the limit,"). So the convention is unambiguous: a cited byte is the exact
start of the element or sentence it names. **157653 is the start of nothing it names**, and it sits
198 bytes before the sentence the knowledge entry and the lesson bind it to.

`receipts/check-s390-locator.py` is the check, and it **fails** on the pre-correction locator:
`--row old` prints `S390 byte 157653 -> measured 157525 FAIL` and `locators 5, failing 1`,
**exit 1**; the same script over the four S389 locators prints four `PASS` lines. A check that
cannot fail is not a check.

**Closed at `8fdb05e1`.** The L1 corrected the row's anchor cell to "`sys.int_info.default_max_str_digits`
attribute (id at byte **157525**; quoted sentence starts at byte **157851**, split by a code
element) of the 2026-11-08 pin (sha256 `a7e00587…`)", and the same commit corrected
`corpus/knowledge/limine-bound-per-component-r96.md` and this lesson's integrated copy. The check
now reads `--row new` → five `PASS` lines, `locators 5, failing 0`, **exit 0**
(`receipts/13-locator-check-both-readings.txt`) — the same script, the same pins, the only change
the byte the row cites. Both readings are kept in the receipt, so the defect stays re-derivable.
(The "split by a code element" clause is itself part of the correction's precision: in the raw
bytes the sentence's first words sit at 157851 and a `<code>` element splits it before
`sys.get_int_max_str_digits()`, so a reader must not expect the whole sentence to be contiguous —
which is exactly why a byte that names *the element* is the stable locator and a byte that names
*the sentence* needs the caveat.)

Class: `calibration` (a locator in the lane's own self-assessment that does not resolve against the
bytes it names — the same family as the six routed r95 classes C2 counts). The row's proposition is
true and its quote is verbatim; only the **locator** was wrong. Captured-by: **none** — the census
(E01-E12) validates row *shape*, not whether a cited byte lands on the thing the cell names, and
`QUALITY.md` 21 (R15-LOCATOR) asks for "a stable source heading/fragment, exact quote and observed
revision or access date", which the row satisfies without ever resolving the byte. Fix: applied —
the anchor cell now cites a byte that resolves, and the byte was re-derived from the pinned bytes
rather than recorded from memory. The r95 lesson already warns that this page's digest is
Sphinx-stamp dependent ("Last updated on Nov 08, 2026" is a moving line), so the correction must
re-verify by title, attribute id and byte offset, never by the digest alone. **Still open for
r97:** nothing in the lane checks a *byte* locator — the census checks row shape and QUALITY 21
asks for a stable fragment. A registry-wide check that every cited byte resolves (the script here
is a two-row prototype) would catch the next one before it lands.

## Mistakes

- **R96-FRONTIER-NOT-SENT** — class: `calibration` (self-assessment vs the instrument's bytes).
  Round 95's README Frontier bullet said the four-component extra-component shape was "not sent at
  battery level": `git show 73c47107:corpus/README.md | grep -n '12\.9\.6\.1'` → line 1147, "Still
  open from r94: the `12.9.6.1` extra-component shape (not sent at battery level)". The battery's own
  roster contradicts the class claim: `grep -n 'REFUSAL_VERSIONS = ' tools/limine-pin-battery-r96.py`
  → line 1662, `REFUSAL_VERSIONS = ("12.9", "12.9.5.1", "abc", …)` — and the same tuple was already
  in the r95 battery (`git show 73c47107:tools/limine-pin-battery-r95.py | grep -n 'REFUSAL_VERSIONS
  → line 1643, identical). **The class was sampled before this round** (`12.9.5.1`), so
  `EXTRA-COMPONENT` broadens a class rather than closing a first. Evidence pointer:
  `receipts/04-mistakes-evidence.txt` §(a); the two-family bend reading in §(b) of the same
  receipt. Captured-by: **none** (the Frontier bullet was not re-derived against the instrument
  before it was published). Fix: the r96 declaration records the class as broadened rather than
  first, the README correction names the pre-existing row, and the round's own C2 predicate counts
  it. **And the class was sampled *twice* before this round, not once — a correction the r96
  README's own wording understates.** The r95 battery's `--usage-check` leg sends `12.9.6.1`
  itself and expects rc 64 (`tools/limine-pin-battery-r95.py:2300`, the case list
  `[("12.9", 64), ("abc", 64), ("12.9.6.1", 64), …]`), and on the N04 bend that leg reads
  **unmet** — the bent gate answers rc 0 where 64 is wanted (`receipts/10-r95-usage-check-leg.txt`;
  the failing case is `{'version': '12.9.6.1', 'want_rc': 64, 'rc': 0, 'ok': False}`). So the
  four-component *shape* reached the r95 instrument twice — once as the roster row `12.9.5.1` and
  once in the usage leg `12.9.6.1` — and r96's `EXTRA-COMPONENT` is the **third** send of the same
  shape. The round-96 README's "the class was sampled once, and r96 broadens it" is true of the
  **family roster** and false of the instrument; the r95 spot-check §6 item 5 made exactly this
  distinction for the r94 in-bound case ("the sentence is scoped to the roster, not the
  instrument"), and the round-96 correction re-opens the same scope slip in the other direction.
  Fix: the correction must name which surface was sampled how many times (roster once, usage leg
  once, r96 family once), and the r97 Frontier must say so rather than counting the class once.

- **R96-N04-TWO-FAMILIES** — class: `calibration` (a frozen target clause against the instrument's
  actual reading). The bend `N04-extra-components` does not fail one family: it fails **two**.
  Measured twice, identically:
  `python3 tools/limine-pin-battery-r96.py --gate
  .ufo/waves/round-96/before/controls/bends/N04-extra-components.py --runs 1 --work <scratch>
  --json <out>` → `verdict unmet`, `families_passed 101/103`, `failed_families ['EXTRA-COMPONENT',
  'REFUSAL-VERSIONS']`, 412 cases, **0 error rows**; and the frozen pre-freeze development run
  `.ufo/waves/round-96/before/dev/N04-extra-components.json` → the same `101/103`, the same
  two-family list, 0 error rows (`receipts/04-mistakes-evidence.txt` §(b)). The second member is
  the **pre-existing** `REFUSAL-VERSIONS` row: its roster value `12.9.5.1` is also a four-component
  version, so the bend's one-clause grammar change (`len(parts) != 3` → `len(parts) < 3`) releases
  that row too. Evidence pointer: the two receipts named above, and the roster tuple at
  `tools/limine-pin-battery-r96.py:1662`. Captured-by: **QUALITY 140** (a target clause re-read
  against one development run before the freeze) — the correction was caught *before* the freeze
  (the dev run is committed under `before/dev/`), which is the rule working, not the rule failing.
  Fix: the frozen target states the two-family set exactly, the report prints the raw
  `failed_families` list, and the plan records that the class was broadened. **What the rule does
  not yet cover:** QUALITY 140 asks the L1 to compare *every clause* of the target against one
  development run; the N04 reading was caught, but the run's *error-row field* was not inspected
  for the same bend family set — see R96-N02-ERRORROWS below, which is the same class one round
  later and shows the rule needs a per-field reading, not a verdict-line reading.

- **R96-N02-ERRORROWS** (the r96 twin of the N04 miss) — class: `calibration` (frozen target vs
  instrument reading). The frozen C1 target says every bend leg carries "0 error rows". The N02 bend
  refuses the four Y-family cases (rc 64, empty stdout, no JSON), so its receipt carries **four**
  `error` rows per run. The r96 plan's amendment **A3** narrows the clause accordingly. Evidence:
  the amendment file `.ufo/waves/round-96/before/plan-amendments-A1-A2.md` (A3), and the seat
  receipts `w1/ExecBend/bend-N02-y-cap-8.json` and `w1/ExecBattery/c1-bend-N02-y-cap-8.json`. This
  seat's own runs corroborate the shape without re-deriving it: the N04 bend reading above has 0
  error rows, and `MutBound`'s matrix shows the N02 bend at `102/103 unmet` with **4** error rows
  while N01/N03/N04 carry 0. Captured-by: **QUALITY 140** (the rule existed; the L1's development
  run printed the verdict but did not inspect the error-row field). Fix: A3's narrowing, and the
  report prints the per-leg error-row counts.

- **R96-REPORT-WORD-COUNT** (the routed r95 report-count miss) — class: `calibration` (report
  prose against the committed ledger). Round 95's filed report wrote **"four**
  `falsifies-wording` **rows"** (`.ufo/reports/round-95/tsukuroi.md:219`, verbatim: "the artifact
  column; the four `falsifies-wording` rows point at A2/A3/A4 and the one"). The committed ledger
  `.ufo/waves/round-95/claim-falsification.tsv` holds **six**: `grep -c 'falsifies-wording'` → 6,
  `grep -c 'falsifies-number'` → 1, `grep -c ''` → 21 rows total. The count was wrong by two, in
  the round that also produced the A2/A3/A4 narrowings the rows name — the sentence under-counted
  the very rows it cited. Evidence pointer: `receipts/04-mistakes-evidence.txt` §(c). Captured-by:
  **none in r95** — the spot-check caught it by reading the ledger; r96's C2 **F6** makes the
  sentence machine-checkable. Fix: F6 binds the report's count sentence to the ledger's committed
  counts, and the round's own report states the numeral the checker compares. **The round's own
  report closes the miss end to end** (`receipts/12-f6-end-to-end.txt`): the committed r96 ledger
  holds **3** `falsifies-wording`, **1** `falsifies-number` and **7** neutral over **11** rows
  (`awk -F'\t' 'NF>1{c[$3]++} …'`), the filed r96 report says exactly that
  (`.ufo/reports/round-96/tsukuroi.md:64`, "3 falsifies-wording rows and 1 falsifies-number row,
  plus 7 neutral"), and `check-r96-calibration.py --root . --report <r96 report> --tsv
  .ufo/waves/round-96/claim-falsification.tsv` reads `status PASS`, `findings []`, **exit 0**.
  **And the r95 sentence fails F6 for a second reason worth recording:** F6's regex is
  `(\d+)\s+.?falsifies-wording` — a *numeral* — and the r95 report spells the count as the **word**
  "four", so the checker cannot bind a count at all and reports "report states no
  falsifies-wording count" (measured: the same checker against the r95 report and the r95 ledger
  reads `status FAIL` with F6 twice). The routed defect was therefore not only a wrong number but
  an unbindable one; a round whose report writes the count in words passes no check at all.
  **A limit of F6 worth recording (measured, from the checker's own source):** F6 binds the *first*
  numeric occurrence of each class in the report text, so a truthful report that quotes the r95
  wrong count first is rejected — the r96 plan's amendment **A5** records this narrowing.

- **R96-FRONTIER-COUNTED-ONCE** (the round's own correction undercounts) — class:
  `calibration` (a frontier sentence against the instrument's own case list). The round-96 README
  correction reads: "the r95 Frontier sentence that said the four-component shape was not sent at
  battery level is corrected: **the class was sampled once**, and r96 broadens it"
  (`corpus/README.md:1163`). Measured, the class reached the r95 instrument **twice**:
  `tools/limine-pin-battery-r95.py:2300` sends `("12.9.6.1", 64)` in the `--usage-check` leg, and
  on the N04 bend that leg reads **unmet** with the failing case
  `{'version': '12.9.6.1', 'want_rc': 64, 'rc': 0, 'ok': False}`
  (`receipts/10-r95-usage-check-leg.txt`); the roster row `12.9.5.1` is the second send
  (`tools/limine-pin-battery-r95.py:1643`). r96's `EXTRA-COMPONENT` is the third. The sentence is
  true of the **family roster** and false of the **instrument** — exactly the roster-vs-instrument
  scope slip the r95 spot-check §6 item 5 caught in the r94 case and that r95's A4 fixed there.
  The correction re-opens the same slip in the other direction. Captured-by: **none** (nothing
  re-derives a correction's own count against the instrument it corrects). Fix: the sentence must
  name the surface and the count (roster once, usage leg once, r96 family once) — the form the r95
  lesson's A4 uses. **Closed at `8fdb05e1`**: the README sentence now reads "the class reached the
  r95 instrument **twice** (the roster's `12.9.5.1` row and the `--usage-check` value
  `12.9.6.1`), and r96 broadens it a third time" (`corpus/README.md:1164`, verbatim from
  `git show 8fdb05e1 -- corpus/README.md`).

- **R96-S390-LOCATOR-BYTE** — the locator defect described in `## Gate` above: the round's own new
  registry row cited a byte that landed inside an HTML attribute rather than on the element or
  sentence it names, while the sibling row S389's four bytes were exact. Class: `calibration`.
  Captured-by: **none** (the census validates row shape, not byte resolution). Fix: applied at
  `8fdb05e1` — the anchor cell now cites bytes that resolve, and
  `receipts/check-s390-locator.py --row new` reads `locators 5, failing 0`, **exit 0**
  (`receipts/13-locator-check-both-readings.txt`); `--row old` keeps the defect re-derivable at
  exit 1.

## Routed

The r95 spot-check (`corpus/lessons/round-95-verifier-spotcheck.md` §6) routed seven items. This
round's treatment, each with the receipt that carries it:

| r95 routed item | r96 treatment | evidence |
|---|---|---|
| 1 — report prose count ("four" vs six `falsifies-wording` rows) | **closed for r96** by C2's F6, which binds the report's count sentence to the committed ledger; the r95 filed bytes stay as they are. The r96 report states the numeral its own ledger holds (3 / 1 / 7 over 11 rows) and the checker reads `PASS`, `findings []`, exit 0 against the landed tree. | `receipts/04-mistakes-evidence.txt` §(c); `receipts/08-c2-calibration.txt`; `receipts/12-f6-end-to-end.txt` |
| 2 — `corpus/QUALITY.md` owes M1 a criterion | **closed** — QUALITY 140 exists and cites the lesson, the mistake id and a development run. | `receipts/11-routed-closures.txt` §routed 2 (the checker's own `criterion_block(q,140)` → found, and `round-95.md`/`M1`/`development run` all present) |
| 3 — C2's void clause has a dead pointer | **closed** — `.ufo/waves/round-96/before/r95-registry-gate.sha256` records the registry gate's sha256 (`6fcb2d0a…`, equal to the current `tools/check-registry-coverage.py`), the r96 freeze manifest pins the same hash, and `SCORECARD.md`'s "## Round 96" section binds the clause to an empty `git diff`. | `receipts/11-routed-closures.txt` §routed 3 |
| 4 — superseded superlative left standing in frozen r95 tool docstrings | **closed** — both r95 tools now say "boundary member" and no longer say "largest in-bound" (`grep -c`: 0 and 4 / 0 and 1); the edits are docstring-only (ASTs equal modulo docstrings); the relation to the r95 freeze manifest is stated in the next section. | `receipts/09-r95-freeze-manifest-relation.txt`; `receipts/11-routed-closures.txt` §routed 4 |
| 5 — `corpus/README.md` A4 over-scope | **closed** — the sentence is scoped to the r94 family roster (`grep -c 'r94 family roster'` → 1; `grep -c 'before instrument has no in-bound'` → 0). | `receipts/11-routed-closures.txt` §routed 5; `receipts/08-c2-calibration.txt` (F4 reads 0 findings at the landed tree) |
| 6 — derived, not measured, C2 revisions | **closed** — `.ufo/waves/round-96/before/c2-tip-b8f878c8.json` is a committed receipt: `status PASS`, `revision b8f878c88fa795fbf20d6129807dfc5222e5fadf`, `tools_total 151`, `registered 151`, `findings 0`. | `receipts/11-routed-closures.txt` §routed 6; `receipts/08-c2-calibration.txt` |
| 7 — carried Frontier rows | **still open**, except the four-component entry, which this round corrects (R96-FRONTIER-NOT-SENT above). The r92 launcher residuals, the r93 probe pre-release caveat, r89's blanks-before-CRLF / ESP containment / empty labels, and the registry gate's missing name→path/content binding stay Frontier. | `receipts/11-routed-closures.txt` §routed 7; `corpus/README.md` "### Frontier (round-96 addition)" |

**The r96 spot-check has not been written yet** — this lesson is written before the r96 verifier
spot-check exists, so the `## Routed` list above is the r95 queue only. A round-96 spot-check
should also route the two findings this seat measured that no queue currently carries:

- **R96-S390-LOCATOR-BYTE** (in `## Gate` above): a registry `anchor` cell whose cited byte did
  not resolve against the pinned bytes it names — a defect the census (E01-E12) cannot see and no
  round has yet ruled on. **Closed at `8fdb05e1`** (the row, the knowledge entry and the integrated
  lesson were corrected together); **still open for r97** as a *rule*: nothing in the lane checks a
  byte locator, and `receipts/check-s390-locator.py` is a two-row prototype of the registry-wide
  check that would catch the next one before it lands.
- **R96-FRONTIER-COUNTED-ONCE** (in `## Mistakes` above): the round's own README correction said
  the four-component class "was sampled once"; the instrument sampled it twice (roster row
  `12.9.5.1` and the usage leg `12.9.6.1`). The r95 spot-check §6 item 5 made the same
  roster-vs-instrument distinction for the r94 in-bound case; the r96 correction re-opened it.
  **Closed at `8fdb05e1`** — the sentence now names the surface and the count.

**Carried from round 94's spot-check §6, as the r95 lesson left it.** r94 routed 1 (the registry
rows) is closed by C2; r94 routed 8 (the declared-and-unused `REFUSAL_DIGIT9`) is closed by C1's
`REFUSAL-VERSIONS-9DIGIT`; r94 routed 9's second half (the `<= 8` gate reads `met`) is closed by
the frozen bend `N05-strict-8`; r94 routed 4 (the do-nothing arithmetic and the stderr clause) is
corrected in the r95 report and lesson; r94 routed 9's first half (the extra-component shape) is
the entry this round corrects (R96-FRONTIER-NOT-SENT); r94 routed 10 (the contested
kaidoku/revenger RE ownership) remains **operator-owned, reported, not absorbed**. The r93 queue
items the r94 lesson left unmapped — routed 4's M12 timeout survivor and routed 5's
**probe-grammar leniency** (the first-`X.Y.Z` parse reads `12.9.6-rc1` as `12.9.6`, and no family
sends the probe answer `Limine 12.9.6.1`) — remain open. **Note for r97:** the r96 `EXTRA-COMPONENT`
family now sends four-component *flag values*, not the probe answer `Limine 12.9.6.1`, so r93
routed 5's probe-side half is still uncovered — the two must not be merged.

**The three new families' own limits, as measured by this seat.** The r95 do-nothing battery is
blind to all three new families and reads `met 99/99` on the landed gate; on the N04 bend it reads
`98/99 unmet` with `failed_families ['REFUSAL-VERSIONS']` — the pre-existing row, not the new
family (`receipts/07-do-nothing-blindness.txt`). That is the blindness receipt C1's target asks
for, and it also shows the four-component class is not new to the instrument. The r96 battery's own
survivors are in `w1/MutBound/matrix.md` (M06 Z-cap, M07 echo-lower and M08 refusal-below-1e8 read
`met 103/103`), so the era label, the echo and the Y cap are each certified on one direction only.

## Relation to the r95 freeze manifest

The r95 freeze manifest (`.ufo/waves/round-95/before/instruments.sha256`) pins the **r95 landed**
bytes. Round 96 corrects two of those files' **docstrings** (r95 routed 4: the "largest in-bound
member" superlative is false under a per-component cap), so the manifest no longer verifies in the
working tree — and that is expected, disclosed, and re-derivable. Measured
(`receipts/09-r95-freeze-manifest-relation.txt`):

```
$ sha256sum -c .ufo/waves/round-95/before/instruments.sha256
tools/check-limine-pins.py: OK
tools/limine-pin-battery-r95.py: FAILED
tools/make-r95-bends.py: FAILED
... (the other seven lines: OK)
sha256sum: WARNING: 2 computed checksum(s) did NOT match
exit=1
```

The pinned bytes are re-derivable at the r95 landed commit, exactly as the plan's Limits section
states:

```
$ git show b8f878c8:tools/limine-pin-battery-r95.py | sha256sum
a51dca18d3c7641664a2f64476a7abc2bb14ff1133772f109ac73490828b9ebb  -
$ git show b8f878c8:tools/make-r95-bends.py | sha256sum
57669e190e3e695956c0c4bca4302050daef62dd1b3ce8f9d7f98b869ba97554  -
$ git show b8f878c8:tools/check-limine-pins.py | sha256sum
7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32  -
```

— the three digests the r95 manifest pins, to the byte.

**The edits are wording, not behaviour**, and that is measurable rather than asserted: parsing both
the `b8f878c8` blobs and the current files with `ast`, stripping the leading docstring of every
module / class / function, and comparing `ast.dump`, gives **equal** ASTs for both files
(`receipts/ast-docstring-only.txt`). The current bytes are
`e19d3c0b50aa07dba3ab8b5646314d39ab9bb721e754eaa8bd4c3fb96de9dcf5`
(`tools/limine-pin-battery-r95.py`) and
`bbcb18f3c2b1c80e6ed375249bffb53fcc1def7d1043bb2e75e1452ba1003da7`
(`tools/make-r95-bends.py`); the unchanged gate is still
`7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32`.

The **round-96** manifest verifies in full: `sha256sum -c
.ufo/waves/round-96/before/instruments.sha256` → 17 lines **OK**, 0 FAILED, exit 0. The historic
r95 manifest is not rewritten; the correction is recorded as an append-only relation here, which is
what the plan's Limits section promised.

**One caveat the L1 must carry.** The `tools/make-r95-bends.py` digest quoted above
(`bbcb18f3…`) is the byte state after the L1's wrap-only reflow (plan amendment **A2**). The
word-only diff the correction installs is the `largest in-bound member` → `boundary member`
replacement in both files' docstrings; the reflow is a separate, disclosed packaging repair that
changes no AST. A reader who wants the "docstring edit only" claim in isolation should re-derive it
from the AST equality above, not from the digest.
