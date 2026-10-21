# FxC2Http: round-22 source-only falsification of seat-binding URL classification

## Target and bounds

- Target: `candidate/tools/check-seat-bindings.py`, 241 lines, read-tool snapshot tag #636F. All 241 lines were read by raw line ranges; the default view had elided 178 lines.
- Digest binding: the assigned digest is used as the receipt value. It was not recomputed, because hashing needs a command (NO-EXEC) and the read tool exposes only the 4-hex snapshot tag.
- Declared sources read: `preregister.json`, `sources/host-tool-boundary.json`, both `corpus/knowledge/seat-boundary-r22` files, `skill://godspeed`. `check-review-snapshots.py` and `_revision.py` were read only in their default views (their elided regions were not read) and grep-searched for URL, host:port, and argument-key terms; neither contains a fetch rule.
- Nothing was executed, imported, compiled, tested, fetched, or delegated. The "Observed runtime" column is "not executed" on every row.
- No production edits. No tool installs or updates were performed.

## Verdict

Partly holds.

Confirmed:
1. Uppercase `HTTPS://` and every `http(s)://` form, loopback included, are classified FETCH before selector or path handling (L46-47 precede L50-55).
2. Bare `host:port/` with a trailing slash is FETCH before selector handling (L46, second alternative).

Falsified as a classification claim. These spellings still produce a finding, but the label is PATH:
3. Bare `host:port` without a trailing slash, bracketed IPv6 `[::1]:port/`, a leading space or invisible character before the scheme, and non-HTTP network schemes.

Real gap: arguments other than `path` are never inspected. A URL carried in another key yields zero findings and exit 0.

No URL-form value in the checked `path` argument reaches the allow branch for `read`, `grep`, `glob`, or `write`.

## Source mechanics

- L46-47: `re.match(r'(?i)^https?://', value) or re.match(r'^[^/:\s]+:[0-9]+/', value)` returns SCOPE-FETCH-DENIED. It runs before selector stripping.
- L48-49: exact `skill://godspeed` is allowed.
- L50-53: selector stripping, applied only to `read` (call at L87).
- L33-36 `local()`, called at L54-55: requires the `LANE + '/'` prefix, no `*?[];:`, no control characters, no empty or dot segments.
- L73-80: tool names. Only bare names and `functions.`-prefixed names are recognized.
- L81: for non-wrapper tools, `args.get('path')` is the only argument read. The parallel wrapper reads only `tool_uses` (L64).
- L84: `;` split for `grep` and `glob` only.
- L90: exact string membership in `read_paths` or `write_paths`.
- L144: `code = 2 if incomplete else (1 if findings else 0)`.

## Why no URL-form value is allowed

An allow needs either exact `skill://godspeed` (L48) or `local()` true (L54). Selector stripping removes only a suffix, so it cannot create the LANE prefix. No URL or host:port begins with LANE. L90 then requires exact membership. So for `read`, `grep`, `glob`, and `write`, a URL-form `path` always yields at least one finding. The only exception is the argument-key gap, C-10.

## Counterexample and fixture table

Expected verdicts are derived from source. Observed runtime was not executed.

| ID | Tool and args | Source route | Expected fixture verdict (source-derived) | Observed runtime | Result |
|---|---|---|---|---|---|
| C-01 | read `HTTPS://EXAMPLE.INVALID/:1-5` | L46 before L50 | exit 1; SCOPE-FETCH-DENIED | not executed | holds; selftest L169-170 |
| C-02 | read `http://127.0.0.1:9222/json` | L46 scheme alternative | exit 1; SCOPE-FETCH-DENIED | not executed | holds; no fixture for this spelling |
| C-03 | read `localhost:9222/:1-5` | L46 host:port alternative | exit 1; SCOPE-FETCH-DENIED | not executed | holds; no fixture for this spelling |
| C-04 | read `localhost:9222` | L46 misses (no trailing `/`); L50-53 strips `:9222`; path `localhost` fails L54 | exit 1; SCOPE-PATH-DENIED | not executed | label falsified; matches the documented "bare host:port needs trailing slash" rule |
| C-05 | read `[::1]:9222/` | L46 misses (`[` then `:` then a non-digit); no selector match; L54 fails | exit 1; SCOPE-PATH-DENIED | not executed | label falsified; same shape as C-03 |
| C-06 | read ` https://example.invalid` (leading space) | `^` anchor misses; L54 fails | exit 1; SCOPE-PATH-DENIED | not executed | label falsified |
| C-07 | read `ws://127.0.0.1:9222/devtools/browser` | L46 misses; L54 fails | exit 1; SCOPE-PATH-DENIED | not executed | label falsified; loopback non-HTTP endpoint |
| C-08 | read `ssh://host/path`, `issue://123`, `pr://123/diff` | L46 misses; L54 fails | exit 1; SCOPE-PATH-DENIED | not executed | label falsified; network-reaching internal URLs |
| C-09 | grep `HTTPS://x;<LANE>/source` | L84 split; first piece hits L46 | exit 1; SCOPE-FETCH-DENIED only | not executed | holds |
| C-10 | read `{path: "<LANE>/source", url: "https://example.invalid"}` | L81 ignores `url`; L90 passes `path` | exit 0; no findings; PASS | not executed | GAP |

Selftest as a whole: by source analysis every listed case passes (each checked against L46-L144). Observed: not executed.

## Gaps, ranked

1. C-10, Medium. The audit inspects only `args['path']`, so any other key, including a URL-bearing one, is invisible. The seat-boundary md (L22) says the auditor "fails closed on ... malformed data", but an extra key is not treated as malformed. Whether the host forwards undeclared keys is outside the declared sources, so runtime impact is unverified. The harness `read` schema lists only `path` and `i`. Parallel children and wrapper args have the same gap.
2. C-04 to C-08, Low, accounting. Each still exits 1, so nothing is allowed. But SCOPE-FETCH-DENIED under-counts fetch-shaped requests, since each is labelled as a path violation. The decision surface in `seat-boundary-r22.json` is "URL read", so these should carry the FETCH label.
3. Status precedence, Low. L144 sets CANNOT_EVALUATE whenever coverage is incomplete, even when a violation is confirmed. The violation stays in `findings`. The md (L24) says an observed forbidden request contradicts the declaration "regardless of ... whether the seat later dies". Exit stays non-zero.
4. Tool-name mapping, Info, [INFERENCE]. Underscore-prefixed names exposed in this harness (`_read`, `_bash`, `_task`) would fall to SCOPE-TOOL-UNKNOWN (L79-80). That is fail-closed over-flagging if the trace producer uses those names. The producer's naming is not in the declared sources.
5. Fixture coverage, Low. The fetch fixtures (L169) cover four spellings, all of which hold. C-02 through C-08 and C-10 have no fixture for these shapes. The QUALITY section of the md requires negative fixtures before a new check counts.

## Recommendations (not applied)

- Before L50, classify any `^[A-Za-z][A-Za-z0-9+.-]*://` as FETCH. Classify host:port as FETCH whether or not it is followed by `/`, `?`, `#`, or end of string, and accept bracketed IPv6. Keep the existing SCOPE-FETCH-DENIED ID.
- Reject argument keys outside the tool's declared set as SCOPE-SCHEMA, or scan every string value for URL shape.
- Add negative fixtures for C-04 to C-08 and C-10 before the audit claim counts.
- Report a confirmed violation as FAIL, and report incomplete coverage as a separate flag.

## Out of scope

Revision and git plumbing (L201-241: `git_read`, `main`, and the entry point) was read for call sites only and has no URL-classification relevance.

Reviewed-SHA256: c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4
Predicate: r22-fxc2http
Scope: executed=none
