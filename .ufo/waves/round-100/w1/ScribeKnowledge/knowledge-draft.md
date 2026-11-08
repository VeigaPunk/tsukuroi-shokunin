source: tools/make-r100-bends.py @ 743ce449 + tools/check-registry-content-r100.py @ 743ce449 (S396, S397)
verified-at: 2026-11-08
recheck: `python3 tools/limine-pin-battery-r99.py --gate .ufo/waves/round-100/before/controls/bends/N13-y-echo.py --runs 1 --work <scratch>` must print `families_passed 104/105 verdict unmet failed REFUSAL-VERSIONS-9DIGIT-Y` and exit 1; `python3 .ufo/waves/round-100/before/dev/make-fixtures.py <dir> && python3 tools/check-registry-content-r100.py --root <dir>/SEP-SPACE` must print `registry-content: status PASS bindings 7/7 findings 0` and exit 0 while `python3 tools/check-registry-content-r99.py --root <dir>/SEP-SPACE` prints `FINDING RC-CELL-MISSING` and exits 1.

# The echo legs get spelling-targeted bends, and a registry cell becomes a label set

Round 100 adds no family to any battery and changes no pin rule. What it adds is two *articles* —
one-clause bends of the unchanged gate — and one *capture* that stops reading a registry cell as a
span string and reads it as a set of labels. The first closes the round-99 Frontier sentence "The
X/Y **echo** legs have no spelling-targeted committed bend" on the Y side and narrows it on the X
side; the second closes the two round-99 named capture limits, "the capture's alphabet is still
`N<digits>` with no space token" and "a registry cell that legitimately states two spans in one cell
must be rewritten to one span".

Every number below carries the command that produced it, and every absence carries its sweep
(CORPUS.md §Rules: "A count carries its command", "A negative claim carries its sweep"). Byte
offsets are measured at the byte level on the pinned bytes with `bytes.find` / `grep -abo`, never
from a decoded string's index (QUALITY 141).

## 1. The two instruments, and the bytes they are anchored on

The gate is unchanged: `tools/check-limine-pins.py`, sha256
`7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32`, verified by
`sha256sum -c .ufo/waves/round-100/before/instruments.sha256` (16 entries, all OK, rc 0 —
`.ufo/waves/round-100/w1/ScribeKnowledge/receipts/00-instrument-manifest.txt`; the manifest also pins
`.ufo/plans/round-100.md`, whose line reads FAILED after the lane appended its A1 amendment to that
file at 12:28 — every *instrument* byte, all 15 of them, still verifies, and the receipt
`…/receipts/00b-manifest-after-A1.txt` shows both runs). The gate reports the
flag's version in the JSON it returns; the MAIN return emits `"limine_version": limine_version,` at
BYTE 16931 and `"visibility_era": "12.9.5+" if era_b else "pre-12.9.5",` at BYTE 17037, and the
CANNOT-EVALUATE early return carries copies of the same two lines at BYTE 11230 and BYTE 11344 —
`grep -abo` over `tools/check-limine-pins.py`, receipt `…/receipts/30-quote-word-counts.txt` and
`…/receipts/44-gate-emission-sites.txt`.

`tools/make-r100-bends.py` (sha256 `7ccfe69e52604ec5bb8db423e377cf9f0eb468baf03d0ef7be77b3209654e695`,
4471 bytes) emits the two bends; `tools/check-registry-content-r100.py` (sha256
`7a23a522871ab5dd33a94ae51b09c70ab182a0d2a53d7380f82bb11a13f3c2d2`, 38009 bytes) is the label-set
capture. The generator's two emission clauses are at BYTE 2615 (N12) and BYTE 3365 (N13) of the
generator — the second is the start of the `"limine_version": (` token of the N13 clause, while the
row S396 anchors at BYTE 3384, the falsified literal *inside* that same clause; both offsets are
recorded and quoted in `…/census-check.txt`, and neither names a byte the other does.

The generator refuses a substitution that does not match exactly one site and refuses a
substitution that changes nothing (`tools/make-r100-bends.py`, VARIANTS/loop), so a bend cannot be a
no-op dressed as a control.

## 2. What each bend asks of the battery

A bend that changes only the returned `limine_version` line, keyed on one version component, asks
one question of the unchanged r99 battery: *does the family that sends this spelling read the
field it certifies?* Pins, `rc` and `visibility_era` are computed from the true value in both
bends, so the only family whose expected answer can move is one that reads the echo.

| bend | key | falsifies the echo exactly when | generator clause (BYTE) |
|---|---|---|---|
| `N12-x-echo` | FIRST component is `999999999` | the X-cap spelling `999999999.9.9` | 2615 |
| `N13-y-echo` | SECOND component is `999999999` | the Y-cap spellings `12.999999999.4`, `0.999999999.0` | 3365 |

Each bend's diff against the gate is exactly one changed line: `diff -u tools/check-limine-pins.py
.ufo/waves/round-100/before/controls/bends/<bend>.py` prints one `-` line and one `+` line, and
`diff … | grep -c '^<'` / `grep -c '^>'` each print `1` for both bends (this seat's own receipt
`…/receipts/13-bend-diffs.txt`; the diff is against the pinned control bends, whose bytes the
manifest above verifies).

## 3. What the bends prove — and what they do not

### 3.1 The measured readings

Counting command (the claim's own): `python3 tools/limine-pin-battery-r99.py --gate <ARTICLE> --runs
3 --work <scratch> --json <out>`, then `python3
.ufo/waves/round-95/before/controls/count-runs.py <out> --family REFUSAL-VERSIONS-9DIGIT --family
REFUSAL-VERSIONS-9DIGIT-Y --family EXPLICIT-VERSION-ECHO`. The freeze's development runs (one run
each) are committed under `.ufo/waves/round-100/before/dev/`; this seat re-ran every leg at three
runs. Both readings agree.

| article | instrument | families_passed | failed_families (exact) | error rows |
|---|---|---|---|---|
| landed gate | r99 battery | 105/105 `met` | `[]` | 0 |
| `N12-x-echo` | r99 battery | 103/105 `unmet` | `[EXPLICIT-VERSION-ECHO, REFUSAL-VERSIONS-9DIGIT]` | 0 |
| `N13-y-echo` | r99 battery | 104/105 `unmet` | `[REFUSAL-VERSIONS-9DIGIT-Y]` | 0 |
| `N12-x-echo` | r98 battery (do-nothing control) | 104/105 `unmet` | `[EXPLICIT-VERSION-ECHO]` | 0 |
| `N13-y-echo` | r98 battery (do-nothing control) | 105/105 `met` | `[]` | 0 |

Each of the three runs of each leg carries the same verdict, the same exact failed-family set and
0 error rows (`…/receipts/11-count-runs-bends.txt` for the three r99/control legs,
`…/receipts/11b-count-runs-n13-control.txt` for the blind N13 control; the JSONs are the seat's own
scratch files).
The per-family detail the counter prints is the delta's own arithmetic: on `N12-x-echo` under r99
the family `REFUSAL-VERSIONS-9DIGIT` reads 0 passed / 4 failed and `EXPLICIT-VERSION-ECHO` reads 3
passed / 1 failed, while `REFUSAL-VERSIONS-9DIGIT-Y` reads 4 passed / 0 failed; on `N13-y-echo` only
`REFUSAL-VERSIONS-9DIGIT-Y` moves (0/4) and the other two stay 4/0.

### 3.2 The Y leg is a met-to-unmet closure

`N13-y-echo` falsifies the echo for the two Y-cap spellings `12.999999999.4` and `0.999999999.0`
(`grep -oE '"[0-9]{1,9}\.[0-9]{1,9}\.[0-9]{1,9}"' tools/limine-pin-battery-r99.py | sort -u` lists
both; receipt `…/receipts/41-version-spellings.txt`). The r98 control reads `met 105/105` on that
article — it is blind, so the r99 battery's `REFUSAL-VERSIONS-9DIGIT-Y` is the only witness, and
that family is the only one whose expected answer moves (104/105 vs the gate's 105/105). This is a
closure in the strict sense: the family that asserts the echo on the Y-cap spelling fails under a
gate that lies there, and no other family is affected.

### 3.3 The X leg is a one-family delta, never a flip

`N12-x-echo` falsifies the echo for `999999999.9.9` — the spelling the r96
`EXPLICIT-VERSION-ECHO` family already sends (`EXPLICIT_VERSION_META = ("12.9.4", "12.9.5",
"12.9.6", REFUSAL_DIGIT9)` with `REFUSAL_DIGIT9 = "9" * 9 + ".9.9"`, measured from
`tools/limine-pin-battery-r99.py`; receipt `…/receipts/41-version-spellings.txt`). So the r98
control is *not* blind on that article: it reads `unmet 104/105` with
`failed_families [EXPLICIT-VERSION-ECHO]`, because r96 already set `check_echo` on that family.
The X-cap family's own echo assertion is new in r99 (`c.check_echo = True` in
`fam_refusal_versions_9digit`, measured by the sweep in `…/receipts/39-check-echo-owners.txt`), and
it is that one additional assertion which moves the r99 reading from 104/105 to 103/105.

So the honest statement is: **the X leg is a discrimination delta of exactly one family, not a
met-to-unmet flip.** The r98 control shows the X-cap spelling was already read by a *different*
family; the r99 reading shows the X-cap *family* now reads it too. A later round that wants the X
leg as a flip needs a spelling no other family sends.

### 3.4 What these bends do not prove

- They do not prove the X-cap family is the *only* reader of the X spelling. A battery that dropped
  the X family's echo assertion would still read 104/105 on this article (the r98 control's own
  reading is that battery's shape).
- They do not exercise the battery selftest's `--reference` leg — the blanket `lie-limine-version`
  wrapper. That leg stays owed from round 99 (A6a); `--selftest` without `--reference` prints
  `selftest PASS 5/5` and `reference-gate skipped (no --reference)`, which this seat measured
  (`…/receipts/40-battery-selftest.txt`). The wrapper proves the battery *sees* the field; these
  bends prove a *named family* asserts it.
- They do not attribute a blanket echo lie. A gate that lies in the echo for every version moves
  every echo-reading family at once; the r99 battery sets `c.check_echo = True` on five families
  (`fam_refusal_versions_9digit`, `fam_explicit_version_echo`,
  `fam_refusal_versions_9digit_y`, `fam_refusal_versions_9digit_z`, `fam_leading_zero_normalize`;
  sweep in `…/receipts/39-check-echo-owners.txt`), so such an article cannot single one out.
- They do not change any family's roster or case count: the roster stays 105 families and 420 cases
  in every leg of every run (`cases: 420` in each JSON; `families_total: 105`).

### 3.5 The nearest prior art is a blanket bend, not a spelling-targeted one

Sweeping every bend generator under `tools/` (`ls tools/make-r*-bends.py`; receipt
`…/receipts/32-prev-generator-field-sweep.txt`) and classifying each substitution by the field it
changes (receipt `…/receipts/33-echo-bend-classification.txt`) shows that only two generators ever
bend the *echo value* rather than mention it: `tools/make-r96-bends.py`'s `N01-echo-wrong`, whose
substitution is

```
"limine_version": "99.9.9" if limine_version_source == "flag" else limine_version,
```

— keyed on the version's *source*, not on any component, so it lies for every explicitly flagged
version at once — and this round's `N12-x-echo` / `N13-y-echo`. Every other generator
(r93/r94/r95/r97/r98/r99) bends `visibility_era`, a bound or a shape, and never the echoed value.
That is why the round-99 Frontier sentence said the echo legs had no *spelling-targeted* bend
rather than no bend at all: r96's blanket lie exercises the field but cannot single out the family
that asserts a given spelling.

## 4. The registry capture: a cell is a label set, not a span string

`tools/check-registry-content-r99.py` bound the `RC-BEND-SPAN` cell with a span regex whose alphabet
had no space token and which raised `RC-CELL-AMBIGUOUS` on any second mention. Two consequences
were fail-closed but wrong for a legitimate cell: `VARIANTS N01 N02 N03` read `RC-CELL-MISSING`, and
a cell stating a union of two spans had to be rewritten to one span.

`tools/check-registry-content-r100.py` binds the cell as a **set**:

- one `VARIANTS` mention (counted with `\bVARIANTS\b`; a second mention is `RC-CELL-AMBIGUOUS`);
- tokens are `N<digits>` or `N<digits>-N<digits>` — `TOKEN = re.compile(r"N([0-9]+)(?:-N([0-9]+))?")`
  at BYTE 12025 — matched with `re.fullmatch`, so a letter or extra-digit suffix cannot ride along
  (S397: "If the whole string matches the regular expression pattern, return a corresponding Match",
  the `re.fullmatch` sentence at BYTE 112171 of the 2026-11-08 fetch — the page's verbatim wording
  is `return a corresponding Match`, not `match object`);
- tokens may be joined only by `,`, whitespace, `;`, `+`, `/` or the word `and` —
  `SEPARATORS = re.compile(r"\s*(?:,|;|\+|/|\band\b)\s*|\s+")` at BYTE 12073; a range expands to
  its members in `parse_label_set` (BYTE 12134); any other token (`through`, a descending range, a
  letter suffix) raises and the caller fails closed as `RC-CELL-MISSING`;
- the declared set must *equal* the set of N-labels in the tool's module-level `VARIANTS` keys; an
  extra or missing label is `RC-VALUE-MISMATCH` naming both sides.

### 4.1 The six acceptance cells and the five fail-closed controls

The fixtures are built by the committed `.ufo/waves/round-100/before/dev/make-fixtures.py`, which
calls the frozen r100 checker's own `build_fixture` — the fixture bytes are the instrument's, not a
hand copy. Each cell below was read from the fixture's own `SKILL.md` bytes and each was run
through *both* checkers (`…/receipts/36-fixture-cells.txt` for the cell text, `…/receipts/22-fixture-matrix.txt`
for the two readings).

Six cells the r99 control rejects now bind (r100 `PASS`, r99 a finding):

| cell (registry text) | r99 finding | r100 |
|---|---|---|
| `VARIANTS N01 N02 N03` | `RC-CELL-MISSING` | `PASS` |
| `VARIANTS N01; N02; N03` | `RC-CELL-MISSING` | `PASS` |
| `VARIANTS N01 + N02 + N03` | `RC-CELL-MISSING` | `PASS` |
| `VARIANTS N01/N02/N03` | `RC-CELL-MISSING` | `PASS` |
| `VARIANTS N01-N02 and N03` | `RC-VALUE-MISMATCH` | `PASS` |
| `VARIANTS N01-N02 and N04-N05` (union) | `RC-VALUE-MISMATCH` | `PASS` |

Five forged shapes stay closed on r100:

| shape (registry text) | r100 finding | r99 finding |
|---|---|---|
| `VARIANTS N01a-N03` (letter suffix) | `RC-CELL-MISSING` | `RC-CELL-MISSING` |
| `VARIANTS N01 through N03` (prose) | `RC-CELL-MISSING` | `RC-CELL-MISSING` |
| `VARIANTS N01-N02 and N04` (extra label omitted) | `RC-VALUE-MISMATCH` | `RC-VALUE-MISMATCH` |
| `VARIANTS N01-N04,N05` (hybrid comma cell) | `RC-VALUE-MISMATCH` | `RC-CELL-MISSING` |
| `VARIANTS N01,N03 then VARIANTS N01-N03` (restated) | `RC-CELL-AMBIGUOUS` | `RC-CELL-AMBIGUOUS` |

and the positive control `VARIANTS N01,N03` (the non-contiguous gap cell) reads `PASS` on both
checkers. The hybrid cell is the one whose *finding id* moves: r99 could not parse it at all
(`RC-CELL-MISSING`) while r100 parses the tokens and then finds the label sets unequal
(`RC-VALUE-MISMATCH`) — the shape is closed on both, but by different rules.

### 4.2 The live table and the selftests

`python3 tools/check-registry-content-r100.py --revision <REV>` reads `PASS bindings 7/7 findings 0`
at the pre-round tip `ce73ccaf`, at the freeze `743ce449` and at the landing tip `69474c55`; the
r99 do-nothing control reads the same `PASS 7/7` on the same three revisions (receipt
`…/receipts/21-live-table.txt`). `--selftest` prints `selftest PASS 26/26` for r100 and
`selftest PASS 17/17` for the r99 control (this seat's own runs; the r100 case list is the 26
names `span-sep-space`, `span-sep-semicolon`, `span-sep-and`, `span-sep-slash`, `span-sep-plus`,
`span-union`, `span-letter-suffix`, `span-prose`, `span-union-lie` among others).

The registry coverage gate keeps reading `PASS` after the landing rows are added:
`python3 tools/check-registry-coverage.py --revision 69474c55` prints
`{"counts":{"findings":0,"missing":0,"registered":165,"rows_total":165,"tools_total":165},"status":"PASS"}`
rc 0 (`…/receipts/23-coverage-gate.txt`). At the freeze revision `743ce449` the same gate reads
`FAIL` with two `REGISTRY-ROW-MISSING` findings — the two new tools had no registry row yet at that
revision; the rows land later in the same round, which is why the gate reads PASS at the tip.

### 4.3 What the label-set capture does not bind

- It binds separators, not prose: `N01 through N03` stays a finding, and `N01a-N03` stays a finding.
- It binds N-labels only for the one `RC-BEND-SPAN` cell of the `make-r96-bends` row. The other
  registry rows stay presence-only — the coverage gate's scope, not the content gate's
  (`tools/check-registry-content-r100.py` docstring, "Named limits": "Only the cells in BINDINGS are
  bound. The other rows of the operative table stay presence-only (the coverage gate's scope)";
  receipt `…/receipts/45-named-limits-and-derivation.txt`).
- It does not bind N-labels outside the tool's `VARIANTS` keys: the derived side is exactly the set
  of N-labels in that dict (`variant_labels` parses the tool's module-level `VARIANTS` assignment
  with `ast` and keeps the `N<digits>` prefix of each key — same receipt), so a cell naming a label
  the tool does not declare reads `RC-VALUE-MISMATCH`.

## 5. Why the two instruments are worth having together

The bends answer "does the family assert the field its spelling selects?", and their control is a
predecessor battery that cannot answer it for the Y spelling. The label-set binder answers "does
the registry row still state the tool's whole label set at a granularity a reader can write?", and
its control is a predecessor checker that could not parse that text. Both keep their predecessors'
bytes as controls (`tools/limine-pin-battery-r99.py` `c2e8c8fc…`, `tools/limine-pin-battery-r98.py`
`8198bd84…`, `tools/check-registry-content-r99.py` `b489f5b8…`; the manifest above), so a later
round can re-run the same article against the do-nothing instrument and re-derive the difference
rather than trust this entry's table.

## 6. Sources

- **S396** (own-work, tier A) — `tools/make-r100-bends.py` (sha256 `7ccfe69e…`) and
  `tools/check-registry-content-r100.py` (sha256 `7a23a522…`) at the round-100 freeze `743ce449`.
  Anchors: the generator's N12 clause at BYTE 2615 and its N13 clause at BYTE 3365 (the falsified
  literal inside it at BYTE 3384); the checker's `TOKEN`/`SEPARATORS`/`parse_label_set` at BYTES
  12025 / 12073 / 12134. Every offset in this entry is re-measured with `bytes.find` on those
  pinned bytes (`…/receipts/30-quote-word-counts.txt`, `…/census-check.txt`).
- **S397** (docs, tier A) — CPython `re` module, `https://docs.python.org/3/library/re.html`,
  fetched 2026-11-08: HTTP 200, 257722 bytes, sha256 `69d64759ed7e269bd617470594dfb8c7970b61fa4def81530a5ea2953d42493b`,
  reproduced twice in this seat with byte-identical results (`…/receipts/37-s397-fetch-and-quotes.txt`).
  Anchors: `id="re.fullmatch"` at BYTE 111489, its sentence at BYTE 112171, the `\b` word-boundary
  sentence at BYTE 69787. It grounds the two primitives the tokeniser relies on: `fullmatch`
  anchors a token to the whole part, so a suffix cannot ride along, and `\b` asserts a word
  boundary rather than a literal character. The sentence is quoted verbatim as
  "If the whole string matches the regular expression pattern, return a corresponding Match" — the
  page's HTML at BYTE 112171 reads `return a corresponding Match`; the phrase `match object` does
  not occur there (this seat's own `bytes.find` of the printed phrase returns -1, and `match
  object` sits at BYTE 57131 in an unrelated table cell — receipts
  `…/receipts/37-s397-fetch-and-quotes.txt` and `…/receipts/46-s397-fullmatch-sentence.txt`).
