# AttackAllowedNewPackages — critic, round 15 (report only)

Axes: depth (judged), plus calibration/freshness/operability as impact checks. Target: the
contract guard "`pacman -Sp --print-format '%n %v' <pkgs>`; only uninstalled candidates could
qualify; existing installed package means forbidden partial upgrade". Verdict: **defective as an
explanation** — "all requested names uninstalled" is not sufficient for non-partial. Fixable by
wording; the round's no-transaction rule already holds, so no ordinal/axis harm if corrected.

## Counterexamples (strongest first)
1. **Stale-ahead sync DB makes every `-S` partial, even all-new targets.** `host-snapshot.json`
   (captured 2026-10-20T07:44:39Z): `pacman -Qu` = 413 lines against DBs born 2026-10-18T17:11Z;
   last `synchronizing package lists` = log line 2288. That is ArchWiki's named unsupported state:
   "`pacman -Sy` followed by `pacman -S package` (instead, `-Su` should be used ...)" (S047
   System maintenance, §Partial upgrades are unsupported, oldid=885170). Installedness of `<pkgs>`
   is irrelevant while `-Qu` is non-empty.
2. **Unversioned dependency on an installed-but-outdated lib is never pulled.** libinput PKGBUILD
   (gitlab packaging main, pkgver 1.32.0 pkgrel 1 = installed, sha256 d25d04ce…473c):
   `package_libinput-tools` `depends=(... libinput ...)` unversioned. libalpm `_alpm_resolvedeps`
   resolves only `alpm_checkdeps` misses (lib/libalpm/deps.c:788-834); installed libinput 1.31.3
   satisfies `libinput`. So `pacman -S libinput-tools` alone would print one line,
   `libinput-tools 1.32.0-1`, pass "all uninstalled", and install tools 1.32 over lib 1.31.3
   [INFERENCE: resolver path; not executed]. Same for libinput's own deps — snapshot pending
   join: glibc, libevdev, libwacom, systemd-libs, cairo, glib2, gtk4, libx11, python all outdated,
   none pulled by the 04:25 transaction's resolver [INFERENCE; see limit L2].
3. **`-Sp` output is the whole add-set, not `<pkgs>`, and hides the action kind.** Print path:
   src/pacman/sync.c:818-829 prints `alpm_trans_get_add` after prepare (targets + pulled deps).
   `alpm_add_pkg` (lib/libalpm/add.c:82-101) admits installed targets: cmp==0 → reinstall
   (without `--needed`), cmp<0 → **downgrade**; print mode masks those warnings
   (pacman.c:1295-1301 `logmask &= ~ALPM_LOG_WARNING`). `%n %v` shows only the sync version, so
   install/upgrade/downgrade/reinstall need a per-printed-`%n` join with `pacman -Q`; joining on
   requested names fails for provides: `-S libinput.so` resolves to installed provider libinput
   (deps.c:705-712 "provide is already installed so return early").
4. **`-Sp` skips conflict checks and the lock.** pacman.c:1295-1298 sets `NOCONFLICTS`, `NOLOCK`,
   `noconfirm`; libsync.c:509 gates conflict resolution, the only place `trans->remove` gains
   conflict removals (libsync.c:582-649). A clean print can precede a real `-S` that fails or
   removes installed packages; the plan can also race a concurrent transaction.
5. **`--needed` upgrade trap is observed, not hypothetical.** add.c:87-92 skips only `cmp == 0`
   ("packages up to date are not reinstalled"); pacman(8) S048: "Do not reinstall the targets
   that are already up-to-date." Snapshot log line 2429 `Running 'pacman -S --needed --noconfirm
   libinput libinput-tools'` → 2432 `upgraded libinput (1.31.3-1 -> 1.32.0-1)`. That command is
   verbatim the operator channel `sudo pacman -S --needed --noconfirm <pkg>` (RULES.md:7);
   RULES.md:12-13 forbids only `pacman -Sy <pkg>`, missing the `-Sy`-then-`-S` form.

## Impacted axes
- calibration/freshness (C2): a "new packages could qualify" reading overclaims safety at 413
  pending. depth (C1) unaffected. No host/package action is needed to fix.

## Smallest safe correction (for IncidentEntry/L1 wording; I edited nothing)
- Replace guard clause with: "`-Sp --print-format '%n %v'` is an advisory read-only plan of the
  full add-set (targets plus pulled deps; no conflict removals, no lock, no action kind). Any `-S`
  is a partial upgrade while `pacman -Qu` is non-empty (413 at 07:44:39Z). Even with `-Qu` empty,
  every printed `%n` must be absent from `pacman -Q`. `--needed` skips only exact-version-equal
  targets: outdated installed targets upgrade, newer local ones downgrade. Round 15 executes no
  `-S` regardless; decision stays BLOCKED_FOR_AGENT_PACKAGE_ACTION."
- Route to operator (L1, not agents): RULES channel order step 1 conflicts with its own
  partial-upgrade ban whenever `-Qu` is non-empty; the 04:25 incident is that conflict realized.

## Sources (opened 2026-10-20 ~04:44-03:00)
- S048 https://man.archlinux.org/man/pacman.8 — TRANSACTION OPTIONS `-p, --print`,
  `--print-format`; UPGRADE OPTIONS `--needed` (stable headings; no reader line numbers).
- S047 https://wiki.archlinux.org/title/System_maintenance §Partial upgrades are unsupported, oldid=885170.
- pacman source, gitlab master a6f7467d8c7c (2026-01-25): sync.c af6f1104…, add.c c63fb24d…,
  deps.c e42e6c01…, pacman.c 197cbc42…, callback.c 9dadcc56…, lib/libalpm/sync.c 6b297364… (sha256 prefixes).
- https://gitlab.archlinux.org/archlinux/packaging/packages/libinput/-/raw/main/PKGBUILD.

## Limits
- L1: installed pacman version not probed (HostSnapshot owns probes); source is master HEAD.
- L2: snapshot log grep omits lines 2430-2431/2433-2435; whether the 04:25 transaction pulled or
  newly installed other packages is unobserved. Read-only `sed -n 2429,2440p /var/log/pacman.log`
  by HostSnapshot/L1 would close it.
- No `-Sp`, `-S`, `-Sy`, sudo, service or snapper action; no runtime breakage is claimed.
- Tools installed/updated: none. No tests/build/lint run.
