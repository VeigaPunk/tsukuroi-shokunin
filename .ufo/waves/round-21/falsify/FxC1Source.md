# FxC1Source — falsify attack on C1 selector-contract source grounding

Seat: TsukuroiR21.FxC1Source (critic, leaf). Candidate revision 0a14952b59d20179e1c813af58befaecd6992a17.

Reviewed-SHA256: 1dc94c5f733a9a0112c5db0e94dda5eca31e4f2d982950bc56e08461040d7dd7
Predicate: C1-located source quotes
Lane bounds: leaf member — no subagent dispatch.

Primary file: `.ufo/waves/round-21/candidate/corpus/knowledge/selector-contract-r21.json`. Its digest is the one declared in `candidate-files.json`. I did not hash it myself, because hashing would require execution.

Auxiliary snapshot dependencies, all read from the frozen candidate tree, with digests as declared in `candidate-files.json`:
- `corpus/knowledge/selector-contract-r21.md` (b4966a9b…6353)
- `corpus/SOURCES.md` (ef697b7c…c3e4), rows S077, S081, S082, S050 and the Round21 curation paragraph
- `corpus/lessons/round-21.md` (ab841b25…49c9)
- `corpus/QUALITY.md` (1ac63541…8596), criteria 19 and 21
- `tools/check-selector-contract.py` (239758b4…aea50)
- `SKILL.md` and `SCORECARD.md` (C1 rows only)

Advisory evidence only, not candidate files and not production:
- `.ufo/waves/round-21/build/ExecDecision.md`
- `.ufo/waves/round-21/drafts/ExecDecision/selector-contract-r21.json`
- `.ufo/waves/round-21/sources/git-types.txt`
- `.ufo/waves/round-21/preregister.json` (C1 block)

Official sources reopened on 2026-10-21 with the read-only URL reader. No local program, git, hashing or test was run:
- S081 https://git-scm.com/docs/gitrevisions/2.56.0
- S082 https://git-scm.com/docs/git-rev-parse/2.56.0

## Axes

1. Quote fidelity and locator: is the exact text present, at most 25 words, under the cited heading and version?
2. Row attribution: does each JSON row's `source` actually support that row's proposition?
3. Tier and scope: does each source support only what its row says, and nothing about host or ancestry?
4. Registry and used-by: are paths accurate, and is there any duplicate authority?
5. Gate enforcement (auxiliary): does the checker actually enforce the predicate?

## Observations (read directly from fetched pages and frozen files)

O1. The S081 quote is present. Under SPECIFYING REVISIONS, in the entry for the typed suffix (rendered as `^{}, e.g. v0.99.8^{commit}`), the page reads: "For example, if <rev> is a commit-ish, <rev>^{commit} describes the corresponding commit object." The renderer strips the `<rev>` placeholders; every other word matches. The quote is 13 words. The gitrevisions change list shows 2.56.0 dated 2026-09-28.

O2. The S081 empty-brace entry is present: "A suffix ^ followed by an empty brace pair means the object could be a tag, and dereference the tag recursively until a non-tag object is found." The prose (md line 11) paraphrases it accurately. The lessons file (line 54) correctly rejects the claim that `^{}` peels only one level.

O3. The S082 quote is present and verbatim: "you can add the `^{type}` peeling operator to the parameter." It is 10 words. It is the main clause of a conditional sentence; the omitted condition ("If you want to make sure that the output actually names an object … and/or can be used as a specific type of object you require") does not change the meaning.

O4. The S082 paragraph also says, without being quoted anywhere in the candidate: `"$VAR^{commit}"` "will make sure `$VAR` names an existing object that is a commit-ish (i.e. a commit, or an annotated tag that points at a commit)."

O5. The S081 typed entry also says, without being quoted anywhere in the candidate: "dereference the object at <rev> recursively until an object of type <type> is found or the object cannot be dereferenced anymore (in which case, barf)." This is exactly 25 words. It is the only text in either source that supports nested-tag recursion under typed peeling, and the only text that supports refusing a tree or blob.

O6. The S082 locator says "OPTIONS --verify". In the fetched render, `--verify` sits under the sub-heading "Options for Output". The render shows no literal `OPTIONS` level-2 heading; it goes straight from DESCRIPTION to "Operation Modes". [INFERENCE] The AsciiDoc source probably has an OPTIONS heading that the renderer dropped.

O7. Each JSON row carries one `source`:

| Row | JSON source |
|---|---|
| commit | S082 |
| tree | S081 |
| blob | S081 |
| tag-to-commit | S082 |
| tag-to-noncommit | S081 |

The md table cites "S081, S082" on every row. The JSON has no quote or proposition field. The advisory ExecDecision draft assigned `tag-to-commit` to S081 and had a `proposition` field.

O8. In SOURCES.md, S081 and S082 are both tier A, docs, mined, recheck on-release. Their used-by is `corpus/lessons/round-21.md, corpus/knowledge/selector-contract-r21.md`. Both files exist in the snapshot and cite both IDs. The primary JSON cites both IDs (top-level `sources` plus per-row `source`), but it is not listed in used-by. Precedent is mixed:
- S050 (SOURCES line 56) lists both its `.md` and `.json`.
- The S039/S040 note (line 114) lists only the `.md`, even though the `.json` cites them.

O9. S077 and S082 share a URL and both point at `--verify`. S077's scope already includes "commit-ish peeling", and its teaches line says verification "can peel an annotated-tag object to a commit". The Round21 curation paragraph (SOURCES line 146) calls S082 "the narrower typed-verification scope". Earlier curation paragraphs (lines 122, 126, 134) state the W04 duplicate-URL count increment explicitly; line 146 does not.

O10. `check-selector-contract.py` checks:
- the five-class set and the exact outcome/finding tuples;
- `sources == ["S081","S082"]`;
- that each row's `source` is one of the two IDs;
- that the rationale is a non-empty string;
- one md table row per class, where the outcome and finding must appear as substrings anywhere in that row;
- that the registry row's URL is a substring of the source cell, with tier A and status mined.

It does not read the md quote line, the md `source:` header, used-by, the Sources column of the prose table, or whether a row's source fits its proposition.

## Counterexamples

### F1 — wrong source on the tag-to-commit row (medium; fixable defect)

The JSON row's rationale claims "Ordinary and nested annotated tags recursively peel to a commit" and cites only S082. S082's own definition says "an annotated tag that points at a commit" (O4). Read literally, that is a single hop and never mentions nesting or recursion. The recursion appears only in S081's unquoted typed-peel clause (O5).

A reviewer checking this row against its declared source alone cannot locate support for "nested". The build draft had this right (S081); the candidate regressed it.

- Axes: attribution, quote fidelity.
- Smallest correction: set `tag-to-commit` source to S081, or allow a list ["S081","S082"]. Add the located 25-word typed-peel quote (O5) to the md/lessons quote rows.

### F2 — tree and blob refusals rest on quotes that don't say it (low-medium; fixable defect)

These rows say "A non-empty tree / file-content object is not commit-ish", citing S081. The only located S081 quote is conditional ("if <rev> is a commit-ish") and does not define commit-ish, so on its own it cannot establish that a tree or blob is not commit-ish. The real support is S081's unquoted "cannot be dereferenced anymore (in which case, barf)" (O5), or S082's unquoted definition (O4).

QUALITY19 requires each admitted sentence to name the source object, its located ≤25-word quote, and the exact proposition. That is met for "typed peeling exists", not for "refuse tree/blob".

- Axes: attribution, quote fidelity.
- Smallest correction: add the O5 clause and the O4 parenthetical "(i.e. a commit, or an annotated tag that points at a commit)" as located quotes, and tie the tree, blob and tag-to-noncommit rows to them.

### F3 — the gate cannot catch quote or attribution regressions (medium; auxiliary dependency, not a defect in the primary file)

These are predictions from reading the code; none was executed:
- Deleting md line 11 (both quotes) still leaves the checker at PASS with `decision_rows=5`.
- Swapping any row's `source` between S081 and S082 still passes.
- A prose tree row whose outcome cell says `accept-if-landed-and-pushed` while another cell contains "refuse … E-REVISION-INVALID" passes, because the outcome check is a row-wide substring test. The selftest's `prose-outcome` mutant does not catch this, since its replaced row contains no other "refuse".

So a green `decision_rows=5` cannot be read as evidence for the predicate "C1-located source quotes". SCORECARD line 638's "validated decision_rows0→5" is accurate only for the tuples.

- Axes: gate enforcement, calibration.
- Smallest correction: make the claim explicit in SCORECARD and SKILL ("gate checks tuples and registry rows, not quote location or row attribution"). Optionally, check the outcome cell by column index rather than by substring.

### F4 — S082 overlaps S077 rather than narrowing it (low; tradeoff, disclosed)

S082 is called narrower than S077, but S077's scope and teaches already cover commit-ish peeling under the same URL and option (O9). That gives two mutable authorities for one on-release recheck, which can drift apart. The W04 increment is not stated.

- Axes: registry, duplicate authority.
- Smallest correction: state the new W04 count in the Round21 curation paragraph, and phrase S082's scope as the `^{type}` paragraph's requested-type guarantee, explicitly overlapping S077. Alternatively, extend S077's used-by instead of adding a row. This is a judge's tradeoff, not a correctness defect.

### F5 — used-by omits the primary JSON (low; convention inconsistency)

The JSON is the C1 primary and cites both sources, but neither row's used-by lists it (O8). The repo has precedent both ways.

- Axes: registry.
- Smallest correction: append `corpus/knowledge/selector-contract-r21.json` to the used-by of S081 and S082, following S050, and record the mutable change.

### F6 — the tree rationale is narrower than the class (low)

"A non-empty tree" is a test-control qualifier; neither source distinguishes empty from non-empty trees. It also reads narrower than the prose ("even a non-empty one", meaning all trees) and leaves the empty tree unaddressed in the JSON wording.

- Axes: attribution, scope.
- Smallest correction: change the JSON rationale to "A tree object is not commit-ish."

### F7 — "tree or blob" is derived, not quoted (low; label as inference)

The `tag-to-noncommit` rationale says empty-brace peeling "can stop at a tree or blob". S081 says only "a non-tag object". Naming tree and blob relies on Git's object model, which neither quoted text states.

- Axes: quote fidelity.
- Smallest correction: say "a non-tag object (tree or blob)" and mark the instantiation as derived.

### F8 — S082 locator could be more precise (low)

The observed path is "Options for Output › --verify" (O6). "OPTIONS --verify" is probably correct but was not observed literally in this render.

- Axes: locator.
- Smallest correction: use "OPTIONS › Options for Output › `--verify`".

## Held ground (no counterexample found)

- All five outcome/finding tuples agree with S081/S082 semantics combined with the lane's object-prefix, ancestry and push policy. No row is falsified on its outcome.
- Both located quotes are present and at most 25 words, under the cited headings, at version 2.56.0. The S081 version date was observed; the S082 version is observed only in the URL.
- Tier-A scope statements correctly exclude host health and ancestry, and the S082 teaches line ("a valid object ID alone is not a commit") is supported by the `--verify` paragraph.
- The lessons gate row rejecting "`^{}` is interchangeable with `^{commit}`" is source-correct.

## Limits

- [INFERENCE] The candidate digest is bound only through the inventory's declaration.
- The renderer strips placeholders, so exact `<rev>` and `<type>` tokens are reconstructed from the entry structure, the in-repo excerpt (`sources/git-types.txt`) and the lessons file.
- The WebFetch reader may return cached content.
- Nothing about consumer or binder behavior, C2 or C3 was evaluated. No non-author closure or outside promotion is claimed.
- No tool was installed or updated, and none was needed.

Scope: executed=none
