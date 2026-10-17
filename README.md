# tsukuroi-shokunin — 繕

Host operability and system repair. 繕 is mending: the OS substrate
itself — package state, systemd, drivers and firmware, boot health.

The lane detects and reports. It does not install, upgrade, or remove
packages, and it does not restart services. The operator remediates.

## The job

`PROVINCE.md` owns read-only probes of pacman state (`pacman -Qkk`,
foreign and AUR census, package-receipt discipline), systemd user units
and timers, journal and boot triage (`journalctl -b`, dmesg error
classes), and the driver and firmware plane (kernel modules, the nvidia
driver and GSP firmware presence, `nvidia-smi` shape). Update-safety
questions — what an `-Syu` would touch, which holds exist — are in
scope as questions. Applying the update is not.

It refuses endpoint and model-serving health (kama), secrets (kagi),
and binary reverse engineering of drivers (kaidoku and revenger).
Tsukuroi tracks state and health, not internals. Host memory and kill
events support OS triage; which fleet wave caused pressure is mori's
question. The province carries an adjacency table (ADJ-01 onward) that
says, for each shared finding, what tsukuroi keeps, who analyzes next,
and the minimum evidence in the handoff. A recipient is an analysis
owner. The table is not permission to repair.

## Census

`tools/tsukuroi-census.sh` answers one question: what is the state of
the owned host planes right now, and can an unprivileged shell assess
them at all. Verdict `TSUKUROI_CENSUS: HEALTHY`, `DEGRADED`, or
`BLOCKED`. An unreadable plane fires the `BLOCKED` arm. The script
does not invent a pass.

```sh
bash tools/tsukuroi-census.sh --selftest
```

`--selftest` runs on a fixture tree. A live run reads the host and
writes nothing. The header names the planes and the exit map.

A selftest on 2026-10-17 exited 1:
`TSUKUROI_CENSUS_SELFTEST: FAIL (80 cases, 79 passed, 1 failed)`.
The failing case was `degraded: a repo-side behind row joins the candidate class (R9)`,
which printed `TSUKUROI_CENSUS: HEALTHY` and exit 0 where the fixture
wanted exit 1. The other 79 cases passed, including the healthy, degraded,
and blocked arms around it. Treat a green live census as the script's
verdict for that host, and treat this selftest gap as open.

## Read this first

1. [`PROVINCE.md`](PROVINCE.md) — planes, refusals, and the adjacency table.
2. [`SKILL.md`](SKILL.md) — standing rules and the playbook.
3. [`corpus/README.md`](corpus/README.md) — the coverage map.
4. [`tools/tsukuroi-census.sh`](tools/tsukuroi-census.sh) — the census contract, in the header.

## On disk

| Path | Role |
|---|---|
| `SKILL.md` | Playbook. Read-only substrates; secrets stay shape-only. |
| `PROVINCE.md` | Planes and the finding-to-owner table. |
| `tools/tsukuroi-census.sh` | Four-plane health census. |
| `corpus/` | Knowledge and lessons. |
| `plans/`, `reports/` | Round plans and reports. |
| `MINT.md`, `SHONEN.md` | Mint record and promotion checklist. Rank is shonen. |
| `LOG.md`, `SCORECARD.md` | Audit trail and axis verdicts. |

## Fleet

Protocol and roster: [shokunin](https://github.com/VeigaPunk/shokunin).
This repository is a sibling lane. It is not an object in the fleet
root's `MANIFEST.json` `roster` array (13 ids, ending at `kaidoku`,
read 2026-10-17). Rank **shonen**.
