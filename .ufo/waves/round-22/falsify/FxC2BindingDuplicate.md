# FxC2BindingDuplicate — seat-binding duplicate / malformed-name rejection

Target: `.ufo/waves/round-22/candidate/tools/check-seat-bindings.py` (SHA256 c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4).
Mode: source-only falsification, NO-EXEC / NO-FETCH; no fixture was run, no network used, no file outside the seat's declared read/write paths touched.

Verdict summary: the four rejection claims **hold at the source level** (each duplicate/malformed input reaches a `raise ValueError` that is caught into a fail-closed `CANNOT_EVALUATE` result). The falsification lands on **fixture isolation**: three of the four guards have no negative fixture at all, and the two fixtures that touch duplicate handling are non-isolating — the selftest stays green if the guards are deleted. This is a source-visible counterexample to the claim that these checks are demonstrated, not to their code presence.

## Observed facts (source-visible, confidence high)

| # | Claim | Guard site | Preceding lines | Observable |
|---|---|---|---|---|
| 1 | duplicate manifest seat name rejected | L109 `seat['name'] in bound`; `bound[seat['name']] = seat` L115 | L107-110 | `SCOPE-SCHEMA` site `input`, exit 2 |
| 2 | malformed name rejected | L109 `re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,127}', seat.get('name', ''))` | L109-110 | same |
| 3 | duplicate path-list member rejected | L113 `len(paths) != len(set(paths))`, per field read/write | L111-114 | same |
| 4 | duplicate JSON member key rejected | `unique` L22-26 as `object_pairs_hook`, applied L103 (manifest) and L104 (events) | L102-104 | same |

All four converge on L145-146 (`except (ValueError, TypeError, KeyError, AttributeError, UnicodeError)` → `add('SCOPE-SCHEMA','input')`, `code = 2`), status `CANNOT_EVALUATE` via L149.

Precision notes, all source-visible:

- Name regex comes **before** the `seat['name']` subscript, so a missing/non-str name cannot leak a `KeyError` past the guard; a non-str name would raise `TypeError` inside `re.fullmatch`, also caught at L145. Empty, leading `-`/`.`, embedded space, non-ASCII, and >128-character names all fail `fullmatch`.
- Duplicate path detection is exact string identity **within one field**. `local()` (L33-36) forbids `\`, control/format characters, `*?[];:`, empty/`.`/`..` components, and the `LANE + '/'` prefix requirement removes `../` re-entry; a repeated `skill://godspeed` also collides under `set`. Unhashable list members cannot reach `set()` because the `any(...)` clause at L113 rejects them first (`local()` requires `str`), so the tuple of guards is total.
- `unique` is recursive via `object_pairs_hook`, so duplicates at any nesting depth are caught, and JSON escape spellings are normalized by the parser before the hook (e.g. `"name"` vs `"\u006eame"` collide).
- The trace-side twins (L120) reject duplicate event-seat names and duplicate agents, and a trace name outside `bound` — malformed names cannot enter through events.

## Falsification: fixture verdicts (expected vs observed runtime)

Expected fixture verdict under the predicate, for an otherwise-valid manifest:

| Fixture | Expected | Source-derived result |
|---|---|---|
| second seat `{'name':'A', ...}` identical incl. root/paths | exit 2, `SCOPE-SCHEMA` | exit 2, `SCOPE-SCHEMA` |
| `read_paths` containing the same path twice (or the skill URI twice) | exit 2, `SCOPE-SCHEMA` | exit 2, `SCOPE-SCHEMA` |
| name `''`, `' A'`, `'A B'`, 129 chars, non-ASCII | exit 2, `SCOPE-SCHEMA` | exit 2, `SCOPE-SCHEMA` |
| otherwise-valid object with a repeated member key, last wins to the same valid value | exit 2, `SCOPE-SCHEMA` | exit 2, `SCOPE-SCHEMA` |

Observed runtime: **none** — `executed=none`. The right-hand column is derived by reading the guards, not by execution.

The fixture *coverage* claim fails, concretely and source-visibly:

- **F1 — `duplicate-json-key` is masked (L190).** The fixture manifest is `{"seats":[],"seats":[]}`. Even if `unique` were replaced by plain `dict` (last-wins → `{"seats":[]}`), L105 `not data['seats']` raises `ValueError('binding schema')` and yields the *same* exit 2 / `SCOPE-SCHEMA`. The fixture therefore cannot distinguish duplicate-key detection from an empty-seat schema error.
- **F2 — `duplicate` (trace) is masked (L186).** `copy.deepcopy(duplicate['seats'][0])` duplicates the name **and** the agent `'agent-A'`; if the `seat['name'] in by_name` clause at L120 were deleted, `seat['agent'] in agents` still raises `ValueError`, again yielding exit 2 / `SCOPE-SCHEMA`. The fixture isolates the disjunction (name ∨ agent), never the name clause.
- **F3 — no manifest-side duplicate-name fixture exists.** Every case at L156/L189-190 reuses the single-seat `binding` unchanged except `fetches`; `seats` is never lengthened with a second binding entry.
- **F4 — no duplicate-path-list fixture exists.** L156 holds distinct `[src, 'skill://godspeed']` / `[report]`; no case appends a repeat, so L113's `len(paths) != len(set(paths))` is never exercised.
- **F5 — no malformed-name fixture exists.** No case sets a name outside `[A-Za-z0-9][A-Za-z0-9._-]{0,127}`; L109's regex branch is exercised only by the well-formed `'A'`.

Consequence, by source-only mutation reasoning: deleting the manifest duplicate-name clause (L109), the path-duplicate clause (L113), the name regex (L109), or the `object_pairs_hook=unique` wiring (L103-104) leaves the selftest's `cases` table passing — the `duplicate-json-key` case survives via F1 and the trace `duplicate` case via F2. The checks exist; their rejection behaviour is nonetheless **unproven by the shipped fixtures**.

Constructible isolating fixtures (differential, otherwise-valid base):

- duplicate manifest name with a single trace seat (guard removed → `bound['A']` overwritten → exit 0), which F2 cannot achieve because it also duplicates the agent;
- duplicated `read_paths` member on the valid single-seat binding (guard removed → exit 0);
- malformed name **mirrored into the trace name**: a manifest-only malformed name is masked by L120's `seat.get('name') not in bound`, so a naive fixture would pass without the regex; and a malformed name equal to the trace name (guard removed → exit 0) is the only differential that isolates the regex;
- repeated member key inside an otherwise-valid seat object, last-wins to the identical valid object (guard removed → exit 0), which is exactly the differential F1 fails to provide.

These are directly required by the round-22 knowledge doc's checklist item 4: "new checks require fixed negative fixtures before their improvement counts." For the four surfaces above, that precondition is currently unmet.

## Observation / policy / unknown separation

- Observation: guard code, its ordering, its single generic observable, and the exact selftest inputs above are literal file content (L22-26, L33-36, L103-115, L120-121, L145-149, L154-197, L201-241).
- Policy: the tool's own `SCOPE` string (L20) and the knowledge-doc scope limit the claim to post-hoc recorded-request auditing; no preventive enforcement is asserted or should be inferred from this report.
- Inference (not observed): "selftest stays green under guard deletion" is a source-only mutation argument over the case table; it was not executed and no mutated input was run.

## Residual unknowns

- `build/bindings.json` and `build/events.json` are outside this seat's declared read paths, so live fixture content beyond the embedded selftest is unknown; the masking analysis covers the selftest only.
- `evaluate` bypasses `unique` when handed pre-parsed dicts (L103-104 conditional); unreachable from `main` (both inputs are bytes from `git_read`, L201-208), but it is the path the selftest itself uses, so duplicate-member-key behaviour is never exercised through the production parsing route.
- Missing manifest at revision returns `FAIL`/exit 1 with `SCOPE-BINDINGS-MISSING` (L99-100), while an absent events file becomes `None` → schema `ValueError` → `CANNOT_EVALUATE`/exit 2. Asymmetry noted; outside this predicate.
- Cross-field overlap (a path in both `read_paths` and `write_paths`) is accepted because L111-113 checks each field separately; whether that should count as a "duplicate member" is a policy question the source does not settle.
- Symlink aliases and Unicode-normalization aliases are not duplicates under exact-string comparison; the SCOPE string already disclaims symlink/effect proof, so this is bounded, not an open bypass claim.

Reviewed-SHA256: c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4
Predicate: r22-fxc2bindingduplicate
Scope: executed=none

Lane bounds: leaf member — no subagent dispatch.
