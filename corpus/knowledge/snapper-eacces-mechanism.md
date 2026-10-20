source: S019 https://gitlab.com/Zesko/limine-snapper-sync/-/raw/master/README.md § Requirements and features; S020 https://gitlab.com/Zesko/limine-snapper-sync/-/raw/master/install/arch-linux/usr/lib/systemd/system/limine-snapper-sync.service § Service and Security hardening; S023 https://wiki.archlinux.org/title/Snapper § Creating a new configuration; S027 https://man.archlinux.org/man/capabilities.7 § CAP_DAC_OVERRIDE; S028 https://man.archlinux.org/man/systemd.exec.5 § CapabilityBoundingSet=; access(2) https://man.archlinux.org/man/access.2 § DESCRIPTION and ERRORS (opened lead; no S-id assigned in ART).
verified-at: 2026-10-19 (re-opened S019-S020, S023, S027-S028 and access(2) (S034); re-ran non-root filesystem, package, service and journal probes).
recheck: on-release; procedure: `stat -c '%a %U:%G' /; getfacl -p /; systemctl cat limine-snapper-sync.service | grep -n -E 'User|CapabilityBoundingSet|ProtectSystem|ReadOnlyPaths|ProtectHome'; journalctl --no-pager -o short-iso -g 'create subvolume failed' | grep -c 'errno:13'; snapper list-configs; pacman -Qo /; zcat /var/lib/pacman/local/filesystem-*/mtree | grep -cE '^\./?[[:space:]]'; findmnt -n -o SOURCE,FSTYPE,TARGET /boot; df -h /boot`.

# Snapper `/.snapshots` EACCES mechanism and limits

## Current host evidence

- [obs] `/` is `555 root:root`; `getfacl -p /` shows `user::r-x`, `group::r-x`, and `other::r-x` — `stat -c '%a %U:%G' /` and `getfacl -p /` 2026-10-19.
- [obs] The local `limine-snapper-sync.service` declares `User=root` and `CapabilityBoundingSet=CAP_SYS_ADMIN`; the requested property sweep also shows `ProtectHome=yes`, with no matching `ProtectSystem` or `ReadOnlyPaths` lines — `systemctl cat limine-snapper-sync.service | grep -n -E '^(User|CapabilityBoundingSet|ProtectSystem|ReadOnlyPaths|ProtectHome)'` 2026-10-19. The narrower requested sweep returned lines 14 and 19 — `systemctl cat limine-snapper-sync.service | grep -n -E 'CapabilityBoundingSet|ProtectSystem|ReadOnlyPaths|ProtectHome'` 2026-10-19.
- [obs] The journal query matched **8** `errno:13` messages — `journalctl --no-pager -o short-iso -g 'create subvolume failed' | grep -c 'errno:13'` 2026-10-19. First match: `2026-10-16T12:47:26-03:00`; last match: `2026-10-19T08:11:47-03:00` — first: `journalctl --no-pager -o short-iso -g 'create subvolume failed' | grep -m1 'errno:13'`; last: `journalctl --no-pager -o short-iso -g 'create subvolume failed' | grep 'errno:13' | tac | grep -m1 'errno:13'` 2026-10-19.
- [obs] `snapper list-configs` prints only its header, i.e. **0** configured rows — `snapper list-configs` 2026-10-19. `stat -c '%F %a %n' /.snapshots` reports no such file — `stat -c '%F %a %n' /.snapshots` 2026-10-19.
- [obs] `pacman -Qo /` reports `No package owns /` — `pacman -Qo /` 2026-10-19. The installed filesystem mtree sweep prints **0** root-directory entries — `zcat /var/lib/pacman/local/filesystem-*/mtree | grep -cE '^\./?[[:space:]]'` 2026-10-19 (grep returns 1 when no lines match). This leaves no package metadata baseline for `/`'s mode; [inf] `pacman -Qkk` cannot report drift for this unowned root-directory mode.
- [inf] Mechanism: root's mode and ACL provide no write bit on `/`; the service runs as root but its sole listed bounding capability is `CAP_SYS_ADMIN`. S027 says `CAP_DAC_OVERRIDE` bypasses DAC checks, while S028 says capabilities omitted from `CapabilityBoundingSet=` are removed from the process's bounding, effective, and permitted sets. Thus the unit lacks the root DAC bypass needed to create `/.snapshots`, which is consistent with the observed `EACCES` (errno 13). This is a source-grounded explanation, not a syscall trace; other confinement such as an LSM was not tested here.
- [obs] `/boot` is `/dev/nvme0n1p1`, `vfat`, mounted at `/boot` — `findmnt -n -o SOURCE,FSTYPE,TARGET /boot` 2026-10-19. It reports **2.0G** total, **279M** used, **1.8G** available — `df -h /boot` 2026-10-19. [obs] S019 recommends a FAT32 boot partition of at least **4 GiB**; the current mount's reported capacity is below that recommendation. The exact FAT subtype was not probed.

## Rejected readings

- **R6 — “A pre-existing `@.snapshots` explains the EACCES.”** S023 documents the old archinstall layout where `@.snapshots` is already mounted at `/.snapshots` and `snapper create-config` fails. The current `stat` finds no `/.snapshots`, and the fresh journal matches are `errno:13` (Permission denied), not an “already exists” result. The measured evidence therefore does not support that collision as the cause; no privileged Btrfs subvolume inventory was run.

## Falsifier

[inf] Operator-only, non-mutating discriminator; **not run** (this lane did not use `sudo`):

```sh
sudo systemd-run --wait --pipe -p CapabilityBoundingSet=CAP_SYS_ADMIN test -w /; echo rc=$?  # predicted rc=1
sudo test -w /; echo rc=$?  # predicted rc=0
```

The first returning 0 falsifies the proposed DAC/capability mechanism. `access(2)` (S034) explains why this `test -w` comparison distinguishes root's permitted capabilities from its effective capabilities; it is a permission probe, not a subvolume-create test.

## Operator options (reported, never performed)

- An operator may determine why `/` is `0555`; if that mode is unintended, the ART K2 candidate is to restore the expected owner-write permission (for example, `chmod 755 /`). `/` is unowned, so package verification cannot restore a known mode. No permission change was made.
- An operator may provision the root Snapper configuration with full capabilities (`snapper -c root create-config /`) and configure the integration's `SNAPPER_CONFIG_NAME="root"` only after reviewing the intended Btrfs layout and service policy. These are state-changing actions and were not run.
- The `/boot` capacity comparison is a separate capacity concern, not a cause of this `EACCES`; any partition resizing or boot-file change is operator work.

## QUALITY check

1. Falsifiable: the operator-only `test -w /` predictions are explicit; mode, ACL, unit, journal, config and ownership results are re-runnable.
2. Evidence names exact host commands and source anchors below.
3. `[obs]` and `[inf]` are separated; untested LSM/subvolume details remain explicit limits.
4. This new note does not rewrite prior claims; any correction to existing knowledge must be an appended dated erratum.
5. R6 is retained under `## Rejected readings`.
6. No pacman transaction is advised; no bare `pacman -Sy` is recommended.
7. External claims cite scoped S-rows below. S023 is tier B and only supports the competing layout, not the mechanism; the mechanism rests on tier-A unit/man-page evidence and measured host state.
8. The mechanism is `[inf]` and includes a falsifier.
9. The negative ownership, mtree, config and path claims each carry the explicit sweep that produced them.

## Sources

- **S019, tier A** — https://gitlab.com/Zesko/limine-snapper-sync/-/raw/master/README.md (master fetched 2026-10-19; registry row pins commit 4695dd1c) § Requirements: “A FAT32 boot partition of at least 4 GiB is recommended”; § Features describes restore methods and repair behavior. The source is the mutable `master` branch, reopened 2026-10-19.
- **S020, tier A** — https://gitlab.com/Zesko/limine-snapper-sync/-/raw/master/install/arch-linux/usr/lib/systemd/system/limine-snapper-sync.service (master fetched 2026-10-19; registry row pins commit cd909745) § `[Service]` / Security hardening: `User=root`; `CapabilityBoundingSet=CAP_SYS_ADMIN`; `ProtectHome=yes`. The source is mutable `master`, reopened 2026-10-19.
- **S023, tier B** — https://wiki.archlinux.org/title/Snapper § Creating a new configuration: “the `@.snapshots` subvolume will already be mounted to `/.snapshots`, and the `snapper create-config` command will fail.” It is used only to describe the excluded competing layout.
- **S027, tier A** — https://man.archlinux.org/man/capabilities.7 § CAP_DAC_OVERRIDE: “Bypass file read, write, and execute permission checks.”
- **S028, tier A** — https://man.archlinux.org/man/systemd.exec.5 § CapabilityBoundingSet=: “Capabilities listed will be included in the bounding set, all others are removed”; the section says this also affects effective and permitted sets.
- **S034, tier A — access(2)** — https://man.archlinux.org/man/access.2 § DESCRIPTION: “for the root user, the check uses the set of permitted capabilities rather than the set of effective capabilities”; § ERRORS describes `EACCES` when requested access is denied.
- **Host evidence (own-work, all read-only, non-root, 2026-10-19)** — `stat -c '%a %U:%G' /`; `getfacl -p /`; `systemctl cat limine-snapper-sync.service | grep -n -E 'CapabilityBoundingSet|ProtectSystem|ReadOnlyPaths|ProtectHome'`; `journalctl --no-pager -o short-iso -g 'create subvolume failed' | grep -c 'errno:13'` plus first/last sweeps; `snapper list-configs`; `stat -c '%F %a %n' /.snapshots`; `pacman -Qo /`; `zcat /var/lib/pacman/local/filesystem-*/mtree | grep -cE '^\./?[[:space:]]'`; `findmnt -n -o SOURCE,FSTYPE,TARGET /boot`; `df -h /boot`.

## Erratum (2026-10-20, round 12) — permission proxy is not causal proof

The Falsifier paragraph above incorrectly says the two `test -w` processes
distinguish root's permitted from effective capabilities. They change the
whole credential envelope instead. S034 describes `access(2)` semantics, not
which syscall any particular `test` binary uses. Neither predicted exit
certifies the failed subvolume operation; no privileged falsifier was run.
The mode-change example above is conditional operator advice, not a sourced
universal requirement that `/` be `0755`.

S027/S028 support a DAC/capability explanation consistent with the observed
error family, not proven historical attribution. Inactive-unit properties
are configuration evidence; runtime sets, exact syscall/path, incident-time
mode and ioctl ordering remain unknown. The independently usable branch
procedure and retained counterexamples supersede that inference shortcut:
`root-dac-decision-r12.md` and `.json`, sources S027/S028/S034/S035/S038–S040.
Evidence: `.ufo/waves/round-12/SourceReview.md`,
`.ufo/waves/round-12/error-order-smoke.json` and resumed source reviews.

## Erratum (2026-10-20, round 12) — unowned is not policy-free

The earlier "no package metadata baseline" inference was too broad.
Although `pacman -Qo /` cannot establish an inode ownership baseline,
the opened `/usr/lib/tmpfiles.d/root.conf` explicitly contains
`z / 555 - - -`. ClaimCriticR also opened systemd's version-261 policy
change and inspected the local override/boot-unit evidence:
`.ufo/waves/round-12/resumed/ClaimCriticR.md`.
The existing mode is consistent with a packaged declarative policy (S039/S040).
The earlier conditional `chmod 755 /` suggestion is superseded: do not
change the root mode without reviewing the policy and affected service.
No mode change or boot test ran; a present policy does not reconstruct
the incident-time syscall, credentials or inode history.

## Erratum (2026-10-20, round 13) — R13-DAC-EXCLUSIVITY

The round-12 procedure pointer above now resolves to a historical entry
rejected at outside closure. Use `root-dac-correction-r13.md` and `.json`
(S041) for active unit-read-only discrimination. It supersedes the false
claim that only strict ProtectSystem or ReadOnlyPaths can make a unit's
root/path read-only. BindReadOnlyPaths and read-only TemporaryFileSystem
are alternative examples; RootDirectory/RootImage change the path view,
not inherently its writability. These are non-exhaustive source-grounded
mechanisms, not new evidence of this host's failing invocation. Historical
Btrfs syscall/path, capability and private-namespace attribution remain
unproven; no configuration change is recommended by this correction.

## Erratum (2026-10-20, round 14) — active source-scope supersession

`root-dac-correction-r13.md` remains the active unit-path entry, now read with
`source-scope-correction-r14.md` / `.json`: R14-VALUE-DOMAIN supersedes its
ProtectSystem “value set is not exhaustive” cell (the documented domain is a
boolean argument or the special values `full`/`strict`; non-exhaustiveness is
about unit-side mechanisms, S044), and R14-COMMENT-ATTRIBUTION supersedes the
#8047 self-description attribution (verified account fields are separate from
the comment's unverified VM assertion and its second opinion; the maintainer
deferral concerns #6634, and #6629's disclaimer is not transferred, S045).
The namespace discrimination in this note is unchanged; no host cause is
established. This erratum adds no recheck procedure of its own: for the
read-only unit-property procedure use `SKILL.md:1742-1750`, which excludes
`snapper list-configs` (root `snapperd` D-Bus activation) and raw
`systemctl cat`. No command text from the #8047 or #6629 comments is adopted
or repeated here.

## R17-FRESHNESS — dated host re-verification (2026-10-20)

Scope of this notice: later host captures (`.ufo/waves/round-17/l1-capture/fresh-capture.txt`, `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt`, 2026-10-20) checked against the 2026-10-19 statements above. Historical captures stay historical; the measurements above are not rewritten. Nothing here authorizes any package, service, or boot action, and the falsifier above remains not run.

- Stale: "`snapper list-configs` prints only its header, i.e. **0** configured rows". [obs] sudo snapper list-configs lists two configs, home (/home) and root (/). That probe was sudo-run; the 2026-10-19 probe was non-root, so the contexts differ. Capture: `.ufo/waves/round-17/l1-capture/fresh-capture.txt:46`.
- Stale: "`stat -c '%F %a %n' /.snapshots` reports no such file". [obs] /.snapshots/1/snapshot and /.snapshots/2/snapshot exist as subvolumes with ro=true (btrfs property get). Capture: `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:160`.
- Stale: "It reports **2.0G** total, **279M** used, **1.8G** available". [obs] limine_history alone reports total 836148 (1K blocks), and /boot/EFI/Linux reports total 552512 (1K blocks); df was not re-run, so the 2026-10-19 used figure has no current df value. [inf] the listed files alone exceed the earlier 279M figure. Capture: `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:111`.
- Stale: "The local `limine-snapper-sync.service` declares `User=root` and `CapabilityBoundingSet=CAP_SYS_ADMIN`". [obs] limine-snapper-sync was upgraded from 1.31.0-1.1 to 1.32.1-2 at 2026-10-20 09:16:42; the post-upgrade unit file was not re-read, so the 2026-10-19 unit properties describe the prior package only. Capture: `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:50`.
- Stale: "The current `stat` finds no `/.snapshots`". [obs] /.snapshots is present after sudo create-config at 2026-10-20 09:03:02, and the /.snapshots/1 and /.snapshots/2 subvolumes exist. Capture: `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:80`.
- Stale: "An operator may provision the root Snapper configuration with full capabilities (`snapper -c root create-config /`)". [obs] that step was already run via sudo at 2026-10-20 09:03:02, and the root config is listed (`fresh-capture.txt:46`). It is not repeated or re-authorized here. Capture: `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:80`.


## R17-RECHECK — steer-safe procedure

Appended 2026-10-20 by the tsukuroi round-17 L1; earlier bytes unchanged. Supersedes the package-manager invocations in this file's `recheck:` line for any round whose steer forbids running pacman (QUALITY 26); file reads replace them and the substitution is recorded in that round's report. Read-only.

- `stat -c "%a %U:%G" /`
- `getfacl -p /`
- `systemctl cat limine-snapper-sync.service | grep -n -E "User|CapabilityBoundingSet|ProtectSystem|ReadOnlyPaths|ProtectHome"`
- `journalctl --no-pager -o short-iso -g "create subvolume failed" | grep -c "errno:13"`
- snapper configs without D-Bus activation: `grep SNAPPER_CONFIGS /etc/conf.d/snapper`
- packaged metadata for `/` without a package query (replaces the package-ownership query for `/`): `zcat /var/lib/pacman/local/filesystem-*/mtree | grep -cE "^\./?[[:space:]]"`
- `findmnt -n -o SOURCE,FSTYPE,TARGET /boot`
- `df -h /boot`
