# FxC1CommitTag — critic attack on C1 tag-to-commit (recursive / nested) row

Reviewed-SHA256: 1dc94c5f733a9a0112c5db0e94dda5eca31e4f2d982950bc56e08461040d7dd7
Predicate: C1-recursive tag commit

Primary: `.ufo/waves/round-21/candidate/corpus/knowledge/selector-contract-r21.json` (candidate revision 0a14952b59d20179e1c813af58befaecd6992a17; digest from `candidate-files.json`, not recomputed by me — NO-EXEC).

Auxiliary snapshot dependencies, read only, cited by their `candidate-files.json` digests:
- `candidate/tools/check-selector-contract.py` 239758b49da4f24415f53adb52cc6833818d0e340f0832d0389416bce50aea50
- `candidate/corpus/knowledge/selector-contract-r21.md` b4966a9bcf4ac124a964718b0ed76104e2f07c41b63050dc8bda618ea5136353
- `candidate/corpus/lessons/round-21.md` ab841b2562e41fa69f90b63b8444d5ab47670ce2acf0ec1208f71cf7980349c9
- `candidate/corpus/SOURCES.md` ef697b7c6b60bf0e5b71e1267f30cda678d5de01abc803b24dcc7dce1b93c3e4
- `candidate/tools/_revision.py` 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
- `candidate/tools/check-revision-binding.py` 0722537d1b3fffbb78566ddaba21dbd796f4a89ceb81f772a20596cb40af6fa6

Non-snapshot advisory material (not in `candidate-files.json`, so these are not candidate verdict inputs): `.ufo/waves/round-21/sources/git-types.txt` (retained source excerpt), `build/ExecDecision.md`, `build/Oracle09NestedTag.md`.

## Axes

- **Source grounding (depth C1):** does a retained or quoted source text actually support the recursive or nested claim made in the tag-to-commit row?
- **Fail-capability (calibration C1/C3):** would the C1 gate refuse a contract that dropped the recursive claim or turned it into a one-level claim?
- **Semantic correctness:** do the nested-tag and empty-brace (`^{}`) statements match Git semantics, and is the one-level `^{}` claim correctly rejected?
- **No-harm / identity:** does the row change binder behavior or create a duplicate authority?

## Observations (read from frozen bytes)

1. **Mapping is correct.** JSON line 8 puts nested tags in `tag-to-commit`: `"Ordinary and nested annotated tags recursively peel to a commit"`, with outcome `accept-if-landed-and-pushed` and finding `null`. Prose row md:22 matches ("including nested annotated tags, peels recursively"). Nested tags that end at a tree or blob fall under `tag-to-noncommit` (JSON:9, md:23), although that row never says "nested".
2. **No one-level claim survives in the candidate.** I grepped the candidate tree for `one-level|one level|single dereference|depth-1|one-hop|nested|recursiv`. The only `^{}` one-level proposition is the explicit rejection at lessons:54: "Rejected `Oracle09NestedTag.md`'s proposition that `^{}` is a one-level peel: S081 expressly says recursively until a non-tag object." The empty-brace wording in JSON:9 ("can stop at a tree or blob") and md:11 ("stops at a non-tag object") is consistent with recursion. The rejection is correct. The retained excerpt for `<rev>^{}` reads: "dereference the tag recursively until a non-tag object is found." Oracle09:86–88 ("`^{}` (single dereference)") is therefore wrong, and the candidate does not adopt it.
3. **The recursive typed-peel claim is attributed to a source that does not state it.** The JSON tag-to-commit row cites `"source": "S082"`. The only S082 text quoted or retained (lessons:23, md:11, git-types.txt:10) is "you can add the `^{type}` peeling operator to the parameter." It says nothing about recursion or nesting. For S081, the retained `<rev>^{<type>}` text is only "if <rev> is a commit-ish, <rev>^{commit} describes the corresponding commit object." The word "recursively" appears in the retained excerpt only under `<rev>^{}`, the empty-brace form, which is not the operator the binder uses (`_revision.py:139–140` peels with `^{commit}`).
4. **The gate does not enforce the recursive claim.** `check-selector-contract.py:70–82` checks only these things for each row: the `(outcome, finding)` tuple; `source ∈ {S081, S082}` with no per-class source; a non-empty `rationale` string; and one prose row starting with `| tag-to-commit |` that contains the outcome substring. The words "nested" and "recursive", and the content of the rationale, are never inspected. The selftest (`:100–133`) has no rationale or proposition mutation.
5. **Downstream controls (C2 auxiliary).** `_revision.py:362–365` asserts `nested-annotated-tag-object → tip`. `check-revision-binding.py:702` adds `nested_tag_to_commit` to the new opt-in matrix. The only mutant, `target-generic-peel` (`:986–988`, a tag-only `^{}`), is checked at `:1247–1250` for `tag_to_tree` failing and `all(ok)` being False. There is no assertion about `nested_tag_to_commit` under that mutant, and no one-hop mutant exists. Lessons:54 concedes that "a genuine one-hop implementation would need a different mutant."
6. **The advisory ExecDecision draft is a different shape.** Per its report (md:11), it uses `schema_version`/`rows` with required `id` and an exact `proposition` field that must also appear in the Markdown row. That would have tied the proposition text to the prose. The landed candidate dropped that field (`schema`/`decisions`, no `proposition`), which is why observation 4 holds. This is advisory only, not a production comparison.

## Source predictions (not observed; nothing was run)

- **P1, gate vacuity counterexample.** Suppose the tag-to-commit rationale is mutated to "Only a directly tagged commit is accepted; nested annotated tags are refused" and md:22's description becomes "one-level annotated tag peels to the commit", with `accept-if-landed-and-pushed` kept in the row. I predict `evaluate()` returns code 0, `decision_rows: 5`, PASS. The same holds if the row's `source` is changed to either S081 or S082. The C1 PASS would then certify a proposition opposite to the one the row claims.
- **P2, Git semantics [INFERENCE from recall, page not reopened in this review].** The full gitrevisions `<rev>^{<type>}` entry also says it dereferences "the object at <rev> recursively until an object of type <type> is found or the object cannot be dereferenced anymore". gitglossary defines commit-ish to include a tag that points to a commit-ish. Either text, if located and retained, would ground the nested and recursive claim. Neither is in the retained excerpt, SOURCES S081 scope, or lessons quotes.
- **P3, generic-peel mutant on nested tags.** Because `^{}` is recursive, `target-generic-peel` resolves `nested_tag_to_commit` to the commit and the case stays `ok`. The mutant therefore cannot test nested recursion; it only tests noncommit tag targets. Lessons:54 says the same.
- **P4, one-hop mutant.** A binder that reads the tag's `object` header once and then requires `cat-file -t == commit` would refuse `nested_tag_to_commit`. The new matrix case (`:702`) and the binder selftest (`:364`) would fail. So a control able to catch it exists, but no witness exercises it.

## Counterexample and verdict

Strongest counterexample: P1 combined with observation 3. The tag-to-commit row's recursive claim is the thing this predicate concerns. It has no retained source quote that states it for typed peeling: its JSON citation is S082, which is silent on recursion. The C1 gate cannot fail if that claim is removed or reversed. The classification and outcome are correct, and the one-level `^{}` rejection is correct. However, "C1 counts five source-grounded decisions" grounds and gates only the outcome/finding tuple, not the recursive proposition carried in the row.

This is a **fixable defect**, not a tradeoff for the judge to reject. The binder and outcomes are unaffected, so there is no behavioral regression and no change of identity.

## Impacted axes

- Source grounding: degraded. The recursion claim is cited to S082 and quoted from the wrong S081 entry (`^{}` instead of `^{<type>}`).
- Fail-capability: the claim is not gated (P1). The nested recursion control has no killing mutant (P3, P4).
- Semantic correctness: unharmed. Nested→commit acceptance, nested→tree/blob refusal and recursive `^{}` are all correct.
- No-harm / identity: unharmed. No binder change, no duplicate authority, and the five-class identity is preserved.

## Smallest safe correction

1. Change JSON:8 to `"source": "S081"`. Add the located S081 `<rev>^{<type>}` recursion sentence (≤25 words) to the retained excerpt, the lessons quote row and md:11. Alternatively, open and register gitglossary "commit-ish" as a scoped source. Do not reuse the `^{}` sentence as the typed-peel ground.
2. In `check-selector-contract.py`, pin each class's source (`tag-to-commit → S081`). Require a fixed proposition token for tag-to-commit, for example `recursive` plus `nested`, in both the JSON rationale and the md row. Add a selftest case `tag-one-level` (rationale or prose without that token) that must give MISMATCH.
3. Optional, C2 auxiliary: assert `new_mutant_cases["nested_tag_to_commit"]["ok"] is True`. That is an execution witness that `^{}` is recursive and refutes the one-level claim. Also add a one-hop mutant that `nested_tag_to_commit` must kill.

## Limits

I ran nothing, computed no hashes, ran no mutants and opened no network source. The reviewed digest is the one stated in the assignment and in the inventory. P2 is recalled Git documentation, not an observation from this session. Author-dispatched critic: this is not non-author closure or outside promotion. No tools were installed or updated, and none were needed.

Lane bounds: leaf member — no subagent dispatch.

Scope: executed=none
