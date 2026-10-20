# Round-12 — Simplify (C1/C2 minimal-design review)

Seat: Simplify (simplifier, leaf). Scope: static review of the planned C1 (root metadata census arm) and C2 (EACCES decision matrix) shape against baseline HEAD `b76b5c3`. Evidence only. No census code, matrix, source row or test was written or run by this seat. Author-side seat evidence: **not** independent non-author verification.

Installs/updates by this seat: **none** (used existing `stat`, `ls`, `findmnt`, `getfacl`, `id`).

## 1. Commands run (read-only unless marked) and results

| # | Command | Exit | Observed |
|---|---|---|---|
| P1 | `id -u; id -un` | 0 | `1000` / `vgpnk` — the census's live process is non-root |
| P2 | `stat -c '%a %u:%g %F' /` | 0 | `555 0:0 directory` |
| P3 | `ls -ld / \| cut -c1-10` | 0 | `dr-xr-xr-x` (no `+` ACL marker) |
| P4 | `findmnt -n -o TARGET,FSTYPE /` | 0 | `/ btrfs` |
| P5 | `git status --porcelain` | 0 | only `?? .ufo/waves/round-12/`; `git rev-parse --short HEAD` = `b76b5c3` |
| P6 | Scratch ACL probe in `mktemp -d /tmp/simplify-acl-probe.*` (created, chmod 0555, `setfacl -m u:nobody:rwx`, then removed; cleanup rc=0) | 0 | `stat -c %a` → **`575`**; `stat -c %A` → `dr-xrwxr-x`; `ls -ld` → `dr-xrwxr-x+`; `getfacl -p` → `user::r-x`, `mask::rwx` |
| P7 | `read https://man.archlinux.org/man/acl.5` | — | ACCESS CHECK ALGORITHM step 1 (owner match → ACL_USER_OBJ only); CORRESPONDENCE section (owner bits ↔ ACL_USER_OBJ; group bits ↔ ACL_MASK when a mask exists). Not yet a `corpus/SOURCES.md` row. |
| G1 | grep/read of `tools/tsukuroi-census.sh` (lines 1–143, 326–355, 456–463, 529–685, 687–693, 1570–1666, 1757–1788, 2339–2403) | — | see §3 |
| G2 | grep of `tools/`, `SKILL.md`, `corpus/README.md` for JSON consumers | 0 | no reader of `corpus/knowledge/*.json` other than a documented one-liner `jq` check in `corpus/knowledge/adjacency-handoffs-fleet-r1.md:147` |

Not run: census `--selftest`, live census, any `systemctl show`, `btrfs`, `sudo`, `systemd-run`, pacman, or any command against a sibling repo. Those are other seats' or the operator's.

## 2. Planned shape reviewed

From `.ufo/waves/round-12/dispatch.json` task text (Planner/Census/Matrix/Simplify):

- **C1 (Census seat):** stat `/` via overridable `TSUKUROI_ROOT_DIR` (default `/`); append `root_mode= root_uid= root_gid=` to the packages note; owner-write absence → DEGRADED; unavailable/non-directory → BLOCKED; integrate before package early returns; wire override into every fixture; add 0555 / 0755 / inaccessible-or-missing / non-directory / non-root-ownership cases.
- **C2 (Matrix seat):** `corpus/knowledge/root-dac-decision-r12.md` + `.json`; ≥4 branches: DAC, read-only filesystem, service sandbox/capabilities, existing snapshot layout; JSON branch fields `id/evidence/interpretation/discriminator/limit/source_ids`; new source row for mkdir(2) requested.

## 3. Findings

### F1 — The existing seam for a sub-arm is already in `main()`; use it, do not edit the packages early returns (necessary simplification)
- `main()` folds the memory arm into the drivers verdict with `DRV_V=$(worse "$DRV_V" "$MEM_V")` (`tools/tsukuroi-census.sh:2371-2372`) and prints it as a suffix (`PLANE drivers: … mem=%s`, `:2379`). Comment at `:23-27` documents the "arm rides a plane line, no new plane id, rollup keys unchanged" convention.
- `probe_packages` has **six early returns** that overwrite `PKG_NOTE` (`:537`, `:542`, `:550`, `:558`, `:566`, `:571`) plus the final return (`:684`). Putting root fields into each path (as the Census task's "integrate before package early returns" literally reads) multiplies the drift surface.
- Minimal shape: `probe_root_arm` in `main()` (own `ROOT_V`/`ROOT_NOTE`), then `PKG_V=$(worse "$PKG_V" "$ROOT_V")` and `PKG_NOTE="$PKG_NOTE; $ROOT_NOTE"` before the `PLANE packages:` print at `:2377`. This makes the root observation visible on every packages path, including `pacman`-missing / `db.lck` / `-Qq` failure, with no change to those returns and no rollup edit.
- Risk if ignored: a 7th-site copy of the note in `probe_packages` will silently diverge from the other six.

### F2 — On this host the C1 verdict cannot move the live rollup or exit code (operability gain is observational live; verdict value is testability)
- Live packages plane is already `DEGRADED` from pacman drift (`PLANE packages: DEGRADED (pacman -Qkk rc=1 … drift=2[1password-beta,1password-cli] …)`, `.ufo/evidence/fleet-r1-interactive/live.json` line 10; rollup `DEGRADED`, exit 1 per `SKILL.md` census record).
- Worst-of rollup (`:2384-2392`) therefore absorbs a `root=DEGRADED`. Live effect of C1 = extra note fields only.
- Keep the DEGRADED arm anyway: without a verdict difference, the "isolated 0755 vs 0555 discrimination" claim can only be checked by string-matching a note, which is the test-count-as-quality pattern the ScoreReview seat is asked to avoid. The arm is cheap (one `if`).

### F3 — The owner-write verdict is a per-process claim the census cannot observe (wording risk, not a reason to drop the arm)
- The census runs as uid `1000` (P1). For that process `/` is judged by the *other* class (`other` bits `r-x`, P2) — no write, for any mode-only reason, regardless of root's capabilities.
- The planned DEGRADED reason ("owner-write absence") is only the owner class applied to a root process. Whether a root *service* can write `/` depends on its effective capabilities (CAP_DAC_OVERRIDE / CAP_DAC_READ_SEARCH), which are per-process and not visible to `stat` (ClaimCritic's falsifier). Source: `corpus/SOURCES.md:33` S027 (CAP_DAC_OVERRIDE bypasses DAC), `:40` S034 (root access uses permitted set).
- Required wording: the arm reports "owner write bit absent on `/` (DAC; root-service write additionally requires CAP_DAC_OVERRIDE/READ_SEARCH, not census-observable)". It must not say "root cannot write `/`" or "mount is read-only".

### F4 — ACL: omit from C1; never claim group/other write from `stat` octal (necessary caveat, simplifies C1)
- Owner bits always equal ACL_USER_OBJ (acl(5) CORRESPONDENCE; access algorithm step 1 for the owner match). So owner-write absence is ACL-robust for an owner-matching process.
- Group bits do **not** reflect the group entry when an ACL is present: P6 shows `stat %a = 575` while the ACL group-class value is the mask `rwx` and `user::r-x`. Any group/other-write claim from octal is wrong under ACLs.
- On this host `/` has no ACL (P3, no `+`), so ACL omission is exact here. If ACL presence is ever needed, `ls -ld` `+` suffix is the dependency-free flag (P6), not `getfacl`.
- C2 keeps ACL facts (`getfacl -p /`, already in RootLive's list); C1 does not.

### F5 — Dead planned advice vs necessary detail, C1
| Item | Verdict | Evidence / reason |
|---|---|---|
| `root_mode` (octal) | KEEP | required for the arm; QUALITY #13 requires root-directory mode reported separately (`corpus/QUALITY.md:17`) |
| `root_uid` | KEEP | selects which DAC class applies (owner vs other); P1/P2 |
| `root_gid` | KEEP (cosmetic cost) | not used by the verdict; `QUALITY #13` says "owner" (user:group); same `stat` format string, zero extra call. Do not let it drive a verdict. |
| ACL presence | DROP from C1 | F4 |
| Non-root ownership fixture case | DROP | cannot chown as uid 1000; not safely fixtureable; `uid` is already reported |
| "Unreadable/inaccessible" fixture case | DROP as separate case | as uid 1000 `stat /` never fails on this host; a chmod-000 parent is bypassed by root and cannot be created reliably by the selftest; the BLOCKED branch is the same `stat`-failure branch triggered by a **missing** `TSUKUROI_ROOT_DIR` path |
| Non-directory BLOCKED case | KEEP | a regular file as `TSUKUROI_ROOT_DIR` (real temp file, no stub) |
| Missing path BLOCKED case | KEEP | same `stat` failure branch as "unreadable" |
| 0755 HEALTHY case | KEEP | the discrimination baseline; no host-default 0755 requirement is asserted |
| 0555 DEGRADED case | KEEP, with fixture constraint | see F6 |
| `TSUKUROI_ROOT_DIR` seam | KEEP | `tools/tsukuroi-census.sh:326` "every host path is override-able" + `:327-355` `${TSUKUROI_*:-default}` convention |
| Separate `PLANE root` or new rollup key | DROP | format change; F1/F2 |
| Second DEGRADED for same root cause as update-safety rollback-net | NOTE only | `SKILL.md` update-safety row treats absent snapper net as DEGRADED; rollup is worst-of so no rollup change; C1 must not cite snapper as its reason |

### F6 — Selftest wiring: one seam, two hazards (necessary)
- Every probe case goes through `check()` (`tools/tsukuroi-census.sh:1757`); its `env` list at `:1763-1778` is the single place host paths are pinned. Add `TSUKUROI_ROOT_DIR="$FX/root"` there. The `env` command inherits the parent environment, so an operator-exported `TSUKUROI_ROOT_DIR` leaks into every case unless `check()` pins it. Pinning only in `fx_default` is not enough.
- `fx_default()` (`:1662`) is called by 78 sites (77 `case_home=` definitions). It must create `$d/root` as a **0755** directory so the default fixture stays HEALTHY and the existing 80-case baseline is preserved. Without it, a missing directory → BLOCKED → cascading failures.
- Hazard H1 (cleanup): `trap 'rm -rf -- "${work:-}"' EXIT INT TERM` (`:1574`). As uid 1000, `rm -rf` cannot unlink entries inside a `0555` directory. The 0555 fixture must be **empty** (or the trap must restore mode first). An empty directory's own mode does not block its removal (removal needs write on the parent).
- Hazard H2 (zero-mutation hash): `check()` hashes `$FX` before and after (`:1761`). Put the root fixture under `$FX` only if `fx_hash` covers directory mode; this seat did **not** read `fx_hash`'s definition — unverified, see §5.

### F7 — C2 matrix: only two live hypotheses; two planned branches are already measured negatives (depth risk: padding)
Live hypotheses (one mechanism, two conjunctive parts):
- **H-DAC:** `/` is `555 root:root` (P2) and the writer lacks CAP_DAC_OVERRIDE / CAP_DAC_READ_SEARCH → DAC denial. Discriminator: `stat -c '%a %U:%G' /` plus `ls -ld /` (no `+`). Sources: S027, S034.
- **H-CAP:** the unit's bounding set omits CAP_DAC_OVERRIDE (`CapabilityBoundingSet=CAP_SYS_ADMIN` in S020; `cap_sys_admin` in `corpus/knowledge/degraded-triage-r4.md:319-321`). Discriminator: `systemctl show limine-snapper-sync.service -p CapabilityBoundingSet,User,ProtectSystem,ReadOnlyPaths,ProtectHome` (read-only). Source: S028.
- H-DAC is necessary and H-CAP is its per-unit explanation; they are not two independent causes. Presenting them as four branches inflates the count.

Controls (not hypotheses; already measured negatives):
- **Read-only filesystem / subvolume:** refuted for this event — `btrfs property get -ts / → ro=false` and `ProtectSystem=no` (`degraded-triage-r4.md:319-323`); errno is 13 (EACCES) not 30 (EROFS) (`snapper-eacces-mechanism.md:11`). Keep one discriminator row: `findmnt -n -o OPTIONS /` (no `ro` flag measured in this seat — `P4` shows only target/fstype). Its job is to separate mount flags from DAC, not to be a live cause. Do not cite `S033`'s "mode 555 is a read-only mount" text (rejected; `SOURCES.md:39`).
- **Existing snapshot layout (`@.snapshots`):** refuted — `stat -c '%F %a %n' /.snapshots` reports no such file (`snapper-eacces-mechanism.md:12`), and the collision would give EEXIST, not EACCES. Already a rejected reading at `snapper-eacces-mechanism.md:17-19` (R6). Cite it; do not re-derive it as a branch.

Unknown (explicit residual, not a branch): LSM / AppArmor / SELinux confinement — the note says it was not tested (`snapper-eacces-mechanism.md:14`).

Honest count: 2 live (one conjunctive mechanism) + 2 measured controls + 1 unknown. Reaching "≥4 grounded branches" by listing controls as branches would be padding.

### F8 — Dead planned advice in C2
| Item | Verdict | Reason |
|---|---|---|
| `corpus/knowledge/root-dac-decision-r12.json` | DROP (single authority) | no reader in `tools/`, `SKILL.md`, `corpus/README.md` (G2); a sibling JSON duplicates the Markdown branch table = second authority (the target of this lane). Keep JSON only if a named counted check reads it. |
| Scenario inputs / expected classifications "grounded in real API errors" | SIMPLIFY | the only discriminating content is observation → branch → discriminator command → expected rc. The existing falsifier (`snapper-eacces-mechanism.md:23-30`: `systemd-run … test -w /` predicted rc=1; a 0 falsifies H-DAC/H-CAP) already carries it. |
| New source row for **mkdir(2)** | DROP unless a mkdir call is mapped | the observed failure is a btrfs subvolume create (`errno:13`, `btrfs_util_create_subvolume_fd() failed`, `degraded-triage-r4.md:314-315`), not mkdir; mkdir(2) does not bind that errno. EROFS-vs-EACCES ordering is not sourced by any registered row. If kept, it is a control-only anchor and its applicability to the btrfs path is `[unk]`. |
| Issues `omacom/omarchy#8047`, `#6629` | DROP from C2 | unopened leads (`SOURCES.md:73`); community text is not host truth; the two live hypotheses do not need them. Keep with the Origin/Issue seats' lane. |
| Re-open S027/S028/S034 | KEEP | these carry both live hypotheses |

### F9 — Scope/ownership
- The C2 matrix does not need any C1 output (the Matrix task's "independent of C1" holds): its branches use `stat`, `systemctl show`, `findmnt`, `btrfs property get` (operator-run for ro), and existing notes.
- ADJ-07 (tameshi method question for the blind spot) is not a dependency of C1's shape; it is a method note. Do not gate C1 on it (`PROVINCE.md:52`, `lessons/round-1.md:43` D6 "future census arm").

## 4. Recommended minimal shape (design only; parent decides)
1. C1: `probe_root_arm` in `main()` folded with `worse` into packages and appended to `PKG_NOTE` (F1). One `stat -c '%a %u %g %F' "$ROOT_DIR"` call; missing/non-directory/stat-failure → BLOCKED; owner-write bit absent → DEGRADED with the F3 wording; otherwise HEALTHY. Note field: `root_mode= root_uid= root_gid=`. No ACL, no new plane, no rollup change.
2. Override: `ROOT_DIR=${TSUKUROI_ROOT_DIR:-/}` next to `:327-355`; pin it in `check()`'s env list (`:1763-1778`); `fx_default` creates an empty 0755 `root` directory.
3. Selftest cases (4): root 0755 HEALTHY; root 0555 (empty dir) DEGRADED; root missing path BLOCKED; root regular file BLOCKED.
4. C2: one Markdown file, one table: 2 live branches (H-DAC conjunctive with H-CAP), 2 measured controls (RO, layout), 1 unknown (LSM); no JSON sidecar; no mkdir(2) row; no issue rows.

## 5. Risks and unverified items
- R1 (verdict overreach): DEGRADED on mode alone asserts a per-process property (F3). Mitigation: fixed wording.
- R2 (selftest leftover / flake): 0555 fixture must be empty (F6 H1); as non-root cleanup otherwise fails silently under `rm -rf` into `/tmp`.
- R3 (env leak): `env` inherits; pin in `check()` (F6).
- R4 (group-bit masking): `stat %a` shows mask under ACL (P6 575); no group claims from octal.
- R5 (double-count perception): update-safety already DEGRADED for absent rollback net; live rollup worst-of, so no rollup change (F2); do not cite snapper as C1 evidence.
- R6 (unsourced errno chain): EROFS/EEXIST/EACCES mapping for btrfs path is `[inf]`; no registered row binds it. Keep as inference with falsifier.
- R7 (unverified): `fx_hash` definition not read — whether it hashes directory mode (affects where the root fixture may live). Unrun.
- R8 (unverified): ACL-mask behavior was shown on a scratch directory only (P6), not on `/`; `/` has no `+` marker (P3). Unrun on `/` beyond P3.
- R9: `acl(5)` is cited from the live man page (P7) but is not a `corpus/SOURCES.md` row; any use in the knowledge note needs a registered row (lane owner's call).
- Unrun by this seat: census selftest, live census, any `systemctl show`, `btrfs property get`, `findmnt -n -o OPTIONS /`, `sudo`, `systemd-run`. All remain other seats' or operator's to run.

## 6. Judgment for parent (no PASS claimed)
- Design is sound only with F1 (fold, not per-return edits) and F3 (wording). Without them: scattered note edits (F1) and an overstated DEGRADED reason (F3).
- Depth: the C2 matrix reaches honest depth with 2 live + 2 measured controls + 1 unknown; a "4 branches" count is achievable only by padding (F7). Score impact belongs to ScoreReview; not judged here.
- Operability: C1's live effect is observational (F2). The gain is testable only through the 4 selftest cases in §4.3.
- Not an independent verification. Parent runs the census selftest and live census once after integration.
