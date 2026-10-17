# tsukuroi-shokunin — 繕

**Host operability and system repair — detect, report, hand off. The
operator mends.**

A **shokunin lane** minted and trained under the
[shokunin](https://github.com/VeigaPunk/shokunin) skill. 繕 (tsukuroi,
mending) owns the OS substrate: package state, systemd, drivers /
firmware, boot health.

**Wiki:** [lane overview](https://app.devin.ai/org/veigapunk/wiki/VeigaPunk/tsukuroi-shokunin?branch=master)

## Domain

Read-only probes from `PROVINCE.md`:

- pacman state (`pacman -Qkk`, foreign/AUR census, `.pkg.tar.zst` receipts)
- systemd user units and timers (`systemctl --user`, failed states)
- journal / boot triage (`journalctl -b`, dmesg error classes)
- driver / firmware plane (modules, nvidia driver + GSP presence, `nvidia-smi` shape)
- update-safety: what an `-Syu` would touch, what pins/holds exist

**Never** installs, upgrades, or removes packages. **Never** restarts
services. Host memory and kill-event measurements support OS triage;
fleet-wave attribution belongs to [mori](https://github.com/VeigaPunk/mori-shokunin).

## Adjacent handoffs

`PROVINCE.md` §Adjacent classifies seven shared-work classes. A recipient
is an analysis/report owner, **not** permission to repair. Shared
evidence is not shared ownership.

| ID | Question | Next analysis |
|---|---|---|
| ADJ-01 | is the served model the expected one? | [kama](https://github.com/VeigaPunk/kama-shokunin) |
| ADJ-02 | credential-bearing helper / auth flow | [kagi](https://github.com/VeigaPunk/kagi-shokunin) |
| ADJ-03 | desktop config / bind / idle behavior | [mado](https://github.com/VeigaPunk/mado-shokunin) |
| ADJ-04 | fleet/wave attribution of pressure or kill | [mori](https://github.com/VeigaPunk/mori-shokunin) |
| ADJ-05 | dispatch / routing semantics | [kumitate](https://github.com/VeigaPunk/kumitate-shokunin) |
| ADJ-06 | shipped-artifact RE of a driver/firmware | integrator (kaidoku/revenger unresolved) |
| ADJ-07 | reusable verification-method question | [tameshi](https://github.com/VeigaPunk/tameshi-shokunin) |

Select the row by the **question being asked**, not the binary name.
Executed example and source pins:
`corpus/knowledge/adjacency-handoffs-fleet-r1.md`.

## In this repository

```
PROVINCE.md     OS surfaces + seven-row handoff table
SKILL.md        census playbook + verdict vocabulary
SHONEN.md  SCORECARD.md  LOG.md  MINT.md   (minted 2026-10-14)
corpus/         knowledge/, lessons/, QUALITY.md
tools/
  tsukuroi-census.sh
reports/
```

## Census

```bash
bash tools/tsukuroi-census.sh
```

Detection and report. The operator remediates.

## How a lane learns

Append-only corpus; every claim separates observation / inference /
unknown; rounds are non-author-verified. See the fleet
[README](https://github.com/VeigaPunk/shokunin#readme).
