# MutBattery — method (round-91 w1, mutation-tester seat on the frozen C1 battery)

Axes: (A) oracle strength — does the battery still reject every frozen control when one
comparison is removed? (B) fixture coverage — does reducing an enumerated corpus let a control
escape? (C) model self-consistency — does a battery-model change keep the candidate gate met
(else the change is not a pure weakening and cannot test the controls).

Procedure per mutant:
1. Copy the frozen battery (`tools/limine-pin-battery-r91.py`, sha256 655ee8f3…, identical to the
   tasking digest) into scratch; apply one textual mutation; `py_compile`; assert
   `tuple(FAMILIES) == FAMILY_ROSTER` and that the roster equals the frozen roster minus any
   intentionally dropped family (AST check in `gen.py`).
2. Purity run: `python3 <mutant> --gate tools/check-limine-pins.py --runs 1`. A mutant that does
   not read `met` here is not a pure weakening and is excluded from the control matrix.
3. Control matrix: the mutant runs once against each of the 12 frozen control gates in
   `.ufo/waves/round-91/before/controls/gates/` (K1, K2, N01–N10). A mutant is DETECTED iff at
   least one control that the frozen battery rejects (all 12) now reads `met` (escape).
4. Escape confirmation: every escaping control is re-run with `--runs 3`.

Fixtures are generated fresh per run by the battery itself (OS entropy, shuffled case order); the
mutants change only battery source bytes, never the gate, the controls, or the lane.
