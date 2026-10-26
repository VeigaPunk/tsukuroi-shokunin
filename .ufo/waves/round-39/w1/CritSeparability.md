VERDICT: supports

# R-2 causal separability — CritSeparability (round 39, hyaku run 8)

Claim under attack: SCORECARD.md:2236-2239 "Causal separability: C1 touches `tools/tsukuroi-census.sh` … C2 touches
a new knowledge entry and `corpus/SOURCES.md`; neither counter reads the other's surface", and the item's demand that
each claim pass with the other absent and fail without its own commit.

## Method (receipts: `.ufo/waves/round-39/w1/CritSeparability/`, `SHA256SUMS.txt`, `provenance.txt`)

Three scratch clones of the lane (`git clone -q --shared`, `git remote remove origin`, local fixture identity
`CritSeparability fixture <critsep@fixture.invalid>`, `rev-parse --show-toplevel` == clone path before the first
commit). Frozen counters run from the **lane's** `tools/` copies, shas re-verified against the declaration:

```
75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973  tools/score-storage-hidden-r39.py
f1c97836abb50887231b82d27cd026d05b8083cefcdd713217071648b07c991e  tools/check-transaction-order-r39.py
```

| tree | contents | commit | tree object |
|---|---|---|---|
| d0 | declaration only | `93fddb2c37aed8227b4a0ff2417b104e01446a9d` | `2a21b1ca9d1a2b454de1e5880de8bff65ab15d4c` |
| c1only | d0 + cherry-pick `49cc53c` (rc=0, no conflict) | `9efcfb09b6a76ef1fc39c1cbdac071d15df80713` | `3f552720918c072b93da0a9e210a8f19dd67e13d` |
| c2only | d0 + cherry-pick `4078eb2` (rc=0, no conflict) | `162e4f22d646190b6cf588a4ae720d25cb74d17b` | `3b26610f25342ee5a687fe3b12ddb50767cddadd` |

Pick fidelity: `c1only`'s tree is **bit-identical** to the upstream commit (`git rev-parse 49cc53c^{tree}` ==
`3f55272…`), so C1's commit is graded exactly as landed. `4078eb2`'s tree also contains C1 (it is a child of
`49cc53c`), so `c2only` is checked per path instead: `git -C c2only diff 4078eb2 HEAD -- corpus/SOURCES.md
corpus/knowledge/pacman-transaction-order-r39.md` is empty, and `git rev-parse HEAD:tools/tsukuroi-census.sh` =
`8ef604c0…` = the declaration blob (C2's commit does not touch the census).

Commands (TMPDIR inside scratch; `--repo <tree> --revision <tree-HEAD> --branch master`):
`tools/score-storage-hidden-r39.py --scratch <scratch>/s`, `tools/check-transaction-order-r39.py`,
`tools/score-storage-arm-r38.py`, `tools/score-storage-arm-r38-q82.py`, `tools/check-knowledge-header.py --lane`,
`bash tools/tsukuroi-census.sh --selftest`.

## The four results

| tree | C1 counter (predicate `hidden==2 and views==3 and fixtures==5 and live==1 and six==1`) | C2 counter (predicate `rules==8 and dup_rows==0 and dup_heads==0 and source_ok==1 and counts_ok==2 and oracle==0`) |
|---|---|---|
| **c1only** (C2 absent) | **PASS** exit 0 — `hidden_matched 2, views_matched 3, fixtures_matched 5, live_match 1, six_planes_all 1` (`c1only-c1.json`; seed `cb5e30e6…`) | **FAIL** exit 1 — `entry_present false, rules_verified 0, source_ok 0, counts_ok 0` (`c1only-c2.json`) |
| **c2only** (C1 absent) | **FAIL** exit 1 — `hidden_matched 0, views_matched 3, fixtures_matched 2, live_match 1, six_planes_all 1` (`c2only-c1.json`; seed `634bad8f…`) | **PASS** exit 0 — `rules_verified 8, duplicate_rows 0, duplicate_headings 0, source_ok 1, counts_ok 2, oracle_violations 0` (`c2only-c2.json`) |
| d0 (neither) | FAIL exit 1 — `0 / 3 / 2 / 1 / 1` (`d0-c1.json`) | FAIL exit 1 — `entry_present false, rules 0, source 0, counts 0` (`d0-c2.json`) |

Both directions hold: each claim passes with the other's commit absent and fails without its own.

Direction evidence, C1-without-C2 (`c1only-c1.json`): both hidden legs return exactly
`STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs`
(H1-hidden-empty, H2-hidden-absent) and all five fixtures match, including `F2-absent-root-btrfs-mounted`,
`F3-absent-root-mounts-unreadable`, `F5-empty-root-btrfs-mounted`.

Direction evidence, C2-without-C1 (`c2only-c1.json`): both hidden legs read
`STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0` and the failing fixtures are exactly
`F2`, `F3`, `F5` (passing: `F1`, `F4`). That is byte-for-byte the declared base behaviour
(`.ufo/waves/round-39/before/c1-before.jsonl:8-11` and its per-leg blocks) — as expected, because the census blob at
base `0eff65b` and at declaration `93fddb2` is the same object `8ef604c0…`, so the c2only run is a fresh
reproduction of the before receipt two commits later.

Cross-surface independence as designed (`SCORECARD.md:2236-2239`): `grep -n "corpus\|SOURCES\|transaction"
tools/score-storage-hidden-r39.py` → no match; `grep -n "census\|tsukuroi-census\|sys/fs/btrfs"
tools/check-transaction-order-r39.py` → no match. The C1 counter reads only `tools/tsukuroi-census.sh`
(`score-storage-hidden-r39.py:53`); the C2 counter reads `corpus/SOURCES.md` + the new entry via `git show`
(`check-transaction-order-r39.py:51,53`) plus its frozen oracle.

## Regression probes (nothing undeclared found)

- **Round-38 v1 counter** (`score-storage-arm-r38.py`): d0 **PASS 10/10**, c2only **PASS 10/10**, c1only
  **FAIL 9/10** — the single failure is `F06-no-btrfs-root`, got `BLOCKED … detail=mounts:btrfs-without-sysfs` where
  the counter expects `HEALTHY 0/0/0`. This is *pre-declared*: SCORECARD.md:2232-2234 says exactly "at post-C1
  revisions it reads BLOCKED and `score-storage-arm-r38.py` FAILs 9/10 by construction; the round-38 claim stays
  measured at `b0005ae9`". Mechanism: `tools/score-storage-arm-r38.py:82` pins `F06` absent-root to `HEALTHY 0/0/0`
  and the counter never sets `TSUKUROI_PROC_MOUNTS` (`grep -c TSUKUROI_PROC_MOUNTS tools/score-storage-arm-r38.py`
  = 0), while the new census arm reads `${TSUKUROI_PROC_MOUNTS:-/proc/self/mounts}`
  (census at c1only, blob `e3ff0be…` = `tools/tsukuroi-census.sh:460` in the lane)
  and blocks on the host's btrfs root mount. Declared tradeoff, measured, not silent —
  a peer seat's uncommitted working-tree append to `SKILL.md` ("Storage integrity arm — round 39", observed during
  this seat) documents the same F06 consequence.
- **Round-38 Q82 conjunct** (`score-storage-arm-r38-q82.py`, the production-path counter): d0 **PASS**
  (`ns_views_matched 3, ns_available 1`), c1only **PASS** (3/3). The round-38 gate that mattered is intact.
- **Knowledge header gate**: d0 `clean_count 59, finding_count 0`; c2only `clean_count 60, finding_count 0` — the new
  entry conforms, no gate red.
- **Census selftest without C2** (`bash tools/tsukuroi-census.sh --selftest` in the c1only worktree, TMPDIR/HOME in
  scratch): `TSUKUROI_CENSUS_SELFTEST: PASS (117 cases, 117 passed, 0 failed)`, rc 0 — C1's commit is self-contained.

## Calibration notes (what the four results do and do not prove)

1. The author's after receipt for C1 was taken with C2 already landed: `.ufo/waves/round-39/after/c1-after-49cc53c.jsonl:5`
   records `"branch_tip": "4078eb236c7c67f343c76956c587d0a356e0bf5c"`. That receipt alone cannot show C1 passes
   without C2; the c1only run above does, on a tree bit-identical to `49cc53c`.
2. **Saturation of the C1 predicate.** Three of five conjuncts already hold at base: `views_matched 3`,
   `live_match 1`, `six_planes_all 1` in the before receipt (`.ufo/waves/round-39/before/c1-before.jsonl:9-12`).
   Only `hidden` (0→2) and `fixtures` (2→5) move. The declaration prints the before column, so this is not hidden —
   but 3 of 5 terms carry no evidence of the change. The pre-seat controls do cover the discriminating space
   (`controls/controls.jsonl`: K1 fixture-gated `hidden 0, fixtures 5`, K2 over-block `hidden 2, fixtures 4`,
   K3 mountinfo-keyed `hidden 2, fixtures 2` — all FAIL; K4 candidate `hidden 2, fixtures 5` PASS), so I do not read
   this as a defect.
3. **C2's `counts_ok` is tree-independent**: it compares the entry's cells with host counts read from the frozen
   `frozen/txcapture/pacman.log` (`check-transaction-order-r39.py:102` reads `CAP_DIR / 'pacman.log'`; `host_counts()` at `:105`), identical in every tree; only
   `entry_present`/`rules_verified`/`source_ok` discriminate.
4. **C2's oracle is lane-anchored, not tree-anchored**: `TOOL_ROOT = Path(__file__).resolve().parent.parent`,
   `SRC_DIR`/`CAP_DIR` under it (`tools/check-transaction-order-r39.py:55-57`). A variant tree's own
   `.ufo/waves/round-39/frozen/src` is never graded. Harmless for these trees (neither claim touches it), but the C2
   verdict is not a pure function of the tree under test — relevant to any future seat that mutates frozen inputs.
5. **Not run (so not evidence):** `tools/check-adjacency-anchors.py` for C1's IN-109 repin
   (`corpus/knowledge/adjacency-anchors-r19.json`, `found_line 2425 → 2447`, commit `49cc53c`). No round-39 counter
   references the anchor registry (no hit in `score-storage-hidden-r39.py`), so that part of C1's commit is unguarded
   by both frozen counters; grading it is outside R-2 and outside my leaf bounds (the checker walks sibling repos).
   I also did not build mutants — the discriminating space is the controls' job.

## Impacted axes

Operability (C1) and depth (C2): no harm — both claims are causally separable as declared. Adjacency is touched only
by the one-line IN-109 `found_line` repin inside C1's commit, which item 5 above leaves unverified by me.

## Smallest safe correction

None required for R-2. If the outcome section wants measurement rather than design intent behind
`SCORECARD.md:2236-2239`, append one sentence (optional, no claim changes):

> Separability measured (`w1/CritSeparability.md`, scratch clone at `93fddb2`): declaration + C1 only → C1 counter
> PASS (2/3/5/1/1), C2 counter FAIL (entry absent); declaration + C2 only → C2 counter PASS (8/0/0/1/2/0), C1 counter
> FAIL (hidden 0/2, fixtures 2/5); declaration only → both FAIL; the round-38 F06 9/10 side effect reproduced as
> declared.
