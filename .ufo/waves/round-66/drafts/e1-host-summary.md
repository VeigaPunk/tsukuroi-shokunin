# Round 66 / w1 — host probe summary (seat E1HostProbes, item C1-PROBES)

Stamped: 2026-11-03T21:00:22Z
Receipts live in `.ufo/waves/round-66/probes/`; each starts with its own UTC stamp
(`2026-11-03T20:58:41Z`, except `r66-cmdline.txt` at `2026-11-03T21:00:56Z` after its value-withholding
rewrite) and carries `$ command`, verbatim stdout+stderr, and `rc=` per command.
No sudo, no pacman transaction, no service action, no write outside this lane's `probes/` + `drafts/`.

## One line per receipt

| receipt | rc | reading |
|---|---|---|
| `r66-bootctl.txt` | 1 (partial read: `/boot/EFI/systemd` and `/boot/loader/loader.conf` Permission denied) | bootctl still printed the System block: Firmware UEFI 2.110 (American Megatrends 5.41), `Secure Boot: disabled`, `TPM2 Support: no`, `Measured UKI: no`; loader is Limine 12.9.4 with `Loader: /boot/EFI/Linux/omarchy_linux.efi` and `Current Stub: systemd-stub 262.1-1-arch`. |
| `r66-cmdline.txt` | 0 (`cat` withheld by rule), 0 (sha256 anchor), 0 (token count), 0 (tokenizer), 1 (`grep -c`, no match) | `/proc/cmdline` has 15 tokens; only names (and has-value/bare shape) are on disk, raw values withheld per item rule with sha256 `690a9178…d79f7` as the integrity anchor; `systemd.credentials_boot_policy=` is **absent** (`grep -c` prints `0`, rc 1). |
| `r66-tpm2.txt` | 3 (`systemd-analyze has-tpm2`), 3 (`systemd-creds has-tpm2`, redirect only), 0 (`ls /sys/class/tpm/`) | `partial` with `-firmware -driver +system +subsystem +libraries`; `/sys/class/tpm/` is empty, so **no TPM device** is exposed. |
| `r66-secureboot.txt` | 1 (`command -v mokutil`), 127 (`mokutil --sb-state`), 0 (`ls|grep`), 1 (prescribed `od -j4 -N1`), 0 (supplement `od -N5`) | mokutil is **absent**; the efivar exists (5 bytes, `SecureBoot-8be4df61-…`); the prescribed `od -j4 -N1` fails with `Illegal seek` on efivarfs, so a disclosed minimal sequential read `od -An -t u1 -N5` gives `6 0 0 0 0` → attribute bytes `06 00 00 00`, **SecureBoot data byte = 0 (disabled)**, matching bootctl. |
| `r66-limine-keys.txt` | 0 (anchored grep: only `ENABLE_UKI=yes`), 0 (`pacman -Q limine` → 12.9.4-1), 0 (`ls /etc/default/limine`), 0 (supplement `grep -n ENABLE_LIMINE` → line 11 is `ENABLE_LIMINE_FALLBACK=yes` only), 2/2/2/2 (`protocol:` greps), 0 (`findmnt /boot`), 1 (`findmnt /efi`), 1 (no `protocol` in limine-entry-tool.conf), 0 (`ENABLE_UKI=no` at `/etc/limine-entry-tool.conf:168`) | `/etc/default/limine` sets `ENABLE_UKI=yes` and has **no** `ENABLE_LIMINE=` line; `/boot` is a vfat ESP mounted `fmask=0077,dmask=0077`, so every `/boot` read — including `limine.conf` and therefore the `protocol: efi` datum — is **BLOCKED** with `Permission denied`; `/etc/limine-entry-tool.conf:168` says `ENABLE_UKI=no` (conflict recorded, not interpreted). |
| `r66-uki-stub.txt` | 2 (`ls /boot/EFI/Linux/`), 1 (`command -v ukify`), 1 (`pacman -Q systemd systemd-ukify`), 0 (stub dir), 0 (`uname -r`), 0 (`systemctl --version`) | Direct UKI listing is **BLOCKED** (`Permission denied`); `ukify` and package `systemd-ukify` are **absent**; the shipped stubs are present (`linuxx64.efi.stub`, `addonx64.efi.stub`, …); kernel `7.2.11-arch1-1`, systemd `262 (262.1-1-arch)`. |
| `r66-root-policy-units.txt` | 0 (PIPESTATUS of `grep -rl … | head -20`), 0 (count), 0 (line numbers) | Exactly **one** path in `/etc/systemd`, `/usr/lib/systemd`, `/etc/kernel` carries the string — the shared library `/usr/lib/systemd/libsystemd-shared-262.1-1.so` (match at line 5005); **no unit or config file** references `credentials_boot_policy`. |

## CB input status (facts only; applicability is the L1's and the scribe's)

| CB row | probe | status |
|---|---|---|
| CB1 documented mechanism (S283) | not a host probe; `grep` of `corpus/knowledge/systemd262-credentials-boot-policy-r66.md` → rc 2 `No such file or directory` at probe time | **ABSENT** (note not on disk when probed; other seats own it) |
| CB2 host boot chain — limine `protocol: efi` | `grep -n 'protocol:' /boot/limine.conf` → `Permission denied (os error 13)`, rc 2 | **BLOCKED** (no-sudo boundary; `/boot` ESP is `fmask=0077`) |
| CB2 host boot chain — limine identity/version | `bootctl status` `Product: Limine 12.9.4`; `pacman -Q limine` → `limine 12.9.4-1`, rc 0 | **PRESENT** |
| CB2 host boot chain — UKI presence | `bootctl status` `Loader: └─/boot/EFI/Linux/omarchy_linux.efi` + `Current Stub` block; direct `ls /boot/EFI/Linux/` rc 2 Permission denied | **PRESENT** (via bootctl; direct listing BLOCKED) |
| CB2 host boot chain — stub version | `bootctl status` `Product: systemd-stub 262.1-1-arch` | **PRESENT** |
| CB2 host boot chain — `ENABLE_UKI` | `/etc/default/limine`: `ENABLE_UKI=yes`; `/etc/limine-entry-tool.conf:168`: `ENABLE_UKI=no` | **PRESENT** (two sources disagree; recorded, not interpreted) |
| CB3 policy input — cmdline token | `grep -c 'systemd.credentials_boot_policy=' /proc/cmdline` → `0`, rc 1 | **ABSENT** |
| CB3 policy input — TPM2 presence | `systemd-analyze has-tpm2` → `partial`, rc 3, `-firmware -driver`; `ls -la /sys/class/tpm/` → empty, rc 0 | **ABSENT** (no TPM device node) |
| CB3 policy input — SecureBoot state | efivar `SecureBoot-8be4df61-…` 5 bytes, sequential read `6 0 0 0 0` → data byte 0; `bootctl status` `Secure Boot: disabled` | **PRESENT** (mokutil itself ABSENT, rc 127) |
| CB4 applicability verdict + named falsifier | not a host read; depends on CB2+CB3 above | **NOT-A-HOST-INPUT** — prerequisites recorded; verdict text belongs to L1/scribe |

## Risks / caveats carried forward
- The prescribed `od -An -t u1 -j4 -N1` is not usable on `efivarfs` (non-seekable): it prints the
  offset-0 attribute byte (`6`) and exits 1 with `Illegal seek`. Verified against a seekable control
  file (`.ufo/waves/round-66/probes/r66-secureboot.txt`, last two blocks; `-j4` returns offset 4 only
  when the file is seekable). The SecureBoot value rests on the disclosed `-N5` sequential read plus
  bootctl's independent `Secure Boot: disabled`.
- `r66-cmdline.txt` deliberately does **not** contain raw cmdline values: the first capture wrote the
  verbatim line (which would have carried `resume`, `cryptdevice`, `root`, `zswap.*`, `rootflags`
  values), and it was rewritten before delivery so that only token names plus the has-value/bare shape
  remain, with `sha256(printf %s "$(cat /proc/cmdline)") = 690a9178…d79f7` as an integrity anchor.
  No secret, key, token, cookie or credential was ever part of that line.
- `Measured UKI: no` and `TPM2 Support: no` are bootctl's own readings; no interpretation is offered here.
