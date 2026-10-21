# FxC1Tree — falsify C1 tree refusal (critic, round 21)

Target: candidate revision 0a14952b59d20179e1c813af58befaecd6992a17, primary `.ufo/waves/round-21/candidate/corpus/knowledge/selector-contract-r21.json`, SHA-256 1dc94c5f733a9a0112c5db0e94dda5eca31e4f2d982950bc56e08461040d7dd7 (as stated in `candidate-files.json`; I did not recompute any hash because this seat is no-exec).

Auxiliary frozen snapshot dependencies I read (digests from `candidate-files.json`, not recomputed):
- `candidate/tools/check-selector-contract.py`, 239758b49da4f24415f53adb52cc6833818d0e340f0832d0389416bce50aea50
- `candidate/corpus/knowledge/selector-contract-r21.md`, b4966a9bcf4ac124a964718b0ed76104e2f07c41b63050dc8bda618ea5136353
- `candidate/corpus/SOURCES.md`, ef697b7c6b60bf0e5b71e1267f30cda678d5de01abc803b24dcc7dce1b93c3e4 (S081 and S082 rows only)
- `candidate/tools/_revision.py`, 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf (binder behaviour for tree objects)

Other evidence I used, which is not part of the candidate inventory: the retained source extract `.ufo/waves/round-21/sources/git-types.txt` and the advisory build draft report `.ufo/waves/round-21/build/ExecDecision.md`. I did not read any production or moving draft file to reach a verdict.

Axes: C1 depth (data/prose/source agreement for the tree row); calibration (whether the selftest is faithful to the real layout); source grounding; no-harm (exit-code contract). C2 operability is out of scope.

## Verdict

The JSON-level C1 tree refusal holds. If the tree row in the JSON says accept, the validator rejects it with SELECTOR-CONTRACT-MISMATCH and exit 1 (a source prediction, not executed). The prose-agreement half of the contract can be defeated: the Markdown tree row can say accept, or a second contradictory tree row can be added, and the validator would still return PASS. This is a fixable defect in the frozen checker, not a tradeoff that the judge must reject. The frozen JSON bytes and the frozen prose are currently correct and agree with each other.

## Observations (read from frozen bytes)

- O1. The JSON tree row, `selector-contract-r21.json` line 6, is `{"class": "tree", "outcome": "refuse", "finding": "E-REVISION-INVALID", "source": "S081", "rationale": "A non-empty tree is not commit-ish."}`.
- O2. The prose tree row, `selector-contract-r21.md` line 20, is `| tree | Existing tree, even a non-empty one, is not commit-ish | refuse | E-REVISION-INVALID | S081, S082 |`. It agrees with O1.
- O3. The checker hard-codes `EXPECTED["tree"] = ("refuse", "E-REVISION-INVALID")` at `check-selector-contract.py` lines 17–23. Lines 70–80 compare the JSON tuple `(outcome, finding)` against this constant exactly. Prose support at lines 73–76 is weaker: the checker takes every line that starts with `"| tree |"`, requires exactly one such line, and then only requires `outcome in line` and `finding in line` as substrings anywhere in that line. It does not check which column the text is in, does not tokenise cells, and does not check for the opposite outcome.
- O4. The `rationale` field is only checked to be a non-empty string (line 78). Its meaning is never checked.
- O5. The checker parses with `json.loads` and no duplicate-key hook (line 41).
- O6. The selftest `tree-accept` mutant (line 116) changes the JSON outcome and expects MISMATCH with exit 1. The `prose-outcome` mutant (lines 122–123) runs against a synthetic three-column prose fixture (lines 105–106) using `replace("| tree | refuse", "| tree | accept")`. The real prose has five columns, with the Git-distinction column between the class and the outcome, so the string `| tree | refuse` does not occur in the real file.
- O7. The binder `_revision.py` refuses trees. `_object_commit` (lines 133–137) returns None for any object type other than commit or tag, and `bind` (lines 177–179) then raises E-REVISION-INVALID. This matches the C1 tree outcome and finding. Tree objects are never peeled.
- O8. The S081 and S082 rows in `SOURCES.md` (lines 88–89) have 11 columns, which split into 13 cells. Cell 2 contains the URL, cell 4 is `A` and cell 8 is `mined`, which satisfies checker lines 58–66.
- O9. The retained extract `sources/git-types.txt` (lines 3–6) contains only the conditional "if <rev> is a commit-ish, <rev>^{commit} describes the corresponding commit object" and the definition of empty-brace peeling. It has no sentence saying that a tree is not commit-ish, or that `^{commit}` fails on a tree.

## Counterexamples (source predictions, not executed)

- CE1, the target case. Change JSON line 6 to `"outcome": "accept-if-landed-and-pushed"` (with the finding kept or set to null) and leave the prose alone. Predicted result: `(outcome, finding) != EXPECTED["tree"]` is true, giving a SELECTOR-CONTRACT-MISMATCH finding with detail `tree`, `decision_rows` 4 and exit 1. The refusal holds, consistent with the SKILL registry row "1 missing/wrong decision".
- CE2, a prose row containing both tokens. Change line 20 to `| tree | Existing tree; lane no longer must refuse it | accept-if-landed-and-pushed | E-REVISION-INVALID | S081, S082 |`. Predicted result: there is still exactly one `| tree |` line and it contains both `refuse` and `E-REVISION-INVALID`, so the checker returns PASS 5/5 while the visible Lane-outcome cell says accept. A variant such as `| accept-if-landed-and-pushed | none (was: refuse / E-REVISION-INVALID) |` also passes.
- CE3, a contradictory row the prefix match does not see. Insert directly after line 20 a row such as `|tree| non-empty tree | accept-if-landed-and-pushed | — | S081 |`, or `| tree  | ...` with two spaces, or `| Tree | ...`. Markdown renders it as a second tree row in the same table, but `startswith("| tree |")` does not count it. Predicted result: PASS. A stronger variant is to rewrite the visible row with a variant prefix and place the canonical `| tree | refuse E-REVISION-INVALID |` line inside an HTML comment (`<!--` … `-->`). Readers then see only accept, and the checker still finds exactly one matching row. Predicted result: PASS.
- CE4, the meaning of the data is not bound. A tree rationale such as `"Trees are accepted once landed."` with outcome refuse passes (O4). A duplicate-key object, `{"class":"tree","outcome":"accept-if-landed-and-pushed","outcome":"refuse",...}`, passes because Python keeps the last key (O5), even though the raw bytes show accept first. [INFERENCE] Parsers that keep the first duplicate key would read accept.
- CE5, the selftest does not model the real file. The `prose-outcome` mutant cannot represent a real-layout prose regression (O6), so a passing selftest is not evidence that CE2 or CE3 would be caught. Calibration impact only.

## Source grounding (tree row)

The JSON rationale claims "not commit-ish", but the cited S081 quotation in the retained extract only establishes the forward conditional (O9). That a tree fails commit peeling is inferred, not quoted. [INFERENCE] The full gitrevisions page says `^{<type>}` dereferences until the type is found "or the object cannot be dereferenced anymore (in which case, barf)", and gitglossary defines commit-ish. Neither sentence is retained or cited. This weakens the source/prose agreement axis but does not change the outcome, and it is fixable by adding that located quotation.

## Advisory comparison (build ExecDecision draft, not production)

The draft report describes a stronger design: an `id` and `proposition` per row, with the exact proposition required in the same Markdown row or block. The frozen candidate dropped both and checks only substrings, which is the regression CE2 and CE3 exploit. The draft's missing-origin refusal is also absent from the frozen checker. That is consistent with the frozen prose ("origin tracking ref when present") and `_revision.py`, so it does not affect the tree row.

## Smallest safe correction

1. In `check-selector-contract.py`, split each table line into cells. Require exactly one row whose normalised first cell (stripped and lower-cased) is `tree`. Require cell 3 to equal the outcome exactly and cell 4 to equal the finding exactly for refusal rows. Reject the file if any other table-like line has a normalised first cell equal to a class name. Ignore or reject HTML-comment and fenced regions.
2. Add `object_pairs_hook` duplicate-key rejection, giving SELECTOR-CONTRACT-SCHEMA with exit 2.
3. Rebuild the selftest prose fixture in the real five-column layout and add mutants for CE2 (both tokens in one row) and CE3 (variant-prefix duplicate row).
4. Either stop treating `rationale` as support, or cite the located "cannot be dereferenced … barf" quote in the S081 extract.

The current frozen JSON and prose need no change.

## Limits

No test, mutant, selftest, hash computation, Git command or network fetch was run. All CE results are predictions from the source text. I did not judge, admit or integrate anything. This is not non-author closure. No tools were installed or updated, and none were needed.

Reviewed-SHA256: 1dc94c5f733a9a0112c5db0e94dda5eca31e4f2d982950bc56e08461040d7dd7
Predicate: C1-tree refusal
Lane bounds: leaf member — no subagent dispatch.
Scope: executed=none
