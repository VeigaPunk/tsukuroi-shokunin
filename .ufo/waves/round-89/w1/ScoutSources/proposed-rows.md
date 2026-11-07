# Candidate rows for `corpus/knowledge/limine-uri-failure-r89.md` — seat ScoutSources, round-89 w1

Scout seat. These are **candidate** rows for the L1 to consider; the lane file was NOT edited.
Each quote is verbatim from the file and raw line range named in the same row, whitespace-normalised
(leading/trailing space stripped, internal whitespace runs collapsed), and at most 25 words.
Every quote was machine-checked as a substring of the whitespace-normalised quoted file.

Provenance of the quoted text:

| Row | File | Raw lines | sha256 of the quoted file |
|---|---|---|---|
| SR1 | v12.9.4 common/lib/part.s2.c | 1064-1074 | `70ec629297dc96a2d40e861ec052345c84bc1b45fab03f79a2fa5cb95476061f` |
| SR2 | v12.9.4 common/lib/part.s2.c | 1035-1048 | `70ec629297dc96a2d40e861ec052345c84bc1b45fab03f79a2fa5cb95476061f` |
| SR3 | v12.9.4 common/lib/part.s2.c | 1050-1062 | `70ec629297dc96a2d40e861ec052345c84bc1b45fab03f79a2fa5cb95476061f` |
| SR4 | v12.9.4 common/lib/tpm.c | 113-115 | `d6892d0b430c7639ad7e10d98715d4953892e81e9bfe9d7381c366cf0743f090` |
| SR5 | v12.9.4 common/protos/limine.c | 627-632 | `ed99ad82b04fc09763c1ec00ae761404758fb9db38d7fcd27613893136143501` |
| SR6 | v12.9.4 common/protos/limine.c | 1498-1502 | `ed99ad82b04fc09763c1ec00ae761404758fb9db38d7fcd27613893136143501` |
| SR7 | v12.9.4 common/lib/uri.c | 72-74 | `e06cac1212fec55150c109843e22dfe01cd618d4e81235e357d9a256e2a2ed6f` |
| SR8 | v12.9.4 common/lib/uri.c | 89-92 | `e06cac1212fec55150c109843e22dfe01cd618d4e81235e357d9a256e2a2ed6f` |
| SR9 | v12.9.4 common/lib/uri.c | 226-235 | `e06cac1212fec55150c109843e22dfe01cd618d4e81235e357d9a256e2a2ed6f` |
| SR10 | v12.9.4 common/lib/uri.c | 301-318 | `e06cac1212fec55150c109843e22dfe01cd618d4e81235e357d9a256e2a2ed6f` |
| SR11 | v12.9.4 common/lib/config.c | 488-492 | `aafc9c410a250efc9674e3c93e839d32ae2731ba2ca60bb7f5edd7ad5828fba8` |
| SR12 | v12.9.4 common/menu.c | 1719-1721 | `628001e88564525f8d1e0e6193ea86145e5613eaea97c04110545cd182168f95` |
| SR13 | v12.9.6/trunk common/lib/uri.c | 145-163 | `6f6642f138b6d0cda765870f95b8d7ef423419bd019447ab792a9739d1999a89` |
| SR14 | v12.9.6/trunk common/lib/panic.s2.c | 79-100 | `f7c13b9f9f709fb44444dec15ae104a6b91eb158592eeedfd205a60197a2825d` |
| SR15 | v12.9.6/trunk CONFIG.md | 73-78 | `f44f3a19133cb3dc14d6d8b402ed585feb98a36bc4b263c37aa92f621f603763` |
| SR16 | v12.9.6/trunk common/menu.c | 33-36 | `de1f7cc7b03869df63a5db3d38e0ff0c926f58dfc757794af1666373bc78851c` |
| SR17 | v12.9.5 common/lib/tpm.c | 117-127 | `c91734237cb2583f33d8beddf9fc0bd87392cc5c684f8a51c79fe367ac127898` |
| SR18 | v12.9.4 common/lib/panic.s2.c | 93-99 | `0233d557db8fdf96918350a305cde91a8a4aca33216d2ac8c712cf47c79a3ff1` |
| SR19 | v12.9.4 common/menu.c | 1719-1728 | `628001e88564525f8d1e0e6193ea86145e5613eaea97c04110545cd182168f95` |
| SR20 | v12.9.4 common/menu.c | 1711-1717 | `628001e88564525f8d1e0e6193ea86145e5613eaea97c04110545cd182168f95` |
| SR21 | v12.9.4 common/lib/panic.s2.c | 71-77 | `0233d557db8fdf96918350a305cde91a8a4aca33216d2ac8c712cf47c79a3ff1` |
| SR22 | v12.9.4 common/lib/print.s2.c | 180-202 | `8ab511c1d7020a6860b06edea16d633d5477704d2c895ec91235ef67902ba37d` |

`v12.9.4` = the tag clone, HEAD `8ad14430bc9f2c24679cda558981ef53e6e3b18c` — byte-identical to the lane's
r89 pins `chainload.c`/`panic.s2.c` and r87 pins `uri.c`/`config.c`/`menu.c`/`CONFIG.md` (see `receipt-cmp-urls.txt`).
`v12.9.6/trunk` = the shallow clone of the default branch `refs/heads/v12.x`, HEAD `89a9512c623a4779cc73e3869383876d54264b28`,
which is the `v12.9.6` tag (`refs/tags/v12.9.6^{}`); `refs/heads/trunk` is `31e8865c9545c337982f05415c30a8bc80055d07`,
whose `chainload.c` and `panic.s2.c` bytes are the same as the default branch's.
`v12.9.5` = tag `v12.9.5^{}` = `55a93085435aa1b8f91054df3794b2a43fb7984a`.

## Rows

### SR1 [src]

**Statement.** `volume_get_by_coord` is where a `boot(N)`/`hdd()`/`odd()` lookup silently ends: it walks `volume_index` for a volume whose drive index, optical flag and partition all match, and returns NULL with no message when none matches — the NULL the URI dispatcher sees is born in the volume layer, not in the dispatcher.

**Source, raw lines.** v12.9.4 common/lib/part.s2.c, raw 1064-1074
**Quote (13 words).** `if (volume_index[i]->index == drive && volume_index[i]->is_optical == optical && volume_index[i]->partition == partition) {`
**Note.** closes the entry's Limit: `volume_get_by_coord` was not opened

### SR2 [src]

**Statement.** `volume_get_by_guid` matches either the volume's own GPT GUID or its partition GUID (16-byte `memcmp` on each) and returns NULL when neither matches, so a `guid():/` URI can resolve through a partition GUID the operator did not name.

**Source, raw lines.** v12.9.4 common/lib/part.s2.c, raw 1035-1048
**Quote (11 words).** `if (volume_index[i]->part_guid_valid && memcmp(&volume_index[i]->part_guid, guid, 16) == 0) { return volume_index[i];`
**Note.** closes the entry's Limit: `volume_get_by_guid` was not opened

### SR3 [src]

**Statement.** `volume_get_by_fslabel` compares labels case-insensitively (`strcasecmp`) — the one case-insensitive string comparison in the volume layer, since both filesystems Limine reads a label from store it upper-cased.

**Source, raw lines.** v12.9.4 common/lib/part.s2.c, raw 1050-1062
**Quote (8 words).** `if (volume_index[i]->fslabel_valid && strcasecmp(volume_index[i]->fslabel, fslabel) == 0) {`
**Note.** closes the entry's Limit: `volume_get_by_fslabel` was not opened

### SR4 [src]

**Statement.** `tpm_present()` is a firmware-side question, not a Linux one: it is true iff the firmware located an EFI TCG2 or CC measurement protocol at boot, and `tpm.c` is compiled only under `#if defined (UEFI)`. An empty `/sys/class/tpm/` is a different signal and does not answer it.

**Source, raw lines.** v12.9.4 common/lib/tpm.c, raw 113-115
**Quote (12 words).** `bool tpm_present(void) { return tcg2 != NULL || cc != NULL; }`
**Note.** closes the entry's Limit: `tpm_present()` was not opened

### SR5 [src]

**Statement.** Each protocol's own failure message differs: the `limine` protocol says "Failed to open executable", `linux` (x86) says "Failed to open kernel", and the RISC-V `linux` path says "failed to open kernel" in lower case; all are `panic(true, …)`.

**Source, raw lines.** v12.9.4 common/protos/limine.c, raw 627-632
**Quote (17 words).** `)) == NULL) panic(true, "limine: Failed to open executable with path `%#`. Is the path correct?", kernel_path);`
**Note.** also linux_x86.c 270-277, multiboot1.c 78-83, multiboot2.c 118-123, linux_risc.c 683-685; closes the entry's Limit that these messages were not read

### SR6 [src]

**Statement.** A module path that cannot be opened is not uniformly fatal: the `limine` protocol warns and continues when the module is a non-required internal one (and panics when it is required), while the `linux` x86 protocol panics on any module path.

**Source, raw lines.** v12.9.4 common/protos/limine.c, raw 1498-1502
**Quote (10 words).** `} printv("limine: Warning: Non-required internal module `%#` not found\n", module_path);`
**Note.** compare common/protos/linux_x86.c 487-494, which always panics

### SR7 [src]

**Statement.** `uri_resolve` has a third silent failure besides a missing `(` or `):/`: an empty path after `):/` returns false with no message, and reaches the same "Failed to open image" panic as the other two.

**Source, raw lines.** v12.9.4 common/lib/uri.c, raw 72-74
**Quote (6 words).** `if (*uri == 0) return false;`

### SR8 [src]

**Statement.** A malformed pin in a `path:` is its own panic with its own message — "Blake2b hash must be 128 characters long" — not the "Failed to open image" panic and not a silent NULL.

**Source, raw lines.** v12.9.4 common/lib/uri.c, raw 89-92
**Quote (16 words).** `if (strlen(uri + i) != 128) { URI_ERROR("Blake2b hash must be 128 characters long"); return false;`
**Note.** also uri.c 95-101 (invalid hex character at position)

### SR9 [src]

**Statement.** `boot(N)`'s partition number is parsed with `strtoui` and never validated as a whole string, and only `val > 256` is rejected, so a non-numeric root yields 0 and a root with trailing characters yields its numeric prefix: `boot(x):/` silently opens partition 0.

**Source, raw lines.** v12.9.4 common/lib/uri.c, raw 226-235
**Quote (24 words).** `if (s_part[0] != '\0') { uint64_t val = strtoui(s_part, NULL, 10); if (val > 256) { URI_ERROR("Partition number outside range 0-256"); return NULL; }`
**Note.** with common/lib/misc.s2.c 56-77, where `strtoui` stops at the first non-digit

### SR10 [src]

**Statement.** A hash mismatch is a panic only when `hash_mismatch_panic` is set, and Secure Boot forces it on; with the value `no` a mismatch on a required key is a prompt whose `Y` answer continues the boot with the mismatching file.

**Source, raw lines.** v12.9.4 common/lib/uri.c, raw 301-318
**Quote (23 words).** `print("WARNING: Blake2b hash for URI `%#` does not match!\n" "         Press Y to continue, press any other key to return to menu...", uri);`
**Note.** with common/menu.c 1711-1717, where Secure Boot forces hash_mismatch_panic = true

### SR11 [src]

**Statement.** Limine's "Secure Boot is active" is narrower than the firmware's flag: `init_config` clears `secure_boot_active` when the config carries no enrolled checksum, and USAGE.md 52-56 says an unenrolled checksum means none of the Secure Boot hardening applies.

**Source, raw lines.** v12.9.4 common/lib/config.c, raw 488-492
**Quote (11 words).** `if (memcmp((void *)config_b2sum, CONFIG_B2SUM_EMPTY, 128) == 0) { secure_boot_active = false;`
**Note.** also USAGE.md 52-56

### SR12 [src]

**Statement.** `measured_boot`'s value is compared with `strcmp`, so only the exact lower-case `yes` enables it, while `hash_mismatch_panic` is matched case-insensitively — the two global booleans of the same config are parsed by different rules.

**Source, raw lines.** v12.9.4 common/menu.c, raw 1719-1721
**Quote (10 words).** `measured_boot = measured_boot_str != NULL && strcmp(measured_boot_str, "yes") == 0;`
**Note.** compare common/menu.c 1711-1712, which uses strcasecmp

### SR13 [src freshness]

**Statement.** Upstream v12.9.5 added a Fast-Boot retry under UEFI: a volume that is not found makes Limine connect all disks and search again — for `hdd()`, `odd()`, `guid()`/`uuid()` and `fslabel()`, but not for `boot()`, which still looks the volume up once.

**Source, raw lines.** v12.9.6/trunk common/lib/uri.c, raw 145-163
**Quote (23 words).** `// volume not found may be on one of its other disks, so all are connected and // the search is had again.`
**Note.** compare v12.9.4 uri.c 344-366, where the dispatch has no retry; the retry wraps hdd/odd/guid/fslabel, not boot()

### SR14 [src freshness]

**Statement.** The two rules this entry is built on are unchanged upstream: `chainload()`'s failure path is byte-identical between v12.9.4 (raw 414-437) and v12.9.6/trunk (raw 429-452), and `panic()`'s menu-return rule is byte-identical (raw 71-92 vs 79-100).

**Source, raw lines.** v12.9.6/trunk common/lib/panic.s2.c, raw 79-100
**Quote (17 words).** `allow_menu == true) { print("Press a key to return to %s.", booting_from_editor ? "editor" : "menu");  getchar();`
**Note.** v12.9.5 added only a screen clear before the PANIC line under the UEFI fallback terminal

### SR15 [src freshness]

**Statement.** Upstream v12.9.6 changed the config grammar: global options must come before the first menu entry and any that follow it are ignored — so a `hash_mismatch_panic: no` that ever sat after the first entry would be silently dropped by an upgrade.

**Source, raw lines.** v12.9.6/trunk CONFIG.md, raw 73-78
**Quote (23 words).** `*Global options* must come before the first *menu entry*. Any that come after it are part of an entry, where they are ignored.`
**Note.** compare v12.9.4 CONFIG.md 73-75

### SR16 [src freshness]

**Statement.** Upstream v12.9.5 changed `limine_efi_vendor_guid`, the vendor GUID of the `LimineLastBootedEntry` EFI variable, so an upgrade stops reading the last-booted entry written by the older build.

**Source, raw lines.** v12.9.6/trunk common/menu.c, raw 33-36
**Quote (18 words).** `EFI_GUID limine_efi_vendor_guid = { 0x03884334, 0x1756, 0x4978, { 0x9c, 0x8c, 0x86, 0xfb, 0x89, 0x98, 0xb4, 0xea } };`
**Note.** compare v12.9.4 common/menu.c 33-36

### SR17 [src freshness]

**Statement.** Upstream v12.9.5 changed measured boot's TPM handling: a full event log now counts the component as measured with one warning, where v12.9.4 had no `EFI_VOLUME_FULL` branch at all.

**Source, raw lines.** v12.9.5 common/lib/tpm.c, raw 117-127
**Quote (11 words).** `tcg2, 0, (EFI_PHYSICAL_ADDRESS)(uintptr_t)data, (EFI_UINT64)data_size, event); if (status == EFI_VOLUME_FULL) { tpm_log_full();`
**Note.** compare v12.9.4 common/lib/tpm.c, which has no EFI_VOLUME_FULL handling

### SR18 [src]

**Statement.** The `System halted.` string is UEFI-only: under BIOS the same `allow_menu == false` path prints "Press CTRL+ALT+DEL to reboot." and calls `rm_hcf()` instead of spinning on `hlt`, so the halt half of UF7 is a UEFI statement.

**Source, raw lines.** v12.9.4 common/lib/panic.s2.c, raw 93-99
**Quote (8 words).** `#if defined (BIOS) print("Press CTRL+ALT+DEL to reboot."); rm_hcf();`
**Note.** compare common/lib/panic.s2.c 97-99, the UEFI branch that prints "System halted." and halts

### SR19 [src]

**Statement.** Measured boot is a UEFI-only notion in Limine: the `measured_boot` force-off when no TPM/CC measurement interface exists sits inside `#if defined (UEFI)`, so on BIOS the menu return is never refused for measurement reasons.

**Source, raw lines.** v12.9.4 common/menu.c, raw 1719-1728
**Quote (16 words).** `// Cannot do measured boot without a TPM/CC interface. if (!tpm_present()) { measured_boot = false; }`
**Note.** compare common/lib/panic.s2.c 23-29, whose measured-boot branch is likewise UEFI-only

### SR20 [src]

**Statement.** Under Secure Boot with an enrolled config hash, an `efi` entry whose pin is present but WRONG still panics: `chainload()`'s clearing of `secure_boot_active` suppresses only the no-hash rule, while the mismatch check reads `hash_mismatch_panic`, which Secure Boot forces to true — so UF6's "a pin that IS present is still compared" ends in a panic, not a warning.

**Source, raw lines.** v12.9.4 common/menu.c, raw 1711-1717
**Quote (9 words).** `if (secure_boot_active) { hash_mismatch_panic = true; editor_enabled = false;`
**Note.** compare common/protos/chainload.c 426-437 (only the no-hash rule is waived) and common/lib/uri.c 301-305

### SR21 [src]

**Statement.** A `panic(true, …)` returns to the menu only while the firmware's boot services are still up: under UEFI the menu-return branch is gated on `efi_boot_services_exited == false`, so a panic raised after the handoff halts the machine even with no measured boot.

**Source, raw lines.** v12.9.4 common/lib/panic.s2.c, raw 71-77
**Quote (21 words).** `if ( #if defined (BIOS) stage3_loaded == true && #elif defined (UEFI) efi_boot_services_exited == false && #endif allow_menu == true) {`
**Note.** compare common/lib/panic.s2.c 93-99, the branch that prints "System halted."

### SR22 [src]

**Statement.** The panic text differs in what it shows the operator: the `efi` protocol prints the path with `%s`, so the screen keeps the `#<blake2b>` pin, while the `linux`, `limine` and `multiboot` protocols print with `%#`, whose handler cuts the string at the last `#` and so hides the pin.

**Source, raw lines.** v12.9.4 common/lib/print.s2.c, raw 180-202
**Quote (23 words).** `for (int i = (int)strlen(str) - 1; i >= 0; i--) { if (str[i] != '#') { continue; }  prn_nstr(print_buf, &print_buf_i, str, i);`
**Note.** compare common/protos/chainload.c 435 (`%s`) with common/protos/linux_x86.c 277 (`%#`)

