# FxC2Semicolon falsification report (round 22)

Seat: FxC2Semicolon, leaf, source-only. Target: candidate/tools/check-seat-bindings.py. The read tool snapshot tag is #636F; that is the tool's tag, not a SHA-256. The assigned Reviewed-SHA256 (c45c93e5...69c4) is carried into the receipt as assigned. I did not recompute it: the seat forbids execution and the read, grep and glob tools do not hash. Executed: none. Fetches: none. Production edits: none. Tools installed or updated: none.

Tool calls made: read of the declared support files and of skill://godspeed; grep and glob over declared paths only (including one `;`-joined glob of declared paths, a read-only probe); write to the exact report path.

## Verdict

No source-visible counterexample to the grep/glob semicolon claim. The branch checks every component, and the bounded reason holds: an admissible bound entry can never contain `;`, so a `;`-joined request passes only when every component is exactly a bound entry. Two gaps remain. The fixture set does not prove the allowed-only (nonvacuity) direction, and recorded tool names may not match the classifier's name set. Both are detection or calibration gaps, not bypasses in the reviewed bytes.

## Source chain (line numbers in the target)

- L84: `value.split(';')` is applied only when tool is grep or glob. Other tools use the whole string.
- L82: a non-empty string is required, so the split yields at least one component and the loop cannot be vacuous.
- L86-91: every component goes through requested_path (selector stripping only for read) and then exact membership in binding['read_paths']. There is no break, return, filter or dedup. Each denial appends a finding (L89, L91).
- L34-36 local(): rejects non-str, empty, paths not under LANE + '/', backslash, controls, any of `*?[];:`, and `''`, `.`, `..` components.
- L111-113: every read_paths and write_paths entry must pass local(), except the exact string skill://godspeed in read_paths. So no admissible bound entry contains `;`, and a whole `;`-containing string can never equal one.
- L46-47 fetch, L48-49 exact skill, L54-55 local denial: all per component.
- L98 and L140 aggregate every finding. L144: code = 2 if incomplete else (1 if findings else 0). Exceptions at L145-147 give code 2; an uncaught exception exits 1. No path yields exit 0.

Consequence: the split only widens what is admitted. Without it, every `;` request is denied (over-denial). With it, each component must be an exact bound entry. The security property does not depend on the split. Partial-checking regressions are the only bypass-class risk (F1).

## Expected fixture verdicts versus observed runtime

Observed runtime: none. Nothing was executed (NO-EXEC).

- Existing fixture 'semicolon' (L177), grep `src + ';/outside'`: expected exit 1 with SCOPE-PATH-DENIED. Derived statically from L84-91. Observed: not run.
- Proposed fixtures, static expectations only. Observed: not run.
  - grep `src;src`: exit 0, no findings. Nonvacuity positive; absent today.
  - grep `/outside;src`: exit 1, one SCOPE-PATH-DENIED. Catches last-only regression; absent today.
  - glob `skill://godspeed;src`: exit 0. Glob positive; absent today.
  - grep `src;` (empty component): exit 1, SCOPE-PATH-DENIED.
  - grep `src; src` (padded component): exit 1, SCOPE-PATH-DENIED.
  - grep `https://example.invalid;src`: exit 1, SCOPE-FETCH-DENIED.
  - glob `src;/outside;src`: exit 1, one SCOPE-PATH-DENIED.
  - multi_tool_use.parallel child functions.glob with `/outside;src`: exit 1, SCOPE-PATH-DENIED.

## Findings

F1 (medium): nonvacuity and regression gap. The selftest has no grep or glob exit-0 fixture. The only grep semicolon fixture (L177) puts the disallowed component last. Static consequences, not executed:
- If L84 kept only the last component (`[-1:]`), L177 would still return exit 1 and the selftest would still pass, while `/outside;src` would be admitted. This is the bypass-class regression the fixtures cannot see.
- Denying every grep or glob request containing `;` would still pass the selftest.
- Dropping 'glob' from L84 would still pass, because glob `;` lists would become fail-closed denials.
- Removing the split entirely would still pass (fail-closed over-denial).
The existing fixture does catch first-only checking (it would return exit 0) and any-instead-of-all semantics.

F2 (medium; conditional on recorder naming, [INFERENCE]): tool-name set. classify recognizes only read, grep, glob, write, bash, eval, task, web_search and browser* (L63-80), plus the `functions.` prefix and parallel wrappers. The dispatch names this seat sees are _read, _grep, _glob, _write, _bash, _eval, _task, _wait and _edit. The recorder's naming is not in my read set. If events are recorded under those names, every call, including allowed reads and the report write, classifies as SCOPE-TOOL-UNKNOWN, a violation. Compliant seats would then be reported as violators, and the grep/glob branch would never run for those records. The direction is fail-closed (forbidden _bash is also a violation), but no fixture pins the recorder's naming.

F3 (low): grep selectors over-denied. The harness grep schema documents file-only selectors (for example src/foo.ts:50-100). L87 strips selectors only when tool == 'read', so such a grep component is denied by the `:` rule at L35. Fail-closed.

F4 (low): skill selector over-denied. L48 compares the exact skill string before selector stripping (L50-53). A read of skill://godspeed with a selector therefore strips to 'skill://godspeed', fails local() at L54, and is denied. Fail-closed.

F5 (low; policy note): empty and padded components are denied, not ignored or trimmed. `A;`, `;A`, `A;;B` and `A; B` are all denied. This matches the literal-path policy but over-denies if the grep or glob tool ignores or trims such components. Tool behavior is not verified here.

F6 (info): nonvacuity at seat level. A complete seat with zero events passes (fixture 'empty-trace' expects 0). The audit takes `complete` at face value (L130), so "no calls" and "calls not recorded" can be told apart only by the recorder.

F7 (info): binding trust and disclaimed residuals. The audit validates the shape of the committed manifest, not that its per-seat sets equal the dispatch-time frozen bindings. Intent-level nonvacuity therefore depends on the pre-dispatch freeze, which the code does not check. Exact-string membership does not model directory expansion or symlink targets, and L113 accepts directories as bound entries. The audit's own SCOPE string (L17) disclaims both. The assigned binding for this seat lists regular files only.

## Checked, no counterexample

- Trailing, leading and doubled `;`: each empty component denied.
- Unicode lookalikes (U+FF1B, U+FF0F), NUL, surrogates: denied by exact membership or controls() (L29-30).
- Normalization: `.`, `..`, `//`, trailing `/`, backslash: denied by local().
- Fetch forms per component (https, HTTP, host:port/): L46-47.
- Duplicate JSON keys in manifest or events: object_pairs_hook (L20-26) raises, giving schema and exit 2.
- Parallel wrapper recursion (L63-72), depth limit (L61), malformed children: exit 2.
- The grep and glob separator `;` matches the audit's split (L84).

## Out-of-target notes

- check-review-snapshots.py safe_path (L26-30) does not forbid `;`, `:`, `*` or `?`, unlike local(). It validates declared review file paths, does not split on `;`, and is not used for request classification. Divergence noted only.
- The read tool's selector grammar (L51) lacks the time-form selectors the harness documents for video (1h5m42s, 90s, 01:23). Those requests are denied, fail-closed.

## Verification gaps

- Nothing executed. Selftest not run. No observed runtime for any fixture.
- Reviewed-SHA256 not recomputed (see header).
- build/bindings.json, build/events.json and the recorder's tool-name format are outside my read set.
- _revision.bind freshness and the remainder of check-review-snapshots.py were not falsified.

Reviewed-SHA256: c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4
Predicate: r22-fxc2semicolon
Scope: executed=none
