# FxC2TraceIncomplete — source-only falsification

Reviewed-SHA256: c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4
Predicate: r22-fxc2traceincomplete
Scope: executed=none

    Lane bounds: leaf member — no subagent dispatch.

Target: `.ufo/waves/round-22/candidate/tools/check-seat-bindings.py`. The SHA-256 is the one assigned to this seat; this seat could not recompute it (NO-EXEC). Nothing was executed, imported, mutated or fetched. `skill://godspeed` was not read, because this harness's read tool takes only filesystem paths.

## Verdict

**The attack holds for a well-formed forbidden request. It is FALSIFIED for a forbidden request whose recorded metadata is malformed, and for any violation recorded after a malformed event.**

## Where the claim holds (bounded reason)

`evaluate` lines 130–142: `if not seat['complete']` adds `SCOPE-TRACE-INCOMPLETE` and does **not** `continue`. The event loop then runs, and `classify` findings are added to `findings`, `seat_findings` and `violations`. Take a single seat with `complete=false` and events `[{"tool":"bash","args":{}}]`. The expected result, read from source, is:

- `findings`: `[SCOPE-TRACE-INCOMPLETE@A, SCOPE-EXEC-DENIED@A:0]`
- `violations=1`, `incomplete_seats=1`, exit 2, status `CANNOT_EVALUATE`

The exception path does not reset `findings`, so findings added before an abort are also kept. Runtime result: not observed (no execution).

## Counterexample 1: forbidden tool with malformed args loses the violation

`classify` line 61 checks `isinstance(args, dict)` and raises `ValueError` **before** the exec and fetch denials at lines 75–78. Take a seat with `complete=false` and events `[{"tool":"bash"}]`, or `{"tool":"bash","args":null}`, or args that sanitization removed:

- Expected under policy (UNKNOWN row: "incomplete metadata is not command absence"; md: "observed forbidden request contradicts that declaration"): both `SCOPE-TRACE-INCOMPLETE` and `SCOPE-EXEC-DENIED` are present.
- Expected from source: `[SCOPE-TRACE-INCOMPLETE@A, SCOPE-SCHEMA@input]`, `violations=0`. The bash request is never classified as exec.
- The same happens for `web_search`/`browser` (fetch) and for a `multi_tool_use.parallel` child `{"recipient_name":"functions.bash"}` with `parameters` missing.

## Counterexample 2: an abort drops later violations

The whole seat loop sits inside one `try`. A malformed event stops classification of every later event and every later seat:

- One seat, `complete=false`, events `[{"tool":"read","args":{}}, {"tool":"bash","args":{}}]`. Expected from source: `[SCOPE-TRACE-INCOMPLETE, SCOPE-SCHEMA]`. `SCOPE-EXEC-DENIED@A:1` is lost.
- Seats A and B in manifest order. A is complete and has a malformed event. B has `complete=false` and `bash`. B is never visited, so **both** of B's findings (incomplete and violation) are missing, and its row is missing too.

## Secondary finding: status precedence

When a violation is observed on an incomplete seat, the exit code is 2 (`CANNOT_EVALUATE`). The finding is still in the output. However, a consumer that reads only the status or exit code sees the same code that schema errors produce, not FAIL. Incompleteness should block PASS, but a definite observed violation is a definite FAIL. This is a tradeoff for the judge, not a lost finding.

## Selftest gap

The `incomplete` fixture (line 184) uses a clean read event. `case` asserts only one `fid`. No fixture checks that `incomplete` and `violation` appear together, and none checks a forbidden tool with non-dict args. So the claimed property has no negative fixture to back it.

## Impacted axes

- **operability (C2)**: fail-closed audit can under-report actual forbidden requests. Contradicts "actual request precedence" (md QUALITY, criteria 42/44/46).
- **calibration (C3)**: a faulty seat can be accounted for without its contradicting violation.

## Smallest safe correction

1. In `classify`, validate that `tool` is a string, strip `functions.`, and return the exec/fetch denials **before** requiring `args` to be a dict. A malformed request should then produce `[denial, ...]` rather than raising.
2. Wrap each event (and each parallel child) in its own try. On error, add `SCOPE-SCHEMA` at `name:index`, keep going, and force code 2. This keeps every later event and seat.
3. Add these fixtures with set-containment of all expected ids:
   - `complete=false` plus `bash` gives `{SCOPE-TRACE-INCOMPLETE, SCOPE-EXEC-DENIED}`.
   - `{"tool":"bash"}` with no args gives `SCOPE-EXEC-DENIED`.
   - A malformed event before `bash` gives `{SCOPE-SCHEMA, SCOPE-EXEC-DENIED}`.
4. Optional (judge decision): when a violation exists, report FAIL as the status alongside `incomplete_seats>0`, or document that exit 2 hides it.
