# tsukuroi-shokunin — 繕

The question this lane answers is what state the OS substrate is in — packages, systemd, drivers and firmware, boot — and whether that state can be assessed from an unprivileged shell (`PROVINCE.md`, `tools/tsukuroi-census.sh`).

**Rank:** `SHONEN.md` boxes are `[~]`, each labeled author-side evidence, with non-author verification still owed. That is not a promotion.

## Owns / refuses

Owns read-only probes of pacman state, systemd user units and timers, journal and boot triage, and the driver and firmware plane, plus the question of what an `-Syu` would touch (`PROVINCE.md`).

Refuses endpoint and model-serving health (kama), secrets (kagi), and binary reverse engineering of drivers (kaidoku and revenger). This lane tracks state and health, not internals. It never installs, upgrades, removes packages, or restarts services. The operator remediates (`PROVINCE.md`).

Host memory and kill events support OS triage. They do not say which fleet wave caused pressure. That correlation belongs to mori (`PROVINCE.md`).

## Start here

`tools/tsukuroi-census.sh` can run as a live host census. That path is read-only (the header: it never installs, upgrades, removes, restarts, or writes). Prefer the hermetic self-test, which writes only under its temp directory:

```sh
bash tools/tsukuroi-census.sh --selftest
```

Usage text: no flags means the live census; `--sample N` bounds the pacman sample (default 8); verdict `TSUKUROI_CENSUS: HEALTHY|DEGRADED|BLOCKED`; exit `0` / `1` / `2`. `corpus/README.md` records earlier self-test and live verdicts as historical rows. Do not treat those rows as this host, today.

## How to read the corpus

`corpus/README.md` is the coverage map. Its sha256 is pinned in `.ufo/evidence/fleet-r1-interactive/inherited.json` and in the preservation check, and knowledge notes cite lines such as `corpus/README.md:11` through `:15`. It was not edited. The v1 census row is explicitly superseded by the v2 row inside that file. `corpus/knowledge/adjacency-handoffs-fleet-r1.md` is the handoff packet. `corpus/QUALITY.md` is the admission bar.

## Map

| Path | What it is |
|---|---|
| `PROVINCE.md` | Four planes, refusals, ADJ-01..07 handoff table |
| `SKILL.md` | Health-verdict table and checklist |
| `SHONEN.md` | Checklist, author-side `[~]` |
| `MINT.md` | Mint cause |
| `LOG.md` | Append-only record |
| `SCORECARD.md` | Axis verdicts |
| `AGENTS.md` | Operating rules |
| `corpus/` | Plane notes, handoffs, lessons, index |
| `tools/tsukuroi-census.sh` | Four-plane census |
| `plans/` | Round plans |
| `reports/` | Round reports |
| `.ufo/` | Round machinery |

## Neighbors

The handoff table in `PROVINCE.md` names the next reader, not a permission to repair: kama (ADJ-01), kagi (ADJ-02), mado (ADJ-03), mori (ADJ-04), kumitate (ADJ-05), the protocol integrator for unresolved kaidoku/revenger ownership (ADJ-06), tameshi (ADJ-07). Re-read the cited sibling declaration before a later handoff. The table does not freeze another lane's authority.

Fleet protocol: [VeigaPunk/shokunin](https://github.com/VeigaPunk/shokunin).
