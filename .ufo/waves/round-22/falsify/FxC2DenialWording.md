# FxC2DenialWording — `DENIED` is post-hoc rejection, not runtime blocking

Attack target: candidate `tools/check-seat-bindings.py` (SHA256 c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4) and its paired docs. Claim audited: an audit finding `SCOPE-*-DENIED` denotes post-hoc rejection of a recorded request spelling, never observed runtime blocking or a blocked effect.

Verdict: **HOLDS** for the exact claim. No source-visible path emits a `DENIED` finding without a recorded event, and no source-visible surface asserts that any request was blocked. One concrete counterexample exists only against the stronger unstated converse (`no DENIED` ⇒ `no forbidden request`) and against reading `request_audit_mode`/`PASS` as audit coverage; it does not overturn the claim as stated.

## Evidence (literal anchors)

- `candidate/tools/check-seat-bindings.py:2` — module docstring: "Audit recorded requests against frozen prompt scopes; not preventive enforcement."
- `:17` — `SCOPE` literal: "Recorded request spellings only; not runtime prevention, symlink/effect proof, reading proof or universal trace completeness."
- `:60` — `classify` docstring: "Return finite post-hoc findings; never execute the requested operation."
- `:75-76`, `:77-78`, `:90-91` — the only runtime emission sites of `SCOPE-EXEC-DENIED`, `SCOPE-FETCH-DENIED`, `SCOPE-PATH-DENIED`. All are pure string returns from a classifier over an explicit `(tool, args)` dict; `classify` contains no dispatch, mutation, import side effect, or execution.
- `:134-142` — every finding is appended inside the per-seat event loop with site `f'{name}:{index}'`; `DENIED` identifiers cannot arise outside a recorded event, and no other `add(...)` call uses a `DENIED` id (`:100`, `:128`, `:132`, `:146`, `:226`, `:233`, `:235` are BINDINGS-MISSING / TRACE-* / SCHEMA / revision ids).
- `:100`, `:149-151` — the `evaluate` payloads carry `'scope': SCOPE`; status names are `PASS`/`FAIL`/`CANNOT_EVALUATE` over an audit-conformance code (`:144`, `:149`), not over a dispatch decision.
- `:202-210`, `:229-230` — inputs are committed blobs read at a landed revision with `git show`; the audit runs offline from the dispatch it classifies. Its only `subprocess` use is that committed read.
- `candidate/corpus/knowledge/seat-boundary-r22.json:47` — "Prompt policy and post-hoc request classification only; no native preventive enforcement or effects/reading proof."
- `candidate/corpus/knowledge/seat-boundary-r22.md:20-22` — "This is **post-hoc detection, not preventive runtime enforcement**"; `:24` — an observed request contradicts `executed=none` "regardless of whether its command is harmless"; `:31` — "Never ... label prompt compliance runtime prevention."
- `preregister.json:10` — "fail-closed post-hoc audit ... Never call this runtime enforcement"; `:13` — "No native preventive tool enforcement".
- `sources/host-tool-boundary.json:9-10,12` — `tools` are "Eval-defined additive extras; not an allowlist", `native_per_seat_allowlist: false`, approved scope is "prompt-level scope bindings plus fail-closed post-hoc audit".

## Defeaters tested, all fail to break the claim

1. **Fabricated denial without a request.** No `DENIED` literal exists outside `requested_path`/`classify` (`:47`, `:55`, `:76`, `:78`, `:91`); the only call site is the event loop `:137-142`, and each finding keeps its `name:index` site. Unmatched seats, absent traces, malformed data and schema faults produce non-`DENIED` ids (`:100`, `:124-132`, `:146`).
2. **Runtime interposition.** The script has no dispatch hook, no allowlist mutation, and no consumer of its return values besides `print`/exit status (`:228-237`). It cannot block anything it classifies.
3. **Payload-level blocking assertion.** The payload says `status: FAIL` plus `request_audit_mode: 1` plus `scope` disclaiming runtime prevention (`:149-151`). `FAIL` is audit non-conformance, not a blocked call.
4. **Doc-level prevention claim.** Five independent surfaces negate prevention (`json:47`, `md:20-22`, `md:31`, `preregister:10,13`, `host:12`) and the host record explicitly denies a native allowlist (`host:10`).
5. **Fixture treated as observation.** `selftest` synthesizes its traces in `trace()` (`:157-158`) and builds the expected table at `:168-190`; its `status: PASS` (`:197`) is conformance of those expected verdicts, not observed runtime. No candidate surface calls those traces observed requests.

## Expected fixture verdict vs observed runtime (kept separate)

- **Expected fixture verdicts (source-derived, not executed).** The `selftest` table contains 42 cases: 7 expect exit `0` (`clean-read`, `qualified`, `selector`, `skill`, `write-exact`, `parallel-local`, `empty-trace`), 27 expect exit `1` (3 exec + 4 fetch-path + 3 fetch-tool + 9 path + 3 write-path + 1 semicolon + 1 unknown-tool + 1 parallel-exec + 1 parallel-fetch + `missing-manifest`), and 8 expect exit `2` (`bad-args`, `parallel-malformed`, `missing-trace`, `incomplete`, `duplicate`, `unknown-seat`, `nonempty-fetch-allowlist`, `duplicate-json-key`). These are expectations checked against `evaluate`'s return, not recordings of any seat.
- **Observed runtime: none.** This seat executed no fixture, test, import or command; `Scope: executed=none` stands literally. The target SHA256 is the assignment-provided value and was not recomputed.

## Adjacent concrete counterexample (does not apply to `DENIED`)

`evaluate` returns `'request_audit_mode': 1` unconditionally at `:149`, including code `2` schema failures and a zero-request trace; `:190` expects `empty-trace` to exit `0` with no finding, and `:124` validates `complete` only as `bool` (caller-declared, unverified). Therefore `request_audit_mode=1` and `PASS` attest audit-mode presence and fixture conformance, not that any request was classified and not that none violated. The payload already disclaims "universal trace completeness" (`:17`). This defeats the converse, never `DENIED` ⇒ post-hoc rejection.

## Contradiction stated, not smoothed

Two token families share the root `DENY`: the policy table's `"decision": "DENY"` (`seat-boundary-r22.json:7,14,35`; `md:13,14,17`) is a pre-dispatch prompt instruction, while the auditor's `SCOPE-*-DENIED` (`py:47,55,76,78,91`) is a post-hoc finding over a recorded request. The docs separate them (`json:47`, `md:22`), but the only lexical bridge is the shared word; and the section heading `md:20` "What is enforced and what is not" uses enforcement language inside a section whose body negates runtime enforcement. Both are wording defects, not semantic counterexamples.

## Affected axes

- **C2 operability (primary):** the audit's evidence is self-describing on its `evaluate` payloads; the disclaimer is the load-bearing artifact for reading `DENIED` correctly.
- **C3 calibration (second-order):** cohort accounting consumes audit findings; a reader who upgrades `DENIED` to "blocked" would mis-partition delivered-faulty seats.
- **C1 depth:** untouched; the six boundary decisions remain policy data, and their validator is outside this seat's read set.
- No ordinal change is claimed; `ordinal_deltas` stays 0.

## Proposed move (one, bounded, advisory only)

Extend the existing disclaimer to every terminal payload rather than renaming identifiers: add the literal `'scope': SCOPE` and one additive classification field (e.g. `'disposition': 'posthoc-record-classification'`) to `main`'s three failure payloads (`:226`, `:233`, `:235`), which currently omit `scope`, and add the same `disposition` key to `evaluate`'s return (`:149-151`). Add one sentence to `seat-boundary-r22.md` § "What is enforced and what is not" mapping policy `DENY` to finding `SCOPE-*-DENIED`.

Why this move: it closes the only terminal paths where a payload arrives without the post-hoc disclaimer, without touching finding ids, exit codes, the 42 fixture expectations, or the strict receipt contract. Renaming `SCOPE-*-DENIED` is rejected for this round because eight fixture expectations (`:168,170,172,174,176,177,180,181`) and any immutable round-22 report already quoting those ids would go stale.

## Risks

- Additive keys change the payload key set; a strict-key consumer would need updating. No consumer appears in this seat's read set, and `selftest` reads only `result['findings']` (`:194`).
- A constant `disposition` string declares, it does not prove; the actual evidence remains the event-anchored site `name:index` (`:141`).
- The vacuous `empty-trace` PASS (`:190`) and constant `request_audit_mode` (`:149`) remain open; the move must not be cited as closing them, and making `request_audit_mode` conditional on `requests_total` would alter the C2 metric and must be preregistered separately.
- `main`'s early payloads are not fixture-covered; adding keys there is source-only and cannot be validated by the current `selftest`.

## Verification (source-only)

1. Static count: every `evaluate` return (`:100`, `:149-151`) and each `main` failure payload (`:226`, `:233`, `:235`) must contain `'scope': SCOPE`; the current gap is exactly the three `main` payloads.
2. Fixture invariance: the 42 expected verdicts depend only on exit `code` and `result['findings']` (`:191-197`); additive keys cannot change either, so the 7/27/8 expectation split is preserved without execution.
3. No `DENIED` literal may appear outside `requested_path`/`classify` and the fixture table; re-grep after any edit.
4. No exit-code branch (`:144`, `:226-237`) may change; `FAIL`/`CANNOT_EVALUATE` semantics stay audit-only.

Reviewed-SHA256: c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4
Predicate: r22-fxc2denialwording
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
