# FxC2XD — internal-URI read/write classification and side effects

Seat: `TsukuroiR22.FxC2XD-2` (leaf). Target: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/candidate/tools/check-seat-bindings.py`, seat-declared SHA256 `c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4` (not recomputed: NO-EXEC). Supporting declared reads: `round-22/preregister.json`, `round-22/sources/host-tool-boundary.json`, `round-22/candidate/corpus/knowledge/seat-boundary-r22.{json,md}`, `round-22/candidate/tools/_revision.py`, `round-22/candidate/tools/check-review-snapshots.py`, `skill://godspeed`. No command, test, import, hash, or fixture was run; no runtime verdict is reported.

## Claim attacked

A recorded request whose path is an internal URI — `read xd://…` vs `write xd://…`, plus `artifact://`, `proc://`, `agent://` in either direction — must not (a) be classified clean by the auditor (a clean verdict would hide a side-effecting request) and (b) execute inside the auditor. A counterexample is any event spelling that yields zero findings while naming one of those URIs, or any code path where such a spelling reaches a host effect.

## Verdict

HOLDS as a post-hoc, string-level classification invariant [observed from source; high confidence]. No clean-classification counterexample exists in this file. The stronger reading — “no side effect can occur” — does **not** hold and is not claimed: the audit runs after dispatch (`SCOPE` line 17: “Recorded request spellings only; not runtime prevention … effect proof”), and the target’s own runtime is **not** zero-execution (it runs read-only git). Detection is not prevention; `sources/host-tool-boundary.json` records `native_per_seat_allowlist: false` and only prompt-level bindings plus post-hoc audit.

## Source facts (observed, with anchors)

1. **`classify` is pure.** Lines 59–92 contain no `subprocess`, filesystem open, or binding mutation. It strips a `functions.` prefix (72–73), hard-denies `bash`/`eval`/`task` (74–75) and fetch tools (76–77), rejects every other tool name (78–79), reads only `args['path']` (80–83), and returns finding ids. Its docstring “never execute the requested operation” is accurate for this function.
2. **`local()` is scheme-blind and colon-hostile.** Lines 33–36 require `path.startswith(LANE + '/')`, reject `\`, control categories `Cc/Cf/Cs/Zl/Zp`, reject any of `*?[];:`, and reject empty/`.`/`..` components. `LANE` is the absolute lane root (line 16). Every internal URI contains `:` and none starts with `LANE + '/'`, so `local()` is false for all of them.
3. **`requested_path` cannot strip a scheme away.** Lines 43–56: fetch spellings return early (46–47), the single literal `skill://godspeed` returns early (48–49), then a **read-only** selector strip runs (50–53) before the `local()` denial (54–55). The fullmatch is `(.+?)(?::(?:raw|img|conflicts|[0-9]+(?:[-+][0-9]*)?|-[0-9]+|[0-9,-]+))*`. For `xd://`, `artifact://`, `proc://`, `agent://`, `local://`, `ssh://`, `issue://`, `pr://`, `mcp://`, `history://` and `skill://` the remainder after the scheme colon begins `//` (or a non-token host), never a selector token. The minimum-match prefix therefore remains the whole scheme string, which fails `local()`. Suffixed forms such as `artifact://a:1-5` strip only the numeric tail and still leave `artifact://a`, which fails `local()`.
4. **Bindings cannot whitelist an internal URI.** In `evaluate`, the binding loop lines 111–114 accepts a non-local path only when `field == 'read_paths' and p == 'skill://godspeed'`; every other non-local entry in either `read_paths` or `write_paths` raises `binding paths` → `SCOPE-SCHEMA`, exit 2. `skill://godspeed` cannot enter `write_paths` at all.
5. **Write is checked strictly more tightly than read.** `classify` calls `requested_path(..., selector=tool == 'read')` (line 87): writes skip selector stripping and match `write_paths`; reads match `read_paths` after stripping. `write skill://godspeed` clears `requested_path` (48–49) but fails membership (90–91), so it is still `SCOPE-PATH-DENIED`. No write path is ever more permissive than the read predicate.
6. **The auditor’s only effect surface is read-only git.** `git_read` runs `git --no-pager -C ROOT show <rev>:<path>` and, on failure, `git --literal-pathspecs … ls-tree -z <rev> -- <path>`; `_revision.bind` runs `check-ref-format`, `rev-parse`, `cat-file -t`, `merge-base --is-ancestor` (module docstring: “only reads … never writes a ref, the index or the worktree”). `_revision.clean_env` sets `GIT_OPTIONAL_LOCKS=0`, `GIT_PAGER=cat`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`; there is no fetch/ls-remote verb. The revision is hex-bound (`REV.fullmatch`) and CLI manifest/event paths are placed after `rev:` or after `--`, so trace-supplied tool/path strings never reach an argv. `sys.dont_write_bytecode = True` (line 12) precedes `import _revision` (line 13), avoiding a `__pycache__` write in `tools/`.
7. **Wrapper recursion preserves the guard.** `multi_tool_use.parallel`/`parallel` recurse with `depth + 1` (63–71) and `depth > 8` raises (60–61), which `evaluate` maps to `SCOPE-SCHEMA` exit 2. `grep`/`glob` split on `;` (84) but `local()` already rejects `;`, so no bound path can smuggle a second component.

## Attack attempts and outcomes (static)

| Attempt | Source path | Outcome |
|---|---|---|
| A. Strip a scheme URI down to a bound local path with a `read` selector (`xd://tool:1-5`, `artifact://a:raw`, `proc://1:12`) | 50–53 → 54–55 | Fails: tail after `:` begins `//`; no selector decomposition; whole string fails `local()`. Denied. |
| B. Whitelist `xd://`/`artifact://`/`proc://`/`agent://` in the manifest | 111–114 | Fails: raises `binding paths`, exit 2 `SCOPE-SCHEMA`, before any event is graded. Only `skill://godspeed` read is admitted. |
| C. Smuggle the effect through another tool/alias/argument shape (`functions.write`, wrapper child, extra keys, `grep x; uri`) | 63–73, 80–84 | Fails: alias strip, recursion, and `;` split all re-enter the same path predicate; a missing/non-string path raises → `SCOPE-SCHEMA`; unknown tools return `SCOPE-TOOL-UNKNOWN`. |
| D. Make the auditor itself dispatch the URI | `classify`/`evaluate` | Fails: both are pure string/JSON code; git is invoked only from `main`/`git_read` on validated CLI inputs, with read-only verbs. |
| E. URI-shaped CLI `--manifest`/`--events` (e.g. `xd://x`) | `repo_path` (39–40), `git_read` | Not a URI read: `repo_path` permits `:`, but git receives `rev:xd://x` / `-- xd://x` as a literal repo path (absent → `SCOPE-READ`/`SCOPE-BINDINGS-MISSING`), never a fetch or dispatch. |

No row yields zero findings; no row reaches an effect primitive with URI semantics.

## Expected fixture verdicts (source-derived) vs observed runtime

Expected values below are derived by tracing the code, not by executing `--selftest`. **Observed runtime for every row: none** — this seat executed nothing. The shipped fixture covers only the two marked rows; the rest are derived, so they must not be reported as fixture observations.

| Recorded event (binding: report-only write, `skill://godspeed` + locals read) | Expected exit | Expected finding |
|---|---|---|
| `read xd://tool` (**shipped case**) | 1 | `SCOPE-PATH-DENIED` |
| `read artifact://a` (**shipped case**) | 1 | `SCOPE-PATH-DENIED` |
| `read artifact://a:1-5` | 1 | `SCOPE-PATH-DENIED` (scheme prefix survives strip) |
| `read proc://123` | 1 | `SCOPE-PATH-DENIED` |
| `read agent://all` | 1 | `SCOPE-PATH-DENIED` |
| `read local://x.md`, `read ssh://h/p`, `read issue://12`, `read pr://12/diff`, `read mcp://uri`, `read history://id` | 1 | `SCOPE-PATH-DENIED` |
| `read skill://godspeed` (bound) | 0 | none (only permitted non-local spelling; read-only) |
| `read skill://other` (unbound) | 1 | `SCOPE-PATH-DENIED` |
| `write xd://bash`, `write proc://bg_1`, `write agent://all`, `write artifact://a`, `write local://x.md` | 1 | `SCOPE-PATH-DENIED` |
| `write skill://godspeed` | 1 | `SCOPE-PATH-DENIED` via membership (90–91), not via `requested_path` |
| `functions.write` with `xd://…` | 1 | `SCOPE-PATH-DENIED` after alias strip |
| `multi_tool_use.parallel` child `write proc://…` | 1 | `SCOPE-PATH-DENIED` (site is the outer event index) |
| Same URI event in a seat with `complete: false` | 2 | `SCOPE-TRACE-INCOMPLETE` plus the URI finding |
| Binding `write_paths` contains `xd://x` **or** `read_paths` contains `artifact://a` | 2 | `SCOPE-SCHEMA` (`binding paths`) |
| Binding `read_paths` is exactly `['skill://godspeed']` | 0 with no events | binding accepted (only non-local read literal) |

## Bounded reason it holds

The guard is not URI-semantic, and does not need to be: `local()` admits only absolute paths under `LANE` with no `:`, and the manifest may add exactly one non-local read literal (`skill://godspeed`). All named internal URI spellings therefore land in `SCOPE-PATH-DENIED` for both `read` and `write`, whether or not the harness treats the specific channel as harmless (a `read proc://` status page is denied too — over-detection, not a hole). Selector stripping occurs only for `read`, only strips a strict alternation that cannot match `//` after the scheme colon, and occurs before the same `local()` test. `classify`/`evaluate` never dispatch; the only subprocesses are constant read-only git verbs whose argv is bounded by a hex revision and `--`-separated or `rev:`-prefixed paths.

## Limitations (not counterexamples, but claim-bounding)

1. **Post-hoc only.** A seat could execute a side-effecting `write proc://`/`write agent://`/`write xd://<tool>` during dispatch; this tool detects the recorded request afterward. It never prevented it. Do not upgrade any verdict to “no side effects occurred.”
2. **No channel attribution.** Every named URI and every out-of-scope local path share `SCOPE-PATH-DENIED`; the finding does not distinguish stdin injection (`proc://`), peer messages (`agent://`), MCP tool invocation (`xd://`), or a typo path. Detection granularity is exit code + generic id.
3. **Trace trust.** A seat with `complete: true` and zero events returns PASS/exit 0 (fixture `empty-trace`). The invariant covers recorded requests only; missing/incomplete traces exit 2 by design.
4. **Selector-strip DoS surface (static inference, untested).** Line 51 has an ambiguous alternation (`[0-9]+(?:[-+][0-9]*)?` and `[0-9,-]+` both match `1-2`) inside a `*` and a lazy `(.+?)`. A `read` event path built from many `:1-2` tokens and a failing tail can force exponential backtracking before `local()` is reached. `grep`/`glob` skip the strip; bound paths cannot contain `:`. This burns CPU; it does not execute the URI. Untested under NO-EXEC.
5. **Uncaught recursion.** Deeply nested events JSON raises `RecursionError`, absent from the `except (ValueError, TypeError, KeyError, AttributeError, UnicodeError)` tuple; the run crashes non-zero instead of printing `CANNOT_EVALUATE`. Fail-closed in status, unstructured in output.
6. **Minor id drift.** `read localhost:9222` (no trailing slash) fails the fetch regex’s `…/` requirement and is labelled `SCOPE-PATH-DENIED` rather than `SCOPE-FETCH-DENIED`; still exit 1.
7. **Out-of-set effect channels.** Per the host tool descriptions, a **bound local** `read` can spawn decoders (archive/SQLite/video `ffmpeg`, SVG rasterization). `local()` is string-only and cannot see file type, and the target’s `SCOPE` explicitly disclaims “symlink/effect proof.” This blocks any broader “read is effect-free” claim but is outside the named URI set.
8. **Unresolved:** whether the live adapter that emits `tsukuroi-seat-events-v1` ever records internal-URI `write` calls in this `{tool, args.path}` shape is not visible in this file; and whether `ROOT = parents[1]` resolves to the same git repo as `LANE` for the candidate directory (git `-C` behavior) was not verified without execution.

## What may and may not be claimed

May claim: for a complete recorded trace, every `read`/`write` event naming `xd://`, `artifact://`, `proc://`, or `agent://` (and the other scheme URLs) yields a violation, so the audit cannot return PASS while such a request is recorded; `classify` executes nothing.

Must not claim: preventive enforcement; absence of side effects; a read/write URI-semantic distinction; per-channel evidence; or that the target runs no processes at all (it runs read-only git).

Reviewed-SHA256: c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4
Predicate: r22-fxc2xd
Scope: executed=none
