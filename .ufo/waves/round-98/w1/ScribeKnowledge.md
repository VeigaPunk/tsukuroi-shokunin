# ScribeKnowledge — round 98, wave w1 (scoped findings)

Seat: scribe (leaf member, no dispatch). Scope: review, and where improvable redraft, the round's
knowledge entry `corpus/knowledge/limine-metadata-assertions-r98.md`.

- **Review (the deliverable):**
  `.ufo/waves/round-98/w1/ScribeKnowledge/limine-metadata-assertions-r98.review.md` — per-claim
  verification (command → observed → matches yes/no), every over-wide sentence with its
  narrowing, the trio check, and a corrected draft of only the sentences that need it.
- **Seat report with commands, raw output and the PASS/FAIL table:**
  `.ufo/waves/round-98/w1/ScribeKnowledge/report.md`
- **Receipts:** `.ufo/waves/round-98/w1/ScribeKnowledge/receipts/` (20 files)

## What this seat measured (own runs, own receipts)

| leg | measured | verdict |
|---|---|---|
| roster | 105 families, unchanged (AST `FAMILY_ROSTER` len on both batteries); member tuples `Z_DIGIT9` / `LEADING_ZERO_VALUES` / `Y_DIGIT9` / `CASES_PER_FAMILY` identical in r97 and r98 | PASS |
| landed gate, 3 runs | `met 105/105`, `failed_families []`, 0 error rows, each named family `[4,0]` | PASS |
| `N07-era-field-lie`, 3 runs | `unmet 103/105`, `failed_families ["LEADING-ZERO-NORMALIZE","REFUSAL-VERSIONS-9DIGIT-Z"]`, 0 error rows, both families `[0,4]` | PASS |
| `N08-echo-norm`, 3 runs | `unmet 104/105`, `failed_families ["LEADING-ZERO-NORMALIZE"]`, 0 error rows | PASS |
| r97 do-nothing battery, 3 runs × landed gate and both bends | `met 105/105`, 0 error rows on all three gates (blind to both bends); byte-identical to the r97 landed battery (`e678c34f…`) | PASS |
| which families set the flags (AST) | r98: `fam_refusal_versions_9digit_z` and `fam_leading_zero_normalize` set `check_echo`+`check_era`; r97: neither does; X and Y set neither in either | PASS |
| byte offsets on the pinned gate | main return `16931` / `17037` (lines 316/318); early-return copies `11230` / `11344` (lines 200/202); `VISIBILITY_ERA_SPLIT` at 7399; `era_b = version >= VISIBILITY_ERA_SPLIT` at 10910; docstring phrase at 4425 | PASS |
| the gate's own JSON | `12.09.4`→echo verbatim/era A; `000000012.9.4`→era A; `12.000000009.000000005`→era B; `000000000.000000000.000000000`→era A; `12.9.999999999`→era B; `0.9.999999999`→era A; `12.9.5`→era B, `12.9.4`→era A; source `flag` for an explicit flag, `probe` for the installed-version probe | PASS |
| the draft's `recheck:` procedure, run verbatim | `families_passed 105/105 verdict met` ×3, `count-runs.py` exit 0, both named families `[4,0]` | PASS |
| corpus gates | knowledge-header 114/114 clean, 0 findings, the entry's keys at column 0; recheck-commands PASS with 0 invocations; `sources-census.sh validate` → `tsukuroi ok`, exit 0 | PASS |
| r97 attack receipts (READ, not re-run) | `attack-1-field.json` and `attack-2.json`: 3 runs each, `met 105/105`, `failed_families []`, 1260 `"error": null` rows | PASS |

## Findings (reported, not edited — the entry and the corpus are the L1's)

1. **PC1's era readings are cited to receipts that cannot carry them.** The battery's case log
   records `got[8]` (echo) and `got[9]` (source) and drops `got[10]` (`visibility_era`), so
   `grep -c 'visibility_era'` is 0 in every `before/dev/c1-*.json`. The era pair is observable only
   from the gate's own JSON. Narrowing drafted.
2. **PC2's pin-consequence sentence is wider than the fixture.** `prompt` follows only from
   `hash_mismatch_panic: no`; with another value the consequence is `panic` in both eras.
   Narrowing drafted.
3. **PC2's member list omits `0.9.999999999`** (era A), a Z-family member the battery sends.
4. **PC3's "the same two lies" conflates two mutants** — the gone r97 attack gates and the r98
   bends; N07's era lie covers every Z/LZ spelling, r97's attack-1 covered the Z tuple.
   Narrowing drafted.
5. **The Limits bullet's N07 trigger is looser than the bend's clause** (`len(p) > 1 and
   p.startswith("0")`; a bare `0` component does not trigger it). Narrowing drafted.
6. **Missing proposition, drafted as a new section PC4:** the battery asserts the **source token**
   as well as the echo (`meta_ok`: `got[8] == c.version and got[9] == "flag"`). A scratch mutant
   that echoes the flag spelling verbatim but labels the source `probe` for the Z/LZ spellings
   reads `unmet 103/105` (two families) on the r98 battery and `met 105/105` on the r97 control —
   the blindness receipt for a third asserted field the entry does not yet cover.
7. **The `source:` row differs between the committed copy and the working tree; the landing commit
   must carry both.** Committed: S393 (whose anchor cell mislabels the early-return byte pair as
   the main return). Working tree: `SOURCES.md` moves S393 to `queued` / `used-by —` and adds S394
   (`mined`, `used-by` naming the entry) as its superseding row; the working-tree draft cites S394
   and its wording matches the measured bytes exactly. Landing the entry with S393 while
   `SOURCES.md` says S393 is `queued` would leave a dangling citation.
8. **No repair needed on the trio's placement.** `own-work:` between `source:` and `verified-at:`
   matches the two sibling entries; both corpus gates are order-insensitive and read clean.
   Flagged so the L1 does not "fix" it and diverge from the siblings.

## Constraints honoured

Only `.ufo/waves/round-98/w1/ScribeKnowledge/` and the scratch root
`/fast/scratch/hyaku/tsukuroi-r98/ScribeKnowledge` were written; the scratch tree was deleted
before the report. No lane file was edited — `tools/`, `SKILL.md`, `corpus/`, `SCORECARD.md`,
`LOG.md`, `.ufo/plans/`, `.ufo/waves/round-98/before/` and `claims.json` are untouched by this seat.
`tools/make-r98-bends.py` and every earlier `make-r*-bends.py` were **not** run: the two bends
used are the frozen copies under `before/controls/bends/`, and the one mutant this seat needed was
re-derived in scratch and diffed against the pinned gate bytes. No git or jj mutation in the lane
repo (read-only `git show` / `rev-parse` / `status` / `diff` only); no tool installed or upgraded;
no subagent dispatched; `sudo` never invoked.

{"seat":"ScribeKnowledge","verdict":"findings","notes":"Review at .ufo/waves/round-98/w1/ScribeKnowledge/limine-metadata-assertions-r98.review.md; report and 20 receipts under the seat dir. RUN: landed gate met 105/105 x3 (0 error rows); N07 unmet 103/105 x3 with failed_families exactly [LEADING-ZERO-NORMALIZE,REFUSAL-VERSIONS-9DIGIT-Z]; N08 unmet 104/105 x3 with failed_families [LEADING-ZERO-NORMALIZE]; r97 do-nothing battery met 105/105 x3 on the landed gate and both bends (blindness); AST shows check_echo+check_era set on the two families in r98 and on neither in r97 (roster 105 both, member tuples identical); grep -abo confirms main-return bytes 16931/17037 and early-return copies 11230/11344; the gate run gives the era per spelling and source flag vs probe; the draft's recheck procedure runs verbatim met 105/105. READ: the r97 attack receipts (met 105/105 x3 each). Six sentences need narrowing (PC1's era citation, PC2's consequence fixture, PC2's member list, PC3's mutant identity, the Limits N07 trigger) and a missing proposition is drafted as PC4 - the battery asserts the source token too, so a mutant echoing verbatim but labelling the source 'probe' reads 103/105 on r98 and met 105/105 on the r97 control. Trio confirmed in both copies; the source row differs (committed S393, working tree S394 superseding S393) and must land with its SOURCES.md. Corpus gates clean: knowledge-header 114/114 0 findings, recheck-commands PASS, sources census tsukuroi ok."}
