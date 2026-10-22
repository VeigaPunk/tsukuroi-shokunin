# C1 counter shape attack — CritCounterC1Shapes

**Verdict: PARTLY HOLDS.** The frozen counter `tools/check-btrfs-repair-r31.py`
(sha256 `4f69a109…`) correctly refuses the forgery shapes that matter for *depth*
(nested duplicate JSON keys, fenced/indented SKILL lines, `./` and symlink snapshot
paths — all blocked), but it carries **two real defects**: (1) R5's "status cell is
mined" check is position-blind and accepts `mined` in any cell, letting a row with a
non-mined status claim mined provenance; (2) R7's 6-word-run anti-copy guard — the one
rule meant to stop "the quote copied as the statement" — is defeated both by Unicode
look-alikes and by punctuation-merging, so a statement that is the quote's own words
reaches the same fail set as a genuine restatement. Neither alone reaches `new_sourced`
(R7's sealed answer-key groups still gate, and I did not recover the keys), but defect 2
dissolves the only *structural* barrier between a restatement and a copy, leaving the
claim's truth resting entirely on the sealed keys (whose key-harvest ceiling is already
declared) plus wave-2 row review.

## Method
Sandbox clone of the lane at `8cff9e7cfb034b49c645d548801ac3185a827cb4`. The six pinned
btrfs-progs v7.1 snapshots were fetched from the frozen URLs and verified byte-for-byte
against the counter's pins (`fixtures/snapshots.sha256`, all six match). For each shape a
single-row Q01 fixture commit was built on the base and scored with
`python3 tools/check-btrfs-repair-r31.py --revision <commit> --lane <clone>`. Harness,
raw outputs and commit hashes: `w1/CritCounterC1Shapes/fixtures/{attack.py,results.json,run.log}`.

The **baseline** `s00` (commit `8eb504a5`) is a well-formed row with a junk filler
statement; its only failures are `R7 sealed answer-key group 2/3 missing`. So every
structural gate (R1–R6, R8) passes on junk — a shape "passes a gate" exactly when that
gate's fail string is **absent** from the Q01 line (matching the baseline). R7's sealed
groups are left failing on purpose: I never recover the sealed keys (that is a separate
labrat).

## Findings

1. **[obs] DEFECT — R5 accepts `mined` in any cell, not the status column.**
   `s02_mined_wrong_cell` (commit `8e6ad72f`) commits the registry row with the **tier**
   cell set to `mined` and the **status** cell set to `draft`; URL and pin unchanged. Its
   Q01 fail list is identical to the baseline — no R5 failure at all. The contrasting
   control `s03_mined_absent` (commit `87480dec`, same row with no cell equal to `mined`)
   does raise `R5 status cell is not mined`. Committed row proving the column positions:
   `… | docs | mined | fixture | … | fixture row | draft | 2026-10-22 | …` (tier=`mined`,
   status=`draft`). Root cause: `status_cell()` returns *all* cells and the check is
   `if 'mined' not in cells` — list membership, not the status position
   (`tools/check-btrfs-repair-r31.py:171-176, 273-276`). The predicate requires the source
   row be "`mined` at REV"; this lets a `draft`/`rejected`/withdrawn row pass by placing
   the literal word `mined` anywhere (tier, scope, teaches, used-by). **False provenance.**
   Smallest safe fix: split the row into its 11 fixed columns and require
   `cells[STATUS_INDEX] == 'mined'` (status is column 8 of the frozen 11-column shape), not
   membership across the whole row.

2. **[obs] DEFECT — R7's 6-word-run anti-copy guard is bypassable; "quote as statement" passes.**
   The guard (`shares_run`, `tools/check-btrfs-repair-r31.py:137-142`, called at `:296`)
   tokenises with `words()` = `re.findall(r"[a-z0-9][a-z0-9=_.+/-]*", text.lower())`
   (`:134-135`). The plain copy `s04_quote_as_statement` (commit `e3ff06f9`) is correctly
   caught: `R7 statement shares a 6-word run with the quote`. Two cheap transforms defeat
   it while keeping every word of the quote:
   - **Unicode look-alikes** `s06_unicode_lookalike` (commit `32014ef2`). Statement bytes:
     `Defragmentation dоеs nоt prеsеrvе еxtеnt shаring, е.g. filеs crеаtеd by **cp and defragment stays here now`
     — the quote with ASCII `e/o/a` replaced by Cyrillic `е/о/а`. `words()` is ASCII-only,
     so those tokens drop out of the stream, no 6-run matches, and the fail set equals the
     baseline (no run failure, ≥12 words, token `defragment` intact). Renders identically
     to the quote to a human reviewer.
   - **Punctuation merge** `s05_punct_merge` (commit `bb209eed`). Statement is the quote
     with the pivot pair joined by `.` (`extent sharing` → `extent.sharing`). `.` is a
     word-continuation char in `words()`, so the single token every 6-window shares is
     merged and no window can match; all words stay readable and `split()` ≥ 12. Fail set
     equals the baseline.
   Impact: R7's sealed answer-key groups still gate `new_sourced`, but the counter's own
   docstring concedes the keys are single words harvestable from the source and
   dictionary-attackable against the in-file `KEYHASH` ("a writer who has read the source
   can string them together… a dictionary attack on the 16-hex digests is possible"). The
   run guard is the *only* structural rule separating a harvested-word copy from a genuine
   restatement; defeating it makes the copy indistinguishable from a restatement to the
   counter. Smallest safe fix: before `shares_run`, NFKC-normalise both strings and compare
   on a punctuation-insensitive whitespace-split token stream (strip trailing/embedded
   punctuation, fold confusables) so neither a `.`-merge nor a look-alike shifts the stream.

3. **[obs] DEFENSE HOLDS — nested duplicate JSON keys are rejected.**
   `s01_dupkey_nested` (commit `27b79dba`) duplicates `"id"` inside the row object; the
   counter reports `R1 duplicate key 'id'` and `R1 0 rows for Q01`. `object_pairs_hook=no_dup`
   (`:125-131`, used at `:212`) fires for every nested object, not just the top level.

4. **[obs] DEFENSE HOLDS — SKILL line cannot be hidden in a code fence or by indentation.**
   `s10_skill_in_fence` (commit `203cf5bf`) and `s11_skill_indented` (commit `203d16eb`)
   both yield `R6 0 SKILL.md lines for Q01`: fenced lines are skipped by `skill_lines`
   (`:149-165`) and an indented line fails the column-0 `ln.startswith('| [R31-Q01] ')`.

5. **[obs] NO SMUGGLING VIA `<details>`.** `s09_skill_in_details` (commit `bd76e65a`)
   places the required SKILL line inside a `<details>`…`</details>` block; it is still
   counted (passes, baseline fail set) because `<details>` is neither a fence nor an HTML
   comment to `skill_lines`. `s12_skill_double_details` (commit `b3aec241`) adds a second
   copy inside `<details>` and the counter reports `R6 2 SKILL.md lines for Q01`. So a
   `<details>` block can neither hide the required line nor smuggle a decoy past the
   "exactly one" rule — it offers the attacker nothing.

6. **[obs] DEFENSE HOLDS — snapshot path tricks rejected.** `s07_snap_dotslash`
   (commit `5e58723b`, snapshot cited as `.ufo/waves/round-31/./Defragmentation.rst`)
   gives `R3 snapshot absent at revision` — `git show rev:<path>` does not resolve the `./`
   segment and git cannot store a path with a literal `./` component. `s08_snap_symlink`
   (commit `7b4b3a79`, a committed symlink pointing at the real `.rst`) gives
   `R3 snapshot sha256 differs from pin` — the blob is the link-target string, not the file
   bytes. `..` is already blocked explicitly (`:247`).

7. **[inf] NO CROSS-PARSER CONFUSION between SOURCES rows and SKILL lines.**
   `registry_rows` matches `^\|\s*S\d{3}\s*\|` (`:169`) and `skill_lines` matches the
   `| [R31-Qnn] ` prefix (`:163`); the prefixes are disjoint, so a `| [R31-Qnn] |` table
   line cannot be read as a registry row nor a `| S### |` row as a SKILL line. The
   `len(rr) != 1` and `len(sl) != 1` guards (`:271, :280`) catch duplicate rows of either
   kind. No fixture produced a cross-count.

## Legitimate rows wrongly refused
None found. Every refusal above is a shape that *should* be refused; I did not find a
well-formed, truly-sourced row that the structural gates reject. (R7's sealed-key gate on
the baseline is by design, not a wrongful refusal — it only blocks statements that lack the
answer words.)

## Judgement for the canonical judge
- Finding 1 (mined position) is a clean **fixable defect**: a one-line change to the status
  column closes it with no effect on legitimate rows; it weakens the provenance claim today.
- Finding 2 (run-guard bypass) is closer to a **declared tradeoff than a reject**: the
  counter already disclaims that true/useful restatement is judged by wave-2 row reviewers
  "never by this counter", and the key-harvest ceiling is declared. The bypass makes the run
  guard non-additive, so it strengthens the case that row-level human review (not the
  counter) is load-bearing for C1 — but it does not by itself let a sourceless row reach
  `new_sourced`.

Scope: read=tools/check-btrfs-repair-r31.py, .ufo/waves/round-31/measure/controls/build-c1-controls.py, corpus/SOURCES.md+SKILL.md at base; wrote=.ufo/waves/round-31/w1/CritCounterC1Shapes.md, .ufo/waves/round-31/w1/CritCounterC1Shapes/fixtures/{attack.py,results.json,run.log,snapshots.sha256}, fixture commits in /fast/scratch/hyaku/tsukuroi-r31/CritCounterC1Shapes/repo; executed=curl (6 pinned snapshots), python3 attack.py (13 fixture commits + counter runs), read-only git show/rev-parse
Model: not exposed
Installs: none
