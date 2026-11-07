# Candidate rows for `corpus/knowledge/limine-tpm-volume-r90.md` — seat ScoutVolume, round-90 w1

Scout seat, volume half of C2. These are **candidate** rows for the L1 to consider; the lane file was NOT edited.
Each quote is verbatim from the pinned upstream file, whitespace-normalised (leading/trailing space stripped, internal
whitespace runs collapsed), at most 25 words, and machine-checked as a substring of the whitespace-normalised
quoted file range (0 failures over 37 quotes; `receipt-quote-verification.txt`).

Provenance of the quoted text: Limine tag **v12.9.4**, clone HEAD `8ad14430bc9f2c24679cda558981ef53e6e3b18c`
(verified identical to `raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/...` for every file below —
`receipt-upstream-vs-clone.txt`). The four files already in the lane's pinned set
(`.ufo/waves/round-90/before/src/`: `uri.c`, `config.c`, `menu.c`, `chainload.c`) are byte-identical to the
clone (`receipt-pins-vs-clone.txt`). `part.s2.c`, `file.s2.c`, `bli.c`, `entry.s3.c`, `guid.c` are additionally
byte-identical to the L1's own `.ufo/waves/round-90/after/src-c2/` pins (`receipt-src-c2-vs-clone.txt`).
`fat32.s2.c`, `iso9660.s2.c`, `disk.s2.c` are NEW opens (not yet pinned by the lane) — see `proposed-sources.md`.

## Host facts used (all read-only, this round)

| Fact | Value | Where |
|---|---|---|
| ESP device | `/dev/nvme0n1p1`, PARTN 1, PARTUUID `b80445be-18ee-45e6-9a30-14339ea785a7`, vfat, UUID `86D8-C3F6`, mounted `/boot` | `.ufo/waves/round-90/before/host/receipt.txt` lines 26-44 (lsblk/findmnt) |
| ESP FAT label | empty (`lsblk` LABEL column blank; `/run/blkid/blkid.tab` has no `LABEL=` for the ESP) | receipt line 36; `lsblk -o LABEL`; `blkid.tab` |
| EFI var `LoaderDevicePartUUID` | `b80445be-18ee-45e6-9a30-14339ea785a7` (UTF-16, 37 wchars) | read from `/sys/firmware/efi/efivars/` this round |
| Limine config on host | `/boot/limine.conf`; every `path:` is `boot():/…`; no `measured_boot`, no `on_panic` | receipt lines 47-72 |


### SV1

**Statement.** [src] `guid(X)` and `uuid(X)` are the same dispatcher: `uri_guid_dispatch` parses the argument text as a **mixed-endian** GUID first (`string_to_guid_mixed`), looks the volume up, and only if that finds nothing retries the same text as a **big-endian** GUID (`string_to_guid_be`). A text that is not a GUID-shaped string returns NULL with no message of its own.

**Source, raw lines.** v12.9.4 common/lib/uri.c, raw 172-176
**Quote (18 words).** `static struct file_handle *uri_guid_dispatch(char *guid_str, char *path) { struct guid guid; if (!string_to_guid_mixed(&guid, guid_str)) { return NULL; }`
**Host value.** —

**Byte order, measured.** `guid_to_string` (guid.c 78-93) and `string_to_guid_mixed` (guid.c 58-69) are exact inverses on GUID text: compiled from the pinned upstream `common/lib/guid.c`, 50000 random GUID texts round-trip identically and the 20000 random raw-byte renderings collide 0 times (`receipt-guid-harness.txt`). The mixed parse therefore reproduces exactly the byte order the GPT entry and `header.disk_guid` are stored in — this is the reason the `lsblk` PARTUUID text is the text a `guid()` URI must carry.

### SV2

**Statement.** [src] The `guid()` lookup matches **two** different GUID namespaces, in this order: a volume's own `guid` field, then its `part_guid`. Both are 16-byte `memcmp`s; a match on either returns that volume.

**Source, raw lines.** v12.9.4 common/lib/part.s2.c, raw 1037-1040
**Quote (12 words).** `if (volume_index[i]->guid_valid && memcmp(&volume_index[i]->guid, guid, 16) == 0) { return volume_index[i]; }`
**Host value.** —

**Also quoted (SV4b, part.s2.c 1041-1044).** `if (volume_index[i]->part_guid_valid && memcmp(&volume_index[i]->part_guid, guid, 16) == 0) { return volume_index[i]; }`

### SV3

**Statement.** [src] A partition volume's `guid` field is populated **only** from `fs_get_guid`, and in v12.9.4 `fs_get_guid` returns false for every filesystem — so no filesystem UUID ever satisfies a `guid()` URI on this version. A FAT volume serial (`86D8-C3F6` on this host's ESP) is not a GUID-shaped string either (`is_valid_guid` requires dashes at 8/13/18/23 and a NUL at 36), so `guid(86D8-C3F6)` is rejected by the parser before any lookup happens.

**Source, raw lines.** v12.9.4 common/fs/file.s2.c, raw 27-31
**Quote (13 words).** `bool fs_get_guid(struct guid *guid, struct volume *part) { (void)guid; (void)part; return false; }`
**Host value.** ESP vfat serial `86D8-C3F6` (never matches)

**Also quoted (SV6, part.s2.c 582-587).** `if (!fs_get_guid(&guid, ret)) { ret->guid_valid = false; } else { ret->guid_valid = true; ret->guid = guid; }`
**Also quoted (SV36, guid.c 10-15).** `case 8: case 13: case 18: case 23: if (s[i] != '-') return false;`

### SV4

**Statement.** [src] A partition's `part_guid` is the GPT entry's **unique partition GUID**, and only GPT partitions get one: the MBR path sets `part_guid_valid = false`. The whole-medium volume, by contrast, gets a `guid` from the GPT **header**'s disk GUID. So `guid()` addresses a GPT partition by its PARTUUID and a GPT whole disk by its disk GUID, and never an MBR partition.

**Source, raw lines.** v12.9.4 common/lib/part.s2.c, raw 597-598
**Quote (6 words).** `ret->part_guid_valid = true; ret->part_guid = entry.unique_partition_guid;`
**Host value.** ESP PARTUUID `b80445be-18ee-45e6-9a30-14339ea785a7`

**Also quoted (SV8, part.s2.c 869-870).** `ret->part_guid_valid = false; ret->part_type_guid_valid = false;`
**Also quoted (SV9, disk.s2.c 986-988).** `if (gpt_get_guid(&block->guid, block)) { block->guid_valid = true; }`
**Also quoted (SV10, part.s2.c 495).** `*guid = header.disk_guid;`

### SV5

**Statement.** [src] `boot(N)` is not a free-standing partition selector: it resolves against **the same drive index as the boot volume** and the volume's own partition number. With an empty root it uses the boot volume's own partition number; with `N` it parses `N` (0-256, above that a `URI_ERROR`) and asks for partition `N` of the boot volume's drive.

**Source, raw lines.** v12.9.4 common/lib/uri.c, raw 233-238
**Quote (14 words).** `} else { partition = boot_volume->partition; } struct volume *volume = volume_get_by_coord(boot_volume->is_optical, boot_volume->index, partition);`
**Host value.** host has no `boot(N)` URI

**Also quoted (SV13, uri.c 220-224).** `static struct file_handle *uri_boot_dispatch(char *s_part, char *path) { if (boot_volume->pxe) return uri_tftp_dispatch(s_part, path); }`
**Also quoted (SV14, uri.c 226-232).** `if (s_part[0] != '\0') { uint64_t val = strtoui(s_part, NULL, 10); if (val > 256) { URI_ERROR("Partition number outside range 0-256");`
**Also quoted (SV19, part.s2.c 1066-1069).** `if (volume_index[i]->index == drive && volume_index[i]->is_optical == optical && volume_index[i]->partition == partition) { return volume_index[i]; }`

### SV6

**Statement.** [src] GPT partition numbers are **1-based over the GPT entry slots**, not over the partitions that exist: `ret->partition = partition + 1` where `partition` is the entry index, and the enumeration loop skips empty slots without renumbering. An MBR logical partition is numbered 5+.

**Source, raw lines.** v12.9.4 common/lib/part.s2.c, raw 575-575
**Quote (5 words).** `ret->partition = partition + 1;`
**Host value.** ESP is PARTN 1 on `nvme0n1`

**Also quoted (SV11b, part.s2.c 847).** `ret->partition = partition + 4 + 1;`
**Also quoted (SV12, disk.s2.c 1010-1013).** `if (ret == END_OF_TABLE || ret == INVALID_TABLE) break; if (ret == NO_PARTITION) continue;`

### SV7

**Statement.** [src] `fslabel(L)` compares labels **case-insensitively** (`strcasecmp`) and matches either a FAT volume label or an ISO 9660 volume identifier; both are read per volume at enumeration time. The FAT label comes from the root directory's volume-label entry (attribute `0x08`), not from the BPB label field, and the BPB's `volume_serial_number` is never used for identity at all.

**Source, raw lines.** v12.9.4 common/lib/part.s2.c, raw 1055-1057
**Quote (10 words).** `if (volume_index[i]->fslabel_valid && strcasecmp(volume_index[i]->fslabel, fslabel) == 0) { return volume_index[i];`
**Host value.** ESP FAT label empty -> no `fslabel()` URI names this host's ESP

**Also quoted (SV21, file.s2.c 16-22).** `if ((ret = fat32_get_label(part)) != NULL) { return ret; } if ((ret = iso9660_get_label(part)) != NULL) { return ret; }`
**Also quoted (SV22, fat32.s2.c 513-522).** `if (name == NULL) { if (directory_entries[i].attribute != FAT32_ATTRIBUTE_VOLLABEL) { continue; } char *r = ext_mem_alloc(12); memcpy(r, directory_entries[i].file_name_and_ext, 11);`
**Also quoted (SV23, fat32.s2.c 71-72).** `uint32_t volume_serial_number; char label[11];`
**Also quoted (SV35, iso9660.s2.c 146-151).** `char *iso9660_get_label(struct volume *vol) { struct iso9660_primary_volume pv; if (!iso9660_find_PVD(&pv, vol)) { return NULL; }`

### SV8

**Statement.** [src] `hdd(d:p)` and `odd(d:p)` are **drive-index** selectors, and the two index spaces are disjoint: `hdd` asks for a non-optical volume, `odd` for an optical one. The drive number must be 1-256 (an omitted drive is a `URI_ERROR`) and the partition 0-256. The indices are Limine's own enumeration counters (`hdd_indices`/`optical_indices` starting at 1), not the host's device names, so a `hdd()` URI on this host cannot be written from Linux's `lsblk` output.

**Source, raw lines.** v12.9.4 common/lib/uri.c, raw 150-152
**Quote (7 words).** `struct volume *volume = volume_get_by_coord(false, drive, partition);`
**Host value.** unmappable: Limine's drive index order is firmware-determined; host `lsblk` shows device names, not Limine indices

**Also quoted (SV30, uri.c 164-166).** `struct volume *volume = volume_get_by_coord(true, drive, partition);`
**Also quoted (SV16, uri.c 118-120).** `if (*loc == 0) { URI_ERROR("Drive number cannot be omitted for hdd():/ and odd():/");`
**Also quoted (SV17, uri.c 123-125).** `if (val < 1 || val > 256) { URI_ERROR("Drive number outside range 1-256");`
**Also quoted (SV18, uri.c 134-139).** `val = strtoui(loc, NULL, 10); if (val > 256) { URI_ERROR("Partition number outside range 0-256"); return false; }`
**Also quoted (SV27, disk.s2.c 909).** `int optical_indices = 1, hdd_indices = 1;`
**Also quoted (SV28, disk.s2.c 951-956).** `if (is_optical) { block->index = optical_indices++; block->is_optical = true; } else { block->index = hdd_indices++; }`

### SV9

**Statement.** [src] A `guid()`/`uuid()`/`fslabel()`/`hdd()`/`odd()` URI that resolves to no volume returns NULL **silently** — no `URI_ERROR`, no message — and on an `efi` entry that NULL is what turns into the `efi: Failed to open image` panic. A syntactically invalid GUID text is likewise a silent NULL (the parser rejects it before any lookup).

**Source, raw lines.** v12.9.4 common/lib/uri.c, raw 368-370
**Quote (8 words).** `if (raw == NULL) { return NULL; }`
**Host value.** host config has no such URI

**Also quoted (SV31, chainload.c 434-435).** `)) == NULL) panic(true, "efi: Failed to open image with path `%s`. Is the path correct?", image_path);`

### SV10

**Statement.** [inf] **Which URI would name this host's ESP.** Two do, and they are the same file: `boot():/…` (the empty root resolves to the boot volume — the ESP, since the ESP is where `/boot/limine.conf` and the UKIs live) and `guid(b80445be-18ee-45e6-9a30-14339ea785a7):/…` (the ESP's GPT unique partition GUID, in the text form `lsblk` prints, which SV1/SV4 show is exactly the parse Limine expects). `uuid(...)` with the same text is the same dispatcher. `fslabel(...)` cannot name it: the ESP's FAT label is empty. `hdd(d:p)`/`odd(d:p)` cannot name it either: their drive index is Limine's own enumeration counter, which the host does not expose.

**Source, raw lines.** v12.9.4 common/lib/uri.c, raw 355-358
**Quote (20 words).** `} else if (!strcmp(resource, "guid")) { raw = uri_guid_dispatch(root, path); } else if (!strcmp(resource, "uuid")) { raw = uri_guid_dispatch(root, path);`
**Host value.** ESP `nvme0n1p1`; `boot()` and `guid(<ESP PARTUUID>)` both name it; `fslabel()` cannot (no label); `hdd()`/`odd()` unmappable from the host
**Note.** The host's `LoaderDevicePartUUID` efivar carries the ESP's PARTUUID, which corroborates that Limine's own boot volume on this host was the ESP partition (it is written from `boot_volume->part_guid`, bli.c 109-111 — SV24) and that the ESP's partition GUID is the value a `guid()` URI needs.

### SV11

**Statement.** [src] The EFI `LoaderDevicePartUUID` variable Limine writes is the **boot volume's `part_guid`** rendered by `guid_to_string` — i.e. Limine's own rendering of a GPT unique partition GUID. On this host it reads `b80445be-18ee-45e6-9a30-14339ea785a7`, the ESP's PARTUUID, so the ESP is the volume Limine booted from.

**Source, raw lines.** v12.9.4 common/lib/bli.c, raw 109-111
**Quote (7 words).** `if (boot_volume->part_guid_valid) { char part_uuid_str[37]; guid_to_string(&boot_volume->part_guid, part_uuid_str);`
**Host value.** `b80445be-18ee-45e6-9a30-14339ea785a7` (read from the efivar this round)

**Also quoted (SV26, guid.c 78-81).** `void guid_to_string(const struct guid *guid, char *s) { uint_to_hex(guid->a, s, 8); s[8] = '-'; uint_to_hex(guid->b, s + 9, 4);`
**Also quoted (SV25, guid.c 62-64).** `guid_convert_le_cluster((uint8_t *)guid + 0, s + 0, 8); guid_convert_le_cluster((uint8_t *)guid + 4, s + 9, 4); guid_convert_le_cluster((uint8_t *)guid + 6, s + 14, 4);`

### SV12

**Statement.** [src] The boot volume on UEFI is the volume the firmware loaded Limine from (`disk_volume_from_efi_handle`), and the config-file search may then re-point `boot_volume` at the partition that actually holds `limine.conf`. Both paths end with the ESP on this host, which is why the empty-root `boot()` URI resolves inside the ESP.

**Source, raw lines.** v12.9.4 common/entry.s3.c, raw 156-156
**Quote (3 words).** `boot_volume = disk_volume_from_efi_handle(loaded_image->DeviceHandle);`
**Host value.** ESP (both paths)

**Also quoted (SV34, menu.c 1644-1647).** `volume_iterate_parts(boot_volume, if (!init_config_disk(_PART)) { boot_volume = _PART; break; }`
