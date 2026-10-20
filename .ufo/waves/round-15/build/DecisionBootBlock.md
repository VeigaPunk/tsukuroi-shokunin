# DecisionBootBlock — R15-BOOT-01: full upgrade vs the mkinitcpio-42 hook gate

author: `TsukuroiR15.DecisionBootBlock` (executor, leaf; no child dispatch) · date: 2026-10-20
axes: depth (primary), operability boundary (no package/service action) · status: report-only advisory fragment; no docs edits, no host probes, no checker, no tests.
evidence: `.ufo/waves/round-15/build/host-snapshot.json`, captured `2026-10-20T07:44:39Z`, SHA256 `b101f3747827cefd0ed604c14b669267ec0fcc1b6c2fbe6e486be0cdbbc6ea81`.

## Merge-ready row

| field | value |
|---|---|
| id | `R15-BOOT-01` |
| role | separate advisory row; **do not fold into C2's `decision` field** |
| decision | `OPERATOR_DECISION_REQUIRED` — full upgrade stays deferred; agent action is `BLOCKED_FOR_AGENT_PACKAGE_ACTION` (no transaction) |
| trigger | any full upgrade that would resolve `mkinitcpio 41.1-1` to `>=42` while the configured busybox runtime hooks still target `/new_root` |
| measured state | `mkinitcpio 41.1-1` installed; `mkinitcpio 41.1-1 -> 42.2-1` pending; also pending: `linux 7.2.3.arch1-3 -> 7.2.11.arch1-1`, `plymouth 26.134.222-2 -> 26.134.222-3`, `limine-mkinitcpio-hook 1.38.0-1.1 -> 1.40.0-2`; 413 `-Qu` lines against the 2026-10-18 DBs |
| installed hook state | `btrfs-overlayfs:4: root_mnt="/new_root"`; `plymouth:11: plymouth update-root-fs --new-root-dir=/new_root`; zero `/sysroot` matches in either file (snapshot `boot_hook_mentions`, exit 0) |
| mechanism | v42/v42.2 init mounts root at `/sysroot` and runs `run_latehook` after it; `btrfs-overlayfs` probes `/new_root`, and a failed probe returns 0 before the overlay mount, so the snapshot overlay is skipped; Plymouth is told the wrong root directory. The mkinitcpio upgrade triggers a post-transaction initramfs rebuild, pairing the new init with the pending hook files |
| owner | operator. This row grants no agent clearance and no repair action |
| clearance evidence required | (a) hook versions at transaction time source-verified `/sysroot`-aware or dynamic-path, **and** an operator-rebuilt initramfs snapshot-boot rehearsed; or (b) operator migrates HOOKS to the systemd initramfs with its `/sysroot`-aware variant and tests it; or (c) operator records explicit risk acceptance. None is performed here |
| falsifier | the transaction no longer includes mkinitcpio `>=42`; or the pending hook versions ship `/sysroot`/dynamic handling; or HOOKS stop selecting the busybox hooks; or the mkinitcpio upgrade does not rebuild the image. Then re-measure; do not silently clear |

## Measured evidence and exact source chain

- Snapshot `package_versions` (exit 0): `libinput 1.32.0-1`, `libinput-tools 1.32.0-1`, `mkinitcpio 41.1-1`, `systemd 261.2-1`. The boot gate is **latent**, not active: no v42 init is installed.
- Snapshot `pending_updates` (exit 0, 413 lines) carries the boot-chain rows above; `mkinitcpio 41.1-1 -> 42.2-1` is line 272 of the captured stdout.
- S015, v42 release notes (reopened 2026-10-20): “Busybox-based init now uses /sysroot as the root mountpoint just like the systemd-based one.” S016, v42.2 `init`: `# Mount root at /sysroot`, `"$mount_handler" /sysroot`, `run_hookfunctions 'run_latehook' ...`, `/usr/bin/switch_root /sysroot`; `init` and `init_functions` contain **0** `/new_root` references (v41 `init` had 7, per the r14 note).
- S021, `limine-entry-tool` tag `1.40.0` (the pending `1.40.0-2` `pkgver`): `root_mnt="/new_root"` at line 4; line 7 `findmnt --mountpoint "$root_mnt" ... || return 0`. It is byte-identical to `master`; the hook's latest change is `3c011dc2` (2026-01-11), with no `/sysroot` work. The omarchy `PKGBUILD` for `1.40.0-2` copies the upstream `usr` tree and applies no hook patch.
- S022, plymouth packaging tag `26.134.222-3` (the pending `pkgrel`): line 11 still `--new-root-dir=/new_root`; its `PKGBUILD` installs that file as `/usr/lib/initcpio/hooks/plymouth` with no path patch.
- mkinitcpio packaging tag `42.2-1` sources upstream `v42.2`; its `libalpm/hooks/90-mkinitcpio-install.hook` triggers `PostTransaction` on `Target = mkinitcpio` and runs “Updating linux initcpios...”. The rebuild is in the same upgrade.
- The same family ships an `sd-btrfs-overlayfs` systemd-hook variant whose script uses `/sysroot`. This host's HOOKS omit `systemd` and select the busybox `btrfs-overlayfs`, so the compatible variant is not the configured path: a configuration-path coupling, not proof that the package lacks `/sysroot` code.

## Separation from the partial-upgrade finding (C2)

| | C2 partial-upgrade finding | `R15-BOOT-01` |
|---|---|---|
| measured event | `pacman -S --needed --noconfirm libinput libinput-tools` at `2026-10-20T04:25:16-0300`; `libinput 1.31.3-1 -> 1.32.0-1`, `libinput-tools` installed (snapshot `libinput_log`, lines 2429/2432/2436) | conditional future full upgrade; the pending set includes mkinitcpio 42.2-1 and the hook packages |
| gate | unsupported partial upgrade / completed targeted transaction | boot-chain compatibility of the *full* upgrade and its rebuilt initramfs |
| cross? | **No.** `mkinitcpio` stayed `41.1-1`; the 04:25 transaction did not install v42 | **No.** A deferral here neither cures nor erases the partial-upgrade record |
| what crosses it | a full upgrade is the doctrinal supported path (S047), but it is exactly the transaction this row blocks until hook clearance | hook clearance plus rebuild/rehearsal; a boot fix does not retroactively authorize the 04:25 state |

No causal or health claim links the 04:25 transaction to boot behavior. The incident is evidence that the findings are separate, not that it caused or cleared the boot gate.

**Recommendation to L1:** land `R15-BOOT-01` as a separate advisory row with this owner and falsifier; never cite the completed 04:25 transaction as upgrade authorization, and record the operator handoff as deferred, not cleared.

## Limits

- Source tags and PKGBUILDs, not binary payloads: no `.pkg.tar.zst` was opened; distro patch sets beyond the inspected recipes remain uninspected.
- No initramfs image, preset or cmdline was read; no rebuild, reboot, snapshot boot, package transaction, service action or privilege escalation occurred. Hook consequences are code-path inference, not observed boot outcomes.
- Ordinary (non-snapshot) boots are **not** predicted to fail from the overlay hook: it acts only on a read-only `/snapshot` subvolume. Plymouth's late hook runs on every boot with the wrong directory; its runtime effect is `[unk]` and is not claimed fatal. Impact is scoped to snapshot/rollback boots and that Plymouth handoff.
- The snapshot is point-in-time; `-Qu` is relative to the 2026-10-18 DBs, not upstream freshness. `413` must not be restated as a current upstream count.
- Tools installed or updated: **none**. No host probe was run by this seat; the retained HostSnapshot was consumed read-only.

## Sources

- S015 `https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/releases/v42` (A, mined); S016 `.../raw/v42/init` and `.../raw/v42.2/init` (A, mined).
- S021 `https://gitlab.com/Zesko/limine-entry-tool/-/raw/1.40.0/install/arch-linux/limine-mkinitcpio-hook/usr/lib/initcpio/hooks/btrfs-overlayfs` (A, mined); S022 `https://gitlab.archlinux.org/archlinux/packaging/packages/plymouth/-/raw/26.134.222-3/plymouth.initcpio_hook` (A, mined).
- S047 ArchWiki System maintenance § Partial upgrades are unsupported (A, mined; doctrine only).
- Package recipes (supporting source reads, not new registry rows): mkinitcpio `42.2-1` PKGBUILD; plymouth `26.134.222-3` PKGBUILD; omarchy `limine-mkinitcpio-hook 1.40.0-2` PKGBUILD.
