#!/usr/bin/env python3
"""Round-74 E3HostProbe attack on the frozen C2 checker (check-r73-routed-r74.py).

Tests whether vacuous or incomplete repair drafts can deceive the C2 checker.

Mutants tested against the frozen checker:
  1. CONTROL: fully compliant repair texts for both defects -> ROUTED_STALE=0 ROUTED_OK=2/2, rc 0.
  2. M1-LESSON-MISSING-NEW-LOC: missing install.c:2383 in lesson body -> stale=1 rc 1.
  3. M2-LESSON-MISSING-OLD-LOC: missing 2387 in lesson body -> stale=1 rc 1.
  4. M3-LESSON-MISSING-ANCHOR: missing :368-370 in lesson body -> stale=1 rc 1.
  5. M4-LESSON-HEADER-ONLY: tokens placed solely in heading, absent in body -> stale=1 rc 1.
  6. M5-LOG-MISSING-SUPERSEDED: missing superseded counts (12 and 11) in log -> stale=1 rc 1.
  7. M6-LOG-MISSING-FINAL-COUNTS: missing final instrument counts (13 and 14) in log -> stale=1 rc 1.
  8. M7-LOG-HEADER-ONLY: heading matches but body is empty/vacuous -> stale=1 rc 1.

Run:  python3 attack-c2-vacuous.py
rc 0 = every mutant caught, control accepted (checker held closed);
rc 1 = at least one failure.
"""
import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
CHECKER_PATH = REPO_ROOT / "tools" / "check-r73-routed-r74.py"

spec = importlib.util.spec_from_file_location("c2", str(CHECKER_PATH))
c2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c2)

GOOD_LESSON = """# Round 73 lesson

## Gate
Some gate prose.

## Correction (R73-GATE-QUOTE-LINE-DRIFT)
In the Gate section, the S306 quote was attributed to install.c:2387 but sits at install.c:2383 in the v262 snapshot.
The S304 line anchors carried one extra edge line: :368-370 replaces :367-370, :237-238 replaces :236-238, and :238-239 replaces :238-240.
"""

GOOD_LOG = """# Log

## Round 73 (hyaku run 15)
Initial log entry mentioning a twelfth selftest case and checker growing to eleven cases.

## Round 73 — correction (R73-LOG-COUNT-STALE)
The entry above cited mid-wave counts: a twelfth selftest case (12) and checker growing to eleven cases (11).
The final committed instruments carry 13 cases for tools/count-ul-rows-r73.py and 14 cases for tools/check-r72-routed-r73.py.
"""


def main():
    cases = [
        ("CONTROL",
         {"corpus/lessons/round-73.md": GOOD_LESSON, "LOG.md": GOOD_LOG},
         0, 2),

        ("M1-LESSON-MISSING-NEW-LOC",
         {"corpus/lessons/round-73.md": GOOD_LESSON.replace("install.c:2383", "install.c:2380"), "LOG.md": GOOD_LOG},
         1, 1),

        ("M2-LESSON-MISSING-OLD-LOC",
         {"corpus/lessons/round-73.md": GOOD_LESSON.replace("2387", "old-line"), "LOG.md": GOOD_LOG},
         1, 1),

        ("M3-LESSON-MISSING-ANCHOR",
         {"corpus/lessons/round-73.md": GOOD_LESSON.replace(":368-370", ":368-375"), "LOG.md": GOOD_LOG},
         1, 1),

        ("M4-LESSON-HEADER-ONLY",
         {"corpus/lessons/round-73.md": "## Correction (R73-GATE-QUOTE-LINE-DRIFT: install.c:2383 2387 :368-370 :237-238 :238-239)\nEmpty body text.", "LOG.md": GOOD_LOG},
         1, 1),

        ("M5-LOG-MISSING-SUPERSEDED",
         {"corpus/lessons/round-73.md": GOOD_LESSON, "LOG.md": """# Log
## Round 73 — correction (R73-LOG-COUNT-STALE)
Final instruments carry 13 and 14 cases.
"""},
         1, 1),

        ("M6-LOG-MISSING-FINAL-COUNTS",
         {"corpus/lessons/round-73.md": GOOD_LESSON, "LOG.md": """# Log
## Round 73 — correction (R73-LOG-COUNT-STALE)
Mid-wave counts were 12 and 11. Final counts unspecified.
"""},
         1, 1),

        ("M7-LOG-HEADER-ONLY",
         {"corpus/lessons/round-73.md": GOOD_LESSON, "LOG.md": """# Log
## Round 73 — correction (R73-LOG-COUNT-STALE 12 11 13 14)
No content in body.
"""},
         1, 1),
    ]

    passed = 0
    failed = 0
    for name, fixtures, exp_stale, exp_ok in cases:
        stale, ok, reasons = c2.evaluate(fixture_texts=fixtures)
        if stale == exp_stale and ok == exp_ok:
            passed += 1
            status = "CONTROL PASS" if name == "CONTROL" else "PASS (caught mutant)"
            print(f"{status}: {name} (stale={stale}, ok={ok})")
        else:
            failed += 1
            print(f"FAIL: {name} expected (stale={exp_stale}, ok={exp_ok}) got (stale={stale}, ok={ok}) reasons={reasons}", file=sys.stderr)

    print(f"\nC2 CHECKER BATTERY: {passed}/{len(cases)} tests passed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
