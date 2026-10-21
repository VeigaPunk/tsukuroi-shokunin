# FxC1DeclaredEdit — falsification of C1 row `DECLARED_EDIT -> ALLOW`

Seat: `TsukuroiR23-2.FxC1DeclaredEdit` (leaf member — no subagent dispatch; no execution, no fetch).
Lane bounds: leaf member — no subagent dispatch.
Target under attack: `.ufo/waves/round-23/candidate/tools/check-edit-contract.py` (declared SHA256 supplied by the
assignment; **not** independently computed — no hashing, listing, import, compile or run was performed).
Attacked claim: **C1** (`preregister.json` claims[0]: axis `depth`, metric `validated_edit_decisions`, before 0, target 8,
command `python3 tools/check-edit-contract.py --revision <REV>`), and specifically its row
`DECLARED_EDIT -> ALLOW` ("Exact target is predeclared for edit and for both read and write").

Inputs actually read (all declared local paths): `candidate/tools/check-edit-contract.py`,
`.ufo/waves/round-23/preregister.json`, `candidate/corpus/knowledge/structured-edit-r23.json`,
`candidate/corpus/knowledge/structured-edit-r23.md`, `.ufo/waves/round-23/sources/structured-edit-observations.json`,
`candidate/corpus/SOURCES.md`, `.ufo/waves/round-23/sources/godspeed-directive.txt`.
Method: **static reading only**. Every claim below is derived from the evaluator source, not from a run.

---

## 0. Landed row vs preregistered tuple (direct comparison)

| carrier | location | DECLARED_EDIT tuple |
|---|---|---|
| preregistered (policy source) | `preregister.json` → `edit_decisions[0]` | `["DECLARED_EDIT","ALLOW","Exact target is predeclared for edit and for both read and write"]` |
| landed knowledge JSON | `structured-edit-r23.json` → `decisions[0]` | `id=DECLARED_EDIT, decision=ALLOW, reason="Exact target is predeclared for edit and for both read and write", evidence=S086, policy=round23-preregister` |
| landed prose table | `structured-edit-r23.md` → Decision table, row 1 | `\| DECLARED_EDIT \| ALLOW \| Exact target is predeclared for edit and for both read and write \| S086 \| round23-preregister \|` |
| evaluator literal | `check-edit-contract.py` `EXPECTED[0]` | `('DECLARED_EDIT','ALLOW','Exact target is predeclared for edit and for both read and write','S086','round23-preregister')` |

**No drift:** the landed row equals the preregistered tuple character-for-character, and the preregistered tuple equals
the evaluator's own literal. The landed row is therefore *not* a false statement about what was preregistered — the
attack below is not about row drift.

---

## 1. Bounded search: what cannot be falsified (the "no-go" half)

`evaluate()` pins three carriers to the evaluator's own `EXPECTED` literal, so **no literal
JSON / Markdown / SOURCES / preregister input can make the tool report `DECLARED_EDIT` validated with a different
decision value, reason, evidence or policy**:

* JSON row — `check-edit-contract.py:146-147`: `set(row) == {'id','decision','reason','evidence','policy'}` **and**
  `tuple(row.get(k) for k in ('id','decision','reason','evidence','policy')) == expected`. Any change to `decision`
  (`ALLOW`→`DENY`), to `reason`, to `evidence` (`S086`→`S085`) or to `policy` fails the equality, and any added key
  fails the set equality → `EDIT-DECISION-MISMATCH` → `validated_edit_decisions` collapses to 0 (`:159-160`).
* Markdown row — `:148-149`: `matches = [r for r in cells if r and r[0] == ident]` must equal exactly
  `[list(expected)]`, i.e. **exactly one** parsed row whose first cell is `DECLARED_EDIT` and whose five cells are
  the literal tuple. A second, conflicting row (even quoted, see §2.3) fails.
* preregister — `:135-136`: `declared != [list(e[:3]) for e in EXPECTED]` → `EDIT-POLICY-SOURCE`. Reordering the
  preregistered tuples is detected (the evaluator's own selftest case `policy-source-swap` reverses the list).
* SOURCES row — `:137-140`: exactly one row with first cell `S086`, 11 cells, source cell ending in the exact
  `EVIDENCE` path, kind/tier `own-work`/`A`, status `mined`, and **no backslash in any cell**.

**Conclusion of the bounded search:** the *value* `ALLOW` and the *text* of the row are unfalsifiable-by-input. The
attack therefore has to target the row's **meaning** — i.e. whether the artifact that the tool certifies actually
asserts and supports "an exact target predeclared for edit **and** for both read and write may be edited". That is
where falsifiers exist, and they are found below. All of them are **one-line mutations of a single declared input
file**, with the other three inputs left byte-identical to the landed state.

---

## 2. Findings by severity

### 2.1 [MEDIUM-HIGH] F1 — The normative procedure that *defines* the row is unconstrained: a one-line prose edit can invert the row's condition and the tool still reports `PASS` / `validated_edit_decisions: 8`

**Where:** `candidate/corpus/knowledge/structured-edit-r23.md`, "## Bounded procedure", step 1:

> `1. Freeze explicit schema-v2 `edit_paths` as canonical literal subsets of both read and write targets. ...`

This sentence is the only operative statement in the corpus of the row's precondition ("predeclared for edit **and
for both read and write**"). The evaluator never constrains it. `evaluate()` touches the prose only through
`table_cells(text)` (the decision table) and one substring test — `:153-154`:
`data.get('scope') != LIMIT or PROSE_LIMIT not in '\n'.join(visible(text))`, where `PROSE_LIMIT` is only
`'It is not native permission enforcement'`. Every other prose sentence is free text.

**Concrete falsifier (smallest literal input).** Keep `structured-edit-r23.json`, `corpus/SOURCES.md` and
`preregister.json` byte-identical to the landed state, and change exactly one line of the Markdown:

```
- 1. Freeze explicit schema-v2 `edit_paths` as canonical literal subsets of both read and write targets. A malformed authority declaration is non-clean before interpreting an event.
+ 1. Freeze explicit schema-v2 `edit_paths` as canonical literal subsets of write targets; a read listing of the same path is optional. A malformed authority declaration is non-clean before interpreting an event.
```

Trace against `evaluate()` (all by reading, no run):

| check | result under the mutation |
|---|---|
| `:123-130` JSON schema / 8 unique ids / row set | unchanged → passes |
| `:146-147` JSON `DECLARED_EDIT` row == `EXPECTED[0]` | unchanged → passes |
| `:148-149` Markdown row for `DECLARED_EDIT` | table untouched → passes |
| `:153-154` `data['scope'] == LIMIT` and `PROSE_LIMIT in visible(text)` | unchanged (limit sentence is in the closing paragraph) → passes |
| `:137-140` SOURCES `S086` row | untouched → passes |
| `:131-132` `evidence_ok(S086)` | untouched → passes |
| `:135-136` preregister `edit_decisions` | untouched → passes |
| **verdict** | `code = 0`, `status: 'PASS'`, `validated_edit_decisions: 8`, `findings: []` |

**Why that violates the row's meaning.** After the mutation the corpus states two incompatible things: the decision
table row says an edit is ALLOWed only when the target is predeclared "for edit **and for both read and write**"
(and the sibling row `WRITE_ONLY_EDIT` says "Edit also needs its explicit target read authority" → DENY), while the
operative procedure now tells an auditor that a write listing alone suffices. An auditor following "Bounded
procedure" — the section the corpus itself calls the bounded procedure — would apply a **different rule** than the
`DECLARED_EDIT` row the checker certifies, and the checker reports the row as validated. The tool's PASS therefore
does not imply that the corpus's operative rule equals the rule the row names.

**Severity note.** This is not a claim that the *landed* corpus is wrong — §0 shows the landed corpus is internally
consistent and matches the preregister. It is a claim about the **gate's discriminating power**: `C1`'s metric
`validated_edit_decisions: 8` is satisfied by a corpus whose procedure contradicts its own table, so the metric does
not measure what its name suggests.

**Bounded search behind this finding.** I enumerated the four declared inputs and every field of each that the
evaluator constrains. The unconstrained surfaces that survive in the *same* corpus file are: (a) all non-table prose
in `structured-edit-r23.md` (except the limit substring); (b) SOURCES cells 0, 4 (scope), 5 (anchor), 6 (teaches),
9 (opened), 10 (used-by) of the `S086` row — only 1, 2, 3, 7 and the no-backslash rule are checked; (c) the evidence
file's top-level `scope` string — `evidence_ok()` reads `schema` and `observations` only, never `scope`; (d) the
`recorded_starts` **contents** of every observation — only "is a non-empty list" is checked, the `tool`/`path`/`line`
values are free; (e) every field of `preregister.json` other than `edit_decisions` (`claims`, `limits`,
`ordinals`, `sources_opened`, …) — never read by this evaluator. Findings 2.2 and 2.4 are the strongest of these.

### 2.2 [MEDIUM] F2 — The cited evidence for the row is a free-text cell: S086's `teaches` and the evidence file's `scope` can be rewritten to contradict the row (or overclaim native enforcement) with no finding raised

`check-edit-contract.py:137-140` validates the `S086` row's **id, source path, kind, tier, status and
backslash-freedom** only. The `teaches` cell — the cell that states what the source actually teaches and therefore
the only textual link between source `S086` and the row's `evidence: S086` — is unconstrained. Likewise
`evidence_ok()` never reads the evidence file's own top-level `scope`
(`structured-edit-observations.json`: *"Observed structured path metadata and recorded adapter steps only, not
universal tool semantics, native permission enforcement, effects, or reading proof."*).

**Concrete falsifier (one line, one file).** In `candidate/corpus/SOURCES.md`, row `S086`, replace the `teaches` cell
with a sentence that contradicts the `DECLARED_EDIT` row, e.g.

> `Structured edit metadata exposes a target path plus opaque body-key forms; permission need not be declared per exact target and any discovered edit target may be edited.`

All checked cells are unchanged (`S086`, the ` — <EVIDENCE>` path, `own-work`, `A`, `mined`, no backslash), so
`:137-140` raises no `EDIT-SOURCE`; the table and JSON rows are untouched; the verdict stays
`PASS / validated_edit_decisions: 8` while the source that the row cites now teaches the opposite of the row.

The symmetric mutation is the evidence file's `scope` string: replacing it with
`"Native runtime enforcement of edit targets is enforced."` leaves `evidence_ok()` true (it checks `schema`,
`observations`, and per-row `tool`/`argument_keys`/`body_fields`/`path`/`recorded_starts`/`transcript_sha256` only),
so `EDIT-EVIDENCE` is not raised. Note that the corpus's own honesty guards (`LIMIT` in the JSON `scope`, and
`PROSE_LIMIT` in the Markdown) still hold — so this specific overclaim cannot be introduced in the *knowledge* file,
only in the *cited source* file, which is precisely the gap.

### 2.3 [LOW-MEDIUM] F3 — A "validated decision table row" need not be a rendered table row: block-quoted or bare pipe-lines are parsed as table rows

`table_cells()` strips leading `>` quote markers (`while line.startswith('>'): line = line[1:].lstrip(' ')`) and
accepts **any** line containing `|`, with no header row and no delimiter row required. `visible()` drops fenced
blocks and 4-space-indented lines, and strips HTML comments, so hidden carriers are excluded — but quoted carriers
are not.

**Concrete falsifier.** Move the `DECLARED_EDIT` line out of the Markdown decision table and put it in the corpus as a
block-quoted line:

```
> | DECLARED_EDIT | ALLOW | Exact target is predeclared for edit and for both read and write | S086 | round23-preregister |
```

Parsed result: `table_cells()` yields `['DECLARED_EDIT','ALLOW','Exact target is predeclared for edit and for both
read and write','S086','round23-preregister']` — i.e. exactly `list(expected)`, and it is still the *only* row whose
first cell is `DECLARED_EDIT`, so `:148-149` passes and `count` reaches 8. But in rendered Markdown a block-quoted
single pipe-line is **not** a table row (a table needs a header row plus a delimiter row); the rendered corpus would
show a seven-row decision table and a stray quoted paragraph. The evaluator's own selftest case `quoted-duplicate`
(checker `:218`) confirms the design intent — a quoted row is *counted* as a row — but it only ever tests a
conflicting quoted row, never the "sole row is quoted" shape.

Consequence: `validated_edit_decisions: 8` does not imply "the rendered Decision table has eight rows". The same
applies to bare pipe-lines with no delimiter row.

### 2.4 [LOW-MEDIUM] F4 — The substance of S086 that the row leans on is not verified, and the observed data exercises the row's precondition in only one of four cases

The row's `evidence` is `S086`. `evidence_ok()` verifies only: schema string, non-empty observations, per-row
`tool == 'edit'`, unique `argument_keys` whose shape-union is exactly `{{path,stream_content},{path,old_string,
new_string}}` (minus `i`), `body_fields` exactly `'omitted; no report text copied'`, `path` starting with the lane
prefix and containing no `/../`, `recorded_starts` being a **non-empty list**, and `transcript_sha256` matching
`[0-9a-f]{64}`. Everything else — the *contents* of `recorded_starts`, the digest *values*, the `seat`, `agent`,
`request_line`, `call_id` — is unvalidated.

Two consequences relevant to `DECLARED_EDIT`:

1. **Recorded native steps can be rewritten freely.** `recorded_starts` may be replaced with e.g.
   `[{"tool":"write","path":"/etc/shadow"}]` and the tool still reports the evidence as valid and the row as
   validated. The corpus sentence "Recorded native steps include report reads/writes under the same parent call ID"
   (and the `S086` `teaches` cell "separate read/write starts") is therefore not enforced anywhere.
2. **The observed data does not exercise the row's precondition.** In `structured-edit-observations.json`, only the
   first observation (`CritRuntime`, `CritRuntime.md`) records a **read and a write** of the exact edited target —
   i.e. exactly one of four observations shows the "declared for both read and write" pattern the `DECLARED_EDIT`
   reason names. The other three (`OraclePathArtifact`, `OraclePathArtifact.md`) record a single `edit` start with no
   read and no write start. So the cited evidence for the ALLOW row exhibits the ALLOW's condition in 1/4 of its
   observations; the corpus' broader phrasing ("include report reads/writes") is true only in that weak sense.
   This is not itself a contradiction — the corpus states that S086 "establish[es] those finite metadata shapes, not
   universal editor semantics" — but it does mean the row's `evidence: S086` cell grounds the *shape* half of the
   decision, never the "predeclared for edit and for both read and write" half.

### 2.5 [NOTE, not a finding] F5 — The row's precondition has no referent anywhere in C1's inputs

`DECLARED_EDIT -> ALLOW` asserts a rule about **authority**: a target is editable only if it is predeclared for edit
**and** read **and** write. `check-edit-contract.py` reads exactly five things — the knowledge JSON, the knowledge
Markdown, `corpus/SOURCES.md`, the S086 observations file, and `preregister.json`. **None of them contains a seat
binding (`read_paths` / `write_paths` / `edit_paths`) or a captured event**, so the row's precondition cannot be
evaluated by this tool under any input. `PASS / validated_edit_decisions: 8` means "these five strings agree in three
carriers", not "the ALLOW rule was exercised".

This is consistent with the tool's own declared `LIMIT` ("Declared audit authority for structured target metadata only;
no native prevention, opaque patch interpretation, effect or reading proof") and with the corpus' closing paragraph
("This is declared post-hoc audit authority only. It is not native permission enforcement…"). The finding is about
**reading the metric**: `validated_edit_decisions` is a string-identity metric and should not be reported as
"eight validated decisions" without the qualifier. Whether the *behavioural* half of the rule is tested anywhere in
this round is out of this seat's declared read scope (`tools/check-seat-bindings.py`, the C2 audit, is not in the
`FxC1DeclaredEdit` read paths and was therefore **not** opened); I make no claim about C2.

---

## 3. What the landed artifact does get right (so the verdict is calibrated)

* The landed `DECLARED_EDIT` row equals the preregistered tuple exactly (§0); no drift, no forgery.
* The JSON row, the Markdown row and the preregister tuple are three independent carriers of the same literal, and
  the evaluator requires all three plus the `S086` source row and the evidence file — a **fail-closed** structure
  for value drift (§1).
* The corpus is honest about its own limits: `LIMIT` in the JSON `scope` and `PROSE_LIMIT` in the Markdown are both
  present, and `:153-154` fails the gate if either is removed or overclaimed (`EDIT-LIMIT-MISSING`). The corpus also
  states that the task API has no restrictive per-seat allowlist and that numeric mode availability is not compliance —
  consistent with the assignment's "no native restrictive task toolset" and with the prohibition on claiming runtime
  enforcement.
* The evaluator's selftest covers value forgery, extra/duplicate rows, hidden and fenced carriers, a quoted
  conflicting row, limit omission, source tier/status/path defects, evidence shape/path/tool defects and preregister
  reordering — a genuinely adversarial fixture set (checker `:195-236`).
* `SOURCES.md` contains exactly one `S086` row, so the `len(found) != 1` uniqueness rule is satisfied by the landed
  state.

---

## 4. Residual risk and verification gaps

1. **No execution.** Per this seat's NO-EXEC scope I did not run `check-edit-contract.py`, `--selftest`, git, or any
   other command. Every verdict above is a static trace of `evaluate()`, `visible()`, `table_cells()` and
   `evidence_ok()`. The falsifiers in §2.1–§2.3 are stated as traces, not as observed runs; they should be
   confirmed by executing the mutated fixtures before anything is amended.
2. **The declared digest was not independently computed** — it is treated as a supplied identity, per the
   assignment's receipt rule. The reviewed file was read, not hashed.
3. **Cross-checker behaviour is unknown to this seat.** `tools/check-seat-bindings.py` (C2) and
   `tools/check-path-reconciliation.py` (C3) are outside this seat's declared read paths and were not opened, so
   whether C2 independently enforces "declared for edit and for both read and write" is unknown and unclaimed.
4. **Unverified sub-claims of S086.** `transcript_sha256` values are format-checked only; no transcript is in C1's
   scope, so the values cannot be confirmed from these inputs. `recorded_starts` line numbers and paths are
   unverified free text.
5. **Adjacent, out-of-my-row observation** (belongs to the `EDIT_TRAVERSAL` seat, flagged only because it lives in
   the same `evidence_ok()`): the path rule rejects only the literal substring `/../`; a path containing `..` at the
   end, `/./`, or a percent-encoded separator would satisfy `evidence_ok()` while the corpus's `EDIT_TRAVERSAL` row
   denies "dot-segment or alternate spelling" expansions. Not re-litigated here.
6. **Prevalence.** The findings in §2.1–§2.3 are properties of the *evaluator*, not of a corrupted landed corpus.
   They mean the C1 gate would not have caught such a corpus; they do not claim the landed corpus contains one
   (§0 and §3 show it does not).

---

## 5. Smallest in-scope remedy

Primary (kills F1 — the only finding that flips a meaning-bearing rule):

* **Document (1 line).** In `candidate/corpus/knowledge/structured-edit-r23.md` "## Bounded procedure", restate each
  row's operative condition in the exact wording of its decision-table row (starting with step 1's
  "canonical literal subsets of both read and write targets" for `DECLARED_EDIT`/`WRITE_ONLY_EDIT`), so the normative
  prose and the table are textually bound.
* **Gate (1 check, ~4 lines).** In `evaluate()`, require that each `EXPECTED` row's `reason` literal also occurs in
  the visible prose **outside** the decision table (i.e. in `visible(text)` lines without `|`, or a count ≥ 2 for the
  reason string across `visible(text)`), and raise `EDIT-DECISION-MISMATCH` otherwise. This makes the §2.1 mutation
  fail while leaving the landed corpus passing.

Secondary one-liners, each independently sufficient for its own finding:

* **F2:** pin the `S086` row's `teaches` cell to a required literal substring set (e.g. it must name the per-exact-target
  declaration that grounds the `DECLARED_EDIT` row) and assert the evidence file's top-level `scope` against a pinned
  literal, so the cited source can neither contradict the row nor overclaim native enforcement.
* **F3:** require the decision table to have a header row plus a delimiter row, and reject any decision row that
  appears only in a block-quoted or non-table context (`table_cells()` should record the carrier kind of each row and
  `evaluate()` should require each `ident` to be carried by exactly one *table* row).
* **F4:** validate `recorded_starts` structurally (each entry's `tool` and `path` must be a string; the set of
  observed start-tools must be reported) and require `structured-edit-observations.json` to contain at least one
  observation whose recorded starts cover both a read and a write of the exact edited target, so the `DECLARED_EDIT`
  row's cited evidence actually exhibits its own precondition.

No remedy here requires new inputs, a seat-binding dependency, or any native/runtime-enforcement claim; all four
stay inside C1's declared scope (decision/prose/source contract only).

---

Reviewed-SHA256: 620f3e5bad34c4ba77a0f0e458bedd79cb05b04a5b1d90200c0baf60038e5081
Predicate: r23f-fxc1declarededit
Scope: executed=none
