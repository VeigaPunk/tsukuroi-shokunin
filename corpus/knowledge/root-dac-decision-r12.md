source: S027 capabilities(7) — https://man.archlinux.org/man/capabilities.7 § Capabilities list > CAP_DAC_OVERRIDE, § Thread capability sets > Effective/Bounding; S028 systemd.exec(5) — https://man.archlinux.org/man/systemd.exec.5 § CapabilityBoundingSet=, § ProtectSystem=, § ReadWritePaths=, § ProtectHome=; S034 access(2) — https://man.archlinux.org/man/access.2 § DESCRIPTION (permitted-set sentence only); S035 mkdir(2) — https://man.archlinux.org/man/mkdir.2 § ERRORS; S038 access(2) proxy limit — https://man.archlinux.org/man/access.2 § DESCRIPTION (supersedes S034 for actual-operation writability); S039 tmpfiles.d(5) — https://man.archlinux.org/man/tmpfiles.d.5 § LINE TYPES > z; S040 local root policy — /usr/lib/tmpfiles.d/root.conf line 10 (`z / 555 - - -`, systemd 261.2-1).
verified-at: 2026-10-20 (re-opened S027/S028/S034/S035 and the access(2) page behind S038 this round; consumed the SourcesR-verified S039 row and verified S040 locally; re-ran the read-only host probes below; re-read the parent smoke fixtures as historical author-side data).
recheck: on-release; procedure: `stat -c 'mode=%a owner=%U:%G type=%F path=%n' /; getfacl -p /; findmnt -n -o TARGET,FSTYPE,VFS-OPTIONS,FS-OPTIONS /; systemctl show -p User -p Group -p CapabilityBoundingSet -p AmbientCapabilities -p ProtectSystem -p ProtectHome -p ReadOnlyPaths -p ReadWritePaths -p NoNewPrivileges -p ActiveState -p Result -p ExecMainPID -p MainPID limine-snapper-sync.service; systemctl is-active limine-snapper-sync.service; systemctl is-enabled limine-snapper-sync.service; ps -o pid=,comm= -p 1386; stat -c '%F %a %n' /.snapshots; findmnt -n -o SOURCE,FSTYPE,OPTIONS /.snapshots; snapper list-configs; journalctl --no-pager -o short-iso -g 'create subvolume failed' | grep -c 'errno:13'`.

# Root-DAC create-failure decision matrix (round 12)

## Purpose, scope and independence

This note documents a **read-only indicator matrix for ordinary `mkdir`/`mkdirat`
create-class failures** at a target path: the `EACCES` (13), `EROFS` (30), `EEXIST` (17)
and `EPERM` (1) families. It is built for the rollback-net surface and grounded in
S027, S028, S034, S035, S038, S039 and S040.

The four branches are **API-grounded indicator families and controls**, not four
simultaneously live causes on this host. The matrix performs **no syscall-priority proof**:
the steps in the JSON `decision_procedure[]` are a diagnostic collection order, and the
observed errno is an input, never a conclusion. **This note does not classify the Btrfs
subvolume ioctl** used by the snapshot tool; ordinary `mkdir` controls must never be
presented as proof of that path or of any historical host cause.

C2 is independent of the C1 census arm: this matrix reads no census script, census output,
census fixture or root-metadata census field. The root-mode policy origin below is cited
only so the DAC indicator is not misread as corruption; the health judgment belongs to C1.

## Canonical JSON records

The canonical branch records (`id`/`evidence`/`interpretation`/`discriminator`/`limit`/
`source_ids`, plus `evidence_kind`), the diagnostic collection procedure, the ten
deterministic scenarios and the host observation live in
`corpus/knowledge/root-dac-decision-r12.json` (`tsukuroi-dac-decision-matrix-v1`). That file
is the single source for branch content; this note explains it and does not restate every
record.

| id | role | API error family | evidence kind |
|---|---|---|---|
| B1 | parent DAC write/search denial (control) | `EACCES` (13) | measured filesystem metadata |
| B2 | read-only filesystem or unit read-only namespace (control) | `EROFS` (30) | current host mount view + configured unit text |
| B3 | capability-bound root / sandbox drop (conjunct of B1 for the `EACCES` class) | `EACCES` (13) | configured unit text; live caps unobserved |
| B4 | target path already present (ordinary-mkdir control) | `EEXIST` (17) | current target-path existence |

B2 explicitly excludes `ProtectSystem=full` as a cause for `/`: `full` covers `/usr/`,
`/boot/`, `/efi/` and `/etc/`, while only `strict` mounts the entire hierarchy read-only
(S028). B3 is a configured restriction, not a live `CapEff`/`CapPrm` measurement; bounding
membership alone does not establish the effective set (S028, S027).

## Current host evidence (read-only, non-privileged, 2026-10-20)

- [obs] `/` is a directory, mode `555`, `root:root` — `stat -c 'mode=%a owner=%U:%G type=%F path=%n' /` exit 0. `getfacl -p /` exit 0 shows base entries only: `user::r-x`, `group::r-x`, `other::r-x`; owner/group/other write absent, execute present for all classes. `stat -c 'path=%n mode=%a uid=%u gid=%g ctime=%z mtime=%y birth=%w' /` exit 0 gives ctime/mtime `2026-10-03 17:45:33 -0300`, birth `2026-10-03 17:41:30 -0300`; these are dated metadata only.
- [obs] The host `/` mount is btrfs **`rw`**: `/ btrfs rw,relatime,compress=zstd:3,ssd,space_cache=v2,subvolid=256,subvol=/@` — `findmnt -n -o TARGET,FSTYPE,OPTIONS /` exit 0; the literal `findmnt -no OPTIONS /` also exits 0 with `rw,relatime,compress=zstd:3,ssd,space_cache=v2,subvolid=256,subvol=/@`; `findmnt -n -o VFS-OPTIONS,FS-OPTIONS /` exit 0 gives VFS `rw,relatime` and FS `rw,compress=zstd:3,ssd,space_cache=v2,subvolid=256,subvol=/@`. Mode `555` is a DAC bit pattern on a read-write mount, not a read-only mount.
- [obs] The `555` mode is shipped policy on this host: `grep -n '^z / ' /usr/lib/tmpfiles.d/root.conf` exit 0 prints `10:z / 555 - - -`; `pacman -Qo /usr/lib/tmpfiles.d/root.conf` exit 0 reports `systemd 261.2-1`. S039 documents the `z` line type; S040 records the effective line, file digest, upstream origin and `systemd-tmpfiles-setup` state (`ActiveState=active`, `Result=success`, `ExecMainStatus=0` at this capture). This matrix treats the mode as configured policy, does not grade it unhealthy, and gives no `chmod` advice; C1 owns that judgment.
- [obs] Configured unit properties — `systemctl show -p User -p Group -p CapabilityBoundingSet -p AmbientCapabilities -p ProtectSystem -p ProtectHome -p ReadOnlyPaths -p ReadWritePaths -p NoNewPrivileges -p ActiveState -p Result -p ExecMainPID limine-snapper-sync.service` exit 0: `ActiveState=inactive`; `Result=success`; `ExecMainPID=1386`; `User=root`; `Group=` (empty); `CapabilityBoundingSet=cap_sys_admin`; `AmbientCapabilities=` (empty); `ProtectSystem=no`; `ProtectHome=yes`; `ReadOnlyPaths=` (empty); `ReadWritePaths=/tmp`; `NoNewPrivileges=yes`. `systemctl is-active` exits 3 (`inactive`). `ps -o pid=,comm= -p 1386` exits 1 with no output, so the reported `ExecMainPID` is **stale** and must not be used for a `/proc/<pid>/status` read; a separate `systemctl show -p MainPID` gives `MainPID=0` (no running process).
- [obs] These are **configured** properties, not live capability sets. S028 says `CapabilityBoundingSet=` includes the listed capabilities in the bounding set and also affects the effective, permitted and inheritable sets; the live `CapEff`/`CapPrm` of the failing issuer were not measured. S028 also says `This does not affect commands prefixed with "+"`; the unit's `ExecStart` prefixes were not inspected here, so the configured restriction is conditional.
- [obs] `ProtectSystem=no` and empty `ReadOnlyPaths=`: B2 is not configured for `/`. For reference, `ProtectSystem=full` covers `/usr/`, `/boot/`, `/efi/` and `/etc/` but not `/`; only `strict` (or a `ReadOnlyPaths=` entry covering `/`) would make `/` read-only through the unit (S028). The B2 discriminator also queries `BindReadOnlyPaths=`, `TemporaryFileSystem=`, `RootDirectory=` and `RootImage=`, which can change the unit's path view; they were not part of this capture.
- [obs] `/.snapshots` current state: `stat -c 'path=%n type=%F mode=%a owner=%U:%G' /.snapshots` exits 1 with `No such file or directory` (ENOENT) text; `findmnt -n -o SOURCE,FSTYPE,OPTIONS /.snapshots` exits 1, which means **not a mountpoint**, not proof of path absence; `snapper list-configs` exits 0 with its header only (0 configured configs), which is not path proof. These are current-state observations and do not reconstruct the failure-time state.
- [obs] Journal context: `journalctl --no-pager -o short-iso -g 'create subvolume failed' | grep -c 'errno:13'` → **9** at the 2026-10-20 query (first matched entry `2026-10-16T12:47:26-03:00`, last matched entry `2026-10-19T22:48:24-03:00`; these are the current journal's match bounds, not necessarily the oldest retained boot). The count is context only; the branches key on the observed errno family, never on a text-match count.
- [obs] Non-root cross-checks (uid 1000): `test -w /` rc=1, `test -x /` rc=0; `lsattr -d /` shows no inode flags; AppArmor `parameters/enabled` = `N`; `/sys/fs/selinux` absent (`ls -d` rc=2); `/sys/kernel/security/lsm` = `capability,landlock,lockdown,yama,bpf`. Loaded BPF-LSM programs were not enumerated as non-root, so foreign LSM mediation remains an explicit unknown.
- [obs, parent smoke — author-side, not independent verification] `discriminator-smoke.json` (captured 2026-10-20T02:16Z, uid 1000, disposable temp directory): parent `0555` + new target → `EACCES` (13); **invoker-owned** parent `0755` → child created; `0755` + existing target → `EEXIST` (17). `error-order-smoke.json` (02:17Z): parent `0555` + new target → `EACCES`; parent `0555` + existing target → `EEXIST`; its own limit is ordinary `mkdir` on this kernel, not the Btrfs ioctl. The `0755` fixture parent was created by uid 1000, not root-owned.
- [correction] The inherited SC3 record claimed uid 1000 success against a **root-owned** `0755` parent. That was wrong: mode `0755 root:root` grants write to the owner only, so uid 1000 falls to group/other `r-x` and the ordinary-mkdir result is `EACCES` (S035). SC3 now records `EACCES`; SC9 records the invoker-owned `0755` fixture case (`success`). Ownership, not mode alone, decides the uid-1000 class.

## Worked example — the host-shaped walk (scenario SC7)

1. **Observed input:** the journal context is `errno:13` ×9 at query time. This is an input and context, not proof of the path or issuer.
2. **Target indicator:** `stat /.snapshots` → `ENOENT` text; `findmnt` → not a mountpoint; `snapper list-configs` → 0 configs. For an ordinary `mkdir`, target presence would be a B4-family indicator; here none is observed. These are current-state facts, not failure-time proof.
3. **Read-only indicator:** host `/` is `rw`; `ProtectSystem=no`; `ReadOnlyPaths=` empty. B2 is not configured on this host, but a host `findmnt` cannot exclude a unit-private namespace or another sandbox mechanism.
4. **DAC indicator:** `/` is `555 root:root` with base-only ACL entries; write absent, search present. B1 signal.
5. **Capability indicator:** configured `User=root`, `CapabilityBoundingSet=cap_sys_admin`, empty `AmbientCapabilities=`, `NoNewPrivileges=yes`. B3 configured signal; live `CapEff`/`CapPrm` unobserved and the reported PID is stale. A `+` command prefix would bypass the property, and `ExecStart` prefixes were not inspected.
6. **Interpretation:** the configured B1 + B3 conjunction with a `rw` mount is **consistent with** an observed `EACCES` class for an ordinary `mkdir`. It is not proof of the historical operation, a measured capability state, or the Btrfs ioctl path.
7. **Classification:** `consistent, not proven`. The residual unknowns in the next section remain.

## Factual branches vs unknown attribution

- **Factual and re-runnable:** branch API semantics and errno families (S027/S028/S034/S035/S038/S039); the host metadata in the previous section; the ordinary-`mkdir` fixture results; the shipped `555` policy line and its package ownership (S040).
- **Unknown:** the failing issuer's live `CapEff`/`CapPrm` and identity (the unit was inactive, `ExecMainPID` was stale, and the issuer may be a child); the unit-private mount namespace; the `ExecStart` `+` prefixes; the actual Btrfs subvolume ioctl ordering and path at each failure; whether all nine logged failures share one cause; any foreign BPF-LSM mediation; the failure-time target state. Inode timestamps do not establish mode continuity across the nine failures.
- **Leading [inf] explanation:** the configured B1 + B3 conjunction (mode `555` on `/` plus a bounding set that omits `CAP_DAC_OVERRIDE`) is consistent with the logged `EACCES` class. It is an explanation, not a syscall trace; no privileged probe was run.
- **Reading correction (append-only discipline):** the round-11 falsifier in `snapper-eacces-mechanism.md` compares a capability-bounded process with an unbounded one, which changes the whole capability envelope. S034's permitted-set sentence describes `access(2)`'s proxy for root; it does **not** authorize an actual write or `mkdir`. S038 is the superseding row: `access()` explicitly does not answer the actual-operation question. The parent has appended the erratum to the old note; this note does not edit it.
- **No historical inference gain:** the matrix does not use current target absence, current mount options or configured capabilities to assert what happened in any past event. Those are indicators only.

## Rejected readings

- **R7 — "mode `0555` means the filesystem is mounted read-only."** Rejected: `0555` is a DAC bit pattern on the inode, while the host `/` mount is `rw` (`findmnt`); a read-only mount is a separate mechanism whose write failures are `EROFS` (S035), not the observed `EACCES`.
- **R8 — "root always bypasses DAC."** Rejected: the bypass is the capability `CAP_DAC_OVERRIDE` (S027), exercised from the effective set; a bounding set that omits it restricts the executed process (S028), and `User=root` alone decides nothing.
- **R9 — "the logged `errno:13` proves the DAC + capability mechanism (or proves the target was absent / the mount was read-only)."** Rejected as proof: branch semantics are factual, but the historical host cause is not established — no syscall trace, no privileged probe, the issuer's live caps are unobserved, the tool's own ioctl ordering is outside this matrix, and current path absence is a dated current-state observation.
- **R10 — "`EEXIST` is checked after the parent write permission, so `EACCES` proves the target was new."** Rejected: on this kernel the isolated **ordinary `mkdir`** order is existing target → `EEXIST` even under a `0555` parent (`error-order-smoke.json`). This is a collection-order fact for ordinary `mkdir`, not a universal syscall priority, and it must not be transferred to the Btrfs subvolume ioctl; `errno:13` does not establish target absence for that operation.
- **R11 — "any `0755` parent lets uid 1000 create a child."** Rejected: the owner write bit is not other write. `0755 root:root` gives uid 1000 only `r-x` (SC3 → `EACCES`); the fixture's success used an **invoker-owned** `0755` parent (SC9), not a root-owned one.
- **R12 — "`CapabilityBoundingSet=cap_sys_admin` proves the live process's `CapEff` omits `CAP_DAC_OVERRIDE`."** Rejected: the option is configured text that also affects the sets at spawn (S028), but it is not a live `CapEff`/`CapPrm` measurement; the reported `ExecMainPID` was stale, the issuer may be a child, and a `+` command prefix is not affected by the option. Use `/proc/<live-issuer-pid>/status` only when a live PID is confirmed.
- **R13 — "`ProtectSystem=full` makes `/` read-only."** Rejected: `full` covers `/usr/`, `/boot/`, `/efi/` and `/etc/`; only `strict` mounts the entire hierarchy read-only (S028). Only `strict` or a `ReadOnlyPaths=` entry covering `/` could produce a B2-family `EROFS` for `/` through the unit.
- **R14 — "`stat` exit 1 alone proves the target path does not exist."** Rejected as proof: the observed output carries `ENOENT` text for this path, but `findmnt` exit 1 only means "not a mountpoint" and `snapper list-configs` 0 rows only means no configured configs. None reconstructs the failure-time state.
- **R15 — "mode `555` on `/` is a wrong mode or has no baseline."** Rejected: it is a package-owned systemd tmpfiles policy line (`S040`, `z / 555 - - -`, systemd 261.2-1; `S039` for `z` semantics), re-applied by tmpfiles. Whether that policy is desirable is C1's healing judgment; this matrix records it and gives no `chmod` advice.

## QUALITY check

Performed on this entry at 2026-10-20; all applicable criteria #1–#16 are evaluated below.

1. **Falsifiable:** every branch discriminator is a re-runnable read-only command with an explicit expected signal; scenarios SC1–SC10 state deterministic inputs and expected errno families. No claim is a PASS; host attribution remains `[inf]`/unknown.
2. **Measured anchor:** §"Current host evidence" gives exact commands, exit codes and observed values; sources cite `corpus/SOURCES.md` rows with anchors.
3. **Observation / inference / unknown:** separated by `[obs]`, `[inf]` and the unknown list; the residual `UNCLASSIFIED` scenario is a first-class outcome.
4. **Errata append-only:** the old `snapper-eacces-mechanism.md` is not edited; its owner appended the falsifier erratum. This new entry is uncommitted mid-wave and was corrected in place before landing; no old wave evidence or LOG/lesson/SCORECARD/README/SKILL file was edited.
5. **Rejections retained:** R7–R15 are kept, including the inherited SC3/SC4 corrections and the `ProtectSystem=full` rejection.
6. **Pacman advice:** none is given; no bare `pacman -Sy` is mentioned.
7. **External citations:** each external claim cites an exact `corpus/SOURCES.md` row with tier A and a section anchor: S027/S028/S034/S035/S038/S039; S040 is the local own-work policy row. S038 supersedes S034 only for actual-operation writability. No unregistered kernel source is cited.
8. **Unknown sweep and provenance:** the journal, mount, unit properties, target path, LSM list and shipped root policy were swept; the entry begins with `source:`, `verified-at:` and `recheck:`.
9. **Negative claims bounded:** target-path absence is bounded by `stat` (ENOENT text), `findmnt` (not a mountpoint) and `snapper list-configs` (0 configs) with the explicit limit that none proves historical absence; LSM presence is bounded by the `/sys/kernel/security/lsm` read; live caps are explicitly unobserved; dates are recorded.
10. **Supersession / mention sweep:** `grep -n 'root-dac-decision-r12' SKILL.md README.md LOG.md SCORECARD.md corpus/knowledge/snapper-eacces-mechanism.md` found `SKILL.md:1695` and `snapper-eacces-mechanism.md:75`, both listing only S027/S028/S034/S035; README/LOG/SCORECARD have no mention. The parent must update SKILL.md and the old note's pointer to include S038/S039/S040 at landing; this seat is not allowed to edit those files. The branch table has 4 columns and a matching 4-column delimiter row.
11. **LOG entry:** parent-owned; not written by this seat. No landing commit is claimed here.
12. **Unavailable tool:** no absent tool is used for a mechanism claim. `stat`, `getfacl`, `findmnt`, `systemctl`, `snapper`, `lsattr` and `journalctl` were available and used; no web search was needed.
13. **EACCES triage fields:** target mode/owner/ACL (555 root:root, base ACL), unit `CapabilityBoundingSet`/`ProtectSystem`/`ReadOnlyPaths`/`ReadWritePaths`/`NoNewPrivileges` and the configured-vs-live capability limit are recorded.
14. **Performed, not promised:** this section is the executed check; the evidence pointers resolve to the commands and rows above. It is an author-side check, not an independent non-author verification.
15. **Root metadata and denial separation:** §3 reports owner-write/search bits and the policy origin, not a universal mode policy; the denial analysis distinguishes inode DAC/ACL (B1), mount/namespace (B2), and runtime credentials/capabilities (B3). Ordinary `mkdir` controls are explicitly not used to certify the historical Btrfs ioctl cause.
16. **Policy sources and overrides:** before any health reading, the owning policy was inspected: S039 (`z` line type), S040 (`/usr/lib/tmpfiles.d/root.conf` line 10, package owner systemd 261.2-1, no `/etc` or `/run` override recorded) and the tmpfiles-setup state. The `555` mode is therefore a known configured observation, not an automatic drift or "wrong mode" finding; this matrix makes no unhealthy verdict.

## Sources

- **S027, tier A — capabilities(7)** — https://man.archlinux.org/man/capabilities.7 § Capabilities list > CAP_DAC_OVERRIDE: “Bypass file read, write, and execute permission checks.” § Thread capability sets > Effective: “This is the set of capabilities used by the kernel to perform permission checks for the thread.” § Thread capability sets > Bounding: “The capability bounding set is a mechanism that can be used to limit the capabilities that are gained during execve(2).”
- **S028, tier A — systemd.exec(5)** — https://man.archlinux.org/man/systemd.exec.5 § CapabilityBoundingSet=: “Capabilities listed will be included in the bounding set, all others are removed.”; “Note that this option also affects the respective capabilities in the effective, permitted and inheritable capability sets.”; “This does not affect commands prefixed with "+".” § ProtectSystem=: “If true, mounts the /usr/ and the boot loader directories (/boot and /efi) read-only for processes invoked by this unit.”; “If set to "full", the /etc/ directory is mounted read-only, too.”; “If set to "strict" the entire file system hierarchy is mounted read-only, except for the API file system subtrees /dev/, /proc/ and /sys/”. § ReadWritePaths=: “Note that ReadWritePaths= cannot be used to gain write access to a file system whose superblock is mounted read-only.”
- **S034, tier A — access(2)** — https://man.archlinux.org/man/access.2 § DESCRIPTION: “for the root user, the check uses the set of permitted capabilities rather than the set of effective capabilities”. This sentence describes the `access(2)` proxy only; it does not establish actual-operation writability.
- **S035, tier A — mkdir(2)** — https://man.archlinux.org/man/mkdir.2 § ERRORS: EACCES “The parent directory does not allow write permission to the process, or one of the directories in path did not allow search permission.”; EROFS “path refers to a file on a read-only filesystem.”; EEXIST “path already exists (not necessarily as a directory). This includes the case where path is a symbolic link, dangling or not.”; EPERM “The filesystem containing path does not support the creation of directories.”
- **S038, tier A — access(2) proxy limit** — https://man.archlinux.org/man/access.2 § DESCRIPTION: “access() does not answer the "can I read/write/execute this file?" question”. Supersedes S034 for actual-operation writability; the permitted-set sentence remains a proxy statement only.
- **S039, tier A — tmpfiles.d(5)** — https://man.archlinux.org/man/tmpfiles.d.5 § LINE TYPES > z: “Adjust the access mode, user and group ownership, and restore the SELinux security context of a file or directory, if it exists.”; “when set to "-", the file ownership will not be modified”.
- **S040, tier A — local root policy** — `/usr/lib/tmpfiles.d/root.conf` line 10 `z / 555 - - -`; package-owned by systemd 261.2-1 (`pacman -Qo`, 2026-10-20); no `/etc` or `/run` override recorded; `systemd-tmpfiles-setup` active, `Result=success`, `ExecMainStatus=0`. The `-` columns leave ownership unchanged; this is shipped policy, not an incident artifact.
- **Host evidence (own work, read-only, uid 1000, 2026-10-20)** — the command list in `recheck:` above, plus `lsattr -d /`, `cat /sys/module/apparmor/parameters/enabled`, `ls -d /sys/fs/selinux`, `cat /sys/kernel/security/lsm`, `pacman -Qo /usr/lib/tmpfiles.d/root.conf`.
- **Parent smoke fixtures (author-side, historical)** — `.ufo/waves/round-12/discriminator-smoke.json` and `.ufo/waves/round-12/error-order-smoke.json`; isolated disposable directories, uid 1000, no host root writes, no read-only filesystem mounted. The `0755` fixture parent was invoker-owned; see the SC3 correction above.
