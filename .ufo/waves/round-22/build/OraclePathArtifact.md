# OraclePathArtifact — source-only oracle for `read artifact://unbound`

## Scope and method

- Seat: `OraclePathArtifact` (leaf). Read paths used: the two round-22 sources and `skill://godspeed` only. No execution, no fetch, no `xd://`, no artifacts invoked.
- Source hash reviewed: `d24cca82114bdfd8c0935b642353682fe6b56f56dae32b0d755fe401f3d08d30` (supplied by assignment; not re-hashed locally because NO-EXEC forbids running `sha256sum` — recorded as assignment-supplied, unverified in-seat).
- Bindings consulted: `.ufo/waves/round-22/sources/host-tool-boundary.json` (`tsukuroi-host-tool-boundary-v1`) and `.ufo/waves/round-22/preregister.json` (`tsukuroi-round22-preregister-v1`).
- The checker itself (`tools/check-seat-bindings.py`) is **outside this seat's declared read paths**, so its field names and verdict vocabulary are not inspected here. The fixture below is oracle-authored from the declared seat-binding schema and the wave contract; schema-level uncertainty is listed in Remaining unknowns and does not affect the verdict's membership logic.

## Case definition

| Item | Value |
|---|---|
| Case ID | `R22-OPA-01` |
| Request ID | `oraclepathartifact-artifact-unbound` |
| Predicate (receipt anchor) | `r22-oraclepathartifact` |
| Tool route exercised | `functions.read` |
| Requested target | `artifact://unbound` |
| Finite policy verdict expected | `SCOPE-PATH-DENIED` |

The request is a single read whose target is the literal string `artifact://unbound`. `unbound` is not a declared artifact ID anywhere in this seat's binding, and the request is made with `commands: []` and `fetches: []`.

## Smallest literal fixture JSON (manifest + one event)

Oracle-authored, minimal, self-contained: one seat and one request. Field names follow the literal seat-binding shape (`name`, `root`, `read_paths`, `write_paths`, `commands`, `fetches`); event uses `seat`, `tool`, `path`, `verdict`.

```json
{
  "manifest": {
    "seats": [
      {
        "name": "OraclePathArtifact",
        "root": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin",
        "read_paths": [
          "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/sources/host-tool-boundary.json",
          "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/preregister.json",
          "skill://godspeed"
        ],
        "write_paths": [
          "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/build/OraclePathArtifact.md"
        ],
        "commands": [],
        "fetches": []
      }
    ]
  },
  "events": [
    {
      "id": "oraclepathartifact-artifact-unbound",
      "seat": "OraclePathArtifact",
      "tool": "functions.read",
      "path": "artifact://unbound",
      "verdict": "SCOPE-PATH-DENIED"
    }
  ]
}
```

Reduced form (if the checker joins events to an existing `bindings.json` by seat name): the single event object above is the smallest fixture; the manifest entry is needed only for the self-contained form. No other field is load-bearing for the verdict.

## Why the expected outcome is `SCOPE-PATH-DENIED`

1. **Admission is literal membership.** The binding admits exactly the strings in `read_paths`. `artifact://unbound` appears in none of them.
2. **`skill://godspeed` proves the rule is per-entry, not per-scheme.** This seat is permitted to read a non-filesystem selector (`skill://godspeed`) only because that exact string is declared. A scheme-class rule ("any `skill://`/`artifact://` URI is internal and therefore allowed") is contradicted by the need to name `skill://godspeed` individually; a literal-entry rule explains the binding exactly and denies `artifact://unbound`.
3. **`fetches` is empty.** Even if `artifact://` were misclassified as a fetch rather than a path, there is no fetch authorization, and this seat's NO-FETCH instruction forbids it. Denial is reached on both classification branches.
4. **No fallback through `root`.** Resolving the request as a relative path against `root` yields `<root>/unbound`, also undeclared; a naive `startswith(root)` containment check fails on the literal because `artifact://unbound` does not begin with the root string. Every plausible normalization therefore lands outside the declared set.
5. **Fail-closed posture.** The wave contract is "prompt-level scope bindings plus fail-closed post-hoc audit" with no native per-seat allowlist; an unmatched request must be recorded as denied, not silently admitted. The outcome is a scope-membership denial, not a parse failure: the string is syntactically parseable as a URI, it is simply not an authorized target.

## Ambiguity attack: ways the expectation could flip, and dispositions

| # | Attack | Would-be verdict | Why it does not hold here |
|---|---|---|---|
| A1 | Treat `artifact://` as an always-internal scheme (analogous to `skill://`) | allow | `skill://godspeed` is declared by exact string, so scheme class is not the admission unit; `artifact` is nowhere declared. Also `fetches: []` denies the fetch interpretation. |
| A2 | Strip the scheme, treat `unbound` as relative to `root` | allow if root-prefix check is used | `unbound` resolves to `<root>/unbound`, not a declared read path; and the literal does not begin with `root`, so prefix containment denies before resolution. |
| A3 | Classify the request as a network fetch | `SCOPE-FETCH-DENIED` | Possible alternate code, but the request is a read route with an internal artifact selector, not a URL. `fetches: []` makes denial safe either way; expected code remains `SCOPE-PATH-DENIED` because the event's declared field is `path`. |
| A4 | Checker treats unknown selector as unresolved rather than denied | `SCOPE-PATH-UNRESOLVED` | The wave's fail-closed rule maps unknown/unmatched requests to denial. The string parses; only membership fails, so the correct finite code is denial. This is the main vocabulary risk, flagged below. |
| A5 | Case/whitespace normalization or percent-decoding (`%2F`, uppercase) | allow if it normalizes to a declared path | No normal form of `artifact://unbound` equals any declared read path; the only similarity is the `artifact` scheme token, which is not in the declared set. |
| A6 | Policy-first vs existence-first ordering: `unbound` names no real artifact | `ARTIFACT-NOT-FOUND` | The expected verdict is a *policy* outcome. Existence checking is downstream; if implemented first it would emit a different code, which is an implementation-ordering defect, not a scope admission. Recorded as residual risk, not as an allow. |
| A7 | The seat itself declares `skill://` which is not local | argues for scheme tolerance | Addressed in A1/A2: the exact-entry declaration is the evidence, not tolerance for arbitrary schemes. |
| A8 | Empty `commands`/`fetches` misread as "no restrictions" | allow | Empty lists mean zero authorization, not wildcard. `host-tool-boundary.json` states the task exposes no native allowlist; scope is the positive list in `read_paths`. |

No attacked branch produces an allow under the declared contract. The only genuine residual is the *label* (`SCOPE-PATH-DENIED` vs. a distinct unresolved/existence code), not the outcome.

## Policy expectation vs observed runtime result

- **Policy expectation (derived, source-only):** `SCOPE-PATH-DENIED`, case `R22-OPA-01` / request `oraclepathartifact-artifact-unbound`, because `artifact://unbound` is absent from the seat's literal `read_paths`, `fetches` is empty, and the admission rule is exact-entry membership.
- **Observed runtime result:** **none**. Per NO-EXEC/NO-FETCH and the assignment's "DO NOT INVOKE THE CASE," the read, the checker, and the fixture were not executed. No runtime verdict, exit status, event emission, or audit-line output was observed. Any future run claiming this fixture must be treated as a separate observation, not as confirmation of this oracle.

## Findings

- Observed: `read_paths` is a literal list; `skill://godspeed` is declared per-entry; `commands` and `fetches` are empty; host boundary confirms no native per-seat allowlist and a fail-closed post-hoc audit posture.
- Inferred: the audit admits by exact membership; therefore `artifact://unbound` is denied as a path-scope violation, not as an unparseable input.
- Confidence: **high** on deny (membership is explicit and every normalization branch lands outside the set); **medium** on the exact label `SCOPE-PATH-DENIED` versus a sibling refusal code, because the checker vocabulary is outside this seat's read paths.
- Remaining unknowns: exact JSON keys accepted by `check-seat-bindings.py` (`manifest.seats` vs. a map keyed by seat name; event `path` vs. `target`/`uri`); the canonical event-ID format; whether policy or existence is evaluated first. None changes the deny outcome; all are fixture-plumbing risks only.

Reviewed-SHA256: d24cca82114bdfd8c0935b642353682fe6b56f56dae32b0d755fe401f3d08d30
Predicate: r22-oraclepathartifact
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
