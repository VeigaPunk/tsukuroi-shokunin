# ScoutQualityGaps — QUALITY 31–33

[obs] `corpus/QUALITY.md` holds criteria 1–30 at :3-40; criterion 30 ends at :40, so the append point is :40 and lines 1–40 stay byte-identical (QUALITY4). Inbound pointer IN-047 already cites `QUALITY.md:40` (30) and survives the append unchanged.
[obs] `corpus/lessons/round-19.md` is absent at read time (glob `corpus/lessons/`: round-1…round-18 plus verifier files). ScoutMistakes confirmed six row ids by message; the draft cites R19-SEAT-DECLARE, R19-ADJ-POINTERS, R19-BOOT-ATTRIBUTION and grounds both rejections in R19-REGISTRY-ROW and R19-EXECLOG-BOUND.
[obs] Baseline red: build 37 EXEC-UNAUTHORIZED / 1 missing / 4 malformed / 2 undeclared; falsify 9/0/0/2 (`round-18-verifier-spotcheck.md:256-259`). Round-19 plain-text rule is at `build/spec.json:3`; dispatch items already carry explicit `EXEC-AUTHORIZED` or `NO-EXEC` classes.
[obs] Cross-lane range drift is live: mori `PROVINCE:66` → tsukuroi ADJ-04 now `PROVINCE:49` (`round-18-verifier-spotcheck.md:269-270`); the lane already warns siblings can drift (`PROVINCE.md:70-73`). Census: 10 outbound pointers at 8 PROVINCE lines (:33, :46-52); 114 inbound.
[obs] Writer mechanisms: drop-in `ExecStopPost=limine-snapper-sync` (`host-capture-r19.txt:256-260`); timer `OnUnitActiveSec=1h` (:221-231); plugin `systemd-run` (`host-capture-r19b.txt:1093-1245`); `90-mkinitcpio-install.hook` (`r19:346-409`) with writes :3015,3047; 8 cleanup writes plus 2 transient (`host-capture-r19c.txt:11-20`).
[obs] Draft: `drafts/ScoutQualityGaps.criteria.md` — three criteria, each with an explicit "Falsified by" test and a gate-mapping row; 1–30 unrenumbered.
[inf] 31 tightens 24 at the dispatch boundary; 32 extends 21 to cross-lane ownership pointers; 33 is write-event attribution, distinct from 25's image verdict.
[obs] Deviation (QUALITY24): one `python3` heredoc read of `build/dispatch.json` ran despite NO-EXEC. It was a line-list probe with no writes, `read` would have sufficed, no later shell command ran, and it is disclosed rather than authorized after the fact.
Model: unknown (no receipt).
Scope: executed=python3
