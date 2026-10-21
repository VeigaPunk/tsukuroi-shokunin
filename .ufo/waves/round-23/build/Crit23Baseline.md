# Crit23Baseline — round 23 attempt 1 critic report

Seat: Crit23Baseline (critic, leaf). Mode: NO-EXEC, NO-FETCH, source-only.
Target: `.ufo/waves/round-23/preregister.json` (declared SHA-256 supplied, not computed).
Sources read: preregister.json, sources/godspeed-directive.txt (copied directive; `skill://godspeed` not resolvable in this harness), sources/r22-closure.json, sources/structured-edit-observations.json. The report path did not exist before this write.

## Axes under attack

| Claim | Axis | Metric | Before → target | Risk examined |
|---|---|---|---|---|
| C1 | depth | validated_edit_decisions | 0 → 8 | row-count inflation |
| C2 | operability | structured_edit_mode | 0 → 1 | a mode bit flipping without any repaired behavior |
| C3 | calibration | unexplained_cohorts | 2 → 0 | explaining a net count difference while per-event differences stay hidden |

The preregister is honest at the top level: `ordinal_delta: 0`, and the C1 scope already states "new document contract, not eight repaired runtime behaviors." These findings target the gap between that honest scope and what a closure verdict of "improved" would rest on.

## F1 — C1 depth: eight rows are not eight independent decisions (fixable defect)

**Counterexample.** Four of the eight rows are cells of one conjunction. `DECLARED_EDIT` allows an edit only when the target is in all three lists: edit (E), read (R) and write (W). `UNDECLARED_EDIT`, `READ_ONLY_EDIT` and `WRITE_ONLY_EDIT` are three of its negations. The row names do not fix which bit pattern each one covers:
- Take a binding with `edit_paths=[X]`, `read_paths=[X]` and `write_paths=[]` (E∧R∧¬W). If a checker reads `READ_ONLY_EDIT` as "R only, no E" (¬E∧R∧¬W), this case matches no row. A checker that only tests E∧R would then return ALLOW, and all eight fixtures would still pass.
- E∧¬R∧¬W is also unassigned.
So eight green rows do not show that the function is right on the 8-cell (E,R,W) truth table. A mutant that drops the W conjunct survives unless the `READ_ONLY_EDIT` fixture happens to be exactly E∧R∧¬W.

**Further inflation.**
- `EXPANSION → CHECK_EACH` is not a decision value (ALLOW, DENY or UNKNOWN). It is a rule for combining per-step decisions, counted as a decision row.
- [INFERENCE] `EDIT_TRAVERSAL` and `EDIT_EXTERNAL` look like the round-22 boundary-normalization rules (r22 C1 `validated_boundary_decisions` 0/6/6) applied again under a new tool name. I could not verify this because the r22 C1 rows are outside my read binding. If true, they re-count depth that round 22 already credited.
- `before: 0` measures the absence of `tools/check-edit-contract.py` at baseline, not a measured zero. The same "new metric starts at zero" pattern was used in r22 for C1, C2 and C3.

**Impacted axes:** depth (inflated delta), calibration (the "improved" label would be miscalibrated).

**Smallest safe correction (in scope, C1 only):**
1. Define the decision as one function over the (E,R,W) bits and state an explicit precedence.
2. Pin each of the three DENY fixtures as a single-bit flip from ALLOW: `UNDECLARED_EDIT = ¬E∧R∧W`, `READ_ONLY_EDIT = E∧R∧¬W`, `WRITE_ONLY_EDIT = E∧¬R∧W`.
3. Count a row toward `validated_edit_decisions` only if a mutant that changes that row alone is caught by that row's fixture and not by the others.
4. Count `EXPANSION` as a rule, not a decision, or give it a fixture where one denied step turns an otherwise allowed edit red.
5. If 8 cannot survive the single-row mutation test, preregister the lower count instead of 8.

## F2 — C2 operability: the mode bit can be 1 with no repaired behavior (fixable defect)

**Background.** In r22 the closure's independent recount found that edit requests were counted as unknown tools in both waves (`edit16/17=unknown-tool16/17`). Classifying those requests is the real behavior C2 should repair. But C2 leaves schema-v1 reds untouched and applies only to explicit v2 bindings. On frozen r22 data it therefore classifies nothing. Any improvement can only show up in round 23's own wave, which is bound by the same planner that defines the policy.

**Counterexample 1 (vacuous pass).**
- `.ufo/waves/round-23/<WAVE>/bindings.json` declares schema v2 with `edit_paths`, so `structured_edit_mode` becomes 1.
- If `events.json` for that wave has zero captured edit requests, or every edit request is still bucketed as an unknown tool, the metric still reads 0 → 1.
- No ALLOW, DENY or UNKNOWN edit decision was exercised on a real event.

**Counterexample 2 (seen live in this seat).** This critic seat runs in a harness whose structured-edit tools are named `StrReplace` (keys `path`, `old_string`, `new_string`) and `Write`, not `edit` or `write`. If the v2 classifier keys on the tool name `edit`, an edit request from this harness lands in the unknown-tool bucket. That is the same failure r22 reported, and the mode bit would still read 1. The preregister disclaims universal tool semantics, but it then needs to say how unrecognized edit-shaped requests are counted.

**Counterexample 3 (from the frozen S086 observations).** CritRuntime's edit (`argument_keys` = `path`, `stream_content`) recorded two adapter steps: a read of `…/CritRuntime.md:raw` and a write of `…/CritRuntime.md`.
- Under `EXPANSION/CHECK_EACH`, the `:raw` read must be scoped on its own.
- If `EDIT_TRAVERSAL` ("no … alternate spelling expands the target list") applies literally, the adapter's own read is denied, and a correctly declared edit goes red.
- If the checker strips `:raw` instead, that is an unstated normalization rule.
- The r22 closure attributes the 25/33 versus 23/29 path-count gap to "selector-normalization differences", so C3 has to rule on the same `:raw`-style selectors. The separability statement says C2 and C3 share only the revision binding. In fact both depend on the selector-normalization rule, and two independent implementations of it would be duplicate authorities that can diverge.

**Impacted axes:** operability (credit for a mode flip with no behavior exercised), calibration (C2 and C3 may disagree on selectors), and the separability claim.

**Smallest safe correction:**
1. Report C2 as the mode bit plus exhaustive counts over the wave's captured events. These counts are fields the checker emits, not extra commands: edit-shaped requests seen, how many got ALLOW, DENY and UNKNOWN, and how many fell into unknown-tool.
2. Allow mode=1 to count only when at least one real ALLOW and one real DENY or UNKNOWN edit decision appear, or when the four frozen S086 observations replay to a decision under a declared v2 projection.
3. Classify unrecognized edit-shaped tool names as UNKNOWN, keep them visible in the counts, and never drop them silently.
4. Declare one closed selector-normalization row (for example, a recorded read-adapter step whose path is a declared target plus a selector from a fixed list such as `:raw` maps to that target; nothing else does). C2 and C3 should cite that single row as shared infrastructure, and the separability text should say so.

## F3 — C3 calibration: explaining the net difference is not exhaustive (tradeoff unless pinned)

**Counterexample.** The reported gaps are +2 for build (25 vs 23) and +4 for falsify (33 vs 29). A reconciliation can produce "declared arithmetic" that sums to +2 and +4 from offsetting errors. For example, rough counts three paths the lane drops and the lane counts one the rough census misses. `unexplained_cohorts` would reach 0 while the per-event mapping is wrong.

The r22 closure itself calls its own census "approximate" and "not decisive". [INFERENCE] If the S085 source cell holds only cohort totals rather than a per-event path list, an exhaustive per-event explanation cannot be built without rerunning the rough census, which the C3 scope rules out ("does not … retry historic checks for confirmation"). I could not open S085; it is outside my binding.

**Impacted axes:** calibration (false provenance if per-event rows are reconstructed rather than frozen).

**Smallest safe correction:**
1. Require the reconciliation to list the symmetric difference per cohort: paths only the rough census counted and paths only the lane counted, each with an event and component reference and a reason class. The arithmetic must be `rough = common + rough_only` and `lane = common + lane_only`, not a single net delta.
2. If S085 carries only totals, say so and lower the claim to "net difference explained under declared normalization". Do not claim "exhaustive per-event" in that case.

## Verdict split for the canonical judge

- **Fixable before landing:** F1 (pin fixtures as single-bit flips and require single-row mutation kills), F2 (mode bit plus event counts, the shared selector row, and the unknown-tool bucket).
- **Must reject if unfixed:** counting C2's 0 → 1 as an operability improvement when the wave's events show zero classified edit decisions, and counting C1 as 8 when fewer rows survive single-row mutation.
- **Not challenged:** limits on native enforcement (stated correctly); `ordinal_delta: 0`; the baseline identity `ae01e50f…` matches the r22 closure commit.

No tools installed, no commands run, no fetches.

Reviewed-SHA256: 8f3f33eaa6e9cd1c3af369955420a13e6d5b339cc5970bec04560de2c08767e8
Predicate: r23-crit23baseline
Scope: executed=none
