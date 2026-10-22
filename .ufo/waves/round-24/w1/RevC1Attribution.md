# Round 24 — independent C1 cross-check (RevC1Attribution, attempt 2)

Verdict: the claimed 268-finding baseline reproduces exactly, the operation split is read 230, grep 28, glob 6, write 2, edit 1 (schema), seat-level 1, and the checker's real join is positional (seat name plus array index), not request_line joining; a request_line join would be many-to-one and ambiguous.

## Findings

1. [obs] Baseline reproduced exactly. Command `python3 tools/check-seat-bindings.py --revision f169b3ba --manifest .ufo/waves/round-23/falsify/bindings.json --events .ufo/waves/round-23/falsify/events.json` from /home/vgpnk/Projects/shokunin/tsukuroi-shokunin exits 2, status CANNOT_EVALUATE, 268 findings: SCOPE-PATH-DENIED 266, SCOPE-SCHEMA 1 at site FxC3Build08:17, SCOPE-TRACE-INCOMPLETE 1 at seat ConnFxPlanner. Same run reports seats_bound 76, requests_total 1647, violations 266, structured_edit_mode 0, revision f169b3ba9a59abaf3e324c1b591e1e07a4d6003a. All claimed numbers confirmed.

2. [obs] Frozen inputs are identical in working tree and revision. sha256 of .ufo/waves/round-23/falsify/bindings.json equals `git show f169b3ba:` blob (8c72460bf7561c65...), and sha256 of .ufo/waves/round-23/falsify/events.json equals its blob (52a5021bb18647ca...). My independent computation over the working-tree files therefore evaluates the same bytes the checker reads at the revision.

3. [obs] Independent replication matches the checker byte for byte. I reimplemented the classifier from /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-seat-bindings.py (no import of the checker) and rederived all findings from the two JSON inputs: 268 findings, requests_total 1647, and the findings list is equal to the checker's output element by element, including order.

4. [obs] Operation split of the 268 findings by finding id and recorded tool (join of each finding site back to its event record):

   | finding id | recorded tool | count |
   |---|---|---|
   | SCOPE-PATH-DENIED | read | 230 |
   | SCOPE-PATH-DENIED | grep | 28 |
   | SCOPE-PATH-DENIED | glob | 6 |
   | SCOPE-PATH-DENIED | write | 2 |
   | SCOPE-SCHEMA | edit | 1 (site FxC3Build08:17) |
   | SCOPE-TRACE-INCOMPLETE | none (seat completeness flag, not an operation) | 1 (seat ConnFxPlanner) |

   Per-seat spread of the 266 path denials over 21 seats (matches `path_finding_seats: 21` in /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/measure/post-falsify/falsify-limit.json): ConnFxPlanner 114 (read 95, grep 14, glob 5), FxC3Build06 38 (all read), FxKnowReconcile 30 (read 22, grep 8), FxC3Falsify03 19, FxC3Falsify02 11, FxC3Falsify07 9, SentFxPrivacy 8, FxC2OracleSpelling 6, FxC2OracleLegacy 5, FxC1WriteOnlyEdit 3, FxC1Expansion 3, FxC1Table 3 (grep 2, read 1), FxKnowEdit 3, FxSources 3 (write 2, read 1), FxC1EditTraversal 2, FxC1Selftest 2 (grep 2), FxC2Selftest 2, FxC3Pins 2 (read 1, glob 1), FxC1UndeclaredEdit 1, FxC1OpaquePatch 1 (grep 1), FxC3Build08 1 (grep 1). Seat ConnFxPlanner accounts for 115 of 268 findings (114 path denials inside its 125 classified events plus the incomplete flag).

5. [obs] Per-tool denominators over all 1647 events: read 1237 events with 230 denials, grep 263 with 28, write 78 with 2, edit 63 with 1 schema finding and 62 clean, glob 6 with 6 denied (every glob in the cohort was denied). Zero multi_tool_use.parallel or parallel wrapper events exist in the frozen events. The two write denials are FxSources:38 (relative path `.ufo/waves/round-23/falsify/FxSources.md`, not lane-local) and FxSources:44 (absolute path under /home/vgpnk/Projects/shokunin, outside the lane root).

6. [obs] The checker's real join is positional, not request_line based. Site strings are produced only at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-seat-bindings.py:190 (`add(fid, f'{name}:{index}')`) from the loop at line 181 (`for index, event in enumerate(seat['events'])`). A text search of the checker finds no occurrence of request_line, start_line, call_id, or digest anywhere; `origin` appears only inside a selftest fixture at line 350, and the top-level `coverage` key is merely tolerated by the schema check at line 163 and never inspected. The classifier reads only each event's `tool` and `args`.

7. [obs] request_line is a transcript-frame projection, not an event identity, and it diverges from the site index everywhere. All 1647 events carry a request_line field, and for all 1647 events the request_line value differs from the positional index; every one of the 76 seats has a non-contiguous request_line sequence, with 732 distinct (seat, request_line) values carrying the 1647 events. Example: seat FxC1DeclaredEdit events at indices 0 through 6 all carry request_line 10 while their start_line values are 11 through 17, so one recorded request line projects to seven separate tool-call records. Joining the 267 event-level findings by (seat, request_line) would collapse them to 121 keys, with 146 findings sharing a key with a sibling finding (maximum 4 findings on one key, for example FxC3Build06 request_line 59, 75, 84, 105, and 114). So site-to-request_line joining is NOT the checker's semantics, and adopting it would lose attribution precision.

8. [obs] Can a site name a start line? No. start_line and start_lines are never read by the checker (see finding 6). In the frozen events, start_lines has one entry for 1608 events, zero entries for the 26 events with origin additional-recorded-start, and two entries for 13 events, so even the trace's own line fields are projections that one event record can project onto several start frames.

9. [obs] Can a site name a nested wrapper? Yes in the checker's general semantics, no in this cohort. classify() recurses into multi_tool_use.parallel children (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-seat-bindings.py:61-73) and attributes every leaf finding to the wrapper's single site, so one site can name a wrapper carrying several distinct operations; multi-path semicolon arguments on grep and glob, and the unknown-key plus path-denial combination, can likewise put several findings on one site. In this frozen cohort there are zero wrapper events, no finding event uses semicolon splitting (the 13 semicolon paths are read events, denied singly by the character rule in local()), and no site carries more than one finding, so the site-to-operation join is unambiguous for these 268 findings.

10. [obs] The schema finding is rename-invariant. Event FxC3Build08:17 is an edit whose retained args keys are `__unknown_argument__`, i, new_string, old_string, path; the checker raises SCOPE-SCHEMA because set(args) minus `i` is neither edit shape. Substituting the author-recalled name `replace_all` for `__unknown_argument__` yields the same shape mismatch and the same SCOPE-SCHEMA verdict, so per-cause attribution at this site does not depend on the retained rename.

11. [unk] The recorded arguments digest does not recover the original key name either. The event's request_arguments_sha256 is 0fd4d531122cb956...; I hashed the retained args and the replace_all-substituted args under four common json.dumps serializations (ensure_ascii and utf-8, default and compact separators) and none match, so the exact serialization is unknown and the author list `schema_original_keys` in falsify-limit.json remains author recollection, not recoverable from retained events, consistent with /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-23-verifier-spotcheck.md:52. My probes do not prove the name wrong; they fail to confirm it.

12. [obs] Structural cross-checks against falsify-limit.json: falsify_request_count 1647 equals the events array total; trace_complete 75 with incomplete_seat ConnFxPlanner matches; native_completed 76 equals the trace seat count; path_findings 266 and edit_requests 63 match; schema_site FxC3Build08:17 matches. The lesson's routing requirements at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-23-verifier-spotcheck.md:52 and :64 (per-cause observability, keep the unknown key visible, keep the incomplete seat) are all satisfiable from the retained data, since every one of the 267 event-level findings joins to exactly one event with exactly one recorded tool.

## Residual risk and verification gaps

- The arguments digest serialization is unspecified, so the original extra-key name stays unrecoverable from retained bytes; the C1 report must keep labelling `replace_all` as author recollection (finding 11).
- The checker validates event records only as dicts with tool and args; it never cross-checks the trace's request_line, start_line, or call_id metadata, so nothing in the tool itself vouches that the retained event array is complete or ordered as recorded; the events file's own coverage string says as much ("request projections, not operation effects or universal trace completeness"). This is a scope statement, not a defect found in the 268.
- 13 events project onto two start frames and 26 additional-recorded-start events occupy positional indices without carrying findings; a future tool that reports per-request-line counts should state which frame space it counts, or its totals will not reconcile with 1647.
- I verified the classification logic by faithful reimplementation and exact output equality, not by running the checker's own selftest in this session.

Scope: read=tools/check-seat-bindings.py, tools/_revision.py, .ufo/waves/round-23/falsify/bindings.json, .ufo/waves/round-23/falsify/events.json, .ufo/waves/round-23/measure/post-falsify/falsify-limit.json, corpus/lessons/round-23-verifier-spotcheck.md; wrote=.ufo/waves/round-24/w1/RevC1Attribution.md (scratch scripts and baseline capture under /fast/scratch/hyaku/tsuku24-RevC1Attribution/); executed=check-seat-bindings baseline run (exit 2), read-only git show/sha256sum identity checks, read-only Python analysis of the two frozen JSON inputs
Installs: none
