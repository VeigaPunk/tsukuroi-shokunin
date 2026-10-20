# FixtureReviewR — round-12 resumed selftest architecture review (seat: FixtureReviewR)

Scope: census selftest architecture; cases that kill `missing-root-probe` and wrong-octal-bit mutants; fixture root off the live `/`; 80-case baseline protection.
Status: **static review only. No selftest, census, mutant, or fixture run.** Author-side seat evidence, not independent verification. Nothing here is a PASS.
Supersedes the inherited `.ufo/waves/round-12/FixtureReview.md` (historical). Corrections to it are in §0.

## 0. Corrections to the inherited FixtureReview.md

| Inherited | Current evidence |
|---|---|
| Seam named `TSUKUROI_ROOT_PATH` | Landed header names **`TSUKUROI_ROOT_DIR`** (`tools/tsukuroi-census.sh:311`, `:350` `ROOT_DIR=${TSUKUROI_ROOT_DIR:-/}`). Use that. |
| Default fixture root `0751` | Spec and landed contract say **0755** (`.ufo/waves/round-12/spec.json` Census item). Keep 0751 out of the default. |
| `0744` = "owner-search absent" (MutationPlan.md) | **Wrong.** 0744 owner = `7` (rwx), so owner-search is present. Owner-search-absent needs owner digit without x, e.g. `0655`. Verified by arithmetic §3. |
| Missing path does not reach the stat-failure arm, so M3 needs a `stat` shim (MutationPlan.md) | Holds only if Census keeps a `-d` pre-check. Landed header is one `stat -L` call. Recommendation §4-R1: keep a single `stat -L` as the only validator; then the missing-path case reaches the failure arm and no shim is needed. |
| Trap cleanup needs `chmod -R` for `locked/` | Confirmed (§2-F2), and `fx_hash` also aborts under `pipefail` (new, §2-F1). |

## 1. Evidence base (this seat, read-only or arithmetic)

| # | Probe | Result | Exit |
|---|---|---|---|
| E1 | `grep -cE "^\s+check(_cli)? '" tools/tsukuroi-census.sh` at HEAD b76b5c3 | 80 | 0 |
| E2 | `git status --short tools/` (now) | ` M tools/tsukuroi-census.sh`, +23 lines, header and globals only (`:293-311`, `:350`, `:460`). **No probe function, no `check()` root pin, no root case yet.** Census is mid-landing; line numbers below for `check()`/`fx_*` are HEAD (`b76b5c3`), not the dirty tree. | 0 |
| E3 | Umask: `sed -n` of `tools/tsukuroi-census.sh:320-321` | `set -euo pipefail` and `umask 077` apply to the whole script, including `run_selftest`. Bare `mkdir` in a fixture gives 0700. | — |
| E4 | `stat -c '%a %F' <symlink-to-0751-dir>` (no `-L`) vs `stat -L -c '%a %F'` (temp dir in /tmp, removed) | plain: `777 symbolic link`; `-L`: `751 directory` | 0 |
| E5 | `stat -L` of child of a `chmod 000` parent (non-root uid 1000) | `Permission denied`, rc=1 | 1 |
| E6 | `stat -L` of a dangling symlink | `No such file or directory`, rc=1 | 1 |
| E7 | `chmod 000 dir` then `stat -c '%a %F' dir` (non-root) | `0 directory`, rc=0 — stat of a 000 directory itself succeeds | 0 |
| E8 | Pipeline shaped like `fx_hash` (`find … -type f -exec sha256sum {} + \| sort \| sha256sum \| cut`) under `set -euo pipefail`, one child 000 | `find: Permission denied`; `x=$(fx_hash …)` aborts the shell; the echo after the assignment is **not reached**; subshell rc=1 | 1 |
| E9 | `chmod -R u+rwx` on a tree whose parent is 000 with a child, then `rm -rf` | chmod rc=0, rm rc=0, path gone | 0 |
| E10 | Arithmetic-only owner-bit kill table (§3) | integer ops only; no fixture built | — |

Host `/` (read earlier by sibling seats, not re-measured here): `555 root root`. Not used as an oracle below.

## 2. Architecture findings (ordered by severity)

### F1 — HIGH (harness abort): `fx_hash` kills the whole selftest on any unreadable fixture subtree
- Evidence: E8. `fx_hash` at HEAD `tools/tsukuroi-census.sh:1748`: `find "$1" -type f -exec sha256sum {} + | LC_ALL=C sort | sha256sum | cut -d' ' -f1`. `check()` calls `before=$(fx_hash "$FX")` at HEAD `:1761` and `fx_no_mutation` at `:1807` with `set -e` active (`:320`). A 000 directory anywhere under `$FX` gives `find` rc=1, pipefail propagates it, and the assignment aborts the script. Output: no `TSUKUROI_CENSUS_SELFTEST:` summary, no PASS or FAIL count. The mutant run then reads as a crash, not as a verdict.
- Consequence for the planned cases: U1 (0000 root), U2 (locked parent) would abort the suite. They must not be added until F1 is fixed.
- Fix (harness only, no production change):
  ```bash
  fx_hash() { { find "$1" -printf '%p %m %y %U %G\n' 2>&1 || true; } | LC_ALL=C sort | sha256sum | cut -d' ' -f1; }
  ```
  - `2>&1` puts find's error lines into the hash input, so an unreadable subtree is recorded instead of silently skipped.
  - `-printf '%p %m %y %U %G'` also hashes modes, types and owners. Zero-mutation then covers metadata as well as content (the inherited A6 gap). It changes the before/after digest for all 80 legacy cases but not their outcomes: the census never writes, so before equals after either way. Verify by reasoning only; no run was made.

### F2 — HIGH (cleanup residue): trap `rm -rf` cannot empty non-writable or unreadable fixture dirs
- Evidence: trap at HEAD `:1574`: `trap 'rm -rf -- "${work:-}"' EXIT INT TERM`. E9 shows `chmod -R u+rwx` before `rm -rf` clears a 000 parent holding a child. Without it, `rm` cannot list the directory and `/tmp/tsukuroi-r3-2-selftest.*` is left behind.
- Fix: `trap 'chmod -R u+rwx -- "${work:-}" 2>/dev/null || true; rm -rf -- "${work:-}"' EXIT INT TERM`. This only touches the `mktemp -d` tree.
- Note: the `rm` status never reaches the script exit status (EXIT trap), so the existing trap cannot fail a run; it only leaks.

### F3 — HIGH (hermetic isolation): nothing in the output proves the probe read the fixture root, so a live-root leak can pass
- Landed header (`tools/tsukuroi-census.sh:93-101`) prints `root_status=ok root_mode= root_uid= root_gid= root_euid= root_owner_write= root_owner_search=`. It does **not** print the path.
- Hazard: on a host whose `/` is `0755 root:root` (the usual Linux default) and a selftest run as uid 0, fixture root (`0755`, owner 0, group 0) and live root print identical tokens. A leak to `/` passes every token assertion. The host guard at HEAD `:1793` (`host=fixture-host`) checks hostname only.
- Fix, two parts:
  1. Census prints `root=<path>` in the same note (ClaimCritic.md:116 proposed it). It is a private `mktemp` path, so it is safe to print.
  2. Every root-bearing assertion pins `root=$FX/root ` (trailing space). `FX` is unique per case under `$work`, so a leak cannot match.
- Harness pin: in `check()`, add `TSUKUROI_ROOT_DIR="$FX/root"` to the fixed `env` block above `"${EXTRA_ENV[@]}"` (after `TSUKUROI_EXPAC` at HEAD `:1786`). Per-case overrides stay possible; cases that replace `EXTRA_ENV` (`:1892`, `:1916`, `:1941`, …) cannot unset it. Putting it only in `fx_default` would leak through every case that sets `EXTRA_ENV`.
- Optional guard in `check()`: `case "$FX" in "$work"/*) ;; *) bad "fixture outside work dir ($FX)" ;; esac`. Harness-only; no legacy outcome changes.
- Do **not** add a case that sets `TSUKUROI_ROOT_DIR=/`. That reads host state and breaks the zero-host-read guarantee in the header (`:290-295`).

### F4 — HIGH (fixture mode): `umask 077` makes an unmodified root fixture 0700
- E3. `fx_default` must `chmod 0755 "$d/root"` explicitly. Without it the healthy-case assertion reads `root_mode=700` for the wrong reason. Also note: `root_mode` 700 is still HEALTHY, so the verdict alone would not show the error.
- `fx_default` should create the root empty. Any child under it would make cleanup and hashing depend on contents.

### F5 — HIGH (missing-root-probe kill power): every legacy case is blind to the root arm
- All 80 legacy `check` lines assert verdict and/or regexes that tolerate an extra field (`.*`; anchored prefixes at HEAD `:2135`; rollup `\)$` at `:2319`). None mentions `root_`. Removing the probe leaves all 80 green. Kill power for missing-root-probe therefore comes only from new cases with exact root tokens.
- The new cases must check the **packages line** (`^PLANE packages:`), not `grep` anywhere in the output. The `check()` regex loop greps the whole output, so a token on another line would match.
- Kill check: a missing probe removes `root_status=` and all root tokens. The healthy case (§4-C1) fails on that alone. Also each DEGRADED/BLOCKED case fails on its token.

### F6 — MEDIUM (fold / early returns): root evidence must survive every packages early return
- Landed header says the root note is composed at emit time, "never through PKG_NOTE". Early returns at HEAD `:541`, `:549`, `:556`, `:565`, `:570` set `PKG_V`/`PKG_NOTE` and return; with `probe_packages` `PKG_V=HEALTHY` reset at `:531`. Any root verdict set inside `probe_packages` would be lost (reset at `:531`) or overwritten (`:678`, `:681`, `:683` assign `PKG_V=DEGRADED` unconditionally).
- Required: the verdict fold lives in `main()` (`PKG_V=$(worse "$PKG_V" "$ROOT_V")` after `probe_packages`, same shape as `DRV_V` at HEAD `:2372`). Cases in §4-C17–C19 kill: (a) probe moved after returns, (b) root BLOCKED overwritten by packages DEGRADED, (c) fold dropped.

### F7 — MEDIUM (stat semantics): symlink and type parsing
- E4: without `-L`, `stat` reports the link (`777 symbolic link`), so a symlink-to-directory reads as non-directory; with `-L` it reports the target. The landed header says `stat -L`. Keep it.
- E5/E6: EACCES and ENOENT both give rc=1 with no stdout. A single `stat -L -c '%a %u %g %F'` call handles missing, dangling and unreadable identically (BLOCKED) with no `-d` gate.
- Type check: `%F` must equal `directory`. A regular file (0755, otherwise healthy) is the only case that proves the type check exists.

### F8 — MEDIUM (M3 realisation): choose a single `stat` as the sole validator, or a shim is required
- If Census keeps `[ -d "$ROOT_DIR" ]` before `stat`, a missing path never reaches the stat-failure arm (the MutationPlan.md M3 objection). Then the only way to kill "ignore unknown" is a `stat` shim.
- If Census uses one `stat -L` (recommended, §4-R1), the missing-path case *is* the stat-failure arm. A mutant that falls through there leaves no verdict/token and fails `blocked-root-missing`. No shim is needed, and the shim's own risk (it could mask a real stat call) disappears.

### F9 — MEDIUM (unreadable cases): U1 is uid-independent; U2 is not
- U1 (`0000` root, E7): stat of the directory itself succeeds for every uid. Expected `root_status=ok`, `root_mode=0`, both owner bits 0, DEGRADED. Uid-independent, so it stays. Kills a mutant that maps mode 0 to "unavailable".
- U2 (child of a 000 parent, E5): EACCES only for a non-root uid. Under root the stat succeeds and the case is a false negative. Guard: `if [ "$(id -u)" -eq 0 ]; then <skip line>; else <case>; fi`. The skip line must not count as PASS (§2-F11). U2 adds no branch beyond E6: both are stat rc≠0 → BLOCKED. Keep it only if Census emits distinct reason tokens for EACCES versus ENOENT.

### F10 — LOW (format conflict): `root_mode` spelling
- Landed header: `root_mode=<%a>` (unpadded, e.g. `755`, `0`, `1777`). ClaimCritic.md:76 and MutationPlan.md:27 propose `%04o`. The expectation strings depend on this choice. Pick one before cases are written. This plan uses `%a` (the landed header).

### F11 — LOW (accounting): a skip must not look like a pass
- `ok`/`bad` update PASS/FAIL only. A skip needs its own `skip()` that prints `SKIP <label>: <reason>` and does not touch PASS or FAIL. Keep the summary line format unchanged (`:2333`) so consumers of `TSUKUROI_CENSUS_SELFTEST:` do not break; report skips separately in the parent's count.

## 3. Mutant kill table (arithmetic only; E10; not measured)

Correct owner bits from octal mask `0200` (write) and `0100` (search). Each row is a plausible single-token mutant of the owner-bit predicate. "Kills-on" lists fixture modes from the proposed set where the mutant's bit differs from the correct bit.

| Mutant (single predicate change) | Kills-on (fixture modes) | Proposed-set kill count |
|---|---|---|
| owner-write read as decimal text (`$((mode & 0200))` on `"775"`) | 0775, 0355, 0500, 0777 | 2 (0775, 0355) |
| owner-search read as decimal text (`$((mode & 0100))`) | 0555, 0557, 0575, 0775, 0700, 4755, 0777 | 6 |
| group-write mask (0020) for owner-write | 0755, 0575, 0655, 0751, 0355, 0700, 2755, 4755, 0750 | 7 |
| other-write mask (0002) for owner-write | 0755, 0557, 0655, 0751, 0775, 0355, 0700, 2755, 4755 | 8 |
| read mask (0400) for owner-write | 0555, 0557, 0575, 0355, 0500 | 4 |
| search mask (0100) read as write | 0555, 0557, 0575, 0655, 0500 | 4 |
| write mask (0200) read as search | 0555, 0557, 0575, 0655, 0500 | 4 |
| group-search mask (0010) for owner-search | 0655, 0700, 0500 | 2 (0655, 0700) |
| other-search mask (0001) for owner-search | 0655, 0700, 0750 | 2 (0655, 0700) |
| inverted owner-write (M2) | all modes | all |
| inverted owner-search | all modes | all |
| last-3-digit slice, parsed octal | none on owner bits | kills only through the printed `root_mode=` on 2755/4755/1777 |

Reading: the mode set in §4 gives every single-predicate mutant at least two killing fixtures, and the owner-bit mutants are killed through their printed `root_owner_write=`/`root_owner_search=` tokens, not only the verdict. A last-3-digit slice is equivalent on owner bits and is killed only by the exact `root_mode=` token on the special-bit fixtures.

Sanity note: 0755 alone does **not** kill the decimal-text owner-write mutant (755 & 128 = 128 = octal 0200). The inherited FixtureReview.md's point stands.

## 4. Proposed cases and exact assertions (for Census to bind after landing)

### 4-R. Required implementation seams (proposals to Census)
- R1: single `stat -L -c '%a %u %g %F' -- "$ROOT_DIR"` via `cap` (`:456-461`), no `-d` pre-check. Non-zero rc or empty output → `root_status=unavailable`, BLOCKED. `%F` ≠ `directory` → `root_status=non-directory`, BLOCKED. The reason tokens are requested; the header does not name them yet.
- R2: print `root=<path>` (see F3).
- R3: keep `root_mode=%a` (F10). Compute owner bits as `$((8#$mode & 0200))` and `$((8#$mode & 0100))` (F9 of the C1 review).
- R4: the `root_status=` token must appear on every packages line, including the early returns (F6).

### 4-F. Fixture changes (harness)
- F-a: `fx_default` adds `mkdir -p "$d/root"; chmod 0755 "$d/root"`.
- F-b: `fx_hash` replaced as in §2-F1.
- F-c: trap as in §2-F2.
- F-d: `check()` common env: `TSUKUROI_ROOT_DIR="$FX/root"` above `"${EXTRA_ENV[@]}"`.
- F-e: header seam list (`:293-311`) names `TSUKUROI_ROOT_DIR` (already present in the dirty tree at `:311`; keep it).

### 4-C. Case table (proposed new cases; N≈20; all append after HEAD `:2331`, before the summary at `:2333`)
Shorthand: `ROOTOK(m,w,s)` = regex `root=$FX/root root_status=ok root_mode=m root_uid=$(id -u) root_gid=$(id -g) root_euid=$(id -u) root_owner_write=w root_owner_search=s`. Exact token order is the landed header order; if Census reorders, the regex changes with it.

| ID | Fixture | check() args (wrc, verdict) | Assertions (each regex is one argument) | Kills |
|---|---|---|---|---|
| C1 | fx_default (0755) | 0 HEALTHY | `^PLANE packages: HEALTHY .*ROOTOK(755,1,1)` | missing probe; hard-coded tokens; dropped uid/gid |
| C2 | 0555 | 1 DEGRADED | `^PLANE packages: DEGRADED .*ROOTOK(555,0,1)`; `^TSUKUROI_CENSUS: DEGRADED \(packages=DEGRADED ` | owner-write mask; inverted owner-write; fold dropped |
| C3 | 0557 | 1 DEGRADED | `^PLANE packages: DEGRADED .*ROOTOK(557,0,1)` | other-write mask on owner-write |
| C4 | 0575 | 1 DEGRADED | `^PLANE packages: DEGRADED .*ROOTOK(575,0,1)` | group-write mask on owner-write |
| C5 | 0655 | 1 DEGRADED | `^PLANE packages: DEGRADED .*ROOTOK(655,1,0)` | owner-search read as write; group/other search masks |
| C6 | 0775 | 0 HEALTHY | `^PLANE packages: HEALTHY .*ROOTOK(775,1,1)` | decimal-text owner-write (775&128=0) and owner-search |
| C7 | 0355 | 0 HEALTHY | `^PLANE packages: HEALTHY .*ROOTOK(355,1,1)` | decimal-text owner-write; read mask on owner-write |
| C8 | 0700 | 0 HEALTHY | `^PLANE packages: HEALTHY .*ROOTOK(700,1,1)` | group/other search masks |
| C9 | 4755 | 0 HEALTHY | `^PLANE packages: HEALTHY .*ROOTOK(4755,1,1)` | last-3-digit slice print; four-digit parse |
| C10 | 1777 | 0 HEALTHY | `^PLANE packages: HEALTHY .*ROOTOK(1777,1,1)` | sticky misparse |
| C11 | 2755 | 0 HEALTHY | `^PLANE packages: HEALTHY .*ROOTOK(2755,1,1)` | setgid misparse; group-write mask |
| C12 | 0000 (U1) | 1 DEGRADED | `^PLANE packages: DEGRADED .*ROOTOK(0,0,0)` | mode 0 treated as unavailable |
| C13 | `$FX/no-such-root` (EXTRA_ENV) | 2 BLOCKED | `^PLANE packages: BLOCKED .*root=$FX/no-such-root root_status=unavailable`; `^TSUKUROI_CENSUS: BLOCKED ` | missing-probe on failure arm; M3 (ignore unknown) |
| C14 | dangling link `$FX/dangling` | 2 BLOCKED | `^PLANE packages: BLOCKED .*root=$FX/dangling root_status=unavailable` | plain `stat` reading a link as a non-error |
| C15 | regular file `$FX/rootfile` | 2 BLOCKED | `^PLANE packages: BLOCKED .*root_status=non-directory` | dropped `%F` type check |
| C16 | symlink `$FX/rootlink -> root` | 0 HEALTHY | `^PLANE packages: HEALTHY .*root=$FX/rootlink ` + `root_mode=755 root_owner_write=1` | plain `stat` without `-L` (reads 777 link → BLOCKED) |
| C17 | `db.lck` present (existing blocked-lck fixture) + root 0555 | 2 BLOCKED | `^PLANE packages: BLOCKED .*db\.lck=present`; `^PLANE packages: BLOCKED .*ROOTOK(555,0,1)` | probe moved after early return; root token lost on early return |
| C18 | `pacman` missing (existing blocked-pacman-missing) + root 0555 | 2 BLOCKED | `^PLANE packages: BLOCKED .*pacman=missing`; `^PLANE packages: BLOCKED .*root_owner_write=0` | same, second early return |
| C19 | missing root + `qkk` drift (existing `degraded-sample-drift` fixture) | 2 BLOCKED | `^PLANE packages: BLOCKED .*drift=3`; `^PLANE packages: BLOCKED .*root_status=unavailable` | root BLOCKED overwritten by packages DEGRADED (F3 of C1 review); fold dropped |
| C20 | U2: child of a 000 parent (non-root only) | 2 BLOCKED (or SKIP) | `^PLANE packages: BLOCKED .*root_status=unavailable` | EACCES swallowed; only meaningful if Census tokenises EACCES |

Notes on C12–C20:
- C16 and C20 need `TSUKUROI_ROOT_DIR` via `EXTRA_ENV` (explicitly set, which replaces the default in the `check()` env block).
- C17/C18 are the existing `blocked-lck` (`:1936`) and `blocked-pacman-missing` (`:1940`) fixtures with a root override added. Do not edit those legacy lines; copy them as new labelled cases.
- C19 is the existing `degraded-sample-drift` fixture (`:1861`) with the root missing. Do not edit the legacy line.
- Non-owner (`root_uid≠$(id -u)`) 0555 is not fixtureable non-root. Record it as a named skip, not a pass (C1Review.md CX7 / F8).
- Under euid 0 the owner bits do not block the process (parent decision, C1Review.md contract clarification). Pin `root_euid=$(id -u)` in every root-bearing case; do not add a euid-0 pass case.

### 4-S. Skips and cleanup for U2 (C20) only
```bash
if [ "$(id -u)" -eq 0 ]; then
  skip 'blocked: root under unreadable parent' 'uid 0 bypasses DAC; stat succeeds'
else
  mkdir -p "$FX/locked/root"; chmod 000 "$FX/locked"
  check 'blocked: root under unreadable parent' 2 BLOCKED \
    "^PLANE packages: BLOCKED .*root_status=unavailable"   # EXTRA_ENV=(TSUKUROI_ROOT_DIR="$FX/locked/root")
fi
```
`skip()` prints `SKIP ...` and touches neither PASS nor FAIL (§2-F11). The trap fix (F2) is mandatory before U2 lands.

## 5. Protecting the 80-case baseline
- Add only. Do not edit any existing `check`/`check_cli` line (HEAD `:1838-2331`). Insert new cases before the summary (`:2333`).
- Changed shared helpers: `fx_default` (adds root), `fx_hash` (F1), trap (F2), `check()` env (F-d). None of these edits a legacy `check` line. Their effect on legacy outcomes: none expected (verify by reasoning; not run). The only legacy-visible change is the hash input now including metadata; before and after are equal for an unchanged tree.
- Legacy regexes survive the root note because it is appended (`root=…` after the existing fields), not inserted mid-note (HEAD `:2135`). The rollup regex at HEAD `:2319` is unaffected.
- Expected count after landing: 80 + N (N≈20 from §4-C, fewer by one if C20 SKIPs under root). A decrease means a legacy case was lost.

## 6. Risks and open decisions
1. Census has not landed the probe. The token names above (`root_status=unavailable`, `non-directory`, `root=<path>`) are proposals, not current contract.
2. Owner-write/search DEGRADED on a non-owned root (parent decision, C1Review.md) means C2/C3/C4 pass on the uid-1000 fixture, while the live `/` (555 root) will also read DEGRADED. Expected behaviour on the live host must be stated before landing.
3. Mutation kill counts in §3 are arithmetic only. They assume the mutant changes exactly one predicate and that the landed code uses the mask shapes in §3. Post-landing measurement is the parent's job.
4. Running as root: U2 skips, C6–C11 still pass on uid 0, but `root_uid=$(id -u)` must be 0 and `root_gid=$(id -g)` must be 0. Fixture root owner equals the probe uid in both cases, so these assertions hold.
5. The trap fix uses `chmod -R` on the `mktemp` tree. Safe because `$work` is ours; it must never point at a host path.
6. `stat` ownership is printed raw; the census owns no ACL reading. ACL-carrying roots (named ACL entries) are invisible to `%a` (C1Review.md F1). Not a fixture case; a documented limit.

## 7. Messages and coordination
- No edits to `tools/tsukuroi-census.sh` by this seat. Census owns it. The fixture and trap changes in §4-F are proposals for Census to apply, in its own lane.
- Assertions in §4-C go to Census by agent message (see outcome). Census binds them to the landed token names.

## 8. Verification gaps
- No selftest, census, mutant, or fixture run (contract). Every kill claim is design-level and unmeasured.
- E1–E10 are one-off probes in `/tmp` mktemp trees and bash arithmetic. They verify stat/find/pipefail/chmod semantics, not the census.
- Host `/` was not re-measured in this seat.
- Census has not landed a probe at review time; the case table cannot be bound to exact output yet.
- Nothing here is independent non-author verification.
