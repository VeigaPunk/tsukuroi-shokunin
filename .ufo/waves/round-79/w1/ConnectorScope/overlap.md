# Sibling Overlap and Province Boundary Scan — Round 79 Wave 1

## Objective
Grep sibling repos under `/home/vgpnk/Projects/shokunin` (kumitate, kotodama, chousa, kama, mado, mori, kagi, kaidoku, revenger, tabi, souji, kensei/kengaku) for `BindsTo=`, `PartOf=`, `Upholds=`, `RequiresMountsFor=`, `unit dependency`, `systemd.unit`, classify each hit as `owned-by-tsukuroi` (unit state/triage), `contested`, or `sibling-owned`, and record evidence pointers.

## Methodology & Execution
Examined all present sibling repositories:
- `kumitate-shokunin`
- `kotodama-shokunin`
- `chousa-shokunin`
- `kama-shokunin`
- `mado-shokunin`
- `mori-shokunin`
- `kagi-shokunin`
- `kaidoku-shokunin`
- `revenger-shokunin`
- `tabi-shokunin`
- `souji-shokunin`
- `kengaku-shokunin` (`kensei-shokunin` is not present on disk; `kengaku-shokunin` is present)

Grep targets:
1. `BindsTo=`
2. `PartOf=`
3. `Upholds=`
4. `RequiresMountsFor=`
5. `unit dependency`
6. `systemd.unit`

## Exact Match Results
A strict grep over `PROVINCE.md` and `SKILL.md` across all 11 present sibling repositories yields **0 hits** for the exact strings.
Furthermore, a whole-tree scan across all markdown files across all sibling repositories also yielded **0 hits**.

By contrast, in `tsukuroi-shokunin`:
- `systemd.unit` appears in `PROVINCE.md:491`, `SCORECARD.md:6603`, `LOG.md:7386`, `corpus/SOURCES.md`, `corpus/knowledge/systemd-unit-load-plane-r73.md`, `tools/count-ul-rows-r73.py`, and `tools/measure-unit-deps-r79.py`.
- `BindsTo=`, `PartOf=`, `Upholds=`, `RequiresMountsFor=` appear in `SCORECARD.md:6606-6608`, `LOG.md`, and `tools/measure-unit-deps-r79.py`.

## Broader Semantic Scan & Province Boundary Classification
Scanning for looser variants (`systemd unit`, `unit` state, `systemd` service) across sibling `PROVINCE.md` and `SKILL.md` files reveals extensive explicit province boundary definitions that unanimously confirm tsukuroi's sole ownership:

| Sibling Repository & Location | Matched Text / Context | Classification | Evidence Pointer / Analysis |
|---|---|---|---|
| `mori-shokunin/PROVINCE.md:13` | "systemd unit, driver/firmware and boot state (→ tsukuroi) — mori reads journal" | `owned-by-tsukuroi` | Mori explicitly delegates host OS, systemd unit, and boot diagnosis outward to tsukuroi. |
| `mori-shokunin/PROVINCE.md:66` | "\| tsukuroi \| Owns host OS, package, systemd-unit, driver, firmware, and boot diagnosis." | `owned-by-tsukuroi` | Direct province statement assigning all systemd-unit ownership to tsukuroi. |
| `mori-shokunin/SKILL.md:33` | "\| fleet vs non-fleet unit failure \| generic severity is info on both sides: fleet UNIT_FAILURE_JOURNAL" | `owned-by-tsukuroi` | Mori routes non-fleet unit failures to tsukuroi. |
| `mori-shokunin/SKILL.md:143` | "- **Refuses OS-package state** — pacman/systemd units/drivers/firmware/boot are (→ tsukuroi)" | `owned-by-tsukuroi` | Explicit refusal of systemd units; mapped to tsukuroi. |
| `mori-shokunin/SKILL.md:370` | "to `~/.config`, `~/.omp`, or systemd units ... the operator repoints them" | `owned-by-tsukuroi` / operator | Unit modification write boundary is operator-owned; diagnosis is tsukuroi's. |
| `mori-shokunin/SKILL.md:375` | "\| 1 — triage/diagnosis \| read-only domain specialist \| `tsukuroi` (OS substrate, units, drivers)" | `owned-by-tsukuroi` | Mori's routing table places unit diagnosis under tsukuroi. |
| `mori-shokunin/SKILL.md:384` | "`UNIT_FAILURE_OUT_OF_SCOPE` is the Tier-1 pointer for a non-fleet unit failure: `severity=info`, `owner=tsukuroi`" | `owned-by-tsukuroi` | Structural protocol routing non-fleet unit failures directly to tsukuroi. |
| `mado-shokunin/PROVINCE.md:483` | "Unit health remains tsukuroi's, mutation craft..." | `owned-by-tsukuroi` | Mado explicitly defers unit health to tsukuroi. |
| `mado-shokunin/SKILL.md:252-254` | "unit-state reads establish prerequisites, with OS diagnosis retained by tsukuroi" | `owned-by-tsukuroi` | Mado reads unit state solely for display prerequisites; OS diagnosis belongs to tsukuroi. |
| `kama-shokunin/PROVINCE.md:47-48` | "**Write boundary (hard):** kama never writes to `~/.config`, `~/.omp`, or systemd units. Those are operator-owned; kama detects and reports stale pins..." | `owned-by-tsukuroi` / operator | Kama strictly refuses unit writes or service restoration. |
| `kama-shokunin/SKILL.md:21, :84, :346` | "systemd unit moved the listener to `--port 34113`", historical citations | `owned-by-tsukuroi` / operator | Kama observes port bindings and unit files as historical citations; does not manage or diagnose units. |
| `kengaku-shokunin/SKILL.md:775` | "systemd unit, chat template) is absent per the receipt" | `sibling-owned` (fixture citation) | Kengaku references historical unit presence/absence in its model test receipt, not as unit diagnostic authority. |
| `kumitate-shokunin/SKILL.md:620, :738` | "`cap-run` ... needs `systemd-run --user`" | `sibling-owned` (tool substrate) | Kumitate invokes `systemd-run` purely as a resource-capping subprocess execution runner, not as unit configuration or dependency modeling. |

## Conclusion
1. **Contested Claims:** Zero (0). No sibling claims ownership or attempts to parse or define systemd unit dependencies (`BindsTo=`, `PartOf=`, `Upholds=`, `RequiresMountsFor=`, `Wants=`, `Requires=`, `Requisite=`, `After=`).
2. **Tsukuroi Province Authority:** Tsukuroi holds undisputed ownership over systemd unit load (`R73-UNIT-LOAD-VIEW`), unit fragment resolution (`R74`), job transactions (`R75`), and dependency propagation (`R79-C1`).
3. **Boundary Integrity:** Siblings (`mori`, `mado`, `kama`) maintain clean, unidirectional boundary pointers assigning all host OS unit triage and health diagnosis to tsukuroi.
