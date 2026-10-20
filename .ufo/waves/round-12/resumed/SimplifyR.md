# Round-12 resumed — SimplifyR (C1/C2 minimal-design review)

Seat: TsukuroiR12.SimplifyR · leaf · evidence only · lane repo `tsukuroi-shokunin` · baseline HEAD `b76b5c3`.
Author-side seat evidence. **Not** independent non-author verification. This seat claims no PASS.
Writes: this file only. Installs/updates by this seat: none.
Not run: census `--selftest`, live census, the wave's `C2_command` jq check, sudo, systemd-run, btrfs, pacman, any host write.
Inherited `.ufo/waves/round-12/Simplify.md` read as historical data; not edited.
Filename: the task's `Report:` line names `resumed/SimplifyR.md` (used here); the acceptance line's `resumed/Simplify.md` was not used.

## 0. Pinned source state (moving during review)

| Artifact | State when read | Evidence |
|---|---|---|
| `tools/tsukuroi-census.sh` | C1 **landed, uncommitted**; md5 `fec91e3d535297f55c72d1e0661cc1de`, 2515 lines. HEAD blob md5 `945c76fc…`, 2402 lines | `md5sum`, `wc -l`, `git show HEAD:tools/tsukuroi-census.sh \| md5sum` |
| `corpus/knowledge/root-dac-decision-r12.md` | 91 lines, md5 `76340aa0…` | `md5sum`, `wc -l` |
| `corpus/knowledge/root-dac-decision-r12.json` | 316 lines, md5 `e62d9c0f…` | `md5sum`, `wc -l` |
| `SKILL.md` | modified by another seat, md5 `f4e1e9c6…`; `## Round 12 — root metadata…` at line 1676 | `git status --short` |
| `git status --short` at start | `?? .ufo/waves/round-12/`, `?? corpus/knowledge/root-dac-decision-r12.{json,md}`, `?? corpus/lessons/round-12.md`, `M corpus/QUALITY.md`, `M corpus/SOURCES.md` | `git status --short` |
| `git status --short` later | also `M tools/tsukuroi-census.sh`, `M SKILL.md`, `M PROVINCE.md`, `M corpus/README.md`, `M corpus/knowledge/snapper-eacces-mechanism.md` | `git status --short` |

The census changed three times during this review (`#4AD2` → `#3921` → `#3EB0`/`#B8D1`; md5 `e5695843…` → `fec91e3d…`). Line numbers below refer to md5 `fec91e3d…`. The parent must re-hash before trusting any line cite.

## 1. Commands and exit codes (read-only)

| # | Command | rc | Observed |
|---|---|---|---|
| R1 | `git status --short`; `git rev-parse --short HEAD` | 0 | HEAD `b76b5c3` |
| R2 | `stat -c '%a %u:%g %F' /`; `ls -ld /` | 0 | `555 0:0 directory`; `dr-xr-xr-x` (no `+`) |
| R3 | `findmnt -n -o TARGET,FSTYPE,OPTIONS /` | 0 | `/ btrfs rw,relatime,compress=zstd:3,ssd,…,subvol=/@` |
| R4 | `getfacl -p /` | 0 | `user::r-x`, `group::r-x`, `other::r-x` (base entries only) |
| R5 | `id -u`; `test -w /`; `test -x /` | 0 (test: w=1, x=0) | uid `1000`; write=no; x=yes |
| R6 | `systemctl show limine-snapper-sync.service -p User -p CapabilityBoundingSet -p AmbientCapabilities -p ProtectSystem -p ProtectHome -p ReadOnlyPaths -p ReadWritePaths -p NoNewPrivileges -p ActiveState` | 0 | `User=root`; `CapabilityBoundingSet=cap_sys_admin`; `AmbientCapabilities=` empty; `ProtectSystem=no`; `ProtectHome=yes`; `ReadOnlyPaths=` empty; `ReadWritePaths=/tmp`; `NoNewPrivileges=yes`; `ActiveState=inactive` |
| R7 | `systemctl list-unit-files 'limine*'`; `systemctl list-units --all 'limine*'` (names/states only) | 0 | `limine-snapper-sync.service` enabled; `limine-snapper-watcher.service` alias |
| R8 | `journalctl -o json -g 'create subvolume failed'` → `jq -r '[._SYSTEMD_UNIT,._COMM,._EXE]'` (metadata fields only; no message bodies recorded) | 0 | 9 entries, all `_SYSTEMD_UNIT=limine-snapper-sync.service` |
| R9 | `journalctl -o short-iso -g 'create subvolume failed' \| grep -c 'errno:13'` | 0 | `9` |
| R10 | `read` live man pages mkdir(2) and access(2) | — | quotes match S035 and S034 rows (§4) |
| R11 | `grep` / `md5sum` / `wc` / `read` of census header, arm, fixtures, `check()`; matrix MD/JSON; SKILL root section; lesson; QUALITY; SOURCES rows; `.ufo/evidence/fleet-r1-interactive/live.json` lines 9–10 | 0 | see sections 3–5 |
| R12 | `read` JSON with jq filter (`?q=`): `[.branches[] \| {id, has_all6, n_src}]`; `{scenarios, decision_steps, branch_count}` | — | `has_all6` true for B1–B4; `n_src` 3,2,3,1; scenarios 8; decision steps 6; branches 4 |

## 2. Verdicts for the parent (no PASS)

- **C1 landed shape: accept the shape; do not credit operability yet.** The arm is minimal, reuses existing seams, adds no plane and no rollup key, and edits no packages early return. **But no root-arm selftest case exists at md5 `fec91e3d`.** `grep` for `case_home='…root…'`, `check '…root…'`, `chmod 0555` / `0655`, and `root_finding=owner` finds nothing. The only hit is `healthy-nonroot-artifact` (`:2133`), a false match on "nonroot". The lesson requires "distinct hermetic 0755/0555/unavailable outcomes" (`corpus/lessons/round-12.md:24`). This is a **blocker for C1 PASS** until the cases land.
- **C2: accept.** Four branches, six procedure steps, eight scenarios. The JSON is read by the wave's own counted check (`.ufo/waves/round-12/before.json:3`, `C2_command`), so it is not dead. That check was not run here.

## 3. C1 — dead advice vs necessary detail (landed code, md5 `fec91e3d`)

Landed pieces: `probe_root_meta()` `:720-771`; header block `:91-105`; override `ROOT_DIR=${TSUKUROI_ROOT_DIR:-/}` `:353`; fold in `main` `:2459-2460` (`PKG_V=$(worse "$PKG_V" "$ROOT_V")`); emit `:2490` (`PLANE packages: %s (%s; %s)`); fixture `:1764` (`chmod 0755 "$d/root"`); `check()` pin `:1877`.

| Item | Verdict | Evidence / reason |
|---|---|---|
| Fold via `worse` after `probe_packages`, note composed at emit (`:2459-2460`, `:2490`) | KEEP (better than inherited F1) | None of the packages early returns (`:563, 568, 576, 583, 592, 597`) or the final return (`:710`) is edited; no PKG_NOTE threading |
| `cap` captures stdout+stderr (`:482-487`) | KEEP, required | The `why` mapping (`:729-733`) matches stderr text; without `2>&1` every failure would read `unknown` |
| `owner-search` bit (`:763`) | KEEP, needs a case | Not in the dispatch text (owner-write only), but QUALITY.md:20 (#15) says "owner-write/search bits" and SKILL.md:1685 says "owner write or search bit". No fixture exercises it |
| `root_euid` in note | KEEP (cheap) | Makes the uid-independence claim checkable. Risk: a reader may take it as a process claim; header `:100` says the verdict is uid-independent |
| `root_owner_write` / `root_owner_search` duplicate the mode digits | KEEP | They are the verdict inputs; SKILL.md:28-29 requires the observed value with each verdict |
| `root_type=symlink(unresolved)` (`:734-736`) and header claim "dangling link → BLOCKED" (`:101`) | DECIDE: add a one-line dangling-link fixture (`ln -s`, no privilege) or drop both | The header claims the outcome; no fixture tests it |
| `why` mapping arms `permission-denied` / `symlink-loop` / `no-such-path` (`:729-733`) | KEEP only with tests; otherwise collapse to a generic `stat-failed` | Only `no-such-path` is reachable from the planned cases |
| Header `:103`: "0575/0775/0751/1777/2755 with owner w+x are observations" | **FIX.** 0575 has owner `r-x` (no w). Code yields `DEGRADED owner-write-absent` for 0575 (`ow=(num&0200)`, `:760`) | Doc contradicts code |
| Header note format `:95-96` omits `root_dir=` | Minor doc fix | Code appends `root_dir=${ROOT_DIR@Q}` (`:769`) and in BLOCKED branches |
| `ROOT_V=BLOCKED ROOT_NOTE='probe not run'` default (`:463`) | Neutral | `main` always calls the probe; harmless `set -u` default |
| Fixture `chmod 0755 "$d/root"` (`:1764`) | KEEP, necessary | `umask 077` at `:340` makes a bare `mkdir` 0700. Inherited F6 missed this; the landed code handles it |
| `check()` pin `TSUKUROI_ROOT_DIR="$FX/root"` (`:1877`); `EXTRA_ENV` expands after it (`:1896`) | KEEP, necessary | The last assignment wins, so per-case override works. Without the pin, an operator export or the live `/` reaches fixtures |
| `fx_default "` call sites | 77 | `grep -c` = 77 (inherited F6 said 78) |

**Missing cases (recommended minimal set; not written here):**
1. `0755` → HEALTHY; assert `root_mode=755 root_owner_write=1 root_owner_search=1` and no `root_finding`.
2. `0555`, empty → DEGRADED; `root_finding=owner-write-absent`.
3. `0655`, empty → DEGRADED; `root_finding=owner-search-absent`.
4. Missing path (`EXTRA_ENV` `TSUKUROI_ROOT_DIR="$FX/no-root"`) → BLOCKED; `root_status=unavailable(stat=rc=1 errno=no-such-path)`. This is the "unavailable" outcome the lesson names.
5. Regular file → BLOCKED; `root_status=not-directory(type=regular file)`.
6. (optional) dangling symlink → BLOCKED; `root_type=symlink(unresolved)`.

Do not add a permission-denied case as a default. As uid 1000 it needs a non-searchable parent. Root (CAP_DAC_OVERRIDE) bypasses search, so the case is uid-dependent. The landed trap (`:1670`, `chmod -R u+rwx` before `rm -rf`) removes the cleanup hazard, so if the case is added it must say "skipped when run as root", not PASS.

**Zero-mutation hash (inherited R7 resolved):** `fx_hash` (`:1848-1856`) now digests `find -printf '%y %m %U %G %p'` plus regular-file content. Directory modes are covered, so the 0555/0655 fixture modes sit inside the proof.

**Live consequence (not run by this seat):** `/` is `555 root:root` (R2). The landed arm sets `root_finding=owner-write-absent`, which makes packages DEGRADED and the rollup DEGRADED with exit 1, **regardless of pacman**. The packages plane is already DEGRADED from pacman drift (`.ufo/evidence/fleet-r1-interactive/live.json` line 10: `drift=2[1password-beta,1password-cli]`; `exitCode` 1 at line 9; dated 2026-10-15, historical). If that drift clears, the root arm alone keeps the rollup at exit 1. The arm is therefore a standing verdict on this host, not observational. The defensible framing is "DEGRADED = named unresolved item, intent unverified" (SKILL.md:35), not "defect" (QUALITY #15 forbids universal mode policy). The parent must accept this knowingly.

## 4. C2 — current matrix

Verified facts:
- Host probes R2–R9 agree with the matrix §3 facts: `/` 555 root:root; `rw` mount; base-only ACL; unit `cap_sys_admin`; `ProtectSystem=no`; `test -w` rc=1 for uid 1000; errno:13 ×9.
- Snapper note line 11 reports 8 (last 2026-10-19T08:11:47); the matrix reports 9 (last 22:48:24). This is an older sweep, a drift and not a contradiction.
- Caller identification: all 9 `errno:13` entries are emitted by `limine-snapper-sync.service` (R8), the same unit whose bounding set the matrix reads. B3 names the right unit.
- Source quotes (live man pages, R10). mkdir(2) ERRORS (footer 2026-02-11): EACCES "The parent directory does not allow write permission to the process, or one of the directories in path did not allow search permission"; EEXIST; EROFS "path refers to a file on a read-only filesystem"; EPERM. These match the S035 row (`corpus/SOURCES.md:41`). access(2) DESCRIPTION: "for the root user, the check uses the set of permitted capabilities rather than the set of effective capabilities" matches S034 (`SOURCES.md:40`). S027 and S028 were not re-opened by this seat.
- Registry: S033 is REJECTED ("mode 555 read-only mount", `SOURCES.md:39`). #8047 and #6629 are now tier-C REJECTED rows S036 / S037 (`SOURCES.md:42-43`); the unopened-leads list is at `:76`.

| Item | Verdict | Reason |
|---|---|---|
| `root-dac-decision-r12.json` | KEEP | Inherited F8 "DROP, no reader" is superseded: `before.json:3` `C2_command` counts `.branches[]` on six field predicates. All four branches carry all six keys (R12) |
| MD §2 branch table (`root-dac-decision-r12.md:28-33`) | KEEP as index, or trim to a pointer | Duplicates JSON ids, families and sources. The MD itself says JSON is authoritative. Harmless |
| S035 mkdir row | KEEP (inherited DROP superseded) | Only registered source for the EROFS and EEXIST definitions (B2, B4). The matrix limits it to a control anchor and states that mkdir ≠ btrfs ioctl (md §5–6, R10). QUALITY #15 compliant |
| Four branches | ACCEPT | Two live (B1 DAC ∧ B3 capability, one conjunctive mechanism) and two controls (B2 RO, B4 existing target). Each branch has its own procedure step (1 target stat, 2 mount/ProtectSystem, 3 mode/ACL/search, 4 unit caps), so they discriminate rather than pad |
| Step 5 "explained" | ACCEPT the wording | Signal-consistency only. The matrix says "consistent, not proven" (md §4.6). The procedure never takes the observed errno as input; do not upgrade it to a classifier |
| Step 4 capabilities | ACCEPT with the stated limit | Configured unit text on an inactive unit (`ActiveState=inactive`), as md §3 says |
| R7 "0555 is not a ro mount" | KEEP | Matches QUALITY #15 and SKILL.md:1689 |

SKILL.md (another seat's uncommitted edit; not this seat's file): the root table at `SKILL.md:1683-1687` row 1 says "Named metadata concern" with no verdict word; the code says DEGRADED. Align it to "DEGRADED: owner-write or owner-search bit absent". Row 1 also says "owner-identity caller", which is unclear.

## 5. Inherited `Simplify.md` — reuse / reject / correct (historical; not edited)

| Inherited claim | Status now | Evidence |
|---|---|---|
| F1 fold, not per-return edits | REUSED (landed as emit-time composition) | `:2459-2460`, `:2490` |
| F2 "C1 cannot move the live rollup" | CORRECTED. It holds only while pacman drift keeps packages DEGRADED; the root arm can set packages DEGRADED alone | §3 live consequence; `live.json:9-10` |
| F3 owner-write wording | SUPERSEDED. The landed arm reports owner-write and owner-search bit facts (QUALITY #15 wording) | QUALITY.md:20; census `:717-719` |
| F4 ACL omitted from C1 | REUSED | no `getfacl` in the landed arm |
| F5 `root_uid` "selects which DAC class applies" | REJECTED. The verdict is uid-independent and mode-only | `:762-767`; census header `:100` |
| F5 `root_gid` cosmetic | REUSED | kept |
| F5 unreadable-case DROP | REUSED, reason corrected. A stat EACCES comes from a non-searchable path prefix (S034: "search permission… path prefix"), not from the directory's own mode. Root bypass makes it uid-dependent. The trap now restores modes | `:1670`; S034 |
| F6 "78 `fx_default` sites" | CORRECTED to 77 | `grep -c` |
| F6 H2 / R7 "fx_hash: does it cover directory mode?" | RESOLVED: covered | `:1848-1856` |
| F6 H1 cleanup hazard | RESOLVED by the landed trap | `:1670` |
| F6 "fixture creates 0755" | CORRECTED: explicit `chmod 0755` is required because of `umask 077` | `:340`; landed `:1764` |
| F7 "errno 13 not 30" cited to snapper note:11 | CORRECTED cite: errno:13 wording is `degraded-triage-r4.md:315`; ro refutation (`ro=false`) is `:322`. Snapper note line 11 is the journal count | `degraded-triage-r4.md:315,322` |
| F7 2 live + 2 controls + 1 unknown | REUSED | the matrix matches |
| F8 JSON DROP | REJECTED | `before.json:3` |
| F8 mkdir row DROP | REJECTED. Kept as a control anchor | §4 |
| F8 issues "unopened leads (SOURCES.md:73)" | CORRECTED: leads at `:76`; #8047 / #6629 are now REJECTED tier-C S036 / S037 at `:42-43` | `SOURCES.md` |
| F9 C2 independent of C1 | REUSED. The matrix reads no census artifact | matrix §1 |

## 6. Risks and open items

- **R-A (blocker):** no root-arm selftest cases at `fec91e3d`; C1 operability is uncredited.
- **R-B:** header `:103` example list is false for 0575. Doc-only, but it is the arm's own definition.
- **R-C:** standing DEGRADED for `/` at 555 on this host (§3). Accept knowingly, or reword as a named unresolved item.
- **R-D:** the SKILL.md root table lacks a verdict word and its wording differs from the code (§4). Not this seat's file.
- **R-E:** the census moved three times during this review. Re-hash at integration.
- **R-F [unk]:** the falsifier `systemd-run … test -w /` (`snapper-eacces-mechanism.md:26`) relies on `test` being resolved by execve (no shell), so coreutils `test` is used, whose `access(2)` path follows the permitted-set behaviour (S034). Not verified here; belongs to the Capabilities seat.
- **R-G:** adding the cases changes the selftest case count. Any pinned expected-count line in docs becomes history.

## 7. Judgment for parent

- **C1:** shape accepted. PASS withheld until ≥5 root cases exist and pass in the parent's single selftest run. Fix header `:103`. Give the owner-search row a case.
- **C2:** accepted. JSON kept; mkdir row kept. This seat claims no depth PASS. The wave's counted check (`before.json` `C2_command`) is the parent's to run once.
- **Not an independent verification.** The parent runs `bash tools/tsukuroi-census.sh --selftest` and the live census once after integration, and re-hashes the census and matrix.
