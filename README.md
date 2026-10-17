# tsukuroi-shokunin — 繕

**Mending the OS substrate — by seeing it clearly, not by touching it.**
Package state, systemd, drivers / firmware, boot health. Detection and
report. The operator remediates.

This is a [shokunin](https://github.com/VeigaPunk/shokunin) lane. Rank:
shonen. Tsukuroi never installs, upgrades, or removes packages, and
never restarts services. Host memory and kill-event measurements
support OS triage; they do not establish which fleet wave caused
pressure (that is [mori](https://github.com/VeigaPunk/mori-shokunin))
or whether an endpoint works (that is
[kama](https://github.com/VeigaPunk/kama-shokunin)).

Shared evidence is not shared ownership. Route a finding by the
*question being asked*, not the binary or service name.
[`PROVINCE.md`](PROVINCE.md) §Adjacent is the seven-row handoff table.

## Province

**Owns (read-only probes):** pacman state (`pacman -Qkk`, foreign / AUR
census, `.pkg.tar.zst` receipt discipline); systemd user units and
timers; journal / boot triage (`journalctl -b`, dmesg error classes);
driver / firmware plane (kernel modules, nvidia driver + GSP firmware
presence, `nvidia-smi` shape); update-safety — what an `-Syu` would
touch, what pins / holds exist.

**Refuses:** endpoint / model serving health (→ kama); secrets (→ kagi);
binary RE of drivers (→ kaidoku / revenger — tsukuroi tracks *state and
health*, not internals). Kaidoku and revenger both declare
shipped-artifact RE; the integrator must arbitrate that shared scope.
Tsukuroi neither picks an owner nor absorbs it (ADJ-06).

Full boundary and handoff checklist: [`PROVINCE.md`](PROVINCE.md).

## Adjacent handoffs (summary)

| ID | Question | Next analysis |
|---|---|---|
| ADJ-01 | Is this local model the one the config believes? | kama |
| ADJ-02 | Permission / ownership on a credential-bearing helper? | kagi (shape only — no secret values) |
| ADJ-03 | Desktop rendering / bindings / idle as configuration? | mado |
| ADJ-04 | Host pressure needing fleet / wave attribution? | mori |
| ADJ-05 | Dispatch / routing semantics, not just a failed unit? | kumitate |
| ADJ-06 | Driver / firmware mechanism needing shipped-artifact RE? | integrator — kaidoku / revenger unresolved |
| ADJ-07 | A census blind spot that is a verification-method question? | tameshi |

A recipient is an analysis owner, **not permission to repair**.
Acknowledgement is not acceptance. Source fingerprints:
`corpus/knowledge/adjacency-handoffs-fleet-r1.md`. Re-read the cited
sibling declaration before a later handoff.

## Start here

1. [`SKILL.md`](SKILL.md) — standing rules and the census playbook.
2. [`PROVINCE.md`](PROVINCE.md) — four-plus-one planes and the handoff table.
3. [`tools/tsukuroi-census.sh`](tools/tsukuroi-census.sh) — the executable census.

## The census

```
bash tools/tsukuroi-census.sh            # live unprivileged read
bash tools/tsukuroi-census.sh --selftest # hermetic fixture tree
```

The census answers one question, read-only: what is the state of the
owned host planes right now, and can it be assessed at all from an
unprivileged shell. Planes: packages, systemd, drivers (including the
round-7 memory-pressure arm), journal / boot, and the round-9
update-safety plane. Rollup vocabulary:
`TSUKUROI_CENSUS: HEALTHY|DEGRADED|BLOCKED`. An unreadable plane fails
closed `BLOCKED` — never a fake pass. Remaining planes still report.

## What's in the repo

```
tsukuroi-shokunin/
├── SKILL.md          host-operability playbook
├── PROVINCE.md       planes + seven handoffs
├── SHONEN.md         promotion checklist
├── MINT.md           why this lane was minted
├── LOG.md            append-only audit trail
├── SCORECARD.md      axis verdicts
├── AGENTS.md         operating rules
├── tools/            tsukuroi-census.sh
├── plans/            round plans
├── reports/          verifier / adjudicator reports
└── corpus/           knowledge/, lessons/, QUALITY.md
```

Protocol: append-only corpus; secrets are shape-only; rounds are
non-author-verified. See the fleet
[README](https://github.com/VeigaPunk/shokunin#readme) for how a lane
learns.
