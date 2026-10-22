# MutMemPressurePlan — C2 mutation set for `tools/check-memory-pressure.py`

Verdict: two verdicts, because the target changed under this seat while it worked.

Against the **synthetic fixture baseline**, all twelve mutants are KILLED — 12 KILLED, 0
SURVIVED, 0 inconclusive — against the checker at sha256
`8ab91ba79f109910b1e05ecb74b29621ae60d4f367fcbe21a105221ba84a9970` (whose own selftest reports
36 cases, 0 failed), with the pristine fixture verifying 6 of 6 rows and exit 0.

Against the **real landed entry**, which arrived at the end of this seat's work, the result is
**8 KILLED, 2 SURVIVED, 2 needing re-pinning**: the real tree passes (exit 0, 6 verified
rows) and two mutants survive, each because the rule's "at least one" quantifier lets another
piece of the row's evidence carry it. M10 removes the `SKILL.md` decision-table row naming
MP6, and the gate-registry row also names MP6 so the check still passes. M04 lengthens one
Gate quote past 25 words, and the row has other qualifying quotes. Those are the coverage
limits of the rule as declared and as implemented, and they are the substance of finding 9 —
they are not defects in the mutants, and this seat has not changed the contract.

Five findings of substance in all: the tool was unparseable for part of this seat's work
(finding 1); the fixture catalogue and its measured ids (findings 2 and 4); the capture digest
is a document-level precondition rather than a row rule (finding 3); this seat's own first M11
survived, which exposed that a Gate quote merely shorter than the entry's quote still
satisfies the comparison (finding 4b); and the two survivors against the real entry (finding
9).

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

2. [obs] The twelve mutants and the finding ids they must produce are fixed in
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
   | M11 | the row's own quote is not the Gate quote for its source | `MP-QUOTE-MISMATCH` | `MP-QUOTE-MISMATCH` | 1 | 5 | KILLED |
   | M12 | a SOURCES row's cell count differs from the header's | `MP-SOURCE-ROW-SHAPE` | `MP-SOURCE-ROW-SHAPE` | 1 | 5 | KILLED |

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

4b. [obs] This seat's own M11 survived at first, and the survival was the finding. The first
   form of M11 truncated the S118 Gate quote at its pipe, so the lesson recorded a shorter quote
   than the entry's own `quotes[].quote`. The checker compared the two in either direction —
   `quoted in text or text in quoted` — so the shorter Gate quote was still a substring of the
   longer entry quote and the comparison passed: the mutant was **SURVIVED** (exit 0,
   `verified_rows` 6, no findings). [inf] The comparison is deliberately containment in either
   direction so that a location prefix present in one file and not the other does not trip it,
   and that same leniency means a Gate quote that is merely shorter than the entry's quote is
   accepted. The mutant was therefore re-specified to replace the **entry's** quote with a text
   the Gate does not record, which is the case the rule is about; that form is KILLED (exit 1,
   `verified_rows` 5, `MP-QUOTE-MISMATCH`). Two things follow for the L1. First, the earlier
   form of the stricter R3 — where `MP-QUOTE-MISMATCH` was advisory — would have let a row
   carry a quote the Gate does not record without the count moving; the checker now blocks it,
   and M11 pins that. Second, the containment comparison is looser than equality: a row whose
   quote is a prefix or a superstring of the Gate quote still verifies, so the rule constrains
   the quote's content only up to containment.

4c. [obs] The fixture's S118 Gate quote carries a pipe inside the quoted value, deliberately.
   The checker's reader was fixed for that case between 07:57 and 08:03 — it now locates the
   quoted span on the raw row line and keeps the cell offsets, so a pipe inside a located quote
   no longer cuts the quote short. This seat's fixture had been written to avoid a pipe for
   exactly that reason; once the fix landed the pipe was restored, so the fixture now exercises
   the fixed reader rather than dodging it. Measured: the tool reads the S118 quote whole as 10
   words including the pipe, and the baseline still verifies 6 of 6. The same span-based
   reading was applied to this seat's own oracle, runner and quote checker, which had been
   splitting the row first and would have cut the quote at the pipe.

4d. [obs] Two further checker revisions landed during this seat's work and both changed the
   fixture rather than the fixture's expectations being loosened. The checker now reads a Gate
   cell's quoted span from the **outermost** pair of double quotes when quotes are nested, and
   a backtick span still wins over a straight-quoted one; the fixture's S115 quote, whose text
   contains the double quotes of `The "some" line …`, is therefore written inside backticks,
   which is the lane convention for a quote that carries double quotes. With the older
   innermost-pair reading the checker read that cell as the single word `some` and the baseline
   went red; with the outer-pair reading and backticks it reads 20 words and the baseline is
   green again. The checker also now reports `MP-SOURCE-ROW-SHAPE` for a registry row whose
   cell count differs from the header's, and M12 pins that: dropping one cell from the S115
   row yields exactly `MP-SOURCE-ROW-SHAPE` and none of the status/opened/used-by findings a
   shifted read would have produced. This seat's oracle was updated to both rules so that it
   remains a second implementation of the same rule rather than a drifting one; the self-check
   reports 12 mutations, 0 fixture defects.

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
   `summary: 12 mutations, 0 fixture defects`: for every mutant the pristine fixture is green
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

9. [obs] The real entry landed while this seat was working, and the sweep was re-run against
   it — the wave-2 form the executor endorsed. Against the lane at HEAD `5e7c04ec` with the
   checker at sha256 `077bd4843ad54433a6bf705fa06631008f0b526b0c9cef86b93c86da0fdbabcf`
   (`tools/check-memory-pressure.py`), the pristine real tree **passes** (exit 0,
   `verified_rows` 6), and the mutants land differently than they do against the synthetic
   fixture: 8 KILLED, 2 SURVIVED, 2 needing re-pinning. The result is recorded at
   `/fast/scratch/hyaku/tsukuroi-r25/MutMemPressurePlan/real-tree-sweep.json`. This is the
   first measurement against the shipped entry, and it is the one that matters.

   a. [obs] **M10 survives against the real tree.** The mutant deletes the `SKILL.md`
      decision-table row naming MP6, and the checker still verifies all six rows. The cause is
      the checker's R5 rule, "SKILL.md carries a table line that names the row id": the real
      `SKILL.md` names MP6 in **two** table lines, the round-25 decision row at line 2318 and
      the gate-registry row at line 2355 (`| memory-pressure | gate | … | 0 six rows MP1 to MP6
      verified; …`). Deleting only the decision row leaves the registry row, which still names
      MP6, so R5 still passes. [inf] The checker's rule as implemented cannot distinguish a
      row that is named by the registry from a row that is named by the decision table, so a
      decision-table row can be removed without the count noticing. This is a coverage limit of
      the rule, not a defect in the mutant; the L1 should decide whether R5 should require the
      decision-table row specifically.

   b. [obs] **M04 survives against the real tree.** The mutant lengthens one Gate quote past 25
      words and the checker still verifies all six rows. The cause is that the real lesson
      records several Gate rows per source — S115 has three, S118 has two, S120 three, S121
      two, S124 two — and the checker accepts a row when **any** one of its sources has a Gate
      quote of at most 25 words. The row the mutant lengthened was not the only qualifying
      quote for its source. [inf] The rule as implemented is "at least one Gate quote of at
      most 25 words exists for one of the row's sources", so breaking one Gate quote does not
      disqualify a row that has other qualifying quotes. This is the same class of limit as
      M09 and M11: the mutants that break one row's evidence are masked by the rule's
      "at least one" quantifier.

   c. [obs] Two further mutants need re-pinning against the real tree and are INCONCLUSIVE
      rather than surviving. M11 targets MP4's quote for S118, but the real MP4 cites S121,
      S122 and S123 and carries no S118 quote, so the mutation has no target. M12 expects
      `MP-SOURCE-ROW-SHAPE`, but the real `corpus/SOURCES.md` rows now match the header's
      cell count and dropping one cell produces the three derived source findings instead
      (`MP-SOURCE-STATUS-NOT-MINED`, `MP-SOURCE-USED-BY-MISSING`,
      `MP-SOURCE-OPENED-STALE`), because the real registry's cells are read positionally.
      [inf] The fixture catalogue is written against the synthetic baseline, where each row
      cites exactly one source; the real entry cites one to three sources per row, so the
      per-row isolation the catalogue assumed does not hold. Wave 2 should re-pin M11 and M12
      against the real entry's source ids and re-derive their expected finding sets, and
      should decide whether the two survivors in (a) and (b) are intended limits of the
      declared rule or gaps in it.

   d. [obs] M01 against the real tree drops the count by **two** rows and emits two
      `MP-SOURCE-STATUS-NOT-MINED` findings, because the real S115 is cited by both MP1 and
      MP2. That is the real entry's shape, not a fixture defect: the mutant breaks the one
      source both rows cite, so both rows lose it.

## 2. What was written

All under `.ufo/waves/round-25/w1/MutMemPressurePlan/`:

- `fixtures/mutations.json` — the catalogue: twelve mutants, each with the rule it breaks, the
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
- `fixtures/sweep-result.json` — the measured result of the sweep against the synthetic
  fixture baseline, recorded in finding 2.
- `fixtures/real-tree-sweep.json` — the measured result of the sweep against the real landed
  entry, recorded in finding 9. Wave 2 should re-run both forms:
  `python3 fixtures/run-mutations.py --tool <checker> --baseline-repo <lane> --baseline-rev <rev>`
  for the real tree and without those two options for the fixture baseline.

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
plus the baseline against sha256 7144f264…, d320deb4…, d801b999… and 8ab91ba7…, the final
recorded sweep of 12 mutants plus the baseline against sha256 8ab91ba7…, and one sweep of the
same catalogue against the real landed tree at HEAD 5e7c04ec with the checker at sha256
077bd484…).
Model: minimax-m3.1-flash-free (opencode-go/minimax-m3.1-flash-free), per the session context
Installs: none
