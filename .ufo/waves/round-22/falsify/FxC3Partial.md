# FxC3Partial: source-only falsification of check-review-cohort.py (round 22)

Target: `.ufo/waves/round-22/candidate/tools/check-review-cohort.py`, read at snapshot tag ADD3. The declared digest comes from the assignment. It was not recomputed, because NO-EXEC forbids hashing commands.
Read set: the declared read paths only, some by range. `_revision.py` was read at helper level only. No command, test, import, mutation, fetch, or delegation was run. Observed runtime: none.

## Verdict

Attack claim: a failed outcome with a partial report is `delivered_faulty`, never dropped or absent.

- **Falsified** for a receipt-complete partial report. For any present report, the category comes only from the strict receipt result. The settlement outcome is never consulted (F1).
- **Holds** for receipt-malformed partials (B1), for a report missing at the bound revision, which is `absent_dead` by design (B2), and for seat-set accounting, which cannot silently drop a row (B3).
- Two adjacent defects on the same path weaken calibration more than the attack does. The cohort metric reads `1` on runs that accounted nothing (F2). One unreadable committed report discards every seat's category (F3).

## Axes

1. Category fidelity for failed rows (the attack axis).
2. Fail-closed accounting: no seat lost without a non-zero exit.
3. Metric honesty: `cohort_accounting_mode` must not claim accounting that did not happen.
4. Absent-versus-present discrimination at the bound revision.
5. Fixture sensitivity: whether the selftest detects the defects above.

## F1: counterexample to the attack claim (Medium-High)

Trace (target lines):
- 54: `outcome = by_name[name]`. 55: `report = read_bytes(review['report'])`.
- 58-61: if the report is present, `category = 'delivered_conformant' if one_code == 0 else 'delivered_faulty'`. `outcome` is read at 59 only, which runs only when the report is absent.
- Strict evaluator `check-review-snapshots.py` 107-118: exact-equality checks over prefix-matched physical lines (digest, predicate, scope). Nothing requires a body, completeness, or a completed outcome.
- 44-45: a failed row needs only a non-empty error. Nothing forbids a conformant report on a failed row.
- 63: the row keeps `outcome: failed`. The failure is visible in `seats` but not in categories or counts.

Counterexample shape (described, not run): the manifest pins the source. The settlement row is `failed` with an observed error. The report is exactly the three receipt declarations for the pinned digest and predicate (the bytes the selftest uses for its clean report, line 88), or a complete receipt block followed by a truncated body.

Fixture verdicts:
- Attack-expected: `delivered_faulty` = 1, `delivered_conformant` = 0. Exit left at 0, matching the candidate's own `partial-failed` convention (line 96).
- Observed runtime: none executed.
- Source-derived prediction [INFERENCE]: `delivered_conformant` = 1, `delivered_faulty` = 0, `strict_receipt_exit` 0, `strict_conformance` PASS, status PASS, exit 0, findings empty, row `outcome` failed. The fixture would fail against this candidate.

Why the candidate's own fixture misses it: `partial-failed` (line 96) uses the bytes `b'partial'`, which fail the receipt check. Its name states the invariant, but its bytes cover only the receipt-malformed subset. None of the 18 selftest cases (lines 93-110) combines a failed row with a receipt-complete report.

Definition check: SCOPE (line 19) defines `delivered_conformant` as receipt-well-formed, so F1 is consistent with that definition. It still contradicts the attack invariant and the fixture name. A failed provider seat is counted in the `delivered_conformant` total.

Decision for Main: may a failed row ever be `delivered_conformant`? A minimal option that changes no existing selftest expectation is line 61: `category = 'delivered_conformant' if one_code == 0 and outcome['outcome'] == 'completed' else 'delivered_faulty'`. [INFERENCE] Every current case with a non-completed row is either the absent branch (`dead-missing`), `partial-failed` (already faulty), or rejected earlier (`false-death`). The only behavior change is `unknown` rows with conformant reports, which Main must accept or exempt.

## F2: `cohort_accounting_mode` reads 1 on runs that accounted nothing (High for metric consumers)

- 24: manifest missing gives mode 0.
- 75-76 (schema: ValueError, TypeError, KeyError, AttributeError, UnicodeError) and 77-78 (read: OSError, RuntimeError, TimeoutExpired) give **mode 1**, with no `seats` and no counts. Status is `CANNOT_EVALUATE` (79), exit 2.
- main 149-150 and 156-158: those results have no mode key at all.
- Concrete trigger [INFERENCE]: the settlement path is absent at the bound revision. `git_read` returns None (129-130). `json.loads(None)` raises TypeError at 31. The result is mode 1 with exit 2.
- The C3 metric in `preregister.json` (line 7) is `cohort_accounting_mode`, target 1. C3_bound (line 9) requires every declared seat to be accounted. A metric-only consumer therefore accepts a run that accounted zero seats.
- No selftest asserts the mode. The observation loop (111-118) checks exit, ids, category, and strict_exit only.
- Non-harming fix: emit 0 on every exit-2 path, or omit the key uniformly. No existing fixture asserts the mode.

## F3: one unreadable committed report discards every seat's accounting (Medium)

- 55 sits inside the main `try` but outside any per-seat guard.
- The outer handler (77-78) replaces the whole result. `counts` and `rows` (62-65) are discarded, so no seat gets a category, including the failed one.
- The strict evaluator handles the same exceptions per seat (`check-review-snapshots.py` 84-97: REVIEW-READ-FAILED, then continue). The cohort path does not.
- Exit 2 keeps this fail-closed. The C3_bound "every declared seat" is still unmet, and F2 makes the metric read 1 anyway.
- Reachability: RuntimeError from `git_read` (131) when `git show` (125) fails and the probe (128) is non-empty or fails (see F4). Or `subprocess.TimeoutExpired` at 125 or 128 after 30 s.
- Fix needs Main's choice: a per-seat guard that records `absent_unresolved` or faulty with a COHORT-READ finding, instead of aborting.

## F4: absence probe is relative to ROOT, not the repository root (Low; latent in production layout)

- 125: `git show rev:path` is repository-root-relative.
- 128: `git ... ls-tree -z rev -- path` runs with `-C ROOT` and no `--full-tree`. `ls-tree` is cwd-relative, so it probes `ROOT/path`. [INFERENCE: documented git behavior, not executed.]
- ROOT = `parents[1]` of the tool (line 15). In this staged layout the tool sits under `candidate/tools`, so ROOT is `candidate/`, a subdirectory of the repository. [INFERENCE] In production, `tools/` sits at the toplevel and the two probes agree.
- Effects when staged: a missing root path whose ROOT-relative twin exists makes the probe non-empty, which gives RuntimeError (131) and then the F3 abort. Conversely, if `git show` rejects a present root entry, the probe can return "absent" and misclassify it.
- Same probe pattern: `check-review-snapshots.py` 135-140 (strict's own CLI). The cohort passes its own reader, so the cohort does not use it.
- Non-harming fix: add `--full-tree` to the `ls-tree` call. Production output is unchanged, because ROOT is the toplevel.

## F5: selftest blind spots (Medium, sensitivity)

- [INFERENCE, not run] All 18 current cases match their expectations on this source. The selftest would therefore report PASS while F1-F3 are live.
- Missing cases: failed row with a receipt-complete report (F1). Mode on exit-2 paths (F2). Committed report read raising (F3). Probe mismatch (F4). Empty-bytes report (source-derived faulty, uncovered).

## Bounded holds (the attack survives here)

- **B1** receipt-malformed partial: a missing, duplicated, or mismatched Reviewed-SHA256, Predicate, or Scope line; empty bytes; invalid UTF-8; or an unpinned source gives `delivered_faulty` (61 with one_code 1). Invalid UTF-8 gives one_code 2, and the cohort exits 2 via 68-69 with rows kept. Covered by `partial-failed` and `encoding` (the latter a completed row). Empty bytes are uncovered.
- **B2** failed row with no committed report at the bound revision gives `absent_dead` (59, 129-130). A partial that exists only in the worktree is absent by construction. The attack's "not absent" premise holds only for committed partials.
- **B3** no silent drop or duplicate: seat-set equality (50-51), duplicate-name rejection (42), and the `dropped`, `duplicate`, and `unknown` fixtures (104-106). Dropping a failed row exits 2 with COHORT-SCHEMA.
- **B4** (residual, by design): `absent_dead` and `delivered_faulty` produce no finding, so exit stays 0 (66-70). C3_bound calls C3 "detection and evidence", so this is not a defect under the bound. But top-level `status` PASS can sit beside `strict_conformance` FAIL. The candidate's `partial-failed` expects exit 0 with strict_exit 1. `seat-boundary-r22.md` line 24 says clean accounting is never a clean strict receipt verdict. Main should decide whether the status word needs separating.

## Fixture verdict summary (not executed)

| Case | Attack-expected | Source-derived prediction [INFERENCE] | Result |
|---|---|---|---|
| failed row, malformed partial (`partial-failed`) | delivered_faulty, exit 0 | delivered_faulty, exit 0 | holds (B1) |
| failed row, receipt-complete partial | delivered_faulty, exit 0 | delivered_conformant, exit 0 | falsified (F1) |
| failed row, no committed report | absent_dead | absent_dead, exit 0 | holds (B2) |
| committed report read raises | per-seat category | no seats, exit 2, mode 1 | falsified (F3, F2) |
| settlement absent | exit 2, mode 0 | exit 2, mode 1 | falsified (F2) |

## Verification gaps

- No execution. Every prediction is a static trace of the cited lines.
- Declared digest not recomputed (NO-EXEC).
- `_revision.py` read at helper level only (`clean_env` and `_git` seen). `bind()` is not on the attack path.
- git semantics in F4 are documented behavior, not verified by running git.
- No installs or updates were performed.

## Receipt

Reviewed-SHA256: 34b532dda9e69ed81638151572a95f5f665a3f65b8b794d8996e5fb50f4c92e0
Predicate: r22-fxc3partial
Scope: executed=none

Lane bounds: leaf member — no subagent dispatch.
