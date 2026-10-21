# FxC2ZeroTrace — empty recorded trace versus missing coverage

Reviewed-SHA256: c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4
Predicate: r22-fxc2zerotrace
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.

## Axes and result

Axes: distinguish present-empty from missing coverage; preserve fail-closed incomplete coverage; avoid upgrading a bounded request audit into universal absence proof.

**Bounded predicate holds by source inspection.** A valid bound seat with an explicitly present trace record, boolean `complete: true`, and `events: []` is clean for that supplied record. An absent seat record is not treated as zero requests: it produces `SCOPE-TRACE-MISSING` and `CANNOT_EVALUATE`. No source-visible counterexample to that distinction was found. This is not a runtime result or a claim that a complete-empty declaration proves no real requests occurred.

## Source evidence

All line references below are to the assigned candidate `tools/check-seat-bindings.py` unless otherwise stated.

- Lines 105–115 validate a nonempty binding population and its exact seat identities/path lists.
- Lines 116–123 require the events envelope and each present seat's identity, unique nonempty agent, boolean `complete`, and list-valued `events`. An empty list is valid; an absent/non-list `events` field is not.
- Lines 124–129 iterate every bound seat. A missing record increments `incomplete`, records `SCOPE-TRACE-MISSING`, and continues before appending a seat result.
- Lines 130–143 independently record `SCOPE-TRACE-INCOMPLETE` when `complete` is false. With a present complete-empty record, the event loop has no iterations and the seat row has zero requests and no violations.
- Lines 144–151 map any incomplete coverage to exit 2 / `CANNOT_EVALUATE`; otherwise no findings maps to exit 0 / `PASS`.
- Lines 184–190 already distinguish the `missing-trace` fixture (empty top-level seat list; expected exit 2 and missing-trace finding) from `empty-trace` (present complete seat, empty event list; expected exit 0). Lines 192–198 compare actual fixture exit codes/findings when the selftest is run; it was not run here.

## Expected fixtures — static predictions, not observed runtime

Use the valid single-seat `A` binding constructed at lines 155–156. All traces have schema `tsukuroi-seat-events-v1`; a present seat has `name: A` and `agent: agent-A`.

| Supplied trace difference | Expected exit/status | Expected findings | Expected accounting |
|---|---|---|---|
| Present seat; `complete: true`; `events: []` | 0 / PASS | None | Bound 1; requests 0; violations 0; incomplete 0; one complete seat row |
| Top-level `seats: []` | 2 / CANNOT_EVALUATE | `SCOPE-TRACE-MISSING`, site `A` | Bound 1; requests 0; violations 0; incomplete 1; no seat row |
| Present seat; `complete: false`; `events: []` | 2 / CANNOT_EVALUATE | `SCOPE-TRACE-INCOMPLETE`, site `A` | Bound 1; requests 0; violations 0; incomplete 1; one incomplete seat row |
| Events input absent (`None`), with valid binding | 2 / CANNOT_EVALUATE | `SCOPE-SCHEMA`, site `input` | Bound 1; no evaluated requests or seat rows |
| Present seat; `complete: true`; `events` omitted | 2 / CANNOT_EVALUATE | `SCOPE-SCHEMA`, site `input` | Bound 1; no evaluated requests or seat rows |

The absent-events-input case reaches the events-schema guard, not the missing-seat branch. A zero request counter therefore cannot substitute for inspecting status/findings and coverage.

## One plausible defect and expected detector

**Hypothetical mutant only:** at line 126, replace `if seat is None:` with `if seat is None or not seat['events']:`. This is a small, plausible conflation of an explicitly empty request list with an absent trace. No candidate bytes were changed.

**Expected detector:** the existing bounded `empty-trace` selftest fixture at lines 188–195. Its required exit is 0. By source reasoning, the hypothetical mutant instead returns exit 2 with `SCOPE-TRACE-MISSING` for `A`, incomplete count 1, and no seat row. That fixture would reject this mutant. The existing `missing-trace` case separately expects exit 2, so accepting missing coverage is not necessary to accept terminal empty records.

**Actual detector outputs:** pristine — not run; mutant — not run; restored — not run. No behavioral stdout/stderr or exit codes were observed. **Mutation verdict: INCONCLUSIVE / not executed**, not killed or survived. The positive bounded-predicate conclusion above is source inspection only.

## Limits, hashes, and restoration evidence

The auditor validates the supplied boolean `complete`; it does not authenticate how that value or event list was collected. A genuine zero-request history and an omitted history mislabeled complete can supply identical JSON. Neither `PASS` nor zero requests establishes universal historical absence. Line 17 explicitly excludes universal trace completeness, request effects, reading proof, and runtime prevention. The host source also declares `native_per_seat_allowlist: false`; this remains prompt-bound post-hoc detection, not preventive enforcement.

Before SHA-256: the assignment supplies `c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4`; it was not independently computed. After/restored SHA-256: not independently measured. The tool record contains only permitted source reads and this separate report write, with no source edit, mutation, import, detector execution, or restoration operation. Candidate bytes were left untouched; no exact-byte restoration was necessary. No tools were installed or updated.
