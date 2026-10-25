# Frontier6Errno630 — Round-37 Frontier Assimilation Assessment (errno discrimination)

- **Seat:** `Frontier6Errno630` (L2 leaf connector, wave 1)
- **Judged on:** `adjacency`, `frontier:errno`
- **Milestone:** Source and overlap scan
- **Target Axes:** C1 operability (probe V8), C2 depth (r36 note corrections), C3 calibration (self-assessment mismatch repair; 27 fixed checks); frontier assimilation theme: errno discrimination

---

## 1. Evidence & Opened Sources

### Staged Package Entries Inspected
Three staged entries residing in `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/knowledge/corpus/knowledge/`:
1. `errno-name-discrimination-r25.md` (citing S204, S205): advocates replacing bare `errno:13` with 6 symbolic names (`EACCES`, `EPERM`, `EXDEV`, `EROFS`, `ESTALE`, `EBUSY`); distinguishes subvolume deletion `EPERM` from DAC `EACCES`.
2. `mount-errno-contract-r26.md` (citing S214, S220): examines `mount(2)` syscall and kernel `fs/btrfs/ioctl.c` handlers (`__btrfs_ioctl_snap_create`, `create_snapshot`); expands the vocabulary to a closed 12-class table replacing the 6-class table.
3. `errno-contract-variance-r37.md` (citing S279–S282, S286, S287): demonstrates `asm-generic/errno-base.h` assigns `EACCES` 13 on Linux kernel ABI and local Arch Linux x86_64 libc headers, discharging the portability caveat for this host; observes that host journal evidence for `errno:13` has aged out to 0 matches.

### Primary Sources Opened This Round (2026-10-25)
- **Upstream Linux UAPI `asm-generic/errno-base.h` (S282):**
  - **URL:** `https://raw.githubusercontent.com/torvalds/linux/v7.2/include/uapi/asm-generic/errno-base.h`
  - **Access date:** 2026-10-25
  - **Located quote (line 17):** `#define	EACCES		13	/* Permission denied */`
- **Local Host C Header `asm-generic/errno-base.h` (S286):**
  - **Path:** `/usr/include/asm-generic/errno-base.h`
  - **Access date:** 2026-10-25
  - **Located quote (line 17):** `#define	EACCES		13	/* Permission denied */`
- **Upstream `btrfs-subvolume.rst` (btrfs-progs v7.1) (S204):**
  - **URL:** `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/btrfs-subvolume.rst`
  - **Access date:** 2026-10-25
  - **Located quote (lines 104-106):** `"The default subvolume ... cannot be deleted and returns error (EPERM) and this is logged to the system log."` (19 words)
- **Upstream Linux manual page `errno(3)` (S279/S280):**
  - **URL:** `https://man7.org/linux/man-pages/man3/errno.3.html`
  - **Access date:** 2026-10-25
  - **Located quote (under Error numbers and names):** `"The error numbers that correspond to each symbolic name vary across UNIX systems, and even across different architectures on Linux."` (20 words)

### Local Host State Measurements (Read-Only)
- `journalctl --no-pager -o short-iso -g 'create subvolume failed' | grep -c 'errno:13'` returns `0` (retained boots aged out; 0 matches since 2026-10-01).
- `stat -c '%a %U:%G' /` returns `555 root:root` (underlying DAC mode unchanged).
- `systemctl cat limine-snapper-sync.service` confirms `User=root` and `CapabilityBoundingSet=CAP_SYS_ADMIN` remain unchanged.

---

## 2. Assessment Against PROVINCE, Coverage Map, Corpus & Sibling Boundaries

### Tsukuroi PROVINCE & Sibling Boundaries
- **In-Province:** `PROVINCE.md:8-14` owns read-only host/systemd and recovery diagnosis; `PROVINCE.md:20-24` owns the Snapper/rollback net (`snapper-eacces-mechanism.md`); `PROVINCE.md:85-97` (rounds 12-13) owns create-failure DAC/ACL, mount/namespace, and configured-credential discrimination.
- **Sibling Separation:**
  - Mori (ADJ-04, OUT-001, OUT-005): owns kill/OOM signals and cgroup memory evidence; the three staged entries strictly diagnose filesystem and syscall return codes, touching zero memory or kill events.
  - Kaidoku/Revenger (ADJ-06, OUT-008, OUT-009): owns reverse engineering of shipped binary artifacts; the staged entries inspect public open-source kernel sources (`fs/btrfs/ioctl.c`), UAPI headers, and man pages, performing zero binary reverse engineering.
  - Tameshi (ADJ-07, OUT-010): owns reusable verification methods; the entries supply host-domain failure taxonomy without attempting to absorb gate method ownership.

### Coverage Map & Corpus Boundaries
- Existing corpus notes `corpus/knowledge/snapper-eacces-mechanism.md`, `root-dac-decision-r12.md`, and `root-dac-correction-r13.md` already establish that ordinary `mkdir(2)` controls do not classify Btrfs ioctl failures and that historical `errno:13` causality remains inferential (`[inf]`).
- Staged Entry 2 (`mount-errno-contract-r26.md`) directly addresses this gap by opening `fs/btrfs/ioctl.c` to identify actual ioctl failure returns (`EXDEV`, `EPERM`, `EINVAL`, `EEXIST`, `ENOENT`, `ETXTBSY`, `EOPNOTSUPP`).

---

## 3. Precise Scope, Duplicate & Second-Order Issues

1. **Intra-Theme Redundancy & Table Supersession:**
   `mount-errno-contract-r26.md` explicitly replaces `errno-name-discrimination-r25.md`'s 6-class table with a 12-class table ("## What round 1 could not do", "## The discriminating table this replaces"). If admitted concurrently without explicit lineage metadata, the corpus retains two conflicting discriminating tables for identical paths. Furthermore, S205 (`man.archlinux.org/man/errno.3`) duplicates S279–S281 (`man7.org/linux/man-pages/man3/errno.3.html`).
2. **Second-Order Verification Coupling (C3 Calibration Risk via K07):**
   `tools/check-self-assessment.py` check K07 evaluates:
   `stated = stated_in(depth_cell, depth_row_text, r"(\d+)\s+notes\b")`
   `observed = len([p for p in list_dir_entries(repo, rev, "corpus/knowledge/") if p.endswith(".md")])`.
   Admitting three `.md` notes into `corpus/knowledge/` increments observed notes by +3. If `SCORECARD.md` depth row stated count is not simultaneously updated at the change commit, K07 triggers an immediate self-assessment mismatch (FAIL), breaking the C3 calibration target (27 fixed checks match).
3. **Epistemic Masking in Recheck Procedures:**
   `snapper-eacces-mechanism.md` line 3 records the recheck query: `journalctl ... -g 'create subvolume failed' | grep -c 'errno:13'`. As verified today, this command returns `0` solely because historical records aged out of the 6 retained boots. Treating count 0 as "fixed" is a false-negative trap identified by Entry 3 (`errno-contract-variance-r37.md`).

---

## 4. Proposed Move (One Bounded Synthesis)

**Implement an Ordered Assimilation Lock with Epistemic Recheck Guard and Atomic C3 Note-Count Sync:**

1. **Admit all three entries with explicit hierarchical sequencing:**
   - Admit `errno-contract-variance-r37.md` as the primary host-grounding note (discharging portability on x86_64, documenting aged-out evidence).
   - Admit `mount-errno-contract-r26.md` as the authoritative 12-class syscall/ioctl failure discriminator.
   - Admit `errno-name-discrimination-r25.md` with an appended header notice marking its 6-class table as historically foundational and superseded by `mount-errno-contract-r26.md`.
2. **Lock C3 calibration coupling:**
   - In the change commit that places the 3 notes into `corpus/knowledge/`, atomically increment the `depth` row note count in `SCORECARD.md` by +3 to ensure check K07 passes without regression.
3. **Guard the Recheck Contract:**
   - Update `corpus/knowledge/snapper-eacces-mechanism.md` recheck documentation to require checking root mode (`stat -c '%a' /`) and unit capabilities alongside journal counts, explicitly forbidding inference of resolution from an aged-out journal count of 0.

---

## 5. Affected Axes, Risks & Verification

- **frontier:errno:** Advances failure attribution from bare numbers to kernel-level ioctl/syscall discrimination while eliminating portability ambiguity on this host.
- **adjacency:** Zero boundary leakage into Mori (OOM/pressure) or Kaidoku/Revenger (binary RE).
- **C3 calibration:** Defends the 27-check self-assessment against an uncoordinated K07 mismatch.
- **C1 operability & C2 depth:** No interference; cleanly separable.
- **Risks:** ID collisions if imported S204+ rows are appended before C1 allocates S200 (strace) and S201 (probe own-work); mitigate by reserving S200-S201 for C1 and appending package rows starting at S204.
- **Verification:**
  - Run `python3 tools/check-self-assessment.py --revision <REV>` verifying K07 matches observed note count.
  - Verify `stat -c '%a %U:%G' /` reads `555 root:root` and `journalctl --no-pager -o short-iso -g 'create subvolume failed' | grep -c 'errno:13'` reads `0`.
  - Re-verify opened source quotes against upstream git tags v7.1 and v7.2.

---

## 6. Tooling Record
- No tools installed or updated.
- Host pacman transactions remained paused host-wide; no pacman commands executed.
- Repository state: read-only; no tracked lane, fleet, or sibling files modified.
