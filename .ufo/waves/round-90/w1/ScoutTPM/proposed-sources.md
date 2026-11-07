# SOURCES row drafts — seat ScoutTPM, round-90 w1 (TPM half of C2)

Drafts only; `corpus/SOURCES.md` was NOT edited. Ids are `TBD` as instructed (the registry's next free ids
are S372+ after the landed S371). Format follows the registry: id | source | kind | tier | scope | anchor |
teaches | status | opened | recheck | used-by.

Every URL below was fetched and its content hash checked during this seat (see `receipt-sources.txt` for the
exact commands and hashes). The four Limine/systemd files already in the registry (S365 `tpm.c`, S366
`part.s2.c`, S367 `file.s2.c`, S368 `bli.c`, S369 `export-vars.c`, S370 `measure.c`, S371 host receipts) are
**not** re-drafted; the drafts below are the *additional* sources this seat opened.

---

## TBD-1 — TCG EFI Protocol Specification rev13 (primary spec)

| field | value |
|---|---|
| id | TBD (suggest S372) |
| source | TCG EFI Protocol Specification, Family "2.0", Level 00 Revision 00.13, 2016-03-30 — <https://www.trustedcomputinggroup.org/wp-content/uploads/EFI-Protocol-Specification-rev13-160330final.pdf> (redirects to `https://medias.cdn.trustedcomputinggroup.org/production/EFI_Protocol_Specification_rev13_160330final_791550543b.pdf`; PDF sha256 `40a2568e99bc110c10c551ab921be8aaeb784da017b045090f0e5630d3f9ddc3`, 1189538 bytes, both URLs hash-identical) |
| kind | docs |
| tier | A |
| scope | The normative definition of `EFI_TCG2_BOOT_SERVICE_CAPABILITY` (size, `TPMPresentFlag`, `ActivePcrBanks`), of the no-TPM reply, and of the `GetActivePcrBanks()` service — the primary source behind "what does `LoaderTpm2ActivePcrBanks = 0x00000000` mean" |
| anchor | p. 24 Table 4 (GetActivePcrBanks, "Only implemented for ProtocolVersion 1.1 or above."); p. 27 §6.4.3 struct; p. 28 Table 6 ("TPMPresentFlag \| False = TPM not present"; "ActivePcrBanks \| A bitmap of currently active PCR banks …"); p. 29 §6.4.4 item 5 (no TPM ⇒ `TPMPresentFlag = FALSE`, `ActivePcrBanks = 0`); p. 37 §6.8.3 ("The returned bitmap is the same as the ActivePcrBanks field …"); p. 24 §6.4 ("not packed", 36 bytes on x86) |
| teaches | A zero active-bank mask is the spec's own encoding of "no TPM present"; `0xffffffff` is instead "protocol too old to report banks" (v1.0); `GetActivePcrBanks()` and the capability's `ActivePcrBanks` field carry the same bitmap |
| status | mined |
| opened | 2026-11-07 |
| recheck | on-release (spec revision) |
| used-by | corpus/knowledge/limine-tpm-volume-r90.md (candidate rows A1) |

---

## TBD-2 — PicoEFI `inc/efi/efitcg2.h` (the EFI headers Limine v12.9.4 compiles against)

| field | value |
|---|---|
| id | TBD (suggest S373) |
| source | PicoEFI `inc/efi/efitcg2.h` at commit `0515ccde7a3ac9c52e32c9c21c924a8d50d3261e` — <https://raw.githubusercontent.com/PicoEFI/PicoEFI/0515ccde7a3ac9c52e32c9c21c924a8d50d3261e/inc/efi/efitcg2.h> (sha256 `40114b1da10065176918ab9d6384dad2012347ffcf4f2b1be87349ee41b632b7`) |
| kind | code |
| tier | A |
| scope | The EFI GUIDs and the `EFI_TCG2_BOOT_SERVICE_CAPABILITY` layout that Limine v12.9.4 actually uses — Limine vendors no EFI headers of its own |
| anchor | lines 11-12 (`EFI_TCG2_PROTOCOL_GUID` `{607f766c-7455-42be-930b-e4d76db2720f}`); 19-21 (bitmap typedefs); 28-41 (the 36-byte unpacked capability struct: `TPMPresentFlag` at offset 16, `ActivePcrBanks` at offset 32); 43-47 (`EFI_TCG2_BOOT_HASH_ALG_*` values) |
| teaches | Which protocol GUID Limine asks the firmware for; that `ActivePcrBanks` is an `EFI_TCG2_EVENT_ALGORITHM_BITMAP`; the exact byte offsets of the two fields Limine and the systemd stub read (measured by compiling this header: sizeof 36, `TPMPresentFlag` 16, `ActivePcrBanks` 32 — identical to systemd's own `src/boot/proto/tcg.h`) |
| status | mined |
| opened | 2026-11-07 |
| recheck | on-release |
| used-by | corpus/knowledge/limine-tpm-volume-r90.md (candidate rows A2, A3) |

---

## TBD-3 — PicoEFI `inc/efi/eficc.h` (the confidential-computing fallback protocol)

| field | value |
|---|---|
| id | TBD (suggest S374) |
| source | PicoEFI `inc/efi/eficc.h` at commit `0515ccde7a3ac9c52e32c9c21c924a8d50d3261e` — <https://raw.githubusercontent.com/PicoEFI/PicoEFI/0515ccde7a3ac9c52e32c9c21c924a8d50d3261e/inc/efi/eficc.h> (sha256 `e68d7c75cf6880d77ace9a4ea9126a8500f423672e9823904afbd0fbd2286ef6`) |
| kind | code |
| tier | A |
| scope | The GUID of the protocol Limine's second `tpm_present()` leg looks for |
| anchor | lines 10-11 (`EFI_CC_MEASUREMENT_PROTOCOL_GUID` `{96751a3d-72f4-41a6-a794-ed5d0e67ae6b}`) |
| teaches | That the "CC measurement protocol" leg of `tpm_present()` is a specific EFI protocol (Intel TDX / AMD SEV-SNP platforms), not a generic "confidential computing" flag — so a `--tpm-present 1` answer on such a host is about TDX/SNP, not about a TPM |
| status | mined |
| opened | 2026-11-07 |
| recheck | on-release |
| used-by | corpus/knowledge/limine-tpm-volume-r90.md (candidate row A2) |

---

## TBD-4 — systemd v262.1 `src/shared/efi-api.c` (the OS-side reader of the loader variable)

| field | value |
|---|---|
| id | TBD (suggest S375) |
| source | systemd v262.1 `src/shared/efi-api.c` — <https://raw.githubusercontent.com/systemd/systemd/v262.1/src/shared/efi-api.c> (sha256 `695b4e0391cbaedf83b7ad1a188ed4731386fc430f2666b7a0b11fa3a3649148`) |
| kind | code |
| tier | A |
| scope | How the running OS interprets `LoaderTpm2ActivePcrBanks`, and therefore how `systemd-analyze has-tpm2` reaches its `firmware` verdict |
| anchor | lines 533-586 (`efi_get_active_pcr_banks`: reads the variable, `safe_atou32_full(s, 16, …)`, `UINT32_MAX` special case, EFI→TCG bank-bit conversion); 589-598 (`loader_has_tpm2`: `return active_pcr_banks != 0;`); 601-652 (`efi_has_tpm2`: loader first — "the most accurate source of information regarding the firmware's setup" — then the ACPI `TPM2` table, then the kernel event log) |
| teaches | A zero mask in the loader variable ⇒ the OS concludes "no TPM2 in firmware"; the loader's answer is preferred over the ACPI-table check; the hex string the stub wrote round-trips through `strtoul` base 16 |
| status | mined |
| opened | 2026-11-07 |
| recheck | on-release |
| used-by | corpus/knowledge/limine-tpm-volume-r90.md (candidate rows A6, A7) |

---

## TBD-5 — systemd v262.1 `src/shared/tpm2-util.c` and `src/shared/tpm2-util.h` (the `has-tpm2` verdict and its exit status)

| field | value |
|---|---|
| id | TBD (suggest S376) |
| source | systemd v262.1 `src/shared/tpm2-util.c` — <https://raw.githubusercontent.com/systemd/systemd/v262.1/src/shared/tpm2-util.c> (sha256 `b2c4b041aeab2ff97a59cb3bffc27a8749b722c2ac01f2376f186ee86a7591f3`); `src/shared/tpm2-util.h` — <https://raw.githubusercontent.com/systemd/systemd/v262.1/src/shared/tpm2-util.h> (sha256 `549aa7765c2f8ac46393ba41cbba2e4aa758d227b84e3ba42e01d0be7c8492db`) |
| kind | code |
| tier | A |
| scope | What `systemd-analyze has-tpm2` prints and what its exit status means |
| anchor | `tpm2-util.c` 11880-11899 (`tpm2_support_full`: `/sys/class/tpmrm` empty ⇒ subsystem but no driver), 11937-11961 (`verb_has_tpm2_generic`: `yes`/`no`/`partial` and `return ~s & TPM2_SUPPORT_API;`), 4022-4025 (the `LoaderTpm2ActivePcrBanks == 0` ⇒ "TPM support is not available in the firmware" reading); `tpm2-util.h` 588-597 (`TPM2_SUPPORT_*` bit values, the exit-status ABI) |
| teaches | `has-tpm2`'s exit status is the inverted mask of the *missing* API bits, so `3` = missing `FIRMWARE` and `DRIVER`; an empty `/sys/class/tpmrm` yields `+subsystem` without `+driver`; the zero loader mask is read by systemd as "TPM support is not available in the firmware" |
| status | mined |
| opened | 2026-11-07 |
| recheck | on-release |
| used-by | corpus/knowledge/limine-tpm-volume-r90.md (candidate row A7) |

---

## TBD-6 — systemd v262.1 `src/boot/stub.c` and `src/boot/boot.c` (which component writes the loader variables)

| field | value |
|---|---|
| id | TBD (suggest S377) |
| source | systemd v262.1 `src/boot/stub.c` — <https://raw.githubusercontent.com/systemd/systemd/v262.1/src/boot/stub.c> (sha256 `c7bb6617250b13aae986f44c75ea558bb5155dc0a6fc738baf457d5d92f4501a`); `src/boot/boot.c` — <https://raw.githubusercontent.com/systemd/systemd/v262.1/src/boot/boot.c> (sha256 `f66975c01a94588ddb00b8c7a71cd378bf8777b2f7ba08eab26dd8a36685df96`) |
| kind | code |
| tier | A |
| scope | Which systemd component writes `LoaderTpm2ActivePcrBanks` and the sibling `Loader*` variables, and how the two are told apart on a host |
| anchor | `stub.c` 1256-1257 (`export_common_variables(loaded_image); export_stub_variables(loaded_image, profile);`), 127 (`StubInfo` = `systemd-stub <version>`); `boot.c` 3454 (`export_common_variables(loaded_image);`), 3295 (`LoaderInfo` = `systemd-boot <version>`) |
| teaches | Both sd-boot and the systemd stub call `export_common_variables()`; `LoaderInfo` says which one ran (`systemd-boot …` vs `Limine …`), `StubInfo` says the UKI's stub ran — so on this host the writer of `LoaderTpm2ActivePcrBanks` is the UKI's systemd-stub, not sd-boot |
| status | mined |
| opened | 2026-11-07 |
| recheck | on-release |
| used-by | corpus/knowledge/limine-tpm-volume-r90.md (candidate row A5) |

---

## TBD-7 — Limine v12.9.4 `common/protos/chainload.c` (how the UKI is started, and with which device path)

| field | value |
|---|---|
| id | TBD (suggest S378) |
| source | Limine v12.9.4 `common/protos/chainload.c` — <https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/protos/chainload.c> (sha256 `316eb17df996f91252791b1351e8f88c027ceeb8535becc1a247d614d8b5e1a7`; byte-identical to the landed S361 pin) |
| kind | code |
| tier | A |
| scope | That the `efi` protocol starts the UKI inside Limine's own UEFI session, with a relative device path |
| anchor | lines 354-411 (`build_relative_efi_file_path`: "expected to be relative to the EFI_LOADED_IMAGE_PROTOCOL::DeviceHandle", leading `/` dropped, `/`→`\`), 507 (`gBS->LoadImage`), 541 (`gBS->StartImage`) |
| teaches | The systemd-stub inside the chainloaded UKI runs in the same firmware session as Limine's own TPM probe, and its `FilePath` is the relative path Limine built — which is why `LoaderImageIdentifier` reads `EFI\Linux\omarchy_linux.efi` |
| status | mined |
| opened | 2026-11-07 |
| recheck | on-release |
| used-by | corpus/knowledge/limine-tpm-volume-r90.md (candidate row A8) |

---

## TBD-8 — Limine v12.9.4 `common/entry.s3.c` (when the TPM probe happens)

| field | value |
|---|---|
| id | TBD (suggest S379) |
| source | Limine v12.9.4 `common/entry.s3.c` — <https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/entry.s3.c> (sha256 `9aef63d37c750fdb316bf5739d618d1f00abd12179d8ad59121fb5936ed83732`) |
| kind | code |
| tier | A |
| scope | Where in the boot Limine asks the firmware about the TPM |
| anchor | line 83 (`tpm_init();`, in `uefi_entry`, before the menu and before the configuration is parsed) |
| teaches | The firmware's TPM answer is a boot-time fact taken before the config is read, so `measured_boot: yes` in the config can only request measurement, never supply a TPM |
| status | mined |
| opened | 2026-11-07 |
| recheck | on-release |
| used-by | corpus/knowledge/limine-tpm-volume-r90.md (candidate row A12) |

---

## TBD-9 — Limine v12.9.4 `common/drivers/disk.s2.c` (Limine's own drive numbering)

| field | value |
|---|---|
| id | TBD (suggest S380) |
| source | Limine v12.9.4 `common/drivers/disk.s2.c` — <https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/drivers/disk.s2.c> (sha256 `34e3a81fee89f045f76b01029440ed92fc03836179e8b9f3e6f721c7f5b799d2`) |
| kind | code |
| tier | A |
| scope | Where the drive number in an `hdd(d:p)`/`odd(d:p)` URI comes from |
| anchor | lines 909, 925-926 (logical partitions skipped), 952-956 (`block->index = hdd_indices++` / `optical_indices++`), 960 (`block->partition = 0` for the whole disk) |
| teaches | Limine numbers drives in its own firmware enumeration order, so `hdd(d:p)` cannot be written from Linux device names; combined with `part.s2.c` 575 (GPT partition = index + 1) |
| status | mined |
| opened | 2026-11-07 |
| recheck | on-release |
| used-by | corpus/knowledge/limine-tpm-volume-r90.md (candidate row A13) |

---

## TBD-10 — edk2 `MdePkg/Include/Uefi/UefiMultiPhase.h` (EFI variable attribute bits)

| field | value |
|---|---|
| id | TBD (suggest S381) |
| source | edk2 `MdePkg/Include/Uefi/UefiMultiPhase.h` at tag `edk2-stable202511` — <https://raw.githubusercontent.com/tianocore/edk2/edk2-stable202511/MdePkg/Include/Uefi/UefiMultiPhase.h> (sha256 `0d192475bafdfcb3cef9ef54e9499fdf96d0a648a5a1ec738d9c24f05a2faa0e`) |
| kind | code |
| tier | A |
| scope | The numeric meaning of an EFI variable's attribute bytes — how to read `06 00 00 00` off `/sys/firmware/efi/efivars/*` |
| anchor | lines 15-17 (`EFI_VARIABLE_NON_VOLATILE 0x00000001`, `EFI_VARIABLE_BOOTSERVICE_ACCESS 0x00000002`, `EFI_VARIABLE_RUNTIME_ACCESS 0x00000004`) |
| teaches | `06` = boot-service + runtime access with the non-volatile bit absent ⇒ the variable does not survive a reset, so a value read now belongs to the current boot |
| status | mined |
| opened | 2026-11-07 |
| recheck | on-release |
| used-by | corpus/knowledge/limine-tpm-volume-r90.md (candidate row A9) |

---

## TBD-11 — edk2 `MdePkg/Include/Protocol/Tcg2Protocol.h` (the UEFI-side header stating the same semantics)

| field | value |
|---|---|
| id | TBD (suggest S382) |
| source | edk2 `MdePkg/Include/Protocol/Tcg2Protocol.h` at tag `edk2-stable202511` — <https://raw.githubusercontent.com/tianocore/edk2/edk2-stable202511/MdePkg/Include/Protocol/Tcg2Protocol.h> (sha256 `0a95b6e5a545347e43f2d6dfd57ef91547789c690382802ef4094924ddea3fcd`) |
| kind | code |
| tier | A |
| scope | A second, independent statement of the `TPMPresentFlag` semantics and the `EFI_TCG2_BOOT_HASH_ALG_*` bank-bit values |
| anchor | line 59-62 ("// False = TPM not present" / `BOOLEAN TPMPresentFlag;`), 32-87 (the capability struct), 89-93 (`EFI_TCG2_BOOT_HASH_ALG_*`) |
| teaches | Independent corroboration of the spec's Table 6 wording, in code an implementer reads |
| status | mined |
| opened | 2026-11-07 |
| recheck | on-release |
| used-by | corpus/knowledge/limine-tpm-volume-r90.md (candidate row A1) |

---

## TBD-12 — this seat's own read-only host receipt (TPM signals and ESP identity, re-run)

| field | value |
|---|---|
| id | TBD (suggest S383) |
| source | ScoutTPM read-only host receipt, round-90 w1 — `.ufo/waves/round-90/w1/ScoutTPM/receipt-host.txt` (own-work) |
| kind | own-work |
| tier | A |
| scope | This host's TPM signals (efivar attributes and value, `/sys/class/tpm`, `/sys/class/tpmrm`, `/dev/tpm*`, kernel log, ACPI tables, `systemd-analyze has-tpm2` output and exit status, `CONFIG_TCG_*`) and the ESP's identifiers (`blkid`) |
| anchor | the receipt file, in order: `od -An -tx1 -N4` + UTF-16 decode of `LoaderTpm2ActivePcrBanks`; `ls /sys/class/tpm/`, `/sys/class/tpmrm/`; `ls /dev/tpm*`; `journalctl -k -b --no-pager | grep -i -m5 tpm`; `ls /sys/firmware/acpi/tables | grep -i -e TPM2 -e TCPA`; `systemd-analyze has-tpm2` (+ exit status); `zgrep -E '^CONFIG_(TCG_TPM|TCG_TIS|TCG_CRB)=' /proc/config.gz`; `blkid -o full /dev/nvme0n1p1`; `od` of `StubInfo`/`LoaderInfo`/`StubImageIdentifier`/`LoaderDevicePartUUID` |
| teaches | The measured answer to the gate's `--tpm-present` on this host, and the second (Linux-side, no-sudo) confirmation of it via `systemd-analyze has-tpm2` |
| status | mined |
| opened | 2026-11-07 |
| recheck | after any boot that follows a firmware TPM change, and after any ESP change (event trigger), else 30d |
| used-by | corpus/knowledge/limine-tpm-volume-r90.md (candidate rows A7, A11, A14) |

---

## Sources this seat opened but did NOT propose as registry rows

- Limine v12.9.4 `common/lib/print.h` (`printv` is verbose-gated) and `common/lib/misc.s2.c` (`verbose = false`
  default) — used only to justify a note in A3; the landed entry's TV4 Limit already carries the point.
- Limine v12.9.4 `common/lib/uri.c`, `common/lib/part.s2.c`, `common/fs/file.s2.c`, `common/lib/bli.c`,
  `common/lib/tpm.c` — already registered (S351, S366, S367, S368, S365); re-opened here only to confirm the
  landed rows, all byte-identical to the pins.
- `common/menu.c` (S353), `common/lib/config.c` (S352), `common/lib/panic.s2.c` (S362) — re-opened, unchanged.
- systemd v262.1 `src/boot/measure.c`, `src/boot/export-vars.c` — already registered (S370, S369).
- UEFI 2.10 §8.2 (runtime variable services): **not opened** — `uefi.org` returned HTTP 403 for every
  attempt (spec HTML and PDF); the attribute-bit semantics are therefore cited from edk2's header (TBD-10),
  and no UEFI-spec text is claimed.
- Trusted Computing Group "TCG PC Client Platform TPM Profile" and the TCG EFI Protocol PDF's §5.4 PCR-bank
  explanation: not opened; not claimed.
- `TPMPERBIOSFLAGS` / `AMITCGPPIVAR` payloads: read on the host, **not decoded** — their layout is
  vendor-private and no primary source defining them was opened; no claim is made about their meaning.
