# CrossBootSafety — Boot-Chain Hazard Audit and Cross-Claim Safety Synthesis

**Seat:** `TsukuroiR19Recovery.CrossBootSafety` (connector leaf; author-dispatched, not outside closure)  
**Role:** UFO-FSD connector  
**Production Lane:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`  
**Baseline:** `0cbc34dd6b20896085a8fb07943e3ea4027d8472` (`.ufo/waves/round-20/preregister.json:3`)  
**Declared Axes:** C1 **adjacency** (lowest, ordinal 8, delta 0), C2 **operability** (ordinal 9, delta 0), C3 **calibration** (ordinal 9, delta 0)  
**Contract:** NO-EXEC: `read`, `grep`, `glob`, `write` only; no bash/eval, subprocesses, tests, builds, lint, formatters, host access, git mutations, or target execution. Boot images remain UNKNOWN; no clearance.  

---

## 1. Audit Target & The Boot-Chain Hazard Surface

The canonical boot-chain hazard is the architectural transition in upstream `mkinitcpio >= 42`:
1. **The Root Mountpoint Shift:** Upstream `mkinitcpio 42` moved the busybox initramfs root mountpoint from `/new_root` to `/sysroot` (S015, S016; `corpus/SOURCES.md:21-22`).
2. **Third-Party Runtime Hook Path Invariant:** Runtime hooks configured on this host—specifically `/usr/lib/initcpio/hooks/btrfs-overlayfs` (line 4: `root_mnt="/new_root"`; S021) and `/usr/lib/initcpio/hooks/plymouth` (line 11: `plymouth update-root-fs --new-root-dir=/new_root`; S022)—hardcode `/new_root`.
3. **The Silent Failure Mechanism:** Under an unmodified busybox init with root at `/sysroot`, `/usr/lib/initcpio/hooks/btrfs-overlayfs` executes `findmnt --mountpoint "$root_mnt" ... || return 0`, which fails against `/new_root` and silently exits 0 before mounting OverlayFS. On a Btrfs snapshot boot, this degrades userspace boot into an unmodifiable, read-only subvolume (`corpus/knowledge/initramfs-v42-sysroot-recovery.md:14,48`).
4. **The Buildroot Compatibility Symlink:** While upstream mkinitcpio 42.x MR !482 added a buildroot symlink `new_root -> sysroot` (`/usr/lib/initcpio/functions:1212-1213`; S057, S059; `corpus/knowledge/boot-chain-r17.md:47-51`), that resolution was verified only in unprivileged namespace emulation on a writable `tmpfs` (`overlay-emulation.txt:40-48`). The Btrfs-specific read-only snapshot mounting behavior (`ro=true`) was not executed on live hardware.

**Mandate:** Audit all round-20 candidate code across the four inherited worktrees and all round-20 report wording in the production lane to ensure:
- Static checks never claim host safety or operational clearance.
- No prohibited commands (`pacman -Syu`, `mkinitcpio`, `limine-update`, `reboot`, mutating `systemctl`) are proposed or authorized.
- Any wording leak or overclaim is explicitly identified and fenced.

---

## 2. Evidence from Candidate Worktrees and Round-20 Reports

### A. Candidate Worktrees (The Four Inherited Implementations)

1. **Candidate Worktree 1: Binder (`/tmp/tsukuroi-r20-binder-20261021`)**
   - **Target:** `tools/_revision.py` and `tools/check-revision-binding.py` (`seeded-implementation.json:6`).
   - **Audit Findings:** Modifies hexadecimal object-ID resolution (`_object_commit`) to prioritize object lookups before ref peeling. Fixtures use sandboxed temporary git repositories (`ghost_hex_branch`, `ghost_full_hex_annotated_tag`, decoy branches).
   - **Boot-Chain & Safety Wording:** Contains zero references to `/sysroot`, `/new_root`, `mkinitcpio`, or host boot state. Proposes no commands against host packages, services, or bootloaders. Completely inert relative to the boot hazard.

2. **Candidate Worktree 2: Registry (`/tmp/tsukuroi-r20-registry-20261021`)**
   - **Target:** `tools/check-registry-coverage.py` (`seeded-implementation.json:7`).
   - **Audit Findings:** Lines 31–34 define:
     ```python
     AUDIT_LIVE_MAP = (
         "live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; "
         "selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; "
         "no live DEGRADED; not operator clearance")
     ```
     Lines 270–288 (`_audit_live_map`) enforce that the operative `boot-chain-audit` row matches this string exactly.
   - **Boot-Chain & Safety Wording:** Static checks strictly forbid claiming host safety:
     - `0` is explicitly qualified as `0 CONSISTENT/observation` (an observation of UKI metadata, not a host health verdict).
     - Explicitly mandates `"not operator clearance"`.
     - Explicitly mandates `"no live DEGRADED"`, preventing conflation with census plane degradation.
     - Docstring at line 271 states: `"Finite documented schema-v2 contract, not inference from arbitrary source."`
     - **Leak Status:** No leak found. The candidate gate actively enforces non-clearance.

3. **Candidate Worktree 3: Adjacency (`/tmp/tsukuroi-r20-adjacency-20261021`)**
   - **Target:** `tools/check-adjacency-anchors.py` (`seeded-implementation.json:10`).
   - **Audit Findings:** Lines 44–50 define `OWNERSHIP_CORRECTION` and validate the exact append to `PROVINCE.md:148-152`:
     ```text
     R20-OUT009: OUT-009 is Revenger's sibling declaration of reverse engineering of shipped artifacts — native binaries, managed assemblies, Electron/JavaScript packages, Android APKs, archives, firmware, browser/Electron runtime evidence. It is not a tsukuroi grant of ownership. Kaidoku/Revenger arbitration remains unresolved; ask the protocol integrator before an internals handoff. No configuration, service, package, boot or sibling-file write is authorized.
     ```
   - **Boot-Chain & Safety Wording:** Line 50 explicitly mandates: `"No configuration, service, package, boot or sibling-file write is authorized."`
   - **Leak Status:** No leak found. The gate prevents any attribution from being converted into remediation or boot-write authority.

4. **Candidate Worktree 4: Execscope (`/tmp/tsukuroi-r20-execscope-20261021`)**
   - **Target:** `tools/check-recheck-commands.py` (`seeded-implementation.json:8`).
   - **Audit Findings:**
     - Line 62: `DEFAULT_FORBID = ("pacman", "checkupdates", "yay", "paru", "mkinitcpio", "limine-update")`. Banned binaries directly include bootloader and package mutators.
     - Lines 289–355: `systemctl_violations` filters `--exec-log` lines, rejecting mutating verbs (`restart`, `enable`, `daemon-reload`, `kill`, `set-property`) and conservative unknown verbs with `EXEC-STEER-VIOLATION`.
     - Read-only queries (`cat`, `show`, `status`, `list-units`, `list-timers`, `is-active`, etc.) pass.
   - **Boot-Chain & Safety Wording:** Enforces that recheck procedures never invoke `mkinitcpio` or package managers.
   - **Leak Status:** No leak found. Mutating commands are caught and rejected.

---

### B. Audit of Round-20 Build and Falsify Reports

Every report in `.ufo/waves/round-20/build/` and `.ufo/waves/round-20/falsify/` was audited for host-safety claims, boot actions, and boot-chain wording:

1. **`SrcHookFreshness.md:8-10`:**
   - Evaluated `/usr/lib/initcpio/hooks/plymouth:11` and `btrfs-overlayfs:4` (`/new_root` references).
   - Finding: Explicitly bounds evidence: *"Supports: these two hook files, as read at those paths on the access date, contain `/new_root` references... Does NOT support: that either hook ran, is active in a boot image, or will work/fail at boot; that the host uses `/new_root` or `/sysroot`; any package-version, configuration, service, or boot-readiness claim. No such inference is made... Reject broader host/boot-safety or execution claims."*
2. **`SrcAuditCodes.md:34-35`:**
   - Evaluated `tools/boot-chain-audit.sh:81-86,794-805`.
   - Finding: Explicitly disclaims host safety: *"Does not support: that the selftest was executed or passed; that any host's boot chain is safe, consistent, or currently in use; or any host/boot-safety certification. No command was run. Reject any broader claim that this source demonstrates actual host state or boot safety."*
3. **`OracleC1.md:25`, `OracleC2.md:50`, `OracleC3.md:5`:**
   - C1 Oracle: *"It must not choose kaidoku or revenger, transfer handoff authority, or claim sibling/host safety."*
   - C2 Oracle: *"supports the typed distinction only, never a host/boot-safety certificate."*
   - C3 Oracle: *"These rules support C3's semantic distinction: live 1 DEGRADED is false; a selftest-only 1 is not a live verdict. They do not claim host readiness or boot safety."*
4. **`ScribeErrata.md:53` & `ScribeMistakes.md:39`:**
   - ScribeErrata: *"Out of scope: current host/boot-image state (UNKNOWN), initramfs contents, hook freshness, packages, services, mounts, reboot/recovery, credentials/private configuration, routing, execution authorization and independent R20 closure. No boot image was inspected or dumped; no runtime invoked or delegated."*
   - ScribeMistakes: *"Outside scope: ... boot safety. Boot images remain UNKNOWN. Nothing here authorizes a transaction, service action or reboot."*
5. **`ConnCrossScope.md:78-83,168`:**
   - Binds C1's `"No ... boot ... write is authorized"` directly to C2's `DEFAULT_FORBID` (`pacman`, `mkinitcpio`, `limine-update`) and confirms: *"Host/boot state remains UNKNOWN. No packages installed, upgraded, or removed; no services restarted."*
6. **`MapLiveStatuses.md:11-15` & `MapHighestOperative.md:37`:**
   - Confirms `0 CONSISTENT` is an observation of schema-v2 paths and cannot be interpreted as host readiness. Explicitly disclaims operator clearance.

**Comprehensive Finding on Leaks:** Across all inspected candidate worktree sources, PREREGISTER declarations, and round-20 build/falsify reports, **zero host-safety or boot-safety claims leaked**, and **zero prohibited boot actions or commands were proposed**. All seats maintained literal `Scope: executed=none`.

---

## 3. Explicit Contradictions Across Surfaces

1. **Static Typing vs. Dynamic Boot Reality:**
   - *Contradiction:* In `tools/boot-chain-audit.sh:794-806`, evaluating UKI images with `/new_root -> sysroot` relative symlinks outputs exit 0 (`0 CONSISTENT`). In `corpus/knowledge/boot-chain-r17.md:71-73`, the table labels this `PATH-ALIASED-EMULATED`. An uncalibrated reader could infer that exit 0 means "booting this image is verified safe."
   - *Reality:* The emulation was conducted in an unprivileged namespace on a writable `tmpfs` (`overlay-emulation.txt:40-48`). An actual boot into an encrypted Btrfs snapshot involves kernel VFS mounting, Plymouth late-hook initialization, and root switching. Exit 0 indicates *syntactic consistency of image structures*, NEVER empirical boot safety.
   - *Resolution:* C3's `check-registry-coverage.py` resolves this contradiction by strictly requiring the exact phrase `"not operator clearance"` and `"0 CONSISTENT/observation"` in the operative table.

2. **Finding Referral vs. Remediation Authorization:**
   - *Contradiction:* Sibling finding handoffs (e.g., ADJ-06 regarding reverse-engineered binaries, or Mori's telemetry) frequently lead downstream agents to attempt substrate remediation (rebuilding initramfs via `mkinitcpio -P`, reinstalling packages via `pacman -S`, or restarting units via `systemctl restart`).
   - *Reality:* Tsukuroi tracks OS state and health, but neither owns binary internals nor authorizes destructive live changes.
   - *Resolution:* C1 (`PROVINCE.md:150`) explicitly resolves this by terminating the authority chain: `"No configuration, service, package, boot or sibling-file write is authorized."`

3. **Recheck Procedures vs. Steer-Safety Gate:**
   - *Contradiction:* Historical knowledge files frequently included backticked procedure lines invoking `pacman -Q` or package queries (e.g. `initramfs-v42-sysroot-recovery.md:3`).
   - *Reality:* In multi-agent environments, backticked procedure lines are copied into shell calls by unguided agents, violating steer boundaries.
   - *Resolution:* C2 (`check-recheck-commands.py`) permanently bans `pacman`, `mkinitcpio`, and `limine-update` via `DEFAULT_FORBID`, and requires directory-name inspection (`/var/lib/pacman/local/<pkg>-*`) instead of package manager execution.

---

## 4. Affected Axes

1. **Calibration (C3):**
   - Directly affected: Guarantees that `audit_live_map_errors` drops 1→0 only when the highest operative table explicitly disclaims operator clearance and marks `0 CONSISTENT` as observation-only.
2. **Operability (C2):**
   - Directly affected: Keeps the update-safety gate locked. Guarantees that execution-log checking permanently flags mutating commands (`EXEC-STEER-VIOLATION`), preventing accidental unbootable host states.
3. **Adjacency (C1):**
   - Preserved and uncompromised: Adjacency anchor verification strictly enforces attribution to Revenger while refusing boot, package, or service write authority.

---

## 5. Proposed Non-Obvious Move: The Tripartite Boot-Chain Safety Invariant

**Move:** Formally bind the round's three claims into a **Tripartite Boot-Chain Safety Invariant** during L1 integration synthesis:

$$\text{Tripartite Safety Invariant} = \underbrace{\text{C1: Attributed Authority Boundary}}_{\text{No boot/package writes authorized}} \;\land\; \underbrace{\text{C2: Exec-Log Steer Enforcement}}_{\text{DEFAULT\_FORBID(mkinitcpio, pacman)}} \;\land\; \underbrace{\text{C3: Live-Map Calibration}}_{\text{live 0 = observation, not clearance}}$$

### Coordination Details:
1. **Registry Plane (C3 Calibration Synthesis):**
   - When integrating `check-registry-coverage.py` from `/tmp/tsukuroi-r20-registry-20261021/`, ensure `AUDIT_LIVE_MAP` enforces both `"live: 0 CONSISTENT/observation"` and `"not operator clearance"`.
   - Fix the Markdown fence parser defect identified by `MapHighestOperative.md:32-34` so that fenced code blocks cannot decoy the highest operative table.
2. **Province Plane (C1 Adjacency Synthesis):**
   - When integrating `check-adjacency-anchors.py` from `/tmp/tsukuroi-r20-adjacency-20261021/`, commit `PROVINCE.md:148-152` unchanged.
   - Verify that line 150 retains the complete prohibition: `"No configuration, service, package, boot or sibling-file write is authorized."`
3. **Execution Plane (C2 Operability Synthesis):**
   - When integrating `check-recheck-commands.py` from `/tmp/tsukuroi-r20-execscope-20261021/`, confirm `DEFAULT_FORBID` retains `mkinitcpio` and `limine-update` alongside `pacman`.
   - Ensure `systemctl_violations` in `--exec-log` continues to catch mutating verbs (`restart`, `enable`, `daemon-reload`) and unknown verbs.

**Second-Order Benefit:** This move unifies static analysis across the three independent axes without altering any preregistered metric (C1: 0→1, C2: 0→9, C3: 1→0). It prevents downstream agents or automated evaluators from treating C3's `0 CONSISTENT` as a justification to unlock `pacman -Syu` or perform bootloader modifications.

---

## 6. Risks and Falsifiers

1. **Semantic Conflation Risk:**
   - *Risk:* An operator or verifier reading `tools/boot-chain-audit.sh` exit 0 might assume the mkinitcpio 42 `/sysroot` transition is resolved for live reboots and attempt `pacman -Syu`.
   - *Falsifier / Guard:* `check-registry-coverage.py` rejects any table entry where the verdict omits `"not operator clearance"` or fails to qualify `0` with `/observation`.
2. **Recheck Procedure Evasion:**
   - *Risk:* A future knowledge update adds a procedure with a clustered shell flag (e.g. `bash -ec 'mkinitcpio -P'`) that bypasses simple `-c` matching.
   - *Falsifier / Guard:* `check-recheck-commands.py` includes `mkinitcpio` in `DEFAULT_FORBID` and catches nested invocations in `invocations()`.
3. **Registry In-Place Tampering:**
   - *Risk:* An integrator attempts to modify `corpus/knowledge/adjacency-anchors-r19.json` directly.
   - *Falsifier / Guard:* `check-adjacency-anchors.py:146` enforces exact hash and field match against `OWNERSHIP_PIN`, failing with `OWNERSHIP-CORRECTION-INVALID`.

---

## 7. Verification Plan (For L1 Post-Wave Integrator)

*Note: Per seat contract, NO verification commands were executed by this leaf seat. The commands below are specified for L1 post-wave evaluation.*

1. **C3 Live-Map Calibration Gate:**
   ```bash
   python3 tools/check-registry-coverage.py --revision <REV> --audit-live-map
   ```
   - *Expected output:* `{"counts":{"findings":0},"status":"PASS"}` with `audit_live_map_errors=0; exit=0`.
   - *Negative control:* Altering `SKILL.md` to remove `"not operator clearance"` or restore `1 DEGRADED` yields `REGISTRY-AUDIT-LIVE-MAP; exit=1`.
2. **C1 Ownership & No-Boot-Write Gate:**
   ```bash
   python3 tools/check-adjacency-anchors.py --revision <REV> --ownership-corrections
   ```
   - *Expected output:* `ownership_corrections=1; exit=0`.
   - *Negative control:* Omitting `"boot"` from `PROVINCE.md:150` yields `OWNERSHIP-CORRECTION-INVALID; exit=1`.
3. **C2 Exec-Log Steer Safety Gate:**
   ```bash
   python3 tools/check-recheck-commands.py --revision <REV> --exec-log <lane-log>
   ```
   - *Expected output:* `exec_violation_count=0; exit=0`.
   - *Negative control:* An exec-log containing `$ mkinitcpio -P` or `$ systemctl restart limine-snapper-sync` yields `EXEC-STEER-VIOLATION; exit=1`.

---

## 8. Limitations & Scope

- **Seat Bounds:** Leaf connector seat (`CrossBootSafety`). No subagents spawned; no task delegation.
- **Tools Used:** Only `read`, `grep`, `glob`, `write` (sole write to `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/falsify/CrossBootSafety.md`).
- **NO-EXEC Policy:** Zero shell commands, evaluations, tests, builds, lint runs, formatters, or host probes executed.
- **Host Substrate:** Running kernel, bootloader configuration, package databases, and boot images remain UNKNOWN. No packages installed, upgraded, or removed. No services restarted. No reboot proposed or taken.
- **Tool Installs/Updates:** None (`Tool installs/updates: none`).

Scope: executed=none
