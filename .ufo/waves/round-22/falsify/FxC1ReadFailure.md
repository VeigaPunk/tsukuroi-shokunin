# FxC1ReadFailure — source-only attack on `check-boundary-contract.py`

Round-22 C1 (depth) checker only. Target file
`tools/check-boundary-contract.py`, SHA-256 as assigned `1b91a7c1…fdd2485` (not recomputed:
NO-EXEC). Read-only static derivation from the eight bound paths; no fixture executed, no
import, no subprocess, no production edit. Runtime observed: **none**. Every "source-derived"
verdict below is a static prediction, not a measurement.

`check-review-snapshots.py` and `_revision.py` were read only for shared revision semantics;
they are not audited here beyond that.

## What the checker gates

PASS (exit 0) requires all of: (a) raw JSON parses with duplicate-key rejection, schema string
exact, six unique ids; (b) each of the six `EXPECTED` tuples present verbatim in JSON
(line 87); (c) exactly one visible 5-cell prose row per id (lines 82, 88-90); (d) `scope`
equal to `LIMIT`; (e) the literal phrase "post-hoc detection, not preventive runtime
enforcement" somewhere in the prose (line 93); (f) host `native_per_seat_allowlist is False`
and exact `tools_semantics` (line 75); (g) one 11-cell `S083`/`S084` row each with path
substring, `own-work`, `A`, cell 7 `mined` (line 80).

## Findings

### F1 (fail-open) — the limit phrase is checked on the raw plane, not the visible plane

Line 82 builds the decision table from `visible(text)`; line 93 checks the disclaimer against
`text`. `visible()` (lines 38-55) deletes HTML-comment and fenced lines. The asymmetry means a
disclaimer that renders invisible still satisfies the C1 scope gate.

Fixture (static):
```python
prose = ('\n'.join('| ' + ' | '.join(r) + ' |' for r in EXPECTED)
         + '\n<!-- post-hoc detection, not preventive runtime enforcement -->')
```
Expected verdict (contract: the md's own `hidden`/`fenced` selftest cases establish that
hidden content must not count, and the limit is asserted as a rendered statement):
exit 1 + `BOUNDARY-LIMIT-MISSING`.
Source-derived: `cells` still sees the six rows; line 93 finds the phrase inside the comment;
no findings → **exit 0 PASS**. Same for the phrase placed only inside a ` ``` ` block.

Second-order: a PASS certifies a limit claim the document does not display; C1 credits 6/6 and
C3 can count that seat delivered-conformant.

### F2 (fail-open) — the host check ignores the key that carries the approved scope

Line 75 reads only `native_per_seat_allowlist` and `tools_semantics`. The source file carries
`authority` (line 11) and `approved_scope` (line 12), and the round Goal is "NEVER claim
preventive runtime enforcement". Neither key is compared.

Fixture: live host file with `"approved_scope": "native preventive per-seat enforcement"`.
Expected: FAIL (the artifact of authority would contradict `LIMIT` and the Goal).
Source-derived: line 75 is false only for the two checked keys → no finding → **exit 0 PASS**.
The checker pins the exposed schema but not the decision the schema records.

### F3 (misattribution, still fail-closed) — `sources=None`

Line 62 guards only `raw`/`prose`. Line 73 passes `None` through unchanged; line 77
`visible(None)` raises `AttributeError`; line 96 catches it and line 97 emits
`BOUNDARY-SCHEMA` at site `DATA`. `git_read` returns `None` for a path absent from the landed
tree (line 146), so a revision missing `corpus/SOURCES.md` is reported as a malformed
boundary contract, not a missing source table.
Expected: `BOUNDARY-CONTRACT-MISSING`/`BOUNDARY-SOURCE` at the SOURCES path.
Source-derived: exit 2, `BOUNDARY-SCHEMA` @ `DATA`.

### F4 (misattribution + masking) — `host=None`

Line 74 `json.loads(None)` raises `TypeError` before line 77 runs, so `BOUNDARY-SCHEMA` @
`DATA` fires and the source-row checks are never reached. With forged SOURCES rows and a
missing host file, the forgery is not examined at all.
Expected: a host-missing finding, sources still evaluated.
Source-derived: exit 2, one `BOUNDARY-SCHEMA` @ `DATA`.

### F5 (fail-closed, one collapsed class) — invalid UTF-8

`raw` (line 66), `prose` (72), `sources` (73) and `host` (74) all decode inside the `try`;
`UnicodeDecodeError` is a `UnicodeError` and is caught at line 96 for every one of the four.
`json.loads(bytes)` on invalid UTF-8 raises the same class. Exit is always 2, so the gate
holds; but all four artefacts collapse to one `BOUNDARY-SCHEMA` at `DATA`, losing which input
was corrupt. The selftest has no invalid-UTF-8 case (lines 109-129); its only source-absence
case is `''` (line 126), which exercises the string branch, not the bytes branch `git_read`
actually returns.

Related taxonomy inconsistency on *empty* files: `b''` yields exit 2 for `raw` and `host`,
exit 1 for `prose` and `sources`. Same condition, two classes.

### F6 (contradiction) — missing contract is FAIL-with-zero, not could-not-evaluate

Lines 62-64 return `status: FAIL`, `validated_boundary_decisions: 0` for a missing contract;
lines 96-100 return `CANNOT_EVALUATE` for the schema class. The md's checklist item 3 says
incomplete coverage must be could-not-evaluate, "not zero activity". The least informative
case is labelled FAIL with a numeric zero, which is exactly the reading item 3 forbids. Exit
is non-zero either way, so this is accounting semantics, not a false pass.

Payload shapes also diverge: MISSING omits `total_decisions`; schema includes both counters;
`RevisionError` (167) and `BOUNDARY-READ` (169) include neither. A consumer computing
validated/total breaks on two of four verdict classes.

### F7 (misattribution) — every content-read git error is labelled a revision failure

Line 164 evaluates four `git_read` calls left-to-right; lines 168-169 hardcode
`{'id': 'BOUNDARY-READ', 'site': 'revision'}`. A corrupt object for `corpus/SOURCES.md` or the
host JSON (line 147 `RuntimeError`) is reported against the revision. Absent files do not hit
this path (they return `None`), but unreadable ones do.

CLI first-failure ordering, for the record: `bind` runs before any content read, and inside it
branch validation precedes revision syntax (`_revision.py` selftest "precedence-branch-first"),
so `--revision <bad> --branch 'a..b'` reports `E-BRANCH-INVALID`. The prereg command omits
`--branch`, so this precedence is not live. Non-evaluating exit-0 paths exist: argparse's
`--help` is converted to `return 0` (line 159) with no JSON on stdout, and `--selftest`
returns 0 without evaluating a revision. A wrapper keying on exit code alone can record a
non-evaluating run as clean; the pinned command is unaffected.

### F8 (fail-open, bounded) — source rows are shape-checked, not content-checked

Line 80 verifies 11 cells, cell 1 contains the path as a substring, cells 2:4 are
`own-work`/`A`, cell 7 is `mined`. Cells 4-6 and 8-10 are unchecked and may be empty, and
`path not in cell` accepts the path embedded in a contradicting sentence.
Fixture: `| S083 | not the path .ufo/waves/round-22/snapshot/corpus/lessons/round-21.md |
own-work | A | | | | mined | | | |`.
Expected: FAIL (no scope/anchor/date/status/entry). Source-derived: PASS.

### F9 (calibration hazard) — the metric reaches 6 on failing runs

`count` increments per matched decision (line 92) independently of `findings`. The
`host-overclaim`, `limit` and forged-source fixtures each produce `status: FAIL`, exit 1, and
`validated_boundary_decisions: 6`. The prereg C1 metric is that counter. If a runner reads the
counter without gating on `status == PASS` and exit 0, C1 can be recorded as met on a failing
checker run — the md's own "clean accounting is never a clean strict receipt verdict" hazard
one layer down.

### F10 (bounded, fail-closed) — uncaught classes

`RecursionError` from deeply nested JSON is not in line 96's tuple but is a `RuntimeError`
subclass, so line 168 relabels it `BOUNDARY-READ` @ revision. `MemoryError` escapes entirely
(traceback, non-zero). Neither yields a false PASS.

## Bounded reason the decision gate itself holds

- No silent empty substitution: absence is `None`, and `None` is either MISSING (raw/prose) or
  an exception (sources/host). A failed `git show` is never converted to empty bytes.
- PASS requires the six JSON tuples to equal the embedded `EXPECTED` verbatim and exactly one
  visible 5-cell row per id; duplicate rows or an extra id fail closed.
- `native_per_seat_allowlist is not False` uses identity, so JSON `0` is rejected.
- Reads use the resolved `binding.sha`, not the branch name, so no branch drift between the
  four reads; duplicate JSON keys fail at every object level via `unique`.
- `git_read` passes argv lists, `--literal-pathspecs` on the fallback, and `bind` admits only
  7-64 hex characters, so no selector injection into `rev:path`.

## Expected vs observed, live working-tree inputs

Working tree is internally consistent: JSON `scope` equals `LIMIT` exactly; the six prose rows
(md lines 13-18) are byte-identical to `EXPECTED`; host line 10 is `false` and line 9 matches
`tools_semantics`; the phrase is in visible prose at md line 22; the md contains zero `<!--`
and zero fence markers (grep: no matches for `<!--|```|~~~`).
⇒ If the landed blobs equal these working-tree blobs, the source-derived verdict is exit 0,
`PASS`, 6/6.

Unresolved prerequisite: `corpus/SOURCES.md` is not a bound read path for this seat. I cannot
confirm the `S083`/`S084` rows (11 cells, `own-work`/`A`/`mined`, exact paths) at any revision.
The live PASS is therefore [INFERENCE] conditional on an artefact I could not read; I did not
fetch it.

## Axes

- C1 depth (primary): F1/F2 let the certified contract carry a scope claim the rendered
  document does not make and the authority source contradicts; F8 accepts provenance rows
  that assert nothing.
- C2 operability: F3/F4/F7/F6 report a provenance or content failure against the wrong
  artefact, and expose three payload shapes.
- C3 calibration: F9 lets a FAIL run emit 6/6 on the very counter C1 is scored by.
- Harm: none of these findings turns a live PASS into FAIL; the six decision checks themselves
  are sound.

## Proposed move (one, bounded, advisory only)

At line 93, check the limit phrase on the same filtered plane as the table:
`'\n'.join(visible(text))` instead of `text`, and add two negative fixtures (phrase only in
`<!-- -->`; phrase only inside ` ``` `).

Why it is non-obvious: `visible()` already exists and is applied twice, but the disclaimer is
the one claim checked on the unfiltered source, so the asymmetry is invisible unless you ask
which plane each claim is verified on.

Improves: C1 depth (the scope sentence must be visible to be credited), C2 (the fixtures pin
what "visible" means for limit text), C3 (removes a false-PASS path that would count a seat
delivered-conformant).

Risks: `visible()` drops any line containing `<!--` anywhere, so an inline-commented limit
sentence would fail closed (noisy but safe); a future doc that shows the limit only in a code
block would now FAIL. It does not address F2 or F9.

Not proposed here: changing `EXPECTED`, changing exit codes, or editing production files.

## Verification (for Main; not executed by this seat)

1. `--selftest` still prints PASS with all 19 existing cases under the changed expression.
2. Fixture A (phrase only in a comment): expect exit 1 + `BOUNDARY-LIMIT-MISSING`; current
   code predicts 0 (F1).
3. Fixture B (`approved_scope` overclaim): expect exit 1; current code predicts 0 (F2).
4. Fixtures C-E (`sources=None`, `host=None`, invalid UTF-8 in each of the four inputs):
   expect 2 with an artifact-specific site; current predicts `BOUNDARY-SCHEMA` @ `DATA`.
5. Prereg command on the landed revision: require exit 0 **and** `status: PASS` **and**
   `validated_boundary_decisions: 6`; never the counter alone (F9).

Reviewed-SHA256: 1b91a7c10c971b554bad144035b40d0b7054e06582093f9f851ac0fcafdd2485
Predicate: r22-fxc1readfailure
Scope: executed=none
