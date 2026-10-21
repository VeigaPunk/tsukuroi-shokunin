# FxC1OpaquePatch — C1 row `OPAQUE_PATCH` → `UNKNOWN` falsification

- Seat: `TsukuroiR23-2.FxC1OpaquePatch-2` (reviewer, falsify wave, round 23 attempt 1).
- Target under review: `candidate/tools/check-edit-contract.py`, declared SHA256 `620f3e5bad34c4ba77a0f0e458bedd79cb05b04a5b1d90200c0baf60038e5081` (supplied identity; not independently computed, not hashed, not executed).
- Baseline: `ae01e50f582016384e620022be38bf5367000e2e`; landed copy read from `candidate/` at `.ufo/waves/round-23/candidate/`.
- Nothing was executed, installed, fetched, delegated, or edited outside this report. Only the declared local files were read. No digest was computed.

## 1. Attacked claim

**C1 (axis `depth`, metric `validated_edit_decisions`, before 0 → target 8).** C1's scope text says: "Eight finite source-grounded structured-edit authority decisions; new document contract, not eight repaired runtime behaviors."

The specific sub-claim attacked is the one this row carries:

- row id `OPAQUE_PATCH`, decision `UNKNOWN`, reason "Missing structured target is not inferred from opaque patch text" (tool `EXPECTED[4]`, corpus JSON row, corpus Markdown row, and `preregister.json` `edit_decisions[4]`);
- the invariant it asserts downstream (corpus `structured-edit-r23.md` "Bounded procedure" steps 2–3 and `corpus/QUALITY.md` rule R23-EDIT-AUTHORITY): an opaque patch body never grants authority, a missing structured target is never inferred from patch text, and `UNKNOWN` means could-not-evaluate or rejection, **never permission**.

The claim under test is therefore: *the C1 gate's `validated_edit_decisions == 8` is evidence that the OPAQUE_PATCH decision and its "never infer / never permission" meaning are attested.* The gate is a document-literal validator, so the question is exactly how much of that meaning it can fail to see.

## 2. Landed row vs preregistered tuple

| item | preregistered tuple | landed | match |
|---|---|---|---|
| `preregister.json` `edit_decisions[4]` | `["OPAQUE_PATCH","UNKNOWN","Missing structured target is not inferred from opaque patch text"]` | — | — |
| tool `EXPECTED[4]` | — | `('OPAQUE_PATCH','UNKNOWN','Missing structured target is not inferred from opaque patch text','S086','round23-preregister')` | first three == preregistered |
| `corpus/knowledge/structured-edit-r23.json` row 5 | — | `id/decision/reason/evidence/policy` = the five expected strings, exactly that key set | == `EXPECTED[4]` |
| `corpus/knowledge/structured-edit-r23.md` line 19 | — | `\| OPAQUE_PATCH \| UNKNOWN \| Missing structured target is not inferred from opaque patch text \| S086 \| round23-preregister \|` | == `EXPECTED[4]` |

**No drift:** the landed row equals the preregistered tuple on the first three fields, and the JSON row and the Markdown row are byte-equal to the tool's `EXPECTED[4]`. The landed corpus document is also internally consistent today (step 2 "Opaque body data is not interpreted or executed by the auditor", step 3 "…never gain authority by inference. Unknown means could-not-evaluate or rejection, never permission", and the `LIMIT` string "…no native prevention, opaque patch interpretation, effect or reading proof"). So the falsification below is **not** a claim that the landed artifact is self-contradictory; it is a claim that the C1 gate cannot tell a contradicting artifact from a clean one.

## 3. Concrete falsifier (smallest literal input)

### 3.1 What the gate actually checks (read from `evaluate()` / `table_cells()` / `visible()`)

`main()` reads five files at the bound revision: `corpus/knowledge/structured-edit-r23.json` (`DATA`), `corpus/knowledge/structured-edit-r23.md` (`PROSE`), `corpus/SOURCES.md`, `.ufo/waves/round-23/sources/structured-edit-observations.json` (`EVIDENCE`), `.ufo/waves/round-23/preregister.json` (`PREREGISTER`).

For each of the eight ids, `evaluate()` computes:

```python
correct  = row is not None and set(row) == {'id','decision','reason','evidence','policy'} \
           and tuple(row.get(k) for k in ('id','decision','reason','evidence','policy')) == expected
matches  = [r for r in cells if r and r[0] == ident]     # cells = table_cells(prose)
if not correct or matches != [list(expected)]:
    add('EDIT-DECISION-MISMATCH', ident)
```

Consequences that the falsifier exploits:

1. `table_cells()` only keeps lines containing `|` (`if '|' not in line: continue`), so **any non-table prose line in the Markdown is invisible to the decision check**. The only prose requirement is `PROSE_LIMIT in '\n'.join(visible(text))` — a substring test for the literal "It is not native permission enforcement". No sentence of the prose is required, and no sentence of the prose is inspected for agreement with the decision table.
2. `matches` is computed with a **byte-exact** first-cell comparison (`r[0] == ident`). A Markdown-inline-decorated id (`**OPAQUE_PATCH**`, `` `OPAQUE_PATCH` ``) is not byte-equal to `OPAQUE_PATCH`, so such a row is not counted as a second occurrence of the id, and it raises no finding.
3. The gate's own scope disclaimer is itself only a string equality (`data.get('scope') != LIMIT`) plus a substring presence test for `PROSE_LIMIT`. Nothing checks that the document does not assert the opposite of `LIMIT`.

### 3.2 Falsifier F1 (prose contradiction — no Markdown trick, one line changed)

Input delta: **one line in one file**; JSON, SOURCES.md, preregister.json and the evidence source are untouched.

In `corpus/knowledge/structured-edit-r23.md`, replace in step 3 of "Bounded procedure" the sentence

```
Unknown means could-not-evaluate or rejection, never permission.
```

with

```
Unknown is recorded as provisional permission whenever the patch text names a path.
```

Expected gate result: `status PASS`, exit `0`, `validated_edit_decisions: 8`, `total_decisions: 8`, `findings: []`.

Why, line by line:
- `raw` is unchanged, so `data['schema']`, the exact top-level key set, the eight unique ids and all eight row tuples still satisfy `correct` for every id, including `OPAQUE_PATCH` (`UNKNOWN` + the preregistered reason + `S086` + `round23-preregister`).
- The edited sentence contains no `|`, so `table_cells()` skips it (`'|' not in line`); the eight canonical table rows are untouched, so `matches == [list(expected)]` still holds for every id, including `OPAQUE_PATCH`.
- `PROSE_LIMIT` ("It is not native permission enforcement") is still present in the final paragraph, so `EDIT-LIMIT-MISSING` does not fire; `data['scope'] == LIMIT` is unchanged.
- `evidence_ok(EVIDENCE)` and the preregister comparison are untouched, so `EDIT-EVIDENCE` / `EDIT-POLICY-SOURCE` / `EDIT-SOURCE` do not fire.
- `count` stays 8 (the zeroing branch `if any(f['id'] != 'EDIT-DECISION-MISMATCH' …)` is not reached).

Meaning violated: the document now states, in the same authoritative contract that the C1 gate certifies, that `UNKNOWN` is provisional permission and that patch text names the path — i.e. exactly the inference the row's reason forbids ("Missing structured target is not inferred from opaque patch text") and exactly the reading `LIMIT` disclaims ("no native prevention, opaque patch interpretation, effect or reading proof"). The gate reports the row as validated.

### 3.3 Falsifier F2 (contradictory decision row for the same id — one line added)

Input delta: **one line added** to the existing "Decision table" of `corpus/knowledge/structured-edit-r23.md` (nothing else changes):

```
| **OPAQUE_PATCH** | ALLOW | Opaque patch text names the target, so the edit proceeds | S086 | round23-preregister |
```

Expected gate result: identical — `status PASS`, exit `0`, `validated_edit_decisions: 8`, `findings: []`.

Why: `table_cells()` yields the added row with first cell `'**OPAQUE_PATCH**'`, which is not byte-equal to `'OPAQUE_PATCH'`, so `matches` for that id is still exactly `[list(expected)]` and no `EDIT-DECISION-MISMATCH` is raised. The rendered contract now contains two rows for the same decision id with conflicting decisions (`UNKNOWN` and `ALLOW`). The gate reports 8/8 validated.

### 3.4 Falsifier F3 (co-moved edit of tool + preregister + corpus)

`evaluate()` validates the corpus against the tool's hardcoded `EXPECTED` map **and** validates the preregister against the same map:

```python
if declared != [list(e[:3]) for e in EXPECTED]: add('EDIT-POLICY-SOURCE', PREREGISTER)
```

The preregister is therefore not an independent oracle for the corpus. If `EXPECTED[4]`, `preregister.json` `edit_decisions[4]` and the corpus rows are changed together to `('OPAQUE_PATCH','ALLOW','Opaque patch text names the target, so the edit proceeds')`, the gate still returns PASS with `validated_edit_decisions: 8` — the OPAQUE_PATCH row's meaning is fully inverted and nothing in the tool detects it. [INFERENCE] In r23 the preregister was written before landing, so process (not the tool) is what prevents this co-move; the gate itself provides no protection.

## 4. Bounded search that found none (what *is* pinned)

The following surfaces were checked and are **not** attackable for this row:

- **Canonical JSON row.** `set(row)` must equal exactly `{'id','decision','reason','evidence','policy'}` and the 5-tuple must equal `EXPECTED[4]`; any change to `decision`/`reason`/`evidence`/`policy`, any extra key, any missing key raises `EDIT-DECISION-MISMATCH`; a changed top-level key set or a duplicated JSON key raises `EDIT-SCHEMA`. The `OPAQUE_PATCH` decision literal in the JSON is therefore pinned.
- **Canonical Markdown row.** The matched row must be exactly `[id, decision, reason, evidence, policy]` and must be the only row whose first cell is byte-equal to the id; a second literal row (even inside a blockquote — `table_cells()` strips leading `>`), a renamed id, a hidden row (HTML comment or fenced block, both removed by `visible()`) or a mutated cell all raise `EDIT-DECISION-MISMATCH`. The canonical row's *decision value* is pinned; only *non-canonical* rows and non-table prose escape (F1–F3).
- **`corpus/SOURCES.md`.** The S086 row is pinned to 11 cells, `own-work`, tier `A`, status `mined`, path suffix `.ufo/waves/round-23/sources/structured-edit-observations.json`, no backslash in any cell, exactly one `S086` row. Rows with other ids are unconstrained (a `S087` row asserting patch interpretation would pass), but that is a registry statement, not the decision row.
- **Evidence source.** `evidence_ok()` pins the schema, `tool == 'edit'`, the two observed argument-key shapes `{'path','stream_content'}` and `{'path','old_string','new_string'}` (a third shape, e.g. `'patch'`, fails), `body_fields`, lane-prefixed paths, non-empty `recorded_starts` and 64-hex transcript digests. No evidence field can encode a decision for `OPAQUE_PATCH`.
- **`preregister.json`** as shipped is consistent with the landed row (section 2), so no pre-registration drift exists today.

Conclusion: **no falsifier exists that changes the canonical `OPAQUE_PATCH` row's decision literal** — the JSON tuple, the matched Markdown row and the preregistered tuple are triple-pinned against the tool's hardcoded `EXPECTED`. The falsifiers that do exist (F1–F3) all exploit the same hole: **the gate attests literal decision-table conformance, not the row's meaning**, and the meaning-bearing surface (the prose of the contract, plus any additional rendered row for the same id) is outside its reach.

## 5. Findings by severity

**F-1 (High, C1) — the C1 metric cannot detect a document that asserts the opposite of the row it validates.**
`evaluate()`'s only prose requirement is a substring test for `PROSE_LIMIT`; `table_cells()` discards every prose line without `|`. Therefore `validated_edit_decisions == 8` is compatible with a contract document that states `UNKNOWN` is provisional permission and that patch text names the target (F1/F3), i.e. with a direct violation of the OPAQUE_PATCH reason "Missing structured target is not inferred from opaque patch text" and of the `LIMIT` string "no native prevention, opaque patch interpretation, effect or reading proof". The claim as written in `preregister.json` ("Eight finite source-grounded structured-edit authority decisions") reads as semantic validation; the gate delivers literal conformance. The gap is one line of corpus Markdown away from being invisible.
Evidence: `candidate/tools/check-edit-contract.py` — `table_cells()` (`if '|' not in line: continue`), `evaluate()` (`PROSE_LIMIT not in '\n'.join(visible(text))`, `data.get('scope') != LIMIT`), and the per-id block `matches = [r for r in cells if r and r[0] == ident]`.

**F-2 (Medium, C1) — id uniqueness is byte-exact, so a second rendered row for the same decision id is invisible.**
F2 adds a rendered `OPAQUE_PATCH … ALLOW` row that the gate does not count. Any future row added to the corpus for the same id with a different decision value (which is exactly how a policy table drifts) passes the gate silently. This is the general form of the F1 hole and the one a future editor would hit.
Evidence: `table_cells()` returns raw stripped cells; `evaluate()` compares `r[0] == ident` with no Markdown-inline normalization.

**F-3 (Medium, C1, structural) — the preregister is not an independent oracle for the corpus.**
Both the corpus and `preregister.json` are compared against the same hardcoded `EXPECTED` tuple, so a co-moved edit of tool + preregister + corpus inverts the OPAQUE_PATCH row with the gate still reporting 8/8. [INFERENCE] Pre-registration ordering in the round process is the only thing standing between the two.
Evidence: `evaluate()` — `if declared != [list(e[:3]) for e in EXPECTED]: add('EDIT-POLICY-SOURCE', PREREGISTER)` and `tuple(row.get(k) …) == expected` with `expected` drawn from the same `EXPECTED`.

**F-4 (Low, adjacent row — `EDIT_TRAVERSAL`, not `OPAQUE_PATCH`; no effect on this verdict).**
`evidence_ok()` checks the observed path with `'/../' not in row['path']` plus `row['path'].startswith(LANE)`. A path whose last segment is `..` (e.g. `…/tsukuroi-shokunin/..`) contains no `'/../'` substring, so it passes the S086 shape check while resolving outside the lane root. Belongs to the traversal row, which is not this seat's row; flagged for the owning seat only.

## 6. Smallest in-scope remedy

1. **For F-2 (closes the only decision-flipping falsifier):** normalize each table cell's Markdown inline markup before comparing it to a decision id, and require that exactly one visible row in the whole document has a normalized first cell equal to each of the eight ids. Concretely, in `table_cells()` strip leading/trailing `*`, `_`, `` ` `` from every cell, and in `evaluate()` compute `matches` over normalized cells and additionally reject any other visible row whose normalized first cell equals a known id. F2 then raises `EDIT-DECISION-MISMATCH` instead of passing. (~6 lines; no new dependency.)
2. **For F-1 and F-3 (honesty, not a fix):** narrow the attested scope rather than pretend to check prose. The smallest honest change is to the C1 claim/scope text in `preregister.json` and to the corpus's own "QUALITY check" paragraph: state that the gate attests **exact decision-table literal conformance** (id set, decision, reason, evidence, policy, and the pinned S086/preregister mappings), and that the semantic coherence of the surrounding prose — including "opaque patch bodies are never interpreted" and "`UNKNOWN` is never permission" — is **declared, not machine-verified**. Optionally bind those two sentences as *required literals* so their presence is checked; that pins the authoritative statement without pretending to detect a contradicting one.
3. **For F-3:** keep the preregister as the independent pin by comparing the corpus against `preregister.json` `edit_decisions` and the tool's `EXPECTED` against the preregister, rather than comparing both to the tool's map — a co-moved edit then has to break one of the two comparisons. (Implementation-order caveat: the tool's own `EXPECTED` is what the preregister would be compared against, so a genuine independent third pin would have to live outside the tool.)
4. **Not recommended:** any attempt to machine-verify arbitrary prose meaning. It is unbounded, and the round's own limits already state there is no native restrictive tool interface; the honest move is to stop the metric from implying it.

## 7. Residual risk and verification gaps

- **No execution.** The falsifier outcomes above are derived by reading `evaluate()`, `table_cells()`, `visible()` and `evidence_ok()` in the landed file; the checker was never run, so "expected gate result" is a code-reading prediction, not an observation. A sibling seat with execution rights should replay F1 and F2 once to confirm `status PASS`, `validated_edit_decisions: 8`, `findings: []`.
- **Rendering of the decorated id (F2) is not observed.** The claim that `**OPAQUE_PATCH**` renders as `OPAQUE_PATCH` in the corpus's Markdown reader follows standard CommonMark, not an observation of this repository's renderer. F1 and F3 do not depend on any rendering behaviour and stand on the source text alone.
- **The digest was not verified.** `620f3e5b…5081` is the supplied identity of the reviewed file; it was not hashed, listed, or executed.
- **Semantic enforcement of the invariant remains absent regardless of this report.** Even with the C1 gate fixed, the "opaque patch never grants authority / `UNKNOWN` is never permission" invariant has no runtime enforcer in this lane (per the round's own limits, "No native per-seat restrictive tool interface exists"); C1 attests a document, not a runtime.
- **Scope of this seat.** Only the `OPAQUE_PATCH` row was attacked. F-4 is reported only as a cross-row pointer; the other seven rows were not assessed here, and sibling falsify seats own them.
- **Unpinned surfaces not attacked here:** `corpus/QUALITY.md` (which states the same invariant as rule R23-EDIT-AUTHORITY) is never read by `check-edit-contract.py` at all, so it can contradict the corpus document freely; `corpus/SOURCES.md` rows with ids other than `S086` are unconstrained. Both are recorded as residual risk, not as findings of this row.

    Reviewed-SHA256: 620f3e5bad34c4ba77a0f0e458bedd79cb05b04a5b1d90200c0baf60038e5081
    Predicate: r23f-fxc1opaquepatch
    Scope: executed=none
    Lane bounds: leaf member — no subagent dispatch.
