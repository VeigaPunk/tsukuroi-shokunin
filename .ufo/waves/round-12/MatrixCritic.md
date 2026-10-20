# MatrixCritic — round 12, C2 falsification review (critic seat, author-side)

- Scope: attack the C2 approach (EACCES decision matrix, `corpus/knowledge/root-dac-decision-r12.{md,json}`)
  and the sibling evidence it will draw on. At review time the Matrix artifacts **did not exist**
  (`ls -la corpus/knowledge/ | grep -i 'r12\|root-dac'` → no match). I assessed the baseline contract
  (spec.json `Matrix` prompt), the precedent `corpus/knowledge/snapper-eacces-mechanism.md`, and sibling
  files `C2Review.md`, `Capabilities.md`, `MountErrors.md`, `Issue6629.md`, `UnitLive.md`, `NoOralReview.md`.
- Date 2026-10-19 (host clock -03); HEAD b76b5c3; host kernel `7.2.3-arch1-3`.
- No sudo, no systemd-run, no host writes, no installs, no tests. Scratch source copies lived in
  `/tmp/mc-*` and were deleted at the end of the seat.
- This is author-side critic evidence. It is **not** an independent non-author verification.

## 1. Probes run (read-only, uid 1000)

| # | Command | Exit | Sanitized result |
|---|---|---|---|
| P1 | `findmnt -no FSTYPE,SOURCE,VFS-OPTIONS,FS-OPTIONS /` | 0 | `btrfs`, subvol `/@`; VFS `rw,relatime`; FS options start with `rw` |
| P2 | `stat -c '%a %U:%G ctime=%z mtime=%y' /` | 0 | `555 root:root`, ctime **2026-10-03 17:45:33 -0300** |
| P3 | `getfacl -p /` | 0 | base entries only: `user::r-x group::r-x other::r-x` |
| P4 | `lsattr -d /` | 0 | no attribute flags (no `i`) |
| P5 | `cat /sys/kernel/security/lsm` | 0 | `capability,landlock,lockdown,yama,bpf` |
| P6 | `zgrep CONFIG_BPF_LSM /proc/config.gz`; `ls /sys/fs/bpf` | 0; 2 | `CONFIG_BPF_LSM=y`; bpffs listing **Permission denied** for a non-root user |
| P7 | `systemctl show limine-snapper-sync.service -p …` | 0 | `ActiveState=inactive`, `Result=success`, `ExecMainStatus=0`, `ExecMainPID=1386`, `CapabilityBoundingSet=cap_sys_admin`, `AmbientCapabilities=` (empty), `User=root`, `ProtectSystem=no`, `ProtectHome=yes`, `ProtectKernelModules=yes`, `ReadOnlyPaths=` (empty), `ReadWritePaths=/tmp`, `RootDirectory=`/`RootImage=` (empty), `NoNewPrivileges=yes`, `SystemCallErrorNumber=2147483646`, `RestrictFileSystems=~`, `DropInPaths=` (empty), AppArmor/SELinux/Smack fields empty |
| P8 | `systemctl show … -p SystemCallFilter --value \| tr ' ' '\n' \| grep -nxE '~.*\|ioctl\|mkdir\|mkdirat\|…'` | 0 | allow-list (no `~`); includes `ioctl`, `mkdir`, `mkdirat` |
| P9 | `ps -o pid=,comm= -p 1386` | 1 | no such process now |
| P10 | `journalctl -o json -g 'create subvolume failed' \| jq …` | 0 | **9** matches, one per boot ID (9 distinct), all `_SYSTEMD_UNIT=limine-snapper-sync.service`, `SYSLOG_IDENTIFIER=limine-snapper-watcher`, `_UID=0`, all contain `errno:13` |
| P11 | `journalctl -o cat -g 'create subvolume failed' \| sort \| uniq -c` | 0 | Sanitized inherited summary: create-subvolume failures carry errno 13; newest retained match `2026-10-19 22:48:24 -03`. Raw message bodies omitted by the integrating L1. |
| P12 | `strings -n 6 /usr/lib/limine/limine-snapper-sync \| grep …` | 0 | contains `snapper --no-dbus -c root create-config /` |
| P13 | `pacman -Q snapper btrfs-progs linux coreutils glibc` | 0 | snapper 0.13.1-3, btrfs-progs 7.1-1, linux 7.2.3.arch1-3, coreutils 9.11-2, glibc 2.44+r24 |
| P14 | `strace -e trace=access,faccessat,faccessat2 /usr/bin/test -w /` | 1 | `access("/", W_OK) = -1 EACCES` |
| P15 | `strace -e trace=access,faccessat,faccessat2 bash -c 'test -w /'` | 1 | `faccessat2(AT_FDCWD, "/", W_OK, AT_EACCESS) = -1 EACCES` |
| P16 | `nm -D /usr/bin/test \| grep access` | 0 | `U euidaccess@GLIBC_2.2.5` |

## 2. Primary sources opened (2026-10-19; host-matching tags where available)

| Ref | URL (pinned) | Location | ≤25-word quote / fact |
|---|---|---|---|
| K1 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/ioctl.c | `__btrfs_ioctl_snap_create` L1138; L1148 `-ENOTDIR`; L1150 `mnt_want_write_file`; L1157–1161 `.`/`..` → `-EEXIST`; L1165 `btrfs_mksubvol` | order: ENOTDIR → mount write access (EROFS) → name checks → `btrfs_mksubvol` |
| K2 | same file | `btrfs_mksubvol` L859; L875 `may_create_dentry` | no `capable()` between L859 and L1290 except snapshot-source check L1181–1186 |
| K3 | same file | L1183–1184 | “Subvolume creation is not restricted, but snapshots are limited to own subvolumes only” |
| K4 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/namei.c | `may_create_dentry` L3731; L3735–3736 existing child → `-EEXIST`; L3742 `inode_permission(…, MAY_WRITE \| MAY_EXEC)` | EEXIST is returned **before** any permission check |
| K5 | same file | `sb_permission` L604, L611 `-EROFS`; `inode_permission` L641–642 immutable → `-EPERM`; L661 `security_inode_permission` | LSM hook runs after DAC; may return its own errno |
| K6 | same file | `generic_permission` directory branch L536–541 | directory write passes only via `CAP_DAC_OVERRIDE`; otherwise `-EACCES` |
| K7 | same file | `filename_create` (mkdir path) L4947 | “don't fail immediately if it's r/o, at least try to report other errors” |
| K8 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/namespace.c | L362 `__mnt_is_readonly`; L473 `ret = -EROFS` in `mnt_get_write_access` | `MNT_READONLY` **or** `sb_rdonly` → EROFS |
| K9 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/open.c | L391–392 `AT_EACCESS` → no override; L437–438 `override_cred->cap_effective = override_cred->cap_permitted;` | plain `access(2)` by root checks with permitted caps |
| U1 | https://raw.githubusercontent.com/openSUSE/snapper/v0.13.1/snapper/Btrfs.cc | L139 `y2err("create subvolume failed, " …)`; L143–147 `case EEXIST:` → “creating btrfs subvolume .snapshots failed since it already exists” | host line `Btrfs.cc(createConfig):139` matches tag v0.13.1 = installed 0.13.1 |
| U2 | https://raw.githubusercontent.com/openSUSE/snapper/v0.13.1/snapper/BtrfsUtils.cc | L123–125 | `btrfs_util_create_subvolume_fd(fddst, …)` failure → `runtime_error_with_errno(…, errno)` |
| U3 | https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/libbtrfsutil/subvolume.c | L773 `ioctl(parent_fd, BTRFS_IOC_SUBVOL_CREATE_V2, …)`; L775 returns immediately | ioctl errno is not overwritten before snapper reads it |
| G1 | https://sourceware.org/git/?p=glibc.git;a=blob_plain;f=sysdeps/posix/euidaccess.c;hb=HEAD | L160–161 | “If we are not set-uid or set-gid, access does the same.” → `return __access (path, mode);` (HEAD, not pinned to 2.44; P14 confirms behaviour on host) |
| C1 | https://raw.githubusercontent.com/coreutils/coreutils/master/src/test.c | L382–384 | `case 'w'` → `euidaccess (…, W_OK)` (master; P16 confirms host binary imports `euidaccess`) |

None of these has a `corpus/SOURCES.md` row. If the Matrix cites any of them, the parent must assign new IDs; the Matrix may not cite them unregistered (QUALITY #7).

## 3. Errno precedence the Matrix must encode (and must not transfer between syscalls)

Operation that actually failed: `ioctl(fd("/"), BTRFS_IOC_SUBVOL_CREATE_V2, ".snapshots")`. It was issued by in-process libsnapper (`--no-dbus`), relayed into the unit's stdout (P10–P12, U1–U3).

| Order | Btrfs subvolume create (K1–K8) | `mkdir(2)` (K4, K7) |
|---|---|---|
| 1 | EACCES from path walk (search permission on ancestors) | same |
| 2 | ENOTDIR (fd is not a directory) | — |
| 3 | **EROFS** (`mnt_want_write_file`: mount `MNT_READONLY` or superblock ro) | **EEXIST** (final lookup) |
| 4 | **EEXIST** (`.`/`..` names, then existing child dentry) | **EROFS** (deferred `mnt_want_write`) |
| 5 | ENOENT / EOVERFLOW | ENOENT / EOVERFLOW |
| 6 | EPERM (immutable parent) | same |
| 7 | **EACCES** (DAC without `CAP_DAC_OVERRIDE`) | same |
| 8 | LSM `security_inode_permission` (EACCES or other) | same |

Consequences:
- For the failing ioctl, errno 13 excludes, **at failure time and in the unit's own mount namespace**: read-only mount/superblock (EROFS precedes), an existing `/.snapshots` dentry (EEXIST precedes), and an immutable `/` (EPERM precedes). This exclusion is independent of today's global `findmnt`/`stat`.
- The two columns differ on EEXIST vs EROFS. A `mkdir(2)` fixture (`error-order-smoke.json`, `discriminator-smoke.json`) is valid evidence for EEXIST-before-EACCES only. It is not evidence for the btrfs ioctl's EROFS position.

## 4. Counterexamples / invalid inferences to exclude

**CX1 — HIGH (depth): “`test -w` uses the effective set, so citing access(2)/S034 is wrong.”** Claimed in `C2Review.md:15-19` (F1), repeated as an [inf] in `NoOralReview.md:58`.
- Counterexample: P14 `access("/", W_OK)`; P16 + G1 show that `/usr/bin/test` → glibc `euidaccess` → `__access` when uid==euid and gid==egid. K9: plain access by root uses `cap_permitted`. The AT_EACCESS path (P15) is the **bash builtin** only, which `systemd-run … test` and `sudo test` do not invoke.
- Correct statement: S034's permitted-set rule governs `/usr/bin/test -w` when uid=euid=0. The old note's wording “distinguishes permitted from effective” remains wrong for a different reason (`Capabilities.md:129-140`): permitted equals effective in both runs, so the probe distinguishes bounded root from unbounded root.
- Smallest correction: cite S034 + G1/C1 for `/usr/bin/test`; name the bash-builtin AT_EACCESS divergence as a limit. Drop C2Review F1's “must not cite S034”.

**CX2 — HIGH (depth): “Btrfs subvolume create requires CAP_SYS_ADMIN; CAP_DAC_OVERRIDE without it would fail with EPERM.”** Claimed in `Capabilities.md:164,168`.
- Counterexample: K2/K3. The kernel has no capability gate for subvolume creation (flags 0). The only EPERM in that path is the snapshot-source owner check, which does not apply to `subvol=true`. A sandbox/capability branch keyed on CAP_SYS_ADMIN is therefore wrong. The decisive capability is `CAP_DAC_OVERRIDE` (K6). CAP_SYS_ADMIN in the bounding set is irrelevant to this errno.
- Smallest correction: the capability branch's interpretation names only CAP_DAC_OVERRIDE (and CAP_DAC_READ_SEARCH for search). It must not predict EPERM.

**CX3 — HIGH (depth): “errno 13 proves an authorization failure occurred before target existence could cause EEXIST”; “if parent writable, mkdir returns EEXIST, never EACCES.”** Claimed in `MountErrors.md:92-93`.
- Counterexample: K4 L3735–3736 checks EEXIST **before** `inode_permission`, whatever the parent's writability. The repo's own fixture `error-order-smoke.json` shows a 0555 parent + existing child → EEXIST. The correct inference runs in reverse: errno 13 implies the child did **not** exist in the issuer's namespace at that instant. Path-walk EACCES on ancestors is the only EACCES that precedes EEXIST. It cannot apply to `/` (mode r-x for all classes, P2/P3).
- Smallest correction: rephrase the snapshot-layout discriminator as an ordering fact. Keep `stat /.snapshots` only as a *current-state* check, not a failure-time proof.

**CX4 — HIGH (operability): read-only branch discriminated by global `findmnt -no OPTIONS /`.** (spec contract; `C2Review.md:50` “Excluded for current mount”.)
- Counterexample: the unit runs in a private mount namespace: `ProtectHome=yes` and `ProtectKernelModules=yes` (P7). A `ReadOnlyPaths=`/`ProtectSystem=strict` style bind or a transient btrfs superblock ro is invisible to a later global `findmnt`. In addition, `OPTIONS` merges VFS and FS options; superblock ro shows only in `FS-OPTIONS`. The correct exclusion is K1/K8 ordering (EROFS precedes EACCES for this ioctl), not today's mount table.
- Smallest correction: discriminator = observed errno ≠ 30 + K1 L1150/K8 L473. Record `findmnt -no VFS-OPTIONS,FS-OPTIONS /` and the empty configured `ReadOnlyPaths`/`ProtectSystem=no` as corroboration labelled “current, global namespace / configured”.

**CX5 — HIGH (operability): “capabilities” evidence is configuration, and the obvious runtime read is a trap.**
- Counterexample: `ExecMainPID=1386` is reported for an **inactive** unit (P7) and PID 1386 no longer exists (P9). Any later `/proc/1386/status` read could hit an unrelated reused PID. Even live, the failing syscall came from the child that ran snapper (`Issue6629.md:75-78`: `[1520]` vs main `[1386]`), not from ExecMainPID.
- Correct statement: actual CapEff/CapPrm of the issuer are unobserved. The branch rests on configured `CapabilityBoundingSet=cap_sys_admin`, empty `AmbientCapabilities=`, empty drop-ins (P7) and S028. Root-after-execve recomputation (S027) keeps the bound. Label it `configured`, never `measured`.
- Smallest correction: the JSON branch must carry `evidence_kind: configured` (or equivalent wording) and a limit naming the stale-PID trap.

**CX6 — HIGH (depth/operability): “errno 13 ⇒ DAC” as a closed attribution.**
- Counterexample: after DAC (K6), `security_inode_permission` runs (K5 L661), and the ioctl also passes `security_file_ioctl`. Active LSMs include `bpf` with `CONFIG_BPF_LSM=y` (P5/P6). Loaded BPF-LSM programs cannot be enumerated by a non-root user (P6: `/sys/fs/bpf` permission denied).
- Excluded components: Landlock's `file_ioctl` hook targets device ioctls and applies only to self-restricted processes (`security/landlock/fs.c` v7.2 L2003). Yama and lockdown do not mediate creation. AppArmor and SELinux are absent. Seccomp would kill the process (`SystemCallErrorNumber` sentinel, `ioctl` allow-listed, P7/P8) rather than return EACCES. `RestrictFileSystems=~` is empty. Idmapped-mount EACCES (`HAS_UNMAPPED_ID`) does not apply (no idmap in P1).
- Smallest correction: DAC is the only *positively supported* EACCES producer. Foreign BPF-LSM remains an explicit `unknown` row with an operator-only discriminator (`bpftool prog list` under privilege). The matrix states “DAC+bounding consistent; BPF-LSM not excluded”.

**CX7 — MEDIUM (depth): mode at failure time inferred from today's `stat`.**
- Strengthening counterexample-check: `/` ctime 2026-10-03 (P2) precedes the first `errno:13` (2026-10-16, P11). A chmod, chown or ACL change would bump ctime, so mode, owner and ACL were the same for all 9 failures. The Matrix should use `stat -c %z /` as the read-only discriminator that turns “current DAC” into “DAC at failure time”. Limit: an intervening clock change would also invalidate the comparison; that was not probed.

**CX8 — MEDIUM (operability): misleading booleans the matrix must not accept as success or failure signals.**
- `Result=success` / `ExecMainStatus=0` for a run whose create-config failed (P7, P11; `Issue6629.md:81`).
- `test -w /` as uid 1000 is always false here and answers nothing about root (P14).
- `sudo test -w /` = writable does not prove the ioctl succeeds: LSM `inode_mkdir`/`file_ioctl` hooks, seccomp and EEXIST are not consulted by `access(2)`.
- A rc=1 from `test -w` collapses EACCES, EROFS and EPERM (`Capabilities.md:153-158`, agreed).
- `test -w` probes W only; creation needs W|X (K4 L3742).

**CX9 — MEDIUM (depth): wrong-tool / different-principal framing.**
- `C2Review.md:23` says the note's `snapper create-config` framing “is about a different tool”. Counterexample: P12 and `Issue6629.md:78` show the watcher runs `snapper --no-dbus -c root create-config /`, and the logged line is libsnapper `Btrfs.cc:139` (U1). The tool is snapper.
- `--no-dbus` matters: without it, the syscall would run in `snapperd` under snapperd's own capabilities, and this unit's bounding set would be irrelevant.
- Matrix branch to add or keep: “operation delegated to another principal”. Discriminator: `--no-dbus` in the relayed argv plus `_SYSTEMD_UNIT` of the errno line. Excluded here.
- Limit: journal `_EXE`/`_COMM` name the unit's stream owner, not the syscall issuer.

**CX10 — LOW (freshness/depth): text-match counts as classification inputs.**
- The precedent note says 8, last 08:11:47. At this review: 9, last 22:48:24 (P10/P11). `MountErrors.md:143` still says “8 … directly explaining”, which is stale and overclaims an [inf].
- Branch expectations must key on errno class (13/17/30/1), never on match counts. Any count must carry its query time.

## 5. Verdict on the four mandated branches (baseline contract)

| Branch | Supportable as | Must not claim |
|---|---|---|
| DAC (`/` 555, no ACL, no CAP_DAC_OVERRIDE) | errno 13 + K6 + P2/P3/P7 + S027/S028/S034; mode stable since before failures (CX7) | “proven”; “root always bypasses DAC”; CAP_SYS_ADMIN relevance (CX2) |
| Read-only filesystem | **excluded by errno ordering** (K1 L1150, K8) | exclusion via global `findmnt` alone (CX4); “0555 is a ro mount” |
| Service sandbox / capabilities | configured bounding set + empty ambient/drop-ins; seccomp excluded as an EACCES source; namespace RO excluded by ordering | measured runtime caps (CX5); EPERM-for-missing-CAP_SYS_ADMIN (CX2) |
| Existing snapshot layout | **excluded at failure time** by EEXIST-before-EACCES (K4) and snapper's distinct EEXIST message (U1 L143–147) | “authorization before existence” (CX3); `btrfs subvolume list` as non-root discriminator (EPERM, `NoOralReview.md:93`) |
| Residual (required) | BPF-LSM `unknown` (CX6) | closure of host causal attribution |

## 6. Risks / limits of this seat

- Kernel anchors are tag `v7.2`, not Arch's `7.2.3-arch1-3` patchset. glibc G1 is HEAD and coreutils C1 is master, but the behaviour is confirmed on the host by P14–P16.
- No privileged probe was run: the issuer's runtime caps, the unit namespace mount table and BPF-LSM programs are unobserved.
- Landlock exclusion rests on hook registration plus “self-restriction only”. I did not read the systemd source to prove systemd never applies a Landlock ruleset.
- `SystemCallErrorNumber=2147483646` is read as systemd's kill sentinel. I did not open the systemd source to confirm it; `C2Review.md:52` carries the same caveat.
- Matrix artifacts were absent, so this review cannot PASS or FAIL them. Re-review is needed when the parent sends the final revision.

## 7. Outcome

**No PASS.** The Matrix artifact had not landed. Ten counterexamples were recorded. Four of them (CX1, CX2, CX3, CX9) contradict claims sibling seats will feed into the matrix. CX4 and CX5 reject the contract's own discriminators as stated: global `findmnt`, and configured caps presented as actual caps. With errno ordering, three branches (RO, EEXIST layout, seccomp) can be excluded at failure time **without privilege**. DAC is positively supported but not closed (BPF-LSM residual).

## 8. Qualification (appended 2026-10-19 at parent request; supersedes stronger wording above, append-only)

- **Q1 — ctime/mtime (narrows CX7, §5 DAC row, §7):** P2 is one current snapshot of the inode now mounted at `/`. It does **not** prove that mode, owner and ACL stayed unchanged without interruption across all 9 historical failures. The 9 failures fall on 9 distinct boots (P10). The inode behind `/` may differ per boot (subvolume replacement, rollback or snapshot boot), and clock changes and offline edits were not probed. The origin of the 0555 mode is **unknown**. Retained: P2 as a present-state observation, and the ordering of the 2026-10-03 ctime against the 2026-10-16 first failure as a *consistent-with* datum only.
- **Q2 — source scope (narrows §3, CX3, CX4, CX6, §5, §7):** K1–K9 describe upstream tag `v7.2`. They are **not** proof of the exact Arch `7.2.3-arch1-3` patched runtime path, nor a historical attribution for any of the 9 events. U1–U3 are pinned to the installed snapper and btrfs-progs versions, but the code path actually taken at each event was not traced. K1–K9, U1–U3, G1 and C1 are not registered in `corpus/SOURCES.md`. Main states the Matrix will omit unregistered kernel sources.
- **Q3 — errno 13 is not an unconditional exclusion:** Read §3 “Consequences”, CX3, CX4 and the §5 rows marked “excluded …” as *upstream-source-scoped predictions*: on v7.2 ordering, an EROFS, EEXIST or EPERM condition would be expected to surface first. They are **not** validated host-historical proof of:
  - absence of `/.snapshots`;
  - a read-write mount in the unit namespace;
  - absence of an LSM, including BPF-LSM, which stays unknown;
  - absence of seccomp involvement, which rests on a configured sentinel read as “kill”, unconfirmed in systemd source.

  Primary evidence kept as is: P1–P16 raw observations (journal errno text, configured unit properties, current mount, mode and ACL, `strace` of `test -w`). Limit: each exclusion holds only if the exact host kernel path matches v7.2 and the relayed errno is the ioctl's own.
- **Q4 — CX1, CX2, CX5, CX8, CX9, CX10 unaffected:**
  - CX1, CX8 and CX9 rest on host observations (P12, P14–P16).
  - CX5 and CX10 are evidence-labelling corrections.
  - CX2 still rejects the sibling's EPERM/CAP_SYS_ADMIN *claim* as unsupported by the cited source. Per Q2, my counter-reading (no capability gate) is itself source-scoped to v7.2.
- **Revised outcome:** still **No PASS** (Matrix not reviewed). The “three branches excluded at failure time” statement in §7 is withdrawn. It is replaced by: RO, existing-layout and seccomp are **not supported** as causes by the observed errno text under upstream ordering. They remain unexcluded historically, and DAC remains `[inf]`, consistent but unproven.
