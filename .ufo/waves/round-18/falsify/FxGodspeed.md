# FxGodspeed — documentation/integration falsification

## Findings
No actionable defect established.

- **SURVIVES — dispatch count/band.** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-18/falsify/dispatch.json:8-19` declares wave bounds 64–100 and spawn/total 76; its `taskCall.tasks` contains 76 entries (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-18/falsify/dispatch.json:492-875`), and `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-18/falsify/spawn-result.json:2` says “Spawned 76 background agents.” Count is ≥75 and within band. No standalone validator-output record was observed, so validator provenance is **UNPROVEN**.
- **SURVIVES — dispatch role counts.** JSON projection of all `taskCall.tasks[].agent` (and registry members, `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-18/falsify/dispatch.json:25-482,492-875`) agrees: reviewer 55, scout 7, mutation-tester 4, connector 3, critic 3, revenger 2, sentinel 1, simplifier 1 (76 total). The settled round report’s role-table comparison remains **UNPROVEN**; final ledger/report is pending per `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-18/falsify/spec.json:3`.
- **SURVIVES — Godspeed bytes/exact-once.** Across all 76 actual task-call strings (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-18/falsify/dispatch.json:494-875`), each begins `/skill:godspeed\n\n` plus the same 429-byte directive (including terminal LF), and contains that directive exactly once.
- **SURVIVES — report root.** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-18/falsify/spec.json:3-4` supplies the absolute lane root and relative reportDir `.ufo/waves/round-18/falsify`; resolving it gives `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-18/falsify`. This report is written at its absolute assigned path. Final wave-wide report paths remain pending.
- **SURVIVES — no dead-seat replacement.** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-18/build/outcome.json:17-23` records RerunExecLog’s `invalid_prompt` death and `"replaced": false`; no such member exists in the falsify dispatch registry.

## Residual risk / verification gaps
No execution performed; the independent validator output, final role-table/report reconciliation, and settled final execution ledger remain unverified. These are pending, not passes.

Scope: executed=none