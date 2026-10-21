# FxC2Wildcard — source-only falsification report (predicate r22-fxc2wildcard)

Round: tsukuroi round-22, baseline 894d1e20fb4939b0cc4fadf722c46d1429f257d2.
Reviewed artifact: `.ufo/waves/round-22/candidate/tools/check-seat-bindings.py`, 241 lines, ticket-asserted SHA256 `c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4`. Digest NOT independently verified: this seat is NO-EXEC and no hashing command was run; identity basis is the ticket assertion plus a complete three-range source read (lines 1–103, 100–203, 204–241; no gap, overlapping anchors).

## Predicate under attack

"Unbound wildcards and directory descendants reject; no scope expansion."

## Verdict

Predicate HOLDS at the recorded-request-spelling audit layer. Every concrete expansion vector visible in the source fails closed. No counterexample found. This is a post-hoc spelling auditor, explicitly not preventive enforcement (see Enforcement caveat).

## How the checker implements the predicate (line-anchored)

- Wildcards are banned as characters, never evaluated as patterns. `local()` (lines ~29–33) requires every binding entry and every requested base path to contain none of `* ? [ ] ; :`, no backslash, no control/format/surrogate/separator Unicode (Cc/Cf/Cs/Zl/Zp via `controls()`), to start with the exact constant `LANE + '/'` (trailing slash blocks `LANE-sibling` prefix confusion), and to have no empty, `.`, or `..` component. Binding validation (`evaluate`, ~lines 92–101) re-runs `local()` per entry with uniqueness; a wildcard in a binding raises `ValueError` → `SCOPE-SCHEMA`, exit 2 CANNOT_EVALUATE. A wildcard in a request → `SCOPE-PATH-DENIED`, exit 1. There is no `fnmatch`, no glob evaluator, no `Path.match`/`rglob` anywhere in the file (`PurePosixPath` is imported and never used).
- Directory descendants reject by exact string membership. `classify` (~lines 73–76) admits a request only when the (selector-stripped) spelling equals a literal entry of that seat's `read_paths` (or `write_paths` for `write`): `elif path not in binding['write_paths' if tool == 'write' else 'read_paths']`. No prefix matching, no `is_dir`, no recursive semantics. Descendant spellings such as `<bound>/child` are unequal → `SCOPE-PATH-DENIED`.
- No scope expansion mechanism exists:
  - No globbing, no prefix matching, no case folding, no Unicode normalization, no symlink resolution, no URL/percent decoding. Aliased spellings (`x/../source`, `./source`, `//`, trailing `/`, `%2e`, NFD forms) can only fail validation or membership — fail closed.
  - Read selector stripping (`requested_path`, line ~46 regex) removes only documented suffix tokens (`raw|img|conflicts|[0-9]+([-+][0-9]*)?|-[0-9]+|[0-9,-]+`); the stripped base must still pass `local()` and exact membership. The alternation cannot inject `/`, `.`, `..`, or wildcard characters.
  - `multi_tool_use.parallel` children are fully classified recursively with a depth cap of 8; deeper or malformed wrappers raise → `SCOPE-SCHEMA` (fail closed). `functions.` prefix stripped once; a second strip is impossible (`functions.functions.read` → TOOL-UNKNOWN).
  - Unknown or non-string tools → `SCOPE-TOOL-UNKNOWN`; `bash`/`eval`/`task` → `SCOPE-EXEC-DENIED`; `web_search`/`browser`/`browser.*` → `SCOPE-FETCH-DENIED`; anything else unknown → TOOL-UNKNOWN. Fail closed in every direction.
  - HTTP/HTTPS and `host:port/` spellings are denied pre-strip as `SCOPE-FETCH-DENIED`; other URI schemes (`xd://`, `artifact://`, `skill://evil`) fall through `local()` and reject.
  - The `skill://godspeed` carve-out is exact-string, read_paths-only (binding validation exempts it solely for `read_paths`), and still requires membership in that seat's `read_paths` at request time — double-gated. Write-side has no carve-out.
  - Manifest hardening: duplicate JSON keys (`object_pairs_hook=unique`), duplicate seats, unknown trace seat names, duplicate agents, non-bool `complete`, non-empty `commands`/`fetches`, `root != LANE`, and non-list/empty/duplicate path lists all raise → `SCOPE-SCHEMA`, whole audit CANNOT_EVALUATE. Missing trace → `SCOPE-TRACE-MISSING`, incomplete → `SCOPE-TRACE-INCOMPLETE`, exit 2 — never silently clean.

## Attack vectors attempted — all bounded

| Vector | Outcome |
|---|---|
| fnmatch-style `*` crossing `/` (descendant expansion via glob) | Impossible: no glob evaluator exists; `*` is a banned character in bindings and requests |
| Right-anchored `PurePath.match` suffix matching | Not applicable: `PurePosixPath` unused; no `.match()` call |
| Prefix expansion via `startswith` on seat paths | `startswith` used only for the fixed `LANE + '/'` constant; seat paths use exact equality |
| `..` / `//` / trailing-slash aliasing of a bound path | Components `''`, `.`, `..` banned; no normalization performed; alias spellings cannot equal a bound spelling |
| Selector-suffix smuggling (`:raw`, `:1-5`, `:,`) hiding traversal | Suffix grammar admits only raw/img/conflicts/numeric tokens; base still exact-membership-checked |
| Semicolon multi-path (`grep`/`glob` path lists) | Each component independently validated; `;` banned in bindings so no bound spelling contains a separator |
| `skill://` carve-out abuse (`skill://godspeed/../x`, write-side, selector suffix) | Exact-string gate; write side has no carve-out; `skill://godspeed:1-5` rejects (fail-closed strictness) |
| Wrapper/routing evasion (parallel children, `functions.` prefix, capitalized tools) | Recursive classification, single prefix strip, unknown names fail closed |
| Hostile manifest (dup keys/seats/agents, nonempty commands/fetches, wildcard binding) | `SCOPE-SCHEMA`, exit 2 CANNOT_EVALUATE |
| Fetch spellings on read (`https://`, `HTTPS://…/:1-5`, `localhost:9222/`) | Pre-strip fetch regex → `SCOPE-FETCH-DENIED` |

## Expected fixture verdicts (static derivation — none executed)

| Fixture (LANE = `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`) | Expected verdict |
|---|---|
| read `LANE/x/**` (any wildcard spelling) | `SCOPE-PATH-DENIED`, exit 1 |
| binding `read_paths: ["LANE/**/*.md"]` | `SCOPE-SCHEMA`, exit 2 CANNOT_EVALUATE |
| read `<bound-dir>/child` | `SCOPE-PATH-DENIED`, exit 1 |
| write `<report>/child`; write `LANE/production` | `SCOPE-PATH-DENIED`, exit 1 |
| read `<bound>:1-5:raw` (base bound) | allowed, exit 0 |
| grep `path: <bound>;/outside` | `SCOPE-PATH-DENIED`, exit 1 |
| parallel child `functions.bash` / unbound `functions.read` descendant | `SCOPE-EXEC-DENIED` / `SCOPE-PATH-DENIED` |
| read `skill://godspeed` (URI bound) / `skill://godspeed:1-5` | allowed / `SCOPE-PATH-DENIED` |
| read `xd://tool`, `artifact://a`, `LANE/../sibling/file`, `LANE/x/../source`, `LANE/./source`, `source` | `SCOPE-PATH-DENIED`, exit 1 |
| bash / eval / task; web_search / browser / browser.navigate; edit | EXEC-DENIED / FETCH-DENIED / `SCOPE-TOOL-UNKNOWN`, exit 1 |
| trace missing / incomplete / duplicate seat / unknown seat / duplicate JSON key / nonempty fetch allowlist | TRACE-MISSING, TRACE-INCOMPLETE, SCHEMA×4, exit 2 |

Observed runtime for every row above: **none**. No execution was performed (receipt records executed=none); the NO-EXEC seat forbids running the tool, its selftest, or any mutated input. The tool's own embedded `selftest()` table (lines ~133–186) encodes the same expectations verbatim (`LANE + '/**'`, `src + '/child'`, `report + '/child'`, `LANE + '/production'`, fetch and parallel cases); agreement is a static source observation, not an observed run.

## Residual risks and verification gaps

- Digest and runtime both unverified by construction (no execution permitted); all verdicts are source-derived expectations.
- Spelling-only layer by declared scope (SCOPE constant, line ~18: "not runtime prevention, symlink/effect proof, reading proof or universal trace completeness"). A bound directory's runtime listing effect (child-name exposure through reading the bound directory path itself) is invisible to exact-spelling membership — declared non-goal, not a counterexample to the descendant-spelling predicate.
- Only the `path` argument is audited; `grep`/`glob` pattern contents and other args are outside the scope surface.
- Runtime read-selector dialects beyond the strip grammar (e.g., time selectors like `:1h5m42s`) would false-positive `SCOPE-PATH-DENIED` — conservative direction only, no expansion.
- The auditor's own CLI inputs use the weaker `repo_path` (does not ban `*?[];:`); bounded to reading its manifest/events from the bound landed revision via `git show` — not a seat-scope surface; git pathspec semantics for such spellings unresolved without execution and any misread yields `SCOPE-READ` CANNOT_EVALUATE, not a clean pass.
- Minor non-defects: `PurePosixPath` import is dead; `Path` used only for `ROOT`.

## Enforcement caveat

Per `.ufo/waves/round-22/sources/host-tool-boundary.json` (`native_per_seat_allowlist: false`) and the preregister C2 host decision, this checker is fail-closed post-hoc detection over recorded request spellings. The predicate holds at that layer only; no preventive runtime enforcement is claimed or implied.

Saturation: all 241 lines were read; the expansion-surface inventory above covers every matching, validation, wrapper, and error path in the file. The attack is bounded by the no-execution constraint and by the recorded-spelling model the tool itself declares.
