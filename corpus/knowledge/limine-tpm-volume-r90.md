# Limine TPM presence and volume lookup: how to answer `--tpm-present` and which URIs name this host's ESP (round 90)

source: S365 (Limine v12.9.4 `common/lib/tpm.c` 68-115), S351 (`common/lib/uri.c` 172-190, 192-199, 220-243), S366 (`common/lib/part.s2.c` 488-497, 575, 597-598, 1035-1061), S367 (`common/fs/file.s2.c` 27-31), S373 (`common/drivers/disk.s2.c` 986-988, 1004-1016), S368 (`common/lib/bli.c` 92, 110-124), S369 (systemd v262.1 `src/boot/export-vars.c` 57-63), S370 (systemd v262.1 `src/boot/measure.c` 153-216), S372 (TCG EFI Protocol Specification rev 00.13, p. 29 §6.4.4(5)), S371 (own-work: read-only host receipts); S361 (`common/protos/chainload.c` 505-541), S353 (`common/menu.c` 1719-1728), S352 (`common/lib/config.c` 642-650) and S362 (`panic.s2.c`) for what the answer changes; S365-S370, S372, S373 `mined`, S371 own-work; Gate in `corpus/lessons/round-90.md`
recheck: re-open the pinned files on any `limine` or `systemd` package update (cadence on-release); re-run the host receipt commands after every boot that follows a firmware TPM setting change or a disk/ESP change (event trigger), else 30d
verified-at: 2026-11-07
host capture: `.ufo/waves/round-90/before/host/receipt.txt` (2026-11-06T23:39:27-03:00) and `.ufo/waves/round-90/after/host-c2-receipt.txt` (2026-11-07T00:02:54-03:00), both read-only (efivar `od`/`iconv`, `ls`, `lsblk`, `pacman -Q`, `zgrep /proc/config.gz`; one `sudo -n grep` of `/boot/limine.conf` with a `/boot` digest list before and after, `cmp`-identical)
machine-readable rows: `corpus/knowledge/limine-tpm-volume-r90.json`
snapshots: `.ufo/waves/round-90/after/src-c2/` (Limine v12.9.4 `tpm.c`, `part.s2.c`, `file.s2.c`, `bli.c`, `entry.s3.c`, `guid.c` from the tag clone `8ad14430`; systemd v262.1 `export-vars.c`, `measure.c` from the tag clone `73612ea5`; `URLS.txt`, `SHA256SUMS`, `PROVENANCE.txt`); `uri.c` is the round-87 pin (byte-identical, `.ufo/waves/round-90/before/src/cmp-pins.txt`)
companions: `corpus/knowledge/limine-uri-failure-r89.md` (UF3/UF4 resource dispatch, UF7 menu return vs halt), `corpus/knowledge/limine-pin-plane-r87.md` (pin grammar); gate `tools/check-limine-pins.py` (round-90 rules R9/R10, flag `--tpm-present`)

## What this plane answers

Round 90 gave the `limine-pins` gate a `--tpm-present 0|1` flag: Limine forces measured boot off when its
`tpm_present()` is false, and measured boot decides whether a panic returns to the menu or halts (rule R10,
`menu.c` 1719-1728). The flag is the one input the gate cannot read for itself, and `--live` never guesses it
(absent flag -> `halt-if-tpm` when measured boot is requested). This entry says what `tpm_present()` asks the
firmware, which signal on this host carries the same answer from the last boot, and — for the gate's other
`not-modelled` word, LP-UNRESOLVED — how `guid()`, `uuid()`, `fslabel()` and `boot(N)` find a volume and which
of them would name this host's ESP. The round-89 entry left `tpm_present()` and the volume lookups unopened (its
Limits); this one opens them.

## Rows

Quotes are verbatim from the pinned snapshots; raw line numbers refer to those files (upstream tags; the host
runs the Arch builds `limine 12.9.4-1` and `systemd 262.1-1`, whose line numbers were not checked: QUALITY 103).
`[src]` = stated by the pinned source; `[obs]` = read on this host this round; `[inf]` = inference, not executed.

| Row | Statement | Source, raw lines | Quote (≤25 words) | Host value (2026-11-07) |
|---|---|---|---|---|
| TV1 | [src] Limine's `tpm_present()` is true when `tpm_init` found either an EFI TCG2 protocol whose `GetCapability` succeeds with `TPMPresentFlag` set, or (only if that failed) an EFI CC measurement protocol (TDX/SEV-SNP confidential computing). Nothing else counts: not a Linux driver, not a firmware setup variable. | S365 tpm.c 68-115 | "return tcg2 != NULL \|\| cc != NULL;" (line 114) | — |
| TV2 | [src] Limine v12.9.4 itself writes `LoaderInfo` and `LoaderDevicePartUUID` (the GPT unique partition GUID of the volume it booted from) but no TPM variable. [src] systemd's UKI stub (v262.1) writes `LoaderTpm2ActivePcrBanks` once per boot when no earlier stage set it, as `0x%08x` of `tpm_get_active_pcr_banks()`, which returns 0 when the TCG2 protocol is missing, `GetCapability` fails, `TPMPresentFlag` is clear, or `GetActivePcrBanks` fails; `0xffffffff` for a TCG2 protocol older than 1.1. [src] The TCG EFI Protocol Specification makes a zero mask the defined reply of a platform without a TPM: `TPMPresentFlag = FALSE`, `ActivePcrBanks = 0`. | S368 bli.c 92, 110-124; S369 export-vars.c 57-63; S370 measure.c 153-183, 194-216; S372 p. 29 §6.4.4(5) | "If the platform does not have a TPM then the following values SHALL be returned:" (S372 p. 29) | — |
| TV3 | [obs] This boot: `LoaderTpm2ActivePcrBanks` = `0x00000000`, attributes `06` (boot-service + runtime access, not non-volatile, so it does not survive a reboot and is written again each boot); `LoaderInfo` = `Limine 12.9.4`; `LoaderImageIdentifier` = `EFI\Linux\omarchy_linux.efi`; `systemd 262.1-1` ships `/usr/lib/systemd/boot/efi/linuxx64.efi.stub`, whose bytes contain the variable name. [inf] The UKI Limine chainloaded was built on that stub (mkinitcpio's UKI build); its bytes were not read. [obs] Linux side agrees: `/sys/class/tpm/` is empty although `CONFIG_TCG_TIS=y` and `CONFIG_TCG_CRB=y` are built in, no `TPM2`/`TCPA` ACPI table is exposed, and the kernel log has no `tpm` line. [obs] The AMI firmware keeps TCG setup variables (`AMITCGPPIVAR`, `TPMPERBIOSFLAGS`); what they encode was not read. | S371 (after/host-c2-receipt.txt lines 2-21; before/host/receipt.txt lines 4-25, 73-77, 91-94) | — | `0x00000000`; 0 TPM devices; 0 TPM ACPI tables |
| TV4 | [inf] So on this host `--tpm-present 0` is the answer for the current boot: the stub's `tcg2_interface_check` is the same LocateProtocol + `GetCapability` + `TPMPresentFlag` test Limine's TCG2 leg makes (TV1, TV2), and it found no present TPM; Limine's CC leg does not apply to a bare-metal AMI board. The stub runs as an image Limine itself started (`LoadImage`/`StartImage`, chainload.c 505-541) while boot services are still up, so it asked the same firmware session. One gap keeps this an inference: a TPM with the flag set whose `GetActivePcrBanks` fails would also read 0. With 0 (or with no `measured_boot` key and Secure Boot off, as here) measured boot is off and every `panic` consequence returns to the menu: the live gate reads `on_panic: menu` without the flag. | TV1-TV3, TV9; S361 chainload.c 505-541; S353 menu.c 1719-1728; S362 | — | live gate at `ce89df93`: `on_panic menu`, `measured_boot None` (`.ufo/waves/round-90/after/live-receipt.txt`) |
| TV5 | [src] `guid(X)` and `uuid(X)` are the same dispatcher: X is parsed as a mixed-endian GUID, looked up, then retried big-endian; a text that is not a GUID returns NULL with no message. The lookup compares a volume's `guid` and its GPT unique partition GUID. A partition's `guid` comes from `fs_get_guid`, which returns false for every filesystem in v12.9.4; only a whole-medium volume carries one, the GPT header's disk GUID. So no filesystem UUID ever matches: a `guid()` URI names a partition by its GPT unique partition GUID, or a whole disk by its GPT disk GUID (corrected at landing on wave seat ScoutVolume's finding 1). | S351 uri.c 172-190; S366 part.s2.c 488-497, 597-598, 1035-1047; S367 file.s2.c 27-31; S373 disk.s2.c 986-988 | "bool fs_get_guid(struct guid *guid, struct volume *part) { (void)guid; (void)part; return false;" (lines 27-30, abridged across lines) | ESP `nvme0n1p1` PARTUUID `b80445be-18ee-45e6-9a30-14339ea785a7`, vfat serial `86D8-C3F6` |
| TV6 | [inf] On this host `guid(b80445be-18ee-45e6-9a30-14339ea785a7)` and `uuid(b80445be-18ee-45e6-9a30-14339ea785a7)` name the ESP (Linux prints PARTUUID in the canonical mixed-endian text the parser expects); `uuid(86D8-C3F6)` — the "UUID" `lsblk` shows for the vfat ESP — names nothing, so on an `efi` entry's `path:` it is a "Failed to open image" panic (UF5). | TV5; S371 | — | ESP has no partition GUID duplicate on the other disks (`lsblk`, before/host/receipt.txt lines 26-41) |
| TV7 | [src] `fslabel(L)` compares filesystem labels case-insensitively (`strcasecmp`). [obs] The ESP's vfat label is empty, so no `fslabel()` URI names it on this host. | S366 part.s2.c 1050-1061; S371 | "&& strcasecmp(volume_index[i]->fslabel, fslabel) == 0) {" (line 1056) | ESP label empty |
| TV8 | [src] `boot()` opens the partition Limine booted from; `boot(N)` opens partition N on the same drive. A GPT partition's number is its entry slot plus 1 (`partition + 1`), and empty slots are skipped without renumbering, so N is a slot number with gaps, not a count of partitions (wave seat ScoutVolume's finding 2). [obs] Limine's own `LoaderDevicePartUUID` names `b80445be-…`, the ESP, which Linux numbers partition 1 of `nvme0n1` (Linux numbers GPT slots the same way). [inf] So `boot()` and `boot(1)` name the same volume here. `hdd(d:p)` needs Limine's firmware drive index, which Linux does not show; no `hdd()` URI is mapped. | S351 uri.c 220-243; S366 part.s2.c 575; S373 disk.s2.c 1004-1016; S368 bli.c 110-124; S371 | "ret->partition   = partition + 1;" (part.s2.c line 575) | `LoaderDevicePartUUID` = `b80445be-18ee-45e6-9a30-14339ea785a7`; ESP PARTN 1 |
| TV9 | [obs] An operator check that needs no root: `systemd-analyze has-tpm2` prints `partial` with `-firmware` and `-driver` and exits 3 on this host (its `+system`, `+subsystem`, `+libraries` lines only say the OS could use a TPM). The tool's meaning of `-firmware` was not opened here (wave seat ScoutTPM traced it to the same `LoaderTpm2ActivePcrBanks` variable, `.ufo/waves/round-90/w1/ScoutTPM.md` check 5); read it as a second view of TV3, not an independent probe. | S371 (after/host-c2-receipt.txt lines 28-38) | — | `partial`, `-firmware`, `-driver`, rc 3 |

## Operator actions

1. Run the gate with `--tpm-present 0` on this host until `LoaderTpm2ActivePcrBanks` reads anything other than
   `0x00000000` after a boot (read it with `tail -c +5 /sys/firmware/efi/efivars/LoaderTpm2ActivePcrBanks-4a67b082-0a4c-41cf-b6c7-440b29bb8c4f | iconv -f UTF-16LE`);
   enabling the firmware TPM, then adding `measured_boot: yes` to the global section (before the first `/` entry
   line; Limine does not see the key inside an entry body, config.c 642-650, erratum in `limine-pin-plane-r87.md`),
   turns every `panic` row into a halt (R10, UF7). The gate at `ce89df93` still reads the key anywhere in the file
   (round-90 lesson R90-R1).
2. Keep the pins on `boot()`: a pin written as `guid(b80445be-…)` or `boot(1)` names the same file but the gate
   reports it `LP-UNRESOLVED` (rc 2), because it resolves only an empty-root `boot()` against `--esp`.
3. Never write `uuid(86D8-C3F6)` (the vfat serial): Limine cannot match it (TV5, TV6).

## Limits

- Nothing was booted and no firmware setting was read beyond the efivars named; what `AMITCGPPIVAR` and
  `TPMPERBIOSFLAGS` encode (for example a disabled firmware TPM) was not decoded.
- TV4 is an inference from a systemd-stub variable to Limine's own check; Limine prints its own result only in
  verbose mode (`printv`, tpm.c 85-86, 107), which this host does not log.
- `volume_get_by_coord`'s drive index for `hdd()` and the `odd()` optical index were not mapped to Linux names.
- Upstream drift was not re-read by the L1. Wave seat ScoutDrift (`.ufo/waves/round-90/w1/ScoutDrift.md` §1-§3, E):
  v12.9.5 and v12.9.6 exist and Arch's repository carries limine 12.9.6-1 (the local sync DB is older); `tpm_present()`
  is byte-identical there, `guid()`/`uuid()`/`fslabel()` retry after connecting all disks (a volume may resolve where
  v12.9.4 gives NULL), and since 12.9.5 a conf whose first line is an entry has no global options at all. Re-pin the
  rows on the host upgrade before relying on TV5-TV8 or on R10's visibility.
