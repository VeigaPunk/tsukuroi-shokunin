# FxC1LocalRead - LOCAL_READ source swap S084 -> S083 (round 22, C1 depth)

Reviewed-SHA256: 1b91a7c10c971b554bad144035b40d0b7054e06582093f9f851ac0fcafdd2485
Predicate: r22-fxc1localread
Scope: executed=none

## Question

Attack the named candidate bytes for C1: change the `LOCAL_READ` decision's source label
from `S084` to `S083` and determine, from source alone, whether the fixed source tuple must
reject. Expected fixture verdict is stated separately from observed runtime; nothing was
executed, so "observed runtime" is uniformly none.

## Evidence read (observed static bytes)

- `.ufo/waves/round-22/candidate/tools/check-boundary-contract.py` (175 lines; declarations
  plus verbatim `evaluate` at lines 58-99, `selftest` at 103-140, `git_read`/`main` at 142-175).
- `.ufo/waves/round-22/candidate/corpus/knowledge/seat-boundary-r22.json`
  (`LOCAL_READ` at line 19, `"source": "S084"` at line 23).
- `.ufo/waves/round-22/candidate/corpus/knowledge/seat-boundary-r22.md`
  (table row `LOCAL_READ ... S084` at line 15; narrative `S084` mentions at lines 1, 7, 35).
- `.ufo/waves/round-22/sources/host-tool-boundary.json` (`native_per_seat_allowlist: false`,
  exact `tools_semantics` string, `approved_scope` prompt-level plus post-hoc audit).
- `.ufo/waves/round-22/preregister.json` (C1 metric `validated_boundary_decisions`,
  before 0, target 6; limits disclaim native enforcement).
- `candidate/tools/_revision.py` (binding helper; `--revision` resolves a landed commit).

Declared digest is the assignment's review anchor. It was not recomputed in this seat
(NO-EXEC); no claim is made that the bytes hash to it beyond that binding.

## Enforcing sites

- Line 18-24: module-level literal `EXPECTED`; line 21 pins
  `('LOCAL_READ', ..., 'ALLOW', 'Only literal bound source paths and approved skill URI', 'S084')`
  - a constant not derived from `DATA`, `PROSE`, or the sources table.
- Line 83: `by_id = {r['id']: r for r in rows}`.
- Line 87: `correct = row is not None and tuple(row.get(k) for k in
  ('id','surface','decision','reason','source')) == expected`.
- Line 88: prose cells for the id must equal `[list(expected)]` exactly.
- Line 89: one `BOUNDARY-DECISION-MISMATCH` add per decision id when either check fails.
- Line 92: `count += 1` only in the passing branch.
- Line 95: `code = 1 if findings else 0`; no branch clears `findings`.
- Lines 96-99: `ValueError/TypeError/KeyError/UnicodeError/AttributeError` map to
  `BOUNDARY-SCHEMA` with code 2 (non-zero).
- Lines 27-34 (`unique`): duplicate JSON keys raise `ValueError` before any decision is read.
- Lines 142-152 (`git_read`): the document is read from the committed object
  `rev:path`, not the worktree, so the mutant only reaches `evaluate` as a committed revision.

## Expected fixture verdicts (derived statically, not observed)

| Variant | Mutated bytes | Expected exit | Expected status | Expected findings |
|---|---|---|---|---|
| V1 | JSON line 23 `S084`->`S083` only | 1 | FAIL | `BOUNDARY-DECISION-MISMATCH` / `LOCAL_READ`; validated 5/6 |
| V2 | Prose table line 15 `S084`->`S083` only | 1 | FAIL | same single finding via line 88 |
| V3 | V1 and V2 together (consistent label swap) | 1 | FAIL | same single finding; line 21 still pins `S084` |
| V4 | duplicate `"source"` key inside the LOCAL_READ object (`S084` then `S083`) | 2 | CANNOT_EVALUATE | `BOUNDARY-SCHEMA` (`unique` rejects) |
| V5 | corpus/SOURCES.md `S084` row relabelled `S083` | 1 | FAIL | `BOUNDARY-SOURCE` for `S084` (absent) and `S083` (duplicated); decisions still 6/6 |
| V6 | narrative `S084` at prose lines 1, 7, or 35 only | 0 | PASS | none - not machine-pinned |

V1-V5 reject. V6 is a positive counterexample only to the stronger reading "every S084
occurrence in the prose", not to the decision's `source` field.

## Why the decision-field mutation cannot pass (bounded)

Exit 0 requires `findings` empty. That requires `correct` true for all six `EXPECTED`
entries. For `LOCAL_READ`, `correct` compares `row.get('source')` against the literal
`'S084'` embedded in line 21. JSON can only produce primitives/lists/dicts, none of which
compare equal to `'S084'` unless the value is that string; duplicate-key smuggling is
rejected by `unique` first; a malformed row raises into the code-2 handler. There is no
code path that removes an already-appended finding. Therefore no mutation of the contract
JSON or prose table, at either site or both, can produce exit 0 with `LOCAL_READ` sourced to
`S083`, while `EXPECTED` remains the reviewed literal. Exit 1 (not 2) is expected for V1-V3
because the six-row schema remains valid and only the tuple/cell comparison fails.

The C1 metric consequence is consistent: the mutant's `validated_boundary_decisions` is 5,
below the preregistered target 6, so the round-22 depth claim also fails on these bytes.

## Observed runtime

None. `executed=none` covers the checker, its selftest, the mutant fixtures, git, and any
digest computation. No exit code, stdout, SHA-256, or file mutation was observed; V1-V6 are
static derivations from the read bytes.

## Gaps and residual unknowns

1. `EXPECTED` (line 18-24) is the sole authority and has no independent oracle inside the
   candidate. A mutant that also rewrites line 21 to `S083` would pass both JSON and prose,
   and `selftest` would not notice because its clean fixture is generated from `EXPECTED`
   (lines 104-105). That evasion changes the reviewed SHA-256, so it is caught by review
   pinning, not by the checker's logic. The verdict above is conditional on line 21 being
   byte-identical to the reviewed digest.
2. Existing negative fixtures cover `source` mutation only for `decisions[0]` (NO_EXEC,
   lines 113-116) and `decision` mutation for all six (lines 110-112). No fixture names the
   `LOCAL_READ` S084->S083 swap; the reject generalizes from lines 84-89, not from a
   dedicated fixture.
3. Prose narrative `S084` at lines 1, 7, 35 is unparsed by `evaluate` (only table lines
   starting with `|` and the exact limit phrase are read), so attribution edits there pass.
4. Detection is label equality plus the source-table row shape (path substring, `own-work`,
   `A`, column 7 `mined`). It does not prove that `host-tool-boundary.json` actually
   supports the `LOCAL_READ` reason, nor that any seat obeyed the decision; this matches the
   declared scope limit and the preregister's no-native-enforcement disclaimer.
5. `evaluate` consumes `git show rev:path`; an uncommitted worktree edit to the corpus is
   invisible to `--revision`, so the mutant's reachability depends on it being committed.
6. A first cold read of a partially elided view was resolved by verbatim rereads of
   `evaluate` (54-95) and the selftest cases (104-145); no code region used above is inferred
   from elision.

## Verdict

The named mutation changes `LOCAL_READ`'s fixed source tuple match and must be rejected:
expected FAIL, exit 1, single `BOUNDARY-DECISION-MISMATCH` finding at `LOCAL_READ` with
`validated_boundary_decisions` 5 of 6. Confidence high for the decision-field variants
(V1-V5, direct literal comparison); the bounded exception is an edit to `EXPECTED` itself
or narrative-only prose mentions (V6), both outside the checked contract. No runtime claim.

Report: .ufo/waves/round-22/falsify/FxC1LocalRead.md
