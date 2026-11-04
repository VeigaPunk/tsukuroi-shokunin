# M1Mutation — mutation-test the round's three instruments (round 72, w1)

Scope: source-level mutants of the frozen C1 counter and C3 checker, plus case-removal probes of the C2
`--selftest` draft. Tested bytes are pinned at declaration commit `6b4267…` in a `git clone --shared`
sandbox; the lane tree was never written. Full per-mutant evidence, patch text, fixture inventory and
reproduction: `.ufo/waves/round-72/probes/M1Mutation/score.md`; machine table:
`.ufo/waves/round-72/probes/M1Mutation/mutants.tsv`.

Pinned hashes — C1 `d615c653…06a6`, C3 `df8a59c7…e712`, C2 draft `af46203c…aabb` (uncommitted; 8 table
rows + computed HERMETIC = 9 case lines), C1 battery `5c771378…af30`, C3 battery `9180bc4f…5340`. Baselines under the harness:
C1 battery 11/11 rc 0, C3 battery 5/5 rc 0, C3 green `ROUTED_STALE=0`, C1 control `MD_VERIFIED=6 met=1`.

KEY=C1_MUTANTS=16 C1_KILLED=5 (kind, quote-location, malformed-row, snapshot-reuse, row-count) — 11 survived
the committed battery; 8 survivors are killed by clause-isolated fixtures I built (share, tokens, map-digest,
anchor, contiguity, quote-words, digest-bytes, url-binding). Three survivors are equivalent, not gaps:
quote-pipe is dead code (pipe-in-quote fails `count("|")==7` → malformed), map-url is masked by
source-not-bound, and the `== "own-work"` clause is unreachable because `own-work ∉ KINDS`.
Battery defect: `mutant-duplicate-id` never produces a duplicate id (builder re-numbers MD1…MD6); it is a
reuse-3 fixture. Real duplicate-id/contiguity coverage is absent — `c1-contiguous-drop` survives the battery
and only the new `contiguity` fixture kills it.

KEY=C3_MUTANTS=9 C3_KILLED=2 (re-derivation equality, receipt presence) — 7 survived; each is killed by a
targeted probe (erratum receipt-only/revision-only/anywhere, note-anywhere, five-path, four-figure, and
fresh-summary-None in-process). Real committed bytes: `c3-erratum-anywhere` reads `ROUTED_SCORECARD ok`,
`ROUTED_STALE=2`, because the C3 declaration row itself already names the receipt path and `2b358d2d` — the
`## Round 71 — receipt erratum` block restriction is load-bearing. The checker never reads the receipt's own
`--revision` text: a receipt naming `2959254a` is accepted, and the r71 counter at `2959254a` emits the
identical summary, so the single-revision discipline rests solely on the `RECORD_REVISION` constant.

KEY=C2_BLIND=8/8 declared-case removals silent — `total = len(results)` re-derives itself, so dropping any
row turns the 9-line suite into `SELFTEST: PASS (8 cases, 8 passed, 0 failed)`, including `NO-RECEIPT` (the
only rc-2 case the claim names). The suite does have teeth on behaviour: rc-always-0 → 3 FAIL lines;
superseded-skip/out-of-scope/label-regex disabled → 1 FAIL each.
v2 (`selftest-v2.patch`, af46203c → f22eb94f1ed8…8464, patch rc 0, green 10 case lines): deleting the
`NO-RECEIPT` row or the `HERMETIC` append alone now gives `FAIL (SELFTEST-CASES)` rc 1; deleting the row
**and** its `DECLARED` entry still gives `SELFTEST: PASS (9 cases, 9 passed)` rc 0. Suite completeness is not
self-verifiable, so the closure check must count case lines externally and against the digest-specific N:
`python3 tools/check-selftest-tally.py --selftest | grep -c '^PASS (SELFTEST-'` → 9 at af46203c, 10 at
f22eb94f; never carry one N across the two digests.

Drift observed, not caused by this seat: the lane worktree C3 checker moved `df8a59c7…` → `b17fddfa…` mid-run
(frozen clone bytes tested); the C2 draft moved `e47baa78…` (7 cases, the base E2GateSelftest's report names)
→ `af4620…` (8 cases, fixture writer, stable finding ids) and was stable through my runs. Consequence: C2's
"before rc 2 / 0 case lines" and case inventory must be measured on committed bytes, not this worktree.

No lane/tree writes outside the two scoped artifacts; no git/jj mutation beyond the permitted
`git clone --shared`; no pacman, service or PATH changes. Scratch `/fast/scratch/hyaku/tsukuroi-r72/M1Mutation`
(including the 433 MB clone) is deleted before exit.
