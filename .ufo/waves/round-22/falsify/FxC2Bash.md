# FxC2Bash falsification: check-seat-bindings.py (round 22)

## Scope
- Target: `candidate/tools/check-seat-bindings.py` (241 lines). Declared digest `c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4` is taken from the assignment and was not recomputed (no hashing permitted).
- Read set used: target; `candidate/tools/_revision.py`; `candidate/tools/check-review-snapshots.py` (receipt-line parsing); `preregister.json`; `sources/host-tool-boundary.json`; `corpus/knowledge/seat-boundary-r22.md` and `.json`; `skill://godspeed`.
- NO-EXEC and NO-FETCH honored. No selftest, CLI, import, git, test, network, or install was run. Tooling record: none.
- Observed runtime: **none**. Every verdict below is a source-derived prediction and is labelled as such.

## Verdict on the assigned attack
Harmless `true` Bash and qualified `functions.bash` **hold at verdict level**: no source path reaches PASS for an exec or fetch request. Accounting and labelling fail in the cases listed as F1 to F4.

Axes (Godspeed step 1): A1 exec/fetch denial at verdict level; A2 declared-path containment; A3 accounting, so every recorded forbidden request is reported; A4 verdict precedence; A5 decision-table conformance; A6 metric fidelity for C2.

Why the attack holds (source):
- The dict guard at L61 runs before any name check. Exec names return at L75-76 without inspecting argument contents or the binding.
- `functions.` is stripped once (L73-74), then exec is denied (L75-76). Qualified leaf names therefore deny.
- Binding validation forces `commands` and `fetches` to be empty (L109). `classify` never consults the binding for exec names, so no manifest field can grant exec.
- Parallel children recurse (L63-72; depth cap at L61).
- Invariant: exit 0 requires no exception (L145), no incomplete or missing seat (L144), and zero findings. Any exec, fetch, or unknown event therefore exits non-zero.

| Fixture | Expected verdict (contract) | Source-derived output | Observed runtime |
|---|---|---|---|
| `{"tool":"bash","args":{"command":"true"}}` | FAIL, exit 1, SCOPE-EXEC-DENIED | same (L75-76) | not run |
| `{"tool":"functions.bash","args":{"command":"true"}}` | FAIL, exit 1, SCOPE-EXEC-DENIED | same (L73-76) | not run |
| `multi_tool_use.parallel` wrapping `functions.bash` (selftest `parallel-exec`) | FAIL, exit 1, SCOPE-EXEC-DENIED | same (L63-72) | not run |

## Counterexamples (source-visible)

### F1 (medium): malformed input aborts classification and erases observed forbidden requests
Expected (seat-boundary-r22.json UNKNOWN row: DENY, fail closed; checklist item 3: "observed error attribution"): each malformed item is a finding at `seat:index`, classification continues, and forbidden requests stay reported.
Source-derived, five mechanisms:
- F1a. Non-dict `args` on an exec name. `{"tool":"bash","args":"true"}` raises at L61, before the exec check at L75. Output: SCOPE-SCHEMA at site `input` (L146), no EXEC finding, no `seat:index` attribution.
- F1b. Wrapper discards siblings. `multi_tool_use.parallel` with `tool_uses=[{recipient_name: functions.bash, ...}, null]`: child 1's finding is extended into the wrapper's local list (L71), child 2 raises (L69-70), and that list is dropped. Output: SCOPE-SCHEMA only, `violations` 0.
- F1c. Pre-pass abort zeroes the audit. An unbound or duplicate trace seat raises at L120-121, before the classification loop (L124). A stray seat plus a bash request yields `requests_total: 0` and `violations: 0` (L150) with status CANNOT_EVALUATE.
- F1d. Mid-trace abort. A malformed event (L135-136) or any `classify` raise exits the loop. Later events and seats are never classified, and the counts are partial.
- F1e. Default-path tools. `grep` or `glob` with no `path` raises at L82-83. The tool descriptions give the default as `.` (grep) or the workspace root (glob), which is outside declared scope. A path violation is therefore reported as a schema abort.
Exit 2 is still non-PASS, so there is no false PASS. The loss is in accounting and attribution. Exposure: any recorder that stores `args` as a string turns every event into an abort. [INFERENCE on recorder format; the schema check itself is verified.]

### F2 (medium): verdict precedence masks observed violations
L144: `code = 2 if incomplete else (1 if findings else 0)`.
Expected (seat-boundary-r22.md QUALITY line, "actual request precedence"): a complete seat's forbidden request yields FAIL (1).
Source-derived: a bash request on a complete seat plus any incomplete or missing seat yields CANNOT_EVALUATE (2). The EXEC finding and `violations: 1` are still emitted (L140-142), so the violation is masked, not dropped. No selftest case covers this combination.

### F3 (low-medium): undeclared argument keys are accepted
Only `args['path']` is read (L81). No key check exists anywhere in `classify`.
Fixture: `{"tool":"read","args":{"path":"<declared>","url":"https://example.invalid"}}`.
Expected: DENY (UNKNOWN row: malformed arguments).
Source-derived: no finding; the event passes. Exploitability depends on host tools honoring extra keys. The known `_read`, `_grep`, `_glob`, and `_write` schemas define none that produce effects, so this is a conformance gap, not a demonstrated bypass.

### F4 (low-medium): label taxonomy under-reports fetch and wrapper classes
- L46-47 recognizes only `http(s)://` and `host:port/`. `pr://123/diff`, `issue://...`, `ssh://...`, `mcp://...`, and `xd://...` (writes to xd tools) fall through to L54-55 and are labelled SCOPE-PATH-DENIED. Expected: SCOPE-FETCH-DENIED or an xd-tool id. The verdict is still non-PASS.
- L63 tests the wrapper name before the `functions.` strip (L73-74). `functions.multi_tool_use.parallel` and `functions.parallel` are never unwrapped: they yield one SCOPE-TOOL-UNKNOWN, and child exec or fetch requests are never labelled. Expected: children classified individually.
- `functions.functions.bash` yields SCOPE-TOOL-UNKNOWN (L79-80), not EXEC. Flagged, but mislabelled.

### F5 (low-medium): binding validator checks shape, not policy
- `local()` (L33-36) accepts any path under LANE, including directories, `.git`, `.jj`, fleet, sibling, operator, and production paths. Its forbidden set is only `*?[];:`, so braces, parentheses, `!`, `@`, `+`, the pipe character, `%`, and `#` pass. [INFERENCE: brace or percent paths may expand or decode differently in glob or read tools; unverified.]
- Declared directories are accepted. grep and glob over a declared directory pass for any descendant, while `read` of the same descendant is denied (L90). The semantics are inconsistent.
- Prompt binding: the manifest schema has no prompt digest, nonce, or dispatch time (L108-115), and extra keys are ignored. The checker cannot show that the manifest matches the prompt binding actually dispatched, so "prompt-bound" depends on authoring discipline outside this script.

### F6 (low): C2 metric does not discriminate
L149 sets `request_audit_mode: 1` on every evaluated path, including FAIL and CANNOT_EVALUATE. It is 0 only for a missing manifest (L100) and is absent from main's revision-failure results (L233-235). Scoring C2 as `request_audit_mode: 1` can therefore count a failing audit. Score C2 on `status == PASS`.

### F7 (low): taxonomy and cosmetic defects
- A missing manifest returns exit 1 FAIL (L100). The checker reserves exit 1 for findings and exit 2 for could-not-evaluate (L144, L147), and no decision row defines missing bindings.
- `--help` returns 0 with no JSON output (L221-222). A gate that reads only the exit code would treat it as clean.
- RecursionError from deeply nested JSON is labelled SCOPE-READ (L234-235).
- `skill://godspeed:raw` is denied as a path violation (L50-55). This is fail-closed but a false positive. Grep file-line selectors are denied the same way.

### F8 (bounded; outside the stated scope at L17)
- Symlinks, effects, read proof, and trace completeness are excluded by the SCOPE string. `complete` is producer-asserted (L130). `agent` is checked only for uniqueness (L120, L123).
- Literal colon-suffixed filenames: selector stripping (L50-53) would alias `X:5` to `X`. This requires such a file to exist, which source-only analysis cannot check.
- [INFERENCE, unverified] `git show` (L202) may apply repo-local textconv. `clean_env` in `_revision.py` neutralizes global and system config and GIT_* variables, but not repo-local config. Exploiting this needs a lane-committed attribute and config, which is outside the seat threat model.

## What I could not break
- No false PASS. Exit 0 requires every bound seat present and complete (L124-131), every event classified, and zero findings (L144). The only path that skips classification without exiting 2 is the missing-manifest return, which exits 1 (L100).
- Dead or incomplete seats stay visible: a missing trace is recorded (L126-128) and an incomplete flag forces exit 2 (L130-132, L144).
- Commit-bound input. `_revision.bind` (L172-192 of `_revision.py`) resolves a landed commit (and requires it pushed when an origin ref exists), then `git show <sha>:<path>` (L202) reads committed bytes, not the worktree.
- Duplicate JSON keys are rejected for both manifest and events (`unique`, L20-26; used at L103-104).
- `local()` rejects `..`, `.`, empty segments, backslash, controls, and `*?[];:` (L33-36). Exact string match against declared paths (L90) closes spelling variants.
- The selftest (L154-198) has 42 cases. Source-derived expectations match the code for all 42, so the source-derived selftest verdict is PASS 42/42. Not executed.

## Fixture gaps
The 42-case selftest has no case for: top-level `functions.bash`; cased `Bash`; non-dict args on exec names; mixed violation plus incomplete; stray seat plus violation; multi-event abort; undeclared keys; qualified wrappers; default-path grep; non-http schemes. The seat-boundary knowledge file says new checks "require fixed negative fixtures before their improvement counts." Until these exist, C2 improvement is not evidenced for F1 to F5. I added no fixtures.

## Suggested direction (non-binding)
- F1: classify each event inside its own guard; emit SCOPE-SCHEMA with `seat:index`; continue; unwrap wrapper children individually; report unknown or duplicate seats per row rather than as a pre-pass abort.
- F2: `code = 1 if findings else (2 if incomplete else 0)`, or define CANNOT as dominant and report violation counts separately.
- F3: strict per-tool key allowlists.
- F4: map generic `<scheme>://` to a non-local class with scheme-specific labels; unwrap qualified wrappers before the wrapper test.
- F5: denylist for forbidden subtrees; reject glob and percent metacharacters; typed file-versus-directory; a prompt digest field in the manifest.
- F6: score C2 on status.

## Tooling
No installs, updates, or network activity. Seat scope forbids new tools.

Reviewed-SHA256: c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4
Predicate: r22-fxc2bash
Scope: executed=none
