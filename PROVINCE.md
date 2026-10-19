# tsukuroi-shokunin — Province

**Domain:** host operability & system repair (繕, mending) — the OS
substrate itself: package state, systemd, drivers/firmware, boot health.

## Core

**Owns (surfaces, all read-only probes):** pacman state (`pacman -Qkk`
verify loops, foreign/AUR census, `.pkg.tar.zst` receipt discipline),
systemd user units & timers (`systemctl --user`, unit files, failed
states), journal/boot triage (`journalctl -b`, dmesg error classes),
driver/firmware plane (kernel modules, nvidia driver + GSP firmware
presence, `nvidia-smi` shape). Update-safety questions: what an -Syu
would touch, what pins/holds exist.

**Refuses:** endpoint/model serving health (→ kama), secrets (→ kagi),
binary RE of drivers (→ kaidoku/revenger — tsukuroi tracks *state and
health*, not internals). Never installs, upgrades, or removes packages;
never restarts services. Detection and report; the operator remediates.

Host memory and kill-event measurements support OS triage; they do not
establish which fleet wave caused pressure or whether an endpoint works.
The existing census reports those signals; fleet correlation belongs to mori
(`../mori-shokunin/PROVINCE.md:6-16`).

## Adjacent — finding-to-owner handoffs

This table classifies seven shared-work classes, not every possible host
failure. A recipient is an analysis/report owner, **not permission to repair**.
Tsukuroi retains the OS finding. No row authorizes configuration writes,
service changes, credential reads, endpoint requests, or target execution.
Shared evidence is not shared ownership; unresolved ownership goes to the
protocol integrator, never to whichever lane answered first.

| ID | Finding / boundary trigger | Tsukuroi retains | Next analysis recipient | Minimum handoff evidence | Ownership source |
|---|---|---|---|---|---|
| ADJ-01 | A local model endpoint or served-model identity is wrong; GPU readiness alone cannot decide this | Kernel, driver, device and user-unit state | kama | Capture time; driver query and unit-state command/exit; reported endpoint symptom without credentials. Kama must obtain its own endpoint evidence; no endpoint diagnosis from `nvidia-smi` | `../kama-shokunin/PROVINCE.md:3-24` |
| ADJ-02 | A credential-bearing helper has a permission/ownership finding or an auth-flow question | Package owner/version and filesystem mode; package drift is not proof of credential exposure | kagi | Path, mode, uid/gid, package owner/version, command/exit and capture time only; no secret values, vault references, session bytes or helper invocation | `../kagi-shokunin/PROVINCE.md:3-6,10-17,32-34,54` |
| ADJ-03 | Desktop rendering, bindings, menu or idle behavior needs configuration-level diagnosis | User-manager/unit, package and driver health; an active unit does not prove the UI works | mado | Observed UI symptom and time plus relevant OS probe/exit; identify configuration surface without copying its contents. Mado verifies file/screenshot behavior itself | `../mado-shokunin/PROVINCE.md:3-16` |
| ADJ-04 | Host pressure or a kill signal needs fleet/wave attribution, liveness or progress correlation | OS memory, journal and boot diagnosis; cumulative counters are not dated incidents | mori | Capture time, boot/window, exact counter or PSI command/exit and observed value; distinguish presence, cumulative count and dated event. Request correlation, not a claim that a wave caused OOM | `../mori-shokunin/PROVINCE.md:3-16` |
| ADJ-05 | Task/hub dispatch, routing or orchestration semantics are wrong, rather than merely a failed host unit | systemd and resource evidence; unit liveness cannot prove dispatch correctness | kumitate | Minimal reported dispatch symptom, task/wave identifier if non-sensitive, capture time and OS probe/exit; exclude tokens, environment and raw process arguments | `../kumitate-shokunin/PROVINCE.md:3-6`; `../mori-shokunin/PROVINCE.md:12-16` |
| ADJ-06 | Driver/firmware/package mechanism requires shipped-artifact reverse engineering beyond health inventory | Loaded version, package provenance and driver/boot symptoms; no binary-internals inference | protocol integrator — kaidoku/revenger ownership unresolved | Exact question, authorized artifact identity/path and digest when safely obtainable, capture time and relevant OS evidence. Request an ownership ruling before any RE work; do not invoke a target or forward raw cores | `../kaidoku-shokunin/PROVINCE.md:3-6,88-100`; `../revenger-shokunin/PROVINCE.md:3-7,19-25` |
| ADJ-07 | A census blind spot raises a reusable verification/mutation-testing question | Census bug, domain contract, implementation and repair in this repo | tameshi | Minimal failing behavior, command/exit, measured census revision and expected domain invariant; ask for method advice, not transfer of gate ownership or a general claim from one lane | `../tameshi-shokunin/PROVINCE.md:3-18` |

### Handoff checklist

1. Record the trigger, UTC capture time, boot/time window where relevant,
   exact read-only command, exit code and observed value. Mark inference
   and unknowns separately; do not infer a fresh kill from a cumulative counter.
2. Select the matching row by the **question being asked**, not the binary or
   service name. Split mixed questions: keep OS diagnosis here; name only the
   requested sibling analysis. If no row fits, report to the integrator.
3. Prepare a sanitized evidence packet using that row's minimum fields.
   Report it in the fleet lane report, including the recipient and remaining
   operator action. Never copy credentials, raw configs, raw cores or argv.
4. Track closure states separately: `prepared`, `reported`, `acknowledged`,
   `accepted`, `resolved`. Acknowledgement is not acceptance; resolution
   requires owner-side closure evidence. A missing substrate or disputed
   owner is an explicit limit, not a successful downstream handoff.

Sources were read on 2026-10-15; sibling declarations can drift. Source
fingerprints and an executed host-to-mori packet are in
`corpus/knowledge/adjacency-handoffs-fleet-r1.md`. Re-read the cited declaration
before a later handoff; the table does not freeze another lane's authority.

## Frontier

- Recipient acknowledgement and independently replayed handoffs are not
  verified. The round's author-side replay is not promotion evidence.
- Kaidoku and revenger both declare shipped-artifact RE. The integrator must
  arbitrate this shared scope; tsukuroi neither picks an owner nor absorbs it.

**Out of province → report, never absorb.**
Source re-check 2026-10-19 (fleet round 1): [obs] HEAD pins for kama, kaidoku and
revenger drift; kagi, mado, mori, kumitate and tameshi match their original pins. The cited route
anchors still hold in-range; no ranges moved. See
`corpus/knowledge/adjacency-recheck-2026-10-19.md` for hashes, quotes, lifecycle
states and the receipt sweep.
