# ReviewReservation — predispatch chronology predicate

## Axes

- **Identity:** each dispatch is bound to its exact seat/request and matching reservation.
- **Bytes:** each committed manifest and primary snapshot is bound to its declared content.
- **Order:** reservation and manifest commits are in the commit ancestry of the revision captured for the dispatch.
- **Fail capability:** missing, ambiguous, mismatched, or unverifiable evidence fails closed; timestamps cannot turn it into a pass.

## Predicate

For each dispatched request `d`, let `G(d)` be the full commit ID containing its grant/reservation, `M(d)` the full commit ID containing the exact manifest and primary snapshot declarations, `H(d)` the repository `HEAD` captured immediately before submitting that exact dispatch, and `T` the measured final revision. Let `≼` mean “is the same commit as, or an ancestor of,” determined from Git parent links, not commit dates.

`PREDISPATCH(d) = PASS` **iff all** of the following hold:

1. **Unique contemporaneous binding:** there is exactly one dispatch-start record for `d`, identifying the exact seat/request and effective routed identity, and that record captures `H(d)` as the pre-call `HEAD`. It identifies the matching grant and manifest; no grant is ambiguously reused or exceeds its declared reservation. The call-time record must have verifiable contemporaneous/immutable provenance, not merely a later author-written assertion.
2. **Exact committed content:** the grant/reservation and manifest/snapshot paths exist at their identified commits. The blob identities at those commits equal the expected declared bytes/digests; every primary snapshot also matches its pinned origin. Missing paths, malformed declarations, or any byte mismatch fail.
3. **Commit-graph chronology:** `G(d) ≼ H(d)`, `M(d) ≼ H(d)`, and `H(d) ≼ T`. Thus the exact grant and manifest already exist in the revision captured for the call, and that revision is on the measured history. A grant/manifest first appearing only after the captured dispatch revision fails, even if its timestamp is earlier.
4. **Closed accounting:** every dispatched request has one matching predispatch reservation and manifest, and every declared reservation/manifest is accounted for. Missing, duplicate, conflicting, or unresolved records fail; none are silently dropped or replaced.

Any failed or unobservable clause yields **FAIL / UNRESOLVED, never PASS**. Timestamps, file mtimes, receipt text, and provider timestamp metadata are context only; they satisfy none of these clauses. In particular, ancestry without a contemporaneously integrity-bound `H(d)` cannot prove that a later assertion of the dispatch revision was not backfilled. If the dispatch system cannot supply that binding, the chronology claim is unproven and must fail closed.

This is a falsifiable predicate: post-dispatch-only grant/manifest commits fail clause 3; changed or absent committed bytes fail clause 2; missing or duplicate dispatch/grant bindings fail clauses 1 or 4; a timestamp-only claim fails clauses 1 and 3. It establishes artifact/order evidence only, not that a reviewer actually read the bytes or that a native preventive per-seat allowlist enforced scope.

## Evidence and limits

The round-21 lesson `R21-RETRO-RESERVATION` rejects repairing event order retrospectively and says the current grant must precede the current dispatch; it explicitly says timestamp alone cannot backdate the grant. Its `R21-REVIEW-BYTES` and “Falsify repairs before the once-final run” sections call for primary-byte binding and compare manifests against their actual predispatch commit, with ancestry to the measured revision; they also state this does not prove reading. The same lesson warns that the earlier “five committed grant artifacts” wording was premature, so this predicate checks each dispatch/grant binding rather than treating a count or prior report as proof.

The round-22 preregistration declares C2's `bindings.json` and `events.json` audit inputs and C3's strict cohort accounting; it does not specify the audit implementation or establish that `H(d)` is captured with contemporaneous immutable provenance. The host-tool-boundary record says there is no native per-seat allowlist and approves prompt-level scope bindings plus fail-closed post-hoc audit only. Accordingly, this is an acceptance predicate for chronology evidence, **not** a claim of preventive runtime enforcement.

## Residual risk and verification gap

Only the declared round-21 lesson, round-22 preregistration, and host-tool-boundary source were available in this seat. No implementation or event schema was in the read binding, and no command was run. Therefore whether the C2 evaluator implements this predicate, whether its dispatch record has trustworthy call-time provenance, and whether its failures are exercised remain unverified. A Git DAG check alone is not proof of real-world dispatch chronology if the call-time revision binding can be fabricated or rewritten.

Reviewed-SHA256: 64d2401c244f5f06a39cb4b3785c74422e805f698e3ee5cab21815ed1e88cc70
Predicate: r22-reviewreservation
Scope: executed=none
