# FxC1Table — falsify `check-boundary-contract.py`

Godspeed axes: **depth** (does the visible-table gate actually bind table decision/source to EXPECTED), **calibration** (expected fixture verdict vs statically derived runtime, kept separate; no execution), **operability** (bounded, line-cited hold/counterexample statements usable by C1 integration).

## Target identity

- File: `.ufo/waves/round-22/candidate/tools/check-boundary-contract.py` (working-tree candidate, 175 lines, read in full via declared read_paths today 2026-10-21).
- Claimed SHA256 `1b91a7c10c971b554bad144035b40d0b7054e06582093f9f851ac0fcafdd2485`: **not recomputed** — NO-EXEC seat; hash tools are commands. Identity rests on the assignment line.
- Predicate under attack: right JSON (`corpus/knowledge/seat-boundary-r22.json`) but wrong *visible table* decision/source in the prose must be **rejected**.

## Gate mechanics (source-cited)

- `EXPECTED` six tuples incl. `source` field: lines 19–26; `LIMIT` line 27.
- `visible()` (lines ~39–53) drops HTML-comment lines and fenced blocks; it does **not** model Markdown table semantics — every surviving line is returned raw (indentation preserved).
- `evaluate()` lines 84–104:
  - source rows: `source_rows = [... for line in visible(source_text)]` — **no** `startswith('|')` filter.
  - decision table: `cells = [... for line in visible(text) if line.startswith('|')]` — filter on the **unstripped** line.
  - per id: `correct` = JSON row tuple equals EXPECTED; `matches = [r for r in cells if r and r[0] == ident]`; reject unless `matches == [list(expected)]` (exactly one row, five cells, byte-equal after `strip()`). Cite lines ~93–101.
- Independent gates: SOURCES.md row shape (`BOUNDARY-SOURCE`), host fields (`BOUNDARY-HOST-LIMIT`), scope/limit phrase (`BOUNDARY-LIMIT-MISSING`).

## Finding F1 — MEDIUM: indented duplicate row defeats the visible-table gate (predicate falsified in this variant)

`cells` drops any `|`-line with leading whitespace (unstripped `line.startswith('|')`), while GitHub-flavored Markdown renders a `|`-row indented by 1–3 spaces as a normal table row (4+ spaces would be an indented code block, which is genuinely not a table). A forged **additional** row for an existing id therefore renders in the document but never enters `cells`.

Counterexample shape (prose bytes; JSON canonical):

    | NO_EXEC | bash/eval/task | DENY | No execution or delegation in source-only seats | S083 |
      | NO_EXEC | bash/eval/task | ALLOW | forged reason | S083 |

(second line indented two spaces, adjacent to the table, no blank line). Rendered table shows NO_EXEC twice, second occurrence decision/source wrong.

- Expected fixture verdict (what the predicate demands): **reject** — exit 1, `BOUNDARY-DECISION-MISMATCH` on `NO_EXEC`, `validated_boundary_decisions: 5`.
- Statically derived observed runtime (line trace, not executed): `visible()` passes both lines; `cells` keeps only the column-0 row; `matches == [list(expected)]` and `correct` is true → `count = 6`, `code = 0` → **`status: PASS`, exit 0**. Right JSON, wrong rendered table, checker accepts.
- Bounded: outright replacement, mutation, fencing, commenting, duplication at column 0, extra/missing cells, unicode/case tricks are all still rejected (see hold below). The gap requires a *duplicate id row* indented 1–3 spaces; the canonical row must remain byte-exact. Selftest (`:106–133`) has `wrong-table`, `hidden`, `fenced` fixtures but **no indented-duplicate fixture**, so the gap is untested by the tool's own suite.
- Minimal remedy (recommendation only; no production edits from this seat): compare on `line.lstrip().startswith('|')` so indented rows enter `cells` (4+-space code-block rows then over-match → fail-closed, acceptable), and/or add an indented-duplicate negative fixture.

## Bounded hold — variants that ARE rejected

1. Wrong decision or source in the single canonical row → `matches != [list(expected)]` → `BOUNDARY-DECISION-MISMATCH`, exit 1 (selftest `decision-{i}`, `reason`, `surface`, `source`, `wrong-table`).
2. Table only inside a fence or HTML comment → `visible()` hides it → `matches == []` → reject (selftest `hidden`, `fenced`).
3. Column-0 duplicate row (right + wrong) → two matches → reject.
4. Cell-count games (escaped pipe, extra column) → length differs → reject; NBSP/zero-width inside cells survives `strip()` → byte inequality → reject.
5. `visible()` desync attempts all land fail-closed: 4-backtick opener closed by 3-backtick run makes visible() *over-close* (reveals more rows → stricter); fence markers inside comments or 4-space-indented fences make it *over-hide* (matches go missing → reject). No desync direction hides a Markdown-rendered wrong row while keeping exactly the right one.
6. Wrong S083/S084 row shape in `corpus/SOURCES.md` → `BOUNDARY-SOURCE`; host `native_per_seat_allowlist` not `false` → `BOUNDARY-HOST-LIMIT`. Neither can mask F1, but neither is needed for it either.

## Residual observations (adjacent surface, low)

- F2: LIMIT phrase gate uses raw `text`, not `visible(text)` (`'post-hoc detection, ...' not in text`, line ~103): the phrase inside a fence/comment satisfies the gate invisibly. Not a decision/source defect; committed prose has it genuinely visible.
- F3: extra foreign-id rows (e.g. a seventh `| EXTRA | ... |` row) are ignored by `cells`; only the six EXPECTED ids are compared.
- F4: SOURCES.md gate checks `path not in found[0][1]` (substring) and 6 of 11 cells are unchecked; `corpus/SOURCES.md` itself is outside this seat's read_paths, so committed-row conformance at the evaluated revision is a bounded assumption.
- F5: cosmetic — `BOUNDARY-CONTRACT-MISSING` and `BOUNDARY-SCHEMA` both report `site: DATA` even when the missing/malformed input is PROSE or host; main payload omits `origin_tip` though `Binding` carries it.

## Calibration: expected vs observed summary

| Case | Desired | Static derivation | Runtime |
|---|---|---|---|
| Committed corpus (JSON+md as read; table at column 0, phrase visible, scope exact) | exit 0 PASS 6/6 | exit 0 PASS 6/6 | not run (NO-EXEC) |
| wrong decision/source in visible row | reject | reject (exit 1, MISMATCH) | not run |
| fenced/hidden table | reject | reject | not run |
| F1 indented duplicate wrong row | reject | **exit 0 PASS 6/6 — gap** | not run |

No commands, imports, or tests were executed; every "observed" value above is a line-level trace of the read source, not a run. Runtime confirmation duty: run `python3 tools/check-boundary-contract.py --selftest` (expected PASS, 13 cases) and the F1 fixture (predicted divergence) at integration.

Scope note: no native preventive enforcement is claimed or assumed anywhere; this is post-hoc source validation only, per S084 and the host decision.

    Reviewed-SHA256: 1b91a7c10c971b554bad144035b40d0b7054e06582093f9f851ac0fcafdd2485
    Predicate: r22-fxc1table
    Scope: executed=none
