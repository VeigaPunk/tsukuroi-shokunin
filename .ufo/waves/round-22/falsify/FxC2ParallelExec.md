# FxC2ParallelExec — source-only falsification report

Predicate: r22-fxc2parallelexec. Reviewed bytes:
`.ufo/waves/round-22/candidate/tools/check-seat-bindings.py` (241 lines, full coverage via ranged reads).
SHA256 taken from the assignment header (`c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4`);
independent recomputation would require command execution, which this seat forbids — hash is recorded as declared, not re-derived.

Claim under attack: "Nested parallel wrapper carrying denied Bash; depth bound cannot green."
Scope discipline: this auditor is post-hoc detection over recorded request spellings (S084: no native per-seat
allowlist; file docstring line 3 and SCOPE constant lines 16-17 say the same). "Cannot green" below means the
verdict logic cannot return exit 0 / status PASS for such a recorded request — never runtime prevention.

## Verdict

The claim HOLDS, with a bounded source-level argument. No greening counterexample exists in these bytes.

Every path through `classify` for a bash-bearing wrapper ends non-green:

- `check-seat-bindings.py:61-62` — the guard raises `ValueError` when `depth > 8` (also on non-str/empty tool
  or non-dict args). In `evaluate` (`:105-121`) any raise from `classify` is caught and mapped to
  `SCOPE-SCHEMA` with `code = 2` (CANNOT_EVALUATE).
- `:63-72` — both `multi_tool_use.parallel` and the bare `parallel` alias recurse into `tool_uses` children,
  propagating collected findings with `findings.extend(...)` at `:71`; depth increments exactly once per wrapper
  level (`depth + 1`), starting at 0 for the recorded event.
- `:73-76` — one `functions.` prefix is stripped, then `bash`/`eval`/`task` return `['SCOPE-EXEC-DENIED']`
  unconditionally, before any path/args inspection. There is no branch that returns `[]` for these tools at any
  reachable depth.
- `:122-123` in `evaluate` — `code = 2 if incomplete else (1 if findings else 0)`; exit 0 requires an empty
  findings list and zero incomplete seats, so any denial finding or any raise precludes green.

Depth boundary, precisely: a bash call sitting at depth ≤ 8 (direct child of the 8th nested wrapper or higher)
classifies normally and yields `SCOPE-EXEC-DENIED` (exit 1). A bash at depth 9 (direct child of a wrapper at
depth 8) trips `depth > 8` first — CANNOT_EVALUATE, exit 2. The bound degrades to fail-closed, never to pass.

Counterexample attempts, all source-visible and all failing to green:

1. Double prefix `functions.functions.bash` (`:73-74` strips once) → falls to `:79` `SCOPE-TOOL-UNKNOWN`.
2. Alias spelling `parallel` (no namespace) → still recursed at `:63`.
3. Case/whitespace/Unicode variants (`Bash`, `bash `, fullwidth) → no exact match at `:75` → `SCOPE-TOOL-UNKNOWN`.
4. `tool_uses` absent, non-list, or empty (`:64-66`), child non-dict (`:69-70`), `recipient_name` non-str, or
   `parameters` missing → `ValueError` → exit 2.
5. Depth-exhausted chain (9 wrappers) → `ValueError` at `:61` → exit 2.

## Expected fixture verdicts (derived statically; observed runtime: none)

No execution was performed or permitted (`Scope: executed=none`). Derived expectations for the missing fixtures:

- nested-parallel-exec (wrapper → wrapper → `functions.bash`, depths 0/1/2): expected exit 1,
  finding `SCOPE-EXEC-DENIED` at the event site.
- depth-8-boundary (bash at depth 8): expected exit 1, `SCOPE-EXEC-DENIED`.
- depth-exhaustion (bash at depth 9): expected exit 2, `SCOPE-SCHEMA`.

These are predictions from the cited lines, not observations.

## Findings by severity

- M1 — Verification gap: no nested-parallel or depth-exhaustion fixture exists. All four parallel selftest cases
  (`:180-183`) are single-level; the `depth > 8` branch and wrapper-in-wrapper recursion are unexercised by the
  candidate's own harness. Per the round-22 corpus QUALITY rule (new checks require fixed negative fixtures
  before their improvement counts), the depth-bound claim is currently unproven by fixture even though it holds
  by inspection.
- L1 — Accounting loss on mid-loop raise (fail-closed but lossy): if `classify` raises for any event, `evaluate`
  aborts the whole seat/seat-loop; remaining seats get no `rows` entry, no `requests_total` counting, and neither
  `SCOPE-TRACE-MISSING` nor `SCOPE-TRACE-INCOMPLETE` (`:105-123`). Collected findings survive, exit is 2, so no
  green — but a CANNOT_EVALUATE report can under-report seat-level request counts, which C3 cohort accounting
  consumes. Visible only as `seats_bound` exceeding `len(rows)`.
- L2 — Fail-closed quirk: a selector-qualified read of the approved skill URI (`skill://godspeed:1-5:raw`) is
  denied. The exact-match check (`:44-45`) precedes selector stripping (`:46-49`), and the stripped value fails
  `local()` (`:33-36`, not under LANE). Conservative denial; no violation, worth a deliberate decision.
- L3 — Dead weight: `PurePosixPath` imported at `:7` and never used anywhere in the file.

## Residual risk and verification gaps

- No runtime execution: expected verdicts above are static derivations; the M1 fixtures must actually be added
  and run by an executor seat before the depth-bound behavior counts as validated.
- `subprocess` is imported and used by `git_read`/`main` for committed-read plumbing; out of scope here (the
  auditor itself never executes the audited requests), but any claim that the tool "never executes anything"
  must stay limited to the classified requests, per SCOPE.
- Hash identity of the reviewed bytes rests on the assignment's declared SHA; no independent check was possible
  under NO-EXEC.

Reviewed-SHA256: c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4
Predicate: r22-fxc2parallelexec
Scope: executed=none
