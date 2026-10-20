# VersionSemantics — package version comparison, epoch, pkgrel, and sync nuances

author: TsukuroiR15.VersionSemantics (scout) | date: 2026-10-20 | status: read-only research | judged_on: depth

## 1. Scope & Declared Axes
- **Axes:** `depth` (semantic rigor of version/epoch/pkgrel rules per official specs) and `operability` (informing update safety without host mutations).
- **Target:** Assess installed vs newer sync package comparison rules, epoch precedence, pkgrel nuances, and sync resolution.
- **Mandate:** Read-only research. No verification runs, test suites, mutation probes, or package/service alterations.

## 2. Specification Evidence (`vercmp(8)`, `PKGBUILD(5)`, `pacman(8)`, `libalpm(3)`)
- **Full Version Structure:** `[epoch:]pkgver-pkgrel`. `pkgver` has no colons/hyphens/spaces; `pkgrel` is a positive integer (optional `.y` subrelease); `epoch` is an optional integer prefix (default 0).
- **Epoch Precedence:** An epoch value overrules any version comparison unless epochs are equal (`2:1.0-1` > `1:3.6-1`, `1:001` > `4.34`).
- **Alphanumeric vs Numeric:** Alphanumeric follows `1.0a < 1.0b < 1.0rc < 1.0 < 1.0.a < 1.0.1`; numeric follows standard numerical segment values.
- **Conditional pkgrel Comparison:** `pkgrel` is compared **only if present in both versions**. `vercmp("1.5-1", "1.5") == 0`, while `vercmp("1.5-1", "1.5-2") < 0`. This allows versioned dependencies (`name>=1.5`) without hardcoding `pkgrel`.
- **Local vs Sync DB:** Local DB (`/var/lib/pacman/local/`) tracks installed file packages. Sync DBs (`/var/lib/pacman/sync/`) track remote packages. Plain `-Su` upgrades only when `vercmp(sync, local) > 0`; `-Suu` is required to force downgrades. First repository declared in `pacman.conf` wins on identical package names.

## 3. Incident Analysis (`libinput` Partial Upgrade)
- On 2026-10-20T04:25:16-0300, `pacman -S --needed --noconfirm libinput libinput-tools` was run without `-y`/`-u`.
- Installed state: `libinput 1.32.0-1` (upgraded from `1.31.3-1`) and `libinput-tools 1.32.0-1` (installed).
- Sync DBs (`core.db`, `extra.db`) content stamp: `2026-10-18 14:11:00-0300` (1.6 days older than the transaction).
- `vercmp("1.32.0-1", "1.32.0-1") == 0`: `libinput` dropped off `pacman -Qu`, but 413 other packages remain pending. Equality against a stale sync DB is not proof of currency against upstream Arch, nor ABI harmony with non-upgraded callers.

## 4. Recommendations for C2 & Decision Planes
1. Separate `installed_version` (local ALPM DB), `sync_version` (sync DB), and `running_version` (unmeasured process memory maps).
2. Maintain `BLOCKED_FOR_AGENT_PACKAGE_ACTION`: `vercmp == 0` on `libinput` does not clear full upgrades, which remain blocked by mkinitcpio 42 `/sysroot` vs `/new_root` hook incompatibilities.
3. Account for `pkgrel` omission in dependency evaluations (`vercmp("1.5-1", "1.5") == 0`).

## 5. Exact Sources, Limits & Tools
- **Sources:** `VERCMP(8)` (Pacman 7.1.0, 2026-05-06), `PKGBUILD(5)` (2026-05-06), `PACMAN(8)` (2026-05-06), `libalpm_packages(3)` / `/usr/include/alpm.h`, `update-safety-note.md` §1–§5, `host-snapshot.json`.
- **Limits:** Read-only research. No packages installed/removed/upgraded; no services or process probes; no tests executed.
- **Tools installed/updated:** **none**.
