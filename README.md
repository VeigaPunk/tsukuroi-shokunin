# tsukuroi-shokunin — 繕

**Host operability and system repair.** The OS substrate itself: package
state, systemd, drivers/firmware, boot health — assessed from an
unprivileged shell.

**Detection and report. The operator remediates.** This lane never
installs, upgrades, or removes packages, and never restarts services.

A **shokunin lane**: an expert agent for one domain, minted and trained
under the [shokunin skill](https://github.com/VeigaPunk/shokunin).
Rank: **shonen**. Promotion is a named non-author review of
[`SHONEN.md`](SHONEN.md), never self-attestation.

This lane answers: *what is the state of the owned host planes right
now, and can that state be assessed at all without writing anything?*

## Verdicts

`HEALTHY` · `DEGRADED` · `BLOCKED` — three states, never a scalar.

| Verdict | Means | Never means |
|---|---|---|
| `HEALTHY` | every probe in the plane returned its pass value | “no problems were found” without a run probe |
| `DEGRADED` | the plane answers, with a named defect or unresolved unknown | outage |
| `BLOCKED` | cannot be assessed read-only, or a core function is offline | “corrupt” |

Worst plane wins. An unreadable plane fails closed `BLOCKED` — never a
fake pass.

## Domain

From [`PROVINCE.md`](PROVINCE.md), all **read-only probes**: pacman
(`pacman -Qkk`, foreign/AUR census, `.pkg.tar.zst` receipts), systemd
user units & timers, journal/boot triage, driver/firmware plane
(modules, nvidia + GSP presence, `nvidia-smi` **shape**), update-safety
(what an `-Syu` would touch), OOM/kill watch.

**Refuses:** endpoint/model serving health (→
[kama](https://github.com/VeigaPunk/kama-shokunin)); secrets (→
[kagi](https://github.com/VeigaPunk/kagi-shokunin)); binary RE of
drivers (→ [kaidoku](https://github.com/VeigaPunk/shokunin-reverse-engineering)
/ [revenger](https://github.com/VeigaPunk/shokunin-binary-forensics) —
tsukuroi tracks *state and health*, not internals). Fleet/wave
attribution of pressure belongs to
[mori](https://github.com/VeigaPunk/mori-shokunin).

Shared findings are classified by the **question being asked**, not the
binary name. The seven finding-to-owner handoffs live in `PROVINCE.md`
§Adjacent. A recipient is an analysis owner, **not permission to repair**.

## What's here

| Path | Role |
|---|---|
| [`SKILL.md`](SKILL.md) | plane playbook, verdict vocabulary, probe table |
| [`PROVINCE.md`](PROVINCE.md) | owned surfaces, refusals, adjacency handoff table |
| [`tools/tsukuroi-census.sh`](tools/tsukuroi-census.sh) | five-plane (+ oom) live census |
| [`corpus/`](corpus/) | knowledge and lessons |
| [`SCORECARD.md`](SCORECARD.md) · [`LOG.md`](LOG.md) · [`SHONEN.md`](SHONEN.md) | axes, trail, promotion |

## The census

```sh
bash tools/tsukuroi-census.sh --help
bash tools/tsukuroi-census.sh --selftest
bash tools/tsukuroi-census.sh                 # live, read-only
bash tools/tsukuroi-census.sh --sample N      # pacman -Qkk sample size (default 8)
```

Verdict line: `TSUKUROI_CENSUS: HEALTHY|DEGRADED|BLOCKED (packages=.. systemd=.. drivers=.. journal=.. update-safety=.. oom=..)`.
Exit: `0` HEALTHY · `1` DEGRADED · `2` BLOCKED.

## How a lane learns

Append-only corpus; every claim separates observation / inference /
unknown; rounds are non-author-verified. See the fleet
[README](https://github.com/VeigaPunk/shokunin#readme).
