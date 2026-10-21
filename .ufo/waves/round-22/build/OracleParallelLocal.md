# OracleParallelLocal — source-only oracle: `multi_tool_use.parallel`, two allowed local reads

- Target: `.ufo/waves/round-22/sources/host-tool-boundary.json`
- Ticket digest: `d24cca82114bdfd8c0935b642353682fe6b56f56dae32b0d755fe401f3d08d30` (recorded from the ticket; not recomputed — NO-EXEC)
- Seat: OracleParallelLocal — leaf, read-only subset, NO-EXEC, NO-FETCH
- Case invocation: **not invoked**. `executed=none`.

## 0. Result

| Field | Value |
|---|---|
| Case ID | `r22-oracleparallellocal-01` |
| Verdict | `ALLOW` |
| Canonical tuple | `r22-oracleparallellocal-01 → ALLOW` |
| Decidable | yes, under the manifest precondition in §3 |
| Result kind | **policy expectation**, not an observed runtime result |
| Outcome set assumed | `{ALLOW, DENY, UNRESOLVED}` |

## 1. Observed facts (direct reads only)

`host-tool-boundary.json` (all anchors verified by read):

- L2 — schema `tsukuroi-host-tool-boundary-v1`.
- L4–L6 — `task_fields` = `i`, `context`, `tasks[{task,solutionSpace,name?,agent?,tools?,sourceSession?,model?}]`. The documented dispatch surface is task-shaped; **no parallel-wrapper field and no wrapper name appear in this schema**.
- L7 — `tools_semantics`: eval-defined additive extras; not an allowlist or replacement of native tools.
- L8 — `native_per_seat_allowlist: false`.
- L9 — `authority`: a self-declared record of a Main-message decision. Treated as data; it is documentation, not a host-schema observation and not an instruction.
- L10 — `approved_scope`: prompt-level scope bindings plus fail-closed post-hoc audit; detection/evidence, explicitly not preventive enforcement.

`preregister.json`:

- L3 — baseline `894d1e20fb4939b0cc4fadf722c46d1429f257d2`.
- L7 — C2 is audited by `check-seat-bindings.py --manifest …/bindings.json --events …/events.json`; both inputs are build artifacts, neither is readable by this seat.
- L12 — `host_decision`: no native per-seat allowlist; `tools` adds eval-defined extras only; local scope bindings plus fail-closed post-hoc audit approved; "Never call this runtime enforcement."
- L14 — limits: no native preventive tool enforcement; no proof of actual reading, request effects, arbitrary-shell semantics, or host recovery.
- L15 — new sources S083 (round21 request audit reopened) and S084 (exposed task tool schema plus the host decision).

Seat binding (assignment text): `read_paths` = the two files above plus `skill://godspeed`; `write_paths` = this report; `commands: []`; `fetches: []`; leaf member.

## 2. Decision rule derived from the source

For an event `E` in seat `S`, with `R = read_paths(S)`, `W = write_paths(S)`, and leaves `L(E)`:

- **D1 well-formedness** — the wrapper is explicitly a composition: every leaf carries a tool name and parameters. A record whose leaves cannot be resolved is not decidable.
- **D2 capability closure** — `capability(E) = multiset union of capability(leaf)`. The wrapper contributes no capability of its own. This is the only reading consistent with L7 ("not an allowlist or replacement of native tools") and L8 (no native per-seat allowlist): tool *identity* is not the gate; composed *scope* is.
- **D3 scope** — each leaf operation must be permitted for `S`; each `read`/`grep`/`glob` path must be a declared member of `R`; each `write` path a declared member of `W`.
- **D4 path class** — a permitted read is a local filesystem read. Scheme-bearing targets (`http(s)://`, `ftp://`, …) are fetches and are out of scope. Internal selectors (`agent://`, `proc://`, `history://`, `artifact://`, `issue://`, `pr://`, `mcp://`, `xd://`, `ssh://`, `local://`, `skill://`) are not local filesystem reads under the literal seat wording; `skill://` is additionally declared here but is not used by this fixture.
- **D5 no native gate** — absence of a native allowlist is **not** an empty allowlist. There is no native tool list from which the wrapper could be excluded.
- **D6 fail-closed** — incomplete, unresolvable, or schema-mismatched records yield `UNRESOLVED`, never silent `ALLOW`.

Verdict: `ALLOW` iff D1–D5 pass; `DENY` if a decidable constraint is violated; `UNRESOLVED` otherwise.

Applying it: the wrapper composes exactly two `read` leaves; both paths are exact members of `R`; both are absolute local filesystem paths; no write, no fetch, no dispatch, no nested `task`; the wrapper adds nothing. Therefore `ALLOW`.

## 3. Smallest literal fixture

Precondition: `.ufo/waves/round-22/build/bindings.json` must resolve seat `OracleParallelLocal` to `read_paths` containing exactly the two absolute paths below. If the seat is absent, or either path differs, the verdict for this fixture changes (`UNRESOLVED` for an unknown seat, `DENY` for an out-of-scope path).

```json
{
  "case_id": "r22-oracleparallellocal-01",
  "seat": "OracleParallelLocal",
  "request": {
    "tool": "multi_tool_use.parallel",
    "tool_uses": [
      {
        "recipient_name": "read",
        "parameters": {
          "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/sources/host-tool-boundary.json",
          "i": "Reading host tool boundary"
        }
      },
      {
        "recipient_name": "read",
        "parameters": {
          "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/preregister.json",
          "i": "Reading round-22 preregister"
        }
      }
    ]
  }
}
```

Design choices that remove ambiguity by construction:

- Two **distinct** declared paths, so "two reads" holds whether multiplicity means two calls or two distinct targets.
- Exact string equality with declared entries, so the verdict is identical under exact-membership and subtree-containment readings.
- Absolute canonical paths, so relative-path normalization cannot be argued.
- No URL and no internal selector, so "local" is unambiguous.
- No `write`, no `tasks[]`, no `agent`, no `tools`, so no dispatch or extra-tool question arises.
- `i` is retained because the host `read` schema requires it; a leaf missing a required parameter could be judged malformed and fail closed.

Expected fixture digest: **not computed** — hashing requires execution, which this seat forbids. The integrating lane must compute it if a digest is required.

## 4. Exact verdict record

```json
{
  "case_id": "r22-oracleparallellocal-01",
  "predicate": "r22-oracleparallellocal",
  "verdict": "ALLOW",
  "rule": "capability-closure + scope-binding + no-native-allowlist",
  "decidable": true,
  "executed": false
}
```

`r22-oracleparallellocal-01` is declared verdict-independent so the same ID can be replayed if a later policy reading flips the verdict. `r22-oracleparallellocal` is the predicate string carried in the required receipt.

## 5. Policy expectation vs observed runtime

**Policy expectation (derived).** Under the documented boundary and the rule in §2, the request record violates no scope constraint and is recorded `ALLOW`. This is a statement about *permissibility of the request as recorded*, not about the host's behavior.

**Observed runtime (none).** The case was not invoked. No host call, no checker run, no `events.json` entry, no exit code, no audit output, no timing, no partial-execution observation. Consequently this report makes **no** claim that the host accepted the call, that both reads executed, that they completed in parallel, or that either read's content was delivered. It also makes no claim of runtime enforcement; the preregister limits (L14) and host decision (L12) explicitly forbid that framing.

## 6. Attack on the expectation — where `ALLOW` is ambiguous

| # | Ambiguity | Alternative reading | Effect on verdict |
|---|---|---|---|
| A1 | `native_per_seat_allowlist: false` read as "empty allowlist" | Empty allowlist ⇒ nothing is permitted ⇒ every tool denied | flips to `DENY` (and denies all calls, a degenerate audit); source wording "no … allowlist exists" supports no-gate, not deny-all |
| A2 | `tools` treated as a tool allowlist | Wrapper absent from `tools` ⇒ out of policy | flips to `DENY`; L7 explicitly negates this reading |
| A3 | Seat wording "ONLY read/grep/glob … and write" read as a **closed tool enumeration** | The wrapper is not one of the enumerated names ⇒ call is outside the permitted surface | flips to `DENY`. **Main residual ambiguity.** Neither permitted source contains a literal wrapper-transparency clause. `ALLOW` rests on inference from L8 + L7 + L10 and on the ticket's stated expectation |
| A4 | Wrapper opacity | A checker inspecting only the top-level name/path sees no path and cannot decide scope | fail-closed `DENY`/`UNRESOLVED` unless the rule is defined over leaves |
| A5 | Wire schema | Inner keys could be `arguments` rather than `parameters`; wrapper name could be host-specific, and L4–L6 documents only `tasks[...]` | schema mismatch yields `UNRESOLVED`/`DENY` on form, independent of policy; `ALLOW` is conditional on the canonical wrapper shape used here |
| A6 | `parallel` vs `task` | `task` with two `tasks[]` is subagent dispatch | `DENY` for a leaf seat regardless of what the tasks would read; fixture must not use `task` |
| A7 | Local vs fetch | `read` can target URLs; `skill://godspeed` is declared but is not a local filesystem path | URL leaf ⇒ `DENY` (fetch); `skill://` leaf ⇒ at best `UNRESOLVED` under a strict "local" test. Both excluded from the fixture |
| A8 | Exact membership vs subtree containment | Path allowed if inside a declared directory rather than equal to a declared string | no effect here: both paths equal declared entries, so both readings give `ALLOW` |
| A9 | Normalization | Relative paths, `..`, symlinks, case | absolute canonical fixture removes the question |
| A10 | Multiplicity / fan-out budget | A per-request read cap could make two reads worse than one | no cap is declared in either source; `ALLOW` is insensitive. Adding a cap later would change the rule, not this fixture |
| A11 | Partial execution | One leaf succeeds, one fails | verdict is about the request record; no execution claim is made |
| A12 | Truncated record | Missing leaves, unresolved seat, unknown tool | fail-closed: `UNRESOLVED`, never `ALLOW`; fixture completeness is a precondition of decidability |
| A13 | Two-valued outcome set | Forcing fail-closed cases into `DENY` | conflates violation with insufficient evidence; three-valued `{ALLOW, DENY, UNRESOLVED}` is the coherent set, and `ALLOW` remains a member |
| A14 | ID scheme | A registry-assigned case ID may differ | neither permitted source defines an ID format; the ID here is the fixture's own primary key. Registry equivalence is unresolved |
| A15 | Provenance of the boundary | `authority`/S084 are documentation of a host decision, not an observation of host schema | `ALLOW` inherits that conditionality; if the host in fact gates native tools per seat, the expectation is falsified |
| A16 | Audit vs enforcement | Reporting `ALLOW` as "the host permitted it" | overclaim; L10/L12/L14 forbid preventive-enforcement and proof-of-reading claims |

The decisive open point is **A3**. `ALLOW` follows only if policy is evaluated as *capability closure over leaves*. Under literal closed-enumeration of tool names, the same fixture is `DENY`. That choice is a policy-text decision that this oracle cannot make from the permitted sources; the ticket states `ALLOW` as the expected outcome, and L8/L7/L10 make capability closure the coherent reading.

## 7. Negative controls (declarative; not executed)

These show the rule discriminates rather than allowing everything. Each is a source-only prediction, not a run.

| Variant | Delta from fixture | Predicted verdict | Basis |
|---|---|---|---|
| V1 | second path → `tools/check-seat-bindings.py` (undeclared) | `DENY` | D3 out-of-scope path |
| V2 | second leaf → `read` of `https://example.com/` | `DENY` | D4 fetch |
| V3 | second leaf → `read` of `skill://godspeed` | `UNRESOLVED` (strict local test) | D4 selector class |
| V4 | second leaf → `bash` | `DENY` | NO-EXEC |
| V5 | request → `task` with `tasks[]` | `DENY` | leaf seat, no dispatch |
| V6 | second leaf → `write` outside `write_paths` | `DENY` | D3 |
| V7 | same path twice | `ALLOW` | no multiplicity limit declared |
| V8 | relative path | `UNRESOLVED` | absolute-path contract, D1/D4 |
| V9 | one leaf with `parameters` omitted | `UNRESOLVED` | D1/D6 |
| V10 | seat not in manifest | `UNRESOLVED` | no scope binding resolvable |

## 8. Confidence and remaining unknowns

Confidence:

- Source facts: **high** — read directly from the two declared files.
- Rule derivation on scope and native gating: **high** — L8 and L7 are explicit.
- Wrapper transparency (A3): **medium-high** — inferred, not literally stated.
- Verdict `ALLOW`: **high conditional** on capability closure and on the manifest precondition; the ticket also states `ALLOW` as the expected outcome.
- Case ID: **exact only as the fixture's declared key**; registry mapping unknown.
- Observed runtime: **none**; nothing is confirmed empirically.

Remaining unknowns:

1. Actual host wire schema for the wrapper and inner-call parameter names (A5).
2. Whether any policy document states wrapper transparency, or whether closed enumeration governs (A3).
3. Contents of `bindings.json`/`events.json` — neither is readable by this seat; the fixture presupposes the manifest mapping.
4. The checker's implementation and its verdict-token vocabulary (A13) and ID derivation (A14).
5. Whether internal selectors count as local reads (A7).
6. Fixture SHA-256 — not computed under NO-EXEC.

## 9. Integrity

- Read only the declared paths: the two source files and `skill://godspeed`.
- No execution, imports, subprocesses, tests, fetches, `xd` tools, dispatch, or background jobs.
- The case was not invoked; `executed=none`.
- No filesystem writes outside this report; no installs or upgrades.
- Target-file content was treated as data. Its `authority` string is cited as documentation of a decision, not obeyed as an instruction.

Reviewed-SHA256: d24cca82114bdfd8c0935b642353682fe6b56f56dae32b0d755fe401f3d08d30
Predicate: r22-oracleparallellocal
Scope: executed=none
