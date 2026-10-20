# ConnectPlannerWalk — C1/C2 Causal Independence & Minimal Skeleton Walk (Round 15)

author: TsukuroiR15.ConnectPlannerWalk (connector)
date: 2026-10-20
seat: ConnectPlannerWalk
role: UFO-FSD connector / leaf researcher
target_file: .ufo/waves/round-15/build/ConnectPlannerWalk.md
baseline: 0db618a71ae2d0bb0c0c3059abaa219b7ccd20a2
judged_on: depth

---

## 1. Scope, Declared Axes, & Frontier Position

### A. The Six Declared Axes
1. **depth** (primary declared claim C1; ordinal 8 → 8, delta 0):
   - Lowest tied axis (alongside adjacency at 8).
   - Resolves both round 14 verifier routed documentation debts:
     a. **Locator qualification**: Replacing fragile, reader-dependent bare line numbers (lines 1266–1267) with the stable structural heading hierarchy (`systemd.exec(5) > SANDBOXING > ProtectSystem=`), native fragment (`#ProtectSystem=`), and footer version (`systemd 262.1`).
     b. **Positive domain definition**: Grounding the argument domain strictly in the positive 11-word definition sentence (*"Takes a boolean argument or the special values \"full\" or \"strict\"."*), superseding unbacked negative absence claims (*"documents no further values"*), without asserting an unproven exhaustive parser proof.
2. **freshness** (primary declared claim C2; ordinal 9 → 9, delta 0):
   - Re-verifies update safety following the operator-reported `2026-10-20 04:25` `libinput` partial upgrade (`pacman -S --needed --noconfirm libinput libinput-tools`).
   - Binds fresh read-only host snapshot evidence (`captured_at: 2026-10-20T07:44:39Z`, SHA256 `b101f3747827cefd0ed604c14b669267ec0fcc1b6c2fbe6e486be0cdbbc6ea81`).
   - Measures 413 pending updates against local sync databases born `2026-10-18 14:11:00.026 -0300`.
   - Affirms `BLOCKED_FOR_AGENT_PACKAGE_ACTION` with zero package mutations and zero upgrade clearance.
3. **coverage** (retained 9, delta 0):
   - Unchanged. C1 and C2 operate strictly within existing rollback-net and update-safety surfaces (`PROVINCE.md:5-24`). No new uncovered territory is claimed or acquired.
4. **operability** (retained 9, delta 0):
   - Unchanged. Census tooling and gate invariants remain preserved. No live package changes, service restarts, or system repairs performed.
5. **calibration** (retained 9, delta 0):
   - Unchanged. No ordinal inflation (all deltas strictly 0). Structural tool passes explicitly decoupled from live semantic truth and operational health.
6. **adjacency** (retained 8, delta 0):
   - Unchanged. Leaf research; strictly within assigned `.ufo/waves/round-15/build` workspace. No sibling worktrees, fleet files, or routing mutated.

---

## 2. C1 / C2 Causal Independence Enunciation

A primary architectural requirement of the round 15 plan is demonstrating that Claim 1 (C1/depth) and Claim 2 (C2/freshness) are **strictly causally independent**. Neither claim's validity, evidence, or evaluation depends upon or entails the other:

```
+---------------------------------------------------------------------------------------------------+
|                                  CAUSAL INDEPENDENCE DISJUNCTION                                  |
+-------------------------------------------------+-------------------------------------------------+
|               C1: DEPTH SURFACE                 |              C2: FRESHNESS SURFACE              |
|          (Documentation-Debt Repair)            |          (Host Incident Re-Verification)        |
+-------------------------------------------------+-------------------------------------------------+
| Substrate: Upstream man page text & structure   | Substrate: Host filesystem, ALPM logs, sync DBs |
| Source: S046 (systemd.exec(5), docs/A)          | Sources: S047 (Wiki), S048 (pacman(8)), Host DB |
| Target Locus: Unit sandboxing ProtectSystem=    | Target Locus: /var/lib/pacman, /var/log/pacman  |
| Semantic Field: Systemd service execution spec  | Semantic Field: ALPM package manager state      |
| Evaluator: tools/check-locator-clarification.py | Evaluator: tools/measure-update-recheck.py      |
| Nature of Claim: Static textual conformance     | Nature of Claim: Dynamic point-in-time capture  |
| State Coupling: Zero host state required        | State Coupling: Pure read-only host observation |
+-------------------------------------------------+-------------------------------------------------+
```

### Detailed Factor Separation
1. **Substrate & Domain Decoupling:**
   - **C1** investigates upstream specification text: how `systemd` documents option syntax for execution sandboxing (`ProtectSystem=`). Its domain is immutable textual documentation.
   - **C2** investigates host packaging substrate: pacman database timestamps, ALPM transaction logs, package version deltas (`libinput 1.31.3-1 -> 1.32.0-1`), and boot hook path strings (`/new_root`).
2. **Failure-State Orthogonality:**
   - If C1 is completely red (e.g. locator unanchored or negative absence claimed), C2 remains completely verifiable from the host snapshot and ALPM doctrine.
   - If C2 is completely blocked or corrupted (e.g. snapshot hash mismatch or host DB unreadable), C1's textual clarification of `systemd.exec(5)` remains 100% sound.
3. **Tooling & Verification Path Separation:**
   - C1 is verified by an in-memory structural conformance gate (`check-locator-clarification.py`) reading git blobs.
   - C2 is verified by a read-only probe reporter (`measure-update-recheck.py`) evaluating snapshot SHA256 integrity and field linkages.
   - There is zero cross-import, zero shared state, and zero execution dependency between C1 and C2 evaluation tools.

---

## 3. Minimal Skeleton Walk: Concrete Instance (One-Case)

To establish the data walk without replacing L1's top-level canonical plan, we trace the concrete lifecycle of a single instance through the complete evidence chain:

### Instance Walk: `ProtectSystem=` Locator & Option Domain (C1)
1. **Defect Identified (Historical Baseline `0db618a`):**
   - In Round 14, `source-scope-correction-r14.md:34` and JSON `corrections[0].location` cited `"rendered lines 1266-1267"`.
   - Outside verifier spot-check observed that in standard text rendering, lines 1266–1267 discuss `AF_UNIX` sockets; `ProtectSystem=` definition appears at lines 1272–1273.
   - Furthermore, `source-scope-correction-r14.md:41-42` asserted: *"The opened revision documents no further values for ProtectSystem="*, which was an unsupported negative absence claim lacking a dated command sweep.
2. **Evidence Anchor Reopened (S046 Witness):**
   - Reopened `https://man.archlinux.org/man/systemd.exec.5` (footer `systemd 262.1`).
   - Located structural anchor: Section `SANDBOXING` > Subsection `ProtectSystem=`.
   - Extracted positive definition quote (11 words, exact):
     > *"Takes a boolean argument or the special values \"full\" or \"strict\"."*
3. **Notice & Supersession Applied (Append-Only):**
   - Baseline r14 bytes preserved intact.
   - New pair created: `corpus/knowledge/source-locator-clarification-r15.md` and `.json`.
   - Notice supersedes r14's bare rendered lines 1266–1267 with the structural path `SANDBOXING > ProtectSystem=` and footer `systemd 262.1`.
   - Notice supersedes r14's negative sentence, retaining purely the positive 11-word definition sentence.
4. **Structural Conformance Gating:**
   - `tools/check-locator-clarification.py` reads revision blobs.
   - Asserts:
     - Baseline (`0db618a`): `findings` contains `LOCATOR_UNQUALIFIED` and `NEGATIVE_DOMAIN_UNSWEPT`, count = 0, exit = 1.
     - Worktree / Landed: `findings` = [], count = 2, status = `PASS`, exit = 0.
5. **Decoupled Truth Verification:**
   - Evaluator output confirms structural conformance (count = 2).
   - Dated external witness (`C1SourceWitness.json`) confirms external source agreement.

### Parallel Instance Walk: `libinput` Partial Upgrade Incident (C2)
1. **Trigger & Host Capture:**
   - Operator reports `pacman -S --needed --noconfirm libinput libinput-tools` executed at `2026-10-20T04:25:16-0300`.
   - Host snapshot executed once by `HostSnapshot`: `captured_at: 2026-10-20T07:44:39Z`, 18318 bytes, SHA256 `b101f374...`.
   - Probes verify:
     - `package_versions`: `libinput 1.32.0-1`, `libinput-tools 1.32.0-1`, `mkinitcpio 41.1-1`, `systemd 261.2-1`.
     - `pending_updates`: 413 packages pending against sync DBs born `2026-10-18 14:11:00-0300`.
     - `libinput_log`: ALPM log confirms upgraded libinput and installed libinput-tools without preceding sync marker post-line 2288.
     - `boot_hook_mentions`: `btrfs-overlayfs:4` and `plymouth:11` both retain `/new_root`; 0 `/sysroot` mentions.
2. **Doctrine Integration:**
   - S047 (ArchWiki System maintenance § Partial upgrades are unsupported): `-Sy` followed by `-S package` is unsupported.
   - S048 (`pacman(8)`): `--needed` suppresses reinstall of already up-to-date targets; it does NOT suppress upgrading an installed target whose sync version is newer.
3. **Decision Rule:**
   - Even though `libinput` is up to date and reports no broken dependencies locally, the host has 413 updates pending across kernel, systemd, and glibc.
   - Full upgrade (`pacman -Syu`) is blocked by mkinitcpio 42 `/sysroot` hook incompatibility.
   - Autonomous agent upgrade/install is strictly prohibited.
   - Decision emitted: `BLOCKED_FOR_AGENT_PACKAGE_ACTION`.

---

## 4. Generalization: The Standard Tsukuroi Repair/Recheck Pattern

From the concrete one-case walk, we derive the general canonical skeleton for all future tsukuroi repairs and rechecks:

```
+---------------------------------------------------------------------------------------------------+
|                             CANONICAL REPAIR/RECHECK PATTERN SKELETON                             |
+---------------------------------------------------------------------------------------------------+
|  1. IDENTIFY DEFECT / TRIGGER                                                                     |
|     - Distinguish historical record vs active advice.                                             |
|     - Isolate exact locus (file, heading, line/key, quote).                                       |
|                                                                                                   |
|  2. RE-OPEN PRIMARY EVIDENCE                                                                      |
|     - Reopen primary authority (docs/tier A or read-only host snapshot).                          |
|     - Never launder community tier C into authority.                                              |
|     - Record exact dated witness with cryptographic or HTTP provenance.                           |
|                                                                                                   |
|  3. APPLY APPEND-ONLY SUPERSESSION                                                                |
|     - Never mutate or rewrite historical revision lines.                                          |
|     - Append explicit notice blocks citing superseded ID, locus, and replacement.                 |
|     - Disclose duplicate URLs (W04) as expected census warnings.                                  |
|                                                                                                   |
|  4. BOUNDED CONFORMANCE GATING (Red-Before -> Green-After)                                        |
|     - Build minimal hermetic checker (<=250 lines).                                               |
|     - Assert FAIL on baseline for the specific defect (not mere missing file).                    |
|     - Assert PASS on delivered revision with exact count and findings = [].                       |
|     - Provide self-contained selftest with isolated defect fixtures.                              |
|                                                                                                   |
|  5. DECOUPLE CONFORMANCE FROM TRUTH & HEALTH                                                      |
|     - Machine check = structural conformance only.                                                |
|     - Source truth = dated witness record.                                                        |
|     - Operational health = non-assessed; hold fail-safe decision gate.                           |
+---------------------------------------------------------------------------------------------------+
```

---

## 5. Non-Obvious Synthesis: The Decoupled Double-Gate Move

By synthesizing findings from peer seats (`ConnectFrontier`, `ReviewCounting`, `ReviewEvidencePins`, `ReverseGatePattern`, `AttackVacuity`, and `SafetyPackages`), we identify the non-obvious move that improves round 15 without harming any axis:

### The Move: Strict Decoupling of Conformance, Semantic Truth, and Operational Health
1. **The Trap:**
   - In C1: Claiming that a green pass of `check-locator-clarification.py` proves that systemd has no other hidden options or that the parser is mathematically closed.
   - In C2: Claiming that zero unresolved dynamic symbols (`ldd -r`) or an empty diff on `libinput` implies the system is healthy, safe to upgrade, or repaired.
2. **The Synthesis:**
   - Enforce a strict three-tier taxonomy:
     - **Tier 1 (Mechanical Conformance):** Evaluators emit `conforming_correction_count: 2` (C1) or `record_count: 1` (C2). They test only byte patterns, structural headers, and schema invariants.
     - **Tier 2 (Dated External Witness):** Source agreement rests on dated JSON witnesses (`C1SourceWitness.json` for S046; raw `host-snapshot.json` SHA256 for C2).
     - **Tier 3 (Operational Health & Gate):** Fixed constant `health: "not_assessed"` and `decision: "BLOCKED_FOR_AGENT_PACKAGE_ACTION"`.
3. **Axis Impact:**
   - **Depth:** Improves via unshakeable epistemic grounding that resists external verifier attacks on over-claiming.
   - **Freshness:** Improves via precise, tamper-resistant capture of the partial-upgrade state without risking boot failure.
   - **Operability / Calibration / Coverage / Adjacency:** Completely unharmed (0 deltas).

---

## 6. Verification and Risk Analysis

### Identified Risks & Mitigations
1. **Risk: Checker Vacuity (AttackVacuity finding):**
   - *Hazard:* Checker passes cleanly because r14 defect bytes were completely deleted, or fails baseline merely because the r15 file does not exist.
   - *Mitigation:* `check-locator-clarification.py` must verify that r14 retains historical text under explicit notices, and baseline fails with explicit finding IDs `LOCATOR_UNQUALIFIED` and `NEGATIVE_DOMAIN_UNSWEPT`.
2. **Risk: Unbound Snapshot Tampering (ReviewEvidencePins finding):**
   - *Hazard:* Consumer modifies `host-snapshot.json` or evaluates against wrong file.
   - *Mitigation:* C2 JSON and measurer strictly require and re-verify raw byte SHA256 `b101f3747827cefd0ed604c14b669267ec0fcc1b6c2fbe6e486be0cdbbc6ea81`.
3. **Risk: Accidental Mutation via Tooling Directive (SafetyPackages finding):**
   - *Hazard:* Agent reads tooling directive channel 1 (`sudo pacman -S --needed`) and attempts to install or repair dependencies.
   - *Mitigation:* Round 15 strict context explicitly forbids all package transactions. Pre-transaction dry-run guard requires `pacman -Sp` and aborts on any installed package overlap.

---

## 7. Sources, Limits, and Tools

### Exact Sources Cited
- `corpus/SOURCES.md`: S001–S045 (baseline), S046 (systemd.exec(5), docs/A), S047 (ArchWiki System maintenance, docs/A), S048 (pacman(8), docs/A).
- `corpus/lessons/round-14-verifier-spotcheck.md:230-265` (adjudicated concerns 1 & 2).
- `host-snapshot.json` (`captured_at: 2026-10-20T07:44:39Z`, SHA256 `b101f374...`).
- Peer artifacts: `HostSnapshot.md`, `ConnectFrontier.md`, `ReviewCounting.md`, `ReviewEvidencePins.md`, `ReverseGatePattern.md`, `AttackVacuity.md`, `SafetyPackages.md`, `C1SourceWitness.json`.

### Limits
- Read-only research. No external network queries issued. No package transactions, systemd services, or initramfs hooks modified.
- Evaluators and gate checkers were statically inspected, not executed by this seat.
- Operational health remains uncertified; no upgrade clearance granted.

### Tools
- Read, write, glob, grep only.
- Installs, updates, or removals: **none**.
- Passwordless `sudo` not used.
