# Independent before-data control audit — C3

## Axis and frozen target

**C3 / calibration**: correct the existing self-assessment mismatch by changing the five stale count cells; the unchanged checker must report `checked == 27`, `mismatches == 0`, `status == PASS`, exit 0. The operative declaration is `SCORECARD.md:1950-1968`, specifically the frozen predicate at lines 1958-1967. Its designated no-change control is the committed base `564db0b614b2914de5452f9ebd537a0653ae1de5`.

## Cheapest do-nothing control and observed result

Command (read-only; no edits):

```sh
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 564db0b614b2914de5452f9ebd537a0653ae1de5:tools/check-self-assessment.py >/dev/null && python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-self-assessment.py --revision 564db0b614b2914de5452f9ebd537a0653ae1de5
```

The committed checker SHA-256 is `1e1ab6113d665684e15d147c0f3dae519cf2d313877e1603b841ad4db85d4257`; the working checker SHA-256 is identical. Output summary: `revision=564db0b614b2914de5452f9ebd537a0653ae1de5`, `checked=27`, `mismatches=5`, `status=FAIL`, declaring round 35. Mismatches are K07–K11: depth note count 55 vs 56; SKILL line count 3009 vs 3110; SKILL pipe-prefixed line count 784 vs 839; lesson-file count 46 vs 49; README line count 256 vs 269. The remaining 22 checks match. **Exit: 1.**

## Score against predicate / falsification

The do-nothing control skips the five declared count-cell corrections and **does not** satisfy the exact frozen predicate: 5 ≠ 0, status FAIL, exit 1. Thus the target is **not reachable without claimed work on the committed baseline bytes**; the strongest simple shortcut is falsified for C3. This distinguishes the control from the after receipt at `round-37/after-c3-0e5f70.json` (27 checked, zero mismatches, PASS), which is evidence for a changed assessed revision rather than the base control.

No tooling was installed or updated; no host or lane content was modified.