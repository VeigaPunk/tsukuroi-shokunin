# Frontier8Errno832 — errno-discrimination assimilation: source and overlap scan

- Seat: Frontier8Errno832 (revenger, round-37 w1, frontier item 8/8).
- Date: 2026-10-25. Read-only; no writes outside this report. No tool installs (no
  tool change was needed; nothing to record under RULES.md).
- Scope: assess the chosen errno-discrimination theme and its three staged entries
  against Tsukuroi PROVINCE, the coverage map, the existing corpus and sibling
  boundaries; open the staged sources; identify one precise admit/reject/duplicate/
  scope issue or confirm none with a bounded sweep.

## 1. The staged entries (identity)

The round-37 declaration names the theme and the three staged package entries in
`SCORECARD.md` (round-37 declaration block, assimilation §10):

> "Assimilation (§10): ONE theme — errno discrimination — with THREE package entries
> admitted from `merge/tsukuroi/`: `errno-name-discrimination-r25.md`,
> `mount-errno-contract-r26.md`, `errno-contract-variance-r37.md`; rows
> S204/S205/S214/S220/S279–S282/S286/S287 appended …"

Staged source material (shokuknow `lanes/tsukuroi/`):
1. `errno-name-discrimination-r25.md` — S205 `errno(3)` (man.archlinux.org, 6.19,
   2026-05-28) + S204 `btrfs-subvolume.rst` (btrfs-progs v7.1). Six-class failure
   vocabulary (`EACCES/EPERM/EXDEV/EROFS/ESTALE/EBUSY`) and the exit-status parallel.
2. `mount-errno-contract-r26.md` — S214 `mount(2)` (man.archlinux.org, 6.19,
   2026-02-11) + S220 `fs/btrfs/ioctl.c` (kernel v7.2). Syscall-level errno list for
   mount and for btrfs subvolume/snapshot ioctls; twelve-class discriminating table.
3. `errno-contract-variance-r37.md` — S279–S281 `errno(3)` (man7.org, 6.19) +
   S282 `include/uapi/asm-generic/errno-base.h` (kernel v7.2) + S286 own-work host
   header capture + S287 own-work probe capture (2026-10-24). Number-vs-name
   portability; the host binding; "evidence aged out of the retained journal".

## 2. PROVINCE fit

PROVINCE Core owns journal/boot triage and the "Snapper/rollback net" surface
("Diagnose filesystem mode and unit capability restrictions; report
mechanism/falsifier, never attempt restore/config changes"). The errno-discrimination
theme supplies exactly the vocabulary/falsifier vocabulary for the standing
`errno:13` [inf] entry (`snapper-eacces-mechanism.md`) — a Core surface, not a
refused one (no endpoint/secrets/RE surface touched). All three entries are
suitably bounded (each says it does NOT explain the standing observation and does
NOT license cause-inference from an errno).

## 3. Coverage map and existing corpus

- Registry ids: lane `corpus/SOURCES.md` ends at S199 (296 lines, verified); the
  staged block starts at S200 (`assimilation/reg-ids` = S001–S199, `staged-ids` =
  S200–S346). `assimilation/collisions` is empty. No id collision.
- Content overlap: the corpus holds no errno-name/contract note today (round-9
  proposal states this and it verifies: `corpus/knowledge/` has no `errno*`,
  `zh-*` note). S204/S205/S214/S220/S279–S282/S286/S287 are new documents, not
  re-rows. The discriminated classes extend `root-dac-decision-r12.md`'s
  EACCES/EROFS/EEXIST branches rather than duplicating them.
- One held-knowledge conflict is found — see §5.

## 4. Sibling boundaries (bounded sweep)

- `grep -rn -iE 'errno|EACCES|EROFS|EPERM' <root>/*-shokunin/PROVINCE.md`
  (excluding tsukuroi): 0 hits — no sibling claims errno ground in a province.
- Sibling corpora: only audio's C fixtures (errno use in `.c` code) and mori's
  `pid-probe-conclusion-r44.md:22` host probe (`errno=2`), no domain claim. Mori's
  earlier EDQUOT platform-mismatch rejection (Oracle Solaris 49 vs Linux 122, per
  shokuknow AntiPatterns) is consistent with — and reinforced by — the staged
  portability caveat (S279/S282). No boundary conflict; the theme stays inside
  tsukuroi Core.

## 5. Primary finding — precise scope/accuracy issue in staged entry 2

**Issue:** `mount-errno-contract-r26.md` (staged) states:

> "and the ioctls that change the filesystem require `CAP_SYS_ADMIN` and return
> `EPERM` without it"

and its table row pairs `EPERM` with "missing `CAP_SYS_ADMIN` for mount, or
snapshotting a subvolume you do not own" citing S214+S220.

**Evidence (kernel v7.2, opened 2026-10-25):**
- `fs/btrfs/ioctl.c` `__btrfs_ioctl_snap_create` (L1138): NO
  `capable(CAP_SYS_ADMIN)` gate. It returns `-EINVAL` for a `/` name, `-EEXIST`
  for `.`/`..`, `-ENOTDIR` for non-dir; subvol branch → `btrfs_mksubvol` (no
  EPERM); snapshot branch → `-EXDEV` (other FS) then `-EPERM` only from
  `inode_owner_or_capable(idmap, src_inode)` ("Subvolume creation is not
  restricted, but snapshots are limited to own subvolumes only").
- `create_snapshot` (L735): `-EOPNOTSUPP` (extent-tree-v2), `-ETXTBSY` (active
  swapfile). Still no CAP_SYS_ADMIN gate.
- The `capable(CAP_SYS_ADMIN)` → `-EPERM` pattern is real only for *other* ioctls
  in the file (fitrim L449, resize L1002, …), not for the create/snapshot path the
  lane's standing observation uses.

**Conflict with held corpus:** the lane already corrected this exact overclaim:
round-12/13 (`root-dac-decision-r12.md`, wave artifacts `MatrixCritic.md` CX2,
`Capabilities.md`) hold that the kernel has no capability gate for subvolume
creation; the only EPERM in that path is the snapshot-source owner check, which
does not apply to `subvol=true`; CAP_SYS_ADMIN-in-the-bounding-set is a
config signal, and is not "the capability that gates create".

**Verdict:** reject-as-written / require scoped correction before admission.
Smallest correction: keep the CAP_SYS_ADMIN→EPERM sentence for the mount(2) row
(S214) and for the actually-gated ioctls only; attribute the snapshot EPERM to
source-inode ownership (S220); do not let the merged entry contradict
`root-dac-decision-r12.md` residue R12-DAC-EXCLUSIVITY. As staged, entry 2 would
re-introduce a claim the lane rejected two rounds ago, i.e. a knowledge regression,
not an improvement.

## 6. Secondary notes

- Entry 3 paraphrase "numeric values are deliberately omitted" does not match the
  live text; both man7.org and man.archlinux.org read "Therefore, numeric values
  are not included as part of the list of error names below." Re-ground the gate
  quote verbatim (quote-lint safety).
- Staging-corpus traceability: corpus-expansion-2's scout report lists
  `mount-errno-contract-r26.md` as S212/S218, while the canonical round2 proposal
  (and the round-37 declaration) use S214/S220. S212/S218 belong to other entries
  (Pacman zh wiki; SLES zh filesystems). The L1's choice is the correct one;
  record the stale scout-report mapping so a later reader does not cross-wire.
- Nothing else found: admission of S204/S205/S214/S220/S279–S282/S286/S287 is
  otherwise sound; no duplicate, no sibling overlap, no id collision.

## 7. Sources opened this round (all 2026-10-25)

- S205 — https://man.archlinux.org/man/errno.3 — "The value in errno is significant
  only when the return value of the call indicated an error"; "The error numbers
  that correspond to each symbolic name vary across UNIX systems".
- S204 — https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/btrfs-subvolume.rst
  — "returns error (EPERM) and this is logged to the system log"; "user_subvol_rm_allowed".
- S214 — https://man.archlinux.org/man/mount.2 — "Some filesystems instead return
  the error EROFS on an attempt to mount a read-only filesystem"; "Appropriate
  privilege (Linux: the CAP_SYS_ADMIN capability) is required to mount filesystems."
- S220 — https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/ioctl.c
  — "Snapshot src from another FS"; "Subvolume creation is not restricted, but
  snapshots are limited to own subvolumes only"; "cannot snapshot subvolume with
  active swapfile".
- S279 — https://man7.org/linux/man-pages/man3/errno.3.html — "EACCES 13 Permission
  denied"; "The value of errno is never set to zero by any system call or library
  function"; "errno is thread-local".
- S282 — https://raw.githubusercontent.com/torvalds/linux/v7.2/include/uapi/asm-generic/errno-base.h
  — `#define EACCES 13 /* Permission denied */`, `#define EROFS 30 /* Read-only
  file system */`.
- S286/S287 — anchors `lanes/tsukuroi/round9/host-errno-capture.txt` /
  `lane-errno13-probe.txt` exist; contents match entry 3 (EACCES=13/EROFS=30;
  probe 0 matches, 6 retained boots, unit props unchanged).

## 8. Bottom line

Theme fits PROVINCE Core; no duplicate; no sibling overlap; no id collision. One
precise issue found: staged entry 2 overclaims CAP_SYS_ADMIN→EPERM for the btrfs
create/snapshot ioctls (kernel v7.2 shows no such gate; EPERM is the snapshot-source
ownership check), which would contradict the lane's own R12-DAC-EXCLUSIVITY
correction. Admit after that sentence is scoped to S214/gated ioctls; re-ground the
entry-3 "omitted" quote verbatim.
