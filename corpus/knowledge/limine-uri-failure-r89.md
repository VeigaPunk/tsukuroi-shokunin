# Limine URI failures: what each resource resolves to and what a failed `path:` does to an `efi` entry (round 89)

source: S351 (Limine v12.9.4 `common/lib/uri.c`, new anchors 18-26, 46-63, 109-271, 344-376, 696-708), S361 (`common/protos/chainload.c`), S362 (`common/lib/panic.s2.c`), S353 (`common/menu.c` 1719-1730), S350 (`CONFIG.md` 157-160), S363 (own-work: read-only host receipt); S361-S362 `mined`, S363 own-work; Gate in `corpus/lessons/round-89.md`
recheck: re-open the pinned files on any `limine` package update (cadence on-release); re-run the host receipt command on any `/boot/limine.conf` rewrite
verified-at: 2026-11-06
host capture: `.ufo/waves/round-89/before/host/receipt.txt` (2026-11-06T21:52:29-03:00, read-only: `sudo -n grep` of `/boot/limine.conf`, `/sys/class/tpm/`, SecureBoot efivar, `pacman -Q limine`)
machine-readable rows: `corpus/knowledge/limine-uri-failure-r89.json`
snapshots: `.ufo/waves/round-89/before/src/` (`chainload.c`, `panic.s2.c`, `URLS.txt`, `SHA256SUMS`, `fetch.txt`, `cmp-r87-pins.txt`); tag clone v12.9.4 at `8ad14430bc9f2c24679cda558981ef53e6e3b18c`; `uri.c`, `config.c`, `menu.c`, `CONFIG.md` in that clone are byte-identical to the round-87 pins in `.ufo/waves/round-87/before/src/`; the host runs limine 12.9.4-1
companions: `corpus/knowledge/limine-pin-plane-r87.md` (pin grammar and mismatch consequence), `corpus/knowledge/limine-pin-writers-r88.md` (who writes the pins)

## What this plane answers

The lane's `limine-pins` gate reports a pin it cannot hash as `LP-UNRESOLVED` or `LP-MISSING` with consequence
`not-modelled`, and its rule set calls every resource other than an empty-root `boot()` unresolvable. The round-88
wave (ReviewBattery F1, F3; lesson R88-R5) said two of those words hide Limine behaviour: `boot(N)` does resolve,
and a `path:` Limine cannot open is not "ignored". This entry reads the resolver and the `efi` loader at the
installed tag and answers three operator questions: what each URI resource resolves to; what a URI failure does to
an `efi` entry (the only protocol on this host); and what the word `panic` means on screen. It does not change the
gate or the battery rule set (round-89 C1 freezes R1-R8 as they are); it says where `not-modelled` is a modelling
limit and what Limine does there.

## Rows

Quotes are verbatim from the pinned snapshot; raw line numbers refer to the pinned files. `[obs]` = read on this
host this round; `[src]` = stated by the pinned source; `[inf]` = inference from the source, not executed here.

| Row | Statement | Source, raw lines | Quote (≤25 words) | Host value (2026-11-06) |
|---|---|---|---|---|
| UF1 | [src] Every URI error goes through `URI_ERROR`, which panics unless the URI was opened through `uri_open_optional` (the optional-resource path); only then does it print and return. So any URI failure on a required key (`path:`, `kernel_path:`, `module_path:`) is a panic, and the same panic carries a hash mismatch under `hash_mismatch_panic: yes`. | S351 uri.c 18-26, 301-305, 696-708 | "// Only returns for an optional resource, which the caller then backs out of." (line 20) | — |
| UF2 | [src] After one leading `$` is dropped, the resource is compared with `strcmp` (case-sensitive) against `hdd`, `odd`, `boot`, `guid`, `uuid` (same dispatcher as `guid`), `fslabel`, `tftp`; any other name is "not valid" and goes to `URI_ERROR`, i.e. a panic for a required key. | S351 uri.c 344-366 | "URI_ERROR(\"Resource `%s` not valid.\", resource);" (line 364) | [obs] all six URIs in `/boot/limine.conf` are `boot():/…` (r88 host receipt pin lines 30, 38, 50, 56, 64, 72) |
| UF3 | [src] `boot()` with an empty root opens the partition Limine booted from; `boot(N)` opens partition N (0-256, parsed with `strtoui`) on the SAME drive as the boot volume; N > 256 is a `URI_ERROR`; on a PXE boot `boot()` is redirected to `tftp`. So `boot(N)` is resolvable by Limine — the gate's `LP-UNRESOLVED` for it is a gate limit (it hashes only `--esp`), not a Limine verdict. | S351 uri.c 220-243 | "struct volume *volume = volume_get_by_coord(boot_volume->is_optical, boot_volume->index, partition);" (lines 237-238) | [obs] no `boot(N)` on this host (UF2), so the limit does not fire here |
| UF4 | [src] `guid()`/`uuid()` parse the text mixed-endian first and retry big-endian; `fslabel()` looks a volume up by label; `hdd(d:p)`/`odd(d:p)` need a drive 1-256 (an omitted drive is a `URI_ERROR`) and a partition 0-256. A volume that is simply not found returns NULL with no message of its own; the caller decides what that means (UF5). | S351 uri.c 109-199 | "URI_ERROR(\"Drive number cannot be omitted for hdd():/ and odd():/\");" (line 119) | — |
| UF5 | [src] An `efi` entry (`protocol: efi`, `chainload()`) reads `PATH`, then `IMAGE_PATH`; if `uri_open` returns NULL — file absent, volume not found, or a value `uri_resolve` cannot split (no `(` or no `):/`, which returns false without a message, lines 46-63) — Limine panics with "Failed to open image". So `LP-MISSING`, an unresolvable volume, and a URI-less `path:` value are all a panic of that entry at boot, not an ignored line. | S361 chainload.c 414-435; S351 uri.c 46-63 | "panic(true, \"efi: Failed to open image with path `%s`. Is the path correct?\", image_path);" (line 435) | [obs] all six entries are `protocol: efi` (host receipt lines 29, 37, 49, 55, 63, 71) |
| UF6 | [src] Around that `uri_open`, `chainload()` sets `secure_boot_active = false` and restores it after; inside `uri_open` that flag gates only the "Secure Boot is active and URI has no associated hash" error. So an `efi` entry's `path:` may be unhashed under Secure Boot (the firmware's LoadImage verifies the image instead), while a pin that IS present is still compared (the mismatch path does not read the flag). The code comment says Limine "does not need to enforce its own hash check here"; the code only waives the missing-hash rule. | S361 chainload.c 423-437; S351 uri.c 372-376, 442, 470, 664 | "// The firmware's LoadImage will verify the Secure Boot signature of the chainloaded EFI application, so Limine does not need" (lines 423-424) | [obs] SecureBoot efivar data byte `00` (off) |
| UF7 | [src] Every panic above is `panic(true, …)`: it prints `PANIC`, then "Press a key to return to menu", and the menu comes back, so another entry (a snapshot entry, the fallback) can be chosen. Under measured boot the menu return is refused and the machine prints "System halted." Measured boot is on only when the config says `measured_boot: yes` or Secure Boot is active, and is forced off without a TPM/CC measurement interface. | S362 panic.s2.c 18-29, 70-100; S353 menu.c 1719-1730; S350 CONFIG.md 157-160 | "print(\"Press a key to return to %s.\", booting_from_editor ? \"editor\" : \"menu\");" (panic.s2.c line 78) | [obs] no `measured_boot` key in `/boot/limine.conf`; Secure Boot off; `/sys/class/tpm/` empty |
| UF8 | [inf] On this host, therefore: the gate's `not-modelled` rows cannot come from a resource (every URI is `boot():/`), and an `LP-MISSING` main `path:` would be a panic that returns to the menu after a key press — the snapshot entries and `EFI fallback` stay selectable. The round-86 incident's mismatches stay `prompt` (`hash_mismatch_panic: no`, r87 LP5). The firmware's own TPM state was not read: an empty `/sys/class/tpm/` shows Linux has no TPM device, which is what Limine's `tpm_present()` would also need; not executed at boot. | UF2, UF5, UF7; S363 | — | [obs] host receipt above |

## Operator actions

1. Nothing to repair from this entry: it adds no fault. The open host incident (pins on lines 30 and 38) is still
   the operator's; its consequence is `prompt` (r87 LP5), and after a repair (r88 PW5) the next failure mode to
   watch is a missing UKI, which UF5/UF7 say is a recoverable panic (key → menu → fallback or snapshot entry).
2. If `measured_boot: yes` is ever added, or Secure Boot with an enrolled config is enabled, the same failures halt
   the machine instead (UF7): keep the `EFI fallback` entry's path pin valid before turning either on.

## Limits

- Read from source at the installed tag; nothing was booted. The `limine`, `linux` and `multiboot` protocols' own
  failure messages were not read (their `uri_open` call sites are listed by `grep -n uri_open common/protos/*.c` in
  the tag clone: `limine.c` 627, `linux_x86.c` 270, `multiboot1.c` 78, `multiboot2.c` 118); this host uses only `efi`.
- `volume_get_by_coord`, `volume_get_by_guid`, `volume_get_by_fslabel` and `tpm_present()` were not opened; UF4's
  "not found returns NULL" is the dispatcher's visible behaviour, not the volume layer's.
- The gate and the battery rule set are unchanged; whether the gate should report `boot(N)` or an `efi` `LP-MISSING`
  with consequence `panic` instead of `not-modelled` is routed (round-89 lesson), not decided here.
