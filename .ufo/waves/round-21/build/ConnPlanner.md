# ConnPlanner — round21 three-claim separability, lowest axis (connector, leaf)

Reviewed-SHA256: aabd157d7651c1cca96560f5cf00ee8c665acb2be22a6b5d76239926ccbc67be
Predicate: three-claim-separability-lowest-axis
Lane bounds: leaf member — no subagent dispatch.

Read set: pinned snapshots `snapshot/corpus/QUALITY.md` (the digest above, as declared in `preregister.json` "snapshots"), `snapshot/tools/_revision.py` (06b71e8c…), `snapshot/tools/check-revision-binding.py` (da000de4…), `snapshot/corpus/lessons/round-20.md` (cc5abf67…), plus round data `preregister.json`, `reviews.json`, `build/spec.json` and `census-start.txt`. I could not recompute digests because this seat is NO-EXEC. The digests above are the declared pins, not values I measured.

## 1. Axes

- **depth (ordinal 8, the lowest):** C1 `decision_rows` 0→5.
- **operability (9):** C2 `target_type_tools` 0→9.
- **calibration (9):** C3 `pinned_reviews`, after = "every delivered build/falsify review".
- **No-harm guards:** adjacency 8, coverage 9 and freshness 9; preregistered `ordinal_deltas: 0` (`preregister.json:75-83`).

The round adds no new binder capability. `_revision.py` is unchanged in scope, and every claim measures declaration, coverage or pinning of behavior that already exists.

## 2. Observations

- **O1. The binder already decides all five classes.**
  - `_object_commit` returns commit IDs and peels only tag objects through `^{commit}`. Anything else returns None, which becomes E-REVISION-INVALID (`snapshot/tools/_revision.py:112-146, 172-179`).
  - The binder's own selftest already covers a nested annotated tag (`:362-366`) and direct blob/tree refusal (`:411-412`). It also covers tags pointing to a blob or tree (`:413`, loop over `(blob, "blob"), (tree, "tree")`).
  - This matches round20 lesson R20-BIND-TARGET-TYPE ("`_revision` selftest passes57/57").
- **O2. The old per-consumer matrix already covers part of C2.** `object_selector_probes` in `snapshot/tools/check-revision-binding.py` already runs these cases against every original-nine consumer:
  - `annotated_tag_object` (tag-to-commit, full ID) and `annotated_tag_prefix` (`:631-632`);
  - `noncommit_blob` (`:633`);
  - `full_object_id` (commit) (`:630`).

  C2's fifth case, `annotated_tag_to_commit` (`preregister.json:28-33`), overlaps `annotated_tag_object`. Only `nonempty_tree`, `tag_to_blob`, `tag_to_tree` and `nested_tag_to_commit` are new consumer cells: 4 × 9 = 36. Consistent with that, the oracle fan-out in `reviews.json` covers exactly those four types (Tree, TagBlob, TagTree, NestedTag) for each of the 9 consumers, 36 rows in total, with no AnnotatedTag oracle.
- **O3. C2's "before 0" depends on whether the mode exists, not on behavior.**
  - The ExecMatrix item says to "report target_type_tools0 for measured source lacking explicit type coverage even when its binder happens to behave correctly" (`build/spec.json` ExecMatrix prompt).
  - Neither the consumers nor the binder change this round. Measured on behavior alone, the expected baseline is therefore 9/9 consumers passing all five cases, not 0 [INFERENCE from O1 and O2; unmeasured].
- **O4. C1's count is fixed by its schema.** The ExecDecision gate requires "five exactly unique rows". A missing contract gives `decision_rows0`. So 0→5 is one presence fact, the contract file existing with all required rows, not five independent depth increments.
- **O5. C1's classes do not line up one-to-one with C2's cases.**
  - C1 has a single row, `tag-to-noncommit`, while C2 tests `tag_to_blob` and `tag_to_tree` separately.
  - C1 names no nested class; C2's `nested_tag_to_commit` falls under C1 `tag-to-commit` only if that row explicitly covers recursive peeling.
  - C1 has a `blob` row, but C2 has no blob case (old `noncommit_blob` covers it).
- **O6. C3's 64 manifest rows bind only six distinct source digests.**
  - `reviews.json` contains 64 rows (6 lead seats, 36 oracles, 13 Debt rows, 9 review/critic rows).
  - The distinct sources are QUALITY, `_revision.py`, `check-revision-binding.py`, `check-seat-scope.py`, PROVINCE and the round-20 lesson. 36 of the rows pin `_revision.py` alone.
  - The 13 `Debt*` rows carry predicates of the form `round20-missing-report-*` against the round-20 lesson snapshot.
  - The SKILL.md snapshot is pinned in `preregister.json:66-69`, but no review row uses it.
- **O7. C3 is satisfied by construction.** Every seat prompt dictates the exact `Reviewed-SHA256:`, `Predicate:` and `Scope:` lines. Passing therefore proves the report carries the lines and the committed source bytes match the digest. As the preregister limit already says, it does not prove reading or nonexecution (`preregister.json:42`).
- **O8. Unpinned lead, not used for any verdict.** The live (mutable) `corpus/SOURCES.md:84,89` lists S077 and S082 with the same URL, `git-scm.com/docs/git-rev-parse/2.56.0`, under different scope strings. `scripts/sources-census.sh:644-645` emits W04 for the same URL across scopes, which is a warning, not an E04 failure.
  - The start census has eight W04 warnings (`census-start.txt:3-10`). The end census can be expected to show nine [INFERENCE].
  - I have no digest for this file, so it is a lead only (QUALITY38).

## 3. Separability tests

| Pair | Shared cause | Verdict |
|---|---|---|
| C1 ↔ C2 | The same five-class outcome map: tree, blob and tag-to-noncommit refuse with E-REVISION-INVALID; commit and tag-to-commit are accepted if landed and pushed | **Coupled by common mode.** A single planner error, such as accepting tag-to-tree, would flip C1's hard-coded map and C2's expectations together. Separability holds only if the C2 judge never reads `selector-contract-r21.json` and the C1 gate never executes Git. |
| C2 ↔ oracles | Oracle predicates derive "expected-source-only … from pinned shared binder" (`build/spec.json` Oracle items) | **Contradiction with QUALITY36/41.** Expected outputs must not import the binder under judgment. Reading `_revision.py` is valid only to confirm argument propagation. The expected decision must come from the Git type invariant (S081 `^{commit}` recursive dereference) plus lane policy QUALITY27/36, not from the binder's own control flow. |
| C2 ↔ C3 | The 36 oracle reports are C3 rows | **Separable.** C3 grades bytes and declared lines, while C2 grades consumer exit and finding. A dead oracle turns C3 red without changing C2. |
| C1 ↔ C3 | ScribeDecision and ExecDecision are C3 rows | **Separable**, for the same reason. |
| C1 internal | Each row mixes a Git-source proposition with lane policy | **Partially sourced.** S081/S082 support typed peeling and type verification. Landed/pushed acceptance and object-before-ref identity are lane policy (QUALITY27, QUALITY36), not Git documentation. Per QUALITY2 and QUALITY19, each row's rationale must cite both, or the policy half is unsourced. |

## 4. Proposed move: separate capability change from coverage change, all measured with the final evaluator

This is one bounded proposal: a compatible synthesis across the three claims. It changes no preregistered metric. It adds disclosure fields that L1 reports alongside each metric.

1. **C1 (depth).** Run the final `check-selector-contract.py` at baseline 82e5192 (expected exit 1, SELECTOR-CONTRACT-MISSING, `decision_rows` 0) and at the landed commit (expected exit 0, 5/5).
   - Report this as "selector contract absent→present, 5/5 required rows, each citing S081 or S082 plus QUALITY27/36". Do not report it as five units of depth.
   - The depth ordinal stays 8.
   - Add a crosswalk in the knowledge Markdown, not as extra rows:
     - `tag-to-commit` covers one or more tag levels, which is where C2 `nested_tag_to_commit` maps;
     - `tag-to-noncommit` covers both C2 `tag_to_blob` and `tag_to_tree`.
2. **C2 (operability).** Have the same final evaluator emit per-case behavior cells at baseline even when the coverage gate reports `target_type_tools` 0.
   - Disclose that baseline behavior cells pass [INFERENCE until measured]. If any cell fails at baseline, that is a real gap and is reported as one.
   - State the actual coverage delta as one new opt-in judge mode plus 36 new consumer cells (4 types × 9 consumers).
   - Label `annotated_tag_to_commit` as overlapping round-20 `annotated_tag_object` and do not count it as new.
   - At the landed commit, rerun the old `--object-selectors` and require it to stay at 9/9 with an unchanged case set.
   - The headline "0→9" may stand only with the sentence: "0 reflects absent coverage mode; no consumer or binder bytes changed."
3. **C3 (calibration).** Report `pinned_reviews` / `total_reviews` together with the count of distinct source digests (6) and a per-source breakdown, so 64 receipts are not read as 64 independent sources.
   - L1 additionally checks that each snapshot's bytes equal `git show 82e519203e676c532b1dc5ea91a85671f2286e7b:<baseline path>`. Without that check, reviews bind a copy, not the baseline.
   - The 13 Debt rows must not be counted as discharging round-20's 13 missing build reports, which stay red (`preregister.json:42`; round-20 lesson §Final measured outcome).

## 5. Count-inflation rejections

| Proposed count | Rejected because |
|---|---|
| C2 "9 tools gained target-type capability" | No consumer or binder bytes change (O1, O3). The gain is coverage, not behavior. |
| C2 "45 new cells" | 9 of those 45 duplicate round-20 `annotated_tag_object` (O2). |
| C1 "5 depth units" | The count is fixed by the schema and is one presence fact (O4). |
| C3 "64 independent pinned sources" | Only 6 distinct digests are pinned (O6). |
| An ordinal bump on any axis | `ordinal_deltas: 0` is preregistered. |

## 6. Risks and second-order effects

- **Common mode across C1 and C2:** a shared map error goes unseen unless the C2 judge's expectations come from Git fixture types plus QUALITY27/36 independently of the C1 JSON.
- **Oracle independence:** if oracle reports justify expected outcomes by quoting `_revision.py` branches, they cannot detect a binder defect. They predict baseline behavior; they do not establish semantic correctness (QUALITY41).
- **Census:** the end census can be expected to show one extra W04 for S082/S077 [INFERENCE, O8]. Disclose it; do not file it as a regression or hide it.
- **The presence gate looks like a regression mask:** a reader of "before 0" may infer that consumers failed at baseline. QUALITY17 says a structural counter does not license behavioral prose.

## 7. Checks for L1 after integration (I did not run any)

- `python3 tools/check-selector-contract.py --revision 82e519203e676c532b1dc5ea91a85671f2286e7b` and `--revision <LANDED>`, plus its `--selftest`.
- `python3 tools/check-revision-binding.py --tools-revision <BASELINE|LANDED> --object-target-types`, with per-case cells shown at baseline.
- `python3 tools/check-revision-binding.py --tools-revision <LANDED> --object-selectors`, which must stay 9/9 with the same case set.
- `python3 tools/check-review-snapshots.py --revision <LANDED> --manifest .ufo/waves/round-21/reviews.json`, plus a byte comparison of each snapshot against the baseline commit.
- `python3 tools/_revision.py --selftest`, which must keep its round-20 count.
- An end-of-round census, comparing W04 lines with `census-start.txt`.

## 8. Limits

- Every claim about behavior is an inference from source; nothing was executed.
- I did not recompute any digest.
- I did not read the ExecDecision or ExecMatrix drafts; they are moving candidates and out of the pinned scope.
- O8 is an unpinned live-file lead.
- This is not non-author closure or outside promotion.
- No tool was installed or needed.

Scope: executed=none
