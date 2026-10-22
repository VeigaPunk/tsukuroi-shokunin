# Round 24 wave 1 — ExecRedCauses (claim C1, attempt 2)

Verdict: the C1 per-cause counting tool is delivered and exercised; its selftest passes
14/14, and on the frozen round-23 inputs at revision
674891dfbcb853432a863a6eb82e7b2a9bdb3958 it attributes 268/268 findings, preserves the
checker status CANNOT_EVALUATE, exit 2, the incomplete seat ConnFxPlanner and the
retained unknown key token `__unknown_argument__`, labels `replace_all` as author
recollection, and exits 0.

## Files changed

- Wrote `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecRedCauses/report-red-causes.py`
  (new, 491 lines, Python 3 standard library only). It is a drop-in for
  `tools/report-red-causes.py`: it locates the lane root by walking up from its own
  path for `tools/_revision.py` plus `.ufo/waves`, so the same file works at the draft
  path and at `tools/`. Verified from a mirrored `<fake>/tools/` layout under
  `/fast/scratch/hyaku/tsuku24-ExecRedCauses/fake/tools/report-red-causes.py`:
  `find_root()` returned the fake lane root and the selftest passed there.
- Wrote `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecRedCauses/run-revision-674891d-output.json`
  (the full recorded JSON output of the real run, quoted below in summary).
- Did not touch `tools/report-red-causes.py` or any other production lane file
  (a functionally similar tool was previously landed there at commit 10b45f0; the
  integration decision and the replacement are the L1's).

## Findings

1. Tool contract and invocation. The tool supports exactly the two specified modes:
   `python3 tools/report-red-causes.py --revision <REV>` and
   `python3 tools/report-red-causes.py --selftest`, plus `--branch`. It binds the
   revision through the lane's `tools/_revision.py` (`bind()`), and it runs the
   recorded checker command as a subprocess:
   `python3 tools/check-seat-bindings.py --revision 674891dfbcb853432a863a6eb82e7b2a9bdb3958 --manifest .ufo/waves/round-23/falsify/bindings.json --events .ufo/waves/round-23/falsify/events.json`.
   [obs] command built and executed inside the tool (`checker_command` in the output).

2. Checker identity. The working-tree `tools/check-seat-bindings.py` is byte-identical
   to its blob at the bound revision (both sha256
   `35079db51368105b8392aa0c664ba794485639d14950258d0a2892909d83d880`); the same holds
   for `tools/_revision.py` (sha256 `06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf`).
   In addition to the recorded-command run, the tool independently re-executes the
   revision's own checker bytes (`git show` into a temp file) over the revision's own
   manifest and events blobs; both executions returned identical finding lists (268
   entries), exit 2, status CANNOT_EVALUATE (`cross_check_identical: true`). [obs]

3. Frozen input hashes (as recorded in the output `inputs` map): bindings.json
   `8c72460b...`, events.json `52a5021b...`, falsify-limit.json `e8e22aae...`. [obs]

4. Attribution result on the frozen revision. Exit 0, `preserved: true`, all nine
   preservation checks true. `total_findings: 268`, `attributed_findings: 268`,
   `unattributed: []`. Cause rows (finding, operation, count, seats):
   - SCOPE-PATH-DENIED / read / 230 / 18 seats
   - SCOPE-PATH-DENIED / grep / 28 / 6 seats
   - SCOPE-PATH-DENIED / glob / 6 / 2 seats
   - SCOPE-PATH-DENIED / write / 2 / 1 seat
   - SCOPE-SCHEMA / edit / 1 / 1 seat
   - SCOPE-TRACE-INCOMPLETE / seat-level trace state (no recorded request at this
     site) / 1 / 1 seat
   These totals match the author-written `falsify-limit.json` (266 path findings across
   21 seats, 1 schema site, 1 incomplete seat). [obs]

5. Join semantics (single deviation from the ticket's literal wording, documented in
   the tool and here). The frozen checker emits sites as `f'{seat}:{index}'` where
   `index` is the enumerate() ordinal over that seat's `events` list
   (`tools/check-seat-bindings.py` at line ~190). `request_line` is a different
   retained field: the transcript line on which the request was issued. Joining by
   `request_line == site-number` would succeed for only 34 of the 267 request-level
   findings; the rest would be left unattributed, which contradicts the claim target of
   268/268. The tool therefore joins by the request ordinal (site number), records each
   site's `join` mode and the joined event's `request_line`, and falls back to a unique
   `request_line` match only when the ordinal is out of range. On the frozen inputs all
   267 request-level sites joined as `event_ordinal`; e.g. the schema site
   `FxC3Build08:17` joined the event whose `request_line` is 53. The output exposes the
   full per-site mapping under `sites`. [obs] plus [inf] (the purpose of the field,
   from the checker source).

6. Incomplete seat preserved. `incomplete_seats` contains ConnFxPlanner with
   `trace_complete: false` and 125 recorded requests, and the checker's own
   `present_incomplete_seats` (1) reconciles with the trace. The native-completed flag:
   `native_completed: true`, derived [inf] because `falsify-limit.json` states
   `native_completed: 76` and the retained trace contains exactly 76 seats, so the seat
   lies inside the natively completed cohort; the retained per-seat terminal evidence
   (session_exit_line null, native_failure null) neither proves nor disproves it, and
   the tool says so in `native_completed_basis`. [obs] for the retained values, [inf]
   for the derivation.

7. Unknown extra key visible. `unknown_argument_sites` lists exactly the one schema
   site: FxC3Build08:17 (operation edit), with `retained_key_token: "__unknown_argument__"`
   and retained keys `["__unknown_argument__", "i", "new_string", "old_string", "path"]`.
   The `schema_original_keys` names from falsify-limit.json resolve as follows: i,
   new_string, old_string, path are present in the retained events (label null);
   replace_all is absent and carries the label `author recollection, not recoverable
   from retained events`, exactly per the routed defect note (corpus/lessons/
   round-23-verifier-spotcheck.md line 52). [obs]

8. Selftest coverage. 14 literal-fixture cases, all PASS, including the four mandated
   failure modes: a dropped finding (primary vs. independent cross-execution mismatch),
   a dropped incomplete seat, a renamed/erased unknown key token, and unmatched sites
   (out-of-range ordinal, unknown seat, non-request site). Also covered: checker exit
   change, status relabel, missing schema site, empty findings, and the recollection
   label rule. Each failing case fails with exit 1 and names the failed check(s). [obs]

9. Exit behavior. Real run at 674891d: exit 0 (all preservation conditions hold). If
   any preservation check fails the tool exits 1 with `preserved: false`; fatal
   read/binding failures print a CANNOT_EVALUATE JSON and exit 2. [obs]

## Risks and blockers

- The ticket's phrase "the event ... whose request_line equals line" does not describe
  the frozen checker's emitted sites (they are request ordinals). This is the one
  place where the letter of the spec and the frozen data conflict; the tool follows the
  data and surfaces the mapping transparently. If the L1 wants the join restricted to
  request_line, 233 findings would become unattributed and the tool would exit 1 —
  which is precisely what the claim target forbids.
- `native_completed` for the incomplete seat is an inference from the cohort count in
  falsify-limit.json; the retained trace alone cannot confirm a per-seat native exit.
- No blockers. No tools were installed.

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/_revision.py, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-seat-bindings.py, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-23-verifier-spotcheck.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/falsify/bindings.json, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/falsify/events.json, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/measure/post-falsify/falsify-limit.json, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1-assignments.json, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1-spec.json; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecRedCauses/report-red-causes.py, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecRedCauses/run-revision-674891d-output.json, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecRedCauses.md; executed=python3 .ufo/waves/round-24/w1/ExecRedCauses/report-red-causes.py --selftest (exit 0), python3 .ufo/waves/round-24/w1/ExecRedCauses/report-red-causes.py --revision 674891dfbcb853432a863a6eb82e7b2a9bdb3958 (exit 0), python3 tools/check-seat-bindings.py --revision 674891dfbcb853432a863a6eb82e7b2a9bdb3958 --manifest .ufo/waves/round-23/falsify/bindings.json --events .ufo/waves/round-23/falsify/events.json (exit 2, CANNOT_EVALUATE), python3 fake/tools/report-red-causes.py --selftest in the sandbox mirror (exit 0)
Installs: none
