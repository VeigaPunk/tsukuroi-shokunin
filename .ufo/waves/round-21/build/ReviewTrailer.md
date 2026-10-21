# ReviewTrailer — malformed20 falsify trailers, literal vs annotated none

Axis: C3 calibration (predicate `scope-trailer-punctuation`); reviewed target
`tools/check-seat-scope.py` pinned snapshot #D22E, identical read shape to baseline.

Reviewed-SHA256: add541d8b8d4ea7f4c38415bb31f5f9ffbcaeb177aebb2431239bbb489829dac
Predicate: scope-trailer-punctuation

## Discriminant in the pinned gate [obs]

`evaluate` classifies the last `^Scope: executed=(.+)$` line (`SCOPE` re at `:44`,
`scope_value` `:58-61` last-hit, `.strip()`). Value pipeline `:80-91`:

- `normalized = executed.strip().casefold()`; `== "none"` → continue (clean). So literal
  none is the whole stripped value, case-insensitive.
- `re.match(r"none\b", normalized)` → `SCOPE-TRAILER-MALFORMED` ("annotated none is
  ambiguous…"). `\b` fires on `none` followed by any non-word char — punctuation or space.
  So "annotated none" = `none` + a non-word suffix; the period in `none.` is an annotation.
- `none` + word char (`nonex`, `none0`, `none_`, `nonee`) fails `\b`, falls through to the
  command-list branch → `SCOPE-EXEC-UNAUTHORIZED` when the seat lacks `EXEC-AUTHORIZED`.
  The discriminant is the word boundary, not a `none` prefix.
- Upstream, not punctuation: absent report → `SCOPE-REPORT-MISSING`; no `^` line at column 0
  → `SCOPE-UNDECLARED` (indented trailer is undeclared, selftest `indented-not-a-line`
  `:353-354`).

## malformed20 corpus [obs]

`corpus/lessons/round-20.md:41,63` names the debt: 20 falsify `Scope: executed=none.`
trailers preserved as red. Measured receipt
`.ufo/waves/round-20/measure/final-r20c/seat-scope-falsify.stdout` at `fc2a0085…` reports
`SCOPE-TRAILER-MALFORMED: 20` of `seat_count: 64`, sites exactly the 20 reports whose last
line is `Scope: executed=none.`: BindAmbiguous, BindGhost40Light, BindNoncommit, BindTagPeel,
BindUnlanded, BindUnpushed, C1DigestScope, C1DuplicateSection, C1MissingCorrection,
C1NoPermission, C1QuoteAuthority, C1SelftestCoverage, C1SnapshotBinding, JudgeFullOidShadow,
MapHistoricalOnly, MapMetricExact, SysctlListDeps, SysctlNestedShell, SysctlUserMutations,
WrapperTimeoutSignal (each `none.` is the file's terminal line, e.g. `BindAmbiguous.md:47`).
The other 44 falsify reports end literal `Scope: executed=none` and produce no finding —
the literal/annotated split inside one wave. Build measured `MALFORMED 0 / MISSING 13`
(`seat-scope-build.stdout`): `ConnCrossScope.md` has a mid-body `none.` at `:9` shadowed by
a clean last trailer at `:170` — last-hit semantics, not per-line scanning.

Historical gradient: r18 annotated `none (read-only …)` prose (4 findings, CritDepth,
CritOperability, SimplifyShared, Sweep07 — `round-18/measure` results + `FxCritNoHarm.md`);
r19 falsify mutant `executed= none (no commands)` (`FxMutSeatScope.md` case c, KILLED);
r20 punctuation-only `none.` (20). No `none.` outside r20 (greps of r17–r19 report trees:
0 hits).

## Exact red/green controls (selftest-level fixtures)

- Green: report ending `Scope: executed=none` → PASS, zero findings (selftest `clean`
  `:334`); `Scope: executed=  NONE  ` → PASS (`uppercase-none-normalized` `:360-361`).
- Red, punctuation class (malformed20 form): `Scope: executed=none.` → exit 1, exactly one
  `SCOPE-TRAILER-MALFORMED` at that site; same expected for `none,`/`none;`/`none:`
  (all non-word continuations).
- Red, prose class (retained r18/r19 form): `none (authorized)`, `none (read-only git
  show)` → `SCOPE-TRAILER-MALFORMED` (`:355-357`, `:362-364`).
- Boundary guards: `none_`/`none0`/`nonex` → `SCOPE-EXEC-UNAUTHORIZED` on marker-free seats
  (command-branch fallthrough), never `MALFORMED`; `  Scope: executed=none` (indented) →
  `SCOPE-UNDECLARED`; empty `Scope: executed=` → `SCOPE-UNDECLARED` (`:351-352`);
  `none.` earlier + literal `none` last → clean (last-hit).

Coverage gap [obs]: selftest pins the parenthetical form only; `none.` punctuation has no
dedicated fixture. The pinned corpus is the measured r20 falsify run (20/20 sites); a
`none.` hermetic case plus a `none_`/`none0` boundary guard would preregister the
punctuation discriminant without relying on history. Contract alignment: r20 spec text
`spec.json:2` requires literal `Scope: executed=none` for NO-EXEC, so `none.` is a real
declaration deviation — flagging punctuation is intended, not over-reach. `FxCritNoHarm`'s
r18 "normalize on whitespace/paren" proposal would not turn `none.` green anyway (`.`
matches neither split token); the two annotation classes stay distinct.

No historical edits made or recommended; `round-20.md:41` directs the red be preserved.
Limit: this is declaration parsing — a clean trailer proves no absence of execution
(`FxCritNoHarm.md:10`); findings are review recommendations, not admission.
Reviewed only the pinned snapshot; no LSP device was exposed in this NO-EXEC seat, so
caller/reference claims rest on literal grep, not semantic proof.
Tool installs/updates: none (seat contract forbids; none needed for source review).

Scope: executed=none
