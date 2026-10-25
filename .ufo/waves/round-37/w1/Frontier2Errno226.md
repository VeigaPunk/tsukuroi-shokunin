# Frontier2Errno226 — errno-discrimination theme: source and overlap scan

- **Seat:** Frontier2Errno226 (L2 connector, tsukuroi lane round 37 attempt 1, wave w1).
- **Date:** 2026-10-25.
- **Axes:** Adjacency, frontier:errno.
- **Milestone:** Source and overlap scan.
- **Rules & Bounds:** Read `/home/vgpnk/.omp/agent/RULES.md` lines 1–14; read-only on lane content; no lane/fleet/sibling/source mutations; no git/jj writes; no pacman or host mutation; no subagent dispatch.

---

## 1. Scope and Ground Truth Assessment

The round-37 declaration (`SCORECARD.md:1936-1941`) specifies:
> "Assimilation (§10): ONE theme — errno discrimination — with THREE package entries admitted from `merge/tsukuroi/`: `errno-name-discrimination-r25.md`, `mount-errno-contract-r26.md`, `errno-contract-variance-r37.md`; rows S204/S205/S214/S220/S279–S282/S286/S287 appended (transformed to fleet schema in scratch, census-validated, collision-guard proven) with re-grounded Gate quotes. Quarantine slice (12 data rows) hand-checked with a verdict per row. This rides inside §2b and adds no claim slot."

The staged files were located and inspected in `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/` and in the staging validation directory `.ufo/waves/round-37/assimilation/validate/corpus/`:
1. `errno-name-discrimination-r25.md` (cites S205, S204): abstract POSIX C library errno contract (meaningful only on failed return, thread-local, numbers not portable); 6-class table (`EACCES, EPERM, EXDEV, EROFS, ESTALE, EBUSY`).
2. `mount-errno-contract-r26.md` (cites S214, S220): syscall and ioctl returns (`mount(2)` and `fs/btrfs/ioctl.c`); 12-class table stated as replacing the 6-class table; distinguishes `EROFS` vs `EACCES` on read-only sources.
3. `errno-contract-variance-r37.md` (cites S279–S282, S286, S287): discharges the portability caveat for this host via `asm-generic/errno-base.h` and local glibc headers (Arch Linux x86_64 defines `EACCES 13`); identifies that the historical 8 `errno:13` matches in `snapper-eacces-mechanism.md` have aged out of the retained journal (0 matches on 2026-10-24/25) while the `/` 555 root mode mechanism remains active.

---

## 2. Assessment against Tsukuroi PROVINCE, Coverage Map, and Sibling Boundaries

1. **Tsukuroi PROVINCE:**
   - `PROVINCE.md:3-15`: Owns host operability and system repair (package state, systemd units/timers, journal/boot triage, update safety).
   - `PROVINCE.md:25-28`: Refuses binary reverse engineering of drivers/shipped artifacts (`→ kaidoku/revenger`).
   - `PROVINCE.md:156-176`: Owns storage integrity and rollback net triage.
   - Sibling boundary check: Sibling provinces (`kama`, `kagi`, `mado`, `mori`, `kumitate`, `kaidoku`, `revenger`, `tameshi`) claim no ownership of errno semantics. Mori owns cgroup memory events, kill/OOM catalog-ID records, and fleet attribution (ADJ-04), but tsukuroi retains OS journal and boot diagnosis. Tracking return values from open-source kernel headers (`errno-base.h`) and manual pages is OS triage documentation, not binary reverse engineering. The theme sits firmly within Tsukuroi Core.

2. **Coverage Map (`corpus/README.md`) & Existing Corpus:**
   - `corpus/knowledge/snapper-eacces-mechanism.md`: records the standing `errno:13` observation (`/` 555 root:root, `limine-snapper-sync.service` bounding set `CAP_SYS_ADMIN`), and provides an operator falsifier.
   - `corpus/knowledge/root-dac-decision-r12.md` & `root-dac-correction-r13.json`: explicitly established that the `mkdir(2)` EROFS mapping (S035) was API-scoped for mkdir and not proof of Btrfs ioctl behavior or historical cause (`"api_scope": "The B2/EROFS mapping is API-scoped (mkdir(2) EROFS, S035); it is not proof of the Btrfs subvolume ioctl behavior..."`).

---

## 3. Precise Issues Identified in Staged Entries

1. **Substantive Kernel Contradiction in Entry 2 (`mount-errno-contract-r26.md`):**
   - Staged text asserts: *"and the ioctls that change the filesystem require `CAP_SYS_ADMIN` and return `EPERM` without it"*, pairing `EPERM` with missing `CAP_SYS_ADMIN` for subvolume creation and snapshots.
   - **Ground truth:** Upstream `fs/btrfs/ioctl.c` (kernel v7.2, lines 1138–1186, opened this round) contains no `capable(CAP_SYS_ADMIN)` check in `__btrfs_ioctl_snap_create` for subvolume creation. For snapshots, it checks `inode_owner_or_capable(idmap, src_inode)`, requiring caller ownership of the source subvolume (`"Subvolume creation is not restricted, but snapshots are limited to own subvolumes only"`).
   - **Contradiction with held corpus:** The lane already established in `root-dac-decision-r12.md` and `root-dac-correction-r13.json` that subvolume creation has no capability gate in the kernel. Admitting Entry 2 as written would introduce a direct knowledge regression.

2. **Inter-Entry Supersession / Competing Taxonomy (Entry 1 vs Entry 2):**
   - Entry 1 introduces a 6-class table; Entry 2 introduces a 12-class table explicitly labeled *"The discriminating table this replaces"*. Without explicit append-only supersession metadata, admitting both creates competing classifications within the corpus.

3. **Carrier Failure of S205 vs Live S279–S281:**
   - S205 (`https://man.archlinux.org/man/errno.3`) fails with `ECONNRESET` during round 37. In contrast, S279–S281 (`https://man7.org/linux/man-pages/man3/errno.3.html`) is live, reachable, and verified.

4. **Silent Recheck Vacuity / Moving Journal Window in Entry 3:**
   - Entry 3 discovers that the 8 recorded `errno:13` matches in `snapper-eacces-mechanism.md` have aged out of the journal (confirmed live on host: `journalctl` query returns 0 matches, exit 1), while the structural fault (`/` 555, bounding set `CAP_SYS_ADMIN`) remains active.
   - The official recheck procedure in `snapper-eacces-mechanism.md:3` currently returns 0, creating a risk of false-resolution reporting if not accompanied by a retention-aware erratum.

---

## 4. Proposed Move (Connector Synthesis)

**Conditioned Two-Stage Integration of the Errno Assimilation Package:**

1. **Scope and Correct Entry 2 Before Admission:**
   - Amend `mount-errno-contract-r26.md` to restrict the `CAP_SYS_ADMIN` → `EPERM` claim to `mount(2)` (S214) and general filesystem-modifying ioctls (e.g. FITRIM/resize), while attributing snapshot `EPERM` strictly to source-inode ownership via `inode_owner_or_capable` (S220).
   - Mark Entry 1 as the general C library/POSIX baseline and Entry 2 as the operative syscall/ioctl supersession in the note metadata.
2. **Re-ground S205 to Verified Carriers:**
   - Use the live, verified `man7.org` carrier (S279) and kernel ABI header `include/uapi/asm-generic/errno-base.h` (S282 / local S286) to discharge S205's unstable `man.archlinux.org` carrier.
3. **Bind Entry 3 to `snapper-eacces-mechanism.md` as an Operational Recheck Erratum:**
   - Append an erratum to `snapper-eacces-mechanism.md` citing S287 / Entry 3, recording that the journal retention window closed (0 matches on 2026-10-24/25), and distinguishing between *evidence window closure* and *mechanism resolution*.

### Axes Affected:
- **Adjacency:** Preserves clean boundaries; prevents false claims about kernel capability gates from bleeding into sibling RE / system triage scopes.
- **Frontier:errno:** Strengthens the domain by providing a reconciled, non-contradictory 12-class taxonomy and eliminating silent recheck vacuity.
- **Calibration & Freshness:** Corrects false-negative recheck reporting on the live host substrate.
- **Harms none:** Purely bounds and reconciles existing staged entries and S-rows without expanding claim slots or modifying outside repos.

---

## 5. Verification Surfaces

1. **Kernel ABI & Source Inspection:**
   - `fs/btrfs/ioctl.c:1183-1186`: confirms `inode_owner_or_capable` gates snapshots, not `CAP_SYS_ADMIN`.
   - `/usr/include/asm-generic/errno-base.h:17`: confirms `#define EACCES 13 /* Permission denied */`.
2. **Live Host Substrate Checks (Read-Only):**
   - `stat -c '%a %U:%G' /` outputs `555 root:root`.
   - `systemctl cat limine-snapper-sync.service | grep CapabilityBoundingSet` outputs `CapabilityBoundingSet=CAP_SYS_ADMIN`.
   - `journalctl --no-pager -o short-iso -g 'create subvolume failed' | grep -c 'errno:13'` returns `0` (exit 1), verifying Entry 3's aging-out observation.
3. **Integrity Gates:**
   - Re-running `python3 tools/check-self-assessment.py` and `bash tools/tsukuroi-census.sh --selftest` ensures zero regression on unchanged lane files.

---

## 6. Sources Opened This Round (2026-10-25)

1. `https://man7.org/linux/man-pages/man3/errno.3.html`
   - Opened: 2026-10-25.
   - Located quote (19 words): *"The error numbers that correspond to each symbolic name vary across UNIX systems, and even across different architectures on Linux."*
2. `https://raw.githubusercontent.com/torvalds/linux/v7.2/include/uapi/asm-generic/errno-base.h`
   - Opened: 2026-10-25.
   - Located quote (6 words): *"#define EACCES 13 /* Permission denied */"*
3. `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/btrfs-subvolume.rst`
   - Opened: 2026-10-25.
   - Located quote (19 words): *"The default subvolume ... cannot be deleted and returns error (EPERM) and this is logged to the system log."*
4. `https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/ioctl.c`
   - Opened: 2026-10-25.
   - Located quote (13 words): *"Subvolume creation is not restricted, but snapshots are limited to own subvolumes only"*
5. `https://man7.org/linux/man-pages/man2/mount.2.html`
   - Opened: 2026-10-25.
   - Located quote (15 words): *"Some filesystems instead return the error EROFS on an attempt to mount a read-only filesystem."*
