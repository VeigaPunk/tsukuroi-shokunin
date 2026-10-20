# SrcLimineEntryTool — upstream README: `limine-update`, `ENABLE_UKI`, `KERNEL_CMDLINE`

Opened 2026-10-20: https://gitlab.com/Zesko/limine-entry-tool/-/raw/master/README.md — the landing page https://gitlab.com/Zesko/limine-entry-tool served only the GitLab HTML shell, no README body.

`limine-update` (§Usage → Arch Linux → Easy setup, step 5) [obs]:
> "Regenerate initramfs or UKIs and update kernel boot entries:"
> "On UEFI x86_64 systems, Limine binary is automatically deployed during updates or reinstallation."

`ENABLE_UKI` (§Configuration, comment `### UKI (Unified Kernel Image)`; scoped by README to limine-dracut-support/limine-mkinitcpio-hook installs) [obs]:
> "Automatically create UKIs in '$ESP_PATH/EFI/Linux/' for UEFI. (yes|no)"
> "With Snapper and Secure Boot enabled, UKIs use the kernel cmdline from 'limine.conf' instead of an embedded cmdline."

`KERNEL_CMDLINE` (§Configuration, comment `### Kernel Command Line Configuration`) [obs]:
> "KERNEL_CMDLINE[default] applies to any kernel entries without specific configuration."
> "If unset, the tool will try to read them from '/etc/kernel/cmdline' or '/proc/cmdline'."
> "`+=` appends parameters to an existing cmdline for the same KERNEL_CMDLINE[<key>]" — "Ignores /etc/kernel/cmdline and /proc/cmdline".

[inf] README names mkinitcpio only for UKI build options; per-kernel/all-kernel rebuild scope is unstated.

NOT established [unk]: all-kernel vs hook-target scope; `mkinitcpio -P`; EFI-deploy/UKI-build ordering; stale `*-fallback` UKI deletion when `MKINITCPIO_FALLBACK` unset; pre/post-hook placement; 1.40.0-2 parity.

Corroboration [obs] (raw master `install/arch-linux/limine-mkinitcpio-hook/`): `limine-update` runs `limine-install --no-efi-register`, then `limine-mkinitcpio "$@"`; no args → `echo rebuild | limine-mkinitcpio-install`, setting `rebuild_all=true` and rebuilding every `/usr/lib/modules/*/` with `modules.builtin`. Host `/etc/default/limine`: `ENABLE_UKI=yes`, `CUSTOM_UKI_NAME="omarchy"`, `ESP_PATH="/boot"`.

Scope: executed=none
