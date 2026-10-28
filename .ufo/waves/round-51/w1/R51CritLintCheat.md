VERDICT: defect-found

# R51CritLintCheat — cheating the C1 lint and counter (item C1-L2)

Scope: attack C1 by building entry texts that the frozen lint (`tools/lint-grounding-r51.py` at 2732ee6c) and the frozen counter (`tools/check-scrub-admission-r51.py` at 2732ee6c) accept while a row still carries a defect a reader would reject. Non-counted w1 seat. No lane file written except this report and `R51CritLintCheat/` receipts. No tools installed.

## Method (all observed)

- Frozen bytes read with `git -C <lane> show 2732ee6c…:<path>`. Entry = `corpus/knowledge/btrfs-scrub-grounding-r45.md` (348 lines). Snapshots S237/S240/S242/S243/S247 extracted to scratch; SOURCES.md pinned from the revision (`cmp` with working tree: identical).
- Baseline: `lint-grounding-r51.py --worktree --lane L --entry-file E0 --sources-file SOURCES` → `lint_ok 3`, `quotes 63`, `gaps_computed 62`, `gap_ok 1`. Counter on the frozen entry with an all-holds cohort built by `.ufo/waves/round-51/controls/battery.py` helpers (`section_hashes`, `build_cohort`, `marks`) → `verdict PASS`, `structural 1, lint 3, quotes 3, verdicts 3, seats 18, marks 3`. The battery's K-pass control is therefore reproduced.
- 18 cheat entries (fixtures listed below) run through the lint (`--worktree --lane L --entry-file F --sources-file SOURCES`) and through the counter (per fixture: section hashes recomputed for the fixture bytes, all-holds cohort, marks appended, `--revision 2732ee6c`, `--no-base-check`).
- Fixtures and every result JSON are in `.ufo/waves/round-51/w1/R51CritLintCheat/` (`fixtures/*.md`, `results-plain.json`, `results-prototype-rules.json`, `prototype-lint-grounding-r51.py`). Scratch removed after copy.

Caveat on the counter runs: the cohort is battery-built fixture text, not real seat reports. A PASS here means the mechanical legs accept the cheat; real seats could still read `partly`. The question tested is whether the lint/quote legs are fooled, and they are.

## Result 1 — the frozen lint and counter accept these cheats

Every row below: `lint_ok 3` from the frozen lint. Counter column = frozen `check-scrub-admission-r51.py` verdict with an all-holds cohort.

| id | cheat (what changes vs frozen E0) | lint_ok | quotes_ok | counter |
|---|---|---|---|---|
| A1 | GR2 prose adds `scrub.c lines 3200 to 3250` (no colon) | 3 | 3 | **PASS** |
| A2 | GR2 prose adds `` `scrub.c`:3200 `` (backticked basename) | 3 | 3 | **PASS** |
| A3 | GR2 prose adds `scrub.c :3200` (space before colon) | 3 | 3 | **PASS** |
| A4 | GR2 prose adds `line 3200 of scrub.c` | 3 | 3 | **PASS** |
| A5 | GR2 prose adds `scrub.c:3200–3250` (en dash); block gains `3200` only | 3 | 3 | **PASS** |
| A6 | GR2 prose adds `scrub.c:3200, 3210` (comma, no colon); block gains `3200` | 3 | 3 | **PASS** |
| A7 | GR2 prose adds `fs/btrfs/volumes.c:6100` (basename not pinned for GR2) | 3 | 3 | **PASS** |
| G1 | GR2 prose adds `scrub.c:1-3337`; `--emit-gaps` regenerates the block (`1-1364, 1386-3139, 3163-3214, 3227-3320`) | 3 | 3 | **PASS** |
| G2 | block gains a first line `- S242 scrub.c: 1-3337` before the true S242 line | 3 | 3 | **PASS** |
| D1 | GR3 stripped of all quotes and all citations (statement only) | 3 | **2** | FAIL (quotes_ok) |
| D2 | GR3 stripped to one quote `**Quote.** \`S237\` scrub.c:281: ""` (blank snapshot line) | 3 | 3 | **PASS** |
| Q3 | all 19 `S242` quotes of GR2 moved to a "Quotes moved from GR2" list after `## Limits` (outside every row) | 3 | 3 | **PASS** |
| Q4 | GR2 gains `**Quote.** \`S237\` scrub.c:1512: "…"` (btrfs-progs line 1512, not the kernel row source) | 3 | 3 | **PASS** |
| Q5a | GR2 quote `dev-replace.c:703` relabelled `:1268` (same text, both inside declared ranges) | 3 | 3 | **PASS** |
| Q5b | GR2 quote `dev-replace.c:1287` relabelled `:1213` (same text, outside declared); block gains 1213 | 3 | 3 | **PASS** |
| Q5c | GR2 quote `scrub.c:3142` (`ret = -EIO;`) relabelled `:1989` (same text, outside declared); block regenerated | 3 | 3 | **PASS** |
| Q6 | 18 of 19 GR2 `S242` quotes lose the backticked label and carry text `"return 0;"` | 3 | 3 | **PASS** |
| Q6b | all GR3 quotes but one lose the label and carry text `"wrong"` | 3 | 3 | **PASS** |

Plain-lint `quote_bad` is 0 in every fixture: the whole-line rule is only applied to labels that match `QUOTE_RE`, and the mislabelled/moved/relabelled lines still equal their (wrong) cited line.

Summary: 17 of 18 cheats PASS the frozen counter; D1 fails only on `quotes_ok`, and the lint itself (`lint_ok 3`) passes D1 too.

## Why each cheat passes (code locations at 2732ee6c)

- `tools/lint-grounding-r51.py:77` `CITE_RE` requires `basename.ext:N` with a literal ASCII `:` and `-` and no spaces. A1–A4 (`lines … to`, backtick before colon, space before colon, `line N of`) never reach `prose_cites`. A5's en dash stops the range at `3200`. A6's `, 3210` is not a continuation because `CONT_RE` (line 78) demands a colon.
- `lint-grounding-r51.py:239-240`: `PROSE[row].get(base)` is `None` → `continue`. Any basename the row did not map (A7) is never checked and never added to `gaps`.
- Gap leg: `gaps` is computed only from cited lines (lines ~190-260). A range citation (G1) adds every line of the range; the equality leg then accepts a block that equals the bloat, because the block is generated from the same set.
- `lint-grounding-r51.py:279` `out[(m.group(1), m.group(2))] = expand(...)` silently overwrites an earlier line for the same `(Snnn, file)` key. G2's bloat line is discarded before the equality check.
- `lint-grounding-r51.py:327-328` counts a row as clean when it has no `problems`. A row with zero quotes and zero citations has no problems, so `rows_clean` and `lint_ok` count it (D1). Only the counter's `check-scrub-admission-r51.py:211` `quotes_ok` requires `quotes > 0` (D1 fails there alone).
- D2: `QUOTE_RE` (line 76) accepts `(.*)`, so `""` is a whole-line match for a blank snapshot line. No minimum length or content check.
- Q3: the quote loop runs only over `lines[i:j]` of each `## GRn` extent (`row_extent`, lines 103-~120). A quote outside every row is never read, so it is never counted and never required to match. The moved quotes still justify prose citations, so the gap block is unchanged.
- Q4: `QUOTE_RE` takes the source id from the label (`S237`) and checks the text against `cache[(S237, scrub.c)]`. Nothing ties the label to `PROSE[row]['scrub.c'] = 'S242'`.
- Q5 (same text, different line): the quote check is `norm(want) == norm(src[n-1])` (line 233). Any line number whose text equals the quote passes. Eleven of the 63 frozen quotes have text that also occurs at another line of their snapshot (see Result 2).
- Q6: a line starting `**Quote.**` that does not match `QUOTE_RE` falls through to the prose branch; its `file:line` is still added to `cited`, so the gap leg is satisfied and the quote text is never compared.

## Result 2 — the frozen entry itself, measured

- Frozen E0 under frozen tools: PASS (see method).
- 11 of the 63 frozen quotes have text that occurs at more than one line of their snapshot. The two dev-replace quotes at `dev-replace.c:703` and `:1268` (`&dev_replace->scrub_progress, false, true);`) are identical lines in the same file, and neither enclosing function (`btrfs_dev_replace_start`, `btrfs_dev_replace_kthread`) is named in the GR2 text. A reader cannot tell from the text which call the quote supports. (`entry.md:96`, `:102`.)

## Result 3 — prototype closing rules (my design; scratch only, lane untouched)

Built `prototype-lint-grounding-r51.py` (frozen lint + appended overrides; it also replaces the frozen `__main__` guard at the end so the CLI runs the rules). The counter loads the lint from its own directory, so the prototype counter is the frozen counter running the prototype lint. Results in `results-prototype-rules.json`.

Rules, with the cheats each closes (observed on the fixtures):

1. **Canonical citations only (A1–A4, A6, A7).** A row's prose may not place a digit within 25 characters of a row-source basename unless the occurrence is a canonical `file:N[-M]`; a canonical citation must use the basename mapped in `PROSE[row]`; a canonical citation may not be followed by `, N`, `and N` or `to N`. Closes A1, A2, A3, A4, A6 ("ambiguous continuation"), A7 ("unpinned basename").
2. **Dash variants parsed (A5).** `CITE_RE` accepts `-`, `–`, `—`. With that, the gap leg sees `3201-3214, 3227-3250` as missing from the block (`gap_missing`). Closes A5 (`lint_ok 0`).
3. **Range width cap (G1).** A canonical range wider than 100 lines is an error. Frozen E0 has none wider than 60 (`scrub.c:3094-3153` is the widest).
4. **No duplicate gap keys (G2).** A second `- Snnn file:` line for the same key is an error (`declared_gaps`). Closes G2 (`lint_ok 0`).
5. **Every row has ≥1 quote (D1).** Moves the zero-quote check into the lint so `lint_ok` itself fails. D1 becomes `lint_ok 1`, counter fails on both legs.
6. **No trivial quotes (D2).** Quote text must be ≥8 characters and contain a letter. Empty/punctuation-only quotes fail. Frozen E0 passes (`if (s[0] == '0') {` is 18 characters with letters).
7. **Quotes inside rows only (Q3).** Any `**Quote.**` line outside every `## GRn` extent is an error. Prototype attaches this to GR1 as a placeholder; a real rule should be a global problem.
8. **Quote source = row source (Q4).** A quote's `Snnn basename` must equal `PROSE[row][basename]`. Frozen E0 passes (all 63 quotes).
9. **Label must parse (Q6, Q6b).** A line whose first token is `**Quote` must match `QUOTE_RE`, else error. Frozen E0 passes.
10. **Ambiguous quotes name their function (Q5a, Q5b, Q5c) — heuristic.** For a quote whose text occurs more than once in its snapshot, the enclosing column-0 function (scanned upward) must appear in the row's prose. Flags Q5a (both `dev-replace.c:703` and `:1268`), Q5b (`:1213`, enclosing `btrfs_resume_dev_replace_async`), Q5c (`scrub.c:1989`, enclosing `flush_scrub_stripes`). **It also flags two quotes of frozen E0** (`dev-replace.c:703` and `:1268`), so under rule 10 the frozen entry fails.

Prototype outcome:
- Frozen E0 with rules 1–9: `lint_ok 3`, counter PASS (measured before rule 10 was added).
- Frozen E0 with rules 1–10: `lint_ok 2`, counter FAIL on the two dev-replace quotes (`ambiguous quote S247 dev-replace.c:703 … enclosing fn 'btrfs_dev_replace_start' not named in row`; the same for `:1268` with `btrfs_dev_replace_kthread`).
- Every cheat fails the prototype counter (`results-prototype-rules.json`): A1–A4, A6, A7 by rule 1; A5 by rule 2 (`gap_missing`); G1 by rule 3; G2 by rule 4; D1 by rule 5; D2 by rule 6; Q3 by rule 7; Q4 by rule 8; Q6, Q6b by rule 9; Q5a/b/c by rule 10.

Limits of the prototype: rules were designed on these fixtures and E0 only. Rule 1's 25-character digit window could misfire on prose such as "scrub.c, two threads" (not present in E0). Rule 10 is a heuristic (function scan at column 0); it is the only rule that flags frozen E0.

## Proposed smallest rules (for the L1 amendment decision)

- R1 (A-family): reject any row-prose digit within 25 characters of a basename unless it is a canonical `file:N[-M]` with the row's mapped basename; reject `, N` / `and N` / `to N` after a canonical citation.
- R2 (A5): accept `–`/`—` in citation ranges (or reject non-ASCII dashes in citations); the gap leg then catches the hidden range.
- R3 (G1): cap canonical ranges at 100 lines.
- R4 (G2): reject duplicate `- Snnn file:` keys in `### Range gaps (R51)` (`lint-grounding-r51.py:279`).
- R5 (D1): row problem when a row has zero quotes (lint-level, so `lint_ok` fails alone).
- R6 (D2): quote text ≥8 characters with a letter.
- R7 (Q3): `**Quote.**` line outside every `## GRn` extent is a global error.
- R8 (Q4): quote `Snnn` must equal `PROSE[row][basename]`.
- R9 (Q6): any `**Quote` line must match `QUOTE_RE`.
- R10 (Q5, heuristic): a quote whose text occurs more than once in its snapshot must have its enclosing function named in its row. This is the only rule that cannot be closed by a pure text check; it flags two frozen E0 quotes, which the L1 should weigh as a real ambiguity, not a lint artifact.

## Not done

- C2 (`score-counter-cheats-r51.py`) and C3 (`check-adjacency-table-r51.py`) were not run.
- The battery (`battery.py`) was not run as a whole; only its helper functions were imported for the K-pass cohort construction.
- The prototype rules were not run on the other lane entries or on prior rounds' entries; no false-positive rate is measured beyond E0.
- Real seat reports were not used; all cohorts are battery-built.

## Receipts

`.ufo/waves/round-51/w1/R51CritLintCheat/`
- `fixtures/K-pass-frozen.md` (= frozen E0 bytes) and `fixtures/<id>.md` for each cheat (18 files).
- `results-plain.json`: frozen lint and counter results per cheat.
- `results-prototype-rules.json`: prototype lint and counter results per cheat, including E0.
- `prototype-lint-grounding-r51.py`: the prototype rules file (scratch copy; not a lane tool).
