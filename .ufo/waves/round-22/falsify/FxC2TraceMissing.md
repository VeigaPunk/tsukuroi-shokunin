# FxC2TraceMissing — one binding seat without a trace object

Report: `.ufo/waves/round-22/falsify/FxC2TraceMissing.md`
Target: `.ufo/waves/round-22/candidate/tools/check-seat-bindings.py`
Reviewed-SHA256: c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4 (accepted from the seat target; not recomputed — NO-EXEC)
Method: source-only reading of the declared candidate file and its declared knowledge/source companions. No execution, import, mutation, test, or fetch.

## Candidate under attack

Manifest declares N ≥ 2 seats; the events trace contains N−1 seat objects, omitting exactly one declared seat; every present seat is `complete: true` and every recorded request is inside its binding. Claim: the auditor reports the missing seat exactly once and keeps the remaining seats clean, with exact missing and incomplete counts.

## Observed source facts (no inference)

- `evaluate()` enters at L95. `total = violations = incomplete = 0` is initialized before the try (L101).
- Manifest validation (L105–L115) requires schema `tsukuroi-seat-bindings-v1`, a non-empty `seats` list, per-seat name regex + uniqueness, `root == LANE`, `commands == []`, `fetches == []`, non-empty unique local `read_paths`/`write_paths` (the single exception `skill://godspeed` on read paths). `bound[name] = seat` at L115.
- Trace validation (L116–L123) requires schema `tsukuroi-seat-events-v1`; each trace seat must have `name` already in `bound`, a unique name, a non-empty unique `agent` string, `type(complete) is bool`, and a list `events`. Any unknown trace seat, duplicate name/agent, or malformed shape raises `ValueError` → `SCOPE-SCHEMA`, code 2 (L145–L148).
- Per-seat accounting (L124–L129): for each name in `bound.items()`, `seat = by_name.get(name)`; when `seat is None` the branch executes `incomplete += 1` (L127), `add('SCOPE-TRACE-MISSING', name)` (L128), then `continue` (L129). The `continue` skips both the `SCOPE-TRACE-INCOMPLETE` branch and the row append.
- Present-but-incomplete branch (L130–L132): `incomplete += 1` and `SCOPE-TRACE-INCOMPLETE`; that seat is still audited and still appended to `rows` (L143).
- Exit mapping (L144): `code = 2 if incomplete else (1 if findings else 0)`; status tuple `('PASS','FAIL','CANNOT_EVALUATE')[code]` (L149).
- Output fields (L149–L151): `status`, `request_audit_mode: 1`, `seats_bound: len(bound)`, `requests_total`, `violations` (integer count), `incomplete_seats` (**combined** missing + incomplete), `seats` (rows for present seats only), `findings` (id + site).
- `SCOPE-TRACE-MISSING` is emitted once per absent bound name and never carries an event index; per-seat violation sites use `name:index`.

## Expected fixture verdict (derived, not observed)

For the literal scenario (N declared seats, exactly one absent, N−1 present with `complete: true` and no violating event):

- `incomplete`: exactly 1 — the missing branch runs once for that name and `continue` prevents a second increment.
- `findings`: exactly one `{'id': 'SCOPE-TRACE-MISSING', 'site': <that name>}`.
- `violations`: 0 — the missing branch never calls `classify`; present clean seats add no ids.
- `seats_bound`: N; `requests_total`: sum of present seats' events; `seats`: N−1 rows, each with an empty `violations` list.
- Verdict: exit 2, `status: CANNOT_EVALUATE`, `request_audit_mode: 1`.

**Observed runtime: none.** Per the seat binding (`executed=none` semantics, NO-EXEC), the checker was not run and its selftest was not run. Everything above is a reading of the candidate bytes, not a measured verdict.

## Verdict: the literal claim holds, by construction

Bounded reason: the two incompleteness branches (L126–L129 vs L130–L132) are mutually exclusive via `continue`; `incomplete` is a per-seat counter over `bound` iteration with no cross-seat state other than `total`/`violations` (untouched by a missing seat); `by_name` can only contain bound names because unknown trace seats abort at L120–L121; and exit code 2 (L144) overrides the violation-based 1, so a missing seat cannot be reported as a clean PASS or as FAIL. Hence a single absent seat among clean peers yields missing=1 through the finding id, `incomplete_seats == 1`, `violations == 0`.

## Source-visible counterexamples and limits

1. **No distinct missing/incomplete counters.** L151 exposes only the combined `incomplete_seats`. For 1 missing + 1 declared-incomplete the scalar is 2 and cannot distinguish (2 missing), (1+1), or (2 incomplete) without scanning finding ids. The exact pair is recoverable only from `findings` (`SCOPE-TRACE-MISSING` vs `SCOPE-TRACE-INCOMPLETE`). If the claim is "the tool reports exact missing and incomplete counts as counters", it is false; for the literal one-missing-rest-clean fixture the combined value coincides with missing=1 only because incomplete=0.
2. **The selftest does not encode the candidate scenario.** L184 builds `missing = trace(); missing['seats'] = []` against a one-seat manifest — the all-missing N=1 case, not one-missing-among-clean. L195 asserts only `code == expected and (fid is None or fid in ids)`: no assertion on `incomplete_seats`, `seats_bound`, `requests_total`, finding multiplicity, or row count. The fixture therefore cannot discriminate exact counts or the N>1 partition.
3. **Empty events with `complete: true` PASSes clean (L190, `empty-trace` expected 0).** A seat object whose `events` list is empty and whose producer declares coverage complete is indistinguishable from a genuinely zero-request seat: no finding, `incomplete_seats == 0`, exit 0. `complete` is an unverified producer declaration; the checker never compares it with provider transcript. Under a broader reading of "missing trace" = "no recorded request evidence for the seat", the claim is falsified at this point. Under the literal absent-seat reading it is not.
4. **Remaining-clean caveat (adjacent, outside the literal counts).** `requested_path` strips selectors only when the tool is `read` (L87), while `local()` rejects any `:` (L35). A bound-path `grep` using the harness-supported `path:50-100` selector is therefore `SCOPE-PATH-DENIED` (L54–L55), so a substantively clean seat can accrue a violation. This over-flags; it does not undercount missing seats. It may be intentional if the literal-path seat contract forbids grep selectors, but the `read`-only selector handling makes the clean set depend on tool choice for the same path.
5. **File-level absence routes differently.** A missing events file (or JSON `null`/dict-shaped `seats`) fails schema at L116–L117 → `SCOPE-SCHEMA`/code 2 with no per-seat `SCOPE-TRACE-MISSING` findings; a missing manifest returns FAIL, `request_audit_mode: 0` (L99–L100), not CANNOT_EVALUATE. This is fail-closed but means seat-level absence is only accounted when the events container itself is well-formed.
6. **Minor shape hazard.** Top-level `violations` is an integer (L150) while each row's `violations` is a list of ids (L143). Consumers summing per-seat violations would type-error; "clean" must be read as an empty list.

## Confidence

- Source semantics and the literal one-missing particle counting: high — the branches and counter scope are explicit.
- Interpretation that the candidate demands first-class distinct missing/incomplete counters: medium — the output has no such pair; exactness is derivable only from findings.
- Runtime behavior of any fixture: unobserved (NO-EXEC).

## Remaining unknowns

- The actual round-22 `build/bindings.json` and `build/events.json` are outside this seat's declared read paths, so the landed fixture shape and its real seat population are unverified.
- Whether the producer ever emits an empty `events` list with `complete: true` (case 3) is not decidable from the declared files.
- Whether `grep` selectors are contractually permitted for bound seats (case 4) is not settled by the seat-boundary knowledge file.

Reviewed-SHA256: c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4
Predicate: r22-fxc2tracemissing
Scope: executed=none
Lane bounds (informational, not a receipt field): leaf member — no subagent dispatch.
