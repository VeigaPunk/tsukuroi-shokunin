# MatrixR — round-12 resumed C2 executor evidence

- Seat: `TsukuroiR12.MatrixR` (leaf; no delegation, no background jobs, no git mutation, no fleet writes).
- Axes: **operability** (read-only indicator matrix with runnable discriminators) and **depth** (source-grounded branch semantics, explicit configured-vs-measured limits).
- Repo: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Start HEAD `b76b5c377eaee3e3d8d47fdddde977828d05dbd5`. `git status` before edits: `M corpus/QUALITY.md`, `M corpus/SOURCES.md`, `?? .ufo/waves/round-12/`, `?? corpus/knowledge/root-dac-decision-r12.{md,json}`, `?? corpus/lessons/round-12.md`.
- No packages installed or upgraded. No `sudo`, `systemd-run`, service restart, host write, or privileged probe. No tests/build/lint/formatters run; the only machine check was `jq empty` on the JSON (structural only).

## Inherited state and re-verification

- `.ufo/waves/round-12/Matrix.md` was **absent** (`read` returned not found); no old Matrix evidence file was available to treat as current.
- `corpus/knowledge/root-dac-decision-r12.md` and `.json` existed as inherited mid-work, untracked at the starting HEAD. I read them as historical data, re-ran their host probes, re-read the parent smoke fixtures, and corrected them surgically. This report does **not** claim the inherited output as a new run.
- C2 independence: no census script, census output, census fixture or root-metadata census field was read or used. C1 and C2 remain separate.

## Files changed (only owned paths)

1. `corpus/knowledge/root-dac-decision-r12.json` — corrected branch/scenario/host records; valid JSON (`jq empty` exit 0); 4 branches, 10 scenarios (SC1–SC10).
2. `corpus/knowledge/root-dac-decision-r12.md` — corrected note; provenance trio first; literal `## QUALITY check` with criteria #1–#16 evaluated.
3. `.ufo/waves/round-12/resumed/MatrixR.md` — this evidence report.

Not edited: `corpus/SOURCES.md` (SourcesR-owned), `tools/tsukuroi-census.sh` (Census-owned), `snapper-eacces-mechanism.md` (owner’s appended erratum), `LOG.md`, `SKILL.md`, `SCORECARD.md`, `README.md`, old wave evidence.

## Commands and exits (read-only; uid 1000 unless noted)

| # | Command | Exit | Observed (sanitized) |
|---|---|---|---|
| 1 | `stat -c 'mode=%a owner=%U:%G type=%F path=%n' /` | 0 | `mode=555 owner=root:root type=directory path=/` |
| 2 | `stat -c 'path=%n mode=%a uid=%u gid=%g ctime=%z mtime=%y birth=%w' /` | 0 | `555 0:0`; ctime/mtime `2026-10-03 17:45:33 -0300`; birth `2026-10-03 17:41:30 -0300` |
| 3 | `getfacl -p /` | 0 | base entries only: `user::r-x`, `group::r-x`, `other::r-x` |
| 4 | `findmnt -n -o TARGET,FSTYPE,OPTIONS /`; `findmnt -no OPTIONS /` | 0; 0 | `/ btrfs rw,relatime,compress=zstd:3,ssd,space_cache=v2,subvolid=256,subvol=/@`; literal options `rw,relatime,compress=zstd:3,ssd,space_cache=v2,subvolid=256,subvol=/@` |
| 5 | `findmnt -n -o VFS-OPTIONS,FS-OPTIONS /` | 0 | VFS `rw,relatime`; FS `rw,compress=zstd:3,ssd,space_cache=v2,subvolid=256,subvol=/@` |
| 6 | `systemctl show -p User -p Group -p CapabilityBoundingSet -p AmbientCapabilities -p ProtectSystem -p ProtectHome -p ReadOnlyPaths -p ReadWritePaths -p NoNewPrivileges -p ActiveState -p Result -p ExecMainPID limine-snapper-sync.service` | 0 | `ActiveState=inactive`, `Result=success`, `ExecMainPID=1386`, `User=root`, `CapabilityBoundingSet=cap_sys_admin`, ambient empty, `ProtectSystem=no`, `ProtectHome=yes`, `ReadOnlyPaths=` empty, `ReadWritePaths=/tmp`, `NoNewPrivileges=yes` |
| 7 | `systemctl is-active limine-snapper-sync.service`; `systemctl is-enabled limine-snapper-sync.service`; `systemctl show -p MainPID limine-snapper-sync.service` | 3; 0; 0 | `inactive`; `enabled`; `MainPID=0` |
| 8 | `ps -o pid=,comm= -p 1386` | 1 | no output — reported PID is stale |
| 9 | `stat -c 'path=%n type=%F mode=%a owner=%U:%G' /.snapshots` | 1 | `No such file or directory` (ENOENT) |
| 10 | `findmnt -n -o SOURCE,FSTYPE,OPTIONS /.snapshots` | 1 | no output — not a mountpoint (not proof of path absence) |
| 11 | `snapper list-configs` | 0 | header only, 0 configured rows (not path proof) |
| 12 | `journalctl --no-pager -o short-iso -g 'create subvolume failed' \| grep -c 'errno:13'` | 0 | **9** at 2026-10-20 query; first/last matched entries `2026-10-16T12:47:26-03:00` / `2026-10-19T22:48:24-03:00` (not necessarily oldest retained boot) |
| 13 | `test -w /`; `test -x /` | 1; 0 | write false, search true for uid 1000 |
| 14 | `lsattr -d /` | 0 | no inode attribute flags |
| 15 | `cat /sys/module/apparmor/parameters/enabled`; `ls -d /sys/fs/selinux` | 0; 2 | `N`; SELinux path absent |
| 16 | `cat /sys/kernel/security/lsm` | 0 | `capability,landlock,lockdown,yama,bpf` |
| 17 | `grep -n '^z / ' /usr/lib/tmpfiles.d/root.conf` | 0 | `10:z / 555 - - -` |
| 18 | `pacman -Qo /usr/lib/tmpfiles.d/root.conf` | 0 | owned by `systemd 261.2-1` |
| 19 | `systemctl show -p ActiveState -p Result -p ExecMainStatus systemd-tmpfiles-setup.service` | 0 | `active`, `success`, `0` |
| 20 | `jq empty corpus/knowledge/root-dac-decision-r12.json` | 0 | valid JSON; 4 branches / 10 scenarios |
| 21 | `grep -n 'root-dac-decision-r12' SKILL.md README.md LOG.md SCORECARD.md corpus/knowledge/snapper-eacces-mechanism.md` | 2 | mentions only `SKILL.md:1695` and `snapper-eacces-mechanism.md:75` (both S027/S028/S034/S035); other files absent/no match |

## Sources opened or consumed this round

- **Opened as URLs this round:** S027 `capabilities.7`, S028 `systemd.exec.5`, S034 `access.2`, S035 `mkdir.2` (man.archlinux.org; footers `2026-02-08` / systemd `262.1` / `2026-02-11`). Retained ≤25-word located quotes:
  - S027: “Bypass file read, write, and execute permission checks.” (8 words); § Thread capability sets > Effective: “This is the set of capabilities used by the kernel to perform permission checks for the thread.” (16); § Thread capability sets > Bounding: “The capability bounding set is a mechanism that can be used to limit the capabilities that are gained during execve(2).” (20).
  - S028: “Capabilities listed will be included in the bounding set, all others are removed.” (13); “Note that this option also affects the respective capabilities in the effective, permitted and inheritable capability sets.” (17); “This does not affect commands prefixed with `+`.” (7); ProtectSystem/ReadWritePaths quotes in §Sources of the note (all ≤23 words).
  - S034: “for the root user, the check uses the set of permitted capabilities rather than the set of effective capabilities” (19).
  - S035: EACCES (23), EROFS (9), EEXIST (21), EPERM (11).
- **S038** (`access(2)` proxy limit, tier A, mined): row read; quote “access() does not answer the "can I read/write/execute this file?" question” (11). Same URL already opened; cited only for the proxy-vs-operation limit; S034 remains the permitted-set sentence.
- **S039** (`tmpfiles.d(5)`, tier A): row and quotes supplied by SourcesR this round; this seat did **not** independently open the tmpfiles.d URL. Quote used: “Adjust the access mode, user and group ownership, and restore the SELinux security context of a file or directory, if it exists.” (22).
- **S040** (local root policy, own-work, tier A): verified locally via commands 17–19. Line 10 `z / 555 - - -`, systemd 261.2-1, tmpfiles-setup active/success. No raw config body copied.
- No new source ID was added by this seat.

## Corrections applied (inherited defects)

1. **SC3 ownership error:** inherited SC3 claimed uid 1000 success against `0755 root:root`. Fixed: root-owned `0755` grants write to owner only → `EACCES` (13), S035-grounded. Added **SC9** for the actual fixture case: invoker-owned `0755` → success. The fixture parent was created by uid 1000 (`TemporaryDirectory`).
2. **SC4 effective-set error:** inherited SC4 accepted `CAP_DAC_OVERRIDE` “in the bounding set” as sufficient. Fixed: requires it in the **effective** set; added **SC10** (bounding-only, effective cleared → `EACCES`) to make the distinction explicit and non-privileged to reason about.
3. **B2 ProtectSystem=full scope:** full covers `/usr/`, `/boot/`, `/efi/`, `/etc/` — **not `/`**. Only `strict` or a `ReadOnlyPaths=` entry covering `/` can make `/` read-only through the unit. Host `findmnt` cannot exclude a unit-private namespace or another sandbox mechanism; the discriminator now also queries `BindReadOnlyPaths=`, `TemporaryFileSystem=`, `RootDirectory=` and `RootImage=` (not part of this capture).
4. **B3 configured-vs-measured:** removed the claim that the sets contain only `CAP_SYS_ADMIN`; S028 says the option “also affects” effective/permitted/inheritable. Live `CapEff`/`CapPrm` are unobserved. `ExecMainPID=1386` is stale (`ps` rc=1) and must not be used. Added the `+` command-prefix condition (`This does not affect commands prefixed with "+"`); `ExecStart` prefixes were not inspected.
5. **Errno-order absolutes:** the old B4-first framing is now explicitly a **diagnostic collection order for ordinary `mkdir`**, not a universal syscall-priority rule and not transferable to the Btrfs subvolume ioctl. The `decision_procedure` starts from the observed errno family and treats target presence as an indicator, not a cause. `findmnt` can only report not-a-mountpoint; it cannot report path absence.
6. **Root 0555 policy:** cited S039/S040; mode is shipped tmpfiles policy (`z / 555 - - -`), not corruption and not “no baseline”. No `chmod` advice. C1 owns the health judgment.
7. **Proxy source scope:** S034 retained only for the permitted-set sentence; S038 cites the actual-operation limit. The note no longer treats `access(2)` as an actual create check.
8. **Target-path proof limit:** `stat` rc=1 with `ENOENT` text, `findmnt` rc=1 (“not a mountpoint”), and `snapper list-configs` 0 rows are all current-state indicators; none proves historical absence or failure-time state.
9. **QUALITY:** heading is the literal `## QUALITY check`; criteria #1–#16 are evaluated, including #10 supersession sweep, #11 parent-owned LOG, #12 unavailable tool, #13 EACCES fields, #14 performed-not-promised, #15 root-metadata/denial separation, #16 policy-source inspection.
10. **SC7 host wording:** `measured` → `configured` for unit properties; journal count labelled context only.

## Scenario set (JSON)

| id | inputs (short) | expected |
|---|---|---|
| SC1 | 0555 root:root, uid 1000, rw, new | B1 / EACCES 13 |
| SC2 | 0555 root:root, uid 1000, rw, existing | B4 / EEXIST 17 |
| SC3 | 0755 **root:root**, uid 1000, rw, new | B1 / EACCES 13 |
| SC4 | 0555 root:root, uid 0, CAP_DAC_OVERRIDE **effective**, rw, new | bypass / success |
| SC5 | writable parent, capable root, ro or strict/ReadOnlyPaths covering target | B2 / EROFS 30 |
| SC6 | 0555 root:root, configured bound root (`cap_sys_admin`), rw, new | B1+B3 / EACCES 13 (configured prediction) |
| SC7 | host-shaped current observation | B1+B3 consistent; **not proven** |
| SC8 | writable parent, capable root, rw, new, observed EACCES | UNCLASSIFIED |
| SC9 | 0755 **invoker-owned**, uid 1000, rw, new | success (fixture) |
| SC10 | 0555 root:root, CAP_DAC_OVERRIDE bounding-only / effective cleared | B1+B3 / EACCES 13 |

## Retained factual vs unknown distinction

- **Factual:** branch semantics and errno families (S027/S028/S034/S035/S038/S039/S040); host mode/owner/ACL/mount; unit configured properties; target current state; ordinary-`mkdir` fixture results; root policy line and package owner.
- **Unknown:** live `CapEff`/`CapPrm` and identity of the failing issuer; unit-private mount namespace; `ExecStart` `+` prefixes; Btrfs ioctl ordering/path at failure time; whether the nine logged failures share one cause; foreign BPF-LSM mediation; failure-time target state; mode continuity across the nine boots.
- **Leading `[inf]`:** configured B1+B3 is consistent with the logged EACCES class; not a syscall trace and not proof.

## Risks, limits and blockers

- No live capability measurement was possible: unit inactive, `ExecMainPID` stale, issuer may be a child. The optional `/proc/<live-issuer-pid>/status` discriminator is documented but **unrun**; no fake PID was used.
- The Btrfs subvolume ioctl is outside this matrix. No Btrfs trace, no read-only mount/EROFS test, no BPF-LSM program enumeration, no privileged probe.
- S027's SOURCES row lists only § CAP_DAC_OVERRIDE; SourcesR re-verified both Thread-set sections on 2026-10-20 and decided the inherited anchor field stays unchanged, logging the request/decision. The citation remains valid at section level: this note's header and §Sources name the exact sections, and the row supplies tier A plus the page (same pattern as S028's ProtectSystem/ReadWritePaths use). S027 stays mined with used-by `corpus/knowledge/root-dac-decision-r12.md`.
- S038/S039/S040 are `mined` with `used-by corpus/knowledge/root-dac-decision-r12.md` as of this report; the stale queued note is superseded.
- `SKILL.md:1695` and `snapper-eacces-mechanism.md:75` still list only S027/S028/S034/S035. Parent must update those pointers at landing; this seat is not allowed to edit them.
- No independent non-author verification is claimed. MatrixCriticR/C2ReviewR are reviewer seats, not independent verification.
- No PASS is claimed: this is a diagnostic matrix plus source-backed corrections, with host causal attribution explicitly unproven.

## Tool record

- Installs/upgrades: **none**. No packages, `uv`, `cargo`, `npm` or release binaries installed.
- Network: read-only man-page fetches (`curl`/`read`) for S027/S028/S034/S035 and the same `access(2)` page for S038. No endpoint requests, no credentials.
