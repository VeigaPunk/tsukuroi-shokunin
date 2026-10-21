# OracleV2Opaque — v2 structured-edit authority for patch-only and freeform edit

**Round** 23 · attempt 1 · baseline `ae01e50f582016384e620022be38bf5367000e2e`
**Seat** `OracleV2Opaque` (leaf; no dispatch) · source-only oracle · NO-EXEC / NO-FETCH
**Axes touched** C1 depth (how the eight declared edit decisions apply to a recorded request), C2 operability (making the v2 authority observable as a mode distinct from v1). No C3 claim.
**Bound source** `.ufo/waves/round-23/snapshot/tools/check-seat-bindings.py`; SHA-256 `8fccb655fe94e49d4189dc7e2311e1e29cf50ac6b59f4ff280f49676316a04b6` **as supplied**, not recomputed.
**Method** literal reads of the bound files plus token-level `grep` restricted to the bound checker. No LSP server is mounted on this binding (read/grep/glob only), so no semantic-server trace is claimed and no empty cold result is treated as absence. Every claim below cites literal source text or a named artifact.

**Axes spelled out** (Godspeed step 1): *depth* = the policy rows must be applicable to a concrete request, not just enumerable; *operability* = a consumer must be able to tell "v2 authority ran" from "v1 legacy ran"; *non-harm* = no legacy verdict, no historical red, and no read/write rule may move.

---

## 1. Observed facts in the old gate (v1)

All line numbers are in the bound checker.

| # | Fact | Literal basis |
|---|---|---|
| F1 | The admitted tool vocabulary is closed and contains no `edit`. | L72–73: `if tool not in ('read','grep','glob','write','multi_tool_use.parallel','parallel'): return ['SCOPE-TOOL-UNKNOWN']` |
| F2 | An unknown tool returns **before** any argument inspection, so an `edit` request's `path` is never compared to any list. | L72–73 precede `isinstance(args, dict)` L74 and the path comparison L105 |
| F3 | An unknown tool is counted as a violation and, alone, drives exit 1. | L160 `violations += sum(fid != 'SCOPE-SCHEMA' ...)`; L162 `(1 if findings else 0)` |
| F4 | The legacy red for `edit` is pinned by the gate's own selftest. | L199 `case('unknown', 'edit', {}, 1, 'SCOPE-TOOL-UNKNOWN')` |
| F5 | Per-seat keys are **not** closed: only `name`, `root`, `commands`, `fetches` are checked. An `edit_paths` key is accepted and stored, then never read. | L124 validates those four fields only; L130 `bound[seat['name']] = seat`; no `set(seat)` check anywhere |
| F6 | Manifest list fields validated are only `read_paths`, `write_paths`; each must be non-empty, `local()`, and duplicate-free. | L126–129 |
| F7 | The manifest schema literal is exact; any other schema is a schema failure, not a pass. | L120 `data.get('schema') != 'tsukuroi-seat-bindings-v1'` → L121 → L164–165 exit 2 |
| F8 | The trace schema literal is exact; a bound seat missing from the trace is `SCOPE-TRACE-MISSING` and exit 2. | L131–132; L135–136; L142–144; L162 |
| F9 | Aggregate precedence is cannot-evaluate first, then findings, then clean. `request_audit_mode` is `int(code != 2)`. | L162; L167 |
| F10 | Path semantics: `local()` requires the LANE prefix, rejects backslash, control classes, `*?[];:`, and any empty/`.`/`..` segment; selectors are stripped only when `selector=True` (read/grep); `skill://godspeed` is admitted for read, denied for write. | L33–36; L43–58; L102; L215 |
| F11 | Recorded structured-edit requests carry a structured `path`, in two different body shapes: `['path','stream_content']` and `['i','new_string','old_string','path']`. | `structured-edit-observations.json` observations 1–4 (CritRuntime request line 15; OraclePathArtifact lines 30, 33, 36) |
| F12 | The declared policy has eight rows, including `OPAQUE_PATCH = UNKNOWN` with reason "Missing structured target is not inferred from opaque patch text", and `EXPANSION = CHECK_EACH`. The policy scope is "structured target metadata only; no native prevention, opaque patch interpretation, effect or reading proof." | `edit-decision-policy.json` rows; `scope` field |
| F13 | C2 asks for a **new schema-v2 audit authority** while "legacy schema-v1 policy and historical reds unchanged", with "body data opaque". | `preregister.json` claim C2 `scope` |

One consequence worth stating plainly: the gate audits recorded **spellings**, not file existence (L17 `SCOPE`). A fixture therefore needs no files on disk, and a body's text can never be evidence of a target.

---

## 2. Absence of a capability, not a defect in historical policy

The distinction is testable, not rhetorical:

| Question | v1 answer | Epistemic status |
|---|---|---|
| Does v1 know the tool `edit`? | No (L72–73) | **capability absent** |
| Did v1 judge the edit's target against `write_paths`? | No — it returns at L73, so L105 was never reached | **unclassified**, neither allowed nor target-denied |
| Did v1 reject a manifest that declares `edit_paths`? | No — seat keys are unclosed (L124); the list is stored (L130) and ignored | **silent absence** — the only dangerous form here |
| Is `SCOPE-TOOL-UNKNOWN` a finding about the seat's behaviour? | No — it is a statement that the request spelling lies outside the audit vocabulary | **coverage statement** |
| Does v1 claim otherwise? | No: docstring "not preventive enforcement" (L2); `SCOPE` disclaims "universal trace completeness" (L17) | **no overclaim by v1** |

A defect would require the gate to model `edit` and get it wrong — e.g. resolving `path` and comparing it to the wrong list, rejecting a path that is bound, or dropping the event without a finding. None occurs: the tool check short-circuits before the path check. v1 is therefore *conservative but not incorrect about what it covers*.

Three operational rules follow, and they are the part most likely to be violated downstream:

1. **Never green a historical red by re-reading it under v2.** The r22 edit events are evidence of what was recorded, not of authority. `preregister.json.limits` forbids retrospective authorization and manifest/report rewrite. A v2 fixture must be independent of those seats (mine is, §4).
2. **Never delete the legacy red to "fix" the gap.** The v2 boundary must be a distinct manifest schema. L120 enforces an exact literal, so a v2 manifest fed to the legacy path yields `SCOPE-SCHEMA` / exit 2 (`CANNOT_EVALUATE`, never `PASS`). That is the structurally correct outcome and it is cheap.
3. **Count unknown-target requests separately from violations.** If `OPAQUE_PATCH` were folded into `violations`, the audit would convert absence of a structured target back into an accusation — exactly the error this seat exists to prevent.

---

## 3. Declared v2 authority — exact per-request contract

### 3.1 Pinned literally by the sources

* Decision ids come from the closed eight-row vocabulary: `DECLARED_EDIT`, `UNDECLARED_EDIT`, `READ_ONLY_EDIT`, `WRITE_ONLY_EDIT`, `OPAQUE_PATCH`, `EDIT_TRAVERSAL`, `EDIT_EXTERNAL`, `EXPANSION`.
* Verdicts are `ALLOW`, `DENY`, `UNKNOWN`. `CHECK_EACH` is a **router**, not a fifth verdict: it attaches to a wrapper and yields per-child rows.
* `DECLARED_EDIT` requires the exact target to be predeclared for **edit and both read and write**.
* `OPAQUE_PATCH` is `UNKNOWN`; the target is **not** inferred from opaque patch text.
* `EXPANSION` scopes every recorded adapter read or write separately (parallel children, per-step recording).
* Body data is opaque; no effect, reading, symlink or native-prevention claim.

### 3.2 Deliberate v2 delta (each item is required for the policy to be applicable, not a preference)

| # | Requirement | Why it is forced |
|---|---|---|
| D1 | Dispatch on the **exact** manifest schema literal; v2 must be a different literal from `tsukuroi-seat-bindings-v1` (convention: `tsukuroi-seat-bindings-v2`). | L120's exact match; otherwise v2 semantics leak into legacy runs |
| D2 | Close the v2 per-seat key set to exactly `{name, root, read_paths, write_paths, edit_paths, commands, fetches}`. | L124 tolerates extra keys silently (F5); without closure, `edit_paths` is inert and authority drifts invisibly |
| D3 | Validate `edit_paths` with `local()` (no `skill://` exemption), list-typed, duplicate-free, **empty allowed**. | L128's `not paths` must not be copied: a seat with no edit authority must still be declarable, else `UNDECLARED_EDIT` has no reachable premise |
| D4 | Admit `edit`; resolve the target **before** the generic missing-path `ValueError` (L97–98). | A missing target is policy material (`OPAQUE_PATCH`), not a malformed argument |
| D5 | Apply **no** closed body-key set to `edit`. | Observed shapes differ, and one shape has no `i` at all (F11); a whitelist would schema-fail a real recorded request |
| D6 | Do **not** strip selectors for `edit`. | L102 passes `selector=True` only for read/grep; `local()` rejects `:` outright (L35) |
| D7 | Keep `read` and `write` semantics byte-identical: `write` still compares only `write_paths`, `read` only `read_paths` (L105). `edit` is the only new comparison. | Non-harm: the new authority must not tighten or loosen any existing rule; a bound write path must remain a legal `write` even when it is an illegal `edit` |

### 3.3 Decision function (derived, ordered; structural rows preempt membership)

```
edit_request(seat, args)
  if not isinstance(args, dict)                     -> SCOPE-SCHEMA
  target = args.get('path')
  if 'path' in args:
      if not isinstance(target, str) or not target  -> SCOPE-SCHEMA        # L97-98 parity; path:null is malformed
      if uri_shaped(target)                         -> [EDIT_EXTERNAL]     # any scheme:// or host:port/
      if not local(target)                          -> [EDIT_TRAVERSAL]    # '..', '.', '//', ':', glob, ';', '\', control, non-LANE
      if target not in seat.edit_paths              -> [UNDECLARED_EDIT]
      rows = []
      if target not in seat.write_paths             -> rows += [READ_ONLY_EDIT]
      if target not in seat.read_paths              -> rows += [WRITE_ONLY_EDIT]
      return rows or [DECLARED_EDIT]
  if any(k not in ('path', 'i') and isinstance(v, str) and v for k, v in args.items())
                                                    -> [OPAQUE_PATCH]     # body never read
  return SCOPE-SCHEMA                                                     # empty request is malformed, not opaque
```

Notes that make the function exact:

* `uri_shaped` generalises L46 and L48 to any `scheme://` plus the `host:port/` form, so `https?`, `xd://`, `skill://`, `artifact://`, `local://` are `EDIT_EXTERNAL`, matching the row's reason "Remote or internal URIs do not become filesystem edit targets".
* A relative or alternate spelling (`source`, `a//b`, `x.md:raw`, `x.md;y.md`, `**`) is `EDIT_TRAVERSAL` ("no dot-segment or alternate spelling expands the target list"). Every such string is `DENY`; only the row id is derived.
* A target declared for edit but in neither read nor write emits **both** `READ_ONLY_EDIT` and `WRITE_ONLY_EDIT`; the verdict is `DENY` either way, so row-selection ambiguity never changes an outcome.
* If a target is present, body fields are ignored entirely. v2 therefore audits the **declared** target only; it cannot prove a body touched no other path. That limit is already declared ("body data opaque", "no effects claim") and must be stated in the result scope, not papered over.
* Key presence, not truthiness, selects the structured branch: `path: null` or a non-string `path` is malformed (`SCOPE-SCHEMA`), not opaque. `OPAQUE_PATCH` is reserved for requests with no target slot at all, which is what "missing structured target" (F12) means.
* `OPAQUE_PATCH` requires an actual non-empty body. `edit {}` is malformed, not opaque — otherwise "missing target" would become the normal spelling and `SCOPE-SCHEMA` would lose its meaning.

### 3.4 Verdict and aggregate (derived; two choices must be preregistered)

Per site: `ALLOW` iff the only applicable row is `DECLARED_EDIT`; `UNKNOWN` iff `OPAQUE_PATCH`; `DENY` otherwise. A wrapper carrying `EXPANSION` gets no verdict.

Aggregate, recommended (v1 precedence at L162 is cannot-evaluate first):

* `violations` = count of DENY decisions plus non-schema v1 findings (L160 rule), **excluding** `OPAQUE_PATCH`.
* `unknown_decisions` = count of `UNKNOWN` verdicts, new field.
* `status`: exit 2 if schema failure, missing/incomplete seat, or `unknown_decisions > 0`; else exit 1 if `violations > 0`; else exit 0.
* Rationale for `UNKNOWN` ⇒ exit 2: an opaque request has the same epistemic status as an incomplete trace — compliance was not established. Reporting `PASS` would claim it was.

Alternative, admissible only if preregistered: `DENY` dominates `UNKNOWN` (exit 1). It changes no per-site expectation; it changes only the aggregate in §4 Doc 2.

`structured_edit_mode`:

* `1` iff the v2 manifest validated and the evaluator ran under v2 — **independent of the verdict**. A missing seat trace, an incomplete trace, a per-event schema failure, or an opaque request must not zero it.
* `0` on the legacy path.
* Do **not** implement it as `int(code != 2)` (L167 pattern). That would report 0 precisely when the authority exists but the run is inconclusive, and the C2 metric would be held hostage by an unrelated infrastructure miss.
* Optional, cheap strengthening: also report `structured_edit_events` (number of classified edit events) so `mode=1` is distinguishable from "authority present, zero edit events".
* If the round contract demands byte-identical legacy output, omit the field on the legacy path and preregister "absent = 0" for the metric. Either way, **no legacy status, finding, or red may change**.

---

## 4. Independent literal fixture

Four witness cases, independent of the r22 transcripts and of the gate's own selftest (which uses `/source`, `/report`, seat `A`): different seat names, different file names, synthetic bodies. Doc 1's manifest is reused unchanged by Docs 2 and 3; Doc 0 carries its own v1 manifest. No target file needs to exist (L17). Nothing here is executed.

`LANE = /home/vgpnk/Projects/shokunin/tsukuroi-shokunin` — written in full below.

### Doc 0 — legacy control (v1 manifest, one structured edit)

```json
{
  "schema": "tsukuroi-seat-bindings-v1",
  "seats": [
    {
      "name": "LegacyControl",
      "root": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin",
      "read_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureAlpha.md"
      ],
      "write_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureAlpha.md"
      ],
      "commands": [],
      "fetches": []
    }
  ]
}
```

```json
{
  "schema": "tsukuroi-seat-events-v1",
  "seats": [
    {
      "name": "LegacyControl",
      "agent": "fixture-agent-legacy",
      "complete": true,
      "events": [
        {
          "tool": "edit",
          "args": {
            "i": "fixture legacy control",
            "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureAlpha.md"
          }
        }
      ]
    }
  ]
}
```

**Exact expectation:** `SCOPE-TOOL-UNKNOWN` at `LegacyControl:0`; `violations` 1; exit 1; `status` `FAIL`; `request_audit_mode` 1; `structured_edit_mode` 0.
**Load-bearing claim:** the path is fully bound for read *and* write, yet no path finding appears. That is the literal proof that v1 never judged the target — the absence, not a defect.

### Doc 1 — v2 allow-only (also the empty-`edit_paths` witness)

```json
{
  "schema": "tsukuroi-seat-bindings-v2",
  "seats": [
    {
      "name": "FixtureAlpha",
      "root": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin",
      "read_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureAlpha.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureGamma.md"
      ],
      "write_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureAlpha.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureBeta.md"
      ],
      "edit_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureAlpha.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureBeta.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureGamma.md"
      ],
      "commands": [],
      "fetches": []
    },
    {
      "name": "FixtureEmpty",
      "root": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin",
      "read_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureAlpha.md"
      ],
      "write_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureAlpha.md"
      ],
      "edit_paths": [],
      "commands": [],
      "fetches": []
    }
  ]
}
```

```json
{
  "schema": "tsukuroi-seat-events-v1",
  "seats": [
    {
      "name": "FixtureAlpha",
      "agent": "fixture-agent-alpha",
      "complete": true,
      "events": [
        {
          "tool": "edit",
          "args": {
            "i": "fixture stream edit",
            "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureAlpha.md",
            "stream_content": "fixture-body-opaque"
          }
        },
        {
          "tool": "edit",
          "args": {
            "i": "fixture replace edit",
            "new_string": "fixture-new",
            "old_string": "fixture-old",
            "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureAlpha.md"
          }
        }
      ]
    },
    {
      "name": "FixtureEmpty",
      "agent": "fixture-agent-empty",
      "complete": true,
      "events": []
    }
  ]
}
```

**Exact expectation:** `DECLARED_EDIT` / `ALLOW` at `FixtureAlpha:0` and `:1`; `violations` 0; `unknown_decisions` 0; exit 0; `status` `PASS`; `structured_edit_mode` 1.
**Also pinned:** `FixtureAlpha:0` has no `i` and carries `stream_content` — a body-key whitelist (F11/D5) would wrongly schema-fail it; `FixtureEmpty.edit_paths = []` must validate (D3).

### Doc 2 — v2 full matrix (deny rows, opaque rows, expansion, spellings)

Manifest: Doc 1's, unchanged.

```json
{
  "schema": "tsukuroi-seat-events-v1",
  "seats": [
    {
      "name": "FixtureAlpha",
      "agent": "fixture-agent-alpha",
      "complete": true,
      "events": [
        {
          "tool": "edit",
          "args": {
            "i": "fixture write-only target",
            "new_string": "fixture-new",
            "old_string": "fixture-old",
            "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureBeta.md"
          }
        },
        {
          "tool": "edit",
          "args": {
            "i": "fixture read-only target",
            "new_string": "fixture-new",
            "old_string": "fixture-old",
            "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureGamma.md"
          }
        },
        {
          "tool": "edit",
          "args": {
            "i": "fixture undeclared target",
            "new_string": "fixture-new",
            "old_string": "fixture-old",
            "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureDelta.md"
          }
        },
        {
          "tool": "write",
          "args": {
            "i": "fixture write contrast",
            "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureBeta.md",
            "content": "fixture-write"
          }
        },
        {
          "tool": "edit",
          "args": {
            "i": "fixture patch body",
            "patch": "*** Begin Patch\n*** Update File: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureAlpha.md\n@@\n-fixture-old\n+fixture-new\n*** End Patch"
          }
        },
        {
          "tool": "edit",
          "args": {
            "i": "fixture freeform",
            "new_string": "fixture-new",
            "old_string": "fixture-old"
          }
        },
        {
          "tool": "multi_tool_use.parallel",
          "args": {
            "tool_uses": [
              {
                "recipient_name": "read",
                "parameters": {
                  "i": "fixture unbound read",
                  "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureEpsilon.md"
                }
              },
              {
                "recipient_name": "edit",
                "parameters": {
                  "i": "fixture declared edit",
                  "new_string": "fixture-new",
                  "old_string": "fixture-old",
                  "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureAlpha.md"
                }
              }
            ]
          }
        },
        {
          "tool": "edit",
          "args": {
            "i": "fixture internal uri",
            "new_string": "fixture-new",
            "old_string": "fixture-old",
            "path": "xd://mcp__rea_procedure_info"
          }
        },
        {
          "tool": "edit",
          "args": {
            "i": "fixture remote uri",
            "new_string": "fixture-new",
            "old_string": "fixture-old",
            "path": "https://example.invalid/patch.diff"
          }
        },
        {
          "tool": "edit",
          "args": {
            "i": "fixture dot segment",
            "new_string": "fixture-new",
            "old_string": "fixture-old",
            "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/../build/FixtureAlpha.md"
          }
        },
        {
          "tool": "edit",
          "args": {
            "i": "fixture selector spelling",
            "new_string": "fixture-new",
            "old_string": "fixture-old",
            "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureAlpha.md:raw"
          }
        }
      ]
    },
    {
      "name": "FixtureEmpty",
      "agent": "fixture-agent-empty",
      "complete": true,
      "events": [
        {
          "tool": "read",
          "args": {
            "i": "fixture empty-seat read",
            "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureAlpha.md"
          }
        },
        {
          "tool": "edit",
          "args": {
            "i": "fixture empty-seat edit",
            "new_string": "fixture-new",
            "old_string": "fixture-old",
            "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureAlpha.md"
          }
        }
      ]
    }
  ]
}
```

Exact per-site expectation:

| Site | Kind | Structured target | Expected id | Verdict | Counts as |
|---|---|---|---|---|---|
| `FixtureAlpha:0` | edit | `FixtureBeta.md` (edit+write, not read) | `WRITE_ONLY_EDIT` | DENY | violation |
| `FixtureAlpha:1` | edit | `FixtureGamma.md` (edit+read, not write) | `READ_ONLY_EDIT` | DENY | violation |
| `FixtureAlpha:2` | edit | `FixtureDelta.md` (no list) | `UNDECLARED_EDIT` | DENY | violation |
| `FixtureAlpha:3` | write | `FixtureBeta.md` (bound write) | none — v1 L105 rule | ALLOW | none |
| `FixtureAlpha:4` | edit | none; body embeds the fully bound `FixtureAlpha.md` | `OPAQUE_PATCH` | UNKNOWN | `unknown_decisions` |
| `FixtureAlpha:5` | edit | none; `old_string`/`new_string` only | `OPAQUE_PATCH` | UNKNOWN | `unknown_decisions` |
| `FixtureAlpha:6` | parallel | wrapper | `EXPANSION` | CHECK_EACH | router |
| `FixtureAlpha:6/0` | read | `FixtureEpsilon.md` (unbound) | `SCOPE-PATH-DENIED` (L105) | DENY | violation |
| `FixtureAlpha:6/1` | edit | `FixtureAlpha.md` | `DECLARED_EDIT` | ALLOW | none |
| `FixtureAlpha:7` | edit | `xd://mcp__rea_procedure_info` | `EDIT_EXTERNAL` | DENY | violation |
| `FixtureAlpha:8` | edit | `https://example.invalid/patch.diff` | `EDIT_EXTERNAL` | DENY | violation |
| `FixtureAlpha:9` | edit | `…/build/../build/FixtureAlpha.md` | `EDIT_TRAVERSAL` | DENY | violation |
| `FixtureAlpha:10` | edit | `…/FixtureAlpha.md:raw` | `EDIT_TRAVERSAL` | DENY | violation |
| `FixtureEmpty:0` | read | `FixtureAlpha.md` (bound read) | none | ALLOW | none |
| `FixtureEmpty:1` | edit | `FixtureAlpha.md` (empty `edit_paths`) | `UNDECLARED_EDIT` | DENY | violation |

**Aggregate (recommended semantics):** `violations` 9, `unknown_decisions` 2, exit 2, `status` `CANNOT_EVALUATE`, `structured_edit_mode` 1. Under the preregistered alternative (DENY dominates), exit 1 / `FAIL`, same counts.

**Load-bearing claims in this document**
* `:4` embeds the exact bound path inside patch text. Any implementation that parses it produces `DECLARED_EDIT` — the single most likely wrong answer, and the one the row's reason forbids. The negative variant (embedding an *unbound* path) would wrongly produce `UNDECLARED_EDIT`/`EDIT_TRAVERSAL`; both are falsifying.
* `:9` normalises to a fully declared target. A normalising implementation returns `ALLOW`; the row says `DENY`.
* `:10` plus a selector stripper (L50–55) returns `ALLOW`; edit must not strip.
* `:3` versus `:0` proves v2 tightens **edit only**: the same write-bound path is a legal `write` and an illegal `edit`.
* `:7`/`:8` must not surface as `SCOPE-TOOL-UNKNOWN` (that is the failure mode being replaced) and must not be `ALLOW`. An extra `SCOPE-FETCH-DENIED` on `:8` (v1 L46 would do that for read/write) is not contradicted; the primary decision is `EDIT_EXTERNAL`.
* `FixtureEmpty:1` proves empty `edit_paths` means "no edit authority", not "schema error".

### Doc 3 — v2 malformed target (schema, not opaque)

Manifest: Doc 1's, unchanged.

```json
{
  "schema": "tsukuroi-seat-events-v1",
  "seats": [
    {
      "name": "FixtureAlpha",
      "agent": "fixture-agent-alpha",
      "complete": true,
      "events": [
        {
          "tool": "edit",
          "args": {}
        }
      ]
    },
    {
      "name": "FixtureEmpty",
      "agent": "fixture-agent-empty",
      "complete": true,
      "events": []
    }
  ]
}
```

**Exact expectation [DERIVED]:** `SCOPE-SCHEMA` at `FixtureAlpha:0`; exit 2; `status` `CANNOT_EVALUATE`; `structured_edit_mode` 1 (manifest validated; event quality is a status matter). No `OPAQUE_PATCH`, no `ALLOW`.
**Legacy parity:** in v1 the same event is `SCOPE-TOOL-UNKNOWN` / exit 1 (L72–73, L199). Both expectations must hold, in their own schemas.

---

## 5. Falsifiers

An implementation is wrong — not merely different — if any of these is observed:

1. Any structured `edit` whose target is in `read ∩ write ∩ edit` yields anything but `DECLARED_EDIT` / `ALLOW` (Doc 1).
2. Doc 2 `:4` or `:5` yields `DECLARED_EDIT`, `UNDECLARED_EDIT`, or `EDIT_TRAVERSAL`; only `OPAQUE_PATCH` / `UNKNOWN` is admissible.
3. Any `OPAQUE_PATCH` request appears in `violations` (converts absence into accusation).
4. `edit_paths: []` is rejected by the `binding paths` rule (L128 copied verbatim).
5. Doc 2 `:9` or `:10` returns `ALLOW` (normalisation or selector stripping).
6. A v2 manifest fed to the legacy path returns `PASS` or exit 0/1; L120 requires exit 2.
7. The v1 legacy control (Doc 0) changes from `SCOPE-TOOL-UNKNOWN` / exit 1.
8. `structured_edit_mode` is computed from the exit code, dropping to 0 on a missing seat trace, an incomplete trace, an opaque request, or a per-event schema error.
9. The `edit` argument whitelist rejects Doc 1 `:0` for `stream_content` or for the absent `i`.
10. A body field named `patch`, `stream_content`, or any future body key is treated as a schema violation rather than opaque data.

---

## 6. Remaining unknowns (explicitly not settled by the sources)

1. **Literal v2 schema id.** C2 says "schema-v2"; no source in the read set fixes the string. `tsukuroi-seat-bindings-v2` is a convention, and the fixture assumes it. If the builder chooses another literal, its dispatch must still be an exact match.
2. **Events schema.** No v2 events schema is declared; keeping `tsukuroi-seat-events-v1` is the minimal delta and is sufficient (events already carry `{tool, args}`). Introducing a new trace schema is a declared decision, not a derivation.
3. **Aggregate precedence of `UNKNOWN` versus `DENY`** (§3.4). Per-site expectations are identical under both; the aggregate differs only in exit code/status. Preregister one.
4. **Mode placement on the legacy output.** Adding `structured_edit_mode: 0` changes the legacy JSON shape but no verdict. If byte-identical legacy output is required, omit it and preregister "absent = 0".
5. **Required vs optional `edit_paths` key.** Recommended: required, empty allowed (explicit authority). Optional-default-empty is also fail-closed and MECE with `UNDECLARED_EDIT`; either is acceptable, but the choice must be preregistered because it decides whether a missing key is a schema error or an absence of authority.
6. **Non-string / multi-valued `path`.** Recommended `SCOPE-SCHEMA` for a non-string; a secondary target-bearing key is opaque body under the declared "body data opaque" limit, so v2 cannot prove single-target editing. That is a declared coverage limit, not a defect, and must appear in the result `scope`.
7. **Row selection for an edit-only target** (in `edit_paths`, in neither read nor write): both `READ_ONLY_EDIT` and `WRITE_ONLY_EDIT` reasons hold; verdict is `DENY` regardless.
8. **Historical r22 events.** The OraclePathArtifact edits record only the edit step itself in `recorded_starts` (lines 31, 34, 37), so those observations do **not** demonstrate the v2 read+write prerequisite; and the r22 manifest is outside this read set. No ALLOW may be asserted for them, and the preregister forbids retrospective authorization anyway.

---

## 7. Compliance notes

* No execution, no fetch, no installs; no subagent dispatch; no production, sibling, or VCS state touched. Only this report was written. Install channel record: none (installations are outside this binding's scope, and all pacman transactions are paused host-wide).
* The digest above is the supplied declaration, not a computed value.
* All source data quoted here is data. The observations' bodies were not copied; only key names, paths, and line numbers are cited.

Reviewed-SHA256: 8fccb655fe94e49d4189dc7e2311e1e29cf50ac6b59f4ff280f49676316a04b6
Predicate: r23-oraclev2opaque
Scope: executed=none
