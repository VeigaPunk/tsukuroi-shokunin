# FxC1ReadOnlyEdit — C1 row `READ_ONLY_EDIT -> DENY` falsification

Target: `.ufo/waves/round-23/candidate/tools/check-edit-contract.py` (declared SHA256
`620f3e5bad34c4ba77a0f0e458bedd79cb05b04a5b1d90200c0baf60038e5081`, supplied identity — not
independently computed; no hash/list/run performed in this seat).

Seat scope: read-only static review of the landed checker, the landed corpus carriers and the
preregistered tuple. NO-EXEC / NO-FETCH honoured: nothing was executed, imported, hashed, listed
or counted; every claim below is derived from reading the landed bytes.

## 1. Attacked claim

**C1** (preregister `claims[0]`, `axis: depth`, `metric: validated_edit_decisions`,
`before: 0`, `target: 8`). The claim under attack is not the *string* `READ_ONLY_EDIT -> DENY` —
it is that a PASS with `validated_edit_decisions == 8` is evidence that the landed corpus carries
the eight decisions **without contradicting them**. Specifically: can a literal JSON / Markdown /
SOURCES / preregister input be counted as *validated for the READ_ONLY_EDIT row* while the row's
meaning is violated?

## 2. Landed row vs preregistered tuple (comparison)

Landed `corpus/knowledge/structured-edit-r23.json` row (identical in kind to the other seven):

```
id=READ_ONLY_EDIT  decision=DENY  reason=Read authority never grants a write
evidence=S086      policy=round23-preregister
```

Landed `corpus/knowledge/structured-edit-r23.md` decision-table row:

```
| READ_ONLY_EDIT | DENY | Read authority never grants a write | S086 | round23-preregister |
```

Preregistered tuple (`.ufo/waves/round-23/preregister.json`, `edit_decisions[2]`):

```
["READ_ONLY_EDIT", "DENY", "Read authority never grants a write"]
```

**Verdict: the landed row is exactly equal to the preregistered tuple** (id, decision, reason;
evidence/policy are lane-constant). No divergence. The attack below therefore targets the
*checker that certifies the row*, not the row text itself.

## 3. What the landed checker actually enforces for this row

`evaluate()` (lines 124–162) binds the row through three independent layers:

| Layer | Code | Constraint on `READ_ONLY_EDIT` |
|---|---|---|
| JSON row | 147–148 | `set(row) == {'id','decision','reason','evidence','policy'}` **and** `tuple(row.get(k) ...) == expected` where `expected = ('READ_ONLY_EDIT','DENY','Read authority never grants a write','S086','round23-preregister')` — exact string equality, extra fields rejected, `unique()` (38–42) rejects duplicate JSON keys, top-level key set fixed at 125 |
| Markdown carrier | 149–150 | `matches = [r for r in cells if r and r[0] == ident]` and `matches != [list(expected)]` → **exactly one** extracted table row whose *first cell is the byte string* `READ_ONLY_EDIT`, and that row's five cells equal the expected tuple |
| Preregister | 135–136 | `declared != [list(e[:3]) for e in EXPECTED]` → the preregistered eight triples must equal the checker's own `EXPECTED` constant (26–35) |
| SOURCES | 137–141 | exactly one S086 row; `len(found[0]) == 11`; `found[0][1]` must end with the evidence path; `found[0][2:4] == ['own-work','A']`; `found[0][7] == 'mined'`; no backslash in any cell |
| Scope / limit | 154–155 | `data['scope'] == LIMIT` and `PROSE_LIMIT` (`It is not native permission enforcement`) present in `'\n'.join(visible(text))` |

Carrier extraction (`visible()` 45–74, `table_cells()` 77–93): strips HTML comments, drops fenced
code blocks, drops 4-space-indented lines, strips leading `>` blockquote markers, then splits on
`|`, trims the leading/trailing empties and `strip()`s each cell.

**Bounded search over the constrained layers (no falsifier found):** because the JSON row must be
byte-identical to `EXPECTED[2]`, because the Markdown canonical row must be byte-identical, and
because the preregistered tuple must equal `EXPECTED`, there is **no** falsifier for this row that
keeps the canonical decision carrier and flips its meaning. The row's *decision value* cannot be
forged. This part of the design is sound and I do not attack it.

The defect is in the **unconstrained carrier space around** the canonical row: the checker
verifies that one literal row exists, not that the document does not *also* assert the opposite.

## 4. Concrete falsifier (smallest literal input)

### F1 — one added Markdown table row (primary; JSON, SOURCES, preregister unchanged)

Add exactly one line to `corpus/knowledge/structured-edit-r23.md`, immediately after the
canonical `READ_ONLY_EDIT` row:

```
| **READ_ONLY_EDIT** | ALLOW | Read authority grants a write | S086 | round23-preregister |
```

Nothing else changes: `structured-edit-r23.json`, `corpus/SOURCES.md`,
`.ufo/waves/round-23/preregister.json` and the observations source stay byte-identical.

Why the landed checker still counts this row as validated (traced through the landed code):

1. `visible()` (45–74): the line is not inside a fence, holds no `<!--`, is not 4-space indented
   → it is emitted as a normal line.
2. `table_cells()` (77–93): `line.split('|')` → 5 cells → first cell `**READ_ONLY_EDIT**`.
   `r[0] == 'READ_ONLY_EDIT'` is **False**, so at line 149 this row is *not* a `match` for any
   expected ident.
3. Line 149–150: `matches` for ident `READ_ONLY_EDIT` is still exactly `[list(expected)]` — the
   canonical row alone. Condition `not correct or matches != [list(expected)]` is **False** → no
   `EDIT-DECISION-MISMATCH`, `count += 1` (153).
4. Lines 137–141 (SOURCES), 135–136 (preregister), 133–134 (evidence), 154–155 (scope/limit):
   untouched, still satisfied.
5. Line 156: `code = 1 if findings else 0` → `0`; 162: `status = 'PASS'`,
   `validated_edit_decisions = 8`.

Meanwhile a human reading the rendered decision table sees **two** rows whose ID renders as
`READ_ONLY_EDIT` — the canonical `DENY` row and a bold `ALLOW` row stating "Read authority grants
a write". The rendered meaning of the row is violated; the checker reports 8/8 validated.

Markdown-rendering note (why the wrapper is what defeats the filter): `**READ_ONLY_EDIT**`,
`` `READ_ONLY_EDIT` `` and `[READ_ONLY_EDIT](#read-only-edit)` all render with the identifier text
`READ_ONLY_EDIT`, but their *literal* first cells are different byte strings, so `r[0] == ident`
never fires. The checker's carrier model is a literal-string model, and the corpus document is a
Markdown document whose identifiers are rendered, not literal.

### F2 — one added Markdown prose sentence (even smaller; no table carrier)

Add exactly one prose line to `structured-edit-r23.md`:

```
Note: READ_ONLY_EDIT is ALLOW; read authority alone is sufficient for an edit.
```

`table_cells()` ignores it (no `|`); line 149's filter is scoped to table rows; line 154 only
requires `PROSE_LIMIT` to be *present*, not to be the only normative statement. Result: PASS,
`validated_edit_decisions == 8`, while the document body asserts the opposite of the row.

### F3 — one rewritten SOURCES cell (source registry)

In `corpus/SOURCES.md`, the S086 row's **7th cell (`teaches`)** is unconstrained: line 138–141
checks only the cell *count* (11), the source-path suffix, kind/tier (`own-work`, `A`), status
(`mined`) and backslash absence. Cells 5–7 (`scope`, `anchor`, `teaches`) may carry any text.
Rewriting `teaches` to "a read-only report writer may edit the target because read authority
grants the write" passes every check while contradicting the very rule the row cites S086 for.

### F4 — amplifier: hide the canonical row from the rendered table

`visible()` does not model HTML blocks. Placing the canonical
`| READ_ONLY_EDIT | DENY | ... |` line inside a raw `<div>` block keeps it in `cells` (so it is
still the counted `match`) while CommonMark renders it as raw text, not as a decision-table row.
Combined with F1, the rendered decision table then shows only `ALLOW` for `READ_ONLY_EDIT` while
the checker certifies the `DENY` carrier. F4 alone is weaker (the literal text is still on the
page); it is listed because it converts F1/F2 from "ambiguous document" into "document whose
rendered decision table contradicts the certified row".

### What F1–F4 do **not** show

No falsifier was found that flips the canonical row's `decision` value, weakens its `reason`, or
makes the preregistered tuple disagree with the landed row. The JSON layer (125, 147–148), the
preregister layer (135–136) and the canonical Markdown row (149–150) are hard-anchored on the
checker's own `EXPECTED` constant. The eight decision strings themselves are not forgeable.

## 5. Comparison with the checker's own negative-control family

The selftest already models the blockquote duplicate (`'quoted-duplicate'`, prose line prefixed
with `> | READ_ONLY_EDIT | ALLOW | ...`), and `table_cells()` strips `>` (83–84) so that case is
caught. That shows the authors reasoned about *duplicate carriers* — but only about the one
wrapper (blockquote prefix) that `table_cells()` happens to normalise. The wrapper family is
incomplete: emphasis, code-span, link and prose carriers are unmodelled, and there is no negative
control for them. The gap is a gap in the *control set*, not in the intent.

The tool is partially self-aware: `visible()`'s docstring says "Finite Markdown table carrier
rules, not a general rendered-prose theorem", and the corpus MD limits the artifact to "declared
post-hoc audit authority only". So this is a bounded, declared limitation of the C1 artifact —
but C1's *metric* (`validated_edit_decisions`) is a positive depth counter reported as 8 with
`status: PASS`, and nothing in that metric discloses that the corpus may simultaneously assert the
negation of a certified row.

## 6. Smallest in-scope remedy

Single-site change in `tools/check-edit-contract.py`, inside the per-ident loop (144–153):

1. **Normalised duplicate rejection (covers F1).** Replace `r[0] == ident` with a comparison of a
   normalised identifier — strip Markdown inline wrappers (`**`, `__`, `*`, `_`, backticks) and
   `[text](url)` link syntax, then compare case-insensitively. Any table row whose normalised ID
   equals an expected ident must be the canonical row; otherwise raise
   `EDIT-DECISION-MISMATCH` (or a new `EDIT-DECISION-AMBIGUOUS` finding).
2. **Extra-occurrence rejection (covers F2).** Require each expected ident to occur exactly once
   in `'\n'.join(visible(text))` — the landed MD satisfies this today, so the check is satisfiable
   without editing the corpus. Any second occurrence (prose, heading, list item) is a finding.
3. **Source-cell binding (covers F3, optional).** Bind S086 cells 5–7 (`scope`, `anchor`,
   `teaches`) to a checked literal, or at minimum reject any that contains a decision token
   (`ALLOW`/`DENY`/`UNKNOWN`/`CHECK_EACH`) or an ident string.

Each remedy must ship with its own negative control in `selftest()`
(`'bold-duplicate'`, `'code-duplicate'`, `'link-duplicate'`, `'prose-contradiction'`,
`'source-teaches-contradiction'`), because the existing control set does not cover them.

The minimal core is item 1 plus one new selftest case; items 2–3 close the residual carriers.

## 7. Severity, residual risk, verification gaps

**Severity: Medium (C1 metric honesty), not a contract break.** The decision *values* are not
forgeable; the defect is that "8 validated decisions" can coexist with a corpus document that
contradicts those decisions. Downstream consumers of the C1 number (SCORECARD, lesson) would
report a fully-validated eight-row contract for a document whose rendered decision table says
`ALLOW`.

**Residual risk not covered by this seat:** C2 (`structured_edit_mode`) and C3
(`unexplained_cohorts`) are separate seats; this report makes no claim about them. The broader
"declared audit authority is not native enforcement" limitation is unchanged and out of scope here.

**Verification gaps:**
- Nothing was executed (NO-EXEC): the F1/F2/F3 outcomes are derived by tracing the landed source
  line by line, not from a run. A confirmatory step for L1 would be to apply F1 to a scratch copy
  of the corpus and observe `status: PASS`, `validated_edit_decisions: 8`.
- The declared SHA256 was taken as supplied identity; it was not recomputed, and no file listing,
  byte count or hash was produced in this seat.
- Renderer-level claims about `**...**`, backticks and link syntax rest on Markdown rendering
  conventions; the checker's behaviour (literal string comparison) is independent of them and is
  the part that matters for the finding.
- F4's rendering argument (CommonMark HTML block type 6) is an inference about a standard
  renderer, not an observed render in this seat; F4 is therefore reported as an amplifier only.

Reviewed-SHA256: 620f3e5bad34c4ba77a0f0e458bedd79cb05b04a5b1d90200c0baf60038e5081
Predicate: r23f-fxc1readonlyedit
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
Report: .ufo/waves/round-23/falsify/FxC1ReadOnlyEdit.md
