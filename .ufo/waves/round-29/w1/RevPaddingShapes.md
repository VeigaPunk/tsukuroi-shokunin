# RevPaddingShapes — round 29, wave 1 (residual reproduction at 81a061a)

Verdict: the round-28 residual finding holds at 81a061a67466c5e1be812814a895a4b5ed89b4ff — the same 15 of the 22 wave-1 CritC1NewShapes should-fail shapes still score anchored_rows 6 with exit 0, in both sibling-verified and sibling-unavailable modes. Seven added round-29 fixtures covering the named residual classes (duplicated anchors, PROVINCE-mirror lane quotes, withdrawn markers, clipped words) are all accepted too: 22 of 29 padding shapes score 6.

Method [obs]: `git clone --no-local` of the lane repo to /fast/scratch/hyaku/tsukuroi-r29/RevPaddingShapes/repo, checkout 81a061a, `git archive 81a061a | tar` export to /fast/scratch/hyaku/tsukuroi-r29/RevPaddingShapes/tree (read-only; no git writes in the lane or fleet repo). The runner (runner.py, sha256 9107edcf…) rebuilds each mutant as a private commit in /fast/scratch/hyaku/tsukuroi-r29/RevPaddingShapes/sbx (`git init`, GIT_* stripped from every subprocess env) and runs `python3 tree/tools/check-adjacency-overlap.py --repo sbx --revision <sha>` once with `--siblings-root /home/vgpnk/Projects/shokunin` (sibling-verified; mori-shokunin present read-only) and once with the empty root /fast/scratch/hyaku/tsukuroi-r29/RevPaddingShapes/nosib. Accepted = exit 0 with anchored_rows 6, matching the wave-1 and residual-report definition. Full JSONL: results-81a061a.jsonl (sha256 7f8fd360…, 30 records + summary).

## Per-shape scores at 81a061a (exit/anchored_rows, identical in both modes)

| # | shape | score | accepted |
|---|---|---|---|
| — | control (unchanged) | 0/6 | yes (sanity) |
| 1 | same-anchor-six-times | 0/6 | **yes** |
| 2 | dot-slash-lane-path-snapshot | 1/5 | no — OV3 lane-path-not-lane-knowledge |
| 3 | dot-slash-lane-path-register | 1/5 | no — OV4 lane-path-not-lane-knowledge |
| 4 | dot-segment-lane-path-register | 1/5 | no — OV4 lane-path-not-lane-knowledge, lane-file-missing |
| 5 | lane-from-counter-source | 0/6 | **yes** |
| 6 | lane-from-province-own-summary | 0/6 | **yes** |
| 7 | lane-from-lessons | 0/6 | **yes** |
| 8 | lane-from-scorecard | 0/6 | **yes** |
| 9 | unrelated-lane-quote-agrees | 0/6 | **yes** |
| 10 | mid-word-fragments | 0/6 | **yes** |
| 11 | generic-four-word-quotes | 0/6 | **yes** |
| 12 | placeholder-actions | 0/6 | **yes** |
| 13 | rows-marked-withdrawn | 0/6 | **yes** |
| 14 | consistent-false-class | 0/6 | **yes** |
| 15 | province-html-comment | 0/6 | **yes** |
| 16 | province-mixed-fence | 1/0 | no — all rows province-row-missing |
| 17 | province-indented-code | 1/0 | no — all rows province-row-missing |
| 18 | province-withdrawn-subsection | 0/6 | **yes** |
| 19 | province-no-delimiter-prose | 0/6 | **yes** |
| 20 | province-pointer-contradicts | 0/6 | **yes** |
| 21 | province-later-row-contradicts | 1/5 | no — OV4 province-row-missing (duplicate id maps to None) |
| 22 | province-shadow-section | 1/0 | no — all rows province-row-missing |

Accepted should-fail wave-1 shapes: 15 of 22 — same-anchor-six-times, lane-from-counter-source, lane-from-province-own-summary, lane-from-lessons, lane-from-scorecard, unrelated-lane-quote-agrees, mid-word-fragments, generic-four-word-quotes, placeholder-actions, rows-marked-withdrawn, consistent-false-class, province-html-comment, province-withdrawn-subsection, province-no-delimiter-prose, province-pointer-contradicts. This list is identical to RevC1Repairs.md finding 5 (.ufo/waves/round-28/residual/RevC1Repairs.md:17) and the refusal reasons match its finding 2 (lines 11).

## Round-29 added fixtures (new classes named in the assignment)

| shape | class | score | accepted |
|---|---|---|---|
| r29-dup-anchor-all-six | duplicated anchors | 0/6 | **yes** |
| r29-dup-anchor-lane-side-only | duplicated anchors (lane side only, distinct sibling anchors) | 0/6 | **yes** |
| r29-mirror-pointer-cell | PROVINCE-mirror lane quote (pointer cell as lane_quote) | 0/6 | **yes** |
| r29-mirror-full-row | PROVINCE-mirror lane quote (full `| OV4 | … |` row as lane_quote) | 0/6 | **yes** |
| r29-withdrawn-top-level-and-prose | withdrawn markers (top-level status/superseded_by/deprecated + PROVINCE withdrawn prose) | 0/6 | **yes** |
| r29-clipped-words-two-rows | clipped words (first/last token edge-clipped on OV5 quote + OV1 lane_quote) | 0/6 | **yes** |
| r29-clipped-words-min-four | clipped words (4-word floor, last word mid-token) | 0/6 | **yes** |

Notes [obs]: r29-mirror-* is the concrete fixture for the round-28 wave-1 probe hole `lane-quote-from-province-register-mirror` (CritC1OverStrict finding 10 second hole; RevC1Repairs.md:23) — B5 excludes `.ufo/` and `corpus/knowledge/adjacency-*` but not PROVINCE.md, so a row can anchor itself against its own PROVINCE mirror line. r29-dup-anchor-all-six keeps OV6's null lane side so it does not trip B6; the refusal mode of the naive version (OV6 gains a lane side → lane-gap-with-lane-side) is avoided deliberately. r29-withdrawn-top-level-and-prose extends rows-marked-withdrawn: a bold "**Withdrawn …**" line inside the section plus top-level register markers still leaves every row counting.

## Findings

1. [obs] The residual claim reproduces byte-exactly in membership: identical 15-mutant accepted set, identical refusal reasons for the 7 refused, control still 6/exit 0 (results-81a061a.jsonl, summary line). The counter at 81a061a is byte-identical to the round-28 repaired counter: sha256 7b58652a7e9aaf85858fa110e0a825da15bc9a91eb45217c1ec313f3f6a9fb7c, last touched in commit 9a0654ba (git log --oneline 81a061a -- tools/check-adjacency-overlap.py). The residual finding was therefore guaranteed to reproduce; it is re-measured, not assumed.
2. [obs] All seven r29 fixtures are accepted in both modes with `reasons: {}` — no row is even flagged, so these are clean holes, not near-misses (results-81a061a.jsonl lines 24-30).
3. [obs] Acceptance is identical in sibling-verified and sibling-unavailable modes for all 29 records: no padding shape depends on the live mori repo.
4. [inf] The unfixed holes cluster in three places: nothing requires distinct anchors or lane sides across rows (duplicated anchors); B5's lane_path exclusion list omits PROVINCE.md, tools/, SCORECARD.md and corpus/lessons/ (self-referential lane sides, mirrors); and no register key or PROVINCE prose conveys "withdrawn" (withdrawn markers). Clipped words survive because matching is a whitespace-normalised raw substring test with no token boundary (counter lines 203-204, 222).
5. [unk] r29-mirror-full-row's lane_quote is 18 words — under the 25-word cap — but it embeds `|` characters; if a future repair strips non-word content before counting, re-run to confirm. All mirror/clip fixtures were generated programmatically from the tree's own PROVINCE.md and register where possible, so the runner stays valid under wave-2 corpus edits.

## Deliverables for wave 2

- `.ufo/waves/round-29/w1/RevPaddingShapes/runner.py` — parameterized: `--tree` (export of the revision under test), `--counter`, `--work`, `--siblings-root`, `--nosib-root`, `--out`. Wave 2 re-run on the repaired counter: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 runner.py --tree <export> --counter <export>/tools/check-adjacency-overlap.py --work <fresh sandbox> --out results-<rev>.jsonl`. Success for the repair: wave1_accepted 0 and r29_added_accepted 0 in the summary line, control still accepted.
- `.ufo/waves/round-29/w1/RevPaddingShapes/results-81a061a.jsonl` — this run's 30 records + summary (baseline for the re-run).

## Residual risk and verification gaps

- The 24 declared round-27 battery shapes were not re-run here (not this seat's scope); this reproduces only the residual wave-1 set plus the new classes.
- Scores were measured on committed sandbox trees via `--repo`; no lane working-tree byte was consulted (counter is read-only by design).

Scope: read=.ufo/waves/round-28/residual/RevC1Repairs.md, .ufo/waves/round-28/w1/CritC1NewShapes{,.md}/driver.py + driver.out, .ufo/waves/round-28/w1/CritC1OverStrict/, tools/check-adjacency-overlap.py at 81a061a (sha256 7b58652a…), SCORECARD.md:1097-1110, PROVINCE.md + corpus/knowledge/adjacency-mori-oom-r27.json in the 81a061a export; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/RevPaddingShapes/{runner.py, results-81a061a.jsonl, RevPaddingShapes.md}, /fast/scratch/hyaku/tsukuroi-r29/RevPaddingShapes/{repo, tree, sbx, nosib}; executed=git clone --no-local + checkout + archive of 81a061a (read-only on the lane), git init/add/commit/checkout -f inside the private sbx only, python3 runner.py (30 mutants × 2 sibling modes), sha256sum, python3 -m py_compile
Model: not exposed
Installs: none
