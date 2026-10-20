# Round-17 outcome reconciliation

[obs] Dispatch was 81 (`.ufo/waves/round-17/falsify/dispatch.json:16-19`). `outcome.json` is timestamped `2026-10-20T14:43:09`; it records 29 delivered, 36 provider-429 labels, and 16 still running at landing, with one aggregate retry-exhaustion error (`.ufo/waves/round-17/falsify/outcome.json:14-73`). Its fields describe a landing snapshot, not final completion.

[obs] The later committed-byte census is 37 report files and 44 dispatch items without reports: 29 + 8 later deliveries; 36 named 429 deaths + 8 later absent (`corpus/lessons/round-17-verifier-spotcheck.md:89-95`). Late deliveries were FxBindSectCita, FxC2Rerun, FxConnUnknowns, FxMdJsonAgree, FxOwnS055, FxSimplifyBind, FxSourcesContract, FxSteerScopeFix. The derived reconciliation lists the eight still-absent from the landing set (`.ufo/waves/round-18/build/drafts/round17-outcome-final.json:203-222`). FxGodspeedW2 was already among the interim 29, despite an addendum calling it late (round-17 lesson:91-95).

[inf] The count froze because there was no final tally reconciliation after landing: round-18’s routed defect names “PROTOCOL lands-last; no round-local final tally reconciliation,” and directs preserving the interim snapshot while appending a final derived result (`corpus/lessons/round-18.md:33,37`). The exact writer/update trigger is not established here.

[obs/unk] The persisted registry and record-result each have 81 members with only `kind`, `agentId`, `role`, `item` fields (`.ufo/waves/round-17/falsify/record-result.json:8-495`; `swarm-registry.json:7-494`). Therefore the 36 429 causes are aggregate outcome labels, not individual provider receipts. For the other eight absent seats the final tree establishes no report file, not an individual 429 cause (`round17-outcome-final.json:226-230`).

Confidence: high on the snapshot/final-count mismatch; inferred protocol cause; unknown individual causes for the eight absent seats.

Scope: executed=none