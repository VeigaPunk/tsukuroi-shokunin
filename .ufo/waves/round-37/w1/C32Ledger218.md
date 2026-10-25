# C32Ledger218 — C3 falsification item 2/8

## Verdict / axes

**Calibration (C3):** the round-37 correction was incomplete at declaration/repair base `ee36f9e829f640def6b3c6ab3e31c4ed7186c6eb`. The unchanged checker finds **1 mismatch among 27 fixed checks**, K17. I propose correcting its operative capability self-assessment sentence to include the measured 105-case result; that is a single-cell repair and is predicted to resolve K17. The later tree `0e5f70f` reports zero mismatches, but that later state is not the requested declaration-base falsification.

**Frontier assimilation — errno discrimination:** the actionable difference here is not an absent evidence path (K17's current cited paths exist), but a missing count token in the capability's prose. The checker distinguishes those outcomes: it can resolve both paths and still reject the stated self-assessment because the row states no case count (`None`) while the observed census count is 105.

## Exact checker contract and baseline evidence

Read `tools/check-self-assessment.py` at the assigned lane root. `evaluate()` declares that it runs K01–K27 (lines 434–435), and its result counts the mismatch records while retaining `checked: len(checks)` and `mismatches` in the JSON (799–810). K17 is part of the capability loop: for `host-census-gate`, it extracts a stated case count, compares that with the census selftest count measured for K13, and returns mismatch when unequal or absent (686–719; in particular 702–718). The accepted textual count forms are documented and parsed in `stated_case_count()` (571–582), including `PASS (N cases,...)`.

At base `ee36f9e`, observed checker result is in `.ufo/waves/round-37/after-c3-ee36f9.json`: `checked=27`, `mismatches=1`, `status=FAIL`. Its only mismatch is K17, reported at SCORECARD line 2020: stated `None cases`; observed 105; reason `host-census-gate row states None cases; the census selftest at this revision prints 105 cases`. This is a **positive mismatch** rather than a missing check or untestable baseline.

Base SCORECARD's current K17 row (line 2020) says: `Emits a read-only six-plane host verdict and verdict-neutral DRIFT pacnew-plane line, with a hermetic census selftest`. It names two paths, `tools/tsukuroi-census.sh` and `.ufo/evidence/round-1-kaika/scout-live.md`. The K17 record confirms both named paths were found and the mismatch was exclusively the absent case count. K13 independently observes 105 cases in the same checker result. The complete census output observed directly from the base script begins with healthy/degraded case lines; K13's captured parser result is the authoritative count evidence for this check.

## Concrete fixed check and minimal correction proposal

**Fixed check:** K17, at declaration base `ee36f9e`, `host-census-gate` capability self-assessment must report the hermetic census selftest's case count.

**Stale value:** the K17 row's current phrase `with a hermetic census selftest` conveys no count. The checker parses `stated=None` and compares it with measured `observed=105`, yielding mismatch.

**Correction proposal (do not implement in lane):** replace that phrase in the operative `host-census-gate` row with `with a hermetic selftest that prints PASS (105 cases, 105 passed, 0 failed)`. This wording matches the existing K13 result and K17 parser's documented `PASS (N cases, ...)` shape, while retaining the row's existing capability claim and evidence paths. Do not change the checker or its 27-check set.

Prediction: at the same base tree, with only this capability-row sentence corrected, K17 becomes `stated=105`, `observed=105`, and `match`; with the other 26 checks unchanged, the report becomes `checked=27`, `mismatches=0`, `status=PASS`.

## Validation boundary and fixture status

Observed subsequent evidence: `.ufo/waves/round-37/after-c3-0e5f70.json` reports `checked=27`, `mismatches=0`, `status=PASS`, and K17 matches with stated/observed 105. This establishes a later zero-mismatch state, not an isolated causal validation of this one correction, because the later revision includes additional changes. My fixture attempt did not complete: the lane Git repository no longer had the base commit object available to `git archive ee36f9e...` (fatal `not a tree object`), despite the earlier `git show ee36f9e:SCORECARD.md` read succeeding. The partial seat artifact is `C32Ledger218/build-fixture.sh`; its failed extraction produced no valid fixture commits or checker results. Do not treat that attempt as proof of the predicted zero-mismatch counterfactual.

No lane checker/scorecard/source edits were made. No installs or updates were made. No host/package changes, lane Git writes, or sibling/fleet repo writes were made.

### Checks and citations

- `tools/check-self-assessment.py`, opened locally this round: `evaluate` contract and result construction at lines 434–435, 799–810; K17 count parsing and mismatch behavior at lines 571–582, 686–719.
- `SCORECARD.md`, opened locally this round at declaration-base path: operative current axes/capabilities correction at lines 2000–2030, including base K17 row at 2020.
- `.ufo/waves/round-37/after-c3-ee36f9.json`, opened locally this round: base revision, 27 checks, only K17 mismatch and exact reason.
- `.ufo/waves/round-37/after-c3-0e5f70.json`, opened locally this round: later 27-check result with zero mismatches and K17 match.
- `tools/tsukuroi-census.sh --selftest`, run read-only at current lane tree; stdout included census case output. The checker’s base-revision K13 record specifically reports 105 cases.
- No external URLs were used.

Report trailer: `.ufo/waves/round-37/w1/C32Ledger218.md`
