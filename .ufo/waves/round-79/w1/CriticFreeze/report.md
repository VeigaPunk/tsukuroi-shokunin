# CriticFreeze — round 79 w1 attack battery

claim=C1+C2

## What I attacked

The two frozen predicates, run as they will be run for the claim: the real
counters at the working tree, invoked with `--root <fixture>` over fixture
mirrors. 22 counter runs, 21 fixtures, every fixture under
`/fast/scratch/hyaku/tsukuroi-r79/CriticFreeze/fixtures` with `TMPDIR` fixed to
`/fast/scratch/hyaku/tsukuroi-r79/CriticFreeze/tmp`. Lane files were read only;
no lane byte was written by any run.

Inputs, digest-verified before the first run:

- expected.json SHA-256 `0c09c7a4ad010dd19e99b47940b94030f945498a20b705981b581e308f3add21`
- snapshot systemd.unit.xml SHA-256 `eb9479bea50ccb0e7643836ec083e8ef68bdf9ef2b26f31839939168f82714c6`
- base revision for mirrored blobs `9086589a82f221d130ed6711fbe70b85f0d07aea` (read with `git show`, working tree untouched)
- instruments: measure `132be669e367670e…`,
  gate `0b32ddbcaf1fcab3…`,
  `_revision` `fc861ec8a4f2539a…`
- interpreter `/usr/bin/python3 -> python3.14 (Python 3.14.8)`
- counter selftests re-run in this seat: C1 `SELFTEST total=32 passed=32 failed=0` rc 0,
  C2 `SELFTEST total=8 passed=8 failed=0` rc 0.

The C1 `--root` path reads `expected.json` from the fixture but derives the
comparison object from the lane's frozen copy, so the answer key is not
fixture-controlled: a fixture cannot widen the target.

## Runs

| attack | target | expected | rc | observed | counter line |
|---|---|---|---|---|---|
| A1-base-c1 | C1 | kill | 1 | kill | `DEPS predicate="eight pinned dependency-propagation rows match with review binding" rows=0 verified=0 review=0 met=0 reason=unreadable:FileNotFoundError` |
| A1-base-c2 | C2 | kill | 1 | kill | `GATE_STANDARD predicate="zero duplicate current rows and two gate-standard rows" duplicates=6 shape_ok=0/2 met=0` |
| A2-marker-only | C1 | kill | 1 | kill | `DEPS predicate="eight pinned dependency-propagation rows match with review binding" rows=0 verified=0 review=0 met=0 reason=unreadable:FileNotFoundError` |
| A3-fabricated-bundle | C1 | survive | 0 | survive | `DEPS predicate="eight pinned dependency-propagation rows match with review binding" rows=8 verified=8 review=1 met=1 reason=finite-content-and-review` |
| A5a-nine-rows | C1 | kill | 1 | kill | `DEPS predicate="eight pinned dependency-propagation rows match with review binding" rows=0 verified=0 review=0 met=0 reason=finite-content-mismatch` |
| A5b-wrong-line | C1 | kill | 1 | kill | `DEPS predicate="eight pinned dependency-propagation rows match with review binding" rows=0 verified=0 review=0 met=0 reason=finite-content-mismatch` |
| A5c-quote-swap | C1 | kill | 1 | kill | `DEPS predicate="eight pinned dependency-propagation rows match with review binding" rows=0 verified=0 review=0 met=0 reason=finite-content-mismatch` |
| A5d-duplicate-id | C1 | kill | 1 | kill | `DEPS predicate="eight pinned dependency-propagation rows match with review binding" rows=0 verified=0 review=0 met=0 reason=finite-content-mismatch` |
| A7-answer-key | C1 | survive | 0 | survive | `DEPS predicate="eight pinned dependency-propagation rows match with review binding" rows=8 verified=8 review=1 met=1 reason=finite-content-and-review` |
| A8-duplicate-key | C1 | kill | 1 | kill | `DEPS predicate="eight pinned dependency-propagation rows match with review binding" rows=0 verified=0 review=0 met=0 reason=unreadable:ValueError` |
| A9-no-source-row | C1 | kill | 1 | kill | `DEPS predicate="eight pinned dependency-propagation rows match with review binding" rows=0 verified=0 review=0 met=0 reason=source-unresolved` |
| A10-snapshot-tampered | C1 | kill | 1 | kill | `DEPS predicate="eight pinned dependency-propagation rows match with review binding" rows=0 verified=0 review=0 met=0 reason=snapshot-digest` |
| A15-bogus-source-row | C1 | survive | 0 | survive | `DEPS predicate="eight pinned dependency-propagation rows match with review binding" rows=8 verified=8 review=1 met=1 reason=finite-content-and-review` |
| A0-clean-registry | C2 | survive | 0 | survive | `GATE_STANDARD predicate="zero duplicate current rows and two gate-standard rows" duplicates=0 shape_ok=2/2 met=1` |
| A4-lying-registry | C2 | kill | 1 | kill | `GATE_STANDARD predicate="zero duplicate current rows and two gate-standard rows" duplicates=0 shape_ok=0/2 met=0` |
| A6-unmarked-duplicate | C2 | kill | 1 | kill | `GATE_STANDARD predicate="zero duplicate current rows and two gate-standard rows" duplicates=1 shape_ok=2/2 met=0` |
| A12-marked-live-duplicate | C2 | survive | 0 | survive | `GATE_STANDARD predicate="zero duplicate current rows and two gate-standard rows" duplicates=0 shape_ok=2/2 met=1` |
| A13-nonexistent-selftest-tool | C2 | survive | 0 | survive | `GATE_STANDARD predicate="zero duplicate current rows and two gate-standard rows" duplicates=0 shape_ok=2/2 met=1` |
| A14-thin-verdict-map | C2 | survive | 0 | survive | `GATE_STANDARD predicate="zero duplicate current rows and two gate-standard rows" duplicates=0 shape_ok=2/2 met=1` |
| A17-heading-text-collision | C2 | survive | 0 | survive | `GATE_STANDARD predicate="zero duplicate current rows and two gate-standard rows" duplicates=0 shape_ok=2/2 met=1` |
| A17b-unique-heading | C2 | kill | 1 | kill | `GATE_STANDARD predicate="zero duplicate current rows and two gate-standard rows" duplicates=1 shape_ok=1/2 met=0` |
| A18-operative-boundary-moved | C2 | survive | 0 | survive | `GATE_STANDARD predicate="zero duplicate current rows and two gate-standard rows" duplicates=0 shape_ok=2/2 met=1` |

`outcome` is the counter's behaviour, not my wish: *kill* = the counter refused
(rc 1) and named a reason; *survive* = the counter accepted (rc 0, `met=1`).

## Kills (the predicates hold where they claim to)

- **A1 do-nothing** — base mirror: C1 `unreadable:FileNotFoundError` rc 1, C2
  `duplicates=6 shape_ok=0/2` rc 1. The before-values in the declaration replay
  exactly (`0` and `6 / 0-2`).
- **A2 marker-only** — exact `data.json` and companion, no `verdict.json`, no
  `w1-results.json`: `unreadable:FileNotFoundError` rc 1. A data file alone does
  not move C1.
- **A4 lying registry** — rows advertise `--selftest` while the two shipped tool
  blobs contain no `--selftest` and no `SELFTEST` token: `shape_ok=0/2` rc 1,
  `GATE-STANDARD-SHAPE` on both rows. The named attack is dead.
- **A5a nine rows / A5b wrong line / A5c quote swap / A5d duplicate id** — all
  rc 1 `finite-content-mismatch`. Note *where* they die: A5c's quote is a real,
  locatable quote in the pinned snapshot, yet it is refused by the equality
  check (measure-unit-deps-r79.py:97), never reaching `quote-location` (:110).
- **A6 duplicates left unmarked** — `duplicates=1` rc 1. The marker rule works
  when the table is genuinely new.
- **A8 duplicate JSON key** — `unreadable:ValueError` rc 1 (strict
  `object_pairs_hook`).
- **A9 S329 absent** — `source-unresolved` rc 1.
- **A10 snapshot tampered** — `snapshot-digest` rc 1.

## Survives, and what each one means

**A3 fabricated review bundle — survive, declared.** With `data.json` equal to
the frozen rows, one line of companion, `verdict.json` carrying the two
computed digests and eight `holds`, and a w1 result whose output is
`review_sha256=<digest>`, the counter prints
`rows=8 verified=8 review=1 met=1 reason=finite-content-and-review` rc 0. Nothing
in the bundle is evidence that a reviewer opened the source; the review checks
are digest *arithmetic* over bytes the same seat wrote. This is exactly the
limit the instrument's docstring and the declaration state ("a fully fabricated
report bundle remains a declared limit"), so it is a defect of *scope*, not of
implementation.

**A7 answer-key copier — survive, declared, and the same survive as A3.**
`A7/answerkey_writer.py` (embedded in `attacks.json` as `writer_source`) reads
`expected.json`, writes its `rows` verbatim, hashes its own outputs and emits a
matching review. It has no systemd knowledge and reads nothing else. Result:
identical `met=1` line. The predicate's role is measurement of conformance to a
frozen decision set, not authenticity; this receipt makes that concrete. The
honest consequence for the round: an after-value of 8 proves the eight rows were
transcribed and a digest-consistent review bundle was deposited — it does not
prove depth. The depth verdict must rest on the separate claim that the author
derived and checked the rows, which this counter cannot see.

**A15 bogus source row — survive, NOT covered by the declared limit.** The
declared limit says "the companion and source truth remain separate kill rules".
For the source there is no kill rule in this instrument. `source-unresolved`
fires only when the registry has no 11-cell `S329` row, the row's third cell is
`own-work`, or the second cell does not *contain* the string
`systemd.unit.xml` (measure-unit-deps-r79.py:105). A row whose source cell is
the prose `systemd.unit.xml (claimed, unverified — not a URL)`, kind `blog`, and
anchor `no anchor recorded` resolves; with exact data the counter returns
`met=1` rc 0. So "sourced S329" in the C1 predicate is measured as a substring,
and a fabricated registry row passes. Smallest safe correction: require the
source cell to contain the pinned raw URL and the anchor cell to cite the
snapshot's line range (or its digest), or drop "sourced" from the measured
predicate and keep it as a separate, non-mechanical review claim.

**C2 A0 control — survive by design.** A clean repaired registry with zero
duplicates and both frozen rows gate-standard reads `duplicates=0 shape_ok=2/2`
rc 0, so the fixture family is a valid vehicle: the A4/A6 kills are caused by the
defect under test, not by fixture breakage.

**C2 A12 marked live duplicate — survive by definition.** A second table that
repeats `check-r71-routed-r72` and `measure-unit-deps-r79` while declaring itself
`NON-OPERATIVE` reads `duplicates=0` rc 0. The marker is the sole authority for
"current"; nothing checks that the marked table is actually historical. The
round-78 routed item 4 asks for markers, so this is the intended semantics — but
the after-value "zero duplicate current rows" must be read as "zero duplicates
among rows the document itself calls current".

**C2 A13 false self-test interface — survive, undeclared, and it falsifies the
item's own wording.** Both frozen rows keep a real entry-command blob and a
self-test cell of the form `` `check-r71-routed-r72` — `python3
tools/does-not-exist-a-r79.py --selftest` ``. The shape clause
(check-gate-standard-r79.py:167) tests `'--selftest' in selftest` and
`row[0] in selftest`, both of which a nonexistent tool's path satisfies, and the
source clause reads the *entry command's* tool only. Result `shape_ok=2/2` rc 0.
The claim text says the rows have "hermetic selftests"; the instrument measures
substring presence in the entry-command blob and never resolves the self-test
cell's tool or runs it. Smallest correction: take `TOOL_PATH.findall(row[4])`
and require that blob to exist and carry the tokens (and, if the claim is
"hermetic", that it be the same path as the entry command).

**C2 A14 thin verdict map — survive, minor.** Replacing the maps with
`3 self-test failed` alone still satisfies `'3' in …` and `'self-test' in
verdict.lower()`. The 0/1/2 status codes the registry contract requires are not
checked. Smallest correction: require all four single-digit codes, e.g. a
`{'0','1','2','3'} ⊆ set(re.findall(...))` test.

**C2 A17 heading-text collision — survive, a counter defect with a two-line
fix.** `current_rows` maps a table back to its line with `lines.index(heading)`
(check-gate-standard-r79.py:127), which returns the *first* occurrence of that
string. A table placed after the operative heading whose heading text also
appeared earlier is therefore classified as "before the operative heading" and
dropped (line 129). The fixture has the operative round-79 table plus, after it,
a table under `## Round 72 — continuation` — a heading string already used above
— containing a second current row naming `tools/check-r71-routed-r72.py`. The
counter reads `duplicates=0 shape_ok=2/2` rc 0.
**A17b isolates the cause**: byte-identical rows and positions, only the later
heading renamed `## Round 73 — continuation`; the same counter reads
`duplicates=1` rc 1. So a lane can hide any number of current duplicate rows —
or an entire extra gate row — by reusing a heading string, and the gate goes
green. This is not a definitional survive: the hidden table carries no
`NON-OPERATIVE` token, so by the predicate's own definition its rows are current
and should have been counted. Fix: have `tables()` yield the heading's line index
and use that instead of `lines.index(heading)`.

**C2 A18 operative boundary moved — survive by definition.** Four duplicate
rows under `## Gate and probe registry — round78 …` are not counted once a
round-79 heading exists, with no marker anywhere. This is the cheapest route to
`duplicates=0`: declare a new operative section rather than repair the old
tables. Consistent with the claim's wording ("current rows"), but it means the
after-value is not evidence that the six base duplicates were repaired.

## What the survives do to each claim's declared scope

- **C1.** The numeric gate is answer-key equality plus a self-consistent review
  bundle. It kills every content divergence (A2, A5a–d, A8, A9, A10) and cannot
  distinguish an author who read systemd from a copier of `expected.json`
  (A3/A7) — declared. It also cannot distinguish a curated registry row from a
  junk one (A15) — *not* declared, and the declaration's "source truth remains a
  separate kill rule" sentence should either name that rule elsewhere in the
  round or lose the word "sourced" from the measured predicate.
- **C2.** The duplicate leg is defeated by a self-declared marker (A12), by
  moving the operative boundary (A18), and by a heading-text collision (A17,
  a bug). The shape leg is defeated by a self-test cell naming a nonexistent
  tool (A13) and by a one-line verdict map (A14). The named A4 and A6 attacks
  are dead; the claim's phrase "two gate rows with hermetic selftests" is not
  what the predicate measures.

## Residual notes

- `quote-location` (measure-unit-deps-r79.py:110) and `row-shape` (:112) cannot
  fire in the measured path: data must equal a digest-frozen expected set
  (:97), the snapshot digest is checked first (:108), and for the frozen
  snapshot every recorded range re-derives exactly (all eight, DP1–DP8, computed
  = recorded; token counts 15–24, all ≤25). They are live only in the selftest's
  synthetic buffers, where the equality check also runs first.
- `analyze` line 138 contains a tautology (`table['heading'] == table['heading']`);
  it does not change the result because `current_rows` already filtered, but it
  hides that every yielded table is treated as current regardless of heading.
- `duplicates` counts tool paths from the entry-command and self-test cells only
  (line 149/151 region, `row[2] + ' ' + row[4]`); a tool named only in Pinned
  values, Write scope or Owner is not counted. Not exercised as an attack here.
- My battery did not exercise the `--revision` binding (`_revision.bind`) — all
  runs used `--root`, so branch/landed/pushed refusals are outside this receipt;
  they are already covered by `_revision`'s own selftest and by the frozen
  controls' base arm.
- I did not edit the counters, SKILL.md, SCORECARD.md or any registry; my writes
  are this report, `attacks.json`, the replay driver `battery.py`, and the seat
  report one level up.

## Replay

Fixtures were deleted with the scratch tree per the round's scratch rule.
`battery.py` rebuilds every fixture deterministically from `git show 9086589a`
plus the two frozen inputs and rewrites `attacks.json`; `TMPDIR` is set
explicitly for every counter run. The mirror SHA-256 in each record is the
tree digest over that fixture's files, so a replay can be compared byte-wise.
