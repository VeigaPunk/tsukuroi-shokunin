# Frontier5Errno529 — Connector Report: Errno-Discrimination Theme and Staged Entries

## 1. Evidence

### Staged Package and Source Inspection
Inspected the three staged knowledge entries and their associated sources staged under `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/`:
1. `errno-name-discrimination-r25.md` (cites S205 `errno(3)` and S204 `btrfs-subvolume(8)`): Establishes the distinction between bare error numbers and symbolic names; differentiates DAC permission denial (`EACCES`) from capability/mount-option requirements on subvolume deletion (`EPERM`).
2. `mount-errno-contract-r26.md` (cites S214 `mount(2)` and S220 `fs/btrfs/ioctl.c`): Formulates a closed 12-class errno table directly derived from kernel syscall contracts and filesystem ioctl handlers (`EXDEV`, `EPERM`, `EINVAL`, `EEXIST`, `ENOENT`, `ETXTBSY`, `EOPNOTSUPP`).
3. `errno-contract-variance-r37.md` (cites S279–S281 `errno(3)`, S282 `asm-generic/errno-base.h`, S286 host header capture, S287 lane recheck probe): Examines upstream contract variance, confirms host ABI binding on Arch Linux x86_64, and records that the standing journal matches for `errno:13` have aged out of retention (0 matches across 6 retained boots) while host mechanism bits (`/` mode 0555 root:root, `CapabilityBoundingSet=CAP_SYS_ADMIN`) remain unchanged.

### Re-opened Staged Sources (accessed 2026-10-25)
Four external sources were opened and verified this round:
1. `https://raw.githubusercontent.com/torvalds/linux/v7.2/include/uapi/asm-generic/errno-base.h` (accessed 2026-10-25):
   - Anchor: line 19
   - Quote: `#define	EACCES		13	/* Permission denied */`
2. `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/btrfs-subvolume.rst` (accessed 2026-10-25):
   - Anchor: lines 104–106
   - Quote: `The default subvolume ... cannot be deleted and returns error (EPERM) and this is logged to the system log.`
3. `https://man7.org/linux/man-pages/man3/errno.3.html` (accessed 2026-10-25):
   - Anchor: `DESCRIPTION` §Error numbers and names, paragraph 3 (Linux man-pages 6.19, 2026-05-28)
   - Quote: `The error numbers that correspond to each symbolic name vary across UNIX systems, and even across different architectures on Linux.`
4. `https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/ioctl.c` (accessed 2026-10-25):
   - Anchor: lines 1183–1186 (`__btrfs_ioctl_snap_create`)
   - Quote: `Subvolume creation is not restricted, but snapshots are limited to own subvolumes only`

### Alignment with Tsukuroi PROVINCE, Corpus, and Sibling Boundaries
- **Tsukuroi PROVINCE:** Lines 8–14 own read-only host substrate, systemd units, journal/boot triage, and recovery net (`snapper-eacces-mechanism.md`). Lines 25–28 refuse binary reverse engineering (kaidoku/revenger ADJ-06, OUT-008/009); citing public kernel C source and headers (`ioctl.c`, `errno-base.h`) to verify syscall/ioctl contracts is established corpus practice (e.g. S190–S192) and does not constitute binary RE.
- **Sibling Boundaries (Mori):** ADJ-04 and OUT-005 assign host pressure, OOM catalog-ID events, and cgroup memory correlation to Mori. Filesystem mount error taxonomy and subvolume creation errnos are OS substrate diagnostics belonging strictly to Tsukuroi.
- **Coverage Map & Existing Corpus:** `corpus/README.md:40–41` explicitly tracks the `errno:13` mechanism in `snapper-eacces-mechanism.md` as open frontier debt. Admitting these entries directly resolves the bare-number ambiguity.

### Round Cache & Proposal Synthesis (Frontier4 vs Staged Reality)
- Seat `Frontier4Errno428` proposed rejecting any entry that relies on `mkdir(2)` as a proxy for Btrfs subvolume-create `errno:13`.
- Inspection of the actual staged payloads confirms that `mount-errno-contract-r26.md` directly grounds subvolume creation in `fs/btrfs/ioctl.c` (S220) and `mount(2)` (S214), not `mkdir(2)` (which `errno-name-discrimination-r25.md` cites only as an exit-code analogy, explicitly fenced in §Boundaries).
- However, bounded inspection revealed two real substrate/schema contradictions:
  1. **Source Registry Duplication & URL Splitting:** S205 (`https://man.archlinux.org/man/errno.3`) and S279–S281 (`https://man7.org/linux/man-pages/man3/errno.3.html`) cite the exact same upstream document (`errno(3)`, Linux man-pages 6.19). S205 already carries the significance rule and non-portability caveat in its Teaches cell. Splitting across two distribution URLs creates unneeded registry duplication and bypasses single-URL collision checks.
  2. **External Path Brokenness on Own-Work:** Staged rows S286 and S287 cite file paths under `lanes/tsukuroi/round9/` (e.g. `lanes/tsukuroi/round9/host-errno-capture.txt`), which reside in the external `shokuknow` campaign tree and do not exist within the `tsukuroi-shokunin` repository root.

## 2. Affected Axes
- **adjacency:** Preserves Tsukuroi's OS substrate boundary; ensures kernel source citations remain interface contracts (avoiding binary RE overlap with Kaidoku/Revenger) and keeps failure attribution distinct from Mori's OOM/pressure tracking.
- **frontier:errno:** Replaces ambiguous bare numbers with a 12-class, kernel-verified diagnostic vocabulary; accounts for journal retention aging; eliminates duplicate S-space rows and dead path citations.

## 3. Proposed Move
Synthesize the admission of all three staged entries (`errno-name-discrimination-r25.md`, `mount-errno-contract-r26.md`, `errno-contract-variance-r37.md`) through a bounded three-part integration harmonization:
1. **Consolidate `errno(3)` Sources under S205:** Unify S279 and S280 into the existing S205 row (which already teaches the significance rule and non-portability caveat), retaining S281 as a scoped sub-row or mapped citation for the worked example `errno -s permission`, preventing duplicate manual registrations across `man.archlinux.org` and `man7.org`.
2. **Localize Own-Work Capture Paths:** Before landing S286 and S287, copy or re-capture the host header and probe records into lane-local paths under `.ufo/waves/round-37/assimilation/` (or re-probe `/usr/include/asm-generic/errno-base.h` and `journalctl`), ensuring that `corpus/SOURCES.md` points to verifiable repository artifacts.
3. **Append Retention Aging Notice to `snapper-eacces-mechanism.md`:** Link `errno-contract-variance-r37.md`'s finding to `corpus/knowledge/snapper-eacces-mechanism.md` as an appended dated notice, recording that the 8 historical journal matches have aged out of the retained log (0 matches in 6 boots), preventing operators from reading a zero count as mechanism resolution.

## 4. Risks
- **Schema Validation Drift:** Altering source IDs in the header of `errno-contract-variance-r37.md` could fail `tools/check-knowledge-header.py` if not updated in tandem with `corpus/SOURCES.md`.
- **Misinterpreting Zero Matches:** Operators might assume mode 0555 on `/` was repaired; mitigated by the explicit statement in `errno-contract-variance-r37.md` §4 that the mechanism remains in place.

## 5. Verification
- Run `python3 tools/check-knowledge-header.py --lane tsukuroi-shokunin` across all admitted files to confirm valid `source:`, `verified-at:`, and `recheck:` headers.
- Run `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` to verify row schema (11 columns, no duplicate IDs, valid URLs/paths).
- Validate that all cited capture paths exist locally and that `fs/btrfs/ioctl.c` anchors match kernel v7.2 lines 752–765 and 1177–1186.
