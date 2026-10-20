# CritOperability — C2 attack surface after round-18 judge hardening

Axes: operability, calibration. Read-only review of `51dd9ee`.

## All six FxSimplifyBind defects attacked? Yes [obs]

`check-revision-binding.py:340-357`: D1→`branch-range/slash/space`; D2→`branch-first` (HEAD+`a..b`→E-BRANCH-INVALID); D3→`git-failed` (`update-ref origin/master <blob>`→merge-base rc≥2→E-GIT-FAILED); D4→`single-id`; D5→`branch-missing`; D6→range/slash. Baseline `measure/c2-before-842a531.json`: consistent1/9 (seat-scope), shared0, copies9, FAIL — matches claim.

## Counterexamples (axis: operability)

1. **Green gate ≠ consolidation** [obs]: `status=PASS`/`grade` test only `consistent==total` (`:401`,`:411-412`); `shared_tools`/`local_rev_regex_copies` never gate. Nine identical hand-synced copies, no `_revision`, give 9/9 PASS with copies=9. Fix: conjunct `shared==total and copies==0` into `grade`, or C2 evidence must quote all three fields, not exit code (SCORECARD:538 names them).

2. **"Exactly one id" enforced on 1 of 6 refusals** [obs]: `refused()` (`:296-300`) checks only `finding==want`; `finding_id` (`:264-267`) takes the *first* finding. `single-id` exists only for unlanded (`:348-351`). Emitting `[E-BRANCH-MISSING, E-REVISION-NOT-LANDED]` on `--branch nosuch` → ok=True, two ids emitted. Fix: `binding_ids==[want]` inside `refused`.

3. **Origin-absent path unprobed** [obs]: `prepare` always recreates `refs/remotes/origin/master` (`:189-190`); the conditional push check (`_revision.py:146`) is never exercised. A tool erroring when origin is absent passes 9/9. Fix: probe deleting the remote ref; tip must still be accepted.

4. **Markers text-level; probes enumerable** [obs]: `SHARED_IMPORT` counts dead `if False: import _revision` (selftest `:516` relies on it); `LOCAL_REV_REGEX` evadable (`"{7,"+"64}"`). Six probe inputs are published; special-casing them + dead import reads shared/consistent=True with a divergent local binder — same weakness class FxSimplifyBind found. Not closable by census; raise cost: require tools to echo `branch_tip`/`origin_tip` matching judge-computed values.

5. **Denominator mixes discovered tools** [obs]: `discover()` folds into `total`/`consistent` (`:376`,`:396-401`); claim says "among original nine, discovered separately" (SCORECARD:541). Inconsistent discovered tool → FAIL despite 9/9; consistent → headline reads 10/10. Fix: report named/discovered split.

Judge independence holds (no `_revision` import; own bind `:136-149`, rev-first/no branch-format — deliberate authority, not defect).

Scope: executed=none (read-only: file reads, git log/show/ls-tree/status, python3 JSON parse)
