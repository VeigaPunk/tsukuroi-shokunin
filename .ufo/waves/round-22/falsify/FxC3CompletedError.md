# FxC3CompletedError — completed outcome with nonempty error

- Seat: TsukuroiR22.FxC3CompletedError-2 (leaf falsifier, C3 calibration)
- Target: `.ufo/waves/round-22/candidate/tools/check-review-cohort.py`
- Reviewed digest (declared): 34b532dda9e69ed81638151572a95f5f665a3f65b8b794d8996e5fb50f4c92e0
- Baseline: 894d1e20fb4939b0cc4fadf722c46d1429f257d2
- Method: source-only reading of the declared paths; NO-EXEC and NO-FETCH observed. No runtime
  observation, no selftest execution, no hash recomputation, no mutation. Every behavioral
  statement below is derived from the source text, not from a run.

## Predicate under attack

A settlement seat declaring `outcome == "completed"` together with a nonempty `error` string must
be rejected as a schema fault, and the checker must not assert any provider causation that the
observed settlement bytes do not support. The falsifier searches for (a) a source-visible input in
which such a seat is accepted or silently accounted, or (b) a path in which the checker attributes
causation to a provider without evidence.

## Observed source facts

1. Settlement rows are validated before any report is read (lines 41-49). The two outcome rules are:

   - line 44-45: `outcome == "failed"` and `error.strip()` empty -> `ValueError("failure without observed error")`
   - line 46-47: `outcome == "completed"` and truthy `error` -> `ValueError("completed outcome with failure error")`

   The type gate at line 42 already requires `error` to be a `str`, so the line 46 test is total
   over JSON strings: every nonempty `str` is truthy, including whitespace-only, NUL and
   zero-width content.

2. Both `ValueError`s are caught by the same handler at lines 75-76, which returns
   `code = 2` and `result = {'cohort_accounting_mode': 1, 'findings': [{'id': 'COHORT-SCHEMA',
   'site': 'input'}], 'scope': SCOPE}`. Line 79 then maps code 2 to `CANNOT_EVALUATE`.

3. The rejection occurs before the per-review loop (lines 53-65), so report presence, report
   bytes, strict receipt findings and the strict exit code cannot change the outcome. The
   strict evaluator has already run at line 36, but its `findings`, `strict_receipt_exit`,
   `strict_conformance`, `total`, per-category counts and `seats` rows are discarded by the
   line 76 result literal.

4. No causation is synthesized anywhere on this path. The exception is caught without binding
   the message, and the emitted finding is `COHORT-SCHEMA` with `site: "input"` — an input-schema
   statement, not a provider statement. The settlement `error` text is echoed only for rows that
   pass validation, verbatim at line 63, as observed data.

## Counterexample search (source-reachable inputs)

| Input shape | Line-visible outcome | False PASS possible |
|---|---|---|
| clean manifest, settlement seat completed + nonempty error, report present | raises line 47 -> code 2, COHORT-SCHEMA, CANNOT_EVALUATE | no |
| same, report absent | raises line 47 before the read loop | no |
| same, but row also duplicates a name/agent or is absent from the manifest | raises line 43 or line 51 -> same code 2, COHORT-SCHEMA | no |
| repeated JSON key or non-object settlement | `unique_object`/shape gate raises -> code 2, COHORT-SCHEMA | no |
| manifest missing (`manifest is None`, lines 23-24) | early return code 1, FAIL, `COHORT-MANIFEST-MISSING`, mode 0; settlement is never parsed | no (still nonzero) |
| `error` supplied as `null`, number, object, or missing | line 42 type gate raises -> code 2, COHORT-SCHEMA | no |
| outcome relabelled `unknown` or `failed` with the same error text | accepted; failure with nonempty error is a supported row shape | not a counterexample: the rule is keyed on the declared outcome label, and no causation is inferred from the error text |

No source-visible input accepts a `completed` row carrying a nonempty `error`. The only path that
does not apply the rule is the `manifest is None` short-circuit, and that path still returns a
failing verdict (`FAIL`, exit 1). The predicate therefore holds as a fail-closed rejection rule.

## Concrete bounded counterexamples to stronger readings

- **Coverage gap (fixture-level).** The selftest has no case for this branch. The case list at
  lines 93-110 covers `clean`, `dead-missing`, `partial-failed`, `missing-unresolved`, receipt
  mismatches, `crlf`, `unicode`, `encoding`, `dropped`, `duplicate`, `unknown`, `false-death`,
  `manifest-missing`, `duplicate-manifest`, `duplicate-json-key`. `false-death` exercises the
  failed-without-error branch (line 45); nothing exercises line 46-47. A source-only mutation
  argument: deleting lines 46-47 leaves every listed case with identical inputs and expected
  values, so the full selftest would still report PASS while a completed+error settlement would
  become acceptable and be categorized by report presence (`delivered_conformant` or
  `absent_unresolved`). Per `.ufo/waves/round-22/candidate/corpus/knowledge/seat-boundary-r22.md`
  ("new checks require fixed negative fixtures before their improvement counts"), this branch's
  protection is unobserved by the fixed negative fixture set.

- **Accounting loss on the rejected input.** The C3 bound says every declared seat is accounted
  while strict receipt findings are preserved. For a completed+error settlement the tool accounts
  zero seats (no `total`, no counts, no `seats`) and drops the already-computed strict receipt
  findings. This is fail-closed, not a false pass, but it means the bound's "preserving strict
  receipt findings" does not hold for this input class.

- **Metric ambiguity.** `cohort_accounting_mode` is set to 1 on the schema-failure path (line 76),
  exactly as on a fully accounted cohort (line 71). A C3 grader keying only on the preregister
  metric `cohort_accounting_mode == 1` cannot distinguish "cohort accounted" from "schema
  rejected". Acceptance must require `status == "CANNOT_EVALUATE"`, `findings ==
  [COHORT-SCHEMA @ input]`, and the absence of `total`/`accounted`, not the mode field alone.

## Provider-causation assessment

Holds, with the scope stated in the code. On the attacked branch the emitted record contains no
provider, no seat name, and no error text; the internal message `completed outcome with failure
error` is not surfaced. For accepted rows the settlement `error` field is copied verbatim, which
preserves observed attribution rather than inventing it. Nothing in the target infers that a
provider failed from a reported outcome or from the presence of error text. The `absent_dead`
label at line 59 is applied only when the declared outcome is `failed`, and the knowledge file's
DEAD row classifies missing final/provider death as UNKNOWN; that label is a cohort bucket name,
not a causal claim about tool activity, so it does not contradict the DEAD decision.

## Expected fixture verdict vs observed runtime

Expected verdict derived from source (no execution):

- Input: valid manifest with one review, clean report bytes, settlement seat `{name: "A",
  agent: "agent-A", outcome: "completed", error: "observed provider failure"}`.
- Exit code 2; `status` `CANNOT_EVALUATE`; `cohort_accounting_mode` 1; `findings` exactly
  `[{"id": "COHORT-SCHEMA", "site": "input"}]`; `scope` present; `total`, `accounted`, the four
  category counts, `strict_receipt_exit`, `strict_receipt_findings` and `seats` all absent
  (`result.get(...)` is `None`, so a fixture asserting `category == 0` or `strict_exit == 2` would
  wrongly fail).
- A conforming fixed negative fixture is `case('completed-error', manifest, settlement_with_error,
  files, 2, fid='COHORT-SCHEMA')`; the row is rejected before any read, so the same verdict holds
  with the report removed.

Observed runtime: none. Execution was prohibited; no case was run, so no runtime observation is
claimed or substituted for the source derivation.

## Remaining unknowns

- The settlement producer semantics are not documented in the declared read set; nothing here
  proves a real producer can or cannot emit `completed` with nonempty `error`. The rejection is
  safe only under the checker's own schema assumption (`completed` implies empty `error`).
- Independent verification of the declared reviewed digest is impossible under NO-EXEC; the review
  covers the bytes read at the target path, identified by the declared digest only.

Reviewed-SHA256: 34b532dda9e69ed81638151572a95f5f665a3f65b8b794d8996e5fb50f4c92e0
Predicate: r22-fxc3completederror
Scope: executed=none
