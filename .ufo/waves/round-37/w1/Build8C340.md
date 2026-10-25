# Build8C340 — C3 self-assessment mismatch correction

## Axes
- **Calibration:** confirm the already-declared fixed 27-check checker distinguishes stale self-assessment counters from counters that agree with measured repository state.
- **Operability (design):** provide a repeatable, isolated fixture that reproduces red-before and checks green-after without writing the lane.

## Deliverable
` .ufo/waves/round-37/w1/Build8C340/c3_mismatch_correction_check.sh` (remove the leading space when invoking) is a runnable shell fixture. It imports declaration-base revision `564db0b614b2914de5452f9ebd537a0653ae1de5` via `git archive` into a fresh `/tmp/c3-fixture.*` Git repository, verifies `git rev-parse --show-toplevel` equals the exact fixture root before its first commit, and invokes the existing `tools/check-self-assessment.py` against committed revisions. It records `before.json`, `after.json`, and `run.log` in this seat directory when run with `SEAT_OUT=<seat-dir>`.

Run from any directory:

```sh
SEAT=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-37/w1/Build8C340
SEAT_OUT="$SEAT" bash "$SEAT/c3_mismatch_correction_check.sh"
```

The correction in the fixture changes only the five self-assessment values the checker reads (K07–K11): depth note count 55→56; `SKILL.md` line count 3009→3110; table lines 784→839; lesson files 46→49; `corpus/README.md` lines 256→269. The baseline and corrected revisions are commits only inside the verified temporary fixture repo; its trap removes the repo on exit. The lane is read-only.

## Observed evidence (2026-10-25)
- Baseline command ran: `python3 tools/check-self-assessment.py --repo . --revision 564db0b614b2914de5452f9ebd537a0653ae1de5` from the lane. Observed exit **1**, JSON `checked=27`, `mismatches=5`, `status=FAIL`, declaring round 35, reference lines 350. The only mismatches were **K07–K11**, with stated/observed values 55/56, 3009/3110, 784/839, 46/49, and 256/269 respectively. This matches `.ufo/waves/round-37/before/c3-before.json` (which records 27/5/FAIL and exit 1).
- Ran the isolated script successfully. Its output: `top-level verified: /tmp/c3-fixture.IySCCJ`; BEFORE `exit=1 status=FAIL checked=27 mismatches=5`, `mismatch_ids=K07,K08,K09,K10,K11`; AFTER `exit=0 status=PASS checked=27 mismatches=0`; after values K07=56, K08=3110, K09=839, K10=49, K11=269, all `match`; final `pipeline_exit=0`. Fixture commits were `7af2c2504d9170c03d760eacd0e4b78b8beb57ee` and `d0278cf40d76951dd0613e79dea1794e6084be5f`; temp root was deleted on exit.
- Existing after snapshots show later-state repair still has residual defects outside this assigned baseline correction: `.ufo/waves/round-37/after-c3-ee36f9.json` records 27 checks and 1 mismatch (K17: host-census-gate row states no case count); `.ufo/waves/round-37/after-c3-d06ced.json` records 2 mismatches (K17 and K18 due absent paths). These are different later revisions, not failures of the fixture’s five-counter correction.

## Checker/parser specification captured
- Fixed predicate set is K01–K27. Required success condition is exactly 27 evaluated checks, `mismatches == 0`, `status == PASS`, and process exit 0. Cannot-evaluate/exit 2 is not a mismatch-free pass.
- For this fixture, expected BEFORE is exit 1, 27 checks, 5 mismatches, exactly IDs K07–K11. AFTER must preserve the same 27-check suite and produce zero mismatches; the script separately asserts each corrected observed value.
- Existing checker reads repository data through Git at an immutable revision (`tools/check-self-assessment.py` docstring lines 7–9) and returns `EXIT_PASS=0`, `EXIT_MISMATCH=1`, `EXIT_CANNOT_EVALUATE=2` (lines 74–76). No checker implementation edits are proposed.

## Risks / blockers
- This is a controlled red-before/green-after counter fixture, not proof that the current lane HEAD’s entire C3 claim is repaired. Recorded after snapshots show remaining K17/K18 path/count issues; main integration should reconcile the exact target revision and all 27 checks.
- The five expected after values are anchored to the declaration-base revision. A future fixture run intentionally fails if its immutable baseline content changes or any relevant checker predicate/output changes; update the fixture expectations only with a new observed baseline.
- No tools installed or updated; no host/package action. No source citations used.

Report trailer: `.ufo/waves/round-37/w1/Build8C340.md`
