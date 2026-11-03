# E1HostProbes — round 65 / w1 — C1 read-only host probes

Seat: E1HostProbes (executor, EXEC-AUTHORIZED). Item: **C1-PROBES** — SY-row host receipts for claim C1.
Host: plazir27 (Arch x86_64, kernel 7.2.11-arch1-1). Lane HEAD at probe time: `37c74e27` (round-65 declaration).
Probe window: 2026-11-03T19:38:56Z … 19:42Z. Every receipt carries its own UTC stamp, command line, verbatim output and rc.
Receipts: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-65/probes/` (10 files, listed at the end).
Privilege used: `sudo -n` **only** for `cat /boot/limine.conf`, `ls -laR /boot`, `stat -c` on `/boot` images, and `stat` on `/etc/limine-entry-tool.conf`. Nothing else escalated. No package, service, boot, firmware or config mutation was performed. **No UKI content was read or extracted.**

## 1. Probe results (what each receipt proves)

| # | Receipt | Command | rc | Content of record |
|---|---|---|---|---|
| 1 | `r65-bootctl.txt` | `bootctl status 2>&1` | **1** (permission artifact, see below) | Firmware `UEFI 2.110 (American Megatrends 5.41)`, `Firmware Arch: x64`; **Secure Boot: disabled**; **TPM2 Support: no**; **Measured UKI: no**; **Measured OS: no**; `Boot into FW: supported`. Boot loader `Limine 12.9.4`; **Loader `└─/boot/EFI/Linux/omarchy_linux.efi`**; **Current Entry `Omarchy.linux`**; **Current Stub: `systemd-stub 262.1-1-arch`** with `✓ Measures kernel+command line+sysexts`. Random seed: `System Token: set`, `Exists: Can't access /boot/loader/random-seed (Permission denied)`. ESP `/boot (/dev/disk/by-partuuid/b80445be-…)`. EFI vars: `Limine` (0x0000, active boot-order) → `/boot//EFI/limine/limine_x64.efi`; `UEFI OS` (0x0004) → `/boot//EFI/BOOT/BOOTX64.EFI`. Permission-denied stderr: `Failed to read "/boot/EFI/systemd": Permission denied`, `Failed to open '/boot/loader/loader.conf': Permission denied`. |
| 2 | `r65-limine-conf.txt` | `sudo -n cat /boot/limine.conf` (+ python parse of the captured bytes) | 0 | Full conf verbatim (4919 B, mtime `2026-11-03 16:19:30`, `limine.conf.old` 4919 B @ `13:19:16`). `default_entry: 2`; **`#timeout: 3` is commented out** → timeout directive unset; `hash_mismatch_panic: no`. **10 entries / 6 protocol lines / all `protocol: efi` / 0 vmlinuz mentions / 0 initramfs-or-initrd mentions.** Entry table below. |
| 3 | `r65-boot-inventory.txt` | `sudo -n ls -laR /boot`; `stat -c '%n\|%s\|%y\|%a\|%U:%G'` on every UKI/EFI image | 0 | `/boot` is `drwx------ root:root` (0700) — all files 0700 root:root. `/boot` holds **`amd-ucode.img` (307200) and no kernel/initramfs payloads**: `find /boot -maxdepth 4 -type f \( -name 'vmlinuz*' -o -name 'initramfs*' -o -name 'initrd*' -o -name '*.img' \)` matched **only `amd-ucode.img`**. `/boot/EFI/Linux/omarchy_linux.efi 284447744 @ 2026-10-29 03:45:24`; `omarchy_linux-lts.efi 281338880 @ 03:45:18`; `/boot/EFI/limine/limine_x64.efi 385024`, `limine_x64.bak 389120`; `/boot/EFI/BOOT/BOOTX64.EFI 385024`, `BOOTIA32.EFI 405504`; `/boot/loader/{boot-secret-mixin,random-seed}` 32 B each; `/boot/432d02b5…/limine_history/` holds 3 snapshot UKIs (290422784 / 284439552 / 281318912) + `snapshots.json`. **Zero `.nlm` files.** Kernel payload source: `/usr/lib/modules/7.2.11-arch1-1/vmlinuz 17244672 @ 2026-10-15 21:28:58`. |
| 4 | `r65-mkinitcpio-conf.txt` | `grep -nE '^(HOOKS\|MODULES\|COMPRESSION\|URI)' /etc/mkinitcpio.conf`; 4 drop-ins in full; `ls -la /etc/mkinitcpio.d`; producer surface | 0 | Main conf: `MODULES=()` (l.7), `HOOKS=(base udev autodetect microcode modconf kms keyboard keymap consolefont block encrypt filesystems fsck)` (l.55); **COMPRESSION and URI unset**. Drop-ins: `nvidia.conf` `MODULES+=(nvidia nvidia_modeset nvidia_uvm nvidia_drm)`; **`omarchy_hooks.conf` reassigns `HOOKS=(base udev plymouth keyboard autodetect microcode modconf kms keymap consolefont block encrypt filesystems fsck btrfs-overlayfs)`** + `FILES+=(/etc/vconsole.conf)`; `omarchy_resume.conf` `HOOKS+=(resume)`; `thunderbolt_module.conf` `MODULES+=(thunderbolt)`. **`/etc/mkinitcpio.d/` is EMPTY (0 entries).** |
| 5 | `r65-hooks.txt` | `ls -1 /usr/lib/initcpio/hooks \| wc -l`; `grep -ls '/new_root' …`; full list | 0 | **12 hooks**; **2 name `/new_root`: `btrfs-overlayfs`, `plymouth`**. Full list: btrfs, btrfs-overlayfs, consolefont, encrypt, keymap, memdisk, plymouth, resume, shutdown, sleep, udev, usr. **No `systemd` hook exists in the set.** |
| 6 | `r65-nvpcr.txt` | `test -d`, `ls -la`, count `*.nvpcr`; `pacman -Qo`; file bytes; `ls /usr/lib/pcrlock.d` | 0 | **`/usr/lib/nvpcr/` EXISTS with 4 definitions** — `cryptsetup` (sha256, nvIndex 30474753, priority 700), `hardware` (30474752, 500, `orderly:false`), `login` (30474755, 800), `verity` (30474754, 300). `pacman -Qo` → **owned by `systemd 262.1-1`**. `/usr/lib/pcrlock.d/` ships the full chain incl. **`770-nvpcr-separator.pcrlock`**, `750-enter-initrd`, `800-leave-initrd`, `850-sysinit`, `900-ready`, `950-shutdown`, `990-final`. |
| 7 | `r65-tpm2-units.txt` | `systemctl list-unit-files \| grep -Ei 'tpm2\|pcr\|nvpcr'`; `pacman -Ql systemd \| grep -E 'tpm2-setup\|nvpcr'`; `/sys/class/tpm`; `/dev/tpm*`; `journalctl -k -b \| grep -i tpm` | 0 (grep rc 0; `/dev/tpm*` rc 2 = absent) | 31 matching unit files. `systemd-tpm2-setup.service` + `-early` are **static and wanted by `sysinit.target`** (pacman -Ql: `sysinit.target.wants/systemd-tpm2-setup{,-early}.service`); `systemd-pcrnvdone.service` static; all 7 `systemd-pcrlock-*` units `disabled`; `tpm2.target` static. **`/sys/class/tpm` exists but is EMPTY (0 entries)**; **`/dev/tpm*` absent**; `systemd-pcrlock`/`systemd-tpm2-setup` not on PATH (rc 1; the binary ships at `/usr/lib/systemd/systemd-tpm2-setup`). Kernel log: **8 TPM lines, every one a `skipped, unmet condition check`** — `ConditionSecurity=measured-os` (PCR Measurements, Machine ID, OS Separator, Early SRK Setup, NvPCR Product ID) and `ConditionSecurity=measured-uki` (Make TPM PCR Policy), plus `ConditionPathExists=/etc/initrd-release` (TPM PCR NvPCR Initialization Separator). systemd build line confirms `+TPM2`. `systemctl is-system-running` → `running`. `/proc/cmdline` captured. |
| 8 | `r65-versions.txt` | `pacman -Q systemd mkinitcpio limine linux nvidia-utils`; `uname -r`; `systemctl --version \| head -1` | 0 | `systemd 262.1-1`; `mkinitcpio 42.2-1`; `limine 12.9.4-1`; `linux 7.2.11.arch1-1`; `nvidia-utils 615.78.08-1`; `uname -r 7.2.11-arch1-1`; `systemd 262 (262.1-1-arch)`. |
| 9 | `r65-ukify.txt` | `command -v ukify`; `pacman -Q systemd-ukify` | **1 / 1** | `ukify` NOT on PATH; `error: package 'systemd-ukify' was not found`. |
| + | `r65-uki-producer.txt` | supplementary read-only (SY5 input) | 0 | `limine-mkinitcpio-hook 1.40.0-2` **Provides: `limine-entry-tool`**; `/etc/default/limine` sets **`ENABLE_UKI=yes`, `CUSTOM_UKI_NAME="omarchy"`, `ESP_PATH="/boot"`**; `/etc/limine-entry-tool.conf` default is `ENABLE_UKI=no` but is overridden by `/etc/default/limine`; `/etc/pacman.d/hooks/90-mkinitcpio-install.hook` → `Exec = /usr/share/libalpm/scripts/limine-mkinitcpio-install` (PostTransaction); that script builds with **`mkinitcpio --uki "$output"`** (line 175) and `MKINITCPIO_UKI_OPTIONS`; mkinitcpio man documents `-U/--uki`, `--ukiconfig` (config **passed to ukify**) and `--no-ukify`; `/usr/lib/kernel/install.d/` ships `50-mkinitcpio.install` (mkinitcpio 42.2-1), `90-uki-copy.install` (systemd 262.1-1), `90-loaderentry.install`; `/etc/kernel/install.d/` EMPTY; **no `/etc/kernel/uki.conf`**; `/usr/local/bin/mkinitcpio` is a 733 B pass-through shim to `/usr/bin/mkinitcpio`. |

### 1.1 Limine entry table (derived from the verbatim conf bytes; depth = 2-space indent)

```
idx|depth|path                          |protocols|media                        |UKI|vmlinuz|initramfs
1  |0    |/+Omarchy                     |0        |container (no protocol)      |no |no     |no
2  |1    |//linux                       |1 (efi)  |UKI /EFI/Linux/omarchy_linux.efi|yes|no     |no
3  |1    |//linux-lts                   |1 (efi)  |UKI /EFI/Linux/omarchy_linux-lts.efi|yes|no |no
4  |2    |//Snapshots                   |0        |container                    |no |no     |no
5  |2    |///2026-10-20 09:29:19        |0        |container                    |no |no     |no
6  |2    |////linux                     |1 (efi)  |UKI limine_history/…efi_sha256_2e9c9bdc…|yes|no|no
7  |2    |////linux-lts                 |1 (efi)  |UKI limine_history/…lts.efi_sha256_2d49da06…|yes|no|no
8  |2    |///2026-10-20 09:03:02        |0        |container                    |no |no     |no
9  |2    |////linux                     |1 (efi)  |UKI limine_history/…efi_sha256_0f1e3c84…|yes|no|no
10 |0    |/EFI fallback                 |1 (efi)  |EFI app /EFI/BOOT/BOOTX64.EFI|no |no     |no
totals: 10 entries, 6 protocol lines, protocol kinds = {efi}, vmlinuz mentions = 0, initramfs/initrd mentions = 0
directives: default_entry: 2 ; timeout: "#timeout: 3" (commented out → unset)
```

Every bootable entry also carries an entry-level `cmdline:` line (root=/dev/mapper/root, `cryptdevice=PARTUUID=cf3d875f-…`, `rootflags=subvol=@`, `rw rootfstype=btrfs`, resume offsets) — i.e. the UKI is booted with an **externally supplied** cmdline, not an embedded one.
`default_entry: 2` → under Limine's depth-first numbering including containers, entry 2 is `/+Omarchy//linux`; this agrees with bootctl's `Current Entry: Omarchy.linux`. If containers were excluded from numbering, entry 2 would instead be `//linux-lts` — the observed running entry favours the former reading. **[INFERENCE]**

## 2. Findings that bear on C1's SY rows

**F1 — the TPM2 plane is absent at firmware level, four ways.** `bootctl status`: `TPM2 Support: no`. `/sys/class/tpm` exists but lists **nothing**; `/dev/tpm*` does not exist; the kernel log contains **no TPM driver line at all** (the only 8 `tpm` matches are systemd unit skip messages). systemd is built `+TPM2`, so this is hardware/firmware absence, not a software gap. → SY2.
**F2 — this host DOES boot UKIs today; the draft's "no UKI" chain is wrong.** 6/6 protocol lines in `limine.conf` are `protocol: efi` naming `.efi` images; `/boot` contains no `vmlinuz*`/`initramfs*` at all; bootctl resolves the running loader to `/boot/EFI/Linux/omarchy_linux.efi` with **`Current Stub: systemd-stub 262.1-1-arch`** and the stub's `✓ Measures kernel+command line+sysexts`. The empty `/etc/mkinitcpio.d/` does **not** mean "no UKI builder": the builder is the **`limine-mkinitcpio-hook` ALPM hook** (`/usr/share/libalpm/scripts/limine-mkinitcpio-install` → `mkinitcpio --uki`), gated by `/etc/default/limine` `ENABLE_UKI=yes` / `CUSTOM_UKI_NAME="omarchy"`. The v262 requirement's *precondition* (a boot chain that ships UKIs) is therefore **met** on this host. → SY3 must be corrected; SY4's premise too.
**F3 — the NvPCR definitions EXIST, so the note's third falsifier has fired.** `/usr/lib/nvpcr/*.nvpcr` = 4 files, owned by `systemd 262.1-1`. SY4's "no NvPCR definitions" is factually false and must be re-expressed as "definitions present but inert". Inertness is proven, not assumed: no TPM2 (F1); **no `systemd` hook in the initramfs** (12 hooks, the set has no `systemd`; effective HOOKS ends `fsck btrfs-overlayfs resume`), so no `/etc/initrd-release` in the initrd and `systemd-pcrnvdone`'s `ConditionPathExists=/etc/initrd-release` cannot be met; and systemd itself logs `Make TPM PCR Policy skipped, unmet condition check ConditionSecurity=measured-uki` on this boot.
**F4 — the v262 signing mechanism has no producer on this host.** `--sign-initrd-pcrs` is a **ukify** option (S282 wording); `ukify` is not on PATH and `systemd-ukify` is not installed (rc 1 / rc 1). mkinitcpio 42.2 only forwards a UKI config to ukify via `--ukiconfig` (and documents `--no-ukify`), and this host has no `/etc/kernel/uki.conf` and no presets. So even with TPM2 present, nothing shipped here would embed the signed initrd-phase PCR policy without installing `systemd-ukify`. → SY4 / SY5.
**F5 — "boots a UKI" and "Measured UKI" are independent axes.** bootctl reports `Measured UKI: no` while the running image *is* a systemd-stub UKI (F2). Measurement is TPM-anchored, so it reads `no` purely because F1 holds. Any SY text that treats `Measured UKI: no` as evidence of "no UKI" is a category error; the two must be stated separately. → SY2 wording.
**F6 — boot-loader config facts for the note.** `default_entry: 2`; the `timeout` directive is present only as a comment (`#timeout: 3`), so Limine has no configured menu timeout; `hash_mismatch_panic: no`; the conf is regenerated by `limine-entry-tool` (fresh mtime `2026-11-03 16:19:30`, backup `13:19:16`) and embeds a per-entry sha256 suffix on each `boot():` path.

## 3. Commands run (with rc)

All commands echo their own rc into their receipt (see the `rc` lines cited in §1). Summary:

- `bootctl status 2>&1` — **rc 1**; full output captured. rc 1 is bootctl's response to the two `Permission denied` paths (`/boot/EFI/systemd`, `/boot/loader/loader.conf`) because `/boot` is 0700 root:root and the probe was unprivileged. This is a **privilege artifact, not a probe failure**: every SY field the note cites (Firmware, Secure Boot, TPM2 Support, Measured UKI/OS, loader, stub, current entry) printed.
- `sudo -n cat /boot/limine.conf` — rc 0 (4919 B).
- `sudo -n ls -laR /boot` — rc 0; `sudo -n stat -c …` on 8 UKI/EFI images — rc 0 each (a first attempt passed a glob that the unprivileged shell could not expand; the retry used explicit names and succeeded).
- `grep -nE '^(HOOKS|MODULES|COMPRESSION|URI)' /etc/mkinitcpio.conf` rc 0; `cat` of the 4 drop-ins rc 0 each; `ls -la /etc/mkinitcpio.d` rc 0 (0 entries).
- `ls -1 /usr/lib/initcpio/hooks | wc -l` rc 0 → 12; `grep -ls '/new_root' /usr/lib/initcpio/hooks/*` rc 0 → 2 names.
- `ls -la /usr/lib/nvpcr` rc 0; `ls -1 …/*.nvpcr | wc -l` rc 0 → 4; `pacman -Qo` ×4 rc 0; `cat` ×4 rc 0; `ls -la /usr/lib/pcrlock.d` rc 0.
- `systemctl list-unit-files | grep -Ei 'tpm2|pcr|nvpcr'` rc 0; `pacman -Ql systemd | grep -E 'tpm2-setup|nvpcr'` rc 0; `ls -la /sys/class/tpm` rc 0 (empty); `ls -la /dev/tpm*` **rc 2** (absent — expected); `journalctl -k -b --no-pager | grep -i tpm` rc 0 (8 matches, all skip conditions); `systemctl is-system-running` rc 0 → `running`.
- `pacman -Q systemd mkinitcpio limine linux nvidia-utils` rc 0; `uname -r` rc 0; `uname -a` rc 0; `systemctl --version | head -1` rc 0.
- `command -v ukify` **rc 1**; `pacman -Q systemd-ukify` **rc 1** (`not found`).
- Supplementary producer surface: `pacman -Qi limine-mkinitcpio-hook` rc 0; `pacman -Qo /usr/bin/limine-entry-tool` rc 0; `pacman -Qo` on `90-uki-copy.install` / `50-mkinitcpio.install` rc 0; `pacman -Ql limine-mkinitcpio-hook` rc 0; `cat /etc/default/limine` rc 0; `cat /etc/pacman.d/hooks/90-mkinitcpio-install.hook` rc 0; `cat` of `/etc/boot/hooks/{pre.d/10-limine-reset-enroll,post.d/90-limine-enroll-config}` rc 0; `grep -nE 'uki|UKI' /usr/lib/limine/limine-entry-tool` rc 0; `grep -nE 'uki|UKI' /usr/share/libalpm/scripts/limine-mkinitcpio-install` rc 0; `zcat /usr/share/man/man8/mkinitcpio.8.gz | grep …` rc 0; `head /usr/local/bin/mkinitcpio` rc 0; `head /usr/bin/limine-mkinitcpio` rc 0.
- Receipt integrity: `grep` for PEM/password/token/Bearer across all receipts → **no matches**; long-base64 scan of the `/boot` receipt → **0**.

## 4. Files written

Receipts (all under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-65/probes/`, filename → bytes at last write):

| file | contents |
|---|---|
| `r65-bootctl.txt` | probe 1 |
| `r65-limine-conf.txt` | probe 2 + derived entry table |
| `r65-boot-inventory.txt` | probe 3 + `stat` metadata for 8 images + payload-name `find` + conf mtimes |
| `r65-mkinitcpio-conf.txt` | probe 4 + preset dir + effective-HOOKS derivation + producer/ownership surface |
| `r65-hooks.txt` | probe 5 |
| `r65-nvpcr.txt` | probe 6 + ownership + def bytes + `pcrlock.d` |
| `r65-tpm2-units.txt` | probe 7 + `/sys/class/tpm`, `/dev/tpm*`, kernel log, `/proc/cmdline` |
| `r65-versions.txt` | probe 8 |
| `r65-ukify.txt` | probe 9 |
| `r65-uki-producer.txt` | supplementary: `limine-mkinitcpio-hook`, `/etc/default/limine`, ALPM hook, `mkinitcpio --uki` invocation, shim |

No other lane file was created or modified. `git status --porcelain` in the lane shows only untracked `.ufo/waves/round-65/**` paths (the wave dirs themselves); nothing tracked was touched.

## 5. Risks / limits of this evidence

1. **UKI interior unread** (bound-respected): whether the four `/usr/lib/nvpcr/*.nvpcr` files are actually embedded in `/boot/EFI/Linux/omarchy_linux.efi` is **unknown**; proving it needs a UKI inspection tool (`ukify inspect`), which does not exist here. Do not assert embedding either way.
2. **`bootctl` rc 1** is a permission artifact; cite the output, not the rc, and do not treat it as a failed probe.
3. **Unprivileged `/boot` reads are denied** (0700 root:root) — `Random Seed: Exists: Can't access…` and the two `Permission denied` lines are the evidence of that gating, not host breakage.
4. **Draft contradictions to fix before landing** (§2 F2/F3/F5): the note's current SY3/SY4 text is falsified — the host boots UKIs, ships 4 NvPCR definitions, and `Measured UKI: no` is orthogonal to "is a UKI". The draft's own falsifier list (a preset that builds UKIs / TPM2 present / nvpcr defs appearing) has **two items already true** on this host today; the applicability verdict must be re-expressed as "preconditions partly met, blockers = no TPM2 + no systemd initrd hook + no ukify producer", not "requirement inapplicable because none of it exists".
5. **Host identifiers in receipts**: root cmdline, PARTUUIDs and machine-id are recorded (they are public-ish, non-secret). No token, key, password or secret value was read or captured; `/boot/loader/boot-secret-mixin` and `random-seed` are named/sized only.
6. **Limine entry numbering** for `default_entry: 2` is an inference (§1.1); stated as such, with the bootctl corroboration and the alternative reading.
7. No tool install/update was needed or performed (no pacman/uv/npx/release-binary action).

## 6. Scratch

All temporary work was confined to `/fast/scratch/hyaku/tsukuroi-r65/E1HostProbes/` (one python parse of the captured conf producing `entrytable.txt`; its output is appended into the receipt). That directory was removed before yielding — confirmed absent at the end of this seat.
