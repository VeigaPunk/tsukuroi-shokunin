# FxC1Table — falsification of the table-extraction leg of the C1 edit-contract check

Seat: `TsukuroiR23-2.FxC1Table-2` (FALSIFY wave, round 23, attempt 1).
Target under attack: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/candidate/tools/check-edit-contract.py`
Landed-copy root under attack: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/candidate/`

## 0. Attacked claim

**C1 (preregister `claims[0]`, axis `depth`, metric `validated_edit_decisions`, before 0, target 8)** — "Eight finite source-grounded structured-edit authority decisions; new document contract, not eight repaired runtime behaviors."

I attack **C1's prose/source leg only**, i.e. the two checks that make the metric a claim about a *visible document* rather than a self-consistency check between three byte-identical copies of one list:

* `check-edit-contract.py:148-152` — for each of the eight expected tuples, `matches = [r for r in cells if r and r[0] == ident]` must equal exactly `[list(expected)]`, where `cells = table_cells(text)` and `text` is `corpus/knowledge/structured-edit-r23.md`.
* `check-edit-contract.py:137-140` — the `S086` source row must be found in `corpus/SOURCES.md` with exactly 11 cells, path `…/structured-edit-observations.json`, `['own-work','A']`, status `mined`, no backslash in any cell.

I do **not** attack C2 (schema-v2 edit audit authority) or C3 (path-census ledger); those are separate seats' targets. I do **not** claim any native runtime enforcement, and I make no claim about the tool's *exit status on the landed revision* — see §5 (no execution).

## 1. Method and its limits

* Read-only. I used `read` and `grep` only (see the scope disclosure below for the single exception). **No command was executed** (no bash, no python, no import, no compile, no test, no lint, no hash, no `wc`, no `ls`). The declared SHA-256 is treated as supplied identity and was **not** independently computed.
* Every statement below is **static analysis by inspection of the source text**, with `path:line` citations. Where I say "yields", I mean "the code path yields, by reading" — I did not observe a run.
* Markdown semantics are stated as **GFM/CommonMark rules** (a table needs a header row *and* a delimiter row; a table is broken at the first blank line; a 4-space indent is an indented code block only when it is 4 spaces beyond the enclosing container's content indent; inline code spans are literal text, not HTML). Those are the rules the tool's own docstring at `check-edit-contract.py:46` disclaims ("Finite Markdown table carrier rules, not a general rendered-prose theorem") — so where a divergence appears, the finding is about the **gap between the carrier rule and what the artifact and the metric name claim**, not a claim that the tool promised a renderer.
* Files read: `candidate/tools/check-edit-contract.py`, `candidate/corpus/knowledge/structured-edit-r23.md`, `candidate/corpus/knowledge/structured-edit-r23.json`, `candidate/corpus/SOURCES.md`, `.ufo/waves/round-23/preregister.json`, `.ufo/waves/round-23/sources/structured-edit-observations.json`.
* **Scope disclosure.** One `grep` was issued over the whole `.ufo/waves/round-23/` tree rather than over the declared read paths only. Its purpose was to settle a suspected word-level divergence in the `UNDECLARED_EDIT` reason string across the three copies of that list, after a non-raw read of the knowledge Markdown had rendered the cell as "ownership" while a targeted grep rendered it as "permission". The tree-scoped grep returned, besides the declared files, matches under `.ufo/waves/round-23/build/` (round-23 build-seat notes) and `.ufo/waves/round-23/sources/edit-decision-policy.json`. I did not open those files, did not use any of their content in a finding, and the divergence they showed is recorded above as **not present**. Every other grep and read in this seat was confined to the declared read paths, to the report's own directory (one directory listing, to check whether a file of mine already existed), and to this report file.

## 2. Findings by severity

### F1 — HIGH — the landed `SOURCES.md` registry table ends at S064; the S086 "row" the tool certifies is not a table row

**Evidence (landed defect, not hypothetical).**

* `candidate/corpus/SOURCES.md:5` header `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`; `:6` delimiter `|---|…|`.
* `:7`–`:70` — rows `S001`…`S064`, contiguous, no blank line between them.
* `:71` — **a single blank line**, the only blank line anywhere inside the registry region (bounded grep for `^$` over the file returns 2, 4, **71**, 94, 96, 101, 103, 105, … — 71 is the only one between the header and the last row).
* `:72`–`:93` — rows `S065`…`S086`, contiguous, **with no header row and no delimiter row**.
* `:93` is the S086 row: `| S086 | Structured edit request metadata and adapter steps — .ufo/waves/round-23/sources/structured-edit-observations.json | own-work | A | … | mined | 2026-10-21 | on-release | corpus/knowledge/structured-edit-r23.md, corpus/lessons/round-23.md |` — 11 cells.

**Why it is wrong.** GFM breaks a table at the first empty line, and a table requires a single header row plus a delimiter row. The blank line at `:71` therefore terminates the registry table at `S064`; the block `:72`–`:93` has no delimiter row, so it is **one paragraph of pipe-bearing text, not 22 registry rows**. The rendered `corpus/SOURCES.md` registry contains 64 rows and **no S086 row**.

`check-edit-contract.py:137` selects the source row with `found = [r for r in table_cells(source_text or '') if r and r[0] == 'S086']`, and `:138-139` validates its cell count, path, `kind`/`tier` (`['own-work','A']`), `status` (`mined`) and backslash-freeness. `table_cells` (`:77-93`) has **no notion of a table at all** — it accepts any pipe-bearing line — so it accepts the paragraph line at `:93` as "the S086 registry row" and emits no `EDIT-SOURCE` finding.

**Consequence for C1.** The `EDIT-SOURCE` leg is the only check that ties the eight decisions to a *registered* source with a declared tier and status. As landed, it certifies a paragraph line as a registry row. The round-23 knowledge note's header (`structured-edit-r23.md:1`, "source: S086 — .ufo/waves/round-23/sources/structured-edit-observations.json") and the SOURCES "Registry" section therefore do not, in the rendered document, contain an S086 registry entry at all. The S086 row is also the row the *preregister* names as the opened source for C1 (`preregister.json` `sources_opened[1]`).

**Smallest in-scope remedy (one line, corpus side).** Delete the blank line at `candidate/corpus/SOURCES.md:71` so the registry is one contiguous 11-column table `S001`…`S086`. (The blank line predates round 23 — it arrived with the round-18 `S065` row — but round 23 is the first wave whose tool depends on the S086 row being a *registry* row, so round 23 inherits it.) **Tool side, for the class rather than the instance:** make `table_cells` require a header row and a delimiter row before accepting a row as a table row, and require the S086 row to come from a table whose header cell is `id`.

**Note on the preregister/SOURCES cross-check.** `preregister.json` `edit_decisions[1]` is `["UNDECLARED_EDIT","DENY","No implicit edit permission from generic report ownership"]`; `candidate/corpus/knowledge/structured-edit-r23.json:14` and `candidate/corpus/knowledge/structured-edit-r23.md:16` both carry the identical string "No implicit edit permission from generic report ownership", matching `check-edit-contract.py:22`. (An earlier non-raw read of the Markdown rendered that cell as "No implicit edit **ownership** from generic report ownership"; a targeted `grep` of the file and a second raw read of `:13-24` both show "**permission**". The word-level divergence I first suspected is **not** present — recorded here so no other seat re-chases it.)

### F2 — HIGH — the eight decisions can be certified with no table in the document at all

**Evidence.** `table_cells` (`:77-93`) treats *any* line containing `|` as a row:

* `:85` — `if '|' not in line: continue` is the only content filter.
* `:87` — `cells = line.split('|')`; `:88-91` drop the leading/trailing empty elements; `:92` strips each cell.
* There is **no** header-row requirement, **no** delimiter-row requirement, **no** blank-line/paragraph-break handling, and **no** setext handling anywhere in the file.

**Falsifier (static).** In `candidate/corpus/knowledge/structured-edit-r23.md`: delete the delimiter row at `:14` (`|---|---|---|---|---|`) and append a line `===` after `:22`.

* Effect on the tool: the delimiter row's first cell is `---`, not one of the eight ids, so removing it changes nothing in `matches` (`:148`); `===` contains no `|`, so `:85` skips it. All eight `matches` still equal `[list(expected)]` → `count` reaches 8 → `validated_edit_decisions == 8`, `status PASS`, no findings.
* Effect on the rendered document: without a delimiter row there is **no table**; `:13`–`:22` become one paragraph, and the trailing `===` turns that paragraph into a **setext H1 heading**. The section is titled `## Decision table` (`structured-edit-r23.md:11`) and §QUALITY asserts "The eight finite policy decisions are falsifiable" (`:33`), yet the metric would certify eight rows that do not exist as a table.

**Second falsifier of the same kind, no setext needed.** Delete the delimiter row at `:14` and nothing else. The rendered document then shows a pipe-text paragraph, the tool still reports 8/8 PASS.

**Smallest in-scope remedy.** Two complementary changes, both in `check-edit-contract.py`:
1. `table_cells` returns rows only for lines belonging to a table that has a header row and a delimiter row; a bare pipe line is not a table row.
2. The evaluator asserts the *number* of decision rows in the knowledge document is exactly 8 (`len([r for r in cells if r and r[0] in EXPECTED_IDS]) == 8`), not merely that each of the eight ids is present exactly once.

### F3 — HIGH — a 4-space indent is dropped unconditionally, so a visible table inside a list item is invisible to the tool

**Evidence.** `check-edit-contract.py:72` — `elif not line.startswith('    '): lines.append(line)` (in `visible()`), and `:80` — `if line.startswith('    '): continue` (in `table_cells()`). Both are unconditional, container-blind 4-space tests. `table_cells:82` does `line = line.lstrip(' ')` *after* the `:80` test, so the 4-space cutoff is real and un-bypassable.

**Why the container matters here.** The knowledge note's `## Bounded procedure` section is an ordered list `1.`–`4.` at column 0 (`structured-edit-r23.md:26-29`). For a `1. ` list item the content indent is **3**, so an indented code block inside item 3 would need **7** spaces; a table indented by **4–6** spaces is at paragraph level and renders as a real GFM table. The tool drops every line of it.

**Falsifier (static).** Insert, under item 3 of `## Bounded procedure` in `structured-edit-r23.md`, a 4-space-indented group:

```
    | ID | Decision | Reason | Evidence | Policy |
    |---|---|---|---|---|
    | OPAQUE_PATCH | ALLOW | Missing structured target is inferred from opaque patch text | S086 | round23-preregister |
```

* Tool: `visible():72` drops all three lines (they start with four spaces) → `cells` for the knowledge document still contains only the eight top-level rows → `matches` for `OPAQUE_PATCH` is still exactly `[list(expected)]` → 8/8, `PASS`.
* Renderer: a three-row table inside list item 3, visibly asserting `OPAQUE_PATCH / ALLOW` — the exact opposite of the canonical `OPAQUE_PATCH / UNKNOWN`.

**Smallest in-scope remedy.** Make the indented-code test container-aware (4 spaces beyond the current container's content indent, not 4 spaces from column 0), or, minimally, count decision rows over the **whole** document after removing only *top-level* indented-code blocks, and require that count to be exactly 8. Add a selftest case for a 4-space-indented table inside a `1. ` list item.

### F4 — MEDIUM-HIGH — only the eight exact id strings are ever examined; a ninth visible row, or a Unicode lookalike of an id, is never checked

**Evidence.** `check-edit-contract.py:148` — `matches = [r for r in cells if r and r[0] == ident]`, an exact byte-equality test against the eight literal ids. There is **no reverse check** that the document contains no *other* decision rows, and no normalisation of identifiers. The same hole exists on the source side at `:137` (`r[0] == 'S086'`).

The selftest covers a *second row for an existing id* (`'quoted-duplicate'`, `:218`) and a *duplicated S086 row* (`'source-duplicate'`, `:226`), but **no case adds a row whose first cell is not one of the eight ids**, and no case uses a lookalike id.

**Falsifier (static), two variants.**

1. Add a ninth visible row to the knowledge table, e.g. `| EDIT_ANY_TARGET | ALLOW | Every target is predeclared | S086 | round23-preregister |`. `r[0] == ident` is False for all eight ids, so the row is never examined; `count` stays 8; `PASS`. The published document now carries a ninth decision that no control in the tool or the selftest can see.
2. Add a lookalike row using Cyrillic `Е` (U+0415) in place of the ASCII `E`:
   `| DECLARED_ЕDIT | ALLOW | Exact target is predeclared for edit and for both read and write | S086 | round23-preregister |`
   The id is byte-different from `DECLARED_EDIT`, so it is not matched by any of the eight `matches` filters → 8/8 `PASS`. But to a human reader — and to any screenshot, diff, or copy-paste review — this row is visually indistinguishable from the genuine `DECLARED_EDIT` row, so the contradiction is invisible to review and to the tool simultaneously. The same construction on the source side (`S08６` with a fullwidth digit, or `S086` with a U+00A0 no-break space) defeats the `EDIT-SOURCE` check at `:137-139` without changing a single byte the check looks at.

**Smallest in-scope remedy.** After the per-id loop, add a completeness assertion: the set of first cells of all rows in the knowledge document that *look like* a decision id (i.e. match `^[A-Z][A-Z0-9_]*$` or that differ from an id only by non-ASCII code points) must be exactly the eight ids, and any such row must be one of the eight expected tuples. On the source side, assert that exactly one row in `corpus/SOURCES.md` has a first cell that normalises to `S086`.

### F5 — MEDIUM — HTML comment stripping is a raw text scan, not Markdown-aware: a `<!--` inside an inline code span silently hides every later visible row

**Evidence.** `check-edit-contract.py:54-68` strips `<!--`/`-->` wherever they occur on a line, and the `comment` flag (`:47`) persists across lines. The scan runs **before** any block classification (fence detection is at `:69`, after the strip), and there is **no code-span awareness**. In CommonMark a code span is literal text: `` `<!--` `` does not open an HTML comment.

**Falsifier (static).** In `structured-edit-r23.md`, after the existing table (`:22`), add a paragraph that contains the inline code `` `<!--` ``, and after it a second table whose `OPAQUE_PATCH` row says `ALLOW`:

* Tool: the scanner opens a comment at the inline code and never encounters a `-->`, so the whole second table is dropped from `visible()` → `matches` for `OPAQUE_PATCH` is still exactly the one good top-level row → 8/8, `PASS`.
* Renderer: the code span is literal; the second table is fully visible and asserts the opposite of the canonical decision.

The selftest's `'hidden'` case (`:216`, `'<!--\n' + prose + '\n-->'`) covers only the *well-formed whole-document wrap*; there is no case where a comment opens **after** the good rows and swallows a later contradiction. The `'hidden-limit'` case (`:221`) likewise only wraps the limit sentence.

**Smallest in-scope remedy.** Make the comment scanner skip inline code spans (and, at minimum, treat `<!--` inside backtick runs as literal), plus a selftest case with a comment opened *after* the decision table.

### F6 — MEDIUM — CRLF: the fence-close regex rejects `\r`, and a trailing pipe plus CRLF injects a phantom empty cell

**Evidence.** `:48` `for line in text.split('\n')` leaves a trailing `\r` on every line of a CRLF file. `:51` `re.fullmatch(r' {0,3}' + re.escape(marker) + '{' + str(length) + r',}[ \t]*', line)` — `\r` is not in `[ \t]*`, so **a closing fence in a CRLF file never matches**. `:90` `if line.endswith('|')` is then False for a CRLF line, so `:87` `line.split('|')` leaves a trailing `'\r'` element, which `:92`'s `.strip()` turns into `''`.

**Consequences (static).**

* *Fail-closed (false alarm).* In a CRLF copy of the knowledge document, every pipe-terminated row gains a phantom sixth cell → `matches != [list(expected)]` for all eight ids → eight `EDIT-DECISION-MISMATCH` findings and `validated_edit_decisions == 0`; the S086 row becomes 12 cells → `EDIT-SOURCE`. A document byte-identical to the passing LF document except for line terminators fails. Same for two trailing spaces after a final pipe (`:90`) and for a `\|` inside a cell (`:87` splits on the escaped pipe too).
* *Hide direction.* In a CRLF file the tool's fence never closes, so **every row after the first fenced block is dropped from the tool's view**, while a renderer (which strips the CR before parsing) closes the fence normally and shows those rows. A contradictory table placed after a fenced block is therefore invisible to the tool and visible to the reader.

**Bounded search that found nothing.** `grep '[ \t]+$'` over `candidate/corpus` → **no matches**; the landed corpus is LF with no trailing whitespace. `grep` for the eight ids over `structured-edit-r23.md` → exactly 8 hits, at lines 15–22, one per id, none in prose. `grep` for `\|` over the same file → hits only at lines 13–22, so no prose line in the note can be mistaken for a row. The landed S086 row has exactly 11 cells. **F6 is latent, not a landed mis-scoring.**

### F7 — LOW-MEDIUM — the selftest has no carrier case for any of the named attack vectors except the whole-document wrap

**Evidence.** The selftest's carrier-related cases are exactly: `'hidden'` (`:216`), `'fenced'` (`:217`), `'quoted-duplicate'` (`:218`), `'limit-omitted'` (`:219`), `'hidden-limit'` (`:221`), `'source-missing'` (`:222`), `'source-wrong-path'` (`:223`), `'source-wrong-tier'` (`:224`), `'source-rejected'` (`:225`), `'source-duplicate'` (`:226`), plus the eight `table-<i>` cell renames (`:203`) and the eight per-field JSON mutants (`:202`).

**Absent:** indented (4-space) tables; CRLF; trailing spaces after the final pipe; escaped `\|`; setext; nested blockquotes (`>>`); a comment opened *after* the decision table; a second table in the same document; a row with a non-listed or lookalike id; a table with no header/delimiter row. The knowledge note's own §QUALITY (`:33`) requires controls that "check every row, source/policy mapping and refusal class" — the eight-row completeness property (F2/F4) is exactly the property with no control.

**Smallest in-scope remedy.** Add the missing carrier cases as literal fixtures, in the same style as the existing ones (never synthesised from `EXPECTED`): (a) table without a delimiter row; (b) 4-space-indented table inside a `1. ` list item; (c) comment opening after the decision table; (d) ninth row with an unknown id; (e) lookalike id; (f) CRLF copy; (g) trailing-space and escaped-pipe rows. Each must assert the *expected* outcome, which for (a)–(e) is **not** a silent PASS.

### F8 — LOW — setext and blockquote are false-alarm / false-accept directions, not hides (bounded negative results)

* **Setext.** `visible()` has no setext handling, so a setext underline never *removes* a row from the tool's view; a pipe-bearing line followed by `===` is a heading in the renderer but a row to the tool. That direction is fail-closed (a contradictory setext line yields a second match → `EDIT-DECISION-MISMATCH`). The only setext-shaped *false accept* is the positive-direction one already reported as F2 (the tool certifies 8/8 for content that renders as a setext heading).
* **Blockquotes.** `:83-84` — `while line.startswith('>'): line = line[1:].lstrip(' ')` — strips blockquote markers with no depth limit and no container tracking, so a quoted row is counted as a top-level row. A contradictory row in a blockquote is *caught* (two matches for that id → `EDIT-DECISION-MISMATCH`), so this is not a hide; the residual is a false accept in the other direction: the document's only decision table may sit inside a blockquote (`> | ID | Decision | … |`) and still satisfy the check, while the `## Decision table` section contains no table.
* **Nested blockquotes (`>>`).** Both the renderer and the tool count the row, so they agree; the tool is stricter only in that it treats a quoted row as equivalent to a top-level one.

## 3. Bounded searches that found nothing (negative results, stated as such)

1. `grep '[ \t]+$'` over `candidate/corpus` → no matches. No trailing whitespace anywhere in the landed corpus; the trailing-space false alarm of F6 is latent.
2. `grep` for the eight decision ids over `candidate/corpus/knowledge/structured-edit-r23.md` → exactly 8 hits, one per id, at lines 15–22. No id occurs in prose, so the `matches == [list(expected)]` filters are not currently tripped by a prose mention.
3. `grep` for `\|` over the same file → hits only on lines 13–22. No prose line in the knowledge note can be mistaken for a table row today.
4. `grep` for `^$` over `candidate/corpus/SOURCES.md` → the only blank line inside the registry region is line 71 (F1); there is no second break that would further fragment the registry.
5. `grep` for `^\| S08[0-9] \|` over `candidate/corpus/SOURCES.md` → S079 at 86 … S085 at 92, S086 at 93, contiguous with no blank line among them; the S065–S086 paragraph block is a single contiguous run.
6. Word-level check of the `UNDECLARED_EDIT` reason across `preregister.json:65`, `candidate/corpus/knowledge/structured-edit-r23.json:14`, `candidate/corpus/knowledge/structured-edit-r23.md:16` and `check-edit-contract.py:22` → all four read "No implicit edit **permission** from generic report ownership". No divergence.

## 4. What the landed state actually does, and does not, establish

* The landed knowledge note is, for the tool's carrier rules, well-formed: a 5-column table with header, delimiter and exactly eight rows, each matching the expected tuple; each id appears once; no fences, no HTML comments, no trailing whitespace, no escaped pipes, no stray pipe-bearing prose. `PROSE_LIMIT` ("It is not native permission enforcement", `:31`) is present as plain prose and survives `'\n'.join(visible(text))`.
* The landed `SOURCES.md` is **not** a single registry table: the table ends at `S064` (line 70) and `S065`–`S086` (lines 72–93) are a paragraph. The tool cannot see this difference, and the S086 row it certifies is inside the paragraph region (F1).
* The tool's own limits are honest about the narrow part: `:46` ("not a general rendered-prose theorem"), `:29` `LIMIT` ("Declared audit authority for structured target metadata only; no native prevention, opaque patch interpretation, effect or reading proof."), and the `PROSE_LIMIT` string. What is **not** honest is the metric name `validated_edit_decisions` and the artifact's own wording: the section is titled `## Decision table` (`structured-edit-r23.md:11`) and §QUALITY (`:33`) claims the eight decisions are "falsifiable" with controls that "check every row". As implemented, the check certifies that eight specific tuples appear as pipe-delimited text in the file — it does not certify that the file contains an eight-row decision table, that it contains *only* those eight decisions, or that the S086 source is a rendered registry row.

## 5. Residual risk and verification gaps

* **No execution.** Every finding is static. I did not run `check-edit-contract.py --selftest` or `--revision`, did not compute the digest, and did not verify the tool's exit code on revision `5a25c88b…`. The predicted landed-state outcome (F1 notwithstanding, `validated_edit_decisions == 8`, exit 0) is an inference from the code path, not an observed run. A falsify seat with execution rights should run the tool at the landed revision and at each F1–F5 falsifier and compare against the predictions.
* **Renderer dependence.** F2, F3, F5 and the SOURCES half of F1 assume GFM/CommonMark semantics (table needs header+delimiter; table breaks at a blank line; list content indent 3 for `1. `; inline code spans are literal). I did not render the documents (no execution). If the lane's renderer differs, F1 remains valid independent of any renderer (a paragraph is not a table under any Markdown reading), while F2/F3/F5 would need re-stating against that renderer.
* **Pre-existing corpus scope.** The blank line at `candidate/corpus/SOURCES.md:71` predates round 23. I flag it because round 23's `EDIT-SOURCE` leg is the first check to depend on the S086 entry being a *registry* row; removing it edits a corpus file, which is L1's call, not a falsify seat's.
* **Untested in this seat:** the `evidence_ok` leg (`:100-113`) and the `EXPANSION`/`OPAQUE_PATCH` semantics of the eight decisions themselves — those belong to the per-decision seats (`FxC1DeclaredEdit`, `FxC1UndeclaredEdit`, `FxC1ReadOnlyEdit`, `FxC1WriteOnlyEdit`, `FxC1OpaquePatch`, `FxC1EditTraversal`, `FxC1EditExternal`, `FxC1Expansion`), not to the table-extraction attack. I make no claim about their verdicts.
* **Not claimed anywhere in this report:** native runtime enforcement, sandboxing, patch/body interpretation, proof of reading or of effects, recorder completeness, or host/package/service/boot authority. The task API still exposes no restrictive per-seat allowlist.

## 6. Smallest in-scope remedy, consolidated

1. **Corpus (one line, L1):** delete the blank line at `candidate/corpus/SOURCES.md:71` so the registry is one contiguous 11-column table including S086. *(F1)*
2. **Tool (two assertions, `check-edit-contract.py`):**
   * `table_cells` must require a header row + delimiter row before treating a line as a table row, and must break a table at a blank line. *(F1, F2)*
   * The evaluator must assert that the knowledge document contains **exactly eight** decision rows and that their ids are exactly the eight expected ids — not merely that each id appears once. *(F2, F4)*
   * Make the indented-code test container-aware and make the HTML-comment scan code-span aware. *(F3, F5)*
   * Normalise/reject non-ASCII lookalike ids on both the decision side and the S086 side. *(F4)*
   * Tolerate CRLF and trailing spaces in row framing (strip a trailing `\r`; trim before the trailing-pipe test; treat `\|` as a literal pipe). *(F6)*
3. **Selftest (7 literal fixtures):** no-delimiter-row table; 4-space table inside a `1. ` list item; comment opened after the decision table; ninth row with an unknown id; lookalike id; CRLF copy; trailing-space / escaped-pipe rows. *(F7)*
4. **Wording (one line, artifact):** either rename the metric to something carrier-accurate (e.g. `validated_edit_carriers`) and say so in §QUALITY, or implement (2) so that "decision table" and "validated_edit_decisions" are literally true. *(§4)*

    Reviewed-SHA256: 620f3e5bad34c4ba77a0f0e458bedd79cb05b04a5b1d90200c0baf60038e5081
    Predicate: r23f-fxc1table
    Scope: executed=none
    Lane bounds: leaf member — no subagent dispatch.
