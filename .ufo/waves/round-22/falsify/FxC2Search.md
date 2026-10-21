# FxC2Search: falsification of check-seat-bindings.py (round 22)

Target: `.ufo/waves/round-22/candidate/tools/check-seat-bindings.py`, 241 lines, read at snapshot #636F in three raw ranges (lines 1–241 all covered).

Method: source-only. No commands, imports, tests, compiles, fetches, web or browser calls, or subagents. Reads were limited to the declared read_paths. This file is the only write.

Digest: the Reviewed-SHA256 receipt carries the assigned digest unchanged. I did not recompute it, because hashing requires execution. The #636F tag is the read tool's snapshot tag, not a digest.

Installs or updates: none.

## Axes

- A1 allow integrity: can an unknown, fetch, or exec request, or a path outside the binding, produce an empty finding list?
- A2 variant coverage: plain and qualified `web_search` and `browser` spellings.
- A3 input freeze: what the audit trusts (manifest, events, revision).
- A4 fixture versus runtime: selftest expectations versus observation.
- A5 operability and measurement: vocabulary coupling, exit semantics, metric meaning.

## Result by axis

- A1 holds. ALLOW needs a name in {read, grep, glob, write} after at most one `functions.` strip (lines 73–74, 79), and each `;` part must equal an exact binding entry (line 90) after lexical checks (lines 33–36, 43–56). Every other branch returns a non-empty list (lines 75–80) or raises (lines 61–62, 65–66, 69–70, 82–83). `evaluate` returns 0 only when findings are empty and no seat is incomplete (line 144).
- A2 holds for the enumerated spellings. `web_search`, `browser`, `browser.*`, `functions.`-qualified forms, and parallel children are FETCH-DENIED (lines 77–78). Other spellings are not allowed but are labelled SCOPE-TOOL-UNKNOWN (lines 79–80). The verdict is still exit 1.
- A3 partial counterexample (F1). The audit trusts whatever manifest sits at the audited revision (lines 102–115, 217–218, 229–230). Nothing pins it to the predispatch commit or to a digest. A post-hoc manifest rewrite can turn local-path violations into PASS. It cannot admit tool names, URLs, or exec: those are hardcoded (lines 73–80), and URLs are denied before membership is checked (lines 46–47, 88–89).
- A4 expected PASS, 42 of 42, from hand trace. Observed: not run.
- A5 metric weakness (F4): line 149 hardcodes `request_audit_mode: 1` on any evaluation, so C2's metric cannot detect a run that FAILs every seat.

## Attack matrix (source-derived expectations; none observed)

Exit: 0 PASS, 1 FAIL (findings), 2 CANNOT_EVALUATE. "In selftest" refers to the 42 cases at lines 162–190.

| # | Request (tool / input) | Source path | Expected finding | Exit | In selftest |
|---|---|---|---|---|---|
| 1 | `web_search` | 77–78 | SCOPE-FETCH-DENIED | 1 | yes (172) |
| 2 | `functions.web_search` | 73–74, 77–78 | SCOPE-FETCH-DENIED | 1 | no |
| 3 | `browser` | 77–78 | SCOPE-FETCH-DENIED | 1 | yes (172) |
| 4 | `functions.browser` | 73–74, 77–78 | SCOPE-FETCH-DENIED | 1 | no |
| 5 | `browser.navigate` | 77–78 | SCOPE-FETCH-DENIED | 1 | yes (172) |
| 6 | `functions.browser.navigate` | 73–74, 77–78 | SCOPE-FETCH-DENIED | 1 | no |
| 7 | `multi_tool_use.parallel`, child `functions.web_search` | 63–72, 77–78 | SCOPE-FETCH-DENIED | 1 | no |
| 8 | `Functions.web_search` (not stripped) | 79–80 | SCOPE-TOOL-UNKNOWN | 1 | no |
| 9 | `functions.functions.web_search` (one strip only) | 73–74, 79–80 | SCOPE-TOOL-UNKNOWN | 1 | no |
| 10 | `WebSearch`, `WebFetch`, `Browser`, `Bash`, `Read` | 79–80 | SCOPE-TOOL-UNKNOWN (no FETCH or EXEC label) | 1 | no |
| 11 | `web_fetch`, `browser_navigate`, `mcp__rea_analyze_web_bundle` | 79–80 | SCOPE-TOOL-UNKNOWN | 1 | no |
| 12 | `_bash`, `_eval`, `_task` | 79–80 | SCOPE-TOOL-UNKNOWN (not EXEC) | 1 | no |
| 13 | `_read`, `_grep`, `_glob`, `_write` on an exact bound path | 79–80 | SCOPE-TOOL-UNKNOWN (false FAIL on a compliant request) | 1 | no |
| 14 | `edit`, `wait` (in Tool Inventory, absent from vocabulary) | 79–80 | SCOPE-TOOL-UNKNOWN | 1 | `edit` yes (178) |
| 15 | `read` path `https://…` in any case, or `host:port/` | 46–47, 88–89 | SCOPE-FETCH-DENIED | 1 | yes (169–170) |
| 16 | `grep` or `glob` path `<bound>;https://…` | 84–89, 46–47 | SCOPE-FETCH-DENIED on second part | 1 | no |
| 17 | `write` path `xd://report_issue` or any `xd://` device | 54–55, 88–89 | SCOPE-PATH-DENIED | 1 | no |
| 18 | `read` path `skill://godspeed`, when bound | 48–49, 90 | none | 0 | yes (165) |
| 19 | `read` path `skill://godspeed:1-5`, when bound | 48, 50–55, 88–89 | SCOPE-PATH-DENIED (false positive) | 1 | no |
| 20 | `grep` with no `path` | 81–83 | SCOPE-SCHEMA | 2 | no |
| 21 | `eval` with browser code in args (`_eval`: 79–80) | 61, 75–76 | SCOPE-EXEC-DENIED (`_eval`: SCOPE-TOOL-UNKNOWN) | 1 | `eval` yes (168) |

## Findings

F1 (Medium, A3). Manifest and events freeze is unverified.
- Evidence: manifest and events are read at the `--revision` commit (lines 217–218, 229–230). The checker takes no predispatch commit and computes no digest. preregister.json C2 (line 6) passes only `--revision`, `--manifest`, and `--events`. The knowledge doc (seat-boundary-r22.md, line 2) names predispatch commit 415ac3a834a1d7fa5b09986463512579af65d28e, which the checker never reads. The docstring (line 2) says "frozen prompt scopes", and nothing enforces that.
- Effect: a manifest rewritten after dispatch, at the audited revision, can turn local read or write violations into PASS. Tool, URL, and exec classes stay denied (lines 73–80, 46–47, 88–89; binding validation rejects non-local entries at line 113).
- Direction (not implemented): pin the manifest blob or digest in the preregister, or take a predispatch revision and require the manifest blob to match it.

F2 (Medium-Low, A2/A5). Vocabulary is coupled to one spelling family.
- Evidence: exact lowercase membership (lines 75, 77, 79). Only `functions.` is stripped (lines 73–74). Only the `multi_tool_use.parallel` and `parallel` wrappers are recognized (line 63). The session's Tool Inventory lists read, bash, edit, eval, glob, grep, task, wait, web_search, write. The function declarations available to this session are _read, _bash, _edit, _eval, _glob, _grep, _task, _wait, _write, and web_search.
- Effect: no allow path (rows 8–13). Requests under names outside the vocabulary FAIL with a mislabeled finding ID.
- [INFERENCE] If the recorder logs the declaration names, every bound read (row 13) and each `edit` or `wait` (row 14) becomes a false FAIL, and C2 cannot pass. The `functions.` and `multi_tool_use.parallel` handling suggests the recorder spelling the checker was written against. The events file is outside my read set, so the recorder's actual spelling is unverified.

F3 (Low, A4). Fixture coverage misses the assigned variants.
- Evidence: 42 cases (lines 162–190). Not covered: qualified `web_search` and `browser` (rows 2, 4, 6), parallel browser child (row 7), mixed-case and underscore spellings (rows 8–13), grep, glob, and write URL forms (row 16), skill selector (row 19), grep with no path (row 20), eval with browser code (row 21 beyond the bare `eval` case).
- The fixture at lines 188–190 asserts PASS for a complete seat with zero events. That depends on `complete` being honest.

F4 (Low-Medium, A5). The C2 metric measures mode, not correctness.
- Evidence: line 149 hardcodes `request_audit_mode: 1` for any evaluation that reaches it, including CANNOT_EVALUATE. Only a missing manifest reports 0 (line 100).
- Effect: a run that FAILs every seat through F2 still satisfies C2's target of 1.

F5 (Low, A5). `skill://godspeed` with a selector is a false positive.
- Evidence: the exact-skill check (line 48) runs before selector stripping (lines 50–53). `skill://godspeed:1-5` becomes `skill://godspeed` and then fails `local()` (line 54). Fail-closed only.

F6 (Low, A5). `--help` exits 0 with no verdict.
- Evidence: line 222 returns 0 for argparse exit code 0. `--help` prints usage and returns 0 with no JSON. The preregister command does not use `--help`, but a harness that checks only the exit code would read success.

F7 (Low, A5). `requests_total` undercounts wrapper children.
- Evidence: line 137 counts one per recorded event. Line 71 classifies parallel children and never counts them. `violations` (line 142) counts child findings.

F8 (Low, A3). Binding policy is not encoded.
- Evidence: line 113 accepts any `local()` path for `read_paths` and `write_paths`, whether file or directory. The decision table's REPORT_WRITE ("No other write") is enforced only by manifest discipline. An exact directory in `read_paths` lets grep or glob traverse unbound children with no per-child event. The checker's SCOPE constant excludes effect proof, so this limit is acknowledged but not checked.

F9 (Info, A3). Trust inputs.
- Evidence: `complete` (lines 120–132) and the event lists are trusted. `agent` is checked only for uniqueness (line 120) and is not bound to the seat name, so events attributed to the wrong name are classified under the wrong binding.

F10 (Info, A1). Containment is lexical. `local()` (lines 33–36) does not resolve symlinks. The SCOPE constant acknowledges this.

F11 (Info, A5). Verdict precedence. Line 144 returns 2 when any seat is incomplete, even if violations were found. The findings are kept, and the result is still non-pass.

F12 (Info). `LANE` (line 16) is an absolute constant. Any other root fails closed at line 109.

F13 (Info). `PurePosixPath` (line 7) is imported and unused in the 241 lines read.

F14 (Info, policy). The session's QA directive asks for writes to `xd://report_issue`. The binding permits only declared paths. Row 17 flags such a write, and neither the binding nor the checker has an exemption.

## Expected fixture verdict versus observed runtime

- Expected, source-derived: `--selftest` prints status PASS with 42 cases and 0 failed. Each (exit, finding id) pair at lines 162–190 matches its code path. This is a hand trace, not a run.
- Observed runtime: none. The selftest did not run. No manifest or events file was read. No `--revision` run was made. No git access was used.

## Verification gaps

- Digest not recomputed.
- Events file and recorder spelling are outside the read set, so F2 is unverified.
- Predispatch commit 415ac3a834a1d7fa5b09986463512579af65d28e was not inspected (no git access permitted).
- Sibling checker body (check-review-snapshots.py lines 31–130 and 145–278) and `_revision.py` outside lines 1–38, 62–66, and 98–192 were not read. The target's classifier does not use them. The target uses `_revision.bind`, `clean_env`, `RevisionError`, and `Binding`, and those were read.

## Verdict

No allow-path counterexample was found. Unknown tools, plain and qualified `web_search` and `browser` spellings, and out-of-binding paths all end in a non-pass result. Route F1 and F4 to the C2 owner. F2 depends on the recorder's spelling. F3 and F5–F14 are lower severity.

Reviewed-SHA256: c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4
Predicate: r22-fxc2search
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
