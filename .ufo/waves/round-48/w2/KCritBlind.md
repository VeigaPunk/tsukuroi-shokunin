VERDICT: defect-found

# KCritBlind — item C3-R1 (blind spots of the 27 fixed checks)

Scope read: `git show ae99f021b76f8eb1c8805d32d80644464afb1ff6:SCORECARD.md` (3110 lines), the same rev of
`tools/check-self-assessment.py` (the 27 checks, below), `corpus/lessons/round-4{4,5,6,7}-verifier-spotcheck.md`, and
every cited receipt re-opened at the freeze `ae99f021`. Nothing was edited; commands run are named per finding.

## What the 27 checks can see (boundaries, re-derived from `tools/check-self-assessment.py`)

- K01–K06: only the **score cell** of the six axes rows vs the last `X → Y` ordinal inside a `measured outcome`
  section (`evaluate()` :517–556). Evidence text, verdicts, counts and pointers are not read.
- K07–K11: numeric claims inside the depth/coverage evidence cells (notes, SKILL.md lines, table lines, lesson
  files, README lines) (:591–637).
- K12/K14/K15: exact pres/abs phrases for PROVINCE sections, `--identity` arm, formal overlap table (:639–691).
- K13: the operability row's case count vs a live census `--selftest` run (:656–663).
- K16–K19: existence of backtick-quoted paths in the **four** named capability rows only (sources-registry,
  host-census-gate — plus its case count —, root-metadata-observer, boot-chain-audit) (:693–734).
- K20–K27: path existence and knowledge-note supersession in the four SHONEN boxes (:736–804).

**Never read:** the measured-outcome tables themselves (claim verdicts, per-leg counter values, receipt
provenance), the `storage-error-counter-reader` capability row, planned/retired lists, wrap/correction blocks,
no-harm/kill-rule text, and any path not wrapped in backticks inside the checked cells. The round-46 closure
said the same in one line (`round-46-verifier-spotcheck.md:158` "its fixed checks do not read outcome rows");
the findings below are the current live instances.

## Findings, ranked by 27-check visibility

### Tier 1 — statements the 27 checks DO read (all already declared by C3 as K10/K13/K17; listed for completeness)

| # | SCORECARD (ae99f021) | Contradicting receipt / observed state | Proposed correction |
|---|---|---|---|
| F1 | :3029 `corpus/lessons/` 70 files (depth row) | `git ls-tree -r ae99f021 corpus/lessons | wc -l` → **71**; C3 battery K0/K0b (`controls/battery-summary-r48-c3.jsonl`) reports K10 | already the declared C3 restatement: 70 → 71 |
| F2 | :3031 `PASS (164 cases, 164 passed, 0 failed)` (operability row, "at the round-47 implementation") | I ran the frozen bytes once: `TMPDIR=<scratch> bash census.sh --selftest` → `TSUKUROI_CENSUS_SELFTEST: PASS (166 cases, 166 passed, 0 failed)` (rc 0, ~37 s); C3 battery K0b reports K13 | 164 → 166 in the C3 restatement |
| F3 | :3041 `selftest prints PASS (164 cases, 164 passed, 0 failed)` (host-census-gate row) | same run: 166 cases; K17 flags it | 164 → 166 with F2 |

### Tier 2 — statements committed receipts CONTRADICT, invisible to all 27 checks

| # | SCORECARD line (text) | Contradicting path:line (re-opened at ae99f021) | Proposed correction (one line) |
|---|---|---|---|
| F4 | :3018 C1 verdict cell `**PASS** — kill rules … counters PASS→PASS where measured` | `.ufo/waves/round-46/w1/C1ExecPriorB/score-selftest-literals-r40-2042117c.jsonl` tail `"result": "PASS"` vs `…-a4477049.jsonl` tail `"result": "FAIL"` (`selfref` 5→17); the kill clause at :2979 names r40 explicitly; spot-check `round-46-verifier-spotcheck.md:85-91` | mark the cell: `**PASS (author) → not verified** — r40 kill rule fired (receipt C1ExecPriorB a4477049 FAIL); superseded by the round-47 verifier correction` |
| F5 | :3019 C2 After cell `verdicts_ok 2 (GR1, GR3)` | `.ufo/waves/round-46/after/c2-final.jsonl:2` `"verdicts_ok": 1` (only GR3 `row_ok`; GR1 unbound — `w1-results.json` absent until `91601905`, after closure); `round-46-verifier-spotcheck.md:134-135` | `verdicts_ok 1 (GR3)` |
| F6 | :3012 `C2 measured at the outcome commit` | `c2-final.jsonl:1` `"revision": "b2eafc385ed1…"`; the receipt file itself landed at `102cf670`, while the outcome commit `b313963c` already cited it (future pointer, `round-46-verifier-spotcheck.md:156`) | `C2 measured at b2eafc38 (receipt committed at 102cf670, after the outcome commit)` |
| F7 | :3025 intro `Each count is re-derived from the committed lane tree at the round-46 outcome commit` | the table under it now carries round-47 state: lessons 70 (= count at r47 tip `76819197`; 68 at `102cf670`), "164 cases at the round-47 implementation", GR2 `partly`, withdrawn capability — restated by `e1567211`; and is stale again at ae99f021 (71 lessons, 166 cases) | rename to `## Axes — current self-assessment (restated; last full restatement round 47)` or restate to round 48 — the C3 end-statement must fix the heading too, not only the numbers |
| F8 | :3021 `the D12 ceiling is closed` | F4's receipts: the `--identity` claim is unverified under the frozen kill rule (`round-46-verifier-spotcheck.md:108-109` "capability is real … the claim, however, is killed by its own frozen rule") | `the D12 feature is present; the claim is not verified (r40 kill rule; see correction below)` |
| F9 | :3050 `**retired:** none` | :3082 records the `census-identity` admission **withdrawn** (removed from the capabilities table at `c5397574`; row present at `102cf670:3045`) | `**withdrawn (pending re-verification):** census-identity (round-46 verifier correction)` — or note that "retired" means permanent retirements only |
| F10 | :3060 `space-free PASS 162/162` (r47 before state) | the named receipt `before/selftest-space-before.log` is **not committed** (spot-check R47-V2, `round-47-verifier-spotcheck.md:98-100`); `ls .ufo/waves/round-47/before/` at ae99f021 = 3 files; the spaced leg IS receipted (`controls/battery-summary-r47.jsonl` C2-K0 `FAIL (162 cases, 13 passed, 149 failed)`) | `(space-free run expected PASS; its receipt was never committed)` — the spaced leg stands on the battery |
| F11 | :3032 freshness row `Each round record re-ran predecessor pins; round 46 re-fetched S246-S248, S237, S242-S244 …` | no round-47 or round-48 line exists in the current row; round-47 work was receipted (S252 fetch `round-47-verifier-spotcheck.md:76`, digest-pinned snapshots re-verified in `w1/R47CritGR2a.md`) but is unrecorded here | append a round-47/48 freshness line (S252 admitted, snapshot pins re-verified by the counted cohort) |
| F12 | :3031/:3041 `at the round-47 implementation` / `at the current round-47 implementation` | the current implementation is round-48 (`ae99f021` census sha256 `375aa737…`, selftest 166 cases) | drop the round qualifier or name round 48 (folds into the C3 restatement) |

### Tier 3 — statements a committed receipt FAILS TO SUPPORT (no contradicting receipt; weaker)

| # | SCORECARD line | Gap | Proposed correction |
|---|---|---|---|
| F13 | :3046-3049 round-46 **planned** list still labelled `planned (next round)` | items (1)-(2) were taken by round 47 (its declaration :3057) and (1)-(2) again by round 48 (:3097); the list reads as still-open | mark `(1)`/`(2)` `taken by round 47 / re-taken by round 48`; carry `(3)` openly or drop it |
| F14 | :3094-3095 attempt-1 incident numbers (`32-seat w1`, `wrong base 76819197`, `no counter file`, `empty frozen/src`) | the incident dir `.ufo/waves/round-48/w1*` is declared VOID and seats were instructed never to read it as evidence — I did **not** verify these figures (access refused by instruction, not by absence) | none needed if the orchestrator record is the authority; otherwise the L1 re-derives the counts itself |
| F15 | :3034 adjacency row pins `check-adjacency-anchors.py` PASS `at a4477049` | true then, but two repins landed since (`f6bc6d05` 2582→2593, `d7843b3a` 2593→2642); the anchors receipt the row cites is three censuses old (current: `IN-109 found_line 2642` == `tsukuroi-census.sh:2642`, verified) | cite the newest anchor receipt (repin `d7843b3a` lineage) instead of `a4477049` |

## Checked and found supported (no correction needed)

- :3048 `149/160 FAIL` — matches `w1/C1ExecRerunB.md:69` `FAIL (160 cases, 11 passed, 149 failed)` exactly (the
  r47 line `13/162 (149 failed)` :3060 is the *base* run, matching battery C2-K0 `162 cases, 13 passed`). Both
  denominators are correct for their runs.
- :3018 data cell `identity_ok 1 … selftest_r46 8` — matches `l1/c1-61e06740.jsonl` (`identity_ok 1,
  selftest_pass 1, selftest_r46 8`); `l1/c1-impl-a4477049.jsonl` exists and is `identity_ok 1`.
- :3088 wrap status — `w1/R47CritGR2a.md` exists (`ROW GR2 VERDICT: partly`, hash `909830c8…` ≠ frozen
  `e0b391e1…`, so the r47 post-correction bytes are what C2 now scores); `controls/k22-s240-map.txt` prints
  `(False, 'ioctl.c not a pinned snapshot file')`; `before/selftest-space-after.txt` prints `PASS (164 cases, 164
  passed)` rc 0; `w1/C2ExecRerunA.md` verdict `supports`.
- :3098-3100 round-start receipts — `before/sources-census-start.txt` ends `tsukuroi ok …/corpus/SOURCES.md`;
  K0 legs in `battery-summary-r48-c1.jsonl`/`r48-c2.jsonl`/`r48-c3.jsonl` match the declared before-values
  exactly (loc 3, clean 4, ff 1, pass 0, term 0, static 0 / structural 1, quotes 3, verdicts 0, marks 0 / K10).
- :3104-3106 claim cells — counter predicate, blob sha256 `375aa737…2426` (I re-hashed the blob: identical),
  base legs, case labels (`grep -n 'R48-C2' census` → cases at :3526-3554), GR hashes (I ran the frozen counter
  `--section-hash`: `GR1 fe77ac76…, GR2 e0b391e1…, GR3 43430a14…` — `e0b391e1` ≠ the r47 read `909830c8`,
  confirming "GR2 already carries the round-47 correction"), K22 map (`CITE['GR2']` contains `ioctl.c`, S240
  pinned `round-43/frozen/src/ioctl.c`), `D12` (`corpus/knowledge/closeout-r11.md:42` `--identity` is **not
  landed** — the declaration cites it as `closeout-r11.md:42-44` without its directory, a stable bare name).
- :3110 assimilation — `assimilation/collisions` = **53** lines, S200–S252 contiguous, "none appended" consistent.
- :2833-2836 capability rows — every cited receipt path exists at ae99f021 (round-38/39/40/41/43 `after/*.json*`,
  round-12 `resumed/*`, round-17 `l1-capture/*`, `.ufo/evidence/round-1-kaika/*`, PROVINCE `| ID | Finding` table
  :44 and `## Round-44 promotion` :256); `boot-chain-audit` `total=49` is backed by
  `.ufo/waves/round-47/w1/C2ExecKillRules/bootchain-final.txt` `PASS total=49 failed=0`.
- `**retired:** none` at :2813/:2929 — no capability was withdrawn before round 46, so the older rows stand.
- `w1-results.json` (round 46) — first commit `91601905` (after closure): "GR1 unbound because w1-results.json
  was absent" (:3084) is accurate; r47's `w1-results.json` (64 results) landed at `76819197` post-wrap.

## One-line summary for the L1

Six live contradictions sit where the 27 checks structurally cannot look: the r46 outcome cells (F4, F5, F6,
F8), the table provenance line (F7), the retired list (F9); three more statements lack any committed receipt
(F10, F11, F13) and two provenance qualifiers are stale (F12, F15). All are fixable by append-only marks in the
C3 restatement; none requires touching frozen bytes.

Work not done: I did not run `check-self-assessment.py` myself (the frozen C3 battery K0/K0b lines already
report K10/K13/K17 and my selftest run confirmed the 166-case leg); I did not read `.ufo/waves/round-48/w1*`
(void); scratch dir `/fast/scratch/hyaku/tsukuroi-r48/KCritBlind/` removed after this file was written.
