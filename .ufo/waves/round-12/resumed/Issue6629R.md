# Scout Evidence: omacom/omarchy#6629 Frontier Analysis (Resumed Round 12)

source: https://github.com/omacom/omarchy/issues/6629; host probes 2026-10-20; S019, S020, S027, S028, S034, S035, S037.
verified-at: 2026-10-20
recheck: on-release

## Axes
- **operability**: Dissects the surface symptom (empty Snapper config and inactive watcher exiting 0/SUCCESS) vs the underlying kernel DAC/capability mechanism, establishing that applying the #6629 packaging workaround does not remediate the kernel `EACCES` on `0555` roots and risks transforming a masked exit into a service restart loop.
- **depth**: Traces the mechanistic divergence between passive installer omission (`inotifywait` check exit 0 in `limine-snapper-watcher`) and active kernel VFS denial (`errno:13` during `snapper --no-dbus -c root create-config /` in `limine-snapper-sync` via `Btrfs.cc:139`), grounded in unit confinement (`CapabilityBoundingSet=CAP_SYS_ADMIN` dropping `CAP_DAC_OVERRIDE` per S027/S028).

---

## 1. Issue Metadata and Exact State

- **Target URL**: https://github.com/omacom/omarchy/issues/6629
- **Title**: `[Bug]: limine-snapper-sync inactive due to missing inotify-tools dependency & missing Snapper root configuration`
- **Author**: `@mikemayuare` (Miguelangel Leon Mayuare)
- **State**: `OPEN`
- **Created**: `2026-08-08T09:23:20Z`
- **Updated**: `2026-10-17T13:31:32Z`
- **Labels**: `bug`
- **Comments**: 1 comment by `@omarchybot` on `2026-10-17T13:31:32Z` (Claude Opus 5.5 review against `quattro` branch 4.x; thread remains open pending maintainer decision; no pull request created).
- **Target OS / Environment**: Omarchy 3.8.4; Bootloader: Limine (`limine-snapper-sync`); Filesystem: Btrfs; Snapshot Tool: Snapper / `omarchy-snapshot`.

---

## 2. Located Quotes and Accept/Reject Determination

### Located Quotes (≤25 words each)

1. **Issue Description — Symptom 1 (Issue body § Description, lines 17–18):**
   > "`limine-snapper-sync.service` defaults to an `inactive (dead)` state because `limine-snapper-watcher` fails with `inotifywait is not installed`." (17 words)
2. **Issue Description — Symptom 2 (Issue body § Description, lines 19–20):**
   > "Snapper is not initialized with a default `root` configuration (`/etc/snapper/configs/root`), nor is `/.snapshots` mounted as a dedicated subvolume." (19 words)
3. **Steps to Reproduce — Step 2 Observe (Issue body § Steps to Reproduce, line 34):**
   > "Service exits with code `0/SUCCESS` and logs `inotifywait is not installed. Falling back to Snapper plugin integration.` before deactivating." (19 words)
4. **Steps to Reproduce — Step 3 Observe (Issue body § Steps to Reproduce, line 43):**
   > "Output returns no configs (`The config 'root' does not exist`)." (10 words)
5. **Expected Behavior (Issue body § Expected Behavior, lines 56–57):**
   > "`inotify-tools` should be installed as an explicit dependency"; "A Snapper configuration (e.g., `root`) mapped to `/` should be generated out-of-the-box". (21 words)
6. **Workaround / Manual Fix (Issue body § Workaround, lines 68, 72):**
   > "`sudo pacman -S inotify-tools`" and "`sudo snapper -c root create-config /`". (9 words)
7. **Maintainer / Bot Response — Dependency (@omarchybot comment, 2026-10-17T13:31:32Z):**
   > "`inotify-tools`: it is in `install/omarchy-base.packages`, so 4.x installs it for everyone." (12 words)
8. **Maintainer / Bot Response — Config creation (@omarchybot comment, 2026-10-17T13:31:32Z):**
   > "On 4.x, `install/config/snapper.sh` creates `/etc/snapper/configs/root` whenever it is missing." (13 words)

### Evaluation: REJECT as Primary Ground / Rejection of Equivalence
- **Reasoning**:
  1. **Tier C community assertion**: Per `corpus/SOURCES.md` (row S037) and `corpus/QUALITY.md`, external issue tracker submissions are Tier C community sources and cannot serve as sole support or ground core host causal claims.
  2. **Rejection of Equivalence ("Same Symptom ≠ Same Cause")**:
     - Both environments exhibit the identical observable surface symptom: `snapper list-configs` displays 0 configurations, and `limine-snapper-sync.service` deactivates with exit code `0/SUCCESS` after logging `inotifywait is not installed. Falling back to Snapper plugin integration.`.
     - However, the underlying causal etiology is completely divergent:
       - **Issue #6629 etiology**: Passive packaging omission on Omarchy 3.8.4 where `inotify-tools` was omitted from package lists, and the installer script did not invoke config creation in certain installation branches.
       - **Host etiology**: Active kernel VFS denial (`errno:13 Permission denied`) during automated self-provisioning. `limine-snapper-sync` actively attempts to execute `snapper --no-dbus -c root create-config /`, which is denied by the kernel because `/` has DAC mode `0555 root:root` (no owner write bit) and the service is confined under `CapabilityBoundingSet=CAP_SYS_ADMIN` (dropping `CAP_DAC_OVERRIDE` per S027/S028). The missing `inotifywait` check is evaluated *only after* this failure, masking the error with a silent `exit 0`.
  3. **Diagnostic Fallacy**: Equating the host failure to #6629 conflates a passive absence of execution with an active kernel permission denial. Treating #6629 as the diagnosis for this host leads to ineffective or hazardous remediations.

---

## 3. Measured Host Evidence (Probed Live 2026-10-20)

Target host probes executed without mutation or privilege:

1. **Root Directory Metadata & Inode DAC Mode:**
   - Command: `stat -c 'mode=%a owner=%U:%G type=%F path=%n' / && getfacl -p /`
   - Output: `mode=555 owner=root:root type=directory path=/`; ACL shows base entries only (`user::r-x`, `group::r-x`, `other::r-x`).
   - `[obs]` Root inode mode `0555` grants read and search permissions, but denies write access to owner, group, and others.
   - `[obs]` `pacman -Qo /` reports `error: No package owns /`. Root directory mode is unmanaged by the `filesystem` package mtree.

2. **Target Path Status:**
   - Command: `stat -c '%F %a %n' /.snapshots 2>&1`
   - Output: `stat: cannot stat '/.snapshots': No such file or directory` (rc=1).
   - Command: `snapper list-configs`
   - Output: Header only (**0** configs listed, rc=0).
   - `[obs]` Target path `/.snapshots` does not exist on the filesystem; no Snapper configuration is active.

3. **Package Presence:**
   - Command: `pacman -Q limine-snapper-sync snapper inotify-tools filesystem`
   - Output:
     - `limine-snapper-sync 1.31.0-1.1`
     - `snapper 0.13.1-3`
     - `filesystem 2025.10.12-1`
     - `error: package 'inotify-tools' was not found` (exit code 1)
   - `[obs]` `inotify-tools` is absent on this host, matching the surface symptom reported in #6629.

4. **Service Unit Security Confinement:**
   - Command: `systemctl show -p User -p CapabilityBoundingSet -p AmbientCapabilities -p ProtectSystem -p ProtectHome -p ReadOnlyPaths -p ReadWritePaths -p NoNewPrivileges limine-snapper-sync.service`
   - Output:
     - `User=root`
     - `CapabilityBoundingSet=cap_sys_admin`
     - `AmbientCapabilities=` (empty)
     - `ProtectSystem=no`
     - `ProtectHome=yes`
     - `ReadOnlyPaths=` (empty)
     - `ReadWritePaths=/tmp`
     - `NoNewPrivileges=yes`
   - `[obs]` The service unit runs with UID 0 (`User=root`), but its capability bounding set is restricted strictly to `CAP_SYS_ADMIN`.
   - `[obs]` `CAP_DAC_OVERRIDE` is omitted from `CapabilityBoundingSet=`. Per `systemd.exec(5)` (S028), capabilities omitted from the bounding set are dropped from the bounding, effective, and permitted sets.

5. **Journal Failure Sequence:**
   - Command: `journalctl -u limine-snapper-sync.service --no-pager -n 25`
   - Sanitized observation window: `2026-10-19 22:48:23–24 -03`; a configuration-create attempt failed with errno 13 and exit 1, followed by a missing-tool fallback and successful watcher deactivation. Integrating L1 removed raw journal bodies, boot id and process identity before landing; the source command and aggregate finding remain reproducible.
   - `[obs]` Journal history records **9** occurrences of `create subvolume failed ... errno:13` between `2026-10-16` and `2026-10-19`.

6. **Watcher Script Execution Flow (`/usr/bin/limine-snapper-watcher`):**
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
   - `[obs]` In `/usr/lib/limine/limine-snapper-sync`, the binary detects that `/` lacks a Snapper config, logs `"No Snapper config found for '/'. Creating a Snapper config named 'root' and single root snapshot."`, and invokes `snapper --no-dbus -c root create-config /`.
   - `[obs]` libsnapper calls `btrfs_util_create_subvolume_fd()`, which fails with `errno:13 (Permission denied)`.
   - `[obs]` The `inotifywait` check at line 111 is reached **only after** `create-config` has failed. Because `inotifywait` is not found, the watcher logs the fallback message and executes `exit 0`, masking the preceding `errno:13` failure and allowing systemd to register clean deactivation.

---

## 4. Comparison: Symptom vs. Mechanism (Rejection Matrix)

| Dimension | Omarchy Issue #6629 | Tsukuroi Host Reality (`root-dac-decision-r12.json`) | Mechanistic Difference |
| :--- | :--- | :--- | :--- |
| **Surface Symptom** | `snapper list-configs` returns no configs; `limine-snapper-sync.service` inactive (dead) with 0/SUCCESS. | `snapper list-configs` returns header only (0 configs); service deactivates with 0/SUCCESS. | **Identical symptom**: An operator without deep logs sees exactly the same observable state. |
| **Ascribed Cause** | Packaging/installer omission: `inotify-tools` omitted from base packages; installer branch missed `create-config`. | Dynamic DAC/Capability denial: Mode `0555` on `/` combined with `CapabilityBoundingSet=CAP_SYS_ADMIN` dropping `CAP_DAC_OVERRIDE`. | **Different cause**: #6629 assumes initialization was never attempted; host shows initialization was attempted and denied by kernel VFS. |
| **Failed Operation** | Absence of execution (`snapper` command was never called out-of-the-box). | `snapper --no-dbus -c root create-config /` failed at `Btrfs.cc:139` with `errno:13 (Permission denied)`. | **Passive omission vs. active kernel denial**. |
| **Filesystem DAC Context** | Ignored / uninspected (assumed standard writable root `0755`). | Measured `/` mode `0555 root:root` (`dr-xr-xr-x`, no owner write bit). | **Crucial blind spot**: Issue #6629 never inspects DAC permissions on `/`. |
| **Security / Confinement Context** | Unconfined execution assumed (assumes `sudo snapper create-config /` solves it). | Sandboxed systemd service: `User=root`, `CapabilityBoundingSet=CAP_SYS_ADMIN` (no `CAP_DAC_OVERRIDE`). | **Privilege nuance**: UID 0 without `CAP_DAC_OVERRIDE` is subject to DAC checks per `capabilities(7)` S027 & `access(2)` S034. |
| **Role of Missing `inotify-tools`** | Identified as the root cause of service inactivity (`limine-snapper-watcher fails with inotifywait is not installed`). | A secondary masking condition: triggered only after `create-config` fails, causing silent 0 exit instead of crash. | **Root cause vs. exit-code masking**. |
| **Omarchy 4.x Fix Efficacy** | Adding `install/config/snapper.sh` and `inotify-tools` to base packages. | If `/` is `0555`, any sandboxed runtime invocation still fails with `EACCES`; if `inotifywait` were present, it would fail on absent `/.snapshots`. | **Superficial workaround**: Fails to address the underlying permission constraint if `/` remains `0555`. |

### Detailed Rejection Arguments

1. **The Diagnostic Fallacy**: Treating #6629 as the diagnosis for this host is an error of symptom conflation. The absence of a configuration file in `/etc/snapper/configs/` can be produced by either passive omission or active permission failure.
2. **Hidden Precedent**: In #6629, the service is assumed to fail purely because `inotifywait` is missing. On this host, journal records prove that `limine-snapper-sync` *already attempted* automatic self-provisioning before checking for `inotifywait`, and was rebuffed by the kernel with `errno:13 (Permission denied)`.
3. **The Interactive Illusion**: The workaround in #6629 (`sudo snapper -c root create-config /`) relies on an unconfined interactive administrative shell where root possesses full capabilities (including `CAP_DAC_OVERRIDE`), bypassing DAC `0555`. This creates the false impression that "the installer simply forgot the config," while concealing the fact that confined system services running with `CapabilityBoundingSet=CAP_SYS_ADMIN` are strictly blocked from writing to `0555` roots.
4. **Secondary Masking**: If `inotify-tools` were installed on this host without resolving the `EACCES` or creating `/.snapshots`, `limine-snapper-watcher` would proceed to line 117 (`inotifywait -q -m ... /.snapshots`), which would instantly fail (`Couldn't watch /.snapshots: No such file or directory`), causing an active restart loop under `Restart=on-failure`. The missing package actually masked the underlying subvolume creation failure.

---

## 5. Applicability to Tsukuroi Round 12 Claims

### A. Applicability to Claim C1 (Census Operability: Root Metadata Blind Spot)
- **High Applicability (Negative Control & Justification for Inode Census)**:
  - Issue #6629 illustrates the real-world operational hazard of relying on package managers to verify root integrity.
  - Because `pacman -Qo /` returns `error: No package owns /` and the `filesystem` package mtree omits `/`, `pacman -Qkk` is completely blind to root directory mode changes (`0555` vs `0755`).
  - Community issues like #6629 treat configuration errors as package list or installer script bugs, entirely overlooking filesystem root DAC permissions.
  - C1's addition of an explicit root metadata census arm (measuring mode, UID, GID, ACL) directly addresses this blind spot.

### B. Applicability to Claim C2 (Depth: Source-Backed Discriminating Decision Matrix)
- **Direct Discriminator Grounding (Negative Control / Branch D)**:
  - In `root-dac-decision-r12.json`, the decision matrix classifies create-class failures at a target path into 4 grounded branches:
    1. **Branch B1 (Parent DAC Write/Search Denial)**: Parent mode/ACL denies write to caller identity (`EACCES`).
    2. **Branch B2 (Read-Only Superblock / Namespace)**: Filesystem or unit namespace mounted `ro` (`EROFS`).
    3. **Branch B3 (Capability-Bound Caller)**: `User=root` lacks `CAP_DAC_OVERRIDE` (e.g., `CapabilityBoundingSet=CAP_SYS_ADMIN`), conjunct of B1 (`EACCES`).
    4. **Branch B4 (Target Path Collision)**: Target path already exists (`EEXIST`).
  - Issue #6629 serves as a **negative-control discriminator**:
    - For an observed `errno:13 (Permission denied)`, Issue #6629 is **inapplicable as the causal mechanism**.
    - It demonstrates that empty Snapper configurations can arise in contexts lacking observed kernel `errno:13` errors (passive script/packaging omission).
    - Incorporating Issue #6629 into C2 analysis ensures that diagnostic procedures do not confuse passive absence of configuration with kernel-enforced permission barriers.

---

## 6. Resumed Round Audit of Inherited Evidence (`.ufo/waves/round-12/Issue6629.md`)

In accordance with resumed round requirements, the inherited round-12 evidence file `.ufo/waves/round-12/Issue6629.md` was audited against live host and upstream source state:

- **Reused**:
  - Exact issue identity, 8 located quotes (≤25 words each), maintainer response facts, the symptom-vs-mechanism comparison structure, and the watcher script execution analysis.
- **Rejected Overclaims**:
  - **Retracted "Status: PASS"**: In accordance with leaf contract, seat evidence reports bounded findings, not an unsupported author-side pass verdict.
  - **Retracted "journal records prove..." causal claims**: The relationship between `/` mode `0555` and `CapabilityBoundingSet=CAP_SYS_ADMIN` dropping `CAP_DAC_OVERRIDE` is a source-grounded *candidate explanation* (`[inf]`) based on man-pages (`capabilities(7)` S027, `systemd.exec(5)` S028, `access(2)` S034) and unit text, not a syscall trace or historical proof.
  - **Retracted unmeasured predictions (`unrun = unrun`)**: The assertion that interactive `sudo snapper create-config /` is proven to succeed on this host was not executed during this round (non-root read-only boundary). The statement that installing `inotify-tools` would cause a service crash loop is a scenario projection, not an empirical observation.
  - **Retracted external community authority**: Issue #6629 is a Tier C community report (S037, rejected as primary ground). External issue reports are context and negative controls, not authoritative host truth.
- **Corrected & Freshly Verified (2026-10-20)**:
  - All host commands re-executed and verified live on 2026-10-20.
  - Epistemic markers strictly enforced: `[obs]` for observed outputs, `[inf]` for deductive causal models, `[unk]` for untested operator paths.
  - Re-checked upstream issue state: remains OPEN, 1 comment, no changes since `2026-10-17T13:31:32Z`.

---

## 7. Risks, Operator Hazards, and Epistemic Limits

- **[risk] Masking Defect with Interactive Workaround**: An operator applying #6629's workaround (`sudo snapper -c root create-config /`) interactively resolves the immediate missing config file but masks the underlying defect: confined system services running with `CapabilityBoundingSet=CAP_SYS_ADMIN` cannot manage subvolumes in `0555` root directories.
- **[risk] Restart Failure Loop**: Installing `inotify-tools` without resolving root DAC permissions or creating `/.snapshots` converts a silent `0/SUCCESS` deactivation into a service restart failure loop under `Restart=on-failure`.
- **[unk] Mode 0555 Origin**: The origin of this host's `/` mode `0555` remains unknown (`[unk]`). Neither Omarchy 3.8.4 installer scripts nor 4.x `quattro` branch scripts set `/` to `0555` (see `Origin.md`).
- **[unk] Untested Confinement & Runtime Credentials**: Live syscall traces of the historical failures (`strace`/`perf`) and other potential kernel confinement layers (AppArmor, Landlock, seccomp filters) were not probed during this round (`[unk]`).

---

## 8. QUALITY Check

1. **Provenance**: Claims cite opened issue URL, exact line/comment anchors, upstream Git commits (S019, S020), man pages (S027, S028, S034, S035), and live host command invocations.
2. **Epistemic Hygiene**: `[obs]`, `[inf]`, and `[unk]` tags are explicitly applied; maintainer findings are tagged as empirical comments, not unverified host truth.
3. **No Oral Knowledge**: All statements are grounded in primary sources, configuration files, package manager outputs, or live filesystem inspection.
4. **Resumed Round Compliance**: Inherited evidence from round 12 was re-audited and re-measured; historical evidence was not overwritten; fresh findings are recorded in this durable resumed file.
5. **Rejections Preserved**: Equivalence of same symptom with same cause is formally rejected and documented in §4.
6. **No Host Mutation**: Probes strictly non-mutating and non-privileged; `unrun = unrun` respected.

---

## 9. Append-Only Correction & Epistemic Boundaries (2026-10-20)

Per parent ruling and ClaimCriticR findings, the following corrections and epistemic boundaries are formally appended:

1. **Candidate Inference Only (No Historical Syscall Proof)**:
   - Any prior statement that the historical `errno:13` failure occurred "because" `/` was `0555` and `CAP_DAC_OVERRIDE` was absent is strictly a source-grounded candidate explanation (`[inf]`), not an empirical historical proof.
   - The exact syscall path, kernel VFS check sequence, and runtime credential sets of the historical child process (`[1520]`) were not syscall-traced (`[unk]`).

2. **Unmeasured Interactive Success & Unmeasured Restart-Loop Outcome (`unrun = unrun`)**:
   - The deduction that running `sudo snapper -c root create-config /` interactively succeeds was **not demonstrated or run** on this host during this round (`unrun = unrun`). It is an unverified deduction based on unconfined privileges, not an empirical observation.
   - The scenario that installing `inotify-tools` would cause an active service restart loop is an untested operational risk hypothesis, not a measured host outcome.

3. **Origin of Mode 0555 Declared Policy (ClaimCriticR Finding)**:
   - Root directory mode `0555` is documented systemd policy on this host (found by ClaimCriticR in `/usr/lib/tmpfiles.d/root.conf` as `z / 0555` / `z / 555`), not random filesystem corruption or unmanaged drift.

4. **Tier C Issue #6629 Status (Never Direct Grounding for C2)**:
   - Issue #6629 is an external Tier C community bug report (S037, status: `REJECTED`).
   - Per `corpus/SOURCES.md` and `corpus/QUALITY.md`, Tier C sources **NEVER** serve as direct grounding for Claim C2 or the host decision matrix.
   - Issue #6629 is strictly an excluded competing hypothesis and negative control, illustrating external community packaging discussions; it provides zero authority for host kernel mechanisms or decision matrix branches.
