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

**Additional owned surfaces, documented in fleet round 1 (all read-only):**

| Surface | Boundary | Corpus entry |
|---|---|---|
| `Arch News` upgrade gate | Match official notices to local package/config evidence; a public feed read is not host state, and upgrade actions remain operator-owned. | `corpus/knowledge/arch-news-gate-2026.md` |
| `.pacnew` / `.pacsave` drift | Pair pacman-log history with current readable filesystem findings; report skipped unreadable paths. | `corpus/knowledge/pacnew-plane.md` |
| Initramfs v42 and boot recovery | Inspect effective mkinitcpio drop-ins, hooks and recovery stages; never rebuild or boot. | `corpus/knowledge/initramfs-v42-sysroot-recovery.md` |
| Snapper/rollback net | Diagnose filesystem mode and unit capability restrictions; report mechanism/falsifier, never attempt restore/config changes. | `corpus/knowledge/snapper-eacces-mechanism.md` |

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
Source re-check 2026-10-19T22:57:14Z (fleet round 1): committed sibling HEAD pins match the original 1/8 (mado); 7/8 drift. Re-reading the cited source ranges at those clean HEADs still finds all 8/8 route anchors in-range. The committed-kaika receipt sweep found one recipient-side packet response in mori; acceptance/resolution are not inferred. See `corpus/knowledge/adjacency-recheck-2026-10-19.md` for the pin table, receipt scope and exact evidence.

Round-12 refinement: root-directory metadata and create-failure DAC/ACL,
mount/namespace and configured-credential discrimination remain within the
existing host/rollback-net surface. The census owns detection only; no mode
repair, service restart, subvolume creation, boot or package transaction is
authorized by a finding. `corpus/knowledge/root-dac-decision-r12.md` refines
this existing core surface without absorbing sibling verification methods.

Round-13 correction R13-DAC-EXCLUSIVITY: the active refinement is now
`corpus/knowledge/root-dac-correction-r13.md` and `.json`; the round-12
entry is retained with an explicit supersession notice after outside
rejection. This remains the same host/rollback-net surface and grants
no namespace mutation, privileged inspection or sibling-method ownership.

Round-14 source-scope erratum: R14-VALUE-DOMAIN and R14-COMMENT-ATTRIBUTION
(`corpus/knowledge/source-scope-correction-r14.md`/`.json`) supersede two
round-13 loci only — the ProtectSystem “value set is not exhaustive” cell
(`ProtectSystem=` is documented as a boolean argument or the special values
`full` or `strict`; mechanism non-exhaustiveness is separate, S044) and the
#8047 “self-described model-generated triage” attribution (verified account
fields only; VM execution unverified; second opinion and maintainer deferral
stand; #6629's disclaimer is not transferred, S045). Round-13 namespace
guidance remains active; no new surface, capability or host cause is claimed.

## Adjacent — portable ownership anchors (round 19)

Append-only. The line-range table under `## Adjacent — finding-to-owner handoffs`
(ADJ-01..ADJ-07) and the Core pointer retained above are not changed. Each row
below cites its ownership text by anchor id, exact heading and exact quote from
the pinned sibling snapshot, never by line number; OUT-001 is the Core pointer
(ADJ row shown as Core). The pinned commit and blob sha256 identify the bytes,
so an anchor is valid only for those bytes. Inbound classification and
owner-handoff packets are in `corpus/knowledge/adjacency-anchors-r19.md`. This
section grants no authority and is an ownership locator, not a repair mandate.

| Anchor | ADJ row | Sibling file @ commit | Heading | Quote | Proposition |
|---|---|---|---|---|---|
| OUT-001 | Core | `mori-shokunin/PROVINCE.md` @ `91940fa339e3` | `# mori-shokunin — Province` | independently labeled user/system journals, plus cgroup `memory.events` and the explicit same-boot journal window after a retained anchor; | Mori owns kill/OOM and cgroup memory evidence; fleet correlation of host pressure is mori's, not OS triage. |
| OUT-002 | ADJ-01 | `kama-shokunin/PROVINCE.md` @ `e75cf680b534` | `# kama-shokunin — Province` | `GET /v1/models` vs `--alias` vs the configured model id | Kama owns served-model identity reconciliation; an endpoint or served-model mismatch is kama's analysis, not a driver/GPU-readiness finding. |
| OUT-003 | ADJ-02 | `kagi-shokunin/PROVINCE.md` @ `c2cab35bc92e` | `# kagi-shokunin — Province` | **Domain:** secrets & vault ops — the-janitor flows, credential hygiene evidence | Kagi owns secrets and vault operations, the-janitor credential flows, and credential-hygiene evidence. |
| OUT-004 | ADJ-03 | `mado-shokunin/PROVINCE.md` @ `a4046a821608` | `# mado-shokunin — Province` | **Owns (surfaces):** `~/.config/hypr/` (hyprland.conf, keybinds, rules, | Mado owns the Hyprland, waybar, walker and terminal configuration plane, themes/wallpapers and screen/idle behavior. |
| OUT-005 | ADJ-04 | `mori-shokunin/PROVINCE.md` @ `91940fa339e3` | `# mori-shokunin — Province` | kill/OOM-related catalog-ID records and signal-11 coredump records | Mori owns kill/OOM catalog-ID and signal-11 coredump classification from separately labeled user/system journals; fleet attribution is its correlation, not tsukuroi's. |
| OUT-006 | ADJ-05 | `kumitate-shokunin/PROVINCE.md` @ `1770305fae20` | `# kumitate-shokunin — Province` | **Domain:** orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime | Kumitate scopes OMP task/hub and orchestration tooling, so task/hub dispatch and routing semantics are its analysis, not tsukuroi's. |
| OUT-007 | ADJ-05 | `mori-shokunin/PROVINCE.md` @ `91940fa339e3` | `# mori-shokunin — Province` | **Refuses:** dispatch and orchestration mechanism (→ kumitate); OS package, | Mori refuses dispatch and orchestration mechanism and routes it to kumitate, supporting ADJ-05's kumitate recipient. |
| OUT-008 | ADJ-06 | `kaidoku-shokunin/PROVINCE.md` @ `d1d981d2cc04` | `# kaidoku-shokunin — Province` | **Domain:** reverse engineering of shipped artifacts with REA on this Linux | Kaidoku declares shipped-artifact reverse engineering with REA as its domain, the scope ADJ-06 would hand to an RE owner. |
| OUT-009 | ADJ-06 | `revenger-shokunin/PROVINCE.md` @ `cf02419276e5` | `# revenger province` | Owns: reverse engineering of shipped artifacts | Revenger owns shipped-artifact reverse engineering (binaries, packages, APKs) with an observation/inference/unknown evidence ledger; tsukuroi tracks state only. |
| OUT-010 | ADJ-07 | `tameshi-shokunin/PROVINCE.md` @ `01d586ddbc5f` | `# tameshi-shokunin — Province` | **Owns:** the method, documented from the fleet's existing gates | Tameshi owns the reusable verification/mutation-testing method, applied to fleet gates as read-only primary surfaces; each lane keeps its own gate. |

Limits (round-19 first falsifiers CritAdjBoundary/CritAdjVacuity): the quoted words are the sibling's, attributed to it, never a tsukuroi assertion of sibling authority; the pins are stale by design once a sibling commits again, so re-read the live declaration before any later handoff (the paragraph above `## Frontier` still governs). Every heading above is the sibling file's title heading because the cited ownership text sits in its preamble. Recheck: `python3 tools/check-adjacency-anchors.py --revision <REV>`.
