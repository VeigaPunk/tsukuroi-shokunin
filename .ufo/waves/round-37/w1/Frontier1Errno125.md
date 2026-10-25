# Frontier1Errno125 — Errno Discrimination Theme & Staged Entries Assessment

## 1. Overview & Declared Axes

- **frontier:errno:** Ground symbolic errno classification against Linux VFS, kernel ABI, and Btrfs ioctl semantics while avoiding symptom/cause conflation and ungrounded causal attribution.
- **adjacency:** Keep diagnosis strictly within Tsukuroi's read-only OS/rollback-net domain boundary (`PROVINCE.md:8–14, 85–97`), without encroaching into sibling lanes: mori (kill/OOM and disk runway, ADJ-04), kaidoku/revenger (binary reverse engineering, ADJ-06), kama (endpoint/model serving, ADJ-01), or tameshi (mutation testing/verification method, ADJ-07).
- **depth (C2):** Protect established diagnostic depth by preventing regression of verified knowledge (specifically guarding against the re-emergence of the refuted CX2 `EPERM`/`CAP_SYS_ADMIN` error).
- **calibration (C3):** Maintain consistency across SCORECARD self-assessment records and the 27 fixed checks in `tools/check-self-assessment.py`.

---

## 2. Bounded Evidence Sweep

### 2.1 Repository & Corpus Context
1. **Tsukuroi PROVINCE (`PROVINCE.md`):**
   - Owns read-only OS substrate triage, package state, systemd units, journal/boot error triage, and Snapper rollback-net capability/permission diagnostics (`PROVINCE.md:8–24`).
   - Round-12/13 refinements (`PROVINCE.md:85–97`): Root-directory metadata, DAC/ACL, mount/namespace, and configured capability boundaries remain within the host/rollback-net surface. Tsukuroi owns detection and mechanism reporting; it refuses configuration mutation, service restart, subvolume creation, or package installation.
2. **Coverage Map (`corpus/README.md`):**
   - Lines 20 & 40–41: `snapper-eacces-mechanism.md` candidate mechanism for recurring `errno:13` (`/` mode 0555 + `CapabilityBoundingSet=CAP_SYS_ADMIN` dropping `CAP_DAC_OVERRIDE`) remains `[inf]` with a defined operator falsifier.
   - Lines 57 & 73: `root-dac-decision-r12.md` and active correction `root-dac-correction-r13.md` (R13-DAC-EXCLUSIVITY) establish ordinary directory creation error boundaries (`EACCES` vs `EROFS` vs `EEXIST`), isolating API-level illustrative models from historical Btrfs ioctl proof.
3. **Round-12 Verification Precedents:**
   - `MatrixCritic.md:81–83` (Counterexample CX2): Caught and rejected the claim that Btrfs subvolume creation requires `CAP_SYS_ADMIN` and fails with `EPERM` when absent. Upstream kernel source confirmed `btrfs_mksubvol` executes `may_create_dentry` (VFS DAC check returning `-EACCES`), not a `CAP_SYS_ADMIN` gate.

### 2.2 Staged Artifacts Located
The three staged entries and supporting source rows were located under `/home/vgpnk/Projects/shokuknow/`:
- **Entry 1:** `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/knowledge/corpus/knowledge/errno-name-discrimination-r25.md` (citing S204, S205)
- **Entry 2:** `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/knowledge/corpus/knowledge/mount-errno-contract-r26.md` (citing S214, S220)
- **Entry 3:** `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/knowledge/corpus/knowledge/errno-contract-variance-r37.md` (citing S279–S282, S286, S287)
- **Staged Sources:** `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md` (rows S204, S205, S214, S220, S279–S282, S286, S287).

### 2.3 Primary Sources Opened This Round
All citations opened and verified in-round on 2026-10-25:
1. **Linux Kernel Generic Errno Base Header (`include/uapi/asm-generic/errno-base.h` @ tag v7.2):**
   - URL: `https://raw.githubusercontent.com/torvalds/linux/v7.2/include/uapi/asm-generic/errno-base.h`
   - Access Date: 2026-10-25
   - Located Quote (line 21): `#define EACCES 13 /* Permission denied */`
   - Located Corroboration (line 9 & 38): `#define EPERM 1 /* Operation not permitted */` and `#define EROFS 30 /* Read-only file system */`
2. **Btrfs-Progs Subvolume Manual Source (`Documentation/btrfs-subvolume.rst` @ tag v7.1):**
   - URL: `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/btrfs-subvolume.rst`
   - Access Date: 2026-10-25
   - Located Quote (lines 62–63): `still retry the remaining destinations, but would return 1 to indicate the failure (similar to what :command:`mkdir` would do.`
   - Located Corroboration (lines 102–104): `The default subvolume ... cannot be deleted and returns error (EPERM) and this is logged to the system log.`
3. **Linux Kernel Btrfs Ioctl Implementation (`fs/btrfs/ioctl.c` @ tag v7.2):**
   - URL: `https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/ioctl.c`
   - Access Date: 2026-10-25
   - Located Quote (lines 1178–1180): `/* Subvolume creation is not restricted, but snapshots are limited to own subvolumes only */ ret = -EPERM;`
4. **Linux Programmer's Manual — `errno(3)` (Linux man-pages 6.19):**
   - URL: `https://man.archlinux.org/man/errno.3` / `https://man7.org/linux/man-pages/man3/errno.3.html`
   - Access Date: 2026-10-25
   - Located Quote: `The error numbers that correspond to each symbolic name vary across UNIX systems, and even across different architectures on Linux.`
   - Located Corroboration: `The value in errno is significant only when the return value of the call indicated an error`

---

## 3. Assessment of the Three Staged Entries

### 3.1 Entry 1 (`errno-name-discrimination-r25.md`) — Scope & Status
- **Core Proposition:** Records that `errno:13` is an unsafe notation because `errno(3)` numbers vary across architectures; establishes that errno is thread-local and only significant on failed return; introduces a 6-class vocabulary (`EACCES`, `EPERM`, `EXDEV`, `EROFS`, `ESTALE`, `EBUSY`).
- **Assessment:** Sound general theory, but superseded and completed by Entry 3. Entry 1 leaves the host-specific binding open, stating that the number 13 cannot be cited as `EACCES`. Entry 3 demonstrates that on this Linux x86_64 ABI, the portability caveat is formally discharged.
- **Verdict:** Admissible as foundational vocabulary, but subordinated to Entry 3 for host-specific claims.

### 3.2 Entry 2 (`mount-errno-contract-r26.md`) — Precise Scope Defect & Contradiction
- **Core Proposition:** Expands error vocabulary to 12 classes across `mount(2)` (S214) and `fs/btrfs/ioctl.c` (S220).
- **Critical Flaw:**
  - In lines 61–62, Entry 2 asserts: *"`13` alone carries almost no information; `EPERM` plus 'the caller lacked `CAP_SYS_ADMIN`' carries the diagnosis."*
  - Line 46 similarly maps `EPERM` to *"`missing CAP_SYS_ADMIN for mount, or snapshotting a subvolume you do not own"`*.
- **Contradiction Analysis:**
  1. Conflates `subvol=true` (`btrfs_mksubvol`) with `subvol=false` (`create_snapshot`). In `__btrfs_ioctl_snap_create`, the check for subvolume ownership returning `EPERM` applies strictly to snapshot creation (`subvol=false`), not subvolume creation (`subvol=true`).
  2. For subvolume creation (`snapper create-config` creating `/.snapshots`), `btrfs_mksubvol` delegates to `may_create_dentry` in `fs/namei.c`. Mode `0555` on `/` without `CAP_DAC_OVERRIDE` returns `-EACCES` (errno 13). It does *not* require `CAP_SYS_ADMIN` for directory DAC traversal, nor does it return `EPERM`.
  3. This directly revives counterexample CX2, which was formally refuted in Round 12 (`MatrixCritic.md:81–83`). Admitting Entry 2 unamended would contradict both the host journal observations (`errno:13`) and the landed knowledge in `root-dac-correction-r13.md`.
- **Verdict:** REJECT the subvolume ioctl diagnostic claim in Entry 2. ADMIT only the `mount(2)` syscall contract (S214) scoped to the snapshot-boot overlayfs path.

### 3.3 Entry 3 (`errno-contract-variance-r37.md`) — Substrate Precision & Age-Out Discovery
- **Core Proposition:**
  1. Anchors `errno(3)` semantics (S279–S281).
  2. Discharges the portability caveat on this host via kernel ABI `include/uapi/asm-generic/errno-base.h` (S282) and host C library headers `/usr/include/asm-generic/errno-base.h` (S286): on Linux x86_64, `EACCES` is 13, `EROFS` is 30, and `EPERM` is 1.
  3. Discovers an essential host substrate fact: re-running the `snapper-eacces-mechanism.md` probe on 2026-10-24 yields **0** matches because retained journal logs rotated (6 boots retained), whereas the underlying causal substrate (`/` mode `0555`, `CapabilityBoundingSet=CAP_SYS_ADMIN` dropping `CAP_DAC_OVERRIDE`) remains active.
- **Assessment:** Exemplary diagnostic discipline. Prevents the false conclusion that the absence of recent journal errors implies resolution of the permission/capability block.
- **Verdict:** ADMIT as the primary operative entry for the round-37 errno-discrimination theme.

---

## 4. Proposed Move (Connector Synthesis)

**Bounded Proposal:**
Execute an asymmetric admission and reconciliation of the three staged entries:
1. **Admit Entry 3 (`errno-contract-variance-r37.md`)** as the primary operative note for the round-37 errno-discrimination theme, along with its supporting sources (S279–S282, S286, S287).
2. **Condition / Narrow Entry 2 (`mount-errno-contract-r26.md`):** Admitting S214 (`mount(2)`) strictly for the boot-time `btrfs-overlayfs` mount contract, while explicitly **rejecting and excising** lines 46 and 61–62 that claim `EPERM` / `CAP_SYS_ADMIN` explains the subvolume creation failure.
3. **Index Entry 1 (`errno-name-discrimination-r25.md`)** as conceptual background, recording in its preamble that its general portability limitation is resolved for this host by Entry 3.

---

## 5. Risks and Second-Order Effects

1. **Risk:** If Entry 2 were rejected entirely, the corpus would lose the valid `mount(2)` closed errno mapping needed for diagnosing `btrfs-overlayfs` snapshot-boot failures.
   - *Mitigation:* Retain the `mount(2)` syscall error mapping (S214), isolating it from the Btrfs subvolume ioctl path.
2. **Risk:** Sibling seats or operators inspecting a 0-match journal sweep could mark `snapper-eacces-mechanism` as resolved.
   - *Mitigation:* Entry 3's explicit distinction between log retention window expiration and substrate state persistence provides an active barrier against false-positive resolution.
3. **Substrate & Verification Safety:** All probes and cited documents are strictly read-only. No packages are modified, no services restarted, and no repo Git/jj states altered.

---

## 6. Verification

1. **Kernel Ioctl Verification:** Inspect `fs/btrfs/ioctl.c` (tag v7.2, lines 1170–1195) to confirm that `btrfs_mksubvol` is called for subvolume creation without owner-`EPERM` checks, while `EPERM` is restricted to snapshotting unowned subvolumes (`subvol=false`).
2. **Host ABI Header Verification:** Inspect `/usr/include/asm-generic/errno-base.h` to confirm:
   - Line 21: `#define EACCES 13`
   - Line 9: `#define EPERM 1`
   - Line 38: `#define EROFS 30`
3. **Journal Log Sweep Verification:** Execute `journalctl -u limine-snapper-sync.service` to verify that 0 `errno:13` matches are returned in the currently retained 6-boot window, while `stat -c '%a' /` remains `555`.
