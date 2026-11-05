# Round 83 — `## Mistakes` draft (input to corpus/lessons/round-83.md; not a lane file)

Seat: ScribeMistakes. Pointers verified by read or grep at drafting time against the lane root
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Paths are relative to that root. Nothing is UNRESOLVED.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| **R83-CHRONOLOGY** — instrument selftest iterations and the controls receipts ran before the round-83 declaration commit (the controls file says its runs were made at tip `a8598038` and the declaration names that tip as the pre-round tip) | `SCORECARD.md:7086` (`## Round 83 — declaration`) and its chronology paragraph starting `SCORECARD.md:7088` ("Chronology, stated plainly: the round-83 instruments … were written and run by the L1 before this declaration"); `.ufo/waves/round-83/before/controls.txt:1-5` (header: tip `a8598038…`, date `2026-11-05T04:54:45-03:00`, "round-83 freeze candidates in the working tree"), `controls.txt:7-47` (all C1/C2/C3 blocks) | none | The freeze commit `d78b3b3982b5df62286dd65b0a42ae8a91847608` pins the bytes (`.ufo/waves/round-83/before/instrument-sha256.txt`, `SHA256SUMS`). Disclosed, not repaired retroactively. Wave seats re-measure against the freeze. |
| **R82-V2** — global retirement in the round-82 ordinal counter: `if key[0] == round_no or True:` lets a retirement in one round retire assertions of every round. The round-82 selftest (8 cases) has no case where a correction is followed by a later re-assertion, so it stays green | `tools/check-scorecard-ordinals.py:102` (the defect line); selftest cases `tools/check-scorecard-ordinals.py:122-177` (contradiction, named-correction, silent-correction, single-block, two-axes, no-blocks, hyphenated-name, ascii-arrow; 8/8 green at drafting); red-before `.ufo/waves/round-83/before/controls.txt:33-36` ("C3 red-before A": r82 counter over `ordinals-fixture-late-contradiction.md` prints `finding: clean`, rc 0); fixed counter after `controls.txt:40-45` (rc 1, one finding for round 81 depth, ordinals 8 and 9) | none | `tools/check-ordinals-r83.py` positional retirement: a block retires only assertions made earlier in the file. Quoted prose is not an assertion. |
| **R82-V5** — the r82 anchor counter never reads the entry's declared `snapshot_sha256`, so a doctored snapshot is accepted as met | `tools/check-anchor-coordinates.py:110` (`def load`); grep for `snapshot_sha256` or `digest` in that file returns no match at drafting; red-before `.ufo/waves/round-83/before/controls.txt:20-22` ("C2 red-before": r82 counter over `anchor-fixture-doctored` prints `rc=0 … 'count': 8, 'finding': 'met'`) | none | `bind_digest` in `tools/check-anchor-coordinates-r83.py`: the doctored snapshot returns cannot-evaluate (rc 2, `controls.txt:23-26`); the digest-consistent fixture returns 8/8 (`controls.txt:27-29`). |
| **R82-V1** — recipe encoding: `C16-empty-manifest` and `M06-mutation-unlink-noop` store a two-character backslash-n in `old`, so `source.count(old) == 0` at every revision and the mutants cannot be built | `.ufo/waves/round-82/before/mutants-r82.json:123` (C16 id) and `:126` (`old` with `\\n`); `:187` (M06 id) and `:190` (`old` with `\\n`); `.ufo/waves/round-83/before/controls.txt:15-19` ("C1 red-before": recipe-missing on both ids) | none | Re-encoded recipe file `.ufo/waves/round-83/before/mutants-r83.json` (sha256 `499c594b…4f09`, per `SHA256SUMS`). Shown: `.ufo/waves/round-83/before/do-nothing-reencoded-mutation-r83-at-tip.json` reaches `killed 24/26, genuine 17/17, met` with zero tool edits, so the frozen target was an encoding defect. Not credited as operability. |
| **R82-V3** — `--revision` cannot-evaluate in the r82 ordinal counter leaks a traceback with rc 1 (the findings code) when SCORECARD.md is absent at the revision | `tools/check-scorecard-ordinals.py:204-206` (`raise CannotEvaluate(f"absent-at-revision:…")` inside a `try` whose handler catches only `_revision.RevisionError`); `.ufo/waves/round-83/before/controls.txt:50-52` (absent-SCORECARD control: `rc=1 stdout-empty … CannotEvaluate: absent-at-revision:SCORECARD.md (traceback; R82-V3)`) | none | `read_scorecard_at` in `tools/check-ordinals-r83.py:222-229` returns cannot-evaluate as JSON with rc 2 (`controls.txt:53`). |
| **R82-V7** — S333's `used-by` cell names two knowledge files that do not cite S333; the census does not check used-by reverse references | `corpus/SOURCES.md:344` (S333 row, used-by cell, 11 columns); `corpus/knowledge/mount-unit-fstab-plane-r81.md:3` (`source: S331 …; S332 …`, no S333); `corpus/knowledge/mount-unit-fstab-plane-r81.json:13,22,36,45,54,68,82,91` (per-row `source: S331`); `grep -n 'used-by\|used_by' scripts/sources-census.sh tools/check-knowledge-refs-r68.py` returns no match; `corpus/lessons/round-82-verifier-spotcheck.md:187-193` (R82-V7 finding) | census passes (no rule checks used-by reverse references) | Append-only used-by correction (draft cell text below). |
| **seat-harm / provider event** — none observed at drafting. The round-83 wave has written no results: `.ufo/waves/round-83/` lists no `w1-results.json`, and `.ufo/waves/round-83/w1/` holds only `swarm-registry.json` | `.ufo/waves/round-83/` directory listing at drafting | n/a | n/a |

## R82-V7 — draft cell text for `corpus/SOURCES.md:344`, S333 row, `used-by` cell

Old (verbatim, the cell between the 10th and 11th pipes):

```
 corpus/knowledge/mount-unit-fstab-plane-r81.md, corpus/knowledge/mount-unit-fstab-plane-r81.json 
```

New:

```
 corpus/lessons/round-82.md 
```

Rationale: the one path that cites S333 is `corpus/lessons/round-82.md` (lines 20-21 and 32-37). The knowledge entry cites S331 and S332 by design; its `source:` and per-row `source` fields are not edited by this correction. The alternative in the spotcheck (cite S333 inside the knowledge entry) would change knowledge-entry provenance and is not drafted here. The L1 decides which of the two lands.
