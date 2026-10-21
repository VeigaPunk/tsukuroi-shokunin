# Falsify — C1 tag-to-noncommit refusal row (FxC1NoncommitTag)

Target: candidate revision 0a14952b59d20179e1c813af58befaecd6992a17, primary file `.ufo/waves/round-21/candidate/corpus/knowledge/selector-contract-r21.json` (row `tag-to-noncommit`, JSON line 9).

Axes: depth (C1 decision-row count), source provenance, calibration/fail-capability of the C1 gate, operability (C2 matrix, auxiliary only), scope/safety.

## Verdict

The decision itself survives: by source reading, `(refuse, E-REVISION-INVALID)` for an annotated tag whose recursive peel ends at a tree or blob matches the frozen binder, and I found no counterexample that would make the binder accept such a tag. Three fixable defects remain around the row. Its provenance claims more than the cited source text supports. The C1 gate's prose binding can be satisfied by prose that contradicts the row. The nested noncommit-tag subcase is implied by the row but has no control at any layer. None of these is a tradeoff that requires rejection, provided the row is not counted as a source-grounded refusal finding until the provenance is corrected.

## Auxiliary snapshot dependencies (frozen bytes, from `candidate-files.json`)

- `tools/check-selector-contract.py` sha256 239758b49da4f24415f53adb52cc6833818d0e340f0832d0389416bce50aea50 (the new C1 checker)
- `corpus/knowledge/selector-contract-r21.md` sha256 b4966a9bcf4ac124a964718b0ed76104e2f07c41b63050dc8bda618ea5136353 (the prose)
- `tools/_revision.py` sha256 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf (the behavior authority)
- `tools/check-revision-binding.py` sha256 0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6 (the C2 judge, auxiliary)
- `corpus/SOURCES.md` sha256 ef697b7c6b60bf0e5b71e1267f30cda678d5de01abc803b24dcc7dce1b93c3e4; `corpus/lessons/round-21.md` sha256 ab841b2562e41fa69f90b63b8444d5ab47670ce2acf0ec1208f71cf7980349c9
- Not in the candidate inventory, so these were read as unpinned wave files: `.ufo/waves/round-21/sources/git-types.txt` (the retained source excerpt), `.ufo/waves/round-21/preregister.json` (lines 1–30), and the build draft `.ufo/waves/round-21/build/ExecDecision.md` plus `drafts/ExecDecision/*` (advisory only, not production).

## Observations (from reading the source; nothing was executed)

1. **Binder path.** `_revision.py` `_object_commit` (lines 112–146) handles an object whose `cat-file -t` is `tag` by running `rev-parse --verify --quiet <oid>^{commit}`. If that fails and `rev-parse --git-dir` succeeds, it returns `None`. `bind` (lines 177–179) then raises `E-REVISION-INVALID`. The binder selftest has `annotated-tag-to-blob-invalid` and `annotated-tag-to-tree-invalid` (lines 413–419), each covering one level only.
2. **Retained source text.** `sources/git-types.txt` contains exactly three propositions:
   - S081, positive conditional: "if <rev> is a commit-ish, <rev>^{commit} describes the corresponding commit object."
   - S081, empty-brace form: "dereference the tag recursively until a non-tag object is found."
   - S082: "you can add the `^{type}` peeling operator".
   No retained sentence says that `^{commit}` fails, errors, or refuses on a non-commit-ish target. Grep for `barf` in the excerpt returned no match.
3. **JSON row.** Line 9 has `"source": "S081"` and the rationale "Empty-brace peeling can stop at a tree or blob; commit-type peeling cannot accept those targets." The first clause paraphrases the `^{}` sentence. The second clause, which carries the refusal, is not quoted from any source. `E-REVISION-INVALID` is a lane identifier defined in `_revision.py` line 44, not a Git identifier.
4. **Checker prose binding.** `check-selector-contract.py` lines 73–76 accept the prose row when exactly one line starts with `| tag-to-noncommit |` and contains the substrings `refuse` and `E-REVISION-INVALID` anywhere on the line. Column positions, the "Git distinction" cell, and the rationale content are not compared. Rationale only has to be a non-blank string (line 79). `source` may be either S081 or S082 (line 78).
5. **Checker selftest.** The mutations cover tree→accept (index 1), tag-to-commit→refuse (index 3), and wrong source on commit (index 0). No case names `tag-to-noncommit`. The `prose-outcome` case (line 122) replaces `| tree | refuse`, which appears only in the in-memory three-column fixture. The real prose row places a distinction cell between the class and the outcome (prose line 20), so that case does not model real prose.
6. **C2 matrix (auxiliary).** `target_type_probes` (check-revision-binding.py lines 676–736) builds `tag_to_blob` and `tag_to_tree` as single annotated tags pointing directly at the blob or tree. It requires exit code CANNOT, `binding_ids == [E-REVISION-INVALID]`, and `finding_count == 1` (lines 721–725), so the finding ID is graded, not just the exit class. No nested tag-to-tag-to-tree or tag-to-tag-to-blob case exists.
7. **Advisory draft comparison.** The build draft's `tag-to-noncommit` row (draft JSON lines 52–59) attributed the refusal to "lane policy", scoped it to "Annotated tag object IDs", and its checker required an exact proposition match (draft checker lines 211–291). The candidate removed the lane-policy attribution and the word "annotated" from this row, and weakened the prose binding to substring matching. This is advisory evidence only.

## Counterexamples

**CX1: false or over-broad provenance (axis: source provenance).** The row credits S081 for `refuse` and `E-REVISION-INVALID`. The retained S081 text supports only the positive direction (commit-ish to commit object) and the fact that `^{}` can stop at a non-tag object. The refusal direction is the converse of a conditional, which the excerpt does not state. The finding ID is lane-owned (`_revision.py` contract step 3). Prose line 13 assigns object-prefix, ancestry and push restrictions to the lane, but not this refusal outcome or finding. [INFERENCE, not observed in the retained excerpt: the full gitrevisions `<rev>^{<type>}` paragraph probably contains a failure clause, "(in which case, barf)", which would ground the Git half.]

**CX2: prose contradiction passes C1 (axis: calibration).** Prediction from lines 73–80, not executed: replace prose line 23 with `| tag-to-noncommit | Tag peels to tree or blob | accept-if-landed-and-pushed | never refuse; E-REVISION-INVALID not emitted | S082 |`. The line still starts with `| tag-to-noncommit |` and contains `refuse` and `E-REVISION-INVALID`, so `supported` is True. With the JSON unchanged, the checker reports this row valid and `decision_rows` stays 5 while the prose now says accept. The same substring weakness affects the tree and blob rows.

**CX3: nested noncommit tag has no control at any layer (axes: depth, calibration, operability).** The prose distinction "Tag peels to tree or blob" and the S081 "recursively" wording cover tag-to-tag-to-tree. Consider this mutant, a prediction that was not built or run:
- If the object is a tag whose immediate target (`cat-file -p`, `object` header) has type tree or blob, emit `E-REVISION-INVALID`.
- Otherwise peel with `^{}`.

This mutant passes all five C2 classes. `tag_to_blob` and `tag_to_tree` are single-level and refused correctly. Nested and ordinary commit tags peel to the commit. A direct tree is not a tag. It also passes the binder's single-level selftest pattern. On tag-to-tag-to-tree, however, `^{}` yields the tree, and `merge-base --is-ancestor <tree> refs/heads/<branch>` follows. [INFERENCE: Git exits ≥2 here, giving `E-GIT-FAILED`.] Either way the finding is not `E-REVISION-INVALID`, which violates the C1 row while every control stays green. The candidate's own generic-peel witness (lines 981–989, 1239–1259) is killed by single-level controls, so this survival is specific to an immediate-target check.

**CX4: tag scope wording (axis: scope, minor).** Prose line 23 and JSON line 9 say "Tag" without "annotated". A lightweight tag is a ref, not an object. Its name is refused as a ghost ref (`E-REVISION-INVALID`) or by the hex regex, so the outcome still holds. The issue is that the class name reads as covering ref-level tags, which the binder never peels.

**Out-of-scope limits, not defects.** These are not among the five declared classes and must not be read as covered:
- a tag whose target object is missing (corrupt repository, shallow clone, or promisor remote);
- a tag whose `type` header contradicts its target.

[INFERENCE: both reach `E-REVISION-INVALID` through the same `rev-parse` failure path, because `--git-dir` succeeds.] The candidate correctly claims no universal tag-target coverage (SKILL line 2114, lessons line 65).

## Duplicate authorities

The outcome/finding tuple is stored three times: the checker's `EXPECTED` constant (lines 17–23), the JSON, and the prose. Behavior comes from a fourth authority, `_revision.py`. C1 checks the copies against each other, never against the binder. This is disclosed (SKILL line 2150, "fixed five class/outcome/finding tuples in code"), so it is a tradeoff rather than a defect. It does mean C1 green says nothing about whether the binder refuses.

## Smallest safe corrections

1. **Provenance (CX1).** Do one of the following:
   - Add the located S081 failure clause, quoted in 25 words or fewer, to `sources/git-types.txt`, the lessons source row and prose line 11.
   - Or label the `refuse`/`E-REVISION-INVALID` half of this row as lane policy, citing `_revision.py` contract step 3, and keep S081 only for the Git distinction.

   Restoring the draft's "under lane policy" rationale wording is enough for the second option.
2. **Prose binding (CX2).** Split each prose row on `|` and require the exact class in cell 1, outcome in cell 3, and finding in cell 4 for refusal rows. Add a selftest case that uses the real five-column layout and puts `refuse` in a non-outcome cell, and require that case to fail.
3. **Named control.** Add a C1 selftest mutation `tag-noncommit-accept` that sets `decisions[4].outcome = accept-if-landed-and-pushed` and expects `SELECTOR-CONTRACT-MISMATCH`.
4. **Nested noncommit (CX3).** Either add a `nested_tag_to_tree` or `nested_tag_to_blob` case to the binder selftest and a separately named, preregistered-next-round C2 class, or narrow the C1 prose to single-level annotated tags. Do not add the case to the frozen round-21 C2 five-class count after outcomes are seen.
5. **Scope wording (CX4).** Write "Annotated tag" in prose line 23 and JSON line 9.

## Limits

- This is a source-only review. Every behavioral statement above is a prediction from reading the code; no test, mutant, Git command or checker was run.
- The retained Git excerpt is a bounded extract. I did not open the official manuals.
- No tool install or update was needed or performed.
- This is an author-dispatched seat, not outside or non-author closure. No admission, promotion or integration is claimed.

Reviewed-SHA256: 1dc94c5f733a9a0112c5db0e94dda5eca31e4f2d982950bc56e08461040d7dd7
Predicate: C1-noncommit tag refusal
Lane bounds: leaf member — no subagent dispatch.
Scope: executed=none
