# Round 25 wave 1 — registry home format for the two new tools

Verdict: the lane registry home is `SKILL.md`, and the only section shape `tools/check-registry-coverage.py` accepts is one section headed exactly `## Gate and probe registry — round25 superseding current rows` containing the exact eight-column header, an eight-column separator, and all 28 rows contiguously (the 26 round-24 rows repeated verbatim plus one row per new tool); a section headed `— round25 additions`, or one holding only the two new rows, leaves the audit red.

## 1. How the checker discovers tools

[obs] `GitReader.tool_files` runs `git ls-tree -r -z --full-tree <rev> -- tools/` and keeps only entries whose mode is `100644` or `100755`, whose kind is `blob`, whose name starts with `tools/`, and whose path has no `__pycache__` component (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-registry-coverage.py:84-93`). Discovery is over the committed tree at the bound revision, not the working tree, and it recurses into subdirectories of `tools/`.

[obs] The consequence is that every committed regular file under `tools/`, of any extension and any depth, is a tool that needs exactly one registry row. Symlinks (mode `120000`) and directories are not counted. At the claim base the set is 26 files: `git ls-tree -r --name-only b9046016831237cd04d38da11ba76e50d5380c53 -- tools/` lists `_revision.py`, `boot-chain-audit.sh`, `check-registry-coverage.py`, `measure-update-recheck.py`, `report-red-causes.py`, `tsukuroi-census.sh` and the twenty other `check-*.py` files.

[obs] `--baseline-tools <REV>` adds three informational counts to the JSON (`baseline_tools_total`, `baseline_tools_missing`, `discovered_tools`) and does not change the pass rule (`check-registry-coverage.py:392-396`). It is the cheapest receipt that round 25 added exactly two tools and covered both.

## 2. How the checker discovers registry rows

[obs] `_operative_rows` (`check-registry-coverage.py:165-213`) reads committed `SKILL.md` and works as follows.

1. Heading match is a full-line fullmatch against `^## Gate and probe registry — round([0-9]+) superseding current rows$` (`:23-24`). The dash is U+2014 with one space on each side, the word `round` is joined to the digits, and the literal words `superseding current rows` must follow. A `###` heading, a space after `round`, a trailing space, or any other wording does not match.
2. At least one such heading must exist, or the result is `CANNOT_EVALUATE` with `E-REGISTRY-TABLE`. The operative section is the one with the highest round number; two headings with that same highest number is also `E-REGISTRY-TABLE` (`:174-184`).
3. The section runs from the heading to the next ATX heading of level one or two, that is, the next line matching `^ {0,3}(#{1,6})[ \t]+` with at most two hashes (`:25`, `:185-187`). A `###` subheading does not end it; a `##` does.
4. Inside the section exactly one line must split into the eight-cell `HEADER` tuple `Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner` (`:21-22`, `:189-192`). No match is `E-REGISTRY-TABLE`; that line must be followed by an eight-column `---` separator (`:193-196`).
5. Rows are the consecutive non-blank lines after the separator (`:198-211`). A blank line ends the table silently, and the rows below it are never read. A line that starts with `|` but does not split into exactly eight cells raises `E-REGISTRY-TABLE`; a line that does not start with `|` simply ends the table. Cells split on unescaped pipes, so `\|` stays inside a cell (`:114-132`).

[obs] Everything after the first blank line of the operative section is invisible to the coverage check, which is why the round-24 section's own trailing prose at `SKILL.md:2286-2301` costs nothing.

## 3. Per-row acceptance rules and the finding each one raises

[obs] `_coverage` (`check-registry-coverage.py:233-297`) applies six rules to the operative rows.

| Rule | Code location | Finding id when violated |
|---|---|---|
| `Kind` must be `gate`, `probe` or `library` | `:243-246` | `REGISTRY-KIND-INVALID` |
| A `gate` row's verdict map must contain standalone `0`, `1` and `2`; a `probe` row's must contain `0` and `2`; `library` is unchecked | `:247-269` | `REGISTRY-VERDICT-INCOMPLETE` |
| Tool paths are harvested only from the `Entry command` and `Self-test` cells, by `(?<![A-Za-z0-9_.-])tools/[A-Za-z0-9_./-]+` | `:26`, `:216-222` | — |
| A row that names two or more discovered tools | `:248-251` | `REGISTRY-ROW-AMBIGUOUS` |
| A row that names a `tools/` path that is not a committed regular tool | `:270-273` | `REGISTRY-ROW-ORPHAN` |
| A tool named by no row / by two rows | `:288-295` | `REGISTRY-ROW-MISSING` / `REGISTRY-ROW-DUPLICATE` |
| Every `--self-test` or `--selftest` spelling found in the `Self-test` cell must appear literally in the committed source of the tool that row names | `:27`, `:275-286` | `REGISTRY-SELFTEST-UNRESOLVED` |

[obs] Any finding makes the exit code 1; no finding makes it 0; a table or revision error makes it 2 (`:397`, `:399-405`).

[obs] `--audit-live-map` first blanks fenced code blocks (`:141-163`, `:383-384`) and then requires exactly one row named `boot-chain-audit`, exactly one row referencing `tools/boot-chain-audit.sh` in its entry or self-test cell, and that row byte-equal to the frozen kind, entry text, self-test text, whitespace-normalized verdict map and write scope in `:31-37` (`_audit_live_map`, `:300-323`). The retained round-24 row already satisfies this; any rewording of it raises `REGISTRY-AUDIT-LIVE-MAP`.

## 4. What the round-25 section must contain

[obs] The table below is the complete normative checklist; every item was exercised against the real checker in section 6.

1. One new section headed exactly `## Gate and probe registry — round25 superseding current rows`, appended after the round-24 section, so it is the unique highest round number. Keeping the round-24 heading is fine and required for history: the experiment kept it and the audit passed.
2. A short preamble paragraph before the table, stating that the unique highest complete table is operative, that every earlier table is historical, and that every round-24 row is retained verbatim. The round-24 preamble at `SKILL.md:2256` is the template. Nothing in the checker parses this paragraph.
3. Exactly one eight-cell header line and one eight-cell separator, copied from `SKILL.md:2258-2259` unchanged.
4. Exactly 28 contiguous data rows and no blank line among them: the 26 round-24 rows from `SKILL.md:2260-2285` repeated verbatim, then one row for `tools/check-self-assessment.py` and one for `tools/check-memory-pressure.py`. The earlier round-24 table is historical once the round-25 heading exists, so any row dropped from the new table becomes `REGISTRY-ROW-MISSING` for its tool.
5. Each new row names exactly one tool, and names it in both the `Entry command` and the `Self-test` cells; neither cell may mention any other `tools/` path, not even in prose.
6. Each new row's `Kind` is `gate`, because both tools can return 0, 1 and 2. Its verdict map must therefore contain the standalone digits `0`, `1` and `2`, for example `0 six rows verified;1 row or evidence invalid;2 could-not-evaluate`. A `probe` kind without `1` is accepted by the checker but contradicts the PROTOCOL row schema for a gate, and a `gate` map missing `1` is a finding.
7. The `Self-test` cell's flag spelling must match the committed tool source literally. `--selftest` and `--self-test` are both recognised by the checker's regex, but the string in the cell has to appear in the source bytes; a cell saying `--self-test` over a source that defines `--selftest` raises `REGISTRY-SELFTEST-UNRESOLVED` (observed).
8. No fenced code block and no blank line anywhere between the header and the last row, because `--audit-live-map` blanks fenced lines and a blank line silently truncates the table.
9. The section must end at a level-two heading or at end of file. Appending at end of file is the simplest safe shape.
10. Only one heading anywhere in `SKILL.md` may carry round number 25 in that exact form.
11. The audited revision must be a commit landed on `master` (and pushed when an origin ref exists), because every tool binds through `tools/_revision.py:172` `bind`; an uncommitted or branch-only `SKILL.md` is not read.
12. Both tool files and the `SKILL.md` edit must be present at the same measured revision. A row committed before its tool exists is `REGISTRY-ROW-ORPHAN` at that revision.

## 5. Drop-in row drafts

The two rows below satisfy every mechanical rule in section 3 in a fixture run. They are drafts: the verdict wording and the self-test flag must be reconciled with the bytes the two executors actually commit, per rule 7 above.

```text
## Gate and probe registry — round25 superseding current rows

The unique highest complete table is operative; every earlier table is historical. Every round24 row is retained verbatim, including its pinned values and its write scope; round25 adds the two round-25 claim instruments and changes no earlier row. A self-test flag is resolved against the committed tool source at the bound revision, not against this prose.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
<the 26 rows of SKILL.md:2260-2285, unchanged>
| self-assessment | gate | `python3 tools/check-self-assessment.py --revision <REV>` | 0 all 23 fixed checks match;1 one or more mismatches;2 could-not-evaluate | `python3 tools/check-self-assessment.py --selftest` | R25 fixed K01-K23 check set read at the bound revision; measured self-assessment only, not host state | immutable Git reads; selftest in-memory fixtures | tsukuroi |
| memory-pressure | gate | `python3 tools/check-memory-pressure.py --revision <REV>` | 0 six rows MP1-MP6 verified;1 row or evidence invalid;2 could-not-evaluate | `python3 tools/check-memory-pressure.py --selftest` | R25 fixed MP1-MP6 rows, capture sha256 e60f1bbc and per-row source, quote and pointer rules; committed evidence only, not a host re-measurement | immutable Git reads; selftest in-memory fixtures | tsukuroi |
```

The 26 retained rows must be copied as committed bytes. Re-emitting them through a Markdown table writer is safe only because `_split_table_row` keeps the backslash of an escaped pipe, but a byte copy from `SKILL.md:2260-2285` is what "retained verbatim" means and is what the round-24 preamble promises.

## 6. Evidence: the recommended shape passes, the plausible wrong shapes fail

[obs] Baseline measurement at the claim base. Command `python3 tools/check-registry-coverage.py --revision b9046016831237cd04d38da11ba76e50d5380c53 --audit-live-map`, exit 0, output excerpt: `{"counts":{"audit_live_map_errors":0,"findings":0,"missing":0,"registered":26,"rows_total":26,"tools_total":26},"status":"PASS"}`. The registry is green before round 25 and the only gap the two new files can open is coverage.

[obs] I built a scratch git repository under `/fast/scratch/hyaku/tsukuroi-r25/ScoutRegistryFormat/fixture` from `git archive b9046016831237cd04d38da11ba76e50d5380c53 SKILL.md tools/`, imported the real `check-registry-coverage.py` as a module, pointed its `ROOT` at the fixture (the same technique its own `selftest` uses) and invoked its `main` on fixture commits. Results, each run with `--audit-live-map`:

| Fixture shape | Exit | Counts | Findings |
|---|---|---|---|
| Base tree, 26 tools | 0 PASS | 26/26 rows | none |
| Section headed `— round25 superseding current rows`, 26 rows verbatim plus the two new rows, 28 tools | 0 PASS | `tools_total 28, rows_total 28, registered 28, missing 0` | none |
| The same, plus `--baseline-tools` on a 26-tool parent commit | 0 PASS | `discovered_tools ["tools/check-memory-pressure.py","tools/check-self-assessment.py"], baseline_tools_missing 0` | none |
| Section headed `— round25 additions` with only the two new rows (the wording in the `DraftSkillTable` dispatch item) | 1 FAIL | `rows_total 26, tools_total 28, missing 2` | `REGISTRY-ROW-MISSING` for each new tool |
| Section headed correctly but holding only the two new rows | 1 FAIL | `rows_total 2` | 27 findings, 26 `REGISTRY-ROW-MISSING` plus `REGISTRY-AUDIT-LIVE-MAP` |
| Correct rows, one blank line inserted after the twentieth row | 1 FAIL | `rows_total 20, missing 8` | `REGISTRY-ROW-MISSING` for the six dropped rows and both new tools |
| New row whose entry cell names `check-self-assessment.py` and whose self-test cell names `check-memory-pressure.py` | 1 FAIL | 28/28 | `REGISTRY-ROW-AMBIGUOUS` plus `REGISTRY-ROW-DUPLICATE` |
| New row publishing `--selftest` over a tool source that lacks that literal | 1 FAIL | 28/28 | `REGISTRY-SELFTEST-UNRESOLVED` |
| New row publishing `--self-test` over a source that defines `--selftest` | 1 FAIL | 28/28 | `REGISTRY-SELFTEST-UNRESOLVED` |
| Two round-25 headings | 2 CANNOT_EVALUATE | — | `E-REGISTRY-TABLE` |
| A new row with a raw pipe inside the verdict cell, giving nine cells | 2 CANNOT_EVALUATE | — | `E-REGISTRY-TABLE` |

[obs] Fixture commits: `982a973` (additions heading), `5dc1da2` (correct heading, 28 rows), then `P`/`Q` for the baseline comparison. These are scratch commits outside the lane and are not evidence in the lane sense; the checker's verdict is the evidence.

[inf] The `DraftSkillTable` dispatch item (`.ufo/waves/round-25/w1-spec.json`, item name `DraftSkillTable`) asks for a section headed `## Gate and probe registry — round25 additions`. That heading does not match `:23-24`, so the round-24 table would stay operative and the audit would report two `REGISTRY-ROW-MISSING` findings — before any question of missing rows arises. If the integrator pastes that draft as the operative section, the audit is red. The drafted content is still useful as a source of the two rows.

## 7. Obligations from PROTOCOL and interactions with the rest of the edit

[obs] PROTOCOL's registry rule at `/home/vgpnk/Projects/shokunin/PROTOCOL.md:398-406` fixes the same eight row fields and states that a child lane's registry home is its own `SKILL.md`; the appendix row at `/home/vgpnk/Projects/shokunin/PROTOCOL-APPENDIX.md:51` records why main-repo lanes use `SCORECARD.md` instead. Tsukuroi is a child lane, so `SKILL.md` is the correct home and no `SCORECARD.md` registry section is needed.

[obs] PROTOCOL's Delivery bullet at `PROTOCOL.md:420-421` says closure grades no gate conformant until its registry row exists at that home, so both rows are mandatory for C1 and C2 to count as conformant instruments, not just for the coverage audit.

[obs] PROTOCOL's Self-test and Two-evidences bullets at `PROTOCOL.md:389-397` add two obligations the coverage checker does not enforce: each tool needs a real fixture-based self-invocation mode, and a gate whose verdict depends on a mutable fleet artifact needs a frozen run whose `expected.json` pins the digest of every snapshot input. For `check-memory-pressure.py` the natural pin is the capture sha256 `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136`, which belongs in that row's pinned-values cell; for `check-self-assessment.py` the pin is the fixed K01-K23 check set in the round-25 `SCORECARD.md` declaration.

[obs] C1 check K09 reads `N table lines` as the count of `SKILL.md` lines that start with `|` (`SCORECARD.md:794`), and K08 reads the `wc -l` count. At the claim base those are 259 and 2301 (`grep -c '^|'` and `wc -l` on `git show b9046016:SKILL.md`). The round-25 registry section adds 30 pipe lines (header, separator, 28 rows) and the C2 decision table adds 8 (header, separator, 6 rows), so whichever edit lands last must leave the axes-table counts at the final numbers or K08 and K09 mismatch. Registry formatting is therefore coupled to the C1 target and cannot be integrated after the self-assessment measurement without re-measuring.

[obs] No other committed tool parses the gate registry. `grep -l "Gate and probe registry" tools/*` returns only `check-registry-coverage.py`; `check-freshness-r17.py`'s `--registry-from` refers to its JSON source/notice registry, and `check-appended-notices.py` treats `SKILL.md` only as an allowed notice-bearing path (`tools/check-appended-notices.py:82-90`).

[obs] Neither `tools/check-self-assessment.py` nor `tools/check-memory-pressure.py` existed in the lane worktree or in the two executor clones when I read them (`ls tools/` listed the same 26 files; `/fast/scratch/hyaku/tsukuroi-r25/ExecSelfAssessTool/repo/tools/` and `.../ExecMemPressureTool/repo/tools/` also listed 26 files). Their CLI shapes are therefore taken from the round-25 declaration and the dispatch items, not from source.

## 8. Remaining unknowns

[unk] Whether both new tools will define the flag as `--selftest` exactly. The registry row must copy whatever they define.
[unk] Whether `check-self-assessment.py` will return 2 for a read/revision failure and 1 only for a real mismatch. Its row's verdict map must describe its actual exit codes, or the map is misleading even though the checker accepts any text containing 0, 1 and 2.
[unk] Whether the two tool commits and the `SKILL.md` edit will land in one revision. If they land in separate commits, the audit is only green at the later of them, and C1's measured revision must be that later commit.

Scope: read=tsukuroi-shokunin SKILL.md (2240-2261, 2284-2292), SCORECARD.md (784-812), tools/check-registry-coverage.py (full logic 1-360, 357-415, 428-620), tools/_revision.py (bind/branch_tip greps), tools/check-appended-notices.py (69-103), tools/check-freshness-r17.py and tools/check-adjacency-anchors.py (greps), corpus/lessons/round-24-verifier-spotcheck.md (whole), .ufo/waves/round-25/w1-spec.json (items), fleet PROTOCOL.md (389-418 plus greps), PROTOCOL-APPENDIX.md (51); wrote=.ufo/waves/round-25/w1/ScoutRegistryFormat.md and scratch fixtures under /fast/scratch/hyaku/tsukuroi-r25/ScoutRegistryFormat/; executed=git ls-tree, git archive, git show, git log-free read-only queries, python3 tools/check-registry-coverage.py --revision b9046016831237cd04d38da11ba76e50d5380c53 --audit-live-map (exit 0), and a python harness importing the real checker and running its main() against the scratch fixture repository (exit codes 0, 1 and 2 as tabulated), wc and grep counts
Model: opencode-go/deepseek-v4.1-flash
Installs: none
