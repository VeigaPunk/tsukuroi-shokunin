# ArchDoctrine — ArchWiki System Maintenance: Partial Upgrades Analysis

Seat: `TsukuroiR15.ArchDoctrine` (scout, depth axis).
Baseline: `0db618a71ae2d0bb0c0c3059abaa219b7ccd20a2`.
Target: Read ArchWiki System maintenance § Partial upgrades are unsupported; analyze exact scope vs installing an entirely new package and dependency upgrades.
Report: `.ufo/waves/round-15/build/ArchDoctrine.md`.
Read-only research; no verification or test execution; tools: none.

## 1. Primary Source Evidence: ArchWiki System Maintenance

From ArchWiki article *System maintenance* (`https://wiki.archlinux.org/title/System_maintenance`, revision `oldid=885170`, 2026-09-07), section **"Partial upgrades are unsupported"** (S010 / S047):

> "Arch Linux is a rolling release distribution. That means when new library versions are pushed to the repositories, the Developers and Package Maintainers rebuild all the packages in the repositories that need to be rebuilt against the libraries. For example, if two packages depend on the same library, upgrading only one package might also upgrade the library (as a dependency), which might then break the other package which depends on an older version of the library.
>
> That is why partial upgrades are **not supported**. Do **not** use:
> - `pacman -Sy package`,
> - `pacman -Sy` followed by `pacman -S package` (instead, `-Su` should be used in the installation of the package).
>
> **Note**
> - `pacman -Syuw` carries the same risks as `pacman -Sy`, because it will update the *pacman* sync database without installing the newer packages.
> - The bash script *checkupdates*, included with the pacman-contrib package, provides a safe way to check for upgrades to installed packages without running a system update, and provides an option (`-d`) to download the pending updates to the *pacman* cache without synchronizing the database, thus avoiding partial upgrade issues when later attempting to use `pacman -S package` to install packages.
>
> When refreshing the package database, **always** do a full upgrade with `pacman -Syu`."

Section **"Avoid certain pacman commands"**:
> "Avoid doing partial upgrades. In other words, **never** run `pacman -Sy`; instead, **always** use `pacman -Syu`."

## 2. Exact Scope: What Constitutes an Unsupported Partial Upgrade?

Arch doctrine defines a partial upgrade by state transition and dependency relationship, not merely by the presence of `-y` in the invocation:

1. **The Core Mechanism**:
   Arch Linux packages are built and linked against specific sonames and library ABIs available in the official repositories at build time. When a shared library receives an update (and especially a soname bump), all dependent packages in the repository are rebuilt and published together. A system is only guaranteed to be coherent when all installed packages and their shared libraries match the repository snapshot.
2. **Explicitly Prohibited Command Sequences**:
   - `pacman -Sy <pkg>`: Fetches fresh sync databases and installs `<pkg>`, pulling the latest versions of `<pkg>` and its direct dependencies, leaving all other installed packages on older versions.
   - `pacman -Sy` followed by `pacman -S <pkg>`: Even though separated in time, the sync DB is now ahead of the local system state. Installing `<pkg>` later queries the updated sync DB and pulls newer libraries, producing the exact same partial state.
   - `pacman -Syuw`: Updates the sync DB while downloading packages to cache without installing them; any subsequent `pacman -S <pkg>` runs against the updated sync DB and triggers a partial upgrade.
   - Selective holds: Careless use of `IgnorePkg` or `IgnoreGroup` in `pacman.conf` replicates partial upgrade hazards across full system upgrade attempts.

## 3. Installing an Entirely New Package vs. Dependency Upgrades

When an agent or user requests installation of an *entirely new package* (a package not currently installed on the host):

1. **The "All-New Package" Illusion**:
   A naive guard might assume: "If the requested package `<pkg>` is not currently installed, running `pacman -S <pkg>` cannot be a partial upgrade." Arch doctrine proves this assumption false:
   - **Transitive Dependency Upgrades**: A new package `<pkg>` may depend on library `libX`. If `libX` is already installed on the host at version $V_1$, but the sync repository requires version $V_2$ ($V_2 > V_1$), installing `<pkg>` will force pacman to upgrade `libX` from $V_1$ to $V_2$.
   - **Collateral Breakage**: Any existing installed package on the system depending on `libX` $V_1$ may now break (e.g. failing with `error while loading shared libraries: libX.so.N: cannot open shared object file`) if $V_2$ broke backward compatibility or bumped its soname.
2. **Unversioned Dependencies and Stale Sync State**:
   Even if `<pkg>` does not upgrade an installed library, if `<pkg>` itself was compiled upstream against newer libraries, but its `depends` field is unversioned (e.g., `libinput` unversioned), installing `<pkg>` against an outdated local environment can result in immediate runtime failure or unresolved symbols.
3. **Stale-Ahead Sync Database**:
   If the local sync databases are already newer than the installed packages (such as this host's state, where sync databases were updated on 2026-10-18 and 413 updates remain pending), **every** `pacman -S <pkg>` command operates against newer repository metadata. Even an entirely new package will pull dependencies from the newer metadata, directly executing the unsupported "`pacman -Sy` followed by `pacman -S package`" pattern.

## 4. The `--needed` Option Trap

From `pacman(8)`:
> `--needed`: "Do not reinstall the targets that are already up-to-date."

- `--needed` only compares `local_version == sync_version`. If a package is installed at an older version, `--needed` does **not** skip it; pacman treats it as outdated and proceeds to upgrade it!
- In the 2026-10-20 04:25:16 incident on this host, running `pacman -S --needed --noconfirm libinput libinput-tools` upgraded installed `libinput 1.31.3-1 -> 1.32.0-1` while newly installing `libinput-tools 1.32.0-1`, directly causing a partial upgrade because `libinput` was already installed and outdated.

## 5. Synthesis and Recommendations for Tsukuroi Round 15

1. **Clear Distinction**:
   - `pacman -Sp --print-format '%n %v' <pkgs>` provides a plan-only printout of all targets pacman would add (requested targets plus transitive dependencies).
   - If any target in the plan is already installed on the host and its version differs, the command would perform an upgrade.
   - However, even if *every* target in the plan is uninstalled, if the system has pending updates (`pacman -Qu` non-empty), installing new packages from an updated sync DB still risks ABI divergence.
2. **Action Gate Rule**:
   - In round 15, the host instruction strictly prohibits all package transactions, upgrades, downgrades, removals, and service actions.
   - Decision stands as: `BLOCKED_FOR_AGENT_PACKAGE_ACTION`.
   - Any remediation (whether rolling back `libinput` via cache or performing a complete `pacman -Syu` through the update-safety gate) is strictly an operator responsibility.

## 6. Limits and Sources

- Sources:
  - ArchWiki *System maintenance* (`https://wiki.archlinux.org/title/System_maintenance`, rev `oldid=885170`, 2026-09-07), sections § Partial upgrades are unsupported and § Avoid certain pacman commands.
  - `pacman(8)` manual page (Pacman 7.1.0, 2026-05-06).
  - Host snapshot `.ufo/waves/round-15/build/host-snapshot.json` (2026-10-20T07:44:39Z).
- Limits: Read-only research. No live package commands executed; no test or verification asserted.
- Tools: None installed or updated.
