# ReviewScope — check-seat-scope.py missing-report / dead-seat handling

Artifact: `.ufo/waves/round-21/snapshot/tools/check-seat-scope.py` (pinned snapshot of
baseline `tools/check-seat-scope.py`, 673 lines, reviewed in full).
Reviewed-SHA256: add541d8b8d4ea7f4c38415bb31f5f9ffbcaeb177aebb2431239bbb489829dac
Predicate: scope-fail-closed-missing-dead

Axes: correctness (fail-closed verdicts), honesty (no fabricated/placeholder pass),
operability (typed finding ids; CANNOT distinct from FAIL), evidence class
(self-reported declarations only, per docstring).

Verdict: predicate holds. Dead seats remain red; there is no code path that fabricates
a placeholder report, and no optional/dead-skip path that could pretend clean.

## Findings by severity

No blocking or high-severity findings.

### Low — finding-id misclassification, still fail-closed (observed)

`evaluate()` lines 75-91: a `Scope: executed=` line whose value is whitespace-only
(e.g. `Scope: executed= `) matches `SCOPE`'s `.+`, `scope_value` returns `" "`, which
strips to `""` — not `none`, fails `none\b`, and falls into the EXEC check, yielding
`SCOPE-EXEC-UNAUTHORIZED` with detail `declared executed= without EXEC-AUTHORIZED`.
The verdict is still FAIL, so the predicate is unharmed; only the finding id is
arguably wrong (an undeclared/malformed class would be more accurate). Note an
*empty* value (`Scope: executed=`) does not match `.+` at all and correctly reports
`SCOPE-UNDECLARED` (selftest `empty-value`).

### Low — last-match-wins trailer selection (observed, documented, selftested)

`scope_value` takes the last `Scope: executed=` line; an earlier executed=cmd line
followed by a later `executed=none` reads clean (`last-line-clean` selftest). This is
an unverifiable-self-report limitation the docstring already concedes ("Counts are
declarations, NEVER independently verified executions"); it is not a missing-report
gap.

## Predicate evidence (observed)

1. Missing report ⇒ red, both backends. `evaluate()` 70-74: `reports.get(name)` is
   `None` → `SCOPE-REPORT-MISSING`. Worktree `read_file` (217-223) returns `None`
   only on `FileNotFoundError`; any other `OSError`/`UnicodeDecodeError` raises
   `E-READ-FAILED` → CANNOT, never a silent pass. Revision mode `collect` (266-271)
   consults the `ls-tree` listing first, so a committed-but-unreadable blob cannot be
   confused with an absent one; absent ⇒ `None` ⇒ missing finding.
2. No fabrication path. Outside `sandbox()`/`selftest()` (hermetic mktemp fixtures,
   lines 281-637), the tool performs no writes; `sys.dont_write_bytecode` is set
   (line 35). `reports` values come only from `read_file`/`read_git`; `evaluate`
   receives them as data. There is no optional/dead/status field consulted anywhere
   in `load_seats` — every seat declared in `swarm-registry.json` or `spec.json`
   demands a report, so an "optional-dead seat skipped and wave reads clean" state
   cannot be produced by this gate.
3. Empty or source-less waves cannot pass: `E-SEAT-SOURCE-MISSING`, `E-NO-SEATS`,
   `E-WAVE-MISSING`, malformed JSON → CANNOT (exit 2).
4. Seat names are constrained to safe report stems (`NAME` fullmatch, 120-134), so
   seat enumeration cannot escape the wave directory or alias a non-seat file.
5. Corroborating in-repo history (observations, not re-verified runs):
   `.ufo/reports/round-19/tsukuroi.md` records the falsify wave FAIL with 100
   `SCOPE-REPORT-MISSING` for seats without dispatches; `.ufo/reports/round-20/
   tsukuroi.md` records `seat-scope-build` exit 1 with 13 `SCOPE-REPORT-MISSING` for
   provider-rate-limit deaths, noting no reports/trailers were rewritten and no dead
   seat was replaced — behavior consistent with this source.

## Residual risk / limits

- The gate sees only seats declared in registry/spec. If a dead seat is removed from
  *both* inputs, the gate cannot know it existed — redness holds only while the seat
  remains declared. Input-generation integrity is outside this file's scope.
- A symlinked `<Name>.md` in worktree mode is followed by `read_file`; content still
  needs a valid trailer to pass, so fail-closed holds.
- Duplicate `name` entries in `spec.items` silently overwrite (last wins) — benign
  for this predicate.
- A hand-written placeholder report reading `Scope: executed=none` passes
  regardless of truth; documented self-report limitation, not a gate defect.

## Verification gaps

- NO-EXEC seat: snapshot byte-identity to baseline SHA
  `add541d8…` could not be re-hashed; the pinned snapshot path was reviewed per
  assignment. `--selftest` (44+ cases covering report-missing in both backends) was
  read, not run. No lsp device consulted (Python gate, single file, full read).
- No tool installs performed; none needed (NO-EXEC; pacman pause noted).

Scope: executed=none
