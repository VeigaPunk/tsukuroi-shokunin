# C3 — selftest-1 versus live-1 fixture design

## Evidence

- Preregistration pins baseline `0cbc34dd6b20896085a8fb07943e3ea4027d8472`, C3 metric `audit_live_map_errors`, and expected behavior: legacy live `1` → exit 1 / `REGISTRY-AUDIT-LIVE-MAP`; corrected map → exit 0 / `audit_live_map_errors=0`; selftest-only `1` is allowed; historical-row-only correction still fails.
- The selector is `_operative_rows()` in `tools/check-registry-coverage.py:133-179`: it chooses the unique maximum-numbered exact registry heading, parses only that section, and raises `TableError` for a duplicate highest heading; it does not fall back to an older table. Existing `unique-highest-table` selftest (`:490-496`) establishes historical rows are ignored, but does not test the C3 map semantics.
- The registry evidence illustrates the distinction: the historical round18 boot-chain-audit row says live `0/2` (`SKILL.md:1965`), while the round19 operative row says `0 CONSISTENT;1 DEGRADED;2 UNKNOWN` (`:2073`). The source explicitly says schema-v2 emits no live `1` (`tools/boot-chain-audit.sh:81-85`); live summary logic returns only `0` or `2` (`:795-801`), while failed selftest assertions return `1` (`:1216-1221`).

## Proposed fixture delta (design only; no runs)

Build a synthetic `SKILL.md` containing a corrected round18 historical boot-chain-audit row and a round19 operative row. Include a regular synthetic `tools/boot-chain-audit.sh` blob so the row has its tool target; its bytes are fixture data only.

1. **Historical-row-only fix / forbidden live-1:** leave the round19 Verdict map at `0 CONSISTENT;1 DEGRADED;2 UNKNOWN`; keep its Self-test cell `0 PASS;1 FAIL`; make only round18 correct (`live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate`). `--audit-live-map` must fail on the selected round19 row: exit `1`, finding ID `REGISTRY-AUDIT-LIVE-MAP`, `audit_live_map_errors=1`. A missing boot-chain-audit row in round19, with the corrected historical row retained, must likewise fail with that ID rather than borrowing the historical row.
2. **Selftest-1-only / corrected live map:** change the selected row’s Verdict map to `live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; no live DEGRADED; not operator clearance`. Expect exit `0`, `audit_live_map_errors=0`, and no `REGISTRY-AUDIT-LIVE-MAP` finding.

The check must select the unique highest table first, identify the boot-chain-audit row there, and classify the **Verdict map cell’s live clause separately from the Self-test clause**. Merely finding a corrected historical row misses the bad operative row; merely requiring digits `0` and `2` accepts the legacy row, which already contains both; rejecting any `1` anywhere falsely rejects the corrected row because selftest failure legitimately uses `1`. These are finite registry fixtures, not proof of arbitrary program semantics or host/boot safety.

Report path: `.ufo/waves/round-20/build/MapSelftestOne.md`
Scope: executed=none