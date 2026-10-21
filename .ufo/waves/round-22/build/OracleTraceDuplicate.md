# OracleTraceDuplicate — source-only oracle for the duplicate event seat name (C2)

Baseline: `894d1e20fb4939b0cc4fadf722c46d1429f257d2`
Source under review: `.ufo/waves/round-22/sources/host-tool-boundary.json` (hash pinned by the required receipt below).
Round policy source: `.ufo/waves/round-22/preregister.json`.

## Bounds actually exercised

- Read: `host-tool-boundary.json`, `preregister.json`, `skill://godspeed` only.
- Not read: `tools/check-seat-bindings.py`, existing build outputs, any other wave artifact, any sibling/operator file.
- Executed: none. The case was not invoked. No fetch, no subagent, no install, no package transaction.
- Consequence: the manifest/event schema, the C2 verdict vocabulary, the finding-ID format, the exit-code mapping, and the parser's duplicate-member policy are all unobservable from this seat. Statements about them below are labeled inference.

## Axes (godspeed)

A1 fixture minimality · A2 verdict soundness · A3 ID exactness · A4 ambiguity coverage · A5 policy/observation provenance separation.

## Observed source facts

From `host-tool-boundary.json`:

- Schema `tsukuroi-host-tool-boundary-v1`, date `2026-10-21`.
- Task surface: `i`, `context`, `tasks[{task,solutionSpace,name?,agent?,tools?,sourceSession?,model?}]`; `tasks[].name` is optional.
- `tools_semantics`: "Eval-defined additive extras; not an allowlist or replacement of native tools."
- `native_per_seat_allowlist: false`.
- `authority`: Main confirmed "no host-native per-seat allowlist exists in the task dispatch path."
- `approved_scope`: prompt-level scope bindings plus fail-closed post-hoc audit; C3 detection/evidence, explicitly not preventive enforcement.

From `preregister.json`:

- C2: axis operability, metric `request_audit_mode`, before 0, target 1, command `check-seat-bindings.py --revision <REV> --manifest bindings.json --events events.json`.
- C3_bound admits a four-way seat accounting that includes an "absent-unresolved" class; limits disclaim preventive enforcement, proof of actual reading, request effects, and host recovery.
- Neither file defines an event schema, a duplicate-name rule, a verdict vocabulary, a tie-break, or a finding-ID format.

Derivation leverage: with no native per-seat allowlist and `tools` explicitly not an allowlist, the post-hoc audit's only attribution surface is the prompt-level seat name carried in the manifest and events. If that name is duplicated with conflicting values inside one event, there is no declared secondary authority that could disambiguate the event. [INFERENCE from the two source facts, not a claim about host internals.]

## Interpretation lattice for "duplicate event seat name"

| # | Reading | Locus | Is CANNOT_EVALUATE robust? |
|---|---|---|---|
| I1 | One event object repeats its seat-name member with different values | one event object | Yes, under a fail-closed audit that detects duplicates and has a non-binary outcome |
| I2a | Two request events carry the same seat name | events array | No — repeated requests per seat are normal and each is independently checkable |
| I2b | Two terminal/receipt events carry the same seat name | events array | Only if an unstated one-terminal-event-per-seat rule exists |
| I3 | `bindings.json` declares two seats with the same name | manifest | Yes, but this is a manifest-duplication case, not an event case |
| I4 | Two `tasks[]` entries share `tasks[].name` | dispatch batch | Rule unstated; `name` is optional and auto-generated when omitted |

The stipulated expectation (`CANNOT_EVALUATE`) is robust only under I1 (and under I2b if the one-event-per-seat rule is granted). I2a is the counterexample: duplicate seat names across requests are ordinary, and a per-event evaluator can decide each request without any ambiguity. The fixture therefore encodes I1.

## Fixture

The fixture must be materialized as raw bytes. Any parse followed by re-serialization collapses repeated member names and destroys the case; a `json.dumps`-generated fixture is vacuous. The literal bytes below were not hashed here (NO-EXEC); the integrator must record the materialized SHA-256.

### Smallest audit-complete pair

`bindings.json`:

```json
{"seats":[{"name":"OracleTraceDuplicate","root":"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin","read_paths":["/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/sources/host-tool-boundary.json"],"write_paths":["/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/build/OracleTraceDuplicate.md"],"commands":[],"fetches":[]}]}
```

`events.json` (raw literal; the repeated `seat` member is intentional and must not be normalized):

```json
{"events":[{"seat":"OracleTraceDuplicate","seat":"OracleTraceDuplicate-decoy","tool":"read","path":"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/sources/host-tool-boundary.json"}]}
```

### Irreducible witness

```json
{"events":[{"seat":"OracleTraceDuplicate","seat":"OracleTraceDuplicate-decoy"}]}
```

### Why this is smallest

- One declared seat, one event, one request, two occurrences of one member name with distinct values.
- The second value is undeclared, so attribution fails under last-wins regardless of which request kinds the audit checks; the conflict does not depend on reads being audited. (If reads are not audited, the first-wins parse accepts the event and the second parse still fails attribution, so the parses diverge.)
- No second event, no duplicate event identity, no extra fields beyond the binding surface evidenced by this seat's own literal binding.

Schema assumptions [INFERENCE; unobservable in bounds]:

- Manifest root key `seats`; binding keys `name`, `root`, `read_paths`, `write_paths`, `commands`, `fetches`.
- Events root key `events`; event keys `seat`, `tool`, `path`.
- If the checker's envelope or request-field spelling differs, substitute the envelope only; the invariant is the repeated member name with conflicting values inside one event, and the verdict analysis below is unchanged.

### Opposite outcomes reachable from identical bytes

- First occurrence wins: event attributed to `OracleTraceDuplicate`; the read path is declared; a request audit yields PASS.
- Last occurrence wins: event attributed to undeclared `OracleTraceDuplicate-decoy`; the event cannot be attributed within the declared manifest; a fail-closed audit must not yield PASS (it yields FAIL or unresolved).

Both parses are syntactically valid JSON. Neither declared source selects first-wins, last-wins, or reject-on-duplicate. PASS and non-PASS are therefore both reachable by a legal parse of the same bytes.

## Exact verdict / ID

| Field | Exact value | Basis |
|---|---|---|
| Case ID | `r22-oracletraceduplicate` | Required receipt predicate; independent of the seat name, so the identifier cannot itself collide under duplication |
| Claim | `C2` | Preregister C2 metric/command |
| Expected policy verdict | `CANNOT_EVALUATE` | Work order; derivation below |
| Reason | duplicate event seat name with conflicting values | Work-order phrase + fixture shape |
| Observed runtime verdict | none | Case not invoked; NO-EXEC |
| Observed exit code | none / not derivable | Checker source outside `read_paths` |
| Internal finding ID | not asserted | Unobservable; inventing a `C2-…` string would be fabrication |

Canonical oracle record:

```json
{"case_id":"r22-oracletraceduplicate","claim":"C2","expected":{"verdict":"CANNOT_EVALUATE","reason":"duplicate_event_seat_name"},"observed":null,"invoked":false}
```

Exact verdict line: `r22-oracletraceduplicate => CANNOT_EVALUATE`.

Non-outcomes that do not satisfy this expectation: traceback or uncaught duplicate-key error; hang; silent skip of the event; exit 0 with no verdict; last-wins evaluation reported as PASS or FAIL. A finite policy outcome means the checker emits the explicit non-verdict token, not an accident of its parser.

## Why CANNOT_EVALUATE (policy derivation)

1. Repeated member names with distinct values make the event's effective seat a function of parser policy, not of the bytes.
2. No declared source fixes first-wins, last-wins, reject-on-duplicate, or name normalization.
3. The audit's only attribution surface is the seat name; there is no native per-seat allowlist and `tools` is not an allowlist.
4. Fail-closed forbids upgrading an undecidable input to PASS.
5. Asserting FAIL would overstate: the attribution failure exists only under one of two admissible parses, and the other parse satisfies the declared scope.
6. Therefore the parser-independent finite outcome is CANNOT_EVALUATE: the audit cannot decide, and says so.

Weak corroboration: the round's C3 ontology already contains an "absent-unresolved" class, so a non-binary outcome is structurally consistent with round22. This does not entail C2's verdict domain. [INFERENCE]

## Attacks on the expectation

1. **Equal duplicate values are benign.** If both members carry the same value, first-wins and last-wins agree and the event is evaluable (PASS/FAIL by request). CANNOT_EVALUATE then survives only under a strict "any repeated name is invalid" rule that no source states. The fixture must use distinct values; the class label "duplicate event seat name" does not by itself require that.
2. **Default parser detection.** `json.loads` and many parsers silently retain the last occurrence and expose no duplicate signal. Without an `object_pairs_hook`, raw scanner, or strict-mode parse, the checker cannot observe the duplication and will emit PASS/FAIL, not CANNOT_EVALUATE. Verifying the parser is outside this seat's bounds.
3. **Detection layer and normalization.** An escaped member name (`"se\u0061t"`) decodes to the same name but evades a raw-text scan; case, Unicode normalization, and whitespace variants are distinct names unless normalized. Detection must occur after decode with an exact-name comparison, and no normalization policy is declared.
4. **Verdict-domain assumption.** Neither source names a verdict set. If C2 emits only PASS/FAIL, CANNOT_EVALUATE is out of domain and "fail-closed" most plausibly maps malformed input to FAIL. The expectation requires a three-valued domain that separates undecidable from violated, plus a rule that duplicates are undecidable rather than a violation. This is the largest unverified assumption.
5. **Violation dominance.** If any unambiguous out-of-scope request exists in the same audit unit, FAIL is determined regardless of the duplicate and CANNOT_EVALUATE would be too weak. The fixture carries exactly one request and no other events.
6. **Legitimate recurrence.** The same seat name across revisions, roots, or separate audit units is not a duplicate; a checker keying globally would emit false CANNOT_EVALUATE. The fixture confines both values to one event, one root, one unit.
7. **Adjacent cases.** Manifest duplication (I3) and task-name duplication (I4) are different conditions with potentially different IDs; folding them into this case makes the ID inexact.
8. **Silent skip.** An implementation may drop the unresolvable event and PASS the remainder. That is a false PASS and an operability defect; the audit needs a unit-poisoning rule so any unresolvable event blocks a PASS for the unit.
9. **Serializer round-trip.** A fixture produced with `json.dumps` cannot contain repeated members. Store raw bytes and hash the materialized file; otherwise the test is empty and any PASS is vacuous.
10. **ID conflation.** Using the seat name as the case ID reproduces the duplication inside the identifier. Keep `r22-oracletraceduplicate` independent of `OracleTraceDuplicate`.

## Policy expectation vs observed runtime

- **Policy expectation (derived, normative):** `CANNOT_EVALUATE` for case `r22-oracletraceduplicate`. Conflicting duplicate seat members leave two admissible attributions with opposing outcomes, and the declared policy supplies no tie-break.
- **Observed runtime result:** none. The case was not invoked; the checker was not read; no verdict, finding ID, stderr, or exit code was observed. Nothing in this report is a runtime observation.
- **Confidence:** observed source facts high; I1 reading medium; CANNOT_EVALUATE as policy medium-high under the stated preconditions; as a source entailment low, because the three-valued domain and the duplicate-as-undecidable rule are unstated; internal finding ID and exit code none.

## Falsifiers

- Checker documents and applies first-wins or last-wins: the result becomes determinate PASS (this fixture, first-wins) or FAIL/unresolved (last-wins), so CANNOT_EVALUATE is falsified.
- Checker maps malformed or duplicate input to FAIL: expected outcome is FAIL, not CANNOT_EVALUATE.
- Checker dedupes equal-valued duplicates only, with the fixture changed to equal values: evaluable, not CANNOT_EVALUATE.
- Checker has no duplicate detection and uses last-wins: observed FAIL (or unknown-seat handling), not CANNOT_EVALUATE.
- The two declared values resolve to the same scope: both parses PASS, so the expectation is falsified.
- C2's verdict domain is binary: CANNOT_EVALUATE cannot be emitted.

## Remaining unknowns

- Actual manifest/event schema and required fields.
- C2 verdict domain and exit-code mapping.
- Duplicate-member policy and parser behavior.
- Finding-ID format.
- Whether events are per-request records or per-seat terminal receipts.
- Materialized fixture hash (not computed under NO-EXEC).

All are outside this seat's `read_paths` and cannot be resolved by invocation, which is forbidden for this case.

## Required receipt

Reviewed-SHA256: d24cca82114bdfd8c0935b642353682fe6b56f56dae32b0d755fe401f3d08d30
Predicate: r22-oracletraceduplicate
Scope: executed=none
