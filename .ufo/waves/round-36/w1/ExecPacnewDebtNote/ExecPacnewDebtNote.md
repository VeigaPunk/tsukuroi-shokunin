# ExecPacnewDebtNote — routed debt 3b

## Result

Read-only assessment complete. No production code, counter, census, corpus or shared state was changed. Created the future-reclaim requirement document at `v3-requirements.md` in this seat directory.

The recorded decision is **no pacnew claim or re-claim in round 36**. The round-36 declaration says routed debt 3b (the pacnew VERSION 3 counter) is not owed this round and directs the requirements from the named wave-2 reports into the future freeze condition (`SCORECARD.md:1673-1677`). Round 35 did not verify C1: W2TreeKeyed and W2LogKeyed met V2's 24/24 after-value; W2LiveOracle later added two more 24/24 live-gate controls; V2's battery also missed ctime/live-view mutations (`corpus/lessons/round-35.md:36,44,64`; `SCORECARD.md:1553-1556`).

## Files changed

- `.ufo/waves/round-36/w1/ExecPacnewDebtNote/v3-requirements.md` — enumerated future V3 claim/freeze criteria with evidence paths and explicit evidence gaps.
- `.ufo/waves/round-36/w1/ExecPacnewDebtNote/ExecPacnewDebtNote.md` — this scoped report.

## Retained evidence consulted

- `corpus/lessons/round-35.md:36,44,64`: V2 control outcomes, forced-shape mistake and later live-gate controls.
- `SCORECARD.md:1536-1556,1673-1677`: frozen kill rule, V2 claim outcome and explicit no-reclaim decision.
- `.ufo/waves/round-35/w2/W2MutCounter.md:4-11` and receipts `W2MutCounter/drop-ctime.jsonl`, `skip-live-view.jsonl`: ctime and live-view counter mutations survived the declared detection measure.
- `.ufo/waves/round-35/w2/W2ArmAuditA.md:11-19`, `W2ArmAuditA/probe-mutated.jsonl`, `base-top-level-valid.json`, `base-suffix-not-basename.json`, and `../l1/dev-v2-run2-base.jsonl`: F04 contamination and F07 collateral FIFO loss.
- `.ufo/waves/round-35/w2/W2ArmAuditB.md:21-30`, `W2ArmAuditB/assigned-battery-summary.json`, `control-oracle-input-classes-continued.json`, `control-oracle-special-locked-name.json`, and `unreadable-diagnostics.json`: F14 ctime evidence and eight control/oracle disagreements.
- `.ufo/waves/round-35/w2/W2RevCounterV2.md:3-9`: count-only live integrity, locked-child ctime, collision safety and preflight-schema review findings.
- `.ufo/waves/round-35/w2/W2SentinelViews.md:5`: malformed DRIFT value can enter parser reasons and receipts.
- `.ufo/waves/round-35/w2/W2LiveOracle.md:80-104` and the committed `livecache-variant.jsonl`, `cwdgate-variant.jsonl` receipts: two host/cwd-keyed controls met V2 live-view after-value.
- `.ufo/waves/round-35/w2/W2TreeKeyed/variant.jsonl` and `W2LogKeyed/variant.jsonl`: each keyed patch met V2's after-value.

The referenced round-35 receipt artifacts are retained in the repository's committed tree. No evidence was generated or re-scored by this seat.

## Risks and evidence gaps

- `[inf]` W2SentinelViews identifies raw-token exfiltration by source-path analysis; no malformed-token canary receipt is retained. The requirements call for a safe synthetic canary receipt in a future V3 assessment.
- `[inf]` W2RevCounterV2's locked-descendant ctime, live-tree write detection, fixture-collision and preflight-schema findings are review findings, not direct runtime receipts. W2MutCounter did directly demonstrate the drop-ctime/live-view mutation-survival problem.
- The eight audit inputs are marked `development_only`; they record disagreements, not V3 behavior or a passed independent oracle.
- No build, tests, lint, formatter or counter run was performed; this was a read-only requirements assessment. No tool was installed.

## Blockers

None for this scoped documentation deliverable. The future re-claim is blocked on satisfying and freezing the V3 requirements; this seat did not implement or verify them.
