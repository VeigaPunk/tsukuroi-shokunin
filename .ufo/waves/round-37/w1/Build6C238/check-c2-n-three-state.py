#!/usr/bin/env python3
"""Check the C2 -n/--lines third-state correction using captured matrix evidence.

Read-only against the lane. Requires the round-36 matrix-mini.json and note.
Usage: python3 check-c2-n-three-state.py [LANE_ROOT]
Exit 0: note clearly distinguishes REJECT, WORK and WORK-ALTERED and its
       named -n evidence proves -F truncation but not -N truncation.
Exit 1: missing/inconsistent receipt or missing/incorrect note correction.
Stdlib only; no subprocesses, writes, or live journal access.
"""

import json
import sys
from pathlib import Path

MATRIX_REL = Path(".ufo/waves/round-36/w1/ScribeC2Draft/matrix-mini.json")
NOTE_REL = Path("corpus/knowledge/journalctl-v262-field-filter-r36.md")
FAILURES: list[str] = []


def fail(message: str) -> None:
    FAILURES.append(message)
    print(f"  FAIL: {message}")


def check(root: Path) -> int:
    matrix_path = root / MATRIX_REL
    note_path = root / NOTE_REL
    try:
        matrix = json.loads(matrix_path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read valid matrix {MATRIX_REL}: {exc}")
        return 1
    try:
        note = note_path.read_text()
    except OSError as exc:
        fail(f"cannot read note {NOTE_REL}: {exc}")
        return 1

    cells = {cell.get("cell"): cell for cell in matrix.get("cells", [])}
    required = ("core_plain", "ext_lines1_F", "ext_plain_N", "ext_lines1_N")
    missing = [name for name in required if name not in cells]
    if missing:
        fail(f"matrix is missing required cells: {', '.join(missing)}")
        return 1

    plain_f, lines_f, plain_n, lines_n = (cells[name] for name in required)
    for label, cell in zip(required, (plain_f, lines_f, plain_n, lines_n)):
        if cell.get("exit") != 0 or cell.get("stderr_bytes") != 0:
            fail(f"{label} is not a successful, silent run")
    if plain_f.get("argv")[-2:] != ["-F", "PRIORITY"]:
        fail("core_plain does not measure plain -F PRIORITY")
    if lines_f.get("argv")[-4:] != ["-n", "1", "-F", "PRIORITY"]:
        fail("ext_lines1_F does not measure -n 1 -F PRIORITY")
    if plain_n.get("argv")[-1:] != ["-N"] or lines_n.get("argv")[-3:] != ["-n", "1", "-N"]:
        fail("the N cells do not compare plain -N with -n 1 -N")

    # These are measured byte counts and heads, not inference from the note.
    if (plain_f.get("stdout_bytes"), len(plain_f.get("stdout_head", []))) != (12, 6):
        fail("core_plain no longer records six values / 12 bytes")
    if (lines_f.get("stdout_bytes"), len(lines_f.get("stdout_head", []))) != (2, 1):
        fail("ext_lines1_F no longer records one value / 2 bytes")
    if plain_n.get("stdout_bytes") != 2882 or lines_n.get("stdout_bytes") != 2882:
        fail("the -N/-n comparison no longer records 2882 bytes in both cells")
    if plain_n.get("stdout_sha256") != lines_n.get("stdout_sha256"):
        fail("-N output changed under -n; no longer an unchanged-output control")

    altered = "WORK-ALTERED"
    if altered not in note:
        fail("decision table lacks a distinct WORK-ALTERED third state")
    for name in ("REJECT", "WORK", altered):
        if name not in note:
            fail(f"decision table does not state {name}")
    # Ensure the note links this classification to every measured control.
    for name in ("core_plain", "ext_lines1_F", "ext_plain_N", "ext_lines1_N"):
        if name not in note:
            fail(f"note does not cite required matrix cell {name}")
    if "12" not in note or "2" not in note or "2882" not in note:
        fail("note does not state the measured byte-count contrast (12, 2, 2882)")
    if FAILURES:
        print(f"result: FAIL ({len(FAILURES)} assertion(s) failed)")
        return 1
    print("result: PASS (REJECT / WORK / WORK-ALTERED; -F truncation and -N control evidenced)")
    return 0


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[5]
    print(f"checking C2 -n three-state correction at {root}")
    return check(root)


if __name__ == "__main__":
    sys.exit(main())
