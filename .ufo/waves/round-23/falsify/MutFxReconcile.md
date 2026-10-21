# MutFxReconcile — three design-only mutation probes

## Axes, claim and bounds

Axes: C3 calibration (complete fixed-cohort reconciliation), detector independence (literal controls rather than self-generated expected rows), and scope integrity (no execution, source modification or runtime-enforcement claim).

Attacked claim: C3 and the frontier of its mutation/selftest evidence, not C1 or C2. Preregister lines 46–52 restrict C3 to the two frozen round22 cohorts. These proposed synthetic controls challenge checker discrimination; they do not demonstrate an error in either actual frozen cohort or justify widening that claim.

Observed evidence: read the complete 387-line candidate `tools/check-path-reconciliation.py`, the complete recorded `measure/l1-mutation.json`, preregistration and the required Godspeed skill. The log records ten reconciliation mutants (0–9), plus an earlier canonical-token survivor/fix. None of the three exact substitutions below appears in that log. Its reported 27/27 kills cover its recorded substitutions, not these designs.

All outputs below labeled [INFERENCE] are static predictions. No detector, baseline, mutation, hash computation or restoration run occurred.

## M1 — silently accept duplicate JSON keys

Location: `strict`, line 53. One-line replacement:

```python
    return json.loads(raw, object_pairs_hook=unique)
```

becomes:

```python
    return json.loads(raw)
```

Plausible defect: simplifying JSON parsing discards the duplicate-key rejection used for pins, events, bindings, audit and ledger data.

Killing literal control: pass exactly these bytes to `strict`:

```python
b'{"schema":"tsukuroi-path-reconciliation-v1","schema":"tsukuroi-path-reconciliation-v1"}'
```

Detector predicate: a `ValueError` whose message is exactly `duplicate JSON key` must be raised. A returned dictionary fails the control; an unrelated exception is inconclusive.

- Pristine expected output [INFERENCE]: `ValueError('duplicate JSON key')`, from `unique` lines 43–48.
- Mutant expected output [INFERENCE]: `{'schema': 'tsukuroi-path-reconciliation-v1'}`; detector fails and therefore kills the mutant if the pristine control passes.
- Existing selftest discrimination [INFERENCE]: likely survivor. The only explicit duplicate-key fixture, `ledger-duplicate-key` at line 322, uses `{"schema":1,"schema":2}`. Dropping the hook still fails ledger-schema validation because the resulting schema is numeric, so the same expected exit/finding can occur without detecting duplicates. The other displayed fixtures do not supply duplicate JSON keys.
- Concrete falsifier: the literal control distinguishes duplicate rejection from independent schema rejection; the current fixture does not.
- Smallest remedy: add this direct `strict` negative control, keeping its expected exception independent of ledger generation. No production change is warranted from an unexecuted mutant design.

## M2 — omit the reverse roster-coverage requirement

Location: `derive`, line 153. One-line replacement:

```python
        if set(bound) != names:
```

becomes:

```python
        if not names.issubset(bound):
```

Plausible defect: checking that event seats are bound but forgetting that every binding seat must have an event-seat entry. The forward direction is already checked at line 125.

Killing literal control: give `derive` wave `build` and these exact three objects:

```json
{
  "events": {
    "schema": "tsukuroi-seat-events-v1",
    "seats": [{"name": "S", "events": []}]
  },
  "bindings": {
    "schema": "tsukuroi-seat-bindings-v1",
    "seats": [
      {"name": "S", "read_paths": [], "write_paths": []},
      {"name": "T", "read_paths": [], "write_paths": []}
    ]
  },
  "audit": {"findings": []}
}
```

The three members are separate arguments, not an extra wrapper passed to `derive`.

Detector predicate: derivation must raise `Unevaluable` with `fid == 'RECONCILIATION-INPUT-MALFORMED'` and `site == 'build:ValueError'`.

- Pristine expected output [INFERENCE]: that exact exception, because binding seat `T` is absent from the event roster.
- Mutant expected output [INFERENCE]: a returned build cohort with empty rows, no orphans and every total zero. Returning it fails the control and would kill the mutant after a passing baseline.
- Existing selftest discrimination [INFERENCE]: likely survivor. `event-roster-forgery` at lines 325–326 exercises an unknown event seat (`GHOST`), rejected at line 125 before the mutated check. No displayed fixture supplies an extra binding seat omitted from events.
- Concrete falsifier: acceptance of the literal unmatched `T` is a missing-roster witness, not proof that actual frozen inputs omit a seat.
- Smallest remedy: add this reverse-roster negative fixture to the existing selftest, expecting exit 2 and `RECONCILIATION-INPUT-MALFORMED`; keep the production equality unchanged.

## M3 — copy the call ID into the request-argument identity field

Location: ledger-row construction, line 147. One-line replacement:

```python
                    'request_arguments_sha256': event.get('request_arguments_sha256'),
```

becomes:

```python
                    'request_arguments_sha256': event.get('call_id'),
```

Plausible defect: adjacent-field copy/paste corrupts per-event identity while leaving every path count and disposition intact.

Killing literal control: give `derive` wave `build` and the following separate argument objects:

```json
{
  "events": {
    "schema": "tsukuroi-seat-events-v1",
    "seats": [{"name": "S", "events": [{
      "tool": "read",
      "args": {"path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/a.md"},
      "call_id": "call-literal-7",
      "request_arguments_sha256": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
    }]}]
  },
  "bindings": {
    "schema": "tsukuroi-seat-bindings-v1",
    "seats": [{
      "name": "S",
      "read_paths": ["/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/a.md"],
      "write_paths": []
    }]
  },
  "audit": {"findings": []}
}
```

The path and identity string are synthetic literal data; this detector needs neither a real `a.md` nor a computed digest.

Detector predicate: row zero must have `site == 'S:0'`, `call_id == 'call-literal-7'`, and `request_arguments_sha256` equal to the exact 64-character literal above. The expected identity must not be regenerated through `derive` or `build_ledger`.

- Pristine expected output [INFERENCE]: those distinct call-ID and request-identity values are preserved; predicate true.
- Mutant expected output [INFERENCE]: request identity becomes `call-literal-7`; predicate false and thus a kill after a passing baseline.
- Existing selftest discrimination [INFERENCE]: likely survivor. Auto ledgers at lines 278–285 and reevaluation at line 332 use the same derivation; line 334 checks exit/finding behavior, not an independently expected metadata value. Direct controls at lines 336–345 concern counting/selector rules. This is not a claim that a revision-bound check would survive: exact comparison with an independently retained ledger at line 189 could reject the changed field.
- Concrete falsifier: the literal independent row assertion exposes systematic metadata corruption that self-generated expected ledgers can share.
- Smallest remedy: add this direct two-identity preservation control to selftest, without changing frozen ledgers or widening historical authority.

## Verdict and restoration evidence

Actual detector output: none. Empirical verdict for M1, M2 and M3: INCONCLUSIVE / NOT RUN, neither killed nor survived. Each proposed literal detector is predicted to kill its corresponding mutant; current-selftest survival predictions require an authorized execution elsewhere to establish. A failing pristine baseline would make a subsequent mutant failure inconclusive.

Bounded search: the complete target source and complete recorded L1 mutation log were compared by reading only. It found three distinct unrecorded one-line mutations and corresponding discriminating literal controls. No executed falsifier of the landed C3 result was established. C1/C2, frozen input contents and revision-bound outcomes were not independently inspected or tested in this seat.

Before identity: supplied SHA-256 in the receipt below, not independently computed. After hash: unobserved and not computed. Source/scratch writes: none; no mutated bytes existed and no restoration was required. The sole write is this bound report. No commands, fetches, delegation, installations or other runtime invocation occurred.

Lane bounds: leaf member — no subagent dispatch.
Reviewed-SHA256: fd0393be9140579424bdfc3c099b2b82fee11ccf9306d926c998235ce7ee1a6b
Predicate: r23f-mutfxreconcile
Scope: executed=none
