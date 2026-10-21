# ConnPlanner — round 22 bounded planning data walk

**Seat** `TsukuroiR22.ConnPlanner-3` (leaf planning data walk). L1 holds the canonical planner and sole production/VCS integrator role; this file is advisory input to L1's plan and edits no claim, manifest, source, or fleet state.

**Baseline** `894d1e20fb4939b0cc4fadf722c46d1429f257d2` (`preregister.json` `baseline`).

**Read set (exclusive)** `.ufo/waves/round-22/snapshot/corpus/QUALITY.md`, `.ufo/waves/round-22/preregister.json`, `.ufo/waves/round-22/sources/host-tool-boundary.json`, `skill://godspeed`.

**Write set** this file only.

**Execution class** `NO-EXEC`: no bash/eval/subprocess/import/test/compile/run, no URL/network/xd fetch, no child task. Tool calls used for this report: `read` on the four declared read paths and `write` on this path.

**Reviewed digest** the assignment-declared SHA-256 for `QUALITY.md`, reproduced once in the receipt at the end. `NO-EXEC` forbids `sha256sum`, so this seat binds the digest by declaration and does not recompute it. QUALITY item 42: “A receipt is a declaration, not proof of actual reading or command nonexecution.”

Labels used below: **[OBS]** content observed in the declared read set; **[INF]** planning inference or design requirement; **[UNK]** not observable from this seat. QUALITY item 3: “Observation, inference, and unknown stay separate.”

## 1. Axes named

| Axis | Ordinal [OBS] | Claim | Target [OBS] | Metric kind |
|---|---:|---|---|---|
| depth | 8 | C1 | `validated_boundary_decisions` 0→6 | count |
| adjacency | 8 | none | — | unclaimed |
| coverage | 9 | none | — | unclaimed |
| operability | 9 | C2 | `request_audit_mode` 0→1 | mode |
| freshness | 9 | none | — | unclaimed |
| calibration | 9 | C3 | `cohort_accounting_mode` 0→1 | mode |

Anchor: `preregister.json` `ordinals` = `{"depth":8,"adjacency":8,"coverage":9,"operability":9,"freshness":9,"calibration":9}`; `ordinal_deltas` = `0`; `claims[0]` = `"metric":"validated_boundary_decisions","before":0,"target":6`; `claims[1]` = `"metric":"request_audit_mode","before":0,"target":1`; `claims[2]` = `"metric":"cohort_accounting_mode","before":0,"target":1`.

Depth is tied-lowest with adjacency at 8. Exactly one of the two tied-lowest axes carries a claim (depth), and it carries the only multi-instance target (6). The two binary-mode claims sit on ordinal-9 axes.

## 2. Three claims → independent predicates

Only the metric names, targets, and command strings are **[OBS]** (`preregister.json` `claims[0..2]`). The predicate definitions below are planning requirements **[INF]**, because the tool internals and output schemas were not read (out of the declared read set).

### 2.1 Mapping table

| Claim | Predicate | Pass condition | Exclusive inputs (per preregister command) | Minimal negative control |
|---|---|---|---|---|
| C1 depth | **P1** validated-decision enumeration | ≥6 distinct decision tuples, each with explicit boundary class, explicit outcome, resolving evidence anchor, and a falsifier or opinion tag; count derived from the tuples, not asserted | revision tree artifacts at `REV` only | flip one decision outcome with ID and anchor unchanged |
| C2 operability | **P2** fail-closed request audit | mode 1 only if every captured request is classified `conformant`/`violation`/`cannot_evaluate`, every unclassifiable request is non-clean, the captured set is non-empty, and no enforcement claim is made | `bindings.json` + `events.json` only | one request to an undeclared path; one unclassifiable event; one empty event set |
| C3 calibration | **P3** four-class cohort accounting | mode 1 only if every declared seat is assigned exactly one of `delivered-conformant`, `delivered-faulty`, `absent-dead`, `absent-unresolved`; settlement seat set equals declared set; strict receipt findings preserved; no replacement seats | `reviews.json` + `settlement.json` only | one seat with period-appended `none.`; one declared seat with no report and no death record; one provider-death record; duplicate or missing seat |

### 2.2 P1 — depth

```
P1(REV) := |{d : d ∈ Decisions(REV),
                  unique id(d),
                  explicit boundary_class(d) ∧ explicit outcome(d),
                  resolves(evidence_anchor(d), REV),
                  falsifiable(d) ∨ opinion(d)}| ≥ 6
```

Requirements **[INF]**:

1. The output enumerates one tuple per counted decision: `decision_id`, `boundary_class`, `outcome`, `evidence_anchor`, `falsifiable|opinion`. The summary count must equal the number of tuples and must not count duplicate IDs.
2. “Validated” means the evidence anchor resolves at `REV` and supports the stated outcome; an ID present with an unreadable or absent anchor is not counted.
3. Each decision is itself a claim, so it must be falsifiable or explicitly marked opinion. QUALITY item 1: “Every claim falsifiable or marked opinion.”
4. Expected outcomes must not be imported from the gate under judgment. QUALITY item 36: “Independent expected outputs precede candidate outputs and must not import the binder under judgment.”

Failure modes P1 must reject: duplicate ID padding the count; six tuples all of one boundary class with no class breadth; an anchor that resolves to a different decision; an outcome present but unsupported; a decision marked opinion counted as validated without disclosure.

### 2.3 P2 — operability

```
P2(REV) := mode = 1
        ∧ Events(REV) ≠ ∅
        ∧ ∀e ∈ Events(REV): class(e) ∈ {conformant, violation, cannot_evaluate}
        ∧ (unclassifiable(e) ⇒ status(e) ≠ clean)
        ∧ output_claims_detection_only
```

Requirements **[INF]**:

1. `events.json` records dispatch-time request metadata — request identity, declared binding reference, observed tool/path/arguments, class, finding ID. It is not reconstructed from the seat's report prose. QUALITY item 46: “record actual tool-call metadata separately.” QUALITY item 42: a receipt is not proof of reading or nonexecution.
2. Fail-closed means an unclassifiable request yields `cannot_evaluate` with a non-clean status, never a silent pass. A missing binding for a declared seat is `cannot_evaluate`, not `conformant`.
3. An empty or shrunken event set cannot pass mode 1. Cardinality is printed and reconciled to the declared dispatch set.
4. A `CANNOT_EVALUATE` result that echoes its requested input is diagnostic only. QUALITY item 39: “that field is diagnostic, not an accepted binding.”
5. The binding is prompt-level and post-hoc. Host source: `native_per_seat_allowlist` is `false`; `tools_semantics` is “Eval-defined additive extras; not an allowlist or replacement of native tools”; `approved_scope` is “prompt-level scope bindings plus fail-closed post-hoc audit; C3 detection/evidence not preventive enforcement.” `preregister.json` `host_decision` ends “Never call this runtime enforcement.”

Failure modes P2 must reject: one conformant request producing mode 1 with the fail-closed branch unexercised; an undeclared-path request passed as conformant; an event with unknown tool/arguments silently dropped; wording that claims prevention or blocking.

### 2.4 P3 — calibration

```
P3(REV) := mode = 1
        ∧ Seats(settlement) = Seats(manifest)
        ∧ ∀s ∈ Seats: exactly_one(class(s), {
              delivered-conformant, delivered-faulty, absent-dead, absent-unresolved})
        ∧ strict_receipt_findings_preserved
        ∧ no_replacement_seats
```

Requirements **[INF]**:

1. `delivered-conformant` requires a present report whose receipt is strict. A period-appended `none.` is non-clean. QUALITY item 44: “Missing reports and period-appended `none.` stay non-clean under the original scope gate.”
2. `delivered-faulty` covers a present but non-conformant report, including malformed trailers and receipt content that contradicts observed tool metadata. QUALITY item 46: “a literal `Scope: executed=none` never overrides an observed Bash/eval/child invocation.”
3. `absent-dead` requires an observed provider outcome, not mere absence. QUALITY item 44: reconcile with “a delivered report or observed provider death,” and “never a fabricated placeholder or replacement.”
4. `absent-unresolved` is the residual for no report and no death record. It is accounted but not clean; accounting completeness is not conformance.
5. `preregister.json` `C3_bound`: “Account for every declared seat as delivered-conformant, delivered-faulty, absent-dead, or absent-unresolved”; the same field says this is detection and evidence, “not an every-receipt-conforms claim.”
6. “Every declared seat” is scoped to `reviews.json`. If a round-level claim covers the union of `bindings.json` and `reviews.json`, that union needs its own roster reconciliation; neither mode supplies it.

### 2.5 Independence

**Disjoint inputs.** P1 reads revision tree artifacts; P2 reads `bindings.json` and `events.json`; P3 reads `reviews.json` and `settlement.json`. No predicate consumes another's output or expected values. The preregister commands are separated accordingly (`claims[0..2]`).

**Non-entailment witnesses** (abstract states, no execution): S1 has P1 true, P2 false, P3 false (six decisions land; no audit or cohort artifacts). S2 has P2 true, P1 false, P3 false (audit runs on a revision with no boundary contract). S3 has P3 true, P1 false, P2 false (cohort accounted with neither new tool green). These are constructible because the input sets are disjoint, so no claim's green entails another's.

**Common-mode surfaces that remain:**

1. **Revision binding.** All three commands take `--revision <REV>`. QUALITY item 28: “every lane gate imports `tools/_revision.py` for branch/revision checks” and “Keep the measuring judge independent of that module.” One shared binder defect can make all three predicates agree wrongly. Three greens are not three independent revision confirmations.
2. **Roster origin.** If `bindings.json` and `reviews.json` are generated from one roster, a missing seat disappears from both P2 and P3 and both can pass on a shrunken set. Each predicate must print its declared-set cardinality and reconcile it to an independent roster.
3. **Report prose.** If `events.json` is reconstructed from reports, P2 and P3 both trust receipt text. QUALITY item 42 forbids treating a receipt as proof.
4. **Mode abstraction.** C2 and C3 both report a `*_mode` scalar. If one code path or one shared schema emits both modes, the two claims stop being independent. Each mode needs its own tool, schema, and inputs, as the preregister commands imply.

Independence is therefore a verdict-level property, not a whole-pipeline property. It holds only if the three common-mode surfaces above are separately judged and separately reported.

### 2.6 Explicit contradictions (not smoothed into a scalar)

1. **“Three independent predicates” vs one revision binder.** Verdict independence coexists with a shared `_revision.py` substrate. QUALITY item 28 requires both the shared module and an independent judge; a summary must not present three greens as three independent revision results.
2. **C3 accounting vs C3 conformance.** A mode-1 green can coexist with red strict-receipt findings. `C3_bound` explicitly says detection/evidence, “not an every-receipt-conforms claim”; no summary may call such a cohort “clean.”
3. **C2 detection vs enforcement.** Host source says no native per-seat allowlist and approved scope is prompt-level plus post-hoc. Any predicate or report that says “prevented,” “blocked,” or “enforced” is false against `native_per_seat_allowlist: false` and `host_decision` “Never call this runtime enforcement.”
4. **Depth metric vs depth ordinal.** `ordinal_deltas` is `0`. C1 can move `validated_boundary_decisions` 0→6 while depth remains 8. A report claiming depth 8→9 contradicts the preregister unless it appends a named superseding declaration.
5. **Tied-lowest adjacency has no claim.** No C1–C3 configuration closes the depth/adjacency 8 tie or makes all axes 9. Any “all axes improve” summary is unsupported by `ordinals`, `ordinal_deltas`, and `limits`.

## 3. Depth against the tied-lowest tier

**[OBS]** depth 8 and adjacency 8 are the two lowest ordinals; the other four axes are 9. `ordinal_deltas` is 0. C1 targets 6 instances, C2 and C3 target binary modes.

**Comparison.** The lowest tier carries the round's largest and most expensive target; the two cheap targets sit on upper-tier axes. The inverse relation between ordinal level and target magnitude is consistent with depth being the current constraint, but it is not evidence that six decisions raise the ordinal. The preregister freezes the ordinal delta at zero, so the honest final statement after a green C1 is: “depth metric 0→6 at `REV`; depth ordinal unchanged at 8; adjacency remains 8 and unclaimed.”

**Planning consequences [INF]:**

1. Do not let the cheap C2/C3 mode greens stand in for depth substance. They are on already-higher axes and are binary.
2. Do not sequence C1 last as a “cheap wins first” optimization. A presence-only C1 is the round's most misleading green precisely because it sits on the tied-lowest axis.
3. A green C1 supports depth evidence only if its six decisions are class-distinct and outcome-sensitive. If the evaluator later re-grades depth from the metric, class breadth matters more than the count; a class-degenerate six does not support a tier move.
4. Adjacency's 8 is an unclaimed residual. It is not a defect of C1, but it caps what the round can claim about the frontier.

## 4. Selected minimal one-case-overfit / generalization risk

**R-1: C1's six-count is presence-degenerate.**

- **Minimal case.** Flip exactly one decision's `outcome` while leaving its `decision_id` and `evidence_anchor` unchanged.
- **Required observable.** The gate reports five validated decisions plus one explicit outcome-mismatch or `cannot_evaluate`; it must not report 6.
- **Why it is minimal.** One field mutation in one decision record; no new seat, no new manifest, no execution by this seat. L1 can run it post-integration under QUALITY item 24 (“only L1 performs authorized verification after integration”) and item 31 (`NO-EXEC` with “the literal trailer `Scope: executed=none`”).
- **Overfit face.** If the gate counts IDs or tuples without checking the outcome against an independent expectation, six instances of one decision shape pass. The metric then measures instance presence, not “six explicit boundary decisions.”
- **Generalization face.** A seventh legitimate boundary class absent from the literal expected set is either silently uncounted (the metric under-reports a valid contract) or rejected (the gate overfits the current case set). The class schema must be authored before the six IDs are read.
- **Depth link.** Depth is tied-lowest at 8 and C1 is the only claim on a tied-lowest axis. A presence-only 6/6 would falsely indicate that the lowest axis gained substance without exercising outcome discrimination.

**Not selected, retained separately (no scalar synthesis):**

- **R-2 shared-revision one-case.** One valid `REV` exercises no malformed branch, missing branch, merge-base, unlanded, or unpushed case, yet all three gates bind through one `_revision.py`. This is a common-mode overfit, not a C1-specific one; it is handled by the independent judge requirement, not by R-1.
- **R-3 C2 zero-violation mode.** A single conformant captured request can yield mode 1 with the fail-closed branch never exercised.
- **R-4 C3 one-class cohort.** A one-seat cohort exercises one of four classes; the precedence between `delivered-faulty` and `delivered-conformant` (period-appended `none.`) and between `absent-dead` and `absent-unresolved` is untested.

## 5. Proposed move (one bounded proposal)

**Enumeration-first claim evidence.** Require each claim's green to be derived from a printed per-case tuple enumeration rather than a bare scalar, with one negative fixture per claim:

- **C1** prints one tuple per decision: `decision_id`, `boundary_class`, `outcome`, `evidence_anchor`, `falsifiable|opinion`. The count is recomputed from the tuples; a flipped outcome must drop the count or emit `cannot_evaluate`.
- **C2** prints one tuple per captured request: request id, binding reference, observed target, class, finding id. Unclassifiable requests are non-clean; an empty set cannot pass.
- **C3** prints one tuple per declared seat: seat id, one of four classes, report/evidence reference, preserved strict-receipt findings. The declared seat set must equal the settlement seat set.
- **Shared annex** judges the revision binder independently (QUALITY item 28) and records its result separately from the three claim results.

This is a single structural move: the same enumeration discipline across the three claims, plus one shared independence annex. It adds no claim, no enforcement assertion, no replacement seat, no ordinal claim, and no production edit by this seat.

**Affected axes.**

- **depth (improve):** C1 becomes class-distinct and outcome-sensitive, so 0→6 measures validated decisions rather than tuple presence.
- **calibration (improve):** every case is visible and countable; the R-1/R-3/R-4 overfits become explicit red controls rather than hidden generalizations.
- **operability (improve, detection-only):** P2 exposes per-request fail-closed behavior; it does not become preventive enforcement.
- **adjacency, coverage, freshness (neutral):** no claim targets them, and the move reads no artifacts on their behalf.
- **Harm check:** no new preventive claim, no ordinal movement claim, no replacement seats, no rewrite of round-21 reports or manifests (`preregister.json` `limits`: “No replacement seats”; “Original round21 reports and manifests remain immutable”).

## 6. Risks of the move

1. **Class-schema overfit.** If the boundary classes are authored from the same six decisions, R-1 survives in a new form. Mitigation: author the class list before reading the decision set, and add a seventh-class fixture that must be accepted or explicitly reported unsupported.
2. **Enumeration noise.** Long tuple lists can obscure the count. Mitigation: one machine-readable line per case, and a summary count derived from the lines, not typed independently.
3. **Legitimate `cannot_evaluate`.** A missing independent expectation must produce a non-clean result, never a fabricated pass. QUALITY item 39: a `CANNOT_EVALUATE` echo is “diagnostic, not an accepted binding.”
4. **Empty or shrunken sets.** C2 and C3 can pass vacuously on an empty manifest. Mitigation: cardinality guards and reconciliation to an independent roster.
5. **Shared revision substrate.** A single binder can make all three enumerations fail or pass together. Mitigation: the independent judge annex and negative revision cases; do not count three greens as three independent revision confirmations.
6. **Receipt trust.** If `events.json` comes from report prose, P2 and P3 share a false witness. Mitigation: dispatch-time metadata only (QUALITY items 42 and 46).
7. **Scope creep.** Adding “preventive” wording or a fourth claim would contradict the host boundary and the preregister `limits`. Mitigation: reject such wording in review.

## 7. Verification (L1 only; this seat executes none)

**Commands [OBS] from `preregister.json` `claims[0..2]`:**

```
python3 tools/check-boundary-contract.py --revision <REV>
python3 tools/check-seat-bindings.py --revision <REV> --manifest .ufo/waves/round-22/build/bindings.json --events .ufo/waves/round-22/build/events.json
python3 tools/check-review-cohort.py --revision <REV> --manifest .ufo/waves/round-22/build/reviews.json --settlement .ufo/waves/round-22/build/settlement.json
```

**Assertions [INF]:**

1. C1 enumerated count ≥6 distinct decision IDs, each with a class, an explicit outcome, a resolving anchor, and a falsifier/opinion tag; summary count equals tuple count.
2. C2 tuple count equals captured-request count; no request is unclassified; every unclassifiable request is non-clean; output says detection, not enforcement.
3. C3 tuple count equals declared-seat count; every seat has exactly one class; settlement seat set equals declared set; strict receipt findings are retained.
4. The revision judge is independent of `tools/_revision.py` and covers malformed-branch, missing-branch, merge-base, unlanded, unpushed, and invalid-revision cases (QUALITY item 28).
5. The final report states metric movement only (0→6, 0→1, 0→1) and does not claim an ordinal delta (`ordinal_deltas` is 0).

**Negative fixtures:** flip one C1 outcome; add one C2 request to an undeclared path and one unclassifiable event; add one C3 seat with period-appended `none.`, one declared seat with no report and no death record, one provider-death record, and one duplicate or missing seat. Each fixture must move exactly the targeted tuple, not the whole mode.

**No verification is claimed by this seat.** The above is a prospective plan for L1's post-integration run.

## 8. Unknowns and limits

- **Tool internals and output schemas [UNK]:** `tools/check-boundary-contract.py`, `tools/check-seat-bindings.py`, and `tools/check-review-cohort.py` were not read; they are outside the declared read set. P1/P2/P3 are design requirements, not observations of current behavior.
- **Decision names and boundary classes [UNK]:** no repository evidence for the six decisions or their classes is in the declared read set. This report deliberately does not invent them.
- **Manifest contents and seat counts [UNK]:** `bindings.json`, `events.json`, `reviews.json`, and `settlement.json` were not read. Whether any violating request or dead seat exists is unknown; if absent, the audit must report `cannot_evaluate` rather than pass fail-closed or complete.
- **Digest recomputation [UNK]:** forbidden by `NO-EXEC`; the reviewed digest is declared, not recomputed.
- **Execution and integration [UNK]:** none performed by this seat. All verification is prospective and assigned to L1 (QUALITY item 24).

Reviewed-SHA256: 7f2bd22429b53446939e56bcfdfb188126fe711e5cc72ef957e2a0140206e14d
Predicate: r22-connplanner
Scope: executed=none
