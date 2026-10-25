# SecurityBoundary — r13 read-only namespace diagnostics safety

Seat `TsukuroiR13.SecurityBoundary` (sentinel, leaf). Axis: **depth**, meaning the correction's diagnostics must be safe and actually read-only.
Inputs read: `corpus/knowledge/root-dac-decision-r12.{md,json}` (recheck line 3, B2/B3/B4 discriminators), `SKILL.md:142-168,1717-1740`, `.ufo/waves/round-13/correction/NoOralReview.md` (D1–D6, Residual), `snapper-eacces-mechanism.md:3,23-28`, `LOG.md:562`.
Probes: uid 1000, metadata only. Used `systemctl show -p …`, `ls/stat` on `/proc`, `grep -c`/`grep -ao` key-name and string **counts**, and journal `-o json --output-fields=` metadata (no MESSAGE bodies kept). No sudo, no service operation, no snapper, no nsenter. Installs/updates: **none**.
`root-dac-correction-r13.*` and `tools/check-root-dac-correction.py` were absent when I inspected, so findings 8 and 10 are forward requirements.

## Findings (severity · exploit path · evidence · impact · smallest remediation)

**F1 HIGH: `snapper list-configs` is a "read that mutates" because it D-Bus-activates root `snapperd`.**
- Evidence: `/usr/share/dbus-1/system-services/org.opensuse.Snapper.service` (snapper 0.13.1-3) declares `Exec=/usr/bin/snapperd`, `User=root`, `SystemdService=snapperd.service`.
- The system bus policy allows any sender to reach that service (`org.opensuse.Snapper.conf:11`).
- Journal metadata for `-u snapperd.service` in this boot shows start jobs (MESSAGE_ID 7d4958e8…/39f53479…) each followed by deactivation (7ad2d189…):
  - 22:48:24: boot, the same second as the last `errno:13`
  - **23:15:51**: brackets r12 smoke at 02:16Z/02:17Z (23:16/23:17 −03)
  - **00:43:12**: 2 min after the resumed r12 launch at 00:41:10
  - [inference] the last two came from r12 probes. Other actors cannot be excluded.
- `snapperd` runs with a bounding set that includes `cap_dac_override cap_sys_admin` and `ProtectSystem=no`.
- The command still appears in:
  - r12 MD `recheck:` (line 3)
  - JSON B4 `commands` (json:161, `read_only: true`)
  - SKILL "Allowed (read-only)" list (`SKILL.md:153`)
- `LOG.md:562` claims "no … service operation".
- Side trap: after GC unload, `systemctl show snapperd.service` reports empty `InactiveExitTimestamp=`/`ExecMainStartTimestamp=` even though the journal shows three starts. Empty timestamps do not show the service never ran.
- Impact: every recheck rerun starts a privileged daemon, and the "no service operation" provenance is false as written.
- Remediation: r13 MD/JSON must not carry `snapper list-configs` in any `recheck:` or discriminator. A non-activating substitute is `ls -A /etc/snapper/configs` (observed empty, listable). `--no-dbus` requires root, so it is not a substitute. Route the SKILL Allowed-list and LOG wording fix to a later round as its own append-only correction. It falls outside r13's single claim.

**F2 HIGH (guidance): the "fresh invocation" residual is a boot-chain mutation, not an observation.**
- NoOralReview §3 Residual's operator discriminator says to read `/proc/<live-pid>/…` "during a fresh invocation" (`systemctl start`/`systemd-run`).
- Evidence:
  - The unit runs `ExecStart=limine-snapper-watcher` with `Restart=on-failure`.
  - Strings in `/usr/lib/limine/limine-snapper-sync`: `create-config`×1, `limine.conf`×6, `/boot/efi` (string counts only; [inference] for behaviour).
  - Each start bus-activates `snapperd` (F1).
- Host friction is zero: passwordless sudo was measured (`degraded-triage-r4.md:31`), and uid 1000 is in group `docker`, which is root-equivalent.
- Impact: a reader following the recipe with no oral context could trigger snapper config/subvolume creation and limine boot-entry writes while the mkinitcpio-42 `/sysroot` gate is open.
- Remediation: in r13, label this "state-changing operator action, update-safety gate first". It is never a read-only discriminator and never goes in `recheck:`. The namespace stays `unknown`.

**F3 MEDIUM: the D4 premise is wrong, so the non-root vs privileged boundary was misdrawn.**
- `/proc/1/mountinfo` is `-r--r--r--` and readable as uid 1000 (31 lines). `/proc/1/status` is readable too (3 `Cap(Eff|Prm|Bnd)` lines).
- `readlink /proc/1/ns/mnt` rc=1, so the namespace handle is ptrace-gated.
- Impact: D4's "probably denied → operator-only" overstates the privilege needed for metadata reads. Meanwhile `nsenter`/`findmnt -N`/`unshare` really are privileged and stay forbidden.
- Remediation: for a *bound* live PID (F4), read only the `/proc/<pid>/mountinfo` rows for `/` and the target (mount options and super options), plus the `Cap*` lines of `/proc/<pid>/status`. List path names only. Never open `/run/credentials/*` or any other path the table reveals.

**F4 MEDIUM: PID binding.**
- The r12 recheck hard-codes `ps -o pid=,comm= -p 1386`. NoOralReview D3 uses `[ -d /proc/$pid ]` liveness alone, so a reused PID would misattribute caps or namespace.
- Evidence closing NoOralReview's D2 `[unk]`:
  - All 9 `create subvolume failed` records carry `_SYSTEMD_INVOCATION_ID`.
  - They come from 9 distinct invocations across 9 boots, with `_PID`s 1506–1523.
  - The last one (`1520`, `d0460e24…`) equals the unit's current `InvocationID`.
- Remediation:
  - Require `_PID` to match `^[0-9]+$` (quoted, no shell interpolation).
  - Require `_SYSTEMD_INVOCATION_ID` to equal the live `InvocationID`.
  - Require `/proc/<pid>/cgroup` to contain the unit's cgroup.
  - Require `/proc/<pid>/stat` starttime to match `ExecMainStartTimestampMonotonic`.
  - Any mismatch → `unknown`.

**F5 MEDIUM: credential-bearing output.**
- D1 requests `ExecStartEx/PreEx/PostEx`, which print argv verbatim. Bare `systemctl show` dumps `Environment=`. `systemctl cat` (the `snapper-eacces-mechanism.md:3` recheck) prints raw unit and drop-in text, including literal `SetCredential=` and `Environment=`.
- Shape evidence: in both `limine-snapper-sync.service` and `snapperd.service`, `grep -c` for `Environment|EnvironmentFile|SetCredential*|LoadCredential*|ImportCredential|PassEnvironment` = 0, and `DropInPaths=` is empty. Current risk on this host is nil, but the recipe uses a generic `<unit>`.
- Remediation:
  - Always use an explicit `-p` list.
  - Never use `systemctl cat`, or `show` without `-p`.
  - Project `Exec*Ex` to `path=`/`flags=` only.
  - Never print credential/environment properties, and never read `EnvironmentFile` targets.

**F6 MEDIUM: silent omission looks like "not configured".**
- `systemctl show -p BogusPropXyz <unit>` prints nothing with rc=0, even with `--all`.
- Impact: a misspelled or version-dropped property name reads as empty, which is a false negative for B2.
- Remediation: assert that a `Name=` line is present for every requested property. A missing line means could-not-evaluate (exit 2), never "absent".

**F7 MEDIUM (depth guard): configured text does not bound the runtime view of a CAP_SYS_ADMIN service.**
- `systemd-analyze(1)` local man page, lines 572–576: if a service retains "the privilege to establish or undo mount points many of the sandboxing options can be undone by the service code itself."
- The unit's bounding set is `cap_sys_admin`.
- The `errno:13` records were *logged* by `limine-snapper-sync.service` (`_EXE=/usr/lib/limine/limine-snapper-sync`, `_UID=0`). In the same second, `snapperd` (with `cap_dac_override`) was activated. The ioctl issuer, watcher or snapperd, is therefore [unknown].
- Remediation: phrase D1 results only as "as configured, the unit names no unit-side read-only path for `/`". Never write "namespace excluded". Do not upgrade issuer identity.

**F8 LOW (forward, checker): `--revision REV` git argv construction.**
- A REV beginning with `-` becomes a git option. For example, `git show --output=…:path` is option injection with a write side effect.
- Remediation:
  - Resolve with `git -C <lane-root> rev-parse --verify --end-of-options REV^{commit}`.
  - Read with `git cat-file blob <oid>:<path>`.
  - Use list argv (no shell) and a fixed lane root, not the cwd.

**F9 LOW:** `systemctl show` on an unloaded unit makes the manager load it into memory. This is benign (it is not a start), but avoid wording it as "zero host effect".

## Command boundary for r13 MD/JSON/recheck (proposed)

- **Allowed (metadata, uid 1000):**
  - `systemctl show -p <explicit list>`, with the F6 presence assertion and the F5 projection
  - `systemd-analyze security <unit>` (settings analysis; that it never starts the unit is [inference] from man §security)
  - `findmnt -R -n -o TARGET,VFS-OPTIONS,FS-OPTIONS /`, labelled "host namespace only"
  - `stat`, `getfacl`
  - `/proc/<bound-pid>/{mountinfo,status}` reads (F3/F4)
  - `journalctl -o json --output-fields=_PID,_SYSTEMD_INVOCATION_ID,_BOOT_ID,_SYSTEMD_UNIT`
  - `ls -A /etc/snapper/configs`
- **Forbidden:**
  - `systemctl start|restart|reload|daemon-reload|set-property|edit`, `systemd-run`
  - any `snapper` verb, including `list-configs`; `busctl call org.opensuse.Snapper`
  - `nsenter`, `findmnt -N`, `unshare`, `mount`/`umount`
  - `sudo`, `pkexec`, `docker run -v /:…`
  - `systemctl cat`, bare `systemctl show`
  - reading `EnvironmentFile` targets or `/run/credentials/*`
  - hard-coded PIDs
- `SKILL.md:1717-1730` (r13 section) contains no unsafe command.
- NoOralReview D1/D3/D4/Residual need the F2–F5 edits. D5/D6 are safe as labelled.

## Routed (not this round's claim)

- SKILL Allowed list and `LOG.md:562` vs F1. A future append-only correction is owed; no in-place rewrite.
- F7's issuer ambiguity (watcher vs `snapperd`) goes to CausalityCritic/the correction unknown list as [unknown]. It is not a new branch.
