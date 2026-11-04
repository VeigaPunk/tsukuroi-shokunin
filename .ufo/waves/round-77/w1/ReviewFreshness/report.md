# ReviewFreshness — final adversarial review

## Recommendation and findings

**No actionable factual contradiction found in the three frozen C2 repairs.** Each is a real, source-checkable correction rather than a contentless marker. Recommendation only: their substantive content holds; this is not admission, production integration, an outside round-77 closure, or a claim that the current working tree is committed.

Axes: **depth (8, lowest tied)** and **freshness (9)**. No ordinal uplift, saturation, runtime/routing certification, or promotion claim is made. L1 remains the integration owner.

## Scope and evidence

Read the round-77 declaration through `git show eb4bedb92da4d0d2ea2808d4e9e6ad7c9d429be5:SCORECARD.md` (exit 0), frozen `before/expected.json`, counter, round-76 lesson, external round-76 spot-check, and the pinned `journald-manager.c:143–186` / `macro.h:320–350` ranges. `read xd://lsp` returned **No such tool**; references, definition and diagnostics were unavailable. Source/text inspection below is not semantic-LSP proof.

Actual changed behavior was inspected with:

`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff 06f1bbbb803790b35358d277bb7807b82a9fab99 -- /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-76.md`

Exit 0: append-only correction section containing all three exact repairs, followed by two explicit reject rows and an outside-result paragraph. Original historical prose is retained. At inspection, the repairs occupy lesson lines 181, 183 and 185; the supplementary table is lines 189–192 and qualification lines 194–197. Direct full-string membership finds **3/3** in the working tree, not a committed-revision gate result.

`git diff eb4bedb92da4d0d2ea2808d4e9e6ad7c9d429be5 -- <absolute counter path> <absolute expected.json path>` exited 0 with no output. Byte comparisons using `git show <declaration>:<path>` also match current bytes:

- Counter SHA-256 `e686baf3a7b489f2b55c6fdd61b68600562e0adc6f595f892bf62c5d700b2878`.
- Expected SHA-256 `1469154cf9ce2b3c8bcaf6d8ee6698cca912c8ba8ea7e21452b47a5d31fa8694`.

No predicate, instrument or expected data was changed by this seat.

## Repair-by-repair adversarial result

### R77-GATE-SHAPE — substantive, accurately scoped

The original lesson's Search log at lines 35–36 says four candidates, four included, “rejected none this round”; its Gate lines 18–23 has admits only. The repair explicitly supersedes that phrase **as a description of the whole round**, rather than falsely asserting an upstream snapshot itself was rejected. It names a rejected proposition, its falsifier, and a concrete flip condition.

Pinned manager lines 168–171 use `LESS_BY(free, keep_free)`, then `CLAMP(used + avail, min_use, max_use)`, then `LESS_BY(limit, used)`. Macro lines 320–325 define saturated subtraction, not minimum. External `corpus/lessons/round-76-verifier-spotcheck.md:112–127` agrees with the actual rejections but explicitly disagrees with the missing reject-row shape. Its lines 158–165 route that defect. Thus the repair's reference to section 3 is accurate, not a fabricated endorsement of the original Gate.

The actual diff additionally supplies explicit reject rows and an outside-result paragraph. Its final paragraph correctly refuses retroactive admission of round-76 C1. “Outside round-77 spot-check is pending” does not impersonate this author-side wave review or the historical external round-76 check. No outside round-77 closure was observed or claimed here.

### R77-GATE-COUNT — real historical correction

Lesson line 25 retains the wrong “317 → 322” figure. The repair identifies the **round-76 measured revision** `780bad66cd0d62a58153bad541531ebc4f349c4e`, not today's changing tree, and names the omitted S323.

Independent `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 780bad66cd0d62a58153bad541531ebc4f349c4e:corpus/SOURCES.md` exited 0. Counting row IDs with `^ {0,3}\|\s*(S[0-9]{3,})\s*\|` gives **323 rows / 323 unique IDs; S323 present**. At these bytes, this agrees with the repair's spaces-only counting expression. External spot-check lines 166–169 also names 323 and S323. Its header's later closure tip `1ac36bcf…` is not confused with the lane measurement revision.

### R77-COLLISION-COUNT — fresh base, unchanged quarantine

Lesson lines 41–43 retain “114 of 147”. The repair explicitly supersedes it using the **round-77 base** `06f1bbbb803790b35358d277bb7807b82a9fab99`, not a claim that 114 was the fresh r76 result or that the working tree still has 323 rows after r77 integration.

Independent `git show <base>:corpus/SOURCES.md` exited 0 and gives **323 rows / 323 unique IDs**. Read-only `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md` extraction gives **147 unique staged IDs**, with **124 intersections**. Complete sets exactly equal all three lists in `before/collisions.json`, not merely its headline numbers. External spot-check lines 170–173 independently identifies 114 as stale and 124 as the corrected figure.

The correction retains “Assimilation remains none” and “operator hold is not released.” A fresh intersection count neither authorizes adoption nor resolves id drift.

## Causal separability and do-nothing

Counter `tools/measure-journal-arithmetic-r77.py:36–52` is the canonical counting logic:

- C2 takes its early branch, reads only `corpus/lessons/round-76.md`, and tests membership of the three frozen full strings; it does not read the C1 JSON, source snapshots or registry.
- C1 reads the two pinned snapshots and `corpus/knowledge/journald-space-arithmetic-r77.json`; it never reads the lesson. Its required source labels are S324/S325.
- Both use the instrument's expected.json loaded at lines 104–105. This is shared frozen specification, not a dependency on the other claim's production output. `--revision` changes the target reader, not that specification.

Executed exactly the required base controls, with explicit `TMPDIR=/fast/scratch/hyaku/tsukuroi-r77/ReviewFreshness/` and `PYTHONDONTWRITEBYTECODE=1`:

`python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/measure-journal-arithmetic-r77.py --revision 06f1bbbb803790b35358d277bb7807b82a9fab99 --claim C1`

→ `C1 predicate="six pinned arithmetic vectors match" count=0 met=0 reason=missing:.ufo/waves/round-77/before/src/macro.h`, **exit 1**.

Same command with `--claim C2`:

→ `C2 predicate="three exact corrective blocks exist" count=0 met=0 reason=blocks`, **exit 1**.

**The unchanged base cannot meet either target.** C1's observed failure is missing pre-declaration snapshots, so this run alone does not isolate the missing new JSON as its failure cause. Static reader separation establishes the disjoint production paths; no stronger counterfactual execution claim is made. The supplied controls.json records 16 selftests and other negative controls; this seat read those receipts, did not rerun them, and does not present them as seat-executed checks.

## Exact counter limitations and residual risk

1. **C2 is full-substring presence, not semantic repair proof** (lines 37–40). All strings inside a quoted rejected example, a commented-out block, or surrounded by negation still count. It does not enforce append-only provenance, section placement, an actual Gate table, chronological accuracy, the referenced counts, or the promised pending status. It counts each expected string once regardless of repetitions. The current actual diff and independent source checks address these risks for this candidate; the instrument itself does not.
2. **C1 compares six explicit examples**, in order, with integer field checks; it does not execute the upstream macros. It checks snapshot digests and exact S324/S325 labels but does not read registry definitions, companion prose, source-reading behavior, or validate universal manager semantics. Top-level additional JSON metadata is not prohibited. No claim about overflow, startup-normalized min_use, observed journal state, or deletion/vacuum behavior follows.
3. Frozen expected answers are an intentional answer key. A copier can satisfy the mechanical tests; this is different from an unchanged base satisfying them. C2's three strings have substantive content here because their propositions were independently checked, not because exact matching proves truth.
4. Missing/unreadable target bytes return failure through the canonical reader/main exception path (lines 108–120). The tool reads expected.json from its own current instrument checkout, not the target revision; reuse later requires the same pinned specification. Frozen-byte equality was observed now, not guaranteed for a future execution.
5. Working-tree presence is not committed landing. L1 must run the unchanged canonical C2 checker over its final committed revision and retain the receipt. Non-author round-77 closure and final admission remain outside this seat.

## Receipts, guard compliance and self-evaluation

`receipts.json` beside this report records exact executed argument lists, exits, reduced registry counts, specification digests and complete-set comparisons. Both `git show` count inputs exited 0; frozen-byte reads exited 0. The historical full registry text is deliberately reduced in the receipt, not falsely presented as retained raw stdout. The staged source was read directly, not changed.

No fixture or scratch tree was created, so none remains to delete. TMPDIR was explicit for subprocess checks; these read-only checks do not allocate a fixture. No tool installs, package operations, commits, pushes, delegation, service actions, credential/raw-message reads or production writes occurred. Only this seat evidence directory was written. The conflicting sibling `ReviewFreshness.md` trailer was not written because the explicit sole-write-directory restriction excludes it; this report is the requested acceptance deliverable.

Self-evaluation (not an axis admission): accuracy 4/5 (committed counts checked; final landing not observed), completeness 4/5 (all requested substantive checks covered; external r77 closure intentionally pending), clarity 4/5 (line-specific evidence; necessarily distinguishes three revisions), actionability 4/5 (L1 has canonical final command; cannot admit from working-tree presence), conciseness 4/5 (detailed limitations retained for audit). Mean 4.0. Highest-impact remaining verification is final committed-revision C2 landing, then non-author closure. Would the user agree? Evidence is reproducible and the remaining authority/landing boundaries are explicit.
