# CritC2OverStrict — round 28 residual check, C2 over-strictness

Verdict: fails (partly). "No axis harmed" does not hold for C2 as a property of the counter. The counter at 9a0654ba refuses 9 legitimate entry or lesson shapes that the counter at 75f410c8 accepted. The live entry is not affected (control is 6 of 6 under both counters), so the declared after-value stands. The harm is latent and can be fixed without giving up any of the five routed refusals.

Harness: `/fast/scratch/hyaku/tsuku28/CritC2OverStrict/probe.py`. It builds a sandbox from a `git archive` export of 9a0654ba at `/fast/scratch/hyaku/tsuku28/CritC2OverStrict/tree`, makes a private `git init` repo with one branch per probe, and runs both counter blobs through `--repo/--revision`. Output: `/fast/scratch/hyaku/tsuku28/CritC2OverStrict/probe.out`. "Accepted" means exit 0 with `verified_rows` 6.

## Findings

1. [obs] **Short code-line and doc-line quotes are refused** (rule R4a, `/fast/scratch/hyaku/tsuku28/CritC2OverStrict/tree/tools/check-kernel-taint.py:78-79` and `:710-713`; the floor is at least 2 words and at least 16 non-whitespace characters). Each probe appends one real quote to an existing row and adds the matching Gate row:
   - The documented taint string `Tainted: P        W  O` (`.../tree/.ufo/waves/round-27/sources/S140.rst:39`, 4 words, 11 non-whitespace characters), added to KT1. The old counter gives exit 0 with 6 rows. The new counter gives exit 1 with 5 rows and `KT-QUOTE-TOO-SHORT`.
   - The code line `return -EPERM;` (`.../sources/S141.c:104`, 2 words, 14 characters), added to KT5. Old: 6 rows. New: 5 rows with `KT-QUOTE-TOO-SHORT`.
   - The bare identifier `TAINT_UNSIGNED_MODULE` (S142, 1 word), added to KT1. Old: 6 rows. New: 5 rows with `KT-QUOTE-TOO-SHORT`.
   - Boundary control: `#define TAINT_OOT_MODULE` (2 words, exactly 16 characters) is accepted by both counters.

   [inf] **Harm to a real future entry: yes for the first two.** A kernel-taint row about reading taint flags in an oops would naturally quote the `Tainted:` flag string. Because any failing quote fails its row, adding one such corroborating quote to a row that already verifies drops that row. The identifier refusal is a defensible tradeoff, since a bare token proves little. **Fixable defect:** a floor of 2 words and 10 characters still refuses `kernel` and `the` (and `the cat` in the selftest).

2. [obs] **A Gate table whose S### id sits in an `Id` column, with a URL in the `Source` column, is refused** (rule R4c, `.../tree/tools/check-kernel-taint.py:353-354,362`). Probe `gate_id_column_and_source_url` renames the live header (`.../tree/corpus/lessons/round-27.md:13`) to `| Id | Source | Opened | Located quote (at most 25 words) | Location |`. Old: exit 0 with 6 rows. New: exit 1 with 0 rows and `KT-GATE-QUOTE-MISSING`, so all six rows are lost.

   [inf] **Harm: medium.** Id plus Source-URL is the usual registry layout, and the corpus `SOURCES.md` header itself is `| id | source | ...` (`.../tree/tools/check-kernel-taint.py:863`). The committed round-27 lesson uses `Source`, so nothing breaks today. **Fixable defect:** prefer a column named exactly `id` or `source id`, then fall back to `source`. The routed shape (`gate_source_from_location_cell`) stays refused because a Location cell is never an id column.

3. [obs] **Ordinary Gate heading variants are refused** (rule R4c, `.../tree/tools/check-kernel-taint.py:343`, `title != 'Gate'`). Each of the following lost all six rows under the new counter (exit 1, 0 rows, `KT-GATE-HEADER-MISSING` and `KT-GATE-QUOTE-MISSING`), while the old counter accepted it with 6 rows:
   - `## Gate ##`, a valid closing ATX heading; the title is read as `Gate ##`.
   - `## Gate (round 27)`
   - `## gate`
   - `## Gate:`
   - A `### Gate table` sub-heading inserted above the table. `sections()` splits on every heading level.

   Parity control: a `### Admitted rows` sub-heading is refused by both counters.

   [inf] **Harm: low on the round-27 data**, because the lesson path is fixed and its heading is `## Gate`. It is higher if this rule is cloned into a later round's counter. **Fixable defect:** after removing closing `#` characters and punctuation, match "gate" as the first word, case-insensitively. `Things to investigate` stays refused.

4. [obs] **No regression in these shapes.** Both counters accept each of the following with exit 0 and 6 rows:
   - Row sources as objects (`{"id": ..., "role": ...}`); the R4b normalisation at `:704` handles them.
   - Row sources under the `source_ids` key.
   - Quote source under the `source_id` key.
   - A Gate table with an extra leading `#` column and a trailing `Decision` column.
   - A `Source id` or `Source ID` header.
   - A Source cell holding a link `[S140](#)`.
   - A Source cell holding an annotation `S140 (admitted)`.

5. [obs] **A candidate correction keeps every routed refusal.** The scratch copy `/fast/scratch/hyaku/tsuku28/CritC2OverStrict/patched.py` makes three changes: `MIN_QUOTE_CHARS = 10`, the first-word-"gate" heading test (my probe narrowed the second word to `table` or `round`), and the `id`/`source id` column preference. Results:
   - Battery `python3 tools/mutants-kernel-taint.py --base 9a0654ba... --counter-file .../patched.py` exits 0 with `"should_fail_accepted": 0`, `"control_verified_rows": 6`. Its `other_accepted` list is identical to the shipped counter's under the same battery: 8 non-declared mutants, the same names.
   - `--selftest` reports `"status": "PASS"`, including `r4a-quote-too-short-*`, `r4b-*`, `r4c-gate-heading-not-exact` and `r4c-gate-source-outside-source-cell`.
   - Probes (`probe-patched.out`): every finding-1 to finding-3 shape is accepted except `quote_identifier`. `subhead_other` is still refused.

   [inf] The battery's `other_accepted` shows 8 should-fail-looking mutants that the shipped counter still accepts. They are outside C2's declared five and are noted only.

**Impacted axes:** depth only. The depth counter falsely refuses legitimate rows; this does not change the declared values today. The claim "while the live entry keeps its count" holds.

**Smallest safe correction:**
- Lower `MIN_QUOTE_CHARS` to 10 and keep `MIN_QUOTE_WORDS = 2`.
- Read the Gate source id from an `id` or `source id` column before `source`.
- Accept a Gate heading whose first word is "gate", ignoring case, closing hashes and punctuation.
- Add selftest pass-cases for `Tainted: P W O`, `return -EPERM;`, the `Id | Source` header, and `## Gate ##`.

Scope: read=SCORECARD.md round-28 declaration; tools/check-kernel-taint.py at 75f410c8 and 9a0654ba (diff and full read of the changed sites); tools/mutants-kernel-taint.py at 9a0654ba; corpus/lessons/round-27.md Gate; round-27 source snapshots; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-28/residual/CritC2OverStrict.md, /fast/scratch/hyaku/tsuku28/CritC2OverStrict/{tree/,repo/,counter/,probe.py,probe.out,probe-patched.out,patched.py}; executed=git archive 9a0654ba | tar -x; git show of both counter blobs; python3 probe.py (exit 0); python3 probe.py patched.py (exit 0); python3 tools/mutants-kernel-taint.py --counter-file patched.py (exit 0) and --counter-rev 9a0654ba (exit 0), both in the export; patched --selftest (PASS)
Model: not exposed
Installs: none
