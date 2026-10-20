# ConnectMadoBoundary — mado desktop behavior vs tsukuroi package health

**Axes:** depth (structural separation of layers, explicit causal non-inference), calibration (zero overreach, zero fabricated health claims), operability (re-executable read-only anchors), adjacency (ADJ-03 contract boundary).  
**Ownership:** TsukuroiR15.ConnectMadoBoundary (read-only research; no config edits, no UI conclusions, request owner validation only).  
**Judged on:** depth.

---

## 1. Executive Summary & Synthesis

The assignment maps **mado desktop behavior** versus **tsukuroi package health** on host `plazir27` following the operator-reported `2026-10-20 04:25:16-0300` partial upgrade of `libinput` (1.31.3-1 -> 1.32.0-1) and installation of `libinput-tools` (1.32.0-1).

### The Non-Obvious Move: Invariant-Decoupled Layer Boundary
A naive analysis might either:
1. Infer that because `libinput` was partially upgraded and package state is `DEGRADED`, the user desktop / input delivery / compositor state is broken or degraded.
2. Infer that because Hyprland is running (`running` unit state, clean config load, active IPC socket), the package upgrade was completely harmless and the system is `HEALTHY`.

**Both inferences are categorically rejected.**
We formulate a strict, non-obvious **four-layer causal separation** grounded in `PROVINCE.md`, `mado-shokunin/PROVINCE.md`, `mado-shokunin/corpus/knowledge/input-debugging-boundaries-r15.md`, and the contract route `ADJ-03` (`corpus/knowledge/adjacency-handoffs-fleet-r1.json`):
- **Layer 1: OS Package Substrate & Update Safety (Tsukuroi Province)**
  - Measured state: `libinput 1.32.0-1` installed via `pacman -S --needed --noconfirm` against a stale sync database (born `2026-10-18T17:11:00Z`).
  - 413 pending updates in sync DB (`mkinitcpio`, `plymouth`, `systemd`, `linux`, `glibc`, `mesa`, `aquamarine`, etc.).
  - Verdict: `DEGRADED` / `BLOCKED_FOR_AGENT_PACKAGE_ACTION`.
- **Layer 2: Process Memory & Shared Object Linkage (Substrate Invariant)**
  - Running compositor was launched under `libinput.so.10` (mapped `1.31.3-1` at boot/launch).
  - On disk: `libinput.so.10` soname preserved in `1.32.0-1`; `ldd -r` on `aquamarine` shows 0 unresolved symbols.
  - Crucial boundary: Mapped in-memory ELF image != on-disk package archive. No process was restarted.
- **Layer 3: Compositor Configuration Plane & Protocol Binding (Mado Province)**
  - Hyprland config orchestrator (`~/.config/hypr/hyprland.conf`, 18 includes, 32 lines).
  - Wayland protocol globals: `wl_seat` (interface version 9 in S041), `zwlr_output_manager_v1`, etc.
  - Mado owns declarative configs (`~/.config/hypr/`, `waybar`, `walker`, terminals, themes, idle/lock).
- **Layer 4: End-to-End User Experience & Visible UI Delivery (Operator Domain)**
  - Event delivery: hardware keypress -> kernel evdev -> libinput context -> compositor policy -> Wayland client focus surface (`wl_keyboard.enter` / `wl_pointer.enter`) -> toolkit text insertion.
  - Neither tsukuroi nor mado possesses runtime authorization, screenshot authority, or input injection permissions to assert UI health.

---

## 2. Structural Evidence Map

| Plane / Layer | Controlling Repo | Controlling Source / Anchor | Measured Observation | Falsifiable Boundary / What Remains Unproved |
|---|---|---|---|---|
| **OS Package State** | `tsukuroi-shokunin` | `PROVINCE.md:6-14`; `host-snapshot.json:probes` | `libinput 1.32.0-1` installed at `2026-10-20T04:25:16-0300` (`pacman.log:2429-2436`). Sync DB mtime: `2026-10-18T17:11:00Z`. `pacman -Qu` yields 413 pending updates. | **Proves:** Package drift and partial upgrade violation. **Does NOT prove:** Desktop crash, input failure, or UI brokenness. |
| **Boot Hook Coupling** | `tsukuroi-shokunin` | `initramfs-v42-sysroot-recovery.md`; `host-snapshot.json` | `mkinitcpio 41.1-1` installed (42.2-1 pending). Hooks `btrfs-overlayfs:4` and `plymouth:11` require `/new_root`. | **Proves:** Full upgrade `-Syu` is blocked until hooks/operator gate clears. Latent boot breakage, not active desktop failure. |
| **Compositor Config** | `mado-shokunin` | `../mado-shokunin/PROVINCE.md:3-16`; `hyprland-config-plane.md` | `~/.config/hypr/hyprland.conf` orchestrator with 18 includes; `hyprctl configerrors` historically empty. | **Proves:** Config plane syntax. **Does NOT prove:** Dynamic event delivery or physical monitor rendering. |
| **Input Debugging Boundary** | `mado-shokunin` | `input-debugging-boundaries-r15.md:29-38` (S051/S052) | `libinput list-devices` documents built-in defaults, not Hyprland's active configuration; `wl_seat` capability bits != client delivery. | **Proves:** Layer ladder separation. **Does NOT prove:** Client focus, shortcut execution, or IME input. |
| **Adjacency Contract** | Shared (ADJ-03) | `corpus/knowledge/adjacency-handoffs-fleet-r1.json:60-72` | Trigger: UI visible symptom. Retains: OS package, GPU, user units. Recipient: `mado`. | **Forbidden inference:** "An active user unit proves that the visible UI works." "A package defect proves a desktop defect." |

---

## 3. Second-Order Effects Across Substrates

1. **Runtime Execution Substrate:**
   - The partial upgrade touched disk files (`/usr/lib/libinput.so.10.15.0`, headers, docs, tools).
   - The live compositor process was not signaled, restarted, or re-executed. It retains memory-mapped text segments from the pre-transaction inode.
   - Any *newly spawned* subprocess linking `libinput` (e.g. ad-hoc `libinput-tools` CLI runs) executes against `1.32.0-1`, while the compositor runs `1.31.3-1`.
2. **Contract & Interface Substrate:**
   - Sibling province integrity: `tsukuroi` explicitly refuses UI conclusions (`PROVINCE.md:26-29`). `mado` explicitly refuses package state mutations and OS repair (`../mado-shokunin/PROVINCE.md:12-14`).
   - S051 (`libinput` tools documentation) and S052 (`wayland.xml` seat contract) demonstrate that tool outputs (e.g. `libinput-list-devices`) represent built-in hardware defaults, not active desktop settings.
3. **Verification & Gate Substrate:**
   - No cross-lane gate execution: Tsukuroi never invokes `mado-verify.sh`; Mado never invokes `tsukuroi-census.sh`.
   - Any future verification of the desktop must proceed via Mado's read-only inspection methods, not OS-level package assertions.

---

## 4. Bounded Recommendations for Operator & Lane Leads

1. **Strictly Preserve ADJ-03 Contract:**
   - Do NOT file an ADJ-03 defect ticket to `mado` for the `libinput` partial upgrade. The package incident is 100% owned by `tsukuroi` and the operator.
   - Only if a concrete visual/binding symptom is reported (e.g., cursor freeze, gesture failure, compositor crash) should an ADJ-03 packet be prepared, providing symptom time, OS probe exits, and config surface pointer.
2. **Handoff to Operator (Read-Only Stance Maintained):**
   - No package installation, downgrade, rollback, or daemon restart is permitted.
   - The operator owns full-system upgrade clearance via the `mkinitcpio` 42 hook safety gate (`/sysroot` transition).
3. **Request Owner Validation Only:**
   - Mado owner validation: Confirm that desktop config structures (`hyprland.conf`, bindings, toggles) remain unmutated by the OS event.
   - Tsukuroi owner validation: Maintain `BLOCKED_FOR_AGENT_PACKAGE_ACTION` in C2 `partial-upgrade-recheck-r15.json` without asserting UI degradation.

---

## 5. Exact Sources, Limits, and Tooling

### Sources Opened & Cited
- `tsukuroi-shokunin/PROVINCE.md:3-75` (Core domain, Refuses, ADJ-01..07 handoff contract).
- `tsukuroi-shokunin/corpus/knowledge/adjacency-handoffs-fleet-r1.json:60-72` (ADJ-03 route definition).
- `tsukuroi-shokunin/corpus/knowledge/adjacency-handoffs-fleet-r1.md:20-55` (Handoff rules & counterexamples).
- `tsukuroi-shokunin/.ufo/waves/round-15/build/host-snapshot.json` (Probes: `package_versions`, `pending_updates`, `sync_metadata`, `libinput_log`, `boot_hook_mentions`).
- `tsukuroi-shokunin/.ufo/waves/round-15/build/HostSnapshot.md` (Capture metadata: 2026-10-20T07:44:39Z).
- `../mado-shokunin/PROVINCE.md:3-16` (Mado domain, owns, refuses).
- `../mado-shokunin/corpus/knowledge/input-debugging-boundaries-r15.md:1-93` (S051 tools.rst, S052 wayland.xml, layer ladder).
- `../mado-shokunin/corpus/lessons/round-15.md:1-60` (M2 partial upgrade mistake analysis, `libinput 1.31.3-1 -> 1.32.0-1`).

### Limits
- Static research and host snapshot review only. No live interactive probes or input event captures performed.
- Running compositor memory map was not probed (`/proc/<pid>/maps` was not read).
- No test suite, gate, or verification script was executed; no check is claimed as passed.

### Tools Recorded (Rules directive)
- Local tools used: `read`, `glob`, `grep`, `write`.
- Tools installed or updated: **none**.
- Package, service, or sudo operations: **none**.
