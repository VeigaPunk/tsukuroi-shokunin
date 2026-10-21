# OracleTraceMissing — round 22, C2 posthoc request audit

Role: critic, source-only. No case was invoked. Every verdict below is what the policy should produce. None of it is a result observed at runtime.

## Sources read

- `.ufo/waves/round-22/sources/host-tool-boundary.json`: the assignment declares its SHA-256 as `d24cca82…3d08d30`. I could not recompute the hash because this seat is NO-EXEC, so that digest is the declared value and has not been verified.
- `.ufo/waves/round-22/preregister.json`
- `skill://godspeed`: my file tools cannot resolve this selector. I only had the copy of the skill text embedded in the assignment.

## Facts the sources establish

- `native_per_seat_allowlist: false`. The `approved_scope` is "prompt-level scope bindings plus fail-closed post-hoc audit". C2 is the `check-seat-bindings.py --manifest bindings.json --events events.json` audit.
- Fail-closed means an absent trace can never become PASS. The only available evidence of what a seat requested is its recorded events. If those are missing, the audit has nothing to check.
- Neither source defines the verdict vocabulary (PASS, FAIL, CANNOT_EVALUATE), the case-ID scheme, or the schema of `bindings.json` and `events.json`. The verdict token comes from the assignment, not from these sources. All field names below are [INFERENCE], modelled on the seat-binding JSON shape used in this round's dispatch.

## Fixture: events omit one manifest seat

The manifest (`bindings.json`) declares two seats. Seat B is conformant, so no FAIL can compete with the expected verdict.

```json
{
  "schema": "tsukuroi-round22-seat-bindings-v1",
  "seats": [
    {"name": "SeatA", "root": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin",
     "read_paths": ["/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/preregister.json"],
     "write_paths": [], "commands": [], "fetches": []},
    {"name": "SeatB", "root": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin",
     "read_paths": ["/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/preregister.json"],
     "write_paths": [], "commands": [], "fetches": []}
  ]
}
```

The events file (`events.json`) contains no trace for SeatA at all:

```json
{
  "schema": "tsukuroi-round22-seat-events-v1",
  "traces": [
    {"seat": "SeatB", "complete": true,
     "requests": [{"tool": "read", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/preregister.json"}]}
  ]
}
```

Expected policy outcome:

- **Overall verdict:** `CANNOT_EVALUATE`
- **Finding:** seat `SeatA` is declared in the manifest but has no trace in the events file. Proposed finding ID `trace-missing`; the case ID is [INFERENCE], since no canonical ID registry is in my read scope.
- **SeatB:** evaluated as conformant.
- **Exit status:** must be non-success, because the audit is fail-closed. A `CANNOT_EVALUATE` result must not count toward the C2 target `request_audit_mode = 1` as a pass.

A smaller variant also works: one seat, SeatA, with `"traces": []`. It should produce the same verdict and finding. I recommend the two-seat form because it shows the defect is per-seat rather than a whole-file failure.

## Ways the expectation can go wrong

1. **A missing trace treated the same as an empty trace (the strongest counterexample).** Take `{"seat":"SeatA","complete":true,"requests":[]}`. It means SeatA recorded zero requests, so the expected verdict is PASS. If the checker loops over the events and looks up each seat in the manifest, it never notices that SeatA has no trace. It then returns PASS for the omission fixture, which is a false PASS that violates fail-closed. The fix is to loop over the manifest seats, look each one up in the events, and require that present-but-empty and absent produce different verdicts. Axes affected: operability (C2) and calibration (C3's `absent-unresolved` accounting depends on the same distinction).
2. **Which verdict wins when results conflict.** If SeatB had a real violation, which overall verdict should the audit report? The sources do not say. I recommend FAIL taking precedence over CANNOT_EVALUATE, with SeatA's `trace-missing` still listed. Either way, the fixture stays unambiguous only if SeatB is conformant. Leaving this undefined lets a single overall-verdict field hide either finding.
3. **A missing trace confused with an incomplete trace.** A trace that exists but has `complete:false` is a separate case, the TraceIncomplete oracle's. It may reach the same verdict, but it needs its own finding ID. Merging the two would mean one finding standing for two different absences.
4. **Seats in the events but not in the manifest.** This is the reverse case. It must not be counted as covering SeatA, and it must not be dropped silently, which an events-first lookup would do.
5. **Matching by name.** Seat identity is the `name` string. Matching that ignores case, or a stray trailing space, could let a near-miss name count as SeatA's trace. Names should match exactly.
6. **Overclaiming.** `CANNOT_EVALUATE` only records that evidence is missing. It does not show that SeatA requested anything, or that it requested nothing, and it must not be worded as runtime enforcement. This follows the preregister `limits` and `host_decision`.

## Smallest safe correction

Make the manifest the only list of seats to check. For each manifest seat, require exactly one trace with an exactly matching name. If there is none, record `trace-missing` and give that seat `CANNOT_EVALUATE`. Never fold that into PASS. Define the overall verdict precedence (I recommend FAIL, then CANNOT_EVALUATE, then PASS) and list every finding. Keep an `events.json` fixture with a present-but-empty trace alongside the omission fixture, so a regression to checking events-first shows up as a disagreement between the two verdicts.

Judgment, admission, and integration are left to the canonical judge.

Reviewed-SHA256: d24cca82114bdfd8c0935b642353682fe6b56f56dae32b0d755fe401f3d08d30
Predicate: r22-oracletracemissing
Scope: executed=none
