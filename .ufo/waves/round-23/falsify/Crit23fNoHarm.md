# Crit23fNoHarm — round23 falsify: no-harm attack on C1, C2, C3 and the frontier

Seat: TsukuroiR23-2.Crit23fNoHarm-2 (critic, leaf, NO-EXEC, NO-FETCH). The preregister digest is the supplied declaration and was not computed. `skill://godspeed` was not resolvable as a file, so I used the copied directive at `.ufo/waves/round-23/sources/godspeed-directive.txt`.

## Verdict

Within the eight declared files I found **no falsifier**. No landed text that I can read weakens an existing gate, rewrites history, reauthorizes an old event, or changes a schema-v1 result. The attack did find **three no-harm claims that are asserted but not measured**. One of them, the meaning of the C1 OPAQUE_PATCH `UNKNOWN` outcome, could become a real weakening of a gate depending on how the checker maps it to an exit status. I cannot see that mapping from here.

## Bounded search

- **Read:** `preregister.json`, `sources/r22-closure.json`, `candidate/corpus/lessons/round-23.md`, `candidate/corpus/knowledge/path-reconciliation-r23.md`, `candidate/corpus/knowledge/structured-edit-r23.md`, and the godspeed directive.
- **Not readable under this binding:** tool sources (`tools/check-*.py`), the ledger `path-reconciliation.json`, `structured-edit-observations.json`, the round-22 lesson, LEARNING, QUALITY, SCORECARD, MANIFEST, and any Git history.
- **Patterns checked:** gate relaxation; retroactive authority (v2 applied to v1 seats); relabelling of retained reds; overwriting the outside verdict; arithmetic forged to agree; identity changes; whether the preregistration still predates the build.

### Checks that held

1. **C3 arithmetic.** Build has 376 agree + 2 selector-normalization = 378 requests, and 25 − 23 = 2 − 0. Falsify has 991 + 4 = 995, and 33 − 29 = 4 − 0. The named events match those counts: DebtSixReceipts:4 and ReviewReservation:4 for build, and FxC1Unknown:8/9/10/14 for falsify. This agrees with the reported 25/33 and 23/29 in `r22-closure.json` `verification.rechecks`.
2. **C3 regex claim.** I traced the quoted rough expression `:(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$` by hand. It matches only `:58-58` at the end of `<path>:raw:58-58`, so `<path>:raw` is left. The claim is correct. The six rough-only events are not retained violations in round 22, so classifying them as `selector-normalization` relabels no old violation. `path-reconciliation-r23.md` says "The other retained reds (16/17 unknown-tool, 2 exec) are untouched … and stay red" and "Any actual scope violation remains a violation".
3. **The outside verdict is kept.**
   - The closure calls the 25/33 census "approximate … selector-normalization differences, not decisive". The C3 conclusion agrees with that rather than overriding it.
   - The lesson's R23-QUALITY-TREND row says "Append the outside correction, never rewrite r22", and the lesson says "that quality unchanged assessment supersedes the author's earlier improved label".
   - The Bash requests keep the closure's wording: "process noncompliance … not retrospectively authorized".
4. **No retroactive v2 authority.** The lesson Gate table rejects "Retrospectively allow r22 report reads or edits under new v2 policy". `structured-edit-r23.md` says "Schema-v1 historical bindings remain unchanged and retain all earlier violations. No grant is retroactive." The preregister `limits` say "No historical manifest/report rewrite or retrospective authorization".
5. **The C1 decisions only tighten the policy.**
   - DECLARED_EDIT requires the target to be in edit ∩ read ∩ write.
   - WRITE_ONLY_EDIT and READ_ONLY_EDIT are denied.
   - EDIT_TRAVERSAL and EDIT_EXTERNAL are denied.
   - EXPANSION is CHECK_EACH: "A valid frontend target cannot clear an out-of-binding backend step or a forbidden command/fetch".
   - Under v1 every edit was already red as unknown-tool. None of these rows grants v1 seats anything.
6. **Frontier metadata.** The preregister has `retired: []`, `ordinal_delta: 0` and `capability_acquisition: false`, and claims no native enforcement. The lesson rejects "A new gate … automatically improves quality trend". The retry and prelude-shadow mistakes are disclosed and attributed to the lane, not hidden.

## Attacks (counterexample candidates, none confirmed)

### A1 — C1/C2: OPAQUE_PATCH `UNKNOWN` may be a clean pass

- **Claim attacked:** C1 decision OPAQUE_PATCH = UNKNOWN, and C2's v2 audit.
- **Counterexample:** a v2 seat issues an edit that has no structured `path`, only freeform patch text.
  - Under v1 the same request was red as unknown-tool.
  - `structured-edit-r23.md` step 3 says "Unknown means could-not-evaluate **or** rejection, never permission".
  - "Could-not-evaluate" is not tied to a non-zero exit or a counted violation. If the checker emits UNKNOWN without making the run non-clean, v2 is strictly weaker than v1 for this shape.
- **Evidence:** the wording above, and the preregister row `["OPAQUE_PATCH","UNKNOWN",…]`. The checker source is outside my binding, so whether this actually happens is [INFERENCE].
- **Axes:** operability and depth. It would be a hidden regression of the existing unknown-tool red.
- **Smallest remedy:** in `check-edit-contract.py`, `check-seat-bindings.py` and the prose, state that UNKNOWN is never a clean result: either exit 2 or a counted violation. Add one literal selftest where an opaque-patch edit under a v2 binding must produce a non-zero exit. A judge should reject the C2 operability claim if that control passes clean.

### A2 — C2: "historical reds unchanged" has no measurement

- **Claim attacked:** the C2 scope, "legacy schema-v1 policy and historical reds unchanged".
- **Counterexample:** C2 makes `edit` a recognized tool, which v2 needs. If tool recognition is global rather than gated by schema, replaying the round-22 waves at the landed revision would turn the r22 unknown-tool reds (edit 16/17) into a different code, or clear them. The closure's 41/46 violation counts or their codes would then drift.
- **Evidence:** the preregister C2 command runs only on `.ufo/waves/round-23/<WAVE>/…` waves. None of the readable files records a round-22 replay at the landed revision. The closure had recorded that replay's stdout ("requests378/995, violations41/46").
- **Axes:** operability and calibration, specifically an identity change in the v1 results.
- **Smallest remedy:** add one measurement: run the r22 C2 command at the landed revision against the round-22 bindings and events. Require stdout identical to the retained r22 output except `branch_tip`: 41/46 violations, with unknown-tool 16/17 and exec 2 unchanged. Until that exists, report the claim as unverified, not as satisfied.

### A3 — frontier: append-only state and the freeze are not visible to this seat

- **Claim attacked:** "never rewrite r22", and "Claims frozen … landed 56c8ba38… before any successful build spawn".
- **Counterexample shape:**
  - R23-QUALITY-TREND names a "LEARNING quality definition" change, and R23-RAW-ORDER adds QUALITY51. If either edited earlier text instead of appending, past trend judgments would be reinterpreted.
  - Separately, the integrated state 5a25c88 is later than the freeze commit 56c8ba38. If `preregister.json` changed between them, the targets were edited after the build.
- **Evidence:** both claims appear only in lesson prose. LEARNING, QUALITY, the round-22 lesson and Git history are outside my binding.
- **Axes:** freshness and calibration (provenance).
- **Smallest remedy (for L1 or the judge, not this seat):**
  - Run the closure's no-harm check again over ae01e50..5a25c88: zero deleted lines, LOG/SCORECARD/SKILL/QUALITY/README/LEARNING still prefix-preserving, and no round-22 file modified.
  - Confirm the `preregister.json` blob is identical at 56c8ba38 and 5a25c88.
  - "Before any successful build spawn" is acceptable only because refused calls spawned zero seats. Pin the freeze timestamp against the first refused call as well.

### Note — tradeoff, not harm

C3's dispositions depend on a "canonical" re-implementation that is required to equal the retained result. That ties canonical to retained, which weakens its independence as a calibration check. It does not change any v1 result, so I assign it to the quality and separability critics rather than to no-harm.

## Result for the judge

- **C1:** no harm found. A1 is open until UNKNOWN is shown to be non-clean.
- **C2:** no harm found in the prose. A1 and A2 are unmeasured no-harm preconditions.
- **C3:** no harm found. The arithmetic, the regex claim and the retained reds are preserved.
- **Frontier:** no harm found in readable evidence. A3 needs a diff check that this binding cannot perform.

No tool was installed or updated, and nothing was executed or fetched.

Reviewed-SHA256: 8f3f33eaa6e9cd1c3af369955420a13e6d5b339cc5970bec04560de2c08767e8
Predicate: r23f-crit23fnoharm
Scope: executed=none
