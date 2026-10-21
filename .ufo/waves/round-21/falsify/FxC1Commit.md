# FxC1Commit — falsify: C1 commit row and lane ancestry/origin policy boundary

Candidate revision 0a14952b59d20179e1c813af58befaecd6992a17. Primary: `.ufo/waves/round-21/candidate/corpus/knowledge/selector-contract-r21.json` (the inventory lists SHA-256 1dc94c5f…40d7dd7). I read only the frozen snapshot. Every claim below is a source reading or a source prediction. No test, mutant, selftest, Git command or import was run.

Axes: source grounding (S081/S082 versus lane policy), commit-row outcome fidelity to the binder, provenance and duplicate authority, control coverage (fail-capability), and scope/safety.

## Verdict

The commit row is correct as lane policy. Its outcome `accept-if-landed-and-pushed` agrees with the frozen binder, with QUALITY27, and with the frozen judge. No defect forces rejection. I found three fixable precision defects and one limit that should be disclosed. The ExecDecision build draft disagrees with the lane on what "pushed" means, and the candidate correctly did not adopt the draft's position.

## Observations (from source reads)

- O1, the row agrees with the binder. The JSON commit row (line 5) gives outcome `accept-if-landed-and-pushed`, finding `null` and source `S082`, and its rationale says ancestry and origin checks "remain separate". The checker's `EXPECTED["commit"]` (check-selector-contract.py:18) holds the same tuple. In `_revision.py` `_object_commit` (:112–146), an object whose type is `commit` is returned by its confirmed object ID without reparsing. `bind` (:172–192) then checks, in order: branch-ref existence, local ancestry, and origin ancestry only `if _exists(repo, remote)`. QUALITY.md:37 (item 27) says "when present, of `refs/remotes/origin/<branch>`".
- O2, "pushed" is satisfied vacuously when there is no origin ref, and that is the intended policy. The frozen judge check-revision-binding.py deletes the origin ref and requires acceptance (`shared_cases["origin-absent"] = accepted(...)`, :455–457). It also grades a `require-origin` stub as failing exactly `{"origin-absent"}` (:1176). The prose (md:25) defines "Pushed" as "only the local origin tracking ref when present". The JSON row and the outcome token do not carry that qualifier.
- O3, the advisory draft is not lane policy. build/ExecDecision.md:8 says its draft "refuses acceptance when no `origin/<branch>` tracking ref exists". That is exactly the `require-origin` behavior the frozen judge rejects (O2). The candidate checker does not do this; it calls `_revision.bind` unchanged (:153). The draft's schema (`schema_version`/`rows`/`proposition`) is also incompatible with the candidate checker. Because the draft is advisory, this conflict is resolved in favor of the candidate.
- O4, the commit row lists only some of its refusal findings. The prose commit row (md:19) says "ancestry failures retain E-REVISION-NOT-LANDED / E-REVISION-NOT-PUSHED". The binder can also refuse a commit with E-BRANCH-INVALID (checked first, :174), E-BRANCH-MISSING (:182–183), E-REVISION-INVALID for an ambiguous prefix even when one candidate is a commit (:123–124), and E-GIT-FAILED for an origin ref that names a non-commit (:156–160; selftest `git-failed-origin-blob` :420–421). The outcome conditions are therefore wider than "landed and pushed".
- O5, the source citation in JSON differs from the prose. JSON commit `source: "S082"` disagrees with the prose Sources cell "S081, S082" (md:19). The checker only tests `row.get("source") in urls` (:77–78) and never cross-checks the prose Sources column. Neither S081 nor S082 supports the landed/pushed half of the outcome; md:13 and the S081/S082 scope cells in SOURCES.md:88–89 say so. Even so, the single machine-readable `source` field attributes the whole tuple, including the policy half, to S082. The policy authority (QUALITY27/36 and `_revision.py` at the baseline) appears only in md:1 and the round-21 lesson (:50), not in the row.
- O6, the prose check is a substring match. `supported` (:75–76) requires that the outcome string appears somewhere in the single `| commit |` line. A prose commit row that also said `refuse | E-REVISION-INVALID` would still pass, so the checker cannot tell an accept row from a contradictory one.
- O7, the checker has duplicate authorities and no link to the binder. Agreement is measured among three copies: the code constant `EXPECTED`, the JSON file, and the prose table. `_revision.py` is never consulted. A binder regression (for example, dropping the origin check) leaves C1 at 5/5. This is disclosed (docstring :2, scope string :32, SCORECARD:650), so it is a tradeoff, not a defect.
- O8, the selftest does not mutate the commit row's outcome. Its mutations cover tree-accept, tag-refuse and the commit row's *source* (`S999`), but not commit outcome→refuse or a commit prose-cell change (:114–123). [INFERENCE] The generic per-row comparison would still catch an outcome change; the gap is in fail-capability evidence, not in behavior.

## Counterexamples (source predictions, not run)

1. **Strongest: `git replace` changes object identity (all rows; commit identity).** `clean_env` (:62–66) strips `GIT_*` and does not set `GIT_NO_REPLACE_OBJECTS`. No git call passes `--no-replace-objects`, and a candidate-wide grep for replace, graft or shallow finds nothing relevant.
   - [INFERENCE from Git's documented default of honoring `refs/replace/*`] Suppose a landed commit X is replaced by commit Y. Then `cat-file -t X` reports `commit` and `bind` returns `sha=X`. But `merge-base --is-ancestor` and the checker's `git show X:path` (:87) traverse and read Y's history and tree, so the receipt names X while the bytes come from Y.
   - With `git replace -f`, a blob or tree replaced by a landed commit would be typed `commit` and accepted. That contradicts the tree/blob rows and the "existing commit object" premise in md:19.
   - The threat requires local ref tampering in the lane repo, so this is a disclosed-limit or tradeoff case rather than a C1 rejection.
2. **Origin absent.** Take a landed commit in a clone whose remote is not named `origin`, or one that has never fetched. The binder accepts it under `accept-if-landed-and-pushed` with `origin_tip=None` (:186–192). This matches the intended policy (O2), but a reader of the JSON alone gets false "pushed" provenance.
3. **Ancestry for tag-to-commit is never tested (adjacent row; FxC1CommitTag owns that row).** Every annotated-tag acceptance control targets `tip`, which is both landed and pushed: binder selftest :353–365, the round20 matrix :502–505 and :631–632, and the new target-type matrix :697–703. No control tags an unlanded or unpushed commit.
   - [INFERENCE] A mutant that returned immediately after peeling a tag, before the ancestry checks, would pass every listed control.
   - The text "the peeled commit is what is checked" (md:13) is therefore supported by source reading but has no control showing it can fail. The direct-commit row is covered (`unlanded`, `not-pushed`, `unpushed_object`, origin-absent).

## Impacted axes

- Source grounding: O5.
- Commit-row fidelity: O2, O4 and counterexample 2.
- Provenance and identity: counterexample 1 and O5.
- Control coverage: O6, O8 and counterexample 3.
- Scope/safety: unaffected, because the gate does only immutable Git reads.

## Smallest safe corrections

- JSON commit row (primary): put the conditions inside the row. Change the rationale to say that "pushed" is checked only when `refs/remotes/origin/<branch>` exists, per QUALITY27. Alternatively, add a policy-authority field naming QUALITY27/`_revision.py`, keeping S082 for the type proposition only. Make the prose Sources cell agree with JSON (S082 alone, or both).
- Prose commit row (auxiliary): list the full refusal set: E-BRANCH-INVALID, E-BRANCH-MISSING, E-REVISION-INVALID (ambiguous prefix), E-REVISION-NOT-LANDED, E-REVISION-NOT-PUSHED and E-GIT-FAILED. Keep first-failure precedence.
- Checker (auxiliary): compare the outcome and finding cells exactly, column by column, instead of with `in`. Add a commit-outcome selftest mutation.
- Disclosure, or a binder follow-up outside C1: state that object type and ancestry are as resolved with replace refs honored. If a binder change is chosen, it is one environment entry, `GIT_NO_REPLACE_OBJECTS=1`, in `clean_env`, and it needs its own cross-consumer review.
- Coverage follow-up (tag-row owner): add a control with an annotated tag pointing to an unlanded commit (expect E-REVISION-NOT-LANDED) and one pointing to an unpushed commit (expect E-REVISION-NOT-PUSHED).

## Auxiliary snapshot dependencies read

From the candidate inventory: `tools/check-selector-contract.py` (239758b4…), `corpus/knowledge/selector-contract-r21.md` (b4966a9b…), `tools/_revision.py` (06b71e8c…), `tools/check-revision-binding.py` (0722537d…), `corpus/QUALITY.md` (1ac63548…), `corpus/SOURCES.md` (ef697b7c…), `SKILL.md` (c43477cb…), `SCORECARD.md` (04403120…) and `corpus/lessons/round-21.md` (ab841b25…).

Outside the candidate, read as advisory or contextual only: `.ufo/waves/round-21/build/ExecDecision.md`, `.ufo/waves/round-21/drafts/ExecDecision/selector-contract-r21.json`, `.ufo/waves/round-21/sources/git-types.txt`, `.ufo/waves/round-21/preregister.json` and the FxC1Commit entry in `.ufo/waves/round-21/falsify-reviews.json`.

## Limits

- I did not fetch the Git documentation. Git semantics beyond the retained excerpts, such as the replace-ref default, are [INFERENCE].
- This is an author-dispatched falsify seat, not non-author closure or promotion.
- No tool was installed or updated, and none was needed.

Reviewed-SHA256: 1dc94c5f733a9a0112c5db0e94dda5eca31e4f2d982950bc56e08461040d7dd7
Predicate: C1-commit policy boundary
Lane bounds: leaf member — no subagent dispatch.
Scope: executed=none
