# C2 review — root EACCES decision matrix (round-12)

Reviewer: C2Review (leaf, static review; no sudo, no host mutation, no installs).
Repo: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin. Start HEAD b76b5c377eaee3e3d8d47fdddde977828d05dbd5; `git status` shows only `.ufo/waves/round-12/` untracked.

## Status

- **Matrix not present.** `ls corpus/knowledge/root-dac-decision-r12.*` → "No such file or directory" (exit 2). Review therefore covers the existing mechanism note `corpus/knowledge/snapper-eacces-mechanism.md` (QUALITY #13 DAC pairing) plus a checklist the Matrix lane must satisfy.
- **C2 verdict: NOT PASSED.** No four-branch matrix exists to judge. The existing note contains one causal mechanism ([inf], DAC) and one rejected reading (R6); it does not contain a branch set.
- Commands run (all read-only or fetch-to-/tmp): `stat -c '%a %U:%G' /`; `getfacl -p /`; `systemctl cat/show/list-units/list-unit-files` for limine units; `systemctl show … -p SystemCallErrorNumber`; `diff` of installed unit vs upstream fetch; `journalctl --no-pager -o short-iso -g 'create subvolume failed'` (count + emitter sweep); `pacman -Qo /usr/bin/test`, `pacman -Qs`, `pacman -Ql limine-snapper-sync`; `findmnt -n -o FSTYPE,OPTIONS /` (subvol option redacted); `stat -f -c %T /`; `cat /sys/kernel/security/lsm`; `uname -r`; `id -un`; `curl` of primary sources into `/tmp/c2rev` (outside repo). Exit codes: all 0 except the noted 404/502 fetch misses and the missing-matrix `ls` (exit 2).
- Privileged/state-changing commands executed: **none**. Not run: sudo, systemd-run, snapper, chmod, btrfs subvolume create, pacman -S/-Sy/-Syu. Installs/updates: **none**.

## Findings (by severity)

### F1 — High: explanatory citation for the `test -w` falsifier is wrong (prediction still holds)
- Note line 30: "`access(2)` (S034) explains why this `test -w` comparison distinguishes root's permitted capabilities from its effective capabilities."
- Source: coreutils `src/test.c` lines 382–384 (`case 'w': … return euidaccess (argv[pos - 1], W_OK) == 0;`) — fetched 2026-10-19 from raw.githubusercontent.com/coreutils/coreutils master. `euidaccess(3)` (man.archlinux.org/man/euidaccess.3, fetched 2026-10-19): "Like access(2), euidaccess() checks permissions … uses the effective … identifiers of the process." access(2) root rule (S034) describes the *non*-AT_EACCESS path: "for the root user, the check uses the set of permitted capabilities rather than the set of effective capabilities."
- Consequence: the probe `test -w` uses the **effective** set, not permitted. The note's stated reason is inverted for this probe. Under `CapabilityBoundingSet=CAP_SYS_ADMIN` permitted = effective = {CAP_SYS_ADMIN}, so the predicted rc=1 is unaffected; but the matrix must not cite S034 as the discriminator.
- Fix for matrix: cite euidaccess(3) for the probe; state that the probe only matches the kernel check when permitted = effective (true here by bounding-set construction).
- **Correction (2026-10-19, after Main's IRC report):** SourceReview's strace of `/usr/bin/test -w /` shows `access('/',W_OK)`, not `faccessat(…,AT_EACCESS)`. Upstream `test.c` calls `euidaccess`; I did not obtain the gnulib `euidaccess` implementation (404 on all tried URLs), so the mapping from `euidaccess` to `access()` vs `faccessat(AT_EACCESS)` is unverified here. Plausible [inference]: gnulib's euidaccess may call `access()` when real and effective IDs match (root: uid=euid=0). The F1 conclusion that the probe uses the effective set is therefore withdrawn as an unverified claim. The matrix does not depend on `test -w`; the parent's `mkdir` probe on a 0555 parent (EACCES new / EEXIST existing, error-order-smoke.json) is the kernel-level observation to cite instead.

### F2 — High: causal link from EACCES to DAC is asserted, not source-cited
- Note line 14 [inf] asserts the unit "lacks the root DAC bypass needed to create `/.snapshots`". The note never names the emitting code path. Source chain (torvalds/linux master, fetched 2026-10-19; line numbers are master's, not the host kernel 7.2.3-arch1-3's):
  - Sanitized journal metadata: the watcher associated with `limine-snapper-sync.service` reported a create-subvolume failure, errno 13 (inherited journal sweep, 2026-10-19). Raw message body omitted by the integrating L1; this does not establish the historical syscall/path.
  - Kernel: `fs/btrfs/ioctl.c` `__btrfs_ioctl_snap_create` (subvol branch) → `btrfs_mksubvol` (line 881) → `may_create_dentry` (line 897) → `fs/namei.c` `may_create_dentry` (line 3742) `inode_permission(…, MAY_WRITE | MAY_EXEC)` → `generic_permission` (namei.c 521–560) returns -EACCES unless `capable_wrt_inode_uidgid(CAP_DAC_OVERRIDE)`. The subvol path contains no `capable()` check of its own (grep of ioctl.c 1150–1196 and the function header).
  - So the DAC branch is causally supported for a directory write without CAP_DAC_OVERRIDE. The note should cite these three locations with the kernel version it reflects; currently it cites only man pages.
- Risk: without the kernel link the note's mechanism is an analogy from capabilities(7) + systemd.exec(5), i.e. [inf] by construction.

### F3 — Medium: falsifier is a proxy, not the failing operation; it is privileged
- Note lines 25–28: `sudo systemd-run --wait --pipe -p CapabilityBoundingSet=CAP_SYS_ADMIN test -w /` (predicted rc=1) and `sudo test -w /` (predicted rc=0).
- The failing operation is an ioctl that performs `may_create_dentry` on `/` for a child named by the config (see F2). `test -w /` checks write on the directory, which matches the DAC decision but not the btrfs ioctl itself. The matrix must label this as a proxy.
- The second line (`sudo test -w /`, predicted 0) is a control only under full caps; it does not discriminate anything the first line does not.
- The command is privileged (sudo, transient unit creation). It is labeled operator-only and "not run" in the note: acceptable. The matrix must keep that label and must not present either line as executed evidence.
- The transient unit inherits none of the real unit's other properties (ProtectHome, SystemCallFilter, NoNewPrivileges). That is fine for a DAC-only probe but must be stated as a limit.

### F4 — Medium: journal count is stale and untimestamped
- Note line 11: 8 matches, last `2026-10-19T08:11:47-03:00`. Re-run at review time: **9** `errno:13` matches; newest `Mon 19 Oct 2026 10:48:24 PM -03`. The count is a moving snapshot; the note records no query time. Matrix must record query time (or `--since`) with any count.

### F5 — Medium: note's `systemd.exec` quote is incomplete
- Note line 56 says S028 "also affects effective and permitted sets." Source (man.archlinux.org/man/systemd.exec.5, fetched 2026-10-19): "Note that this option also affects the respective capabilities in the effective, permitted and inheritable capability sets." The note omits *inheritable*. Quoted sentence "Capabilities listed will be included in the bounding set, all others are removed" is verbatim. Minor, but the matrix quote must be exact.

### F6 — Medium: package-version to source-commit mapping not checked
- Installed unit (`/usr/lib/systemd/system/limine-snapper-sync.service`, package `limine-snapper-sync 1.31.0-1.1`) is **byte-identical** to today's fetch of the S020 `master` raw file (`diff` exit 0). The note pins S020 to commit cd909745, but no step ties package 1.31.0-1.1 to that commit. Because S020 is mutable `master`, the matrix's unit citation is current-master evidence only.

### F7 — Medium: branch set not present; the note's only discriminator is one DAC branch
Checklist of branches the matrix must include, with the evidence already available to C2 (each row is what the Matrix lane must turn into a discriminating test):

| Branch | Predicted observable if this is the cause | Already measured / source | Status for C2 |
|---|---|---|---|
| DAC: owner class has no write, no CAP_DAC_OVERRIDE | errno 13 at ioctl; `test -w /` rc=1 under bounding CAP_SYS_ADMIN | `/` = 555 root:root; `getfacl` base entries only; fs/namei.c generic_permission | Supported by source; falsifier is proxy (F3) |
| Mount read-only (EROFS) | errno 30 from `mnt_want_write_file` before `may_create` | `findmnt -n -o FSTYPE,OPTIONS /` → `btrfs rw,…` (2026-10-19) | Excluded for current mount; a mode-0555 directory is not a ro mount — the matrix must not conflate |
| EEXIST (pre-existing `.snapshots` / `@.snapshots`) | errno 17; `may_create_dentry` returns EEXIST **before** the permission check (namei.c 3735–3736) | errno 13 observed (so no existing child dentry at event time); `stat /.snapshots` → no such file | Excluded for observed events; R6 rejection stands |
| Seccomp (SystemCallFilter) | SIGSYS/kill, not errno 13, unless SystemCallErrorNumber=EACCES | Unit has `SystemCallFilter=@system-service @mount`; `SystemCallErrorNumber` unset → `systemctl show` value 2147483646; systemd.exec(5): default is "terminating the process immediately" | Excluded as an errno 13 source for this unit ([inf] on systemd sentinel value; verify against systemd source before citing) |
| LSM (AppArmor/SELinux) | EACCES from security hook | `/sys/kernel/security/lsm` = `capability,landlock,lockdown,yama,bpf` → no AppArmor/SELinux | Largely excluded; Landlock only if the process self-applies (not shown) |
| ACL on `/` | EACCES via named ACL entries | `getfacl -p /` → only user/group/other base entries | Excluded |
| Filesystem not btrfs | ENOTTY/EOPNOTSUPP, not EACCES | `stat -f -c %T /` → btrfs | Excluded |
| Path search (component not searchable) | EACCES on a parent component | `/` is the only component of the target path | Excluded for this path |

The note as written provides only the first row, and it lacks the link to the kernel call (F2). An "existing snapshot layout" branch (archinstall `@.snapshots`) is covered only by R6's rejection.

### F8 — Low: remediation derived from an unverified branch
- Note line 34 offers `chmod 755 /` as the "ART K2 candidate" if `0555` is unintended. It is labeled operator-only and not performed (compliant). But the recommendation rests on F2 and on the DAC branch being the cause; it should be gated on the matrix's discriminator. C1 owns whether `0555` is unhealthy; C2 must not carry that judgment.

## Checklist for the Matrix lane (when `corpus/knowledge/root-dac-decision-r12.md` lands)

1. Each branch states: observable, predicted errno/rc, the probe, and the probe's privilege class. Mark any sudo/systemd-run probe as "operator-only, not run".
2. Each branch must differ in predicted outcome from at least one other branch under the same observation; otherwise it is advice, not a discriminator.
3. Cite the kernel path (F2) for any EACCES/EROFS/EEXIST ordering claim, with the kernel version the claim reflects.
4. Cite euidaccess(3) for `test -w` and access(2) only for the non-AT_EACCESS root rule (F1).
5. Quote systemd.exec(5) exactly, including "inheritable" (F5).
6. Record query time for every count (F4) and the upstream commit or package version for the unit (F6).
7. Do not state "`0555` is a read-only mount" or "root always bypasses DAC" (both false here; the branch list above excludes them).
8. Keep the proxy caveat (F3) and the unlisted-property limit of the transient unit.
9. Any branch left unmeasured (e.g. Landlock self-application) must be listed as residual, not claimed excluded.

## Residual risks and verification gaps

- Kernel source reviewed is master as of 2026-10-19, not the host kernel 7.2.3-arch1-3; line numbers may differ. Not verified: exact host kernel tag.
- `EROFS` ordering (`mnt_want_write_file` before `btrfs_mksubvol`) read from ioctl.c 1181–1188 only; the EROFS return inside `mnt_get_write_access_file` was not line-checked.
- bash `test -w` path: `lib/sh/eaccess.c` (savannah) lines 194–199 call `faccessat(AT_FDCWD, path, mode, AT_EACCESS)`; root shortcut at lines 143–146 is in `sh_stataccess`. Not relevant to the note (which uses /usr/bin/test via systemd-run), recorded only to exclude a false-positive trap.
- Gnulib `euidaccess-stat.c` could not be fetched (404); the glibc-level mapping rests on euidaccess(3) text.
- The falsifier was not executed; all predicted rc values are [inf] until an operator runs them.
- No non-author verification: this is author-side static review by a leaf reviewer seat; it is not independent spotcheck.

## Sources (fetched 2026-10-19; /tmp/c2rev, outside repo)

- coreutils `src/test.c` (raw.githubusercontent.com/coreutils/coreutils, master) — lines 382–384.
- `fs/btrfs/ioctl.c` (raw.githubusercontent.com/torvalds/linux, master) — `btrfs_mksubvol` line 881–897; `__btrfs_ioctl_snap_create` ~1181–1188.
- `fs/namei.c` (torvalds/linux, master) — `generic_permission` 521–560; `may_create_dentry` 3731–3743.
- `fs/namespace.c` (torvalds/linux, master) — `mnt_want_write_file` 571–579.
- man.archlinux.org: systemd.exec(5) (CapabilityBoundingSet=, SystemCallErrorNumber=), access(2) (DESCRIPTION, ERRORS), capabilities(7) (CAP_DAC_OVERRIDE), euidaccess(3).
- Upstream unit: gitlab.com/Zesko/limine-snapper-sync master `install/arch-linux/usr/lib/systemd/system/limine-snapper-sync.service` (byte-identical to installed file at review time).
- bash `lib/sh/eaccess.c` (git.savannah.gnu.org/cgit/bash.git/plain, fetched).

Installs/updates recorded: none.
