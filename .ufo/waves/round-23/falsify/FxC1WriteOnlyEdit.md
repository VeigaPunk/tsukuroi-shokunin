# FxC1WriteOnlyEdit — attack C1 row WRITE_ONLY_EDIT → DENY

Seat: `TsukuroiR23-2.FxC1WriteOnlyEdit-2`. Mode: falsify, NO-EXEC/NO-FETCH. All statements below are
static reads of declared files; nothing was executed, hashed, listed or imported.

Target: `.ufo/waves/round-23/candidate/tools/check-edit-contract.py` (supplied digest
`620f3e5b…8e5081`, treated as the declared identity, not recomputed).

## 1. Attacked claim

C1 (`axis: depth`, metric `validated_edit_decisions`, before 0 → target 8), restricted to the
`WRITE_ONLY_EDIT` row and to the carrier fields the checker validates for it: decision JSON,
prose Markdown, `corpus/SOURCES.md` S086 row, preregistered tuple. Not a frontier claim. No
runtime-enforcement claim is attacked; the tool, `LIMIT` and prose all already say "declared
audit authority … not native permission enforcement", and this seat does not contradict that.

**Verdict.** The decision triple itself is not falsifiable by any literal input: it is pinned
three ways with exact equality (tool constant, preregister, JSON row + prose row). The claim
that the validated prose/source *carries* that decision is falsifiable: a two-line Markdown
delta and, separately, a one-cell `SOURCES.md` delta both pass `evaluate()` with
`status: PASS`, no findings, `validated_edit_decisions: 8`, while the rendered decision table
reads `WRITE_ONLY_EDIT | ALLOW`. Confidence: high for F1/F2 (direct trace of the predicates
quoted below); the tuple-pinning negative result is also high but bounded to the read inputs.

## 2. Landed row vs preregistered tuple (observed)

Checker constant (`check-edit-contract.py:20-29`, row at `:24`):

    ('WRITE_ONLY_EDIT', 'DENY', 'Edit also needs its explicit target read authority', 'S086', POLICY)
    POLICY = 'round23-preregister'   (line 19)

Landed `candidate/corpus/knowledge/structured-edit-r23.json`, decision 4:
`id=WRITE_ONLY_EDIT`, `decision=DENY`, `reason=Edit also needs its explicit target read authority`,
`evidence=S086`, `policy=round23-preregister`, and the object's key set is exactly
`{id, decision, reason, evidence, policy}`. Landed
`candidate/corpus/knowledge/structured-edit-r23.md` has the identical five cells in the
`| ID | Decision | Reason | Evidence | Policy |` table. `preregister.json.edit_decisions[3]` is
`["WRITE_ONLY_EDIT","DENY","Edit also needs its explicit target read authority"]` — the exact
first three fields, in the same order, with no `evidence`/`policy` fields preregistered.

So: **landed row == preregistered tuple (3/3), plus two non-preregistered fields.** No
divergence. `SOURCES.md` S086 has 11 cells, `own-work`, tier `A`, status `mined`, and its
source cell ends with ` — .ufo/waves/round-23/sources/structured-edit-observations.json` after
the last ` — `; it passes the source predicate. `_revision.bind(ROOT, …)` + the five
`git_read(binding.sha, …)` calls (`:271-272`) mean `evaluate` receives all five artifacts from
the same audited revision.

## 3. Bounded search — why the decision cannot be flipped literally

1. **JSON row.** `set(row) == {'id','decision','reason','evidence','policy'}` plus tuple
   equality against the constant (`:146-147`). Extra key, wrong value, missing key, duplicate
   id (schema, code 2) or duplicate JSON key (`unique()`) all fail. No accepted input carries a
   different `decision` value for this id.
2. **Prose exact row.** `matches = [r for r in cells if r and r[0] == ident]` and
   `matches != [list(expected)]` (`:148-150`). A row whose raw first cell differs — even by
   one space after `strip()` — is not this row; zero or two exact rows both fail, and *any*
   non-mismatch finding forces `count = 0` (`:159-160`). Fenced, 4-space-indented and
   HTML-comment-hidden prose is dropped by `visible()` (`:45-74`) before `table_cells()`
   (`:77-93`), which the selftest's `hidden`/`fenced` cases already pin as mismatch. Hiding the
   exact row is therefore caught.
3. **Preregister.** `declared != [list(e[:3]) for e in EXPECTED]` (`:134-136`) is exact list
   equality, so a preregister that disagrees is rejected.
4. **Evidence file.** `evidence_ok` proves only: two observed `argument_keys` shapes
   (`{path,stream_content}`, `{path,old_string,new_string}` modulo `i`), `tool == 'edit'`,
   lane-prefixed path with no `/../`, non-empty `recorded_starts`, 64-hex transcript digest,
   `body_fields` exact. It does **not** require any observation to be a write-only target.

Therefore the only remaining attack surface is the carrier predicates — and they are not
universal.

## 4. Falsifier F1 — two-line Markdown delta, PASS with a rendered ALLOW row

**Input (smallest delta to the landed `.md`; JSON, SOURCES, preregister and evidence unchanged):**

Replace the table line

    | WRITE_ONLY_EDIT | DENY | Edit also needs its explicit target read authority | S086 | round23-preregister |

with

    | **WRITE_ONLY_EDIT** | ALLOW | Edit is implied by write authority | S086 | round23-preregister |

and add, as its own paragraph after a blank line (e.g. in "Bounded procedure"):

    | WRITE_ONLY_EDIT | DENY | Edit also needs its explicit target read authority | S086 | round23-preregister |

**Why `evaluate()` still returns code 0 / `PASS` / `validated_edit_decisions: 8`** (trace, not a run):

- `visible()` keeps both lines (no fence, no 4-space indent, no comment) — the paragraph line is
  a plain line in the body.
- `table_cells()` has no header or delimiter-row requirement and no notion of table membership:
  any line containing `|` becomes a row (`:77-93`). The bold row yields first cell
  `**WRITE_ONLY_EDIT**`; the paragraph row yields exactly `WRITE_ONLY_EDIT`.
- `matches` for `WRITE_ONLY_EDIT` is therefore `[[...expected five cells...]]` (the paragraph),
  so `matches == [list(expected)]` holds; `by_id`/tuple equality holds from unchanged JSON; the
  other seven rows are untouched; `LIMIT`/`PROSE_LIMIT`, S086 and `evidence_ok` are untouched.
- No finding is emitted, so the `any(...) → count = 0` guard (`:159-160`) never fires.

**Why the row's meaning is violated.** In any CommonMark/GFM renderer the bold row is a real
body row of the `ID | Decision | …` table and displays `WRITE_ONLY_EDIT | ALLOW`; the exact
DENY line is a paragraph, not a table row (pipe text with no preceding header+delimiter pair is
not tabulated). The audited artifact now both (a) renders the opposite decision for the same
logical id and (b) passes the audit that is supposed to certify the prose records the decision.
The JSON still says DENY, so this is a carrier/audit-fidelity falsifier, not a JSON flip — which
is exactly the gap: the checker reports 8/8 without any check that the validated row is the one
the reader sees. Equivalent decorated carriers the same predicate misses: `` `WRITE_ONLY_EDIT` ``,
`<b>WRITE_ONLY_EDIT</b>`, `[WRITE_ONLY_EDIT](#x)`; equivalent non-rendered carriers for the exact
row: a `>` blockquote line (`table_cells` strips `>`), a paragraph line, or a line inside a
`<div hidden>` HTML block (HTML is opaque to `visible()`/`table_cells()`).

## 5. Falsifier F2 — one-cell `SOURCES.md` delta, evidence row contradicts the decision

The S086 predicate (`:137-140`) validates only: exactly one `S086` row, 11 cells, the substring
after the last ` — ` in cell 1 equals the evidence path, `cells[2:4] == ['own-work','A']`,
`cells[7] == 'mined'`, and no backslash anywhere. Cells 4 (`scope`), 5 (`anchor`), 6
(`teaches`), 8 (`opened`), 9 (`recheck`), 10 (`used-by`) and the title prefix of cell 1 are
unconstrained. So this passes:

    | S086 | Write-only edit targets are allowed without read authority — .ufo/waves/round-23/sources/structured-edit-observations.json | own-work | A | … | … | … | mined | 2026-10-21 | on-release | … |

and so does rewriting `teaches` to assert that edit authority is implied by write authority.
The row's `evidence: S086` then cites a registry row whose visible text denies the row's
decision, while the checker still reports the row validated. This is the evidence-side form of
the same non-universal predicate, and it is the smallest possible delta (one cell).

Separately (warrant gap, not a contradiction): the four S086 observations contain **no
write-only instance**. Observation 1 (`CritRuntime`) records a `read` start at line 12 followed
by a `write` start at line 13 on the same path; observations 2–4 (`OraclePathArtifact`) record
only `edit` starts. No observation has write authority without read authority, and
`evidence_ok` does not require one. The row's DENY is a lane-policy declaration, which the
document says explicitly ("Authority is separately declared lane policy") and the checker
docstring concedes ("S086 proves only observed metadata shapes and adapter steps; lane policy is
separate"). The `evidence` column is thus a metadata-source tag, not a warrant; a reader who
takes the column at face value over-reads S086. Remedy below is to make that distinction
machine-checked rather than prose-only.

## 6. F3 — the "preregistered" tuple is read from the audited revision

`main()` passes `git_read(binding.sha, PREREGISTER)` for the preregister (`:271-272`), i.e. the
copy in the revision under audit, and `evaluate` never checks `pre['baseline']` or any digest of
the preregister. A landing that edits `preregister.edit_decisions` together with the JSON row,
the prose row and the tool's `EXPECTED` compares the edited copy to itself and still passes. The
current preregister text does match the tool constant and the landed row, so the *landed state*
is consistent; the *binding* is not pre-committed. (The preregister postdates the named baseline
`ae01e50…`, since it carries that hash in its `baseline` field, so `git show ae01e50:preregister.json`
is not the fix; a pinned preregister commit or supplied digest is.)

## 7. F4 — `EXPECTED` is in the audited tree; `policy` is an unbound label

`ROOT = Path(__file__).resolve().parents[1]` and the C1 command is
`python3 tools/check-edit-contract.py --revision <REV>`, so the tool resolving `tools/` is the
in-tree copy; `EXPECTED`, `LIMIT` and `PROSE_LIMIT` come from that file, while the five data
artifacts come from `binding.sha`. Nothing in `evaluate()` or `main()` compares the running tool
against `git show <rev>:tools/check-edit-contract.py`, so the constants are not pinned to the
revision whose data they judge. Likewise `policy: round23-preregister` is a literal repeated in
all eight rows; the preregister has no policy object with that name, so the field names an
artifact, not a checked authority. Both are auditability boundaries, not evidence that the
landed bytes are wrong.

## 8. Smallest in-scope remedies (no round24, no new claim)

1. **Universal id-mention rule (kills F1).** Over `visible(prose)`, require for every `EXPECTED`
   id that exactly one line contains the id as a case-sensitive substring, and that this line's
   `table_cells` row equals the expected five cells. This makes decoration, paragraph carriers
   and blockquote carriers mismatches without changing any currently landed byte.
2. **Real-table requirement.** Require the eight rows to be the body of one table whose header
   row cells are exactly `['ID','Decision','Reason','Evidence','Policy']` and whose next line is
   a delimiter row of `---`-style cells; reject any stray `S0xx`/id row outside it.
3. **Bind the evidence column (kills F2).** Either pin S086's `scope`/`teaches` (and the cell-1
   title prefix) to literals in the tool, or rename the JSON field to `metadata_source` and add
   a `policy` authority object so the row no longer asserts that S086 warrants the decision; add
   one write-only observation (or state in-check that no write-only instance exists) before
   counting the row as source-grounded.
4. **Pin the preregister/tool (kills F3/F4).** Require `pre['baseline']` to equal a tool literal
   and add a supplied preregister digest (or `--preregister-rev`); record the tool's own digest
   in the gate output so the constants cannot silently drift with the data they judge.

## 9. Observed / inference / unresolved

- Observed: all quotations above; landed rows match the preregistered triple; S086 observations
  contain no write-only target; `evaluate`, `visible`, `table_cells`, `evidence_ok` predicates;
  `main()` reads all five artifacts at `binding.sha`.
- Inference: renderer behaviour (bold row displays as an ordinary table row; headerless pipe text
  is a paragraph) is standard CommonMark/GFM, not executed here; the two deltas would return code
  0 by the quoted predicates.
- Unresolved: `tools/_revision.py` is outside this seat's declared read paths, so revision
  binding/fixity mechanics are unverified; whether the integration gate runs the in-tree tool or
  the `candidate/` copy is not observable here (F4 applies only to the in-tree run path);
  runtime output of the checker (NO-EXEC), including the selftest, was not observed.

Reviewed-SHA256: 620f3e5bad34c4ba77a0f0e458bedd79cb05b04a5b1d90200c0baf60038e5081
Predicate: r23f-fxc1writeonlyedit
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
