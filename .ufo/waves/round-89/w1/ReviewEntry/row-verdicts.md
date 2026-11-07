# ReviewEntry — row-by-row verification of corpus/knowledge/limine-uri-failure-r89.md (+ .json)

Lane master reviewed: `665408cc45a88ed49717e22f4593e8e6152ac665`. Pinned bytes verified first:
`sha256sum -c SHA256SUMS` in `.ufo/waves/round-87/before/src/` (5/5 OK, rc=0) and
`.ufo/waves/round-89/before/src/` (2/2 OK, rc=0). `cmp-r87-pins.txt`: uri.c, config.c, menu.c, CONFIG.md
byte-identical to the r87 pins; `fetch.txt`: both r89 raw URLs http=200.

Line numbers below are raw pinned-file lines, located with line-numbered grep on the pinned files (not from the
entry's table).

## UF1 — partial (label/wording)

- Quote ✓ verbatim: uri.c:20 `// Only returns for an optional resource, which the caller then backs out of.`
  (14 words). Anchors ✓: 18-26 is exactly `static bool optional_resource` (18) + the whole `URI_ERROR` macro
  (21-26); 301-305 is exactly `uri_hash_mismatch`'s `hash_mismatch_panic || optional_resource → URI_ERROR →
  return false` block (so "the same panic carries a hash mismatch under `hash_mismatch_panic: yes`" ✓);
  696-708 is `uri_open_optional` setting/clearing `optional_resource` ✓.
- Defect a: "Every URI error goes through `URI_ERROR`" overstates — silent NULL returns exist and do NOT go
  through `URI_ERROR` (volume not found: uri.c 239-240, 194-196, 185-186; file absent: fopen NULL → 368-370
  `if (raw == NULL) return NULL;`). UF4/UF5 document exactly that, so the entry contradicts itself at the margin.
  Fix: "every raised URI error message".
- Defect b: "`kernel_path:`, `module_path:`" callers (limine.c 627, linux_x86.c 270, multiboot1.c 78,
  multiboot2.c 118) are listed in the entry's Limits but not pinned/opened; for those two keys the panic is an
  inference, so the clause is [inf], not [src]. `path:` (efi) is [src] via S361 chainload.c 434-435 ✓.
- Verdict: partial. Proposed wording under proposed-wording.md.

## UF2 — support

- Quote ✓ verbatim: uri.c:364 `URI_ERROR("Resource `%s` not valid.", resource);` (5 words). Anchor 344-366 ✓
  covers `$` drop (344-347: `gz_compressed = *resource == '$'` → `resource++`, one leading `$`), the full
  case-sensitive `strcmp` chain hdd/odd/boot/guid/uuid/fslabel/tftp (349-363, uuid → same `uri_guid_dispatch`
  as guid at 357-358), and the unknown-resource `URI_ERROR` (364).
- Host value ✓: r88 receipt "limine.conf pin lines" shows all six `path:` lines boot():/ — conf lines
  30, 38, 50, 56, 64, 72 as cited.

## UF3 — support (one nit)

- Quote ✓ verbatim: uri.c:237-238 `struct volume *volume = volume_get_by_coord(boot_volume->is_optical,` /
  `boot_volume->index, partition);` (7 words on line 237; the quote cites both lines). Anchor 220-243 ✓ covers
  the whole `uri_boot_dispatch`: PXE redirect 221-222, empty root → `boot_volume->partition` 233-235,
  `strtoui` + `val > 256` → URI_ERROR 226-231, same-drive lookup 237-238.
- Gate-side claim ✓: tools/check-limine-pins.py:11 "only `boot()` (empty root) resolves, to --esp; anything
  else is LP-UNRESOLVED" and 133-136 (resource != "boot" or root != "" → LP-UNRESOLVED, consequence
  not-modelled). So `boot(N)` LP-UNRESOLVED is a gate limit, and Limine resolves it — the row's point stands.
- Nit: the PXE redirect at 221-222 fires before the `s_part` check, so `boot(N)` on a PXE boot is redirected to
  tftp too, not only `boot()`.

## UF4 — support

- Quote ✓ verbatim: uri.c:119 `URI_ERROR("Drive number cannot be omitted for hdd():/ and odd():/");` (9 words).
- Anchors ✓: 109-199 covers `parse_bios_partition` (drive 1-256 at 123-126, omitted drive URI_ERROR at 119,
  partition 0-256 at 134-138), `uri_hdd_dispatch`/`uri_odd_dispatch` (volume NULL → silent NULL),
  `uri_guid_dispatch` (mixed-endian 174 then big-endian retry 180, both silent NULL), `uri_fslabel_dispatch`
  (192-193, silent NULL). Registry S351 says 109-243; the row's 109-199 covers everything the statement claims.
- "not found returns NULL with no message of its own" ✓ (each dispatcher returns NULL without URI_ERROR).

## UF5 — support

- Quote ✓ verbatim: chainload.c:435 `panic(true, "efi: Failed to open image with path `%s`. Is the path
  correct?", image_path);` (14 words). Anchor 414-435 ✓: PATH→IMAGE_PATH 415-418, "Image path not specified"
  panic(true) 420, uri_open NULL → panic 434-435.
- uri.c 46-63 ✓: missing `(` → `return false` at 48-49, missing `):/` → `return false` at 61-62, both without
  URI_ERROR (the URI-too-long case at 38 does raise URI_ERROR — the row scopes the silent-false correctly).
- "LP-MISSING … a panic" ✓: gate LP-MISSING = pinned file absent (check-limine-pins.py 145-146
  `if not os.path.isfile(target)` → LP-MISSING; selftest line 219-220), and an absent file at boot is
  fopen NULL → panic 435. Host value ✓: r89 receipt conf lines 29, 37, 49, 55, 63, 71 all `protocol: efi`
  (six entries: 2 main, 3 snapshot, EFI fallback).

## UF6 — support (recommended addition)

- Quote ✓ verbatim across chainload.c:423-424, 20 words. Anchors ✓: 423-427 comment + save + clear,
  437 restore; uri.c 372-376 is the only `secure_boot_active` site in uri.c (line-numbered grep over the whole
  file: exactly one hit), so "gates only the no-hash error" ✓; 442, 470, 664 are the three mismatch paths and
  none reads the flag — `uri_hash_mismatch` (301-319) reads only `hash_mismatch_panic || optional_resource` ✓.
- Host value ✓: receipt line 16 `06 00 00 00 00` → data byte 00 (off).
- Recommended addition (not a defect): under Secure Boot, menu.c:1714-1717 forces `hash_mismatch_panic = true`,
  so a present-pin mismatch under SB is a URI_ERROR panic, not the Y-prompt. The parenthetical "the mismatch
  path does not read the flag" is literally true; adding the menu.c coupling closes the misreading that
  mismatches would still prompt under SB. S353 (menu.c 1711-1717) is already pinned, so the addition costs
  nothing.

## UF7 — support

- Quote ✓ verbatim: panic.s2.c:78 `print("Press a key to return to %s.", booting_from_editor ? "editor" :
  "menu");` (12 words). Anchors ✓: 18-29 (measured boot clears allow_menu at 26-28), 70-100 (press-key at
  78, `menu(false)` at 85, "System halted." at 98 under UEFI). menu.c 1719-1730 ✓: MEASURED_BOOT read 1720-1721,
  SB forces on 1722-1724, `!tpm_present()` forces off 1725-1728. CONFIG.md 157-160 ✓: the measured_boot bullet.
- "Every panic above is `panic(true, …)`" ✓: URI_ERROR macro (uri.c:23), chainload.c 420 and 435.
- Host value ✓: r89 receipt — no `measured_boot` key (grep lines 3-10), SecureBoot 00, /sys/class/tpm empty.

## UF8 — support (one wording nit)

- Sound [inf]: resource-based not-modelled impossible on this host (UF2 obs: all six URIs boot():/; gate
  133-136); an LP-MISSING main `path:` → panic → menu return (UF5+UF7; no measured boot, no TPM, SB off);
  snapshots and `/EFI fallback` exist and stay selectable (r88 receipt lines 41-72); r86-incident mismatches
  stay prompt (receipt line 8 `hash_mismatch_panic: no` — the FIRST value — gate rule 14-16; r87 lesson LP5
  exists, "Default panic; only `no` prompts").
- TPM honesty ✓ as written: firmware TPM state explicitly not read; `/sys/class/tpm/` claim scoped to Linux;
  row labelled [inf]; "not executed at boot".
- Nit: "an empty `/sys/class/tpm/` … is what Limine's `tpm_present()` would also need" invites equating a
  Linux device observation with Limine's firmware-interface probe. Suggest "evidence (not a firmware probe)
  that `tpm_present()` would also come up empty".

## Header `source:` line — partial (numbers drift from the registry)

- Header: "new anchors 18-26, 46-63, 109-271, 344-376, 696-708". Registry S351 (SOURCES.md, this round's edit,
  confirmed in the round-89 lesson's registry-change note): "18-26 (URI_ERROR), 28-104 (…46-63 silent false…),
  109-243 (dispatchers…), 301-319, 344-366, 372-376, 403-487, 662-664, 696-710 (uri_open_optional)".
  18-26 is not new (r87 anchor, round-87 lesson Gate line 34), and 109-271 / 696-708 match nothing — no row
  cites past 243 or 710. Align the header with the registry.
- Cosmetic, same line: "read-only: `sudo -n grep` of `/boot/limine.conf`, `/sys/class/tpm/`, SecureBoot efivar"
  — only limine.conf was grepped; tpm was `ls`ed, efivar `od`ed, pacman unprivileged (S363's own wording is
  already exact).

## SOURCES.md — support

- S361/S362/S363 and edited S350/S351/S353: all six rows exactly 11 cells, no literal `|` inside a cell
  (mechanical check). All six quoted sha256 digests match the pinned bytes on disk (recomputed). Anchor text
  verified against code: S361 414-421/423-427/437/430-435 ✓; S362 18-29/70-86/87-100 ✓; S350 157-160
  (measured_boot) ✓; S351 anchor list ✓ (every named region found at the stated lines); S353 1719-1730 ✓.
  S363's receipt line mapping (3-10, 11-14, 15-16, 17-18) ✓ against the 18-line receipt.

## .json vs .md — support

- All 8 rows match field-for-field (statement, source, quote, host_value) — mechanical diff, 8/8.
- All 8 quotes ≤ 25 words (14, 5, 7, 9, 14, 20, 12, 1).

## Cross-checks that corroborate the entry's frame

- r88 lesson R88-R5 (round-88.md:122-124) names ReviewBattery F1 (boot(N) resolves) and F3 (URI-less path is an
  entry failure) — the entry's stated ground ✓ exists.
- round-89 lesson Gate: S361-S363 admitted with the same anchors/digests the registry carries ✓.
