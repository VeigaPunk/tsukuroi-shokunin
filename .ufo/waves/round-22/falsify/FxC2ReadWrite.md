# FxC2ReadWrite — read/write membership separation in `check-seat-bindings.py`

Target (declared read set): `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/candidate/tools/check-seat-bindings.py`, 241 lines, read in full across lines 1-241.

Method: source-only reading. No execution, imports, mutations, or fixtures were run (NO-EXEC). The reviewed digest `c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4` is the ticket-declared identity of the bytes read; it was not recomputed, because hashing requires execution in this seat.

## Claim under attack

P1: membership in `read_paths` never confers write permission.
P2: membership in `write_paths` does not make a path readable.

## Verdict

P1 and P2 **hold for the recorded-request classifier**. No source-visible counterexample exists in the 241 reviewed lines. Two bounded qualifications (A, B) and one fixture-coverage gap (C) are recorded below; none of them is an automatic read/write derivation.

## Source facts

- L90: `elif path not in binding['write_paths' if tool == 'write' else 'read_paths']:` — the only membership decision in the file. Exactly one of the two lists is indexed per request.
- L73: a single `functions.` prefix is stripped. L79-80: the tool must then be one of the literals `('read', 'grep', 'glob', 'write')`, otherwise `SCOPE-TOOL-UNKNOWN` (denied). There is no alias that maps a write onto the read branch or vice versa; `'functions.write'` strips to `'write'`, `'functions.functions.write'` is unknown and denied.
- L84: multi-path splitting on `;` applies only to `grep`/`glob`; L87: selector stripping applies only when `tool == 'read'`. Both preserve the branch identity.
- L33-36 `local()`: lane-prefix, no backslash, no control characters, no `*?[];:`, no empty/`.`/`..` segments. L48-49 special-cases `skill://godspeed` before `local()` but returns no membership decision; L90 still enforces membership, and L113 forbids the URI in `write_paths`, so the branch cannot grant write.
- L111-114: per-field validation only — non-empty list, every entry `local()` (read paths may additionally be `skill://godspeed`), uniqueness *within* the list.
- Grep across the file for `read_paths|write_paths` returns only three sites: L90 (selection), L111-113 (validation), L156 (fixture binding). There is no union, fallback, or second lookup.

## Why it holds (bounded)

`tool` reaching L90 is a four-literal string; the ternary tests `tool == 'write'`. For `write` the expression can only yield `write_paths`; for `read`/`grep`/`glob` it can only yield `read_paths`. Neither branch ever consults both lists, and every non-literal tool exits at L79-80 before L90. Therefore read membership cannot produce a write pass, and write membership cannot produce a read pass, for any request the classifier can reach.

## Attempted counterexamples that do not break the predicate

1. `write` of `skill://godspeed`: L48 returns no denial, but L90 rejects it — the URI cannot appear in `write_paths` (L113 requires `local()` for that field). Expected verdict: exit 1, `SCOPE-PATH-DENIED`.
2. `functions.write`: L73 strips to `write`, so L90 indexes `write_paths`. Still no read grant.
3. Write path carrying a selector (`.../report:1-5`): selector stripping is read-only (L87), and L35 rejects `:` outright. Expected exit 1, `SCOPE-PATH-DENIED`.
4. Parallel wrapper: `classify` recurses with the same `binding` and depth; no rebinding, no mutation of `binding`.
5. Malformed event args (`{}`, non-dict child): `ValueError` at L61-62/L82-83 is caught in `evaluate` and converted to `SCOPE-SCHEMA` exit 2 — fail closed, not an allow.
6. Path traversal (`LANE/../sibling`, `LANE/x/../source`, `LANE/./source`, double slash): rejected by L34-36.

## A. Declared overlap is accepted (schema boundary)

L113 validates each field independently and never requires `set(read_paths) ∩ set(write_paths) == ∅`. A binding with the same literal path in both lists validates and then permits both a read and a write of it. This falsifies only a stronger "the auditor guarantees disjointness" reading: readability still originates in an explicit `read_paths` declaration, not in write membership, so P2 as stated ("not automatically readable") survives.

Concrete case: `read_paths = [LANE + '/report']`, `write_paths = [LANE + '/report']`, event `{'tool': 'read', 'args': {'path': LANE + '/report'}}` → no finding, exit 0. The auditor emits no overlap-specific finding.

## B. Ancestor-directory read membership (exact-string boundary)

L90 compares exact strings, so declaring the parent directory readable does not make the write-only file itself readable through `read`; that request is denied. However, `grep`/`glob` accept a declared directory path, and per the host's grep/glob semantics [INFERENCE — tool semantics, not this file], a declared parent can surface descendants that include a write-only report. The permission remains grounded in the explicit read declaration, not in `write_paths`; the auditor sees only the requested directory and cannot distinguish listing from descendant content access.

Concrete case: `read_paths` contains `LANE + '/reportdir'`, event `{'tool': 'grep', 'args': {'path': LANE + '/reportdir'}}` → no finding, exit 0.

## C. Fixture coverage gap (strongest surviving attack)

The selftest (L154-192) contains 42 cases. Exactly four use `tool == 'write'`: `write-exact` at L166 (allowed) and the three near-miss denials at L175-176 (`report + '.extra'`, `report + '/child'`, `LANE + '/production'`). There is:

- no `read` of the write-only fixture path `report`;
- no `write` of the read-only fixture path `src`;
- no `functions.write` case (`qualified` covers `functions.read` only, L163).

So neither cross-list direction is pinned by a fixed negative fixture, even though the knowledge doc's own QUALITY line requires fixed negative fixtures before a check's improvement counts (`.ufo/waves/round-22/candidate/corpus/knowledge/seat-boundary-r22.md` L35). The shipped PASS cannot discriminate L90's exclusive index from a hypothetical merged-membership implementation on these two directions.

### Expected fixture verdicts (source-derived) vs observed runtime

Expected values are traced by reading `evaluate`/`classify`; none was executed, so the observed column is empty by construction, and none of these cases exists in the shipped selftest.

| Fixture event (binding A at L156) | Expected exit | Expected ids | Observed runtime |
|---|---|---|---|
| `read` `LANE + '/report'` (write-only path) | 1 (FAIL) | `SCOPE-PATH-DENIED` | not executed; absent from selftest |
| `write` `LANE + '/src'` i.e. `src` (read-only path) | 1 (FAIL) | `SCOPE-PATH-DENIED` | not executed; absent from selftest |
| `functions.write` `report` | 0 (PASS) | none | not executed; absent from selftest |
| `read` `report + ':1-5'` | 1 (FAIL) | `SCOPE-PATH-DENIED` | not executed; absent from selftest |
| `write` `report + ':1-5'` | 1 (FAIL) | `SCOPE-PATH-DENIED` | not executed; absent from selftest |
| `read` `skill://godspeed` with it undeclared | 1 (FAIL) | `SCOPE-PATH-DENIED` | not executed; absent from selftest |
| overlap-A: `read` `report` with `report` in both lists | 0 (PASS) | none | not executed; absent from selftest |

Trace basis for the first row: `requested_path` returns `(report, None)` because `local()` passes; L90 finds no membership in `read_paths`; one finding, `incomplete == 0`, so `code = 1`. Second row is symmetric with `write_paths`. Third row: L73 strips the prefix, L90 matches `write_paths`, so no findings and `code = 0`.

## Declared scope

The file is a post-hoc auditor of recorded request spellings (docstring L2; SCOPE at L17; knowledge doc L22). It does not prevent runtime action, prove reading, prove request effects, or cover universal traces. This seat executed nothing; `executed=none` remains the strict receipt declaration.

## Confidence and remaining unknowns

- High confidence in the mechanical reading: the file was read in full and the only two membership lists are the three grep sites above.
- Unknown: contents of `.ufo/waves/round-22/build/bindings.json` and `events.json` are outside this seat's declared read set, so the real cohort's list disjointness (boundary A) cannot be asserted, only the classifier's rule.
- Unknown: byte identity of the reviewed file was not recomputed (NO-EXEC); the digest above is the ticket declaration.
- Unknown: no fixture verdict was observed at runtime, so every "expected" value in section C is source-derived, not measured.

Reviewed-SHA256: c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4
Predicate: r22-fxc2readwrite
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
