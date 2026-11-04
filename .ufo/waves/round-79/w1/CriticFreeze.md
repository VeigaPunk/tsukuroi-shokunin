# CriticFreeze — round 79 w1 attack item

claim=C1+C2
verdict=C1's numeric gate is answer-key equality plus digest arithmetic over a bundle the same seat writes: A1/A2/A5a–d/A8/A9/A10 are killed, A3 and A7 survive by declared design, and A15 (a junk S329 registry row) survives *undeclared*. C2's duplicate and shape legs kill the named A4 and A6 attacks, but A13 (self-test cell names a nonexistent tool), A14 (verdict map with code 3 only), A17 (heading-text collision silently drops current rows) and A12/A18 (self-declared marker and operative boundary) all survive, so "two gate rows with hermetic selftests" is not what the instrument measures. Neither predicate is an authenticity check and neither claims to be; the A15 and A13 gaps are outside the declaration's disclosed limit.

## Axes attacked

- **depth (C1, target 8)** — what the 0→8 measurement can and cannot establish.
- **operability (C2, target 0 duplicates / 2 gate rows)** — whether the two advertised
  interfaces are measured or merely spelled.
- **calibration** — the round must report these survives rather than let a green stand
  as a stronger statement than the counter made.

## Method

22 counter runs over 21 fixtures, all with `--root <fixture>`; real counters at
working-tree HEAD `883aae6`; base blobs read from `9086589a` with `git show`
(never checked out); frozen inputs digest-verified (`expected.json`
`0c09c7a4…add21`, snapshot `eb9479be…14c6`). Counter selftests re-run here:
C1 32/32 rc 0, C2 8/8 rc 0. Scratch `TMPDIR` fixed under
`/fast/scratch/hyaku/tsukuroi-r79/CriticFreeze/tmp`; no lane byte written.
Receipt: `CriticFreeze/attacks.json` (22 records with mirror digest, argv, rc,
counter line, findings); narrative: `CriticFreeze/report.md`; replay driver:
`CriticFreeze/battery.py`.

Every run agreed with its stated expectation on first observation except two
fixture-construction bugs of mine (A13 shared one ghost path across both rows,
which tripped the duplicate leg; A17's generated fixture had a lost header
line). Both were fixed and the whole battery re-run; the recorded 22 runs are
the post-fix set.

## Kills (13)

| Attack | Counter answer |
|---|---|
| A1 do-nothing (base mirror) | C1 `unreadable:FileNotFoundError` rc 1; C2 `duplicates=6 shape_ok=0/2` rc 1 |
| A2 marker-only (data + companion, no verdict/results) | `unreadable:FileNotFoundError` rc 1 |
| A5a nine rows / A5b wrong line / A5c quote swap / A5d duplicate id | `finite-content-mismatch` rc 1 (all four) |
| A8 duplicate JSON key | `unreadable:ValueError` rc 1 |
| A9 S329 unresolved | `source-unresolved` rc 1 |
| A10 snapshot tampered | `snapshot-digest` rc 1 |
| A4 lying registry (`--selftest` claimed, blobs carry none) | `shape_ok=0/2`, `GATE-STANDARD-SHAPE` ×2, rc 1 |
| A6 unmarked current duplicate | `duplicates=1` rc 1 |
| A17b heading made unique (control for A17) | `duplicates=1` rc 1 |

The specified attacks A2, A4, A5, A6 all die as required.

## Survives (9) and what they mean

- **A3 fabricated review bundle — survive, declared.** Correct digests + eight
  `holds` + a result line carrying `review_sha256=` yields `rows=8 … met=1` rc 0
  with no evidence any reviewer read the source. This is the limit the
  instrument docstring and the declaration already state. For C1's scope it
  means the after-value measures conformance, not depth; the depth verdict must
  rest on something this counter cannot see.
- **A7 answer-key copier — survive, declared, same line as A3.** The writer
  (`writer_source` embedded in `attacks.json`) reads `expected.json`, emits its
  rows verbatim, hashes itself and passes. Plainly: a seat with zero systemd
  knowledge reaches the target. The predicate's role is measurement against a
  frozen decision set, not authenticity.
- **A15 junk S329 row — survive, NOT declared.** `source-unresolved` only fires
  on a missing 11-cell `S329` row, kind `own-work`, or a second cell that lacks
  the substring `systemd.unit.xml` (`tools/measure-unit-deps-r79.py:105`). A row
  with source cell `systemd.unit.xml (claimed, unverified — not a URL)`, kind
  `blog`, anchor `no anchor recorded` resolves and the run is `met=1` rc 0. The
  declaration's "source truth remains a separate kill rule" names no such rule
  in this instrument.
- **A0 clean-registry control — survive by design.** Confirms the C2 fixture
  family is valid: the A4/A6 kills are caused by the defect under test.
- **A12 marked live duplicate — survive by definition.** A genuinely current
  table that repeats a tool passes while carrying `NON-OPERATIVE`. The marker is
  the only authority; nothing checks the claim of historicity.
- **A13 false self-test interface — survive, undeclared.** Self-test cell
  `` `check-r71-routed-r72` — `python3 tools/does-not-exist-a-r79.py --selftest` ``
  passes the shape clause (`tools/check-gate-standard-r79.py:167` tests
  substring presence, and the source clause reads the *entry-command* blob). The
  item's own words — "two gate rows with hermetic selftests" — are falsified by
  a green counter.
- **A14 thin verdict map — survive, minor.** `3 self-test failed` alone satisfies
  both tests; codes 0/1/2 are never required.
- **A17 heading-text collision — survive, counter defect.** `current_rows` maps a
  table to its line with `lines.index(heading)` (`:127`), which returns the first
  occurrence of that string, so a table after the operative heading that reuses
  an earlier heading text is treated as pre-operative and dropped (`:129`). One
  repeated `## Round 72 — continuation` heading hides a second current row
  naming `tools/check-r71-routed-r72.py`: `duplicates=0 shape_ok=2/2` rc 0.
  **A17b isolates it**: identical rows and positions, heading renamed, same
  counter reads `duplicates=1` rc 1. Unlike A12, the hidden table carries no
  `NON-OPERATIVE` token, so it is current by the predicate's own definition and
  should have been counted. Two-line fix: `tables()` should yield the heading's
  line index instead of recomputing it by string.
- **A18 operative boundary moved — survive by definition.** Four duplicate rows
  become historical the moment a round-79 registry heading exists, with no
  marker anywhere. `duplicates=0` therefore does not show the six base
  duplicates were repaired.

## Smallest safe corrections

1. **C2 / A17 (highest severity, in-scope bug):** key tables by heading line
   index, not `lines.index(heading)`. Without it a lane can hide current
   duplicate rows — or an extra gate row — and still go green.
2. **C2 / A13:** resolve `TOOL_PATH.findall(row[4])` (the self-test cell's tool)
   and require that blob to exist with the tokens, and that it equal the
   entry-command path, if "hermetic selftest" is to be measured.
3. **C2 / A14:** require all four codes 0–3 in the verdict map, not just `3`.
4. **C1 / A15:** bind the source cell to the pinned raw URL and the anchor cell to
   the snapshot's line range (or digest); otherwise drop "sourced" from the
   measured predicate and carry source truth as a review claim outside the gate.

All four are changes to frozen predicates or the claim text and are therefore
the round owner's, not mine; I edited no counter, `SKILL.md`, `SCORECARD.md` or
registry byte.

## Declared limits of this probe

- All runs used `--root`; the `--revision` binding path (`_revision.bind`,
  branch/landed/pushed refusals) was not exercised here.
- `quote-location` (`measure-unit-deps-r79.py:110`) and `row-shape` (`:112`) are
  unreachable in the measured path: data must equal the digest-frozen expected
  set (`:97`), and the snapshot digest is checked first (`:108`). For the frozen
  snapshot all eight ranges re-derive exactly (DP1–DP8, token counts 15–24), so
  those two branches contribute only to the selftest.
- `analyze` `:138` holds a tautology (`table['heading'] == table['heading']`);
  harmless today, but it hides that every yielded table is treated as current.
- The duplicate leg counts tool paths only in the entry-command and self-test
  cells; a tool named only in Pinned values/Write scope/Owner is not counted.
  Not exercised as an attack.
- Fixtures are deleted with the scratch tree; `CriticFreeze/battery.py` rebuilds
  them deterministically from `git show 9086589a` plus the frozen inputs.
