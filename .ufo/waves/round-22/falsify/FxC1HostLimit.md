# FxC1HostLimit — round22 C1 boundary-contract falsification

Candidate: `.ufo/waves/round-22/candidate/tools/check-boundary-contract.py`
Declared digest: `1b91a7c10c971b554bad144035b40d0b7054e06582093f9f851ac0fcafdd2485` (as supplied in the seat ticket; not recomputed — NO-EXEC forbids running a hash command).
Baseline: `894d1e20fb4939b0cc4fadf722c46d1429f257d2`.
Mode: source-only reading. No execution, no imports, no selftest, no mutated inputs run, no network, no production edits.

## Axes

- A1 host-limit strictness — does `native_per_seat_allowlist=true` reject?
- A2 no-prevention strictness — does removing the no-prevention phrase reject?
- A3 report fidelity — does the emitted metric track the reject?

## Observed source facts (candidate bytes)

1. `evaluate` reads the prose as raw text at `check-boundary-contract.py:72`:
   `text = prose.decode('utf-8') if isinstance(prose, bytes) else prose`.
2. The host gate at `:75-76` reads exactly two fields:
   `host_data.get('native_per_seat_allowlist') is not False` or `host_data.get('tools_semantics') != 'Eval-defined additive extras; not an allowlist or replacement of native tools.'` → `add('BOUNDARY-HOST-LIMIT', 'S084')`.
   The host path is hardcoded at `:164` (`.ufo/waves/round-22/sources/host-tool-boundary.json`); the S084 row path is only substring-matched (`:80`).
3. The decision table is validated against `visible(text)` at `:82` (comments and fences stripped by `visible`, `:38-53`).
4. The no-prevention gate at `:93-94` is
   `data.get('scope') != LIMIT or 'post-hoc detection, not preventive runtime enforcement' not in text`
   → `BOUNDARY-LIMIT-MISSING`. It tests raw `text`, **not** `visible(text)`.
5. `count += 1` happens per matching decision at `:92`, before the limit gate. `code = 1 if findings else 0` (`:95`); `status` is indexed from `code` (`:99`).
6. Selftest fixtures (`:120-128`): `hidden` (`:123`) and `fenced` (`:124`) wrap the **entire** prose, so they fail via the table (`BOUNDARY-DECISION-MISMATCH`), not via the limit gate. `host-overclaim` (`:127`) is `{"native_per_seat_allowlist":true}` with `tools_semantics` absent. `limit` (`:128`) removes the phrase from the **raw** prose string.
7. Host evidence file fields: `tools_semantics` (`host-tool-boundary.json:9`), `native_per_seat_allowlist` (`:10`), `authority` (`:11`), `approved_scope` (`:12`, contains "not preventive enforcement"). The checker never references `authority` or `approved_scope` (grep over the candidate file: only `:74-75` touch `host_data`).
8. Prose: the checked sentence is at `seat-boundary-r22.md:22`; a second no-prevention sentence follows it ("No native toolset restriction, OS sandbox, arbitrary-shell semantic equivalence, proof of actual reading, or proof of request effects is claimed."). JSON `scope` is the exact `LIMIT` at `seat-boundary-r22.json:47`.
9. `git_read` (`:140-149`) evaluates committed blobs at the bound revision only; a mutant must be committed to be seen. Absent path → `None` → early `BOUNDARY-CONTRACT-MISSING` (`:63-66`); unreadable → code 2 (`:168-169`).

## Attack 1 — set `native_per_seat_allowlist=true`

Expected verdict (source-derived): exit 1, `status: FAIL`, `findings: [BOUNDARY-HOST-LIMIT @ S084]`, `validated_boundary_decisions: 6` (the count is already incremented; the host finding does not reset it). **Rejected.**

Observed runtime: none — not executed.

Bounded reason it holds: JSON yields the singleton `False` only from the literal `false`. `.get` returns `None` when the key is absent; `0`, `1`, `"false"`, `null`, `[]` are not identical to `False`. Duplicate keys raise inside `json.loads` via `unique` → `BOUNDARY-SCHEMA`, code 2. A non-object payload raises `AttributeError` inside `evaluate` → `BOUNDARY-SCHEMA`, code 2. A missing/unreadable host blob yields `None` → code 2. Every source-visible path is non-zero; no input makes a truthy value pass the `is not False` identity test.

Fixture gap (A1): no fixture isolates the boolean flip with otherwise-valid host JSON; the only host fixture also drops `tools_semantics`. The reject is therefore guaranteed by code but not separately regression-pinned.

## Attack 2 — remove the no-prevention phrase

### 2a. Raw removal — holds

Expected: exit 1, `FAIL`, `BOUNDARY-LIMIT-MISSING` (`:93`), matching fixture `limit` (`:128`). Removing the phrase from the JSON `scope` also fails the `!= LIMIT` operand. Observed runtime: none.

### 2b. Occluded retention — counterexample (exit 0, PASS)

Constructed mutant (`seat-boundary-r22.md`): keep the exact decision table and every other line; replace the visible sentence at `:22` with an enforcement claim (for example "This is **native preventive runtime enforcement**."), and append the physical line
`<!-- post-hoc detection, not preventive runtime enforcement -->`
(or place the phrase in a fenced block instead).

Expected verdict: exit 0, `status: PASS`, `validated_boundary_decisions: 6`, `findings: []`.
Reason: `visible(text)` (`:38-53`, applied at `:82`) strips the comment/fence, so the table and source rows still match; the limit gate at `:93` reads raw `text` (`:72`), so the substring is present. The rendered prose now claims enforcement while the limit survives only in non-rendered bytes. No fixture covers this channel split; `hidden`/`fenced` (`:123-124`) hide the whole file and fail on the table instead.

### 2c. Visible negation — counterexample (exit 0, PASS)

Constructed mutant: replace `:22` with a visible sentence that embeds the phrase under negation, for example "This is **not** post-hoc detection, not preventive runtime enforcement; native prevention is active."

Expected verdict: exit 0, `PASS`. The guard is bare substring containment, not a semantic or polarity check; the sentence is visible and denies the limit, and the file then contradicts the unchanged JSON `scope` at `:47`. Nothing cross-checks prose against `scope`.

### 2d. Unread host no-prevention fields — counterexample (exit 0, PASS)

Constructed mutant (`host-tool-boundary.json`): delete `"approved_scope"` (`:12`) and/or `"authority"` (`:11`), or invert `approved_scope` to "native preventive enforcement is active", while keeping `tools_semantics` (`:9`) exact and `native_per_seat_allowlist: false` (`:10`).

Expected verdict: exit 0, `PASS`. `evaluate` reads only the two fields at `:75`; the S084 row check (`:78-81`) validates a row in `corpus/SOURCES.md`, not the host file's own claims. A no-prevention phrase removed from the S084 evidence itself is not rejected.

### 2e. Other prose no-prevention sentences — counterexample (exit 0, PASS)

Constructed mutant: delete the visible sentence "No native toolset restriction, OS sandbox, arbitrary-shell semantic equivalence, proof of actual reading, or proof of request effects is claimed." while keeping the one checked phrase.

Expected verdict: exit 0, `PASS`. Only the decision table, the JSON `scope` equality, and the single substring at `:93` constrain the prose; the remaining no-prevention claims are unguarded.

## Expected fixture verdict vs observed runtime

| Mutant (source-only, constructed) | Expected verdict (source-derived, not executed) | Observed runtime |
|---|---|---|
| host `native_per_seat_allowlist: true`, all else exact | exit 1 / FAIL / BOUNDARY-HOST-LIMIT; metric 6 | not executed |
| host `0` / `"false"` / `null` / key missing | exit 1 / FAIL / BOUNDARY-HOST-LIMIT (identity) | not executed |
| host duplicate `native_per_seat_allowlist` keys | exit 2 / CANNOT_EVALUATE / BOUNDARY-SCHEMA | not executed |
| prose phrase removed from all raw bytes | exit 1 / FAIL / BOUNDARY-LIMIT-MISSING | not executed |
| JSON `scope` edited away from exact `LIMIT` | exit 1 / FAIL / BOUNDARY-LIMIT-MISSING | not executed |
| phrase retained only in HTML comment; visible text claims enforcement | exit 0 / PASS / metric 6 — **counterexample** | not executed |
| phrase retained only in a fenced block | exit 0 / PASS — **counterexample** | not executed |
| visible negation embeds the phrase | exit 0 / PASS — **counterexample** | not executed |
| host `approved_scope`/`authority` removed or inverted | exit 0 / PASS — **counterexample** | not executed |
| other prose no-prevention sentences removed | exit 0 / PASS — **counterexample** | not executed |

No exit code, stdout, or selftest observation exists for any row: this seat performed no execution.

## Accounting caveat (A3)

`BOUNDARY-HOST-LIMIT` and `BOUNDARY-LIMIT-MISSING` do not reduce `validated_boundary_decisions`; the count is completed at `:92` before the limit gate at `:93`. A host overclaim therefore emits `validated_boundary_decisions: 6` with `status: FAIL` and exit 1. The preregistered C1 metric is `validated_boundary_decisions` target 6 (`preregister.json:6`). Any consumer keying on the metric alone would read 6/6 under a host overclaim; the authoritative reject is the exit code / `status`. This does not defeat rejection, but it makes the preregistered metric insufficient as a pass gate.

## Minor adjacent observations

- A malformed host blob is caught by the shared `except` at `:96-98` and reported as `BOUNDARY-SCHEMA` at site `corpus/knowledge/seat-boundary-r22.json`, misattributing the fault to the JSON corpus. Still fail-closed (code 2).
- The S084/S083 path test is substring containment (`path not in found[0][1]`, `:80`), so a row naming a different path that contains the expected path also passes. Not part of the two attacked mutations.
- The selftest can be green while 2b-2e hold, because no fixture encodes those negatives; selftest PASS is not evidence of the limit guard's semantic strictness.

## Confidence

High for every code-anchored claim above (lines cited against the candidate bytes; host and corpus fields read directly). Medium for the clean-baseline dependency in "Remaining unknowns" item 1.

## Remaining unknowns

1. `corpus/SOURCES.md` is outside this seat's read paths; whether it currently holds exactly one S083 and one S084 row with 11 cells and the expected metadata is unverified, so a clean baseline exit 0 is assumed rather than observed.
2. The declared SHA256 could not be recomputed under NO-EXEC; the digest is taken from the ticket.
3. Whether downstream consumers (`check-seat-bindings.py`, `check-review-cohort.py`, scorecard) key on `status`/exit rather than `validated_boundary_decisions` is outside the declared read paths; the A3 hazard is stated conditionally.
4. The checker at `--revision` reads committed blobs; this report analyzes the candidate working-tree bytes, which are assumed to be the bytes that will land.

## Conclusion

The attack sentence is falsified in the semantic/rendered reading and holds only in the literal raw-bytes reading. Setting `native_per_seat_allowlist=true` rejects deterministically. Removing the phrase from raw prose rejects. But visible removal plus non-rendered retention, visible negation, removal of the host file's own `approved_scope`/`authority`, and removal of the prose's other no-prevention sentences all produce exit 0 / PASS. The checker's no-prevention guarantee is byte-presence in one hardcoded prose substring plus two host fields — not a rendered-prose or evidence-completeness guarantee.

Reviewed-SHA256: 1b91a7c10c971b554bad144035b40d0b7054e06582093f9f851ac0fcafdd2485
Predicate: r22-fxc1hostlimit
Scope: executed=none

Lane bounds: leaf member — no subagent dispatch.
