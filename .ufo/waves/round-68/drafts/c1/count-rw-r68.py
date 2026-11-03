#!/usr/bin/env python3
"""Round-68 C1 strict RW-row counter (frozen before the note exists).

SCORECARD.md "Round 68 - declaration", row C1, freezes the counting command
`grep -cE '^\\| RW[0-9]+ \\| '` over
`corpus/knowledge/linux-v73-pinwatch-r68.md`. That grep counts SHAPE only: the
round-67 defect R67-COUNTER-SHAPE-ONLY
(`corpus/lessons/round-67-verifier-spotcheck.md` §2) is that duplicate ids,
fenced example rows, prose rows and empty evidence cells all satisfy it. This
counter keeps the frozen anchor and adds the strict clauses the declaration
names, so the number it prints is the number of rows that actually carry a
registry re-read.

The note's table layout (8 columns, required):

    | id | row-kind | fact | v7.2 anchor | v7.3 anchor | verdict | applicability | evidence |

A line is one valid row iff ALL of the following hold.

  R1 FENCE     outside a ``` / ~~~ fence; fence delimiter lines and every line
               between them are not data. Fence tracking follows
               `tools/check-knowledge-header.py` (a delimiter toggles, the
               closing run must use the same character and be at least as long).
  R2 ANCHOR    `^\\| RW[0-9]+ \\| ` at column 0, with a space (or end of line)
               after the second pipe. Leading whitespace fails: markdown does
               not open a table row there and the frozen grep misses it. The
               space requirement is the frozen grep's own form, so every row
               this counter accepts also matches the frozen predicate: the
               strict count is a SUBSET of the frozen count, never larger. A
               counter that could exceed the frozen predicate would be answering
               a different question than the one the declaration froze.
  R3 TABLE     the row belongs to a table: in the contiguous run of
               `|`-prefixed, non-fenced lines above it there is a `|---|`
               separator line. A row-shaped line inside a paragraph is prose.
  R4 SHAPE     exactly 8 data cells (id, row-kind, fact, v7.2 anchor, v7.3
               anchor, verdict, applicability, evidence). A `\\|` inside a cell
               is protected before the split, so an evidence cell may quote a
               shell pipeline. `| a | ... | h |` splits into 10 raw fields; the
               same 8-cell row without its trailing pipe splits into 9 — the
               item's NF — and both are the same row, so the rule is the
               data-cell count, never the raw field count. A NINTH cell is
               rejected even though the item's parenthetical reads evidence as
               "the 4th-from-last data cell": in an 8-column table a ninth cell
               means an unescaped pipe or an extra column, and then no cell is
               the evidence cell. Accepting it would test the verdict cell in
               the evidence's place — a false accept of a row whose evidence is
               blank (M1Mutation's round-68 live-note probe, whose rows carried
               unescaped pipes inside cells, and its m8/m4 blank-evidence read).
               The note's own header (8 columns, evidence last) is the layout
               the note must keep.
  R5 ID        ids are distinct by NUMERIC value: `RW7` and `RW007` are the
               same row id, and the second occurrence is rejected. (The id cell
               cannot disagree with the anchor: R2 consumes `| RW<n> |` as the
               row's first cell, so an equality test there would be dead.)
  R6 EVIDENCE  the evidence cell is non-empty after trim and is not a
               placeholder (`-`, `--`, `\u2014`, `\u2013`, `...`, `\u2026`, `TBD`, `TODO`, `n/a`,
               `none`): a dash is a blank, so it cannot satisfy "non-empty".

Output on stdout, one measurement per file, in this order:

    RW_ROWS=<count of strictly valid rows>
    LAYOUT=<8|none>
    REJECT line=<n> id=<RWn|-> reason=<FENCED|ANCHOR|TABLE|SHAPE|EMPTY-EVIDENCE|DUPLICATE-ID> detail=<...>

One REJECT line per candidate (a line that names an `RW<digits>` id next to a
pipe) that failed at least one rule, in file order; `detail` names the rule
violated and the observed shape, so a rejected row is diagnosable without
re-running anything.

Exit 0 = measured (whatever the count); 2 = the file could not be read, in
which case nothing is measured and no RW_ROWS line is printed. Read-only: the
one file named on argv, no temp files, no bytecode
(`sys.dont_write_bytecode`), never writes outside its argv.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # a counter must not drop a __pycache__ anywhere

import argparse
import re
from pathlib import Path

ANCHOR = re.compile(r"^\| RW([0-9]+) \|(?= |$)")
CANDIDATE = re.compile(r"RW[0-9]+")
SEPARATOR_CELL = re.compile(r"\s*:?-{1,}:?\s*")
ESCAPED_PIPE = "\x00"

PLACEHOLDERS = {
    "-",
    "--",
    "\u2014",
    "\u2013",
    "...",
    "\u2026",
    "tbd",
    "todo",
    "n/a",
    "none",
}


def fence_flags(lines: list[str]) -> list[bool]:
    """True for a line that is a fence delimiter or sits inside a fence."""
    inside = [False] * len(lines)
    char = None
    width = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        opening = re.match(r"^(`{3,}|~{3,})", stripped)
        if char is None:
            if opening:
                char = opening.group(1)[0]
                width = len(opening.group(1))
                inside[i] = True
            continue
        inside[i] = True
        closing = re.match(r"^" + re.escape(char) + r"{%d,}\s*$" % width, stripped)
        if closing:
            char = None
            width = 0
    return inside


def split_cells(line: str) -> tuple[list[str], int]:
    """Data cells of one pipe row, plus the raw field count of the split."""
    protected = line.replace("\\|", ESCAPED_PIPE)
    raw = protected.split("|")
    cells = list(raw)
    if cells and cells[0].strip() == "":
        cells = cells[1:]
    if cells and cells[-1].strip() == "":
        cells = cells[:-1]
    return [cell.replace(ESCAPED_PIPE, "|").strip() for cell in cells], len(raw)


def is_separator(stripped: str) -> bool:
    core = stripped
    if core.startswith("|"):
        core = core[1:]
    if core.endswith("|"):
        core = core[:-1]
    cells = core.split("|")
    if len(cells) < 2:
        return False
    return all(SEPARATOR_CELL.fullmatch(cell) for cell in cells)


def has_table_above(lines: list[str], inside: list[bool], index: int) -> bool:
    j = index - 1
    while j >= 0:
        if inside[j]:
            return False
        stripped = lines[j].strip()
        if stripped == "" or not stripped.startswith("|"):
            return False
        if is_separator(stripped):
            return True
        j -= 1
    return False


def measure(path: Path) -> tuple[int, str, list[str]]:
    text = path.read_bytes().decode("utf-8", errors="replace")
    lines = text.splitlines()
    inside = fence_flags(lines)

    accepted: dict[int, int] = {}  # numeric id -> line number
    layouts: set[int] = set()
    rejects: list[str] = []

    for index, line in enumerate(lines):
        if not CANDIDATE.search(line) or "|" not in line:
            continue
        line_no = index + 1
        anchor = ANCHOR.match(line)
        if inside[index]:
            rejects.append(
                "REJECT line=%d id=%s reason=FENCED detail=line sits in a fenced block"
                % (line_no, ("RW" + anchor.group(1)) if anchor else "-")
            )
            continue
        if not anchor:
            if line[:1] in (" ", "\t"):
                reason, detail = "ANCHOR", "row is indented; the frozen anchor starts at column 0"
            elif line.startswith("|"):
                reason, detail = "ANCHOR", "no `| RW<n> | ` prefix (id cell or pipe spacing differs)"
            else:
                reason, detail = "ANCHOR", "line does not start with a pipe (prose)"
            rejects.append(
                "REJECT line=%d id=- reason=%s detail=%s" % (line_no, reason, detail)
            )
            continue
        row_id = anchor.group(1)
        if not has_table_above(lines, inside, index):
            rejects.append(
                "REJECT line=%d id=RW%s reason=TABLE detail=no `|---|` separator above in the pipe block"
                % (line_no, row_id)
            )
            continue
        cells, raw_fields = split_cells(line)
        if len(cells) != 8:
            rejects.append(
                "REJECT line=%d id=RW%s reason=SHAPE detail=%d data cells, %d raw fields (need 8)"
                % (line_no, row_id, len(cells), raw_fields)
            )
            continue
        key = int(row_id)
        evidence = cells[7]  # the 8-column layout names evidence last
        if evidence == "" or evidence.lower() in PLACEHOLDERS:
            rejects.append(
                "REJECT line=%d id=RW%s reason=EMPTY-EVIDENCE detail=evidence cell %r"
                % (line_no, row_id, evidence)
            )
            continue
        if key in accepted:
            rejects.append(
                "REJECT line=%d id=RW%s reason=DUPLICATE-ID detail=already counted at line %d"
                % (line_no, row_id, accepted[key])
            )
            continue
        accepted[key] = line_no
        layouts.add(len(cells))

    if not layouts:
        layout = "none"
    elif len(layouts) == 1:
        layout = str(next(iter(layouts)))
    else:
        layout = "mixed"
    return len(accepted), layout, rejects


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Count strictly valid `| RW<n> | ...` rows of a round-68 knowledge note."
    )
    parser.add_argument("note", metavar="NOTE", help="markdown file to measure")
    args = parser.parse_args(argv)

    path = Path(args.note)
    try:
        if not path.is_file():
            raise OSError("not a regular file")
        count, layout, rejects = measure(path)
    except OSError as exc:
        print("CANNOT-MEASURE %s: %s" % (args.note, exc), file=sys.stderr)
        return 2

    print("RW_ROWS=%d" % count)
    print("LAYOUT=%s" % layout)
    for line in rejects:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
