# OverlapHost — Round 13 Scoped Findings & Connector Proposal

Seat: `TsukuroiR13.OverlapHost` (connector, leaf).
Assigned write set: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-13/correction/OverlapHost.md`.
Read-only probes only; no tests/checks run; no commits; no tool installs/updates (none needed).

## 1. Evidence: Province Boundaries & Zero Scope Transfer

Re-read current committed declarations: `tsukuroi-shokunin/PROVINCE.md`, `mado-shokunin/PROVINCE.md`, `kama-shokunin/PROVINCE.md`, and `mori-shokunin/PROVINCE.md`.

- **tsukuroi core domain** (`PROVINCE.md:6-15, 86-90`): Owns OS substrate operability, package state, systemd user units & timers, unit files, failed states, and the rollback-net surface. Round-12 refinement explicitly retained root-directory metadata, create-failure DAC/ACL, mount/namespace, and configured-credential discrimination within tsukuroi's core host/rollback-net surface (`PROVINCE.md:86-90`). Round 13's correction of systemd unit read-only namespace mechanisms (`systemd.exec(5)`) refines this exact owned surface.
- **mado boundary** (`../mado-shokunin/PROVINCE.md:3-16`): Owns desktop/compositor craft (`~/.config/hypr/`, waybar, walker, terminal configs). ADJ-03 routes desktop rendering/binding configuration-level diagnosis to mado while tsukuroi retains user-manager/unit, package, and driver health. Systemd mount/namespace sandboxing is an OS execution property, not a desktop config. **Scope transfer: 0.**
- **kama boundary** (`../kama-shokunin/PROVINCE.md:3-29, 40-52`): Owns local model serving & endpoint health (port discovery, baseURL pins, served-model reconciliation). Hard write boundary refuses writes to systemd units (`PROVINCE.md:46-49`). ADJ-01 retains kernel, driver, device, and user-unit state in tsukuroi; kama tests endpoint responsiveness only. Diagnosing unit sandbox mechanisms (`ProtectSystem`, `BindReadOnlyPaths`) stays in tsukuroi. **Scope transfer: 0.**
- **mori boundary** (`../mori-shokunin/PROVINCE.md:6-17, 50-54`): Owns fleet & host observability (watchdog liveness, wave settlement, kill/OOM catalog-ID counts, disk/cgroup runway). Mori explicitly refuses OS package, systemd unit, driver/firmware, and boot state (`PROVINCE.md:12-14`). ADJ-04 routes fleet/wave correlation to mori while tsukuroi retains OS memory, journal, and boot diagnosis. Unit-level namespace configuration and errno classification (EROFS vs EACCES) are strictly tsukuroi's domain. **Scope transfer: 0.**

## 2. Relevant Routing Evaluation

Review of adjacency routes ADJ-01..07 (`tsukuroi-shokunin/PROVINCE.md:35-54`):
- No trigger in ADJ-01..07 authorizes or requires transferring unit mount/namespace analysis to any sibling.
- Systemd sandbox diagnosis for host units (e.g. `limine-snapper-sync.service` or daemon helpers) is an internal OS execution property, not an endpoint (ADJ-01), secret (ADJ-02), UI symptom (ADJ-03), fleet correlation (ADJ-04), dispatch bug (ADJ-05), binary RE (ADJ-06), or fleet verification method (ADJ-07).
- Routes ADJ-01..07 remain strictly contract-only controls; no new packet or handoff transition is prepared or needed.

## 3. Connector Proposal: Dual-Boundary In-Province Encapsulation Rule

**Proposal:** Formulate and document an explicit **Dual-Boundary In-Province Encapsulation Rule** in the round-13 correction synthesis:
1. **Substrate Separation:** Explicitly bifurcate global host mount namespace evidence (`findmnt -R /`) from unit-execution private namespace configuration (`systemd.exec(5)` properties: `ProtectSystem`, `BindReadOnlyPaths`, `TemporaryFileSystem=ro`, `RootDirectory`, `RootImage`). Host `findmnt` can never prove or disprove a unit's private sandbox namespace.
2. **Zero-Handoff Invariant:** Codify that systemd sandbox/namespace diagnosis for any unit running on the host belongs exclusively to tsukuroi's core OS surface. Sibling lanes receive only downstream application symptoms (ADJ-01 for endpoints, ADJ-03 for UI) without permission or authority to diagnose systemd isolation properties; tsukuroi never absorbs sibling application domain logic.
3. **Hermetic Gate Scope:** Bind `tools/check-root-dac-correction.py` to evaluate unit-property syntax and documentation claims against committed artifacts and S028/S041 only, preventing any runtime cross-unit inspection or sibling dependency leakage.

## 4. Affected Axes

- **Depth (Target Axis):** Improved. Replaces the invalid round-12 exclusive universal with a comprehensive, source-grounded enumeration of systemd unit mount-isolation mechanisms, while cleanly distinguishing host mount views from unit-private namespaces.
- **Adjacency:** Unchanged / unharmed. Affirms zero scope transfer across mado, kama, and mori; preserves the seven ADJ-01..07 contract routes without drift or false handoffs.
- **Operability:** Unchanged / unharmed. Preserves read-only, zero-mutation discipline; no service operations, restarts, or sudo probes.
- **Coverage, Freshness, Calibration:** Unchanged / unharmed. Stays within the existing rollback-net surface, uses dated 2026-10-20 evidence, and explicitly records unmeasured invocation namespaces as residual unknowns.

## 5. Risks and Contradictions

- **Contradiction to avoid:** Conflating configured unit text (`systemctl show`) with the effective runtime mount namespace created at exec-time. Properties like `ProtectHome=yes` or `ProtectKernelTunables=yes` create mount namespaces at spawn, but completed/inactive invocations (such as PID 1386) leave no live `/proc/<pid>/mountinfo` to inspect.
- **Risk:** Attempting live namespace inspection on an inactive unit risks reading a recycled PID. Configured properties must be recorded as static unit text (`[obs]`), while built mount tables remain an explicit residual unknown (`[unk]`).

## 6. Verification Plan (for L1 Integration)

- Verify `tsukuroi-shokunin/PROVINCE.md`, `mado-shokunin/PROVINCE.md`, `kama-shokunin/PROVINCE.md`, and `mori-shokunin/PROVINCE.md` remain unmodified by this seat.
- Verify `root-dac-correction-r13.md` and `.json` incorporate the 5 unit namespace mechanisms (`ProtectSystem`, `BindReadOnlyPaths`, `TemporaryFileSystem`, `RootDirectory`, `RootImage`) without transferring diagnosis to siblings.
- Run `check-root-dac-correction.py` hermetically without live sibling daemon dependencies.

## 7. Tooling Record

- Tools installed or updated: none (none needed). Standard environment used.
