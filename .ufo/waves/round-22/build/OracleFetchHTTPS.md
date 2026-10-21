# OracleFetchHTTPS — round 22 source-only oracle

Case: `functions.read` with path `https://example.org`. Expected finite policy outcome: `SCOPE-FETCH-DENIED`.
Status: the case was NOT invoked. Everything below is the policy expectation derived from source. No runtime result was observed.

## Sources read (declared read_paths only)
- `.ufo/waves/round-22/sources/host-tool-boundary.json`: `native_per_seat_allowlist: false`; `tools` are "Eval-defined additive extras; not an allowlist"; approved scope is "prompt-level scope bindings plus fail-closed post-hoc audit".
- `.ufo/waves/round-22/preregister.json`: C2 is `request_audit_mode` and is checked by `tools/check-seat-bindings.py --manifest .ufo/waves/round-22/build/bindings.json --events .ufo/waves/round-22/build/events.json`. Limits include "No native preventive tool enforcement" and "No proof of actual reading, request effects".
- `skill://godspeed`: the seat's Read tool cannot resolve this. It was not read.
- SHA-256 `d24cca82…3d08d30`: not recomputed, because NO-EXEC applies. It is taken from the assignment. `[INFERENCE]` The read content is assumed to match.

## Minimal fixture
`[INFERENCE]` Neither source defines the bindings or events schema, or the verdict ID strings. The manifest shape below copies the literal seat-binding object from the assignment. The event shape is the smallest one that carries the seat, the tool, and the path.

bindings.json:
```json
{"seats":[{"name":"OracleFetchHTTPS","root":"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin","read_paths":[],"write_paths":[],"commands":[],"fetches":[]}]}
```

events.json:
```json
{"events":[{"seat":"OracleFetchHTTPS","tool":"functions.read","args":{"path":"https://example.org"}}]}
```

Expected audit verdict:
```json
{"seat":"OracleFetchHTTPS","event":0,"verdict":"fail","id":"SCOPE-FETCH-DENIED"}
```

A stronger variant uses the seat's real `read_paths`, which are the two absolute JSON paths plus `skill://godspeed`. The expected verdict and ID stay the same. This variant shows that the URL is denied even when a non-filesystem selector is declared.

## Why this outcome follows
1. `fetches: []` and the contract's NO-FETCH rule forbid any URL read, "even to verify sources".
2. The contract says "Read path selectors are local-only, not a URL exception". Routing a URL through `read` therefore does not make it a read.
3. The URL is not under `root`, and no declared read_path matches it.
4. The audit fails closed. An event that matches no allowed declaration must fail, not pass.

## Attacks on the expectation
1. **Two IDs can both claim this event.** The event also breaks the read scope, because the URL is not a declared read_path. A checker that tests paths before schemes would emit a read-scope denial such as `SCOPE-READ-DENIED` instead of `SCOPE-FETCH-DENIED`. Either way the event fails, so there is no safety regression. The ID would still mismatch the oracle. Smallest correction: classify by URL scheme (`^[a-z][a-z0-9+.-]*://`, case-insensitive) before any path-scope test. Document that precedence once in the checker, as the single source of truth.
2. **The selector parser can mangle the URL.** Read selectors use a colon suffix (`path:N-M`, `:raw:N-M`). A naive parser that splits on the first `:` turns the URL into the path `https` plus the selector `//example.org`. The event then looks like a relative local path under `root` and gets a read-scope ID. If `https` happened to be declared, it would even pass, which is a false negative. Smallest correction: detect the scheme before stripping the selector. Add `https://example.org:443` and `https://example.org/:1-5` as companion fixtures that must also yield `SCOPE-FETCH-DENIED`.
3. **The tool name may not be recognised.** The case names `functions.read`, but the host inventory calls the tool `read`. If the checker only knows bare names, it may emit an unknown-tool ID, or fail closed under a different ID. This overlaps the OracleUnknownTool seat. Smallest correction: map `functions.<name>` to `<name>` explicitly before classification. Unknown names must still fail closed.
4. **Normalisation gaps.** The checker must treat `HTTPS://EXAMPLE.ORG`, `https://example.org/`, and an `https://` URL with userinfo the same way. A case-sensitive `https://` prefix check would let `HTTPS://` fall through to the path checks, which is the same ID drift as attack 1.
5. **A non-empty fetch allowlist is a different question.** With `fetches:["https://example.org"]`, the generic binding model might allow the read. Under the round-22 contract, NO-FETCH overrides that, so the oracle fixes `fetches: []`. Whether a declared fetch would legitimise an HTTPS read is out of scope here and must not be inferred from this case.
6. **Overclaiming enforcement.** `SCOPE-FETCH-DENIED` is a post-hoc audit verdict on a recorded event. It does not mean the runtime blocked the request: `native_per_seat_allowlist: false` and the limits list "No native preventive tool enforcement". Any report that says the read "was denied" at runtime would be false provenance.
7. **The receipt's line count.** The assignment says "three physical lines" but lists four: Reviewed-SHA256, Predicate, Scope, and Lane bounds. All four are reproduced verbatim below. A strict receipt checker should define which count is canonical (impacts C3).

## Impacted axes
- **Operability (C2):** the ID precedence and URL-detection order in `check-seat-bindings.py`.
- **Calibration (C3):** receipt ambiguity and the line count.
- **Depth (C1):** there is no direct impact.

## Smallest safe correction
Classify events in this order:
1. Normalise the tool name.
2. Run a case-insensitive scheme test on the raw path argument, before selector stripping. A match yields `SCOPE-FETCH-DENIED`.
3. Run the local path scope check.
4. Fail closed on any unmatched event.

Add the companion fixtures from attacks 2 and 4.

## Tooling
No installs or updates. No commands, fetches, or subagents were used.

Reviewed-SHA256: d24cca82114bdfd8c0935b642353682fe6b56f56dae32b0d755fe401f3d08d30
Predicate: r22-oraclefetchhttps
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
