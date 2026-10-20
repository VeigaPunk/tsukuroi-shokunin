# ConnMistakes — neighbor restatement

Axes: depth (C1), operability (C2), separability, discernment. C3 and ordinals unchanged. Model: Grok 4.7. Installs: none.

## Evidence

Captured-by, reused r13–r17 (`corpus/lessons/round-13.md:30,32`, `round-16.md:27`, `round-17.md:39`), names a green QUALITY beside a wrong neighbor.

C1 [obs] at `842a531`. `boot-chain-r17.md:19` says “13 named packages (B:59, B:82)”; `boot-chain-capture.txt:59` lists 12 names. `:42` cites `B:182, 251` and omits lts init `B:198`. `:45` cites `B:183–184, 252–253` and omits `B:199–200` (`B:190–191`, `B:194` already cited). `:88` pairs mtime `09:26:22` with `B:115` (`09:29:18`); the mtime line is `B:124`. Defect 3 (`round-17-verifier-spotcheck.md:197-200`) leaves verdicts, so QUALITY25 (`QUALITY.md:35`) stays green. QUALITY23 (`QUALITY.md:32`) is wrong-section repair. `round-17.md:42` left number-drift as a QUALITY25 extension with no gate. [unk] No BootChainTruthR17 in the lane.

C2. QUALITY27 (`QUALITY.md:37`) accepts landed hex. [obs] `c2-before-842a531.json`: bound 9, consistent 1, shared 0, regex copies 9. Consistent `check-seat-scope.py` is unshared. D1–D6: `tools/check-revision-binding.py:26-33`.

## Move

Append 28 only. Keep 23, 25, 27. No SCORECARD claim.

28. **Neighbor restatement (R18-NEIGHBOR):** A green probe does not certify an unread restatement. Match the count, quantifier, and timestamp to the cited line; one image’s hashes do not support “both”. Bound (27) does not certify copied predicates: one module implements the contract, and the judge keeps its own binding. Counters stay separate: `check-appended-notices.py` on the statement registry, versus `consistent_tools` / `shared_tools` / `local_rev_regex_copies`. One miss leaves the other claim. Count it only when its own old disagreement fails. Append only.

Class `number-drift / copied-predicate`. Captured-by 23/25/27.

## Risks

A quantifier parser in the notice gate would specialize shared C1/C3 infrastructure (`SCORECARD.md:541`). One combined counter would merge separable claims (`SCORECARD.md:532-538`). Importing `_revision` from the judge contradicts `check-revision-binding.py:9-10`.

## Verification

After landing: `842a531` registry-from flags the three quotes; tip consistent 9/9, shared 9/9, copies 0; only 28 added.

Scope: executed=git rev-parse, git grep, git show, git merge-base --is-ancestor, wc -w (read-only, lane)
