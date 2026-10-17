# tsukuroi-shokunin — 繕

Host operability: package state, systemd, drivers and firmware, boot
health. Detection and a report. The operator remediates.

The census answers one question: what is the state of the owned host
planes right now, and can an unprivileged shell assess them at all? An
unreadable plane is `BLOCKED`. It is not a quiet pass. A loaded driver
version is not a reverse-engineering of that driver. Memory and kill
counters support OS triage. They do not say which fleet wave caused the
pressure — that correlation is mori's.

Rank: **shonen**. `SHONEN.md` is still here. The fleet `MANIFEST.json`
minted this lane on 2026-10-14 and withheld the roster row.

## Province

**Owns, as read-only probes.** Pacman state (`pacman -Qkk`, foreign and
AUR census, package-receipt discipline). Systemd user units and timers.
Journal and boot triage. The driver and firmware plane: kernel modules,
NVIDIA driver and GSP firmware presence, `nvidia-smi` shape. Update-safety
questions: what an `-Syu` would touch, which pins and holds exist.

**Hands off.** Endpoint and model-serving health (kama). Secrets (kagi).
Binary reverse engineering of drivers (kaidoku / revenger — the integrator
chooses; this lane does not). Installing, upgrading, or removing packages.
Restarting services.

The province's adjacent table (ADJ-01 through ADJ-07) classifies seven
shared-work classes. A recipient is an analysis owner, not permission to
repair. Tsukuroi retains the OS finding. The handoff checklist — capture
time, exact command, exit, inference marked as inference — is in
`PROVINCE.md`.

## Start here

1. `PROVINCE.md` — Core, the handoff table, the frontier.
2. `SKILL.md` — the playbook. The census header cites it for the exit map.
3. `tools/tsukuroi-census.sh` — the four-plane gate.
4. `corpus/knowledge/adjacency-handoffs-fleet-r1.md` — source fingerprints
   for the handoff table. The province says sibling declarations can
   drift; re-read the cited file before a later handoff.
5. `SCORECARD.md` — the closeout banner names what was still uncommitted
   when that refresh was written. Treat the banner's "owed" list as part
   of the record.

## Run the census

```sh
bash tools/tsukuroi-census.sh --help
bash tools/tsukuroi-census.sh --selftest
bash tools/tsukuroi-census.sh
```

Usage, from the script: `--selftest`, `--sample N`, `--help`.
`--selftest` builds a fixture tree and writes only under its temp
directory. The verdict line is `TSUKUROI_CENSUS: HEALTHY|DEGRADED|BLOCKED`.
A live run is read-only: no install, no upgrade, no restart. `DEGRADED`
with evidence is a successful census of a host that needs an operator.

## The tree

| Path | What it is |
|---|---|
| `tools/tsukuroi-census.sh` | Packages, systemd, drivers, journal/boot |
| `corpus/knowledge/` | Plane notes and the handoff fingerprints |
| `corpus/README.md` | Coverage map |
| `reports/` | Round audits |
| `plans/` | Round plans and completion evidence |
| `MINT.md` | The demand that justified the mint |

## Fleet

Minted under [shokunin](https://github.com/VeigaPunk/shokunin).
Fleet liveness is
[mori-shokunin](https://github.com/VeigaPunk/mori-shokunin). OS state
stays here.
