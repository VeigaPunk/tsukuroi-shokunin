# PriorDebt — Round-12 Resumed UFO-FSD Connector Evidence

**Seat:** PriorDebtR (connector, resumed wave, round-12)  
**Role:** UFO-FSD connector  
**Target:** Connect prior lessons D3/MC3, D6, and QUALITY #13 with current round-12 Claims C1/C2 and the outside round-1 spotcheck disagreement (missing `## QUALITY check`). Specify exact regressions these should catch (not more index rows). Read-only evidence.  
**Judged axes:** Operability, Depth  
**Status:** Read-only analysis complete; no host mutations, no git commits, no test/build executions mid-flight.  
**Baseline Commit:** `b76b5c377eaee3e3d8d47fdddde977828d05dbd5`

---

## 1. Re-check of Inherited Wave-1 Evidence (`PriorDebt.md`)

In accordance with resumed round requirements, the inherited artifact `.ufo/waves/round-12/PriorDebt.md` was re-checked against current repository source state and sibling critic/review findings.

### 1.1 What is Reused
- **D3/MC3 & D6 Causal Core:** The core connection between D3/MC3 (triage assuming root execution bypasses DAC without checking target DAC bits or `CapabilityBoundingSet` dropping `CAP_DAC_OVERRIDE`) and D6 (`pacman -Qkk` blind spot because `/` is unowned by any package) remains fully valid and grounded.
- **Seam Regressions R1–R4:** The failure modes identifying early-return masking in `tools/tsukuroi-census.sh:probe_packages()` (R1), fail-open downgrade of unreadable root to DEGRADED/HEALTHY (R2), conflation of inode mode `0555` with `EROFS` (R3), and the process-blind capability assumption (R4) are confirmed by code inspection.

### 1.2 What is Corrected and Sharpened
- **Critical Discovery in C2 Knowledge Draft (`root-dac-decision-r12.md`):**
  Inherited `PriorDebt.md` anticipated that C2 must include a `## QUALITY check` evaluating Criterion 13.
  **Inspection of present source state reveals an immediate regression in the uncommitted artifact:**
  In `corpus/knowledge/root-dac-decision-r12.md:72-83`, section `## 7. QUALITY check` evaluates criteria **1 through 9 only**.
  It **completely omits evaluating Criterion 13** (mandatory pairing of DAC mode/owner/ACL with unit capabilities and noting `-Qkk` `/` blind spot), **Criterion 14** (requiring explicit evaluation of applicable numbered criteria), and **Criterion 15** (distinguishing DAC from mount state and barring extrapolation of mkdir to Btrfs ioctl).
  This is the exact failure pattern of the outside round-1 spotcheck disagreement (`round-1-verifier-spotcheck.md:12-13`), reproduced inside the round-12 C2 deliverable before landing.
- **Sharpening of 0555 Census Discrimination (R6 vs QUALITY #15):**
  Inherited analysis warned against naive `0755` checks. Cross-checking with `ClaimCritic.md:38-42`, `C1Review.md:29-36`, and `corpus/QUALITY.md:20` (Criterion 15) proves that mode `0555 root:root` is a legitimate, hardened distribution default (e.g. Fedora `filesystem.spec` line 409). The census runs as uid 1000 (non-owner). The census must evaluate owner-write absence relative to the caller or report raw bits without falsely emitting a `DEGRADED` verdict on healthy hosts.
- **VFS Error Ordering vs Btrfs Ioctl Extrapolation (New Regression R7):**
  Parent isolated fixtures (`error-order-smoke.json`) and kernel VFS inspection (`may_create_dentry` in `fs/namei.c`) confirmed that ordinary `mkdir` returns `EEXIST` before `EACCES` when the target exists. Furthermore, `limine-snapper-sync` invokes `btrfs_util_create_subvolume_fd` (`BTRFS_IOC_SUBVOL_CREATE_V2` ioctl), not `mkdir(2)`. The C2 matrix must catch the regression of extrapolating ordinary `mkdir` behavior to historical Btrfs subvolume creation.

---

## 2. Grounded Evidence: The Prior Debt and Current Claims Nexus

### 2.1 The Prior Defect Mechanisms (D3/MC3 and D6)
- **Lesson D3/MC3 (`corpus/lessons/round-1.md:40`):**
  In `corpus/knowledge/degraded-triage-r4.md:315-325`, Snapper self-init failure with `errno:13 (Permission denied)` was analyzed. Triage observed `ro=false`, `ProtectSystem=no`, and `User=root` with `CapabilityBoundingSet=CAP_SYS_ADMIN`, and prematurely concluded: *"none of the obvious candidates explains errno 13"*.
  *Root Mechanism:* The triage failed to measure DAC permissions on `/` and assumed uid 0 execution inherently bypasses DAC. In reality, host `/` was mode `0555 root:root`, and `CapabilityBoundingSet=CAP_SYS_ADMIN` in `limine-snapper-sync.service` explicitly stripped `CAP_DAC_OVERRIDE` (`capabilities(7)` S027, `systemd.exec(5)` S028). Without `CAP_DAC_OVERRIDE`, root is subject to standard DAC checks (`access(2)` S034, `path_resolution(7)`), triggering `EACCES`.
- **Lesson D6 (`corpus/lessons/round-1.md:43`):**
  In `corpus/knowledge/package-state-plane.md:146-175`, `pacman -Qkk` verification was benchmarked across all 1188 packages. However, `pacman -Qo /` returns `error: No package owns /` (exit 1), and Arch's `filesystem` package mtree contains 0 entries for `./` (`snapper-eacces-mechanism.md:13`).
  *Root Mechanism:* Package manager verification has an architectural blind spot for unowned filesystem paths, specifically `/`. The census (`tools/tsukuroi-census.sh:529-685`), which relied exclusively on `pacman -Qkk` and foreign package baselines, inherited this blind spot, emitting 0 root metadata findings.

### 2.2 The Admission Bar Rules: QUALITY #13, #14, and #15 (`corpus/QUALITY.md:17-20`)
- **QUALITY #13:** *"EACCES triage records target mode/owner/ACL and the unit's CapabilityBoundingSet/ProtectSystem; because -Qkk cannot see /, the census separately reports root-directory mode (lesson: corpus/lessons/round-1.md ## Mistakes D3/MC3, D6)."*
  Directly couples diagnostic triage (pairing inode DAC facts with unit capability sets) with census integrity (independent reporting of unowned `/`).
- **QUALITY #14:** *"Before recording an admit for a new knowledge entry, require its explicit `## QUALITY check` to evaluate the applicable numbered criteria and resolve its source/evidence pointers; a promised check is not a performed check (lesson: corpus/lessons/round-12.md ## Mistakes, outside round-1 omission)."*
  Arises directly from the outside round-1 spotcheck disagreement.
- **QUALITY #15:** *"Root metadata findings report owner-write/search bits, not universal mode policy or process writability. Permission-denial explanations distinguish inode DAC/ACL, mount namespace and runtime credentials; ordinary `mkdir` controls never certify a historical Btrfs ioctl cause (lesson: corpus/lessons/round-12.md ## Mistakes, ordering and permission-proxy errors)."*
  Bars conflating permission proxies with actual operations or extrapolating test fixtures to kernel ioctl state.

### 2.3 Outside Round-1 Spotcheck Disagreement (`corpus/lessons/round-1-verifier-spotcheck.md:12-13`)
- Outside verifier `W3ReviewTsukuroi` reviewed round-1 admissions and recorded an explicit disagreement: `adjacency-recheck-2026-10-19.md` was admitted *without* its required `## QUALITY check` section, despite lane self-attestation that criteria 1–13 were satisfied.
- Admission was salvaged only via post-review fix commit `459e3ce` (`round-1.md:141-147`, `LOG.md:415-420`).
- *Core Lesson:* Narrative self-attestation cannot substitute for structural, executable evaluation of applicable criteria.

### 2.4 Current Round-12 Claims (C1 and C2)
- **Claim C1 (Census Operability):** Close the unowned `/` metadata census blind spot in `tools/tsukuroi-census.sh`, moving root metadata findings from 0 to 1, discriminating `0755` (pass/healthy), `0555` (degraded/hardened), and unreadable/non-directory (blocked), while strictly preserving the 6-plane rollup contract.
- **Claim C2 (Matrix Depth):** Deliver `corpus/knowledge/root-dac-decision-r12.{md,json}` providing an independent, source-grounded, 4-branch EACCES decision matrix (DAC, Read-Only FS, Service Sandbox/Capabilities, Existing Target), grounded in primary sources (S027, S028, S034, S035), without conflating mode `0555` with `EROFS` or asserting root always bypasses DAC.

---

## 3. Exact Regressions These Must Catch (Not More Index Rows)

Connecting D3/MC3, D6, QUALITY 13–15, C1, C2, and the spotcheck disagreement defines seven exact, observable regressions across runtime, diagnostic, and gate surfaces:

### Regression R1: Early-Return Masking of Root Inode State (C1 Seam Regression)
- **Failure Mechanism:** In `tools/tsukuroi-census.sh:536-570`, `probe_packages()` issues early returns on package manager faults: `pacman` absent (536), `db.lck` present (541), `pacman -Qq` failure (549), empty db (556), and `pacman -Qkk` failure (570). Each reassigns `PKG_NOTE=` from scratch. If root probing is placed after these checks or writes into `PKG_NOTE` before them, any pacman error erases root metadata.
- **Exact Regression Caught:** A system experiencing a locked package database (`db.lck`) or missing pacman binary alongside a damaged `/` inode (e.g. unreadable or mode 0000) reporting only `pacman db.lck present` while completely suppressing the root failure, reviving the D6 blind spot under failure conditions.
- **Verification Anchor:** Hermetic fixture test where `db.lck` is present, asserting that `PLANE packages:` still contains `root_mode=` and root metadata findings.

### Regression R2: Fail-Open Downgrade on Inaccessible Root Substrate (C1 Contract Regression)
- **Failure Mechanism:** In `probe_packages()`, line 531 initializes `PKG_V=HEALTHY`, and lines 678, 681, 683 assign `PKG_V=DEGRADED` based on pacman drift. If root directory metadata cannot be read (e.g. `stat -L` fails or path is dangling/non-directory), the condition requires `PKG_V=BLOCKED` (exit 2). If root evaluation is folded inside `probe_packages()` prior to drift sweeps, lines 678–683 overwrite `BLOCKED` with `DEGRADED` or leave it `HEALTHY`.
- **Exact Regression Caught:** An inaccessible root filesystem (fatal substrate failure) being downgraded to `DEGRADED` or masked as `HEALTHY` because pacman reported 0 drifted files.
- **Verification Anchor:** Hermetic fixture with an unreadable or non-existent root path override, asserting script exit 2 and rollup `packages: BLOCKED`.

### Regression R3: Conflating Inode DAC Mode 0555 with Read-Only Mount State / EROFS (C2 vs S033 Regression)
- **Failure Mechanism:** Synthesized tier-C source S033 (rejected in round 1) claimed mode `0555` is a "read-only mount" and advised sudo overrides. In VFS mechanics, an inode with mode `0555` on a read-write mount (`findmnt -no OPTIONS /` → `rw`) returns `EACCES` (errno 13) via `mkdir(2)` / `path_resolution(7)`. A filesystem mounted read-only (`ro` / `MS_RDONLY`) returns `EROFS` (errno 30) regardless of mode bits or capabilities.
- **Exact Regression Caught:** Diagnostic tools or runbooks attributing an `EACCES` failure to mount options, or claiming that mode `0555` generates `EROFS`.
- **Verification Anchor:** C2 JSON matrix schema requiring strictly separate branches for DAC (`EACCES`, branch B1) and Read-Only Filesystem (`EROFS`, branch B2), grounded in `mkdir(2)` S035.

### Regression R4: Process-Blind DAC Assumption (C2 vs D3/MC3 Regression)
- **Failure Mechanism:** Historical triage in `degraded-triage-r4.md:315-325` observed `User=root` and `CapabilityBoundingSet=cap_sys_admin` and asserted that DAC could not explain `errno:13`, assuming root execution inherently bypasses DAC.
- **Exact Regression Caught:** Any diagnostic engine or triage document claiming uid 0 execution unconditionally bypasses filesystem DAC checks. Under Linux capabilities (`capabilities(7)` S027, `path_resolution(7)`), DAC write bypass is governed exclusively by `CAP_DAC_OVERRIDE`. When systemd's `CapabilityBoundingSet=` drops `CAP_DAC_OVERRIDE`, uid 0 is subject to standard DAC checks (`access(2)` S034) and is denied write access to `0555` directories.
- **Verification Anchor:** C2 decision matrix branch B3 asserting that root write access requires either owner-write permission (mode `0200`) or `CAP_DAC_OVERRIDE` in the effective capability set.

### Regression R5: Gate Admission Omission of QUALITY #13, #14, and #15 (Round-1 Spotcheck Regression)
- **Failure Mechanism:** In round 1, `adjacency-recheck-2026-10-19.md` was admitted without a `## QUALITY check` section. In round 12, the initial draft of `corpus/knowledge/root-dac-decision-r12.md:72-83` includes a `## QUALITY check`, but **only numbers items 1 through 9**, completely omitting evaluation of:
  - Criterion 13: Pairing target mode/owner/ACL with unit `CapabilityBoundingSet`/`ProtectSystem` and accounting for `-Qkk` unowned `/` blind spot.
  - Criterion 14: Executing and recording explicit evaluation of applicable criteria rather than promising checks.
  - Criterion 15: Reporting owner-write/search bits accurately without universal mode policy overclaim, and separating mkdir controls from historical Btrfs ioctl causes.
- **Exact Regression Caught:** A knowledge entry claiming to close EACCES triage debt being admitted without explicitly evaluating the criteria created specifically to govern EACCES triage and unowned root metadata.
- **Verification Anchor:** Gate verification asserting that `root-dac-decision-r12.md` contains explicit evaluations of criteria 13, 14, and 15 in its `## QUALITY check` section before parent landing.

### Regression R6: Non-Owner Host Overfitting & False Degradation on Mode 0555 (C1 Operability Regression)
- **Failure Mechanism:** Host `/` is `555 root:root`. The census runs as uid 1000. Distros such as Fedora package `/` as `0555` by policy (`filesystem.spec:409`). Arch's `filesystem` package specifies no baseline for `/`. A naive census rule declaring "missing owner-write (0200) → DEGRADED" evaluates owner bits against a non-owner process and falsely degrades standard hardened systems.
- **Exact Regression Caught:** False-positive `DEGRADED` rollup emitted on healthy hosts due to an unsupported requirement for mode `0755` or evaluating owner-write bits against non-owner probing processes.
- **Verification Anchor:** Census probe evaluating mode bits via octal masks, reporting `root_mode=%04o` in `PLANE packages:` note, and restricting `DEGRADED` verdicts to cases where caller ownership matches or where owner search is absent.

### Regression R7: Extrapolation of VFS mkdir Error Ordering to Historical Btrfs Subvolume Ioctls (C2 Epistemic Regression)
- **Failure Mechanism:** Assuming that ordinary `mkdir(2)` ordering (e.g. checking parent write permission before target existence) dictates the internal error precedence of `BTRFS_IOC_SUBVOL_CREATE_V2` ioctl (`fs/btrfs/ioctl.c`), or asserting that parent smoke fixtures prove the historical host failure cause.
- **Exact Regression Caught:** Conflating an isolated userspace control (`mkdir(2)`) with a kernel ioctl implementation, presenting an inferred explanation as an established historical fact.
- **Verification Anchor:** C2 matrix section 5 asserting that historical host attribution is unproven (`[inf]`) and maintaining clear separation between factual re-runnable branch discriminators and the unknown historical syscall sequence.

---

## 4. Affected Axes

### Operability (Current Baseline Score: 9)
- **Positive Effect:** C1 eliminates the unowned root directory census blind spot (moving root metadata findings from 0 to 1) without perturbing the six-plane contract.
- **Guard Against Harm:** Resolving Regression R1 ensures root metadata remains visible even when pacman is locked (`db.lck`). Resolving R2 ensures fatal root substrate failures are never masked as healthy. Resolving R6 guarantees that valid, hardened `0555` host configurations do not trigger spurious `DEGRADED` verdicts.

### Depth (Current Baseline Score: 8, tied lowest with Adjacency)
- **Positive Effect:** C2 replaces informal narrative triage with a formal, source-backed 4-branch decision matrix in `root-dac-decision-r12.{json,md}` grounded in primary Linux specifications (S027, S028, S034, S035).
- **Guard Against Harm:** Resolving Regressions R3, R4, and R7 guarantees that the matrix rigorously separates DAC from VFS mount flags (`EACCES` vs `EROFS`), grounds the capability-bounding mechanism, and explicitly avoids overclaiming historical Btrfs ioctl causes.

### Neutral Axes Guard (Freshness 9, Adjacency 8, Calibration 9)
- Maintained strictly neutral. C1 and C2 remain causally decoupled: C2 consumes no census script or output, and C1 evaluates no EACCES diagnostic text.

---

## 5. Proposed Move: The Tripartite QUALITY 13–15 Structural Contract

To synthesize across proposals without coupling runtime code, the recommended move is to **bind C1 and C2 through an explicit structural admission contract governed by QUALITY #13, #14, and #15:**

1. **In C1 (`tools/tsukuroi-census.sh`):**
   - Isolate root directory metadata collection from `probe_packages()` into independent variables (`ROOT_V`, `ROOT_NOTE`).
   - Compose the root finding into `PLANE packages:` note in `main()`, preserving the six-plane rollup.
   - Fold `ROOT_V` into `PKG_V` using the existing helper `PKG_V=$(worse "$PKG_V" "$ROOT_V")` in `main()` (mirroring the memory arm fold `DRV_V=$(worse "$DRV_V" "$MEM_V")` at line 2372).
   - In `run_selftest()`, include a fixture asserting that when `pacman db.lck` is present, `PLANE packages:` still reports `root_mode=`. This permanently blocks Regression R1.
2. **In C2 (`corpus/knowledge/root-dac-decision-r12.md`):**
   - **Remediate the Omitted QUALITY Criteria (Regression R5):** Expand section `## 7. QUALITY check` to explicitly evaluate Criteria 13, 14, and 15:
     - *Criterion 13:* Formally pairs target DAC attributes (mode `0555`, owner `root`, base POSIX ACL) with unit properties (`CapabilityBoundingSet=cap_sys_admin`, `ProtectSystem=no`), citing S027, S028, S034; explicitly documents that direct filesystem inspection is necessary because `pacman -Qkk` cannot verify unowned `/` (D6).
     - *Criterion 14:* Demonstrates that all applicable criteria (1–9, 13–15) have been evaluated with explicit evidence rather than promised.
     - *Criterion 15:* Validates that mode `0555` is documented as a DAC bit pattern, not a universal policy violation or mount property; explicitly records that parent `mkdir` controls do not certify historical Btrfs ioctl ordering.
3. **In the Gate Admission Checklist (`GateScribe` / Parent Landing):**
   - Enforce an automated check verifying that `root-dac-decision-r12.md` contains explicit evaluations of Criteria 13, 14, and 15 in its `## QUALITY check` before recording round closure, permanently preventing recurrence of the outside spotcheck disagreement.

---

## 6. Risks and Failure Modes

1. **Rollup Key Mutation Risk:** Downstream parsers and selftests rely on exact regex matching of `^PLANE packages: (HEALTHY|DEGRADED|BLOCKED) (.*)$`. Emitting root metadata as an independent plane or modifying the rollup string would break the six-plane contract. Root metadata must be contained strictly within the packages note.
2. **Fixture Umask Leak:** In `run_selftest()`, `umask 077` at line 321 causes `mkdir` in temp fixtures to create directories with mode `0700`. Hermetic test fixtures expecting `0755` must execute an explicit `chmod 755 "$FX/root"` on the fixture path only.
3. **Non-Author Verification Gap:** As established in `round-1-verifier-spotcheck.md`, author-side seat execution is not independent verification. The parent integrator and subsequent outside reviewers must execute independent replay before claiming score advancement.

---

## 7. Verification Method (Parent Post-Integration Checks)

Parent agent should execute the following read-only checks once integration lands:

```sh
# 1. Verify C1 root metadata probe survives db.lck (Regression R1 check)
bash tools/tsukuroi-census.sh --selftest

# 2. Verify C2 decision matrix JSON schema and branch count (>=4 branches)
jq '[.branches[] | select((.id|length)>0 and (.evidence|length)>0 and (.interpretation|length)>0 and (.discriminator|length)>0 and (.limit|length)>0 and (.source_ids|length)>0)] | length' corpus/knowledge/root-dac-decision-r12.json

# 3. Verify C2 carries ## QUALITY check explicitly evaluating Criteria 13, 14, and 15 (Regression R5 check)
grep -n -A 25 '^## 7. QUALITY check' corpus/knowledge/root-dac-decision-r12.md | grep -E '13\.|14\.|15\.'

# 4. Verify negative guards in C2 (no assertion that mode 0555 is a read-only mount, Regression R3 check)
grep -n -i 'read-only mount' corpus/knowledge/root-dac-decision-r12.md || true

# 5. Verify SOURCES registry validity
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
```

---

## 8. Tool Record
- **Installs/upgrades:** None. Used existing host utilities (`stat`, `findmnt`, `pacman`, `systemctl`, `getfacl`, `bash`, `python3`).
- **Probes executed:** Targeted, read-only file inspections and AST/schema validations.
- **Independence:** Author-side seat evidence only; not independent non-author verification.
