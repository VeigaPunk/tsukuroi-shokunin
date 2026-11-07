# SOURCES registry drafts — seat ScoutVolume, round-90 w1

Candidate rows for `corpus/SOURCES.md`. The lane file was NOT edited. IDs **S373-S376** are **proposed**:
S365-S372 are already taken at the round-90 tip (S372 is the L1's TCG-spec row), so the numbering continues from
there and must be renumbered again if the L1 lands further rows first.

Three of these four files (`fat32.s2.c`, `iso9660.s2.c`, `disk.s2.c`) are **new opens** for the lane: no
`.ufo/waves/round-90/{before,after}/src*/` pin covers them yet. `guid.c` is already pinned by the L1 in
`.ufo/waves/round-90/after/src-c2/` (sha256 `ae18e678…`, byte-identical to the upstream raw file) but has no
registry row of its own — S375 is that row.

The files `common/lib/part.s2.c`, `common/fs/file.s2.c`, `common/lib/bli.c`, `common/entry.s3.c` are already
registered (S366, S367, S368) or pinned-but-unregistered; the rows below add only what those rows do not say.

## Proposed rows

| S373 | Limine v12.9.4 common/fs/fat32.s2.c — https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/fs/fat32.s2.c | code | A | How a FAT volume's label and serial are read, and where the label comes from | tag v12.9.4 (clone HEAD 8ad14430bc9f2c24679cda558981ef53e6e3b18c), raw lines 71-72 (BPB volume_serial_number and label fields), 513-527 (root-directory volume-label entry, attribute 0x08, trailing spaces trimmed), 620-649 (fat32_get_label); byte-identical to the upstream raw file (verified 2026-11-07) sha256 2a488078589d7b574f6aa4833b48390778ffec02b78e576c2326222e3c0f7f61 | a FAT label is the root directory's volume-label entry, not the BPB label field, and the BPB volume serial is never used for identity, so a vfat serial can never satisfy a guid() URI | mined | 2026-11-07 | on-release | corpus/knowledge/limine-tpm-volume-r90.md |
| S374 | Limine v12.9.4 common/fs/iso9660.s2.c — https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/fs/iso9660.s2.c | code | A | How an ISO 9660 volume identifier becomes a comparable label | tag v12.9.4 (clone HEAD 8ad14430bc9f2c24679cda558981ef53e6e3b18c), raw lines 146-164 (iso9660_get_label: PVD volume_identifier, trailing spaces trimmed); byte-identical to the upstream raw file (verified 2026-11-07) sha256 56c3350cc6352be22021600aa11e6e15eca3bc5bff9621fb3a59dec0948f25d3 | an ISO 9660 label is its PVD volume identifier with trailing spaces trimmed | mined | 2026-11-07 | on-release | corpus/knowledge/limine-tpm-volume-r90.md |
| S375 | Limine v12.9.4 common/drivers/disk.s2.c — https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/drivers/disk.s2.c | code | A | How Limine numbers drives and partitions, and where each volume's GUID comes from | tag v12.9.4 (clone HEAD 8ad14430bc9f2c24679cda558981ef53e6e3b18c), raw lines 229, 306-317 (BIOS: drive indices, GPT disk GUID on the whole medium), 909, 946-1026 (UEFI: drive indices, GPT disk GUID, partition enumeration); byte-identical to the upstream raw file (verified 2026-11-07) sha256 34e3a81fee89f045f76b01029440ed92fc03836179e8b9f3e6f721c7f5b799d2 | drive indices are Limine's own 1-based enumeration counters, disjoint for optical and non-optical, and a whole GPT medium carries the header disk GUID | mined | 2026-11-07 | on-release | corpus/knowledge/limine-tpm-volume-r90.md |
| S376 | Limine v12.9.4 common/lib/guid.c — https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/lib/guid.c | code | A | The GUID text format Limine accepts and the byte order it parses it in | tag v12.9.4 (clone HEAD 8ad14430bc9f2c24679cda558981ef53e6e3b18c), raw lines 7-25 (is_valid_guid: 8-4-4-4-12 hex with dashes at 8/13/18/23, NUL at 36), 27-43 (le/be cluster conversion), 45-69 (string_to_guid_be, string_to_guid_mixed), 71-93 (guid_to_string); byte-identical to the upstream raw file (verified 2026-11-07) sha256 ae18e6789d2eeec2d573417ca613c33f3c7164ecdfd7454a9b76f047dee0ea6c | a GUID text is 36 hex chars in 8-4-4-4-12 groups; string_to_guid_mixed and guid_to_string are exact inverses, so the text lsblk prints for PARTUUID is the text a guid() URI must carry | mined | 2026-11-07 | on-release | corpus/knowledge/limine-tpm-volume-r90.md |

## Files cited by these rows but not yet pinned by the lane (for the L1 to pin under
`.ufo/waves/round-90/after/src-c2/` if it wants the snapshot to cover them)

| file | upstream URL (tag v12.9.4) | sha256 |
|---|---|---|
| `common/fs/fat32.s2.c` | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/fs/fat32.s2.c | `2a488078589d7b574f6aa4833b48390778ffec02b78e576c2326222e3c0f7f61` |
| `common/fs/iso9660.s2.c` | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/fs/iso9660.s2.c | `56c3350cc6352be22021600aa11e6e15eca3bc5bff9621fb3a59dec0948f25d3` |
| `common/drivers/disk.s2.c` | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/drivers/disk.s2.c | `34e3a81fee89f045f76b01029440ed92fc03836179e8b9f3e6f721c7f5b799d2` |
| `common/lib/guid.c` (already pinned) | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/lib/guid.c | `ae18e6789d2eeec2d573417ca613c33f3c7164ecdfd7454a9b76f047dee0ea6c` |

All four sha256 values are of the upstream raw file at tag v12.9.4 and are byte-identical to the clone this seat
read (`receipt-upstream-vs-clone.txt`).
