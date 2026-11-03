# E1HostProbes — item C1-PROBES (round 66, wave w1)

Stamped: 2026-11-03T21:01:15Z · lane base `c68bfe97` · lane repo `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
Axis served: **depth / C1** (host policy-input receipts for CB2–CB4). No interpretation of applicability is offered here.

## Files changed (all untracked additions; zero tracked edits)

Receipts (`.ufo/waves/round-66/probes/`, each stamped `2026-11-03T20:58:41Z` except
`r66-cmdline.txt` at `2026-11-03T21:00:56Z` after its value-withholding rewrite):

| file | sha256 | lines |
|---|---|---|
| `r66-bootctl.txt` | `33fe2fb4150cb62f74d67eb4ae545e3f772dce13fbaa9f151f08490a30b0ec75` | 81 |
| `r66-cmdline.txt` | `67d7dcad09e6890d4b4f593182594e7a6bbb7cd62529d80ce595aa09a99aa0df` | 29 |
| `r66-tpm2.txt` | `c74d4817937f19ec5dd521e332555bdbd6d613ed176be09026750a44e692eb1a` | 29 |
| `r66-secureboot.txt` | `903b5d33f90951cb1b4180c2920598c59979da84de6ae1d03858a9757bc2f2fd` | 30 |
| `r66-limine-keys.txt` | `1ec6253ae771078783ea7834260c425a677ba3c0943ced1d32564a269f528a05` | 55 |
| `r66-uki-stub.txt` | `4ff60425ba473c319a33d6c6453304f5242d5c7760d6cf78d1d4ffbb55d93a08` | 27 |
| `r66-root-policy-units.txt` | `c5b4ae4c0cd63d3e189430edd3ed69b2ccb2d86dd7de595bce2f2b81461a64c5` | 11 |

Summary: `.ufo/waves/round-66/drafts/e1-host-summary.md` (one line per receipt with its rc and reading, plus the CB2–CB4 PRESENT/ABSENT/BLOCKED table).

`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status --porcelain` (rc 0) lists only untracked
`?? .ufo/waves/round-66/{drafts,probes,w1}/` and the wave runner's own files — **no tracked file touched**,
no commit, no packagemanager transaction, no service action, no sudo, scratch deleted at exit.

## Behavior — what each receipt establishes (verbatim excerpts)

### CB2 — boot chain
```
$ bootctl status
Failed to read "/boot/EFI/systemd": Permission denied
Failed to open '/boot/loader/loader.conf': Permission denied
      Firmware: UEFI 2.110 (American Megatrends 5.41)
 Firmware Arch: x64
   Secure Boot: disabled
  TPM2 Support: no
  Measured UKI: no
 ...
        Product: Limine 12.9.4
      Partition: /dev/disk/by-partuuid/b80445be-18ee-45e6-9a30-14339ea785a7
         Loader: └─/boot/EFI/Linux/omarchy_linux.efi
  Current Entry: Omarchy.linux

Current Stub:
        Product: systemd-stub 262.1-1-arch
rc=1
```
- Limine identity: `pacman -Q limine` → `limine 12.9.4-1`, rc 0; `command -v limine` → `/usr/bin/limine`, rc 0.
- UKI in use: bootctl resolves the running loader to `/boot/EFI/Linux/omarchy_linux.efi` and the
  running stub to `systemd-stub 262.1-1-arch`.
- Direct ESP reads are **BLOCKED** without privilege: `ls -la /boot/EFI/Linux/` → `ls: cannot open
  file '/boot/EFI/Linux/': Permission denied`, rc 2; `grep -n 'protocol:' /boot/limine.conf` →
  `Permission denied (os error 13)`, rc 2. Cause, receipted: `findmnt -no SOURCE,TARGET,FSTYPE,OPTIONS /boot`
  → `/dev/nvme0n1p1 /boot vfat rw,relatime,fmask=0077,dmask=0077,…`, rc 0 (`/efi` is not a mountpoint, rc 1).
  Therefore the `protocol: efi` datum CB2 names is **not observable at this privilege**.
- `ENABLE_UKI` is set twice in different files: `/etc/default/limine` →
  `ENABLE_UKI=yes` (anchored grep, rc 0; no `ENABLE_LIMINE=` line exists there — line 11 is
  `ENABLE_LIMINE_FALLBACK=yes`), while `/etc/limine-entry-tool.conf:168` → `ENABLE_UKI=no` (rc 0).
  Recorded as a conflict; not interpreted.
- `ukify` is absent (`command -v ukify` rc 1) and package `systemd-ukify` is **not installed**
  (`pacman -Q systemd systemd-ukify` → `error: package 'systemd-ukify' was not found` + `systemd 262.1-1`, rc 1);
  shipped stubs do exist: `/usr/lib/systemd/boot/efi/{linuxx64,linuxia32,addonx64,addonia32}.efi.stub`, rc 0.
- Runtime: `uname -r` → `7.2.11-arch1-1`; `systemctl --version | head -1` → `systemd 262 (262.1-1-arch)`.

### CB3 — policy inputs
- **cmdline token ABSENT**: `grep -c 'systemd.credentials_boot_policy=' /proc/cmdline` → `0`, rc 1.
  15 tokens, names only on disk (raw values withheld per item rule), shape anchor
  `printf %s "$(cat /proc/cmdline)" | sha256sum` → `690a91783b1e569e949f9490e671df782cef5b239bb50ac4a7eab617605d79f7`, rc 0.
- **TPM2 ABSENT at the device level**: `systemd-analyze has-tpm2` →
  `partial` / `-firmware` / `-driver` / `+system` / `+subsystem` / `+libraries`, rc **3**;
  `systemd-creds has-tpm2` emits the replacement notice and the same block, rc 3;
  `ls -la /sys/class/tpm/` → only `.` and `..`, rc 0.
- **SecureBoot PRESENT = disabled**: `ls -la /sys/firmware/efi/efivars/ | grep -i SecureBoot` rc 0 →
  `SecureBoot-8be4df61-93ca-11d2-aa0d-00e098032b8c` (5 bytes) and
  `SecureBootSetup-7b59104a-c00d-4158-87ff-f04d6396a915` (11 bytes). The prescribed
  `od -An -t u1 -j4 -N1 <SecureBoot file>` prints `6` then `od: …: Illegal seek`, rc 1 — efivarfs is
  non-seekable, and `-j4` only selects offset 4 on a seekable file (proved on a 5-byte control file
  `06 00 00 00 01`: `-j4 -N1` → `1`, rc 0; `-N5` → `6 0 0 0 0`). The disclosed minimal sequential read
  `od -An -t u1 -N5 <SecureBoot file>` → `6 0 0 0 0`, rc 0 ⇒ attributes `06 00 00 00`, **data byte 0
  (Secure Boot disabled)**, agreeing with `bootctl` `Secure Boot: disabled`. `mokutil` is absent
  (`command -v mokutil` rc 1; `mokutil --sb-state` → `error: command not found: mokutil`, rc 127).

### Extra receipted fact (delivered as-is, no verdict)
`grep -rl 'credentials_boot_policy' /etc/systemd /usr/lib/systemd /etc/kernel | head -20`, rc 0, count 1:
the only path is the shared library `/usr/lib/systemd/libsystemd-shared-262.1-1.so`, whose single match
is at line 5005 (binary match; line numbers only were extracted, no content dumped). No unit file, drop-in
or `/etc/kernel` file in those trees mentions the key.

## Axes moved
- **depth / C1**: every CB2/CB3 host value now has a no-sudo receipt with command, verbatim output and rc;
  the two genuinely unreadable items (`/boot` config, `/boot/EFI/Linux` listing) are recorded as BLOCKED
  with their exact errors instead of being asserted.
- **boot-chain**: Limine 12.9.4 + systemd-stub 262.1-1-arch + UKI `omarchy_linux.efi` pinned with hashes.
- **policy-inputs**: token absent, TPM device absent (has-tpm2 `partial`, rc 3), SecureBoot byte 0.
- No axis harmed: nothing outside `probes/`, `drafts/`, `w1/` was written; no tracked file changed.

## Risks / blockers
1. **`protocol: efi` is BLOCKED** at this privilege (`/boot` vfat ESP, `fmask=0077`). The claim's CB2
   wording names it; the receipt shows the denial and the mount options, so the L1 can either accept the
   bootctl-derived chain facts or raise privilege out of band. I did not attempt elevation, per the
   host-probes boundary.
2. **Prescribed `od -j4` is unusable on efivarfs** (prints the offset-0 attribute byte, rc 1). A minimal
   `-N5` sequential read plus a seekable control file are recorded as a disclosed deviation; the value
   agrees with bootctl independently.
3. **`ENABLE_UKI` disagrees across two host files** (`/etc/default/limine` yes vs
   `/etc/limine-entry-tool.conf:168` no). Recorded, not resolved — resolving it is beyond an executor's
   boundary and outside C1's frozen predicates.
4. `Measured UKI: no` / `TPM2 Support: no` are bootctl's readings; no applicability verdict is offered here.

## Tooling
None installed or upgraded (no pacman/uv/npx/curl). Scratch `/fast/scratch/hyaku/tsukuroi-r66/E1HostProbes-2/`
removed at exit; the control-byte provenance needed to reproduce the `od` semantics is written into
`r66-secureboot.txt` itself.
