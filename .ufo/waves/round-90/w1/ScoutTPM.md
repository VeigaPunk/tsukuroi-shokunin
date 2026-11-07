# ScoutTPM — C2 (TPM half) scouting report, round-90 w1

Seat: ScoutTPM (scout, TPM half of the C2 entry `corpus/knowledge/limine-tpm-volume-r90.md`).
Lane revision measured: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master` →
`b380483e2a1d8edc97556fdd021794f619b6e1a6` (the L1's C2 landing, "round-90: C2 entry
limine-tpm-volume-r90 TV1-TV8 (S365-S371, pinned src-c2, host receipt)"). The candidate commit named in the
wave brief, `ce89df93e5f576c5c236d4547299e9ea954e8853`, is its parent (`58723499` is between); the C1
measurement was not re-run by this seat (not my scope).

**No lane file was edited.** Deliverables, all inside my seat dir
`.ufo/waves/round-90/w1/ScoutTPM/`: `proposed-rows.md` (candidate rows A1–A14),
`proposed-sources.md` (12 SOURCES row drafts, ids TBD), `receipt-host.txt`, `receipt-quotes.txt`,
`receipt-sources.txt`. This report is the trailer file.

## Verdict per check

| # | Check | Verdict | Evidence |
|---|---|---|---|
| 1 | Limine v12.9.4 `tpm_present()` — what it asks the firmware | **pass (measured at source)** | `common/lib/tpm.c` 74-115: TCG2 leg = `LocateProtocol` + `GetCapability` + `TPMPresentFlag`; CC fallback = `EFI_CC_MEASUREMENT_PROTOCOL` + `GetCapability`; `return tcg2 != NULL \|\| cc != NULL;` |
| 2 | Where `tpm_init()` is called | **pass** | exactly one call site: `common/entry.s3.c:83` (`tpm_init();`), in `uefi_entry`, before the config is parsed |
| 3 | Who writes `LoaderTpm2ActivePcrBanks` | **pass** | systemd's `export_common_variables()` (`src/boot/export-vars.c` 57-63), format `"0x%08x"`; called by **both** sd-boot (`boot.c` 3454) and the UKI stub (`stub.c` 1256). On this host the writer is the **UKI's systemd-stub**: `LoaderInfo` = `Limine 12.9.4` (sd-boot would have written `systemd-boot …`), `StubInfo` = `systemd-stub 262.1-1-arch` |
| 4 | What `0x00000000` means | **pass** | systemd reaches `0` three ways: no TCG2 protocol / `GetCapability` failure / `TPMPresentFlag` clear; or `GetActivePcrBanks()` failure. `0xffffffff` is the *distinct* "protocol older than 1.1" value. Normatively (TCG EFI Protocol Spec rev13 p. 29 §6.4.4(5)), a platform with **no TPM** returns `TPMPresentFlag = FALSE` and `ActivePcrBanks = 0` — so `0x00000000` is the spec's own encoding of "no TPM present" |
| 5 | How the operator answers `--tpm-present` on this host | **pass — answer `0`**, two independent readings | (a) the efivar reads `0x00000000`; (b) **`systemd-analyze has-tpm2`** prints `partial`, `-firmware`, `-driver`, exit **3** — the OS's own firmware-TPM verdict, derived from that same variable, no sudo. Linux side agrees: `/sys/class/tpm/` and `/sys/class/tpmrm/` empty, no `/dev/tpm*`, no TPM2/TCPA ACPI table, no `tpm` line in the kernel log (despite `CONFIG_TCG_TPM/TIS/CRB=y`) |
| 6 | Is the efivar value stale? | **pass — no** | attributes `06 00 00 00` = `BOOTSERVICE_ACCESS\|RUNTIME_ACCESS`, `EFI_VARIABLE_NON_VOLATILE` (0x01) absent ⇒ volatile ⇒ the value belongs to the current boot |
| 7 | Same firmware, same boot? | **partial (narrowed, not closed)** | the UKI's stub runs inside Limine's own UEFI session (`LoadImage`/`StartImage` at `chainload.c` 507/541, before any `ExitBootServices`), and `LoaderImageIdentifier` = `EFI\Linux\omarchy_linux.efi` is exactly the *relative* path Limine builds ⇒ the stub's probe describes the same firmware state Limine queried. **Residual gap kept open**: a TPM with `TPMPresentFlag` set whose `GetActivePcrBanks()` fails also reads `0` |
| 8 | Which URIs name this host's ESP | **pass** | `guid(b80445be-18ee-45e6-9a30-14339ea785a7)` / `uuid(...)` (the ESP's GPT partition GUID = Linux `PARTUUID` = Limine's own `LoaderDevicePartUUID`) name it; `uuid(86D8-C3F6)` (the vfat serial) cannot — Limine never reads a filesystem GUID (`fs_get_guid` returns false); `fslabel()` cannot — the ESP's FAT label is empty; `hdd(d:p)` needs Limine's own firmware enumeration index, which Linux does not expose |
| 9 | Spec quote (primary doc) | **pass** | TCG EFI Protocol Specification rev13 (2016-03-30), PDF sha256 `40a2568e…`, fetched 2026-11-07; p. 28 Table 6, p. 29 §6.4.4(5), p. 37 §6.8.3, p. 24 Table 4 |
| 10 | Layout cross-check (Limine vs systemd) | **pass** | PicoEFI `efitcg2.h` (the headers Limine v12.9.4 compiles against, pinned by its own `bootstrap`) and systemd's `src/boot/proto/tcg.h` both give a 36-byte unpacked struct with `TPMPresentFlag`@16, `ActivePcrBanks`@32 (compiled with gcc 16.2.1) — the two programs read the same firmware bytes |

## Counts

- 14 candidate rows (A1–A14): 12 TPM-side extensions to the landed TV1–TV8, 2 supplementary volume rows
  (A13, A14). 41/41 quotes machine-verified as substrings of the quoted raw line ranges
  (`receipt-quotes.txt`, `MISSES: 0`).
- 12 SOURCES row drafts (ids TBD; the registry's next free ids are S372+), 6 of them brand-new source
  families (TCG spec, PicoEFI ×2, edk2 ×2, systemd `efi-api.c`/`tpm2-util`/`stub.c`/`boot.c`, Limine
  `chainload.c`/`entry.s3.c`/`disk.s2.c`). The four already-registered Limine/systemd files
  (S365, S366, S367, S368, S369, S370) and S371 were re-opened and confirmed byte-identical to the pins,
  not re-drafted.
- Host measurements: 21 read-only commands, no sudo, 0 writes outside my seat dir.

## The operator answer, in one paragraph

On this host `--tpm-present 0` is correct, and it can be established two ways without booting anything:
the systemd-stub in the chainloaded UKI wrote `LoaderTpm2ActivePcrBanks = 0x00000000` — the value the TCG EFI
Protocol Specification defines for a platform with no TPM (p. 29 §6.4.4(5)) — and `systemd-analyze
has-tpm2` prints `-firmware` and exits 3 for the same reason. Since the config has no `measured_boot` key
and Secure Boot is off, measured boot is off either way and every `panic` consequence returns to the menu;
adding `measured_boot: yes` turns a panic into a halt only once a firmware TPM is actually present
(`menu.c` 1725-1727 forces measured boot off when `!tpm_present()`).

## Things I refused / did not do

- No `sudo`, no write to `/boot`, `/efi`, `/etc`, `/usr`, `/var`, `/sys`, `/proc`, no efivar write, no
  firmware setting read beyond the efivars listed, nothing booted, no `objcopy`/`strip`/`sbsign`/`ukify`/
  `limine` invoked, no pacman transaction, no lane file edited, no subagent spawned.
- The UEFI 2.10 spec HTML/PDF on `uefi.org` returned **HTTP 403** on every attempt, so no UEFI-spec text is
  cited; the EFI variable attribute bits are cited from edk2's `UefiMultiPhase.h` instead.
- `TPMPERBIOSFLAGS` and `AMITCGPPIVAR` payloads were read but **not decoded**: their layout is
  vendor-private and I opened no primary source defining them, so no claim is made about their meaning.
- The `0x00000000` → "no TPM" conclusion is an **inference** from the spec plus the measured value; it was
  not confirmed against a TPM, and the residual gap (row A4's `GetActivePcrBanks()` failure branch) is left
  open for the L1.

## Residual work for the L1

1. The candidate rows A1–A14 and the 12 SOURCES drafts in my seat dir are proposals only; nothing is
   landed. The highest-value additions are **A1** (the primary spec, which the landed entry cites only
   through systemd's code), **A7** (a no-sudo operator command) and **A8** (narrowing TV4's stated gap).
2. A8 narrows TV4's gap but does not close it — keep the "TPM present but `GetActivePcrBanks` fails" branch
   open in the entry's Limits.
3. New registry sources need real snapshots under the wave's pinned-snapshot discipline if the L1 admits
   them (this seat wrote no snapshot: the pins are the lane's `after/src-c2/` plus the exact commit/tag and
   sha256 recorded in `receipt-sources.txt`).

Scratch (`/fast/scratch/hyaku/tsukuroi-r90/ScoutTPM`) removed after the receipts were copied into the wave dir.
