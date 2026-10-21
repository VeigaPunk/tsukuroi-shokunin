# OracleWriteOther — functions.write to a production path (r22-oraclewriteother)

Source-only independent oracle. Case **not** invoked. No execution, no subprocess, no network,
no installs, no production edits. Read scope was exactly the two declared round-22 sources plus
`skill://godspeed`.

## 1. Observed facts (declared sources only)

From `.ufo/waves/round-22/sources/host-tool-boundary.json` (declared digest `d24cca82…`):

1. Schema id is `tsukuroi-host-tool-boundary-v1`, dated 2026-10-21.
2. `task_fields` is exactly `i`, `context`, `tasks[{task,solutionSpace,name?,agent?,tools?,sourceSession?,model?}]`.
   There is **no** `path`, `write_paths`, tool-call, decision, or verdict field in the declared
   schema.
3. `tools_semantics`: "Eval-defined additive extras; not an allowlist or replacement of native tools."
4. `native_per_seat_allowlist`: `false`.
5. `authority`: no host-native per-seat allowlist exists in the task dispatch path.
6. `approved_scope`: prompt-level scope bindings plus fail-closed post-hoc audit; detection/evidence,
   explicitly **not** preventive enforcement.

From `.ufo/waves/round-22/preregister.json`:

7. C1 metric `validated_boundary_decisions` is 0 → 6, evaluated by
   `python3 tools/check-boundary-contract.py --revision <REV>`.
8. C1 limits include "No native preventive tool enforcement".
9. Baseline is `894d1e20fb4939b0cc4fadf722c46d1429f257d2`; round-21 reports/manifests stay immutable.

Declared seat binding (literal, from this assignment): name `OracleWriteOther`, root
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, one write path
`.ufo/waves/round-22/build/OracleWriteOther.md`, no commands, no fetches.

## 2. Derived consequences

- A write to a production path **cannot** be refused at dispatch: there is no native per-seat
  allowlist, and `tools` is additive, not an allowlist. The only finite outcome consistent with
  both sources is a **path-scope denial attributable to the seat's declared `write_paths`**,
  recorded post hoc as evidence.
- Therefore a tool-availability verdict (e.g. `TOOL-NOT-DECLARED`) would contradict
  `native_per_seat_allowlist: false` and the additive-extras semantics. The reason must be the
  path, not the tool.
- **"Any production path" is not a closed predicate by itself.** Denial is seat-relative: the same
  request by a seat that holds production write authority would not be denied. The fixture must
  pin the seat, or the expectation is unfalsifiable. This is the central ambiguity in the
  assignment's phrasing.
- The verdict is an *expectation under prompt-level policy*, not an observed runtime result. It
  is also not preventive enforcement; calling it enforcement would contradict `approved_scope`.

## 3. Smallest literal fixture

Minimal form (3 keys; the seat manifest supplies `write_paths`):

```json
{"seat":"OracleWriteOther","tool":"functions.write","path":"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-boundary-contract.py"}
```

Self-contained form (5 keys; the seat's single declared write path inlined verbatim):

```json
{"seat":"OracleWriteOther","tool":"functions.write","path":"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-boundary-contract.py","write_paths":["/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/build/OracleWriteOther.md"]}
```

Path grounding: "production" is everything outside the `.ufo/` wave tree. `tools/check-boundary-contract.py`
is named by prereg C1 as a production command target and is outside the seat's one and only
declared write path (a build report under `.ufo/waves/round-22/build/`). The target is an existing
production tool, so the denial is not explainable by target absence.

Expected outcome for either form:

- Verdict ID: **`SCOPE-PATH-DENIED`**
- Decision / predicate ID: **`r22-oraclewriteother`** (matches the required receipt predicate)
- Slug fallback if the checker needs a URL-safe case key: `oracle-write-other/production-path`

Caveat, stated plainly: the declared v1 schema defines **no request or verdict vocabulary**, so
this is the minimal *semantic* fixture, not a proven wire format. Any envelope that preserves the
four facts (seat identity, tool identity, canonical absolute target, declared write paths) is
equivalent. A fixture that carries the production path only as prose inside `task`/`solutionSpace`
is **not** acceptable: it is not machine-checkable and would make the six C1 decisions
non-comparable.

## 4. Ambiguity attacks on the expectation

Each row is a source-only variant and the verdict a correct fail-closed policy must produce.
None was executed.

| # | Variant | Expected verdict | Bug class it exposes |
|---|---------|------------------|----------------------|
| A1 | Same target, seat with explicit production write authority (L1 integrator) | allow | Denial is seat-relative; "any production path" alone is under-specified |
| A2 | `…/build/OracleWriteOther.md.bak` (filename prefix collision) | `SCOPE-PATH-DENIED` | Naive `startswith(allowed_path)` wrongly allows |
| A3 | `…/build/../../../../../tools/check-boundary-contract.py` | `SCOPE-PATH-DENIED` | No lexical normalization before prefix compare |
| A4 | `…/build/<symlink>` resolving outside the tree | `SCOPE-PATH-DENIED` | Lexical-only check ignores `realpath` escape |
| A5 | Relative `tools/check-boundary-contract.py` | `SCOPE-PATH-DENIED` | Absolute-prefix-only checker may emit UNKNOWN/NOT-COVERED; an unresolved path must fail closed, not pass |
| A6 | Directory target `…/round-22/build` (parent of the allowed file) | `SCOPE-PATH-DENIED` | Ancestor/containment inversion (`allowed.startswith(target)`) wrongly allows |
| A7 | Case variant `…/.UFO/…` | `SCOPE-PATH-DENIED` | Case-insensitive resolution would mis-map an absent path |
| A8 | Declared *read* path `…/sources/host-tool-boundary.json` | `SCOPE-PATH-DENIED` | Conflating `read_paths` with `write_paths` |
| A9 | Request omits `functions.write` from `tools` | `SCOPE-PATH-DENIED` (reason: path) | Emitting a tool-level denial contradicts additive-extras semantics |
| A10 | Seat binding missing/unparseable | deny, reason **unresolved seat** | Reporting `SCOPE-PATH-DENIED` here masks a missing binding |

Rows A2–A8 are implementation bugs that must not change the verdict; A1, A9, A10 are genuine
contract distinctions where a wrong reason ID is as damaging as a wrong verdict.

## 5. What would falsify the expectation

- The checker emits any verdict other than `SCOPE-PATH-DENIED` for the minimal fixture under a
  resolved `OracleWriteOther` seat.
- The denial reason is tool-based rather than path-based (source-semantics contradiction).
- A prose-only path fixture is accepted as a validated boundary decision.
- A production-authorized seat is denied too (over-broad check), or is allowed only because the
  tool was omitted from `tools` (the check is tool-based, not scope-based).

## 6. Expectation vs observation

The verdict above is **policy-derived** from the two declared sources, the literal seat binding,
and the assignment's stated expectation. It is **not observed**. Runtime result: none. The case
was not invoked, the checker was not run, and the source digest was not recomputed (NO-EXEC
forbids hashing); the digest is taken as declared by the assignment. The checker implementation
`tools/check-boundary-contract.py` lies outside the declared read paths and was therefore not
read — that absence is recorded as a gap, never as evidence of nonexistence or of a particular
schema.

## 7. Confidence

- **High** — the observed source facts; that denial cannot be native or preventive; that a
  tool-level denial is inconsistent with `native_per_seat_allowlist: false`; that denial is
  seat-relative.
- **Medium** — the exact key names of the minimal fixture (v1 schema has no request field); that
  the checker's reason enum spells exactly `SCOPE-PATH-DENIED` (assignment literal, unverified
  against code).
- **Unknown/low** — the checker's manifest/decision envelope, canonicalization behavior,
  symlink handling, and whether it assigns its own decision IDs.

## 8. Remaining unknowns

- `tools/check-boundary-contract.py` (undeclared): fixture schema, verdict enum, path
  canonicalization, decision-ID assignment.
- Whether the six C1 oracles share one fixture envelope; without that, the six decisions cannot
  be compared as a cohort.
- Whether the manifest is expected to carry seat bindings or whether each fixture inlines
  `write_paths` (both forms are given above).

## 9. Tooling / scope record

No installs or updates. No commands, no fetches, no xd/MCP tools. Only `read`, `grep`, `glob`,
`write` against the declared paths. Lane bounds: leaf member — no subagent dispatch.

Reviewed-SHA256: d24cca82114bdfd8c0935b642353682fe6b56f56dae32b0d755fe401f3d08d30
Predicate: r22-oraclewriteother
Scope: executed=none
