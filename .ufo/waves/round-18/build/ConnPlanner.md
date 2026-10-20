# ConnPlanner — ten routed r17 defects

Axes: depth C1, operability C2, freshness C3, routed-debt closure, registry separability. Model grok-4.7-fast. Installs: none.

[obs] `round-17-verifier-spotcheck.md:191-231`; claims `SCORECARD.md:536-539`; 81 seats; build wave `dispatch.json:3`.

1. **Supporting.** FinalR17Outcome → `drafts/round17-outcome-final.json`. ReviewReportCoverage classifies cca3343/661020f. RevOutcome traces 29/16. Fleet report stays outside lane writes.
2. **Claim C2.** Six probes [obs] `check-revision-binding.py:26-33`; order [obs] `_revision.py:11-24`; judge independent [obs] `:9-10`. Nine Mig* seats; MutateShared/MutateJudge cover them.
3. **Claim C1.** NoticeBootCorrections + ReviewPackageCount/UkiCites/Mtime. [obs] `boot-chain-r17.md:19` “13 named packages”; `:40-46`; `:88` mtime via B:115. Split of `:40-46` is in the scribe prompt (four records; floor 3). No BootChainTruthR17 path. L1 builds `statement-corrections-r18.json` (`SCORECARD.md:537`).
4. **Repair unassigned.** ReviewRegistry, RevRegistryHistory, CritMistake, CritNoHarm attack or trace only. [obs] `SKILL.md:1897` “53”, `:1898` “44”, `:1900` omits `--exec-log`, `:1902` “five”/“23”; `SCORECARD.md:164` `44/44` vs `:520` `45/45`.
5. **Claim C3.** Eight scribes, eight files (`SCORECARD.md:539`). Sweep01–14 are other files.
6. **Supporting.** MigRecheck, NoticeAur, ReviewPointer. [obs] pointer `aur-risk-plane.md:347`. Heading only `## R17-RECHECK — steer-safe procedure` (`check-recheck-commands.py:36`).
7. **Harness half unassigned.** [obs] `exec-log.txt:5` (`pacman -Q`); limit `round-17.md:43`. RerunExecLog grades `host-capture-r18.txt`, an L1 script transcript (`capture-r18.sh:3-4`). A clean rerun leaves defect 7 open [inf].
8. **Remeasure assigned; lesson numeral unassigned.** [obs] `seat-r17-build.json` count 30 (`revision: worktree`); falsify 16; `round-17.md:45` says 29. RerunSeats uses `842a531`. No lesson-append seat.
9. **Read-only re-attack.** ReviewSeparability17, ReviewReadme, ReviewFrozen, ConnSibling.
10. **Nonlane.** Closure `:227-231`. No route-map seat.

**Move.** C1 JSON: boot-chain `## R18-CORRECTION` only. C3 JSON: eight `## R18-FRESHNESS` files; Sweep01–14 stay out. aur-risk also gets `## R18-RECHECK — steer-safe procedure`, outside the C3 registry. Keep `SKILL.md:1897-1902` and `SCORECARD.md:164` out of both until a non-claim append exists.

**Risk.** MigRecheck’s pointer edit is inside a C2 file. Journal `:244-245` and health `:591-594` are extra lines in assigned files.

**Verify.** C1 ids: package count, two UKI cites, mtime. C3 paths: the eight. aur-risk has both headings.

Scope: executed=none
