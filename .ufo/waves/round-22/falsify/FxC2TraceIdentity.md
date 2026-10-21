# FxC2TraceIdentity: source-only falsification of check-seat-bindings.py

Seat: FxC2TraceIdentity, leaf (no subagent dispatch). Attack basis: source reading of the named candidate bytes only. Executed: none. No tests, imports, mutations, fetches, or sibling reads. Observed runtime is none in every row below; "prediction" means what the source implies when read, not an observation.

## Target and digest

- Target: `.ufo/waves/round-22/candidate/tools/check-seat-bindings.py`, 241 lines, read through its declared path. The read tool's tag for these bytes is `636F`.
- The assigned digest `c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4` was not recomputed. SHA-256 needs execution, which this seat may not perform, and `636F` is a 4-hex hashline tag, not a SHA-256. The digest is taken from the assignment.
- Line numbers below refer to the same bytes.

## Verdict on the named claim

Claim: an unknown or duplicate trace seat, or a duplicate agent, cannot silently match a wrong binding.

Verdict: the claim holds for exact-match entries inside `trace['seats']`. It does not extend to entries placed outside that list (F1), and well-formed misattribution is outside what the checker can observe (F2).

Bounded reason for the holding cases:
1. The identity loop (lines 119-123) validates every trace entry against `bound` before any event is classified. The first call to `classify` is at line 138.
2. A trace name must equal a bound key exactly (line 120). Bound names are ASCII-only by the regex at line 109, so no confusable-name route reaches the join.
3. A duplicate name (`in by_name`) or a duplicate agent string (`in agents`) raises `ValueError` at lines 120-121.
4. The single handler at lines 145-148 catches the raise and sets `code = 2`. Lines 149-151 derive status from code, giving CANNOT_EVALUATE.
5. Duplicate JSON keys are rejected by `unique` (lines 20-26), applied through the hooks at lines 103-104.
6. Agent values never select a binding. They are used only at lines 120 and 123, and echoed in the output row at line 143.

| Input inside `seats` | Guard | Source-derived result | Selftest coverage |
|---|---|---|---|
| name not bound | line 120, first clause | exit 2, SCOPE-SCHEMA | `unknown-seat`, defined line 187, registered line 190 |
| same name twice | line 120, `in by_name` | exit 2, SCOPE-SCHEMA | `duplicate`, defined line 186, registered line 190 |
| same agent under two names | line 120, `in agents` | exit 2, SCOPE-SCHEMA | none (see F3) |
| bound name with no entry | lines 126-128 | exit 2, SCOPE-TRACE-MISSING | `missing-trace`, defined line 184 |

## Counterexamples and weaknesses

### F1 (Medium): entries outside the checked containers are silently dropped, so the audit can PASS over requests it never examined

- Only `trace['schema']` and `trace['seats']` are read (lines 116-119). No other top-level key is inspected.
- Line 120 checks name, agent, complete, and events for each seat. No other seat key is inspected.
- Line 135 checks only that each event is a dict. Event keys other than `tool` and `args` are never inspected. Line 81 reads only `args['path']`. [INFERENCE] A second path-bearing argument is ignored, which matters only if the runtime honors it.

Counterexample (prediction): `seats` holds a clean entry for every bound seat. A sidecar top-level key, for example `late`, holds `{"name":"A","agent":"agent-A2","complete":true,"events":[{"tool":"bash","args":{}}]}`. Nothing reads the sidecar, so evaluate returns code 0 (PASS), and `requests_total` leaves out the bash call. This is the duplicate-seat failure in a form that is neither rejected, matched, nor counted.

Contract conflict: seat-boundary-r22.md line 22 says the auditor "fails closed on unknown tools, malformed data, unmatched seats or unavailable trace coverage". Unknown containers and keys are not rejected.

- Expected verdict (proposed fail-closed contract): exit 2, SCOPE-SCHEMA.
- Observed runtime: none.
- Prediction: exit 0, PASS.

### F2 (Medium): identity is keyed by name and the agent is never bound, so a well-formed misattribution silently matches the wrong binding

- The bindings schema has no agent field. Binding validation (lines 108-115) checks name, root, commands, fetches, and paths only. The join is `by_name.get(name)` (line 125) and `classify(..., binding)` (line 138). The agent appears only at lines 120 and 123, and in the `rows` output at line 143.
- The `rows` output pairs each bound name with a trace-asserted agent. That pairing reads like verified identity; it is only asserted.
- Consequence: a trace that records seat X's requests under seat Y, while X keeps a complete empty entry, passes whenever Y's binding permits those requests. Nothing in the checker can detect the mis-recording. Detection depends on the attributed binding excluding the request:
  - Reads: a surface shared by both bindings is allowed under both, so neither binding can exclude it. This seat's binding includes `skill://godspeed` and `candidate/tools/_revision.py`. The peer roster lists other seats as reading the revision helper. [INFERENCE from roster status text only; sibling bindings are outside this seat's read set.] Misattributed reads among such seats are invisible.
  - Writes: disjoint write paths make a misattributed write detectable as SCOPE-PATH-DENIED. Nothing enforces disjointness across seats. The duplicate check at line 113 is per seat, and each seat is validated in isolation (lines 108-115). Two seats may bind the same write path.
  - Precedent in this wave: check-review-snapshots.py evaluate rejects duplicate report paths across rows (`row["report"] in reports`, lines 72-73). The seat checker has no equivalent.
- SCOPE (line 17) disclaims "universal trace completeness" but says nothing about attribution trust.
- Expected verdict (proposed): two seats binding one write path should exit 2, SCOPE-SCHEMA. The contract requires each seat to write "its exact report" (seat-boundary-r22.md line 29). No fixture exists.
- Prediction: the overlapping manifest is accepted. Pure read misattribution has no detectable verdict under the current design.

### F3 (Low): the duplicate-agent guard has no fixture that reaches it, and agent equality is exact code-point

- The selftest binds exactly one seat (line 156). No case can have two bound seats, so no case makes the agent clause true. The agent clause is evaluated in clean cases, where it is false.
- The only duplicate fixture (line 186, registered line 190) is caught first by the name clause, which precedes the agent clause in the same `or` chain.
- Source-derived mutation reading (not executed): deleting `or seat['agent'] in agents` leaves every selftest result unchanged. Deleting `seat['name'] in by_name` also leaves every result unchanged. Neither guard is covered alone. seat-boundary-r22.md line 35 says new checks need fixed negative fixtures before they count.
- NFC and NFD spellings of one agent id, or an id with an appended zero-width code point, are distinct at line 120 and pass. This has no binding effect because agents do not select bindings. It is a gap in the duplicate guard's semantics only.

## Adjacent observations (outside the named claim; low severity)

- A1, metric: the return at lines 149-151 hard-codes `'request_audit_mode': 1` on every path except the missing-manifest return at line 100. A CANNOT_EVALUATE run (exit 2) still reports `request_audit_mode` 1. preregister C2 measures `request_audit_mode` with target 1, so a gate that reads only that field would accept a fail-closed run. Gates must read status or exit code.
- A2, precedence: line 144, `code = 2 if incomplete else (1 if findings else 0)`, reports an observed violation as CANNOT_EVALUATE whenever any seat is incomplete. The violation still appears in `findings`. seat-boundary-r22.md line 24 says an observed forbidden request contradicts the declaration regardless of later seat death.
- A3, missing manifest: lines 99-100 return FAIL (1). Selftest `missing-manifest` (line 190) encodes 1. seat-boundary-r22.md line 17 says incomplete metadata is not command absence; CANNOT_EVALUATE (2) fits that rule better. [INFERENCE on the intended mapping.]
- A4, vocabulary: classify recognizes `read`, `grep`, `glob`, `write`, `bash`, `eval`, `task`, `web_search`, `browser*`, and `functions.`-prefixed forms (lines 73-80). The function names exposed in this session carry a leading underscore (`_read`, `_bash`, and so on). Those would be classified SCOPE-TOOL-UNKNOWN. That fails closed, but it produces false violations if traces use those names. [INFERENCE: trace vocabulary is outside the read set.] Wrapper detection (line 63) also runs before prefix stripping (line 73), so `functions.multi_tool_use.parallel` is UNKNOWN rather than expanded.

## Expected fixture verdicts versus observed runtime

Observed runtime is none in every row (executed=none). "Expected" is the fail-closed contract in seat-boundary-r22.md, or a proposal where the contract is silent.

| Case | Expected | Source-derived prediction |
|---|---|---|
| `unknown-seat` (exists) | exit 2, SCOPE-SCHEMA | exit 2, SCOPE-SCHEMA |
| `duplicate` (exists) | exit 2, SCOPE-SCHEMA | exit 2, SCOPE-SCHEMA |
| same agent under two bound names (absent) | exit 2, SCOPE-SCHEMA | exit 2, SCOPE-SCHEMA |
| sidecar bash entry for a bound name (absent, proposed) | exit 2, SCOPE-SCHEMA | exit 0, PASS |
| two bound seats sharing a write path (absent, proposed) | exit 2, SCOPE-SCHEMA | manifest accepted |
| NFC/NFD agent duplicate (absent, proposed) | exit 2, SCOPE-SCHEMA | accepted |

## Verification gaps

- Digest not recomputed (see Target and digest).
- Build artifacts (`.ufo/waves/round-22/build/*.json`) and sibling bindings are outside this seat's read set. No claim is made about the actual data.
- `_revision.bind` (lines 172-192 of `_revision.py`) was read. Revision resolution is not part of the named claim and is not falsified here.
- Nothing was executed. Every prediction is source-derived.

## Suggested direction (no edits made)

1. Exact key-set checks at trace, seat, and event level. Closes F1.
2. Reject overlapping `write_paths` across seats, mirroring the `reports` set in check-review-snapshots.py. State that read overlap is expected and that read misattribution is not detectable. If an expected agent identity per seat is knowable before dispatch, pre-register it so attribution becomes checkable. Addresses F2.
3. Add two-bound-seat fixtures and per-guard mutation fixtures for the name and agent duplicate clauses. Addresses F3.
4. Derive `request_audit_mode` from audit status, or document that C2 gates must read status or exit code. Addresses A1.

Receipt:
Reviewed-SHA256: c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4
Predicate: r22-fxc2traceidentity
Scope: executed=none
