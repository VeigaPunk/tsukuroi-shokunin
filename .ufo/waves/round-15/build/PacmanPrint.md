# PacmanPrint — pacman(8) --print/--print-format and -S --needed analysis

Seat: TsukuroiR15.PacmanPrint (scout, depth axis).
Baseline: 0db618a71ae2d0bb0c0c3059abaa219b7ccd20a2.
Contract: read-only research; no tests run; tools none.

## 1. Primary Evidence: pacman(8) Specifications

From the installed manual page `pacman(8)` (Pacman 7.1.0, dated 2026-05-06):

- **`-p, --print` (Transaction Option, applies to `-S`, `-R`, `-U`)**:
  > "Only print the targets instead of performing the actual operation (sync, remove or upgrade). Use *--print-format* to specify how targets are displayed. The default format string is \"%l\", which displays URLs with *-S*, file names with *-U*, and pkgname-pkgver with *-R*."
- **`--print-format <format>`**:
  > "Specify a printf-like format to control the output of the *--print* operation. The possible attributes are: \"%a\" for arch, \"%b\" for builddate, \"%d\" for description, \"%e\" for pkgbase, \"%f\" for filename, \"%g\" for base64 encoded PGP signature, \"%h\" for sha256sum, \"%m\" for md5sum, \"%n\" for pkgname, \"%p\" for packager, \"%v\" for pkgver, \"%l\" for location, \"%r\" for repository, \"%s\" for size, \"%C\" for checkdepends, \"%D\" for depends, \"%G\" for groups, \"%H\" for conflicts, \"%L\" for licenses, \"%M\" for makedepends, \"%O\" for optional depends, \"%P\" for provides and \"%R\" for replaces. Implies *--print*."
- **`--needed` (Upgrade Option, applies to `-S` and `-U`)**:
  > "Do not reinstall the targets that are already up-to-date."

## 2. Why `--needed` Still Upgrades an Installed Outdated Package

The definition in `pacman(8)` is exact: `--needed` directs pacman to *"Do not reinstall the targets that are already up-to-date."*

1. **"Reinstall" vs "Upgrade" Distinction**:
   In ALPM/pacman terminology, "reinstall" specifically designates installing the identical version of a package that is currently installed on the host (`local_version == sync_version`).
2. **Evaluation of "Up-to-Date"**:
   A package target is only considered "already up-to-date" if `local_version >= sync_version` (evaluated via ALPM version comparison rules: epoch, version, pkgrel).
3. **Outdated Package Behavior**:
   When a package target is installed on the local system at version `V_local`, but the sync database specifies version `V_sync` where `V_sync > V_local`, the target is **not** up-to-date. Therefore:
   - It is not classified as an already up-to-date target.
   - The `--needed` filter does **not** prune or skip the target.
   - Pacman proceeds to schedule the package for an upgrade transaction (`V_local -> V_sync`).
4. **The Partial Upgrade Risk in `-S --needed`**:
   The operator directive often suggests `sudo pacman -S --needed --noconfirm <pkg>`. If `<pkg>` is already installed at an older version, `--needed` does **not** prevent pacman from upgrading it against the sync database! In the presence of outdated sync metadata or without a full system upgrade (`-Syu`), running `pacman -S --needed <pkg>` performs a partial upgrade on `<pkg>` (as observed in the 2026-10-20 incident where `libinput` was upgraded from 1.31.3-1 to 1.32.0-1 despite `--needed`).

## 3. The Read-Only Pre-Transaction Guard

To safely evaluate package install candidates without initiating an upgrade or partial upgrade:
- `pacman -Sp --print-format '%n %v' <pkgs>` computes the resolved targets and print-plan without acquiring `db.lck`, downloading, or altering state.
- **Guard rule**:
  Before any install command, query local installation status (`pacman -Q <pkg>`).
  - If `<pkg>` is **already installed** (even if outdated), executing `pacman -S` (with or without `--needed`) executes a partial upgrade on that package or reinstalls it, which is strictly prohibited.
  - If `<pkg>` is **not installed**, check the planned transitive dependency upgrades printed by `pacman -Sp --print-format '%n %v' <pkgs>`. If any dependency in the printed list is already installed on the host and its printed version differs from the installed version, the transaction will upgrade that dependency, producing an unsupported partial upgrade.
  - For round 15: the host instruction strictly prohibits any package transaction regardless of guard clearance.

## 4. Limits and Caveats

- `--print-format '%s'` caveat: As documented in `corpus/knowledge/update-safety-note.md:199-202`, `%s` in `--print-format` prints download size for sync targets, which can report `0` for certain packages or cached objects; it is not reliable for installed size (use `pacman -Si` for verified sync metadata).
- Man page version examined: Pacman 7.1.0 manual page (`/usr/share/man/man8/pacman.8.gz`), dated 2026-05-06.
- Research only: no host commands were executed, no tests run, no verifications claimed.

## Tools
None. No packages installed, updated, or removed; no daemons or services started.
