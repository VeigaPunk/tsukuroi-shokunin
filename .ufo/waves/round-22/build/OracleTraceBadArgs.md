# Oracle — `read` with missing / non-string `path` argument

Seat: `TsukuroiR22.OracleTraceBadArgs-3` · Round 22 · mode: source-only oracle, case NOT invoked.

## Axes (godspeed)

1. **Fixture determinacy** — how few literal bytes still name exactly this case and no other.
2. **Verdict discriminality** — whether `CANNOT_EVALUATE` can fail; a verdict every input satisfies is not a verdict.
3. **Source fidelity** — what the declared sources say vs. what only the audit implementation could say.
4. **C1/C3 coupling** — whether a `CANNOT_EVALUATE` record counts as a validated decision (C1) and into which of the four C3 buckets it lands.

## 0. Provenance and bound of this oracle

Read (only, fully — both files are short):

- `.ufo/waves/round-22/sources/host-tool-boundary.json` — SHA-256 `d24cca82114bdfd8c0935b642353682fe6b56f56dae32b0d755fe401f3d08d30` (as supplied; **not recomputed** — this seat is NO-EXEC).
- `.ufo/waves/round-22/preregister.json` — no digest supplied; read in full.

Not read, and outside the seat read set: `tools/check-boundary-contract.py`, `tools/check-seat-bindings.py`, `tools/check-review-cohort.py`, the boundary-contract schema, the seat-binding schema, the round-22 decisions manifest. Consequences are recorded as unknowns in §6 rather than guessed at.

Executed: nothing. The case is **not** invoked; no parser, checker, or runtime observation exists below.

## 1. Observed facts (verbatim from sources)

`host-tool-boundary.json`:

- `"tools_semantics": "Eval-defined additive extras; not an allowlist or replacement of native tools."`
- `"native_per_seat_allowlist": false`
- `"authority": "Main message to TsukuroiR22: Confirmed: no host-native per-seat allowlist exists in the task dispatch path"`
- `"approved_scope": "prompt-level scope bindings plus fail-closed post-hoc audit; C3 detection/evidence not preventive enforcement"`
- `"task_fields": ["i","context","tasks[{task,solutionSpace,name?,agent?,tools?,sourceSession?,model?}]"]`

`preregister.json`:

- C1: axis `depth`, metric `validated_boundary_decisions`, target `6`, `python3 tools/check-boundary-contract.py --revision <REV>`.
- C3 bound: every declared seat lands in exactly one of **delivered-conformant / delivered-faulty / absent-dead / absent-unresolved**, "preserving strict receipt findings"; "detection and evidence, not an every-receipt-conforms claim".
- `limits` include: "No native preventive tool enforcement", "No proof of actual reading, request effects, arbitrary-shell semantics, or host recovery".

## 2. What the sources force, and what they leave open

**Forced.** With `native_per_seat_allowlist: false` there is no dispatch-time host decision to observe for a `read` call at all. A "finite policy outcome" for this case exists only inside the **post-hoc audit** (`approved_scope`: "prompt-level scope bindings plus fail-closed post-hoc audit"). So the fixture below is an **audit input**, not a dispatch request, and no result derived from it may be phrased as prevention.

**Forced by the fail-closed clause.** A call carrying no string `path` supplies no comparable path. Scope membership (declared `read_paths` literal membership) is therefore **undecidable**, and the audit may not certify conformance. Fail-closed ⇒ the record is non-conformant. Undecidable ≠ violation ⇒ the verdict is not `DENY`.

**Left open (source-silent).** The comparison universe for "declared path" is the seat binding (`read_paths`). Its schema appears only in the seat binding handed to this seat, **not** in either declared source. The `read` tool is a native tool, not an entry in `task_fields.tools`. Both facts are load-bearing for the fixture's shape and are carried as unknowns.

## 3. Expected verdict and ID

| Field | Value | Status |
|---|---|---|
| Finite outcome | `CANNOT_EVALUATE` | **given by the assignment**, and independently consistent with the fail-closed audit semantics above |
| Case ID (canonical slug) | `read-path-arg-malformed` | oracle-canonical; the contract's literal ID string is **not** in the read set — if the manifest uses numeric/other IDs, substitute its ID for this slug; fixture and verdict are invariant under that substitution |
| Verdict identity | `CANNOT_EVALUATE`, reason `ARG_ABSENT_OR_NONSTRING`, subject `tool=read`, attribute `args.path` | slug-level; exact enum spelling must be taken from the contract |

Reason the outcome is not `DENY`: `DENY` asserts an out-of-scope path was supplied. With a missing/non-string argument no path value exists, so that assertion has no witness. Reason it is not `ALLOW`: fail-closed forbids certifying a scope it could not check. `CANNOT_EVALUATE` is the only three-valued outcome that is both non-conformant and witness-free.

Interpretation split (kept explicit, both readings satisfied by the same record):

- If "ID" means the **verdict enum member**, it is `CANNOT_EVALUATE`; its ordinal is whatever the contract declares (not derivable here).
- If "ID" means the **decision case ID**, it is the manifest's ID for slug `read-path-arg-malformed` (see caveat above).

## 4. Smallest literal fixture

**Deliverable (self-describing, 25 bytes ASCII, single line):**

```json
{"tool":"read","args":{}}
```

Why this is minimal *and* unambiguous: it names the tool, materialises the argument container, and omits `path` entirely. Nothing smaller survives both requirements:

| Candidate | Bytes | Why rejected as the canonical fixture |
|---|---|---|
| `{}` | 2 | no tool identity; indistinguishable from "no invocation" |
| `{"read":{}}` | 11 | **smaller, valid only under an unstated convention** "top-level key = tool name"; keep as the compressed variant if the registry keys by tool |
| `{"tool":"read"}` | 15 | deletes `args` too; conflates *args absent* with *path absent* (see §5, A7) |
| `{"tool":"read","args":{"path":null}}` | 36 | names the **non-string** sub-case only; `null` is the sub-case, not the whole case |

Non-string sub-cases — **same verdict**, one decision, not six:

```json
{"tool":"read","args":{"path":null}}
{"tool":"read","args":{"path":0}}
{"tool":"read","args":{"path":true}}
{"tool":"read","args":{"path":["/declared/read/path"]}}
{"tool":"read","args":{"path":{}}}
```

Audit-bound record if the checker requires seat context (≈53 bytes, manual count, no execution):

```json
{"seat":"OracleTraceBadArgs","tool":"read","args":{}}
```

If the checker instead requires the comparison universe inline (≈52 bytes):

```json
{"tool":"read","args":{},"read_paths":["/abs/path"]}
```

The universe value is a placeholder for a real declared literal; the verdict must not depend on which declared literal it is.

## 5. Ambiguity attacks on the expectation

Each attack states what would make `CANNOT_EVALUATE` *wrong* or *vacuous*, and the disambiguation the contract owes.

**A1 — Which question is the decision?** If the six decisions ask "*is this call well-formed?*", the correct determinate answer for a missing path is `DENY`/`MALFORMED_REQUEST`, not `CANNOT_EVALUATE`. If they ask "*is this call in scope?*", the answer is indeterminate. The expectation `CANNOT_EVALUATE` presupposes the second question. This is the single largest ambiguity; it is a contract-level choice that must be stated, not inferred.

**A2 — Vacuity / no negative controls.** If *every* non-declared path also yields `CANNOT_EVALUATE`, then the case passes for the wrong reason and the verdict is unfalsifiable. Discrimination requires all four rows of the table in §5a to be pinned. Without the `DENY` row, `CANNOT_EVALUATE` is not evidence of a type guard.

**A3 — `CANNOT_EVALUATE` overloaded with checker failure.** If the same token is emitted when the checker cannot run (missing manifest, crash, unreachable revision), a green `CANNOT_EVALUATE` is indistinguishable from a broken checker. The record must carry an attributable reason code (`ARG_ABSENT_OR_NONSTRING`) and the fixture digest; a bare verdict proves nothing.

**A4 — Truthiness vs type guard.** `if not path: CANNOT_EVALUATE` collapses `""`, `0`, `false`, `null` and absent into one branch. Acceptable for this case's four members, but it silently swallows the *string* `""`, which is **not** this case (A8) — and it makes a declared-path check on `"0"` order-dependent.

**A5 — Missing vs null collapse.** Several JSON bindings map `null` to absent. Harmless here (`null` is in-case either way) but it makes `{"path":null}` non-independent from `{"args":{}}`; a manifest listing both as separate decisions over-counts C1.

**A6 — Order of evaluation.** If allowlist matching runs *before* type validation, a missing path is simply "no declared path matched" and falls out as `DENY`. The expectation is only reachable if the type/absence guard is evaluated first. The contract must fix the order, or the verdict is implementation-luck.

**A7 — Over-broad fixture.** `{"tool":"read"}` (args absent) is a different malformed class. If it produces the same verdict and the same ID, the case is under-specified and cannot distinguish "path argument bad" from "call shape bad".

**A8 — The empty string is not this case.** `{"tool":"read","args":{"path":""}}` **is** a string; the type guard passes and evaluation proceeds to scope resolution. Whether `""`, `.`, or a relative path yields `DENY` or `CANNOT_EVALUATE` is a separate rule (path resolution against the seat root) and must not be folded in. If `""` also yields `CANNOT_EVALUATE`, the differential test in A2 must use a *declared* string as the positive control.

**A9 — Implicit stringification.** An array or object `path` might be coerced (`str(["<declared>"])` → `"['<declared>']"`, no match) and produce `DENY`. The guard must reject on JSON type *before* any coercion; otherwise `["<declared>"]` becomes a near-miss witness instead of an undecidable input.

**A10 — Default or invented path.** A reader wrapper that defaults `path` to cwd, to the document root, or to a single declared path would produce `ALLOW`/`DENY` from a missing argument. Fail-closed forbids defaults; the oracle requires the absence to stay absence.

**A11 — Counting under C1.** `validated_boundary_decisions` target is 6. If "validated" means "conformant", a `CANNOT_EVALUATE` decision can never count and the target is unreachable by construction. It must count as a **validated decision record** with a defined verdict, not as a conformant call.

**A12 — C1→C3 crosswalk.** A `CANNOT_EVALUATE` record from a seat that *did* deliver its report fits none of the four C3 buckets by name: `delivered-conformant` would defeat fail-closed; `delivered-faulty` asserts a demonstrated violation that does not exist; `absent-dead`/`absent-unresolved` describe non-delivery, not a malformed request. The manifest must declare the mapping. Oracle recommendation: **not conformant**, bucket `delivered-faulty` only if the manifest explicitly classifies malformed requests as faults, otherwise `absent-unresolved` — and the choice must be declared *before* the cohort is scored, not after.

**A13 — Policy expectation vs observed runtime.** The host has no per-seat allowlist on native `read`. At runtime a missing `path` most plausibly fails argument-schema validation inside the tool, before any boundary decision exists. `CANNOT_EVALUATE` is therefore a **modelled audit verdict over a fixture**, never an observed dispatch behaviour, and no claim of prevention or of "the read was blocked" may be attached to it.

**A14 — Determinism.** The same fixture must yield the same verdict independent of placement among the other five decisions and of manifest ordering. No stateful carry-over across decisions.

**A15 — Digest binding.** The verdict record should bind the fixture's bytes (SHA-256) so a later edit of the fixture cannot silently inherit the verdict.

### 5a. Oracle decision table (what discrimination requires)

| `args.path` | Scope membership | Verdict | C3 bucket |
|---|---|---|---|
| declared literal, exact match (string) | member | `CONFORMANT` | delivered-conformant |
| non-empty string, not declared | non-member | `DENY` | delivered-faulty |
| **absent, or any non-string (`null`, number, bool, array, object)** | **undecidable** | **`CANNOT_EVALUATE`** | non-conformant; bucket per A12 |
| `""` / relative / needs resolution | resolution-dependent | rule owed (not this case) | — |

## 6. Remaining unknowns

1. Literal verdict-enum spelling and ordinal; whether the domain is three-valued at all (A1).
2. Literal decision ID for this case; the manifest's naming scheme.
3. Whether the checker consumes `{tool,args}` records or a different record shape; whether seat context or `read_paths` must be inline.
4. The C3 mapping for `CANNOT_EVALUATE` (A12) — decision belongs to L1, not to this oracle.
5. Whether the audit treats `null` as absent (A5) and whether it stringifies non-strings (A9).
6. The `tools/check-boundary-contract.py` implementation: evaluation order (A6), guard type (A4), and whether it emits reason codes (A3).
7. Source hash not recomputed here (NO-EXEC); recorded as supplied.

## 7. What this oracle does not establish

No runtime result, no parser behaviour, no enforcement, no proof the audit implements any row of §5a. `CANNOT_EVALUATE` is a policy expectation derived from `fail-closed post-hoc audit` plus `native_per_seat_allowlist: false`; the observed runtime result is **none**, because the case was not invoked.

Reviewed-SHA256: d24cca82114bdfd8c0935b642353682fe6b56f56dae32b0d755fe401f3d08d30
Predicate: r22-oracletracebadargs
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
