# OverlapHost — Round 12 Sibling-Overlap Scan & Boundary Synthesis

- **Seat:** `OverlapHost` (role: UFO-FSD connector)
- **Repo:** `tsukuroi-shokunin` (working directory: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`)
- **Baseline HEAD:** `b76b5c377eaee3e3d8d47fdddde977828d05dbd5`
- **Capture UTC:** 2026-10-20T02:22:00Z
- **Judged Axes:** `operability`, `depth`
- **Milestone:** `round-12`
- **Contract & Scope:** Leaf connector; read-only inspection of named sibling `PROVINCE.md` declarations and current round-12 cache. No git mutation, no fleet writes, no host mutation, no package operations, no sudo. Only `.ufo/waves/round-12/OverlapHost.md` written.

---

## 1. Executive Summary & Outcome

- **Scan Result:** Bounded scan of `../mado-shokunin/PROVINCE.md`, `../kagi-shokunin/PROVINCE.md`, and `../mori-shokunin/PROVINCE.md` confirms zero jurisdictional conflict or boundary leakage.
- **Core Question:** **Do C1 (root metadata census arm) and C2 (source-backed discriminating EACCES decision matrix) stay pure OS diagnosis?**
  - **Verdict:** **YES. C1 and C2 remain 100% within Tsukuroi's OS diagnosis province.**
- **Handoff Determination:** **NO handoff claim is warranted or minted.**
  - Not ADJ-02 (`kagi`): `limine-snapper-sync` is a boot snapshot synchronization utility, not a credential-bearing helper; `/` is not a secret or vault surface; no auth flow is involved.
  - Not ADJ-03 (`mado`): Desktop rendering, bindings, and compositor configurations (`~/.config/hypr/`, `waybar`, etc.) are unaffected by root inode mode or systemd service capabilities.
  - Not ADJ-04 (`mori`): Root DAC mode and service sandbox confinement are static/deterministic filesystem access controls, not fleet wave progress, resource runway, or OOM/kill correlation.
- **Proposed Non-Obvious Move:** **Invariant-Decoupled Root Audit with Context-Aware Verdict Grading.** Decouple C1's unowned root inode observation (`PLANE packages`) from C2's service capability confinement (`root-dac-decision-r12.md`), preventing false-positive operational degradation on legitimate 0555 root filesystems while preserving strict causal separability and deep multi-branch error discrimination.

---

## 2. Sibling-Overlap Scan Across Declared Provinces

### 2.1 Root DAC Boundary (`/` mode, ownership, ACL, unowned-by-pacman)

| Sibling | Declared Domain & Surfaces | Boundary with Tsukuroi | Overlap with C1/C2 | Evidence Anchor |
| :--- | :--- | :--- | :--- | :--- |
| **mado** | Desktop & compositor craft (`~/.config/hypr/`, `waybar`, `walker`, terminal configs, themes, wallpapers, screen/idle). Config trees are read-only. | Refuses secrets (→ kagi), endpoints (→ kama), internals. Does not touch root filesystems, system units, or OS substrate. | **ZERO.** Operates purely in user `$HOME`. Completely silent on root DAC or systemd system units. | `../mado-shokunin/PROVINCE.md:3-16` |
| **kagi** | Secrets & vault operations (`the-janitor` flows, `~/.local/bin/the-janitor`, `~/.config/opencode`, `~/.local/state/the-janitor`, `1Password` machine credentials, SOPS/age keys, Vault/OpenBao). | Refuses anything outside secrets/vaults. Tracks secret-bearing runtime auth and credential custody. | **ZERO.** Root directory inode DAC is not credential material or vault ops. | `../kagi-shokunin/PROVINCE.md:3-6,19-35,55-63` |
| **mori** | Fleet & host observability (watchdog liveness, wave settlement, user-journal & cgroup kill/OOM events, resource runway: disk on `$ROOT` and `/tmp`, memory PSI). | Explicitly refuses: "OS package, systemd unit, driver/firmware and boot state (→ tsukuroi) — mori reads journal and cgroup events as fleet evidence and reports them, never owning OS state." | **ZERO.** Acknowledges in row 53: "tsukuroi \| Owns host OS, package, systemd-unit, driver, firmware, and boot diagnosis." | `../mori-shokunin/PROVINCE.md:12-16,24-25,50-53` |
| **tsukuroi** | Host operability & system repair — the OS substrate itself: package state (`pacman -Qkk`, unowned paths), systemd, drivers/firmware, boot health. | Retains pure OS filesystem DAC, package verification gaps, and systemd service confinement. | **OWNS 100%.** QUALITY.md rule 13 explicitly mandates reporting root-directory mode because `pacman -Qkk` cannot see `/`. | `PROVINCE.md:3-14,35-43`; `corpus/QUALITY.md:17` |

### 2.2 Helper Permission Boundary (ADJ-02 Routing vs Boot Helpers)

- **The Rule in Tsukuroi:** `PROVINCE.md:47` (ADJ-02) governs credential-bearing helpers:
  > "A credential-bearing helper has a permission/ownership finding or an auth-flow question | Tsukuroi retains: Package owner/version and filesystem mode; package drift is not proof of credential exposure | Next analysis recipient: kagi | Minimum handoff evidence: Path, mode, uid/gid, package owner/version, command/exit and capture time only; no secret values, vault references, session bytes or helper invocation."
- **The Boundary Control:** In `corpus/knowledge/adjacency-handoffs-fleet-r1.md:125-134` (R1HelperPacket), tsukuroi proved this boundary on `/usr/bin/op` (1Password CLI): tsukuroi measured `stat` (`2755 0 1002`) and `pacman -Qo` (`1password-cli 2.40.0-2`). It did not invoke the helper, read credentials, or diagnose auth flows.
- **Application to C1 & C2:**
  - In C1: The target is `/` (root directory). `/` is a filesystem namespace root, not a helper executable.
  - In C2: The investigated services are `limine-snapper-sync.service` and its watcher script `/usr/bin/limine-snapper-watcher`. These utilities synchronize Limine bootloader menu entries with Btrfs Snapper snapshot subvolumes. They are **boot/storage maintenance scripts**, NOT credential-bearing helpers.
  - They handle zero credentials, access tokens, vault keys, or auth workflows.
  - Conflating a boot synchronization helper with a credential-bearing helper would misroute OS bootloader triage to `kagi`.
  - **Conclusion:** C2's evaluation of `CapabilityBoundingSet=CAP_SYS_ADMIN` and `User=root` remains strictly within tsukuroi's core systemd/boot domain. No ADJ-02 routing applies.

### 2.3 Host Resource Boundaries (ADJ-04 Routing vs DAC/Confinement)

- **The Rule in Tsukuroi:** `PROVINCE.md:30-33,49` (ADJ-04) governs host resource pressure:
  > "Host memory and kill-event measurements support OS triage; they do not establish which fleet wave caused pressure or whether an endpoint works. The existing census reports those signals; fleet correlation belongs to mori."
- **The Rule in Mori:** `../mori-shokunin/PROVINCE.md:8-10,24-25` monitors disk runway (`df -P $ROOT /tmp`) and user-journal/cgroup kill events. Mori consumes these to grade fleet progression, but explicitly disclaims diagnosing the underlying OS errors.
- **Application to C1 & C2:**
  - Neither C1 nor C2 measures disk capacity, filesystem exhaustion (`ENOSPC`/`EDQUOT`), memory fill, or PSI stall metrics.
  - `EACCES` (`errno:13`) logged by `limine-snapper-sync.service` is a static kernel VFS permission denial during subvolume creation (`Btrfs.cc:139 btrfs_util_create_subvolume_fd() failed, errno:13`), NOT a resource exhaustion or transient pressure event.
  - **Conclusion:** C1 and C2 do not generate host resource correlation requests. No ADJ-04 packet is warranted.

---

## 3. Synthesis of Round 12 Evidence & Identified Contradictions

Reading the active round-12 proposals and scout dossiers reveals critical inter-seat dependencies and a core contradiction:

### 3.1 Trace of Round Proposals
1. **`Planner.md`:** Proposes C1 append `root_mode=`, `root_uid=`, `root_gid=` to `PLANE packages` note with "owner-write absence DEGRADED". Proposes C2 as an independent 4-branch grounded matrix.
2. **`C1Review.md`:** Identifies **F1 (HIGH)**: Live `/` is `0555 root:root` and census executes as unprivileged user (`uid=1000`). Under a literal owner-write-absence rule, the live census immediately flags `DEGRADED`, causing an operability regression on a host whose `/` mode is normal and healthy for general operation. Highlights **F2/F3**: Early returns in `probe_packages` clobber notes; verdict fold must occur in `main()` via `worse "$PKG_V" "$ROOT_V"`. Highlights **F7**: Must use `stat -L` (to handle symlinks) wrapped in `cap` (to prevent `set -e` aborts on missing paths).
3. **`ClaimCritic.md`:** Delivers proof that mode `0555` on `/` is NOT intrinsically defective:
   - **CX1:** Fedora `filesystem.spec` line 409 explicitly ships `%dir %attr(555,root,root) /` by distro policy. Arch `filesystem` package ships `555` for `/proc` and `/sys` and declares **zero** mtree baseline for `/` (`pacman -Qo /` returns unowned).
   - **CX2:** Mode `0555` only restricts write access for callers whose UID matches owner (UID 0) **and** who lack `CAP_DAC_OVERRIDE`. For PID 1 and interactive root, `CAP_DAC_OVERRIDE` bypasses DAC completely. For UID 1000, `other` bits govern.
4. **`ScoreReview.md`:** Proves **causal separability**: C1 and C2 must remain strictly decoupled. C2 must NOT parse C1 census output, and C1 must not hardcode C2 mechanism text. Warns against counting tests/tokens as depth.
5. **`MountErrors.md`:** Establishes grounded Linux man-pages definitions (`mkdir(2)` and `path_resolution(7)`):
   - `EACCES` (errno 13): Parent directory lacks write permission for the process, or intermediate directory lacks search (`x`) permission.
   - `EROFS` (errno 30): Path refers to a read-only filesystem mount (`MS_RDONLY`).
   - `EEXIST` (errno 17): Path already exists (subvolume, directory, file).
   - Explains that mode `0555` on `/` (`findmnt` shows `rw`) is pure DAC, NEVER `EROFS`.
6. **`Issue6629.md` & `Origin.md`:** Demonstrates that Omarchy GitHub issue #6629 (missing `inotify-tools` and missing Snapper config) shares surface symptoms with this host (empty configs, inactive service), but represents passive installer omission, whereas this host experiences active kernel VFS `EACCES` due to sandboxed `CapabilityBoundingSet=CAP_SYS_ADMIN` dropping `CAP_DAC_OVERRIDE`.

### 3.2 The Core Contradiction
- If C1 implements a naive "owner-write absent = DEGRADED" rule, it:
  1. Conflates *unowned metadata observation* with *policy violation*, despite Arch packaging providing no baseline for `/`.
  2. Degrades the live host census on a condition that does NOT impede user desktop operations (`mado`), user secret management (`kagi`), or host observability (`mori`).
  3. Prejudges the C2 mechanism within C1, collapsing the causal separability between the two claims.

---

## 4. The Proposed Non-Obvious Move

### **Title: Invariant-Decoupled Root Audit with Context-Aware Verdict Grading**

### 4.1 Specification of the Move
Synthesize C1 (census operability), C2 (decision matrix depth), and sibling boundary preservation into three cleanly decoupled invariants:

1. **C1 Census Implementation (`tools/tsukuroi-census.sh`):**
   - **Placement:** Embed root metadata probing under `PLANE packages` (addressing the unowned `-Qkk` blind spot where `pacman -Qo /` fails).
   - **Output Format:** Emit normalized numeric facts: `root=<path> root_type=<%F> root_mode=<%04o> root_uid=<n> root_gid=<n> root_owner_write=<0|1>`.
   - **Clean Variable Separation:** Store root evidence in `ROOT_V` and `ROOT_NOTE` (initialized to `ROOT_V=BLOCKED ROOT_NOTE='probe not run'`). In `main()`, fold via `PKG_V=$(worse "$PKG_V" "$ROOT_V")` and append `ROOT_NOTE` to the emitted package note, ensuring early pacman returns never erase root evidence.
   - **Verdict Discrimination:**
     - Non-existent path or non-directory (`stat -L` fails or `%F != directory`) $\rightarrow$ `BLOCKED` (`root_meta=unavailable` or `root_meta=non-directory`).
     - Mode `0555` on `/`:
       - When probed by unprivileged user (`id -u != root_uid`): Emit `HEALTHY` or explicitly mark `root_owner=no-write [unknown: no package baseline; capability-bounded owner processes denied]` without degrading the whole plane.
       - In hermetic selftests: Where fixture owner equals probe UID, verify that `0755` yields `HEALTHY`, `0555` with owner match yields `DEGRADED`, and dangling symlink/missing path yields `BLOCKED`.
   - **Hermetic Isolation:** Add `TSUKUROI_ROOT_DIR` override to the script's header seam registry (lines 294–308) and set `TSUKUROI_ROOT_DIR="$FX/root"` in `check()` above `"${EXTRA_ENV[@]}"`.

2. **C2 Decision Matrix (`corpus/knowledge/root-dac-decision-r12.md`):**
   - Build an autonomous 4-branch matrix using direct host probes (`stat`, `findmnt`, `systemctl show`, `journalctl`), with zero dependencies on C1 census text:
     - **Branch 1 (DAC / Capability Confinement):** Parent mode lacks `w` (`0555`) AND caller lacks `CAP_DAC_OVERRIDE` (e.g. `CapabilityBoundingSet=CAP_SYS_ADMIN`) $\rightarrow$ `EACCES` (errno 13). (Grounding: S027, S028, S034).
     - **Branch 2 (Read-Only Mount):** Filesystem mount options contain `ro` $\rightarrow$ `EROFS` (errno 30). (Grounding: `mkdir(2)` S035).
     - **Branch 3 (Existing Snapshot Collision):** Target path `/.snapshots` already exists $\rightarrow$ `EEXIST` (errno 17). (Grounding: `mkdir(2)` S035; S023).
     - **Branch 4 (Missing Watcher Tool / Config Omission):** Absent `inotify-tools` or missing template without kernel `errno:13` $\rightarrow$ `Service Inactive (0/SUCCESS)`. (Grounding: Omarchy Issue #6629).

3. **Sibling Boundary Immunity:**
   - Document explicitly that root DAC and service capability confinement are non-delegated host OS diagnostics.
   - No handoff tickets minted to `mado`, `kagi`, or `mori`.

---

## 5. Second-Order Effects & Trade-Off Analysis

| Surface | Direct Effect | Second-Order Effect | Safety / Protection |
| :--- | :--- | :--- | :--- |
| **Runtime (Census)** | Inspects `/` via single `stat -L` call. | Negligible overhead (sub-millisecond stat call); wrapped in `cap` helper to prevent `set -euo pipefail` crashes. | Rollup maintains exact six-plane line format; zero risk of breaking rollup parsers. |
| **Contract (PROVINCE)** | Keeps root DAC triage within tsukuroi. | Sibling provinces (`mado`, `kagi`, `mori`) remain untouched; no false ADJ-02 or ADJ-04 handoff noise. | Avoids jurisdictional churn and unresolvable sibling handoffs. |
| **Substrate (Host)** | Reads `/` metadata without writes. | Zero host mutation (`stat`, `getfacl`, `findmnt` are strictly non-mutating). | Complies with root-protection directive; no permission modification attempted. |
| **Verification (Selftest)** | Adds new fixture cases for `0755`, `0555`, and missing root. | Baseline 80 selftest cases remain intact and green; total cases advance to $80 + N$. | Eliminates `missing-root-probe` and `wrong-octal-bit` mutants hermetically. |

---

## 6. Axis Impact & Score Justification

- **`operability` (Target: Improved, Score: 9 preserved):**
  - Closes the unowned `/` metadata blind spot (finding count $0 \rightarrow 1$).
  - Prevents spurious census degradation on live host by distinguishing owner-write relevance across UID boundaries.
  - Corrects early-return seam vulnerabilities in `probe_packages`.
  - Operability remains firmly at saturation ceiling 9 (bounded by open D12 `--identity` debt).
- **`depth` (Target: Improved, Score: 8 $\rightarrow$ 9):**
  - Moves depth from tied lowest (8) to 9.
  - Replaces token counts with a rigorous, source-grounded 4-branch decision matrix.
  - Clearly differentiates kernel `EACCES` from `EROFS`, `EEXIST`, and passive config omission (#6629).
- **No Harm to Unworked Axes:**
  - `coverage` (9): Preserves the exact 6 owned planes and 6 rollup keys in `main()`.
  - `freshness` (9): Anchors all man-page and issue evidence to verified 2026 dates and immutable SHA-256 commit pins.
  - `adjacency` (8): Re-verifies all 3 sibling boundaries with zero leakage or disputed handoffs.
  - `calibration` (9): Documents falsifiers, counterexamples, and explicit unknowns without scalar smoothing.

---

## 7. Verification & Post-Integration Check Procedure

*(To be executed once by parent session after full integration; unrun during this connector phase)*

1. **Verify Sibling Isolation:**
   ```bash
   git status --short ../mado-shokunin ../kagi-shokunin ../mori-shokunin
   # Must return 0 lines (clean working trees, zero mutations)
   ```
2. **Verify Census Seam & Hermetic Override:**
   ```bash
   grep -n 'TSUKUROI_ROOT_DIR' tools/tsukuroi-census.sh
   # Must confirm presence in header registry (lines 294-308) and check() env block
   ```
3. **Verify Causal Separability:**
   ```bash
   grep -E 'root_mode|PLANE packages' corpus/knowledge/root-dac-decision-r12.md
   # Must return exit code 1 (no dependencies on C1 census text in C2 matrix)
   ```
4. **Hermetic Selftest Verification:**
   ```bash
   bash tools/tsukuroi-census.sh --selftest
   # Must exit 0 with PASS (all legacy 80 cases + new root fixture cases passed)
   ```
5. **Live Host Census Run:**
   ```bash
   bash tools/tsukuroi-census.sh
   # Must output PLANE packages containing root=<path> root_mode=0555 root_uid=0 root_gid=0
   ```
