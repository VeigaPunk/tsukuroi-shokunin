# ExecMemPressureTool — round 25, C2 counting checker

Seat: `TsukuroiR25.ExecMemPressureTool` (executor). Draft only; the L1 integrates.
Date: 2026-10-22. Clone: `/fast/scratch/hyaku/tsukuroi-r25/ExecMemPressureTool/repo`, at
`6c580b155840c8750a7bb5f14dcb8e48913d0073` (the round-25 declaration commit).

## Verdict

The C2 counting rule is implemented as `tools/check-memory-pressure.py`: it counts the verified
rows of `corpus/knowledge/memory-pressure-r25.json` at a named revision, reads only through git,
exits 0 only when 6 of 6 rows verify, and its 36-case hermetic selftest passes (exit 0). At the
declaration revision `6c580b15` it exits 2 with `ENTRY-MISSING`, which is the declared before-state
("entry and checker absent"). The L1 landed the C2 entry, the registry rows, the lesson's Gate and
the checker in `5e7c04e`, and the counting command returns exit 0 with `verified_rows` 6 and
`status` PASS at that revision (§2.4b).

## 1. What was built

`tools/check-memory-pressure.py` (sha256
`4bb8ec96d71120ec7a9e01d1b4019d5072dfa1c320bbb179660f8c7bcc41504a`), delivered for integration at
`.ufo/waves/round-25/w1/ExecMemPressureTool/check-memory-pressure.py` in the lane repo and authored
in my clone at `/fast/scratch/hyaku/tsukuroi-r25/ExecMemPressureTool/repo/tools/check-memory-pressure.py`.
Pure standard library, no new dependency, no install.

**Inputs, all read through `git show <rev>:<path>` at the bound revision** [obs]:
`corpus/knowledge/memory-pressure-r25.json`, `corpus/SOURCES.md`, `corpus/lessons/round-25.md`,
`SKILL.md`, `.ufo/waves/round-25/capture/capture.txt`. No host probe, no working-tree byte of the
measured revision is consulted; the working tree is read only for the tool's own source and for
`tools/_revision.py`.

**The five row rules, as declared** (`SCORECARD.md:797`, the "C2 rows, fixed now" paragraph):

| Rule | What must hold | Blocking finding |
|---|---|---|
| R1 | the row carries a non-empty `statement`, `verdict` and `action` | `MP-STATEMENT-EMPTY`, `MP-VERDICT-EMPTY`, `MP-ACTION-EMPTY` |
| R2 | every listed source is a `mined` SOURCES row whose `used-by` names `corpus/knowledge/memory-pressure-r25.md` and that was opened 2026-10-22 or has its `recheck` changed in place with the change logged old → new in `corpus/lessons/round-25.md` | `MP-SOURCE-MISSING`, `MP-SOURCE-STATUS-NOT-MINED`, `MP-SOURCE-USED-BY-MISSING`, `MP-SOURCE-OPENED-STALE`, `MP-SOURCE-DUPLICATE`, `MP-SOURCE-ROW-SHAPE`, `MP-SOURCES-EMPTY` |
| R3 | at least one Gate quote of at most 25 words exists in the lesson's Gate for one of the row's sources; and when the row carries a `quotes` array, every quote it carries is the Gate quote of a source the row lists, and is at most 25 words | `MP-QUOTE-MISSING`, `MP-QUOTE-TOO-LONG`, `MP-QUOTE-MISMATCH`, `MP-QUOTE-SOURCE-UNKNOWN`, `MP-QUOTES-SHAPE` |
| R4 | at least one capture pointer resolves to a line whose text is unique in the capture, is not a `### ` header, a `$ ` echo or an `[exit ` line, holds at least one letter or digit, and contains the pointer's declared token (case-sensitive, ≥ 3 chars) | `MP-CAPTURE-POINTER-MISSING`, `MP-CAPTURE-POINTER-UNUSABLE`, `MP-CAPTURE-POINTER-SHAPE`, `MP-CAPTURE-POINTER-PATH`, `MP-CAPTURE-POINTER-LINE-RANGE`, `MP-CAPTURE-POINTER-HEADER`, `MP-CAPTURE-POINTER-ECHO`, `MP-CAPTURE-POINTER-EXIT`, `MP-CAPTURE-POINTER-BLANK`, `MP-CAPTURE-POINTER-NOT-UNIQUE`, `MP-CAPTURE-POINTER-TOKEN-ABSENT`, `MP-CAPTURE-POINTER-TOKEN-SHORT` |
| R5 | `SKILL.md` carries a table line naming the row id | `MP-SKILL-ROW-MISSING` |

`MP-SUPERSEDES-SHAPE` is recorded but non-blocking. `MP-QUOTE-MISMATCH` and
`MP-QUOTE-SOURCE-UNKNOWN` were advisories and are now blocking (§2.6).

**Global findings** (`SCORECARD.md` fixes the exit contract): `CAPTURE-MISSING`,
`CAPTURE-TAMPERED`, `ENTRY-MISSING`, `ENTRY-MALFORMED`, `ENTRY-SCHEMA`, `LESSON-MISSING`,
`SOURCES-MISSING`, `SKILL-MISSING` all exit 2; `MP-ROW-SET`, `MP-CAPTURE-PATH-MISMATCH` and
`MP-CAPTURE-DECLARED-MISMATCH` are global blocking findings that set `verified_rows` to 0.

**Exit codes and output** [obs]: exit 0 when `verified_rows == 6`, exit 1 when it is below, exit 2
when the entry cannot be evaluated. The JSON on stdout carries `revision`, `branch`, `status`,
`declared_rows` (6), `verified_rows`, the capture's observed sha256, a `rows` array with a
per-rule view (`R1_statement_verdict_action`, `R2_sources`, `R3_gate_quote`, `R4_capture_pointer`,
`R5_skill_row`, each with `ok` and its findings), a per-row detail block (`sources`, `quotes`,
`capture_pointers`, `skill_row`) and a flat `findings` array whose entries carry `id`, `site` and
`blocking`.

**The L1's binding refinement is implemented as given** [obs]: the capture sha256 is verified
before anything else is read (`CAPTURE-TAMPERED`, exit 2); each pointer is an object
`{line: N, token: "<substring>"}`; a pointer counts only if the line text is unique in the capture,
is not a `### ` header, a `$ ` echo or an `[exit ` line, contains at least one letter or digit,
and contains its declared token (case-sensitive, ≥ 3 characters). The selftest has the two extra
cases the refinement asked for: `blank-unique-line-pointer` and `token-absent-pointer`.

**One addition beyond the declared rule** [inf]: the tool requires a non-empty `statement` on
every row, because the entry JSON schema needs a slot for the row's claim and the six rows would
otherwise differ only by id. `DraftEntry` has been told; if the L1 prefers the declaration's
literal two-field wording, deleting the `MP-STATEMENT-EMPTY` check and the `statement` field
requirement is a one-line change that does not touch any other rule.

## 2. Evidence

### 2.1 Selftest: 37 hermetic cases, 0 failed

Command: `python3 -B tools/check-memory-pressure.py --selftest` in the clone.
Output saved at `.ufo/waves/round-25/w1/ExecMemPressureTool/selftest.json`.
Result: `{"status": "PASS", "cases": 37, "failed": 0, ...}`, exit 0.

Each case builds a throwaway git repository (`git init`, one commit, no remote) holding the five
inputs, then evaluates the entry in it through the same `git show` reader the revision mode uses.
No lane byte is read or written by the selftest. The cases, each with its committed expected
finding ids and expected exit code:

`clean-pass`, `source-not-mined`, `source-used-by-other-entry`,
`source-opened-other-day-without-recheck`, `source-opened-other-day-with-logged-recheck`,
`source-missing`, `no-sources`, `quote-too-long`, `quote-missing`, `gate-quote-with-pipe`,
`gate-quote-with-inner-quotes`, `source-row-wrong-column-count`, `entry-quote-not-in-gate`,
`entry-quote-source-not-listed`, `skill-row-id-only-in-prose`, `header-pointer`, `echo-pointer`,
`exit-pointer`,
`duplicate-line-pointer`, `blank-unique-line-pointer`, `token-absent-pointer`,
`token-too-short-pointer`, `pointer-line-out-of-range`, `missing-skill-row`, `verdict-empty`,
`action-empty`, `statement-empty`, `capture-digest-tampered`, `capture-missing`, `entry-missing`,
`entry-malformed`, `entry-wrong-schema`, `lesson-missing`, `sources-missing`, `skill-missing`,
`row-id-unknown`, `declared-capture-digest-mismatch`.

Each case is a single-rule break: the expected finding set is compared exactly against the
blocking findings the tool emitted, together with the expected exit code and the expected
`verified_rows`. `source-opened-other-day-with-logged-recheck` is the positive control for the
routed-defect-5 relaxation: a source opened 2026-10-19 whose `recheck` cell is changed in place
and whose change is logged old → new in the lesson passes, exit 0, `verified_rows` 6.

### 2.2 The declared before-state

Command: `python3 -B tools/check-memory-pressure.py --revision 6c580b155840c8750a7bb5f14dcb8e48913d0073`.
Output saved at `.ufo/waves/round-25/w1/ExecMemPressureTool/revision-6c580b15.json`.

```json
{"branch": "master", "declared_rows": 6, "findings": [{"blocking": true, "id": "ENTRY-MISSING", "site": "corpus/knowledge/memory-pressure-r25.json"}], "revision": "6c580b155840c8750a7bb5f14dcb8e48913d0073", "rows": [], "status": "CANNOT_EVALUATE", "verified_rows": 0}
```

Exit 2, `ENTRY-MISSING` — as the assignment requires. The same reading at the lane's current head
`0cd9b28` and at `master` also gives exit 2 with `ENTRY-MISSING` [obs], because
`corpus/knowledge/memory-pressure-r25.json` is not in the tree yet.

### 2.3 The capture pin holds

`git cat-file blob 6c580b15:.ufo/waves/round-25/capture/capture.txt | sha256sum` gives
`e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136`, equal to the value declared
at `SCORECARD.md:797` and to the constant in the tool [obs]. The same blob at the lane's later head
`0cd9b28` hashes to the same value [obs], so the pin survives the declaration refinement commit.

### 2.4 Six of six is reachable

A temporary entry was built on the real capture bytes at the pinned sha256, with six `mined`
sources opened 2026-10-22 whose `used-by` names the entry, six Gate quotes of four words each in a
lesson Gate table, six SKILL.md table rows and six capture pointers onto lines 14, 15, 38, 117, 106
and 47 of the real capture. Evaluated through the same reader in a throwaway repository: exit 0,
`status` PASS, `verified_rows` 6, every row's five rules `ok` with no findings [obs]. Re-verified
after each of the three fixes of §2.6; the count still holds under the stricter R3.

The `DraftEntry` draft is the second independent demonstration: with its registry rows carrying
one cell per column, it verifies 6 of 6 against the real capture with no findings (§2.6).

Two dry runs before that one were useful negatives, and they show the pointer rule bites. A first
attempt pointed MP4 at capture line 80 and MP6 at line 62; the tool answered
`MP-CAPTURE-POINTER-EXIT`, `MP-CAPTURE-POINTER-NOT-UNIQUE`, `MP-CAPTURE-POINTER-TOKEN-ABSENT`
and `MP-CAPTURE-POINTER-UNUSABLE` for those rows, exit 1, `verified_rows` 3. Line 80 is an
`[exit ` line, and line 62's text `oom_kill 0` also occurs at line 51. The pointers were moved to
lines that are unique in the capture and the count reached 6.

### 2.4b The C2 target is met at the landed revision

The L1 landed the round-25 work in commit `5e7c04e` ("round-25: C1 self-assessment checker and
current axes table; C2 memory-pressure entry, sources S115-S125, checker, SKILL table and
registry; lesson, QUALITY 57-59, LOG; wave-1 evidence"). Measuring that commit with the checker
the L1 landed at `tools/check-memory-pressure.py`:

```
$ python3 -B tools/check-memory-pressure.py --revision 5e7c04e
{"branch": "master", "declared_rows": 6, "status": "PASS", "verified_rows": 6, "findings": [], ...}
exit 0
```

[obs] The landed checker's own selftest at that revision: `PASS`, 32 cases, 0 failed, exit 0.

Measuring the same commit with my current checker (`8ab91ba…`, 36 selftest cases) gives the same
result — exit 0, `status` PASS, `verified_rows` 6, no findings — because the landed registry rows
all carry one cell per column and the landed lesson's Gate quotes are read whole [obs]. All 125
registry rows at that revision parse with no malformed row and no duplicate id, and the lesson's
Gate carries a located quote for each of S115 to S125 [obs]. The landed entry declares the pinned
capture sha256 `e60f1bbc…` and its six row ids are MP1 to MP6 [obs].

**The L1 landed a checker that is one revision behind mine** [obs]: the committed
`tools/check-memory-pressure.py` at `5e7c04e` hashes to
`077bd4843ad54433a6bf705fa06631008f0b526b0c9cef86b93c86da0fdbabcf`, and differs from my current
`8ab91ba…` in the four places the last round of fixes touched: the `MP-SOURCE-ROW-SHAPE` check
(the landed reader still reads a short registry row by header name rather than reporting it as
malformed), the header detection that requires a separator row after it, the stricter R3 in which
`MP-QUOTE-MISMATCH` and `MP-QUOTE-SOURCE-UNKNOWN` block, and the two corresponding selftest
cases. None of the four changes the landed measurement: the landed tree has no malformed
registry row and no entry/Gate quote disagreement, so both checkers read it as 6 of 6 [obs]. The
difference matters for future rounds, not for this claim, and the L1 owns the integration
decision.

### 2.5 Capture facts the L1 and the source seats need

From the real capture at the pinned sha256 [obs], the lines whose text occurs exactly once and
which are neither a `### ` header, a `$ ` echo nor an `[exit ` line:
3 (`2026-10-22T10:06:23Z`), 6 (`7.2.11-arch1-1`), 9 (`systemd 262 (262-1-arch)`), 14 and 15 (the
first `some`/`full` totals), 34, 35, 38, 39, 42, 43 (the per-cgroup `some`/`full` totals), 47
(`low 0`), 50 (`oom 0`), 52 (`oom_group_kill 0`), 53 (`sock_throttled 13763`), 58 (`fail 510`),
66 to 69 (`MemTotal`, `MemAvailable`, `SwapTotal`, `SwapFree`), 73 (`inactive`), 86 to 108 (the
`oomd.conf` comment block and its three commented defaults, including 106 `#SwapUsedLimit=90%`
and 107 `#DefaultMemoryPressureLimit=60%`), 117 (`MemoryPressureWatch=skip`), 149 and 150.

Lines whose text is duplicated and therefore unusable as a pointer [obs]: 21 and 29, 22 and 30
(the root cgroup prints the system PSI totals again — `include/linux/psi.h:37-40` maps the root
cgroup onto `psi_system`, so this is a kernel property, not a capture slip, as `SrcPsiDoc`
reported), 48 and 56 (`high 0`), 49 and 57 (`max 0`), 51 and 62 (`oom_kill 0`), 76 and 79
(`disabled`), and every `[exit 0]` line.

### 2.6 Three defects found by the sibling seats, and the fixes

**Defect 1 — a pipe inside a quoted Gate cell truncated the quote.** `MutMemPressurePlan`
reported it. Reproduced before the fix: a Gate row
`| S115 | https://x/a | "the pipe | inside" | SrcA |` yielded the quote `"the pipe` — two words and
the wrong text — because the row was split on the bare pipe before the quote was located. The fix
reads the quote from the raw row line rather than from a pre-split cell: the row is split with the
same backslash-escape rule as before (a `\|` does not separate cells), the cell offsets are kept,
and the quoted span is located against them. After the fix the same row yields
`the pipe | inside`, and a backtick-quoted span `code | span` is likewise found whole [obs]. Pinned
by the selftest case `gate-quote-with-pipe`.

**Defect 2 — a located quote containing double quotes was read as its innermost pair.** The
`DraftEntry` draft exposed it: the S115 Gate quote is
`The "some" line indicates the share of time in which at least some tasks are stalled on a given
resource.`, and the reader took the innermost pair and returned the single word `The`. Every S115
quote would have mismatched. The extractor now reads a cell's quoted span from the outermost pair
when the quotes are nested, and from the left when the cell separates several located quotes with
`"; `, which is how a registry anchor cell holding three located quotes is written. A
backtick-delimited span still wins over a straight-quoted one, because the lane writes a quote
that contains double quotes inside backticks. After the fix all 14 of the draft's quotes match
their Gate cell, and the longest is 20 words [obs]. Pinned by the selftest case
`gate-quote-with-inner-quotes`.

**Defect 3 — a registry row with the wrong cell count was read as a shifted row.** The
`DraftEntry` draft's `corpus/SOURCES.md` rows carry ten cells against the registry header's
eleven (`id | source | kind | tier | scope | anchor | teaches | status | opened | recheck |
used-by`, `corpus/SOURCES.md:5`): the `teaches` column was dropped and the anchor and teaches
text were merged into one cell, so every column after `scope` sat one position to the left. The
reader located the columns by the header's names when the count matched and could not name them
when it did not. It now reports one finding, `MP-SOURCE-ROW-SHAPE`, and does not guess — and it
does not also emit the three derived findings that a shifted read would have produced. The header
is located by a table row whose next line is the separator row, so a prose line that merely looks
like a header is not read as one [obs]. Pinned by the selftest case `source-row-wrong-column-count`.

**One semantic question the mutation tester raised, resolved.** Its M11 mutant truncates the Gate
quote at its pipe; the tool reported `MP-QUOTE-MISMATCH` but the row still verified, because the
finding was advisory. The declared rule (`SCORECARD.md:797`) reads "a located quote of at most 25
words recorded in that lesson's Gate", so the Gate quote alone satisfies it literally — but a row
carrying a quote the Gate does not record asserts a quote that no cited page supplies, and its
evidence chain has a hole. `MP-QUOTE-MISMATCH` and `MP-QUOTE-SOURCE-UNKNOWN` are therefore now
blocking. A row with no `quotes` array is unaffected: the Gate quote still carries the row. The
comparison is whitespace-normalised and matches in either direction, so a location prefix present
in one file and not the other does not trip it. Pinned by `entry-quote-not-in-gate` and
`entry-quote-source-not-listed`.

**The draft entry reaches the target once one cell per registry row is restored.** I ran the
checker against the `DraftEntry` draft in a throwaway repository. The entry itself is clean: all
twelve capture pointers count, all fourteen quotes match the Gate, all six row ids appear once
each, and every `statement`, `verdict` and `action` is non-empty. The draft's registry rows are
the one defect (`MP-SOURCE-ROW-SHAPE` on every source). Splitting the merged cell at the
`"; lines "` boundary in a throwaway copy — the anchor before it, the teaches after — gave exit 0,
`status` PASS, `verified_rows` 6 and no findings at all, under both the previous and the stricter
R3 [obs]. The L1 has been sent this and the exact fix.

### 2.7 The two survivors against the landed tree, and what they are

`MutMemPressurePlan` swept the landed tree at `5e7c04e` and reported 8 killed, 2 survived, 2
needing re-pinning. I reproduced both survivors against that exact revision and measured what
each mutant actually does. One is a defect in the mutant, one was a real gap in my rule.

**M10 survived, and it was a real gap in my R5 rule — now fixed.** The mutant deletes the
SKILL.md decision-table row whose first cell is `MP6`. My rule was "some SKILL.md table line names
the row id", and the landed SKILL.md has a second table line that names MP6 inside a cell's prose:
the gate-registry row at line 2355 reads `| memory-pressure | gate | ... | 0 six rows MP1 to MP6
verified; ... |`. That is not a decision-table row for MP6, but my rule could not tell the
difference, so the deleted row left the registry row to carry the check. The declaration asks for
"a SKILL.md decision-table row, appended this round, that names the row id", so the rule now
requires the row id to be a cell of its own (`skill_names_row`), not a mention inside a cell's
prose. After the fix the same mutant gives exit 1, `verified_rows` 5,
`MP-SKILL-ROW-MISSING` on MP6 [obs]. The landed tree still verifies 6 of 6, because its decision
table names each id in its own `id` column. Pinned by the selftest case
`skill-row-id-only-in-prose`.

**M04 survived, and the mutant was aimed at the wrong cell.** The landed lesson's Gate table has
five columns — `| Source | URL | Opened | Located quote (at most 25 words) | Location |` — so the
quote is in `cells[3]`. The mutant writes its replacement into `cells[2]`, which in the landed
table is the `Opened` date. It therefore overwrites a date with a 26-word string and leaves every
quote untouched; the quote rule has nothing to reject. Two further facts confirm the mutant is
mis-aimed rather than the rule being loose: its `expected_rows_broken` is `MP4`, but MP4 lists
S121, S122 and S123 and never S118, so the quote it corrupts belongs to MP3 and MP6; and the
synthetic baseline it was written against has a three-column Gate table where `cells[2]` is the
quote.

I confirmed the rule does kill the mutation the mutant means, by running the corrected mutation
against the landed tree [obs]. Writing 26 words into the quote cell that MP3 cites gives exit 1,
`verified_rows` 5, `MP-QUOTE-MISMATCH` on S118; writing 26 words into the quote cell that MP6
cites gives the same; and writing 26 words into the quote cell *and* updating the entry's own
quote to match gives exit 1, `verified_rows` 5, `MP-QUOTE-TOO-LONG` on S118. The "at least one
quote per row" quantifier is not what saves the row — the per-quote checks do that work.

**The re-cut draft verifies 6 of 6.** `DraftEntry` re-cut the registry rows with one cell per
column and the quotes in backticks. Running the checker against the re-cut sources rows, the
re-cut lesson Gate and the unchanged entry JSON: exit 0, `status` PASS, `verified_rows` 6, no
findings; all eight registry rows parse with `shape` true, and all thirteen capture pointers and
all fourteen quotes are accepted [obs].

**Delivered tool digest.** `4bb8ec96d71120ec7a9e01d1b4019d5072dfa1c320bbb179660f8c7bcc41504a`,
37 selftest cases, 0 failed. The earlier digests the mutation tester swept (`7144f264…`,
`d320deb4…`, `d801b999…`, `8ab91ba…`) each predate at least one of the fixes above and must be
re-pinned.

## 3. The entry JSON schema the L1 must write

The tool reads this schema. It is the shape `DraftEntry` proposed, with two changes: the pointer
token key is `token` (not `contains`), and every row carries a non-empty `statement`.

```json
{
  "schema": "tsukuroi-memory-pressure-r25-v1",
  "entry": "corpus/knowledge/memory-pressure-r25.md",
  "capture": {
    "path": ".ufo/waves/round-25/capture/capture.txt",
    "sha256": "e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136"
  },
  "rows": [
    {
      "id": "MP1",
      "statement": "non-empty claim text for this row",
      "verdict": "non-empty verdict",
      "action": "non-empty action",
      "sources": ["S115"],
      "quotes": [{"source": "S115", "quote": "the located quote, at most 25 words"}],
      "capture_pointers": [{"line": 14, "token": "some avg10=0.02"}],
      "supersedes": ["corpus/knowledge/oom-event-plane.md:301"],
      "notes": "free text"
    }
  ]
}
```

Field by field:

| Field | Type | Requirement |
|---|---|---|
| `schema` | string | exactly `tsukuroi-memory-pressure-r25-v1`; anything else is `ENTRY-SCHEMA`, exit 2 |
| `entry` | string | the entry's markdown path; read, not gated |
| `capture.path` | string | must equal `.ufo/waves/round-25/capture/capture.txt` |
| `capture.sha256` | string | must equal the sha256 of the capture actually read at the revision |
| `rows` | array | six objects, ids exactly MP1..MP6, each id once |
| `rows[].id` | string | one of MP1..MP6, no repeats |
| `rows[].statement` | string | non-empty |
| `rows[].verdict` | string | non-empty |
| `rows[].action` | string | non-empty |
| `rows[].sources` | array of strings | non-empty; each id must be a `mined` SOURCES row whose `used-by` names the entry and that was opened 2026-10-22 or recheck-logged old → new in the lesson |
| `rows[].quotes` | array of `{source, quote}` | `source` must be one of the row's sources; `quote` must be found in the lesson's Gate cell for that source (advisory if not); the lesson's own quote for that source must be ≤ 25 words |
| `rows[].capture_pointers` | array of `{line, token}` | `line` an int inside the capture; `token` a ≥ 3-character case-sensitive substring of that line; the line's text must be unique in the capture and must be neither a `### ` header, a `$ ` echo nor an `[exit ` line, and must hold at least one letter or digit |
| `rows[].supersedes` | array of strings | optional; shape checked only |
| `rows[].notes` | string | optional, not read |

Two parser details the lesson writer needs [obs]. The Gate table's header must carry a cell
containing the word `quote`, and the source id goes in the first cell; the reader then locates the
quote column from that header. The recheck log is read in three shapes — the table form
`| S116 | recheck | 90d | 30d |`, the one-cell arrow form `| S116 | recheck | 90d -> 30d |` and the
prose form `S116 recheck: 90d -> 30d`. A logged change counts for a source only when the logged
NEW value equals that source's `recheck` cell in `corpus/SOURCES.md` and differs from the logged
OLD value, which is what makes it an in-place update rather than a restatement.

Next free source id is `S115` (`corpus/SOURCES.md` ends at `S114`).

## 4. Risks and blockers

1. **The `statement` field is my addition, not the declared rule** [inf]. `DraftEntry` was told and
   may argue for its removal; the check is one line and no other rule depends on it.
2. **The lesson's Gate and recheck-log shapes are the L1's to land** [obs]. The reader accepts the
   three recheck shapes and both Gate shapes listed above, but a lesson written in some other
   shape would silently produce `MP-QUOTE-MISSING` or `MP-SOURCE-OPENED-STALE` rather than a
   parse error. If the L1 writes the Gate table without a header cell naming the quote column, the
   reader falls back to the first cell that carries a quote mark, which is the behaviour I want
   but not one I have seen in a real round-25 lesson.
2b. **The registry rows must carry one cell per column** [obs]. The `DraftEntry` draft dropped the
   `teaches` column, and the tool now reports `MP-SOURCE-ROW-SHAPE` for such a row rather than
   reading it shifted. The L1 must land the rows with all eleven cells, or the count stays at 0.
3. **`MP-QUOTE-MISMATCH` and `MP-QUOTE-SOURCE-UNKNOWN` are now blocking** [inf], on the
   mutation tester's M11 finding (§2.6). The comparison is whitespace-normalised and matches in
   either direction, so a location prefix present in one file and not the other does not trip it.
   This is stricter than the declaration's literal wording, which the Gate quote alone satisfies;
   the L1 should confirm the stricter reading is what the claim intends. A row with no `quotes`
   array is unaffected.
3b. **R5 now requires the row id to be a cell of its own** [inf], on the M10 finding (§2.7). The
   declaration says "a SKILL.md decision-table row ... that names the row id", and the landed
   SKILL.md has a gate-registry row that mentions `MP1 to MP6` inside a cell's prose. Requiring the
   id to stand alone in a cell is the reading that matches the wording. The landed tree still
   verifies 6 of 6 under it.
4. **The `used-by` check accepts the stem** `corpus/knowledge/memory-pressure-r25` [inf], so a
   SOURCES row may name the entry as `.md` or `.json`. A row naming only the `.json` would still
   satisfy the declaration's "used-by names the entry" wording; if the L1 wants the `.md` form
   only, the constant `ENTRY_STEM` becomes `ENTRY_MD`.
5. **Revision binding** uses the shared `tools/_revision.py` [obs], so a revision that is not an
   ancestor of `refs/heads/master` is refused with one `E-*` id and exit 2. The measurement
   revision must therefore be landed on the lane's `master` before the command in the declaration
   can return 0.
6. **The tool is landed, but at a digest several revisions behind my current one** [obs]. The L1
   landed `077bd4843ad54433a6bf705fa06631008f0b526b0c9cef86b93c86da0fdbabcf`; my current copy is
   `4bb8ec96d71120ec7a9e01d1b4019d5072dfa1c320bbb179660f8c7bcc41504a`, which adds the
   `MP-SOURCE-ROW-SHAPE` check, the separator-anchored header detection, the stricter R3 in which
   the entry's own quote must match the Gate, and the R5 rule that requires the row id to be a
   cell of its own (§2.4b, §2.6, §2.7). All of them read the landed tree as 6 of 6 — the landed
   tree has no malformed registry row, no entry/Gate quote disagreement and no SKILL.md table that
   names an MP id only inside prose. The L1 owns which digest stands; if the later one lands, the
   new selftest cases and the two new findings come with it.
7. **The sibling lane's scope is not absorbed** [inf]. `PROVINCE.md` row ADJ-04 routes fleet or
   wave attribution of pressure to `mori`, and `mori`'s `system-pressure-r24.md` owns CPU, IO and
   IRQ pressure reading. This checker counts evidence links in the lane's own committed bytes; it
   makes no claim about CPU, IO or IRQ pressure and reads no sibling repository.
8. **The draft's registry rows needed the `teaches` column restored** [obs]. The L1 landed them
   with one cell per column; my check of the landed tree finds 125 well-formed rows and no
   malformed row. This was the only thing between the `DraftEntry` draft and 6 of 6.
9. **No blocker.** [obs]

## 5. Coordination

`MutMemPressurePlan` received the full finding-id vocabulary, the pointer slot shape
(`{line, token}`) and the capture uniqueness facts, so its mutants assert this tool's ids rather
than a parallel guess. It then swept mutants over temporary git repositories against successive
copies of this tool: 10 of 10 killed on `d320deb4…`, 11 of 11 on `d801b999…` with the baseline
green at 6/6, then 12 of 12 on `8ab91ba…`, and against the landed tree 8 killed, 2 survived, 2
needing re-pinning [obs, reported by that seat]. Its sweeps found the pipe-in-quote defect, the
nested-quote defect and the M11 question about the advisory quote mismatch, all resolved in §2.6;
the M10 survivor was a real gap in my R5 rule and is fixed in §2.7; the M04 survivor is a
mis-aimed mutant, measured in §2.7. It also reported that an earlier draft of this tool did not
compile at 07:51 (`IndentationError`, two adjacent `case()` calls with one closing parenthesis
too many); that was corrected at the time and the current copy compiles
(`python3 -m py_compile` exit 0) [obs]. It has been sent the new digest, the changed expectations
and the M04 column finding, since its oracle and quote checker must use the outer-pair quote rule
and its Gate mutator must address the landed table's quote column.

`DraftEntry` received the schema in §3 with the two changes, the lesson parser shapes and the
reachable-6-of-6 result. It then delivered a draft; I ran the checker against that draft in a
throwaway repository and reported the result: the entry is clean, the registry rows carry ten
cells against the header's eleven, and restoring the `teaches` cell makes the draft verify 6 of 6
with no findings. It re-cut the rows with one cell per column and the quotes in backticks; I ran
the checker against the re-cut sources rows, the re-cut lesson Gate and the unchanged entry JSON
and got exit 0, `verified_rows` 6, no findings (§2.7). The L1 had already landed its own version
of the entry, sources and lesson at `5e7c04e`, and that tree verifies 6 of 6 as well.

## 6. Scope note

No production lane file was edited: `SKILL.md`, `SCORECARD.md`, `LOG.md`, `PROVINCE.md`,
`SHONEN.md`, `corpus/` and `tools/` are untouched in the lane repo. The only lane-repo writes are
this report and the three files under `.ufo/waves/round-25/w1/ExecMemPressureTool/`. No git or jj
write command of any kind was run against `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`; the
lane repo was read only (`git show`, `git ls-tree`, `git cat-file`, `git status`, `git log`,
`git rev-parse`). Nothing was pushed, fetched or written to the lane's `master`. The tool was
developed in the clone named in my item; the scratch git repositories the selftest builds carry no
remote.

Installs: none.

Scope: read=SCORECARD.md (round 25 declaration, C2 rows paragraph at :797), corpus/lessons/round-24-verifier-spotcheck.md (routed defect 1), corpus/SOURCES.md (registry shape and header at :5, next free id S115, all 114 rows re-parsed after the quote and column fixes, all 125 rows at the landed revision), corpus/knowledge/pause-lift-gate-r24.json and tools/check-pause-gate.py (the round-24 counting-tool precedent), tools/_revision.py (shared revision binder), corpus/knowledge/oom-event-plane.md:270-350 (the weaker prior statements), the round-25 capture at the pinned sha256, the landed revision 5e7c04e (entry, registry, lesson, SKILL.md), and the wave-1 drafts and reports of MutMemPressurePlan, DraftEntry, SrcPsiDoc, DraftLessonMistakes; wrote=.ufo/waves/round-25/w1/ExecMemPressureTool.md, .ufo/waves/round-25/w1/ExecMemPressureTool/check-memory-pressure.py, .ufo/waves/round-25/w1/ExecMemPressureTool/selftest.json, .ufo/waves/round-25/w1/ExecMemPressureTool/revision-6c580b15.json, and tools/check-memory-pressure.py in the clone /fast/scratch/hyaku/tsukuroi-r25/ExecMemPressureTool/repo; executed=python3 -B tools/check-memory-pressure.py --selftest (exit 0, 37 cases, 0 failed), python3 -B tools/check-memory-pressure.py --revision 6c580b155840c8750a7bb5f14dcb8e48913d0073 (exit 2, ENTRY-MISSING), python3 -m py_compile on the delivered copy (exit 0), read-only git show/cat-file/ls-tree/log/status/rev-parse on the lane and the clone, and the temporary-repository dry runs of the checker: the synthetic entry at 3 of 6 then 6 of 6; the DraftEntry draft as written, then with the teaches cell restored, then the re-cut draft at 6 of 6; the landed revision 5e7c04e at 6 of 6 with both the L1's landed checker and mine; and the M04 and M10 survivor reproductions, including the corrected M04 in three forms.
Model: opencode-go/minimax-m3.1-flash-free
Installs: none
