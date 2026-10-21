# OracleV2ReadOnly — v2 edit-target audit authority oracle (r23 C2)

Seat: `OracleV2ReadOnly` (leaf). Source-only inspection of the v1 gate and the declared
v2 authority. No execution, no hashing, no installation; digest below is the supplied identity.

## Verdict

The existing gate is a v1 gate with no edit vocabulary and no edit-authority field. A v2
manifest is rejected fail-closed (`SCOPE-SCHEMA`, exit 2), and a recorded `edit` request is
classified `SCOPE-TOOL-UNKNOWN` (exit 1) without ever reaching a path check. That is **absence
of a new capability**, not a defect in historical v1 policy: v1's own selftest codifies
`edit -> SCOPE-TOOL-UNKNOWN` at exit 1. The declared v2 authority adds a conjunctive predicate —
an exact edit target must be predeclared for edit **and** read **and** write — which v1 cannot
express, because v1 selects its sole membership list from a binary `tool == 'write'` test. The
sharpest implementation hazard is that the obvious minimal patch to v1 (add `'edit'` to the tool
tuple) silently checks edit against `read_paths`, which is precisely the forbidden
read-implies-write grant.

## Axes (godspeed)

- **A1 authority exactness** — can the authority express `edit ⊆ read ∩ write` per exact target?
- **A2 version discrimination** — does an unknown/newer manifest fail closed rather than false-pass?
- **A3 fixture independence** — is there a literal, self-contained fixture with decision-level
  expectations that does not depend on any round-23 build artifact?

## Observed facts — v1 gate under review

File: `.ufo/waves/round-23/snapshot/tools/check-seat-bindings.py` (declared
`Reviewed-SHA256` identity in receipt; not computed here).

| # | Lines | Observed fact |
|---|-------|---------------|
| F1 | 2, 17 | Docstring and `SCOPE`: audit of *recorded request spellings only*, explicitly "not preventive enforcement". |
| F2 | 72–73 | Tool vocabulary is exactly `read, grep, glob, write, multi_tool_use.parallel, parallel`; anything else returns `SCOPE-TOOL-UNKNOWN`. `edit` is not a member. |
| F3 | 89–94 | `allowed_keys` has entries only for `read, grep, glob, write`. No `edit` key set. |
| F4 | 99–106 | Path checks run only after the vocabulary gate; the membership test is `binding['write_paths' if tool == 'write' else 'read_paths']`. There is no edit branch and no conjunction of lists. |
| F5 | 120 | Manifest schema must equal the literal `tsukuroi-seat-bindings-v1` (and top-level keys must be exactly `{schema, seats}`). |
| F6 | 123–129 | Per-seat validation checks `name`, `root`, `commands == []`, `fetches == []`, then iterates only `('read_paths', 'write_paths')`. There is **no seat key-set equality check**, so an extra `edit_paths` key is neither validated nor rejected — it is silently ignored. |
| F7 | 160–162 | Each non-`SCOPE-SCHEMA` finding id increments `violations`; exit is 2 iff any `SCOPE-SCHEMA` or incomplete seat, else 1 iff any finding, else 0. A `SCOPE-TOOL-UNKNOWN` therefore yields exit 1 / `FAIL` / `request_audit_mode = 1`. |
| F8 | 199 | Selftest case: `case('unknown', 'edit', {}, 1, 'SCOPE-TOOL-UNKNOWN')`. This is v1 policy *by construction*, not an accident. |
| F9 | whole file | A grep for `edit|Edit|EDIT|v2|V2` over the file matches only line 199. There is no `v2`, no `SCOPE-EDIT-*`, no edit path list anywhere in the gate. |
| F10 | 43–57 | `requested_path` rejects `http(s)://` and `host:port/` as `SCOPE-FETCH-DENIED`, strips range selectors only when `selector=True` (only `read`/`grep` pass that flag), then requires `local()`. |
| F11 | 33–36 | `local()` rejects `\`, control/format/surrogate/line-separator characters, `*?[];:`, and any empty/`.`/`..` segment — but accepts any subpath under `LANE`, including production paths if a manifest declares them. |
| F12 | 114–115, 163–167 | `manifest is None` yields `FAIL`/1 with `SCOPE-BINDINGS-MISSING`; schema exceptions yield `CANNOT_EVALUATE`/2 with `SCOPE-SCHEMA` at `input` and `seats_bound = 0` (the `bound` local is not yet assigned). |

## Absence versus defect

| Question | Finding | Basis |
|---|---|---|
| Does v1 know `edit`? | **No — absence.** `edit` is out of vocabulary and its selftest asserts that classification. | F2, F3, F8, F9 |
| Does v1 have an edit-authority field? | **No — absence.** Schema v1 declares only read/write lists; `edit_paths` is discarded even if present. | F5, F6 |
| Does v1 false-pass a v2 manifest? | **No — fail-closed.** Schema mismatch aborts before any seat/event processing with exit 2. | F5, F12 |
| Does v1 false-pass a recorded edit? | **No.** Every edit event produces a finding and exit 1; there is no path that maps edit to an allow. | F2, F7 |
| Is v1's red on r22 edit requests a historical-policy defect? | **No.** It is the documented v1 classification of an out-of-vocabulary tool, matching C2's "legacy schema-v1 policy and historical reds unchanged". | F8 + preregister C2 scope |
| Can v1 enforce "edit requires write"? | **No — the predicate does not exist.** v1 cannot certify edit authorization in either direction. | F4 |
| Latent v1 traits worth not inheriting | Unknown seat keys silently ignored (F6); unknown tools counted as violations rather than as unevaluable (F7). Both fail **red**, never green, so they are bounded and not defects against v1's declared scope — but v2 must not keep key-blindness. | F6, F7 |

Historical observations (`.ufo/waves/round-23/sources/structured-edit-observations.json`) record
four `edit` requests in round 22 — `CritRuntime` line 15 (`argument_keys: path, stream_content`)
and `OraclePathArtifact` lines 30, 33, 36 (`argument_keys: i, new_string, old_string, path`) —
each with an absolute build-report `path` and `body_fields: omitted`. Under v1 those four events
are `SCOPE-TOOL-UNKNOWN` (F8/F9), i.e. red for being outside the vocabulary, not red for a path
violation. The observation file explicitly disclaims universal tool semantics and is metadata
only; it is **not** authority — authority comes from the manifest plus the event, never from the
observation alone.

## Independent literal fixture

Fixture-local literals; no file on disk is read or implied. Proposed names are marked in the
next section. `E`, `R`, `W`, `X` are aliases used only in the expectation table below.

Manifest (v2):

```json
{
  "schema": "tsukuroi-seat-bindings-v2",
  "seats": [
    {
      "name": "V2FixtureSeat",
      "root": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin",
      "read_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/V2FixtureSeat.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/sources/edit-decision-policy.json",
        "skill://godspeed"
      ],
      "write_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/V2FixtureSeat.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/V2FixtureWriteOnly.md"
      ],
      "edit_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/V2FixtureSeat.md"
      ],
      "commands": [],
      "fetches": []
    },
    {
      "name": "V2FixtureNoWrite",
      "root": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin",
      "read_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/V2FixtureNoWrite.md",
        "skill://godspeed"
      ],
      "write_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/V2FixtureNoWriteOther.md"
      ],
      "edit_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/V2FixtureNoWrite.md"
      ],
      "commands": [],
      "fetches": []
    }
  ]
}
```

Events (v2), aliases: `E` = `.../build/V2FixtureSeat.md`, `R` =
`.../sources/edit-decision-policy.json`, `W` = `.../build/V2FixtureWriteOnly.md`, `X` =
`.../build/V2FixtureUndeclared.md`, `E2` = `.../build/V2FixtureNoWrite.md` (all under
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/`):

```json
{
  "schema": "tsukuroi-seat-events-v1",
  "seats": [
    {
      "name": "V2FixtureSeat",
      "agent": "fixture-agent-1",
      "complete": true,
      "events": [
        {"tool": "edit", "args": {"i": "edit declared target", "path": "E", "old_string": "a", "new_string": "b"}},
        {"tool": "edit", "args": {"i": "edit declared target stream", "path": "E", "stream_content": "c"}},
        {"tool": "edit", "args": {"i": "edit undeclared target", "path": "X", "old_string": "a", "new_string": "b"}},
        {"tool": "edit", "args": {"i": "edit read-only target", "path": "R", "old_string": "a", "new_string": "b"}},
        {"tool": "edit", "args": {"i": "edit write-only target", "path": "W", "old_string": "a", "new_string": "b"}},
        {"tool": "edit", "args": {"i": "edit traversal target", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/../build/V2FixtureSeat.md", "old_string": "a", "new_string": "b"}},
        {"tool": "edit", "args": {"i": "edit external target", "path": "https://example.invalid/edit-target", "old_string": "a", "new_string": "b"}},
        {"tool": "edit", "args": {"i": "edit internal URI target", "path": "xd://edit", "old_string": "a", "new_string": "b"}},
        {"tool": "edit", "args": {"i": "opaque patch only", "patch": "*** Begin Patch"}},
        {"tool": "multi_tool_use.parallel", "args": {"tool_uses": [
          {"recipient_name": "functions.edit", "parameters": {"path": "E", "old_string": "a", "new_string": "b"}},
          {"recipient_name": "functions.edit", "parameters": {"path": "R", "old_string": "a", "new_string": "b"}}
        ]}}
      ]
    },
    {
      "name": "V2FixtureNoWrite",
      "agent": "fixture-agent-2",
      "complete": true,
      "events": [
        {"tool": "edit", "args": {"i": "edit with read but no write", "path": "E2", "old_string": "a", "new_string": "b"}}
      ]
    }
  ]
}
```

The fixture is independent: seat names, agent ids, and target literals do not come from any
round-23 build artifact; the two edit argument shapes mirror only the two recorded shapes named
in the observation source (`path + stream_content`; `path + old_string + new_string + i`).

## Exact policy expectation under declared v2 authority

Declared authority: `.ufo/waves/round-23/sources/edit-decision-policy.json`
(`tsukuroi-edit-policy-v1`, eight rows, scope "declared audit authority for structured target
metadata only; no native prevention, opaque patch interpretation, effect or reading proof") and
preregister C2 ("new explicit schema-v2 audit authority for exact predeclared structured edit
targets; legacy schema-v1 policy and historical reds unchanged"). The policy fixes **decisions**,
not finding ids or exit codes.

| # | Fixture event | Target relation | Exact decision |
|---|---|---|---|
| 1 | seat `V2FixtureSeat` event 0 | `E ∈ edit ∩ read ∩ write` | `ALLOW` (`DECLARED_EDIT`) |
| 2 | event 1 | `E ∈ edit ∩ read ∩ write`, stream shape | `ALLOW` (`DECLARED_EDIT`) |
| 3 | event 2 | `X ∉ edit ∪ read ∪ write` | `DENY` (`UNDECLARED_EDIT`) |
| 4 | event 3 | `R ∈ read` only | `DENY` (`READ_ONLY_EDIT`) |
| 5 | event 4 | `W ∈ write` only | `DENY` (`WRITE_ONLY_EDIT`) |
| 6 | event 5 | dot-segment spelling of `E` | `DENY` (`EDIT_TRAVERSAL`) |
| 7 | event 6 | `https://` target | `DENY` (`EDIT_EXTERNAL`) |
| 8 | event 7 | `xd://` target | `DENY` (`EDIT_EXTERNAL`) |
| 9 | event 8 | no structured target | `UNKNOWN` (`OPAQUE_PATCH`) — not ALLOW, not DENY |
| 10 | event 9 | two targets in one adapter call | `CHECK_EACH` (`EXPANSION`): child `E` ALLOW, child `R` DENY; the aggregate must not be ALLOW |
| 11 | seat `V2FixtureNoWrite` event 0 | `E2 ∈ edit ∩ read`, `E2 ∉ write` | `DENY` (derived: `DECLARED_EDIT` requires "both read and write", so the conjunctive predicate fails; no row grants edit without write) |

Expectation totals over the 11 recorded events: 3 ALLOW (events 0, 1, and the first expansion
child), 7 DENY, 1 UNKNOWN, plus the expansion aggregate is per-target. The crux of the assigned
question: **an edit target declared for edit and read but not write is DENY** — the precondition
is `edit_paths ∩ read_paths ∩ write_paths`, not `edit_paths ∪` any pair. Row 11's label is
[INFERENCE] (the policy has no ninth row); its DENY value is entailed by row 1's declared reason
("predeclared for edit and for both read and write") and row 4's stated principle that edit needs
its explicit target read authority, applied symmetrically to the missing write authority.

Proposed-but-not-declared literals (marked [INFERENCE], not authority): schema string
`tsukuroi-seat-bindings-v2`, seat key `edit_paths`, and a denial id such as
`SCOPE-EDIT-TARGET-DENIED` with `OPAQUE_PATCH` mapping to `SCOPE-SCHEMA` at event level. The
declared sources say "schema-v2" and name no key, id, or code; an evaluator that invents them
must state them as its own contract.

## v1 projection of the identical fixture (inspection only)

- **As written (schema `tsukuroi-seat-bindings-v2`)**: line 120 schema mismatch raises
  `ValueError('binding schema')`; line 163–167 returns code 2, `status: CANNOT_EVALUATE`,
  `request_audit_mode: 0`, `seats_bound: 0`, `requests_total: 0`, findings
  `[{id: SCOPE-SCHEMA, site: input}]`. No seat, path, or event is examined.
- **Relabelled to `tsukuroi-seat-bindings-v1` (keeping `edit_paths`)**: top-level keys still
  match; per-seat validation passes because `edit_paths` is invisible to F6; `skill://godspeed`
  is admitted in `read_paths` only. Event loop then produces 12 `SCOPE-TOOL-UNKNOWN` findings
  for 11 recorded events (9 direct edits + 2 expansion children classified in the same event +
  1 second-seat edit), `requests_total: 11`, `violations: 12`, exit 1, `status: FAIL`,
  `request_audit_mode: 1`. No `SCOPE-PATH-DENIED` or `SCOPE-FETCH-DENIED` is emitted for any
  edit — confirmed by the fact that edit never reaches line 99–106.
- **Naive minimal patch hazard [INFERENCE from F2/F4]**: adding only `'edit'` to the line 72
  tuple raises `KeyError` at line 95 (`allowed_keys['edit']`), caught per event as
  `SCOPE-SCHEMA`. Adding `'edit'` to both the tuple and `allowed_keys` but leaving line 105
  unchanged checks edit against **`read_paths` only** (the `tool == 'write'` ternary is false for
  edit), which would return ALLOW for the `READ_ONLY_EDIT` row (table row 4, event index 3) and
  for the expansion child on `R` — a direct violation of the declared rows 3 and 8. v2 must branch explicitly:
  exact single target, membership in `edit_paths` **and** `read_paths` **and** `write_paths`,
  `selector=False` so a range is not stripped into an exact target (F10), no `;` splitting, and
  no `skill://`/URL admission in `edit_paths`.

## Remaining unknowns

- No v2 evaluator source exists in the declared read set; this report audits the v1 gate and the
  declared policy only. Any v2 implementation is uncited and its ids/codes are unverified.
- The declared policy fixes eight decisions but not their machine encoding (finding ids, exit
  codes, aggregate semantics beyond `CHECK_EACH`); expectations above are decision-level.
- `_revision` binding behavior was not read (outside the declared read set); revision selection
  and branch-tip handling are unaudited.
- Observations are transcript metadata with omitted bodies; they establish argument-key shapes
  and target paths only, never effects or reading proof, and are not authority by themselves.
- No execution was performed: no hashing, listing, import, or test run; the reviewed digest is
  the supplied declaration.

Reviewed-SHA256: 8fccb655fe94e49d4189dc7e2311e1e29cf50ac6b59f4ff280f49676316a04b6
Predicate: r23-oraclev2readonly
Scope: executed=none
