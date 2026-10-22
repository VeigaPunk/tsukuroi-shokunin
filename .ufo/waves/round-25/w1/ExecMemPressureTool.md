# ExecMemPressureTool — round 25, C2 counting checker

Seat: `TsukuroiR25.ExecMemPressureTool` (executor). Draft only; the L1 integrates.
Date: 2026-10-22. Clone: `/fast/scratch/hyaku/tsukuroi-r25/ExecMemPressureTool/repo`, at
`6c580b155840c8750a7bb5f14dcb8e48913d0073` (the round-25 declaration commit).

## Verdict

The C2 counting rule is implemented as `tools/check-memory-pressure.py`: it counts the verified
rows of `corpus/knowledge/memory-pressure-r25.json` at a named revision, reads only through git,
exits 0 only when 6 of 6 rows verify, and its 31-case hermetic selftest passes (exit 0). At the
declaration revision `6c580b15` it exits 2 with `ENTRY-MISSING`, which is the declared before-state
("entry and checker absent"). A 6-of-6 PASS is reachable: a temporary entry built on the real
capture bytes verifies 6 of 6.

## 1. What was built

`tools/check-memory-pressure.py` (39 609 bytes, sha256
`d801b99945b55183ffe91930228cc7dee35150da549ec0dfb0cee3c3d42b8a8f`), delivered for integration at
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
| R2 | every listed source is a `mined` SOURCES row whose `used-by` names `corpus/knowledge/memory-pressure-r25.md` and that was opened 2026-10-22 or has its `recheck` changed in place with the change logged old → new in `corpus/lessons/round-25.md` | `MP-SOURCE-MISSING`, `MP-SOURCE-STATUS-NOT-MINED`, `MP-SOURCE-USED-BY-MISSING`, `MP-SOURCE-OPENED-STALE`, `MP-SOURCE-DUPLICATE`, `MP-SOURCES-EMPTY` |
| R3 | at least one Gate quote of at most 25 words exists in the lesson's Gate for one of the row's sources | `MP-QUOTE-MISSING`, `MP-QUOTE-TOO-LONG` |
| R4 | at least one capture pointer resolves to a line whose text is unique in the capture, is not a `### ` header, a `$ ` echo or an `[exit ` line, holds at least one letter or digit, and contains the pointer's declared token (case-sensitive, ≥ 3 chars) | `MP-CAPTURE-POINTER-MISSING`, `MP-CAPTURE-POINTER-UNUSABLE`, `MP-CAPTURE-POINTER-SHAPE`, `MP-CAPTURE-POINTER-PATH`, `MP-CAPTURE-POINTER-LINE-RANGE`, `MP-CAPTURE-POINTER-HEADER`, `MP-CAPTURE-POINTER-ECHO`, `MP-CAPTURE-POINTER-EXIT`, `MP-CAPTURE-POINTER-BLANK`, `MP-CAPTURE-POINTER-NOT-UNIQUE`, `MP-CAPTURE-POINTER-TOKEN-ABSENT`, `MP-CAPTURE-POINTER-TOKEN-SHORT` |
| R5 | `SKILL.md` carries a table line naming the row id | `MP-SKILL-ROW-MISSING` |

`MP-QUOTE-MISMATCH`, `MP-QUOTE-SOURCE-UNKNOWN` and `MP-SUPERSEDES-SHAPE` are recorded but
non-blocking advisories, so an entry is not failed by a wording drift between its own `quotes`
array and the lesson's Gate copy.

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

### 2.1 Selftest: 32 hermetic cases, 0 failed

Command: `python3 -B tools/check-memory-pressure.py --selftest` in the clone.
Output saved at `.ufo/waves/round-25/w1/ExecMemPressureTool/selftest.json`.
Result: `{"status": "PASS", "cases": 32, "failed": 0, ...}`, exit 0.

Each case builds a throwaway git repository (`git init`, one commit, no remote) holding the five
inputs, then evaluates the entry in it through the same `git show` reader the revision mode uses.
No lane byte is read or written by the selftest. The cases, each with its committed expected
finding ids and expected exit code:

`clean-pass`, `source-not-mined`, `source-used-by-other-entry`,
`source-opened-other-day-without-recheck`, `source-opened-other-day-with-logged-recheck`,
`source-missing`, `no-sources`, `quote-too-long`, `quote-missing`, `gate-quote-with-pipe`,
`header-pointer`, `echo-pointer`, `exit-pointer`, `duplicate-line-pointer`,
`blank-unique-line-pointer`, `token-absent-pointer`, `token-too-short-pointer`,
`pointer-line-out-of-range`, `missing-skill-row`, `verdict-empty`, `action-empty`,
`statement-empty`, `capture-digest-tampered`, `capture-missing`, `entry-missing`,
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
`status` PASS, `verified_rows` 6, every row's five rules `ok` with no findings [obs].

Two dry runs before that one were useful negatives, and they show the pointer rule bites. A first
attempt pointed MP4 at capture line 80 and MP6 at line 62; the tool answered
`MP-CAPTURE-POINTER-EXIT`, `MP-CAPTURE-POINTER-NOT-UNIQUE`, `MP-CAPTURE-POINTER-TOKEN-ABSENT`
and `MP-CAPTURE-POINTER-UNUSABLE` for those rows, exit 1, `verified_rows` 3. Line 80 is an
`[exit ` line, and line 62's text `oom_kill 0` also occurs at line 51. The pointers were moved to
lines that are unique in the capture and the count reached 6.

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

### 2.6 A defect the mutation tester found, and the fix

`MutMemPressurePlan` reported that a pipe inside a quoted Gate cell was read as a cell separator,
so the located quote was truncated and the entry's own quote would not be found. That was a real
defect in my reader [obs]. Reproduced before the fix: a Gate row
`| S115 | https://x/a | "the pipe | inside" | SrcA |` yielded the quote `"the pipe` — two words and
the wrong text — because the row was split on the bare pipe before the quote was located.

The fix reads the quote from the raw row line rather than from a pre-split cell. The row is split
with the same backslash-escape rule as before (a `\|` does not separate cells), but the cell
offsets are kept and the quoted span is located against them, so a quote that spans a pipe is
found whole. After the fix the same row yields `the pipe | inside`, and a backtick-quoted span
`code | span` is likewise found whole [obs]. The `corpus/SOURCES.md` parse is unchanged by the
fix: all 114 registry rows still split into 11 cells with no duplicate ids, checked against
`master` [obs].

The case is now pinned by the selftest case `gate-quote-with-pipe` (exit 0, `verified_rows` 6),
which is the 32nd case. The delivered tool is
`d801b99945b55183ffe91930228cc7dee35150da549ec0dfb0cee3c3d42b8a8f`; the earlier
`d320deb4…` copy that the mutation tester swept had the defect.

**Advice for the lesson writer** [inf]: a located quote that contains a pipe is now read whole, so
the pipe does not have to be escaped. It still must not contain a cell separator that changes the
column count of its row in a way that moves the quote column — the reader locates the quote by the
header's quote column, and a pipe inside the quoted value does not change that, but a pipe inside
the URL or source cell does.

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
3. **`MP-QUOTE-MISMATCH` compares the entry's quote against the lesson's** [inf]. The comparison is
   whitespace-normalised and substring-based, so trailing punctuation inside the quote marks
   (`"…stalls."` against `"…stalls"`) is a mismatch by one character. It is non-blocking, so it
   cannot cost a row, but it will appear in the findings array. A pipe inside the quoted value is
   no longer a problem (§2.6).
4. **The `used-by` check accepts the stem** `corpus/knowledge/memory-pressure-r25` [inf], so a
   SOURCES row may name the entry as `.md` or `.json`. A row naming only the `.json` would still
   satisfy the declaration's "used-by names the entry" wording; if the L1 wants the `.md` form
   only, the constant `ENTRY_STEM` becomes `ENTRY_MD`.
5. **Revision binding** uses the shared `tools/_revision.py` [obs], so a revision that is not an
   ancestor of `refs/heads/master` is refused with one `E-*` id and exit 2. The measurement
   revision must therefore be landed on the lane's `master` before the command in the declaration
   can return 0.
6. **The tool is not in the lane's `tools/` yet** [obs]. Until the L1 lands it, the declared
   command `python3 tools/check-memory-pressure.py --revision <REV>` does not exist in the lane, so
   the C2 after-value is not yet measurable at any revision. The draft is at
   `.ufo/waves/round-25/w1/ExecMemPressureTool/check-memory-pressure.py`.
7. **The sibling lane's scope is not absorbed** [inf]. `PROVINCE.md` row ADJ-04 routes fleet or
   wave attribution of pressure to `mori`, and `mori`'s `system-pressure-r24.md` owns CPU, IO and
   IRQ pressure reading. This checker counts evidence links in the lane's own committed bytes; it
   makes no claim about CPU, IO or IRQ pressure and reads no sibling repository.
8. **No blocker.** [obs]

## 5. Coordination

`MutMemPressurePlan` received the full finding-id vocabulary, the pointer slot shape
(`{line, token}`) and the capture uniqueness facts, so its mutants assert this tool's ids rather
than a parallel guess. It then ran ten mutants over temporary git repositories against an earlier
copy of this tool: 10 killed, 0 survived, 0 inconclusive, with the measured ids and counts
matching the vocabulary above [obs, reported by that seat]. Its sweep also found the pipe-in-quote
defect of §2.6, which is fixed here, and it reported that an earlier draft of this tool did not
compile at 07:51 (`IndentationError`, two adjacent `case()` calls with one closing parenthesis
too many). That was corrected at the time and the current copy compiles
(`python3 -m py_compile` exit 0) [obs].

`DraftEntry` received the schema in §3 with the two changes, the lesson parser shapes and the
reachable-6-of-6 result, and was offered a check of its drafted JSON against the checker in a
throwaway repository.

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

Scope: read=SCORECARD.md (round 25 declaration, C2 rows paragraph at :797), corpus/lessons/round-24-verifier-spotcheck.md (routed defect 1), corpus/SOURCES.md (registry shape, next free id S115, all 114 rows re-parsed after the quote fix), corpus/knowledge/pause-lift-gate-r24.json and tools/check-pause-gate.py (the round-24 counting-tool precedent), tools/_revision.py (shared revision binder), corpus/knowledge/oom-event-plane.md:270-350 (the weaker prior statements), the round-25 capture at the pinned sha256, and the wave-1 drafts of MutMemPressurePlan, DraftEntry, SrcPsiDoc, DraftLessonMistakes; wrote=.ufo/waves/round-25/w1/ExecMemPressureTool.md, .ufo/waves/round-25/w1/ExecMemPressureTool/check-memory-pressure.py, .ufo/waves/round-25/w1/ExecMemPressureTool/selftest.json, .ufo/waves/round-25/w1/ExecMemPressureTool/revision-6c580b15.json, and tools/check-memory-pressure.py in the clone /fast/scratch/hyaku/tsukuroi-r25/ExecMemPressureTool/repo; executed=python3 -B tools/check-memory-pressure.py --selftest (exit 0, 32 cases, 0 failed), python3 -B tools/check-memory-pressure.py --revision 6c580b155840c8750a7bb5f14dcb8e48913d0073 (exit 2, ENTRY-MISSING), python3 -m py_compile on the delivered copy (exit 0), read-only git show/cat-file/ls-tree/log/status/rev-parse on the lane and the clone, and three temporary-repository dry runs of the checker (exit 1 with 3 of 6, then exit 0 with 6 of 6, re-verified after the quote fix).
Model: opencode-go/minimax-m3.1-flash-free
Installs: none
