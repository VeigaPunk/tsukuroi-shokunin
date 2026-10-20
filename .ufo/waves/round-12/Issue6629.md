# Omarchy Issue #6629 Analysis: Missing Snapper Config Symptom vs. Root Mode & Capability Mechanism

- **Target Source:** https://github.com/omacom/omarchy/issues/6629
- **Verified-at:** 2026-10-19
- **Lane Milestone:** Tsukuroi Round 12 (C1 operability / C2 depth)
- **Role:** Scout (`Issue6629`)
- **Status:** Complete read-only investigation; equivalence rejected.

---

## 1. Issue Record & Anchors

- **URL:** `https://github.com/omacom/omarchy/issues/6629`
- **Title:** `[Bug]: limine-snapper-sync inactive due to missing inotify-tools dependency & missing Snapper root configuration`
- **Author:** `@mikemayuare` (Miguelangel Leon Mayuare)
- **State:** `OPEN` (Labels: `bug`)
- **Created Date:** `2026-08-08T09:23:20Z`
- **Updated Date:** `2026-10-17T13:31:32Z`
- **Target OS / Environment:** Omarchy 3.8.4; Bootloader: Limine (`limine-snapper-sync`); Filesystem: Btrfs; Snapshot Tool: Snapper / `omarchy-snapshot`.

### Verified Quotes and Locations (≤25 words each)

1. **Description — Symptom 1 (Issue body § Description, lines 17-18):**
   > "`limine-snapper-sync.service` defaults to an `inactive (dead)` state because `limine-snapper-watcher` fails with `inotifywait is not installed`."
2. **Description — Symptom 2 (Issue body § Description, lines 19-20):**
   > "Snapper is not initialized with a default `root` configuration (`/etc/snapper/configs/root`), nor is `/.snapshots` mounted as a dedicated subvolume."
3. **Step 2 Observe (Issue body § Steps to Reproduce, line 34):**
   > "Service exits with code `0/SUCCESS` and logs `inotifywait is not installed. Falling back to Snapper plugin integration.` before deactivating."
4. **Step 3 Observe (Issue body § Steps to Reproduce, line 43):**
   > "Output returns no configs (`The config 'root' does not exist`)."
5. **Expected Behavior (Issue body § Expected Behavior, lines 56-57):**
   > "`inotify-tools` should be installed as an explicit dependency"; "A Snapper configuration (e.g., `root`) mapped to `/` should be generated out-of-the-box".
6. **Workaround / Manual Fix (Issue body § Workaround, lines 68, 72):**
   > "`sudo pacman -S inotify-tools`" and "`sudo snapper -c root create-config /`".
7. **Maintainer / Bot Response (@omarchybot comment, 2026-10-17T13:31:32Z):**
   > "`inotify-tools`: it is in `install/omarchy-base.packages`, so 4.x installs it for everyone."
8. **Maintainer / Bot Response — Config creation (@omarchybot comment, 2026-10-17T13:31:32Z):**
   > "On 4.x, `install/config/snapper.sh` creates `/etc/snapper/configs/root` whenever it is missing."

---

## 2. Live Host State & Measured Evidence (Read-Only)

Live non-mutating probes executed on the target host (2026-10-19):

1. **Root Directory Metadata & DAC Mode:**
   - Command: `stat -c '%a %U:%G' / && getfacl -p /`
   - Output: `555 root:root`; ACL shows `user::r-x`, `group::r-x`, `other::r-x`.
   - [obs] Mode `0555` lacks any write permission (`w` bit) for user, group, or others.
   - [obs] Package ownership: `pacman -Qo /` reports `error: No package owns /`. Root directory mode is unmanaged by `filesystem` package mtree.

2. **Package State on Host:**
   - Command: `pacman -Q limine-snapper-sync snapper inotify-tools filesystem`
   - Output:
     - `limine-snapper-sync 1.31.0-1.1`
     - `snapper 0.13.1-3`
     - `filesystem 2025.10.12-1`
     - `error: package 'inotify-tools' was not found` (exit code 1)
   - [obs] `inotify-tools` is absent on this host, matching the surface symptom in #6629.

3. **Service Unit Security Confinement:**
   - Command: `grep -n -E 'User=|CapabilityBoundingSet=|Protect' /usr/lib/systemd/system/limine-snapper-sync.service`
   - Output:
     - Line 6: `User=root`
     - Line 13: `CapabilityBoundingSet=CAP_SYS_ADMIN`
     - Lines 16-22: `ProtectControlGroups=yes`, `ProtectClock=yes`, `ProtectHome=yes`, `ProtectHostname=yes`, `ProtectKernelLogs=yes`, `ProtectKernelModules=yes`, `ProtectKernelTunables=yes`
   - [obs] The service runs as `root` (UID 0) but its capability bounding set is strictly constrained to `CAP_SYS_ADMIN`.
   - [obs] `CAP_DAC_OVERRIDE` is omitted from `CapabilityBoundingSet=`. Per `systemd.exec(5)` (S028), capabilities not in the set are dropped from bounding, permitted, and effective sets.

4. **Runtime Execution & Journal Sequence:**
   - Command: `journalctl -u limine-snapper-sync.service --no-pager -n 25`
   - Sanitized inherited observation: a configuration-create attempt failed with errno 13 during the 2026-10-19 22:48:23–24 window; the watcher subsequently exited successfully after a missing-tool fallback. Raw journal bodies, process ids and boot id were removed by the integrating L1 before landing. This remains historical author-side evidence, not a newly executed command.

5. **Watcher Script Execution Logic (`/usr/bin/limine-snapper-watcher`):**
   - Lines 106–109:
     ```bash
     if [ ! -d "$WATCH_DIR" ]; then
         echo "Directory $WATCH_DIR does not exist. limine-snapper-sync is triggered to initialize a snapper config for $WATCH_DIR."
         "${SYNC_CMD[@]}"
     fi
     ```
   - Lines 111–114:
     ```bash
     if ! command -v inotifywait &>/dev/null; then
         info_msg "inotifywait is not installed. Falling back to Snapper plugin integration."
         exit 0
     fi
     ```
   - [obs] When `/.snapshots` does not exist, the watcher triggers `limine-snapper-sync` to initialize the config.
   - [obs] The initial failure is `errno:13 (Permission denied)` during `snapper create-config /`.
   - [obs] The missing `inotifywait` check at line 111 is executed **only after** `create-config` has already failed. It logs fallback and exits 0, masking the prior permission error from systemd.

---

## 3. Comparison: Symptom vs. Mechanism (Rejection of Equivalence)

| Dimension | Omarchy Issue #6629 | Tsukuroi Host Reality (`snapper-eacces-mechanism.md`) | Mechanistic Difference |
| :--- | :--- | :--- | :--- |
| **Surface Symptom** | `snapper list-configs` returns no configs; `limine-snapper-sync.service` inactive (dead) with 0/SUCCESS. | `snapper list-configs` returns header only (0 configs); service deactivates with 0/SUCCESS. | **Identical symptom**: An operator without deep logs sees exactly the same observable state. |
| **Ascribed Primary Cause** | Packaging/installer omission: `inotify-tools` omitted from base packages; installer branch missed `create-config`. | Dynamic DAC/Capability denial: Mode `0555` on `/` combined with `CapabilityBoundingSet=CAP_SYS_ADMIN` dropping `CAP_DAC_OVERRIDE`. | **Different cause**: #6629 assumes initialization was never attempted; host shows initialization was attempted and denied by kernel VFS. |
| **Failed Operation** | Absence of execution (`snapper` command was never called out-of-the-box). | `snapper --no-dbus -c root create-config /` failed at `Btrfs.cc:139` with `errno:13 (Permission denied)`. | **Passive omission vs. active kernel denial**. |
| **Filesystem Permission Context** | Ignored / uninspected (assumed standard writable root). | Measured `/` mode `0555 root:root` (`dr-xr-xr-x`, no owner write bit). | **Crucial blind spot**: Issue #6629 never inspects DAC permissions on `/`. |
| **Security / Confinement Context** | Unconfined execution assumed (assumes `sudo snapper create-config /` solves it). | Sandboxed systemd service: `User=root`, `CapabilityBoundingSet=CAP_SYS_ADMIN` (no `CAP_DAC_OVERRIDE`). | **Privilege nuance**: UID 0 without `CAP_DAC_OVERRIDE` is subject to DAC checks per `capabilities(7)` S027 & `access(2)` S034. |
| **Role of Missing `inotify-tools`** | Identified as the root cause of service inactivity (`limine-snapper-watcher fails with inotifywait is not installed`). | A secondary masking condition: triggered only after `create-config` fails, causing silent 0 exit instead of crash. | **Root cause vs. exit-code masking**. |
| **Omarchy 4.x Fix Efficacy** | Adding `install/config/snapper.sh` and `inotify-tools` to base packages. | If `/` is `0555`, any sandboxed runtime invocation still fails with `EACCES`; if `inotifywait` were present, it would fail on absent `/.snapshots`. | **Superficial workaround**: Fails to address the underlying permission constraint if `/` remains `0555`. |

### Rejection of Equivalence ("Same Symptom ≠ Same Cause")

We explicitly **reject** the equivalence of Omarchy Issue #6629 with the host's root-cause failure:
1. **The Diagnostic Fallacy:** Both environments exhibit `snapper list-configs` empty and `limine-snapper-sync.service` exiting 0 with `inotifywait is not installed`. However, treating #6629 as the diagnosis for this host is an error of symptom conflation.
2. **Hidden Precedent:** In #6629, the service is assumed to fail purely because `inotifywait` is missing. On this host, journal records prove that `limine-snapper-sync` *already attempted* automatic self-provisioning before checking for `inotifywait`, and was rebuffed by the kernel with `errno:13 (Permission denied)`.
3. **Interactive Illusion:** Running the manual workaround from #6629 (`sudo snapper -c root create-config /`) in an interactive administrative terminal succeeds only because interactive root possesses full capability sets (including `CAP_DAC_OVERRIDE`), bypassing DAC `0555`. This creates the false impression that "the installer simply forgot the config," while concealing the fact that confined system services running with `CapabilityBoundingSet=CAP_SYS_ADMIN` are strictly blocked from writing to `0555` roots.
4. **Secondary Masking:** If `inotify-tools` were installed on this host without resolving the `EACCES` or creating `/.snapshots`, `limine-snapper-watcher` would proceed to line 117 (`inotifywait ... /.snapshots`), which would instantly fail (`Couldn't watch /.snapshots: No such file or directory`), causing an active restart loop under `Restart=on-failure`. The missing package actually masked the underlying subvolume creation failure.

---

## 4. Applicability to Tsukuroi Round 12 Claims

### Applicability to Claim C1 (Census Operability: Root Metadata Blind Spot)
- **High Applicability (Negative Control & Blind Spot Justification):**
  - Issue #6629 illustrates the real-world operational hazard of relying on package managers to verify root integrity.
  - Because `pacman -Qo /` returns `error: No package owns /` and the `filesystem` package mtree omits `/`, `pacman -Qkk` is completely blind to root directory mode changes (`0555` vs `0755`).
  - Community issues like #6629 treat configuration errors as package list or installer script bugs, entirely overlooking the filesystem root mode.
  - C1's addition of an explicit root metadata census arm (measuring mode, UID, GID, ACL) directly addresses this blind spot.

### Applicability to Claim C2 (Depth: Source-Backed Discriminating EACCES Decision Matrix)
- **Direct Discriminator Grounding:**
  - Issue #6629 represents **Branch 0 (Installer Omission / Missing Package)** in the broader EACCES / Snapper decision space.
  - However, for an observed `errno:13 (Permission denied)`, #6629 is **inapplicable as the causal mechanism**.
  - C2 requires a source-backed decision matrix with at least 4 grounded branches:
    1. **Branch A (DAC Permission Restriction):** Root `/` is mode `0555` and caller lacks `CAP_DAC_OVERRIDE` (active host mechanism).
    2. **Branch B (Filesystem / Mount Read-Only):** Btrfs filesystem or mount option is `ro` (`is_btrfs_ro`).
    3. **Branch C (Pre-existing Subvolume Layout Collision):** S023 collision where `@.snapshots` is pre-mounted, returning EEXIST/failure.
    4. **Branch D (Missing Tool / Script Omission — Issue #6629):** Missing `inotify-tools` causing premature watcher fallback or uninitialized `/etc/snapper/configs/root` without kernel EACCES.
  - Incorporating Issue #6629 into C2 provides the precise negative-control discriminator between *passive configuration omission* (no `errno:13`) and *active capability/DAC permission denial* (`errno:13` under `CAP_SYS_ADMIN`).

---

## 5. Risks and Quality Bar Compliance

- **QUALITY Bar Rule 1 & 2:** All claims are grounded in measured host commands (`stat`, `pacman`, `grep`, `journalctl`) or exact quotes from GitHub issue #6629.
- **QUALITY Bar Rule 3:** Clear separation maintained between:
  - `[obs]` (Observed facts: host mode 0555, `inotify-tools` absent, journal lines with `errno:13`, issue text).
  - `[inf]` (Inference: `inotify-tools` absence masks `errno:13`; interactive sudo masks DAC constraint via `CAP_DAC_OVERRIDE`).
  - `[unknown]` (Unknowns: exact reason why host root was provisioned as `0555`; whether installer or security profile set it).
- **QUALITY Bar Rule 5:** Rejection of equivalence is explicitly preserved and documented.
- **QUALITY Bar Rule 13:** EACCES triage records target mode/owner/ACL (`0555 root:root`, no ACL mask) and unit's `CapabilityBoundingSet=CAP_SYS_ADMIN`.
- **Operator Risks:**
  - Applying #6629's workaround (`sudo snapper create-config /`) interactively resolves the immediate missing config but masks the underlying defect: services with `CapabilityBoundingSet=CAP_SYS_ADMIN` cannot manage subvolumes in `0555` root directories.
  - Installing `inotify-tools` without fixing `/` permissions or creating `/.snapshots` converts a silent 0/SUCCESS deactivation into a service restart failure loop.

---

## 6. Summary Outcome

- **Status:** PASS (Strictly read-only evidence; no host mutation; no speculative equivalence).
- **Finding:** Omarchy Issue #6629 shares the surface symptom (empty Snapper configs and inactive `limine-snapper-sync`) but exhibits a fundamentally divergent etiology. Issue #6629 represents packaging omission (`inotify-tools`) and installer sequencing; the host failure is an active kernel `EACCES` (`errno:13`) caused by `/` mode `0555` intersecting with systemd's `CapabilityBoundingSet=CAP_SYS_ADMIN` (dropping `CAP_DAC_OVERRIDE`). Equivalence is rejected.
- **Hand-off:** Evidence persisted to `.ufo/waves/round-12/Issue6629.md` for consumption by `Sources`, `Matrix`, `C2Review`, and `Main`.

---

## 7. Erratum & Epistemic Boundaries (2026-10-19)

Per review and quality audit, the following boundaries and retractions are formally appended:

1. **Mechanism Remains Source-Grounded Inference Only (`[inf]`):**
   - Any prior reference to the DAC/capability explanation as a proven "Root Cause" or "active kernel denial proven" is retracted.
   - The relationship between `/` mode `0555` and `CapabilityBoundingSet=CAP_SYS_ADMIN` dropping `CAP_DAC_OVERRIDE` is a source-grounded *candidate explanation* (`[inf]`) based on man-pages (`capabilities(7)` S027, `systemd.exec(5)` S028, `access(2)` S034) and unit text.
   - Neither the non-mutating capability falsifier (`sudo systemd-run ... test -w /`) nor an active syscall tracer (`strace`/`perf`) was run during this round.
2. **Unprobed Confinement & Runtime State (`[unknown]`):**
   - Other kernel confinement mechanisms (such as LSMs, AppArmor, Landlock, namespace isolation, or custom seccomp filters) and the process's live effective/permitted capability sets at the exact instant of `btrfs_util_create_subvolume_fd()` remain unprobed (`[unknown]`).
   - Prior notes (`corpus/knowledge/snapper-eacces-mechanism.md`) and past journal entries are historical records, not live execution proofs of current runtime state.
3. **Unmeasured Predictions Retracted (`unrun = unrun`):**
   - **Manual remediation:** The statement that running `sudo snapper -c root create-config /` "succeeds interactively" was not executed or measured this round. It remains a theoretical deduction based on unconfined root privileges, not a verified host fact.
   - **Service restart loop:** The claim that installing `inotify-tools` without creating `/.snapshots` would cause a continuous service restart loop was an unverified scenario projection, not an empirical observation.
4. **Issue #6629 Treatment (Negative Control, Not Proven Upstream Etiology):**
   - Issue #6629 is an external community issue report. A reported symptom does not prove its underlying cause even in the reporter's environment.
   - "Installer omission" must not be admitted as a proven historical fact on the host absent direct local installer log evidence. Issue #6629 is retained strictly as a *documented competing symptom hypothesis / negative control*, demonstrating that empty Snapper configurations can arise in contexts lacking observed kernel `errno:13` errors.
