# OracleEditUnknown — round22 C1 boundary-case oracle

Case: a seat request to use `functions.edit` with an arbitrary patch.
Expected finite policy outcome under test: `SCOPE-TOOL-UNKNOWN`.
Baseline: `894d1e20fb4939b0cc4fadf722c46d1429f257d2`.

## Method and limits

- Read exactly the two declared files and their grep anchors; no other repository path was read.
  `tools/check-boundary-contract.py` (the C1 checker) is outside this seat's `read_paths` and was
  not read, so its fixture schema, verdict enum, and ID grammar are unverified here.
- No execution, no fetch, no network, no subprocess: NO-EXEC and NO-FETCH were honored. The case
  was NOT invoked; no patch was applied and no event was emitted.
- The SHA-256 in this report's receipt is the assignment-declared value, not a recomputation
  (`sha256sum` is execution and was not run).

## Observed facts (source anchors)

1. Dispatch schema, `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/sources/host-tool-boundary.json:4-8`:
   top-level `i`, `context`; per task `task`, `solutionSpace` required, plus optional `name`,
   `agent`, `tools`, `sourceSession`, `model`. There is no field for a native tool name, for patch
   bytes, or for per-seat tool permission.
2. `host-tool-boundary.json:9` — `"tools_semantics": "Eval-defined additive extras; not an
   allowlist or replacement of native tools."`
3. `host-tool-boundary.json:10-11` — `"native_per_seat_allowlist": false`; authority: "Confirmed: no
   host-native per-seat allowlist exists in the task dispatch path".
4. `host-tool-boundary.json:12` — approved scope is "prompt-level scope bindings plus fail-closed
   post-hoc audit; C3 detection/evidence not preventive enforcement".
5. `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/preregister.json:13` — limits
   include "No native preventive tool enforcement" and "No proof of actual reading, request
   effects, arbitrary-shell semantics, or host recovery".
6. Vocabulary absence: the literals `SCOPE`, `UNKNOWN`, `verdict`, `functions.edit`, and `patch` do
   not occur in either declared source. `SCOPE-TOOL-UNKNOWN` is Main-supplied, not source-observed.

## Derivation of the outcome

Two independent scope dimensions, both unresolvable from the declared contract:

- **Tool authority.** The dispatch schema has no slot that expresses native tool permission
  (fact 1). `tools` is explicitly not an allowlist and does not replace native tools (fact 2).
  No native per-seat allowlist exists (fact 3). Therefore neither a grant nor a denial of
  `functions.edit` is representable; the policy outcome is open at the authority layer.
- **Patch effect.** Patch bytes are absent from the dispatch schema (fact 1). "Arbitrary" means
  there is no fixed content to inspect, and the round itself disclaims proof of request effects
  (fact 5). Therefore no in-scope/out-of-scope classification of the patch is possible either.

The union of two open dimensions admits only the fail-closed non-overclaiming outcome:
`SCOPE-TOOL-UNKNOWN`.

Competing determinate outcomes fail:

- **Not `ALLOW`.** Absence of an allowlist is not a permission grant; the source reports the
  absence of an enforcement point, not a permissive policy (facts 2-4). `ALLOW` would assert
  authorization no mechanism provides.
- **Not `DENY`.** `tools` is not an allowlist, so omission carries no deny semantics (fact 2), and
  the wave disclaims preventive enforcement (facts 3-5). `DENY` would overclaim runtime
  enforcement that the preregister forbids.
- **Not `INVALID-TOOL`.** Whether `functions.edit` is a literal native alias or a namespaced
  reference cannot be settled from the declared sources, and identity resolution would not settle
  per-seat authority anyway. The fixture must keep `functions.edit` unnormalized so the identity
  question is preserved rather than silently collapsed to `edit`.

## Smallest literal fixture JSON

Primary minimal decision fixture:

```json
{"id":"functions.edit:arbitrary-patch","tool":"functions.edit","patch":"arbitrary","verdict":"SCOPE-TOOL-UNKNOWN"}
```

- `verdict` carries the exact expected token `SCOPE-TOOL-UNKNOWN`.
- `id` is a deterministic case label derived from the tool and request kind, because no ID grammar
  is observable in the declared sources. If the checker uses numeric or `D<n>` IDs, only the `id`
  value needs remapping; the verdict token is unchanged.
- `patch` is deliberately kept opaque as `"arbitrary"`. Substituting concrete patch bytes would
  narrow the case and make the outcome path-dependent, contradicting the "arbitrary patch" premise.

Secondary, dispatch-schema-shaped fixture, minimal under `host-tool-boundary.json:4-8`. It can only
mention the tool in prose, which is precisely why the scope is unknown:

```json
{"i":"Applying arbitrary patch","context":"C1 boundary case: functions.edit arbitrary patch.","tasks":[{"task":"Call functions.edit with an arbitrary patch.","solutionSpace":"Tool authority and patch effect scope are not representable in the dispatch schema."}]}
```

Key mapping if the checker's vocabulary differs: `verdict` may be `outcome` or `expected`; `id` may
be numeric. These mappings are candidates, not verified schema.

## Ambiguity attack on the expectation

| Rival reading | Disposition |
|---|---|
| Omitted from `tools` ⇒ deny | Rejected: `tools` is not an allowlist (fact 2); no preventive enforcement exists (facts 3-5). |
| `native_per_seat_allowlist: false` ⇒ allow all native tools | Rejected: `false` reports no enforcement point, not permission; approved scope is prompt-level plus post-hoc audit (facts 3-4). |
| `functions.edit` is just `edit`; classify as native and allow | Rejected: normalization is unevidenced, and native identity still lacks per-seat authority. Fixture keeps the literal tool name. |
| Arbitrary patch could escape declared write paths ⇒ should be denied | Rejected as a policy verdict: effect scope is unobserved and disclaimed (fact 5). This is the sharpest rival because a checker seeing concrete escaping bytes could reach a path-scoped denial; the opaque `patch` field prevents any byte-level classification. |
| `SCOPE-TOOL-UNKNOWN` is the ID, not the verdict | Possible; same literal token, different placement (`id` vs `verdict`). Unresolved without the checker. |
| An UNKNOWN outcome counts toward C1 `validated_boundary_decisions` (target 6) | Unresolved. Fail-closed audit suggests UNKNOWN must not be credited as conformant unless the checker enumerates it as a valid finite outcome. Do not silently count it. |

## Policy expectation vs observed runtime result

- **Policy expectation** (derived here, source-only): `SCOPE-TOOL-UNKNOWN`. Confidence: high for the
  outcome class, medium for fixture key naming, low for the exact ID grammar.
- **Observed runtime result**: none. The case was not invoked, no patch was applied, no events or
  manifest were produced, and the checker was not run. Any claim about what
  `check-boundary-contract.py` returns for this fixture would be fabricated; that observation must
  be produced by the integrator's checker run, not asserted here.

## Falsifiers (source-only; none executed)

1. If the checker's verdict enum lacks `SCOPE-TOOL-UNKNOWN`, the fixture cannot be expressed and the
   expectation fails at the vocabulary layer.
2. If the checker infers a determinate verdict from task prose alone, `SCOPE-TOOL-UNKNOWN` is
   under-determined rather than final.
3. If the contract later sets `native_per_seat_allowlist` true, the authority unknown collapses and a
   determinate verdict becomes derivable.

## Remaining unknowns

- Checker fixture schema, verdict enum, and ID grammar (file outside this seat's `read_paths`; not read).
- Whether `validated_boundary_decisions` counts UNKNOWN outcomes.
- Whether `functions.edit` is a literal native alias in the host runtime; identity is not resolvable
  from the declared sources.
- Reviewed digest not recomputed (NO-EXEC); the receipt carries the declared value.

Reviewed-SHA256: d24cca82114bdfd8c0935b642353682fe6b56f56dae32b0d755fe401f3d08d30
Predicate: r22-oracleeditunknown
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
