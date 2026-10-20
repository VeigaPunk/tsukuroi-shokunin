# FrontierConnector — round 14 repair, seat TsukuroiR14.FrontierConnector

Seat: connector (UFO-FSD connector; author-side synthesis, not non-author verification).
Scope: Connect rollback-net coverage with S044/S045 curation; recommend honest expansion unchanged and precise frontier not advanced, preserving boot-hook blocker.

## 1. Axes & Learning Trends
- **depth (worked, tied lowest at 8):** Improved. C1 repairs r13 MD:97 value-domain defect and S042 attribution overclaim without score inflation (held at 8).
- **coverage (held at 9):** Unchanged. Bounded to existing "Snapper/rollback net" surface (`PROVINCE.md:24,88-96`).
- **operability (9), freshness (9), calibration (9), adjacency (8):** Unchanged.
- **Learning trends:** expansion **unchanged** (honest adherence to LEARNING; repair on existing surface, no geometric expansion); quality **improved**; discernment **improved**.

## 2. Evidence
1. **Rollback-Net Ground (`corpus/README.md:59-78`, `PROVINCE.md:88-96`):** "Snapper/rollback net" owns read-only create-failure diagnostics. R12/R13 refined this surface; R14 repairs active r13 defects without creating a new surface.
2. **S044 Curation (`systemd.exec(5)`):** Documents `ProtectSystem=` value domain as boolean/full/strict; non-exhaustiveness belongs to unit-side mount mechanisms (`BindReadOnlyPaths=`, `TemporaryFileSystem=ro`). Refines unit sandbox diagnostics without expanding OS coverage.
3. **S045 Curation (omarchy #8047 comment 6071740243):** Separates API User/COLLABORATOR fields from body's unverified VM assertion and Codex Medium second opinion; rejects host-cause/maintainer-acceptance use; does not transfer #6629 disclaimer.
4. **Boot-Hook Blocker & Frontier Invariant (`corpus/knowledge/initramfs-v42-sysroot-recovery.md:7-14`, `SKILL.md:1658,1751`):** Host runs `mkinitcpio 41.1-1`. Configured busybox runtime hooks (`btrfs-overlayfs`, `plymouth`) hardcode `/new_root`. Under mkinitcpio v42 (`/sysroot`), `btrfs-overlayfs` silently exits 0, disabling overlayfs on snapshot boot. S045's discussion does not resolve this incompatibility. The update-safety blocker stands; exact failure-time runtime namespace remains unobserved `[unknown]`.

## 3. Affected Axes
- **depth:** Improved / restored. Repairs factual defects on existing rollback-net ground.
- **coverage:** Unchanged. Retains 6 planes and existing surfaces; no new capability or surface claimed.
- **operability, freshness, calibration, adjacency:** Unchanged.

## 4. Proposed Move (One Bounded Synthesis)
Synthesize S044 and S045 curation as **strictly inward-facing diagnostic boundary refinements on the existing rollback-net surface**:
1. **Domain vs Mechanism Disambiguation (S044):** Scope `ProtectSystem=` to its closed documented domain (boolean/full/strict) and distinguish it from open unit-side mount mechanisms, refining unit diagnostics without claiming a new sandboxing plane.
2. **Attribution Disentanglement (S045):** Disentangle API metadata from unverified comment claims; retain community-C host-cause rejection without transferring #6629 disclaimers.
3. **Freeze Frontier & Preserve Boot-Hook Blocker:** Explicitly declare that S045 overlay discussion does not resolve the `mkinitcpio` v42 `/sysroot` transition. The boot-chain upgrade-safety blocker remains unbroken; failure-time namespace remains unobserved `[unknown]`.
4. **Declare Expansion Unchanged:** Formally grade learning trend expansion as **unchanged** in the scorecard/lesson, preventing false coverage or capability inflation.

## 5. Risks & Second-Order Effects
- **Blocker Conflation:** Treating S045 discussion as authorization to bypass the boot-hook upgrade gate. *Mitigation:* Explicitly reaffirm that mkinitcpio v42 `/sysroot` remains blocked.
- **Coverage Inflation:** Treating S044/S045 as new coverage surfaces. *Mitigation:* Bounded strictly to existing "Snapper/rollback net" surface; declare expansion unchanged.
- **Disclaimer Cross-Contamination:** Re-transferring #6629 bot disclaimer to #8047. *Mitigation:* Enforce QUALITY #19/#20 source/quote separation.

## 6. Verification (Non-Author Execution by L1 / Integrator)
1. `scripts/sources-census.sh validate tsukuroi`: Validates S044/S045 schema, quote <= 25 words, disclosed W04 URL reuse.
2. `tools/check-source-scope-correction.py`: Fails baseline r13; passes r14 correction pair.
3. Surface Invariant: `git diff PROVINCE.md corpus/README.md` shows 0 new surfaces or planes added.
4. Update-Safety Invariant: `mkinitcpio` v42 `/sysroot` upgrade-safety blocker remains active; live census unchanged.

## 7. Findings, Limitations & Tooling Record
- **Findings:** S044/S045 curation refines existing rollback-net diagnostic boundaries; expansion is honestly unchanged; frontier is not advanced; boot-hook blocker is fully preserved.
- **Limitations:** Leaf seat; author-side recommendation only; non-author verification is integrator's role.
- **Tooling record:** Tools installed/updated: none.
