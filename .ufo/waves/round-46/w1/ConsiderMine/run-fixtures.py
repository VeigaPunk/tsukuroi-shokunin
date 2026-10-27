#!/usr/bin/env python3
"""Should-fail / should-pass fixtures for check-log-axis-coverage.py.

Four synthetic lanes under the scratch dir; each is a LOG.md plus a
round-90 spot-check and lesson. A fixture is KILLED when the checker's
finding count differs from the expected count (0 = the check must stay quiet,
1 = it must speak). Prints one line per fixture and a closing machine line.
"""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHECK = os.path.join(HERE, "check-log-axis-coverage.py")
BASE = os.path.join(os.environ.get("TMPDIR", HERE), "fx")

LOG_HEAD = "# log\n\n## Round 89 — x\n\nnothing.\n\n## Round 90 — test\n\n"
SPOT = """# spot

## 2. Claims

### Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| operability | improved | measured |
| adjacency | {grade} | anchors gate |
"""
LESSON_OK = """# lesson

## Round-89 routed defects — round-90 disposition

| Defect | State | Evidence |
|---|---|---|
| D1 repin | closed | done |
| D2 sweep | partial | routed |

Conflicts recorded verbatim for the canonical judge:

- a receipt marks D2 "done"; the D2 row above still says partial, so the row
  is the record.

## Next

nothing.
"""
LESSON_CONFLICT = """# lesson

## Round-89 routed defects — round-90 disposition

| Defect | State | Evidence |
|---|---|---|
| D1 repin | closed | done |

Conflicts recorded verbatim for the canonical judge:

- the scout marks D1 "done" on the entry alone; `corpus/README.md:434` and the
  `SKILL.md` row that D1 also names are unchanged from base.

## Next

nothing.
"""

CASES = [
    # name, log names adjacency?, axis grade, lesson text, expected findings
    ("F1 axis harmed, LOG silent", False, "harmed", LESSON_OK, 1),
    ("F2 axis harmed, LOG names it", True, "harmed", LESSON_OK, 0),
    ("F3 closed row contradicted", True, "unchanged", LESSON_CONFLICT, 1),
    ("F4 closed row, unrelated conflict", True, "unchanged", LESSON_OK, 0),
]

killed = 0
for name, named, grade, lesson, want in CASES:
    d = tempfile.mkdtemp(prefix="lane.", dir=BASE)
    os.makedirs(os.path.join(d, "corpus", "lessons"))
    log = LOG_HEAD + ("adjacency unchanged; operability improved.\n" if named else "operability improved.\n")
    open(os.path.join(d, "LOG.md"), "w").write(log)
    open(os.path.join(d, "corpus", "lessons", "round-90-verifier-spotcheck.md"), "w").write(
        SPOT.format(grade=grade)
    )
    open(os.path.join(d, "corpus", "lessons", "round-90.md"), "w").write(lesson)
    out = subprocess.run(
        [sys.executable, CHECK, "--lane", d, "--round", "90"],
        capture_output=True,
        text=True,
    )
    last = out.stdout.strip().splitlines()[-1] if out.stdout.strip() else ""
    got = int(last.split("findings=")[1].split()[0]) if "findings=" in last else -1
    ok = got == want
    killed += 0 if ok else 1
    print(f"{'ok  ' if ok else 'KILL'} {name}: expected {want} findings, got {got}")

print()
print(f"TSUKUROI_BURST_READ_FIXTURES: cases={len(CASES)} failed={killed}")
sys.exit(1 if killed else 0)
