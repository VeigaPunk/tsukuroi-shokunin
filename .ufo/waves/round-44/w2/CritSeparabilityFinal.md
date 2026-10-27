VERDICT: supports

# Seat CritSeparabilityFinal (R-6) — final separability at tip 8eee79db, round 44 w2

Re-ran the w1 separability item at the integrated tip (which hardened the census 141 -> 148
selftest cases and narrowed the r44 entry). Fixture: `git clone --shared` of the lane at
`/fast/scratch/hyaku/tsukuroi-r44/CritSeparabilityFinal/fx`, toplevel asserted, fixture-identity
commits, three synthetic revisions on top of base `98020ece`:

- sepA `c085bee118618b779c0258ed7f5dcc338aafa7c0` = base + C2-files only (12 paths: the r44
  entry, r43 head/corrections, SOURCES census, `.ufo/waves/round-44/frozen/` S242–S245;
  diff vs base verified = those 12 files, nothing else).
- sepB `31dda47758957e4252a5c37d9fd073e816942463` = base + `tools/tsukuroi-census.sh` only
  (+222/−1).
- sepC `7d055f6dda469e0e52a9ef8fbeaa107722ef2539` = tip minus census (diff vs tip = the one
  census file, verified by `git diff --name-only`).

Receipts: `.ufo/waves/round-44/w2/CritSeparabilityFinal/` (c1-on-{base,sepA,sepB}.json,
c2-on-<revision>.json ×5).

## C1 counter (`tools/score-scrub-arm-r44.py`, sha256 1409a5fd… verified at tip)

| revision | tree | cases | correct | wired_ok | live_agree | selftest | r44 | verdict |
|---|---|---|---|---|---|---|---|---|
| 98020ece | base | 16 | 0 | 0 | 0 | PASS 132/132 | 0 | FAIL |
| c085bee1 | base + C2-files | 16 | 0 | 0 | 0 | PASS 132/132 | 0 | **FAIL** |
| 31dda477 | base + census | 16 | 16 | 1 | 1 | PASS 148/148 | 16 | **PASS** |
| 8eee79db | tip (receipt `.ufo/waves/round-44/after/c1-after-8eee79db.jsonl`) | 16 | 16 | 1 | 1 | PASS 148 | — | PASS |

sepA fails with the identical signature to a fresh same-host base run: all 16 namespace cases
rc=127 (`probe_scrub_record: command not found`), empty live SCRUB output, selftest 132/132,
r44=0. C2's files have zero effect on C1's counter; the census change alone flips it to PASS.
Declared after-receipt at 8eee79db corroborates PASS at tip.

## C2 counter (`tools/check-scrub-record-r44.py`, sha256 c96aeda9… verified at tip)

| revision | tree | rows | quotes | props | host | sources | pointer | verdicts | verdict |
|---|---|---|---|---|---|---|---|---|---|
| 98020ece | base | 0 | 0 | 0 | 0 | 0 | 0 | 0/3 | FAIL |
| 31dda477 | base + census | 0 | 0 | 0 | 0 | 0 | 0 | 0/3 | **FAIL** |
| c085bee1 | base + C2-files | 3 | 3 | 3 | 3 | 1 | 1 | 0/3 | FAIL (verdicts only) |
| 7d055f6d | tip − census | 3 | 3 | 3 | 3 | 1 | 1 | 0/3 | FAIL (verdicts only) |
| 8eee79db | tip | 3 | 3 | 3 | 3 | 1 | 1 | 0/3 | FAIL (verdicts only) |

sepB is field-identical to base (rows=0, snapshots/capture absent, all sources False): the
census change has zero effect on C2. sepC is field-identical to tip: everything else present,
census absent — C2's lexical/global conjuncts all hold. `verdicts_ok=0` at every revision is
the declared wave-2 binding gap (w2-dispatch/w2-results/seat reports not yet integrated),
not a separability defect. `novelty_base_hits=0` everywhere.

## Read-set proof (code inspection, bounds the generalization)

C1 reads exactly `rev:tools/tsukuroi-census.sh` from `--lane` (git show, one path) — no other
lane file can influence it. C2 reads: the r44 entry, r43 head, `corpus/SOURCES.md`, snapshots
under `.ufo/waves/round-4{2,3,4}/frozen/`, `w{2}-dispatch/results.json`, w2 seat `.md` files —
none of which is the census. Disjoint surfaces; the measured runs confirm it behaviorally.

## `git diff --stat base..tip` + sources census

683 files, +74143/−3: the only non-`.ufo` changes are SCORECARD.md (+43 declaration),
SOURCES.md (+8/−3), r43 (+5), r44 entry (+149), the two counters (+361/+636), census
(+222/−1). The rest are wave artifacts. SOURCES diff = exactly the declared mutation: new
rows S242 (code, v7.2.11, mined, 2026-10-26, used-by r44), S243 (same), S244 (code, 7.1-1),
S245 (own-work, 30d recheck), and used-by appends naming the r44 entry on S237 and S240 —
no other cell touched; counter's `sources_ok=1` confirms all cells pass its parse.

## Kill-rule scan notes (advisory, not re-scored here)

Fresh base live census produced the same rollup line as the receipt's live leg
(`TSUKUROI_CENSUS` line identical shape; SCRUB line absent at base, present at tip —
declared neutral addition between STORAGE and rollup). Predecessor storage counters and
live-mode file writes are covered by C1ExecFinalPrior / C1ExecFinalLiveRead seats; not
re-run here (scoped item).

## Proposed text

None — separability holds at the final tip in both directions; no defect found.
