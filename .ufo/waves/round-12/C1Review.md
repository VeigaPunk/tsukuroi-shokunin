# C1Review — round-12 C1 (root metadata / census blind spot) — static review

Status: PRE-IMPLEMENTATION REVIEW. The C1 implementation is NOT visible at review time.
- `git status --short` → `?? .ufo/waves/round-12/` only; `git diff --stat` → empty (HEAD b76b5c377eaee3e3d8d47fdddde977828d05dbd5).
- `sha256sum tools/tsukuroi-census.sh` → `1045244387ffcd5d…` (first 16 hex); `grep -c "ROOT_DIR\|root_mode" tools/tsukuroi-census.sh` → `0`.
- No tests, selftests, builds or census runs were executed (assignment: no tests while implementation active).
- Nothing below is a PASS. Every item is a contract/seam finding or a checklist item for the landed revision.

Scope read: `.ufo/waves/round-12/spec.json` (C1 items: Census, Planner, ClaimCritic, C1Review; context Contract),
`tools/tsukuroi-census.sh` (header 299-325, helpers 455-530, `probe_packages` 530-685, `run_selftest`
1570-1808 incl. `fx_default` 1662-1746 and `check()` 1757-1809, main 2339-2403), `corpus/QUALITY.md` item 13
(QUALITY.md:17), `corpus/lessons/round-1.md` D3/D6 (lessons table line 40, 43).

## Host facts measured (read-only)

| probe | result | exit |
|---|---|---|
| `stat -c '%A %a %U:%G %n' /` | `dr-xr-xr-x 555 root:root /` | 0 |
| `stat -c 'mode=%a uid=%u gid=%g type=%F' /` | `mode=555 uid=0 gid=0 type=directory` | 0 |
| `id -u` (census user) | `1000` | 0 |
| `getfacl -p /` (head -5) | `user::r-x`, `group::r-x`; no named entries in the shown lines (`other::` line not captured by head) | 0 (pipe rc) |
| `umask 077; mkdir sub; stat` in a mktemp dir (temp dir removed) | `mode=700` | 0 |
| `git status --short` / `git diff --stat` | untracked `.ufo/waves/round-12/` only / empty | 0 |

Tools installed or updated by this seat: none. (`stat` 0.8.0, `getfacl` at /usr/bin/getfacl already present.)

## Findings (ordered by severity)

### F1 — HIGH (contract): literal "owner-write absence → DEGRADED" degrades the measured-healthy host
- Spec (Census/Planner): "worsen verdict for missing owner write/search as named DEGRADED"; Planner: "Owner-write absence DEGRADED".
- Live `/` is `555 root:root` (table above) and the census runs as uid 1000, a non-owner. The owner-write bit does not govern this process's access to `/`.
- Literal reading → the live rollup becomes `packages=DEGRADED` and exit 1 on a host whose `/` mode is the measured normal state. That is an operability regression and the exact "unsupported default" the contract forbids, now via the owner bit instead of 0755.
- ClaimCritic falsifier (spec) is confirmed by this measurement: 0555 is not, by itself, unhealthy.
- Proposed discriminator (parent owns the judgment): DEGRADED only when the probing euid equals the owner uid AND owner-write (0200) or owner-search (0100, dirs) is absent. Non-owned dirs: fact printed, no DEGRADED. Missing/unreadable/non-directory: BLOCKED.
  - Why owner-only: `acl(5)` (`man -P cat 5 acl`, lines 81-89) maps owner permissions to ACL_USER_OBJ, which `stat %a` reports exactly; group bits in `%a` show the ACL_MASK, and named ACL_USER entries are invisible to `%a`. So an owner-bit reading is exact only for the owner; a non-owner write-absence reading from `%a` is not proof of denial (see F9).
- Tradeoff to record: with owner-only DEGRADED, the root-owned live `/` and a 0755 root-owned `/` produce the same verdict and differ only in the note. That is the honest outcome; the C1 "discrimination" then lives in the printed `root_mode=` field, not the verdict.

### F2 — HIGH (seam): early returns in `probe_packages` overwrite any note appended before them
- Lines 536, 541, 549, 556, 565, 570 assign `PKG_NOTE=` (plain assignment, not append). Any `root_mode=` text placed into `PKG_NOTE` before those returns is erased in exactly the pacman-failure cases the contract says must show the blind spot ("integrate before package early returns so blind spot visible even when pacman fails").
- Line 675 also reassigns `PKG_NOTE` from scratch on the success path.
- Required shape: keep root evidence in its own variables (e.g. `ROOT_V`, `ROOT_NOTE`) and compose the packages line in `main` (where `printf 'PLANE packages: %s (%s)\n'` lives, ~2377), so every early return is covered by construction. Do not thread the root note through `PKG_NOTE`.

### F3 — HIGH (seam, fail-open): verdict downgrade overwrites a root BLOCKED
- Lines 678, 681, 683 assign `PKG_V=DEGRADED` unconditionally. Line 531 resets `PKG_V=HEALTHY` at probe start.
- Fail-open path: if the root probe sets `PKG_V=BLOCKED` before `probe_packages` (line 531 resets it → lost) or inside it before 678/681/683 (→ downgraded to DEGRADED), then a clean pacman sample with an unreadable root reads DEGRADED, not BLOCKED. "Unreadable metadata BLOCKED" (Planner) is not honoured.
- Existing precedent to reuse: `main` folds the mem arm with `DRV_V=$(worse "$DRV_V" "$MEM_V")` (line 2372). Use the same fold: `PKG_V=$(worse "$PKG_V" "$ROOT_V")` in `main` after `probe_packages`, not inside it.

### F4 — HIGH (hermetic fixture): `umask 077` makes a bare fixture root 0700, not 0755
- `set -euo pipefail` + `umask 077` at line 320-321 apply to `run_selftest`. Verified: `umask 077; mkdir` → mode 700.
- The contract's "fixture root (0755 dir)" requires an explicit `chmod 755` on the fixture root. Without it: a healthy-case assertion on `root_mode=0755` fails for the wrong reason, or, worse, a 0700 fixture is read as "owner-write present" and the 0555 degraded case is built on the wrong base.
- Also: any `chmod` must run only on fixture paths; never on the live root.

### F5 — MEDIUM (hermetic isolation): where the root override must live
- `check()` builds the env at lines 1763-1788: fixed `TSUKUROI_*` assignments, then `"${EXTRA_ENV[@]}"`. `EXTRA_ENV` is reset per case (1756, 1808) and several cases overwrite it wholesale (e.g. lines 1892, 1916, 2058, 2112, 2117, 2122, 2201, 2239, 2281, 2286, 2290-series).
- If `TSUKUROI_ROOT_DIR` is set through `EXTRA_ENV` or only in `fx_default`, every case that assigns `EXTRA_ENV` (and the ones that set none) can leak to the live `/`.
- Required: put `TSUKUROI_ROOT_DIR="$FX/root"` in the common block of `check()` (above `"${EXTRA_ENV[@]}"`), so per-case overrides can still replace it deliberately.
- Detection gap: the only host-leak guard, line 1793 (`host=fixture-host`), checks the hostname, not the root. A root leak is caught only if the root-bearing regexes pin fixture-specific values (see F8).

### F6 — MEDIUM (cleanup): non-writable fixture dirs leave residue
- Trap at line 1574: `rm -rf -- "$work"`. Removing entries of a directory requires write permission on that directory (POSIX unlink semantics) [INFERENCE: not executed here]. A fixture root at 0555 or 0000 that holds children will not be emptied by `rm -rf` as the owner; cleanup fails silently and `/tmp/tsukuroi-r3-2-selftest.*` residue remains. Non-root runs are the only case where this matters, but the selftest is designed for non-root.
- Required: keep non-writable fixture dirs empty, or restore `u+w` on fixture dirs before the trap's `rm -rf`.

### F7 — MEDIUM (probe semantics + exit map): `-d` vs `stat` symlink disagreement; bare `stat` under `set -e`
- `[ -d "$root" ]` follows symlinks; plain `stat` does not. A symlinked `TSUKUROI_ROOT_DIR` would be `directory` to `[ -d ]` but `symbolic link` to plain `stat` → spurious BLOCKED (fail-closed, but wrong). Use `stat -L` everywhere.
- Under `set -euo pipefail` (line 320), a bare `root_meta=$(stat …)` that fails exits the script with that command's rc (1 for ENOENT). Exit 1 is the DEGRADED code in the exit map (`main`, 2395-2400), and the rollup line is never printed. That is a fail-open at the exit-code level.
- Required: all stat calls via `cap` (lines 456-461, `set +e` wrapper), never bare command substitution.

### F8 — MEDIUM (test validity): root-run and uid-dependent expectations
- Fixture dirs are owned by the running user (uid 1000 here, 0 under sudo). A regex pinning `root_uid=0` fails on the fixture; a regex pinning `root_uid=$(id -u)` is correct. Under root (uid 0), a `chmod 000` parent makes `stat` succeed (CAP_DAC_OVERRIDE) and turns an "unreadable" case vacuous.
- Deterministic unreadable case: a dangling symlink as `TSUKUROI_ROOT_DIR` (`stat -L` → ENOENT, rc≠0) is uid-independent → BLOCKED. Use the 000-parent case only behind an explicit `[ "$(id -u)" -ne 0 ]` guard that records a named skip, never a pass.
- "non-root ownership if safely fixtureable": a uid 1000 user cannot create a fixture owned by another uid without root. Owner≠probe-user is not fixtureable non-root; say so in the case label rather than asserting it.
- Every root-bearing case should pin `root_mode=<fixture mode>` and `root_uid=$(id -u)` so a leak to live `/` (555/0) fails the regex.

### F9 — MEDIUM (arithmetic / special modes): octal and sticky-bit mistakes
- `%a` is an octal string. `$((mode & 0200))` on the text "555" evaluates decimal 555 and tests the wrong bit. Required: `$((8#$mode & 0200))` (and `0100` for owner-search).
- `%a` can be four digits (`1777`, `2755`, `4755`). Strip or mask via `8#`; never slice the last three characters by string length.
- Required fixture coverage: `1777` (owner-write present, sticky set) must not read as a special-bit failure; `2755` must not change owner-write.
- MutationPlan target "inverted write-bit" is the case this catches.

### F10 — MEDIUM (root process): root's own DAC is not owner-bit-limited
- Under `sudo` (euid 0), DAC write checks are bypassed for CAP_DAC_OVERRIDE [INFERENCE from capabilities(7) semantics; not read in this seat]. Owner-write absence on a root-owned dir then never blocks the census. The F1 owned-only rule would still fire (euid 0 owns `/`), so it needs an explicit euid-0 exclusion: euid 0 → observation only, no DEGRADED for owner-write absence.
- Record euid in the root note (`root_euid=`) so a consumer can tell the two runs apart.

### F11 — LOW (verdict hygiene): empty verdict through `worse`
- `rank` returns 9 for any unknown value, including `""`. `worse HEALTHY ""` prints `""`, producing `TSUKUROI_CENSUS:  (…)` with exit 2 (`*) exit 2`). Safe exit, malformed line.
- Required: declare `ROOT_V=BLOCKED ROOT_NOTE='probe not run'` with the existing shared-state pattern (lines 427-433) so the probe must overwrite it.

### F12 — LOW (docs in header): `TSUKUROI_ROOT_DIR` absent from the env list
- The env-var seam list at lines 293-308 does not name `TSUKUROI_ROOT_DIR`. The spec says "do not touch docs", but this is a script header comment that documents the seam. Add it to the same block so the hermetic override is discoverable.

## Required regression cases (consumer-visible, hermetic; the implementation must pass these, the parent runs them once)
1. `healthy-root-0755`: fixture root 0755 owned by probe uid → `PLANE packages` contains `root_mode=0755 root_uid=<id -u> root_gid=<id -g>`; verdict unchanged.
2. `degraded-root-0555-owned`: fixture root 0555 owned by probe uid → DEGRADED with named owner-write absence; `root_mode=0555` pinned.
3. `healthy-root-0555-not-owned`: only reachable as a non-owned fixture; if not fixtureable non-root, record as a named skip with the reason, not a pass.
4. `blocked-root-missing`: nonexistent path → BLOCKED; root note present.
5. `blocked-root-dangling-link`: dangling symlink → BLOCKED (uid-independent).
6. `blocked-root-nondir`: regular file → BLOCKED (`[ -d ]` and `stat -L %F` agree).
7. `blocked-root-visible-on-pacman-fail`: copy of `blocked-empty-pkgdb` (line 2017) also asserting `root_mode=` appears on the `PLANE packages` line.
8. `healthy-root-special-mode`: fixture root 1777 owned by probe uid → owner-write present, no special-bit DEGRADED.
9. `degraded-root-euid0` (only if the case is run as root; otherwise a named skip): owner-write absent under euid 0 → observation only, no DEGRADED.
10. Rollup shape (existing `blocked-rollup-mixed` at line 2316): still exact six-field line; no new field.

## Verification gaps
- No implementation reviewed (see Status). Every F-item above is a contract or seam finding against the unmodified script plus the spec; each must be re-checked against the landed diff once the parent sends readiness.
- `getfacl -p /` output was truncated by `head -5`; the `other::` entry was not observed.
- Live `/` observed once at 2026-10-19; it is one sample, not a trend.
- F6 (unlink semantics), F10 (CAP_DAC_OVERRIDE) are [INFERENCE] from POSIX/Linux semantics, not verified by an execution in this seat.
- No tests, selftests or census runs executed; no sudo, no host writes, no installs.

## Outcome
Contract literal (owner-write absence → DEGRADED, no owner gate) is unsafe on the measured host: F1. Seam-level fail-open risks F2-F4 must be designed out before any implementation lands; F5-F9 are required for the hermetic cases to be real. No PASS is claimed for C1.

## Parent contract clarification (IRC from Main, received after the review above)
- F1 proposal (owner-only DEGRADED gate) NOT adopted. Parent decision: owner-write/search absence on the root directory is a named unresolved review item (DEGRADED), regardless of the probing uid's ownership. Rationale recorded by parent: census uid 1000 measures a root-owned `/` that a root service uses, so the owner gate would miss the known risk. DEGRADED means "named owner-write/search review", not "corrupt" and not "unhealthy by a universal 0755 baseline".
- F10 proposal (euid-0 observation-only) NOT adopted: no blanket root capability bypass, since capabilities are process-bound. Consequence to keep in view: under euid 0 the owner-write bit does not block that process, so a DEGRADED there is a review flag, not a proven denial. Record `root_euid=` in the note so the run is distinguishable.
- Intentional modes, capabilities and ACL limits must be documented by the parent (not by this seat).
- Forwarded and still binding: F2 (early-return note overwrite), F3 (worse-fold, no unconditional PKG_V downgrade), F4 (explicit chmod on 0755 fixture under umask 077), F5 (root override in check() common env), F7 (stat -L, cap-wrapped stat under set -e), F9 (8# octal, four-digit modes).
- Residual risk accepted by parent: a non-owner 0555 root will read DEGRADED on the live host until the review item is resolved or documented. Final static review of the landed implementation is pending the Census readiness ping.
