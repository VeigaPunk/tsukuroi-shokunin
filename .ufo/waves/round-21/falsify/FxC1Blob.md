# FxC1Blob — falsify C1 blob refusal row

Reviewed-SHA256: 1dc94c5f733a9a0112c5db0e94dda5eca31e4f2d982950bc56e08461040d7dd7
Predicate: C1-blob refusal

Candidate revision 0a14952b59d20179e1c813af58befaecd6992a17. Primary file: `.ufo/waves/round-21/candidate/corpus/knowledge/selector-contract-r21.json`. Its digest is the one declared in `candidate-files.json`. I did not recompute it because this seat is NO-EXEC.

Auxiliary snapshot dependencies, read only, with digests as declared in `candidate-files.json` (not recomputed):
- `candidate/tools/check-selector-contract.py`: 239758b49da4f24415f53adb52cc6833818d0e340f0832d0389416bce50aea50
- `candidate/corpus/knowledge/selector-contract-r21.md`: b4966a9bcf4ac124a964718b0ed76104e2f07c41b63050dc8bda618ea5136353
- `candidate/corpus/SOURCES.md`: ef697b7c6b60bf0e5b71e1267f30cda678d5de01abc803b24dcc7dce1b93c3e4

Advisory only (not production and not a candidate verdict input): `build/ExecDecision.md`, `drafts/ExecDecision/check-selector-contract.py`, `drafts/ExecDecision/selector-contract-r21.json`, and `preregister.json` (C1 classes).

Axes: depth (validity of C1 decision_rows), calibration (whether the controls can actually fail), and scope/safety. Operability and C2 are not touched.

## Verdict

At the frozen bytes, the predicate holds for the ordinary single-key mutants. This is a source prediction, not an observation. A wrong blob outcome or a wrong blob finding should fail. The expected map is a literal in the checker and does not depend on the JSON.

I found three fixable defects in the checker and its controls. None of them changes the result for the current frozen bytes:
- Duplicate JSON keys can shadow the blob row's values.
- The prose check ignores table columns.
- The selftest has no blob mutant and no finding mutant of any kind.

Together these mean the claim that the blob refusal is "able to fail" is predicted but has no witness.

## Observations (bytes read)

- The JSON at line 7 is `{"class": "blob", "outcome": "refuse", "finding": "E-REVISION-INVALID", "source": "S081", "rationale": "A file-content object is not commit-ish."}`. Each key appears once. No key is duplicated anywhere in lines 1–11. `sources` is `["S081", "S082"]`.
- Checker lines 17–23: `EXPECTED["blob"] = ("refuse", "E-REVISION-INVALID")` is a hardcoded literal. It is not derived from the JSON.
- Checker lines 70–82: for each row, the gate compares `(row.get("outcome"), row.get("finding"))` with the `EXPECTED` tuple. It also requires the source to be S081 or S082, a non-blank rationale, and exactly one prose line starting with `| blob |` that contains the outcome and finding strings as substrings.
- Checker line 41: it uses plain `json.loads(raw)`, with no `object_pairs_hook`.
- Checker lines 100–133: the selftest `sample` and `prose` are generated from `EXPECTED` itself. The mutation cases are:
  - `missing-row`, which pops the last row (tag-to-noncommit)
  - `duplicate`, which duplicates row 0
  - `tree-accept`, which changes the outcome at index 1
  - `tag-refuse`, which changes the outcome at index 3
  - `wrong-source`, which changes the source at index 0
  - `prose-outcome`, which edits the tree row only

  No case touches the blob row (index 2). No case changes any `finding` value.
- Markdown line 21: `| blob | Existing file-content object is not commit-ish | refuse | E-REVISION-INVALID | S081, S082 |`. This is the only line that starts with `| blob |`.
- SOURCES lines 88–89: the S081 and S082 rows split into 13 cells. `cells[2]` contains the pinned URL, `cells[4]` is `A`, and `cells[8]` is `mined`. Neither row contains an embedded `|`.
- Advisory: the ExecDecision draft's `evaluate` (lines 231–236) parsed with `object_pairs_hook=_unique_object`, which rejects duplicate keys, and with `parse_constant` rejection. It also required closed key sets for each row. The candidate dropped all of these.

## Source predictions (not executed)

These blob mutants should fail with exit 1, finding `SELECTOR-CONTRACT-MISMATCH` with detail `blob`, and `decision_rows` 4:
- `outcome` set to `accept-if-landed-and-pushed`, with any finding
- `finding` set to `null`, `E-REVISION-NOT-LANDED`, `E-REVISION-NOT-PUSHED`, `"E-REVISION-INVALID "`, or with the key absent
- `outcome` set to `Refuse` or `["refuse"]`
- `source` set to `S999`

Removing or renaming the blob row (for example to `Blob`), or duplicating it, should fail at the class-set check (exit 1, `decision_rows` 0).

## Counterexamples

1. **Duplicate-key shadowing. This passes and should not.** Prediction: the row `{"class": "blob", "outcome": "accept-if-landed-and-pushed", "finding": null, "outcome": "refuse", "finding": "E-REVISION-INVALID", "source": "S081", "rationale": "x"}` passes. Python's `json.loads` keeps the last value, while a human reader or a first-wins parser sees acceptance. The same applies to a shadowed `"class"`, or to a shadowed top-level `"decisions"` array. This creates two authorities for one decision inside one file. It is a regression from the ExecDecision draft, which classified it as SCHEMA (exit 2). Impacted axes: depth and calibration. It is fixable. The frozen bytes are not affected, as observed above.
2. **The prose check ignores columns. This passes and should not.** Prediction: the prose row `| blob | would refuse under typed peeling with E-REVISION-INVALID | accept-if-landed-and-pushed | E-REVISION-NOT-LANDED | S081 |` satisfies `outcome in line and finding in line`, so the prose would back a wrong blob decision. The selftest prose uses 3 columns while the real file uses 5, which confirms the check never looks at columns. Impacted axis: depth (prose/data agreement). It is fixable.
3. **The selftest cannot detect a broken blob or finding check.** Prediction: each of these checker mutants still passes all 12 selftest cases:
   - comparing only `outcome` (dropping `finding` from the tuple and from the prose check)
   - adding `if name == "blob": valid += 1; continue`
   - changing `EXPECTED["blob"]` together with the generated sample

   Because the frozen JSON is correct, the `--revision` run of the first two mutants would also report PASS. So nothing at present witnesses that a wrong blob finding can fail. This conflicts with the prose requirement (md line 39) that controls "show the corresponding fixes able to fail". Impacted axis: calibration. It is fixable.
4. **Unchecked rationale (a tradeoff, not a defect).** The blob rationale "A blob is commit-ish" would pass, because only non-blank text is checked. The gate is declared finite at the tuple level, so this is a disclosed limit.

## Smallest safe correction

- Parse with `object_pairs_hook` set to reject duplicate keys, and route that to `SELECTOR-CONTRACT-SCHEMA` (exit 2). Add a raw-string selftest case with a duplicated `outcome` in the blob row.
- Make the prose check column-aware: split the line into cells and require the outcome cell to equal `refuse` and the finding cell to equal `E-REVISION-INVALID` for blob.
- Add selftest mutants that modify the blob row at index 2:
  - outcome set to accept
  - finding set to `E-REVISION-NOT-LANDED`
  - finding set to `null`
  - prose blob finding removed
- Build the selftest fixture from a literal table that is independent of `EXPECTED`, so that drift in `EXPECTED["blob"]` is caught.

## Limits

- No test, mutant, selftest, or `--revision` run was executed. Every pass/fail statement above is a prediction from reading source.
- I did not recompute the SHA-256 digests.
- I did not fetch S081 or S082. I assume their quoted propositions from the corpus prose.
- This is a review by an author-side seat and does not provide outside or non-author closure.
- No tool was installed or updated.

Scope: executed=none
