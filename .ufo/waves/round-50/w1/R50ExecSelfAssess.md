VERDICT: defect-found

Item D-6 — re-derived every SCORECARD-axes-table count at the freeze
(`8029cdba1049df25632c91a23c8db4eefb54be5f`) independently and ran the counter.
Receipts: `.ufo/waves/round-50/w1/R50ExecSelfAssess/{sa-freeze.json,counts-freeze.txt,provenance.txt,ordinal-reference.txt}`.

## 1. Counter result at the freeze

`python3 tools/check-self-assessment.py --revision 8029cdba1049df25632c91a23c8db4eefb54be5f --scratch <scratch>`
→ **checked 27, mismatches 3, status FAIL, exit 1** (`sa-freeze.json`; stderr empty).
`declaring_round 49`, `axes_heading "## Axes — current self-assessment (round 49 final measured surface)"` (SCORECARD.md:3143), `reference_lines 646`.

| id | subject | stated | observed |
|---|---|---|---|
| K10 | depth row corpus/lessons file count | 73 | 74 |
| K13 | operability row census case count | 167 | 168 |
| K17 | host-census-gate row census case count | 167 | 168 |

All other 24 checks match (sa-freeze.json:K01-K09,K11-K12,K14-K16,K18-K27).
Note: the counter FAILs at the freeze revision. The 3 mismatches are real stated-vs-observed
drifts, and round 50's own byte-landing produced two of them (below).

## 2. Independent re-derivation (extracted `git archive 8029cdba` tree; commands in counts-freeze.txt)

- notes `find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l` → **67** (stated 67, K07 match)
- `wc -l < SKILL.md` → **4572** (stated 4572, K08 match)
- `grep -c '^|' SKILL.md` → **1323** table lines (stated 1323, K09 match)
- `find corpus/lessons -type f | wc -l` → **74** (stated 73 → K10 mismatch)
- `wc -l < corpus/README.md` → **500** (stated 500, K11 match)
- census case count, taken from the K13 leg's run of `bash tools/tsukuroi-census.sh --selftest`
  on the frozen archive: `TSUKUROI_CENSUS_SELFTEST: PASS (168 cases, 168 passed, 0 failed)` → **168**
  (stated 167 in the operability cell AND the host-census-gate capability row → K13, K17)
- `--identity` presence: `--identity) identity=1` arm at census blob line 3727 → **present**
  (stated landed, K14 match)
- overlap-table presence: `| ID | Finding` at PROVINCE.md:44 → **present** (stated present, K15 match);
  7 ADJ- rows in that table (sed 44-75 | grep -c '^| ADJ-' = 7)
- PROVINCE Core/Frontier/Adjacent headings present (K12 match); six PLANE emitters at
  census lines 3769-3774 (packages, systemd, drivers, journal, update-safety, oom) + STORAGE
  (verdict-neutral, no PLANE text) — coverage cell's "six census planes plus verdict-neutral STORAGE" verified.

## 3. Ordinals and last-change pointers

K01-K06 all match: scores 8/9/9/9/9/8 equal the after-values of the last eligible
measured-outcome transitions. Independently recomputed the last eligible reference per axis
(ordinal-reference.txt, exact replication of `reference_lines()`): depth 8→8 at `SCORECARD.md:2250`
(Round 39 outcome), coverage 9→9 at :2171 (Round 38), operability 9→9 at :2249 (Round 39),
freshness/calibration/adjacency 9→9/9→9/8→8 at :1560 (Round 35 — rounds 36-49's outcome sections
carry no freshness/calibration/adjacency transition lines, so the reference stays round 35).

"Last change" column values (round 4 / round 11 / round 11 / fleet round 1 / round 10 / fleet round 1)
are unchanged boilerplate since the round-42 table (measured: identical cells at lines 2623-, 2722-,
2823-, 2939-, 3031-, 3151-). They are move-log provenance, not last-transition provenance; the counter
does not check them. No drift observed between the column and the actual score history (my parse of
every `## Axes` table: the only post-round-25 score move is coverage 8→9, freshness 8→9, adjacency 7→8
at the round-25 table; scores were 8/9/9/9/9/8 since round 25).

## 4. Provenance of the three drifts (provenance.txt)

- **K10 (73→74 lessons):** `corpus/lessons/round-49-verifier-spotcheck.md` (231 lines) landed at
  `b866a1d3` — the round-49 verifier spot-check commit, i.e. AFTER the round-49 restatement
  (lessons = 73 at `0ec92fc2` and at the measured `59cc42aa`). Round 49's own ordering (verifier
  lesson committed after the self-assessment restatement) reopened K10; nothing round 50 did caused it.
- **K13/K17 (167→168 cases):** the entire C2 surface — `buf_has`/`out_has` matchers AND the new
  `(R50-C2)` case — landed at `43bcce06` (the FREEZE commit), not in the wave. `buf_has=0, R50-C2=0`
  at base `b866a1d3`; `buf_has=4, R50-C2=4` at `43bcce06`; `buf_has=5` at `8029cdba` (amendment 1's
  pkgline fix). So the freeze census already prints 168 cases and the freeze axes table still says 167
  in both cells — round 50's own change created these two mismatches before any seat ran.
- S256 (the round's one new source row) also landed at `43bcce06`: SOURCES `| S` rows 255 at
  `b866a1d3` → 256 at the freeze. Its `used-by` already names `corpus/lessons/round-50.md`, a file
  absent at the freeze (lessons count includes no round-50 lesson yet).

## 5. Calibration-cell defects worth reporting (not counter-checked)

- The round-49 calibration cell (SCORECARD.md:3155) says "before the restatement 2 (K13 lesson-file
  count 72 = 72, K17 census case count 166 → 167...)": it mislabels K10's subject as K13 and calls
  `72 = 72` a mismatch (impossible for stated==observed). The round-49 measured-outcome paragraph says
  "before the restatement 4 (K08, K11, K14, K15)" — a different set. The only receipted round-49
  measurements are 0 at `0ec92fc2` (c3b-self-assessment.json) and 0 at `59cc42aa`
  (calibration-final.json); no receipt backs either "before" figure.
- The operability cell's `bash tools/boot-chain-audit.sh --selftest` `PASS total=49 failed=0` is not
  a leg of the self-assessment counter and was NOT re-run by this seat (outside the named commands).

## 6. What the round-end restatement must say (cells the round's own changes move)

- **operability cell:** `167` → **`168`** (`bash tools/tsukuroi-census.sh --selftest` prints
  `PASS (168 cases, 168 passed, 0 failed)`); also restate the matcher change (buf_has/out_has,
  R50-C2 case) and the new C2 counter/predicate if the claim passes. `--identity` landed (unchanged).
- **host-census-gate capability row:** `167` → **`168`** (K17 reads the same number); refresh the
  evidence pointer from the round-49 receipts to the round-50 ones.
- **depth cell:** `corpus/lessons/` `73` → **`75`** — NOT 74: the 74th file is already uncounted at the
  freeze, and the round-50 lesson adds one more (S256's used-by already names it). If a round-50
  verifier lesson lands after the restatement, K10 reopens again — restate lessons AFTER every lesson
  file (incl. the non-author verifier's) is committed, or the round repeats round 49's drift.
  `SKILL.md` `4572`/`1323` → the post-append `wc -l`/`grep -c '^|'` values (no round-50 marks exist at
  the freeze: `grep -c 'round-50' SKILL.md` = 0). `67 notes` holds unless a new note lands (C1 edits an
  existing note). The GR text must be restated from the round-50 cohort result.
- **coverage cell:** `corpus/README.md` `500` → post-append `wc -l` (README prose/marks are permitted
  post-wave edits; FROZEN.md). PROVINCE sections unchanged.
- **calibration cell:** must state the freeze-time measurement — **27 checks, 3 mismatches (K10, K13,
  K17)** — not round 49's figures, then the round-end re-measurement. Fix the K10-as-K13 mislabel.
- **adjacency cell:** `check-adjacency-table-r49.py` → **`check-adjacency-table-r50.py`** with its
  content legs (`quote_at_pin_ok`, `live_quote_ok`, `stub_fails`) and the amendment-1 IN-109 repin
  `2671→2683`. Overlap table present (unchanged).
- **Ordinal caveat (K01-K06):** the counter excludes the declaring round's own measured outcome
  (reference_lines() drops sections with round ≥ declaring; the selftest's
  `own-round-outcome-depth-10` fixture asserts the mismatch). If C1 admits and the round-50 outcome
  records `depth 8 → 9`, the SAME round's axes table must still state **8** — stating 9 makes K01
  resolve to Round 39's `depth 8 → 8` (:2250) and mismatch. The 9 belongs to round 51's table.
- **freshness cell:** restate to the round-50 re-opens (S256 opened this round) and the round-50
  end-census receipt path.

## 7. Checks I did not run

`check-adjacency-table-r50.py`, `check-scrub-admission-r50.py`, `check-selftest-matcher-r50.py`,
`check-registry-coverage.py`, `boot-chain-audit.sh --selftest` — none are named in this item
(EXEC-AUTHORIZED: `check-self-assessment.py` plus the stated counting commands only).
