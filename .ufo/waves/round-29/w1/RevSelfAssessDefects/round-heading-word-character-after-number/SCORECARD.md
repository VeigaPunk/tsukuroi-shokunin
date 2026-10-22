# Fixture scorecard

## Axes - fixture self-assessment (round 2)

| Axis | Score | Evidence pointer | Last change |
|---|---|---|---|
| depth | 8 | 2 notes (`ls corpus/knowledge/*.md`); `SKILL.md` 5 `wc -l` / 3 table lines (`grep -c '^|' SKILL.md`); `corpus/lessons/` 1 file | r1 |
| coverage | 9 | `corpus/README.md` rows stop at r1 (4 `wc -l`); `PROVINCE.md` Core, Frontier and Adjacent sections present | r1 |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` -> rc=0 `PASS (3 cases, 3 passed, 0 failed)`; Ceiling: D12 `--identity` landed | r1 |
| freshness | 9 | receipts | r1 |
| calibration | 9 | notes | r1 |
| adjacency | 8 | Ceiling: formal overlap table present | r1 |

## Round 1 measured outcome

- depth 8 -> 8
- coverage 9 -> 9
- operability 9 -> 9
- freshness 9 -> 9
- calibration 9 -> 9
- adjacency 8 -> 8

## Round 1x measured outcome

- depth 8 -> 3

## Capabilities

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | Curates `corpus/SOURCES.md` | `corpus/SOURCES.md` | r1 |
| host-census-gate | Emits a verdict with a hermetic 3-case `--selftest` | `bash tools/tsukuroi-census.sh --selftest` -> PASS 3/3 rc=0 | r1 |
| root-metadata-observer | Observes root mode | `corpus/knowledge/one.md` | r1 |
| boot-chain-audit | Audits boot entries | `tools/boot-chain-audit.sh` | r1 |
