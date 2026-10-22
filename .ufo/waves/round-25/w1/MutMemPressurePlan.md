# MutMemPressurePlan — C2 mutation set for `tools/check-memory-pressure.py`

Verdict: the C2 counting rule is **killed by all eleven mutants** — 11 KILLED, 0 SURVIVED,
0 inconclusive — against the production checker at sha256
`d801b99945b55183ffe91930228cc7dee35150da549ec0dfb0cee3c3d42b8a8f`
(`.ufo/waves/round-25/w1/ExecMemPressureTool/check-memory-pressure.py`). The pristine fixture
baseline verifies 6 of 6 rows with exit 0 and an empty findings list, so the sweep measured a
real detector on a real green baseline, not a broken one. Three findings of substance: the C2
rule as the tool implements it has **no survivor among the eleven breaks** (findings 2 and 4);
the tool was unparseable for part of this seat's work (finding 1); and the eleven mutants pin
two coverage limits of the rule as the tool implements it — the capture digest is a
document-level precondition rather than a row rule (finding 3), and the entry's own quote
disagreeing with the lesson Gate is advisory rather than blocking (finding 4b).

## 1. Findings

0. [obs] The finding-id vocabulary in this catalogue is the checker's own, confirmed with its
   author on 2026-10-22 and then re-measured. This seat did not take the ids it had proposed to
   the build seat on trust: it read them out of the tool source and recorded the `findings` array
   the tool actually emits for each mutant (finding 2). The one correction the author confirmed
   is in this seat's own proposal: `MP-CAPTURE-DIGEST-MISMATCH` was proposed and the tool emits
   `CAPTURE-TAMPERED`, because the L1's refinement made the capture digest the first check with
   its own exit-2 id; the catalogue carries `CAPTURE-TAMPERED` and keeps the proposed name as an
   alias only. The author's capture-line facts were also reproduced independently by this seat
   before they were sent: the same set of unique-and-non-structural lines, and capture line 21 as
   the duplicate-line target, whose duplication the author attributes to the root cgroup being
   mapped onto `psi_system`.

1. [obs] The production checker was unparseable between 07:51 and 07:57 on 2026-10-22 and this
   seat's first sweep against it was void. At 07:51:23 the file at
   `/fast/scratch/hyaku/tsukuroi-r25/ExecMemPressureTool/repo/tools/check-memory-pressure.py`
   failed to compile: `python3 -m py_compile tools/check-memory-pressure.py` printed
   `IndentationError: unexpected indent (check-memory-pressure.py, line 701)`. The defect was in
   the self-test's `case(...)` calls: the `verdict-empty` and `action-empty` cases closed the
   call with four closing parentheses where three are needed, so the expect-dict on the following
   line became an unexpected indent. At 07:57:39 the executor's own clone carried a rewritten
   file (37850 bytes, previously 33325) that compiles cleanly
   (`python3 -m py_compile` exits 0, sha256 `7144f264…`). [inf] The checker is authored in the
   executor's own clone and was being edited while this seat worked; the sweep below was run
   against the compiling revision, and the earlier void run was discarded rather than reported as
   a mutant result.

2. [obs] The eleven mutants and the finding ids they must produce are fixed in
   `.ufo/waves/round-25/w1/MutMemPressurePlan/fixtures/mutations.json`, and the measured result
   is in `.ufo/waves/round-25/w1/MutMemPressurePlan/fixtures/sweep-result.json`, recorded from
   the run against the landed bytes sha256 `d320deb4…`. The measured finding ids are the tool's
   own, not a proposal:

   | id | break | expected finding id | measured finding id | exit | verified_rows | verdict |
   |---|---|---|---|---|---|---|
   | baseline | none (pristine fixture) | — | none | 0 | 6 | PASS |
   | M01 | source row is `queued`, not `mined` | `MP-SOURCE-STATUS-NOT-MINED` | `MP-SOURCE-STATUS-NOT-MINED` | 1 | 5 | KILLED |
   | M02 | source `used-by` no longer names the entry | `MP-SOURCE-USED-BY-MISSING` | `MP-SOURCE-USED-BY-MISSING` | 1 | 5 | KILLED |
   | M03 | source opened 2026-10-21 with no logged recheck | `MP-SOURCE-OPENED-STALE` | `MP-SOURCE-OPENED-STALE` | 1 | 5 | KILLED |
   | M04 | located quote is 26 words | `MP-QUOTE-TOO-LONG` | `MP-QUOTE-TOO-LONG`, `MP-QUOTE-MISMATCH` | 1 | 5 | KILLED |
   | M05 | capture pointer resolves to a `### ` header (line 12) | `MP-CAPTURE-POINTER-HEADER` | `MP-CAPTURE-POINTER-HEADER`, `MP-CAPTURE-POINTER-UNUSABLE` | 1 | 5 | KILLED |
   | M06 | capture pointer resolves to a `$ ` echo (line 28) | `MP-CAPTURE-POINTER-ECHO` | `MP-CAPTURE-POINTER-ECHO`, `MP-CAPTURE-POINTER-UNUSABLE` | 1 | 5 | KILLED |
   | M07 | capture pointer resolves to an `[exit ` line (line 74) | `MP-CAPTURE-POINTER-EXIT` | `MP-CAPTURE-POINTER-EXIT`, `MP-CAPTURE-POINTER-UNUSABLE` | 1 | 5 | KILLED |
   | M08 | capture pointer line text occurs twice (line 21) | `MP-CAPTURE-POINTER-NOT-UNIQUE` | `MP-CAPTURE-POINTER-NOT-UNIQUE`, `MP-CAPTURE-POINTER-UNUSABLE` | 1 | 5 | KILLED |
   | M09 | capture bytes appended, sha256 no longer the pinned one | `CAPTURE-TAMPERED` | `CAPTURE-TAMPERED` | 2 | 0 | KILLED |
   | M10 | SKILL.md decision-table row for the id is deleted | `MP-SKILL-ROW-MISSING` | `MP-SKILL-ROW-MISSING` | 1 | 5 | KILLED |
   | M11 | Gate quote truncated at its pipe | `MP-QUOTE-MISMATCH` | `MP-QUOTE-MISMATCH` | 0 | 6 | KILLED |

3. [obs] M09 is not a row-level break and cannot be. The tool verifies the capture digest
   **before** it reads anything else and refuses to evaluate a capture whose sha256 is not
   `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136`: it exits 2 with
   `status CANNOT_EVALUATE` and the single finding `CAPTURE-TAMPERED`, and `verified_rows` is 0
   because no row was counted. So M09's expected `verified_rows` is null in the catalogue, not
   5, and the finding id it must produce is the tool's `CAPTURE-TAMPERED` rather than the
   `MP-CAPTURE-DIGEST-MISMATCH` this seat had proposed in the vocabulary sent to the executor on
   2026-10-22. The catalogue now carries the tool's id and keeps the proposed name as an
   alias. [inf] The digest is a document-level precondition rather than a sixth row rule, so
   the "6 verified rows" target is unreachable for a tampered capture rather than reduced to 5.

4. [obs] Nine of the ten mutants break exactly one row: `verified_rows` falls from 6 to 5 and
   the expected finding id is the only rule-specific finding besides the tool's own
   consequence finding (`MP-CAPTURE-POINTER-UNUSABLE` for the pointer mutants, which the tool
   raises when a row has pointers but none that count; `MP-QUOTE-MISMATCH` for M04, which the
   tool raises when the entry's own `quotes` list no longer matches the lesson Gate). [inf] The
   consequence findings are not a second broken rule: they are the tool's way of recording that
   the row lost its last qualifying pointer or its Gate agreement. The self-check oracle
   (`fixtures/oracle-check-memory-pressure.py`) confirms the same row set changed for each
   mutant, so the extra findings do not hide a second defect.

4b. [obs] M11 pins a coverage limit rather than a defect, and it is the one mutant whose
   finding does not move the count. It truncates the S118 Gate quote at its pipe, so the lesson
   records a different quote text from the entry's own `quotes[].quote` for that source. The
   tool reports `MP-QUOTE-MISMATCH` — and marks it **advisory** (`blocking: false`), so the row
   still verifies, `verified_rows` stays 6 and the tool still exits 0. The declared C2 rule
   requires "a located quote of at most 25 words recorded in that lesson's Gate", and the tool
   satisfies that from the lesson side alone; the entry's own copy of the quote is checked
   against the lesson but does not disqualify the row. [inf] The C2 count therefore does not
   depend on the entry's quote agreeing with the Gate. The finding the mutant names is emitted,
   so it is killed, but it is killed as an advisory: the row is not disqualified. The L1 should
   decide whether the declared rule intends that, because a row may then carry a quote that the
   Gate does not record.

4c. [obs] The fixture's S118 Gate quote carries a pipe inside the quoted value, deliberately.
   The checker's reader was fixed for that case between 07:57 and 08:03 — it now locates the
   quoted span on the raw row line and keeps the cell offsets, so a pipe inside a located quote
   no longer cuts the quote short. This seat's fixture had been written to avoid a pipe for
   exactly that reason; once the fix landed the pipe was restored, so the fixture now exercises
   the fixed reader rather than dodging it. Measured: the tool reads the S118 quote whole as 10
   words including the pipe, and the baseline still verifies 6 of 6. The same span-based
   reading (cell offsets plus a balanced quoted span over the raw line) was applied to this
   seat's own oracle, runner and quote checker, which had been splitting the row first and
   would have cut the quote at the pipe.

4a. [obs] The four pointer mutants each break exactly one pointer rule because the runner
   rewrites the whole `capture_pointers` list with one object whose `token` is a run of three or
   more characters taken from the **target** line. Measured tokens: M05 line 12 token
   `system-memory-psi-read-1`, M06 line 28 token `memory.pressure`, M07 line 74 token `exit`,
   M08 line 21 token `41389485`; each token is present in its own target line, so no
   `MP-CAPTURE-POINTER-TOKEN-ABSENT` is produced and the only findings on those four mutants are
   the target's own id and `MP-CAPTURE-POINTER-UNUSABLE`. [obs] The checker reads `token` and
   falls back to `contains` for the same field, so a mutant that rewrote the whole object is
   judged the same under either naming. [inf] This also matters for wave 2: a mutant that
   changed only `line` and left the old token would raise the token-absent finding as well and
   would no longer isolate one rule, so the runner must keep deriving the token from the new
   line.

5. [obs] The fixture set is self-checking and green. `fixtures/self-check-fixtures.py` reports
   `summary: 11 mutations, 0 fixture defects`: for every mutant the pristine fixture is green
   (6 rows, no finding), the mutant verifies exactly 5 rows, exactly the one expected row
   changes, and the expected problem is the one the mutant claims to break. A mutant that broke
   a different rule than it claims would fail this check rather than pass silently.

6. [obs] Every fixture quote is present in the page it names and is at most 25 words.
   `fixtures/check-quotes.py` re-opens each page and prints `OK: every fixture quote is present
   in the page it names and is at most 25 words`, with the fetched page digests:
   psi.rst v7.2 sha256 `11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692` (20 and
   13 words), cgroup-v2.rst v7.2 sha256 `a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad`
   (6 and 15 words), systemd.resource-control(5) sha256 `607c9cfec87f445c84b71c5a2ccadf1e93c4e0be76c85f30bb4bac688627fd1a`
   (15 words, and the quote itself contains a pipe), oomd.conf(5) sha256
   `fd948dd4b671a43d618cc4d4205759b0586e3596ff0dfd2f564e4b445851914f` (17 words). This seat
   fetched these pages itself with `curl`; no quote is taken on trust from another seat's
   transcript.

7. [obs] Two fixture-shape facts the tool's schema forced, and the L1 should know before
   landing a real entry. First, the entry JSON must carry a per-row `quotes` list of
   `{source, quote}` objects; a row without it draws `MP-QUOTES-SHAPE` and the row cannot
   verify. Second, the tool compares the entry's `quotes[].quote` against the lesson Gate text,
   so the two must agree character for character after whitespace normalisation
   (`MP-QUOTE-MISMATCH` otherwise) — the lesson's Gate cell must be written so the tool's quote
   extraction returns the page text, which in the fixture meant wrapping the S115 quote in curly
   quotes and choosing a pipe-free S118 quote, because a `|` inside a markdown table cell is a
   cell separator. [inf] A real entry authored without these two facts in mind will fail on
   shape rather than on substance, and a real lesson that puts a pipe in a quoted cell will be
   read as two cells.

8. [unk] The fixture baseline is a synthetic tree that satisfies the counting rule; it is not
   the lane's real entry, which does not exist yet at any revision this seat could read
   (`git ls-tree -r 6c580b15 | grep memory-pressure` returns nothing). Whether the real landed
   entry breaks under the same ten mutations is therefore not measured by this report. The
   runner supports it: `fixtures/run-mutations.py --baseline-repo <repo> --baseline-rev <rev>`
   extracts the real tree with `git archive` and applies the same ten structural mutations to
   the real `corpus/knowledge/memory-pressure-r25.json`, `corpus/SOURCES.md`,
   `corpus/lessons/round-25.md` and `SKILL.md`, then runs the same counting command. The wave-2
   sweep should use that form, because it is the only one that says anything about the shipped
   entry.

## 2. What was written

All under `.ufo/waves/round-25/w1/MutMemPressurePlan/`:

- `fixtures/mutations.json` — the catalogue: eleven mutants, each with the rule it breaks, the
  expected finding id, the target file, the operation, and the finding-id aliases.
- `fixtures/baseline/` — the pristine fixture tree: entry JSON and markdown, `corpus/SOURCES.md`
  with rows S115-S120, `corpus/lessons/round-25.md` with the Gate (the S118 quote carries a pipe
  inside its quoted value on purpose), `SKILL.md` with the six-row decision table, and a
  byte-for-byte copy of the frozen capture.
- `fixtures/run-mutations.py` — the runner. It builds one temporary git repository per mutant
  with `git init` (no remote, so no push can reach the lane), applies the mutation, commits, and
  runs `python3 tools/check-memory-pressure.py --revision <commit>` inside it. It also installs
  the shared `tools/_revision.py` adapter next to the checker, which the lane's checkers import.
- `fixtures/self-check-fixtures.py` — validates the fixture set against the independent oracle.
- `fixtures/oracle-check-memory-pressure.py` — a small independent implementation of the C2
  counting rule, used only to prove the fixtures are coherent. It is not the lane's checker and
  is not installed into the lane.
- `fixtures/check-quotes.py` — re-opens each cited page and checks the recorded quote against
  the page bytes.
- `fixtures/sweep-result.json` — the measured result of the sweep recorded in finding 2.

## 3. Method and restoration

The runner never writes to the lane repository. Every temporary repository is created under
`/fast/scratch/hyaku/tsukuroi-r25/MutMemPressurePlan/` with `git init --initial-branch=master`
and no remote; the sweep deletes the tree afterwards unless `--keep` is passed. The checker is
copied into the temporary repository and run there, so the tool's own bytes are never modified.
The lane working tree was read only: `git status --porcelain --untracked-files=all` after the
sweep lists twelve files, all of them under
`.ufo/waves/round-25/w1/MutMemPressurePlan/`, and the lane HEAD is unchanged at
`0cd9b28bee5fd5a50d991e6dee0c0d0f48b15935`. The checker's own bytes are unchanged at sha256
`7144f2644ebc9277775963f38de6429093851e4d83c163a658e4af1dab1d9f1d`; the executor's clone was
read, never written. No git write command of any kind was run against the lane repository, and
nothing was pushed.

Scope: read=SCORECARD.md Round 25 declaration and refinements, the frozen capture
.ufo/waves/round-25/capture/capture.txt (sha256 e60f1bbc…), the round-24 pause-gate checker and
its fixture conventions, corpus/SOURCES.md and corpus/lessons/round-24.md for the row and
recheck-log formats, the production checker in the executor's clone
(/fast/scratch/hyaku/tsukuroi-r25/ExecMemPressureTool/repo/tools/check-memory-pressure.py) and
its landed copy (.ufo/waves/round-25/w1/ExecMemPressureTool/check-memory-pressure.py), the
Linux v7.2 and systemd v262 source pages (fetched with curl), and the lane git state;
wrote=.ufo/waves/round-25/w1/MutMemPressurePlan.md and, under
.ufo/waves/round-25/w1/MutMemPressurePlan/, fixtures/mutations.json, fixtures/baseline/ (six
files), fixtures/run-mutations.py, fixtures/self-check-fixtures.py,
fixtures/oracle-check-memory-pressure.py, fixtures/check-quotes.py, fixtures/sweep-result.json;
executed=curl of five source pages (sha256 recorded), python3 -m py_compile on the production
checker, python3 fixtures/check-quotes.py, python3 fixtures/self-check-fixtures.py, and
python3 fixtures/run-mutations.py --tool <production checker> (six runs: one void run against
the unparseable revision, one rehearsal against a stub, three recorded sweeps of 10 mutants
plus the baseline against sha256 7144f264…, d320deb4… and d801b999…, and the final recorded
sweep of 11 mutants plus the baseline against sha256 d801b999…).
Model: minimax-m3.1-flash-free (opencode-go/minimax-m3.1-flash-free), per the session context
Installs: none
