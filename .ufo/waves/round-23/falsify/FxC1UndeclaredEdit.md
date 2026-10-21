# FxC1UndeclaredEdit — attack on C1 row `UNDECLARED_EDIT` → `DENY`

Seat FxC1UndeclaredEdit, round-23 falsify wave, attempt 1, from integrated landed state
5a25c88b77f52e940bcad87825c4ac1cd529470d, baseline
ae01e50f582016384e620022be38bf5367000e2e. Read-only attack; no execution.

## Attacked claim

C1 (`preregister.json` `claims[0]`): axis `depth`, metric `validated_edit_decisions`,
before 0, target 8, command `python3 tools/check-edit-contract.py --revision <REV>`,
scope "Eight finite source-grounded structured-edit authority decisions; new document
contract, not eight repaired runtime behaviors."

Attacked row tuple (`EXPECTED[1]`, `round23-preregister` `edit_decisions[1]`, landed JSON
row, landed table row — all four agree):

```
UNDECLARED_EDIT | DENY | No implicit edit permission from generic report ownership | S086 | round23-preregister
```

The row's meaning: a structured edit whose target is not explicitly predeclared for that
seat is denied; generic report ownership by itself confers no edit authority.

## A. Landed versus preregistered tuple (observed)

- `preregister.json` `edit_decisions[1]` is the exact triple
  `["UNDECLARED_EDIT", "DENY", "No implicit edit permission from generic report ownership"]`.
- Landed `corpus/knowledge/structured-edit-r23.json` decision object for `UNDECLARED_EDIT`
  is the exact five-tuple above; `corpus/knowledge/structured-edit-r23.md` line 16 is the
  exact five table cells above.
- The landed validated contract is strictly wider than the preregistered one: `evidence`
  (`S086`) and `policy` (`round23-preregister`) exist only in the checker's `EXPECTED`
  constant and are identical across all eight rows. `evaluate()` checks the preregister
  only for `[list(e[:3]) for e in EXPECTED]`, so those two extra fields are unpreregistered
  but uniform; no per-row drift.
- Result: no drift between preregistered meaning and landed row. The row is landed correctly.

## B. Row-level bounded search: no falsifier exists

Every surface that can carry the row is closed by exact equality in `evaluate()`:

1. `json.loads(raw, object_pairs_hook=unique)` — duplicate JSON keys raise, giving
   `EDIT-SCHEMA`.
2. `set(data) == {'schema', 'decisions', 'source_path', 'scope'}`, `schema ==
   'tsukuroi-edit-policy-v1'` — no extra or missing top-level JSON field.
3. Exactly 8 rows and 8 unique `id` values — no duplicate or substituted row.
4. `set(row) == {'id', 'decision', 'reason', 'evidence', 'policy'}` and the ordered
   five-tuple equals `EXPECTED` — the JSON row cannot differ and be counted.
5. `matches = [r for r in table_cells(text) if r and r[0] == 'UNDECLARED_EDIT']` and
   `matches != [list(expected)]` — exactly one rendered table row, exact five stripped
   cells; a second row, a renamed row, or a missing row gives `EDIT-DECISION-MISMATCH`.
6. `pre.get('edit_decisions') == [list(e[:3]) for e in EXPECTED]` — the preregister triple
   is exact and ordered, else `EDIT-POLICY-SOURCE`.
7. `data.get('scope') == LIMIT` and `PROSE_LIMIT in '\n'.join(visible(text))` — exact scope
   string and presence of "It is not native permission enforcement", else
   `EDIT-LIMIT-MISSING`.
8. `found` on `corpus/SOURCES.md`: exactly one `S086` row, 11 cells, cell 1 tail after the
   last ` — ` equals the evidence path, cells 2:4 are `own-work`/`A`, cell 7 is `mined`, no
   backslash — else `EDIT-SOURCE`.

Consequently no knowledge-JSON row, rendered table row, SOURCES row, or preregister triple
can be altered while this row still increments `validated_edit_decisions`. The count is a
literal conjunction, and at cell level the row is airtight.

## C. Falsifier found: carrier-level contradiction is invisible to the count

Smallest literal Markdown input: one clause substitution in
`corpus/knowledge/structured-edit-r23.md` line 9 (the only policy paragraph outside the
table). No line is added or removed and no table row is touched.

```diff
 Authority is separately declared lane policy. A source-only report writer can be granted
 exact prospective report-read/write/edit targets before dispatch;
-report ownership alone never grants extra reads or an edit.
+report ownership alone grants extra reads and an edit.
 Schema-v1 historical bindings remain unchanged and retain all earlier violations.
 No grant is retroactive.
```

(The same-byte variant `never` → `always` in place of `never grants` → `grants` behaves
identically. An additive one-line grant appended to the same file behaves identically too;
the additive form is the one that defeats substring sentinels.)

Code-path trace with all other inputs held at landed bytes:

- `visible()`: the edited line is not inside an HTML comment, not inside a fence, and does
  not start with four spaces, so it is appended to the visible lines. It survives.
- `table_cells()`: the line contains no `|`, so it produces no row and never enters
  `cells`; `matches` for `UNDECLARED_EDIT` is still exactly `[list(expected)]`.
- The only prose-level gate is `PROSE_LIMIT not in '\n'.join(visible(text))`. The limit
  paragraph is untouched, so the substring "It is not native permission enforcement" is
  still present; adding prose can never remove it, so the gate is monotone-safe.
- JSON, `source_path`, evidence, SOURCES row, and preregister `edit_decisions` are unchanged,
  so gates 1–8 above all pass.
- Therefore `evaluate()` returns code 0 with findings `[]`, `status: PASS`,
  `validated_edit_decisions: 8`, and `UNDECLARED_EDIT` is one of the eight counted rows —
  while the same carrier document now states that generic report ownership grants an edit,
  the exact authority the row denies. The decision row is no longer an exhaustive statement
  of the document contract.

Landed-state status: the landed line 9 currently reads "never grants", so the shipped
artifact is not self-contradictory. This is a checker-acceptance falsifier (input the landed
tool would certify), not a defect already present in the landed document.

## D. Same validation class elsewhere (supporting, not required for C)

- `corpus/SOURCES.md` S086 row: only cell 1's tail after the last ` — `, cells 2:4, and
  cell 7 are checked. Cell 1 may be prefixed with arbitrary text and cells 4 (scope),
  6 (teaches), 9, 10 are unchecked, so the cited source row can carry a contradicting
  claim and still pass `EDIT-SOURCE`.
- `preregister.json`: `evaluate()` reads only `.get('edit_decisions')`; the document is not
  schema-checked, so an extra top-level grant key beside the frozen eight triples is
  ignored.
- `evidence_ok()`: accepts any lane-prefixed path without `/../`, any number of observations,
  and only requires the shape set to equal `SHAPES`. It compares the recorded paths against
  no declared authority set at all, so the cited evidence stream cannot contradict or
  corroborate the `UNDECLARED_EDIT` decision as far as the checker is concerned.

These are the same root cause: the tool validates a literal subset (cells, triples, shapes)
and treats every remaining byte of the carriers as unchecked.

## E. Smallest in-scope remedy

Primary (closes the demonstrated class, auditor-only, no runtime claim): make the Markdown
carrier closed-world for non-table prose in `evaluate()`:

- Add a literal tuple `PROSE_LINES` beside `PROSE_LIMIT` holding every visible, non-table,
  non-blank line of `structured-edit-r23.md` (header lines 1–3, heading, the three prose
  paragraphs, the numbered procedure, and the limit paragraph).
- Compute `prose_lines = [line for line in visible(text) if line.strip() and '|' not in line]`
  and add `EDIT-PROSE` to `findings` unless `prose_lines == list(PROSE_LINES)`.
- Include `EDIT-PROSE` among the non-mismatch ids that zero `count`, and add one selftest
  case that appends a single grant line and expects `EDIT-PROSE` (positive control: the
  clean fixture builds its prose from `PROSE_LINES` plus the decision table).

Cost: one constant plus roughly five lines in `evaluate()` and one selftest case. This
also rejects the one-clause substitution in C.

Why not a cheaper sentinel: adding the exact sentence "report ownership alone never grants
extra reads or an edit" as a second required substring would pass the deletion variant only
if the sentence is fully restated, and would still pass an additive grant line elsewhere in
the file. The demonstrated class includes additions, so only exact equality of the
non-table prose closes it.

Fallback if the landed code is frozen: disclose the narrower contract in the artifact limit
and the round-23 lesson — the checker validates the decision table rows, the declared limit
sentence, and the finite S086 cells only, and does not certify consistency of any other
prose in the carrier — and stop reading `validated_edit_decisions` as a document-contract
guarantee. That is honest but weaker; it leaves C1's "new document contract" wording
unsupported at carrier level.

## F. Confidence and residual gaps

- High confidence in A, B, and the C code-path: derived from exact expressions in
  `check-edit-contract.py` (`evaluate`, `visible`, `table_cells`, `evidence_ok`).
- `executed=none`: the PASS/8 result for the mutation is a static derivation, not an
  observed run; no command, interpreter, hash, or test was invoked.
- No landed-state defect was found for this row; the row matches its preregistered meaning.
- The residual risk is claim strength, not row text: `validated_edit_decisions=8` cannot
  distinguish a coherent carrier from one that both denies and grants the attacked
  authority, because non-table prose and the preregister beyond `edit_decisions` are
  unchecked.
- Not read (outside seat read paths): sibling falsify reports, the C2 and C3 tools.

Reviewed-SHA256: 620f3e5bad34c4ba77a0f0e458bedd79cb05b04a5b1d90200c0baf60038e5081
Predicate: r23f-fxc1undeclarededit
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
