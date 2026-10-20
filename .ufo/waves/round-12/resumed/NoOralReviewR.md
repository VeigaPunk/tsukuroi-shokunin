# NoOralReviewR — round-12 resumed static review (no executed E2E)

Seat: NoOralReview (reviewer, leaf, resumed wave). Scope: written root-mechanism instructions (RULES, PROVINCE, QUALITY, spec/dispatch seat text, SKILL/corpus notes) plus the Matrix seat's new `corpus/knowledge/root-dac-decision-r12.{md,json}`. Static review. Nothing below is an executed end-to-end result; no PASS is asserted for any seat.
Baseline: HEAD `b76b5c377eaee3e3d8d47fdddde977828d05dbd5`. Working tree at review time: `corpus/QUALITY.md`, `corpus/SOURCES.md`, `SKILL.md`, `tools/tsukuroi-census.sh` modified (in-flight Census/Sources edits, not reviewed here); matrix and lesson present as untracked.
Capture date: 2026-10-20 (UTC). The inherited `.ufo/waves/round-12/NoOralReview.md` (not `resumed/`) is historical; it was read, not edited.

Install/update log: none. No package, tool or unit was installed, upgraded, removed or started. No `sudo` (including `sudo -n`), no `systemd-run`, no census or selftest run, no pacman verify, no host write. Scratch downloads went to `/tmp/r12-noral/` (deleted after this file was written).

## 1. Inherited artifact disposition (reuse / reject / correct)

Inherited `NoOralReview.md` was written when the matrix was absent (its matrix checks were "deferred"). Its findings are re-checked against present source state below. Nothing in the inherited file is rewritten.

| Inherited ID | Inherited claim | Present state (2026-10-20) | Disposition |
|---|---|---|---|
| F1 | Contract / RULES / PROVINCE conflict on sudo and package ops | Still true: `RULES.md:3-9` permits installs and says passwordless sudo is available; `PROVINCE.md:27-28` says "Never installs, upgrades, or removes packages"; spec contract forbids package ops and sudo. No precedence rule written. | **Still open**. Sub-point refined: sudo availability was measured historically (`corpus/knowledge/degraded-triage-r4.md:31-32`, `sudo -n true` rc=0 on 2026-10-14). That is dated history; not re-run here. |
| F2 | Only capability discriminator is privileged; read-only substitute is configuration, not runtime | Matrix B3 uses `systemctl show` config only and states the limit (`root-dac-decision-r12.json` B3 `limit`). Snapper falsifier still `sudo`. | **Partly corrected** (matrix states config-vs-runtime limit). Still open for the snapper note (see H3). |
| F3 | access(2) cited for `test -w`; S028 "effective/permitted" extension unverified | (a) S028 extension is now **verified**: systemd.exec(5) CapabilityBoundingSet text reads "Note that this option also affects the respective capabilities in the effective, permitted and inheritable capability sets" (fetched 2026-10-20). (b) The snapper note still asserts access(2) explains `test -w` (`snapper-eacces-mechanism.md:30`); the matrix §5 corrects this. (c) coreutils `test.c:380-388` calls `euidaccess()`; the gnulib `euidaccess-stat.c` source could not be fetched (GitHub raw 404 on `main` and `master`). | **Corrected for S028; still open for the test-w link** (M1). |
| F4 | Census C1 flips live verdict; "worsen verdict" premise is unproven intent | Spec text unchanged (`spec.json` Census item: "worsen verdict for missing owner write/search as named DEGRADED"). Census edits are in the working tree, unreviewed here. Tension with QUALITY #15 (see M5). | **Still open** (M5). |
| F5 | Unresolved refs (provenance trio, ART K2/K3/K4, S030 path, mkdir(2) ID, update-safety gate, README sweep, census override list, stale S034 text) | See §5 register. mkdir(2) now S035 (resolved). ART ledger still absent. S030 path still absent. | **Mostly still open**; mkdir(2) resolved. |
| F6 | Snapper note uses `systemctl cat \| grep` for a negative ProtectSystem claim | Unchanged: `snapper-eacces-mechanism.md:3,10` and its `recheck:` line still use `systemctl cat … \| grep`. Effective value is `ProtectSystem=no` (my `systemctl show`, rc=0). Matrix uses `systemctl show`. | **Still open** (owner: snapper note). |
| F7 | README states `[inf]` mechanism as fact | `corpus/README.md` row now reads "candidate mechanism … [inf, operator falsifier given]". | **Corrected**. |
| F8 | `/boot` FAT capacity scope creep in snapper note | Still present (`snapper-eacces-mechanism.md` `/boot` bullet and Operator options). | **Still open**, LOW. |
| F9 | Matrix existing-layout branch must not use `btrfs subvolume list` as non-root | Matrix does not use it (grep: no hit in `root-dac-decision-r12.*`). Historical `degraded-triage-r4.md` still lists it (with an erratum per the inherited note; not re-read here). | **Corrected in matrix**. |
| F10 | Checked-and-OK items | Re-checked: lesson anchors resolve; sibling PROVINCE refs exist (`ls`/`[ -e ]`); census early-return anchors not re-read (census under edit). | **Reused**, with census anchors now stale because the census file is modified. |

Inherited "Matrix absent" status is **superseded**: the matrix and its JSON now exist and are reviewed in §6.

## 2. Read-only probes run this review (command → rc → observed)

All run as uid 1000 (`vgpnk`), non-privileged. Values reproduce the matrix's 2026-10-19 host observation except where noted.

| Command | rc | Observed |
|---|---|---|
| `stat -c 'mode=%a owner=%U:%G type=%F path=%n birth=%w' /` | 0 | `mode=555 owner=root:root type=directory path=/ birth=2026-10-03 17:41:30` |
| `getfacl -p /` | 0 | base entries only: `user::r-x`, `group::r-x`, `other::r-x` |
| `findmnt -n -o TARGET,FSTYPE,OPTIONS /` | 0 | `/ btrfs rw,relatime,compress=zstd:3,ssd,space_cache=v2,subvolid=256,subvol=/@` |
| `systemctl show limine-snapper-sync.service -p User -p Group -p CapabilityBoundingSet -p AmbientCapabilities -p ProtectSystem -p ProtectHome -p ReadOnlyPaths -p ReadWritePaths -p NoNewPrivileges -p ActiveState -p UnitFileState` | 0 | `User=root`, `Group=`, `CapabilityBoundingSet=cap_sys_admin`, `AmbientCapabilities=`, `ProtectSystem=no`, `ProtectHome=yes`, `ReadOnlyPaths=`, `ReadWritePaths=/tmp`, `NoNewPrivileges=yes`, `ActiveState=inactive`, `UnitFileState=enabled` |
| `stat -c '%F %a %n' /.snapshots` | 1 | `No such file or directory` |
| `snapper list-configs` | 0 | header only, 0 configured rows |
| `journalctl --no-pager -o short-iso -g 'create subvolume failed' \| grep -c 'errno:13'` | 0 | `9` (matrix states 9, first 2026-10-16T12:47:26-03:00, last 2026-10-19T22:48:24-03:00; the older snapper note states 8 at an earlier capture, a dated drift, not a contradiction) |
| `cat /sys/module/apparmor/parameters/enabled` | 0 | `N` |
| `ls -d /sys/fs/selinux` | 2 | absent |
| `[ -e …/.tower/worktrees/kaika/fleet-ledger/.ufo/waves/kaika-w1/tsukuroi-art.md ]` | 1 | ART ledger absent |
| `ls README.md` (repo root) | 2 | absent; `corpus/README.md` exists |
| `command -v` for stat, getfacl, findmnt, systemctl, systemd-analyze, journalctl, snapper, lsattr, namei, getcap, capsh, getpcaps, jq, btrfs, test, sudo, systemd-run | 0 | all present (`bun` not checked: not referenced by any instruction in scope) |
| `pacman -Qo` on getfacl, snapper, lsattr, findmnt, test, sudo, systemd-run, getcap | 0 | acl 2.4.0-1; snapper 0.13.1-3; e2fsprogs 1.47.4-1; util-linux 2.42.3-1; coreutils 9.11-2; sudo 1.9.17.p2-6; systemd 261.2-1; libcap 2.78-1 |
| `uname -r` | 0 | `7.2.3-arch1-3` |
| `git status --short` | 0 | `corpus/QUALITY.md`, `corpus/SOURCES.md`, `SKILL.md`, `tools/tsukuroi-census.sh` modified; matrix, lesson, `.ufo/waves/round-12/` untracked |

Host-side negative claims carry their sweep above (QUALITY #9). Writes performed on the host: none.

## 3. Tool inventory against the written instructions

- No command named in the matrix recheck line or in the snapper note is missing on this host. Every discriminator in the matrix's `recheck:` is non-privileged and present.
- **Missing tools blocking a read-only step: none.** No install was required and none was performed.
- Missing-capability gap is a privilege/runtime gap, not a tool gap: the running-process capability state (`/proc/<pid>/status` CapBnd/CapEff) has no PID while `limine-snapper-sync.service` is inactive. The matrix states this limit.
- `pacman-contrib` (`checkupdates`) is absent per the inherited census notes; no written instruction in this review's scope requires it.

## 4. Sudo and privilege assumptions

| # | Where | Assumption | Status |
|---|---|---|---|
| S-a | `RULES.md:3-4` | Passwordless `sudo` available to every agent | Asserted by operator. Historical measurement only (`degraded-triage-r4.md:31-32`, rc=0, 2026-10-14). Not re-run (contract). |
| S-b | `RULES.md:7-9` vs `PROVINCE.md:27-28` vs spec Contract | Installs permitted vs forbidden | Conflict; see H1. |
| S-c | `snapper-eacces-mechanism.md:23-27` | Falsifier `sudo systemd-run --wait --pipe -p CapabilityBoundingSet=CAP_SYS_ADMIN test -w /` and `sudo test -w /` | Operator-only, not run. Labeled "non-mutating"; see H3. |
| S-d | `snapper-eacces-mechanism.md:34-35` | Operator options `chmod 755 /` and `snapper -c root create-config /` | Operator-only, not run. Mutating, no ordering rule that diagnosis precedes mutation; see M4. |
| S-e | `degraded-triage-r4.md:86-92, 102-103, 235, 316-332` | `sudo pacman -Qkk`, `sudo dkms remove …`, `sudo snapper -c root create-config /`, and `sudo btrfs subvolume create /.snapshots` ("discriminating test") | Historical r4 text, not current instruction. The last item is a **mutating** proposal labelled as a discriminator; it contradicts the matrix's "every discriminator read-only" rule. Recorded, not re-opened. |

## 5. Findings (severity order)

### HIGH

**H1 — Contradictory authority on installs and package operations (still open).**
- Evidence: `/home/vgpnk/.omp/agent/RULES.md:3-9` (any agent may install/upgrade with full privilege; passwordless sudo available); `tsukuroi-shokunin/PROVINCE.md:27-28` ("Never installs, upgrades, or removes packages"); `spec.json` Census/Matrix/Sources contract text ("NO sudo/host mutation, package operations" and "Prefer no installs").
- Risk: a seat that reads RULES first can justify `sudo pacman -S` while the lane contract and PROVINCE forbid it. No precedence rule is written in any file in scope.
- Recommendation for the parent: state one rule for round-12 (no installs; RULES' directive does not override the lane contract or PROVINCE for this wave) and record it in the integration note.

**H2 — The matrix's decision ordering and B4 limit are contradicted by primary kernel source for the subvolume-create path (new; depth-relevant; host verdict unaffected).**
- The matrix's `decision_procedure` (`root-dac-decision-r12.json`) runs step 1 "present → B4/EEXIST" before step 2 "ro mount → B2/EROFS", and B4's `limit` says an observed errno:13 "does not establish that the target was absent for that ioctl." Both rest on the ordinary-mkdir smoke (`error-order-smoke.json`), which the matrix itself says must not be extrapolated to the Btrfs ioctl.
- The ioctl the snapshot tool reaches is traced in the sources I fetched (upstream tag `v7.2`; the host runs `7.2.3-arch1-3`, and tag `v7.2.3` returned 404, so the Arch build is not byte-verified against upstream):
  - `libbtrfsutil/subvolume.c:742-773` (kdave/btrfs-progs `master`, mutable): `btrfs_util_create_subvolume_fd` → `ioctl(parent_fd, BTRFS_IOC_SUBVOL_CREATE_V2, &args)`.
  - `fs/btrfs/ioctl.c` v7.2:1138-1170: `__btrfs_ioctl_snap_create` runs `mnt_want_write_file(file)` at line 1150 **before** any existence check, then calls `btrfs_mksubvol` at line 1166.
  - `fs/btrfs/ioctl.c` v7.2:859-875: `btrfs_mksubvol` calls `may_create_dentry(idmap, dir, dentry)` at line 875.
  - `fs/namei.c` v7.2:3731-3742: `may_create_dentry` returns `-EEXIST` if the child is positive (3735-3736), `-ENOENT` on a dead dir, `-EOVERFLOW` without mapping, and only then `inode_permission(dir, MAY_WRITE|MAY_EXEC)` (3742).
  - `fs/namei.c` v7.2:533-542: `generic_permission` for directories grants when `capable_wrt_inode_uidgid(…, CAP_DAC_OVERRIDE)` holds (the B3 conjunct is source-grounded here, not only via S027 prose).
  - No `CAP_SYS_ADMIN` check appears on the subvolume-create path between 1138 and the mksubvol call (grep of v7.2 `ioctl.c` for `capable(` in that range returns none).
- Consequences:
  1. On a **read-only** mount, the subvolume create returns EROFS before EEXIST or EACCES. The matrix's step order (EEXIST first) is wrong for this operation class. The matrix's EROFS "no-extrapolation" caveat is correct in spirit, but the matrix does not record the opposite ordering.
  2. On a **rw** mount, `may_create_dentry` checks positive-dentry (EEXIST) before the DAC check. So an EACCES from the subvolume ioctl is evidence that the name was not a positive dentry at that check. The matrix's B4 limit ("does not establish that the target was absent") is therefore too strong for this path, with one caveat: `start_creating_killable` performs a lookup which may return EACCES on a search denial (B1 search variant). I did not read that lookup path; this caveat is [inf].
  3. The matrix §5 "Btrfs ioctl check order unestablished" is now partly established by the sources above (for upstream v7.2, not the Arch build).
- Host verdict: unchanged. The host mount is `rw` (measured above), so the logged EACCES class is still "consistent, not proven" under the matrix's own limits. The change is to the procedure and the B4 limit only.
- Recommendation for the Matrix seat (owner of its file; append-only correction preferred): split decision steps by operation class (mkdir vs subvolume ioctl); put mount-RO (EROFS) before EEXIST for the subvolume class; reword the B4 limit per items 2-3 above; cite the four source locations and their tag/commit. Sources seat to register the URLs as S### rows with a pinned commit (QUALITY #7); `master` for libbtrfsutil is mutable and should be pinned.

**H3 — The snapper falsifier is labelled "non-mutating" but runs a privileged transient root service, and it does not reproduce the unit (new wording/limit defect).**
- Evidence: `snapper-eacces-mechanism.md:23` ("Operator-only, non-mutating discriminator") with `sudo systemd-run --wait --pipe -p CapabilityBoundingSet=CAP_SYS_ADMIN test -w /` (line 26).
- `systemd-run` creates and starts a transient unit under root; it is not a read-only probe, although it leaves no persistent state. The `-p` set does not apply the real unit's `NoNewPrivileges=yes`, `ProtectHome=yes` or `ReadWritePaths=/tmp`, so the predicted rc (1) tests a different process envelope than the unit.
- The matrix already moved away from this (it is config-only and runs no privileged probe). The snapper note should say "operator-only, starts a transient root process; not the unit's full sandbox" and should not be cited as a read-only discriminator.
- Owner: snapper note (not in this seat's write scope). Flagged, not edited.

### MEDIUM

**M1 — `test -w` link to access(2) remains unverified (F3 residual).** `snapper-eacces-mechanism.md:30` attributes the `test -w` comparison to access(2)'s permitted-set rule. coreutils `test.c:380-388` calls `euidaccess()`; the gnulib `euidaccess-stat.c` implementation (which determines whether AT_EACCESS/effective IDs are used) could not be fetched (GitHub raw 404 on two branch names). Until read, the link is [inf] and QUALITY #12 requires the source read before the mechanism is tagged. The matrix §5 already says "must be established per binary."

**M2 — The matrix's own `recheck:` line is non-verifying for the existing-layout branch.** The matrix recheck command includes `journalctl … | grep -c 'errno:13'` (fine) but no command that measures the subvolume ro property (see M6). Only the mount options are probed.

**M3 — Unresolved external/internal refs (see §7 register).** ART K2/K3/K4 point to an absent ledger; S030 cites an absent path (`SOURCES.md:36`, rejected row kept per QUALITY #5, but the dead path remains in the registry).

**M4 — Operator options in the snapper note recommend host mutations without a prior-diagnosis ordering (`snapper-eacces-mechanism.md:34-35`).** `chmod 755 /` is proposed for an unowned root directory whose intent the same note calls unknown ("An operator may determine why `/` is `0555`"). The note also proposes `snapper -c root create-config /`, which creates a subvolume. Both are labelled "reported, never performed," which is acceptable under PROVINCE, but the note does not order them after the mode-intent check. Recommend: state the discriminating read first and make the mode-intent answer a precondition.

**M5 — QUALITY #15 versus the census spec's DEGRADED verdict (F4 residual).** QUALITY #15 (`corpus/QUALITY.md:20`): "Root metadata findings report owner-write/search bits, not universal mode policy or process writability." The Census spec (`spec.json` Census item) requires "worsen verdict for missing owner write/search as named DEGRADED." Naming a verdict DEGRADED on an owner-write bit is a policy judgment, which QUALITY #15 disclaims. The live verdict on this host will change once the Census edit lands (predicted from text only; no census run was made). Resolve by stating the rule explicitly in the census note, or by reporting the bit as a named observation without a verdict. Owner: Census/integrator.

**M6 — Mount-RO exclusion ignores the btrfs subvolume read-only property (new; depth gap).** The matrix's B2 and the host EROFS exclusion rest on `findmnt` options and `ProtectSystem`/`ReadOnlyPaths` only. A btrfs subvolume can carry a read-only property independent of mount options [inf: `btrfs-property(8)` not opened in this review]. The matrix's host walk marks "no B2 signal" from mount options alone. The logged EACCES argues against a ro subvolume for the logged incidents, but no dated probe exists. Unrun discriminator (read-only): `btrfs property get -t subvol / ro` (not executed; source/man-page check pending). Owner: Matrix (append-only).

### LOW

**L1 — ART ledger and S030 path absent.** Evidence: `[ -e ]` rc=1 for `.tower/worktrees/kaika/fleet-ledger/.ufo/waves/kaika-w1/tsukuroi-art.md` (see §7).

**L2 — Snapper note F8 scope creep.** `/boot` FAT capacity (2.0G vs ≥4 GiB) appears in the mechanism note (`snapper-eacces-mechanism.md` Current host evidence and Operator options). Out of the EACCES mechanism; move or drop.

**L3 — Stale negative claim wording.** `snapper-eacces-mechanism.md:3` ("no matching `ProtectSystem` … lines") measures the unit file, not the effective property. Effective is `ProtectSystem=no`. Correct to the `systemctl show` value (F6).

**L4 — QUALITY #10 sweep scope.** Requires sweeping `README.md`; the repo has no root `README.md`, only `corpus/README.md`. State the referent.

**L5 — Gate ambiguity for RULES' "update-safety gate."** RULES says full-system upgrades "go through tsukuroi-shokunin's update-safety gate first." The gate is a note: `corpus/knowledge/update-safety-note.md` (go/no-go decision table, `corpus/README.md:10`). Three versions exist (`update-safety-note.md`, `-v2.md`, `-v3.md`); no file in scope names which is current. No tool performs an upgrade gate; the census plane is a read-only verdict.

**L6 — Historical r4 text proposes a mutating "discriminator."** `degraded-triage-r4.md:331` (`sudo btrfs subvolume create /.snapshots` as a discriminating test). Historical; the matrix does not repeat it. Recorded so no later seat cites it as read-only.

**L7 — Matrix B1 limit wording on RO mounts.** B1 says the same mode "on a rw mount … yields EACCES, never EROFS." That is correct for rw but, per H2, the EROFS-first ordering applies to the subvolume path on a ro mount; the limit should name the mount state explicitly.

### Checked and OK (not findings)

- Quotes in the matrix's S027, S028 (CapabilityBoundingSet effective/permitted/inheritable; ProtectSystem=strict; ProtectHome; ReadWritePaths superblock limit), S034 (root uses permitted set; "A file is accessible only if … search"), and S035 (EACCES, EROFS, EEXIST) match the fetched man pages (2026-10-20). S027 "Bypass file read, write, and execute permission checks" matches.
- Smoke fixtures match the matrix's SC1–SC3 and R10 (`discriminator-smoke.json` fixture_results: 0555 new → EACCES, 0755 → created, 0755 existing → EEXIST; `error-order-smoke.json`: 0555 new → EACCES, 0555 existing → EEXIST). Both are author-side, uid 1000, disposable directories; not independent verification.
- Host shape in §3 of the matrix matches §2 probes above (555 root:root; rw; User=root; CapBnd cap_sys_admin; ProtectSystem=no; /.snapshots absent; 0 snapper rows; AppArmor N; no SELinux path; journal 9).
- QUALITY #14 is satisfied in the matrix (`## 7. QUALITY check` present). QUALITY #13 is satisfied (mode/owner/ACL and unit CapBnd/ProtectSystem recorded).

## 6. Matrix-specific checks (`root-dac-decision-r12.{md,json}`)

- Branch count: 4 (B1 EACCES parent DAC; B2 EROFS ro mount/namespace; B3 cap-bound root/sandbox; B4 EEXIST target present). Meets "≥4 grounded branches" on count. Each branch has `source_ids`; each discriminator is a read-only command list with `read_only: true` and an expected signal.
- Scenarios: 8 (SC1–SC8) with expected classifications; SC4 and SC5 are explicitly "not host-demonstrated." SC8 (UNCLASSIFIED) is a first-class outcome as required.
- Independence from C1: the matrix reads no census script or census output (its `independence` field and §1 say so). I found no census reference in the matrix. Confirmed by grep.
- Ordering and limit claims: see H2 (procedure order for subvolume path; B4 limit).
- Missing branch (depth): a subvolume read-only property branch (M6).
- Sudo: none required; `recheck:` contains no sudo or systemd-run.
- Pacman advice: none; no bare `pacman -Sy` mentioned (QUALITY #6).

## 7. Unresolved references register

| Ref | Where | Target | State |
|---|---|---|---|
| "provenance trio" | `spec.json` Matrix item and `dispatch.json` | Undefined in any instruction file; the matrix header uses `source:`, `verified-at:`, `recheck:` (QUALITY #8) | Resolved by convention; **not defined** in QUALITY. Open, LOW. |
| ART K2 | `snapper-eacces-mechanism.md:34` | ART ledger (absent) | **Unresolved**. |
| ART K3 | `lessons/round-1.md:71` | ART ledger (absent) | **Unresolved**. |
| ART K4 | `arch-news-gate-2026.md:44` | ART ledger (absent) | **Unresolved**. |
| S030 path | `SOURCES.md:36` | `.tower/…/tsukuroi-art.md` (absent) | **Dead path** in a rejected row (kept per QUALITY #5). Open. |
| mkdir(2) ID | Matrix spec | S035 | **Resolved** (`SOURCES.md:41`). |
| "update-safety gate" | `RULES.md:10-13` | `update-safety-note.md` (go/no-go table); three versions | **Ambiguous version**. Open, LOW. |
| QUALITY #10 README | `corpus/QUALITY.md:14` | no root README.md | **Ambiguous referent**. Open, LOW. |
| Census override list | `tools/tsukuroi-census.sh` header | `TSUKUROI_ROOT_DIR` now present in the working tree (lines 311, 350) | **Not verified** this pass; census file is modified and in flight. |
| Snapper `systemctl cat` negative claim | `snapper-eacces-mechanism.md:3,10` | effective `ProtectSystem=no` | **Open** (F6). |
| `test -w` ↔ access(2) | `snapper-eacces-mechanism.md:30` | coreutils `test` → `euidaccess` → gnulib | **Open** (M1). |
| Subvolume ioctl order | Matrix §5 | fs/btrfs/ioctl.c v7.2:1150, 1166, 875; fs/namei.c v7.2:3735-3742 | **Partly resolved by source** (H2). Matrix correction pending. |
| Subvolume ro property | Matrix B2 | btrfs-property(8) | **Unresolved** (M6). |
| Kernel tag | host `7.2.3-arch1-3` | upstream `v7.2.3` tag returned 404; `v7.2` used | **Caveat** (H2). |

## 8. Residual risk and verification gaps

- No E2E execution, no census or selftest run, no unit run, no privileged probe. All findings are static or read-only probes above.
- The kernel-source chain (H2) is upstream `v7.2` and `master` (libbtrfsutil), fetched 2026-10-20; the host kernel is `7.2.3-arch1-3`. The mapping to the Arch build is [inf] until the Arch source is checked or a tag matching 7.2.3 is read.
- `test -w` implementation (M1) is unverified; gnulib source not obtained.
- Runtime capabilities of the unit are unobservable while it is inactive (F2 residual; matrix states it).
- `sudo` availability is historical (degraded-triage-r4, 2026-10-14) and not re-verified (contract).
- Census C1 is in flight in the working tree; its verdict behavior and header override list were not reviewed here (M5, register row).
- Author-side smoke fixtures are not independent verification; no non-author verifier is claimed.

## 9. Verification scope (what this file does NOT claim)

- No PASS is asserted for any seat, the matrix, the census, or the snapper note.
- Operability and depth are reported as the evidence above, not as scores.
- Inherited evidence (`.ufo/waves/round-12/NoOralReview.md`, matrix smoke JSON, degraded-triage-r4) was read and cross-checked, not rewritten.
