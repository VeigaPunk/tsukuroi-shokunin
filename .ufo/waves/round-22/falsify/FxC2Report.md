# FxC2Report — write-target containment under the post-hoc request audit

Target (only file attacked): `.ufo/waves/round-22/candidate/tools/check-seat-bindings.py`.
Mode: source-only falsification. No execution, no import, no mutation, no network.

## Axes

- A1 positive containment: a write whose spelling equals the declared report path is accepted.
- A2 same-prefix extra containment: `report + suffix` is denied.
- A3 parent-sibling containment: sibling spellings in the report's parent directory (and lane-root siblings) are denied.
- A4 fixture fidelity: the selftest's encoded expectations for those four cases equal the behavior the source actually implements.
- A5 fail-closed behavior: malformed, non-string, aliased, or duplicate-key inputs cannot fall through to acceptance.

## Claim under test

"Write exact report allowed, same prefix extra and parent siblings denied."

Read narrowly, the claim is about `classify(tool='write', args={'path': p}, binding)` where `binding['write_paths']` contains the report and nothing else.

## Mechanism (observed in source)

Acceptance for a `write` event with path `p` is decided by exactly two gates, in this order:

1. `requested_path(p, selector=tool == 'read')` (lines 43-56). For `write`, `selector` is False (line 87), so the selector-stripping regex at line 51 is never applied to a write path.
   - line 46: `http(s)://` or `host:port/` spellings return `SCOPE-FETCH-DENIED`;
   - lines 48-49: the literal `skill://godspeed` returns an early non-denial, but the later membership test still runs;
   - line 54: anything failing `local(p)` returns `SCOPE-PATH-DENIED`.
2. line 90: `path not in binding['write_paths' if tool == 'write' else 'read_paths']` appends `SCOPE-PATH-DENIED`.

`local(p)` (lines 33-36) requires: non-empty string, literal prefix `LANE + '/'` (line 34, note the trailing slash), no backslash, no character in Cc/Cf/Cs/Zl/Zp (`controls`, lines 29-30), no `* ? [ ] ; :`, and no path segment equal to `''`, `'.'`, or `'..'` after the leading slash.

Binding validation (line 113) requires every `write_paths` entry to satisfy `local(p)` and to be duplicate-free. So `skill://godspeed` can never appear in `write_paths`: a manifest that tries it is rejected wholesale as `SCOPE-SCHEMA` (exit 2), not silently accepted.

There is no normalization step anywhere on the request path: grep over the file finds `resolve()` only on `__file__` (line 15) and no `normpath`, `realpath`, `casefold`, `normalize`, or `os.path` use. `PurePosixPath` is imported (line 7) but unused.

## Falsification attempt (all source-visible, none executed)

I attacked the containment claim with the following spellings against the fixture binding (`write_paths = [LANE + '/report']`, line 156). In every case the source indicates denial; none reaches acceptance.

- N1 same-prefix extras: `LANE + '/report.extra'`, `LANE + '/report/child'`, `LANE + '/reports'`, `LANE + '/report '` (trailing space). All pass `local`, all miss membership at line 90 → `SCOPE-PATH-DENIED`.
- N2 parent traversal and dot segments: `LANE + '/x/../report'`, `LANE + '/./report'`, `LANE + '/report/.'`, `LANE + '/report/..'`, `LANE + '//report'`, `LANE + '/report/'`. All fail the segment test at line 36 (segments `'..'`, `'.'`, or `''`) → denied before membership.
- N3 sibling lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin-evil/report`. `startswith(LANE + '/')` is false because the character after the lane name is `-`, not `/`, so the classic bare-`startswith` prefix bug is absent → denied.
- N4 skill alias as a write: `skill://godspeed`. Line 48 returns a non-denial, but line 90 denies because `write_paths` cannot legally contain it (line 113) → `SCOPE-PATH-DENIED`. A manifest that declares it is `SCOPE-SCHEMA`, exit 2.
- N5 fetch spellings on a write: `https://…`, `HTTPS://…`, `http://127.0.0.1/`, `localhost:9222/`. Denied at line 46 → `SCOPE-FETCH-DENIED`, exit 1.
- N6 confusables: NBSP/zero-width/bidi characters are rejected by `controls` when in Cc/Cf/Cs/Zl/Zp; a zero-width-space suffix is a different string and misses membership anyway; a `Zs` character passes `local` but cannot equal the declared path → denied.
- N7 tool aliasing: `functions.write` normalizes to `write` (line 75-76) and takes the identical membership path; `functions.functions.write` falls out as `SCOPE-TOOL-UNKNOWN` (exit 1), i.e. denied rather than widened.
- N8 read-selector smuggling: `report:raw` / `report:1-5` on a write. Selector stripping is read-only, and `:` fails `local` → denied. There is no path by which read-style selector tolerance widens a write.
- N9 malformed shapes: non-string or empty `path` raises `ValueError` at line 82-83; a non-dict event or bad tool raises at line 61-62; duplicate JSON keys raise in `unique` (lines 20-25). All are caught by `evaluate` and downgraded to `SCOPE-SCHEMA`, exit 2 — fail closed.
- N10 cross-seat: `bound` dedupes seat names only (line 105, 115); there is no disjointness check over write paths across seats. This is real, but it requires a manifest that itself declares the overlapping spelling, so it is a manifest-trust boundary rather than an escape from the fixture claim (see R1/R5).

Result: no concrete source-visible counterexample. The claim holds for `write` with the bounded argument that acceptance is *byte equality with a declared write path after a local-spelling gate*, and no accepted string can differ from the declared report.

## Expected fixture verdict (as encoded, read from source)

`report = LANE + '/report'`; the binding at line 156 validates under lines 106-113 (name `A` matches the name regex, root equals `LANE`, `commands`/`fetches` are `[]`, read paths local plus the exact skill URI, write path local and unique). Therefore each fixture row reaches classification rather than schema failure.

| fixture | line | recorded write path | expected exit | expected finding | source-indicated result |
|---|---|---|---|---|---|
| `write-exact` | 166 | `LANE + '/report'` | 0 | none | accept; `local` true, membership hit |
| `write-…report.extra` | 175-176 | `LANE + '/report.extra'` | 1 | `SCOPE-PATH-DENIED` | deny at membership (line 90) |
| `write-…report/child` | 175-176 | `LANE + '/report/child'` | 1 | `SCOPE-PATH-DENIED` | deny at membership (line 90) |
| `write-…/production` | 175-176 | `LANE + '/production'` | 1 | `SCOPE-PATH-DENIED` | deny at membership (line 90) |

Notable fixture property: all three negative write rows pass `local` and are stopped by the membership test itself, so the fixtures exercise the claim's actual mechanism rather than an earlier prefix rejection. The same-prefix read rows at line 173-174 exercise the same two gates for `read`.

The selftest's pass rule (exit equals expected and the expected finding id is present) is satisfied for these four rows by the above. I did not certify the remaining selftest rows; they are outside this predicate.

## Observed runtime

None. No process was started: no `python3`, no `--selftest`, no `sha256sum`. The digest in the receipt is the declared pin supplied with the assignment, not a value recomputed here. `.ufo/waves/round-22/build/bindings.json` and `.ufo/waves/round-22/build/events.json` are outside this seat's declared read paths, so the actual declared write scope and recorded event spellings for round 22 were not inspected. Expected and observed are therefore not the same kind of statement: the table above is a source-derived expectation, and the runtime observation is absent by construction.

## Bounded verdict

PREDICATE HOLDS as a spelling-containment rule, with high static confidence inside the write branch: the exact declared report path is the only accepted write spelling, and every same-prefix extra or parent-sibling spelling is rejected either by the `local` segment/character test or by exact string membership. No normalization, aliasing, or selector widening exists that could make a longer or sibling spelling compare equal to the declared path.

## Residual boundaries (boundaries, not counterexamples under this fixture)

- R1 Manifest trust: the checker has no semantic notion of "the report". Acceptance is equality with whatever `write_paths` the frozen manifest declares; a manifest that declares an extra spelling (including a directory spelling without a trailing slash) makes that exact spelling acceptable. The checker cannot detect an over-broad binding beyond locality and uniqueness.
- R2 Cross-seat overlap: no disjointness check over write paths across seats, so two seats declaring the same path can each write it. Requires a defective manifest.
- R3 Spelling-only, explicitly scoped out by line 17: symlink, hardlink, overlay, or mount aliasing, and any write-tool-side path interpretation, are not modeled. A declared path that is a symlink to a sibling is accepted under its declared spelling.
- R4 Recorder trust: classification uses the recorded `event.tool` label. A write recorded under `read` is judged against `read_paths` only; the audit cannot reconstruct the operation from its arguments alone.
- R5 Manifest-absent short circuit: `evaluate(None, events)` returns exit 1 with only `SCOPE-BINDINGS-MISSING` and `request_audit_mode: 0` (line 99) without examining any event, so recorded requests are unclassified in that state. Headline stays FAIL, but the events are not scanned.
- R6 Only `path` is inspected; `content` and any other write arguments are ignored. Whether any other argument can redirect a write is not established by the sources available to this seat.
- R7 Minor precision nits, none of which allow a write: a double-prefixed `functions.functions.bash` yields `SCOPE-TOOL-UNKNOWN` instead of `SCOPE-EXEC-DENIED` (still exit 1); a write to `skill://godspeed` is reported as `SCOPE-PATH-DENIED` via membership rather than as an allowlist fault; `PurePosixPath` is imported and unused.

## Remaining unknowns

- Actual round-22 `bindings.json` write scope per seat (outside declared reads); if any seat's `write_paths` lists more than its own report, the extra spellings are accepted by design.
- Whether the producing harness always records write operations with `tool: "write"` (R4).
- Independent digest verification (forbidden under NO-EXEC).

Reviewed-SHA256: c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4
Predicate: r22-fxc2report
Scope: executed=none
