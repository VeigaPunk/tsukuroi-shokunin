source: S083 — .ufo/waves/round-22/snapshot/corpus/lessons/round-21.md § R21-SCOPE-RECUR and retained request audit; S084 — .ufo/waves/round-22/sources/host-tool-boundary.json fields tools_semantics/native_per_seat_allowlist/approved_scope
verified-at: 2026-10-21; immutable baseline 894d1e20fb4939b0cc4fadf722c46d1429f257d2 and round22 predispatch415ac3a834a1d7fa5b09986463512579af65d28e; final measured revision recorded in SCORECARD
recheck: python3 tools/check-boundary-contract.py --revision <landed-hex>

# Seat boundaries for read-only host-evidence work

These are six finite lane-policy decisions motivated by observed scope contradictions, not six discovered runtime capabilities. S083 records a forbidden Bash `true` request and starts before provider failures; S084 records the exposed dispatch semantics and Main's explicit decision that no native per-seat allowlist exists. Local source-only work must not silently widen into host probing or external fetching. The current steer's six fetch calls/two seats remain historical debt, separate from thirteen Bash starts/nine seats; no historical check is rerun to clear either.

## Decision table

| ID | Surface | Decision | Reason | Source |
|---|---|---|---|---|
| NO_EXEC | bash/eval/task | DENY | No execution or delegation in source-only seats | S083 |
| NO_FETCH | URL read/web_search/browser | DENY | Local source reads never authorize network fetches | S083 |
| LOCAL_READ | read/grep/glob declared local paths | ALLOW | Only literal bound source paths and approved skill URI | S084 |
| REPORT_WRITE | write exact report path | ALLOW | No other write; executor draft exception must be explicit | S083 |
| UNKNOWN | unrecognized tool or malformed arguments | DENY | Fail closed; incomplete metadata is not command absence | S083 |
| DEAD | missing final or provider death | UNKNOWN | No report is not evidence of no earlier tool calls | S083 |

## What is enforced and what is not

A prompt-level binding fixes exact read/write paths and empty command/fetch lists before dispatch. Seats are instructed never to invoke other tools, commands, or URLs. The request auditor compares recorded requests against those bindings and fails closed on unknown tools, malformed data, unmatched seats or unavailable trace coverage. This is **post-hoc detection, not preventive runtime enforcement**. Main confirms `task.tools` adds eval-defined tools; it is not a native-tool allowlist. No native toolset restriction, OS sandbox, arbitrary-shell semantic equivalence, proof of actual reading, or proof of request effects is claimed.

The literal `Scope: executed=none` is still required by the existing strict receipt contract. An observed forbidden request contradicts that declaration regardless of whether its command is harmless or whether the seat later dies. Original reports remain unchanged; contradictions are separate findings. Cohort accounting partitions the fixed declared population into delivered-conformant, delivered-faulty, absent-dead, and absent-unresolved. Clean accounting is never a clean strict receipt verdict or permission to waive a failed receipt.

## Checklist

1. Freeze source snapshots, exact review predicates, literal seat bindings and declared population before dispatch; acquire/check current wave headroom.
2. Every seat reads only its bound local source/skill paths and writes only its exact report or named separate-worktree draft. Empty commands/fetches means no exceptions for hash/list/test/source checks.
3. After settlement, preserve raw report bytes, observed error attribution and sanitized request metadata. Mark incomplete trace coverage could-not-evaluate, not zero activity.
4. Report actual request violations, strict receipt faults and cohort accounting separately. Never replace failed seats, repair historical report lines, drop a denominator or label prompt compliance runtime prevention.

## QUALITY check

Criteria1–5: finite falsifiable decisions, observation/policy/unknown separated and historical rejects retained. Criteria7/19: S083 is scoped own-work evidence; S084 is the exposed schema plus Main host decision, not an implementation audit. Criteria24/31/42/44/46: narrower NO-EXEC/NO-FETCH, immutable bindings, dead-seat visibility and actual request precedence. Original errors remain red; new checks require fixed negative fixtures before their improvement counts. This deepens held evidence-operability ground; no province, host-recovery authority, new frontier, outside admission or promotion is acquired.
