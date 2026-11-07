# Candidate rows — C2 entry `corpus/knowledge/limine-tpm-volume-r90.md` — seat ScoutTPM, round-90 w1

Scout seat (TPM half). These are **candidate** rows for the L1 to consider; the lane file was NOT edited.
The C2 entry was already landed by the L1 at `b380483e` (rows TV1–TV8, sources S365–S371). Rows **A1–A12**
below are *extensions* to the landed entry, each labelled with the landed row it strengthens or the gap it
closes; row **A13/A14** are supplementary volume rows. Every quote is verbatim from the file and raw line
range named in the same row, whitespace-normalised (leading/trailing space stripped, internal whitespace runs
collapsed), at most 25 words. Every quote was machine-checked as a substring of the whitespace-normalised
quoted file (script output in `receipt-quotes.txt`).

Provenance of the quoted text:

| Row | File | Raw lines | sha256 of the quoted file |
|---|---|---|---|
| A1 | TCG EFI Protocol Specification rev13 (PDF, p. 29) | §6.4.4 item 5 | `40a2568e99bc110c10c551ab921be8aaeb784da017b045090f0e5630d3f9ddc3` |
| A1 | TCG EFI Protocol Specification rev13 (PDF, p. 28) | Table 6 | same |
| A1 | TCG EFI Protocol Specification rev13 (PDF, p. 24) | Table 4 | same |
| A1 | TCG EFI Protocol Specification rev13 (PDF, p. 37) | §6.8.3 | same |
| A2 | PicoEFI inc/efi/efitcg2.h @ 0515ccde | 11-12, 28-47 | `40114b1da10065176918ab9d6384dad2012347ffcf4f2b1be87349ee41b632b7` |
| A2 | PicoEFI inc/efi/eficc.h @ 0515ccde | 10-11 | `e68d7c75cf6880d77ace9a4ea9126a8500f423672e9823904afbd0fbd2286ef6` |
| A3 | Limine v12.9.4 common/lib/tpm.c | 74-115 | `d6892d0b430c7639ad7e10d98715d4953892e81e9bfe9d7381c366cf0743f090` |
| A4 | systemd v262.1 src/boot/measure.c | 153-217 | `c5cec8ff6cc488a29e3b695bfab832358e903ec978ea5878074922212b1b54c6` |
| A5 | systemd v262.1 src/boot/export-vars.c | 57-63 | `d540e62739897486305298dc39eb8ad9a95384bd8492bbc8f2420a4f3d3c34ec` |
| A6 | systemd v262.1 src/shared/efi-api.c | 533-598 | `695b4e0391cbaedf83b7ad1a188ed4731386fc430f2666b7a0b11fa3a3649148` |
| A7 | systemd v262.1 src/shared/tpm2-util.c | 11889-11898, 11943, 11961 | `b2c4b041aeab2ff97a59cb3bffc27a8749b722c2ac01f2376f186ee86a7591f3` |
| A7 | systemd v262.1 src/shared/tpm2-util.h | 592-597 | `549aa7765c2f8ac46393ba41cbba2e4aa758d227b84e3ba42e01d0be7c8492db` |
| A8 | systemd v262.1 src/boot/stub.c | 1256-1257, 127 | `c7bb6617250b13aae986f44c75ea558bb5155dc0a6fc738baf457d5d92f4501a` |
| A8 | systemd v262.1 src/boot/boot.c | 3295, 3454 | `f66975c01a94588ddb00b8c7a71cd378bf8777b2f7ba08eab26dd8a36685df96` |
| A9 | Limine v12.9.4 common/protos/chainload.c | 354-411, 507, 541 | `316eb17df996f91252791b1351e8f88c027ceeb8535becc1a247d614d8b5e1a7` |
| A10 | Limine v12.9.4 common/lib/bli.c | 89-124 | `9fb49c513e8a411ee596b0844c86e264e8be4995381b3a6464356d7b45284c7a` |
| A11 | edk2 MdePkg/Include/Uefi/UefiMultiPhase.h @ edk2-stable202511 | 15-17 | `0d192475bafdfcb3cef9ef54e9499fdf96d0a648a5a1ec738d9c24f05a2faa0e` |
| A12 | Limine v12.9.4 common/entry.s3.c | 83 | `9aef63d37c750fdb316bf5739d618d1f00abd12179d8ad59121fb5936ed83732` |
| A13 | Limine v12.9.4 common/drivers/disk.s2.c | 909, 925-926, 952-956 | `34e3a81fee89f045f76b01029440ed92fc03836179e8b9f3e6f721c7f5b799d2` |

`v12.9.4` = the tag clone, HEAD `8ad14430bc9f2c24679cda558981ef53e6e3b18c`; its `common/menu.c`, `common/lib/uri.c`
and `common/lib/tpm.c` are byte-identical to the lane's r87/r89/r90 pins (`.ufo/waves/round-90/before/src/cmp-pins.txt`,
`.ufo/waves/round-90/after/src-c2/SHA256SUMS`).
`v262.1` = the systemd tag clone, HEAD `73612ea502d53baf9b0df4336cfc296a7ee0d524` (the host runs `systemd 262.1-1`);
its `export-vars.c` and `measure.c` are byte-identical to the lane's `after/src-c2` pins.
`@ 0515ccde` = PicoEFI as pinned by Limine v12.9.4's own `bootstrap` (lines 72-75), fetched from that commit.

---

## A1 — [src] the primary spec defines what `0x00000000` means (closes the spec gap in TV2)

**Statement.** The TCG EFI Protocol Specification rev13 states, for a platform with no TPM, that
`GetCapability` SHALL return `TPMPresentFlag = FALSE` and `ActivePcrBanks = 0`; it also states that
`GetActivePcrBanks()` returns the same bitmap as the capability's `ActivePcrBanks` field, and that
`GetActivePcrBanks` is implemented only from protocol version 1.1 on. So a firmware that reports no TPM
answers "no TPM present" with a zero bank mask, and a `0xffffffff` mask is a *different* thing: a protocol
too old to report banks. This is the normative source the landed entry cites only through systemd's code.

**Source, raw lines.** TCG EFI Protocol Specification rev13 (Family "2.0", Level 00 Revision 00.13,
2016-03-30), p. 29 §6.4.4 item 5; p. 28 Table 6; p. 24 Table 4; p. 37 §6.8.3.
PDF sha256 `40a2568e99bc110c10c551ab921be8aaeb784da017b045090f0e5630d3f9ddc3`, fetched 2026-11-07 from
<https://www.trustedcomputinggroup.org/wp-content/uploads/EFI-Protocol-Specification-rev13-160330final.pdf>
(redirects to `medias.cdn.trustedcomputinggroup.org/production/EFI_Protocol_Specification_rev13_160330final_791550543b.pdf`,
same sha256).

**Quote (≤25 words), p. 29 §6.4.4(5).** "If the platform does not have a TPM then the following values SHALL be returned: ProtocolCapability.TPMPresentFlag = FALSE"

**Quote (≤25 words), p. 29 §6.4.4(5) (continuation).** "ProtocolCapability.NumberOfPcrBanks = 0 ProtocolCapability.ActivePcrBanks = 0"

**Quote (≤25 words), p. 28 Table 6.** "TPMPresentFlag|False = TPM not present"

**Quote (≤25 words), p. 37 §6.8.3.** "The returned bitmap is the same as the ActivePcrBanks field in the EFI_TCG2_BOOT_SERVICE_CAPABILITY structure."

**Quote (≤25 words), p. 24 Table 4.** "GetActivePcrBanks|Returns a bitmap of currently active TPM PCR banks. (Only implemented for ProtocolVersion 1.1 or above.)"

**Note.** strengthens landed TV2 (which states the 0 / 0xffffffff distinction from systemd's `measure.c` alone)
with the normative source; adds no new host claim.

---

## A2 — [src] the GUIDs Limine actually asks the firmware for, and where the struct lives

**Statement.** Limine v12.9.4 has no EFI headers of its own: `bootstrap` pins PicoEFI at
`0515ccde7a3ac9c52e32c9c21c924a8d50d3261e` and `common/common.mk` adds `-I ../picoefi/inc`. The TCG2 protocol
Limine locates is `{607f766c-7455-42be-930b-e4d76db2720f}` and the confidential-computing fallback
`{96751a3d-72f4-41a6-a794-ed5d0e67ae6b}`. The capability structure Limine reads is PicoEFI's: 36 bytes,
not packed, `TPMPresentFlag` at offset 16 and `ActivePcrBanks` at offset 32 (measured by compiling PicoEFI's
header with gcc 16.2.1; the same offsets come out of systemd's own copy of the structure, `src/boot/proto/tcg.h`,
compiled the same way — so the stub and Limine read byte-identical firmware fields).

**Source, raw lines.** PicoEFI `inc/efi/efitcg2.h` 11-12, 28-47; `inc/efi/eficc.h` 10-11;
Limine v12.9.4 `common/lib/tpm.c` 75, 92.

**Quote (≤25 words), efitcg2.h 11-12.** "#define EFI_TCG2_PROTOCOL_GUID {0x607f766c, 0x7455, 0x42be, {0x93, 0x0b, 0xe4, 0xd7, 0x6d, 0xb2, 0x72, 0x0f}}"

**Quote (≤25 words), efitcg2.h 28.** "/* Explicitly not packed, unlike the document's other structures: 36 bytes. */"

**Quote (≤25 words), efitcg2.h 35.** "EFI_BOOLEAN TPMPresentFlag;"

**Quote (≤25 words), eficc.h 10-11.** "#define EFI_CC_MEASUREMENT_PROTOCOL_GUID {0x96751a3d, 0x72f4, 0x41a6, {0xa7, 0x94, 0xed, 0x5d, 0xe, 0x67, 0xae, 0x6b}}"

**Host value (2026-11-07).** [obs] no SEV/TDX: `/dev/sev*` absent, `/proc/cpuinfo` has no `sev` flag, no `tdx`
module, `/sys/class/tpm/` empty — so Limine's CC fallback leg cannot be what makes `tpm_present()` true here.

---

## A3 — [src] the two legs of Limine's `tpm_present()`, and where the TCG2 leg is decided

**Statement.** `tpm_init()` locates the TCG2 protocol and keeps it only if `GetCapability` succeeds **and**
`TPMPresentFlag` is set; otherwise it falls back to the EFI CC measurement protocol and keeps that if its
`GetCapability` succeeds. `tpm_present()` is then true if either pointer is non-NULL. The TCG2 leg is decided
by `TPMPresentFlag` alone — Limine does not test the capability `Size` field and does not call
`GetActivePcrBanks()` at all; it reads `cap.ActivePcrBanks` out of the `GetCapability` struct.

**Source, raw lines.** Limine v12.9.4 `common/lib/tpm.c` 74-115.

**Quote (≤25 words), tpm.c 82-83.** "status = tcg2_proto->GetCapability(tcg2_proto, &cap); if (status == EFI_SUCCESS && cap.TPMPresentFlag) {"

**Quote (≤25 words), tpm.c 91.** "// No TCG2/TPM 2.0; fall back to the CC measurement protocol."

**Quote (≤25 words), tpm.c 113-115.** "return tcg2 != NULL || cc != NULL;"

**Quote (≤25 words), tpm.c 85-86.** "printv(\"tpm: TCG2 protocol located, TPM present (active PCR banks: %x)\n\","

**Note.** strengthens landed TV1 with the exact decision points; the `printv` is verbose-gated
(`common/lib/print.h` 12-14 `if (verbose) print(FMT, ##__VA_ARGS__);`), so on this host the verdict is not on
screen — the landed TV4 Limit already says so.

---

## A4 — [src] what systemd's stub measured, precisely (three ways to reach `0`)

**Statement.** The systemd stub's `tpm_get_active_pcr_banks()` reaches `0` on three distinct firmware
outcomes: (a) `tcg2_interface_check()` returned NULL — no TCG2 protocol, or `GetCapability` failed, or
`TPMPresentFlag` was clear; (b) `GetActivePcrBanks()` itself failed (logged as a warning, then `0`); and it
returns `UINT32_MAX` — a *distinct* value, written as `0xffffffff` — only when a TCG2 protocol exists but is
older than version 1.1. So `0x00000000` on this host means "the stub's TCG2 probe found no present TPM (or
the bank query failed)", and it is not the "protocol too old" marker.

**Source, raw lines.** systemd v262.1 `src/boot/measure.c` 153-217.

**Quote (≤25 words), measure.c 157-159.** "err = BS->LocateProtocol(MAKE_GUID_PTR(EFI_TCG2_PROTOCOL), NULL, (void **) &tcg); if (err != EFI_SUCCESS) return NULL;"

**Quote (≤25 words), measure.c 177-178.** "if (!capability.TPMPresentFlag) return NULL;"

**Quote (≤25 words), measure.c 199-201.** "tpm2 = tcg2_interface_check(&version); if (!tpm2) return 0;"

**Quote (≤25 words), measure.c 210-214.** "err = tpm2->GetActivePcrBanks(tpm2, &active_pcr_banks); if (err != EFI_SUCCESS) { log_warning_status(err, \"Failed to get TPM2 active PCR banks, assuming none: %m\"); return 0; }"

**Note.** sharpens landed TV2's "returns 0 when …" with the `GetActivePcrBanks()` failure branch named.

---

## A5 — [src] who writes the variable, and in what format

**Statement.** systemd's `export_common_variables()` writes `LoaderTpm2ActivePcrBanks` **only if it is not
already set**, as the string `"0x%08x"` of `tpm_get_active_pcr_banks()` — hence the host's
`0x00000000`. The same function is called by systemd-boot (`src/boot/boot.c` 3454) **and** by the systemd
stub (`src/boot/stub.c` 1256); on this host the stub is the writer, because `LoaderInfo` is
`Limine 12.9.4` (Limine's own brand, `common/lib/bli.c` 13, 92-96) — sd-boot would have overwritten it with
`systemd-boot …` (`boot.c` 3295) — and `StubInfo` is `systemd-stub 262.1-1-arch` (`stub.c` 127).

**Source, raw lines.** systemd v262.1 `src/boot/export-vars.c` 57-63; `src/boot/stub.c` 1256-1257, 127;
`src/boot/boot.c` 3295, 3454; Limine v12.9.4 `common/lib/bli.c` 13, 92-96.

**Quote (≤25 words), export-vars.c 58-61.** "if (efivar_get_raw(MAKE_GUID_PTR(LOADER), u\"LoaderTpm2ActivePcrBanks\", NULL, NULL) != EFI_SUCCESS) { uint32_t active_pcr_banks = tpm_get_active_pcr_banks();"

**Quote (≤25 words), export-vars.c 61.** "s = xasprintf(\"0x%08x\", active_pcr_banks);"

**Quote (≤25 words), boot.c 3295.** "(void) efivar_set_str16(MAKE_GUID_PTR(LOADER), u\"LoaderInfo\", u\"systemd-boot \" GIT_VERSION, 0);"

**Quote (≤25 words), stub.c 127.** "(void) efivar_set_str16(MAKE_GUID_PTR(LOADER), u\"StubInfo\", u\"systemd-stub \" GIT_VERSION, 0);"

**Host value (2026-11-07).** [obs] `LoaderInfo` = `Limine 12.9.4`; `StubInfo` = `systemd-stub 262.1-1-arch`;
`LoaderImageIdentifier` = `EFI\Linux\omarchy_linux.efi`; `StubImageIdentifier` = `EFI\Linux\omarchy_linux.efi`.

**Note.** strengthens landed TV2/TV3 by naming *which* of the two callers wrote it on this host, using
`LoaderInfo` as the discriminator.

---

## A6 — [src] how the OS reads the variable back — and why `0x00000000` survives the round trip

**Statement.** The OS side reads the same variable: `efi_get_active_pcr_banks()` parses it with
`safe_atou32_full(s, 16, …)` — base 16 with the `0x` prefix that the stub wrote, which `strtoul` accepts
(verified: `strtoul("0x00000000", 16)` = 0, consumes all 10 characters, no error; gcc 16.2.1) — and
`loader_has_tpm2()` reports a TPM only when the parsed mask is non-zero. `efi_has_tpm2()` then consults the
loader first, calling the loader's answer "the most accurate source of information regarding the firmware's
setup". So on this host the OS's own firmware-TPM verdict is false because the loader's variable is zero.

**Source, raw lines.** systemd v262.1 `src/shared/efi-api.c` 533-598.

**Quote (≤25 words), efi-api.c 545.** "r = efi_get_variable_string(EFI_LOADER_VARIABLE_STR(\"LoaderTpm2ActivePcrBanks\"), &active_pcr_banks);"

**Quote (≤25 words), efi-api.c 589-597.** "static int loader_has_tpm2(void) { uint32_t active_pcr_banks; int r; r = efi_get_active_pcr_banks(&active_pcr_banks); if (r < 0) return r; return active_pcr_banks != 0; }"

**Quote (≤25 words), efi-api.c 615-617.** "Secondly, check if the loader told us, as that is the most accurate source of information regarding the firmware's setup"

**Note.** new: the landed entry has no OS-side reader row; this is the reader that `systemd-analyze has-tpm2`
uses (A7).

---

## A7 — [obs] one no-sudo Linux command that answers `--tpm-present` on this host

**Statement.** `systemd-analyze has-tpm2` on this host prints `partial`, `-firmware`, `-driver`, `+system`,
`+subsystem`, `+libraries`, and exits **3**. Its exit status is the inverted mask of the *missing* API bits
(`~s & TPM2_SUPPORT_API`), so `3` = `1 (FIRMWARE) | 2 (DRIVER)` — the firmware bit is missing, and the driver
bit is missing because `/sys/class/tpmrm/` exists but is empty (the kernel has the TPM subsystem compiled in
but no device bound). The `-firmware` bit is the OS reading the very same `LoaderTpm2ActivePcrBanks` variable
(A6), i.e. the kernel side agrees with the stub: the firmware reported no TPM2. So the operator has a plain
Linux command that corroborates `--tpm-present 0` without touching `/sys/firmware/efi/efivars` by hand.

**Source, raw lines.** systemd v262.1 `src/shared/tpm2-util.c` 11889-11898, 11943, 11961;
`src/shared/tpm2-util.h` 592-597.

**Quote (≤25 words), tpm2-util.c 11889, 11893-11894.** "r = dir_is_empty(\"/sys/class/tpmrm\", /* ignore_hidden_or_backup= */ false); ... else if (r == 0) /* populated! */ support |= TPM2_SUPPORT_SUBSYSTEM|TPM2_SUPPORT_DRIVER;"

**Quote (≤25 words), tpm2-util.c 11943.** "printf(\"%spartial%s\\n\", ansi_yellow(), ansi_normal());"

**Quote (≤25 words), tpm2-util.c 11961.** "return ~s & TPM2_SUPPORT_API;"

**Quote (≤25 words), tpm2-util.h 592.** "TPM2_SUPPORT_FIRMWARE     = 1 << 0,  /* firmware reports TPM2 was used */"

**Host value (2026-11-07).** [obs] `systemd-analyze has-tpm2` → `partial`, `-firmware`, `-driver`,
`+system`, `+subsystem`, `+libraries`, exit 3; `/sys/class/tpm/` empty; `/sys/class/tpmrm/` empty;
`/dev/tpm*` absent; `journalctl -k -b | grep -i tpm` → no match; `ls /sys/firmware/acpi/tables | grep -i -e
TPM2 -e TCPA` → no match; `/proc/config.gz` has `CONFIG_TCG_TPM=y`, `CONFIG_TCG_TIS=y`, `CONFIG_TCG_CRB=y`.

**Note.** new operator action; strengthens landed TV4 (which had only the efivar read) with a second,
Linux-side, no-sudo confirmation of the same answer.

---

## A8 — [inf] the stub's probe and Limine's probe are the same firmware, in the same boot session

**Statement.** The UKI that Limine chainloads (`/EFI/Linux/omarchy_linux.efi`, per the host's
`/boot/limine.conf` `protocol: efi` entry) carries a systemd-stub; Limine starts it with
`gBS->LoadImage` / `gBS->StartImage` and does not exit boot services before that. The device path Limine
builds for the chainloaded image is *relative* — leading `/` dropped, `/` mapped to `\` — and the host's
`LoaderImageIdentifier` is exactly `EFI\Linux\omarchy_linux.efi`, i.e. that relative path. The stub therefore
ran **inside Limine's own UEFI session**, after `tpm_init()` but before any `ExitBootServices`, so its
`GetCapability`/`TPMPresentFlag` answer describes the same firmware state Limine queried — the landed TV4's
remaining gap ("the stub ran after Limine, not inside it") is narrower than stated: the stub ran *inside
Limine's session*, on the same firmware, later in the same boot.

**Source, raw lines.** Limine v12.9.4 `common/protos/chainload.c` 354-411, 507, 541;
`common/lib/misc.c` 483; systemd v262.1 `src/boot/export-vars.c` 36-41 (the stub's
`LoaderImageIdentifier` write).

**Quote (≤25 words), chainload.c 356-357.** "expected to be relative to the EFI_LOADED_IMAGE_PROTOCOL::DeviceHandle."

**Quote (≤25 words), chainload.c 377.** "efi_file_path[j++] = efi_file_path[i] == '/' ? '\\\\' : efi_file_path[i];"

**Quote (≤25 words), chainload.c 507.** "status = gBS->LoadImage(0, efi_image_handle,"

**Quote (≤25 words), chainload.c 541.** "EFI_STATUS exit_status = gBS->StartImage(new_handle, &exit_data_size, &exit_data);"

**Host value (2026-11-07).** [obs] `LoaderImageIdentifier` = `EFI\Linux\omarchy_linux.efi`;
`StubImageIdentifier` = `EFI\Linux\omarchy_linux.efi`; `/boot/limine.conf` line 30 (host receipt):
`path: boot():/EFI/Linux/omarchy_linux.efi#b990d8c6…`.

**Note.** strengthens landed TV4's inference; it does not remove the remaining gap (a TPM with
`TPMPresentFlag` set whose `GetActivePcrBanks` fails would also read `0` — A4).

---

## A9 — [obs] the variable is volatile, so the value on disk belongs to *this* boot

**Statement.** The variable's EFI attribute bytes are `06 00 00 00` = `EFI_VARIABLE_BOOTSERVICE_ACCESS (0x02)`
| `EFI_VARIABLE_RUNTIME_ACCESS (0x04)`, with `EFI_VARIABLE_NON_VOLATILE (0x01)` **absent**. A variable
without the non-volatile bit does not survive a reset, so the `0x00000000` read now was written during the
current boot — and because systemd only writes it when unset (A5), it is this boot's stub measurement, not a
leftover from an earlier firmware state. This closes the "is the value stale?" question that the landed TV3
raises only implicitly.

**Source, raw lines.** edk2 `MdePkg/Include/Uefi/UefiMultiPhase.h` @ `edk2-stable202511` 15-17 (the bit
values); host value from `.ufo/waves/round-90/after/host-c2-receipt.txt` (L1) and this seat's own
`od -An -tx1 -N4` read.

**Quote (≤25 words), UefiMultiPhase.h 15-17.** "#define EFI_VARIABLE_NON_VOLATILE 0x00000001 #define EFI_VARIABLE_BOOTSERVICE_ACCESS 0x00000002 #define EFI_VARIABLE_RUNTIME_ACCESS 0x00000004"

**Host value (2026-11-07).** [obs] `LoaderTpm2ActivePcrBanks` attributes `06 00 00 00`, value
`0x00000000` (UTF-16LE, 10 characters + NUL).

**Note.** new source (the EFI variable-attribute bits) and a new narrowing of landed TV3/TV4.

---

## A10 — [src] Limine writes no TPM variable at all (the negative that fixes the writer question)

**Statement.** Limine's Boot Loader Interface writer sets `LoaderInfo`, `LoaderFeatures`,
`LoaderDevicePartUUID`, `LoaderEntries` and `LoaderEntrySelected` — and no TPM variable. There is no `Tpm2`
string anywhere in Limine v12.9.4. So the writer of `LoaderTpm2ActivePcrBanks` on this host is unambiguously
a systemd component (the UKI's stub, per A5), not Limine.

**Source, raw lines.** Limine v12.9.4 `common/lib/bli.c` 89-124.

**Quote (≤25 words), bli.c 92-96.** "gRT->SetVariable(L\"LoaderInfo\", &bli_vendor_guid, EFI_VARIABLE_BOOTSERVICE_ACCESS | EFI_VARIABLE_RUNTIME_ACCESS, sizeof(LIMINE_BRAND), LIMINE_BRAND);"

**Quote (≤25 words), bli.c 119.** "gRT->SetVariable(L\"LoaderDevicePartUUID\","

**Note.** strengthens landed TV2 ("Limine writes LoaderInfo and LoaderDevicePartUUID but no TPM variable")
with the exhaustive statement (a repo-wide `grep -rn "Tpm2" --include=*.c` returns nothing).

---

## A11 — [obs] `Limine 12.9.4` here is Limine's brand string, and the EFI-side GUID of the ESP is the same
number Linux prints as PARTUUID

**Statement.** `LoaderInfo` = `Limine 12.9.4` is `LIMINE_BRAND`, i.e. `L"Limine " LIMINE_VERSION` — the
version string of the bootloader that ran, which pins the firmware-side code to the same v12.9.4 tag this
seat read. `LoaderDevicePartUUID` = `b80445be-18ee-45e6-9a30-14339ea785a7` is the GPT unique partition GUID
of the volume Limine booted from, and it is the same value `blkid` reports as `PARTUUID` for
`/dev/nvme0n1p1`. The vfat *filesystem* serial `86D8-C3F6` is a different number and is not a GPT GUID.

**Source, raw lines.** Limine v12.9.4 `common/lib/bli.c` 13, 109-124; host receipt
`.ufo/waves/round-90/after/host-c2-receipt.txt` and this seat's `blkid -o full /dev/nvme0n1p1`.

**Quote (≤25 words), bli.c 13.** "#define LIMINE_BRAND L\"Limine \" LIMINE_VERSION"

**Quote (≤25 words), bli.c 110-111.** "if (boot_volume->part_guid_valid) { char part_uuid_str[37]; guid_to_string(&boot_volume->part_guid, part_uuid_str);"

**Host value (2026-11-07).** [obs] `blkid -o full /dev/nvme0n1p1` →
`UUID="86D8-C3F6" … PARTUUID="b80445be-18ee-45e6-9a30-14339ea785a7"`; `LoaderDevicePartUUID` =
`b80445be-18ee-45e6-9a30-14339ea785a7`.

**Note.** strengthens landed TV6 (which names `guid(b80445be-…)`/`uuid(b80445be-…)` as the ESP-naming URIs)
by tying the number to the EFI variable Limine itself wrote, and to Linux's PARTUUID.

---

## A12 — [src] Limine probes the TPM before it reads the config, so the verdict cannot depend on `measured_boot`

**Statement.** `tpm_init()` is called once, in stage-3 entry, before the menu and before the configuration is
parsed. The measured-boot decision (`menu.c` 1719-1728) is later and *uses* that probe: measured boot is
requested by the first `measured_boot` key line saying exactly `yes` or by Secure Boot, and is forced off when
`!tpm_present()`. So the firmware's TPM answer is a boot-time fact independent of the config file, and the
config's `measured_boot` key can only turn measurement *on*, never substitute for a TPM.

**Source, raw lines.** Limine v12.9.4 `common/entry.s3.c` 83; `common/menu.c` 1719-1728.

**Quote (≤25 words), entry.s3.c 83.** "tpm_init();"

**Quote (≤25 words), menu.c 1720-1721.** "char *measured_boot_str = config_get_value(NULL, 0, \"MEASURED_BOOT\"); measured_boot = measured_boot_str != NULL && strcmp(measured_boot_str, \"yes\") == 0;"

**Quote (≤25 words), menu.c 1725-1727.** "// Cannot do measured boot without a TPM/CC interface. if (!tpm_present()) { measured_boot = false; }"

**Note.** strengthens landed TV4's operator action 1 (adding `measured_boot: yes` turns a panic into a halt
*only* once a TPM is present).

---

## A13 — [src] `hdd(d:p)`'s drive number is Limine's own firmware enumeration order, not a Linux device name

**Statement.** Limine numbers UEFI block devices itself: it enumerates `BLOCK_IO_PROTOCOL` handles, skips
logical partitions, and assigns `index = hdd_indices++` (optical drives get a separate counter). A partition
of that drive is then `index + 1`. The mapping from that counter to Linux's `/dev/nvme0n1` is not observable
from Linux, so no `hdd()`/`odd()` URI can be written from host tools; `boot()`/`guid()` can.

**Source, raw lines.** Limine v12.9.4 `common/drivers/disk.s2.c` 909, 925-926, 952-956, 960;
`common/lib/part.s2.c` 575.

**Quote (≤25 words), disk.s2.c 909.** "int optical_indices = 1, hdd_indices = 1;"

**Quote (≤25 words), disk.s2.c 925-926.** "if (drive->Media->LogicalPartition) continue;"

**Quote (≤25 words), disk.s2.c 952-956.** "if (is_optical) { block->index = optical_indices++; block->is_optical = true; } else { block->index = hdd_indices++; }"

**Quote (≤25 words), part.s2.c 575.** "ret->partition   = partition + 1;"

**Note.** supplementary; strengthens the landed TV8 limit ("`hdd(d:p)` needs Limine's firmware drive index,
which Linux does not show").

---

## A14 — [obs] the ESP's filesystem label is empty, so `fslabel()` cannot name it

**Statement.** `blkid` reports no `LABEL` and no `PARTLABEL` for `/dev/nvme0n1p1`, so the FAT volume label a
`fslabel()` URI would compare against is empty; Limine reads that label out of the FAT root directory
(`fs_get_label` → `fat32_get_label`) and compares it with `strcasecmp`. Independently of the label, Limine
never reads a filesystem GUID (`fs_get_guid` returns false for every filesystem), so the vfat serial
`86D8-C3F6` cannot be named by `guid()`/`uuid()` either.

**Source, raw lines.** Limine v12.9.4 `common/lib/part.s2.c` 1050-1062; `common/fs/file.s2.c` 13-31, 27-31;
host `blkid -o value -s LABEL /dev/nvme0n1p1` (empty) and `blkid -o full /dev/nvme0n1p1`.

**Quote (≤25 words), part.s2.c 1055-1056.** "if (volume_index[i]->fslabel_valid && strcasecmp(volume_index[i]->fslabel, fslabel) == 0) {"

**Quote (≤25 words), file.s2.c 27-30.** "bool fs_get_guid(struct guid *guid, struct volume *part) { (void)guid; (void)part; return false; }"

**Note.** supplementary; corroborates landed TV5/TV7 from the host side.

---

## Rows this seat did **not** propose (already covered by the landed entry)

- `tpm_present()`'s two legs — landed TV1 (A3 only adds decision points).
- Who writes `LoaderTpm2ActivePcrBanks` — landed TV2 (A5/A8/A10 only narrow *which* writer, on this host).
- `guid()`/`uuid()`/`fslabel()` dispatch and the ESP-naming URIs — landed TV5/TV6/TV7 (A11/A13/A14 corroborate).
- `boot()`/`boot(N)` and the GPT numbering — landed TV8.

## Open items this seat leaves to the L1

1. The spec row (A1) is a **new registry source** (TCG EFI Protocol Specification rev13, tier A docs) and the
   PicoEFI, edk2, systemd-`efi-api.c`/`tpm2-util.c`/`stub.c`/`boot.c` and Limine-`chainload.c`/`disk.s2.c`/
   `bli.c`/`entry.s3.c` files are **new registry sources** too (S365–S371 cover only `tpm.c`, `part.s2.c`,
   `file.s2.c`, `bli.c`, `export-vars.c`, `measure.c` and the host receipts). Drafts in `proposed-sources.md`.
2. A8 narrows TV4's stated gap but does not close it: a TPM whose `TPMPresentFlag` is set while
   `GetActivePcrBanks()` fails also reads `0` (A4). The residual gap should stay open in the entry.
3. Nothing here was executed against a TPM: no firmware setting was changed, nothing was booted, and no
   `/sys/firmware/efi/efivars` file was written.
