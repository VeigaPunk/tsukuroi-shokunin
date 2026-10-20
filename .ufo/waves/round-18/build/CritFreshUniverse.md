# CritFreshUniverse — C3 freshness-universe attack

Verdict: claim wording SURVIVES the total-coverage attack; coverage binding
FAILS on two fixable defects.

## Universe resolution [obs]

Defect5 routes three planes file-scoped; the operative universe is the
FxUnflagged* statement lists (`.ufo/waves/round-17/falsify/`). Scribe targets
cover every routed statement: SKILL :118/:129-135/:1833; health :301-306,
:591-594; journal :147-149/:364-365; PSP :44/:75/:82/:90/:112/:143/:277-279/
:310; ARP :47/:48/:98/:103/:197; FPR6 :29-37/:47/:55/:194; oom :51/:280/:346/
:349/:384; kill :256/:259/:265.

## Counterexamples

1. **U1 siblings in routed file un-noticed** [obs].
   `corpus/knowledge/host-health-report-r3.md:35` "no rollback net (U1/J4)",
   `:53` U1 table row "snapshot-less is the standing exposure for any wave",
   `:290` "snapshot-less; re-audit (cross-ref U1)". Same stale fact as routed
   :301-306; `:53` is literally the U1 finding row — inside defect5's "U1"
   scope, yet untargeted. Notice supersedes only quoted lines; stale U1
   guidance remains unmarked in the summary table.
   Smallest safe correction: NoticeHealth quotes or names :35/:53/:290 as
   superseded siblings, or the report discloses them as residual.

2. **Gate measures registry self-consistency, not routed coverage** [obs,
   spec `build/spec.json` BuildNoticeGate]. Per-record quote/heading/capture
   checks only; no distinct-path census, no routed-statement checklist.
   `resolved_records 0→N` passes with one file and N=1. ConnFreshCoverage's
   enumeration is advisory, not wired into the measurement. Correction: C3
   measurement publishes routed-item → record-id map and path census == 8.

## Surviving basis

- Wording self-scoped ("in eight named files"); r17 dated-capture exemption
  (FxUnflaggedMem) consistently leaves dump/census cells (oom:85, kill:191,
  ARP :41/:62-77) historical.
- No total-host-coverage implication found in SCORECARD C3 row or context.

Scope: executed=none
