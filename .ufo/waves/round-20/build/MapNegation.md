# MapNegation — C3 review/mutation design (round 20, seat TsukuroiR19Recovery.MapNegation-2)

Scope: `--audit-live-map` mode of `tools/check-registry-coverage.py` only — explicit no-live-DEGRADED
contract and the requirement that selftest wording must not false-positive. Baseline registry
selector/source map inspected; prereg `.ufo/waves/round-20/preregister.json:20-27,49-53` is the
contract source. NO-EXEC seat: nothing was run; every expected code/ID below is derived from
committed/candidate source lines, not observed output.

## Findings

### Verified — selector and source map (baseline)

- Selector (baseline `tools/check-registry-coverage.py`, `_operative_rows` ≈:134-190): exact heading
  regex `^## Gate and probe registry — round([0-9]+) superseding current rows$` (:25-27); unique
  highest round wins (`highest = max(...)`, duplicate highest → `TableError "round{highest} heading
  is duplicated"`); section ends at the next ATX heading of level ≤2; exactly one 8-cell header +
  separator; rows until a blank line. Candidate worktree
  `/tmp/tsukuroi-r20-registry-20261021/tools/check-registry-coverage.py:146-149` keeps this selector
  byte-identical (seeded-implementation.json:7 "existing parser").
- Source map ground truth, `tools/boot-chain-audit.sh`: exit map `0 CONSISTENT | 1 DEGRADED |
  2 UNKNOWN` with "DEGRADED is kept in the vocabulary for forward compatibility; no v2 verdict maps
  to it, so exit 1 is never emitted under this schema. Usage errors also exit 2." (:81-86); `audit()`
  emits only `CONSISTENT`/rc0 or `UNKNOWN`/rc2 (:795-806); selftest prints
  `TSUKUROI_BOOTCHAIN_SELFTEST: PASS|FAIL` and returns 1 only on failed selftest assertions
  (:1216-1222); refusals/usage print UNKNOWN/2 (:1250-1290). So live "1" does not exist; "1" is
  selftest-scoped. The corrected registry cell is a transcription of this contract, not an invention.
- The C3 defect row (r19 operative table, retained historical in the integrated lane at
  `SKILL.md:2073`): verdict cell `0 CONSISTENT;1 DEGRADED;2 UNKNOWN; not operator clearance` —
  advertises live 1. The r18 historical row already said the truth ("the live summary never emits 1;
  1 is only a selftest assertion failure", `SKILL.md:1965`); the R19 erratum mistook that historical
  row for operative (`R20-FALSE-OPERATIVE-MAP`, `SKILL.md:2086`).

### Verified — candidate audit surface and exact expected codes/IDs

Candidate (`/tmp/tsukuroi-r20-registry-20261021/tools/check-registry-coverage.py`):

- `AUDIT_LIVE_MAP` (:31-34) = `live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; selftest:
  0 PASS;1 FAIL; usage: 2 could-not-evaluate; no live DEGRADED; not operator clearance` — matches the
  integrated r20 row `SKILL.md:2109` whitespace-for-whitespace.
- `_audit_live_map(rows)` (:270-288) runs on the already-selected operative rows only. Requires
  exactly one `boot-chain-audit` row, else `REGISTRY-AUDIT-LIVE-MAP` at site `SKILL.md` (no line),
  detail `exactly one operative boot-chain-audit row required`. Then requires `kind == "probe"`,
  entry paths exactly `{"tools/boot-chain-audit.sh"}` (:283-284), and whitespace-normalized equality
  of the verdict cell with `AUDIT_LIVE_MAP` (:285); any deviation → `REGISTRY-AUDIT-LIVE-MAP` at
  site `SKILL.md:<row line>`, detail `schema-v2 live0/2 and separate selftest0/1 map required`.
- Wiring (:351-355): findings extend only under the flag; `counts["audit_live_map_errors"]` is added
  only under the flag. Without `--audit-live-map` the mode is inert and the key is absent.
- Parser (:317-318) adds the flag; prereg command
  `python3 tools/check-registry-coverage.py --revision <REV> --audit-live-map` is exercisable.

### Verified — fixture delta and per-class expectations

Canonical fixture (candidate selftest :565-613): minimal repo, `tools/boot-chain-audit.sh` =
`# fixture audit source\nSELFTEST = '--selftest'\n`; `SKILL.md` = `_skill([row])` with
`row = ("boot-chain-audit","probe","python3 tools/boot-chain-audit.sh", <verdict>,
"python3 tools/boot-chain-audit.sh --selftest")`. Deltas (all invoked `--revision <rev>
--audit-live-map`):

| Class (prereg name) | Fixture delta vs green | Expected (exact) |
|---|---|---|
| `corrected_live_map` (green) | verdict = `AUDIT_LIVE_MAP` verbatim | exit 0 / `PASS`; `audit_live_map_errors=0`; `findings == []` (candidate case `audit-live-map-correct`, :576-581) |
| `legacy_live_1` (red) | live segment replaced: `live: 0 CONSISTENT/observation;1 DEGRADED;2 UNKNOWN/could-not-evaluate;` (candidate `legacy_map` :569-571), rest unchanged | exit 1 / `FAIL`; `audit_live_map_errors=1`; findings exactly `[{"id":"REGISTRY-AUDIT-LIVE-MAP","site":"SKILL.md:<row line>","detail":"schema-v2 live0/2 and separate selftest0/1 map required"}]` (case `audit-live-map-live1`, :583-590) |
| `selftest1_only` (admit) | none — the green cell itself carries `1` only inside the `selftest: 0 PASS;1 FAIL` segment and the literal `no live DEGRADED` | allowed: `audit_live_map_errors=0`, exit 0; must not be classified live DEGRADED (encoded inside `audit-live-map-correct`) |
| `historical_row_only_fix` (red control) | round1 (historical) table carries the corrected row; round2 (unique highest) carries `legacy_audit`: `_skill([legacy_audit], round_number=2, before=_skill([corrected_audit], round_number=1))` | identical to `legacy_live_1`: exit 1, exactly one `REGISTRY-AUDIT-LIVE-MAP`, `audit_live_map_errors=1` (case `audit-live-map-historical-only-fix`, :604-613) |
| companion green control | inverse nesting: legacy in round1, corrected in round2 highest | exit 0, `audit_live_map_errors=0`, no findings (case `audit-live-map-highest-table`, :592-603) |
| row-count edge | zero or ≥2 operative `boot-chain-audit` rows | exit 1; one `REGISTRY-AUDIT-LIVE-MAP`, site `SKILL.md`, detail `exactly one operative boot-chain-audit row required` (:278-280) |
| duplicate highest heading | two round-N headings | NOT a C3 verdict: selector raises first → exit 2 / `CANNOT_EVALUATE`, finding id `E-REGISTRY-TABLE`; no `audit_live_map_errors` semantics (selector :146-149; main TableError path) — MapDuplicate.md's facet |

The four prereg C3 expected classes (:49-53) map 1:1 onto candidate selftest cases with the exact
IDs/exits above; candidate selftest declares `total = 17` (:450) = 13 carried checks + 4 new.

### Verified — why any-historical-row or digit-presence checking is insufficient

1. Any-row red (scan every table, flag any legacy cell) is permanently unpassable: historical tables
   are retained by contract (`SKILL.md:2062` "earlier registry table are historical and
   non-operative"; `R20-SKILL-PREFIX-EXCEPTION` :2088 forbids the R19-style −1 historical rewrite).
   `audit_live_map_errors=0` would be unreachable without mutating history.
2. Any-row green (pass if ANY row shows the corrected map) certifies exactly the R19 false state:
   the round18 historical row already carried the correct text (`SKILL.md:1965`) while the operative
   r19 row still advertised live 1 (`:2073`). The R20-FALSE-OPERATIVE-MAP disclosure (:2086) is the
   named receipt that this acceptance rule is the failure mode, not a hypothetical.
3. Digit/word presence, red direction ("contains `1`" or "contains `DEGRADED`"): false-positives the
   required green cell, which legitimately contains bare `1` (selftest segment) and the word
   `DEGRADED` (inside the required negation `no live DEGRADED`). This is precisely the
   "selftest wording must not false-positive" charge: a token scan cannot separate mode-labelled
   segments and would reject the preregistered corrected wording.
4. Digit presence, green direction (baseline generic probe check — bare-token presence of `0` and
   `2`, VERDICT_ZERO/VERDICT_TWO :28-30, applied in `_coverage` ≈:219-236): passes the legacy r19
   row as-is (it contains 0, 1 and 2), so the defect is invisible and before would measure 0,
   contradicting prereg `before: 1`. Presence checks are satisfied by both the defect and the fix.
5. Position heuristics (first/last matching row) do not substitute for the selector: first-row picks
   the historical r19 table (false red forever); last-row coincides with highest-round here but is
   refuted by the duplicate-highest case (must be `E-REGISTRY-TABLE`/CANNOT, not silent
   last-one-wins) and by the historical-only-fix control (a corrected lower table must not mask a
   legacy highest). Only the unique highest round defines the operative contract.
6. The candidate's mechanism is exact transcription of the pinned source contract (whitespace-
   normalized equality, :285), with the negation `no live DEGRADED` as required wording, not a
   scanned token — so the live-1 regression, deletion of the selftest `1`, dilution of the negation,
   wrong kind, or a re-pointed entry cell each fail closed to the single named finding.

## Residual risk and verification gaps

- Integration order (medium, sequencing not candidate defect): production lane
  `tools/check-registry-coverage.py` is still baseline (543 lines, no `--audit-live-map`, selftest
  `total = 12`) while production `SKILL.md` already carries the r20 table advertising
  `[--audit-live-map]` (:2118). A C3 measurement executed on the lane before the registry candidate
  lands exits 2 / `CANNOT_EVALUATE` (`E-CLI`, unrecognized argument), not the preregistered 1/0
  pair. The before-run is only coherent with the final evaluator reading the BASE revision (whose
  highest table is round19 legacy → errors=1, exit 1); if the r20 SKILL table were committed into
  the before-revision, before would read 0.
- Exact-match calibration (accepted tradeoff): legitimate rewording of the verdict cell
  (punctuation, segment order, dropping `not operator clearance`) fails the green case; the
  evaluator is wording-coupled by design. A future legitimate map change requires updating
  `AUDIT_LIVE_MAP` and its selftest fixtures together.
- Scope limit (disclosed, not a gap in the candidate): the mode audits the registry cell only; it
  neither executes nor re-derives `boot-chain-audit.sh` at the revision (docstring :271-276, "not
  inference from arbitrary source"). A tool that one day actually emits live 1 is outside this
  mode's reach; the r20 row states this ("finite boot-chain-audit live/selftest map contract, not
  universal program semantics").
- Baseline cosmetic tally: r19 ledger recorded `PASS (12 cases, 13 passed, 0 failed)`
  (`.ufo/waves/round-19/measure/final/selftest-check-registry-coverage-py.stdout`) while baseline
  declares `total = 12` for 13 checks; the candidate's `total = 17` matches 13 carried + 4 new. The
  recorded after-tally should read 17 when measured.
- Nothing was executed here: no gates, selftests, imports, or host probes; expected values are
  source-derived, and measurement (`measure/run.py:72-74` c3 before/after) is L1's single pass.
  Overlap note: MapDuplicate.md (duplicate-heading CANNOT semantics) and OracleC3.md (fixed input
  classes) cover adjacent facets; this report adds the negation controls and the two-sided
  insufficiency argument.

Scope: executed=none
