# Round 32 — pre-data control receipts (scored before any data seat)

All receipts are `tools/run-receipt.py` receipts (header revision, tool_sha256; footer exit_code). C1 counter v2 = `tools/score-census-handoff-r32.py` at `f28442cb` (sha256 d6a8f07a…); v1 at `fe1ae02c` (b2edc669…). C2 probe = `tools/probe-child-env-allowlist-r32.py` at `fe1ae02c` (2521711b…, unchanged at f28442cb). Target C1: routed 24 of 24, live_consistent true, exit 0. Target C2: leaking 0 of 11, exit 0.

| Control | Claim | What it skips / how it cheats | Receipt | Result | Meets target? |
|---|---|---|---|---|---|
| K0 do-nothing (base census) | C1 | no routing | `measure/c1-before-v2-f28442cb….jsonl` | routed 10/24, live false, exit 1 | no |
| K1 always-emit | C1 | constant lines | `w1/CtlC1AlwaysEmit/K1-always-emit-v2.jsonl` | 0/24, exit 1 | no |
| K2 cumulative-keyed | C1 | ledger counter, total error count | `w1/CtlC1CumulativeKeyed/K2-cumulative-keyed-v2.jsonl` | 9/24, exit 1 | no |
| K3 plane-verdict-keyed | C1 | value=1 on non-HEALTHY | `w1/CtlC1PlaneKeyed/K3-plane-keyed-v2.jsonl` | 9/24, exit 1 | no |
| K4 junk | C1 | random well-formed lines | `w1/CtlC1Junk/K4-junk-v2.jsonl` | 0/24, exit 1 | no |
| K5 peek (expected-set leak) | C1 | — | none: seat CtlC1Peek ended on a safety-filter refusal (hold) | — | not built |
| K6 no-reader line counter | C1 | counts fixture lines, no class reading | `w1/CtlC1LineCounter/K6-line-counter-v2.jsonl` | 22/24, live false, exit 1 (under v1 the seat saw 24/24 on one seed: `w1/CtlC1LineCounter/`) | no under v2 |
| K7 hand-off-and-forget | C1 | changes the journal PLANE line | `w1/CtlC1ParityBreak/K7-parity-break-v2.jsonl` | 15/24, exit 1 | no |
| K9 fixture-gated (L1-built from the CritPredicateC1 idea) | C1 | routes only when the scorer's `.dispatch` stub is present | `controls/L1/K9-fixture-gated-v1.jsonl`, `controls/L1b/K9-fixture-gated-v2.jsonl` | v1: 24/24 exit 0 (the reason for v2); v2: 24/24, live false, exit 1 | v1 yes, v2 no |
| K8 positive (minimal genuine routing) | C1 | does the work | `w1/CtlC1Positive/K8-positive-v2.jsonl` | 24/24, live true, exit 0 | yes (positive control) |
| H0 do-nothing (base tools) | C2 | deny-list | `measure/c2-before-fe1ae02c….jsonl` | 11/11, exit 1 | no |
| H1 deny-list + the four named | C2 | keyed on the probe's fixed names | `w1/CtlC2DenyNamed/H1-deny-named-L1.jsonl` | 11/11, exit 1 | no |
| H2 hollow (exit when BASH_ENV) | C2 | skips work | `w1/CtlC2Hollow/` | 1/1 leaking by parity, exit 1 | no |
| H3 value-keyed | C2 | keyed on values | `w1/CtlC2ValueKeyed/H3-value-keyed-L1.jsonl` | 11/11, exit 1 | no |
| H5 empty environment | C2 | none: passes zero ambient names (the strictest allow-list) | `w1/CtlC2EmptyEnv/H5-empty-env-L1.jsonl` | 0/11, exit 0 | yes — classed as a positive control: it does the claimed work (no ambient name reaches a child) and keeps parity, as ScoutSpawnSitesR32 predicted (children need no ambient name) |

H4 (shape-keyed) and H6 (ten-of-eleven partial) are scored by their seats; their receipts are added when they return.

## Update — final counters (appended; wave-2 RevControlsReceipts)

The table above was written under C1 v2 and probe v1; H4 and H6 have since returned. The receipts that bind the claims are the ones under `final/`, scored with C1 scorer v3 (`f45136c3…`) and C2 probe v2 (`d43f95ed…`) at tool revision `44c8eee5`, all committed before the first data seat: C1 K0 8/24, K1 0, K2 9, K3 9, K4 0, K6 24 (live false), K7 12, K9 24 (live false), K10 24 (live false), all exit 1; K8 24, live true, exit 0. C2 H0 11/11, H1 11, H2 11, H3 11, H4 11 (the v1 shape-keyed pass is killed by v2's long names), H6 1, all exit 1; H5 0/11, exit 0 (positive control: the strictest allow-list).

Post-data control (wave 2, does not bind the claim): `postdata/K10b/K10b-cached-live-current.jsonl`, a fixture-gated census that prints the host's current live values (kill-events 2, coredumps 187) outside fixtures. Plain live view consistent, filtered view inconsistent (124 expected), exit 1: the thinned view is the conjunct that refuses a cache of current values (wave-2 RevQuality82 had noted K10's receipt did not isolate it).

## Erratum (appended round 33, attempt 3, 2026-10-23; round-32 spot-check routed defect 4)

The "Update — final counters" paragraph above (line 27) says the final control receipts were "all committed before the first data seat". That holds per claim only. The C1 controls (`462e40a7`, committed 2026-10-22T22:59:46-03:00 by `git log -1 --format=%cI 462e40a7`) precede the C1 data seat ExecHandoffCensus (dispatched 22:59:51-03:00); the C2 controls (`4e685163`, 23:05:54-03:00) precede the C2 data seats ExecAllowA and ExecAllowB (23:06:02-03:00) but follow the C1 data seat's start. Seat dispatch times: `corpus/lessons/round-32-verifier-spotcheck.md` section 1, "Conformance defects" and the §9 ruling. The paragraph above stays as written.
