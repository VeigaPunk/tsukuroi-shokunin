# OracleTraceUnknown — source-only unknown-seat oracle

## Axes and evidence

Axes: unknown-seat isolation; fail-closed classification; fixture/schema certainty; scope fidelity.

Read only the declared host-boundary source, preregistration, and Godspeed skill. The host-boundary source states that native per-seat allowlisting is absent and that the approved mechanism is prompt-level bindings plus a fail-closed post-hoc audit (lines 9–12). Preregistration identifies C2 as request-audit mode (claim C2, line 6) and explicitly excludes preventive enforcement and proof of request effects (lines 10–13).

The reviewed SHA-256 below is the assignment-supplied digest, not an independently computed digest. No hashing, execution, fetch, installation, delegation, or production modification occurred.

## Smallest logical fixture

```json
{"bindings":[],"events":[{"seat":"u"}]}
```

This is a minimal semantic witness: an explicit empty binding set and exactly one event naming a seat outside that set. The property under examination is `"u" ∉ declared_seats`.

**Schema limitation:** `bindings`, `events`, and `seat` here define the independent oracle's logical representation. Neither permitted JSON source specifies the auditor's manifest/event input schema. This fixture is therefore not asserted to be an accepted CLI input, nor proven byte-minimal among that implementation's valid inputs. A missing tool/request envelope or a forbidden empty binding set could otherwise preempt the intended branch.

A nonempty-binding contrast isolates seat membership without depending on empty-set acceptance:

```json
{"bindings":[{"name":"a"}],"events":[{"seat":"b"}]}
```

The sole conceptual mutation is event seat `"a"` → `"b"`; the binding remains `"a"`. Its pristine and restored logical bytes are both:

```json
{"bindings":[{"name":"a"}],"events":[{"seat":"a"}]}
```

These are embedded report fixtures only. They were not submitted to a detector or written over source bytes.

## Expected detector and exact policy outcome

Expected detector: the bounded C2 post-hoc seat-binding/request auditor identified in preregistration. For a structurally valid event whose seat has no binding, the assignment-stipulated finite policy outcome is exactly **`CANNOT_EVALUATE`**. The auditor must not substitute another seat's permissions, treat missing permissions as unrestricted, drop the event, or count it as conformant.

The exact assigned oracle ID is **`r22-oracletraceunknown`**. This is the assignment's predicate identifier, not an observed auditor diagnostic ID. An implementation-specific verdict field, diagnostic ID, exit status, or output serialization cannot be derived from either authorized source. Claiming one would fabricate evidence. The missing prerequisite for an implementation-exact fixture/diagnostic ID is the auditor's manifest/event schema and unknown-seat result definition; neither is among this seat's readable artifacts.

For the pristine/restored contrast, seat lookup succeeds, so this unknown-seat condition must not fire. That alone does not establish an overall PASS: other event/binding requirements are unavailable.

## Ambiguity attacks

- **Fail closed does not select an enum.** The sources justify refusing to establish conformance, but do not themselves distinguish `CANNOT_EVALUATE` from an audit failure. The exact enum above comes from the assignment, not an observed source rule.
- **Unknown versus absent/malformed.** The mutant explicitly supplies a string seat. An omitted seat, malformed event, or missing trace would test another condition. Implementation fixtures must satisfy unrelated schema requirements first.
- **Empty manifest and validation ordering.** The smallest witness may encounter manifest or request-shape rejection before seat resolution. The nonempty contrast removes empty-set dependence, but cannot resolve the undisclosed schema or validation order.
- **Event-local versus audit-wide outcome.** The sources do not define aggregation. The required unknown-seat finding must survive aggregation; no particular top-level result layout is established.
- **Post-hoc evidence only.** An unknown-seat finding cannot show that a request was prevented, executed, or had effects. No native preventive per-seat allowlist is claimed.

## Actual output, verdict, and restoration

| State | Actual detector output | Probe verdict |
| --- | --- | --- |
| Pristine logical fixture | None; detector not invoked | Not measured |
| Mutated logical fixture | None; detector not invoked | Not measured |
| Restored logical fixture | None; detector not invoked | Not measured |

Overall mutation verdict: **INCONCLUSIVE / NOT EXECUTED**, not killed or survived. NO-EXEC expressly forbids the pristine/mutated/restored behavioral runs; NO-FETCH and the read binding prohibit obtaining additional implementation evidence.

Restoration evidence: no scratch executable/source was authorized or mutated; only this report was written. The two authorized JSON sources received no write/edit calls. The embedded restored fixture exactly repeats its pristine literal. Before/after byte hashes were not measured; the supplied reviewed-source digest is not represented as a measured restoration hash.

Reviewed-SHA256: d24cca82114bdfd8c0935b642353682fe6b56f56dae32b0d755fe401f3d08d30
Predicate: r22-oracletraceunknown
Scope: executed=none
