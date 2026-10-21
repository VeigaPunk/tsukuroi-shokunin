# FxC1Expansion — C1 / EXPANSION → CHECK_EACH

Seat: `TsukuroiR23-2.FxC1Expansion-2`, leaf, NO-EXEC / NO-FETCH.
Inputs read only from the seat binding: the landed `candidate/tools/check-edit-contract.py`
(declared SHA256 `620f3e5bad34c4ba77a0f0e458bedd79cb05b04a5b1d90200c0baf60038e5081`, treated as
declared identity, not recomputed), `preregister.json`, the landed knowledge JSON/Markdown,
`candidate/corpus/SOURCES.md`, and `sources/structured-edit-observations.json`.
No command was executed; no digest was computed. Marker `[OBSERVED]` = read in a named file;
`[INFERENCE]` = code-path result derived by reading, not executed.

## 1. Attacked claim

C1 (axis `depth`, metric `validated_edit_decisions`, before 0, target 8,
`python3 tools/check-edit-contract.py --revision <REV>`), for the row:

```
EXPANSION | CHECK_EACH | Every recorded adapter read or write remains separately scoped | S086 | round23-preregister
```

Attack question: can a literal carrier input be counted as validated for this row while the row's
meaning — each recorded adapter read/write remains separately scoped — is violated?

## 2. Landed row vs preregistered tuple

Landed JSON, `corpus/knowledge/structured-edit-r23.json` `decisions[7]` `[OBSERVED]`:

- `id=EXPANSION`, `decision=CHECK_EACH`,
  `reason=Every recorded adapter read or write remains separately scoped`,
  `evidence=S086`, `policy=round23-preregister`.

`preregister.json` `edit_decisions[7]` `[OBSERVED]`:

- `["EXPANSION","CHECK_EACH","Every recorded adapter read or write remains separately scoped"]`.

Exact match on the three preregistered fields. The row's `evidence` and `policy` columns are not
preregistered at all: every `edit_decisions` entry is a three-element list, and `evaluate()` pins
those two columns itself from `EXPECTED` (`S086`, `round23-preregister`, tool lines 28 and 20–29).
Preregistration is therefore narrower than the landed row: it fixes the decision, not its citation
binding. There is no landed/preregistered divergence to attack.

## 3. What `evaluate()` actually checks for this row `[OBSERVED]`

For every row, including EXPANSION, the gate is (tool lines 141–152):

1. JSON row exists and `set(row) == {'id','decision','reason','evidence','policy'}` and the tuple
   `(id, decision, reason, evidence, policy)` equals `EXPECTED[7]` exactly (line 146–147).
2. Markdown: `matches = [r for r in table_cells(text) if r and r[0] == 'EXPANSION']` must equal
   exactly `[list(EXPECTED[7])]` (line 148–149) — one row, five cells, exact strings after
   `strip()`.
3. Global: no `EDIT-DECISION-MISMATCH` finding, plus `scope == LIMIT`, `PROSE_LIMIT` present in
   `visible(text)`, the S086 SOURCES row gate (lines 137–140), the evidence gate
   `evidence_ok()` (lines 96–112), and the preregister triple gate (lines 135–136).

`CHECK_EACH` itself never appears in executable logic: the token occurs only in `EXPECTED[7]`
(line 28) and in the selftest literal (line 175). There is no function that inspects a recorded
adapter step against a scope.

The only gate that touches adapter records is `evidence_ok()`, and its entire constraint on
`recorded_starts` is line 108:

```python
or not isinstance(row.get('recorded_starts'), list) or not row['recorded_starts']
```

That is: a non-empty list. Its elements are never read. `SHAPES` pins only `argument_keys` sets.
`transcript_sha256` is only `re.fullmatch(r'[0-9a-f]{64}', ...)` (line 109); no hash is recomputed
or compared. Observation-level extra keys are accepted (the landed rows carry `seat`, `agent`,
`request_line`, `call_id`).

## 4. Bounded search over the four named carriers

| carrier | freedom | verdict |
|---|---|---|
| knowledge JSON | none: exact top-level key set `{schema, decisions, source_path, scope}`, exactly 8 unique ids, exact 5-key rows, exact tuple | no falsifier |
| preregister | none: `edit_decisions` must equal `[list(e[:3]) for e in EXPECTED]` exactly; duplicate JSON keys raise via `unique` | no falsifier |
| Markdown table row | none: one row only, exact cells after `strip()`; `visible()` drops comments, fences, 4-space-indented lines | no falsifier |
| Markdown body | unpinned | falsifier (F2) |
| SOURCES | 11 cells, path suffix, `own-work`/`A`, index 7 `mined`, no backslash; cells 4, 5, 6, 8, 9, 10 unpinned | falsifier (F1) |

JSON and preregister are fully pinned `[OBSERVED]`; there is no literal input there that reaches
`count += 1` with a different meaning. The Markdown row is also pinned: comments, fences and
indented lines are invisible to `table_cells()`, escaped pipes only add cells (breaking the
5-cell equality), and HTML entities/emphasis/zero-width characters are not stripped, so a
renderer-visible duplicate or a differently rendered row fails `matches != [list(expected)]`
`[OBSERVED code, INFERENCE on renderers]`. `visible()` is explicitly a finite carrier rule, not a
rendered-prose theorem (docstring line 46).

## 5. Decisive falsifier — the evidence carrier the row cites

`S086` (`sources/structured-edit-observations.json`) is consumed by `evaluate()` and is the only
input that can make the row's proposition true or false. Its `recorded_starts` are unguarded
beyond type/non-empty. One element edit:

Before (landed `observations[0].recorded_starts[1]`) `[OBSERVED]`:

```json
{"line": 13, "tool": "write", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/build/CritRuntime.md"}
```

After:

```json
{"line": 13, "tool": "write", "path": ["/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/build/CritRuntime.md", "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/build/CritRuntime-copy.md"]}
```

This records one adapter write start whose scope is a two-target list — an expansion that is not
separately scoped — so the EXPANSION reason is false. It still passes:

- observation-level `path` is still a `str` under `LANE` (line 107);
- `recorded_starts` is still a non-empty list (line 108), and no element field is inspected;
- `SHAPES`, `body_fields`, `transcript_sha256`, SOURCES S086, decisions, `scope` and
  `PROSE_LIMIT` are untouched.

Result by code path: `evidence_ok()` True, no finding added, `code = 0`, `count = 8`,
`status = PASS` `[INFERENCE — not executed]`.

One-token variant: change that start's `"tool": "write"` to `"tool": "read+write"` — one start
recording both a read and a write under one scope, exactly what CHECK_EACH forbids. Same PASS.
Minimal variant: `"recorded_starts": [{}]` — one empty object, still a non-empty list.

The tool's own clean fixture already demonstrates this insensitivity `[OBSERVED]`:
lines 185–188 build `recorded_starts` as `[{'tool': 'write'}]` and `[{'tool': 'edit'}]` — no
`path`, no `line` — and the `('clean', ..., 0, None)` case asserts
`result['validated_edit_decisions'] == 8` (line 241). So the positive control itself counts
EXPANSION as validated with a recorded write start that carries no target, while the reason claims
every recorded read/write is separately scoped. No mutation was ever needed to show the gate is
shape-only; the fixture proves it without execution.

## 6. Carrier-only falsifiers (contradiction, not a false row)

These make the validated corpus deny the row. None can make the row's proposition false, because
only S086 supplies the records.

**F1 — SOURCES `teaches` cell, index 6 (one cell).** The S086 gate checks `len == 11`,
`cell[1]`'s last ` — ` suffix, `cell[2:4]`, `cell[7] == 'mined'`, and no backslash (lines
137–140). `teaches` is index 6 and is unchecked. Replace the landed text
`Structured edit metadata exposes a target path plus opaque body-key forms and separate read/write
starts; permission must be declared independently and prospectively for each exact target` with
`Recorded adapter steps share one scope; expansion is not separately checked`. The row keeps its
path suffix, `own-work`, `A`, `mined`, 11 cells and no backslashes, so `EDIT-SOURCE` is silent and
the count stays 8 `[INFERENCE]`. The source registry would then state the opposite of the decision
it grounds.

**F2 — Markdown body (one sentence/line).** Only the decision rows and the limit sentence are
read. Replace bounded-procedure item 4, `4. Audit every captured native read/write expansion
against its own authority. A valid frontend target cannot clear an out-of-binding backend step or
a forbidden command/fetch.`, with `4. A recorded read/write expansion inherits the parent call's
scope and is not separately audited.` The line has no `|` and the `It is not native permission
enforcement` sentence is untouched, so the check still returns PASS/8 `[INFERENCE]`. Reduction
proof: the selftest's `prose` fixture (line 181) is only the five-column header, separator, eight
rows and the single line `It is not native permission enforcement, a sandbox.`, and it is asserted
PASS — all other document contract text is outside the checked artifact.

**F3 — table header relabel (display only).** `table_cells()` never identifies a header row, so
`| ID | Policy | Evidence | Reason | Decision |` over the unchanged body still passes; a renderer
then shows `round23-preregister` in the Decision column `[INFERENCE]`. The machine-readable decision
in the JSON is unchanged, so this is an attribution gap, not a decision forgery.

## 7. Verdict

- Against the four named authoring carriers: the EXPANSION row's *text* cannot be forged. JSON,
  the table row and the preregister triple are exact-equality pinned, and the landed row matches
  the preregistered triple exactly.
- Against the row's *meaning*: no check exists. The EXPANSION reason is a literal string echoed
  three ways; `CHECK_EACH` is never executed against any recorded step; the only adapter gate
  accepts arbitrary `recorded_starts` elements and the tool's own clean fixture records an
  unscoped write while asserting 8 validated.
- Therefore C1's `validated_edit_decisions = 8` measures declaration consistency, not
  "Every recorded adapter read or write remains separately scoped". If C1's scope sentence
  "eight finite source-grounded structured-edit authority decisions" is read as each decision
  holding of S086, the EXPANSION contribution is falsified: a one-element S086 edit makes the
  reason false while `status` stays `PASS` and the count stays 8.
- The landed S086 itself does not violate the row: each of its starts carries exactly one
  `line`/`tool`/`path` `[OBSERVED]`. The defect is check strength, not landed source content.
- The tool's `LIMIT` disclaims native prevention, patch interpretation, effects and reading proof,
  but it claims "declared audit authority for structured target metadata". Recorded
  `recorded_starts` scoping *is* structured target metadata, so the disclaimer does not cover this
  gap.

## 8. Smallest in-scope remedy

Close the row at the only place it can be evaluated — the evidence gate — and fix the positive
control that currently encodes the violation:

```python
def start_ok(start):
    return (isinstance(start, dict) and set(start) == {'line', 'tool', 'path'}
            and isinstance(start['line'], int) and not isinstance(start['line'], bool)
            and start['tool'] in {'read', 'write', 'edit'}
            and isinstance(start['path'], str) and start['path'].startswith(LANE)
            and '/../' not in start['path'])
```

Replace line 108's clause with
`or not isinstance(row.get('recorded_starts'), list) or not row['recorded_starts'] or not all(map(start_ok, row['recorded_starts']))`,
then update the clean fixture's starts to `{'line': 12, 'tool': 'write', 'path': lane + 'x/A.md'}`
and `{'line': 31, 'tool': 'edit', 'path': lane + 'x/B.md'}`, and add two selftest cases:

- `('evidence-unscoped-start', ..., start.pop('path'), ..., 1, 'EDIT-EVIDENCE')`
- `('evidence-merged-start', ..., start.update(tool='read+write'), ..., 1, 'EDIT-EVIDENCE')`.

The landed S086 already satisfies `start_ok` (one `line`/`tool`/`path` per element, all paths under
`LANE`), so the landed measurement is unchanged. This is about six lines plus fixtures: no decision
tuple, preregister triple, claim metric or document contract changes.

If the wave also wants the contradiction vectors closed, the cheapest additions are
`found[0][6] != '<landed teaches text>'` in the S086 gate and pinning
`cells[0] == ['ID','Decision','Reason','Evidence','Policy']`; both are one comparison each and
mirror the tool's existing literal-pinning style. Without them the row can be validated while the
same corpus asserts the opposite (F1/F2/F3).

## 9. Residual unknowns

- No execution: PASS and finding-set claims above are code-path inferences. `main()` reads all five
  inputs from a git revision via `git_read()` (tool lines 252–259; call at 276), so reproducing a counterfactual
  requires committing it; the reading itself does not depend on the commit.
- `transcript_sha256` provenance is shape-only (64 lowercase hex) and never recomputed; S086's
  `mined` status therefore also rests on a regex `[OBSERVED]`. This is adjacent to the attacked row
  and not fixed by the remedy above.
- The seat supplied one digest only for the tool; knowledge/SOURCES/evidence digests were not
  supplied and were not computed.
- I did not read `SCORECARD`, `_revision.py`, or any lesson file; the verdict is restricted to the
  declared read set.

Lane bounds: leaf member — no subagent dispatch.
Reviewed-SHA256: 620f3e5bad34c4ba77a0f0e458bedd79cb05b04a5b1d90200c0baf60038e5081
Predicate: r23f-fxc1expansion
Scope: executed=none
