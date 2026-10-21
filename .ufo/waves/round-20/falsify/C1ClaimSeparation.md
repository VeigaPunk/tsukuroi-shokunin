# C1 claim separation — round 20 attempt 1

## Verdict

C1's **claim content and dedicated metric are causally separable** from C2's object-selector claim, C2's systemctl exec-log filter, and C3's live-map claim. The preregistration assigns distinct axes, metrics, and explicit evaluator modes: C1 `ownership_corrections` with `--ownership-corrections`, C2 `object_selector_tools` with `--object-selectors` (plus supporting systemctl cases), and C3 `audit_live_map_errors` with `--audit-live-map` (`.ufo/waves/round-20/preregister.json:5-27,55-65`). The C1 evaluator checks the OUT-009 correction and its pin/context in `PROVINCE.md`, the adjacency registry/census, and the pinned snapshot (`/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py:135-196,761-765`); it does not evaluate the C2 command classifier or C3 verdict-map cell.

There is **no shared claim metric**: C1, C2 object selectors, and C3 report different counters. There are, however, common verification prerequisites that prevent describing the integrated green result as wholly independent.

## Findings by severity

### P2 — Shared revision-binding implementation is a common-mode prerequisite

The C1 and C3 candidate gates both import `bind` from `tools/_revision.py` (C1: `/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py:18,819-823`; C3: `/tmp/tsukuroi-r20-registry-20261021/tools/check-registry-coverage.py:17,339-345`). The C2 candidate changes that same shared module's object-resolution path (`/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:112-180`); the lane maps those as separate inherited worktrees (`.ufo/waves/round-20/worktree-bindings.json:3-8`) and records the binder change (`.ufo/waves/round-20/seeded-implementation.json:5-10`). Thus the C1 and C3 content checks are distinct, but their final CLI runs share the revision-binding code C2 is changing. A binding failure can make either result unevaluable before its claim-specific check; it is not evidence that the C1 correction or C3 map is wrong.

The planned runner uses one full `args.revision`, checks it out once, and runs separate C1/C2/C3 before/after commands in that clone (`.ufo/waves/round-20/measure/run.py:23-28,53-78`). C1 and C3 payloads include the resolved revision (`check-adjacency-anchors.py:769-775`; `check-registry-coverage.py:297-302`). Independent attribution therefore requires retaining each payload and confirming its `revision` is the same intended full SHA; the common binder is infrastructure, not a shared C1/C3 metric. The C2 selector judge also explicitly excludes additional/discovered tools from its original-nine denominator (`/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:674-717`), so C1's ownership metric is not silently counted as part of `object_selector_tools`.

### P2 — C3's overall exit status shares the operative registry artifact with C1/C2

The highest operative `SKILL.md` registry table contains the documented C1, C2, systemctl, and C3 rows (`SKILL.md:2096-2118`, especially `2112,2114-2116,2118`). C3 runs generic registry coverage over that selected table and the candidate's tool set before adding the live-map finding (`/tmp/tsukuroi-r20-registry-20261021/tools/check-registry-coverage.py:345-362`). Its dedicated `audit_live_map_errors` counter is only `len(map_findings)` (`:351-355`), whereas the final status/exit is based on *all* findings (`:350-362`). Consequently, a missing/duplicate/malformed C1 or C2 tool row can make the C3 command fail even when `audit_live_map_errors` is zero. The shared table is a required integration artifact for a clean C3 exit, but it does not merge the C1 and C3 metrics; report the map counter separately from aggregate registry status.

### P3 — C1's no-write sentence motivates, but is not an input to, systemctl filtering

C1's exact correction includes the no-write boundary (`/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py:43-59`), and its checker accepts/rejects the fixed correction through the OUT-009 text/pin checks (`:135-196`). The C2 systemctl classifier instead parses command arguments and classifies finite verbs/flags (`/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:276-355`); `assess_exec_log` applies it only to `$ ...` lines in the supplied log (`:654-668`). It does not read C1's correction text, and the C1 checker does not invoke the classifier. The policy rationale is related, not a causal/data dependency. The preregistered support-systemctl outcomes are finite cases, distinct from the named `object_selector_tools` metric (`preregister.json:13-20,55-65`); the retained runner labels exec-log checks separately (`measure/run.py:93-98`).

## Residual risk and verification gaps

- The same operative `SKILL.md` table is an integration-level coupling; C3's specific map metric remains separable, but its overall exit does not isolate map correctness from generic coverage.
- The C1/C3 command pair shares C2's revised `_revision.py` binding implementation. This is a shared precondition, not a shared metric; the final identity fields must be checked against the one requested revision.
- Round-20 measurement is not evidenced as run here: the Scorecard says measured outcomes remain unobserved until L1 evaluation (`SCORECARD.md:624-626`), and the seeded implementation record says verification was not run (`.ufo/waves/round-20/seeded-implementation.json:11`). No runtime/host/boot-safety conclusion follows.
- No LSP device/server was available in the permitted read/grep/glob/write tool set; I did not obtain semantic references, definitions, or diagnostics. Source conclusions above are based on the cited file contents, not grep as semantic proof. No tests, commands, or evaluator were run.

Scope: executed=none
