# FxCorrection3 — R18-CORR-03 / C1

**FAILS — Medium: mtime source-path identity is not enforced.** `tools/check-boot-chain.py:640-650` parses only the timestamp and basename on capture lines 124 and 115. It never checks that line 124 belongs to the `/boot/EFI/Linux:` listing at B:120. Thus the fixed B:124 quote `2026-10-20 09:26:22... omarchy_linux.efi` could remain unchanged under a different directory header and still satisfy the mtime source predicate; the claimed live-image location would no longer be established. In the observed capture, B:120–125 does show `/boot/EFI/Linux/omarchy_linux.efi` at 09:26:22, while B:110–116 places the 09:29:18 `omarchy_linux.efi_sha256_...` copy in `limine_history`. The correction text at `corpus/knowledge/boot-chain-r17.md:219-226` correctly assigns the mtime to B:124, not B:115, but the gate does not independently bind that assertion to the directory path.

**SURVIVES — R18-CORR-03 correction and independent fixed-ID check.** Original defect: lines 43–46 cited only linux-image hook hashes B:183–184 and installed hooks B:252–253, omitting linux-lts B:199–200. Corrected `Now` adds both. Capture B:183–184, B:199–200, and B:252–253 contains matching btrfs-overlayfs `eeac1ed3…` and plymouth `de852646…` digests for each image and installed hooks. `--statement-corrections` hardcodes CORR-03's ID, exact `Now`, heading, source line/quote, and compares all three digest locations for each hook (`check-boot-chain.py:92-98, 631-639, 692-737`); it does not rely on the generic notice registry alone.

B:59 is the complete pacman argv and lists 12 packages (including `linux-lts-headers`); B:82 is a truncated sudo-journal argv ending at `linux-lts`. This is 12 named packages, not 13; the historical 13 is transaction count. B:182/198/251 likewise support both-UKI init equality.

**Verification gaps:** Read-only review; no gate/selftest execution. LSP unavailable (`read xd://lsp` reported no such tool), so no LSP status/references/definition/diagnostics. Grep was used only to locate text, not as semantic proof.

Scope: executed=none
