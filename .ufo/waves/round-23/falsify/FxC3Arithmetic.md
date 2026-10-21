# FxC3Arithmetic — round23 FALSIFY, attempt1

Attacked claim: **C3** (calibration, `unexplained_cohorts` 2 → 0), specifically the "declared arithmetic" evidence: the cohort identity `rough - retained == selector-normalization - sum(unit extra)` (`cohort_findings` L183-185), the totals checks (L175-182), and the per-row dispositions they rest on (`derive` L136-143).
Target: `.ufo/waves/round-23/candidate/tools/check-path-reconciliation.py` (supplied identity, not recomputed).
Method: static reading only (NO-EXEC/NO-FETCH). I did not read the r22 snapshot `events.json`/`bindings.json`/`audit.json` because they are not in this seat's read paths. So whether any falsifier below matches a real r22 row is **[INFERENCE: unknown]**. Each falsifier is a concrete input that the landed rules mishandle.

## Verdict

- **The identity is a tautology and never fires alone.** For each row, the disposition definitions force `rough - retained` to equal that row's contribution to `selector-normalization - unit_extra`. So `RECONCILIATION-ARITHMETIC` can only fire when `RECONCILIATION-UNEXPLAINED` or `RECONCILIATION-ORPHAN-FINDING` has already fired. `RECONCILIATION-CANONICAL-MISMATCH` has the same problem. Neither check independently witnesses anything.
- **Cancelling errors can still balance, in two ways.** A row can be labelled `agree` even though rough and canonical flagged different components (F1). A fetch-class row can be labelled `selector-normalization` (F2). Both keep every totals check and the identity satisfied, because the identity absorbs any row that gets an explained label.
- **Faithful parts.** The re-authored rough rule (`rough_event`, L61-72) is logically equivalent to the S085 source cell for every input where the source cell printed a number. The canonical rule (`canonical_event`) matches the snapshot lane `classify` path-denial semantics. I found no counterexample in either.

## F3: the identity and the canonical-mismatch check are redundant

Per-row algebra. Write `r` for `rough_path_count`, `c` for `len(canonical)` and `k` for `retained_path_count`.

| disposition | admitted when | `r - k` | contribution to `SN - unit_extra` | `c - k` |
|---|---|---|---|---|
| agree | `r == c == k` | 0 | 0 | 0 |
| selector-normalization | `r=1, k=0, c=0` | +1 | +1 | 0 |
| unit-difference | `r=1, k=c>1` | `1-k` | `-(k-1)` | 0 |
| unexplained | otherwise | any | 0 | any |

Totals: `R - K = Σrows(r - k) - orphans`. With no unexplained rows and no orphans, `R - K == SN - unit_extra` holds exactly, and `C == K` holds exactly.

- So `RECONCILIATION-ARITHMETIC` (L184-185) and `RECONCILIATION-CANONICAL-MISMATCH` (L181-182) are corollaries of the per-row dispositions plus the orphan check. Neither can be the sole finding.
- **Cancelling inside these checks.** Two unexplained rows with `r-k = +1` and `r-k = -1` balance both identities. This is selftest case `offsetting-pair-net-zero`. A rough-only unexplained row plus one orphan retained finding also balances. Only the per-row `UNEXPLAINED` and `ORPHAN` findings catch these, which confirms the totals checks add no detection.
- **Untested and unmutated.**
  - No selftest case expects `RECONCILIATION-ARITHMETIC` or `RECONCILIATION-CANONICAL-MISMATCH` (L291-329). `wrong-arithmetic-total` expects `RECONCILIATION-LEDGER-MISMATCH`.
  - `measure/l1-mutation.json` mutants 0-9 for this tool touch neither line, nor the `ROUGH-COUNT` line, the `agree` condition or the selector-normalization `!=` clause.
  - So deleting L181-185 would very likely survive `--selftest` **[INFERENCE: not executed]**.
- **The non-vacuous totals checks.** `RECONCILIATION-ROUGH-COUNT` (`R` against the outside 25/33) and `RECONCILIATION-RETAINED-COUNT` (`K` against 23/29) are the only totals checks that anchor the ledger to outside observations.
- **Impacted axis:** calibration, through false provenance. "Declared arithmetic" in the C3 scope reads as an independent witness but is definitional.
- **Remedy (choose one):**
  - Preferred: delete L181-185 and describe C3 evidence as "per-row dispositions plus the two outside-count anchors".
  - Smallest: keep the lines, but state in the docstring or claim scope that they are algebraic corollaries, not evidence.
  - Either way, add a selftest or mutant only if a check is meant to stay load-bearing.

## F1: `agree` accepts a mismatched component pair

Falsifier, a single grep event:

    tool=grep  path="<LANE>/a.md:raw:1-2;/outside"  read_paths=[<LANE>/a.md]

- **Rough rule.** On component 0, the `ROUGH_SUFFIX` match strips only `:1-2`, leaving `a.md:raw`, which is not in the read paths. That gives `('path', 0)`, the same result as unit control `rough-misses-raw-first`. Rough stops there, so `r=1, first_bad=0`.
- **Canonical rule.** Component 0 normalizes to `a.md` and is allowed. Component 1, `/outside`, fails `_local`. So `canonical=[1]`, `c=1`.
- **Lane rule** (snapshot `check-seat-bindings.py` `requested_path`). Component 0 is allowed. Component 1 gives one `SCOPE-PATH-DENIED`, so `k=1`.
- **Result.** `r == c == k == 1`, so the row is labelled `agree` (L136). But rough's hit is a selector artifact on component 0, and the real denial on component 1 was never reached by rough. Two errors cancel inside the row, and all totals checks and the identity stay satisfied.
- **Inconsistent guards.** `unit-difference` does guard this case with `first_bad == canonical[0]` (L141). The same spelling with two bad tail components ends up `unexplained`, but with one it ends up `agree`.
- **Impacted axes:** calibration, and the C3 scope wording "exhaustive per-event/component explanation".
- **Smallest remedy.**
  - Tighten `agree` to: `rough_count == len(canonical) == kept and (first_bad is None or canonical[:1] == [first_bad])`.
  - Add selftest case `agree-component-mismatch` with the event above and `audit('S:0')`, expecting `RECONCILIATION-UNEXPLAINED`.
  - Risk: if such a row exists in the r22 cohorts, C3 would truthfully regress from 0. That would be a correct outcome, not a defect of the fix.

## F2: a fetch spelling is labelled `selector-normalization`

Falsifier:

    tool=read  path="https://example.invalid/:1-5"  (any binding)

- **Rough rule.** Stripping gives `https://example.invalid/`, which is not in the read paths. So `r=1, first_bad=0`.
- **Canonical rule.** The URL is skipped (L101-102), so `c=0`.
- **Lane rule.** `SCOPE-FETCH-DENIED`, not a path denial, so `k=0`.
- **Why it becomes selector-normalization.** The `!=` clause (L139) compares `ROUGH_SUFFIX.sub(comp)` (`https://example.invalid/`) with `canonical_base(comp, True)`. Because `//example.invalid/` is not a selector token, `canonical_base` returns the unchanged value. The two differ, so the row is labelled `selector-normalization`, and the identity balances with SN increased by one. The real cause is that rough lacks a fetch class, not selector grammar. The same happens with `localhost:9222/a:5`.
- **A plain URL behaves differently.** `https://example.invalid` with no suffix makes both normalizations equal, so it is `unexplained`. Whether a fetch row gets an explanation therefore depends on whether it has a range-like suffix.
- **The `!=` clause is otherwise dead.** For non-URL components, `c=0` already means `canonical_base ∈ authority` while the rough-stripped value is not, so the two necessarily differ. A `skill://godspeed` component cannot reach `c=0` with `r=1`. So the clause only decides URL rows, and decides them wrongly.
- **The selftest comment is false.** Comment L328 says "URL is a separate class in both totals", but rough counts URLs as `path` and case `non-path-events` contains no URL.
- **Impacted axes:** calibration, through a false selector-normalization count.
- **Smallest remedy.**
  - In the selector-normalization branch, replace the `!=` clause with `not re.match(r'(?i)^https?://', comp) and not re.match(r'^[^/:\s]+:[0-9]+/', comp)`, where `comp` is the first bad component. URL rows then become `unexplained` unless a separate disposition is designed later.
  - Add selftest case `url-selector-not-normalization`: read `https://example.invalid/:1-5`, `audit()`, expecting `RECONCILIATION-UNEXPLAINED`.
  - Correct the L328 comment.

## Bounded search with no falsifier

- **Rough re-authoring against S085.** Same tool sets, `bash` short-circuit, `split(';')` for grep/glob, `strip_sel` regex with `re.sub`, write without stripping, and break at the first bad component. They differ only for non-dict truthy `args`, where the source would raise and print no number. So no cancelling divergence is possible for the admitted outside counts.
- **Canonical against the lane `requested_path`/`local`.** Fetch-first ordering, the `skill://godspeed` special case, the selector token grammar and `local` characters all match. Lane failures that produce schema errors (missing, non-string or non-dict args; `functions.`-qualified or parallel tools) yield `unexplained` rows, never silent agreement.
- **Cross-row cancellation inside explained labels.** Impossible: `agree`, `selector-normalization` and `unit-difference` are all per-row equalities, so only `unexplained` rows can offset each other, and they are always reported.

## Classification

F1 and F2 are fixable defects within scope; they are not tradeoffs. F3 is a provenance defect. It needs rejection only if C3's admission relies on the identity as independent evidence; otherwise the fix is deletion or rewording.

Lane bounds: leaf member — no subagent dispatch.
Reviewed-SHA256: fd0393be9140579424bdfc3c099b2b82fee11ccf9306d926c998235ce7ee1a6b
Predicate: r23f-fxc3arithmetic
Scope: executed=none
