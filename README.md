# tsukuroi-shokunin — 繕

Host operability. The OS substrate itself: package state, systemd user
units, drivers and firmware, journal and boot health.

Rank: **shonen**. [`SHONEN.md`](SHONEN.md) marks its boxes `[~]` on
author-side evidence. Non-author verification remains owed.

Fleet: [shokunin](https://github.com/VeigaPunk/shokunin).

## The question

> What is the state of the owned host planes right now, and can an
> unprivileged shell assess them at all?

Verdicts are three words, never a score: `HEALTHY`, `DEGRADED`,
`BLOCKED`. Every verdict carries the probe and the observed value.
`BLOCKED` means the probe cannot run, or the plane's core function is
offline. It does not mean "the hardware is corrupt." `HEALTHY` means
every probe in that plane returned its pass value. It does not mean "no
problems were found" without a run.

The lane never installs, upgrades, removes, or restarts anything.
Detection and report. The operator remediates.

## Boundary

**Owns:** `pacman` verify loops and foreign-package census, systemd user
units and timers, journal and boot triage, the driver and firmware plane
(kernel modules, nvidia driver and GSP firmware presence, `nvidia-smi`
shape), and update-safety questions about what an upgrade would touch.

**Hands off:** endpoint and model-serving health (kama), secrets (kagi),
binary reverse engineering of drivers (kaidoku / revenger). Host memory
and kill events support OS triage; which fleet wave caused pressure is
mori's question.

`PROVINCE.md` §Adjacent is the finding-to-owner table (ADJ-01 through
ADJ-07). A recipient is the next analyst, not permission to repair.
Tsukuroi keeps the OS finding. Shared evidence is not shared ownership.

## Run

```sh
bash tools/tsukuroi-census.sh --selftest
bash tools/tsukuroi-census.sh
```

Verdict line `TSUKUROI_CENSUS: HEALTHY|DEGRADED|BLOCKED`. The script
header describes the planes (packages, systemd, drivers, journal/boot)
and the fail-closed rule: an unreadable plane is `BLOCKED`, never a fake
pass. `--selftest` runs on a fixture tree and does not need the live
host.

## Map

| Path | What it is |
|---|---|
| [`SKILL.md`](SKILL.md) | health-verdict table and update-safety checklist |
| [`PROVINCE.md`](PROVINCE.md) | planes plus the seven handoff rows |
| [`corpus/knowledge/adjacency-handoffs-fleet-r1.md`](corpus/knowledge/adjacency-handoffs-fleet-r1.md) | executed handoff example and source pins |
| [`corpus/knowledge/`](corpus/knowledge/) | per-plane notes and the round-3 host health report |
| [`LOG.md`](LOG.md), [`SCORECARD.md`](SCORECARD.md) | rounds and axis verdicts |

Re-read the cited sibling declaration before handing a finding off. The
table does not freeze another lane's authority.
