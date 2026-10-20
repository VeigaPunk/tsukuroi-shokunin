# PriorDebt — Round-12 UFO-FSD Connector Evidence

**Seat:** PriorDebt (connector, round-12)  
**Role:** UFO-FSD connector  
**Target:** Connect prior lessons D3/MC3, D6, and QUALITY #13 with current round-12 Claims C1/C2 and the outside round-1 spotcheck disagreement (missing `## QUALITY check`). Specify exact regressions these should catch (not more index rows). Read-only evidence.  
**Judged axes:** Operability, Depth  
**Status:** Read-only analysis complete; no host mutations, no git commits, no tests run mid-flight.

---

## 1. Grounded Evidence: The Prior Debt and Current Claims Nexus

### 1.1 The Prior Defect Mechanisms (D3/MC3 and D6)
- **Lesson D3/MC3 (`corpus/lessons/round-1.md:40`):**
  - *Historical Defect:* In `corpus/knowledge/degraded-triage-r4.md:315-325`, Snapper's self-init failure with `errno:13 (Permission denied)` on `create subvolume .snapshots` was analyzed. The triage observed `ro=false`, `ProtectSystem=no`, and `User=root` with `CapabilityBoundingSet=CAP_SYS_ADMIN`, and erroneously concluded: *"none of the obvious candidates explains errno 13"*.
  - *Root Mechanism:* The triage failed to measure target DAC permissions on `/` and assumed root execution bypasses DAC. In reality, `/` mode was `0555 root:root` (no owner/group/other write bit), and `CapabilityBoundingSet=CAP_SYS_ADMIN` in `limine-snapper-sync.service` explicitly stripped `CAP_DAC_OVERRIDE` (`capabilities(7)` S027, `systemd.exec(5)` S028). Without `CAP_DAC_OVERRIDE`, root is subject to standard DAC checks (`access(2)` S034, `path_resolution(7)`), causing `EACCES`.
- **Lesson D6 (`corpus/lessons/round-1.md:43`):**
  - *Historical Defect:* In `corpus/knowledge/package-state-plane.md:146-175`, `pacman -Qkk` verification was benchmarked across all 1188 packages. However, `pacman -Qo /` returns `error: No package owns /` (exit 1), and Arch's `filesystem` package mtree contains 0 root-directory entries for `./` (`snapper-eacces-mechanism.md:13`).
  - *Root Mechanism:* Package manager verification has an inherent blind spot for unowned filesystem paths, specifically `/`. The census (`tools/tsukuroi-census.sh:529-685`), which relied purely on `pacman -Qkk` and foreign package baselines for the `packages` plane, inherited this exact blind spot, leaving `/` metadata unprobed (0 root metadata findings).

### 1.2 The Admission Bar Rule: QUALITY #13 (`corpus/QUALITY.md:17`)
- Text: *"13. EACCES triage records target mode/owner/ACL and the unit's CapabilityBoundingSet/ProtectSystem; because -Qkk cannot see /, the census separately reports root-directory mode (lesson: corpus/lessons/round-1.md ## Mistakes D3/MC3, D6)."*
- Codifies a dual-surface contract:
  1. *Triage Surface:* Mandatory pairing of target inode DAC facts (mode, owner, ACL) with unit sandboxing/capabilities (`CapabilityBoundingSet`, `ProtectSystem`).
  2. *Census Surface:* Mandatory independent reporting of root-directory mode by the census to bypass the `-Qkk` unowned blind spot.

### 1.3 Outside Round-1 Spotcheck Disagreement (`corpus/lessons/round-1-verifier-spotcheck.md:12-13`)
- *Finding:* Outside orchestrator verifier `W3ReviewTsukuroi` reviewed round-1 admissions and recorded a disagreement: `adjacency-recheck-2026-10-19.md` was admitted *without* its required `## QUALITY check` section, despite the lane's Gate claiming all entries satisfied criteria 1–13. Admission was only granted after emergency post-review fix commit `459e3ce` appended the missing check (`corpus/lessons/round-1.md:141-147`, `LOG.md:415-420`).
- *Root Cause:* Admission gates relied on passive narrative self-attestation rather than active, structural validation that every newly introduced knowledge entry carries an explicit `## QUALITY check` block evaluating applicable criteria.

### 1.4 Current Round-12 Claims (C1 and C2)
- **Claim C1 (Census Operability):** Close the unowned `/` metadata census blind spot in `tools/tsukuroi-census.sh`, moving root metadata findings from 0 to 1, discriminating `0755` (pass/healthy), `0555` (degraded), and unreadable/non-directory (blocked), while avoiding early-return traps.
- **Claim C2 (Matrix Depth):** Deliver `corpus/knowledge/root-dac-decision-r12.md` and `.json` containing an independent, source-grounded, 4-branch EACCES decision matrix (DAC, Read-Only FS, Service Sandbox/Capabilities, Snapshot Layout), grounded in primary sources (S027, S028, S034, `mkdir(2)`, `path_resolution(7)`), without conflating mode `0555` with an `EROFS` mount or asserting root always bypasses DAC.

---

## 2. Exact Regressions These Must Catch (Not More Index Rows)

Connecting D3/MC3, D6, QUALITY #13, C1, C2, and the spotcheck disagreement defines six exact, observable regressions across runtime, diagnostic, and admission surfaces:

### Regression R1: Early-Return Masking of Root Degradation (C1 Seam Regression)
- **Failure Mode:** In `tools/tsukuroi-census.sh:534-572`, `probe_packages()` issues early returns on package manager faults: `pacman` missing (line 536), `db.lck` present (line 541), `pacman -Qq` failure (line 549), empty db (line 556), and `pacman -Qkk` probe error (line 570). Each early return executes `return` after assigning a fresh `PKG_NOTE=`. If the C1 root metadata probe is placed after these checks, or if it writes to `PKG_NOTE` which is overwritten by them, any package manager failure completely erases the root metadata finding.
- **Exact Regression Caught:** A system suffering an aborted package transaction (`db.lck` present) AND an unreadable or degraded `/` directory (e.g. `0000` or `0555`) would report `pacman db.lck present` but silently drop root directory status, completely reviving the D6 blind spot under failure conditions.
- **Verification Anchor:** Hermetic fixture test where `db.lck` is present or `pacman` is missing, asserting that `PLANE packages` output still contains `root_mode=` and root metadata evidence.

### Regression R2: Fail-Open Verdict Downgrade on Inaccessible Root (C1 Contract Regression)
- **Failure Mode:** In `tools/tsukuroi-census.sh`, `probe_packages()` resets `PKG_V=HEALTHY` at line 531, and downstream drift checks assign `PKG_V=DEGRADED` (line 678). If root directory metadata cannot be read (e.g. `stat -L` fails or path is a non-directory), the root probe evaluates to `BLOCKED`. If root evaluation is done within `probe_packages()` before the pacman drift sweep, line 678 (`if [ "$drift" -gt 0 ]; then PKG_V=DEGRADED; fi`) or line 531 resets can overwrite `BLOCKED` with `DEGRADED` or `HEALTHY`.
- **Exact Regression Caught:** An inaccessible root filesystem (a fatal substrate condition requiring exit 2 / `BLOCKED`) being downgraded to `DEGRADED` or masked as `HEALTHY` because the pacman package sample was clean (drift=0).
- **Verification Anchor:** Hermetic fixture test with an inaccessible/dangling-symlink root override, asserting `PKG_V=BLOCKED` and script exit code 2.

### Regression R3: Conflating Inode DAC Mode 0555 with Read-Only Mount State / EROFS (C2 vs S033 Regression)
- **Failure Mode:** Tier-C synthesized source S033 (`corpus/SOURCES.md:39,54`, rejected in round 1) erroneously claimed mode `0555` is a "read-only mount" and recommended `sudo` overrides. In VFS mechanics (`MountErrors.md:76-85`), an inode with mode `0555` on a read-write mount (`findmnt -no OPTIONS /` -> `rw`) returns `EACCES` (errno 13) via `mkdir(2)` / `path_resolution(7)` when a process lacking `CAP_DAC_OVERRIDE` attempts directory creation. Conversely, a filesystem mounted read-only (`ro` / `MS_RDONLY`) returns `EROFS` (errno 30) regardless of mode bits or capabilities.
- **Exact Regression Caught:** Diagnostic tools or operator guides diagnosing `EACCES` by inspecting mount options rather than inode DAC bits and process capabilities, or asserting that mode `0555` causes `EROFS`.
- **Verification Anchor:** C2 JSON matrix schema requiring distinct branches for DAC (`EACCES`) and Read-Only Filesystem (`EROFS`), validated against primary man-pages `mkdir(2)` and `path_resolution(7)`.

### Regression R4: Process-Blind DAC Assumption (C2 vs D3/MC3 Regression)
- **Failure Mode:** Prior triage in `degraded-triage-r4.md:315-325` checked `User=root` and `CapabilityBoundingSet=cap_sys_admin` and declared that DAC could not explain `errno:13`. It assumed that running as uid 0 automatically grants DAC write bypass.
- **Exact Regression Caught:** Any analysis asserting that root execution inherently bypasses DAC permission checks. Under Linux capabilities (`capabilities(7)` S027, `path_resolution(7)`), DAC write bypass is governed solely by `CAP_DAC_OVERRIDE`. When systemd's `CapabilityBoundingSet=` (S028) drops `CAP_DAC_OVERRIDE`, uid 0 is subject to standard DAC checks (`access(2)` S034) and is denied write access to `0555` directories.
- **Verification Anchor:** C2 decision matrix branch asserting that DAC write permission for root requires either owner-write permission (mode `0200`) or `CAP_DAC_OVERRIDE` in the effective/permitted capability set.

### Regression R5: Gate Admission Omission of QUALITY #13 (Round-1 Spotcheck Regression)
- **Failure Mode:** In round 1, `adjacency-recheck-2026-10-19.md` was admitted without a `## QUALITY check` section, caught only during outside review (`round-1-verifier-spotcheck.md:12`). If round-12 admits `root-dac-decision-r12.md` without verifying that its `## QUALITY check` specifically evaluates Criterion 13, the round repeats the exact spotcheck failure.
- **Exact Regression Caught:** A knowledge entry claiming to resolve EACCES triage debt being admitted without explicitly validating Criterion 13 (pairing DAC mode/owner/ACL with `CapabilityBoundingSet`/`ProtectSystem` and accounting for `-Qkk`'s unowned `/` blind spot).
- **Verification Anchor:** Static check in the round-12 gate verifying that `corpus/knowledge/root-dac-decision-r12.md` contains an explicit `## QUALITY check` with a named Criterion 13 evaluation.

### Regression R6: Overfitting / False Degradation on Measured-Healthy Host (C1 Operability Regression)
- **Failure Mode:** Live host `/` is `555 root:root` (`stat -c '%a %U:%G' /`, measured 2026-10-19). The census executes as uid 1000. Shipped Linux distributions (e.g. Fedora `filesystem.spec` line 409, `ClaimCritic.md:29,38`) intentionally set `/` to mode `0555` by policy. If the census implements a naive rule that "missing owner-write (0200) -> DEGRADED" or demands mode `0755` without checking caller ownership, the census will falsely degrade valid, hardened host configurations.
- **Exact Regression Caught:** False-positive DEGRADED verdicts emitted on healthy hosts due to hardcoded `0755` expectations or evaluating owner-write bits against non-owner processes.
- **Verification Anchor:** Census probe evaluating mode bits via octal masks (`$((8#$mode & 0200))`), reporting `root_mode=%04o`, and establishing explicit, documented discrimination between owner and non-owner probing contexts.

---

## 3. Affected Axes
- **Operability (current score: 9):**
  - *Positive effect:* C1 eliminates the unowned root directory blind spot (moving root metadata findings 0 -> 1) without perturbing the six-plane rollup structure or introducing false-positive degradations.
  - *Guard against harm:* Resolving Regression R1 ensures the blind spot remains visible even when pacman is broken or locked (`db.lck`). Resolving R2 preserves fail-closed `BLOCKED` semantics. Resolving R6 ensures the census does not regress into an unsupportable hardcoded `0755` policy.
- **Depth (current score: 8, lowest tied with adjacency):**
  - *Positive effect:* C2 replaces informal narrative triage with a formal, source-backed 4-branch decision matrix grounded in primary Linux man pages (`mkdir(2)`, `path_resolution(7)`, `capabilities(7)`, `systemd.exec(5)`, `access(2)`).
  - *Guard against harm:* Resolving Regressions R3 and R4 ensures the matrix rigorously separates DAC from VFS mount flags (`EACCES` vs `EROFS`) and proves the capability-bounding mechanism without relying on speculative or rejected interpretations (S033).
- **Freshness (9), Adjacency (8), Calibration (9):**
  - Maintained strictly neutral. C1 and C2 remain causally separable: C2 direct probes do not consume census output, and C1 does not evaluate EACCES triage text.

---

## 4. Proposed Move: The Hermetic QUALITY-13 Bi-Directional Anchor

Synthesizing across the round's proposals (`Census`, `Matrix`, `C1Review`, `FixtureReview`, `GateScribe`, `ScoreReview`), the non-obvious move is to **bind C1 and C2 through a structural, bi-directional regression anchor governed by QUALITY #13, without coupling their runtime execution:**

1. **In C1 (`tools/tsukuroi-census.sh`):**
   - Decouple root metadata collection from `probe_packages()` into an independent block/helper that populates dedicated variables `ROOT_V` and `ROOT_NOTE`.
   - Fold `ROOT_V` in `main()` using the existing fold helper: `PKG_V=$(worse "$PKG_V" "$ROOT_V")` (mirroring the memory arm fold `DRV_V=$(worse "$DRV_V" "$MEM_V")` at line 2372).
   - In `run_selftest()`, add a regression test asserting that when `pacman db.lck` is present (`case_home='blocked-lck'`), the output contains `root_mode=` and root metadata. This structurally prevents Regression R1.
2. **In C2 (`corpus/knowledge/root-dac-decision-r12.md`):**
   - Structure the entry's `## QUALITY check` to evaluate Criterion 13 in two distinct, verifiable clauses:
     - *Clause 13a (Triage Pairing):* Formally pairs target DAC attributes (mode `0555`, owner `root`, base POSIX ACL) with unit properties (`CapabilityBoundingSet=CAP_SYS_ADMIN`, `ProtectSystem=no`), citing S027, S028, and S034.
     - *Clause 13b (Blind Spot Disconnection):* Explicitly documents that because `pacman -Qkk` cannot verify unowned `/` (D6), EACCES diagnosis cannot rely on package-manager health and must use direct filesystem inspection.
   - Formally record the rejection of S033 (conflating `0555` with `ro` mount / `EROFS`) under `## Rejected readings`. This structurally prevents Regressions R3 and R4.
3. **In the Gate Admission Checklist (`GateScribe` / `corpus/lessons/round-12.md`):**
   - Add an explicit static validation requirement ensuring that `root-dac-decision-r12.md` contains the `## QUALITY check` section with explicit Criterion 13 evaluation, directly barring the omission that caused the `round-1-verifier-spotcheck.md` disagreement (preventing Regression R5).

---

## 5. Risks and Failure Modes
- **Risk 1 (Rollup Field Disruption):** Downstream consumers and selftest assertions (e.g. line 2319 `^TSUKUROI_CENSUS: BLOCKED ...\)$`) depend on exact regex matches of the six-plane rollup line. Root metadata must be emitted strictly within the `PLANE packages: ...` note and not as a seventh plane or altered rollup key.
- **Risk 2 (Fixture Umask / Mode Leak):** In `run_selftest()`, `umask 077` at line 321 makes newly created fixture directories mode `0700`. Every test fixture expecting `0755` must run an explicit `chmod 755 "$FX/root"`. Furthermore, fixture paths must be cleaned up properly despite non-writable permission tests (e.g. `chmod 755` before `rm -rf` in cleanup traps).
- **Risk 3 (Non-Author Verification Gap):** As recorded across prior rounds, author-side seat execution is not independent non-author verification. Claiming a score advancement from 8 to 9 on Depth or advancing Operability requires subsequent orchestrator/integrator validation.

---

## 6. Verification Method (Parent Post-Integration Checks)

Parent agent should execute the following read-only checks once integration lands:
```sh
# 1. Verify C1 root metadata probe survives db.lck (Regression R1 check)
bash tools/tsukuroi-census.sh --selftest

# 2. Verify C2 decision matrix JSON schema and branch count (>=4 branches)
jq '[.branches[] | select((.id|length)>0 and (.evidence|length)>0 and (.interpretation|length)>0 and (.discriminator|length)>0 and (.limit|length)>0 and (.source_ids|length)>0)] | length' corpus/knowledge/root-dac-decision-r12.json

# 3. Verify C2 carries ## QUALITY check with explicit Criterion 13 (Regression R5 check)
grep -n -A 10 '^## QUALITY check' corpus/knowledge/root-dac-decision-r12.md | grep -E '13|QUALITY.*13'

# 4. Verify negative guards in C2 (no assertion of mode 0555 being ro mount, Regression R3 check)
grep -n -i -E 'read-only mount|always bypass|proven' corpus/knowledge/root-dac-decision-r12.md || true

# 5. Verify SOURCES registry validity
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
```

---

## 7. Tool Record
- **Installs/upgrades:** None. Used existing system binaries (`stat`, `findmnt`, `pacman`, `systemctl`, `getfacl`, `bash`, `python3`).
- **Commands run:** Target file inspection, read-only git queries, and globbing.
- **Independence:** Author-side seat evidence only; not independent non-author verification.
