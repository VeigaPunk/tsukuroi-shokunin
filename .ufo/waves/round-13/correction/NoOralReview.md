# NoOralReview — round 13 correction, unit read-only namespace discriminators

Seat: `TsukuroiR13.NoOralReview` (leaf; read-only; no delegation; no commits; no fleet or corpus writes).
Scope: read the original round-12 matrix recheck commands, then recommend self-contained read-only next discriminators for the **unmeasured unit namespace**, without relying on a stale PID or a global host-namespace read.
Installs/updates: **none**. No sudo, no `systemd-run`, no service start/stop, no unit override. Full invocation IDs, ExecStart argv/flags, environment and credential properties are not recorded here; identifiers appear only as 8-character prefixes. Checks not run (contract).

## 1. Original recheck commands (what round 12 actually asserted)

Sources: `corpus/knowledge/root-dac-decision-r12.md` line 3 (`recheck:`); `.ufo/waves/round-12/resumed/MatrixR.md` commands 4–12; `.ufo/waves/round-12/resumed/MatrixCriticR.md` R2, R11, R14.

| # | Original command | Defect for the unit-namespace question |
|---|---|---|
| O1 | `ps -o pid=,comm= -p 1386` | **Hard-coded stale PID.** `ExecMainPID=1386` is a completed watcher invocation (§2). A future run can read a reused PID and call it "live". |
| O2 | `systemctl show -p … -p ExecMainPID -p MainPID limine-snapper-sync.service` | Omits the path-view controls: `RootDirectory`, `RootImage`, `RootEphemeral`, `BindPaths`, `BindReadOnlyPaths`, `TemporaryFileSystem`, `InaccessiblePaths`, `PrivateTmp`, `PrivateMounts`, `ProtectHome`, `MountAPIVFS`. The JSON B2 discriminator names some of them, so the MD recheck line and the JSON disagree. |
| O3 | `findmnt -n -o SOURCE,FSTYPE,OPTIONS /.snapshots`; `findmnt -no OPTIONS /` | Host-namespace reads. B2's own limit says a host `findmnt` cannot exclude a unit-private namespace; the recheck line does not carry that limit. `OPTIONS` merges VFS and FS options (MatrixCriticR §6). |
| O4 | `journalctl --no-pager -o short-iso -g 'create subvolume failed' \| grep -c 'errno:13'` | Unscoped: no `-u`, no invocation or boot scoping, text match on message bodies. The count 9 spans 9 boots (MatrixCriticR R11, R12) and cannot say which invocation issued any record. |
| O5 | `stat -c … /.snapshots`; `snapper list-configs` | Acceptable as current-state context only (round 12 already limits them). Not a unit-namespace measurement. |

## 2. Observed now (read-only, uid 1000, configured state; this seat)

Path-view properties only: `RootDirectory=` empty; `RootImage=` empty; `RootEphemeral=no`; `BindPaths=` empty; `BindReadOnlyPaths=` empty; `TemporaryFileSystem=` empty; `InaccessiblePaths=` empty; `ReadOnlyPaths=` empty; `ReadWritePaths=/tmp`; `PrivateTmp=no`; `PrivateMounts=no`; `MountAPIVFS=no`; `ProtectHome=yes`; `ProtectSystem=no` (earlier round-12 capture). `FragmentPath=/usr/lib/systemd/system/limine-snapper-sync.service`; `DropInPaths=` empty. Unit inactive.

- Invocation identity, as an 8-character prefix only: `InvocationID` prefix `d0460e24` (current or last invocation; inactive unit).
- `ExecMainPID=1386` is a completed process (`ps` rc 1 is expected). Not used as a live PID.
- Scope: these are configured properties, not the built mount namespace of any invocation. `ProtectHome=yes` creates a mount namespace at exec time; a host `findmnt` cannot show it.
- [inf] The failing issuer is a child of the watcher: the journal's last `errno:13` record (2026-10-19T22:48:24) falls at the watcher's stop time, and MatrixCriticR R11 records a `_PID` (1520) that differs from 1386. Dead child PIDs are unrecoverable now.
- Excluded from this seat's reads and from D1: ExecStart/ExecStartEx argv and flags, environment, credential properties, and kernel-protect properties that are not path-view.

## 3. Recommended read-only discriminators (self-contained; no hard-coded PID; no identifiers beyond 8-char prefixes)

Each row states what it can show and what it cannot. None names a PID in its output; none writes state.

**D1 — configured path-view properties (replaces O2).** Run as uid 1000:
`systemctl show -p FragmentPath -p DropInPaths -p RootDirectory -p RootImage -p RootEphemeral -p MountAPIVFS -p PrivateTmp -p PrivateMounts -p ProtectSystem -p ProtectHome -p ReadOnlyPaths -p ReadWritePaths -p InaccessiblePaths -p BindPaths -p BindReadOnlyPaths -p TemporaryFileSystem <unit>`
- Expected for "no unit-side read-only path for `/`": `ProtectSystem` not `strict`; `ReadOnlyPaths=`, `BindReadOnlyPaths=`, `TemporaryFileSystem=` empty or not covering `/`; `RootDirectory=`/`RootImage=` empty.
- Excludes ExecStart*, environment, credential and non-path-view properties by construction.
- Can show: configured path-view shape at capture time. Cannot show: the built mount table of any invocation, or any failure-time state.
- Record `FragmentPath` ctime and the systemd version beside it (round-12 R9/R10 pattern).

**D2 — journal failure records scoped by unit, counts and 8-char prefixes only (replaces O4).**
`journalctl -u limine-snapper-sync.service -o json --no-pager | jq -r 'select((.MESSAGE\|tostring)\|test("create subvolume failed")) | "\(._BOOT_ID[0:8]) \(._SYSTEMD_INVOCATION_ID[0:8])"' | sort | uniq -c`
- Output is only `count boot8 invocation8` rows. No timestamps, PIDs, message text or full identifiers.
- Expected: rows whose invocation8 prefixes can be compared with the `InvocationID` prefix from §2. If no row matches the current prefix, the current `InvocationID` says nothing about the failing invocations — record as a limit, not a pass.
- Can show: how many distinct boot/invocation pairs carry the errno-13 class. Cannot show: the issuer's capabilities or namespace. Caveat: `_SYSTEMD_INVOCATION_ID` is a documented journal field (systemd.journal-fields(7), local man page) whose presence on these records is **not yet observed** — [unk] until D2 is run.

**D3 — PID liveness, counts only (replaces O1).** Read the record `_PID` values inside the pipe, never print them:
`journalctl -u limine-snapper-sync.service -o json --no-pager | jq -r 'select((.MESSAGE\|tostring)\|test("create subvolume failed")) | ._PID' | sort -u | while read -r p; do [ -d "/proc/$p" ] && echo live || echo gone; done | sort | uniq -c`
- Output is only `live`/`gone` counts. A `live` answer is a reused PID unless `/proc/$p/stat` start time matches the record's timestamp; that match is needed before any reading and is not performed by this recipe.
- Can show: liveness counts only. Cannot show: capabilities of a dead process.

**D4 — live namespace, only if a live matching invocation exists (conditional, non-root reader).** Candidate reads are `/proc/<pid>/mountinfo` and `/proc/<pid>/status` (CapEff/CapPrm/CapBnd) for a PID whose start time matches a D2 record. [inf] A uid-1000 reader is probably denied for a root-owned process (proc(5) ptrace-access rule; sweep not yet read). If denied, record `unknown: ptrace denied, operator-only`; do not fall back to host `findmnt`.

**D5 — static exposure cross-check (optional, unrun).** `systemd-analyze security <unit> --no-pager` is a read-only analysis of unit configuration. [inf] It should not start the unit. Verify that in the local `systemd-analyze(1)` page before citing it; not run here.

**D6 — host-namespace corroboration only (keep O3, relabelled).** `findmnt -R -n -o TARGET,VFS-OPTIONS,FS-OPTIONS /` with VFS and FS options separated (MatrixCriticR §6). Label it "host namespace, current, not the unit's namespace". It can show a superblock read-only state for `/`; it cannot exclude a unit-private remount.

**Residual, operator-only (not recommended this round):** observing the unit's real mount namespace requires a live invocation (`systemctl start` or `systemd-run`), which is state-changing or privileged. It stays `unknown`, with the operator discriminator: read `/proc/<live-pid>/mountinfo` during a fresh invocation, taking the PID from that invocation's journal record.

## 4. Claims these discriminators support (and do not)

- Supports: "as configured, the unit names no unit-side read-only path for `/`" (D1, dated, configured text).
- Supports: "the logged errno-13 records fall into N boot/invocation prefix pairs, and their issuer PIDs are dead or live" (D2+D3, counts only).
- Does not support: any statement about the built mount namespace, the issuer's CapEff, or the Btrfs ioctl ordering. Those stay `unknown`.
- Does not support: "stale ExecMainPID 1386 is the issuer." It is the completed watcher; the recorded issuer PID differs.

## 5. Suggested superseding notes for L1 (no edits made here)

1. MD `recheck:` line: remove `ps -o pid=,comm= -p 1386`; replace the systemctl list with D1; replace the unscoped journal `grep -c` with D2 and D3; label `findmnt` lines as host-namespace only.
2. JSON B2 `commands`: align with D1 and D6. The "not part of the captured property set" limit is closed for configured text by §2; the built namespace stays unmeasured.
3. JSON `host_observation.unit`: add only the path-view values in §2 as dated configured observations, with `exec_main_pid_stale: true`. Do not add ExecStart, environment or credential values.
4. Keep the round-12/13 corrections: `ProtectSystem=full` does not cover `/`, and the B2 alternative-path list stays. This seat adds no exclusivity claim.

## 6. Residual risks and gaps

- D2's `_SYSTEMD_INVOCATION_ID` presence on the failure records is unobserved; no journal body was read by this seat.
- D3 has no start-time match in the recipe; a `live` count is not attribution without that match.
- D4 ptrace denial is [inf] pending a proc(5) sweep.
- D5 not run; its behaviour is unverified here.
- The unit's built mount namespace (ProtectHome and related) remains unmeasured; no live invocation was started.
- ExecStart `+`/`!` prefix status is not re-read in this revision; round-12 R3 remains the only observation of it and is out of this seat's D1 scope.
- No PASS claimed. Author-side reading only; admission belongs to the parent.
