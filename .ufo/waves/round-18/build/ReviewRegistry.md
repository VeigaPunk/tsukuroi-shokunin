# Registry/selftest falsifier

Axes reviewed: depth (correction/audit record), operability (gate registry), freshness (recheck registry); no ordinal change assessed. Round 18 pins baseline `842a5312b704b5cda10fd80ec1fdee5fb381ba97` and shared prerequisite `51dd9eeaa305539fa3cfc6ee275978dc18043b79` (SCORECARD.md:532).

## Findings

- **FAILS — boot-chain count.** `SKILL.md:1897` says 53; the latest committed receipt has 61 passed (`.ufo/waves/round-17/measure/final/selftests.txt:1`), identified as measured at `90037c2` in `SCORECARD.md:513,522`. The post-addenda 62 is only author-reported, not confirmed by that receipt (`corpus/lessons/round-17-verifier-spotcheck.md:109-111`). Evidence-backed replacement: 61; 62 remains **UNPROVEN**.
- **FAILS — audit count.** `SKILL.md:1898` and capability row `SCORECARD.md:164` say 44; receipt line 11 and `SCORECARD.md:520,522` say 45. Superseding field: `--selftest` 45 (45/45), not 44.
- **FAILS — revision-binding classification/denominator/count.** `SKILL.md:1902` calls it a probe, says all five, and gives 23 cases. The receipt says 28 (`selftests.txt:5`); C3 is the gate over all nine tools, with the legacy five tracked separately (`SCORECARD.md:519,522`). Superseding fields: gate; nine tools; 28 cases.
- **PARTIAL — recheck registry.** `SKILL.md:1900`'s 40-case count survives for the latest committed receipt (`selftests.txt:3`), but its command/contract omits the later `--exec-log`, `EXEC-STEER-VIOLATION`, and `exec_violation_count` extension (`SKILL.md:1916`; late run `.ufo/waves/round-17/measure/late/recheck.json:1`). The claimed post-addenda 43-case selftest is **UNPROVEN** by committed selftest evidence (`round-17-verifier-spotcheck.md:109-111`); no execution was performed here.
- **SURVIVES.** Freshness 53 and seat-scope 42 match receipt lines 2 and 4 (`SKILL.md:1899,1901`).

The same registry defects are already routed at `corpus/lessons/round-17-verifier-spotcheck.md:201-206`. `lsp` is not mounted (`xd://lsp` returned “No such tool”); no semantic LSP checks were available. No tests or other commands executed.

Scope: executed=none