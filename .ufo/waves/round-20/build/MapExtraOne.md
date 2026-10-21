# C3 extra-live-code1 mutation design

## Finding
No actionable gap found in this assigned mutation scope by static inspection. The candidate registry checker already contains the required extra-live-`1 DEGRADED` fixture; it has not been executed here.

## Baseline and contract evidence
- C3 is calibration. The preregistered outcomes require `legacy_live_1` → `REGISTRY-AUDIT-LIVE-MAP`, exit 1; corrected map → `audit_live_map_errors=0`, exit 0; and a historical-row-only fix → `REGISTRY-AUDIT-LIVE-MAP`, exit 1 (`.ufo/waves/round-20/preregister.json:49-53`).
- The baseline tool’s selector is `_operative_rows`: it finds the unique highest-numbered exact registry heading and returns only that table’s rows (`tools/check-registry-coverage.py:133-145,147-179`). Its committed-source reader reads `SKILL.md` from the bound revision (`tools/check-registry-coverage.py:86-103`).
- Baseline round18’s boot-chain-audit row already says live `0 CONSISTENT;2 UNKNOWN` and that `1` is only a selftest assertion failure (`SKILL.md:1965`), but the operative round19 row still says `0 CONSISTENT;1 DEGRADED;2 UNKNOWN` (`SKILL.md:2060-2073`). The round20 erratum records that only the historical row had been corrected (`SKILL.md:2086-2088`).
- The audit’s documented schema-v2 exit map says `1 DEGRADED` is retained vocabulary but no v2 verdict maps to it; exit 1 is never emitted under this schema (`tools/boot-chain-audit.sh:81-86`).

## Fixture delta and exact expectation
Use the corrected live map, preserving its selftest mapping, and insert one additional live mapping: `live: 0 CONSISTENT/observation;1 DEGRADED;2 UNKNOWN/could-not-evaluate; ...`. The expected CLI result is **exit 1**, exactly one `REGISTRY-AUDIT-LIVE-MAP` finding, and `audit_live_map_errors=1`.

This delta is already represented in the candidate checker’s fixture source: it inserts `1 DEGRADED` into the corrected live map (`/tmp/tsukuroi-r20-registry-20261021/tools/check-registry-coverage.py:565-574`) and asserts `FAIL`, error count 1, and exactly the `REGISTRY-AUDIT-LIVE-MAP` ID (`:583-590`). Static code also compares the selected audit row’s verdict cell to the finite mode-labelled contract (`:260-287`). No selftest or command was run.

## Why weaker checks are insufficient
- Checking for digits `0` and `2` (or merely requiring the probe’s usual codes) passes this mutation: both digits remain present. It does not bind a code to the live versus selftest mode. Code `1` is permitted for selftest `FAIL`, never as live `DEGRADED`; therefore the check must reject this extra *live* mapping while accepting the separate selftest `1 FAIL` mapping.
- Accepting any historical row also gives a false pass: round18 has the corrected map while the then-operative round19 row still advertises live `1 DEGRADED`. The checker must apply the finite semantic check only to the unique highest operative table. The candidate selftest separately pins this distinction: corrected older row plus legacy operative row must fail (`:604-613`), consistent with the preregistered historical-row-only expectation.

## Residual risk and verification gap
This is a finite registry-cell contract, not proof of arbitrary script semantics or current host/boot readiness. The cited candidate fixture and assertions are source inspection only; no runs were performed.

Scope: executed=none
