# MatrixCriticR — round 12 (resumed), C2 falsification review (critic seat, author-side)

- Seat: `TsukuroiR12.MatrixCriticR`. Axes judged: operability, depth. This is author-side critic evidence. It is **not** independent non-author verification.
- Reviewed state: the current working-tree `corpus/knowledge/root-dac-decision-r12.{json,md}`, tags `#10F4` and `#4137`, as found 2026-10-20. `resumed/Matrix.md` was absent at review time (resumed dir held only `spec.json`, `dispatch.json`, `swarm-registry.json`, `task-result.json`). This is therefore a **baseline-contract review of the inherited matrix**, not of a MatrixR revision. Re-review is needed if the parent sends a revision.
- Path note: the prompt's Acceptance line names `MatrixCritic.md`, and its Report line and the contract name `<seat>.md`. I wrote only this file. Inherited `.ufo/waves/round-12/MatrixCritic.md` was read as historical data and left untouched.
- Constraints honoured:
  - No sudo, no systemd-run, no host writes, no installs or upgrades, no tests, builds or linters.
  - No mkdir or write attempt on the host.
  - Journal reads extracted only errno class, timestamp, boot-id prefix, unit, PID and `rootflags=` token. No message bodies or argv were stored.

## 1. Probes run this session (uid 1000, read-only, 2026-10-20)

| # | Command (sanitized) | Exit | Result |
|---|---|---|---|
| R1 | `cat /sys/kernel/security/lsm` | 0 | `capability,landlock,lockdown,yama,bpf` |
| R2 | `systemctl show limine-snapper-sync.service -p FragmentPath -p DropInPaths -p NeedDaemonReload -p CapabilityBoundingSet -p AmbientCapabilities -p SecureBits -p InaccessiblePaths -p BindReadOnlyPaths -p TemporaryFileSystem -p RootDirectory -p RootImage -p PrivateTmp -p ProtectSystem -p ProtectHome -p ReadOnlyPaths -p ReadWritePaths -p ExecMainPID -p ActiveState -p Result …` | 0 | `ActiveState=inactive`, `Result=success`, `ExecMainPID=1386`, `ExecMainStartTimestamp=2026-10-19 22:48:23 -03`, `DropInPaths=` empty, `NeedDaemonReload=no`, `CapabilityBoundingSet=cap_sys_admin`, `AmbientCapabilities=` empty, `SecureBits=0`, `ProtectSystem=no`, `ProtectHome=yes`, `ProtectKernelTunables=yes`, `ProtectControlGroups=yes`, `ReadOnlyPaths=`/`InaccessiblePaths=`/`BindReadOnlyPaths=`/`TemporaryFileSystem=`/`RootDirectory=`/`RootImage=` empty, `ReadWritePaths=/tmp` |
| R3 | `systemctl show … -p ExecStartEx -p ExecStartPreEx -p ExecStartPostEx`, keeping only `flags=` | 0 | `ExecStartEx` flags empty, so no `+`/`!` privileged prefix in the current config. Argv not recorded |
| R4 | `stat /.snapshots` | 1 | stderr `No such file or directory` |
| R5 | `stat /root/.nonexistent-probe` | 1 | stderr `Permission denied`. Same rc as R4 |
| R6 | `stat -c '%a %U:%G %F birth mtime ctime' /` | 0 | `555 root:root directory`. Birth `2026-10-03 17:41:30.687657678 -0300`. mtime **= ctime** `2026-10-03 17:45:33.001630573 -0300` |
| R7 | `findmnt -no TARGET,FSTYPE,VFS-OPTIONS,FS-OPTIONS /`; `findmnt -no OPTIONS /` | 0; 0 | VFS `rw,relatime`; FS `rw,compress=zstd:3,ssd,space_cache=v2,subvolid=256,subvol=/@`. Merged OPTIONS de-duplicates `rw` |
| R8 | `pacman -Q limine-snapper-sync snapper systemd linux`; `uname -r` | 0; 0 | `limine-snapper-sync 1.31.0-1.1`, `snapper 0.13.1-3`, `systemd 261.2-1`, `linux 7.2.3.arch1-3`; kernel `7.2.3-arch1-3` |
| R9 | `stat` unit fragment; `pacman -Qo` it | 0; 0 | mtime 2026-09-05, ctime **2026-10-11 16:14:34 -0300**; owned by limine-snapper-sync 1.31.0-1.1 |
| R10 | `/var/log/pacman.log` (2409 lines), ALPM install/upgrade lines only | n/a (file read) | L1346 `2026-10-03T17:45:33-0300 installed limine-snapper-sync (1.30.1-1)` (same second as `/` ctime, inside a chroot install, L1350); L1886 upgrade to 1.31.0-1.1 and L1887 linux 7.2.3.arch1-3 on 2026-10-11 16:14 |
| R11 | `journalctl -o json -g 'create subvolume failed'` → (ts, boot8, errno, unit, _PID) | 0 | **9** records, all errno 13, 9 distinct boots, all `_SYSTEMD_UNIT=limine-snapper-sync.service`. First 2026-10-16T12:47:26, last 2026-10-19T22:48:24. Last record `_PID=1520` ≠ `ExecMainPID=1386` |
| R12 | `journalctl --list-boots` | 0 | 10 retained boots. Oldest `dd8e2252` starts 2026-10-16 11:34:43 -03 and has **no** failure |
| R13 | `journalctl -o json -b -9 -u limine-snapper-sync.service` | 0 | 0 unit records in the oldest retained boot |
| R14 | `journalctl -o json _TRANSPORT=kernel -g 'Command line:'`, keeping only the `rootflags=` token | 0 | all 9 failing boots: `rootflags=subvol=@` (oldest boot has no retained kernel cmdline record) |
| R15 | `journalctl -o json -g 'Time has been changed\|clock.*(jump\|changed)'` | 1 | no match in the retained journal |
| R16 | `ls -ld /sys/fs/bpf`; `ls /sys/fs/bpf` | 0; 2 | `drwx-----T root root`; listing `Permission denied` for uid 1000 |
| R17 | `strace -f -e trace=access,faccessat,faccessat2 /usr/bin/test -w /` | 0 (strace) | `access("/", W_OK) = -1 EACCES`; test exit 1 |
| R18 | same, `bash -c 'test -w /'` | 0 (strace) | `faccessat2(AT_FDCWD, "/", W_OK, AT_EACCESS) = -1 EACCES` (builtin) |
| R19 | `stat -c '%a %U:%G' /usr`; Python `os.access('/usr', W_OK)` as uid 1000 | 0 | `755 root:root`; `False` |
| R20 | `MANWIDTH=2000 man -P cat 5 systemd.exec` (local systemd 261.2) | 0 | quotes in §2 |
| R21 | upstream `v7.2` `fs/btrfs/ioctl.c`, `fs/btrfs/inode.c`, `security/commoncap.c` fetched with urllib, line-located | n/a | anchors in §2 |

R17/R18 re-run inherited P14/P15 and match them. R11 matches inherited P10/P11 (still 9, last 22:48:24), so no new failure has occurred since the inherited capture.

## 2. Source anchors (located; ≤25-word quotes)

| Ref | Location | Registered? | Fact / quote |
|---|---|---|---|
| M1 | local `systemd.exec(5)`, systemd 261.2, § ProtectSystem= | S028 (Arch man URL; same text family) | "If true, mounts the /usr/ and the boot loader directories (/boot and /efi) read-only … If set to "full", the /etc/ directory is mounted read-only, too." |
| M2 | same, § CapabilityBoundingSet= (end) | S028 | "This does not affect commands prefixed with "+"." The same sentence appears under User=, SecureBits=, AmbientCapabilities=, AppArmorProfile=, SystemCallFilter= |
| K1 | `torvalds/linux v7.2 security/commoncap.c` L82 (`cap_capable`) | **no** | `return cap_raised(cred->cap_effective, cap) ? 0 : -EPERM;` — the capability decision reads the **effective** set |
| K2 | `v7.2 fs/btrfs/ioctl.c` L1150, L1161, L1165 (`__btrfs_ioctl_snap_create`), L875 (`btrfs_mksubvol`) | **no** | `mnt_want_write_file` (EROFS) precedes the name/EEXIST checks and `btrfs_mksubvol` → `may_create_dentry` |
| K3 | `v7.2 fs/btrfs/inode.c` L6852 (`btrfs_create_new_inode` → `btrfs_add_link`), L6926, L4392–4393 | **no** | a subvolume link calls `update_time_after_link_or_unlink`, which sets the parent's ctime and mtime to `now` (skipped only during log replay, L4389) |
| K4 | `v7.2 fs/btrfs/inode.c` L4665 (`btrfs_unlink_subvol`) | **no** | subvolume unlink sets the parent's mtime from `inode_set_ctime_current` |

K1–K4 have no `corpus/SOURCES.md` row. Under QUALITY #7 the Matrix may not cite them as support. They are recorded here as critic evidence and as QUALITY #8/#12 sweep material.

## 3. Reuse / reject / correct (inherited `MatrixCritic.md`)

- **Reused, re-verified now:**
  - CX1: `/usr/bin/test` uses plain `access`, so the bash builtin AT_EACCESS divergence applies only to the builtin (R17/R18).
  - CX5: stale `ExecMainPID` versus issuer PID, `1386` vs journal `_PID=1520` (R2/R11).
  - CX6: residual BPF-LSM stays non-enumerable (R1/R16).
  - CX8: misleading booleans (`Result=success` with errno 13, R2/R11).
  - CX10: counts carry their query time (R11).
- **Reused as source-scoped only:** CX3, CX4 and the ordering table, per Q2/Q3. Upstream v7.2 is not the Arch-patched runtime, and none of it is registered.
- **Corrected:** inherited Q1 withdrew CX7 (ctime as a failure-time datum). New R6/R10/R14 + K3/K4 support a **conditional** reinstatement; see X8. Q1's "inode may differ per boot" concern is narrowed by R14 and `subvolid=256`, not eliminated.
- **Rejected:** none of the inherited claims was falsified by present state.

## 4. Counterexamples against the current matrix (exact invalid inference → smallest correction)

**X1 — HIGH, depth. SC3 `parent: "0755 root:root"`, `caller: uid 1000` → `success (child created)`.** (JSON `scenarios[2]`)
- Invalid inference: the fixture's success transfers to a root-owned parent.
- Counterexample: the fixture parent is a `TemporaryDirectory` created by uid 1000 (`discriminator-smoke.json` L5), so success came from the **owner** write bit. A `0755 root:root` parent gives uid 1000 the "other" class `r-x`. R19 shows `/usr` `755 root:root`, `os.access(W_OK)=False`. S035's EACCES sentence then predicts EACCES, not success.
- Correction: SC3 parent → `0755, owned by the caller (uid 1000)`. Optionally add an SC3b: `0755 root:root` + uid 1000 → B1 / EACCES, basis S035, not fixture-demonstrated.

**X2 — HIGH, depth. SC4 `caller: "uid 0 with cap_dac_override in the bounding set"` → `success`.**
- Invalid inference: bounding-set membership implies DAC bypass.
- Counterexample: the bounding set is a ceiling. The capability decision reads `cred->cap_effective` (K1). A root process with CAP_DAC_OVERRIDE in its bounding set but not in its effective set gets EACCES on a 0555 parent. Examples: `SecureBits=noroot` (M2 lists it), an explicit capset drop, or a non-root `User=`.
- Correction: SC4 input → "CAP_DAC_OVERRIDE in the **effective** set (measured CapEff), uid 0". Basis S027, `[inf]`, not host-demonstrated. Keep K1 out of `source_ids` unless Sources registers it.

**X3 — HIGH, depth. B2 `ProtectSystem=full/strict` as a signal for the target.** (`branches[1].interpretation`, `discriminator.expected_signal`, `decision_procedure[1]`)
- Invalid inference: `full` makes `/` read-only.
- Counterexample: M1. `yes` covers `/usr`, `/boot`, `/efi`; `full` adds `/etc`. Neither covers `/` or `/.snapshots`. Only `strict` does.
- The B2 signal set also omits other unit-side read-only sources visible in the same `systemctl show`: `BindReadOnlyPaths=`, `TemporaryFileSystem=…:ro`, `RootDirectory=`/`RootImage=`, `ProtectHome=read-only|tmpfs` (R2, all empty or `yes` here).
- Correction: expected_signal → "`ProtectSystem=strict`; or `yes`/`full` only when the target lies under `/usr`, `/boot`, `/efi` (`/etc` for `full`); or ReadOnlyPaths=/BindReadOnlyPaths=/TemporaryFileSystem=:ro covering the target; or RootDirectory=/RootImage= set". Add those `-p` properties to the discriminator command.

**X4 — HIGH, depth. The decision procedure is state-first, not errno-first; step 5 overclaims.** (`decision_procedure[0]`, `[4]`)
- Counterexample (step 1, "present → B4"): after an operator fix creates `/.snapshots`, rerunning the procedure over the logged `errno:13` events classifies them B4 (EEXIST family). That contradicts the observed errno.
- Only SC7/SC8 carry an observed errno. The classifier never gates on it, although errno is the only failure-time datum available without privilege.
- Step 5 says the EACCES class "is explained as DAC denial plus a capability-bound caller". That contradicts note §4.6 ("consistent, not proven") and `host_causal_attribution.status: unproven`.
- Correction:
  - Add step 0: "observed errno: 17 → B4 candidate; 30 → B2 candidate; 13 → B1∧B3 or residual; current-state probes corroborate only and are dated".
  - Step 5: "explained as" → "is consistent with".

**X5 — HIGH, operability. `stat` rc=1 read as "absent"; findmnt/snapper counted as absence sweeps.** (`branches[3].discriminator.expected_signal`, `host_observation.target.stat_rc`, note §7 item 9)
- Counterexample: R4 (ENOENT) and R5 (EACCES) both return rc=1. A non-root caller probing a target under a non-searchable parent gets rc=1 with **no** existence information.
- `findmnt <target>` rc=1 means "not a mountpoint", not "no entry". `snapper list-configs` 0 rows says nothing about a directory entry.
- QUALITY #9's "path absence (stat rc=1 + findmnt rc=1 + snapper list-configs 0 rows)" therefore overcounts: one probe bears on absence, two do not.
- Correction:
  - Key B4 absence on the stat **errno text** (`No such file or directory`), with rc=1 + `Permission denied` → "unknown, search denied".
  - Store `stat_errno: ENOENT` in `host_observation.target`.
  - Relabel findmnt as "not a mountpoint" and snapper as "no config", not as absence.

**X6 — HIGH, depth. B3 reads CapabilityBoundingSet but not whether it applies to the command.**
- Counterexample: M2. CapabilityBoundingSet=, User=, SecureBits= and SystemCallFilter= "do not affect commands prefixed with "+"". A `+ExecStart` runs as full root, so B3 would fire on the property text while the process has CAP_DAC_OVERRIDE.
- Here R3 shows empty `ExecStartEx` flags, so this is excluded for current config.
- Correction: add `systemctl show -p ExecStartEx -p ExecStartPreEx -p ExecStartPostEx <unit>` to B3, reading the `flags=` field only (no argv). Expected signal "flags lack `privileged`/`+`". Add `SecureBits` to the property list.
- B3 interpretation "sets contain only CAP_SYS_ADMIN" should read "at most CAP_SYS_ADMIN (configured ceiling)". Never infer live CapEff (resumed spec requirement; K1).

**X7 — MEDIUM, depth. B2 exclusion silently assumes EROFS precedes EACCES; R10 forbids the same move for EEXIST.**
- Invalid inference: B2 says "EROFS is a different errno … so an observed EACCES is not explained by this branch", and note §4.2 says "the EROFS family is excluded for the host shape". If the DAC check ran before the write-access check, a ro mount plus a 0555 parent would surface EACCES, and the exclusion would be wrong.
- No registered source or fixture establishes the EROFS-vs-EACCES order. Upstream v7.2 (K2, L1150 before L1165) predicts EROFS first for the ioctl, but that is unregistered.
- Note §4.2 also derives "excluded" from **global** `findmnt`, while the unit has a private mount namespace (ProtectHome=yes, ProtectKernelTunables=yes, ProtectControlGroups=yes, R2).
- Correction:
  - B2 limit: "EACCES excludes B2 only if the failing operation checks mount write access before DAC; not established by registered sources or this round's fixtures".
  - §4.2: "excluded" → "no configured-unit or global-namespace read-only signal".

**X8 — MEDIUM, depth (optional gain, not a defect). The matrix under-uses failure-time evidence.** (`host_observation.root.inode_times.note`, §5 unknowns)
- Current wording ("timestamps do not prove the mode was in effect") is safe. A stronger, still conditional reading is available:
  - (a) All 9 failing boots mounted `rootflags=subvol=@` (R14). Current `subvolid=256` is the lowest possible subvolume id (BTRFS_FIRST_FREE_OBJECTID), so `/@` is the filesystem's first subvolume, not a later rollback replacement.
  - (b) `/` ctime = mtime = 2026-10-03 17:45:33.0016, which precedes the first failure 2026-10-16 (R6).
  - (c) chmod/setfacl bump ctime. Upstream v7.2 btrfs bumps the parent's ctime+mtime on subvolume link and unlink (K3/K4).
- Hence `[inf]`: mode/owner/ACL of `/` were unchanged, and no `/.snapshots` entry was created or removed in `/`, throughout the incident window. This holds only if:
  - every failing boot's `@` was subvolid 256 (a per-boot id is not logged);
  - there was no clock rollback (R15 found no match in the retained journal, which is weak);
  - there was no offline edit and no log-replay timestamp restore;
  - Arch's 7.2.3-arch1-3 behaves as v7.2 here.
- Side datum: `/` ctime equals the limine-snapper-sync 1.30.1-1 chroot install second (R10 L1346). Equal mtime/ctime nanoseconds mean the last change to `/` was an entry link/unlink, so the 0555 mode was set **at or before** that instant. The mode's origin remains unknown; this is a lead, not attribution.
- Correction: only with Sources registration of K3/K4. Otherwise keep the current wording and add this as a dated `[inf]` lead with the four conditions.

**X9 — MEDIUM, operability/depth. Incomplete LSM sweep presented as a bounded negative.** (note §7 item 9; `host_observation.cross_checks`)
- Counterexample: QUALITY #9 lists "LSM presence (AppArmor N, no SELinux path)". The active LSM list is `capability,landlock,lockdown,yama,bpf` (R1), and BPF-LSM programs cannot be enumerated by uid 1000 (R16).
- The sweep does not cover the enabled set. SC8's "e.g. another confinement" leaves the residual unnamed.
- Correction: add `cat /sys/kernel/security/lsm` to cross_checks. Name BPF-LSM as an `unknown` residual with an operator-only discriminator (privileged `bpftool prog list`, not run).

**X10 — MEDIUM, freshness/depth. "first" failure is first *retained*; the per-boot pattern is 9/10.**
- Counterexample: journal retention starts 2026-10-16 11:34:43 (R12). That boot has zero unit records (R13).
- The unit file in effect (ctime 2026-10-11, R9) and the 7.2.3 kernel (R10 L1887) predate retention, so failures from 2026-10-11 to 2026-10-16 are unobservable, not absent.
- Correction: `journal.first` → "first in retained journal (oldest retained boot 2026-10-16T11:34:43-03:00, no unit records)".

**X11 — LOW, operability. Misleading labels and booleans.**
- `cross_checks.test_w_root_rc` is uid 1000 testing path `/`. It answers nothing about root (R17). Rename it, e.g. `uid1000_test_w_slash_rc`.
- `NoNewPrivileges=yes` in B3's signal is irrelevant to a root bounding-set drop (M2/NNP text concerns gaining privileges via execve). It can stay as context but should not count as a signal.
- `Result=success` coexists with errno 13 (R2/R11) and must never be read as create success.

**X12 — MEDIUM, gate. QUALITY #14/#8 compliance.**
- The note's heading is `## 7. QUALITY check`. QUALITY #14, and the resumed MatrixR prompt, require literal `## QUALITY check`. The check evaluates criteria 1–9 only. #13 and #15 apply directly (EACCES triage; DAC/ACL vs mount namespace vs runtime credentials) and are not evaluated.
- Under #8/#12, "Btrfs ioctl order unestablished" is retained as an unknown without recording a sweep of readable upstream source. K2 shows the source is readable.
- Correction: rename the heading; evaluate #13–#16 as applicable; record the upstream sweep (K2), either as a registered source via Sources or as a sweep note that keeps the unknown.

## 5. Verdict on the four branches (baseline contract)

| Branch | Holds as | Must change |
|---|---|---|
| B1 DAC | S035/S027 semantics + R6/R19; host state current-only (conditionally failure-time, X8) | none mandatory |
| B2 read-only | S035/S028 semantics | X3 (ProtectSystem=full scope; missing ro sources), X7 (unstated ordering; global-ns "excluded") |
| B3 capability-bound | configured text, labelled configured | X2 (SC4 effective, not bounding), X6 (`+` prefix; "at most") |
| B4 existing target | S035 + fixtures, limit correctly refuses ioctl extrapolation | X5 (rc=1 conflation; non-absence probes), X4 (state-first classification) |
| Procedure/scenarios | 8 scenarios, residual SC8 present | X1 (SC3 owner), X4 (errno gate; "explained as") |

≥4 grounded branches exist. Under X1–X7, three scenario/procedure records currently encode **false** expectations: SC3, SC4, and B2's `full` signal. Step 5 contradicts the artifact's own `unproven` status.

## 6. Risks and limits of this seat

- K1–K4 are upstream tag v7.2, not the Arch 7.2.3-arch1-3 patchset, and are unregistered. M1/M2 come from the host-installed systemd 261.2 man page, not the Arch-web S028 URL; text equivalence was not diffed.
- No privileged probe: issuer CapEff/CapPrm, the unit's mount namespace, BPF-LSM programs and per-boot subvolid are unobserved.
- R3 reads current config only. A `+` prefix at failure time is excluded only via R9 (fragment ctime 2026-10-11 < first failure) plus empty drop-ins now. Historical drop-ins in `/etc/systemd/system` or `/run` were not swept.
- `findmnt` merged OPTIONS behaviour under a superblock-only ro (e.g. btrfs forced ro after an error) was not observed. Its rendering is `[inf]`; the matrix should prefer `VFS-OPTIONS,FS-OPTIONS`.
- Installs/updates: none.

## 7. Outcome

**No PASS.** The inherited matrix meets the "≥4 grounded branches" shape, but the following must be fixed before C2 depth can be admitted:
- X1: SC3 is false for a root-owned parent.
- X2: SC4 keys on the bounding set, not the effective set.
- X3: `ProtectSystem=full` does not cover `/`.
- X4: the procedure is state-first, and step 5 says "explained", contradicting `unproven`.
- X5: stat rc=1 conflates ENOENT and EACCES.
- X6: the `+` prefix bypass is unread.
- X12: the heading and the #8/#14 gates.

X7, X9 and X10 are smaller labelling and limit corrections. X8 is an optional, source-registration-dependent depth gain, not a defect. All corrections are text-local to `root-dac-decision-r12.{json,md}` (Matrix-owned) plus, for K-anchors, `SOURCES.md` (Sources-owned).

## 8. Final static re-check of named defects (appended 2026-10-20; §1–§7 above unchanged)

- Trigger: `TsukuroiR12` asked for a concise static check of named defects only. `TsukuroiR12.MatrixR` then notified final readiness.
- Checked state: `root-dac-decision-r12.json` and `.md` at mtime 2026-10-20 00:53:34 -0300 (note tag `#5999`). The check parsed the JSON with Python `json.load` (exit 0, 10 scenarios) and read both files.
- Two source lookups were made for the S027 anchor question:
  - local `man 7 capabilities` is absent (`No manual entry`);
  - the S027 URL's text rendering (`man.archlinux.org/man/capabilities.7.txt`) contains "Effective This is the set of capabilities used by the kernel to perform permission checks for the thread."
- Nothing else was run: no tests, lint or build.

| Defect | Status | Evidence in current artifact |
|---|---|---|
| X1 SC3 | **fixed** | SC3 `0755 root:root` + uid 1000 → `EACCES (13)`, S035-grounded; SC9 invoker-owned 0755 → success (fixture); R11 retained |
| X2 SC4 | **fixed** (anchor nit) | SC4 requires CAP_DAC_OVERRIDE in the **effective** set; SC10 bounding-only → EACCES. Nit: the effective-set fact is on S027's page (§ Thread capability sets > Effective, quoted above), but S027's registered anchor is only `CAP_DAC_OVERRIDE`. SC10 also attributes "bounding-set membership alone does not populate CapEff" to S028, which does not say that; it belongs to S027 § Bounding. Non-blocking; fix = anchor wording |
| X3 B2 `ProtectSystem=full` | **fixed** | interpretation, expected_signal, step 2 and R13 state that `full` covers /usr,/boot,/efi,/etc, not `/`. Residual (non-blocking): `BindReadOnlyPaths=`, `TemporaryFileSystem=:ro`, `RootDirectory=`/`RootImage=` are still absent from the B2 discriminator; the limit's "another sandbox mechanism" covers them generically |
| X4 procedure | **fixed** | step 0 is errno-first and states "not a universal syscall errno-priority proof"; step 5 says "consistent with"; the string "explained as" is absent from the JSON |
| X5 stat rc=1 | **fixed** (wording nit) | `target.stat_error: ENOENT`, `findmnt_meaning: not a mountpoint`, `snapper_meaning: not path proof`; R14 and QUALITY #9 carry the limit. Nit: B4 `expected_signal` still says "stat/findmnt report the path absent", and findmnt cannot report absence |
| X6 `+` prefix | **fixed as declared unknown** | S028 quote added; B3 limit, `unit.command_prefixes` and the §5 unknown list mark it "not inspected, conditional". "Contain only CAP_SYS_ADMIN" is gone; R12 rejects bounding-as-CapEff. Optional: a cheap read-only sweep exists (my R3: `ExecStartEx` flags empty) and would turn the unknown into a current-config observation |
| X7 EROFS ordering | **resolved by scope** | §4.3 no longer says "excluded"; it says host findmnt "cannot exclude a unit-private namespace". Scope is now ordinary mkdir with "no syscall-priority proof" |
| X9 LSM sweep | **fixed** | `cross_checks.lsm_list` + `bpf_lsm_programs: not enumerated … residual unknown`; QUALITY #9 uses the LSM list |
| X10 first retained | **not fixed** (LOW) | `journal.first` still unqualified; oldest retained boot 2026-10-16 11:34 (my R12/R13) is not mentioned |
| X11 labels | **not fixed** (LOW) | `cross_checks.test_w_root_rc` key unchanged (`caller_uid: 1000` sits beside it) |
| X12 QUALITY | **fixed** | literal `## QUALITY check`; #1–#16 evaluated; the Btrfs ioctl unknown is now out of scope, so no #8 upstream sweep is owed. S038/S039/S040 exist in `corpus/SOURCES.md` L44–46 |
| X8 | optional, not adopted | inode-times note kept conservative; acceptable |

**Final-check outcome:** every HIGH defect I named (X1–X6) and X12 is fixed or honestly declared unknown in the current artifact. Remaining items are non-blocking LOW/nit: X10, X11, the X2 anchor wording, the X5 B4 signal wording, and the X3 extra read-only sources. This is **not a PASS** of C2 or of the artifact: it is an author-side static check limited to named defects, not independent verification, and admission and judgment stay with the parent. Unrun: JSON schema check, source census, and any test.

## 9. Nit re-check (appended 2026-10-20, after MatrixR notice; §1–§8 unchanged)

Checked state: JSON mtime 00:56:35 and MD mtime 00:56:43 -0300. `json.load` exit 0. The new B3 quote was string-matched against the S027 page text (`man.archlinux.org/man/capabilities.7.txt`): match **True**.

- **X10: fixed.**
  - `journal.first_match`/`last_match` + `match_scope` read "first and last matched entries in the current journal, not necessarily the oldest retained boot".
- **X11: fixed.**
  - The key is now `test_w_root_path_rc`.
  - `test_w_root_rc` is absent from both files.
- **X2 anchor: fixed for SC4 and B3; one residual.**
  - B3 evidence now has `S027 § Thread capability sets > Effective` with the exact page sentence.
  - SC4's basis cites it.
  - SC10's basis **still** attributes "bounding-set membership alone does not populate CapEff" to S028, which does not state it. Correct home: S027 § Thread capability sets > Bounding.
  - The S027 row in `SOURCES.md` still lists only the `CAP_DAC_OVERRIDE` anchor (grep `Thread capability sets` → no match); widening it is Sources-owned.
  - Both are wording nits, non-blocking.
- **X5 B4 signal: fixed.**
  - It now reads "stat reports … ENOENT text; findmnt can only report not-a-mountpoint, never absence".
- **X3 extra read-only sources: fixed in the discriminator.**
  - B2 queries `BindReadOnlyPaths`/`TemporaryFileSystem`/`RootDirectory`/`RootImage`.
  - The expected_signal covers them.
  - Values are not captured in `host_observation`; my R2 shows all empty.

**Outcome:** all named defects are resolved except the SC10 S028 misattribution, a LOW wording nit. Still **no PASS**: this is an author-side static check, and admission belongs to the parent.

## 10. SC10 attribution re-check (appended 2026-10-20, after MatrixR notice; §1–§9 unchanged)

- Checked state: JSON mtime 00:57:44 and MD mtime 00:57:49 -0300. `json.load` exit 0.
- SC4 and SC10 bases now cite S027 § Thread capability sets > Effective and > Bounding. The phrase "does not populate" is absent from the JSON, so S028 is no longer credited with it.
- Both B3 quotes string-match the S027 page text (`capabilities.7.txt`): Effective **True**, Bounding **True**.
- Residual 1 (cosmetic): the MD `source:` provenance line still lists S027 only as `§ Capabilities list > CAP_DAC_OVERRIDE`. The body Sources entry does include the Thread-set anchors.
- Residual 2 (Sources-owned, pending): the `SOURCES.md` S027 row anchor is still CAP_DAC_OVERRIDE-only (L33 at check time).

**Outcome:** the SC10 misattribution is fixed. No blocking defect from my named list remains. Still **no PASS**: this is an author-side static check, and admission belongs to the parent.

## 11. `source:` line re-check (appended 2026-10-20; §1–§10 unchanged)

- The MD now has mtime 00:58:11 -0300, later than the 00:57:49 state checked in §10.
- Line 1 now reads `S027 capabilities(7) — … § Capabilities list > CAP_DAC_OVERRIDE, § Thread capability sets > Effective/Bounding`. §10 Residual 1 is resolved.
- Only the Sources-owned S027 row anchor in `SOURCES.md` remains pending.
- Still **no PASS**: author-side static check; admission belongs to the parent.
