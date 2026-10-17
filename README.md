# tsukuroi-shokunin — 繕

**Host operability and system repair** — the OS substrate itself:
package state, systemd, drivers/firmware, boot health.

Tsukuroi (繕, mending) detects and reports. **The operator remediates.**
This lane never installs, upgrades, or removes packages, and never
restarts services.

This is a **shokunin lane** of the [shokunin fleet](https://github.com/VeigaPunk/shokunin).
Rank: **shonen** (probation; roster row withheld).

## The craft

Three verdicts, never a scalar (`SKILL.md`):

| Verdict | Means | Never means |
|---|---|---|
| `HEALTHY` | every probe in the plane returned the listed pass value | "no problems were found" without a run probe |
| `DEGRADED` | plane answers, but carries a named defect or unresolved unknown | outage |
| `BLOCKED` | cannot be assessed read-only, or core function offline | "corrupt" |

Planes: package (`pacman -Qkk`, foreign/AUR census, receipt
discipline), systemd user units & timers, journal/boot triage,
driver/firmware (modules, nvidia + GSP *presence*, `nvidia-smi`
shape), update-safety (what an `-Syu` would touch, pins/holds).

Host memory and kill-event measurements support OS triage. They do
**not** establish which fleet wave caused pressure — that correlation
is [mori](https://github.com/VeigaPunk/mori-shokunin).

## Adjacent handoffs

Shared findings are not shared ownership. `PROVINCE.md` §Adjacent
classifies seven finding-to-owner classes. A recipient is an
analysis/report owner, **not permission to repair**. Tsukuroi retains
the OS finding. Unresolved ownership goes to the protocol integrator.

| ID | Question | Next analysis |
|---|---|---|
| ADJ-01 | served-model identity | kama |
| ADJ-02 | credential helper / auth flow | kagi |
| ADJ-03 | desktop rendering / binds / idle *config* | mado |
| ADJ-04 | fleet/wave attribution of pressure | mori |
| ADJ-05 | dispatch / routing semantics | kumitate |
| ADJ-06 | driver/firmware *internals* (RE) | integrator (kaidoku/revenger unresolved) |
| ADJ-07 | reusable verification question | tameshi |

Handoff packets are sanitized: no secret values, raw configs, raw
cores, or argv. Source pins:
`corpus/knowledge/adjacency-handoffs-fleet-r1.md`.

## Province

Owns (read-only): pacman state, systemd user units & timers,
journal/boot triage, driver/firmware *health*, update-safety
questions.

**Refuses:** endpoint/model serving health (kama), secrets (kagi),
binary RE of drivers (kaidoku/revenger). Out of province → report,
never absorb.

See [`PROVINCE.md`](PROVINCE.md).

## What's in this repository

```
tsukuroi-shokunin/
├── SKILL.md                 HEALTHY/DEGRADED/BLOCKED table + update-safety checklist
├── PROVINCE.md              planes + seven adjacency handoffs
├── SHONEN.md
├── LOG.md
├── SCORECARD.md
├── MINT.md
├── AGENTS.md
├── tools/
│   └── tsukuroi-census.sh
├── reports/
├── plans/
└── corpus/
    ├── knowledge/           package/systemd/driver planes, host-health, handoffs
    └── lessons/
```

## Start here

```sh
bash tools/tsukuroi-census.sh
```

Read the census as a report, not a repair ticket. Then
[`SKILL.md`](SKILL.md) for how to classify a plane, and `PROVINCE.md`
§Handoff checklist before sending anything to a sibling.

## How a round works

One axis-move. Lane identity:
`tsukuroi-shokunin <tsukuroi@shokunin.local>`.

## Fleet

[VeigaPunk/shokunin](https://github.com/VeigaPunk/shokunin) ·
[mori-shokunin](https://github.com/VeigaPunk/mori-shokunin) ·
[kimi-shokunin](https://github.com/VeigaPunk/kimi-shokunin)
